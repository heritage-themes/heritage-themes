"""Writes the preview page of each theme family and, with --png, renders it to the README image.

Usage: python3 preview.py [--png] [THEME ...]
  THEME  a theme folder, for example shuimo; default: every theme folder
  --png  also render <theme>/preview.png; needs Google Chrome or Chromium, and ImageMagick

The page goes to <theme>/build/preview.html. It uses JetBrains Mono, downloaded once from the pinned
release below into ~/.cache/heritage-themes.
"""
import argparse, hashlib, os, shutil, subprocess, sys, tempfile, urllib.request, zipfile

import heritage
from heritage.preview import FONT_DIR, FONTS, page

ROOT = os.path.dirname(os.path.abspath(__file__))
FONT_URL = "https://github.com/JetBrains/JetBrainsMono/releases/download/v2.304/JetBrainsMono-2.304.zip"
FONT_SHA256 = "6f6376c6ed2960ea8a963cd7387ec9d76e3f629125bc33d1fdcd7eb7012f7bbf"
CACHE = os.path.join(os.environ.get("XDG_CACHE_HOME") or os.path.expanduser("~/.cache"), "heritage-themes")
CHROMES = ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser")
# Screenshot geometry in CSS pixels. HEIGHT only has to exceed the page; the PNG is trimmed to the windows.
WIDTH, HEIGHT, SCALE, MARGIN = 1328, 8000, 2, 24


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
    raise SystemExit(f"preview: --png needs one of: {', '.join(names)}")


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
    parser.add_argument("--png", action="store_true", help="also render <theme>/preview.png")
    parser.add_argument("themes", nargs="*", metavar="THEME", help="theme folders; default: all")
    args = parser.parse_args()
    families = {heritage.folder(f): f for f in heritage.load_families()}
    unknown = set(args.themes) - set(families)
    if unknown:
        raise SystemExit(f"preview: no theme folder named {', '.join(sorted(unknown))}")
    for name in args.themes or families:
        out = os.path.join(ROOT, name, "build")
        install_fonts(os.path.join(out, FONT_DIR))
        page_path = os.path.join(out, "preview.html")
        with open(page_path, "w") as f:
            f.write(page(families[name]))
        print(page_path)
        if args.png:
            png_path = os.path.join(ROOT, name, "preview.png")
            render_png(page_path, png_path)
            print(png_path)


if __name__ == "__main__":
    sys.exit(main())
