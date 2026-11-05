"""Rio theme: a TOML file in ~/.config/rio/themes that the theme option, or adaptive-theme, names."""
import tomllib

from . import ANSI_NAMES, colours, header, name, standard_pairs

APP = "Rio"
FOLDER = "rio"
CATEGORY = "Terminal emulators"
INSTALL = """Copy the files in `rio` into `~/.config/rio/themes` and name a theme in `config.toml`, alone or as a pair \
that follows the system's light or dark appearance:

```toml
[adaptive-theme]
light = "{light_stem}"
dark = "{stem}"
```

Each theme colours the terminal, the cursor, the vi mode cursor, selections, search matches, hints, splits and the \
tab bar."""


def keys(p):
    """[colors] key → #RRGGBB, as Rio 0.5 reads them."""
    c = colours(p)
    out = {
        "background": c["bg"], "foreground": c["fg"], "dim-foreground": c["dim_fg"],
        "light-foreground": c["bright_fg"],
        "cursor": c["cursor"], "vi-cursor": c["ansi"][4],
        "selection-background": c["selection_bg"], "selection-foreground": c["selection_fg"],
        # the tab bar on the frame, with the active tab's marker in the accent of the other terminals' borders
        "tabs": c["bar_bg"], "tabs-active": c["active_border"],
        "split": c["border"], "split-active": c["active_border"],
        "search-match-background": c["match_bg"], "search-match-foreground": c["match_fg"],
        "search-focused-match-background": c["focused_match_bg"],
        "search-focused-match-foreground": c["focused_match_fg"],
        "hint-background": c["focused_match_bg"], "hint-foreground": c["focused_match_fg"],
    }
    out.update(zip(ANSI_NAMES, c["ansi"][:8]))
    out.update({f"light-{n}": colour for n, colour in zip(ANSI_NAMES, c["ansi"][8:])})
    out.update({f"dim-{n}": colour for n, colour in zip(ANSI_NAMES, c["dim"])})
    return out


def files(theme, source):
    p = theme["palette"]
    lines = [*header(p, APP, source), "", "[colors]", *(f"{key} = '{value}'" for key, value in keys(p).items())]
    return [(f"{name(theme)}.toml", "\n".join(lines) + "\n")]


def validate(theme, text):
    if tomllib.loads(text) != {"colors": keys(theme["palette"])}:
        raise ValueError("differs from heritage.terminals.rio.keys")


def pairs(p):
    c = colours(p)
    return [*standard_pairs(p), ("hint", c["focused_match_fg"], c["focused_match_bg"], 4.5)]
