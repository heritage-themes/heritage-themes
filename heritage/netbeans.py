"""NetBeans module generated from a palette: one look and feel and one editor colour profile for each Heritage theme.

NetBeans draws its windows with FlatLaf, which reads IntelliJ UI theme JSON itself, so a theme's look and feel is a
FlatLaf IntelliJTheme.ThemeLaf over the UI theme that heritage.ui writes for the JetBrains plugin. NetBeans keeps the
chosen look and feel by its class name, so each theme has a class of its own. NetBeans' FlatLaf module adds the
colours of its own components (editor and view tabs, the Options dialog, the property sheet) to every FlatLaf look and
feel, derived from the colours of the UI theme.

The editor reads its colours from a Fonts & Colors profile: a folder of XML files in the module's layer, one with the
base token categories, one with the editor's highlights (selection, current line, search, line numbers) and one with
the annotations (breakpoints, debugger lines, hints), and a file of token colourings for each language. NetBeans keeps
a profile's language colouring only when its default profile defines one of that name, and resolves the colouring a
colouring inherits from within the same file, so each language file names every colouring of the default profile, with
its inheritance, as heritage/netbeans.json records them. A colouring that the default profile colours, or whose role
differs from the one it inherits, takes a role from overrides(). scripts/netbeans/colorings.py writes the record from an
installation.

NetBeans applies a profile's annotation colours when the profile is chosen in Options, either under Fonts & Colors or
by the look and feel's restart notification.

A look and feel names its profile in the UI default nb.preferred.color.profile: when the user picks a look and feel
under Tools | Options | Appearance, NetBeans offers to switch to that profile after the restart.
"""
import json, os, re
import xml.etree.ElementTree as ET
from xml.sax.saxutils import quoteattr

from .sublime import basename
from .terminals import contrast
from .vscode import mix

# The colourings of NetBeans' default profile, which scripts/netbeans/colorings.py reads from an installation.
with open(os.path.join(os.path.dirname(__file__), "netbeans.json"), encoding="utf-8") as f:
    REFERENCE = json.load(f)
PACKAGE = "io.github.heritagethemes.netbeans"  # the module's code name base and the package of its classes
FOLDER = PACKAGE.replace(".", "/")  # the folder of the classes and resources in the module's jar
PREFIX = "Heritage "  # a theme's name in NetBeans' lists, so that the themes sit together among NetBeans' own
PROFILE_PREFIX = "Heritage"  # a profile's folder name is this followed by the theme's slug
HEX = re.compile(r"ff[0-9a-f]{6}")  # a colour as the profile files write it: ARGB, opaque
FONTS = {"plain", "bold", "italic", "bold+italic"}
# The attributes of a colouring, as (key in a colouring dict, XML attribute) in the order the files write them.
ATTRIBUTES = (("fore", "foreColor"), ("back", "bgColor"), ("under", "underline"), ("wave", "waveUnderlined"),
              ("strike", "strikeThrough"))
DOCTYPE = ('<!DOCTYPE fontscolors PUBLIC "-//NetBeans//DTD Editor Fonts and Colors settings 1.1//EN" '
           '"http://www.netbeans.org/dtds/EditorFontsColors-1_1.dtd">')
# The kinds of base files, as (file name in the layer, nbeditor-settings-ColoringType).
BASE_FILES = (("tokens", "token"), ("highlights", "highlight"), ("annotations", "annotation"))


def name(t):
    """The name of a theme dict from a theme.py in NetBeans' lists of look and feels and profiles, for example
    "Heritage Edo Cha (Dark)"."""
    return PREFIX + basename(t["palette"]["name"])


def profile(t):
    """The folder name of the theme's Fonts & Colors profile, for example "HeritageEdoCha"."""
    return PROFILE_PREFIX + t["slug"]


def look_and_feel(t):
    """The simple name of the theme's look and feel class, for example "EdoChaLookAndFeel"."""
    return t["slug"] + "LookAndFeel"


def c(fore=None, back=None, *, under=None, wave=None, strike=None, font=None, default=None):
    """A colouring: each colour a palette role, or a computed colour as #RRGGBB; font one of FONTS; default the name of
    the colouring that it inherits what it does not set from."""
    return {k: v for k, v in dict(fore=fore, back=back, under=under, wave=wave, strike=strike, font=font,
                                  default=default).items() if v is not None}


