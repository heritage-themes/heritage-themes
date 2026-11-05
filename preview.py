"""Writes the preview page of each theme family and, with --png, renders it to PNG.

Usage: python3 preview.py [--vscode | --visualstudio | --sublime | --zed | --nvim | --notepadpp | --xcode | --helix
                          | --kakoune | --micro | --vim | --emacs | --terminals | --nano | --amp | --textadept
                          | --lapce | --qtcreator | --eclipse] [--png] [THEME ...]
  THEME        a theme folder, for example shuimo; default: every theme folder
  --vscode     write the VS Code preview instead of the IntelliJ one; needs Node.js and npm
  --visualstudio  write the Visual Studio preview instead of the IntelliJ one; needs Windows and Visual Studio 2026
  --sublime    write the Sublime Text preview instead of the IntelliJ one; needs bat
  --zed        write the Zed preview instead of the IntelliJ one; needs a C compiler (cc)
  --nvim       write the Neovim preview instead of the IntelliJ one; needs Neovim and a C compiler (cc)
  --notepadpp  write the Notepad++ preview instead of the IntelliJ one; needs a C++ compiler (c++)
  --xcode      write the Xcode preview instead of the IntelliJ one; needs macOS and Xcode 27 or later, closed
  --helix      write the Helix preview instead of the IntelliJ one; needs Linux or macOS
  --kakoune    write the Kakoune preview instead of the IntelliJ one; needs Linux or macOS, and Kakoune
  --micro      write the Micro preview instead of the IntelliJ one; needs Linux or macOS, and Micro
  --vim        write the Vim preview instead of the IntelliJ one; needs Linux or macOS, and Vim
  --emacs      write the Emacs preview instead of the IntelliJ one; needs Linux or macOS, Emacs and a C compiler (cc)
  --terminals  write the terminals preview instead of the IntelliJ one; needs Linux, Podman and ImageMagick
  --nano       write the Nano preview instead of the IntelliJ one; needs Linux and Podman
  --amp        write the Amp preview instead of the IntelliJ one; needs Linux and Podman
  --textadept  write the Textadept preview instead of the IntelliJ one; needs Linux, Podman and ImageMagick
  --lapce      write the Lapce preview instead of the IntelliJ one; needs Linux, Podman and ImageMagick
  --qtcreator  write the Qt Creator preview instead of the IntelliJ one; needs Linux, Podman and ImageMagick
  --eclipse    write the Eclipse preview instead of the IntelliJ one; needs Linux, Podman and ImageMagick
  --png        also render the page to PNG; needs Google Chrome or Chromium, and ImageMagick

The IntelliJ page goes to themes/<theme>/build/preview.html and its PNG to themes/<theme>/preview.png, the
README image. The VS Code page goes to themes/<theme>/build/preview-vscode.html and its PNG next to it. The
VS Code page is coloured by Shiki, pinned in scripts/shiki and installed there with npm ci on first use.
The Sublime Text page goes to themes/<theme>/build/preview-sublime.html. bat tokenises the samples with the
.sublime-syntax files it bundles, which are Sublime Text's own for most languages, and colours them with the
generated scheme converted to a .tmTheme. The Zed page goes to themes/<theme>/build/preview-zed.html. It is coloured
by scripts/zed/tokens.py, which runs in a virtual environment that preview.py creates in scripts/zed/.venv from the
pinned requirements.txt, and keeps the grammars it compiles in ~/.cache/heritage-themes/zed. The Neovim page goes to
themes/<theme>/build/preview-nvim.html. It is drawn by Neovim itself through scripts/nvim/screen.py, which runs in
scripts/nvim/.venv in the same way and keeps nvim-treesitter and the grammars it compiles in
~/.cache/heritage-themes/nvim. The Notepad++ page goes to themes/<theme>/build/preview-notepadpp.html. It is coloured
by scripts/notepadpp/tokens.py, which compiles the lexers of the pinned Notepad++ source with c++ and keeps them in
~/.cache/heritage-themes/notepadpp. The Visual Studio page goes to themes/<theme>/build/preview-visualstudio.html,
with the captures it shows in themes/<theme>/build/visualstudio. scripts/visualstudio/screen.ps1 takes them in Visual
Studio 2026 itself, in an instance of its own with the family's themes installed. The Xcode page goes to
themes/<theme>/build/preview-xcode.html, with the captures it shows in themes/<theme>/build/xcode.
scripts/xcode/screen.py takes them in Xcode itself, which it runs with the family's themes while restoring Xcode's
settings afterwards; Xcode must be closed. The Helix, Kakoune, Micro, Vim and Emacs pages go to
themes/<theme>/build/preview-<editor>.html. They are drawn by the editor itself through scripts/terminal/screen.py,
which runs in scripts/terminal/.venv in the same way as the Zed one and keeps the pinned Helix release and the grammars
it builds for Emacs in ~/.cache/heritage-themes. The terminals page goes to themes/<theme>/build/preview-terminals.html,
with the screenshots it shows in themes/<theme>/build/terminals. It runs each terminal emulator, shell, prompt and
multiplexer that runs on Linux in the container image of scripts/terminals/Containerfile, which preview.py builds with
Podman, through scripts/terminals/shoot.py and shells.py, and fails when a screenshot lacks one of the theme's 16
colours (scripts/terminals/check.py) or a screen shows a colour the theme does not set or text below its contrast
minimum (scripts/terminals/cells.py). iTerm2, Windows Terminal and Termux do not run on Linux, so the build's checks
of their files are all they get. All pages use JetBrains Mono, downloaded once from the pinned release
below into ~/.cache/heritage-themes.
"""
import argparse, concurrent.futures, hashlib, json, os, pathlib, plistlib, re, shutil, subprocess, sys, tempfile
import urllib.request, zipfile

