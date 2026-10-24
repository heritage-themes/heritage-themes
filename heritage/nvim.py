"""Neovim colour scheme and lualine theme generated from a palette.

A colour scheme sets highlight groups: the UI groups of :help highlight-groups, the syntax groups of :help group-name,
the Tree-sitter captures of :help treesitter-highlight-groups and the LSP semantic token groups of
:help lsp-semantic-highlight. The syntax groups map to the palette roles that heritage.zed gives the matching
Tree-sitter captures, and the semantic token groups to the roles that heritage.vscode gives the matching semantic
tokens. Every group that Neovim's default scheme colours is set, so none of its colours shows through; preview.py --nvim
fails when one does.

The UI groups follow the Islands layout of the other targets: the status line, tab line and message separator on the
frame, the editor on bg, and floating windows and the completion menu on surface.
"""
import re

from .vscode import mix

PREFIX = "heritage-"
FONTS = {"": {}, "bold": {"bold": True}, "italic": {"italic": True}, "bold italic": {"bold": True, "italic": True}}
# Attributes that nvim_set_hl accepts and the scheme uses.
COLOURS = ("fg", "bg", "sp")
FLAGS = ("bold", "italic", "underline", "undercurl", "underdouble", "strikethrough", "reverse", "nocombine")
# Groups drawn as rules, borders, gutter marks or filler rather than text, so the contrast check leaves them out.
DECORATIVE = {"LineNr", "LineNrAbove", "LineNrBelow", "CursorLineNr", "SignColumn", "CursorLineSign", "FoldColumn",
              "CursorLineFold", "NonText", "EndOfBuffer", "Whitespace", "WinSeparator", "FloatBorder", "PmenuBorder",
              "MsgSeparator", "DiffDelete", "Ignore", "GitSignsAdd", "GitSignsChange", "GitSignsDelete",
              "@markup.heading.1.delimiter.vimdoc", "@markup.heading.2.delimiter.vimdoc"}
# Groups held to 3:1 rather than 4.5:1: comments, and the block cursor, which the build checks as the caret.
LOW_CONTRAST = {"Comment", "@comment", "@lsp.type.comment", "Cursor", "lCursor", "CursorIM", "TermCursor"}
# Shadows darken what lies under a float, as the shadows of the VS Code theme do.
SHADOW = "#000000"


def name(theme):
    """The colour scheme name of a theme dict from a theme.py, for example "heritage-shuimo-night"."""
    return PREFIX + re.sub(r"(?<!^)(?=[A-Z])", "-", theme["slug"]).lower()