def neutral(p):
    """The background of a disabled breakpoint's line: the editor's background moved a little towards its text."""
    return "#" + mix(p["bg"], p["fg"], 0.08)


def brace(p):
    """The background of matched braces and of the debugger's current expression: the palette's braceBg, moved towards
    the editor's background in steps of 1% until plain text keeps 4.5:1 on it. Most palettes need no step."""
    for i in range(101):
        colour = mix(p["braceBg"], p["bg"], i / 100)
        if contrast(p["fg"], colour) >= 4.5:
            return "#" + colour
    return "#" + p["bg"]


def keyword_font(p):
    """Keywords are bold in light themes, as in the JetBrains schemes, unless the palette sets kwBold."""
    return "bold" if p.get("kwBold", not p["dark"]) else "plain"


def tokens(p):
    """The base token categories, as (name, colouring). Every language's colourings inherit from these."""
    return [
        ("default", c("fg", "bg")),
        ("identifier", c("fg")),
        ("keyword", c("keyword", font=keyword_font(p))),
        ("operator", c("op")),
        ("separator", c("op")),
        ("string", c("string")),
        ("char", c("string")),
        ("number", c("number")),
        ("comment", c("comment", font="italic")),
        ("field", c("field", default="identifier")),
        ("method", c("call", default="identifier")),
        ("markup-element", c("keyword", default="keyword")),
        ("markup-attribute", c("field", default="field")),
        ("markup-attribute-value", c("string", default="string")),
        ("entity-reference", c("gold", default="default")),
        ("url", c("azure", under="azure")),
        ("whitespace", c("guideSel")),
        ("error", c(wave="error")),
        ("warning", c(wave="warning")),
        ("mark-occurrences", c(back="underCaret")),
    ]


def highlights(p):
    """The editor's highlights, as (name, colouring): selection, current line, search, gutter and the like."""
    caret = "#" + p.get("caret", p["gold"])
    return [
        ("selection", c(back="selection")),
        ("highlight-caret-row", c(back="caretRow")),
        ("highlight-search", c(back="searchBg")),
        ("inc-search", c(back="searchBg", under="searchBorder")),
        ("block-search", c(back="selInactive")),
        ("caret-color-insert-mode", c(caret)),
        ("caret-color-overwrite-mode", c(caret)),
        ("line-number", c("lineNo", "bg")),
        ("indent-guide-lines", c("guide")),
        ("text-limit-line-color", c("guide")),
        ("guarded", c(back="fileYellow")),
        ("readonly-files", c(back="fileYellow")),
        ("hyperlinks", c("azure", under="azure")),
        ("synchronized-text-blocks-ext", c("azure")),
        ("synchronized-text-blocks-ext-slave", c("muted")),
        ("status-bar-bold", c("error")),
        ("code-folding", c("muted", "surface")),
        ("code-folding-bar", c("lineNo")),
        ("code-folding-border", c("lineNo")),
        ("nbeditor-bracesMatching-match", c(back=brace(p))),
        ("nbeditor-bracesMatching-match-multichar", c(back=brace(p))),
        ("nbeditor-bracesMatching-mismatch", c(back="writeCaret", wave="error")),
        ("nbeditor-bracesMatching-mismatch-multichar", c(back="writeCaret", wave="error")),
        ("nbeditor-bracesMatching-sidebar", c("azure")),
        ("coverage-covered", c(back="diffIns")),
        ("coverage-uncovered", c(back="diffDel")),
        ("coverage-inferred", c(back="#" + mix(p["bg"], p["diffIns"], 0.5))),
        ("coverage-partial", c(back="diffConf")),
        ("remove-surround-code-delete", c("muted", "diffDel")),
        ("remove-surround-code-remain", c(back="diffIns")),
    ]


# The annotations that colour a line, grouped by what the line is. Each group takes one background.
BREAKPOINT_LINES = ("Breakpoint CondBreakpoint OtherThread_BP OtherThreads_BP CurrentPC2_BP debugger-mixed_BP "
                    "debugger-multi_BPCBP Dbx_Bpt Dbx_Bpt_broken Dbx_Bpt_cmpx Dbx_Bpt_cmpx_broken Dbx_Bpt_compound")
