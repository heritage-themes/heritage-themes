"""IDLE highlighting themes generated from a palette: one config file for each Heritage theme.

An IDLE theme is a section of the user's config-highlight.cfg: a foreground and a background colour for each of 16
elements, 31 options in all, as the cursor takes a foreground colour only. IDLE paints its editor, its shell and its
code context bar from one theme. It draws its own menus, dialogs and scroll bars with the platform's Tk theme, so a
Heritage theme colours the code and the surfaces behind it, not the application around them.

The roles are those that heritage.spyder and heritage.thonny give the matching constructs. IDLE's highlighter has one
colour for each of these: `keyword` for keywords, `builtin` for builtin names, `definition` for the name after def and
class, `string` and `comment`. It gives numbers, operators and every other name the normal colour, and has no bold or
italic. The backgrounds are those of the matching Neovim, VS Code and Thonny elements: searchBg behind found text,
writeCaret, the red tint that those apps use for a write access, behind a syntax error, and diffConf, their yellow
conflict tint, behind a line with a breakpoint. The shell takes the prompt from `muted`, errors from `ansiRed` and
leaves output in the text colour.

A theme is a custom theme, listed by IDLE under Options | Configure IDLE | Highlights | a Custom Theme, where a
user can edit and delete it. A section name is ASCII, because IDLE shows and stores it as it is.
"""
import re

from .sublime import basename

PREFIX = "Heritage "  # a theme's name in IDLE's list, so that the themes sit together among a user's own
COLOUR = re.compile(r"#[0-9A-F]{6}")


def name(t):
    """The name of a theme dict from a theme.py in IDLE's list, for example "Heritage Holi Night (Dark)"."""
    return PREFIX + basename(t["palette"]["name"])


def roles(p):
    """element → (foreground role, background role) of the colours that the element sets. The background of the text
    and the shell is bg; hilite is the selection, hit a find match, break a line with a breakpoint, error a syntax
    error, context the code context bar and linenumber the line number gutter."""
    return {"normal": ("fg", "bg"), "keyword": ("keyword", "bg"), "builtin": ("call", "bg"),
            "comment": ("comment", "bg"), "string": ("string", "bg"), "definition": ("method", "bg"),
            "hilite": ("fg", "selection"), "break": ("fg", "diffConf"), "hit": ("fg", "searchBg"),
            "error": ("fg", "writeCaret"), "context": ("fg", "surface"), "linenumber": ("lineNo", "bg"),
            "cursor": ("caret", None), "stdout": ("fg", "bg"), "stderr": ("ansiRed", "bg"),
            "console": ("muted", "bg")}


def colour(p, role):
    """The #RRGGBB of a palette role. The caret falls back to gold, as in the other products."""
    return "#" + (p.get("caret", p["gold"]) if role == "caret" else p[role])


def options(p):
    """option → #RRGGBB of a theme, in ELEMENTS order, each element's foreground and then its background."""
    out = {}
    for element, (foreground, background) in roles(p).items():
        out[f"{element}-foreground"] = colour(p, foreground)
        if background:
            out[f"{element}-background"] = colour(p, background)
    return out


def theme(p, theme_name, source):
    """The themes/<theme>.cfg file for a palette: one section. source is the URL of the theme folder."""
    lines = [
        f"# {p['name']}: a Heritage Themes highlighting theme for IDLE.",
        f"# Generated from {source}; changes here are overwritten.",
        f"[{theme_name}]",
        *(f"{option} = {value}" for option, value in options(p).items()),
    ]
    return "\n".join(lines) + "\n"


def styles(p):
    """element → dict(fg, bg) as #RRGGBB for the build's contrast check: each element's text on the background that
    IDLE draws it on, and the colours of the code on the editor's background."""
    return {element: dict(fg=colour(p, foreground), bg=colour(p, background or "bg"))
            for element, (foreground, background) in roles(p).items()}


# The elements that need 3:1 only: comments, as in every target, and the cursor, a shape.
LOW_CONTRAST = {"comment", "cursor"}
# The element that no contrast is required of: the line numbers, which are decorative in every target.
DECORATIVE = {"linenumber"}


def parse(text):
    """option → value of a theme file's options."""
    return {option: value.strip() for option, value in re.findall(r"^([a-z]+-(?:foreground|background)) = (.*)$", text,
                                                                  re.M)}
