"""Colour schemes for Geany, generated from a palette.

Geany colours code through named styles (highlighting.c). Each filetype definition in Geany's filedefs folder maps the
styles of its Scintilla lexer to the named styles of filetypes.common, and a colour scheme, a key file in the
colorschemes folder, sets those named styles for every language at once: it cannot colour one language's constructs
apart from another's. Geany 1.38 to 2.1 have the same named styles, NAMED_STYLES, and read schemes in the same way.

A style is foreground;background;bold;italic with #rrggbb colours, and an empty background keeps the default style's.
For the editor styles the third and fourth fields are flags of their own, which editor_styles() gives with each style.
Geany has no underline, strikethrough or current line number style, and its build-error squiggle, change history and
window are not part of a scheme: Geany draws its window, tabs, side bar and message window in the desktop's GTK theme.

Each named style takes the role that most of the filetypes that use it give it, in the roles heritage.notepadpp gives
the same Scintilla styles, as both apps colour code with Scintilla's lexers. A scheme sets every named style, so no
colour of Geany's default scheme shows through.
"""
from . import gnome_text_editor as gte
from .nvim import name  # noqa: F401 - the files take the names of Neovim's schemes

# "kw" stands for the keyword font: bold where the palette's keywords are bold.
KW = "kw"
# Syntax named style → (role, font), in the order of filetypes.common.
SYNTAX_STYLES = {
    "comment": ("comment", "italic"), "comment_line": ("comment", "italic"),
    "comment_doc": ("doc", "italic"), "comment_line_doc": ("doc", "italic"),
    "comment_doc_keyword": ("docTag", "bold italic"), "comment_doc_keyword_error": ("docTag", "italic"),
    # numbers; number_2 also marks TOML's dates and HTML's processing instructions, number_3 Julia's numbers
    "number": ("number", ""), "number_1": ("number", ""), "number_2": ("number", ""), "number_3": ("number", ""),
    # type and class mark class names and declarations; function marks Python's, Ruby's and GDScript's def names
    "type": ("type", ""), "class": ("type", ""), "function": ("method", "bold"),
    # Bash's ${...}, Rust's lifetimes and CMake's arguments
    "parameter": ("param", ""),
    # GDScript's annotations, Julia's macros and Python's and Dart's decorators
    "annotation": ("annotation", ""), "decorator": ("annotation", ""), "macro": ("annotation", ""),
    # keyword_1 holds each language's primary keywords and Markdown's headings and links; keyword_2 the secondary
    # list, which the C-family languages, Rust, Go and JavaScript fill with built-in types and classes, and CSS takes
    # for property names; keyword_3 and keyword_4 further keywords, such as Rust's Self and Lua's word lists
    "keyword": ("keyword", KW), "keyword_1": ("keyword", KW), "keyword_2": ("type", ""),
    "keyword_3": ("keyword", KW), "keyword_4": ("keyword", KW),
    # names; identifier_2 to identifier_4 mark Perl's arrays and hashes, SQL's quoted names, CoffeeScript's instance
    # properties and Makefile's variables, which the other targets colour as fields
    "identifier": ("fg", ""), "identifier_1": ("fg", ""), "identifier_2": ("field", ""),
    "identifier_3": ("field", ""), "identifier_4": ("field", ""),
    "string": ("string", ""), "string_1": ("string", ""), "string_2": ("string", ""), "string_eol": ("string", ""),
    "character": ("string", ""), "backticks": ("string", ""), "here_doc": ("string", ""), "regex": ("string", ""),
    "label": ("label", "bold"),
    # C's preprocessor, Rust's macros, PHP's variables, Ruby's symbols and CSS's at-rules
    "preprocessor": ("directive", ""),
    "operator": ("op", ""),
    # HTML's text inside tags besides names and values, C's user-defined literals and UUIDs
    "other": ("op", ""),
    # markup: tags as keywords, unknown tags as custom elements in the type colour, which Markdown also gives its
    # lists, quotes and rules; attributes as fields, which Markdown also gives its code spans and blocks
    "tag": ("keyword", ""), "tag_unknown": ("type", ""), "tag_end": ("keyword", ""),
    "attribute": ("field", ""), "attribute_unknown": ("field", ""),
    "value": ("string", ""), "entity": ("gold", ""),
    # diff files' lines
    "line_added": ("ansiGreen", ""), "line_removed": ("ansiRed", ""), "line_changed": ("ansiBlue", ""),
}
# Editor named styles, in the order of filetypes.common.
EDITOR_STYLES = ("default", "error", "selection", "current_line", "brace_good", "brace_bad", "margin_line_number",
                 "margin_folding", "fold_symbol_highlight", "indent_guide", "caret", "marker_line", "marker_search",
                 "marker_mark", "call_tips", "white_space")
# The named styles of filetypes.common in Geany 1.38 to 2.1, which a scheme must all set.
NAMED_STYLES = EDITOR_STYLES + tuple(SYNTAX_STYLES)
LOW_CONTRAST_ROLES = gte.LOW_CONTRAST_ROLES
# The colour of the long line marker by default (keyfile.c), a preference of Geany's that a scheme does not set.
LONG_LINE_COLOUR = "#C2EBC2"


def keyword_font(p):
    return "bold" if p.get("kwBold", not p["dark"]) else ""


