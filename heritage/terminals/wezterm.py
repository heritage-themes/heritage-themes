"""WezTerm colour scheme: a TOML file in ~/.config/wezterm/colors, which color_scheme selects by its metadata name."""
import tomllib

from . import AUTHOR, HEX, colours, header, name, standard_pairs, tab_pairs

APP = "WezTerm"
FOLDER = "wezterm"
CATEGORY = "Terminal emulators"
INSTALL = """Copy the files in `wezterm` into `~/.config/wezterm/colors` and choose a scheme by its name in \
`wezterm.lua`:

```lua
config.color_scheme = "{label}"
```

Each scheme colours the terminal, the cursor, selections, copy mode, quick select, split lines and the retro tab bar \
(`use_fancy_tab_bar = false`); the fancy tab bar takes its colours from `window_frame` instead."""


def quote(value):
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def tables(p, source):
    """Table name → {key: TOML value}."""
    c = colours(p)
    def tab(bg, fg):
        return {"bg_color": quote(c[bg]), "fg_color": quote(c[fg])}
    return {
        "colors": {
            "foreground": quote(c["fg"]), "background": quote(c["bg"]),
            "cursor_bg": quote(c["cursor"]), "cursor_fg": quote(c["cursor_text"]),
            "cursor_border": quote(c["cursor"]),
            "selection_fg": quote(c["selection_fg"]), "selection_bg": quote(c["selection_bg"]),
            "scrollbar_thumb": quote(c["border"]), "split": quote(c["border"]),
            "visual_bell": quote(c["surface"]), "compose_cursor": quote(c["ansi"][3]),
            "copy_mode_active_highlight_fg": "{ Color = " + quote(c["focused_match_fg"]) + " }",
            "copy_mode_active_highlight_bg": "{ Color = " + quote(c["focused_match_bg"]) + " }",
            "copy_mode_inactive_highlight_fg": "{ Color = " + quote(c["match_fg"]) + " }",
            "copy_mode_inactive_highlight_bg": "{ Color = " + quote(c["match_bg"]) + " }",
            "quick_select_label_fg": "{ Color = " + quote(c["focused_match_fg"]) + " }",
            "quick_select_label_bg": "{ Color = " + quote(c["focused_match_bg"]) + " }",
            "quick_select_match_fg": "{ Color = " + quote(c["match_fg"]) + " }",
            "quick_select_match_bg": "{ Color = " + quote(c["match_bg"]) + " }",
            "ansi": "[" + ", ".join(quote(v) for v in c["ansi"][:8]) + "]",
            "brights": "[" + ", ".join(quote(v) for v in c["ansi"][8:]) + "]",
        },
        "colors.tab_bar": {"background": quote(c["bar_bg"]), "inactive_tab_edge": quote(c["border"])},
        "colors.tab_bar.active_tab": tab("active_tab_bg", "active_tab_fg"),
        "colors.tab_bar.inactive_tab": tab("inactive_tab_bg", "inactive_tab_fg"),
        "colors.tab_bar.inactive_tab_hover": tab("hover_tab_bg", "fg"),
        "colors.tab_bar.new_tab": tab("inactive_tab_bg", "inactive_tab_fg"),
        "colors.tab_bar.new_tab_hover": tab("hover_tab_bg", "fg"),
        "metadata": {"name": quote(p["name"]), "author": quote(AUTHOR), "origin_url": quote(source)},
    }


def files(theme, source):
    p = theme["palette"]
    lines = header(p, APP, source)
    for table, values in tables(p, source).items():
        lines += ["", f"[{table}]", *(f"{key} = {value}" for key, value in values.items())]
    return [(f"{name(theme)}.toml", "\n".join(lines) + "\n")]


def validate(theme, text):
    data = tomllib.loads(text)
    colours_ = data["colors"]
    for key in ("foreground", "background", "cursor_bg", "cursor_fg", "selection_fg", "selection_bg"):
        if not HEX.fullmatch(colours_[key].upper()):
            raise ValueError(f"colors.{key} is {colours_[key]!r}")
    if len(colours_["ansi"]) != 8 or len(colours_["brights"]) != 8:
        raise ValueError("ansi and brights need 8 colours each")
    if data["metadata"]["name"] != theme["palette"]["name"]:
        raise ValueError("metadata.name is not the theme's name")
    if set(colours_["tab_bar"]) != {"background", "inactive_tab_edge", "active_tab", "inactive_tab",
                                    "inactive_tab_hover", "new_tab", "new_tab_hover"}:
        raise ValueError("colors.tab_bar is incomplete")


def pairs(p):
    return [*standard_pairs(p), *tab_pairs(p)]
