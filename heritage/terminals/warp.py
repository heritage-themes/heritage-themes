"""Warp theme: a YAML file in Warp's themes folder, which Settings | Appearance | Themes lists by its name."""
from . import ANSI_NAMES, colours, header, name, standard_pairs, yaml as parse_yaml

APP = "Warp"
FOLDER = "warp"
CATEGORY = "Terminal emulators"
INSTALL = """Copy the files in `warp` into Warp's themes folder, creating it if it does not exist: \
`~/.warp/themes` on macOS, `~/.local/share/warp-terminal/themes` on Linux and \
`%LocalAppData%\\warp\\Warp\\data\\themes` on Windows. Then choose a theme, for example **{label}**, under \
**Settings | Appearance | Themes**.

Each theme colours the terminal, the cursor and Warp's accent, and Warp shades its panels from the theme's \
background."""


def theme_data(p):
    c = colours(p)
    return {
        "name": p["name"],
        "accent": c["active_border"], "cursor": c["cursor"],
        "background": c["bg"], "foreground": c["fg"],
        # Warp derives its panels from the background: darker for a dark theme, lighter for a light one
        "details": "darker" if p["dark"] else "lighter",
        "terminal_colors": {"normal": dict(zip(ANSI_NAMES, c["ansi"][:8])),
                            "bright": dict(zip(ANSI_NAMES, c["ansi"][8:]))},
    }


def files(theme, source):
    p = theme["palette"]
    data = theme_data(p)
    lines = header(p, APP, source)
    for key, value in data.items():
        if isinstance(value, dict):
            lines.append(f"{key}:")
            for group, colours_ in value.items():
                lines.append(f"  {group}:")
                lines += [f"    {n}: '{colour}'" for n, colour in colours_.items()]
        else:
            lines.append(f"{key}: '{value}'")
    return [(f"{name(theme)}.yaml", "\n".join(lines) + "\n")]


def validate(theme, text):
    if parse_yaml(text) != theme_data(theme["palette"]):
        raise ValueError("differs from heritage.terminals.warp.theme_data")


def pairs(p):
    c = colours(p)
    return [*(pair for pair in standard_pairs(p) if "search" not in pair[0] and pair[0] != "selection"),
            ("accent", c["active_border"], c["bg"], 3)]
