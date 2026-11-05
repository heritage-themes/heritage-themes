"""XTerm colours: X resources for the VT100 widget of xterm and uxterm, merged with xrdb or included in
~/.Xresources."""
from . import check_lines, colours, header, name, standard_pairs

APP = "XTerm"
FOLDER = "xterm"
CATEGORY = "Terminal emulators"
INSTALL = """Load a theme's resources into the X server, then start a new `xterm` or `uxterm`:

```bash
xrdb -merge xterm/{stem}.Xresources
```

To keep it, copy the file's lines into `~/.Xresources`, which most X sessions load at login. The resources apply to \
the VT100 widget of `xterm` and `uxterm`, colouring the terminal, the cursor, the pointer and selections."""


def resources(p):
    """VT100 widget resource → #RRGGBB."""
    c = colours(p)
    out = {"foreground": c["fg"], "background": c["bg"], "cursorColor": c["cursor"], "pointerColor": c["fg"],
           "pointerColorBackground": c["bg"], "highlightColor": c["selection_bg"],
           "highlightTextColor": c["selection_fg"]}
    out.update({f"color{i}": colour for i, colour in enumerate(c["ansi"])})
    return out


def files(theme, source):
    p = theme["palette"]
    lines = [*header(p, APP, source, "!"),
             # draw selections in the selection colours rather than in reverse video, and reverse video as text and
             # background swapped rather than in the selection colours
             "*VT100.highlightColorMode: true", "*VT100.highlightReverse: false",
             *(f"*VT100.{key}: {value}" for key, value in resources(p).items())]
    return [(f"{name(theme)}.Xresources", "\n".join(lines) + "\n")]


def validate(theme, text):
    check_lines(text, r"\*VT100\.\w+: (?:#[0-9A-F]{6}|true|false)", "!")
    found = dict(line[len("*VT100."):].split(": ") for line in text.splitlines() if line.startswith("*VT100."))
    if found != {"highlightColorMode": "true", "highlightReverse": "false", **resources(theme["palette"])}:
        raise ValueError("differs from heritage.terminals.xterm.resources")


def pairs(p):
    return [pair for pair in standard_pairs(p) if "search" not in pair[0]]
