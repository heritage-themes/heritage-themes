"""iTerm2 colour preset: an .itermcolors property list, imported under Settings | Profiles | Colors | Color Presets."""
import plistlib

from . import colours, standard_pairs

APP = "iTerm2"
FOLDER = "iterm2"
CATEGORY = "Terminal emulators"
INSTALL = """Open **Settings | Profiles | Colors**, choose **Color Presets… | Import…**, select the `.itermcolors` files \
in `iterm2`, then choose a preset, for example **{label}**, from **Color Presets…**.

Each preset colours the terminal, the cursor, the cursor guide, selections, links, the badge and the tab."""


def keys(p):
    """Preset key → #RRGGBB."""
    c = colours(p)
    out = {f"Ansi {i} Color": colour for i, colour in enumerate(c["ansi"])}
    out.update({
        "Background Color": c["bg"], "Foreground Color": c["fg"], "Bold Color": c["bright_fg"],
        "Cursor Color": c["cursor"], "Cursor Text Color": c["cursor_text"], "Cursor Guide Color": c["surface"],
        "Selection Color": c["selection_bg"], "Selected Text Color": c["selection_fg"],
        "Link Color": c["link"], "Underline Color": c["link"], "Badge Color": c["muted"],
        "Tab Color": c["bar_bg"],
    })
    return out


def component(colour):
    """An iTerm2 colour dictionary in sRGB."""
    r, g, b = (int(colour[i:i + 2], 16) / 255 for i in (1, 3, 5))
    return {"Alpha Component": 1.0, "Blue Component": b, "Color Space": "sRGB", "Green Component": g,
            "Red Component": r}


def files(theme, source):
    p = theme["palette"]
    data = {key: component(value) for key, value in sorted(keys(p).items())}
    # iTerm2 names an imported preset after the file
    return [(f"{p['name']}.itermcolors", plistlib.dumps(data).decode("utf-8"))]


def validate(theme, text):
    data = plistlib.loads(text.encode("utf-8"))
    expected = {key: component(value) for key, value in keys(theme["palette"]).items()}
    if data != expected:
        raise ValueError("differs from heritage.terminals.iterm2.keys")


def pairs(p):
    return standard_pairs(p)
