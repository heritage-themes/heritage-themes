"""GNOME Text Editor style schemes generated from a palette.

GNOME Text Editor colours code with GtkSourceView 5, whose language definitions give each of their styles a style it
maps to (map-to), as a chain that ends in a default style of def.lang (gnome_text_editor.json, written by
scripts/gnome-text-editor/definitions.py). A style scheme (an XML file) colours a style by its id: the language's own,
else the first style along the chain that the scheme sets. The scheme sets:

- every default style of def.lang to the role that the other targets give the construct, as heritage.kate does for
  KSyntaxHighlighting's default styles;
- language_rules(): the styles of a language whose chain gives a construct a role other than the one the other targets
  give it, as heritage.vscode does for TextMate scopes: Java's modifiers map to def:type, CSS's property names to
  def:keyword and JSON's keys to def:constant;
- the editor's own styles (EDITOR_STYLES): the text, the selection, the current line, line numbers, search matches,
  matching brackets, the right margin and whitespace.

Every style sets each font flag, so that no flag of an enclosing style shows through.

GNOME Text Editor colours its window from the scheme too (editor-recoloring.c): the metadata set the header bar on
frame, the window and the side bar on bgTool and popovers on surface, as the Islands layout of the other targets, and
the accent, which fills switches and suggested buttons and draws focus rings and links, on ansiBlue with the editor's
background as its text. The editor derives the list views' and dialogs' backgrounds from the text background itself.

A family's dark and light themes name each other as their dark and light variants, so that the editor shows one of
them in its style list and switches between them when the desktop's style changes.
"""
import json, os, re
from xml.sax.saxutils import quoteattr

from .nvim import name  # noqa: F401 - the files take the names of Neovim's schemes
from .terminals import colours as terminal_colours
from .vscode import mix

with open(os.path.join(os.path.dirname(__file__), "gnome_text_editor.json"), encoding="utf-8") as f:
    DATA = json.load(f)
LANGUAGES = DATA["languages"]
DEFAULT_STYLES = tuple(f"def:{style}" for style in LANGUAGES["def"]["styles"])
# The styles of GtkSourceView's views that the scheme sets (gtksourcestylescheme.c, gtksourcemap.c,
# gtksourcesearchcontext.c), and the misspelled words of libspelling, GNOME Text Editor's spell checker. The secondary
# cursor takes the cursor's colour at half its opacity, and the gutter has no border, as the other targets draw it.
EDITOR_STYLES = ("text", "selection", "selection-unfocused", "cursor", "current-line", "line-numbers",
                 "current-line-number", "bracket-match", "bracket-mismatch", "right-margin", "draw-spaces",
                 "background-pattern", "search-match", "map-overlay", "snippet-focus", "def:misspelled-word")
# The window colours that the scheme's metadata set, by GNOME Text Editor's names (editor-recoloring.c).
WINDOW_COLOURS = ("window_bg_color", "window_fg_color", "headerbar_bg_color", "headerbar_fg_color",
                  "sidebar_bg_color", "sidebar_fg_color", "popover_bg_color", "popover_fg_color", "accent_bg_color",
                  "accent_fg_color", "accent_color")
FONTS = {"": {}, "bold": {"bold": True}, "italic": {"italic": True}, "bold italic": {"bold": True, "italic": True},
         "underline": {"underline": True}, "strike": {"strike": True}}
# The background of comment alerts, such as TODO: an attention wash, as heritage.kate gives them.
ALERT_BACKGROUND = "diffConf"
# The roles held to 3:1 rather than 4.5:1: comments, and alerts, which comments hold.
LOW_CONTRAST_ROLES = ("comment", "todo")
# How far GNOME Text Editor mixes the text background with white for dialogs in dark schemes, and with black and
# white for list views in dark and light schemes (editor-recoloring.c).
DIALOG_DARK, VIEW_DARK, VIEW_LIGHT = 0.07, 0.1, 0.3


