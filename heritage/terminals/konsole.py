"""Konsole colour scheme: a .colorscheme file in ~/.local/share/konsole, chosen under Edit Current Profile |
Appearance."""
import configparser

from . import colours, header, name, standard_pairs

APP = "Konsole"
FOLDER = "konsole"
CATEGORY = "Terminal emulators"
INSTALL = """Copy the files in `konsole` into `~/.local/share/konsole`, then choose a scheme, for example \
**{label}**, under **Settings | Edit Current Profile… | Appearance**.

Each scheme colours the terminal, with bold text in the bright colours and faint text in the faint ones. Konsole \
takes the cursor and selection colours from the profile and the system colours, not from the scheme."""


def rgb(colour):
    return ",".join(str(int(colour[i:i + 2], 16)) for i in (1, 3, 5))


def sections(p):
    """Section → colour. Konsole draws bold text in the intense colours and faint text in the faint ones."""
    c = colours(p)
    out = {"Background": c["bg"], "BackgroundFaint": c["bg"], "BackgroundIntense": c["bg"],
           "Foreground": c["fg"], "ForegroundFaint": c["dim_fg"], "ForegroundIntense": c["bright_fg"]}
    for i in range(8):
        out[f"Color{i}"] = c["ansi"][i]
        out[f"Color{i}Faint"] = c["dim"][i]
        out[f"Color{i}Intense"] = c["ansi"][i + 8]
    return out


def files(theme, source):
    p = theme["palette"]
    lines = header(p, APP, source)
    for section, colour in sorted(sections(p).items()):
        lines += ["", f"[{section}]", f"Color={rgb(colour)}"]
    lines += ["", "[General]", "Blur=false", "ColorRandomization=false", f"Description={p['name']}", "Opacity=1",
              "Wallpaper="]
    return [(f"{name(theme)}.colorscheme", "\n".join(lines) + "\n")]


def validate(theme, text):
    parser = configparser.ConfigParser(interpolation=None)
    parser.optionxform = str
    parser.read_string(text)
    p = theme["palette"]
    expected = {section: rgb(colour) for section, colour in sections(p).items()}
    found = {section: parser[section]["Color"] for section in parser.sections() if section != "General"}
    if found != expected or parser["General"]["Description"] != p["name"]:
        raise ValueError("differs from heritage.terminals.konsole.sections")


def pairs(p):
    return [pair for pair in standard_pairs(p) if pair[0] not in ("cursor", "text under the cursor", "selection")]
