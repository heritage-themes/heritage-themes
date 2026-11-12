"""Spyder syntax highlighting themes generated from a palette: one INI file for each Heritage theme.

A Spyder theme is the 18 options that Spyder keeps under `<theme>/` in the [appearance] section of its spyder.ini: the
theme's name, six backgrounds and highlights, a link colour, and a colour with bold and italic flags for each of nine
kinds of text. Spyder paints its editor and its IPython console from one theme. It draws its own menus, tabs, panes and
icons in a fixed light or dark interface theme, so a Heritage theme colours the code and the surfaces behind it, not the
application around them.

The roles are those that heritage.textadept and heritage.pygments give the matching constructs. Spyder's Python
highlighter has one colour for each of these: `keyword` for keywords, `builtin` for builtin functions, `definition`
for the name after def and class, `instance` for self, cls and decorators, and `magic` for IPython's %magic lines. The
backgrounds are those of the matching Neovim, VS Code and Eclipse elements: braceBg behind a matching bracket,
underCaret behind the other occurrences of the word under the caret. A bracket with no partner takes writeCaret, the
red tint that those apps use for a write access. Spyder keeps a character's text colour on each of these backgrounds,
so the build checks the text colour on them.

A theme is registered under `custom_names`, Spyder's list of the themes its users made: Spyder lets a user edit and
delete those, and offers no reset for them, because they have no defaults to reset to. A name in `names` would get a
Reset to defaults button that fails for a theme that Spyder does not ship. Spyder's Create new theme button reads
every custom name as `custom-<number>` and fails on any other, which no name here can avoid without breaking the
selected theme when the set of themes changes.
"""
import re

from .nvim import name  # noqa: F401 - Spyder lists a theme by the same name as Neovim

# The keys of a theme, in the order that a theme file lists them.
KEYS = ("name", "background", "currentline", "currentcell", "occurrence", "ctrlclick", "sideareas", "matched_p",
        "unmatched_p", "normal", "keyword", "builtin", "definition", "comment", "string", "number", "instance",
        "magic")
# The keys that hold a colour with bold and italic flags, as a (colour, bold, italic) tuple.
TEXT_KEYS = KEYS[KEYS.index("normal"):]
# A value that Spyder reads: a colour, or a tuple of a colour and two flags.
COLOUR = re.compile(r"#[0-9A-F]{6}")
TEXT = re.compile(r"\('#[0-9A-F]{6}', (True|False), (True|False)\)")


def roles(p):
    """key → palette role of its colour, for the keys that are backgrounds and highlights."""
    return {"background": "bg", "currentline": "caretRow", "currentcell": "hover", "occurrence": "underCaret",
            "ctrlclick": "azure", "sideareas": "bg", "matched_p": "braceBg", "unmatched_p": "writeCaret"}


def text_rules(p):
    """key → (role, bold, italic) for the keys that are text."""
    kw = bool(p.get("kwBold", not p["dark"]))
    return {"normal": ("fg", False, False), "keyword": ("keyword", kw, False), "builtin": ("call", False, True),
            "definition": ("method", True, False), "comment": ("comment", False, True),
            "string": ("string", False, False), "number": ("number", False, False),
            "instance": ("keyword", False, True), "magic": ("keyword", kw, False)}


def options(p):
    """key → value as Spyder stores it, in KEYS order: a name, a colour, or a (colour, bold, italic) tuple."""
    out = {"name": p["name"]}
    out.update({key: f"#{p[role]}" for key, role in roles(p).items()})
    out.update({key: f"('#{p[role]}', {bold}, {italic})" for key, (role, bold, italic) in text_rules(p).items()})
    return {key: out[key] for key in KEYS}


def theme(p, theme_name, source):
    """The themes/<theme>.ini file for a palette. source is the URL of the theme folder."""
    lines = [
        f"; {p['name']}: a Heritage Themes syntax highlighting theme for Spyder.",
        f"; Generated from {source}; changes here are overwritten.",
        "[appearance]",
        *(f"{theme_name}/{key} = {value}" for key, value in options(p).items()),
    ]
    return "\n".join(lines) + "\n"


def styles(p):
    """key → dict(fg, bg) as #RRGGBB for the build's contrast check: each kind of text on the editor's background and on
    the current line, the link colour on the background, and normal text on the four backgrounds that Spyder draws
    under it."""
    out = {}
    for key, (role, _, _) in text_rules(p).items():
        out[key] = dict(fg="#" + p[role], bg="#" + p["bg"])
        out[f"{key} on current line"] = dict(fg="#" + p[role], bg="#" + p["caretRow"])
    out["ctrlclick"] = dict(fg="#" + p["azure"], bg="#" + p["bg"])
    for key in ("currentcell", "occurrence", "matched_p", "unmatched_p"):
        out[f"normal on {key}"] = dict(fg="#" + p["fg"], bg="#" + p[roles(p)[key]])
    return out


# The styles that need 3:1 only: comments, as in every target, and the one character that a bracket highlight sits on.
LOW_CONTRAST = {"comment", "comment on current line", "normal on matched_p"}


def parse(text):
    """key → value of a theme file's options, with the theme's name in front of each key removed."""
    return {option.split("/", 1)[1]: value.strip()
            for option, value in re.findall(r"^([^;#\[=\s][^=]*?) = (.*)$", text, re.M)}