DISABLED_LINES = ("Breakpoint_broken Breakpoint_stroke CondBreakpoint_broken CondBreakpoint_stroke DisabledBreakpoint "
                  "DisabledBreakpoint_stroke DisabledCondBreakpoint DisabledCondBreakpoint_stroke OtherThread_DBP "
                  "OtherThreads_DBP CurrentPC2_DBP debugger-mixed_BP_broken debugger-multi_BPCBP_broken "
                  "debugger-multi_DBPCBP Dbx_Bpt_dis Dbx_Bpt_broken_dis Dbx_Bpt_cmpx_dis Dbx_Bpt_cmpx_broken_dis "
                  "Dbx_Bpt_cmpx_hit_dis Dbx_Bpt_cmpx_hit_broken_dis Dbx_Bpt_hit_dis Dbx_Bpt_hit_broken_dis "
                  "loadgenProfilingPointD resetResultsProfilingPointD stopwatchProfilingPointD "
                  "takeSnapshotProfilingPointD")
EXECUTION_LINES = ("CurrentPC CurrentPC2 CurrentPCLinePart CurrentPC2LinePart OtherThread_PC OtherThread_PC_BP "
                   "OtherThreads_PC_BP OtherThread_BP_broken OtherThreads_BP_broken debugger-PC_BP "
                   "debugger-PC_BP_broken debugger-PC_BP_stroke debugger-PC_CBP debugger-PC_CBP_broken "
                   "debugger-PC_CBP_stroke debugger-PC_DBP debugger-PC_DBP_stroke debugger-PC_DCBP "
                   "debugger-PC_DCBP_stroke debugger-PC_mixedBP debugger-PC_mixedBP_broken debugger-PC_multi_BPCBP "
                   "debugger-PC_multi_BPCBP_broken debugger-PC_multi_DBPCBP CurrentExpressionLine "
                   "CurrentExpressionLine_BP CurrentExpressionLine_CBP CurrentExpressionLine_DBP "
                   "CurrentExpressionLine_DCBP Dbx_PC Dbx_Bpt_hit Dbx_Bpt_hit_broken Dbx_Bpt_cmpx_hit "
                   "Dbx_Bpt_cmpx_hit_broken Dbx_Bpt_compound_hit")
PROFILING_LINES = ("loadgenProfilingPoint resetResultsProfilingPoint stopwatchProfilingPoint "
                   "takeSnapshotProfilingPoint")
ERROR_UNDERLINES = ("PHPError org-netbeans-modules-cnd-cpp-parser_annotation_err "
                    "org-netbeans-modules-web-core-syntax-JspParserErrorAnnotation")
WARNING_UNDERLINES = "PHPNotice PHPWarning"
ERROR_LINES = "org-netbeans-modules-tomcat5-error org-netbeans-modules-xml-error"
TODO_TEXT = ("org-netbeans-spi-editor-hints-parser_annotation_todo "
             "org-netbeans-spi-editor-hints-parser_annotation_todo_fixable")


def annotations(p):
    """The annotations, as (name, colouring). An annotation's background colours the line or the text it marks, its
    wave the text, and its foreground the text."""
    groups = ((BREAKPOINT_LINES, c(back="diffDel")), (DISABLED_LINES, c(back=neutral(p))),
              (EXECUTION_LINES, c(back="diffMod")), (PROFILING_LINES, c(back="diffIns")),
              ("CurrentExpression", c(back=brace(p))), ("CallSite", c(back="selInactive")),
              (ERROR_UNDERLINES, c(wave="error")), (WARNING_UNDERLINES, c(wave="warning")),
              (ERROR_LINES, c(back="diffDel")), (TODO_TEXT, c("todo")))
    return [(n, colouring) for names, colouring in groups for n in names.split()]


