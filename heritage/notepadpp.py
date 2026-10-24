"""Notepad++ theme XML generated from a palette.

notepadpp.json lists the lexers and styles of stylers.model.xml in the Notepad++ release that
scripts/notepadpp/source.json pins; scripts/notepadpp/styles.py writes it. A theme sets every one of them, so no
colour of Notepad++'s default theme shows through. Each style takes the palette role that heritage.vscode gives the
matching TextMate scope: the rules for its lexer in LEXERS when they name it, else the first rule in NAMES that
matches its name. A style that neither covers fails the build. The styles of a lexer keep the Default Style's
background (colorStyle 1), so the editor has one background, as the theme guide of Notepad++'s Themes Collection
recommends.

GlobalStyles colour the editor around the text: caret, selection, margins, fold markers, highlights, the document map,
the bar that marks the active tab and, in Light Mode, the text of the tabs and the background of inactive ones.
Notepad++ draws the menu bar, toolbar, dialogs and, in Dark Mode, the tabs from its own Dark Mode settings, which a
theme does not carry; DARK_MODE and LIGHT_MODE hold its default colours, which the preview draws them in.
"""
import json, os, re
from xml.sax.saxutils import escape

from .vscode import mix

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "notepadpp.json")
with open(DATA, encoding="utf-8") as f:
    MODEL = json.load(f)
FONT_NAME, FONT_SIZE = "Consolas", 10  # the monospaced font of Windows, as Notepad++'s DarkModeDefault theme sets it
BOLD, ITALIC, UNDERLINE = 1, 2, 4
FONTS = {"": 0, "bold": BOLD, "italic": ITALIC, "bold italic": BOLD | ITALIC, "underline": UNDERLINE}
COLORSTYLE_FOREGROUND = 1
QUOTE = {'"': "&quot;"}  # escaped in attribute values besides &, < and >
# The colours Notepad++ draws its own window in: the menu bar and toolbar (frame), the tab bar and status bar
# (background), the active tab (control) and their text. In Dark Mode they are its default Black tone (darkColors in
# NppDarkMode.cpp); in Light Mode they are the Windows system colours of menus and buttons.
DARK_MODE = dict(frame="202020", background="202020", control="383838", text="E0E0E0")
LIGHT_MODE = dict(frame="FFFFFF", background="F0F0F0", control="F0F0F0", text="000000")
# Roles of the user keyword lists, which Notepad++ fills from the words a user adds in the Style Configurator. Each
# list takes its own role, as IntelliJ's custom file types colour keywords 1 to 4.
USER = {1: ("type", ""), 2: ("call", ""), 3: ("field", ""), 4: ("constant", "bold italic"), 5: ("annotation", ""),
        6: ("typeParam", "italic"), 7: ("label", "bold"), 8: ("param", "italic")}
# Terminal colours, as heritage.nvim gives them, for the lexers that show ANSI escape sequences in colour: the eight
# normal colours, and the bright ones, which differ only for black and white.
TERMINAL = {"BLACK": "disabled", "RED": "ansiRed", "GREEN": "ansiGreen", "YELLOW": "ansiYellow", "BLUE": "ansiBlue",
            "MAGENTA": "ansiMagenta", "CYAN": "ansiCyan", "WHITE": "op"}
BRIGHT = dict(TERMINAL, BLACK="muted", WHITE="fg")
# The 16 colours of the ErrorList lexer by their names there.
ERROR_LIST_ANSI = {**{f"ANSI COLOR {c}": TERMINAL[c] for c in ("BLACK", "RED", "GREEN", "BLUE", "MAGENTA", "CYAN")},
                   **{f"ANSI COLOR BRIGHT {c}": BRIGHT[c] for c in ("RED", "GREEN", "BLUE", "MAGENTA", "CYAN")},
                   "ANSI COLOR BROWN": TERMINAL["YELLOW"], "ANSI COLOR GRAY": TERMINAL["WHITE"],
                   "ANSI COLOR DARK GRAY": BRIGHT["BLACK"], "ANSI COLOR YELLOW": BRIGHT["YELLOW"],
                   "ANSI COLOR WHITE": BRIGHT["WHITE"]}
