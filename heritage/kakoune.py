"""Kakoune colour scheme generated from a palette.

A colour scheme sets faces: the code and markup faces that Kakoune's language scripts highlight with, and the built-in
faces of :doc faces. The language scripts give each construct one of 13 code faces, so a face covers constructs that
the other targets tell apart: meta takes the keyword role, as it marks Java annotations as well as Python's import and
C's #include, the way Vim's PreProc does; attribute takes the annotation role, as the Zed and Helix themes give the
attribute capture, so Python decorators and HTML attribute names take it, and so do Java's modifiers. value is
numbers and literals such as true and null, and takes the number role.

The built-in faces follow the Islands layout of the other targets: the status line on the frame, the editor on bg, and
menus and information boxes on surface. Selections set only a background, so code keeps its colours under them.
Kakoune draws a face's unset colours in the colours of the face under it.
"""
import re

from .nvim import name  # noqa: F401 - Kakoune lists a scheme by the same name as Neovim

ATTRIBUTES = {"bold": "b", "italic": "i", "underline": "u", "curl": "c", "dim": "d", "reverse": "r",
              "strikethrough": "s", "final": "F", "final_fg": "f"}
FONTS = {"": [], "bold": ["bold"], "italic": ["italic"], "bold italic": ["bold", "italic"]}
# The built-in faces of Kakoune 2026.04 (:doc faces).
UI_FACES = (
    "Default", "PrimarySelection", "SecondarySelection", "PrimaryCursor", "SecondaryCursor", "PrimaryCursorEol",
    "SecondaryCursorEol", "MenuForeground", "MenuBackground", "MenuInfo", "Information", "InlineInformation", "Error",
    "DiagnosticError", "DiagnosticWarning", "StatusLine", "StatusLineMode", "StatusLineInfo", "StatusLineValue",
    "StatusCursor", "Prompt", "BufferPadding", "LineNumbers", "LineNumberCursor", "LineNumbersWrapped",
    "MatchingChar", "Whitespace", "WrapMarker",
)
# The faces that the language scripts highlight code and markup with.
SYNTAX_FACES = ("value", "type", "variable", "module", "function", "string", "keyword", "operator", "attribute",
                "comment", "documentation", "meta", "builtin", "title", "header", "mono", "block", "link", "bullet",
                "list")
# Faces drawn as gutter marks, filler or whitespace rather than text, so the contrast check leaves them out.
DECORATIVE = {"BufferPadding", "LineNumbers", "LineNumberCursor", "LineNumbersWrapped", "Whitespace", "WrapMarker"}
# Faces held to 3:1 rather than 4.5:1: comments, and the primary cursor and the prompt's cursor, which the build checks
# as the caret.
LOW_CONTRAST = {"comment", "PrimaryCursor", "PrimaryCursorEol", "StatusCursor"}
# Faces without a background of their own that Kakoune draws on the background of other faces rather than on
# Default's, with the minimum contrast on each.
DRAWN_ON = {}


def syntax_rules(p):
    """(face, role, font style) per code and markup face."""
    kw = "bold" if p.get("kwBold", not p["dark"]) else ""
    rules = []
    def s(faces, role, font=""):
        rules.extend((face, role, font) for face in faces.split())
    s("value", "number")
    s("type", "type")
    s("variable", "field")
    s("module", "fg")
    s("function", "call")
    s("builtin", "call", "italic")
    s("string mono block", "string")
    s("keyword meta bullet list", "keyword", kw)
    s("operator", "op")
    s("attribute", "annotation")
    s("comment", "comment", "italic")
    s("documentation", "doc", "italic")
    # Markdown: headings take the declaration role, markers the keyword role
    s("title header", "method", "bold")
    s("link", "azure")
    return rules


