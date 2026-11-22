"""Kate colour themes and window colour schemes generated from a palette.

Kate draws its editor with KTextEditor, which colours code with KSyntaxHighlighting. A definition gives each of its
items one of the default styles (TEXT_STYLES), which a colour theme colours, and may give an item colours of its own,
which a theme replaces only in its custom-styles, by definition and item name. The theme (a .theme file, JSON) sets
each default style and editor colour of KSyntaxHighlighting (kate.json, written by scripts/kate/definitions.py) to the
role that the other targets give the construct, and in custom-styles:

- language_rules(): items whose default style gives a construct a role other than the one the other targets give it,
  as heritage.vim does for Vim's syntax groups: Python's exceptions take Preprocessor, JSON's keys DataType;
- every item that sets colours of its own, in the role of its default style, so that no colour of a definition
  shows. A background that an item sets can be replaced but not removed, so alerts, such as TODO in a comment, take
  diffConf, an attention wash, and other items the current line's colour, on which every code role is readable.

A rule for a definition also applies to the variants that the library generates from it, such as Jinja/ISO C++.

The window colour scheme (a .colors file, KDE's colour scheme format) colours Kate's window: panels on bgTool, lists
and the editor on bg, buttons and tooltips on surface, the menu bar and tool bars (KDE's Header) on frame, as the
Islands layout of the other targets. The Breeze style fills the open menu-bar item with the focus decoration and draws
the selection's text on it, and outlines focused fields in it, so the window's accent is ansiBlue: the selection of
lists and menus, with the editor's background as its text, and the focus and hover decoration. The editor keeps the
theme's own selection. The scheme's View background is the theme's background, which no other theme has, so that with
Kate's default, Follow System Color Scheme, choosing the window colour scheme chooses the theme of the same name
(KSyntaxHighlighting::Repository::themeForPalette).
"""
import json, os, re

from .nvim import name  # noqa: F401 - the files take the names of Neovim's schemes
from .terminals import colours as terminal_colours
from .vscode import mix

with open(os.path.join(os.path.dirname(__file__), "kate.json"), encoding="utf-8") as f:
    DATA = json.load(f)
TEXT_STYLES = tuple(DATA["text_styles"])
EDITOR_COLOURS = tuple(DATA["editor_colours"])
DEFINITIONS = DATA["definitions"]
HARD_CODED = DATA["hard_coded"]
# The prefixes and suffixes of the definitions that the library generates from another: Jinja/ISO C++ from ISO C++,
# JavaScript/PHP from JavaScript.
VARIANTS = (("Jinja/", ""), ("", "/PHP"), ("", "/Twig"))
FONTS = {"": {}, "bold": {"bold": True}, "italic": {"italic": True}, "bold italic": {"bold": True, "italic": True},
         "underline": {"underline": True}, "strike": {"strike": True}}
# The colour groups of a KDE colour scheme and the roles that each sets.
COLOUR_SETS = ("Window", "View", "Button", "Selection", "Tooltip", "Complementary", "Header", "Header][Inactive")
COLOUR_ROLES = ("BackgroundNormal", "BackgroundAlternate", "ForegroundNormal", "ForegroundInactive",
                "ForegroundActive", "ForegroundLink", "ForegroundVisited", "ForegroundNegative", "ForegroundNeutral",
                "ForegroundPositive", "DecorationFocus", "DecorationHover")
# The background of an item whose own background the theme replaces: diffConf for alerts, the current line's colour
# for the others.
ALERT_BACKGROUND, ITEM_BACKGROUND = "diffConf", "caretRow"
# The window's accent: Breeze's focus and hover decoration and the selection of lists and menus.
ACCENT = "ansiBlue"
# How far Breeze blends the accent into a menu's background behind the item under the pointer (Metrics::Blend_Value).
MENU_HOVER = 0.3
# How opaque KTextEditor fills the minimap's visible range with the accent (KateScrollBar::miniMapPaintEvent).
MINIMAP_SLIDER = 50 / 255
# The roles held to 3:1 rather than 4.5:1: comments, and alerts, which comments hold.
LOW_CONTRAST_ROLES = ("comment", "todo")