# "kw" stands for the keyword font: bold where the palette's keywords are bold.
KW = "kw"

# Rules by style name, in order: (pattern, role, font). They cover the names that many lexers share.
NAMES = [(re.compile(pattern, re.I), role, font) for pattern, role, font in (
    (r"^(DEFAULT( STYLE| TEXT STYLE)?|WHITE ?SPACE|IDENTIFIERS?|ANY OTHER TEXT|TEXT|NAME)$", "fg", ""),
    (r"^USER (KEYWORDS?|TAGS|ATTRIBUTES|SCALAR) ?\d$|^USER ?\d$", "user", ""),
    (r"^(USER( KEYWORDS?| DEFINED?)?|KEYWORD USER)$", "user", ""),
    (r"COMMENT DOC KEYWORD ERROR|COMMENT KEY ERROR", "docTag", "italic"),
    (r"COMMENT DOC KEYWORD|COMMENT KEY|DOCUMENTATION (HELPER|MACRO)", "docTag", "bold italic"),
    (r"\bDOC\b.*COMMENT|COMMENT.*\bDOC\b|^POD", "doc", "italic"),
    (r"COMMENT", "comment", "italic"),
    (r"^VAR IN |VAR$|VARIABLE|SCALAR|^ARRAY$|^HASH$|GLOBAL", "field", "italic"),
    (r"ERROR|ILLEGAL|^BAD |_WRONG|GARBAGE|_UNKNOWN$|UNKNOWN OPCODE|TOO MANY|EOL OPEN|INFIXEOL", "ansiRed", ""),
    (r"ESCAPE|SPECIAL CHAR", "gold", "bold"),
    (r"REGEX", "string", ""),
    (r"STRING|CHARACTER|^CHARS?$|VERBATIM|TRIPLE|LITERAL|HEREDOC|^HERE |BACKTICKS|CDATA", "string", ""),
    (r"NUMBER|NUMERIC|HEX ?DIGIT|^HEXADECIMAL", "number", ""),
    (r"^OPERATORS?\b|OPERATOR2|DELIMITER|SYMBOLS$|BRACES", "op", ""),
    (r"PREPROC|DIRECTIVE", "keyword", KW),
    (r"DECORATOR|ANNOTATION|MACRO", "annotation", ""),
    (r"LABEL", "label", "bold"),
    (r"CLASS NAME|^CLASS$|^TYPES?$|TYPEDEF|DATA TYPE", "type", ""),
    (r"DEF NAME|FUNC NAME|FUNCTION NAME|METHOD NAME|FUNCTION DEFINITION", "method", "bold"),
    (r"^PARAM(ETER)?S?$", "param", ""),
    (r"KEYWORD|INSTRUCTION WORD|^INSTRUCTION$|^WORD\d?$|RESERVED|STATEMENT|^SECTION$|^CONTROL$", "keyword", KW),
    (r"FUNCTION|^FUNC\d$|CMDLET|BUILT-?IN|OPCODE|COMMAND", "call", ""),
    (r"CONSTANT|PREDEFINED", "constant", "bold italic"),
)]

