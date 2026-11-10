"""Checks a screenshot of a GUI editor showing a sample with a theme: no foreign colours, and the main roles present.

Usage: python3 pixels.py SHOT.png PALETTE.json

PALETTE.json holds {"background": #RRGGBB, "backgrounds": [...], "foregrounds": [...], "crop": [top, bottom, left,
right], "allowed": [...], "rounding": N}: the editor's background, the other backgrounds the theme draws text
on, every colour the theme draws, the pixels at each edge of the window that the editor draws itself, in its toolkit's
colours, which the check leaves out, colours that the editor draws itself inside, such as a text cursor that inverts
the background, and how far per channel the background may differ from the most common colour (default 0), for a
screenshot whose background the toolkit blends itself. A colour that covers at least MIN_PIXELS pixels must be one of
the theme's colours, or lie between a foreground and a background, as antialiased text does, within TOLERANCE, blended
in sRGB or, as toolkits that correct text for gamma blend it, in linear light. The background must be the most common
colour. Prints {"problems": [...], "present": [...]}, with present the foregrounds that cover at least
REQUIRED_PIXELS pixels, which the caller checks across samples.
"""
import json, re, subprocess, sys

MIN_PIXELS = 12
TOLERANCE = 10.0  # in 0-255 per channel; rounding at glyph edges reaches about 9, a foreign colour far more
REQUIRED_PIXELS = 6  # pixels of exactly a foreground, as the cores of glyphs draw it


def rgb(colour):
    return tuple(int(colour[i:i + 2], 16) for i in (1, 3, 5))


def histogram(path, top, bottom, left, right):
    out = subprocess.run(["magick", path, "-gravity", "north", "-chop", f"0x{top}", "-gravity", "south", "-chop",
                          f"0x{bottom}", "-gravity", "west", "-chop", f"{left}x0", "-gravity", "east", "-chop",
                          f"{right}x0", "-format", "%c", "histogram:info:-"], capture_output=True, text=True,
                         check=True).stdout
    counts = {}
    for line in out.splitlines():
        match = re.match(r"\s*(\d+):.*?#([0-9A-F]{6})", line)
        if match:
            counts["#" + match[2]] = counts.get("#" + match[2], 0) + int(match[1])
    return counts


def distance_to_blend(c, fg, bg):
    """The distance from c to the segment from bg to fg, in RGB."""
    d = [f - b for f, b in zip(fg, bg)]
    length = sum(x * x for x in d)
    t = 0.0 if not length else max(0.0, min(1.0, sum((x - b) * y for x, b, y in zip(c, bg, d)) / length))
    return sum((x - (b + t * y)) ** 2 for x, b, y in zip(c, bg, d)) ** 0.5


def linear(c):
    """A colour's channels in linear light, scaled to 0-255."""
    def channel(v):
        v /= 255
        return 255 * (v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4)
    return tuple(channel(v) for v in c)


def blend_distance(c, fg, bg):
    """The distance from c to the blends of fg and bg, in sRGB or in linear light, whichever is nearer."""
    return min(distance_to_blend(c, fg, bg), distance_to_blend(linear(c), linear(fg), linear(bg)))


def main():
    path, palette_path = sys.argv[1:3]
    with open(palette_path, encoding="utf-8") as f:
        palette = json.load(f)
    counts = histogram(path, *palette.get("crop", (0, 0, 0, 0)))
    problems = []
    most = max(counts, key=counts.get)
    if max(abs(a - b) for a, b in zip(rgb(most), rgb(palette["background"]))) > palette.get("rounding", 0):
        problems.append(f"background is {most}, not {palette['background']}")
    backgrounds = [rgb(c) for c in [palette["background"], *palette["backgrounds"]]]
    foregrounds = [rgb(c) for c in palette["foregrounds"]]
    allowed = {colour.upper() for colour in palette.get("allowed", [])}
    for colour, count in sorted(counts.items(), key=lambda item: -item[1]):
        if count < MIN_PIXELS or colour in allowed:
            continue
        c = rgb(colour)
        if min(blend_distance(c, fg, bg) for fg in foregrounds + backgrounds for bg in backgrounds) > TOLERANCE:
            problems.append(f"{colour} ({count} pixels) is not a colour of the theme or a blend of one with a "
                            "background")
    present = [colour for colour in palette["foregrounds"] if counts.get(colour.upper(), 0) >= REQUIRED_PIXELS]
    print(json.dumps({"problems": problems, "present": present}))


if __name__ == "__main__":
    main()