import heritage
from build import VERSION
from heritage.preview import (FONT_DIR, FONTS, SHIKI_BOLD, SHIKI_ITALIC, SHIKI_UNDERLINE, XCODE_COLUMN, page, plain,
                              terminals_page, vscode_samples)
from heritage.samples import SAMPLES, XCODE_SAMPLES
from heritage.sublime import resolve, scheme as sublime_scheme
from heritage.vscode import theme as vscode_theme
from heritage.zed import theme as zed_theme

ROOT = os.path.dirname(os.path.abspath(__file__))
SHIKI = os.path.join(ROOT, "scripts", "shiki")
ZED = os.path.join(ROOT, "scripts", "zed")
NVIM = os.path.join(ROOT, "scripts", "nvim")
TERMINAL = os.path.join(ROOT, "scripts", "terminal")
NOTEPADPP = os.path.join(ROOT, "scripts", "notepadpp")
VISUALSTUDIO = os.path.join(ROOT, "scripts", "visualstudio")
XCODE = os.path.join(ROOT, "scripts", "xcode")
TERMINALS = os.path.join(ROOT, "scripts", "terminals")
EDITORS = os.path.join(ROOT, "scripts", "editors")
EDITORS_IMAGE = "localhost/heritage-editors"
# The names that pyte gives the terminal's 16 colours, in order.
ANSI_NAMES = ("black", "red", "green", "brown", "blue", "magenta", "cyan", "white", "brightblack", "brightred",
              "brightgreen", "brightbrown", "brightblue", "brightmagenta", "brightcyan", "brightwhite")
TERMINALS_IMAGE = "localhost/heritage-terminals"
# The terminal emulators that shoot.py screenshots, and the shells, prompts and multiplexers whose screens shells.py
# reads, with the Powerlevel10k style and the rows that the check covers, all when None.
TERMINALS_SHOTS = ("kitty", "alacritty", "wezterm", "ghostty", "foot", "konsole", "terminator", "xterm", "st", "rio",
                   "contour", "warp", "tabby", "hyper")
TERMINALS_SCREENS = (("fish", None, None), ("zsh", None, None), ("nushell", None, None), ("powershell", None, None),
                     ("starship", None, None), ("oh_my_posh", None, None), ("powerlevel10k", "lean", None),
                     ("powerlevel10k", "classic", None), ("powerlevel10k", "rainbow", None), ("tmux", None, None),
                     ("zellij", None, None))
VISUALSTUDIO_ID = "heritage-themes-preview"  # the identity of the VSIX that the preview installs
FONT_URL = "https://github.com/JetBrains/JetBrainsMono/releases/download/v2.304/JetBrainsMono-2.304.zip"
FONT_SHA256 = "6f6376c6ed2960ea8a963cd7387ec9d76e3f629125bc33d1fdcd7eb7012f7bbf"
# The icons and powerline separators that prompts and multiplexers draw, for the terminals page, as a terminal draws
# them with a Nerd Font.
SYMBOLS_URL = "https://github.com/ryanoasis/nerd-fonts/releases/download/v3.5.1/NerdFontsSymbolsOnly.zip"
SYMBOLS_SHA256 = "fdca3682534f6f65e1ccb2345b0362ccf67d9b8eca7c8025330946e93e2473bc"
SYMBOLS_FONT = "SymbolsNerdFontMono-Regular.ttf"
CACHE = os.path.join(os.environ.get("XDG_CACHE_HOME") or os.path.expanduser("~/.cache"), "heritage-themes")
CHROMES = ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser")
# Screenshot geometry in CSS pixels. HEIGHT only has to exceed the page; the PNG is trimmed to the windows.
WIDTH, HEIGHT, SCALE, MARGIN = 1328, 12000, 2, 24


def font_archive(url=FONT_URL, sha256=FONT_SHA256, name="JetBrains Mono"):
    """The path of a font archive in CACHE, downloaded from url on first use and checked against sha256."""
    path = os.path.join(CACHE, os.path.basename(url))
    if not os.path.isfile(path):
        os.makedirs(CACHE, exist_ok=True)
        try:
            with urllib.request.urlopen(url) as response, open(path + ".part", "wb") as f:
                shutil.copyfileobj(response, f)
        except OSError as e:
            raise SystemExit(f"preview: cannot download {name} from {url}: {e}")
        os.replace(path + ".part", path)
    with open(path, "rb") as f:
        if hashlib.sha256(f.read()).hexdigest() != sha256:
            os.remove(path)
            raise SystemExit(f"preview: {url} does not match its SHA-256; the cached copy was removed")
    return path


