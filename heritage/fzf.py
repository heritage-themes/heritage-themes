"""fzf theme generated from a palette: an options file of --color lines, which fzf reads at start when
FZF_DEFAULT_OPTS_FILE names it.

fzf draws on the terminal's own background and text colour, so the theme names the base scheme that matches the
palette's background, dark or light, keeps the terminal's colours for text, the query and the current line's text, and
reads as intended in a terminal that runs the matching theme of the Terminals product. The current line takes
selection, as a selected row does in every target, and so does the gutter beside the list, which fzf draws in the
current line's colour unless a theme sets one of its own. The matched characters of every line take the theme's
accent, the syntax role that heritage.yazi.accent() picks for a file browser's folders, so that each family shows its
own colours where fzf draws most colour. The prompt, the pointer at the current line and the spinner take a second
syntax role, which pointer() picks to stand apart from the accent, the text and the marker. The marker of a selected
line takes ansiMagenta, as yazi's select mode does. The match counters and the header take muted, the palette's
secondary text, and borders and the scroll bar muted too, as the panel borders of lazygit and the box outlines of btop
do. The separator on the info line takes border, the palette's separator colour, and border labels the text colour.

fzf exits with an error on a colour name it does not know, so the theme uses only the names that fzf 0.55 accepts, the
first release that allows comments in FZF_DEFAULT_OPTS_FILE, which the theme opens with. The colours that later
releases added, such as those of the list, input, header and footer borders, inherit the ones the theme sets.
"""
from .colour import contrast, distance
from .nvim import name  # noqa: F401 - the theme's file is named as Neovim names a scheme
from .yazi import accent

# The first fzf release that allows comments in FZF_DEFAULT_OPTS_FILE, whose colour names the theme keeps to, and the
# one the previews run.
MINIMUM_VERSION, TESTED_VERSION = "0.55", "0.75.0"
# The colour names that fzf 0.55 accepts in --color, from parseTheme in its src/options.go. A later release also
# accepts these.
COLOUR_NAMES = ("query", "input", "disabled", "fg", "bg", "preview-fg", "preview-bg", "current-fg", "fg+",
                "current-bg", "bg+", "selected-fg", "selected-bg", "gutter", "hl", "current-hl", "hl+", "selected-hl",
                "border", "preview-border", "separator", "scrollbar", "preview-scrollbar", "label", "preview-label",
                "prompt", "spinner", "info", "pointer", "marker", "header")
# fzf's base schemes, which a --color value can start with.
BASE_SCHEMES = ("dark", "light", "16", "bw")
# The text attributes that fzf 0.55 accepts after a colour.
ATTRIBUTES = ("regular", "bold", "dim", "italic", "underline", "blink", "reverse", "strikethrough")
# The roles that the pointer chooses from, in order: the palette's syntax roles, led by label, then ansiBlue. The
# pointer is the first that suits; see pointer().
POINTERS = ("label", "caret", "method", "constant", "string", "type", "keyword", "number", "field", "call",
            "directive", "annotation", "typeParam", "ansiBlue")
# The least CIE76 distance between the pointer and the accent, the text colour and the marker.
POINTER_DISTANCE = 25
# The role of the marker of a selected line.
MARKER = "ansiMagenta"


def pointer(p):
    """The palette role of the prompt, the pointer and the spinner: the first of POINTERS that reads at 4.5:1 on bg,
    where the prompt and the spinner are drawn, and at 3:1 on selection, where the pointer is, and stands
    POINTER_DISTANCE apart from the accent, the text colour and the marker. A palette with no such role, one that
    builds its hierarchy from tone rather than hue, takes the accent."""
    taken = (p[accent(p)], p["fg"], p[MARKER])
    def fits(role):
        return (role in p and contrast(p[role], p["bg"]) >= 4.5 and contrast(p[role], p["selection"]) >= 3
                and all(distance(p[role], colour) >= POINTER_DISTANCE for colour in taken))
    return next((role for role in POINTERS if fits(role)), accent(p))


def settings(p):
    """fzf colour name → palette role, or "-1" for the terminal's own colour, in the order of fzf's man page."""
    return {
        "fg": "-1", "bg": "-1", "hl": accent(p),
        "fg+": "-1", "bg+": "selection", "gutter": "selection", "hl+": accent(p),
        "query": "-1", "info": "muted",
        "border": "muted", "separator": "border", "scrollbar": "muted", "label": "-1",
        "prompt": pointer(p), "pointer": pointer(p), "marker": MARKER, "spinner": pointer(p), "header": "muted",
    }


def colours(p):
    """fzf colour name → #RRGGBB, or "-1" for the terminal's own colour."""
    return {key: role if role == "-1" else "#" + p[role] for key, role in settings(p).items()}


def base(p):
    """The base scheme that the theme starts from: dark for a dark palette, light for a light one."""
    return "dark" if p["dark"] else "light"


def theme(p, source):
    """The themes/<theme>.fzfrc file for a palette: the base scheme, then one colour per --color option, so a line
    names one setting. source is the URL of the theme folder."""
    lines = [f"# {p['name']}: {source}",
             f"# For a terminal with a {'dark' if p['dark'] else 'light'} background; needs fzf {MINIMUM_VERSION} "
             "or later.", f"--color={base(p)}"]
    lines += [f"--color={key}:{value}" for key, value in colours(p).items()]
    return "\n".join(lines) + "\n"


def styles(p):
    """(element, foreground, background, minimum contrast) as #RRGGBB, for the build's check: text at 4.5:1 and
    graphics at 3:1, on the terminal's background, which is bg in the matching Terminals theme, or on the current
    line. The separator is a rule between sections that the prompt line already sets apart, so it is not held."""
    c = colours(p)
    bg, current = "#" + p["bg"], c["bg+"]
    text = "#" + p["fg"]
    return [("text", text, bg, 4.5), ("matched characters", c["hl"], bg, 4.5),
            ("current line", text, current, 4.5), ("matched characters on the current line", c["hl+"], current, 4.5),
            ("pointer", c["pointer"], current, 3), ("marker", c["marker"], bg, 3),
            ("marker on the current line", c["marker"], current, 3), ("prompt", c["prompt"], bg, 4.5),
            ("spinner", c["spinner"], bg, 3), ("match counters", c["info"], bg, 4.5),
            ("header", c["header"], bg, 4.5), ("border", c["border"], bg, 3), ("scroll bar", c["scrollbar"], bg, 3)]
