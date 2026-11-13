"""Vim colour scheme generated from a palette.

A colour scheme sets highlight groups: the UI groups of :help highlight-groups and the syntax groups of :help group-name,
which Vim's syntax files link their own groups to. Groups that Vim and Neovim share take the definitions of
heritage.nvim, so the two schemes agree; the groups that only Vim has follow the same layout. Every group that Vim's
default scheme colours is set, so none of its colours shows through; preview.py --vim fails when one does.

Where a syntax file links a construct to a group whose role differs from the one the other targets give it, the
language's own group is set (language_rules): Java annotations and Python decorators take the annotation role rather than
PreProc's keyword role, for example.

Each group has its colour for 'termguicolors' and the GUI, and the nearest of the 240 colours of a 256-colour terminal
beyond its 16 user-defined ones, for a terminal without 24-bit colour.
"""
import re

from . import nvim
from .colour import lab
from .nvim import name  # noqa: F401 - Vim lists a scheme by the same name as Neovim

# Attributes of :highlight that the scheme uses.
COLOURS = ("fg", "bg", "sp")
FLAGS = ("bold", "italic", "underline", "undercurl", "underdouble", "strikethrough", "reverse", "nocombine")
# The UI groups that Vim and Neovim share, defined by heritage.nvim.
SHARED = (
    "Normal", "Cursor", "lCursor", "CursorIM", "CursorLine", "CursorColumn", "ColorColumn",
    "LineNr", "LineNrAbove", "LineNrBelow", "CursorLineNr", "SignColumn", "CursorLineSign", "FoldColumn",
    "CursorLineFold", "Folded", "NonText", "EndOfBuffer", "SpecialKey", "Conceal", "Visual", "VisualNOS",
    "Search", "CurSearch", "IncSearch", "MatchParen", "QuickFixLine", "Directory", "Title",
    "SpellBad", "SpellCap", "SpellLocal", "SpellRare",
    "StatusLine", "StatusLineNC", "StatusLineTerm", "StatusLineTermNC", "TabLine", "TabLineFill", "TabLineSel",
    "MsgArea", "ModeMsg", "MoreMsg", "Question", "WarningMsg", "ErrorMsg",
    "Pmenu", "PmenuSel", "PmenuKind", "PmenuKindSel", "PmenuExtra", "PmenuExtraSel", "PmenuMatch", "PmenuMatchSel",
    "PmenuSbar", "PmenuThumb", "PmenuBorder", "WildMenu", "ComplMatchIns", "PreInsert",
    "DiffAdd", "DiffChange", "DiffDelete", "DiffText", "DiffTextAdd", "Underlined", "Ignore",
)
# Groups drawn as rules, borders, gutter marks or filler rather than text, so the contrast check leaves them out.
DECORATIVE = nvim.DECORATIVE | {"VertSplit", "VertSplitNC", "PopupBorder", "TabPanelFill", "Scrollbar"}
# Groups held to 3:1 rather than 4.5:1: comments, and the cursor, which the build checks as the caret.
LOW_CONTRAST = {"Comment", "Cursor", "lCursor", "CursorIM"}
# The levels of the 6x6x6 colour cube of a 256-colour terminal, and its 24 greys.
CUBE = (0, 95, 135, 175, 215, 255)
GREYS = tuple(8 + 10 * i for i in range(24))