def install_fonts(dest, symbols=False):
    """Copies JetBrains Mono into dest and, with symbols, the Symbols Nerd Font that prompts draw icons with."""
    os.makedirs(dest, exist_ok=True)
    with zipfile.ZipFile(font_archive()) as z:
        for name, _, _ in FONTS:
            with z.open(f"fonts/webfonts/JetBrainsMono-{name}.woff2") as src, \
                    open(os.path.join(dest, f"JetBrainsMono-{name}.woff2"), "wb") as out:
                shutil.copyfileobj(src, out)
    if symbols:
        with zipfile.ZipFile(font_archive(SYMBOLS_URL, SYMBOLS_SHA256, "Symbols Nerd Font")) as z, \
                z.open(SYMBOLS_FONT) as src, open(os.path.join(dest, SYMBOLS_FONT), "wb") as out:
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


def venv_python(folder, module):
    """The Python of folder/.venv, created with folder/requirements.txt installed when module does not import."""
    venv = os.path.join(folder, ".venv")
    python = os.path.join(venv, "Scripts" if os.name == "nt" else "bin", "python")
    if not os.path.isfile(python):
        subprocess.run([sys.executable, "-m", "venv", venv], check=True)
    if subprocess.run([python, "-c", f"import {module}"], capture_output=True).returncode:
        subprocess.run([python, "-m", "pip", "install", "--quiet", "--disable-pip-version-check", "-r",
                        os.path.join(folder, "requirements.txt")], check=True)
    return python


def zed_tokens(family):
    """Per theme of the family, the samples coloured by scripts/zed/tokens.py with its Zed theme, in the shape that
    vscode_tokens returns."""
    tool("cc")
    python = venv_python(ZED, "tree_sitter")
    request = dict(themes=[zed_theme(t["palette"]) for t in family.THEMES],
                   samples=[dict(suffix=name.rsplit(".", 1)[1], code=plain(code)) for name, _, code in SAMPLES])
    result = subprocess.run([python, "-I", os.path.join(ZED, "tokens.py"), os.path.join(CACHE, "zed")],
                            input=json.dumps(request), capture_output=True, text=True, encoding="utf-8")
    if result.returncode:
        raise SystemExit(f"preview: tokens.py failed:\n{result.stderr}")
    return json.loads(result.stdout)


def nvim_tokens(family):
    """Per theme of the family, the samples as Neovim draws them with its colour scheme, through scripts/nvim/screen.py,
    in the shape that vscode_tokens returns."""
    tool("cc")
    tool("nvim")
    python = venv_python(NVIM, "msgpack")
    with tempfile.TemporaryDirectory() as plugin:
        os.makedirs(os.path.join(plugin, "colors"))
        for t in family.THEMES:
            scheme = heritage.nvim.name(t)
            with open(os.path.join(plugin, "colors", f"{scheme}.lua"), "w", encoding="utf-8", newline="\n") as f:
                f.write(heritage.nvim.colorscheme(t["palette"], scheme, f"themes/{heritage.folder(family)}"))
        request = dict(schemes=[heritage.nvim.name(t) for t in family.THEMES],
                       samples=[dict(name=name, code=plain(code)) for name, _, code in SAMPLES])
        result = subprocess.run([python, "-I", os.path.join(NVIM, "screen.py"), os.path.join(CACHE, "nvim"), plugin],
                                input=json.dumps(request), capture_output=True, text=True, encoding="utf-8")
    if result.returncode:
        raise SystemExit(f"preview: screen.py failed:\n{result.stderr}")
    return json.loads(result.stdout)


# Terminal editor → its theme file for a theme dict of a theme.py and the URL of its folder, as (name, file name, text).
TERMINAL_THEMES = {
    "helix": lambda t, source: (heritage.helix.name(t), f"{heritage.helix.name(t)}.toml",
                                heritage.helix.theme(t["palette"], source)),
    "kakoune": lambda t, source: (heritage.kakoune.name(t), f"{heritage.kakoune.name(t)}.kak",
                                  heritage.kakoune.colorscheme(t["palette"], source)),
    "micro": lambda t, source: (heritage.micro.name(t), f"{heritage.micro.name(t)}.micro",
                                heritage.micro.colorscheme(t["palette"], source)),
    "vim": lambda t, source: (heritage.vim.name(t), f"{heritage.vim.name(t)}.vim",
                              heritage.vim.colorscheme(t["palette"], heritage.vim.name(t), source)),
    "emacs": lambda t, source: (heritage.emacs.name(t), f"{heritage.emacs.name(t)}-theme.el",
                                heritage.emacs.theme(t["palette"], heritage.emacs.name(t), source, source)),
}


