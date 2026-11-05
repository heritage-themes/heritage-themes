"""Textadept theme generated from a palette: a Lua file in ~/.textadept/themes, which view:set_theme() loads.

A theme sets the styles of the lexers' tags and the colours of the view's elements. The tags map to the palette roles
that heritage.zed gives the matching Tree-sitter captures: Textadept's lexers give a construct one tag in every
language, so preprocessor directives take the keyword role, as Vim's PreProc does, and attributes the annotation role,
as Zed's attribute capture does, which covers HTML attribute names and Java annotations alike. Textadept cannot colour
its own Qt or GTK widgets, so the theme colours the editor: text, margins, the caret and caret line, selections, brace
matches, call tips, markers and indicators.
"""
import re

from .nvim import name  # noqa: F401 - Textadept lists a theme by the same name as Neovim
from .terminals import colours as terminal_colours

FONTS = {"": {}, "bold": {"bold": True}, "italic": {"italic": True}, "bold italic": {"bold": True, "italic": True},
         "underline": {"underline": True}}
# The lexer tags of Textadept 13 (lexer.lua), each set by syntax_rules.
TAGS = ("ANNOTATION", "ATTRIBUTE", "BOLD", "CLASS", "CODE", "COMMENT", "CONSTANT", "CONSTANT_BUILTIN", "EMBEDDED",
        "ERROR", "FUNCTION", "FUNCTION_BUILTIN", "FUNCTION_METHOD", "HEADING", "IDENTIFIER", "ITALIC", "KEYWORD",
        "LABEL", "LINK", "LIST", "NUMBER", "OPERATOR", "PREPROCESSOR", "REFERENCE", "REGEX", "STRING", "TAG", "TYPE",
        "UNDERLINE", "VARIABLE", "VARIABLE_BUILTIN")
# Tags that set only a font style and keep the colour of the text around them.
STYLE_ONLY = {"BOLD": "bold", "ITALIC": "italic", "UNDERLINE": "underline"}
# The names of the terminal's colours in Textadept's styles for ANSI output (styles.csi_*).
CSI = ("black", "red", "green", "yellow", "blue", "magenta", "cyan", "white")


def syntax_rules(p):
    """(tag, role, font style) per lexer tag."""
    kw = "bold" if p.get("kwBold", not p["dark"]) else ""
    rules = []
    def s(tags, role, font=""):
        rules.extend((tag, role, font) for tag in tags.split())
    s("COMMENT", "comment", "italic")
    s("KEYWORD PREPROCESSOR TAG LIST CONSTANT_BUILTIN", "keyword", kw)
    s("STRING REGEX CODE", "string")
    s("NUMBER", "number")
    s("TYPE CLASS", "type")
    s("FUNCTION FUNCTION_METHOD", "call")
    s("FUNCTION_BUILTIN", "call", "italic")
    s("CONSTANT", "constant", "bold italic")
    s("VARIABLE IDENTIFIER EMBEDDED", "fg")
    s("VARIABLE_BUILTIN", "keyword", "italic")
    s("OPERATOR", "op")
    s("ANNOTATION ATTRIBUTE", "annotation")
    s("LABEL", "label", "bold")
    s("ERROR", "ansiRed", "bold")
    # Markdown: headings take the declaration role, links the link colour
    s("HEADING", "method", "bold")
    s("LINK REFERENCE", "azure", "underline")
    return rules


def bgr(colour):
    """Textadept's 0xBBGGRR for #RRGGBB or RRGGBB."""
    colour = colour.lstrip("#")
    return f"0x{colour[4:6]}{colour[2:4]}{colour[0:2]}"


def lua_style(style):
    """A Lua table for a style dict of fore, back and font flags."""
    parts = [f"{key} = colors.{value}" if key in ("fore", "back") else f"{key} = {str(value).lower()}"
             for key, value in style.items()]
    return "{" + ", ".join(parts) + "}"