def languages(p):
    """The token colourings of each language, as {MIME path: [(name, colouring)]}: every colouring that NetBeans'
    default profile defines for the language, in its order and with the colouring it inherits from, and with the
    colours that overrides gives it. NetBeans drops a colouring that its default profile does not define, and resolves
    a colouring's default within the same file, so a file that names fewer colourings loses the ones that inherit."""
    roles = overrides(p)
    out = {}
    for mime, entries in REFERENCE["languages"].items():
        own = roles.get(mime, {})
        out[mime] = [(n, {**({"default": default} if default else {}), **own.get(n, {})}) for n, default, _ in entries]
    return out


def overrides(p):
    """The colourings of each language that take a role, as {MIME path: {name: colouring}}: those that NetBeans colours
    itself, which would otherwise keep their colours from a light profile, and those whose role differs from the one
    they inherit."""
    kw = keyword_font(p)
    # The semantic colourings that Java, Groovy and the TextMate languages share with the JetBrains schemes: method
    # declarations bold, calls plain, statics and interfaces italic, unused code faint and deprecated code struck out.
    deprecated = c(strike="muted")
    unused = c("disabled")
    no_background = c()  # embedded code keeps the editor's background
    java = [
        ("mod-field", c("field")),
        ("mod-field-declaration", c("field")),
        ("mod-record-component", c("field")),
        ("mod-record-component-declaration", c("field")),
        ("mod-local-variable", c("fg")),
        ("mod-local-variable-declaration", c("fg")),
        ("mod-parameter", c("param")),
        ("mod-parameter-declaration", c("param")),
        ("mod-method", c("call")),
        ("mod-method-declaration", c("method", font="bold")),
        ("mod-constructor", c("call")),
        ("mod-constructor-declaration", c("method", font="bold")),
        ("mod-class", c("type")),
        ("mod-class-declaration", c("type", font="plain")),
        ("mod-record", c("type")),
        ("mod-record-declaration", c("type", font="plain")),
        ("mod-enum", c("type")),
        ("mod-enum-declaration", c("type", font="plain")),
        ("mod-interface", c("type", font="italic")),
        ("mod-interface-declaration", c("type", font="italic")),
        ("mod-module", c("type")),
        ("mod-module-declaration", c("type", font="plain")),
        ("mod-annotation-type", c("annotation")),
        ("mod-annotation-type-declaration", c("annotation", font="plain")),
        ("mod-static", c(font="italic")),
        ("mod-deprecated", deprecated),
        ("mod-unused", unused),
        ("string-escape", c("gold", font="bold")),
        ("string-escape-invalid", c("ansiRed", wave="error")),
        ("character-escape", c("gold", font="bold")),
        ("character-escape-invalid", c("ansiRed", wave="error")),
        ("javadoc-first-sentence", c("doc", font="italic")),
        ("javadoc-tag", c("docTag", font="bold+italic")),
        ("javadoc-identifier", c("docTag", font="italic")),
        ("html-tag", c("docTag", font="italic")),
    ]
    javascript = [
        ("mod-regexp", c("gold")),
        ("mod-method", c("method")),
        ("mod-class", c("type")),
        ("mod-field", c("field")),
        ("mod-global", c("field", font="italic")),
        ("mod-local-variable", c("fg")),
        ("mod-local-variable-declaration", c("fg")),
        ("mod-custom1", c("number")),
        ("mod-unused", unused),
        ("COMMENT_KEYWORD", c("docTag", font="bold+italic")),
        ("COMMENT_HTML", c("docTag", font="italic")),
    ]
    jsp = [
        ("attribute-name", c("field")),
        ("attribute-value", c("string")),
        ("comment", c("comment", font="italic")),
        ("error", c("ansiRed")),
        ("symbol", c("op")),
        ("tag-directive", c("keyword", font=kw)),
        ("endtag", c("keyword", font=kw)),
        ("jsp-whitespace", c("fg")),
        ("scriptlet", no_background),
        ("scriptlet-delimiter", c("annotation")),
        ("expression-language", no_background),
    ]
    xml = [
        ("xml-cdata-section", c("string")),
        ("xml-doctype", c("directive")),
        ("xml-pi-start", c("directive")),
        ("xml-pi-end", c("directive")),
        ("xml-pi-target", c("directive")),
        ("xml-pi-content", c("directive")),
        ("xml-value", c("string")),
    ]
    hcl = [("heredoc", c("string")), ("heredoc-guard", c("string", font="bold"))]
    textmate = [
        ("entity.name.function", c("method", font="bold")),
        ("support.function", c("call")),
        ("constant.other", c("constant", font="bold+italic")),
        ("constant.character.escape", c("gold", font="bold")),
        ("support.constant", c("constant", font="bold+italic")),
        ("variable.language", c("keyword", font="italic")),
        ("markup.heading", c("keyword", font="bold")),
        ("markup.bold", c(font="bold")),
        ("markup.italic", c(font="italic")),
        ("markup.underline", c(under="fg")),
        ("mod-namespace", c("type")),
        ("mod-namespace-declaration", c("type")),
        ("mod-package", c("type")),
        ("mod-package-declaration", c("type")),
        ("mod-function", c("call")),
        ("mod-function-declaration", c("method", font="bold")),
        ("mod-method", c("call")),
        ("mod-method-declaration", c("method", font="bold")),
        ("mod-macro", c("annotation")),
        ("mod-macro-declaration", c("annotation", font="bold")),
        ("mod-parameter", c("param")),
        ("mod-parameter-declaration", c("param")),
        ("mod-variable", c("fg")),
        ("mod-variable-declaration", c("fg")),
        ("mod-struct", c("type")),
        ("mod-struct-declaration", c("type")),
        ("mod-enum", c("type")),
        ("mod-enum-declaration", c("type")),
        ("mod-class", c("type")),
        ("mod-class-declaration", c("type")),
        ("mod-typeAlias", c("type")),
        ("mod-typeAlias-declaration", c("type")),
        ("mod-typeParameter", c("typeParam", font="bold")),
        ("mod-typeParameter-declaration", c("typeParam", font="bold")),
        ("mod-field", c("field")),
        ("mod-field-declaration", c("field")),
        ("mod-enumMember", c("constant", font="bold+italic")),
        ("mod-enumMember-declaration", c("constant", font="bold+italic")),
        ("mod-static", c(font="italic")),
        ("mod-deprecated", deprecated),
    ]
    table = {
        "text/x-java": java,
        "text/x-groovy": [
            ("mod-method", c("call")),
            ("mod-constructor", c("call")),
            ("mod-class", c("type")),
            ("mod-field", c("field")),
            ("mod-static", c(font="italic")),
            ("mod-unused", unused),
            ("mod-deprecated", deprecated),
        ],
        "text/textmate": textmate,
        "text/javascript": javascript,
        "text/x-json": javascript,
        "text/x-php5": [
            ("variable", c("fg")),
            ("constant", c("constant", font="bold+italic")),
            ("heredocdelimiter", c("string", font="bold")),
            ("number", c("number")),
            ("htmltag", c("docTag", font="italic")),
            ("phpdockeyword", c("docTag", font="bold+italic")),
            ("mod-field", c("field")),
            ("mod-method", c("method", font="bold")),
            ("mod-custom1", c("call")),
            ("mod-class", c("type")),
            ("mod-custom2", c("param", font="italic")),
            ("mod-annotation-type", c("docTag", font="bold+italic")),
            ("mod-static", c(font="italic")),
            ("mod-unused", unused),
            ("mod-deprecated", deprecated),
        ],
        "text/html": [
            ("sgml-declaration", c("directive")),
            ("css-embedded", no_background),
            ("javascript-embedded", no_background),
            ("el-delimiter", c("annotation")),
            ("el-content", c("fg")),
            ("mod-method", c("type")),
            ("mod-class", c("type", wave="error")),
            ("mod-constructor", c("annotation")),
        ],
        "text/xhtml": [("expression-language", c("fg"))],
        "text/x-jsp": jsp,
        "text/x-tag": jsp,
        "text/css": [
            ("at_rule_symbol", c("keyword", font=kw)),
            ("mod-method", c("type")),
            ("mod-custom1", c("field")),
            ("mod-custom2", c("field", font="italic")),
            ("mod-custom3", c("constant")),
            ("mod-constructor", c("typeParam")),
            ("mod-class", c("annotation")),
            ("mod-local-variable", c("param")),
            ("mod-private", c("call")),
        ],
        "text/xml": xml,
        "text/xml-external-parsed-entity": xml,
        "application/xml-dtd": [("dtd-target", c("directive"))],
        "text/x-markdown": [
            ("header", c("method", font="bold")),
            *((f"header{i}", c("method", font="bold")) for i in range(1, 7)),
            ("bulletlist", c("op")),
            ("orderedlist", c("op")),
            ("link", c("call", font="italic")),
            ("image", c("call", font="italic")),
            ("code", c("string")),
            ("verbatim", c("string")),
            ("blockquote", c("doc", font="italic")),
            ("emph", c(font="italic")),
            ("strong", c(font="bold")),
            ("strikethrough", c(strike="muted")),
        ],
        "text/x-markdown-nb-preview": [
            ("anchor", c("azure")),
            ("code", c(back="surface")),
            ("pre", c(back="surface")),
        ],
        "text/x-properties": [
            ("properties-key", c("field")),
            ("properties-value", c("string")),
            ("properties-equal-sign", c("op")),
        ],
        "text/x-yaml": [
            ("mod-method", c("keyword", font=kw)),
            ("mustache", no_background),
            ("mustache-delimiter", c("annotation")),
            ("ruby", no_background),
            ("ruby-delimiter", c("annotation")),
            ("RUBYCOMMENT", no_background),
        ],
        "text/x-ini": [
            ("comment", c("comment", font="italic")),
            ("section_delim", c("op")),
            ("section", c("type", font="bold")),
            ("key", c("field")),
            ("equals", c("op")),
            ("value", c("string")),
        ],
        "text/x-toml": [
            ("key", c("keyword", font=kw)),
            ("table-mark", c("keyword", font=kw)),
            ("string-escape", c("gold", font="bold")),
        ],
        "text/x-env": [
            ("key", c("field")),
            ("value", c("string")),
            ("dollar", c("gold")),
        ],
        "text/x-sql": [("sql-identifier", c("fg"))],
        "text/x-diff": [
            ("header", c("muted")),
            ("index", c("muted")),
            ("filename", c("keyword", font="bold")),
            ("added", c("ansiGreen")),
            ("removed", c("ansiRed")),
        ],
        "text/x-apache-conf": [
            ("variable", c("field")),
            ("string", c("string")),
            ("number", c("number")),
            ("flag", c("constant")),
            ("tag", c("type")),
            ("tagparam", c("field")),
            ("directive", c("keyword", font=kw)),
            ("directiveparam", c("fg")),
        ],
        "text/x-el": [("tag-lib-prefix", c("type"))],
        "text/x-gsp": [
            ("attribute-name", c("field")),
            ("attribute-value", c("string")),
            ("directive", c("directive")),
            ("gtag", c("keyword", font=kw)),
        ],
        "text/jade": [
            ("sgml-declaration", c("directive")),
            ("javascript-embedded", no_background),
            ("css-embedded", no_background),
            ("plain-text", no_background),
            ("css-id", c("field")),
            ("css-class", c("type")),
            ("file-path", c("string")),
            ("filter", c("annotation")),
            ("block-name", c("method", font="bold")),
            ("mixin-name", c("method", font="bold")),
        ],
        "text/ko-data-bind": [("key", c("field"))],
        "text/x-latte": [
            ("latte-delimiter", c("annotation")),
            ("latte-markup-macro", c("keyword", font=kw)),
            ("latte-markup-number", c("number")),
            ("latte-markup-variable", c("field")),
            ("latte-markup-char", c("op")),
        ],
        "text/x-twig": [
            ("twig_block_delimiter", c("annotation")),
            ("twig_var_delimiter", c("annotation")),
            ("twig_interpolation", c("annotation")),
            ("twig_operator", c("op")),
            ("twig_string", c("string")),
            ("twig_tag", c("keyword", font=kw)),
            ("twig_punctuation", c("op")),
        ],
        "text/x-tpl": [
            ("smarty", no_background),
            ("smarty_delimiter", c("annotation")),
            ("comment", c("comment", font="italic")),
            ("pipe", c("op")),
            ("php_variable", c("field")),
            ("config_variable", c("constant")),
            ("variable_modifier", c("call")),
            ("string", c("string")),
            ("smarty_operator", c("op")),
            ("smarty_function", c("call")),
            ("argument", c("param")),
            ("argument_value", c("string")),
            ("error", c(wave="error")),
        ],
        "text/x-vue": [
            ("vue_directive", c("annotation")),
            ("attr_quote", c("string")),
            ("var_tag", c("annotation")),
        ],
        "text/x-neon": [
            ("valuedblock", c("keyword", font=kw)),
            ("block", c("type")),
            ("variable", c("field")),
            ("string", c("string")),
            ("interpunction", c("op")),
            ("number", c("number")),
            ("reference", c("constant")),
        ],
        "text/x-antlr3": antlr(),
        "text/x-antlr4": antlr(),
        "text/x-jflex": [
            ("option", c("keyword", font=kw)),
            ("options_separator", c("op")),
            ("macro", c("constant")),
            ("mod-custom1", no_background),
            ("regex", c("gold")),
            ("quantifier", c("number")),
            ("error", c("ansiRed")),
        ],
        "text/x-javahints": [("pattern", c(back="underCaret"))],
        "text/x-oql": [("js-block", c("fg"))],
        "text/x-repl": [
            ("output", c("fg")),
            ("delimiter", c("muted")),
            ("message", c("muted", font="italic")),
            ("java", c("fg")),
        ],
        "text/x-terraform+x-hcl": hcl,
        "text/x-tfvars+x-hcl": hcl,
    }
    return {mime: dict(entries) for mime, entries in table.items()}


