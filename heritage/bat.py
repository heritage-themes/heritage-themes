"""bat theme generated from a palette: a TextMate .tmTheme file in bat's themes folder, which bat compiles into its
cache.

bat highlights code with syntect and the Sublime Text syntaxes it bundles, so the theme is heritage.textmate's. bat
prints text on the terminal's own background, so the theme reads as intended in a terminal that runs the matching theme
of the Terminals product. It draws line numbers, the grid and the header's rules in gutterForeground, the line that
--highlight-line names on lineHighlight, and the Git change markers in the terminal's ANSI green, yellow and red. Every
line number is text the reader uses, and the same colour frames the whole output, so gutterForeground takes muted, the
palette's neutral secondary text.
"""
from .nvim import name  # noqa: F401 - bat lists a theme by its file name, as Neovim lists a scheme
from .textmate import rules  # noqa: F401 - the build checks bat's themes against them
from . import textmate


def settings(p):
    """The theme's global settings, as #RRGGBB."""
    return dict(textmate.settings(p), gutterForeground="#" + p["muted"])


def theme(p, source):
    """The themes/<theme>.tmTheme file for a palette. source is the URL of the theme folder."""
    return textmate.theme(p, source, "bat", settings(p))


def styles(p):
    """Rule → dict(fg, bg) as #RRGGBB, for the build's contrast check: the rules on the background and on the
    highlighted line, and the line numbers on the background."""
    return dict(textmate.styles(p), **{"line numbers (gutterForeground)": dict(fg="#" + p["muted"],
                                                                               bg="#" + p["bg"])})