def colours(p):
    """Colour name → RRGGBB: the palette's colours that the theme uses, by role, as view.colors holds them."""
    keys = {"bg", "fg", "muted", "surface", "caretRow", "selection", "selInactive", "lineNo", "guide",
            "searchBg", "searchBorder", "red", "redText", "field", *(role for _, role, _ in syntax_rules(p))}
    out = {key: p[key] for key in sorted(keys)}
    out["caret"] = p.get("caret", p["gold"])
    out.update({f"terminal_{n}": c[1:] for n, c in zip(CSI, terminal_colours(p)["ansi"][:8])})
    out.update({f"terminal_bright_{n}": c[1:] for n, c in zip(CSI, terminal_colours(p)["ansi"][8:])})
    return out


def tag_styles(p):
    """lexer tag → style dict."""
    out = {tag: {"fore": role, **FONTS[font]} for tag, role, font in syntax_rules(p)}
    out.update({tag: FONTS[font] for tag, font in STYLE_ONLY.items()})
    return out


def theme(p, source):
    """The themes/<theme>.lua file for a palette. source is the URL of the theme folder."""
    lines = [
        f"-- {p['name']}: a Heritage Themes theme for Textadept.",
        f"-- Generated from {source}; changes here are overwritten.",
        "",
        "local view, colors, styles = view, view.colors, view.styles",
        "",
        *(f"colors.{key} = {bgr(value)}" for key, value in colours(p).items()),
        "",
        "-- Default font, as Textadept's own themes choose it.",
        "if not font then font = OS == 'windows' and 'Consolas' or OS == 'macos' and 'Monaco' or 'Monospace' end",
        "if not size then size = OS ~= 'macos' and 10 or 12 end",
        "",
        "-- Predefined styles.",
        "styles[view.STYLE_DEFAULT] = {font = font, size = size, fore = colors.fg, back = colors.bg}",
        "styles[view.STYLE_LINENUMBER] = {fore = colors.lineNo, back = colors.bg}",
        "-- a matching brace in bold blue, as Textadept's own themes draw it",
        "styles[view.STYLE_BRACELIGHT] = {fore = colors.terminal_blue, bold = true}",
        "styles[view.STYLE_BRACEBAD] = {fore = colors.redText, back = colors.red}",
        "styles[view.STYLE_INDENTGUIDE] = {fore = colors.guide}",
        "styles[view.STYLE_CALLTIP] = {fore = colors.fg, back = colors.surface}",
        "styles[view.STYLE_FOLDDISPLAYTEXT] = {fore = colors.muted, back = colors.surface}",
        "",
        "-- Tag styles.",
        *(f"styles[lexer.{tag}] = {lua_style(style)}" for tag, style in tag_styles(p).items()),
        "",
        "-- Lexer-specific styles: CSS properties take the field role, diffs the colours of added, deleted and changed",
        "-- lines, and ANSI output the terminal colours of the matching theme of the Terminals product.",
        "styles.property = {fore = colors.field}",
        "styles.addition = {fore = colors.terminal_green}",
        "styles.deletion = {fore = colors.terminal_red}",
        "styles.change = {fore = colors.terminal_blue}",
        "styles.tag_unknown = styles.tag .. {italic = true}",
        "styles.attribute_unknown = styles.attribute .. {italic = true}",
        "styles.command = styles[lexer.KEYWORD]",
        "styles.command_section = styles[lexer.HEADING]",
        "styles.environment = styles[lexer.TYPE]",
        "styles.environment_math = styles[lexer.NUMBER]",
        "styles.csi = {visible = false}",
        *(f"styles.csi_{n} = {{fore = colors.terminal_{n}}}" for n in CSI),
        *(f"styles.csi_{n}_bright = {{fore = colors.terminal_bright_{n}, bold = true}}" for n in CSI),
        "styles.keyword_soft = {}",
        "styles.error_indent = {back = colors.red}",
        "",
        "-- Element colors.",
        "view.element_color[view.ELEMENT_SELECTION_BACK] = colors.selection",
        "view.element_color[view.ELEMENT_SELECTION_ADDITIONAL_BACK] = colors.selection",
        "view.element_color[view.ELEMENT_SELECTION_SECONDARY_BACK] = colors.selInactive",
        "view.element_color[view.ELEMENT_SELECTION_INACTIVE_BACK] = colors.selInactive",
        "view.element_color[view.ELEMENT_SELECTION_INACTIVE_ADDITIONAL_BACK] = colors.selInactive",
        "view.element_color[view.ELEMENT_CARET] = colors.caret",
        "view.element_color[view.ELEMENT_CARET_ADDITIONAL] = colors.muted",
        "if view ~= ui.command_entry then",
        "\tview.element_color[view.ELEMENT_CARET_LINE_BACK] = colors.caretRow",
        "end",
        "view.caret_line_layer = view.LAYER_UNDER_TEXT",
        "",
        "-- Fold margin.",
        "view:set_fold_margin_color(true, colors.bg)",
        "view:set_fold_margin_hi_color(true, colors.bg)",
        "",
        "-- Markers.",
        "view.marker_back[textadept.bookmarks.MARK_BOOKMARK] = colors.terminal_blue",
        "view.marker_back[textadept.run.MARK_WARNING] = colors.terminal_yellow",
        "view.marker_back[textadept.run.MARK_ERROR] = colors.terminal_red",
        "for i = view.MARKNUM_FOLDEREND, view.MARKNUM_FOLDEROPEN do -- fold margin",
        "\tview.marker_fore[i] = colors.bg",
        "\tview.marker_back[i] = colors.lineNo",
        "\tview.marker_back_selected[i] = colors.muted",
        "end",
        "",
        "-- Indicators: search matches and highlighted words in the search colours, as the other targets draw them.",
        "view.indic_fore[ui.find.INDIC_FIND] = colors.searchBorder",
        "view.indic_alpha[ui.find.INDIC_FIND] = 0x60",
        "view.indic_fore[textadept.editing.INDIC_HIGHLIGHT] = colors.searchBorder",
        "view.indic_alpha[textadept.editing.INDIC_HIGHLIGHT] = 0x40",
        "view.indic_fore[textadept.snippets.INDIC_PLACEHOLDER] = colors.muted",
        "view.indic_fore[textadept.run.INDIC_WARNING] = colors.terminal_yellow",
        "view.indic_fore[textadept.run.INDIC_ERROR] = colors.terminal_red",
        "",
        "-- Call tips and the long line marker.",
        "view.call_tip_fore_hlt = colors.terminal_blue",
        "view.edge_color = colors.guide",
        "",
        "-- Find & replace pane entries.",
        "ui.find.entry_font = font .. ' ' .. size",
    ]
    return "\n".join(lines) + "\n"


