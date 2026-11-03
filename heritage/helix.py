"""Helix theme generated from a palette.

Syntax keys are the scopes that the Tree-sitter queries Helix ships capture (runtime/queries/*/highlights.scm). Helix
colours a capture with the longest key that is a dot-separated prefix of it, so "keyword.control.import" takes
"keyword" unless the theme sets a longer key. The keys map to the palette roles that heritage.zed gives the matching
captures. The scopes name the construct, not the language, so a construct takes one colour in every language: keys in
YAML, TOML and JSON take the field colour, and Rust lifetimes the label colour, as the Helix queries capture them as
labels. Helix has no semantic highlighting and its queries give function declarations and calls one scope, so both take
the call role.

The UI keys are those Helix 25.07 looks up (UI_KEYS), laid out as the Islands layout of the other targets: the status
line and buffer line on the frame, the editor and pickers on bg, and popups, menus and help on surface. Helix draws a
key that a theme leaves out, and every broader scope of it, in the terminal's own colours, so the theme sets each of
them. Helix colours have no alpha channel, so every colour is opaque.
"""
import re

from .vscode import mix

PREFIX = "heritage_"
FONTS = {"": [], "bold": ["bold"], "italic": ["italic"], "bold italic": ["bold", "italic"]}
# Attributes and values of a style that Helix accepts (book/src/themes.md).
ATTRIBUTES = ("fg", "bg", "underline", "modifiers")
MODIFIERS = ("bold", "dim", "italic", "slow_blink", "rapid_blink", "reversed", "hidden", "crossed_out")
UNDERLINES = ("line", "curl", "dashed", "dotted", "double_line")
# The UI keys that Helix 25.07 looks up, from the theme lookups in helix-term and helix-view. ui.statusline.active is
# left out: Helix looks it up only for a buffer line without ui.bufferline.active.
UI_KEYS = (
    "ui.background", "ui.background.separator",
    "ui.bufferline", "ui.bufferline.active", "ui.bufferline.background",
    "ui.cursor", "ui.cursor.normal", "ui.cursor.insert", "ui.cursor.select", "ui.cursor.match",
    "ui.cursor.primary", "ui.cursor.primary.normal", "ui.cursor.primary.insert", "ui.cursor.primary.select",
    "ui.cursorline.primary", "ui.cursorline.secondary", "ui.cursorcolumn.primary", "ui.cursorcolumn.secondary",
    "ui.debug.active", "ui.debug.breakpoint",
    "ui.gutter", "ui.gutter.selected", "ui.gutter.virtual", "ui.gutter.selected.virtual",
    "ui.help", "ui.highlight", "ui.highlight.frameline", "ui.linenr", "ui.linenr.selected",
    "ui.menu", "ui.menu.selected", "ui.menu.scroll",
    "ui.picker.header", "ui.picker.header.column", "ui.picker.header.column.active",
    "ui.popup", "ui.popup.info", "ui.selection", "ui.selection.primary",
    "ui.statusline", "ui.statusline.inactive", "ui.statusline.normal", "ui.statusline.insert",
    "ui.statusline.select", "ui.statusline.separator",
    "ui.text", "ui.text.focus", "ui.text.inactive", "ui.text.info", "ui.text.directory",
    "ui.virtual.indent-guide", "ui.virtual.inlay-hint", "ui.virtual.inlay-hint.parameter",
    "ui.virtual.inlay-hint.type", "ui.virtual.jump-label", "ui.virtual.ruler", "ui.virtual.whitespace",
    "ui.virtual.wrap", "ui.window",
    "diagnostic", "diagnostic.error", "diagnostic.warning", "diagnostic.info", "diagnostic.hint",
    "diagnostic.unnecessary", "diagnostic.deprecated", "error", "warning", "info", "hint", "tabstop", "special",
    "diff.plus.gutter", "diff.minus.gutter", "diff.delta.gutter",
)
# Keys drawn as rules, borders, gutter marks or filler rather than text, so the contrast check leaves them out.
DECORATIVE = {"ui.background.separator", "ui.window", "ui.linenr", "ui.linenr.selected", "ui.menu.scroll",
              "ui.virtual.indent-guide", "ui.virtual.ruler", "ui.virtual.whitespace", "ui.virtual.wrap",
              "ui.debug.active", "ui.debug.breakpoint", "ui.statusline.separator",
              "diff.plus.gutter", "diff.minus.gutter", "diff.delta.gutter"}
