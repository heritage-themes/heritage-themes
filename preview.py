"""Writes the preview page of each theme family and, with --png, renders it to PNG.

Usage: python3 preview.py [--vscode | --sublime] [--png] [THEME ...]
  THEME      a theme folder, for example shuimo; default: every theme folder
  --vscode   write the VS Code preview instead of the IntelliJ one; needs Node.js and npm
  --sublime  write the Sublime Text preview instead of the IntelliJ one; needs bat
  --png      also render the page to PNG; needs Google Chrome or Chromium, and ImageMagick

The IntelliJ page goes to themes/<theme>/build/preview.html and its PNG to themes/<theme>/preview.png, the
README image. The VS Code page goes to themes/<theme>/build/preview-vscode.html and its PNG next to it. The
VS Code page is coloured by Shiki, pinned in scripts/shiki and installed there with npm ci on first use.
The Sublime Text page goes to themes/<theme>/build/preview-sublime.html. bat tokenises the samples with the
.sublime-syntax files it bundles, which are Sublime Text's own for most languages, and colours them with the
generated scheme converted to a .tmTheme. All pages use JetBrains Mono, downloaded once from the pinned release
below into ~/.cache/heritage-themes.
"""
import argparse, hashlib, json, os, plistlib, re, shutil, subprocess, sys, tempfile, urllib.request, zipfile

import heritage
from heritage.preview import FONT_DIR, FONTS, SHIKI_BOLD, SHIKI_ITALIC, SHIKI_UNDERLINE, page, plain, vscode_samples
from heritage.samples import SAMPLES
from heritage.sublime import resolve, scheme as sublime_scheme
from heritage.vscode import theme as vscode_theme

ROOT = os.path.dirname(os.path.abspath(__file__))
SHIKI = os.path.join(ROOT, "scripts", "shiki")
FONT_URL = "https://github.com/JetBrains/JetBrainsMono/releases/download/v2.304/JetBrainsMono-2.304.zip"
FONT_SHA256 = "6f6376c6ed2960ea8a963cd7387ec9d76e3f629125bc33d1fdcd7eb7012f7bbf"
CACHE = os.path.join(os.environ.get("XDG_CACHE_HOME") or os.path.expanduser("~/.cache"), "heritage-themes")
CHROMES = ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser")
# Screenshot geometry in CSS pixels. HEIGHT only has to exceed the page; the PNG is trimmed to the windows.
WIDTH, HEIGHT, SCALE, MARGIN = 1328, 12000, 2, 24


def font_archive():
    path = os.path.join(CACHE, os.path.basename(FONT_URL))
    if not os.path.isfile(path):
        os.makedirs(CACHE, exist_ok=True)
        try:
            with urllib.request.urlopen(FONT_URL) as response, open(path + ".part", "wb") as f:
                shutil.copyfileobj(response, f)
        except OSError as e:
            raise SystemExit(f"preview: cannot download JetBrains Mono from {FONT_URL}: {e}")
        os.replace(path + ".part", path)
    with open(path, "rb") as f:
        if hashlib.sha256(f.read()).hexdigest() != FONT_SHA256:
            os.remove(path)
            raise SystemExit(f"preview: {FONT_URL} does not match FONT_SHA256; the cached copy was removed")
    return path


def install_fonts(dest):
    os.makedirs(dest, exist_ok=True)
    with zipfile.ZipFile(font_archive()) as z:
        for name, _, _ in FONTS:
            with z.open(f"fonts/webfonts/JetBrainsMono-{name}.woff2") as src, \
                    open(os.path.join(dest, f"JetBrainsMono-{name}.woff2"), "wb") as out:
                shutil.copyfileobj(src, out)


def tool(*names):
    for name in names:
        if shutil.which(name):
            return name
    raise SystemExit(f"preview: needs one of: {', '.join(names)}")


def vscode_tokens(family):
    """Per theme of the family, the samples tokenised by scripts/shiki/tokens.mjs with its VS Code theme."""
    node = tool("node")
    if not os.path.isdir(os.path.join(SHIKI, "node_modules")):
        subprocess.run([tool("npm"), "ci", "--no-audit", "--no-fund"], cwd=SHIKI, check=True)
    request = dict(themes=[vscode_theme(t["palette"]) for t in family.THEMES], samples=vscode_samples())
    result = subprocess.run([node, os.path.join(SHIKI, "tokens.mjs")], input=json.dumps(request),
                            capture_output=True, text=True, encoding="utf-8")
    if result.returncode:
        raise SystemExit(f"preview: tokens.mjs failed:\n{result.stderr}")
    return json.loads(result.stdout)


def tmtheme(scheme):
    """The .tmTheme for a Sublime Text colour scheme, which bat reads: the scheme's colours with its variables
    resolved, and its rules with the scopes and font styles as they are."""
    globals_ = scheme["globals"]
    settings = {"background": globals_["background"], "foreground": globals_["foreground"],
                "caret": globals_["caret"], "lineHighlight": globals_["line_highlight"],
                "selection": globals_["selection"]}
    rules = [{"scope": rule["scope"], "settings": {"foreground": rule["foreground"],
                                                    "fontStyle": rule.get("font_style", "")}}
             for rule in scheme["rules"]]
    for entry in (settings, *(rule["settings"] for rule in rules)):
        for key, value in entry.items():
            if key != "fontStyle":
                entry[key] = resolve(value, scheme)
    return plistlib.dumps({"name": scheme["name"], "settings": [{"settings": settings}, *rules]})