def syntax_styles(p):
    """Syntax named style → (role, font), with the keyword font resolved."""
    return {style: (role, keyword_font(p) if font == KW else font) for style, (role, font) in SYNTAX_STYLES.items()}


def editor_styles(p):
    """Editor named style → (foreground, background, third field, fourth field), with palette keys for colours and the
    fields as Geany reads each style (filetypes.common, highlighting.c)."""
    caret = "caret" if "caret" in p else "gold"
    return {
        "default": ("fg", "bg", "false", "false"),
        # an error that a lexer marks, such as an unterminated string in TOML or a bad Rust token
        "error": ("ansiRed", "bg", "false", "false"),
        # the background only, so selected code keeps its colours: the fields override the foreground, the background
        "selection": ("fg", "selection", "false", "true"),
        # the background, and the third field turns the highlight on
        "current_line": ("fg", "caretRow", "true", "false"),
        "brace_good": ("fg", "braceBg", "true", "false"),
        "brace_bad": ("ansiRed", "bg", "true", "false"),
        "margin_line_number": ("lineNo", "bg", "false", "false"),
        # the folding margin's background, and in its foreground the fold markers' boxes and lines, around signs in
        # fold_symbol_highlight's foreground
        "margin_folding": ("lineNo", "bg", "false", "false"),
        "fold_symbol_highlight": ("bg", "bg", "false", "false"),
        "indent_guide": ("guide", "bg", "false", "false"),
        # the caret's colour, and the third field false for a line caret
        "caret": (caret, caret, "false", "false"),
        # the arrow in the marker margin at the line that Go to Line and the symbol list jump to
        "marker_line": ("searchBorder", "searchBorder", "false", "false"),
        # the background only: the box around each match that Mark All draws, filled at 60/255
        "marker_search": ("searchBorder", "searchBorder", "false", "false"),
        # the plus in the marker margin at a line that Toggle Marker marks
        "marker_mark": ("azure", "azure", "false", "false"),
        # both fields true, so that the call tip takes both colours
        "call_tips": ("fg", "surface", "true", "true"),
        # the foreground only, the third field true to use it
        "white_space": ("guide", "bg", "true", "false"),
    }


def value(c, role, font):
    """A syntax style: the role's colour on the default background, with the font's flags."""
    return f"{c[role]};;{'true' if 'bold' in font else 'false'};{'true' if 'italic' in font else 'false'}"


def scheme(t, source):
    """The colorschemes/<theme>.conf file for a theme dict; source is the URL of the theme folder."""
    p = t["palette"]
    c = gte.hexes(p)
    lines = [f"# {p['name']}: a Heritage Themes colour scheme for Geany. Generated from {source}; changes here are "
             "overwritten.",
             "# SPDX-License-Identifier: MIT",
             "",
             "[theme_info]",
             f"name={p['name']}",
             f"description={p['name']}: colours drawn from a culture's colour tradition.",
             "author=Heritage Themes",
             "url=https://github.com/heritage-themes/heritage-themes",
             "compat=1.38;2.0;2.1;",
             "",
             "[named_styles]"]
    for style, (fg, bg, third, fourth) in editor_styles(p).items():
        lines.append(f"{style}={c[fg]};{c[bg]};{third};{fourth}")
    for style, (role, font) in syntax_styles(p).items():
        lines.append(f"{style}={value(c, role, font)}")
    return "\n".join(lines) + "\n"


def styles(p):
    """Element → dict(fg, bg) as #rrggbb, for the build's contrast check: each syntax style on the background and on
    the current line, and the text on the editor's highlights. Line numbers are left out, as the other targets leave
    them out."""
    c = gte.hexes(p)
    out = {}
    for style, (role, _) in syntax_styles(p).items():
        out[style] = dict(fg=c[role], bg=c["bg"])
        out[f"{style} on the current line"] = dict(fg=c[role], bg=c["caretRow"])
    editor = editor_styles(p)
    for element, style in (("text", "default"), ("error", "error"), ("matching bracket", "brace_good"),
                           ("unmatched bracket", "brace_bad"), ("call tip", "call_tips")):
        fg, bg, *_ = editor[style]
        out[element] = dict(fg=c[fg], bg=c[bg])
    out["selected text"] = dict(fg=c["fg"], bg=c["selection"])
    return out


def low_contrast(p):
    """The elements of styles() held to 3:1: the syntax styles in the roles of LOW_CONTRAST_ROLES, and the bracket
    match, which draws its background behind one character, as in heritage.kate."""
    out = {"matching bracket"}
    for style, (role, _) in syntax_styles(p).items():
        if role in LOW_CONTRAST_ROLES:
            out |= {style, f"{style} on the current line"}
    return out


def pixel_palette(p):
    """What scripts/editors/pixels.py checks a screenshot against: the editor, cropped from the window that
    scripts/editors/shoot.py opens at 1100x700, with the menu bar, tab bar, scroll bars and status bar left out, where
    Geany draws its GTK theme. The long line marker takes the colour of Geany's preferences, which a scheme does not
    set: LONG_LINE_COLOUR, Geany's default."""
    colours = {colour.upper() for colour in gte.hexes(p).values()}
    backgrounds = ["#" + p[k] for k in ("caretRow", "selection", "braceBg", "surface", "searchBorder")]
    return dict(background="#" + p["bg"], backgrounds=backgrounds, foregrounds=sorted(colours), crop=[65, 55, 1, 16],
                allowed=[LONG_LINE_COLOUR])