def terminal_tokens(family, editor):
    """Per theme of the family, the samples as a terminal editor draws them with its theme, through
    scripts/terminal/screen.py, in the shape that vscode_tokens returns."""
    if os.name == "nt":
        raise SystemExit(f"preview: --{editor} needs Linux or macOS")
    python = venv_python(TERMINAL, "pyte")
    names = []
    with tempfile.TemporaryDirectory() as themes:
        for t in family.THEMES:
            name, filename, text = TERMINAL_THEMES[editor](t, f"themes/{heritage.folder(family)}")
            names.append(name)
            with open(os.path.join(themes, filename), "w", encoding="utf-8", newline="\n") as f:
                f.write(text)
        request = dict(themes=names, samples=[dict(name=name, code=plain(code)) for name, _, code in SAMPLES])
        result = subprocess.run([python, "-I", os.path.join(TERMINAL, "screen.py"), editor, CACHE, themes],
                                input=json.dumps(request), capture_output=True, text=True, encoding="utf-8")
    if result.returncode:
        raise SystemExit(f"preview: screen.py failed:\n{result.stderr}")
    return json.loads(result.stdout)


def notepadpp_tokens(family):
    """Per theme of the family, the samples coloured by scripts/notepadpp/tokens.py with its Notepad++ theme, in the
    shape that vscode_tokens returns."""
    tool("c++")
    request = dict(themes=[heritage.notepadpp.theme(t["palette"], f"themes/{heritage.folder(family)}")
                           for t in family.THEMES],
                   samples=[dict(suffix=name.rsplit(".", 1)[1], code=plain(code)) for name, _, code in SAMPLES])
    command = [sys.executable, "-I", os.path.join(NOTEPADPP, "tokens.py"), os.path.join(CACHE, "notepadpp")]
    result = subprocess.run(command, input=json.dumps(request), capture_output=True, text=True, encoding="utf-8")
    if result.returncode:
        raise SystemExit(f"preview: tokens.py failed:\n{result.stderr}")
    return json.loads(result.stdout)


def png_size(path):
    """(width, height) of a PNG, from its IHDR chunk."""
    with open(path, "rb") as f:
        header = f.read(24)
    return int.from_bytes(header[16:20], "big"), int.from_bytes(header[20:24], "big")


def visualstudio_captures(family, out):
    """Per theme of the family, the samples as Visual Studio 2026 draws them, captured by
    scripts/visualstudio/screen.ps1 into out/visualstudio: per sample, the capture's path relative to out, width and
    height."""
    if os.name != "nt":
        raise SystemExit("preview: --visualstudio needs Windows and Visual Studio 2026")
    captures = os.path.join(out, "visualstudio")
    shutil.rmtree(captures, ignore_errors=True)
    ids = [heritage.visualstudio.setting_id(t["palette"]["name"]) for t in family.THEMES]
    with tempfile.TemporaryDirectory() as tmp:
        samples, package = os.path.join(tmp, "samples"), os.path.join(tmp, "package")
        os.makedirs(samples)
        for name, _, code in SAMPLES:
            with open(os.path.join(samples, name), "w", encoding="utf-8", newline="\n") as f:
                f.write(plain(code) + "\n")
        themes = [(t["slug"], t["id"], t["palette"], f"themes/{heritage.folder(family)}") for t in family.THEMES]
        heritage.visualstudio.package(package, VISUALSTUDIO_ID, "1.0.0", "Heritage Themes Preview",
                                      f"The {family.FAMILY} themes, for preview.py.", themes)
        vsix = heritage.visualstudio.pack(package, os.path.join(tmp, "preview.vsix"), zipfile.ZipInfo)
        result = subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File",
                                 os.path.join(VISUALSTUDIO, "screen.ps1"), "-Vsix", vsix, "-Id", VISUALSTUDIO_ID,
                                 "-Themes", ",".join(ids), "-Samples", samples, "-Out", captures],
                                capture_output=True, text=True, encoding="utf-8")
    if result.returncode:
        raise SystemExit(f"preview: screen.ps1 failed:\n{result.stderr or result.stdout}")
    # Visual Studio draws the samples at twice the default font size, so each capture shows at half its size.
    return [[(f"visualstudio/{i}/{name}.png", *png_size(os.path.join(captures, i, f"{name}.png")), 2)
             for name, _, _ in SAMPLES] for i in ids]


