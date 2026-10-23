"""Zed theme family JSON generated from a palette.

Syntax keys are Tree-sitter capture names. Zed colours a capture with the longest key that is a dot-separated prefix
of it, so "function.method.call" takes "function.method" when defined, else "function". The keys map to the palette
roles that heritage.vscode gives the matching TextMate scopes. Zed's captures name the construct, not the language,
so a construct takes one colour in every language: @attribute, for example, is a Java annotation as well as an HTML
attribute name.

The UI keys follow the Islands layout of the other targets: the title bar and status bar on the frame, the panels
and tab bar on bgTool, the editor and its active tab on bg, and popups on surface. Zed fills in every key a theme
leaves out from its One theme of the same appearance, so the theme sets each key that One sets.
"""
import re

from .vscode import mix, over

AUTHOR = "Heritage Themes"
TRANSPARENT = "#00000000"
FONTS = {"": {}, "bold": {"font_weight": 700}, "italic": {"font_style": "italic"},
         "bold italic": {"font_weight": 700, "font_style": "italic"}}
# Palette roles of collaborators' cursors, after the local player's caret.
PLAYERS = ("ansiBlue", "ansiMagenta", "ansiGreen", "ansiYellow", "ansiCyan", "ansiRed", "azure")


def syntax_rules(p):
    """(capture name, role, font style) per syntax key."""
    kw = "bold" if p.get("kwBold", not p["dark"]) else ""
    rules = []
    def s(names, role, font=""):
        rules.extend((name, role, font) for name in names.split())
    s("comment", "comment", "italic")
    s("comment.doc comment.documentation string.doc", "doc", "italic")
    s("keyword.jsdoc", "docTag", "bold italic")
    s("string string.special string.special.path text.literal markup.raw character", "string")
    s("string.regex", "string")
    s("string.escape keyword.operator.regex operator.regex punctuation.bracket.regex punctuation.delimiter.regex",
      "gold", "bold")
    s("number.quantifier.regex", "number", "bold")
    s("number float", "number")
    s("boolean constant.builtin type.builtin type.qualifier", "keyword", kw)
    s("keyword preproc include import storageclass tag selector selector.pseudo "
      "punctuation.markup punctuation.list_marker charset keyframes media nested supports", "keyword", kw)
    s("constant variant enum.member string.special.symbol type.enum.member", "constant", "bold italic")
    # punctuation.special marks interpolation, decorators and type annotations alike, so it stays an operator
    s("operator punctuation punctuation.bracket punctuation.delimiter punctuation.special", "op")
    s("type enum type.class type.enum type.struct concept constructor", "type")
    s("type.interface interface", "type", "italic")
    s("type.parameter", "typeParam", "bold")
    s("type.unit", "string")
    s("lifetime", "typeParam", "italic")
    s("namespace module embedded text text.jsx primary markup", "fg")
    s("variable", "fg")
    s("variable.special variable.builtin", "keyword", "italic")
    s("variable.parameter parameter", "param")
    s("function.kwargs", "param", "italic")
    s("property variable.other.member attribute.jsx", "field")
    s("function", "call")
    s("function.definition", "method", "bold")
    s("function.builtin", "call", "italic")
    s("function.decorator function.macro function.special attribute", "annotation")
    s("label", "label", "bold")
    # Markdown: headings take the declaration role, markers the keyword role
    s("title markup.heading", "method", "bold")
    s("emphasis", "fg", "italic")
    s("emphasis.strong", "fg", "bold")
    s("link_text markup.link", "azure")
    s("link_uri markup.link.url", "call", "italic")
    # diff text takes the console colours, which the build checks as text on bg
    s("diff.plus", "ansiGreen")
    s("diff.minus", "ansiRed")
    s("diff.delta", "ansiBlue")
    s("hint predictive comment.unused", "muted", "italic")
    s("error", "ansiRed")
    s("warning", "ansiYellow")
    return rules


def syntax(p):
    out = {}
    for name, role, font in syntax_rules(p):
        out[name] = {"color": "#" + p[role], **FONTS[font]}
    return out