def antlr():
    """The colourings of the ANTLR 3 and 4 grammar editors."""
    return [("regexp-chars", c("gold")), ("rule", c("method", font="bold")), ("token", c("constant"))]


def colour(p, value):
    """A role or #RRGGBB as the profile files write it: opaque ARGB in lower case, for example "ff86aac4"."""
    return "ff" + (value[1:] if value.startswith("#") else p[value]).lower()


def fontscolors(p, colourings):
    """The XML of a Fonts & Colors file with the given (name, colouring) pairs."""
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', DOCTYPE, "<fontscolors>"]
    for n, colouring in colourings:
        attributes = [f"name={quoteattr(n)}"]
        attributes += [f'{attribute}="{colour(p, colouring[key])}"' for key, attribute in ATTRIBUTES
                       if key in colouring]
        if "default" in colouring:
            attributes.append(f"default={quoteattr(colouring['default'])}")
        if "font" in colouring:
            lines.append(f"    <fontcolor {' '.join(attributes)}>")
            lines.append(f'        <font style="{colouring["font"]}"/>')
            lines.append("    </fontcolor>")
        else:
            lines.append(f"    <fontcolor {' '.join(attributes)}/>")
    lines.append("</fontscolors>")
    return "\n".join(lines) + "\n"


def files(p):
    """The profile's files, as {path in the theme's folder: XML}: the three base files and one for each language,
    named after its MIME path."""
    out = {f"{kind}.xml": fontscolors(p, colourings)
           for (kind, _), colourings in zip(BASE_FILES, (tokens(p), highlights(p), annotations(p)))}
    for mime, colourings in languages(p).items():
        out[f"{mime.replace('/', '-')}.xml"] = fontscolors(p, colourings)
    return out


