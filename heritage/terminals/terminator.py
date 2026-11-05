"""Terminator profile: the [global_config] title bar colours and a [[profile]] for the [profiles] section of
~/.config/terminator/config. Terminator keeps the title bar colours outside profiles, so they apply to every profile."""
from . import check_lines, colours, header, name, standard_pairs

APP = "Terminator"
FOLDER = "terminator"
CATEGORY = "Terminal emulators"
INSTALL = """Terminator keeps every profile in one file, so merge a theme's file into `~/.config/terminator/config`: \
its title bar colours into the `[global_config]` section and its profile, for example `[[{label}]]`, into the \
`[profiles]` section, adding either section if it is missing. Then choose the profile in **Preferences | Profiles** or \
from the terminal's context menu.

Each theme colours the terminal, the cursor and the title bars of split terminals. The title bar colours apply to every \
profile."""


def title_bars(p):
    """Global option → colour. The focused terminal's title bar takes the red accent with which the other targets mark
    the active tab; terminals receiving broadcast input take the blue accent; the others sit on the frame."""
    c = colours(p)
    red = "#" + p["red"]
    return {
        "title_transmit_fg_color": "#" + p["redText"], "title_transmit_bg_color": red,
        "title_receive_fg_color": c["bg"], "title_receive_bg_color": c["active_border"],
        "title_inactive_fg_color": c["muted"], "title_inactive_bg_color": c["bar_bg"],
    }


def options(p):
    """Profile option → value, quoted as Terminator writes them."""
    c = colours(p)
    return {
        "use_theme_colors": "False",
        "background_color": f'"{c["bg"]}"', "foreground_color": f'"{c["fg"]}"',
        "cursor_color_default": "False", "cursor_bg_color": f'"{c["cursor"]}"',
        "cursor_fg_color": f'"{c["cursor_text"]}"',
        "palette": '"' + ":".join(c["ansi"]) + '"',
        "bold_is_bright": "False",
    }


def files(theme, source):
    p = theme["palette"]
    lines = [*header(p, APP, source), "[global_config]",
             *(f'  {key} = "{value}"' for key, value in title_bars(p).items()),
             "[profiles]", f"  [[{p['name']}]]",
             *(f"    {key} = {value}" for key, value in options(p).items())]
    return [(f"{name(theme)}.config", "\n".join(lines) + "\n")]


def validate(theme, text):
    check_lines(text, r'(\[global_config\]|\[profiles\]|  \[\[[^\]]+\]\]|  \w+ = "#[0-9A-F]{6}"|    \w+ = .+)')
    p = theme["palette"]
    profile = text.split(f"  [[{p['name']}]]\n", 1)[1]
    found = dict(line.strip().split(" = ", 1) for line in profile.splitlines())
    if found != options(p):
        raise ValueError("differs from heritage.terminals.terminator.options")


def pairs(p):
    bars = title_bars(p)
    return [*(pair for pair in standard_pairs(p) if pair[0] not in ("selection", "search match", "focused search match")),
            ("focused title bar", bars["title_transmit_fg_color"], bars["title_transmit_bg_color"], 4.5),
            ("receiving title bar", bars["title_receive_fg_color"], bars["title_receive_bg_color"], 4.5),
            ("inactive title bar", bars["title_inactive_fg_color"], bars["title_inactive_bg_color"], 4.5)]