def ui_groups(p):
    """UI group to highlight definition, with #-prefixed colours."""
    shared = nvim.ui_groups(p)
    groups = {group: shared[group] for group in SHARED}
    c = {k: "#" + v for k, v in p.items() if isinstance(v, str) and re.fullmatch(r"[0-9A-F]{6}", v)}
    return {
        **groups,
        # Vim's window separator, which it draws between windows side by side
        "VertSplit": dict(fg=c["border"], bg=c["bg"]), "VertSplitNC": dict(fg=c["border"], bg=c["bg"]),
        # popup windows, which plugins and the info popup of the completion menu open, as Neovim's floating windows
        "Popup": dict(fg=c["fg"], bg=c["surface"]), "PopupBorder": dict(fg=c["border"], bg=c["surface"]),
        "PopupTitle": dict(fg=c["fg"], bg=c["surface"], bold=True),
        "PopupSelected": dict(fg=c["fg"], bg=c["selection"]),
        "PopupNotification": dict(fg=c["ansiYellow"], bg=c["surface"]),
        "MessageWindow": dict(fg=c["fg"], bg=c["surface"]),
        "PmenuShadow": dict(bg=c["frame"]),
        # the tab panel beside the editor, on the frame like the tab line
        "TabPanel": dict(fg=c["muted"], bg=c["frame"]), "TabPanelSel": dict(fg=c["fg"], bg=c["bg"], bold=True),
        "TabPanelFill": dict(bg=c["frame"]),
        # window toolbars, the GUI's menus, scroll bars and tooltips, and the terminal window
        "ToolbarLine": dict(fg=c["fg"], bg=c["frame"]), "ToolbarButton": dict(fg=c["fg"], bg=c["hover"], bold=True),
        "Menu": dict(fg=c["fg"], bg=c["surface"]), "Tooltip": dict(fg=c["fg"], bg=c["surface"]),
        "Scrollbar": dict(fg=c["guideSel"], bg=c["bg"]),
        "Terminal": dict(fg=c["fg"], bg=c["bg"]),
        # bold and italic text in help files and Markdown
        "Bold": dict(bold=True), "Italic": dict(italic=True), "BoldItalic": dict(bold=True, italic=True),
    }


def syntax_rules(p):
    """(group, role, font style) per syntax group: the groups of :help group-name, as heritage.nvim maps them."""
    return [(group, role, font) for group, role, font in nvim.syntax_rules(p) if not group.startswith("@")]


def language_rules(p):
    """(group, role, font style) per group of a syntax file whose default link gives its construct a role other than
    the one the other targets give it."""
    rules = []
    def s(groups, role, font=""):
        rules.extend((group, role, font) for group in groups.split())
    # annotations, decorators and attributes, which the syntax files link to PreProc, Define or Identifier
    s("javaAnnotation javaAnnotationStart ktAnnotation pythonDecorator pythonDecoratorName rustAttribute rustDerive",
      "annotation")
    # C and C++ preprocessor directives, which link to PreProc, Include, PreCondit and Macro, groups that other syntax
    # files also link imports, keywords and macros to. #define and #undef colour the macro they name as well.
    s("cPreProc cInclude cPreCondit cDefine", "directive")
    s("rustLifetime", "typeParam", "italic")  # Special
    s("rustSelf", "keyword", "italic")  # Constant
    s("rustSigil", "op")  # & and * before a type, StorageClass
    s("cssColor", "number")  # Constant
    s("typescriptEndColons", "op")  # ; and , after a member of a type, Exception
    # Function names where they are declared, linked to Function or Identifier as calls are. Go's and Java's syntax
    # files mark them when go_highlight_functions or java_highlight_functions is set.
    s("goFunction javaFuncDef pythonFunction rustFuncName shFunctionOne typescriptFuncName", "method", "bold")
    s("goFunctionCall", "call")  # Type, when go_highlight_function_calls is set
    s("pythonBuiltin", "call", "italic")  # Python's built-in functions and types, Function
    # The methods and properties of TypeScript's standard library, Keyword or Structure (Vim 9.2's typescriptcommon.vim)
    s(typescript("""
        ArrayMethod ArrayStaticMethod BOMHistoryMethod BOMLocationMethod BOMNavigatorMethod BOMWindowMethod BlobMethod
        CacheMethod ConsoleMethod CryptoMethod DOMDocMethod DOMEventMethod DOMEventTargetMethod DOMFormMethod
        DOMNodeMethod DOMStorageMethod DateMethod DateStaticMethod ES6MapMethod ES6SetMethod EncodingMethod
        FileListMethod FileMethod FileReaderMethod FunctionMethod GeolocationMethod GlobalMethod HeadersMethod
        IntlMethod JSONStaticMethod MathStaticMethod NumberMethod NumberStaticMethod ObjectMethod ObjectStaticMethod
        PaymentMethod PaymentResponseMethod PromiseMethod PromiseStaticMethod ReflectMethod RegExpMethod RequestMethod
        ResponseMethod ServiceWorkerMethod StringMethod StringStaticMethod SubtleCryptoMethod SymbolStaticMethod
        URLStaticMethod XHRMethod"""), "call")
    s(typescript("""
        BOMHistoryProp BOMLocationProp BOMNavigatorProp BOMNetworkProp BOMWindowProp CryptoProp DOMDocProp DOMEventProp
        DOMFormProp DOMNodeProp DOMStorageProp ES6MapProp ES6SetProp EncodingProp FileReaderProp MathStaticProp
        NumberStaticProp PaymentAddressProp PaymentProp PaymentResponseProp PaymentShippingOptionProp RegExpProp
        RegExpStaticProp RequestProp ResponseProp ServiceWorkerProp SymbolStaticProp URLUtilsProp XHRProp"""), "field")
    # The code of an HTML or Vue <script> that no JavaScript group marks, Special
    s("javaScript", "fg")
    return rules


