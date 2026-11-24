"""TextMate .tmTheme files generated from a palette, for the apps that read them: Amp, bat and Eclipse's TM4E.

These apps highlight code with TextMate scopes, which the Sublime Text colour scheme (heritage.sublime) colours, so a
theme takes that scheme's rules with their variables resolved.
"""
import plistlib, re

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


def theme(p, source, app, global_settings):
    """The .tmTheme file for a palette in app, with global_settings. source is the URL of the theme folder."""
    data = {
        "name": p["name"],
        "author": "Heritage Themes",
        "comment": f"{p['name']}: a Heritage Themes theme for {app}. Generated from {source}; changes here are "
                   "overwritten.",
        "colorSpaceName": "sRGB",
        "semanticClass": f"theme.{'dark' if p['dark'] else 'light'}.{slug(p)}",
        "settings": [{"settings": global_settings}] + [
            {"name": rule_name, "scope": scope, "settings": {"foreground": colour, "fontStyle": font}}
            for rule_name, scope, colour, font in rules(p)],
    }
    return plistlib.dumps(data).decode("utf-8")


def slug(p):
    return re.sub(r"[^a-z0-9]+", "_", p["name"].lower()).strip("_")


def styles(p):
    """Rule → dict(fg, bg) as #RRGGBB, for the build's contrast check: each rule's colour on the background and on the
    current line."""
    out = {f"{rule_name} ({scope})": dict(fg=colour, bg="#" + p["bg"]) for rule_name, scope, colour, _ in rules(p)}
    out.update({f"{rule_name} ({scope}) on the current line": dict(fg=colour, bg="#" + p["caretRow"])
                for rule_name, scope, colour, _ in rules(p)})
    return out