def syntax_rules(p):
    """(group, role, font style) per syntax group, Tree-sitter capture and semantic token group."""
    kw = "bold" if p.get("kwBold", not p["dark"]) else ""
    rules = []
    def s(groups, role, font=""):
        rules.extend((group, role, font) for group in groups.split())
    # :help group-name, which syntax files and many plugins link to
    s("Comment", "comment", "italic")
    s("Constant", "constant", "bold italic")
    s("String Character", "string")
    s("Number Float", "number")
    s("Boolean", "keyword", kw)
    s("Identifier", "fg")
    s("Function", "call")
    s("Statement Conditional Repeat Keyword Exception PreProc Include Define PreCondit StorageClass Structure Typedef",
      "keyword", kw)
    s("Label", "label", "bold")
    s("Operator Delimiter", "op")
    s("Macro Debug", "annotation")
    s("Type", "type")
    s("Special", "gold")
    s("SpecialChar", "gold", "bold")
    s("Tag", "azure")
    s("SpecialComment", "docTag", "bold italic")
    s("Todo", "todo", "bold italic")
    s("Error", "ansiRed")
    s("Added", "ansiGreen")
    s("Changed", "ansiBlue")
    s("Removed", "ansiRed")
    # :help treesitter-highlight-groups. Neovim colours a capture with the longest group that is a dot-separated
    # prefix of it, as Zed does, so the captures take the roles of heritage.zed.
    s("@variable @module @module.builtin", "fg")
    s("@variable.builtin", "keyword", "italic")
    s("@variable.parameter", "param")
    s("@variable.parameter.builtin", "param", "italic")
    s("@variable.member @property", "field")
    s("@constant @constant.macro @string.special.symbol", "constant", "bold italic")
    s("@constant.builtin @boolean @type.builtin", "keyword", kw)
    s("@label", "label", "bold")
    s("@string @string.regexp @string.special @string.special.path @character @markup.raw @markup.raw.block "
      "@markup.math", "string")
    s("@string.documentation @comment.documentation @markup.quote", "doc", "italic")
    s("@string.escape @character.special", "gold", "bold")
    s("@string.special.url @markup.link.url", "call", "italic")
    s("@number @number.float", "number")
    s("@type @type.definition @constructor", "type")
    s("@attribute @attribute.builtin @function.macro", "annotation")
    s("@function @function.method", "method", "bold")
    s("@function.call @function.method.call", "call")
    s("@function.builtin", "call", "italic")
    s("@operator @keyword.conditional.ternary @punctuation @punctuation.delimiter @punctuation.bracket "
      "@punctuation.special", "op")
    s("@keyword @keyword.coroutine @keyword.function @keyword.operator @keyword.import @keyword.type "
      "@keyword.modifier @keyword.repeat @keyword.return @keyword.debug @keyword.exception @keyword.conditional "
      "@keyword.directive @keyword.directive.define @markup.list @markup.list.checked @markup.list.unchecked "
      "@tag @tag.builtin", "keyword", kw)
    s("@tag.attribute", "field")
    s("@tag.delimiter", "keyword")
    s("@comment", "comment", "italic")
    s("@comment.error @comment.warning @comment.todo @comment.note", "todo", "bold italic")
    # Markdown: headings take the declaration role, markers the keyword role
    s("@markup.heading @markup.heading.1 @markup.heading.2 @markup.heading.3 @markup.heading.4 @markup.heading.5 "
      "@markup.heading.6", "method", "bold")
    s("@markup.strong", "fg", "bold")
    s("@markup.italic", "fg", "italic")
    s("@markup.link @markup.link.label", "azure")
    s("@diff.plus", "ansiGreen")
    s("@diff.minus", "ansiRed")
    s("@diff.delta", "ansiBlue")
    # A capture specialised by language (@capture.<language>) where nvim-treesitter's queries give a construct a capture
    # whose role differs from the one the other targets give it. Regular expressions read as strings with their
    # operators picked out, as in the Zed and VS Code themes.
    s("@constant.regex", "string")
    s("@punctuation.bracket.regex @punctuation.delimiter.regex @operator.regex @variable.builtin.regex", "gold", "bold")
    s("@number.regex", "number", "bold")
    s("@function.css", "call")  # function calls such as url()
    s("@constant.html", "keyword")  # <!DOCTYPE>
    s("@attribute.sql", "keyword", kw)  # ASC, DESC and other modifier keywords
    s("@attribute.rust @attribute.builtin.rust", "typeParam", "italic")  # lifetimes
    s("@label.yaml", "annotation")  # anchors and aliases
    s("@label.markdown", "constant", "bold italic")  # the language of a code fence
    # :help lsp-semantic-highlight. A @lsp.typemod group outranks the @lsp.type group of its token, so declarations
    # take the declaration role over the call role, as in the VS Code theme.
    s("@lsp.type.namespace @lsp.type.variable", "fg")
    s("@lsp.type.class @lsp.type.struct @lsp.type.enum @lsp.type.type @lsp.type.event", "type")
    s("@lsp.type.interface", "type", "italic")
    s("@lsp.type.typeParameter", "typeParam", "bold")
    s("@lsp.type.enumMember", "constant", "bold italic")
    s("@lsp.type.function @lsp.type.method", "call")
    s("@lsp.typemod.method.static @lsp.typemod.function.defaultLibrary @lsp.typemod.method.defaultLibrary",
      "call", "italic")
    s("@lsp.typemod.function.declaration @lsp.typemod.function.definition @lsp.typemod.method.declaration "
      "@lsp.typemod.method.definition", "method", "bold")
    s("@lsp.type.property", "field")
    s("@lsp.typemod.property.static", "field", "italic")
    s("@lsp.type.parameter", "param")
    s("@lsp.type.decorator @lsp.type.macro @lsp.type.attribute @lsp.type.builtinAttribute", "annotation")
    s("@lsp.type.label", "label", "bold")
    s("@lsp.type.keyword @lsp.type.modifier @lsp.type.selfKeyword @lsp.type.builtinType", "keyword", kw)
    s("@lsp.type.selfParameter @lsp.type.clsParameter", "keyword", "italic")
    s("@lsp.type.lifetime", "typeParam", "italic")
    s("@lsp.type.formatSpecifier @lsp.type.escapeSequence", "gold", "bold")
    s("@lsp.type.comment", "comment", "italic")
    s("@lsp.type.string @lsp.type.regexp", "string")
    s("@lsp.type.number", "number")
    s("@lsp.type.operator", "op")
    return rules