def typescript(names):
    """The TypeScript syntax groups of whitespace-separated names without their typescript prefix."""
    return " ".join("typescript" + n for n in names.split())


def highlights(p):
    """Every highlight group of the colour scheme: UI groups, then syntax groups, then the groups of syntax files."""
    out = ui_groups(p)
    for group, role, font in syntax_rules(p) + language_rules(p):
        if group in out:
            raise ValueError(f"{group} is set twice")
        out[group] = dict(fg="#" + p[role], **nvim.FONTS[font])
    return out


def terminal(p):
    """The 16 colours of Vim's terminal window, as the Neovim scheme gives them."""
    return nvim.terminal(p)


def xterm_colours():
    """Index → (r, g, b) of colours 16 to 255 of a 256-colour terminal, which terminals do not let users redefine."""
    colours = {16 + 36 * r + 6 * g + b: (CUBE[r], CUBE[g], CUBE[b]) for r in range(6) for g in range(6) for b in range(6)}
    colours.update({232 + i: (v, v, v) for i, v in enumerate(GREYS)})
    return colours


XTERM = {index: lab(rgb) for index, rgb in xterm_colours().items()}


def cterm(colour):
    """The index of the 256-colour terminal colour nearest to a #RRGGBB colour, by the CIE76 distance."""
    target = lab(tuple(int(colour[i:i + 2], 16) for i in (1, 3, 5)))
    return min(XTERM, key=lambda index: sum((a - b) ** 2 for a, b in zip(XTERM[index], target)))


def command(group, definition):
    """The :highlight command for a group. Every attribute is set, so nothing of Vim's default scheme remains."""
    flags = ",".join(flag for flag in FLAGS if definition.get(flag)) or "NONE"
    parts = [f"hi {group}"]
    for key, gui, term in (("fg", "guifg", "ctermfg"), ("bg", "guibg", "ctermbg"), ("sp", "guisp", "ctermul")):
        colour = definition.get(key)
        parts.append(f"{gui}={colour or 'NONE'}")
        parts.append(f"{term}={cterm(colour) if colour else 'NONE'}")
    parts += [f"gui={flags}", f"cterm={flags}", "term=NONE"]
    return " ".join(parts)


def colorscheme(p, scheme, source):
    """The colors/<scheme>.vim file for a palette. source is the URL of the theme folder."""
    colours = ", ".join(f"'{c}'" for c in terminal(p))
    lines = [
        f'" {p["name"]}: a Heritage Themes colour scheme for Vim.',
        f'" Generated from {source}; changes here are overwritten.',
        f"set background={'dark' if p['dark'] else 'light'}",
        "hi clear",
        f"let g:colors_name = '{scheme}'",
        "",
        *(command(group, definition) for group, definition in highlights(p).items()),
        "",
        f"let g:terminal_ansi_colors = [{colours}]",
    ]
    return "\n".join(lines) + "\n"