def ui(p):
    """Built-in face to style, with #-prefixed colours."""
    c = {k: "#" + v for k, v in p.items() if isinstance(v, str) and re.fullmatch(r"[0-9A-F]{6}", v)}
    caret = "#" + p.get("caret", p["gold"])
    return {
        # editor. Cursors are blocks with the character under them in bg; the primary one takes the caret colour.
        "Default": dict(fg=c["fg"], bg=c["bg"]),
        "PrimarySelection": dict(bg=c["selection"]), "SecondarySelection": dict(bg=c["selInactive"]),
        "PrimaryCursor": dict(fg=c["bg"], bg=caret, attributes=["final_fg"]),
        "PrimaryCursorEol": dict(fg=c["bg"], bg=caret, attributes=["final_fg"]),
        "SecondaryCursor": dict(fg=c["bg"], bg=c["muted"], attributes=["final_fg"]),
        "SecondaryCursorEol": dict(fg=c["bg"], bg=c["muted"], attributes=["final_fg"]),
        "LineNumbers": dict(fg=c["lineNo"], bg=c["bg"]), "LineNumberCursor": dict(fg=c["lineNoCaret"], bg=c["bg"]),
        "LineNumbersWrapped": dict(fg=c["guide"], bg=c["bg"]),
        "BufferPadding": dict(fg=c["lineNo"], bg=c["bg"]),
        "MatchingChar": dict(bg=c["braceBg"], attributes=["bold"]),
        "Whitespace": dict(fg=c["guide"], attributes=["final_fg"]), "WrapMarker": dict(fg=c["guide"]),
        # diagnostics of lint and other tools: the ANSI colours, which the build checks at 4.5:1 against bg, with an
        # undercurl in the diagnostic colours of the other targets
        "DiagnosticError": dict(fg=c["ansiRed"], underline=c["error"], attributes=["curl"]),
        "DiagnosticWarning": dict(fg=c["ansiYellow"], underline=c["warning"], attributes=["curl"]),
        # frame: the status line, the mode as the Helix theme draws it, and the prompt
        "StatusLine": dict(fg=c["fg"], bg=c["frame"]),
        "StatusLineMode": dict(fg=c["bg"], bg=c["ansiGreen"], attributes=["bold"]),
        "StatusLineInfo": dict(fg=c["muted"], bg=c["frame"]),
        "StatusLineValue": dict(fg=c["fg"], bg=c["frame"], attributes=["bold"]),
        "StatusCursor": dict(fg=c["bg"], bg=caret),
        "Prompt": dict(fg=c["fg"], bg=c["frame"], attributes=["bold"]),
        "Error": dict(fg=c["redText"], bg=c["red"]),
        # popups: menus and information boxes
        "MenuBackground": dict(fg=c["fg"], bg=c["surface"]), "MenuForeground": dict(fg=c["fg"], bg=c["selection"]),
        # The information beside an item shows on unselected and selected items alike, where muted is too faint, so
        # it keeps the item's colour and sets itself apart in italics.
        "MenuInfo": dict(attributes=["italic"]),
        "Information": dict(fg=c["fg"], bg=c["surface"]), "InlineInformation": dict(fg=c["fg"], bg=c["surface"]),
    }


def styles(p):
    """Every face of the scheme: built-in faces first, then code and markup faces."""
    out = ui(p)
    for face, role, font in syntax_rules(p):
        if face in out:
            raise ValueError(f"{face} is set twice")
        out[face] = dict(fg="#" + p[role], **({"attributes": FONTS[font]} if font else {}))
    return out


def face(style):
    """A face value: fg,bg,underline colour and attributes, with Kakoune's default for an unset colour."""
    colours = [style.get(key) for key in ("fg", "bg", "underline")]
    while colours and colours[-1] is None:
        colours.pop()
    value = ",".join(f"rgb:{c[1:]}" if c else "default" for c in colours) or "default"
    attributes = "".join(ATTRIBUTES[a] for a in style.get("attributes", []))
    return value + (f"+{attributes}" if attributes else "")


def colorscheme(p, source):
    """The colors/<scheme>.kak file for a palette. source is the URL of the theme folder."""
    lines = [
        f"# {p['name']}: a Heritage Themes colour scheme for Kakoune.",
        f"# Generated from {source}; changes here are overwritten.",
        "",
        *(f"set-face global {key} {face(style)}" for key, style in styles(p).items()),
    ]
    return "\n".join(lines) + "\n"