def layer(themes):
    """The module's layer.xml: every theme's profile, its base files and its language files. themes are theme dicts
    from the theme.py files, and the profile's files are resources at fontscolors/<slug>/ beside the layer."""
    root = ET.Element("filesystem")

    def folder(parent, path):
        """The folder at path under parent, created once: a layer that names a folder twice is an error."""
        for n in path:
            child = next((f for f in parent.findall("folder") if f.get("name") == n), None)
            parent = child if child is not None else ET.SubElement(parent, "folder", name=n)
        return parent

    def attr(parent, n, value):
        ET.SubElement(parent, "attr", name=n, stringvalue=value)

    for t in themes:
        base = folder(root, ["Editors", "FontsColors", profile(t)])
        attr(base, "SystemFileSystem.localizingBundle", f"{PACKAGE}.Bundle")
        for kind, coloring_type in BASE_FILES:
            file = ET.SubElement(folder(base, ["Defaults"]), "file", name=f"heritage-{kind}.xml",
                                 url=f"fontscolors/{t['slug']}/{kind}.xml")
            attr(file, "nbeditor-settings-ColoringType", coloring_type)
    for mime in languages(themes[0]["palette"]):
        for t in themes:
            ET.SubElement(folder(root, ["Editors", *mime.split("/"), "FontsColors", profile(t), "Defaults"]), "file",
                          name="heritage-token-colorings.xml",
                          url=f"fontscolors/{t['slug']}/{mime.replace('/', '-')}.xml")
    ET.indent(root, space="    ")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<!DOCTYPE filesystem PUBLIC "-//NetBeans//DTD Filesystem 1.2//EN" '
            '"http://www.netbeans.org/dtds/filesystem-1_2.dtd">\n' + ET.tostring(root, encoding="unicode") + "\n")