def default_styles(p):
    """Default style → (role, font): the roles of heritage.kate's default styles, which follow heritage.nvim."""
    kw = "bold" if p.get("kwBold", not p["dark"]) else ""
    return {
        "def:comment": ("comment", "italic"), "def:shebang": ("comment", "bold italic"),
        "def:doc-comment": ("doc", "italic"), "def:doc-comment-element": ("docTag", "bold italic"),
        # named constants and enum members; true, false, null and their kin take def:special-constant
        "def:constant": ("constant", "bold italic"), "def:special-constant": ("keyword", kw),
        "def:boolean": ("keyword", kw),
        "def:character": ("string", ""), "def:string": ("string", ""), "def:special-char": ("gold", "bold"),
        "def:number": ("number", ""), "def:floating-point": ("number", ""), "def:decimal": ("number", ""),
        "def:base-n-integer": ("number", ""), "def:complex": ("number", ""),
        "def:identifier": ("fg", ""),
        # names followed by an argument list, which most definitions take for calls; declarations in language_rules
        "def:function": ("call", ""), "def:builtin": ("call", "italic"),
        "def:statement": ("keyword", kw), "def:keyword": ("keyword", kw), "def:operator": ("op", ""),
        # words that a language keeps for later use, which def.lang maps to def:error
        "def:reserved": ("keyword", kw),
        "def:type": ("type", ""),
        "def:preprocessor": ("directive", ""),
        "def:error": ("ansiRed", "underline"), "def:warning": ("ansiYellow", ""),
        # alerts in comments, such as TODO and FIXME, on ALERT_BACKGROUND
        "def:note": ("todo", "bold"),
        # markup: headings as declarations, emphasis in the text colour, code as strings, link text in azure and
        # addresses as calls, as heritage.vscode draws Markdown
        "def:emphasis": ("fg", "italic"), "def:strong-emphasis": ("fg", "bold"), "def:inline-code": ("string", ""),
        "def:insertion": ("ansiGreen", ""), "def:deletion": ("ansiRed", "strike"),
        "def:link-text": ("azure", "underline"), "def:link-symbol": ("keyword", kw),
        "def:link-destination": ("call", "italic"), "def:net-address": ("call", "italic"),
        "def:underlined": ("call", "italic"),
        "def:heading": ("method", "bold"), "def:thematic-break": ("op", ""),
        "def:preformatted-section": ("string", ""), "def:list-marker": ("keyword", kw),
        # the text of HTML's title and headings and of LaTeX's sectioning commands, which takes no style of its own
        **{f"def:heading{level}": ("fg", "") for level in range(7)},
    }