# Rules for one lexer: (style names separated by |, role, font). They take precedence over NAMES.
CPP = (
    ("TYPE WORD", "keyword", KW),  # primitive types and modifiers
    ("PREDECLARED IDENTIFIERS", "keyword", "italic"),  # Go: true, nil, iota and the built-in functions
    ("WINDOW INSTRUCTION", "call", "italic"),  # JavaScript's browser globals
    ("DIRECTIVE|QUALIFIER", "keyword", KW),  # Objective-C
)
HYPERTEXT = (
    ("TAG|TAG END|XML START|XML END", "keyword", ""),
    ("TAG UNKNOWN", "type", ""),  # custom elements
    ("ATTRIBUTE|ATTRIBUTE UNKNOWN", "field", ""),
    ("VALUE|DOUBLE STRING|SINGLE STRING|CDATA", "string", ""),
    ("ENTITY", "gold", ""),
    ("SGML DEFAULT|SGML COMMAND|SGML 1ST PARAM|SGML BLOCK DEFAULT", "keyword", ""),  # <!DOCTYPE html>
)
LEXERS = {
    **{name: CPP for name in ("actionscript", "c", "cpp", "cs", "go", "java", "javascript.js", "objc", "rc", "swift",
                              "typescript")},
    "javascript.js": (("TYPE WORD", "type", ""),) + CPP,  # Array, Date, Math and the other built-in objects
    "coffeescript": CPP + (("PREDEFINED CONSTANT", "keyword", KW),),
    "html": HYPERTEXT, "xml": HYPERTEXT,
    "javascript": (("WORD", "fg", ""), ("TEMPLATE LIT. (CLIENT)|TEMPLATE LIT. (SERVER)", "string", "")),
    "php": (("QUESTION MARK", "keyword", ""), ("VARIABLE|COMPLEX VARIABLE|STRING VARIABLE", "fg", ""),
            ("PREDEFINED", "call", "italic"), ("FUNCS AND METHODS 1|FUNCS AND METHODS 2", "call", "")),
    "asp": (("ASP SYMBOL|SCRIPT TYPE", "keyword", ""),),
    "css": (("TAG|CLASS|ID|PSEUDOCLASS|UNKNOWN PSEUDOCLASS|PSEUDOELEMENT|LEGACY PSEUDOELEMENT|MEDIA", "keyword", ""),
            ("IDENTIFIER|UNKNOWN IDENTIFIER|ATTRIBUTE", "field", ""), ("VALUE", "string", ""),
            ("IMPORTANT", "keyword", "bold"), ("DIRECTIVE", "keyword", KW)),
    "python": (("BUILTINS", "call", "italic"), ("ATTRIBUTE", "field", ""),
               ("TRIPLE|TRIPLE DOUBLE", "doc", "italic"),  # docstrings
               ("F TRIPLE|F TRIPLEDOUBLE", "string", "")),
    "gdscript": (("WORD2", "call", "italic"), ("TRIPLE|TRIPLE DOUBLE", "doc", "italic"), ("NODEPATH", "string", "")),
    "nim": (("TRIPLE QUOTES|TRIPLE DOUBLE QUOTES", "doc", "italic"), ("CLASS NAME DEFINITION", "type", ""),
            ("FUNCTION OR METHOD NAME DEFINITION", "method", "bold"), ("HIGHLIGHTED IDENTIFIERS", "call", "italic")),
    "sql": (("KEYWORD2", "keyword", KW), ("Q OPERATOR", "string", "")),  # data types; Oracle's q'...' strings
    "mssql": (("DATA TYPE", "keyword", KW), ("SYSTEM TABLE", "type", ""), ("SYSTEM STORED PROC", "call", ""),
              ("COL NAME|COL NAME IN []'s", "field", "")),
    "bash": (("PARAM", "field", "italic"), ("HERE DELIM", "keyword", "bold")),
    "yaml": (("IDENTIFIER", "keyword", KW),  # keys
             ("INSTRUCTION WORD|NUMBER|TEXT", "fg", ""),  # plain scalars read as text, as in the VS Code theme
             ("REFERENCE", "annotation", ""), ("DOCUMENT", "op", ""), ("COMMENT", "doc", "italic")),
    "toml": (("KEY|TABLE", "keyword", KW), ("KEYWORD", "typeParam", "italic"), ("IDENTIFIER", "fg", ""),
             ("DATETIME", "number", "")),
    "json": (("PROPERTY NAME", "field", ""), ("LD KEYWORD", "annotation", ""), ("URI|COMPACT IRI", "call", "italic")),
    "rust": (("KEYWORDS 1|KEYWORDS 2|KEYWORDS 3", "keyword", KW),  # keywords, primitive types, Self
             ("KEYWORDS 4", "type", ""), ("KEYWORDS 5", "call", ""), ("KEYWORDS 6", "field", ""),
             ("KEYWORDS 7", "constant", "bold italic"), ("LIFETIME", "typeParam", "italic")),
    "diff": (("COMMAND", "keyword", KW), ("HEADER|POSITION", "keyword", ""), ("DELETED", "ansiRed", ""),
             ("ADDED", "ansiGreen", "")),
    "ini": (("SECTION", "keyword", KW), ("ASSIGNMENT", "op", ""), ("DEFVAL", "constant", "bold italic"),
            ("KEY", "field", "")),
    "makefile": (("IDENTIFIER", "field", "italic"), ("TARGET", "method", "bold"), ("IDEOL", "ansiRed", "")),
    "batch": (("HIDE SYMBOL", "op", ""), ("AFTER LABEL", "fg", "")),
    "powershell": (("ALIAS", "call", "italic"),),
    "lua": (("FUNC1|FUNC2|FUNC3", "call", "italic"),),
    "perl": (("SYMBOL TABLE", "field", "italic"), ("PROTOTYPE", "type", ""), ("TRANSLATION|FORMAT BODY", "string", ""),
             ("HEREDOC DELIMITER", "keyword", "bold"), ("FORMAT IDENTIFIER", "keyword", ""),
             ("DATA SECTION", "comment", "italic")),
    "ruby": (("SYMBOL", "constant", "bold italic"), ("MODULE NAME", "type", ""), ("INSTANCE VAR", "field", ""),
             ("DATA SECTION", "comment", "italic")),
    "registry": (("VALUE NAME", "field", ""), ("VALUE TYPE", "type", ""), ("ADDED KEY", "ansiGreen", ""),
                 ("REMOVED KEY", "ansiRed", ""), ("GUID IN KEY PATH", "constant", "bold italic")),
    "latex": (("TAG OPENING|TAG CLOSING", "keyword", ""), ("MATH INLINE|MATH BLOCK", "string", "")),
    "tex": (("SPECIAL", "gold", ""), ("GROUP|SYMBOL", "op", "")),
    "txt2tags": (("SPECIAL|PRECHAR (NOT USED)|HRULE", "op", ""), ("STRONG|STRONG 2 (NOT USED)", "fg", "bold"),
                 ("EM1 (ITALIC)", "fg", "italic"), ("EM2 (UNDERLINE)", "fg", "underline"),
                 ("H1|H2|H3|H4|H5|H6", "method", "bold"),  # headings take the declaration role, as in Markdown
                 ("ULIST|OLIST", "keyword", KW), ("BLOCKQUOTE", "doc", "italic"), ("STRIKEOUT", "muted", ""),
                 ("LINK", "azure", "underline"), ("CODE|CODE2|CODEBLOCK", "string", ""),
                 ("OPTION|POSTPROC", "annotation", "")),
    # The other lexers that Notepad++ ships, by what each style colours there.
    "asm": (("CPU INSTRUCTION|MATH INSTRUCTION|EXT INSTRUCTION", "keyword", KW), ("REGISTER", "field", "")),
    "asn1": (("ATTRIBUTES", "annotation", ""), ("DESCRIPTORS", "keyword", KW)),
    "autoit": (("SENT", "gold", ""), ("SPECIAL", "constant", "bold italic"), ("EXPAND", "annotation", ""),
               ("COMOBJ", "type", "")),
    "avs": (("FILTER", "call", ""), ("PLUGIN", "call", "italic"), ("CLIP PROPERTIES", "field", "")),
    "baanc": (("MAIN SECTIONS", "keyword", KW), ("SUB SECTIONS|TABLE SQL", "keyword", ""),
              ("ENUM DOMAINS", "constant", "bold italic"),
              ("TABLE DEFINITIONS|DOMAIN DEFINITIONS|OBJECT DEFINITIONS", "type", "")),
    "caml": (("TAGNAME", "constant", "bold italic"), ("BUILIN FUNC & TYPE", "call", "italic"),
             ("LINENUM", "keyword", KW)),
    "cmake": (("WHILEDEF|FOREACHDEF|IFDEF|MACRODEF", "keyword", KW),),
    "cobol": (("DECLARATION", "keyword", KW),),
    "csound": (("INSTR", "keyword", KW),),
    "erlang": (("RECORD|RECORD QUOTED|MODULE NAME", "type", ""), ("ATOM|ATOM QUOTED", "constant", "bold italic"),
               ("NODE NAME|NODE NAME QUOTED", "string", ""), ("MODULE ATTRIBUTES", "annotation", "")),
    "forth": (("DEFWORDS", "keyword", KW), ("PREWORD1|PREWORD2", "keyword", ""),
              ("LOCALE", "constant", "bold italic")),
    "fortran": (("CONTINUATION", "op", ""),),
    "gui4cli": (("EVENT", "keyword", ""), ("ATTRIBUTE", "field", "")),
    "haskell": (("CLASS|DATA|IMPORT|INSTANCE", "keyword", KW), ("MODULE|CAPITAL", "type", "")),
    "hollywood": (("CORE API", "call", "italic"), ("PLUGIN API|PLUGIN METHOD", "call", "")),
    "lisp": (("SYMBOL", "constant", "bold italic"), ("SPECIAL", "keyword", "")),
    "mmixal": (("DIVSION OF LEADING WHITESPACE IN LINE|DIVISION BETWEEN LABEL AND OPCODE|"
                "DIVISION BETWEEN OPCODE AND OPERANDS|DIVISION OF OPERANDS", "fg", ""),
               ("OPCODE|VALID OPCODE", "keyword", KW), ("REGISTER", "field", ""),
               ("SYMBOL", "constant", "bold italic")),
    "nsis": (("SUBSECTION|SECTION GROUP|PAGE EX", "keyword", ""), ("IF DEFINE", "keyword", KW)),
    "nncrontab": (("TASK START/END", "keyword", KW), ("MODIFICATORS", "keyword", ""), ("ASTERISK", "op", "")),
    "oscript": (("#IFDEF DOC AND #ENDIF", "comment", "italic"), ("OBJECT PROPERTY", "field", ""),
                ("OBJECT METHOD", "call", ""), ("OPERATOR; EITHER SYMBOLIC OR LITERAL", "op", ""),
                ("CONSTANT LITERAL", "constant", "bold italic"), ("STATIC BUILT-IN OBJECT", "type", "")),
    "pascal": (("ASM", "fg", ""),),
    "postscript": (("DSC VALUE", "doc", "italic"), ("IMMEVAL|LITERAL", "constant", "bold italic"),
                   ("PAREN ARRAY|PAREN DICT|PAREN PROC", "op", ""), ("TEXT", "string", "")),
    "r": (("BASE WORD", "call", "italic"), ("INFIX", "op", ""), ("BACKTICKS", "fg", "")),
    "raku": (("ADVERB", "annotation", ""), ("MU|POSITIONAL|ASSOCIATIVE", "field", "italic"),
             ("CALLABLE", "call", ""), ("GRAMMAR", "type", "")),
    "rebol": (("PREFACE", "comment", "italic"),
              ("PAIR ( 800X600 )|TUPLE ( 127.0.0.1 )|BINARY ( 16#{1A803F59} )|MONEY|DATE { 17-FEB-2004 1/3/99 }|"
               "TIME { 12:30 11:22:59 01:59:59.123 }", "number", ""),
              ("ISSUE { #123-CD-456 }", "constant", "bold italic"), ("TAG { <TITLE HEIGHT=100> }", "keyword", ""),
              ("FILE { %/C/WINNT/SOME.DLL }|EMAIL { JOE@MAIL.DOM }", "string", ""),
              ("URL { FTP://THERE.DOM }", "call", "italic")),
    "scheme": (("SYMBOL", "constant", "bold italic"), ("SPECIAL", "keyword", "")),
    "smalltalk": (("SYMBOL", "constant", "bold italic"), ("BINARY|SPECIAL|ASSIGN", "op", ""),
                  ("BOOL|NIL|RETURN", "keyword", KW), ("SELF|SUPER", "keyword", "italic"),
                  ("KWS END", "call", ""), ("SPECIAL SELECTOR", "call", "italic")),
    "spice": (("VALUE", "number", ""),),
    "ihex": (("RECSTART", "keyword", ""), ("RECTYPE", "keyword", KW), ("BYTECOUNT|RECCOUNT", "number", ""),
             ("NOADDRESS|DATA_EMPTY", "muted", ""), ("DATAADDRESS|STARTADDRESS|EXTENDEDADDRESS", "field", ""),
             ("DATA_ODD", "fg", ""), ("DATA_EVEN", "op", ""), ("CHECKSUM", "constant", "bold italic")),
    "tcl": (("MODIFIER", "annotation", ""), ("EXPAND", "keyword", ""), ("SUB BRACE", "op", ""),
            ("SUBSTITUTION", "field", "italic"), ("WORD IN QUOTE|IN QUOTE", "string", "")),
    "vb": (("DATE", "number", ""),),
    "vhdl": (("STD OPERATOR", "keyword", KW), ("ATTRIBUTE", "annotation", ""), ("STD PACKAGE|STD TYPE", "type", "")),
    "visualprolog": (("MAJOR", "keyword", KW), ("MINOR", "keyword", ""), ("ANONYMOUS", "field", "italic")),
    "searchResult": (),  # set by search_result()
    "errorlist": (),  # set by error_list()
    "escseq": (),  # set by escape_sequences()
}
LEXERS["props"] = LEXERS["ini"]
LEXERS["fortran77"] = LEXERS["fortran"]
LEXERS["srec"] = LEXERS["tehex"] = LEXERS["ihex"]


