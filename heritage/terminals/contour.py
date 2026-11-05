"""Contour colour scheme: an entry for the color_schemes section of contour.yml, which a profile's colors option
names, alone or as light and dark."""
from . import ANSI_NAMES, colours, header, name, standard_pairs, yaml as parse_yaml

APP = "Contour"
FOLDER = "contour"
CATEGORY = "Terminal emulators"
INSTALL = """Contour keeps its colour schemes in `contour.yml`. Add a theme's scheme, the lines of a file such as \
`contour/{stem}.yml` under `color_schemes:`, to the `color_schemes` section, then name it in a profile, alone or as a \
pair that follows the system's light or dark appearance:

```yaml
profiles:
    main:
        colors:
            light: {light_stem}
            dark: {stem}
```

Each scheme colours the terminal, the cursor, selections, search matches, vi mode, hints, hyperlinks, the input method \
editor and the indicator status line."""


def scheme(p):
    """The scheme as nested dicts, in the order of contour's generated configuration."""
    c = colours(p)
    def highlight(fg, bg):
        return {"foreground": c[fg], "foreground_alpha": 1, "background": c[bg], "background_alpha": 1}
    return {
        "default": {"background": c["bg"], "foreground": c["fg"], "bright_foreground": c["bright_fg"],
                    "dimmed_foreground": c["dim_fg"]},
        "cursor": {"default": c["cursor"], "text": c["cursor_text"]},
        "hyperlink_decoration": {"normal": c["link"], "hover": c["link"]},
        "vi_mode_highlight": {"foreground": "CellForeground", "foreground_alpha": 1, "background": c["selection_bg"],
                              "background_alpha": 1},
        "vi_mode_cursorline": {"foreground": "CellForeground", "foreground_alpha": 1, "background": c["surface"],
                               "background_alpha": 1},
        "selection": highlight("selection_fg", "selection_bg"),
        "search_highlight": highlight("match_fg", "match_bg"),
        "search_highlight_focused": highlight("focused_match_fg", "focused_match_bg"),
        "word_highlight_current": {"foreground": "CellForeground", "foreground_alpha": 1,
                                   "background": c["match_bg"], "background_alpha": 1},
        "word_highlight_other": {"foreground": "CellForeground", "foreground_alpha": 1,
                                 "background": c["match_bg"], "background_alpha": 1},
        "hint_label": highlight("focused_match_fg", "focused_match_bg"),
        "hint_match": highlight("match_fg", "match_bg"),
        "indicator_statusline": {"default": {"foreground": c["fg"], "background": c["bar_bg"]},
                                 "inactive": {"foreground": c["muted"], "background": c["bar_bg"]}},
        "input_method_editor": {"foreground": c["fg"], "background": c["surface"]},
        "normal": dict(zip(ANSI_NAMES, c["ansi"][:8])),
        "bright": dict(zip(ANSI_NAMES, c["ansi"][8:])),
        "dim": dict(zip(ANSI_NAMES, c["dim"])),
    }


def yaml(value, indent):
    """YAML lines for nested dicts of strings and numbers, colours quoted."""
    lines = []
    for key, item in value.items():
        if isinstance(item, dict):
            lines += [" " * indent + f"{key}:", *yaml(item, indent + 4)]
        else:
            lines.append(" " * indent + f"{key}: " + (f"'{item}'" if str(item).startswith("#") else str(item)))
    return lines


def files(theme, source):
    p = theme["palette"]
    lines = [*header(p, APP, source), "color_schemes:", f"    {name(theme)}:", *yaml(scheme(p), 8)]
    return [(f"{name(theme)}.yml", "\n".join(lines) + "\n")]


def validate(theme, text):
    def strings(value):
        """The values as the YAML holds them: numbers as their text."""
        return {k: strings(v) for k, v in value.items()} if isinstance(value, dict) else str(value)
    if parse_yaml(text) != {"color_schemes": {name(theme): strings(scheme(theme["palette"]))}}:
        raise ValueError("differs from heritage.terminals.contour.scheme")


def pairs(p):
    c = colours(p)
    return [*standard_pairs(p), ("status line", c["fg"], c["bar_bg"], 4.5),
            ("inactive status line", c["muted"], c["bar_bg"], 4.5), ("input method editor", c["fg"], c["surface"], 4.5)]