def language_rules(p):
    """(language, style ids, role, font, background palette key or None) for the styles whose chain gives a construct
    another role than the one the other targets give it, following heritage.vscode and heritage.kate."""
    kw = "bold" if p.get("kwBold", not p["dark"]) else ""
    rules = []
    def s(language, styles, role, font="", background=None):
        rules.append((language, tuple(styles.split("|")), role, font, background))
    # modifiers and declaration keywords, and the primitive types that the other targets give the keyword role, which
    # the definitions map to def:type
    for language in ("java", "groovy"):
        s(language, "declaration|storage-class|scope-declaration|type", "keyword", kw)
    for language in ("kotlin", "swift", "scala"):
        s(language, "declaration|modifier", "keyword", kw)
        # class names, which these definitions map to def:identifier
        s(language, "type", "type")
    s("c", "storage-class|type", "keyword", kw)  # also C++'s and Objective-C's, which map to these
    s("c-sharp", "type", "keyword", kw)
    s("rust", "type", "keyword", kw)
    s("typescript", "basic-type", "keyword", kw)
    s("sql", "type", "keyword", kw)
    s("php", "type", "keyword", kw)
    # imports, which the definitions map to def:preprocessor
    for language in ("java", "kotlin", "groovy", "scala", "swift", "go", "dart", "zig"):
        s(language, "external", "keyword", kw)
    s("python", "module-handler", "keyword", kw)  # also Python 3's, which maps to it
    s("ruby", "module-handler", "keyword", kw)
    s("perl", "include-statement", "keyword", kw)
    # annotations, decorators, attributes and macros, which the definitions map to def:preprocessor
    s("java", "annotation", "annotation")
    s("python", "decorator", "annotation")
    s("rust", "attribute|macro", "annotation")
    s("c", "attribute", "annotation")
    s("julia", "macro", "annotation")
    s("zig", "builtin-funcs", "call", "italic")
    # declarations, which the definitions mark apart from calls
    s("python", "function-name", "method", "bold")
    s("python", "class-name", "type")
    s("sh", "function", "method", "bold")
    s("fish", "function", "method", "bold")
    s("makefile", "targets", "method", "bold")
    # self, this and other names that the language gives a meaning, as keywords in italics
    s("python", "special-variable", "keyword", "italic")
    s("rust", "self", "keyword", "italic")
    s("kotlin", "builtin", "keyword", "italic")
    s("ruby", "special-variable|predefined-variable", "keyword", "italic")
    s("rust", "lifetime", "typeParam", "italic")
    s("rust", "scope", "fg")
    # the built-in objects and properties of JavaScript, and Ruby's classes and constants
    s("js", "built-in-object", "type")
    s("js", "built-in-property", "field")
    s("ruby", "builtin|constant", "type")
    s("ruby", "symbol", "constant", "bold italic")
    s("ruby", "attribute-definition", "keyword", kw)
    # variables by their prefixes, as the other targets give shell variables; PHP's take the text colour of a name
    for shell in ("sh", "fish"):
        s(shell, "variable", "field", "italic")  # also the variables' definitions, which map to it
        s(shell, "others", "op")
        s(shell, "common-command", "call")
        s(shell, "subshell", "op")
    s("perl", "variable", "field", "italic")
    s("powershell", "variable", "field", "italic")
    s("makefile", "variable", "field", "italic")  # also CMake's, which map to it
    s("php", "variable", "fg")
    s("docker", "variable", "field", "italic")
    # escapes and interpolations
    for language in ("kotlin", "swift", "groovy", "terraform"):
        s(language, "interpolated", "gold", "bold")
    s("python", "format", "gold", "bold")
    s("js", "template-placeholder", "gold", "bold")
    s("js", "regex-class", "number", "bold")
    s("js", "regex-group", "gold", "bold")
    s("scss", "interpolation", "gold", "bold")
    # markup: tags as keywords, attributes as fields, entities as escapes
    s("xml", "element-name", "keyword")  # also HTML's and JSX's tags, which map to it
    s("xml", "attribute-name", "field")
    s("xml", "doctype|processing-instruction", "keyword")
    s("xml", "cdata-delim", "string")
    s("xml", "entity", "gold")
    # CSS: properties as fields, selectors and functions as tags, property values as strings, colours as numbers
    s("css", "property-name|vendor-specific|custom-property-name", "field")
    s("css", "type-selector|class-selector|id-selector|pseudo-selector|attribute-selector-name|function", "keyword")
    s("css", "keyword", "string")
    s("css", "at-rule", "keyword", kw)
    s("css", "modifier", "keyword", "bold")  # !important
    s("scss", "variable", "field", "italic")
    s("less", "variable", "field", "italic")
    # data: keys as fields in JSON and keywords in YAML, TOML and INI files
    s("json", "keyname", "field")
    s("yaml", "scalar|null|bool|int|float", "fg")
    s("yaml", "comment", "doc", "italic")
    s("yaml", "anchor|alias", "annotation")
    s("yaml", "tag", "type")
    s("yaml", "directive", "directive")
    for data in ("toml", "ini"):
        s(data, "variable|non-standard-key", "keyword", kw)
        s(data, "boolean-value", "typeParam", "italic")
    s("toml", "datetime-value", "number")
    # Markdown: quotes as doc comments, labels as link text, the two spaces of a line break as muted underlines
    s("markdown", "blockquote-marker", "doc", "italic")
    s("markdown", "label", "azure", "underline")
    s("markdown", "line-break", "muted", "underline")
    # diffs in the console colours, as the other targets draw them; GtkSourceView also draws its annotations in these
    s("diff", "added-line", "ansiGreen")
    s("diff", "removed-line", "ansiRed")
    s("diff", "changed-line", "ansiBlue")
    s("diff", "diff-file", "ansiBlue", "bold")
    s("diff", "location", "ansiCyan")
    s("diff", "special-case", "comment", "italic")
    return rules


def syntax_styles(p):
    """Style id → (role, font, background palette key or None): the default styles, then language_rules()."""
    out = {style: (*value, ALERT_BACKGROUND if style == "def:note" else None)
           for style, value in default_styles(p).items()}
    if set(out) != set(DEFAULT_STYLES):
        raise ValueError(f"default styles that differ from GtkSourceView's: {sorted(set(out) ^ set(DEFAULT_STYLES))}")
    out = {style: out[style] for style in DEFAULT_STYLES}
    for language, styles, role, font, background in language_rules(p):
        for style in styles:
            if style not in LANGUAGES[language]["styles"]:
                raise ValueError(f"{language} has no style {style!r}")
            key = f"{language}:{style}"
            if key in out:
                raise ValueError(f"{key} is set twice")
            out[key] = (role, font, background)
    return out


