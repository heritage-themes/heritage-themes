"""Checks a screenshot of the test card: the background is the most common colour, and each of the 16 ANSI colours
fills at least the area of its two rows of blocks, exactly as the theme gives it.

Usage: python3 check.py [--display-p3] SHOT.png BG COLOUR0 ... COLOUR15   (colours as #RRGGBB)

--display-p3 expects the ANSI colours as Rio 0.5 draws cells on Linux: converted from sRGB to Display P3 primaries,
with the result shown on an sRGB display unconverted. Rio clears the window in the background colour as it is.

Prints the colours that fall short and exits 1 when one does. The screen outside the window is the X server's black
root window, which the background check leaves out; no palette uses pure black.
"""
import re, subprocess, sys

MIN_PIXELS = 1500  # two rows of eight cells at the smallest font the previews use
SRGB_TO_P3 = ((0.8224621, 0.1775380, 0.0), (0.0331941, 0.9668058, 0.0), (0.0170827, 0.0723974, 0.9105199))
ROOT = "#000000"


def display_p3(colour):
    def linear(c):
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    def encode(c):
        c = max(0.0, min(1.0, c))
        return c * 12.92 if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055
    rgb = [linear(int(colour[i:i + 2], 16) / 255) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(encode(sum(m * v for m, v in zip(row, rgb))) * 255):02X}" for row in SRGB_TO_P3)


def histogram(path):
    out = subprocess.run(["magick", path, "-format", "%c", "histogram:info:-"], capture_output=True, text=True,
                         check=True).stdout
    counts = {}
    for line in out.splitlines():
        match = re.match(r"\s*(\d+):.*?#([0-9A-F]{6})", line)
        if match:
            counts["#" + match[2]] = counts.get("#" + match[2], 0) + int(match[1])
    return counts


def main():
    args = sys.argv[1:]
    p3 = args[0] == "--display-p3"
    convert = (lambda colour: display_p3(colour.upper())) if p3 else str.upper
    path, bg, *ansi = args[1:] if p3 else args
    counts = histogram(path)
    counts.pop(ROOT, None)
    problems = []
    most = max(counts, key=counts.get)
    if most != bg.upper():
        problems.append(f"background is {most}, not {bg.upper()}")
    for i, colour in enumerate(ansi):
        if counts.get(convert(colour), 0) < MIN_PIXELS:
            problems.append(f"colour {i} {convert(colour)}: {counts.get(convert(colour), 0)} pixels")
    for problem in problems:
        print(f"{path}: {problem}")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
