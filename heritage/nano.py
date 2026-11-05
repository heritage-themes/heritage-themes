"""Nano colour scheme generated from a palette: the interface colours of a nanorc file, whose lines go into the
user's nanorc, as nano reads set commands only there and not from files it includes.

Nano's syntax files colour code with the terminal's 16 colours by name, so in a terminal that runs the matching theme
of the Terminals product, code takes the palette's ANSI colours; the scheme sets the interface around it. Text takes the
terminal's colours too, by name or as normal (the terminal's own text and background), so it shows the palette's
colours exactly: normal is fg on bg, lightblack the muted text, and red, green, yellow, blue, magenta and cyan the ANSI
colours, as heritage.terminals gives them. Nano offers nothing else in 24-bit colour; a surface that is no terminal
colour, such as the frame of the title bar, takes a three-digit #rgb, which nano draws as one of the 230 colours of a
256-colour terminal that it reaches. The scheme picks the one nearest to the palette's colour.

The layout follows the Islands layout of the other targets: the title bar and mini bar on the frame, the status bar
and prompt on surface, and the help lines on bg.
"""
import re

from .nvim import name  # noqa: F401 - Nano's schemes take the names of Neovim's
from .terminals import colours as terminal_colours, contrast
from .vim import lab, xterm_colours

# The colours that nano names and the terminal's colours they stand for, as heritage.terminals gives them.
NAMES = {"normal": "fg", "lightblack": 8, "red": 1, "green": 2, "yellow": 3, "blue": 4, "magenta": 5, "cyan": 6,
         "white": 7, "lightwhite": 15}
# The interface colour options of nano 9 (nanorc(5)).
OPTIONS = ("titlecolor", "minicolor", "statuscolor", "errorcolor", "promptcolor", "selectedcolor", "spotlightcolor",
           "stripecolor", "scrollercolor", "numbercolor", "keycolor", "functioncolor")
# Options drawn as marks rather than text, which the contrast check leaves out: the guide stripe, the scroll indicator
# and line numbers, which the other targets draw in the guide and line number colours.
DECORATIVE = {"stripecolor", "scrollercolor", "numbercolor"}
# Translation tables of nano's closest_index_color, from #rgb digits to the levels of the 6x6x6 colour cube and to the
# 24 greys.
LEVELS = (0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5)
GREYS = (1, 2, 3, 4, 5, 6, 7, 9, 11, 13, 15, 18, 21, 23)


def index(rgb):
    """The 256-colour index that nano draws a three-digit #rgb in."""
    r, g, b = (int(digit, 16) for digit in rgb[1:])
    if r == g == b and 0 < r < 0xF:
        return 232 + GREYS[r - 1]
    return 36 * LEVELS[r] + 6 * LEVELS[g] + LEVELS[b] + 16


def reachable():
    """Index → the shortest #rgb that nano draws in it, for every index that a #rgb reaches."""
    out = {}
    for value in range(0x1000):
        rgb = f"#{value:03X}"
        out.setdefault(index(rgb), rgb)
    return out


REACHABLE = reachable()
XTERM = xterm_colours()


def nearest(colour, texts=(), minimum=4.5):
    """The #rgb that nano draws nearest to a #RRGGBB colour, by the CIE76 distance, among those on which each of the
    #RRGGBB text colours reaches minimum contrast."""
    target = lab(tuple(int(colour[i:i + 2], 16) for i in (1, 3, 5)))
    candidates = [i for i in REACHABLE
                  if all(contrast(text, "".join(f"{v:02X}" for v in XTERM[i])) >= minimum for text in texts)]
    best = min(candidates, key=lambda i: sum((a - b) ** 2 for a, b in zip(lab(XTERM[i]), target)))
    return REACHABLE[best]


def shown(p, value):
    """The #RRGGBB colour that a colour value of the scheme shows in a terminal that runs the matching theme."""
    c = terminal_colours(p)
    if value.startswith("#"):
        return "#" + "".join(f"{v:02X}" for v in XTERM[index(value)])
    key = NAMES[value]
    return c[key] if isinstance(key, str) else c["ansi"][key]


def options(p):
    """Option → (attributes, foreground, background), with None for a colour left to the terminal. Each surface is
    the colour nearest to the palette's on which its text reaches 4.5:1."""
    fg = "#" + p["fg"]
    def surface(key, *texts):
        """The #rgb nearest to a palette surface on which fg, or the given texts, stay readable."""
        return nearest("#" + p[key], texts or (fg,))
    error_text = nearest("#" + p["redText"])
    return {
        "titlecolor": (["bold"], "normal", surface("frame")),
        "minicolor": ([], "normal", surface("frame")),
        "statuscolor": ([], "normal", surface("surface")),
        "errorcolor": (["bold"], error_text, surface("red", shown(p, error_text))),
        "promptcolor": ([], "normal", surface("surface")),
        "selectedcolor": ([], "normal", surface("selection")),
        "spotlightcolor": ([], "normal", surface("searchBg")),
        "stripecolor": ([], None, nearest("#" + p["guide"])),
        "scrollercolor": ([], "lightblack", None),
        "numbercolor": ([], nearest("#" + p["lineNo"]), None),
        # the help lines: shortcuts in the blue of the other targets' key bindings, their descriptions in the text
        "keycolor": (["bold"], "blue", None),
        "functioncolor": ([], "normal", None),
    }


def value(attributes, fg, bg):
    """A nanorc colour value: attributes, then fgcolor and ,bgcolor, either of which may be left out."""
    return ",".join([*attributes, fg or ""]) + (f",{bg}" if bg else "")


def colorscheme(p, source):
    """The <scheme>.nanorc file for a palette. source is the URL of the theme folder."""
    lines = [
        f"## {p['name']}: a Heritage Themes colour scheme for Nano.",
        f"## Generated from {source}; changes here are overwritten.",
        "## Run it in a terminal that runs the matching Heritage theme, whose colours it names.",
        "",
        *(f"set {option} {value(*spec)}" for option, spec in options(p).items()),
    ]
    return "\n".join(lines) + "\n"


def styles(p):
    """Option → dict(fg, bg) of the #RRGGBB colours it shows, for the build's contrast check."""
    out = {}
    for option, (attributes, fg, bg) in options(p).items():
        out[option] = {key: shown(p, colour) for key, colour in (("fg", fg or "normal"), ("bg", bg)) if colour}
        out[option].setdefault("bg", "#" + p["bg"])
    return out


def parse(text):
    """Option → value of a scheme's set lines."""
    return dict(re.fullmatch(r"set (\w+) (\S+)", line).groups() for line in text.splitlines()
                if line.startswith("set "))