def editor_styles(p):
    """Editor style → dict of the style's attributes, as palette keys for colours: what GtkSourceView draws around
    the code, in the roles of heritage.kate's editor colours."""
    caret = "caret" if "caret" in p else "gold"
    out = {
        "text": dict(foreground="fg", background="bg"),
        "selection": dict(background="selection"), "selection-unfocused": dict(background="selInactive"),
        "cursor": dict(foreground=caret),
        "current-line": dict(background="caretRow"),
        "line-numbers": dict(foreground="lineNo", background="bg"),
        "current-line-number": dict(foreground="lineNoCaret", background="caretRow"),
        "bracket-match": dict(background="braceBg", bold="true"),
        "bracket-mismatch": dict(underline="error", **{"underline-color": "error"}, bold="true"),
        # GtkSourceView draws the margin's line in the foreground at 40/255 and fills the area past it with the
        # background at 15/255
        "right-margin": dict(foreground="muted", background="muted"),
        "draw-spaces": dict(foreground="guide"), "background-pattern": dict(background="guide"),
        "search-match": dict(foreground="fg", background="searchBg"),
        "map-overlay": dict(background="selection"),
        "snippet-focus": dict(background="diffMod"),
        # a wavy underline that leaves the word's colours as they are
        "def:misspelled-word": dict(underline="error", **{"underline-color": "error"}),
    }
    if set(out) != set(EDITOR_STYLES):
        raise ValueError(f"editor styles that differ from EDITOR_STYLES: {sorted(set(out) ^ set(EDITOR_STYLES))}")
    return out


def window_colours(p):
    """Window colour → palette key or ANSI colour name: the Islands layout of the other targets."""
    return {"window_bg_color": "bgTool", "window_fg_color": "fg", "headerbar_bg_color": "frame",
            "headerbar_fg_color": "fg", "sidebar_bg_color": "bgTool", "sidebar_fg_color": "fg",
            "popover_bg_color": "surface", "popover_fg_color": "fg", "accent_bg_color": "ansiBlue",
            "accent_fg_color": "bg", "accent_color": "ansiBlue"}


def hexes(p):
    """Palette key or ANSI colour name (ansiBlack to ansiWhite) → #rrggbb."""
    out = {k: "#" + v.lower() for k, v in p.items() if isinstance(v, str) and re.fullmatch(r"[0-9A-F]{6}", v)}
    out.update({f"ansi{n.title()}": colour.lower() for n, colour in zip(
        ("black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"), terminal_colours(p)["ansi"])})
    return out


def syntax_attributes(p, role, font, background=None):
    """The attributes of a syntax style: its colours and every font flag, so that no flag of an enclosing style shows.
    An error takes the wavy underline of GtkSourceView's spelling and diagnostics, in the error colour."""
    c = hexes(p)
    flags = FONTS[font]
    out = {"foreground": c[role]}
    if background:
        out["background"] = c[background]
    out["bold"] = "true" if flags.get("bold") else "false"
    out["italic"] = "true" if flags.get("italic") else "false"
    if flags.get("underline"):
        out["underline"] = "error" if role == "ansiRed" else "single"
    else:
        out["underline"] = "none"
    if role == "ansiRed" and flags.get("underline"):
        out["underline-color"] = c["error"]
    out["strikethrough"] = "true" if flags.get("strike") else "false"
    return out


def variant(t, themes):
    """The id of t's counterpart among its family's themes, the light one for a dark theme and the dark one for a
    light theme, or None when the family has no such theme, or more than one theme of either kind."""
    others = [o for o in themes if o["palette"]["dark"] != t["palette"]["dark"]]
    mine = [o for o in themes if o["palette"]["dark"] == t["palette"]["dark"]]
    return name(others[0]) if len(others) == 1 and len(mine) == 1 else None


