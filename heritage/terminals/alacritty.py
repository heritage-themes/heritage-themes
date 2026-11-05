"""Alacritty theme: a TOML file of [colors] tables that alacritty.toml imports with general.import."""
import tomllib

from . import ANSI_NAMES, colours, header, name, standard_pairs

APP = "Alacritty"
FOLDER = "alacritty"
CATEGORY = "Terminal emulators"
INSTALL = """Copy the files in `alacritty` into `~/.config/alacritty/themes` (`%AppData%\\alacritty\\themes` on \
Windows) and import one at the top of `alacritty.toml`. Alacritty 0.14 or later is required:

```toml
[general]
import = ["~/.config/alacritty/themes/{stem}.toml"]
```

Each theme colours the terminal, the cursor, the vi mode cursor, selections, search matches, hints and the footer \
bar."""


def tables(p):
    """Table name → {key: #RRGGBB}, in the order of alacritty(5)."""
    c = colours(p)
    def pair(fg, bg):
        return {"foreground": c[fg], "background": c[bg]}
    return {
        "colors.primary": {"foreground": c["fg"], "background": c["bg"], "dim_foreground": c["dim_fg"],
                           "bright_foreground": c["bright_fg"]},
        "colors.cursor": {"text": c["cursor_text"], "cursor": c["cursor"]},
        "colors.vi_mode_cursor": {"text": c["cursor_text"], "cursor": c["ansi"][4]},
        "colors.search.matches": pair("match_fg", "match_bg"),
        "colors.search.focused_match": pair("focused_match_fg", "focused_match_bg"),
        "colors.footer_bar": pair("fg", "bar_bg"),
        "colors.hints.start": pair("focused_match_fg", "focused_match_bg"),
        "colors.hints.end": pair("fg", "match_bg"),
        "colors.line_indicator": pair("fg", "bar_bg"),
        "colors.selection": {"text": c["selection_fg"], "background": c["selection_bg"]},
        "colors.normal": dict(zip(ANSI_NAMES, c["ansi"][:8])),
        "colors.bright": dict(zip(ANSI_NAMES, c["ansi"][8:])),
        "colors.dim": dict(zip(ANSI_NAMES, c["dim"])),
    }


def files(theme, source):
    p = theme["palette"]
    lines = header(p, APP, source)
    for table, values in tables(p).items():
        lines += ["", f"[{table}]", *(f'{key} = "{value}"' for key, value in values.items())]
    return [(f"{name(theme)}.toml", "\n".join(lines) + "\n")]


def validate(theme, text):
    data = tomllib.loads(text)
    for table, values in tables(theme["palette"]).items():
        node = data
        for part in table.split("."):
            node = node[part]
        if node != values:
            raise ValueError(f"[{table}] differs from heritage.terminals.alacritty.tables")


def pairs(p):
    c = colours(p)
    return [*standard_pairs(p), ("footer bar", c["fg"], c["bar_bg"], 4.5), ("hint end", c["fg"], c["match_bg"], 4.5),
            ("vi mode cursor", c["cursor_text"], c["ansi"][4], 3)]