def text_styles(p):
    """Default style → (role, font): the roles of heritage.nvim's syntax groups."""
    kw = "bold" if p.get("kwBold", not p["dark"]) else ""
    return {
        "Normal": ("fg", ""), "Keyword": ("keyword", kw), "ControlFlow": ("keyword", kw), "Import": ("keyword", kw),
        # the primitive types of C, C++, C#, Java, Go and Rust, which the other targets give the keyword role
        "DataType": ("keyword", kw),
        # names followed by an argument list, which most definitions take for calls; declarations in language_rules
        "Function": ("call", ""), "BuiltIn": ("call", "italic"),
        # shell, PHP and Perl variables and C++ members by their prefixes, as the other targets give shell variables
        "Variable": ("field", "italic"),
        "Operator": ("op", ""), "Extension": ("type", ""),
        "Preprocessor": ("directive", ""), "Attribute": ("annotation", ""),
        "Char": ("string", ""), "String": ("string", ""), "VerbatimString": ("string", ""),
        "SpecialString": ("string", ""), "SpecialChar": ("gold", "bold"),
        "DecVal": ("number", ""), "BaseN": ("number", ""), "Float": ("number", ""),
        "Constant": ("constant", "bold italic"),
        "Comment": ("comment", "italic"), "Documentation": ("doc", "italic"), "Annotation": ("docTag", "bold italic"),
        "CommentVar": ("docTag", "italic"), "RegionMarker": ("docTag", "italic"),
        "Information": ("ansiBlue", ""), "Warning": ("ansiYellow", ""), "Alert": ("todo", "bold"),
        "Error": ("ansiRed", "underline"),
        # attribute names of markup languages and instance variables, which most definitions give this style
        "Others": ("field", ""),
    }