SGR = re.compile(r"\x1b\[([0-9;]*)m")


def ansi_tokens(text):
    """Lines of [text, colour, font style] tokens from bat's 24-bit colour output."""
    colour, font, lines = None, 0, []
    for raw in text.split("\n"):
        line, pos = [], 0
        for m in [*SGR.finditer(raw), None]:
            chunk = raw[pos:m.start() if m else len(raw)]
            if chunk:
                line.append([chunk, colour, font])
            if not m:
                break
            pos, codes = m.end(), [int(c or 0) for c in m.group(1).split(";")]
            while codes:
                code = codes.pop(0)
                if code == 0:
                    colour, font = None, 0
                elif code == 1:
                    font |= SHIKI_BOLD
                elif code == 3:
                    font |= SHIKI_ITALIC
                elif code == 4:
                    font |= SHIKI_UNDERLINE
                elif code == 38 and codes[:1] == [2]:
                    colour = "#{:02X}{:02X}{:02X}".format(*codes[1:4])
                    del codes[:4]
        lines.append(line)
    return lines[:-1] if lines and not lines[-1] else lines


def sublime_tokens(family):
    """Per theme of the family, the samples tokenised by bat and coloured with the generated Sublime Text scheme,
    in the shape that vscode_tokens returns."""
    bat = tool("bat", "batcat")
    samples = [(name.rsplit(".", 1)[1], plain(code)) for name, _, code in SAMPLES]
    with tempfile.TemporaryDirectory() as tmp:
        config, cache = os.path.join(tmp, "config"), os.path.join(tmp, "cache")
        os.makedirs(os.path.join(config, "themes"))
        names = []
        for t in family.THEMES:
            names.append(t["palette"]["name"])
            with open(os.path.join(config, "themes", f"{names[-1]}.tmTheme"), "wb") as f:
                f.write(tmtheme(sublime_scheme(t["palette"])))
        env = dict(os.environ, BAT_CONFIG_DIR=config, BAT_CACHE_PATH=cache, COLORTERM="truecolor")
        env.pop("BAT_CONFIG_PATH", None)
        subprocess.run([bat, "cache", "--build"], env=env, check=True, capture_output=True)
        out = []
        for name in names:
            tokens = []
            for extension, code in samples:
                result = subprocess.run(
                    [bat, f"--theme={name}", f"--language={extension}", "--color=always", "--style=plain",
                     "--paging=never", "--wrap=never", "--italic-text=always"],
                    input=code, env=env, capture_output=True, text=True, encoding="utf-8")
                if result.returncode:
                    raise SystemExit(f"preview: bat failed on {extension}:\n{result.stderr}")
                tokens.append(ansi_tokens(result.stdout))
            out.append(tokens)
        return out


def render_png(page_path, png_path):
    chrome = os.environ.get("CHROME") or tool(*CHROMES)
    magick = tool("magick", "convert")
    with tempfile.TemporaryDirectory() as tmp:
        shot = os.path.join(tmp, "shot.png")
        subprocess.run([chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                        f"--force-device-scale-factor={SCALE}", "--default-background-color=00000000",
                        f"--window-size={WIDTH},{HEIGHT}", f"--screenshot={shot}", f"file://{page_path}"],
                       check=True, capture_output=True)
        box = subprocess.run([magick, shot, "-format", "%@", "info:"], check=True, capture_output=True, text=True)
        size, y = box.stdout.split("+")[0], int(box.stdout.split("+")[2])
        if y + int(size.split("x")[1]) >= HEIGHT * SCALE:
            raise SystemExit(f"preview: the page is taller than HEIGHT ({HEIGHT}px); raise HEIGHT in {__file__}")
        subprocess.run([magick, shot, "-trim", "+repage", "-bordercolor", "none", "-border", str(MARGIN * SCALE),
                        png_path], check=True)


def main():
    parser = argparse.ArgumentParser(description="Write theme previews.")
    kind = parser.add_mutually_exclusive_group()
    kind.add_argument("--vscode", action="store_true", help="write the VS Code preview")
    kind.add_argument("--sublime", action="store_true", help="write the Sublime Text preview")
    parser.add_argument("--png", action="store_true", help="also render the page to PNG")
    parser.add_argument("themes", nargs="*", metavar="THEME", help="theme folders; default: all")
    args = parser.parse_args()
    families = {heritage.folder(f): f for f in heritage.load_families()}
    unknown = set(args.themes) - set(families)
    if unknown:
        raise SystemExit(f"preview: no theme folder named {', '.join(sorted(unknown))}")
    for name in args.themes or families:
        out = os.path.join(heritage.THEMES, name, "build")
        install_fonts(os.path.join(out, FONT_DIR))
        family = families[name]
        target = "vscode" if args.vscode else "sublime" if args.sublime else None
        page_path = os.path.join(out, f"preview-{target}.html" if target else "preview.html")
        tokens = {"vscode": vscode_tokens, "sublime": sublime_tokens}.get(target, lambda family: None)(family)
        with open(page_path, "w", encoding="utf-8") as f:
            f.write(page(family, tokens, target))
        print(page_path)
        if args.png:
            png_path = (os.path.join(out, f"preview-{target}.png") if target
                        else os.path.join(heritage.THEMES, name, "preview.png"))
            render_png(page_path, png_path)
            print(png_path)


if __name__ == "__main__":
    sys.exit(main())
