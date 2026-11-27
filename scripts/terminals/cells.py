"""Checks a screen that shells.py read: every colour is one the theme sets, and text reaches its contrast minimum on the
background it is drawn on.

Usage: python3 cells.py SCREEN.json BG FG ALLOWED DIMMED [ROWS [BACKDROPS]]

BG and FG are the theme's background and text colours, which the terminal's default colours stand for when the
terminal runs the matching Terminals theme. ALLOWED is a comma-separated list of the colours the app's theme sets.
DIMMED is a comma-separated list of the colours held to 3:1: the comment colour, as in every target, and the colours an
app dims text to, such as btop's fading process list. ROWS limits the check to those rows, counted from the end when
negative, for example 0,-1 for a multiplexer's bars, or to a slice of them, as 0:-1 for every row but the last. Other
text is held to 4.5:1, except characters drawn as decoration rather than text, such as powerline separators and box
drawing, which are not checked, and characters that draw graphs and meters, which are held to the 3:1 of graphics.
Whitespace shows only its background, so only that is checked. BACKDROPS is a comma-separated list of the colours that
the app fills areas with, such as a selected row: a block element drawn in one of them, as fzf draws its gutter, is part
of that area rather than a graphic, so only its colours are checked. Prints each problem and exits 1 when there is
one.
"""
import json, sys

DECORATION = set("─│╭╮╰╯├┤┬┴┼━┃═║") | {chr(c) for c in range(0xE0A0, 0xE0D8)} | {chr(c) for c in range(0x2500, 0x2580)}
# braille patterns, block elements and the black square, of which graphs and meters are drawn
GRAPHICS = {chr(c) for c in range(0x2800, 0x2900)} | {chr(c) for c in range(0x2580, 0x25A1)}
# block elements, which draw part of a cell's area in the foreground colour
BLOCKS = {chr(c) for c in range(0x2580, 0x25A0)}
MINIMUM, LOW = 4.5, 3


def luminance(colour):
    def channel(c):
        c /= 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (channel(int(colour[i:i + 2], 16)) for i in (1, 3, 5))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    x, y = sorted((luminance(a), luminance(b)), reverse=True)
    return (x + 0.05) / (y + 0.05)


def main():
    path, bg, fg, allowed, dimmed = sys.argv[1:6]
    rows = json.load(open(path, encoding="utf-8"))
    if len(sys.argv) <= 6:
        selected = range(len(rows))
    elif ":" in sys.argv[6]:
        start, end = (int(v) if v else None for v in sys.argv[6].split(":"))
        selected = range(len(rows))[start:end]
    else:
        selected = [int(y) % len(rows) for y in sys.argv[6].split(",")]
    allowed = {c.upper() for c in allowed.split(",")} | {bg.upper(), fg.upper()}
    dimmed = {c.upper() for c in dimmed.split(",")}
    backdrops = {c.upper() for c in sys.argv[7].split(",")} if len(sys.argv) > 7 and sys.argv[7] else set()
    problems = []
    for y in selected:
        for x, (char, cfg, cbg, bold, italic, underline) in enumerate(rows[y]):
            cfg = fg.upper() if cfg == "default" else cfg
            cbg = bg.upper() if cbg == "default" else cbg
            for colour in (cfg, cbg) if char.strip() else (cbg,):
                if colour not in allowed:
                    problems.append(f"row {y} column {x} {char!r}: {colour} is not a colour of the theme")
            if (not char.strip() or char in DECORATION or (char in BLOCKS and cfg in backdrops) or cfg not in allowed
                    or cbg not in allowed):
                continue
            ratio = contrast(cfg, cbg)
            if ratio < (LOW if cfg in dimmed or char in GRAPHICS else MINIMUM):
                problems.append(f"row {y} column {x} {char!r}: {cfg} on {cbg} is {ratio:.2f}:1")
    for problem in dict.fromkeys(problems):
        print(f"{path}: {problem}")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
