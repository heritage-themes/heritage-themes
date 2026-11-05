"""Checks a screen that shells.py read: every colour is one the theme sets, and text reaches its contrast minimum on the
background it is drawn on.

Usage: python3 cells.py SCREEN.json BG FG ALLOWED COMMENT [ROWS]

BG and FG are the theme's background and text colours, which the terminal's default colours stand for when the
terminal runs the matching Terminals theme. ALLOWED is a comma-separated list of the colours the app's theme sets.
COMMENT is the comment colour, which is held to 3:1 as in every target. ROWS limits the check to those rows, counted
from the end when negative, for example 0,-1 for a multiplexer's bars, or to a slice of them, as 0:-1 for every row but
the last. Other text is held to 4.5:1, except characters drawn as decoration rather than text, such
as powerline separators and box drawing. Whitespace shows only its background, so only that is checked. Prints each
problem and exits 1 when there is one.
"""
import json, sys

DECORATION = set("─│╭╮╰╯├┤┬┴┼━┃═║") | {chr(c) for c in range(0xE0A0, 0xE0D8)} | {chr(c) for c in range(0x2500, 0x2580)}
MINIMUM = 4.5


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
    path, bg, fg, allowed, comment = sys.argv[1:6]
    rows = json.load(open(path, encoding="utf-8"))
    if len(sys.argv) <= 6:
        selected = range(len(rows))
    elif ":" in sys.argv[6]:
        start, end = (int(v) if v else None for v in sys.argv[6].split(":"))
        selected = range(len(rows))[start:end]
    else:
        selected = [int(y) % len(rows) for y in sys.argv[6].split(",")]
    allowed = {c.upper() for c in allowed.split(",")} | {bg.upper(), fg.upper()}
    problems = []
    for y in selected:
        for x, (char, cfg, cbg, bold, italic, underline) in enumerate(rows[y]):
            cfg = fg.upper() if cfg == "default" else cfg
            cbg = bg.upper() if cbg == "default" else cbg
            for colour in (cfg, cbg) if char.strip() else (cbg,):
                if colour not in allowed:
                    problems.append(f"row {y} column {x} {char!r}: {colour} is not a colour of the theme")
            if not char.strip() or char in DECORATION or cfg not in allowed or cbg not in allowed:
                continue
            ratio = contrast(cfg, cbg)
            if ratio < (3 if cfg == comment.upper() else MINIMUM):
                problems.append(f"row {y} column {x} {char!r}: {cfg} on {cbg} is {ratio:.2f}:1")
    for problem in dict.fromkeys(problems):
        print(f"{path}: {problem}")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