def colours(p):
    """UI keys to #-prefixed colours."""
    c = {k: "#" + v for k, v in p.items() if isinstance(v, str) and re.fullmatch(r"[0-9A-F]{6}", v)}
    bg = p["bg"]
    def layer(key, base=bg):
        return over(p[key], base)
    def wash(key, base=bg):
        """Halfway from base to the palette colour, as a layer over base."""
        return over(mix(base, p[key], 0.5), base)
    def dim(key):
        return "#" + mix(p[key], p["bgTool"], 0.3)
    ansi = {name: c["ansi" + name.title()] for name in ("red", "green", "yellow", "blue", "magenta", "cyan")}
    return {
        # surfaces: the frame around the islands, the islands, and popups
        "background": c["frame"], "background.appearance": "opaque",
        "title_bar.background": c["frame"], "title_bar.inactive_background": c["frame"],
        "status_bar.background": c["frame"],
        "panel.background": c["bgTool"], "surface.background": c["bgTool"],
        "elevated_surface.background": c["surface"],
        "tab_bar.background": c["bgTool"], "tab.inactive_background": c["bgTool"], "tab.active_background": c["bg"],
        "toolbar.background": c["bg"],
        "border": c["border"], "border.variant": c["border"], "border.focused": c["ansiBlue"],
        "border.selected": c["ansiBlue"], "border.transparent": TRANSPARENT, "border.disabled": c["border"],
        "pane_group.border": c["border"], "pane.focused_border": None, "panel.focused_border": None,
        "panel.indent_guide": c["guide"], "panel.indent_guide_active": c["guideSel"],
        "panel.indent_guide_hover": c["guideSel"],
        "panel.overlay_background": c["bgTool"], "panel.overlay_hover": c["hover"],
        # elements: buttons, inputs and list rows
        "element.background": c["surface"], "element.hover": c["hover"], "element.active": c["selection"],
        "element.selected": c["selection"], "element.disabled": c["surface"],
        "element.selection_background": layer("selection", p["surface"]),
        "ghost_element.background": TRANSPARENT, "ghost_element.hover": c["hover"],
        "ghost_element.active": c["selection"], "ghost_element.selected": c["selection"],
        "ghost_element.disabled": TRANSPARENT,
        "drop_target.background": layer("selInactive"), "drop_target.border": c["gold"],
        # text and icons. Matches take ansiBlue, as VS Code's lists do.
        "text": c["fg"], "text.muted": c["muted"], "text.placeholder": c["muted"], "text.disabled": c["disabled"],
        "text.accent": c["ansiBlue"], "link_text.hover": c["azure"],
        "icon": c["fg"], "icon.muted": c["muted"], "icon.disabled": c["disabled"], "icon.placeholder": c["muted"],
        "icon.accent": c["ansiBlue"], "debugger.accent": c["red"],
        "scrollbar.thumb.background": c["guideSel"] + "99", "scrollbar.thumb.hover_background": c["lineNo"] + "99",
        "scrollbar.thumb.active_background": c["lineNo"] + "CC", "scrollbar.thumb.border": TRANSPARENT,
        "scrollbar.track.background": TRANSPARENT, "scrollbar.track.border": TRANSPARENT,
        "minimap.thumb.background": c["guideSel"] + "66", "minimap.thumb.hover_background": c["lineNo"] + "66",
        "minimap.thumb.active_background": c["lineNo"] + "99", "minimap.thumb.border": TRANSPARENT,
        # editor
        "editor.foreground": c["fg"], "editor.background": c["bg"], "editor.gutter.background": c["bg"],
        "editor.subheader.background": c["bgTool"], "editor.code_lens.foreground": c["muted"],
        "editor.active_line.background": layer("caretRow"),
        "editor.highlighted_line.background": layer("selInactive"),
        "editor.debugger_active_line.background": layer("diffMod"),
        "editor.line_number": c["lineNo"], "editor.active_line_number": c["lineNoCaret"],
        "editor.hover_line_number": c["muted"],
        "editor.invisible": c["guide"], "editor.wrap_guide": c["guide"], "editor.active_wrap_guide": c["guideSel"],
        "editor.indent_guide": c["guide"], "editor.indent_guide_active": c["guideSel"],
        "editor.document_highlight.read_background": layer("underCaret"),
        "editor.document_highlight.write_background": layer("writeCaret"),
        "editor.document_highlight.bracket_background": layer("braceBg"),
        "search.match_background": wash("searchBg"), "search.active_match_background": layer("searchBg"),
        # diff and version control
        "editor.diff_hunk.added.background": layer("diffIns"),
        "editor.diff_hunk.added.hollow_background": wash("diffIns"), "editor.diff_hunk.added.hollow_border": c["added"],
        "editor.diff_hunk.deleted.background": layer("diffDel"),
        "editor.diff_hunk.deleted.hollow_background": wash("diffDel"),
        "editor.diff_hunk.deleted.hollow_border": c["deleted"],
        "version_control.added": c["added"], "version_control.modified": c["modified"],
        "version_control.deleted": c["deleted"], "version_control.renamed": c["modified"],
        "version_control.conflict": c["ansiMagenta"], "version_control.ignored": c["muted"],
        "version_control.word_added": over(mix(p["diffIns"], p["added"], 0.35), bg),
        "version_control.word_deleted": over(mix(p["diffDel"], p["deleted"], 0.35), bg),
        "version_control.conflict_marker.ours": layer("diffIns"),
        "version_control.conflict_marker.theirs": layer("diffMod"),
        # terminal
        "terminal.background": c["bgTool"], "terminal.ansi.background": c["bgTool"],
        "terminal.foreground": c["fg"], "terminal.bright_foreground": c["fg"], "terminal.dim_foreground": c["muted"],
        "terminal.ansi.black": c["disabled"], "terminal.ansi.bright_black": c["muted"],
        "terminal.ansi.dim_black": dim("disabled"),
        "terminal.ansi.white": c["op"], "terminal.ansi.bright_white": c["fg"], "terminal.ansi.dim_white": c["muted"],
        **{f"terminal.ansi.{name}": colour for name, colour in ansi.items()},
        **{f"terminal.ansi.bright_{name}": colour for name, colour in ansi.items()},
        **{f"terminal.ansi.dim_{name}": dim("ansi" + name.title()) for name in ansi},
        "vim.yank.background": layer("searchBg"),
    }