def bundle(themes, display_name, short_description, long_description, category):
    """The module's Bundle.properties: its name, category and descriptions, and the display name of each profile."""
    def escape(text):
        return text.encode("ascii", "backslashreplace").decode().replace("\\x", "\\u00")
    lines = [f"OpenIDE-Module-Name={escape(display_name)}",
             f"OpenIDE-Module-Display-Category={escape(category)}",
             f"OpenIDE-Module-Short-Description={escape(short_description)}",
             f"OpenIDE-Module-Long-Description={escape(long_description)}"]
    lines += [f"Editors/FontsColors/{profile(t)}={escape(name(t))}" for t in themes]
    return "\n".join(lines) + "\n"


def java_look_and_feel(t):
    """The Java source of the theme's look and feel class."""
    return f"""package {PACKAGE};

/** The look and feel of {name(t)}. */
public final class {look_and_feel(t)} extends HeritageLookAndFeel {{

    public {look_and_feel(t)}() {{
        super("{t['slug']}", "{name(t)}");
    }}
}}
"""


def java_themes(themes):
    """The Java source of the class that lists every theme's look and feel for the module's installer."""
    entries = ",\n".join(f'            new UIManager.LookAndFeelInfo("{name(t)}", {look_and_feel(t)}.class.getName())'
                         for t in themes)
    return f"""package {PACKAGE};

import java.util.List;
import javax.swing.UIManager;

/** The look and feel of every Heritage theme, in the order NetBeans lists them. */
final class Themes {{

    static final List<UIManager.LookAndFeelInfo> ALL = List.of(
{entries});

    private Themes() {{
    }}
}}
"""


