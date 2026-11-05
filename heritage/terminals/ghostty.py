"""Ghostty theme: a file in ~/.config/ghostty/themes that the theme option names, alone or as light:...,dark:...."""
from . import check_lines, colours, header, name, standard_pairs

APP = "Ghostty"
FOLDER = "ghostty"
CATEGORY = "Terminal emulators"
INSTALL = """Copy the files in `ghostty` into `~/.config/ghostty/themes` and name a theme in Ghostty's `config`, \
alone or as a pair that follows the system's light or dark appearance:

```text
theme = light:{light_stem},dark:{stem}
```

Each theme colours the terminal, the cursor, selections, search matches, split dividers and the title bar."""


def options(p):
    """(option, value) pairs; palette repeats once per colour."""
    c = colours(p)
    return [
        *(("palette", f"{i}={colour}") for i, colour in enumerate(c["ansi"])),
        ("background", c["bg"]), ("foreground", c["fg"]),
        ("cursor-color", c["cursor"]), ("cursor-text", c["cursor_text"]),
        ("selection-background", c["selection_bg"]), ("selection-foreground", c["selection_fg"]),
        ("search-background", c["match_bg"]), ("search-foreground", c["match_fg"]),
        ("search-selected-background", c["focused_match_bg"]),
        ("search-selected-foreground", c["focused_match_fg"]),
        ("split-divider-color", c["border"]),
        ("window-titlebar-background", c["bar_bg"]), ("window-titlebar-foreground", c["fg"]),
    ]


def files(theme, source):
    p = theme["palette"]
    lines = [*header(p, APP, source), *(f"{key} = {value}" for key, value in options(p))]
    return [(name(theme), "\n".join(lines) + "\n")]


def validate(theme, text):
    check_lines(text, r"[a-z-]+ = (?:\d{1,2}=)?#[0-9A-F]{6}")
    found = [tuple(line.split(" = ")) for line in text.splitlines() if line and not line.startswith("#")]
    if found != options(theme["palette"]):
        raise ValueError("differs from heritage.terminals.ghostty.options")


def pairs(p):
    c = colours(p)
    return [*standard_pairs(p), ("title bar", c["fg"], c["bar_bg"], 4.5)]