# Keys held to 3:1 rather than 4.5:1: comments, and the primary cursor in normal mode, which the build checks as the
# caret.
LOW_CONTRAST = {"comment", "ui.cursor.primary", "ui.cursor.primary.normal"}
# Keys that Helix draws on the background of other keys rather than on ui.background, with the minimum contrast on
# each: the info popup's text; picker matches, which take special in bold on any row, the selected one included; and
# diagnostics, whose messages Helix draws in the editor and whose marks, graphics held to 3:1, in the status line.
DRAWN_ON = {"ui.text.info": (("ui.popup.info", 4.5),), "special": (("ui.background", 4.5), ("ui.text.focus", 4.5)),
            **{key: (("ui.background", 4.5), ("ui.statusline", 3)) for key in ("error", "warning", "info", "hint")}}


def name(theme):
    """The theme name of a theme dict from a theme.py, for example "heritage_shuimo_night". Helix lists a theme by its
    file name. A palette name that ends in (Dark) or (Light) adds the brightness, as in "heritage_edo_cha_dark"."""
    brightness = re.search(r" \((Dark|Light)\)$", theme["palette"]["name"])
    return (PREFIX + re.sub(r"(?<!^)(?=[A-Z])", "_", theme["slug"]).lower()
            + (f"_{brightness[1].lower()}" if brightness else ""))


def syntax_rules(p):
    """(scope, role, font style) per syntax key."""
    kw = "bold" if p.get("kwBold", not p["dark"]) else ""
    rules = []
    def s(scopes, role, font=""):
        rules.extend((scope, role, font) for scope in scopes.split())
    s("comment", "comment", "italic")
    s("comment.block.documentation comment.line.documentation", "doc", "italic")
    s("comment.unused", "muted", "italic")
    s("string string.regexp string.special string.special.path constant.character markup.raw", "string")
    s("string.special.url markup.link.url", "call", "italic")
    s("constant.character.escape", "gold", "bold")
    s("constant.numeric", "number")
    s("keyword constant.builtin type.builtin tag markup.heading.marker markup.list", "keyword", kw)
    s("constant type.enum.variant string.special.symbol", "constant", "bold italic")
    s("operator punctuation", "op")
    s("type constructor", "type")
    s("type.parameter", "typeParam", "bold")
    s("namespace embedded variable", "fg")
    s("variable.builtin", "keyword", "italic")
    s("variable.parameter", "param")
    s("variable.other.member", "field")
    s("function function.method", "call")
    s("function.builtin", "call", "italic")
    s("function.macro function.special attribute", "annotation")
    s("label", "label", "bold")
    # Markdown: headings take the declaration role, markers the keyword role
    s("markup.heading", "method", "bold")
    s("markup.bold", "fg", "bold")
    s("markup.italic", "fg", "italic")
    s("markup.link.label markup.link.text", "azure")
    s("markup.quote", "doc", "italic")
    # diff text takes the console colours, which the build checks as text on bg
    s("diff.plus", "ansiGreen")
    s("diff.minus", "ansiRed")
    s("diff.delta diff.delta.moved", "ansiBlue")
    s("diff.delta.conflict", "ansiMagenta")
    return rules