def font(p, name):
    """The fontStyle bits for a font name, with "kw" as the palette's keyword font."""
    if name == KW:
        return BOLD if p.get("kwBold", not p["dark"]) else 0
    return FONTS[name]


def rule(lexer, style):
    """(role, font) for a style of notepadpp.json, or None when no rule covers it."""
    for names, role, font_name in LEXERS.get(lexer, ()):
        if style["name"] in names.split("|"):
            return role, font_name
    for pattern, role, font_name in NAMES:
        if pattern.search(style["name"]):
            if role == "user":
                digits = re.findall(r"\d", style["name"])
                return USER[int(digits[-1]) if digits else 1]
            return role, font_name
    return None


def search_result(p, style):
    """The Search results panel: the search on the hover colour, each file in the declaration role, the hits on the
    search background."""
    return {"Search Header": (p["fg"], p["hover"], BOLD), "File Header": (p["method"], p["bg"], BOLD),
            "Line Number": (p["muted"], p["bg"], 0), "Hit Word": (p["fg"], p["searchBg"], BOLD),
            "Current line background colour": (None, p["caretRow"], 0)}[style["name"]]


def error_list(p, style):
    """Compiler and tool output: errors in red, diff lines in the diff colours, ANSI colours as a terminal's."""
    name = style["name"]
    if name.startswith("ANSI COLOR "):
        return p[ERROR_LIST_ANSI[name]], p["bg"], 0
    role = {"DEFAULT STYLE": "fg", "DIFF Changed": "ansiBlue", "DIFF Addition": "ansiGreen",
            "DIFF Deletion": "ansiRed", "DIFF Message": "keyword", "Escape Sequence": "muted",
            "GCC Included-From Error": "muted", "GCC Excerpt Error": "fg"}.get(name, "ansiRed")
    return p[role], p["bg"], 0