def scheme(t, themes, source):
    """The styles/<theme>.xml file for a theme dict. themes are its family's themes and source the URL of the theme
    folder."""
    p = t["palette"]
    c = hexes(p)
    metadata = [("variant", "dark" if p["dark"] else "light")]
    counterpart = variant(t, themes)
    if counterpart:
        metadata.append(("light-variant" if p["dark"] else "dark-variant", counterpart))
    metadata += [(key, c[role]) for key, role in window_colours(p).items()]
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             f"<!-- {p['name']}: a Heritage Themes style scheme for GNOME Text Editor. Generated from {source}; changes "
             "here are overwritten. SPDX-License-Identifier: MIT -->",
             f'<style-scheme id={quoteattr(name(t))} name={quoteattr(p["name"])} version="1.0">',
             "  <author>Heritage Themes</author>",
             f"  <description>{p['name']}: colours drawn from a culture's colour tradition.</description>",
             "  <metadata>"]
    lines += [f"    <property name={quoteattr(key)}>{value}</property>" for key, value in metadata]
    lines.append("  </metadata>")

    def style(style_id, attributes):
        attrs = " ".join(f"{key}={quoteattr(value)}" for key, value in attributes.items())
        lines.append(f"  <style name={quoteattr(style_id)} {attrs}/>")
    for style_id, attributes in editor_styles(p).items():
        style(style_id, {k: c[v] if k in ("foreground", "background", "underline-color") else v
                         for k, v in attributes.items()})
    for style_id, (role, font, background) in syntax_styles(p).items():
        style(style_id, syntax_attributes(p, role, font, background))
    lines.append("</style-scheme>")
    return "\n".join(lines) + "\n"


def derived(p):
    """The backgrounds that GNOME Text Editor derives from the text background: list views and dialogs."""
    if p["dark"]:
        return {"view": mix(p["bg"], "000000", VIEW_DARK), "dialog": mix(p["bg"], "FFFFFF", DIALOG_DARK)}
    return {"view": mix(p["bg"], "FFFFFF", VIEW_LIGHT), "dialog": p["bg"]}


def styles(p):
    """Element → dict(fg, bg) as #rrggbb, for the build's contrast check: each syntax style on the background it is
    drawn on, bg unless it sets one, the editor's text on its highlights, and the window's text on its surfaces."""
    c = hexes(p)
    out = {}
    for style_id, (role, font, background) in syntax_styles(p).items():
        out[style_id] = dict(fg=c[role], bg=c[background or "bg"])
        if not background:
            out[f"{style_id} on the current line"] = dict(fg=c[role], bg=c["caretRow"])
    editor = editor_styles(p)
    for element, fg, style_id in (("found text", "fg", "search-match"), ("matching bracket", "fg", "bracket-match"),
                                  ("selected text", "fg", "selection"), ("snippet field", "fg", "snippet-focus"),
                                  ("current line number", "lineNoCaret", "current-line-number")):
        out[element] = dict(fg=c[fg], bg=c[editor[style_id]["background"]])
    window = window_colours(p)
    for fg, bg in (("window_fg_color", "window_bg_color"), ("headerbar_fg_color", "headerbar_bg_color"),
                   ("sidebar_fg_color", "sidebar_bg_color"), ("popover_fg_color", "popover_bg_color"),
                   ("accent_fg_color", "accent_bg_color"), ("accent_color", "window_bg_color"),
                   ("accent_color", "popover_bg_color")):
        out[f"{fg} on {bg}"] = dict(fg=c[window[fg]], bg=c[window[bg]])
    for surface, colour in derived(p).items():
        out[f"text on the {surface} background"] = dict(fg=c["fg"], bg="#" + colour.lower())
    return out


def low_contrast(p):
    """The elements of styles() held to 3:1: the syntax styles in the roles of LOW_CONTRAST_ROLES, and the one
    character that the bracket match draws its background behind, as in heritage.kate."""
    out = {"matching bracket"}
    for style_id, (role, *_) in syntax_styles(p).items():
        if role in LOW_CONTRAST_ROLES:
            out |= {style_id, f"{style_id} on the current line"}
    return out


def pixel_palette(p):
    """What scripts/editors/pixels.py checks a screenshot against: the editor, cropped from the window that
    scripts/editors/shoot.py opens at 1100x700, with the header bar, tab bar and status bar left out, where GNOME
    Text Editor draws Adwaita's icons and widgets."""
    colours = {colour.upper() for colour in hexes(p).values()}
    backgrounds = ["#" + p[k] for k in ("bgTool", "frame", "surface", "caretRow", "selection", "selInactive",
                                        "diffConf", "searchBg", "braceBg")]
    return dict(background="#" + p["bg"], backgrounds=backgrounds, foregrounds=sorted(colours),
                crop=[56, 6, 6, 6])