def language_rules(p):
    """(definition, item names, role, font, background palette key or None) for the items whose default style gives a
    construct another role than the one the other targets give it, following heritage.vscode where a definition
    marks the same construct as a TextMate scope."""
    kw = "bold" if p.get("kwBold", not p["dark"]) else ""
    rules = []
    def s(definition, items, role, font="", background=None):
        rules.append((definition, tuple(items.split("|")), role, font, background))
    # alerts in comments, such as TODO and FIXME: the two levels that set a background of their own and the third
    s("Alerts", "Alert Level 1|Alert Level 2|Alert Level 3", "todo", "bold", ALERT_BACKGROUND)
    # doc comments, which Javadoc and Doxygen mark with the Comment style
    s("Javadoc", "Javadoc|JavadocFS", "doc", "italic")
    s("Doxygen", "Comment|Code|Verbatim|Dot Graph|Formulas|Message Sequence Chart", "doc", "italic")
    s("Doxygen", "Entities", "gold")
    # declarations, which the definitions mark apart from calls
    for js in ("JavaScript", "TypeScript"):
        s(js, "Function Declaration", "method", "bold")
        s(js, "Object Member|Object Property (Built-in)", "field")
        s(js, "Function (Built-in)", "call", "italic")
        s(js, "Built-in Objects", "type")
    for shell in ("Bash", "Zsh"):
        s(shell, "Function", "method", "bold")
        s(shell, "OtherCommand", "call")
    s("JavaScript", "Special Operators", "op")  # =>
    s("Bash", "Escape|String Escape", "gold", "bold")
    s("Bash", "Base", "number")
    s("Bash", "Glob", "op")
    s("Bash", "Option|Expression", "fg")
    s("Rust", "Definition", "method", "bold")
    # members and properties, which take Attribute or DataType in the definitions of Ruby and PHP
    s("Ruby", "Member", "field")
    s("Ruby", "Message|Kernel methods|Module mixin methods", "call")
    s("PHP/PHP", "Properties", "field")
    s("ISO C++", "Data Members (m_*)", "field")
    s("ISO C++", "Globals (g_*)|Statics (s_*)", "field", "italic")
    # local names where they are declared, which Kotlin, Swift and Lua mark as Variable
    for language in ("Kotlin", "Swift", "Lua"):
        s(language, "Variable", "fg")
    # self, this and other names that the language gives a meaning, as keywords in italics
    s("Python", "Special Variable", "keyword", "italic")
    s("Rust", "Self", "keyword", "italic")
    s("PHP/PHP", "Special Variable", "keyword", "italic")
    s("Lua", "Special Variable|Self Variable|BVar", "keyword", "italic")
    s("Ruby", "Pseudo variable", "keyword", "italic")
    s("Zig", "Self Variable", "keyword", "italic")
    s("Go", "Predeclared Identifier", "keyword", kw)
    # types: Go's built-in types and class names, which take DataType in Go, Kotlin, Swift, Ruby and Haskell, and the
    # classes of standard libraries and exceptions, which take BuiltIn or Preprocessor
    s("Go", "Data Type", "type")
    s("Kotlin", "Data Type", "type")
    s("Swift", "Data Type", "type")
    s("Ruby", "Constant", "type")
    s("Haskell", "Type Prelude|Data Prelude|Class Prelude|Type", "type")
    s("ISO C++", "Types (*_t/*_type)|Standard Classes", "type")
    s("Python", "Exceptions", "type")
    s("PHP/PHP", "Classes", "type")
    s("Rust", "Trait", "type")
    # macros and C++'s type modifiers
    s("Rust", "Macro", "annotation")
    s("ISO C++", "Standard Macros", "annotation")
    s("ISO C++", "Type Modifiers", "keyword", kw)
    s("ISO C++", "Internals", "muted")
    s("Rust", "Lifetime", "typeParam", "italic")
    s("Rust", "Scope|Raw Identifier", "fg")
    s("TypeScript", "Parameter", "param")
    # the header that #include names, and the suffixes of literals
    s("C", "Prep. Lib", "string")
    s("ISO C++", "Prep. Lib", "string")
    s("C", "Standard Suffix", "number")
    s("ISO C++", "Standard Suffix|UDL Numeric Suffix|UDL String Suffix", "number")
    s("Go", "Suffix", "number")
    s("Python", "Complex", "number")
    s("R Script", "Numeric Suffix", "number")
    s("Ruby", "Number Suffix", "number")
    s("Ruby", "Symbol", "constant", "bold italic")
    s("Ruby", "Here Document|Command", "string")
    s("Ruby", "Access Control|Attribute Definition", "keyword", kw)
    s("Ruby", "Delimiter", "op")
    s("PHP/PHP", "Symbol|Scope Resolution|Error Control Operator", "op")
    s("PHP/PHP", "Other", "fg")
    s("SQL", "Identifier", "fg")
    s("SQL", "Symbol|External Variable", "op")
    s("SQL", "Preprocessor", "directive")
    # escapes and interpolations
    for language in ("Kotlin", "Swift", "Groovy", "Scala"):
        s(language, "String Interpolation", "gold", "bold")
    for language in ("Go", "SQL", "Python"):
        s(language, "String Char", "gold", "bold")
    s("JavaScript", "Pattern Character Class", "number", "bold")
    # markup: tags and their punctuation as keywords, attributes as fields, entities as escapes
    for markup in ("HTML", "XML", "Vue"):
        s(markup, "Element|Element Symbols|Attribute Separator", "keyword")
        s(markup, "EntityRef", "gold")
    for markup in ("HTML", "XML"):
        s(markup, "Doctype", "keyword")
        s(markup, "CDATA", "string")
    s("XML", "Doctype Name|Doctype Symbols|Processing Instruction|PI Symbols", "keyword")
    s("XML", "CDATA Symbols", "string")
    s("XML", "PEntityRef", "gold")
    for jsx in ("JavaScript React (JSX)", "TypeScript React (TSX)"):
        s(jsx, "Element Tag|Component Tag", "keyword")
        s(jsx, "Code Brackets", "op")
        s(jsx, "Special Operators", "op")  # =>
        s(jsx, "EntityRef", "gold")
    # CSS: properties as fields, selectors and functions as tags, property values as strings, colours as numbers
    for css in ("CSS", "SCSS"):
        s(css, "Property|Vendor Property|Condition Property|Attribute Name", "field")
        s(css, "Property Separator", "fg")
        s(css, "Block Symbol", "op")
        s(css, "Selector Tag|Selector Class|Selector Id|Selector Attribute|Selector Pseudo|Function|"
               "Condition Open/Close", "keyword")
        s(css, "Value|Value Keyword|Unit", "string")
        s(css, "Named Color|Color", "number")
        s(css, "Media Type", "keyword", kw)
        s(css, "Annotation", "keyword", "bold")  # !important
    s("SCSS", "Placeholder Selector", "keyword")
    s("SCSS", "Interpolation", "gold", "bold")
    # data: keys as fields in JSON and keywords in YAML, TOML and INI files, punctuation as operators
    for data in ("JSON", "JSONC"):
        s(data, "Style_String_Key", "field")
        s(data, "Style_Seperator_Pair|Style_Seperator_Array", "op")
        s(data, "Style_String_Key_Char|Style_String_Value_Char", "gold", "bold")
    s("YAML", "Key", "keyword", kw)
    s("YAML", "Normal Text|Attribute|List|Hash|Literal/Folded Block|Null|Boolean|Integer|Float|Timestamp", "fg")
    s("YAML", "Key Points Operator|Operator|Literal/Folded Operator|Document Header|End of Document", "op")
    s("YAML", "Comment", "doc", "italic")
    s("YAML", "Data Types|Tag", "type")
    s("YAML", "Alias|Reference", "annotation")
    s("YAML", "Alert", "todo", "bold", ALERT_BACKGROUND)
    s("TOML", "Key|TableHeader", "keyword", kw)
    s("TOML", "Boolean true|Boolean false", "typeParam", "italic")
    s("TOML", "Array|InlineTable|NextEntry", "op")
    s("INI Files", "Normal Text|Section", "keyword", kw)
    s("INI Files", "Assignment", "op")
    s("Makefile", "Variable|Prereq|SpecialPrereq", "field", "italic")
    s("Makefile", "Target|SpecialTarget|Section", "method", "bold")
    s("Makefile", "Operator|TargetSeparator|RealOperator", "op")
    s("Makefile", "Special", "gold", "bold")
    s("Dockerfile", "Directive", "directive")
    s("Dockerfile", "Option", "fg")
    # Markdown: headings as declarations, emphasis in the text colour, code as strings, link text in azure and
    # addresses as calls
    s("Markdown", "Header H1|Header H2|Header H3|Header H4|Header H5|Header H6", "method", "bold")
    s("Markdown", "Emphasis Text|List: Emphasis Text", "fg", "italic")
    s("Markdown", "Strong Text|List: Strong Text", "fg", "bold")
    s("Markdown", "Strong-Emphasis Text|List: Strong-Emphasis Text", "fg", "bold italic")
    s("Markdown", "Strikethrough Text|List: Strikethrough Text", "fg", "strike")
    s("Markdown", "Highlight Text|Blockquote: Highlight Text|List: Highlight Text", "fg", "", "searchBg")
    s("Markdown", "Blockquote|Blockquote: Normal Text|Blockquote: Emphasis Text|Blockquote: Strong Text|"
                  "Blockquote: Strong-Emphasis Text|Blockquote: Strikethrough Text|Blockquote: Link", "doc", "italic")
    s("Markdown", "List|Number List|List: Checkbox", "keyword", kw)
    s("Markdown", "Code|Fenced Code", "string")
    s("Markdown", "Table|Horizontal Rule", "op")
    s("Markdown", "Line Break", "muted", "underline")
    s("Markdown", "Reference-Link|Reference-Link Name|Reference-Link ID|Footnote|Inline Image|Reference Image",
      "azure", "underline")
    s("Markdown", "Auto-Link|Link|Mailto-Link|Email|Reference-Link Target|Reference-Link Target: Link|"
                  "Reference-Link: Link|Reference-Link: Email|Inline Image: Link", "call", "italic")
    s("Markdown", "Metadata Title", "type", "bold")
    s("Markdown", "Metadata", "comment", "italic")
    s("Markdown", "EntityRef", "gold")
    # diffs in the console colours, as the other targets draw them
    s("Diff", "Removed line|Changed line (old)", "ansiRed")
    s("Diff", "Added line|Changed line (new)", "ansiGreen")
    s("Diff", "File", "ansiBlue", "bold")
    s("Diff", "Header", "ansiCyan")
    # CMake's items with colours of their own, whose default style gives them another role than the construct's
    s("CMake", "True Special Arg|False Special Arg|Generator Expression Keyword", "keyword", kw)
    s("CMake", "Builtin Variable", "keyword", "italic")
    s("CMake", "Generator Expression Sub-Command", "call")
    s("CMake", "Generator Expression", "annotation")
    return rules