def escape_sequences(p, style):
    """ANSI art: each foreground on each background in terminal colours; DEFAULT is the editor's text or
    background."""
    name = style["name"]
    if name == "Sequence Identifier":
        return p["muted"], p["bg"], 0
    if name == "Sequence Unknown":
        return p["ansiRed"], p["bg"], 0
    bold = name.startswith("BOLD ")
    foreground, background = name.removeprefix("BOLD ").split(" on ")
    def colour(word, default, bright):
        return p[default] if word == "DEFAULT" else p[(BRIGHT if bright else TERMINAL)[word]]
    return colour(foreground, "fg", bold), colour(background, "bg", False), BOLD if bold else 0


# Lexers whose styles carry colours of their own, as (fg, bg, fontStyle) from a function of the palette and the style.
OWN = {"searchResult": search_result, "errorlist": error_list, "escseq": escape_sequences}


def decorative(lexer, style):
    """Whether the style named style of the lexer named lexer shows text in the colours a program asked for with ANSI
    escape sequences, as a terminal does, so that the contrast check leaves it out."""
    return lexer == "escseq" or (lexer == "errorlist" and style in ERROR_LIST_ANSI)


def lexer_styles(p):
    """(lexer, style, fg, bg, fontStyle, colorStyle) for every style of every lexer in notepadpp.json; fg is None for
    a style that sets only a background. Raises ValueError for a style that no rule covers."""
    out, missing = [], []
    for lexer in MODEL["lexers"]:
        for style in lexer["styles"]:
            if lexer["name"] in OWN:
                fg, bg, bits = OWN[lexer["name"]](p, style)
                out.append((lexer, style, fg, bg, bits, None))
                continue
            found = rule(lexer["name"], style)
            if found is None:
                missing.append(f"{lexer['name']}: {style['name']}")
                continue
            role, font_name = found
            out.append((lexer, style, p[role], p["bg"], font(p, font_name), COLORSTYLE_FOREGROUND))
    if missing:
        raise ValueError("no rule for the Notepad++ styles " + "; ".join(missing))
    return out