def ui_groups(p):
    """UI group to highlight definition, with #-prefixed colours."""
    c = {k: "#" + v for k, v in p.items() if isinstance(v, str) and re.fullmatch(r"[0-9A-F]{6}", v)}
    caret = "#" + p.get("caret", p["gold"])
    def wash(key):
        """Halfway from bg to the palette colour."""
        return "#" + mix(p["bg"], p[key], 0.5)
    def deepen(key, towards):
        """The diff background moved towards its gutter colour, for the changed text in a changed line."""
        return "#" + mix(p[key], p[towards], 0.35)
    return {
        # editor
        "Normal": dict(fg=c["fg"], bg=c["bg"]),
        "NormalNC": {},
        "Cursor": dict(fg=c["bg"], bg=caret), "lCursor": dict(fg=c["bg"], bg=caret),
        "CursorIM": dict(fg=c["bg"], bg=caret), "TermCursor": dict(fg=c["bg"], bg=caret),
        "CursorLine": dict(bg=c["caretRow"]), "CursorColumn": dict(bg=c["caretRow"]),
        "ColorColumn": dict(bg=c["guide"]),
        "LineNr": dict(fg=c["lineNo"]), "LineNrAbove": dict(fg=c["lineNo"]), "LineNrBelow": dict(fg=c["lineNo"]),
        "CursorLineNr": dict(fg=c["lineNoCaret"]),
        "SignColumn": dict(fg=c["lineNo"]), "CursorLineSign": dict(fg=c["lineNo"]),
        "FoldColumn": dict(fg=c["lineNo"]), "CursorLineFold": dict(fg=c["lineNo"]),
        "Folded": dict(fg=c["muted"], bg=c["caretRow"]),
        "NonText": dict(fg=c["lineNo"]), "EndOfBuffer": dict(fg=c["lineNo"]), "Whitespace": dict(fg=c["guide"]),
        "SpecialKey": dict(fg=c["muted"]), "Conceal": dict(fg=c["muted"]),
        "Visual": dict(bg=c["selection"]), "VisualNOS": dict(bg=c["selInactive"]),
        # Matches keep their syntax colours on a wash of searchBg; the current match takes searchBg and plain text.
        "Search": dict(bg=wash("searchBg")), "Substitute": dict(bg=wash("searchBg")),
        "CurSearch": dict(fg=c["fg"], bg=c["searchBg"], bold=True),
        "IncSearch": dict(fg=c["fg"], bg=c["searchBg"], bold=True),
        "MatchParen": dict(bg=c["braceBg"], bold=True),
        "QuickFixLine": dict(bg=c["selection"]),
        "SnippetTabstop": dict(bg=c["underCaret"]), "SnippetTabstopActive": dict(bg=c["writeCaret"]),
        "Directory": dict(fg=c["ansiBlue"]), "Title": dict(fg=c["method"], bold=True),
        "SpellBad": dict(sp=c["error"], undercurl=True), "SpellCap": dict(sp=c["warning"], undercurl=True),
        "SpellLocal": dict(sp=c["azure"], undercurl=True), "SpellRare": dict(sp=c["ansiMagenta"], undercurl=True),
        "WinSeparator": dict(fg=c["border"], bg=c["bg"]),
        "WinBar": dict(fg=c["fg"], bg=c["bg"], bold=True), "WinBarNC": dict(fg=c["muted"], bg=c["bg"]),
        # frame: status line, tab line and messages. The active tab joins the editor, as in the Zed theme.
        "StatusLine": dict(fg=c["fg"], bg=c["frame"]), "StatusLineNC": dict(fg=c["muted"], bg=c["frame"]),
        "StatusLineTerm": dict(fg=c["fg"], bg=c["frame"]), "StatusLineTermNC": dict(fg=c["muted"], bg=c["frame"]),
        "TabLine": dict(fg=c["muted"], bg=c["frame"]), "TabLineFill": dict(bg=c["frame"]),
        "TabLineSel": dict(fg=c["fg"], bg=c["bg"], bold=True),
        "MsgArea": dict(fg=c["fg"]), "MsgSeparator": dict(fg=c["border"], bg=c["frame"]),
        "ModeMsg": dict(fg=c["fg"], bold=True), "MoreMsg": dict(fg=c["ansiGreen"]),
        "Question": dict(fg=c["ansiGreen"]), "OkMsg": dict(fg=c["ansiGreen"]),
        "WarningMsg": dict(fg=c["ansiYellow"]), "ErrorMsg": dict(fg=c["ansiRed"]),
        "StderrMsg": dict(fg=c["ansiRed"]), "StdoutMsg": {},
        # popups: floating windows and the completion menu. Matches take ansiBlue, as VS Code's lists do.
        "NormalFloat": dict(fg=c["fg"], bg=c["surface"]), "FloatBorder": dict(fg=c["border"], bg=c["surface"]),
        "FloatTitle": dict(fg=c["fg"], bg=c["surface"], bold=True),
        "FloatFooter": dict(fg=c["muted"], bg=c["surface"]),
        "FloatShadow": dict(bg=SHADOW, blend=80), "FloatShadowThrough": dict(bg=SHADOW, blend=100),
        "Pmenu": dict(fg=c["fg"], bg=c["surface"]), "PmenuSel": dict(fg=c["fg"], bg=c["selection"]),
        "PmenuKind": dict(fg=c["muted"], bg=c["surface"]), "PmenuKindSel": dict(fg=c["fg"], bg=c["selection"]),
        "PmenuExtra": dict(fg=c["muted"], bg=c["surface"]), "PmenuExtraSel": dict(fg=c["fg"], bg=c["selection"]),
        "PmenuMatch": dict(fg=c["ansiBlue"], bg=c["surface"], bold=True),
        "PmenuMatchSel": dict(fg=c["ansiBlue"], bg=c["selection"], bold=True),
        "PmenuSbar": dict(bg=c["surface"]), "PmenuThumb": dict(bg=c["guideSel"]),
        "PmenuBorder": dict(fg=c["border"], bg=c["surface"]),
        "PmenuShadow": dict(bg=SHADOW, blend=80), "PmenuShadowThrough": dict(bg=SHADOW, blend=100),
        "WildMenu": dict(fg=c["fg"], bg=c["selection"]),
        "ComplMatchIns": {}, "PreInsert": dict(fg=c["muted"]),
        "ComplHint": dict(fg=c["muted"]), "ComplHintMore": dict(fg=c["muted"]),
        # diff mode
        "DiffAdd": dict(bg=c["diffIns"]), "DiffChange": dict(bg=c["diffMod"]),
        "DiffDelete": dict(fg=c["deleted"], bg=c["diffDel"]),
        "DiffText": dict(bg=deepen("diffMod", "modified")), "DiffTextAdd": dict(bg=deepen("diffIns", "added")),
        # diagnostics. Text takes the ANSI colours, which the build checks at 4.5:1 against bg; undercurls take the
        # diagnostic colours of the other targets.
        "DiagnosticError": dict(fg=c["ansiRed"]), "DiagnosticWarn": dict(fg=c["ansiYellow"]),
        "DiagnosticInfo": dict(fg=c["ansiBlue"]), "DiagnosticHint": dict(fg=c["muted"]),
        "DiagnosticOk": dict(fg=c["ansiGreen"]),
        "DiagnosticUnderlineError": dict(sp=c["error"], undercurl=True),
        "DiagnosticUnderlineWarn": dict(sp=c["warning"], undercurl=True),
        "DiagnosticUnderlineInfo": dict(sp=c["azure"], undercurl=True),
        "DiagnosticUnderlineHint": dict(sp=c["weak"], undercurl=True),
        "DiagnosticUnderlineOk": dict(sp=c["added"], undercurl=True),
        "DiagnosticDeprecated": dict(sp=c["muted"], strikethrough=True),
        "DiagnosticUnnecessary": dict(fg=c["muted"], italic=True),
        # LSP
        "LspReferenceText": dict(bg=c["underCaret"]), "LspReferenceRead": dict(bg=c["underCaret"]),
        "LspReferenceWrite": dict(bg=c["writeCaret"]), "LspReferenceTarget": dict(bg=c["underCaret"]),
        "LspInlayHint": dict(fg=c["muted"], bg=c["caretRow"]),
        "LspCodeLens": dict(fg=c["muted"]), "LspCodeLensSeparator": dict(fg=c["muted"]),
        "LspSignatureActiveParameter": dict(bg=c["underCaret"], bold=True),
        # Help headings draw their ===== and ----- lines as an underline in the text colour.
        "@markup.heading.1.delimiter.vimdoc": dict(fg=c["bg"], bg=c["bg"], sp=c["muted"], underdouble=True,
                                                   nocombine=True),
        "@markup.heading.2.delimiter.vimdoc": dict(fg=c["bg"], bg=c["bg"], sp=c["muted"], underline=True,
                                                   nocombine=True),
        "@markup.strikethrough": dict(strikethrough=True), "@markup.underline": dict(underline=True),
        "@lsp.mod.deprecated": dict(strikethrough=True),
        "Underlined": dict(fg=c["azure"], underline=True),
        "Ignore": dict(fg=c["disabled"]),
        # Neovim's own groups: :Inspect on an expression in the command line, and the redraw debugger
        "NvimInternalError": dict(fg=c["redText"], bg=c["red"]),
        "RedrawDebugNormal": dict(reverse=True), "RedrawDebugClear": dict(bg=c["diffConf"]),
        "RedrawDebugComposed": dict(bg=c["diffIns"]), "RedrawDebugRecompose": dict(bg=c["diffDel"]),
        # gitsigns: gutter marks in the VCS colours of the other targets' gutters
        "GitSignsAdd": dict(fg=c["added"]), "GitSignsChange": dict(fg=c["modified"]),
        "GitSignsDelete": dict(fg=c["deleted"]),
    }