def xcode_captures(family, out):
    """Per theme of the family, the samples of XCODE_SAMPLES as Xcode draws them, captured by scripts/xcode/screen.py
    into out/xcode: per sample, the capture's path relative to out, width and height in pixels, and pixels per
    point."""
    if sys.platform != "darwin":
        raise SystemExit("preview: --xcode needs macOS and Xcode 27 or later")
    captures = os.path.join(out, "xcode")
    shutil.rmtree(captures, ignore_errors=True)
    names = [t["palette"]["name"] for t in family.THEMES]
    with tempfile.TemporaryDirectory() as tmp:
        themes, samples = os.path.join(tmp, "themes"), os.path.join(tmp, "samples")
        os.makedirs(themes)
        os.makedirs(samples)
        for t in family.THEMES:
            with open(os.path.join(themes, f"{t['palette']['name']}.xcworkspacecolortheme"), "wb") as f:
                f.write(heritage.xcode.recipe_document(t["palette"]))
        for name, _, code in XCODE_SAMPLES:
            with open(os.path.join(samples, name), "w", encoding="utf-8", newline="\n") as f:
                f.write(plain(code) + "\n")
        request = [dict(name=t["palette"]["name"], background=t["palette"]["bg"], line=t["palette"]["caretRow"])
                   for t in family.THEMES]
        result = subprocess.run([sys.executable, "-I", os.path.join(XCODE, "screen.py"), os.path.join(CACHE, "xcode"),
                                 themes, samples, captures, str(XCODE_COLUMN), json.dumps(request)],
                                capture_output=True, text=True, encoding="utf-8")
    if result.returncode:
        raise SystemExit(f"preview: screen.py failed:\n{result.stderr or result.stdout}")
    scales = json.loads(result.stdout)
    return [[(f"xcode/{name}/{sample}.png", *png_size(os.path.join(captures, name, f"{sample}.png")),
              scales[name][sample]) for sample, _, _ in XCODE_SAMPLES] for name in names]


def terminals_results(family, out):
    """Per theme of the family, (app, screenshot path relative to out, screen rows) per app that runs on Linux: the
    terminal emulators' windows in out/terminals, the other apps' screens. Fails when a check finds a problem."""
    if not sys.platform.startswith("linux"):
        raise SystemExit("preview: --terminals needs Linux")
    podman = tool("podman")
    subprocess.run([podman, "build", "-q", "-t", TERMINALS_IMAGE, TERMINALS], check=True, capture_output=True)
    shots = os.path.join(out, "terminals")
    shutil.rmtree(shots, ignore_errors=True)
    modules = {m.__name__.rsplit(".", 1)[1]: m for m in heritage.terminals.modules()}
    with tempfile.TemporaryDirectory() as tmp:
        generated, screens = os.path.join(tmp, "generated"), os.path.join(tmp, "screens")
        os.makedirs(screens)
        for module in modules.values():
            files = [entry for t in family.THEMES for entry in module.files(t, "")]
            files += module.combined(family.THEMES, "") if hasattr(module, "combined") else []
            for filename, text in files:
                path = os.path.join(generated, module.FOLDER, filename)
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, "w", encoding="utf-8", newline="\n") as f:
                    f.write(text)
        def container(output, *command):
            """Runs a command in the image with the scripts, the generated files and output mounted."""
            return subprocess.run([podman, "run", "--rm", "--userns=keep-id", "--shm-size=1g",
                                   "--security-opt", "label=disable", "-v", f"{TERMINALS}:/work:ro",
                                   "-v", f"{generated}:/gen:ro", "-v", f"{output}:/out", TERMINALS_IMAGE, *command],
                                  capture_output=True, text=True)
        def shot(t, app):
            p, stem = t["palette"], heritage.terminals.name(t)
            folder = os.path.join(shots, stem)
            os.makedirs(folder, exist_ok=True)
            run = container(folder, "python3", "/work/shoot.py", app, f"{stem}\t{p['name']}",
                            f"/gen/{modules[app].FOLDER}", f"/out/{app}.png")
            if run.returncode:
                return modules[app].APP, None, None, [f"{app} failed: {run.stderr.strip()[-400:]}"]
            check = subprocess.run([sys.executable, "-I", os.path.join(TERMINALS, "check.py"),
                                    *(["--display-p3"] if app == "rio" else []), os.path.join(folder, f"{app}.png"),
                                    "#" + p["bg"], *heritage.terminals.colours(p)["ansi"]],
                                   capture_output=True, text=True)
            os.remove(os.path.join(folder, f"{app}.png.log"))
            return modules[app].APP, f"terminals/{stem}/{app}.png", None, check.stdout.splitlines()
        def screen(t, app, variant, rows):
            p, stem = t["palette"], heritage.terminals.name(t)
            name = f"{app}-{variant}-{stem}" if variant else f"{app}-{stem}"
            run = container(screens, "python3", "/work/shells.py", app, stem, f"/gen/{modules[app].FOLDER}",
                            f"/out/{name}.json", *([variant] if variant else []))
            label = modules[app].APP + (f" ({variant})" if variant else "")
            if run.returncode:
                return label, None, None, [f"{label} failed: {run.stderr.strip()[-400:]}"]
            colours = ",".join("#" + v for v in p.values() if isinstance(v, str) and re.fullmatch(r"[0-9A-F]{6}", v))
            check = subprocess.run([sys.executable, "-I", os.path.join(TERMINALS, "cells.py"),
                                    os.path.join(screens, f"{name}.json"), "#" + p["bg"], "#" + p["fg"], colours,
                                    "#" + p["comment"], *([rows] if rows else [])], capture_output=True, text=True)
            with open(os.path.join(screens, f"{name}.json"), encoding="utf-8") as f:
                return label, None, json.load(f), check.stdout.splitlines()
        with concurrent.futures.ThreadPoolExecutor(4) as pool:
            jobs = [[pool.submit(shot, t, app) for app in TERMINALS_SHOTS]
                    + [pool.submit(screen, t, *entry) for entry in TERMINALS_SCREENS] for t in family.THEMES]
            results = [[job.result() for job in theme_jobs] for theme_jobs in jobs]
    problems = [problem for theme_results in results for *_, found in theme_results for problem in found]
    if problems:
        raise SystemExit("preview: the terminals show problems:\n" + "\n".join(problems))
    return [[(app, image, rows) for app, image, rows, _ in theme_results] for theme_results in results]