def tab_colour(p, key, dark):
    """An individual tab colour: the ANSI colour washed into a light or a dark base, for Light Mode or Dark Mode."""
    base = p["bg"] if p["dark"] == dark else p["fg"]
    return mix(base, p[key], 0.45 if dark else 0.3)


def widgets(p):
    """WidgetStyle name to its attributes. Indicators are drawn at 40 % opacity under the text, so they take the
    accent colours rather than the palette's washes."""
    caret = p.get("caret", p["gold"])
    text = dict(fontName="", fontStyle=0, fontSize="")
    tabs = ("ansiYellow", "ansiGreen", "ansiBlue", "ansiRed", "ansiMagenta")
    return {
        "Default Style": dict(fgColor=p["fg"], bgColor=p["bg"], fontName=FONT_NAME, fontStyle=0, fontSize=FONT_SIZE),
        "Indent guideline style": dict(fgColor=p["guide"], bgColor=p["bg"], **text),
        "Brace highlight style": dict(fgColor=p["fg"], bgColor=p["braceBg"], **dict(text, fontStyle=BOLD)),
        "Bad brace colour": dict(fgColor=p["ansiRed"], bgColor=p["bg"], **dict(text, fontStyle=BOLD)),
        "Current line background colour": dict(bgColor=p["caretRow"]),
        "Selected text colour": dict(bgColor=p["selection"], fgColor=p["fg"]),
        "Multi-selected text color": dict(bgColor=p["selection"]),
        "Caret colour": dict(fgColor=caret),
        "Multi-edit carets color": dict(fgColor=p["ansiBlue"]),
        "Edge colour": dict(fgColor=p["guideSel"]),
        "Line number margin": dict(fgColor=p["lineNo"], bgColor=p["bg"], **text),
        "Bookmark margin": dict(bgColor=p["bg"]),
        "Change History margin": dict(bgColor=p["bg"]),
        "Change History modified": dict(fgColor=p["modified"], bgColor=p["modified"]),
        "Change History revert modified": dict(fgColor=p["ansiYellow"], bgColor=p["ansiYellow"]),
        "Change History revert origin": dict(fgColor=p["ansiCyan"], bgColor=p["ansiCyan"]),
        "Change History saved": dict(fgColor=p["added"], bgColor=p["added"]),
        # Notepad++ draws the fold lines in fgColor and fills the boxes with bgColor.
        "Fold": dict(fgColor=p["lineNo"], bgColor=p["bg"]),
        "Fold active": dict(fgColor=p["lineNoCaret"]),
        "Fold margin": dict(fgColor=p["bg"], bgColor=p["bg"]),
        "White space symbol": dict(fgColor=p["lineNo"]),
        "Smart Highlighting": dict(bgColor=p["azure"]),
        "Find Mark Style": dict(bgColor=p["searchBorder"]),
        "Find status: Not found": dict(fgColor=p["ansiRed"]),
        "Find status: Message": dict(fgColor=p["ansiBlue"]),
        "Find status: Search end reached": dict(fgColor=p["ansiGreen"]),
        "Mark Style 1": dict(bgColor=p["ansiCyan"]),
        "Mark Style 2": dict(bgColor=p["warning"]),
        "Mark Style 3": dict(bgColor=p["ansiYellow"]),
        "Mark Style 4": dict(bgColor=p["ansiMagenta"]),
        "Mark Style 5": dict(bgColor=p["ansiGreen"]),
        "Incremental highlight all": dict(bgColor=p["ansiBlue"]),
        "Tags match highlighting": dict(bgColor=p["ansiMagenta"]),
        "Tags attribute": dict(bgColor=p["ansiYellow"]),
        "Active tab focused indicator": dict(fgColor=caret),
        "Active tab unfocused indicator": dict(fgColor=p["guideSel"]),
        "Active tab text": dict(fgColor=p["fg"]),
        "Inactive tabs": dict(fgColor=p["muted"], bgColor=p["bgTool"]),
        **{f"Tab color {i}": dict(bgColor=tab_colour(p, key, False)) for i, key in enumerate(tabs, 1)},
        **{f"Tab color dark mode {i}": dict(bgColor=tab_colour(p, key, True)) for i, key in enumerate(tabs, 1)},
        "URL hovered": dict(fgColor=p["azure"]),
        # The document map covers the minimap with bgColor and marks the visible part with fgColor.
        "Document map": dict(fgColor=p["gold"], bgColor=p["bg"]),
        "EOL custom color": dict(fgColor=p["lineNo"]),
        "Non-printing characters custom color": dict(fgColor=p["lineNo"]),
        "Global override": dict(fgColor=p["fg"], bgColor=p["bg"], **text),
    }