def variants(definition):
    """The definitions of the library that are definition or a variant that it generates from it."""
    names = [f"{prefix}{definition}{suffix}" for prefix, suffix in VARIANTS]
    return [definition] + [n for n in names if n != definition and n in DEFINITIONS]


def custom_styles(p):
    """Definition → item → (role, font, background palette key or None): language_rules(), then every item that sets
    colours of its own in the role of its default style, each in the definition and its generated variants."""
    defaults = text_styles(p)
    out = {}
    for definition, items, role, font, background in language_rules(p):
        for name_ in variants(definition):
            for item in items:
                if item not in DEFINITIONS[name_]:
                    raise ValueError(f"{name_} has no item {item!r}")
                if item in out.get(name_, {}):
                    raise ValueError(f"{name_} {item} is set twice")
                out.setdefault(name_, {})[item] = (role, font, background)
    for definition, items in HARD_CODED.items():
        for item, colours in items.items():
            style = DEFINITIONS[definition][item]
            role, font, background = out.get(definition, {}).get(item) or (*defaults[style], None)
            if "backgroundColor" in colours and not background:
                background = ALERT_BACKGROUND if style == "Alert" else ITEM_BACKGROUND
            out.setdefault(definition, {})[item] = (role, font, background)
    return {definition: dict(sorted(items.items())) for definition, items in sorted(out.items())}


