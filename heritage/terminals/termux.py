"""Termux colour scheme: ~/.termux/colors.properties, applied with termux-reload-settings."""
from . import check_lines, colours, header, name, standard_pairs

APP = "Termux"
FOLDER = "termux"
CATEGORY = "Terminal emulators"
INSTALL = """Copy a theme's file to `~/.termux/colors.properties` and reload the settings:

```bash
mkdir -p ~/.termux
cp termux/{stem}.properties ~/.termux/colors.properties
termux-reload-settings
```

Each theme colours the terminal and the cursor. The extra keys row stays black in every theme."""


def properties(p):
    c = colours(p)
    out = {"background": c["bg"], "foreground": c["fg"], "cursor": c["cursor"]}
    out.update({f"color{i}": colour for i, colour in enumerate(c["ansi"])})
    return out


def files(theme, source):
    p = theme["palette"]
    lines = [*header(p, APP, source), *(f"{key}={value}" for key, value in properties(p).items())]
    return [(f"{name(theme)}.properties", "\n".join(lines) + "\n")]


def validate(theme, text):
    check_lines(text, r"\w+=#[0-9A-F]{6}")
    found = dict(line.split("=") for line in text.splitlines() if line and not line.startswith("#"))
    if found != properties(theme["palette"]):
        raise ValueError("differs from heritage.terminals.termux.properties")


def pairs(p):
    return [pair for pair in standard_pairs(p) if pair[0] in ("text", "bright text", "cursor") or
            pair[0].startswith("colour")]
