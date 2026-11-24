"""delta theme generated from a palette: a named feature in a Git configuration file that the user includes, which
sets delta's styles and names the theme's bat theme as its syntax theme.

delta highlights code with syntect, reading the themes from bat's cache, so the code takes heritage.bat's theme. The
feature colours what delta draws around the code. Removed and added lines keep their syntax colours on the palette's
diffDel and diffIns, as the IDEs' diff views do. Within those lines delta marks the changed words with the emph
styles: the line's background moved towards the gutter colour of the change, as far as the plain text colour keeps
4.5:1 on it, with that text colour, so the changed words stand out at every contrast. File names and the files of hunk
headers take keyword, as the diff headers of the VS Code and Sublime Text themes do; line numbers, the hunk box and
hints take muted, as bat's frame does; the numbers of removed and added lines take the terminal's red and green. delta
draws text on the terminal's own background, so the theme reads as intended in a terminal that runs the matching theme
of the Terminals product.
"""
from .nvim import name
from .terminals import contrast
from .vscode import mix
from . import textmate

# The file that holds every theme's feature, which the user includes from their Git configuration.
FILENAME = "heritage-themes.gitconfig"


def emphasis(p, line, gutter):
    """The background of changed words in a changed line: the line's background moved towards its gutter colour by up
    to 35 %, as far as fg keeps 4.5:1 on it."""
    for step in range(35, -1, -1):
        colour = mix(p[line], p[gutter], step / 100)
        if contrast(p["fg"], colour) >= 4.5:
            return colour
    raise ValueError(f"{p['name']}: fg is below 4.5:1 on {line}")


def settings(theme):
    """delta option → value as Git returns it, for the feature of a theme dict from a theme.py."""
    p = theme["palette"]
    def c(key):
        return "#" + p[key]
    return {
        "dark" if p["dark"] else "light": "true",
        "syntax-theme": name(theme),
        "minus-style": f"syntax {c('diffDel')}",
        "minus-emph-style": f"{c('fg')} #{emphasis(p, 'diffDel', 'deleted')}",
        "minus-empty-line-marker-style": f"normal {c('diffDel')}",
        "plus-style": f"syntax {c('diffIns')}",
        "plus-emph-style": f"{c('fg')} #{emphasis(p, 'diffIns', 'added')}",
        "plus-empty-line-marker-style": f"normal {c('diffIns')}",
        "whitespace-error-style": f"reverse {c('error')}",
        "file-style": c("keyword"),
        "file-decoration-style": f"{c('keyword')} ul",
        "hunk-header-decoration-style": f"{c('muted')} box",
        "hunk-header-file-style": c("keyword"),
        "hunk-header-line-number-style": c("muted"),
        "line-numbers-left-style": c("muted"),
        "line-numbers-right-style": c("muted"),
        "line-numbers-zero-style": c("muted"),
        "line-numbers-minus-style": c("ansiRed"),
        "line-numbers-plus-style": c("ansiGreen"),
        "grep-file-style": c("keyword"),
        "grep-line-number-style": c("muted"),
        "inline-hint-style": c("muted"),
        "blame-palette": f"{c('bg')} {c('caretRow')}",
    }


def feature(theme, source):
    """The [delta "<name>"] section of a theme dict. source is the URL of the theme folder. Git reads # as the start of
    a comment, so each colour is quoted."""
    lines = [f'[delta "{name(theme)}"]', f"    # {theme['palette']['name']}: {source}"]
    for key, value in settings(theme).items():
        value = " ".join(f'"{word}"' if word.startswith("#") else word for word in value.split())
        lines.append(f"    {key} = {value}")
    return "\n".join(lines) + "\n"


def config(themes):
    """The heritage-themes.gitconfig file. themes holds (theme dict, URL of its family's folder) pairs."""
    example = name(themes[0][0])
    header = f"""# Heritage Themes for delta: one feature for each theme, which names the theme's bat theme as its syntax theme.
# Include this file from your Git configuration and name a feature:
#
# [include]
#     path = PATH/TO/{FILENAME}
# [delta]
#     features = {example}
"""
    return header + "".join("\n" + feature(t, source) for t, source in themes)


def styles(theme):
    """Style → dict(fg, bg) as #RRGGBB, for the build's contrast check: code on blame's backgrounds and on removed and
    added lines, the changed words, and the text that delta draws on the terminal's background."""
    p = theme["palette"]
    # bat's styles hold the code on bg and on caretRow, the two backgrounds of blame-palette
    result = textmate.styles(p)
    result.update({f"{rule} on {line}": dict(style, bg="#" + p[line]) for rule, style in textmate.styles(p).items()
                   if style["bg"] == "#" + p["bg"] for line in ("diffDel", "diffIns")})
    def on_bg(key):
        return dict(fg="#" + p[key], bg="#" + p["bg"])
    for option, value in settings(theme).items():
        if option.endswith("-emph-style"):
            fg, bg = value.split()
            result[option] = dict(fg=fg, bg=bg)
    result.update({"file-style": on_bg("keyword"), "line numbers": on_bg("muted"),
                   "line-numbers-minus-style": on_bg("ansiRed"), "line-numbers-plus-style": on_bg("ansiGreen")})
    return result
