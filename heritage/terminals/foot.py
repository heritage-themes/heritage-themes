"""foot theme: an INI file that foot.ini includes from its [main] section. The colours go in [colors-dark] for a dark
theme and [colors-light] for a light one, which foot's initial-color-theme chooses between, so a dark and a light theme
can be included together and switched with foot's color-theme-toggle key binding."""
import configparser

from . import colours, header, name, standard_pairs

APP = "foot"
FOLDER = "foot"
CATEGORY = "Terminal emulators"
INSTALL = """Copy the files in `foot` into `~/.config/foot/themes` and include a theme from the `[main]` section of \
`foot.ini`. foot 1.26 or later is required. A dark theme sets foot's dark colours and a light theme its light ones, so \
choose a light theme with `initial-color-theme=light`:

```ini
[main]
include=~/.config/foot/themes/{light_stem}.ini
initial-color-theme=light
```

Include a dark and a light theme together to switch between them with the `color-theme-toggle` key binding, \
starting with the one that `initial-color-theme` names. Each theme colours the terminal, the cursor, selections, the \
search box, jump labels, URLs, the scrollback indicator and the flash."""


def options(p):
    """foot colour option → value, colours as RRGGBB."""
    c = {k: (v[1:] if isinstance(v, str) else [x[1:] for x in v]) for k, v in colours(p).items()}
    out = {"foreground": c["fg"], "background": c["bg"]}
    out.update({f"regular{i}": colour for i, colour in enumerate(c["ansi"][:8])})
    out.update({f"bright{i}": colour for i, colour in enumerate(c["ansi"][8:])})
    out.update({f"dim{i}": colour for i, colour in enumerate(c["dim"])})
    out.update({
        "cursor": f"{c['cursor_text']} {c['cursor']}",
        "selection-foreground": c["selection_fg"], "selection-background": c["selection_bg"],
        "search-box-no-match": f"{c['bg']} {c['ansi'][1]}",
        "search-box-match": f"{c['match_fg']} {c['match_bg']}",
        "jump-labels": f"{c['focused_match_fg']} {c['focused_match_bg']}",
        "scrollback-indicator": f"{c['fg']} {c['bar_bg']}",
        "urls": c["link"], "flash": c["bell"],
    })
    return out


def files(theme, source):
    p = theme["palette"]
    lines = [*header(p, APP, source), "", f"[colors-{'dark' if p['dark'] else 'light'}]",
             *(f"{key}={value}" for key, value in options(p).items())]
    return [(f"{name(theme)}.ini", "\n".join(lines) + "\n")]


def validate(theme, text):
    parser = configparser.ConfigParser(interpolation=None)
    parser.optionxform = str
    parser.read_string(text)
    p = theme["palette"]
    if parser.sections() != [f"colors-{'dark' if p['dark'] else 'light'}"] or \
            dict(parser[parser.sections()[0]]) != options(p):
        raise ValueError("differs from heritage.terminals.foot.options")


def pairs(p):
    c = colours(p)
    return [*standard_pairs(p), ("scrollback indicator", c["fg"], c["bar_bg"], 4.5),
            ("search box without a match", c["bg"], c["ansi"][1], 4.5)]