def styles(p):
    """Style name → dict(fg, bg) as #RRGGBB, for the build's contrast check: each tag on bg, and the predefined
    styles with text."""
    out = {f"lexer.{tag}": dict(fg="#" + p[role], bg="#" + p["bg"]) for tag, role, _ in syntax_rules(p)}
    out.update({
        "STYLE_DEFAULT": dict(fg="#" + p["fg"], bg="#" + p["bg"]),
        "STYLE_BRACELIGHT": dict(fg=terminal_colours(p)["ansi"][4], bg="#" + p["bg"]),
        "STYLE_BRACEBAD": dict(fg="#" + p["redText"], bg="#" + p["red"]),
        "STYLE_CALLTIP": dict(fg="#" + p["fg"], bg="#" + p["surface"]),
        "STYLE_FOLDDISPLAYTEXT": dict(fg="#" + p["muted"], bg="#" + p["surface"]),
        "selection": dict(fg="#" + p["fg"], bg="#" + p["selection"]),
        "caret line": dict(fg="#" + p["fg"], bg="#" + p["caretRow"]),
    })
    return out


def parse_colours(text):
    """colors.<name> → RRGGBB of a theme file."""
    return {key: value[4:6] + value[2:4] + value[0:2]
            for key, value in re.findall(r"^colors\.(\w+) = 0x([0-9A-F]{6})$", text, re.M)}


def pixel_palette(p):
    """What scripts/editors/pixels.py checks a screenshot against: the colours the theme draws, the backgrounds that
    text sits on, and the menu bar and status bar at the top and bottom, which are Qt's, cropped off."""
    return dict(background="#" + p["bg"],
                backgrounds=["#" + p[k] for k in ("caretRow", "selection", "selInactive", "surface")],
                foregrounds=sorted({"#" + v for v in p.values() if isinstance(v, str) and re.fullmatch(r"[0-9A-F]{6}", v)}
                                   | set(terminal_colours(p)["ansi"])),
                crop=[24, 26, 1, 1])
