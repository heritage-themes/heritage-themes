"""Amp theme generated from a palette: a TextMate .tmTheme file in Amp's themes folder, which config.yml names.

Amp highlights code with syntect and the Sublime Text syntaxes it bundles, so the theme is heritage.textmate's. Amp
draws text on the terminal's own background, so the theme reads as intended in a terminal that runs the matching theme
of the Terminals product; it takes the theme's lineHighlight for the current line and the status bar, and draws its
mode indicators in colours of its own.
"""
from .nvim import name  # noqa: F401 - Amp lists a theme by its file name, as Neovim lists a scheme
from .textmate import rules, settings, styles  # noqa: F401 - the build checks Amp's themes against them
from . import textmate


def theme(p, source):
    """The themes/<theme>.tmTheme file for a palette. source is the URL of the theme folder."""
    return textmate.theme(p, source, "Amp", settings(p))
