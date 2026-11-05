"""Starship palette: a palette table and the palette option for starship.toml. The palette redefines the colour names
that Starship's modules use, so the default prompt and a configuration that names colours take the theme's ANSI
colours, and adds the theme's text, muted, background and surface colours under those names."""
import tomllib

from . import ANSI_NAMES, colours, header, name, standard_pairs

APP = "Starship"
FOLDER = "starship"
CATEGORY = "Prompts"
INSTALL = """Copy a theme's lines into `~/.config/starship.toml`: the `palette` line at the top, before any table, and \
the `[palettes.…]` table anywhere after it. Starship then draws its modules in the theme's colours, both the default \
prompt and a configuration of your own that names colours such as `bold green`. A style of your own can also name the \
palette's `text`, `muted`, `background` and `surface` colours."""


def palette(p):
    """Colour name → #RRGGBB. Starship calls magenta purple."""
    c = colours(p)
    names = [n.replace("magenta", "purple") for n in ANSI_NAMES]
    out = dict(zip(names, c["ansi"][:8]))
    out.update({f"bright-{n}": colour for n, colour in zip(names, c["ansi"][8:])})
    out.update({"text": c["fg"], "muted": c["muted"], "background": c["bg"], "surface": c["surface"]})
    return out


def palette_name(theme):
    return name(theme).replace("-", "_")


def files(theme, source):
    p = theme["palette"]
    lines = [*header(p, APP, source), "# Add these lines to starship.toml; the palette option goes before any table.",
             f'palette = "{palette_name(theme)}"', "", f"[palettes.{palette_name(theme)}]",
             *(f'{key} = "{value}"' for key, value in palette(p).items())]
    return [(f"{name(theme)}.toml", "\n".join(lines) + "\n")]


def validate(theme, text):
    data = tomllib.loads(text)
    if data != {"palette": palette_name(theme), "palettes": {palette_name(theme): palette(theme["palette"])}}:
        raise ValueError("differs from heritage.terminals.starship.palette")


def pairs(p):
    return [pair for pair in standard_pairs(p) if pair[0] == "text" or pair[0].startswith("colour")]