def status(p):
    """Status colours: text in a state's colour, its background and its border. Text takes the ANSI colours, which
    the build checks at 4.5:1 against bg and bgTool."""
    c = {k: "#" + v for k, v in p.items() if isinstance(v, str) and re.fullmatch(r"[0-9A-F]{6}", v)}
    def layer(key):
        return over(p[key], p["bg"])
    states = dict(
        conflict=(c["ansiMagenta"], layer("diffConf"), c["gold"]),
        created=(c["ansiGreen"], layer("diffIns"), c["added"]),
        deleted=(c["ansiRed"], layer("diffDel"), c["deleted"]),
        error=(c["ansiRed"], layer("diffDel"), c["error"]),
        hidden=(c["muted"], TRANSPARENT, c["border"]),
        hint=(c["muted"], layer("caretRow"), c["border"]),
        ignored=(c["muted"], TRANSPARENT, c["border"]),
        info=(c["ansiBlue"], layer("diffMod"), c["azure"]),
        modified=(c["ansiBlue"], layer("diffMod"), c["modified"]),
        predictive=(c["muted"], layer("caretRow"), c["border"]),
        renamed=(c["ansiBlue"], layer("diffMod"), c["modified"]),
        success=(c["ansiGreen"], layer("diffIns"), c["added"]),
        unreachable=(c["muted"], TRANSPARENT, c["border"]),
        warning=(c["ansiYellow"], layer("diffConf"), c["warning"]),
    )
    out = {}
    for name, (text, background, border) in states.items():
        out.update({name: text, f"{name}.background": background, f"{name}.border": border})
    return out


def players(p):
    """The local player first, with the caret and the editor selection, then collaborators."""
    caret = "#" + p.get("caret", p["gold"])
    local = {"cursor": caret, "background": caret, "selection": over(p["selection"], p["bg"])}
    others = [{"cursor": "#" + p[role], "background": "#" + p[role], "selection": "#" + p[role] + "3D"}
              for role in PLAYERS]
    return [local, *others]


def theme(p):
    """One entry of a Zed theme family's themes array."""
    return {
        "name": p["name"], "appearance": "dark" if p["dark"] else "light",
        # Rainbow brackets would bring hues the palette does not have, so brackets keep the operator role.
        "style": {**colours(p), **status(p), "accents": ["#" + p["op"]], "players": players(p), "syntax": syntax(p)},
    }


def family(name, palettes):
    """A Zed theme family file for the palettes of one family."""
    return {"$schema": "https://zed.dev/schema/themes/v0.2.0.json", "name": name, "author": AUTHOR,
            "themes": [theme(p) for p in palettes]}