def hexes(p):
    """Palette key or ANSI colour name (ansiBlack to ansiWhite) → #rrggbb."""
    out = {k: "#" + v.lower() for k, v in p.items() if isinstance(v, str) and re.fullmatch(r"[0-9A-F]{6}", v)}
    out.update({f"ansi{n.title()}": colour.lower() for n, colour in zip(
        ("black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"), terminal_colours(p)["ansi"])})
    return out


def style_json(p, role, font, background=None):
    """A text style of the theme: colours and every font flag, so that no flag of a definition's item shows."""
    c = hexes(p)
    flags = FONTS[font]
    out = {"text-color": c[role], "selected-text-color": c[role]}
    if background:
        out["background-color"] = c[background]
        out["selected-background-color"] = c["selection"]
    out.update({"bold": bool(flags.get("bold")), "italic": bool(flags.get("italic")),
                "underline": bool(flags.get("underline")), "strike-through": bool(flags.get("strike"))})
    return out


def editor_colours(p):
    """Editor colour → palette key or ANSI colour name. Kate blends a mark's colour into the line's background by a
    tenth, so marks take the accents."""
    out = {
        "BackgroundColor": "bg", "TextSelection": "selection", "CurrentLine": "caretRow",
        "SearchHighlight": "searchBg", "ReplaceHighlight": "diffIns", "BracketMatching": "braceBg",
        "TabMarker": "guide", "SpellChecking": "error", "IndentationLine": "guide", "IconBorder": "bg",
        "CodeFolding": "selInactive", "LineNumbers": "lineNo", "CurrentLineNumber": "lineNoCaret",
        "WordWrapMarker": "guide", "ModifiedLines": "modified", "SavedLines": "added", "Separator": "border",
        "MarkBookmark": "ansiBlue", "MarkBreakpointActive": "ansiRed", "MarkBreakpointReached": "ansiYellow",
        "MarkBreakpointDisabled": "muted", "MarkExecution": "ansiGreen", "MarkWarning": "warning",
        "MarkError": "error",
        # code templates and snippets: the area on bgUi, editable fields in the diff washes
        "TemplateBackground": "bgUi", "TemplatePlaceholder": "diffIns", "TemplateFocusedPlaceholder": "diffMod",
        "TemplateReadOnlyPlaceholder": "diffDel",
    }
    if set(out) != set(EDITOR_COLOURS):
        raise ValueError(f"editor colours that differ from KSyntaxHighlighting's: "
                         f"{sorted(set(out) ^ set(EDITOR_COLOURS))}")
    return {key: out[key] for key in EDITOR_COLOURS}


def revision(version):
    """The theme revision for a release version: KSyntaxHighlighting keeps the theme of the highest revision when two
    files have the same name, so a later release wins over an earlier copy. 1.15.0 → 11500."""
    major, minor, patch = (int(part) for part in version.split("."))
    return major * 10000 + minor * 100 + patch