# Terminal editors that scripts/editors/screen.py runs: (title, the (path, text) of the files of a family's themes,
# the colours that a theme's own settings show besides the palette's, the rows that the check covers).
SCREEN_EDITORS = {
    # Nano: the title bar, status bar and help lines that the scheme colours; code takes the colours that nano's syntax
    # files name, among them nano's own extended colours
    "nano": ("Nano", lambda themes: [(f"{heritage.nano.name(t)}.nanorc", heritage.nano.colorscheme(t["palette"], ""))
                                     for t in themes],
             lambda p: {c for style in heritage.nano.styles(p).values() for c in style.values()}, "0,-3,-2,-1"),
    # Amp: every row but the status bar, where Amp draws its modes in colours of its own
    "amp": ("Amp", lambda themes: [(f"{heritage.amp.name(t)}.tmTheme", heritage.amp.theme(t["palette"], ""))
                                   for t in themes], lambda p: set(), "0:-1"),
}


def screen_results(family, out, editor):
    """Per theme of the family, (sample, None, screen rows) per sample as a terminal editor draws it with the theme,
    in a terminal that runs the theme of the Terminals product: the terminal's named and default colours resolved to
    that theme's. Fails when the rows that the check covers show a colour that neither theme sets, or text below
    4.5:1, or 3:1 for comments."""
    if not sys.platform.startswith("linux"):
        raise SystemExit(f"preview: --{editor} needs Linux")
    title, theme_files, own_colours, checked_rows = SCREEN_EDITORS[editor]
    podman = tool("podman")
    subprocess.run([podman, "build", "-q", "-t", EDITORS_IMAGE, EDITORS], check=True, capture_output=True)
    results, problems = [], []
    with tempfile.TemporaryDirectory() as tmp:
        files, samples, screens = (os.path.join(tmp, name) for name in ("files", "samples", "screens"))
        for folder in (files, samples, screens):
            os.makedirs(folder)
        write_files(files, theme_files(family.THEMES))
        write_files(samples, [(name, plain(code) + "\n") for name, *_, code in SAMPLES])
        def screen(t, name):
            stem, p = heritage.nvim.name(t), t["palette"]
            target = f"{stem}-{name}.json"
            run = subprocess.run([podman, "run", "--rm", "--userns=keep-id", "--security-opt", "label=disable",
                                  "-v", f"{EDITORS}:/work:ro", "-v", f"{files}:/gen:ro", "-v", f"{samples}:/samples:ro",
                                  "-v", f"{screens}:/out", EDITORS_IMAGE, "python3", "/work/screen.py", editor, stem,
                                  "/gen", f"/samples/{name}", f"/out/{target}"], capture_output=True, text=True)
            if run.returncode:
                return name, None, None, [f"{editor} {stem} {name} failed: {run.stderr.strip()[-400:]}"]
            ansi = heritage.terminals.colours(p)["ansi"]
            with open(os.path.join(screens, target), encoding="utf-8") as f:
                rows = [[[char, *(ansi[ANSI_NAMES.index(c)] if c in ANSI_NAMES else c for c in (fg, bg)), *rest]
                         for char, fg, bg, *rest in row] for row in json.load(f)]
            checked = os.path.join(screens, f"checked-{target}")
            with open(checked, "w", encoding="utf-8") as f:
                json.dump(rows, f)
            colours = {"#" + v for v in p.values() if isinstance(v, str) and re.fullmatch(r"[0-9A-F]{6}", v)}
            colours |= set(ansi) | own_colours(p)
            check = subprocess.run([sys.executable, "-I", os.path.join(TERMINALS, "cells.py"), checked, "#" + p["bg"],
                                    "#" + p["fg"], ",".join(sorted(colours)), "#" + p["comment"], checked_rows],
                                   capture_output=True, text=True)
            return name, None, rows, [f"{editor} {stem} {name}: {line.split(': ', 1)[1]}"
                                      for line in check.stdout.splitlines()]
        with concurrent.futures.ThreadPoolExecutor(4) as pool:
            jobs = [[pool.submit(screen, t, name) for name, *_ in SAMPLES] for t in family.THEMES]
            for theme_jobs in jobs:
                theme_results = [job.result() for job in theme_jobs]
                problems += [problem for *_, found in theme_results for problem in found]
                results.append([(name, image, rows) for name, image, rows, _ in theme_results])
    if problems:
        raise SystemExit(f"preview: {title} shows problems:\n" + "\n".join(problems))
    return results


