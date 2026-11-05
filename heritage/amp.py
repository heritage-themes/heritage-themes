"""Amp theme generated from a palette: a TextMate .tmTheme file in Amp's themes folder, which config.yml names.

Amp highlights code with syntect and the Sublime Text syntaxes it bundles, so the theme takes the rules of the Sublime
Text colour scheme (heritage.sublime), which colour the same TextMate scopes, with their variables resolved. Amp draws
text on the terminal's own background, so the theme reads as intended in a terminal that runs the matching theme of
the Terminals product; it takes the theme's lineHighlight for the current line and the status bar, and draws its mode
indicators in colours of its own.
"""
import plistlib, re

from .nvim import name  # noqa: F401 - Amp lists a theme by its file name, as Neovim lists a scheme
from .sublime import resolve, scheme as sublime_scheme


def settings(p):
    """The theme's global settings, as #RRGGBB."""
    caret = p.get("caret", p["gold"])
    return {"background": "#" + p["bg"], "foreground": "#" + p["fg"], "caret": "#" + caret,
            "lineHighlight": "#" + p["caretRow"], "selection": "#" + p["selection"],
            "selectionForeground": "#" + p["fg"], "gutter": "#" + p["bg"], "gutterForeground": "#" + p["lineNo"],
            "findHighlight": "#" + p["searchBg"], "findHighlightForeground": "#" + p["fg"],
            "invisibles": "#" + p["guide"], "guide": "#" + p["guide"]}


def rules(p):
    """(name, scope, foreground #RRGGBB, font style) per rule of the Sublime Text scheme, variables resolved."""
    s = sublime_scheme(p)
    out = []
    for rule in s["rules"]:
        if "foreground" not in rule:
            continue
        out.append((rule.get("name", rule["scope"]), rule["scope"], resolve(rule["foreground"], s).upper(),
                    rule.get("font_style", "")))
    return out


def theme(p, source):
    """The themes/<theme>.tmTheme file for a palette. source is the URL of the theme folder."""
    data = {
        "name": p["name"],
        "author": "Heritage Themes",
        "comment": f"{p['name']}: a Heritage Themes theme for Amp. Generated from {source}; changes here are "
                   "overwritten.",
        "colorSpaceName": "sRGB",
        "semanticClass": f"theme.{'dark' if p['dark'] else 'light'}.{name_slug(p)}",
        "settings": [{"settings": settings(p)}] + [
            {"name": rule_name, "scope": scope, "settings": {"foreground": colour, "fontStyle": font}}
            for rule_name, scope, colour, font in rules(p)],
    }
    return plistlib.dumps(data).decode("utf-8")


def name_slug(p):
    return re.sub(r"[^a-z0-9]+", "_", p["name"].lower()).strip("_")


def styles(p):
    """Rule → dict(fg, bg) as #RRGGBB, for the build's contrast check: each rule's colour on the background."""
    out = {f"{rule_name} ({scope})": dict(fg=colour, bg="#" + p["bg"]) for rule_name, scope, colour, _ in rules(p)}
    out.update({f"{rule_name} ({scope}) on the current line": dict(fg=colour, bg="#" + p["caretRow"])
                for rule_name, scope, colour, _ in rules(p)})
    return out