def theme(t, source, version="0.0.1"):
    """The themes/<theme>.theme file for a theme dict. source is the URL of the theme folder and version the release
    that the theme's revision comes from."""
    p = t["palette"]
    c = hexes(p)
    styles = text_styles(p)
    if set(styles) != set(TEXT_STYLES):
        raise ValueError(f"text styles that differ from KSyntaxHighlighting's: "
                         f"{sorted(set(styles) ^ set(TEXT_STYLES))}")
    data = {
        "metadata": {
            "name": p["name"], "revision": revision(version),
            "copyright": [f"{p['name']}: a Heritage Themes theme for Kate. Generated from {source}; changes here are "
                          "overwritten."],
            "license": "SPDX-License-Identifier: MIT",
        },
        "text-styles": {style: style_json(p, *styles[style]) for style in TEXT_STYLES},
        "editor-colors": {key: c[role] for key, role in editor_colours(p).items()},
        "custom-styles": {definition: {item: style_json(p, *value) for item, value in items.items()}
                          for definition, items in custom_styles(p).items()},
    }
    return json.dumps(data, indent=4, ensure_ascii=False) + "\n"


def disabled_amount(p):
    """How far KDE's Disabled effect fades text towards the panel's background (ContrastEffect 1), so that the
    window's text fades to the palette's disabled colour: the projection of disabled onto the line from fg to bgTool,
    in 0-1, rounded to two places."""
    fg, bg, disabled = ([int(p[k][i:i + 2], 16) for i in (0, 2, 4)] for k in ("fg", "bgTool", "disabled"))
    d = [b - f for f, b in zip(fg, bg)]
    length = sum(x * x for x in d)
    t = sum((x - f) * y for x, f, y in zip(disabled, fg, d)) / length if length else 0
    return round(min(1.0, max(0.0, t)), 2)


def colour_sets(p):
    """Colour group → colour role → palette key or ANSI colour name. Each group draws its text in the colours that the
    palette keeps readable on both of its backgrounds: the console colours on the editor's and panels' backgrounds,
    the plain and muted text on every surface, the blue of matches on popups, and the editor's background on the
    accent."""
    def group(background, alternate, inactive="muted", link="ansiBlue", visited="ansiMagenta", negative="ansiRed",
              neutral="ansiYellow", positive="ansiGreen", active="ansiBlue"):
        return {"BackgroundNormal": background, "BackgroundAlternate": alternate, "ForegroundNormal": "fg",
                "ForegroundInactive": inactive, "ForegroundActive": active, "ForegroundLink": link,
                "ForegroundVisited": visited, "ForegroundNegative": negative, "ForegroundNeutral": neutral,
                "ForegroundPositive": positive, "DecorationFocus": ACCENT, "DecorationHover": ACCENT}
    plain = dict(negative="fg", neutral="fg", positive="fg")
    on_surface = dict(visited="ansiBlue", **plain)
    on_frame = dict(link="fg", visited="fg", active="fg", **plain)
    return {
        # panels, with the editor's background for alternate rows; lists and the editor, with the current line's
        "Window": group("bgTool", "bg"), "View": group("bg", "caretRow", link="azure"),
        "Button": group("surface", "surface", **on_surface), "Tooltip": group("surface", "surface", **on_surface),
        "Selection": group(ACCENT, ACCENT, inactive="bg", link="bg", visited="bg", negative="bg", neutral="bg",
                           positive="bg", active="bg") | {"ForegroundNormal": "bg"},
        # the menu bar and tool bars on the frame
        "Header": group("frame", "bgTool", **on_frame), "Header][Inactive": group("frame", "bgTool", **on_frame),
        "Complementary": group("frame", "bgTool", **on_frame),
    }


def rgb(colour):
    """#rrggbb → r,g,b, as KDE's colour schemes write colours."""
    return ",".join(str(int(colour[i:i + 2], 16)) for i in (1, 3, 5))


def colour_scheme(t, source):
    """The color-schemes/<theme>.colors file for a theme dict."""
    p = t["palette"]
    c = hexes(p)
    lines = [f"# {p['name']}: a Heritage Themes window colour scheme for Kate.",
             f"# Generated from {source}; changes here are overwritten.", "",
             # disabled text fades towards its background to the disabled colour; inactive windows keep their colours
             "[ColorEffects:Disabled]", "ColorEffect=0", "ContrastEffect=1", f"ContrastAmount={disabled_amount(p)}",
             "IntensityEffect=0", "",
             "[ColorEffects:Inactive]", "ChangeSelectionColor=false", "Enable=false", ""]
    for group, roles in colour_sets(p).items():
        lines.append(f"[Colors:{group}]")
        lines += [f"{role}={rgb(c[roles[role]])}" for role in COLOUR_ROLES]
        lines.append("")
    lines += ["[General]", f"ColorScheme={name(t)}", f"Name={p['name']}", "", "[KDE]", "contrast=4", "",
              "[WM]", f"activeBackground={rgb(c['frame'])}", f"activeBlend={rgb(c['fg'])}",
              f"activeForeground={rgb(c['fg'])}", f"inactiveBackground={rgb(c['frame'])}",
              f"inactiveBlend={rgb(c['muted'])}", f"inactiveForeground={rgb(c['muted'])}"]
    return "\n".join(lines) + "\n"