def element(tag, attributes, empty=True):
    """An XML start tag, or an empty element, with the attributes in their order."""
    values = " ".join(f'{key}="{escape(str(value), QUOTE)}"' for key, value in attributes.items())
    return f"<{tag} {values}{' /' if empty else ''}>"


def theme(p, source):
    """The theme file for a palette. source is the URL of the theme folder."""
    lines = ['<?xml version="1.0" encoding="UTF-8" ?>',
             f"<!--\n{escape(p['name'])}: a Heritage Themes theme for Notepad++.\n"
             f"Generated from {source}; changes here are overwritten.\n-->",
             f'<NotepadPlus modelDate="{MODEL["modelDate"]}">', "    <LexerStyles>"]
    current = None
    for lexer, style, fg, bg, bits, colour_style in lexer_styles(p):
        if lexer is not current:
            if current is not None:
                lines.append("        </LexerType>")
            lines.append("        " + element("LexerType", {k: lexer[k] for k in ("name", "desc", "ext")}, empty=False))
            current = lexer
        attributes = {"name": style["name"], "styleID": style["id"]}
        if fg:
            attributes.update(fgColor=fg, bgColor=bg, fontName="", fontStyle=bits, fontSize="")
        else:
            attributes.update(bgColor=bg)
        if colour_style is not None:
            attributes["colorStyle"] = colour_style
        if "keywordClass" in style:
            attributes["keywordClass"] = style["keywordClass"]
        lines.append("            " + element("WordsStyle", attributes))
    lines += ["        </LexerType>", "    </LexerStyles>", "    <GlobalStyles>"]
    values = widgets(p)
    for widget in MODEL["widgets"]:
        settings = values[widget["name"]]
        if set(settings) != set(widget["attributes"]):
            raise ValueError(f"Notepad++ {widget['name']} sets {sorted(settings)}, the model {widget['attributes']}")
        lines.append("        " + element("WidgetStyle", {"name": widget["name"], "styleID": widget["id"],
                                                          **{k: settings[k] for k in widget["attributes"]}}))
    lines += ["    </GlobalStyles>", "</NotepadPlus>"]
    return "\n".join(lines) + "\n"