def styles(p, colourings):
    """(name: {"fg": #RRGGBB, "bg": #RRGGBB}) of colourings that set a foreground, with the background they are drawn
    on where they set one, for the build's contrast check."""
    out = {}
    for n, colouring in colourings:
        style = {}
        if "fore" in colouring:
            style["fg"] = "#" + colour(p, colouring["fore"])[2:].upper()
        if "back" in colouring:
            style["bg"] = "#" + colour(p, colouring["back"])[2:].upper()
        out[n] = style
    return out


def backgrounds(p):
    """The backgrounds that code is drawn on, as (label, #RRGGBB): the editor, its current line, and the lines and
    ranges that highlights and annotations colour behind the text."""
    out = [("bg", "#" + p["bg"]), ("caretRow", "#" + p["caretRow"])]
    for label, colourings in (("token", tokens(p)), ("highlight", highlights(p)), ("annotation", annotations(p))):
        for n, colouring in colourings:
            if "back" in colouring and "fore" not in colouring and n not in DECORATIVE_BACKGROUNDS:
                out.append((f"{label} {n}", "#" + colour(p, colouring["back"])[2:].upper()))
    return out


# Backgrounds that no code is drawn on: the gutter's line numbers carry their own colour.
DECORATIVE_BACKGROUNDS = {"line-number"}
# Foregrounds that are drawn as lines or carets rather than as text, or that are faint on purpose: line numbers other
# than the current line's, which the palette holds to its contrast, and unused code.
DECORATIVE = {"line-number", "caret-color-insert-mode", "caret-color-overwrite-mode", "indent-guide-lines", "text-limit-line-color",
              "code-folding-bar", "code-folding-border", "nbeditor-bracesMatching-sidebar", "whitespace",
              "synchronized-text-blocks-ext", "synchronized-text-blocks-ext-slave", "mod-unused", "status-bar-bold"}