def styles(p):
    """Element → dict(fg, bg) as #rrggbb, for the build's contrast check: each default style and custom style on the
    background it is drawn on, bg unless it sets one, and each foreground of the window colour scheme on its group's
    backgrounds."""
    c = hexes(p)
    out = {}
    for style, (role, font) in text_styles(p).items():
        out[style] = dict(fg=c[role], bg=c["bg"])
    for definition, items in custom_styles(p).items():
        for item, (role, font, background) in items.items():
            out[f"{definition} {item}"] = dict(fg=c[role], bg=c[background or "bg"])
    for group, roles in colour_sets(p).items():
        for role in COLOUR_ROLES:
            if role.startswith("Foreground"):
                for background in ("BackgroundNormal", "BackgroundAlternate"):
                    out[f"{group} {role} on {background}"] = dict(fg=c[roles[role]], bg=c[roles[background]])
    for element, fg, bg in (("replaced text", "fg", "ReplaceHighlight"), ("found text", "fg", "SearchHighlight"),
                            ("matching bracket", "fg", "BracketMatching"), ("selected text", "fg", "TextSelection"),
                            ("template field", "fg", "TemplatePlaceholder"),
                            ("focused template field", "fg", "TemplateFocusedPlaceholder"),
                            ("read-only template field", "fg", "TemplateReadOnlyPlaceholder"),
                            ("template", "fg", "TemplateBackground"),
                            ("current line number", "lineNoCaret", "IconBorder")):
        out[element] = dict(fg=c[fg], bg=c[editor_colours(p)[bg]])
    for group in ("Window", "Button"):
        background = colour_sets(p)[group]["BackgroundNormal"]
        out[f"menu item under the pointer on {group}"] = dict(
            fg=c["fg"], bg="#" + mix(p[background], c[ACCENT][1:].upper(), MENU_HOVER))
    return out


def low_contrast(p):
    """The elements of styles() held to 3:1: the default and custom styles in the roles of LOW_CONTRAST_ROLES, and
    the one character that the bracket match draws its background behind, as in heritage.rstudio, and the menu item
    under the pointer, which Breeze tints with the accent while the pointer rests on it."""
    out = {"matching bracket", "menu item under the pointer on Window", "menu item under the pointer on Button"}
    out |= {style for style, (role, font) in text_styles(p).items() if role in LOW_CONTRAST_ROLES}
    for definition, items in custom_styles(p).items():
        out |= {f"{definition} {item}" for item, (role, *_) in items.items() if role in LOW_CONTRAST_ROLES}
    return out


def pixel_palette(p):
    """What scripts/editors/pixels.py checks a screenshot against: the editor and its minimap, cropped from the
    window that scripts/editors/shoot.py opens at 1100x700, with the menu bar, tool bar, tabs, side bar and status bar
    left out, where Kate draws Breeze's icons in colours of their own."""
    colours = {colour.upper() for colour in hexes(p).values()}
    backgrounds = ["#" + p[k] for k in ("bgTool", "bgUi", "frame", "surface", "caretRow", "selection", "selInactive",
                                        "hover", "border", "diffConf", "searchBg", "braceBg")]

    def under_slider(colour):
        """colour under the minimap's visible range, which KTextEditor fills with the accent."""
        return "#" + mix(colour[1:], p[ACCENT], MINIMAP_SLIDER)

    return dict(background="#" + p["bg"],
                backgrounds=backgrounds + [under_slider("#" + p[k]) for k in ("bg", "caretRow")],
                foregrounds=sorted(colours | {under_slider(colour) for colour in colours}), crop=[122, 34, 46, 0],
                # KTextEditor draws the text cursor by inverting the background: the current line's, or the bracket
                # match's on a bracket
                allowed=["#" + "".join(f"{255 - int(p[key][i:i + 2], 16):02X}" for i in (0, 2, 4))
                         for key in ("bg", "caretRow", "braceBg")])
