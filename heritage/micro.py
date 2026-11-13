"""Micro colour scheme generated from a palette.

A colour scheme links groups to styles: the groups that Micro's syntax files highlight with and the UI groups of
:help colors. Micro colours a group with the longest group of the scheme that is a dot-separated prefix of it, so
"constant.string.url" takes "constant.string" unless the scheme sets it. The groups are named after Vim's syntax
groups, and take the roles that the Vim scheme gives them: statement the keyword role, special gold, and preproc, which
marks C's #include as well as HTML's <script> and Perl's use, the directive role of Vim's C preprocessor groups. The
syntax files use a group for whatever their language needs, so a group covers constructs that the other targets tell
apart: identifier marks Python's built-in functions, Rust's function declarations and HTML attribute names alike, and
takes the call role.

The UI groups follow the Islands layout of the other targets: the status line and tab bar on the frame, the editor on
bg, and the completion menu on surface. Micro draws a syntax group's background over the cursor line, so syntax groups
set no background; and it takes the foreground of cursor-line, color-column, indent-char, tab-error and trailingws as
the colour they draw. Selections and search matches replace the colours of the code under them.
"""
import re

from .nvim import name  # noqa: F401 - Micro lists a scheme by the same name as Neovim

FONTS = {"": [], "bold": ["bold"], "italic": ["italic"], "bold italic": ["bold", "italic"]}
STYLES = ("bold", "italic", "underline", "reverse")
# The UI groups that Micro 2.0.15 looks up (runtime/help/colors.md and internal/), but match-brace: without it, Micro
# draws a matching brace in reverse, bg on the brace's own colour, which every palette makes readable, as text on
# braceBg is not.
UI_GROUPS = (
    "default", "selection", "statusline", "statusline.inactive", "statusline.suggestions", "tabbar", "tabbar.active",
    "indent-char", "line-number", "current-line-number", "cursor-line", "color-column", "gutter-info", "gutter-error",
    "gutter-warning", "diff-added", "diff-modified", "diff-deleted", "scrollbar", "divider", "message",
    "error-message", "hlsearch", "tab-error", "trailingws",
)
# Groups whose foreground Micro draws as a background, or as a rule, gutter mark or filler rather than text, so the
# contrast check leaves them out.
DECORATIVE = {"indent-char", "line-number", "current-line-number", "cursor-line", "color-column", "diff-added",
              "diff-modified", "diff-deleted", "scrollbar", "divider", "tab-error", "trailingws", "ignore"}
# Groups held to 3:1 rather than 4.5:1: comments, and the shebang, which reads as one.
LOW_CONTRAST = {"comment", "preproc.shebang"}


def syntax_rules(p):
    """(group, role, font style) per syntax group."""
    kw = "bold" if p.get("kwBold", not p["dark"]) else ""
    rules = []
    def s(groups, role, font=""):
        rules.extend((group, role, font) for group in groups.split())
    s("comment", "comment", "italic")
    s("comment.bright", "doc", "italic")
    s("preproc.shebang", "comment", "bold italic")
    s("constant", "constant", "bold italic")
    s("constant.bool", "keyword", kw)
    s("constant.number", "number")
    s("constant.string constant.string.char", "string")
    s("constant.string.url", "call", "italic")
    s("constant.specialChar constant.unicode", "gold", "bold")
    s("identifier", "call")
    s("identifier.class", "type")
    s("identifier.var", "field")
    s("identifier.macro", "annotation")
    s("statement type.keyword symbol.tag", "keyword", kw)
    s("preproc", "directive")
    s("symbol symbol.operator symbol.brackets", "op")
    s("type", "type")
    s("special", "gold")
    s("todo", "todo", "bold italic")
    s("error", "ansiRed")
    return rules


def ui(p):
    """UI group to style, with #-prefixed colours."""
    c = {k: "#" + v for k, v in p.items() if isinstance(v, str) and re.fullmatch(r"[0-9A-F]{6}", v)}
    return {
        # editor. default comes first: Micro draws the colours that a group leaves out in default's.
        "default": dict(fg=c["fg"], bg=c["bg"]),
        "selection": dict(fg=c["fg"], bg=c["selection"]),
        "cursor-line": dict(fg=c["caretRow"]), "color-column": dict(fg=c["guide"]),
        "indent-char": dict(fg=c["guide"]),
        "line-number": dict(fg=c["lineNo"], bg=c["bg"]), "current-line-number": dict(fg=c["lineNoCaret"], bg=c["bg"]),
        "hlsearch": dict(fg=c["fg"], bg=c["searchBg"]),
        "tab-error": dict(fg=c["writeCaret"]), "trailingws": dict(fg=c["writeCaret"]),
        "underlined": dict(fg=c["azure"], styles=["underline"]), "ignore": dict(fg=c["disabled"]),
        # gutter: diagnostics in the ANSI colours, which the build checks at 4.5:1 against bg, and version control
        # marks in the VCS colours of the other targets' gutters
        "gutter-error": dict(fg=c["ansiRed"]), "gutter-warning": dict(fg=c["ansiYellow"]),
        "gutter-info": dict(fg=c["ansiBlue"]),
        "diff-added": dict(fg=c["added"]), "diff-modified": dict(fg=c["modified"]), "diff-deleted": dict(fg=c["deleted"]),
        # frame: status line, tab bar and divider. The active tab joins the editor, as in the Zed theme.
        "statusline": dict(fg=c["fg"], bg=c["frame"]), "statusline.inactive": dict(fg=c["muted"], bg=c["frame"]),
        "tabbar": dict(fg=c["muted"], bg=c["frame"]), "tabbar.active": dict(fg=c["fg"], bg=c["bg"], styles=["bold"]),
        "divider": dict(fg=c["border"], bg=c["frame"]), "scrollbar": dict(fg=c["guideSel"], bg=c["bg"]),
        "message": dict(fg=c["fg"], bg=c["bg"]), "error-message": dict(fg=c["ansiRed"], bg=c["bg"]),
        # popups: the completion menu
        "statusline.suggestions": dict(fg=c["fg"], bg=c["surface"]),
    }


def styles(p):
    """Every group of the scheme: UI groups first, then syntax groups."""
    out = ui(p)
    for group, role, font in syntax_rules(p):
        if group in out:
            raise ValueError(f"{group} is set twice")
        out[group] = dict(fg="#" + p[role], **({"styles": FONTS[font]} if font else {}))
    return out


def style(value):
    """A color-link value: the styles, then fg,bg."""
    colours = value["fg"] + (f",{value['bg']}" if "bg" in value else "")
    return " ".join([*value.get("styles", []), colours])


def colorscheme(p, source):
    """The colorschemes/<scheme>.micro file for a palette. source is the URL of the theme folder."""
    lines = [
        f"# {p['name']}: a Heritage Themes colour scheme for Micro.",
        f"# Generated from {source}; changes here are overwritten.",
        "",
        *(f'color-link {group} "{style(value)}"' for group, value in styles(p).items()),
    ]
    return "\n".join(lines) + "\n"
