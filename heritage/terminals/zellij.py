"""Zellij theme: a KDL file in ~/.config/zellij/themes that config.kdl names with theme, or with theme_dark and
theme_light. Zellij 0.42 and later draw their UI from components: text, ribbons (tabs, modes and key hints), tables,
lists, pane frames, exit codes and collaborators' cursors.

The tab and status bars sit on the frame, as the other targets draw bars, or on the first bar background that their
key hints in the ANSI colours are readable on. Ribbons are pills on the bar, as in Zellij's own themes: the selected
one in the blue accent of the selected pane frame, the others in the text colour, both with their text in bg. Zellij
draws the brackets around a ribbon's key in the bar's background colour, which the build checks against the text
colour at 4.5:1, and the key itself in the ribbon's first emphasis colour: the search background on the text colour,
which the build checks at 4.5:1 too. Lists and tables sit on bg, and a pane's frame and title take a text colour.
"""
EMPHASIS = ("ansiYellow", "ansiBlue", "ansiGreen", "ansiMagenta")
import re

from . import colours, contrast, name, readable_background

APP = "Zellij"
FOLDER = "zellij"
CATEGORY = "Multiplexers"
INSTALL = """Copy the files in `zellij` into `~/.config/zellij/themes` and name a theme in `config.kdl`, alone or as a \
pair that follows the terminal's light or dark background. Zellij 0.42 or later is required:

```kdl
theme_dark "{stem}"
theme_light "{light_stem}"
```

Each theme colours the tab bar, the status bar with its key hints, pane frames, the session manager's lists and \
tables, exit codes and collaborators' cursors."""
# Collaborators' cursors, in the order of the Zed theme's players.
PLAYERS = ("ansiBlue", "ansiMagenta", "ansiGreen", "ansiYellow", "ansiCyan", "ansiRed", "azure")


def components(p):
    """Component → {key: #RRGGBB}. Zellij requires the four emphasis colours in every component but the players."""
    c = colours(p)
    bar = readable_background(p, [p[key] for key in EMPHASIS] + [p["fg"], p["muted"]])
    def text(base, background):
        """A component with the ANSI emphasis colours. On the selection, where only ansiBlue is checked at 4.5:1, an
        emphasis colour below that takes ansiBlue, as the other targets colour matches in a selected list row."""
        accents = {f"emphasis_{i}": "#" + p[key if background != c["selection_bg"] or
                                            contrast(p[key], c["selection_bg"]) >= 4.5 else "ansiBlue"]
                   for i, key in enumerate(EMPHASIS)}
        return {"base": base, "background": background, **accents}
    return {
        "text_unselected": text(c["fg"], "#" + p[bar]),
        "text_selected": text(c["fg"], c["selection_bg"]),
        "ribbon_selected": dict(base=c["bg"], background=c["active_border"],
                                **{f"emphasis_{i}": c["bg"] for i in range(4)}),
        "ribbon_unselected": dict(base=c["bg"], background=c["fg"],
                                  **{f"emphasis_{i}": "#" + p[key]
                                     for i, key in enumerate(("searchBg", "selection", "selInactive", "bg"))}),
        "table_title": text(c["ansi"][2], c["bg"]),
        "table_cell_selected": text(c["fg"], c["selection_bg"]),
        "table_cell_unselected": text(c["fg"], c["bg"]),
        "list_selected": text(c["fg"], c["selection_bg"]),
        "list_unselected": text(c["fg"], c["bg"]),
        # Zellij draws a pane's title in its frame's colour, so frames take text colours
        "frame_unselected": text(c["muted"], c["bg"]),
        "frame_selected": text(c["active_border"], c["bg"]),
        "frame_highlight": text(c["ansi"][3], c["bg"]),
        "exit_code_success": text(c["ansi"][2], c["bg"]),
        "exit_code_error": text(c["ansi"][1], c["bg"]),
        "multiplayer_user_colors": {f"player_{i}": "#" + p[PLAYERS[(i - 1) % len(PLAYERS)]] for i in range(1, 11)},
    }


def files(theme, source):
    p = theme["palette"]
    scheme = name(theme)
    lines = [f"// {p['name']}: a Heritage Themes theme for {APP}.",
             f"// Generated from {source}; changes here are overwritten.",
             "themes {", f"    {scheme} {{"]
    for component, values in components(p).items():
        lines += [f"        {component} {{", *(f'            {key} "{value}"' for key, value in values.items()),
                  "        }"]
    lines += ["    }", "}"]
    return [(f"{scheme}.kdl", "\n".join(lines) + "\n")]


def validate(theme, text):
    """Checks the KDL: one theme of components with quoted colours, as components() gives them."""
    found, component = {}, None
    for line in text.splitlines()[2:]:
        if match := re.fullmatch(r"        (\w+) \{", line):
            component = found.setdefault(match[1], {})
        elif match := re.fullmatch(r'            (\w+) "(#[0-9A-F]{6})"', line):
            component[match[1]] = match[2]
        elif line not in ("themes {", f"    {name(theme)} {{", "        }", "    }", "}"):
            raise ValueError(f"malformed line {line!r}")
    if found != components(theme["palette"]):
        raise ValueError("differs from heritage.terminals.zellij.components")


def pairs(p):
    out = []
    parts = components(p)
    for component, values in parts.items():
        if component == "multiplayer_user_colors":
            continue  # cursors are drawn as marks, not text
        keys = ("base",) if component.startswith(("frame", "exit_code")) else \
            ("base", "emphasis_0", "emphasis_1", "emphasis_2", "emphasis_3")
        out += [(f"{component} {key}", values[key], values["background"], 4.5) for key in keys]
    bar = parts["text_unselected"]["background"]
    out += [(f"brackets on {ribbon}", bar, parts[ribbon]["background"], 4.5)
            for ribbon in ("ribbon_selected", "ribbon_unselected")]
    return out