def highlights(p):
    """Every highlight group of the colour scheme: UI groups first, then syntax groups."""
    out = ui_groups(p)
    for group, role, font in syntax_rules(p):
        if group in out:
            raise ValueError(f"{group} is set twice")
        out[group] = dict(fg="#" + p[role], **FONTS[font])
    return out


def terminal(p):
    """The 16 colours of Neovim's terminal, as the Zed theme gives them."""
    normal = [p["disabled"], *(p["ansi" + n] for n in ("Red", "Green", "Yellow", "Blue", "Magenta", "Cyan")), p["op"]]
    bright = [p["muted"], *normal[1:7], p["fg"]]
    return ["#" + v for v in normal + bright]


def lualine(p):
    """lualine theme: modes in the ANSI colours with bg text, the other sections on the frame like the status line."""
    c = {k: "#" + v for k, v in p.items() if isinstance(v, str) and re.fullmatch(r"[0-9A-F]{6}", v)}
    def mode(colour):
        return {"a": dict(fg=c["bg"], bg=colour, gui="bold"), "b": dict(fg=c["fg"], bg=c["hover"]),
                "c": dict(fg=c["fg"], bg=c["frame"])}
    return {
        "normal": mode(c["ansiBlue"]), "insert": mode(c["ansiGreen"]), "visual": mode(c["ansiMagenta"]),
        "replace": mode(c["ansiRed"]), "command": mode(c["ansiYellow"]), "terminal": mode(c["ansiCyan"]),
        "inactive": {"a": dict(fg=c["muted"], bg=c["frame"], gui="bold"), "b": dict(fg=c["muted"], bg=c["frame"]),
                     "c": dict(fg=c["muted"], bg=c["frame"])},
    }


