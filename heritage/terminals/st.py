"""st colours: the colour definitions of st's config.h, which st compiles in."""
import re

from . import colours, header, name, standard_pairs

APP = "st"
FOLDER = "st"
CATEGORY = "Terminal emulators"
INSTALL = """st compiles its colours in. In `config.h` of st 0.9, replace the `colorname` array and the four default \
colour indices that follow it, from `static const char *colorname[]` to `static unsigned int defaultrcs = 257;`, \
with the contents of a theme's file, such as `st/{stem}.h`, then rebuild and install st:

```bash
make clean install
```

Each theme colours the terminal and the cursor."""


def files(theme, source):
    p = theme["palette"]
    c = colours(p)
    lines = [
        *(f"/* {line[2:]} */" for line in header(p, APP, source)),
        "/* Replace the colorname array and the default colour indices in config.h with these, then rebuild st. */",
        "static const char *colorname[] = {",
        "\t/* 8 normal colors */",
        *(f'\t"{colour}",' for colour in c["ansi"][:8]),
        "",
        "\t/* 8 bright colors */",
        *(f'\t"{colour}",' for colour in c["ansi"][8:]),
        "",
        "\t[255] = 0,",
        "",
        "\t/* more colors can be added after 255 to use with DefaultXX */",
        f'\t"{c["cursor"]}", /* 256: cursor */',
        f'\t"{c["cursor_text"]}", /* 257: reverse cursor */',
        f'\t"{c["fg"]}", /* 258: default foreground colour */',
        f'\t"{c["bg"]}", /* 259: default background colour */',
        "};",
        "",
        "unsigned int defaultfg = 258;",
        "unsigned int defaultbg = 259;",
        "unsigned int defaultcs = 256;",
        "static unsigned int defaultrcs = 257;",
    ]
    return [(f"{name(theme)}.h", "\n".join(lines) + "\n")]


def validate(theme, text):
    c = colours(theme["palette"])
    found = re.findall(r'"(#[0-9A-F]{6})"', text)
    if found != [*c["ansi"], c["cursor"], c["cursor_text"], c["fg"], c["bg"]]:
        raise ValueError("does not list the 16 colours, then the cursor, reverse cursor, foreground and background")
    for line in ("unsigned int defaultfg = 258;", "unsigned int defaultbg = 259;", "unsigned int defaultcs = 256;",
                 "static unsigned int defaultrcs = 257;"):
        if line not in text.splitlines():
            raise ValueError(f"lacks {line}")


def pairs(p):
    return [pair for pair in standard_pairs(p) if pair[0] in ("text", "bright text", "cursor", "text under the cursor")
            or pair[0].startswith("colour")]