def ui(p):
    """UI key to style, with #-prefixed colours."""
    c = {k: "#" + v for k, v in p.items() if isinstance(v, str) and re.fullmatch(r"[0-9A-F]{6}", v)}
    caret = "#" + p.get("caret", p["gold"])
    def wash(key):
        """Halfway from bg to the palette colour, for the lines of secondary cursors."""
        return "#" + mix(p["bg"], p[key], 0.5)
    def block(colour):
        """A block cursor: the character under it in bg on the cursor's colour."""
        return dict(fg=c["bg"], bg=colour)
    def mode(colour):
        """A mode's name at the start of the status line, as the lualine theme of the Neovim target draws it."""
        return dict(fg=c["bg"], bg=colour, modifiers=["bold"])
    return {
        # editor. ui.background's fg draws what Helix gives no key of its own, such as picker borders. The primary
        # cursor takes the caret colour in normal mode and the mode's colour in insert and select mode, as the mode
        # name does; secondary cursors take muted in every mode.
        "ui.background": dict(fg=c["fg"], bg=c["bg"]), "ui.background.separator": dict(fg=c["border"]),
        "ui.cursor": block(c["muted"]), "ui.cursor.normal": block(c["muted"]),
        "ui.cursor.insert": block(c["muted"]), "ui.cursor.select": block(c["muted"]),
        "ui.cursor.primary": block(caret), "ui.cursor.primary.normal": block(caret),
        "ui.cursor.primary.insert": block(c["ansiGreen"]), "ui.cursor.primary.select": block(c["ansiMagenta"]),
        "ui.cursor.match": dict(bg=c["braceBg"], modifiers=["bold"]),
        "ui.cursorline.primary": dict(bg=c["caretRow"]), "ui.cursorline.secondary": dict(bg=wash("caretRow")),
        "ui.cursorcolumn.primary": dict(bg=c["caretRow"]), "ui.cursorcolumn.secondary": dict(bg=wash("caretRow")),
        "ui.selection.primary": dict(bg=c["selection"]), "ui.selection": dict(bg=c["selInactive"]),
        "ui.gutter": dict(bg=c["bg"]), "ui.gutter.selected": dict(bg=c["bg"]),
        "ui.gutter.virtual": dict(bg=c["bg"]), "ui.gutter.selected.virtual": dict(bg=c["bg"]),
        "ui.linenr": dict(fg=c["lineNo"]), "ui.linenr.selected": dict(fg=c["lineNoCaret"]),
        "ui.virtual.whitespace": dict(fg=c["guide"]), "ui.virtual.indent-guide": dict(fg=c["guide"]),
        "ui.virtual.ruler": dict(bg=c["guide"]), "ui.virtual.wrap": dict(fg=c["lineNo"]),
        "ui.virtual.inlay-hint": dict(fg=c["muted"], bg=c["caretRow"]),
        "ui.virtual.inlay-hint.parameter": dict(fg=c["muted"], bg=c["caretRow"]),
        "ui.virtual.inlay-hint.type": dict(fg=c["muted"], bg=c["caretRow"]),
        "ui.virtual.jump-label": dict(fg=c["bg"], bg=c["gold"], modifiers=["bold"]),
        "ui.highlight": dict(bg=c["selInactive"]), "ui.highlight.frameline": dict(bg=c["diffMod"]),
        "ui.debug.breakpoint": dict(fg=c["red"]), "ui.debug.active": dict(fg=c["gold"]),
        "ui.window": dict(fg=c["border"]), "tabstop": dict(bg=c["underCaret"]),
        # frame: status line and buffer line. The active buffer joins the editor, as the tab of the Zed theme does.
        # Helix colours the mode names with editor.color-modes.
        "ui.statusline": dict(fg=c["fg"], bg=c["frame"]), "ui.statusline.inactive": dict(fg=c["muted"], bg=c["frame"]),
        "ui.statusline.normal": mode(c["ansiBlue"]), "ui.statusline.insert": mode(c["ansiGreen"]),
        "ui.statusline.select": mode(c["ansiMagenta"]),
        "ui.statusline.separator": dict(fg=c["border"], bg=c["frame"]),
        "ui.bufferline": dict(fg=c["muted"], bg=c["frame"]),
        "ui.bufferline.background": dict(fg=c["muted"], bg=c["frame"]),
        "ui.bufferline.active": dict(fg=c["fg"], bg=c["bg"], modifiers=["bold"]),
        # text: pickers, the command line and popups. Matches take ansiBlue, as VS Code's lists do; Helix draws them
        # in special and bold.
        "ui.text": dict(fg=c["fg"]), "ui.text.focus": dict(fg=c["fg"], bg=c["selection"], modifiers=["bold"]),
        "ui.text.inactive": dict(fg=c["muted"]), "ui.text.info": dict(fg=c["fg"]),
        "ui.text.directory": dict(fg=c["ansiBlue"]), "special": dict(fg=c["ansiBlue"]),
        "ui.picker.header": dict(fg=c["muted"]), "ui.picker.header.column": dict(fg=c["muted"]),
        "ui.picker.header.column.active": dict(fg=c["fg"], modifiers=["bold"]),
        # popups: hover, signature help, the key help and the completion menu
        "ui.popup": dict(fg=c["fg"], bg=c["surface"]), "ui.popup.info": dict(fg=c["fg"], bg=c["surface"]),
        "ui.help": dict(fg=c["fg"], bg=c["surface"]),
        "ui.menu": dict(fg=c["fg"], bg=c["surface"]), "ui.menu.selected": dict(fg=c["fg"], bg=c["selection"]),
        "ui.menu.scroll": dict(fg=c["guideSel"], bg=c["surface"]),
        # diagnostics. Gutter marks and messages take the ANSI colours, which the build checks at 4.5:1 against bg;
        # undercurls take the diagnostic colours of the other targets.
        "error": dict(fg=c["ansiRed"]), "warning": dict(fg=c["ansiYellow"]), "info": dict(fg=c["ansiBlue"]),
        "hint": dict(fg=c["muted"]),
        "diagnostic": dict(underline=dict(color=c["weak"], style="curl")),
        "diagnostic.error": dict(underline=dict(color=c["error"], style="curl")),
        "diagnostic.warning": dict(underline=dict(color=c["warning"], style="curl")),
        "diagnostic.info": dict(underline=dict(color=c["azure"], style="curl")),
        "diagnostic.hint": dict(underline=dict(color=c["weak"], style="curl")),
        "diagnostic.unnecessary": dict(fg=c["muted"], modifiers=["italic"]),
        "diagnostic.deprecated": dict(modifiers=["crossed_out"]),
        # version control marks in the gutter, in the VCS colours of the other targets' gutters
        "diff.plus.gutter": dict(fg=c["added"]), "diff.minus.gutter": dict(fg=c["deleted"]),
        "diff.delta.gutter": dict(fg=c["modified"]),
        "markup.strikethrough": dict(modifiers=["crossed_out"]),
    }


def styles(p):
    """Every key of the theme: UI keys first, then syntax keys."""
    out = ui(p)
    for scope, role, font in syntax_rules(p):
        if scope in out:
            raise ValueError(f"{scope} is set twice")
        out[scope] = dict(fg="#" + p[role], **({"modifiers": FONTS[font]} if font else {}))
    return out


def toml(value):
    """A TOML literal for a string, list of strings or dict of them, with tables inline."""
    if isinstance(value, str):
        return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'
    if isinstance(value, list):
        return "[" + ", ".join(toml(v) for v in value) + "]"
    return "{ " + ", ".join(f"{k} = {toml(v)}" for k, v in value.items()) + " }"


def theme(p, source):
    """The themes/<name>.toml file for a palette. source is the URL of the theme folder."""
    lines = [
        f"# {p['name']}: a Heritage Themes theme for Helix.",
        f"# Generated from {source}; changes here are overwritten.",
        "",
        *(f"{toml(key)} = {toml(style)}" for key, style in styles(p).items()),
    ]
    return "\n".join(lines) + "\n"