def lua(value):
    """A Lua literal for a string, number, boolean or dict of them."""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, str):
        return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'
    return "{ " + ", ".join(f"{k} = {lua(v)}" for k, v in value.items()) + " }" if value else "{}"


def colorscheme(p, scheme, source):
    """The colors/<scheme>.lua file for a palette. source is the URL of the theme folder."""
    lines = [
        f"-- {p['name']}: a Heritage Themes colour scheme for Neovim.",
        f"-- Generated from {source}; changes here are overwritten.",
        f'vim.o.background = "{"dark" if p["dark"] else "light"}"',
        'vim.cmd.highlight("clear")',
        f"vim.g.colors_name = {lua(scheme)}",
        "",
        "local function hl(group, definition)",
        "  vim.api.nvim_set_hl(0, group, definition)",
        "end",
        "",
        *(f"hl({lua(group)}, {lua(definition)})" for group, definition in highlights(p).items()),
        "",
        *(f"vim.g.terminal_color_{i} = {lua(colour)}" for i, colour in enumerate(terminal(p))),
    ]
    return "\n".join(lines) + "\n"


def lualine_theme(p, source):
    """The lua/lualine/themes/<scheme>.lua file for a palette, which lualine's auto theme loads for the scheme."""
    sections = ",\n".join(f"  {mode} = {lua(parts)}" for mode, parts in lualine(p).items())
    return (f"-- {p['name']}: a Heritage Themes lualine theme.\n"
            f"-- Generated from {source}; changes here are overwritten.\n"
            f"return {{\n{sections},\n}}\n")