def write_files(folder, files):
    """Writes (path relative to folder, text) pairs under folder."""
    for name, text in files:
        path = os.path.join(folder, name)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)


# GUI editors that scripts/editors/shoot.py runs: (title, module, the (path, text) of the files of a family's themes,
# as the editor's README has them installed).
GUI_EDITORS = {
    "textadept": ("Textadept", heritage.textadept,
                  lambda themes: [(f"{heritage.textadept.name(t)}.lua", heritage.textadept.theme(t["palette"], ""))
                                  for t in themes]),
    "lapce": ("Lapce", heritage.lapce,
              lambda themes: [("heritage-themes/volt.toml", heritage.lapce.volt(themes, "preview", ""))]
              + [(f"heritage-themes/themes/{heritage.lapce.name(t)}.toml", heritage.lapce.theme(t["palette"], ""))
                 for t in themes]),
    "qtcreator": ("Qt Creator", heritage.qtcreator,
                  lambda themes: [(f"themes/{heritage.qtcreator.name(t)}.creatortheme", heritage.qtcreator.theme(t, ""))
                                  for t in themes]
                  + [(f"styles/{heritage.qtcreator.name(t)}.xml", heritage.qtcreator.scheme(t, "")) for t in themes]),
    "eclipse": ("Eclipse", heritage.eclipse,
                lambda themes: [("eclipse-theme-ids.txt", heritage.eclipse.theme_ids(themes))]),
}
# Files that a GUI editor's preview writes as bytes: the Eclipse plugin, a jar.
GUI_BINARIES = {"eclipse": lambda themes: [(f"eclipse/{heritage.eclipse.BUNDLE}.jar", heritage.eclipse.jar(themes, VERSION,
                                                                                                          "Heritage Themes", ""))]}
# The roles whose colours must show in at least one sample of a GUI editor.
GUI_ROLES = ("keyword", "string", "comment", "number", "type")


def gui_results(family, out, editor):
    """Per theme of the family, (sample, screenshot path relative to out, None) per sample as a GUI editor draws it
    with the theme, in out/<editor>. Fails when a screenshot shows a colour that is no colour of the theme nor a blend
    of one with a background (scripts/editors/pixels.py), or a role of GUI_ROLES shows in no sample."""
    if not sys.platform.startswith("linux"):
        raise SystemExit(f"preview: --{editor} needs Linux")
    title, module, theme_files = GUI_EDITORS[editor]
    podman = tool("podman")
    subprocess.run([podman, "build", "-q", "-t", EDITORS_IMAGE, EDITORS], check=True, capture_output=True)
    shots = os.path.join(out, editor)
    shutil.rmtree(shots, ignore_errors=True)
    results, problems = [], []
    with tempfile.TemporaryDirectory() as tmp:
        files, samples = os.path.join(tmp, "files"), os.path.join(tmp, "samples")
        os.makedirs(files)
        os.makedirs(samples)
        write_files(files, theme_files(family.THEMES))
        for path, data in GUI_BINARIES.get(editor, lambda themes: [])(family.THEMES):
            os.makedirs(os.path.dirname(os.path.join(files, path)), exist_ok=True)
            with open(os.path.join(files, path), "wb") as f:
                f.write(data)
        write_files(files, [(f"{heritage.nvim.name(t)}.pixels.json", json.dumps(module.pixel_palette(t["palette"])))
                            for t in family.THEMES])
        for name, *_, code in SAMPLES:
            with open(os.path.join(samples, name), "w", encoding="utf-8", newline="\n") as f:
                f.write(plain(code) + "\n")
        def shot(t, name):
            stem = heritage.nvim.name(t)
            folder = os.path.join(shots, stem)
            os.makedirs(folder, exist_ok=True)
            # without network access, as no editor needs it and Eclipse would show announcements it downloads
            run = subprocess.run([podman, "run", "--rm", "--network=none", "--userns=keep-id", "--shm-size=1g",
                                  "--security-opt", "label=disable", "-v", f"{EDITORS}:/work:ro", "-v", f"{files}:/gen:ro",
                                  "-v", f"{samples}:/samples:ro", "-v", f"{folder}:/out", EDITORS_IMAGE, "python3",
                                  "/work/shoot.py", editor, stem, "/gen", f"/samples/{name}", f"/out/{name}.png"],
                                 capture_output=True, text=True)
            if run.returncode:
                return name, None, [f"{editor} {stem} {name} failed: {run.stderr.strip()[-400:]}"], []
            os.remove(os.path.join(folder, f"{name}.png.log"))
            check = subprocess.run([sys.executable, "-I", os.path.join(EDITORS, "pixels.py"),
                                    os.path.join(folder, f"{name}.png"),
                                    os.path.join(files, f"{stem}.pixels.json")], capture_output=True, text=True)
            report = json.loads(check.stdout)
            return (name, f"{editor}/{stem}/{name}.png", [f"{editor} {stem} {name}: {problem}"
                                                          for problem in report["problems"]], report["present"])
        with concurrent.futures.ThreadPoolExecutor(4) as pool:
            jobs = [[pool.submit(shot, t, name) for name, *_ in SAMPLES] for t in family.THEMES]
            for t, theme_jobs in zip(family.THEMES, jobs):
                theme_results = [job.result() for job in theme_jobs]
                problems += [problem for _, _, found, _ in theme_results for problem in found]
                present = {colour for *_, colours in theme_results for colour in colours}
                problems += [f"{editor} {heritage.nvim.name(t)}: the {role} colour shows in no sample"
                             for role in GUI_ROLES if "#" + t["palette"][role] not in present]
                results.append([(name, image, None) for name, image, _, _ in theme_results])
    if problems:
        raise SystemExit(f"preview: {title} shows problems:\n" + "\n".join(problems))
    return results


