"""Sublime Text colour scheme generated from a palette.

The rules map the same palette roles as heritage.vscode to scopes. Sublime Text's syntaxes follow the scope naming
of TextMate grammars, so the generic rules are the VS Code token rules; RULES adds the scopes in which Sublime
Text's own syntaxes differ. The scheme names every palette colour as a variable and refers to it as var(role), so a
user override in Packages/User can change a colour once.
"""
import re, unicodedata

from . import vscode

AUTHOR = "Heritage Themes"
VARIABLE = re.compile(r"var\((\w+)\)")
# Letters that Unicode normalisation does not reduce to ASCII, in the Latin spellings the themes use.
TRANSLITERATION = str.maketrans({"Ł": "L", "ł": "l", "ŋ": "ng", "ṉ": "n"})


def filename(name):
    """The scheme's file name for a theme name, in ASCII so that the colour_scheme setting reads the same on every
    file system, for example "Lowicz Wycinanka (Dark).sublime-color-scheme"."""
    ascii_name = unicodedata.normalize("NFKD", name.translate(TRANSLITERATION)).encode("ascii", "ignore").decode()
    if not re.fullmatch(r"[A-Za-z0-9 ()]+", ascii_name):
        raise SystemExit(f"sublime: {name!r} becomes {ascii_name!r}; extend TRANSLITERATION or rename the theme")
    return f"{ascii_name}.sublime-color-scheme"


def variables(p):
    """Every palette colour as a #-prefixed variable named after its role."""
    return {k: "#" + v for k, v in p.items() if isinstance(v, str) and re.fullmatch(r"[0-9A-F]{6}", v)}


def resolve(colour, scheme):
    """The #RRGGBB of a scheme colour, which is a literal or var(role)."""
    match = VARIABLE.fullmatch(colour)
    return scheme["variables"][match.group(1)] if match else colour


def globals_(p):
    """Editor-wide colours."""
    caret = "caret" if "caret" in p else "gold"
    return {
        "background": "var(bg)", "foreground": "var(fg)", "caret": f"var({caret})",
        "invisibles": "var(guide)", "line_highlight": "var(caretRow)",
        "selection": "var(selection)", "inactive_selection": "var(selInactive)",
        "gutter": "var(bg)", "gutter_foreground": "var(lineNo)", "gutter_foreground_highlight": "var(lineNoCaret)",
        "line_diff_added": "var(added)", "line_diff_modified": "var(modified)", "line_diff_deleted": "var(deleted)",
        "find_highlight": "var(searchBg)", "find_highlight_foreground": "var(fg)", "highlight": "var(searchBorder)",
        "scroll_highlight": "var(gold)", "scroll_selected_highlight": "var(red)",
        "guide": "var(guide)", "active_guide": "var(guideSel)", "stack_guide": "var(guide)", "rulers": "var(guide)",
        "brackets_options": "underline", "brackets_foreground": "var(gold)",
        "bracket_contents_options": "underline", "bracket_contents_foreground": "var(guideSel)",
        "tags_options": "stippled_underline", "tags_foreground": "var(gold)",
        "misspelling": "var(error)", "fold_marker": "var(muted)", "minimap_border": "var(border)",
        "accent": "var(red)", "shadow": "#00000059" if p["dark"] else "#00000024",
    }


def rules(p):
    """Scope rules as (scope selectors, role, font style): the VS Code rules, except for the selectors that
    Sublime Text's own rules below set again, then those rules."""
    kw = "bold" if p.get("kwBold", not p["dark"]) else ""
    out = []
    def s(scopes, role, font=""):
        out.append((scopes, role, font))
    # Sublime Text's scope naming: types under entity.name, function calls as variable.function
    s("entity.name.class, entity.name.struct, entity.name.enum, entity.name.union, entity.name.trait, "
      "entity.name.impl, entity.name.type, entity.other.inherited-class, support.class, support.type", "type")
    s("entity.name.interface", "type", "italic")
    s("entity.name.function, entity.name.function.constructor, entity.name.function.destructor", "method", "bold")
    s("variable.function, support.function", "call")
    s("variable.language, constant.language", "keyword", kw)
    s("variable.parameter", "param")
    s("variable.other.member, variable.other.property", "field")
    s("variable.other.constant, entity.name.constant, support.constant", "constant", "bold italic")
    s("variable.annotation, meta.annotation, punctuation.definition.annotation", "annotation")
    s("entity.name.label", "label", "bold")
    s("keyword.declaration, keyword.control, storage.type.class, storage.type.function, storage.type.struct, "
      "storage.type.enum, storage.type.interface, storage.type.trait, storage.type.impl, storage.type.union",
      "keyword", kw)
    s("storage.type.primitive, storage.type.numeric, storage.type.built-in", "keyword", kw)
    s("keyword.operator.word, punctuation.definition.keyword", "keyword", kw)
    s("punctuation.accessor, punctuation.separator, punctuation.terminator", "op")
    s("entity.name.namespace, entity.name.module, support.module", "fg")
    # JSON keys are plain strings under meta.mapping.key; Markdown names its raw text, lists and links differently
    s("source.json meta.mapping.key string, source.json meta.mapping.key punctuation.definition.string", "field")
    s("markup.raw.inline, markup.raw.block", "string")
    s("punctuation.definition.list_item, punctuation.definition.raw.begin, punctuation.definition.raw.end", "keyword", kw)
    s("meta.link.inline.description, meta.link.reference.description", "azure", "underline")
    s("constant.other.language-name", "constant", "bold italic")
    # diff and diagnostic text takes the console colours, which the build checks as text on bg
    s("markup.inserted, diff.inserted", "ansiGreen")
    s("markup.deleted, diff.deleted", "ansiRed")
    s("markup.changed, diff.changed", "ansiBlue")
    s("invalid, invalid.illegal, markup.error", "ansiRed")
    s("invalid.deprecated, markup.warning", "ansiYellow", "underline")
    s("markup.info", "ansiCyan")
    # regions that plugins such as LSP, SublimeLinter and GitGutter colour by name
    for name, role in (("redish", "ansiRed"), ("orangish", "gold"), ("yellowish", "ansiYellow"),
                       ("greenish", "ansiGreen"), ("bluish", "ansiBlue"), ("purplish", "ansiMagenta"),
                       ("pinkish", "ansiMagenta")):
        s(f"region.{name}", role)
    replaced = {selector for scopes, _, _ in out for selector in scopes.split(", ")}
    inherited = []
    for scopes, role, font in vscode.token_rules(p):
        kept = [selector for selector in scopes.split(", ") if selector not in replaced]
        if kept:
            inherited.append((", ".join(kept), role, font))
    return inherited + out


def scheme(p):
    """The .sublime-color-scheme document for a palette."""
    out = []
    for scopes, role, font in rules(p):
        rule = {"scope": scopes, "foreground": f"var({role})"}
        if font:
            rule["font_style"] = font
        out.append(rule)
    return {"name": p["name"], "author": AUTHOR, "variables": variables(p), "globals": globals_(p), "rules": out}