def render_png(page_path, png_path):
    chrome = os.environ.get("CHROME") or tool(*CHROMES)
    # Windows has a convert command of its own, which converts file systems, so ImageMagick 6's name is not looked up.
    magick = tool("magick") if os.name == "nt" else tool("magick", "convert")
    with tempfile.TemporaryDirectory() as tmp:
        shot = os.path.join(tmp, "shot.png")
        subprocess.run([chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                        f"--force-device-scale-factor={SCALE}", "--default-background-color=00000000",
                        f"--window-size={WIDTH},{HEIGHT}", f"--screenshot={shot}", pathlib.Path(page_path).as_uri()],
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
    kind.add_argument("--visualstudio", action="store_true", help="write the Visual Studio preview")
    kind.add_argument("--sublime", action="store_true", help="write the Sublime Text preview")
    kind.add_argument("--zed", action="store_true", help="write the Zed preview")
    kind.add_argument("--nvim", action="store_true", help="write the Neovim preview")
    kind.add_argument("--notepadpp", action="store_true", help="write the Notepad++ preview")
    kind.add_argument("--xcode", action="store_true", help="write the Xcode preview")
    for editor, title in (("helix", "Helix"), ("kakoune", "Kakoune"), ("micro", "Micro"), ("vim", "Vim"),
                          ("emacs", "Emacs")):
        kind.add_argument(f"--{editor}", action="store_true", help=f"write the {title} preview")
    kind.add_argument("--terminals", action="store_true", help="write the terminals preview")
    for editor, (title, *_) in SCREEN_EDITORS.items():
        kind.add_argument(f"--{editor}", action="store_true", help=f"write the {title} preview")
    for editor, (title, *_) in GUI_EDITORS.items():
        kind.add_argument(f"--{editor}", action="store_true", help=f"write the {title} preview")
    parser.add_argument("--png", action="store_true", help="also render the page to PNG")
    parser.add_argument("themes", nargs="*", metavar="THEME", help="theme folders; default: all")
    args = parser.parse_args()
    families = {heritage.folder(f): f for f in heritage.load_families()}
    unknown = set(args.themes) - set(families)
    if unknown:
        raise SystemExit(f"preview: no theme folder named {', '.join(sorted(unknown))}")
    for name in args.themes or families:
        out = os.path.join(heritage.THEMES, name, "build")
        install_fonts(os.path.join(out, FONT_DIR), symbols=args.terminals)
        family = families[name]
        target = next((name for name in ("vscode", "visualstudio", "sublime", "zed", "nvim", "notepadpp", "xcode",
                                          *TERMINAL_THEMES, "terminals", *SCREEN_EDITORS, *GUI_EDITORS)
                       if getattr(args, name)), None)
        page_path = os.path.join(out, f"preview-{target}.html" if target else "preview.html")
        tokens = {"vscode": vscode_tokens, "sublime": sublime_tokens, "zed": zed_tokens, "nvim": nvim_tokens,
                  "notepadpp": notepadpp_tokens,
                  **{editor: lambda f, e=editor: terminal_tokens(f, e) for editor in TERMINAL_THEMES},
                  "visualstudio": lambda f: visualstudio_captures(f, out),
                  "xcode": lambda f: xcode_captures(f, out)}.get(target, lambda family: None)(family)
        with open(page_path, "w", encoding="utf-8") as f:
            f.write(terminals_page(family, terminals_results(family, out)) if target == "terminals"
                    else terminals_page(family, screen_results(family, out, target), SCREEN_EDITORS[target][0],
                                        wide=False) if target in SCREEN_EDITORS
                    else terminals_page(family, gui_results(family, out, target), GUI_EDITORS[target][0])
                    if target in GUI_EDITORS
                    else page(family, tokens, target))
        print(page_path)
        if args.png:
            png_path = (os.path.join(out, f"preview-{target}.png") if target
                        else os.path.join(heritage.THEMES, name, "preview.png"))
            render_png(page_path, png_path)
            print(png_path)


if __name__ == "__main__":
    sys.exit(main())
