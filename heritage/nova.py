"""Nova themes generated from a palette: one extension with a theme stylesheet for each Heritage theme.

A Nova theme is a stylesheet in the Themes folder of an extension, which Nova lists by its file name. Its selectors
are Nova's: meta.* for the window, buttons, text fields and the editor, the syntax scopes of Nova's grammars, and
terminal.* for the terminal's 16 colours. The syntax scopes take the roles that the other targets give the same
constructs, and the terminal the colours of heritage.terminals. The layout follows the Islands of the other targets:
the window and title bar on the frame, the editor on bg, buttons and text fields on surface.
"""
import json, re

from .terminals import ANSI_NAMES, colours as terminal_colours

FOLDER = "Heritage Themes.novaextension"
IDENTIFIER = "heritage-themes.HeritageThemes"


def file_name(t):
    """The theme's stylesheet, named after the theme, as Nova lists a theme by its file name."""
    return f"Themes/{t['palette']['name']}.css"


def syntax(p):
    """Syntax scope → (palette key, font style)."""
    kw = "bold" if p.get("kwBold", not p["dark"]) else ""
    out = {}
    def s(scopes, role, font=""):
        out.update({scope: (role, font) for scope in scopes.split()})
    s("keyword keyword.construct keyword.condition keyword.modifier keyword.operator declaration tag "
      "style.at style.selector style.selector.element style.selector.pseudoclass style.selector.pseudoelement "
      "markup.list value.boolean value.null", "keyword", kw)
    s("processing", "directive")  # preprocessor directives, such as C's #include
    s("keyword.self", "keyword", "italic")
    s("comment", "comment", "italic")
    s("bracket operator", "op")
    s("invalid", "ansiRed", "bold")
    s("value value.number style.value.number style.value.color.hex", "number")
    s("value.entity regex.escaped", "gold", "bold")
    s("value.symbols identifier.constant style.value.color style.value.color.named style.value.keyword", "constant",
      "bold italic")
    s("string string-template regex cdata tag.attribute.value markup.code", "string")
    s("string.key identifier.key identifier.property identifier.global definition.property style.attribute "
      "style.attribute.name", "field")
    s("string-template.value identifier identifier.variable definition definition.package style style.value markup "
      "markup.list.item", "fg")
    s("identifier.type identifier.type.class identifier.type.enum identifier.type.union identifier.type.struct "
      "definition.type definition.class definition.enum definition.union definition.struct tag.framework "
      "style.selector.identifier.id style.selector.identifier.class", "type")
    s("identifier.type.protocol definition.protocol", "type", "italic")
    s("identifier.decorator tag.attribute tag.attribute.name", "annotation")
    s("identifier.function identifier.method", "call")
    s("identifier.core", "call", "italic")
    s("identifier.argument", "param")
    s("definition.function definition.method markup.heading", "method", "bold")
    s("markup.line", "muted")
    s("markup.bold", "fg", "bold")
    s("markup.italic", "fg", "italic")
    s("markup.strikethrough", "fg", "strikethrough")
    s("markup.link", "azure", "underline")
    return out


# Selectors drawn as marks or disabled rather than text, which the contrast check leaves out: line numbers, as every
# target draws them in the line number colours, and disabled buttons.
DECORATIVE = {"meta.gutter", "meta.gutter.selected", "meta.button.disabled"}
FONTS = {"": [], "bold": ["font-weight: bold"], "italic": ["font-style: italic"],
         "bold italic": ["font-weight: bold", "font-style: italic"], "underline": ["text-decoration: underline"],
         "strikethrough": ["text-decoration: line-through"]}


def ui(p):
    """meta selector → {property: palette key or literal}."""
    return {
        "meta": {"-theme-interface-style": "dark" if p["dark"] else "light", "-theme-vibrancy": "none",
                 "-theme-accent-color": "false"},
        "meta.window": {"background-color": "frame", "border-color": "border"},
        "meta.titlebar": {"color": "fg", "background-color": "frame", "border-color": "border"},
        "meta.titlebar.inactive": {"color": "muted", "background-color": "frame", "border-color": "border"},
        "meta.button": {"color": "fg", "background-color": "surface", "border-color": "border"},
        "meta.button.disabled": {"color": "disabled", "background-color": "surface", "border-color": "border"},
        "meta.button.highlighted": {"color": "fg", "background-color": "hover", "border-color": "border"},
        "meta.button.selected": {"color": "fg", "background-color": "selection", "border-color": "border"},
        "meta.button.highlighted.selected": {"color": "fg", "background-color": "selection", "border-color": "border"},
        "meta.document.button": {"color": "fg", "background-color": "surface", "border-color": "border"},
        "meta.document.button.highlighted": {"color": "fg", "background-color": "hover", "border-color": "border"},
        "meta.document.button.selected": {"color": "fg", "background-color": "selection", "border-color": "border"},
        "meta.textfield": {"background-color": "surface", "border-color": "border"},
        "meta.textfield.active": {"background-color": "surface", "border-color": "ansiBlue"},
        "meta.document.textfield": {"background-color": "surface", "border-color": "border"},
        "meta.document": {"background-color": "bg", "border-color": "border"},
        "meta.text": {"color": "fg"},
        "meta.text.selected": {"color": "fg", "background-color": "selection"},
        "meta.cursor": {"background-color": "caret"},
        "meta.indentguide": {"border-color": "guide"},
        "meta.gutter": {"background-color": "bg", "color": "lineNo"},
        "meta.gutter.selected": {"background-color": "caretRow", "color": "lineNoCaret"},
    }


def hexes(p):
    out = {k: "#" + v for k, v in p.items() if isinstance(v, str) and re.fullmatch(r"[0-9A-F]{6}", v)}
    out["caret"] = "#" + p.get("caret", p["gold"])
    out.update({f"ansi{n.title()}": colour for n, colour in zip(ANSI_NAMES, terminal_colours(p)["ansi"])})
    return out


def theme(t, source):
    """The Themes/<theme>.css stylesheet for a theme dict. source is the URL of the theme folder."""
    p = t["palette"]
    c = hexes(p)
    lines = [f"/* {p['name']}: a Heritage Themes theme for Nova. Generated from {source}; changes here are "
             "overwritten. */"]
    for selector, properties in ui(p).items():
        lines += ["", f"{selector} {{", *(f"    {prop}: {c.get(value, value)};" for prop, value in properties.items()),
                  "}"]
    for scope, (role, font) in syntax(p).items():
        lines += ["", f"{scope} {{", f"    color: {c[role]};", *(f"    {style};" for style in FONTS[font]), "}"]
    ansi = terminal_colours(p)["ansi"]
    for i, n in enumerate(ANSI_NAMES):
        lines += ["", f"terminal.{n} {{", f"    color: {ansi[i]};", "}"]
        lines += ["", f"terminal.bright-{n} {{", f"    color: {ansi[i + 8]};", "}"]
    return "\n".join(lines) + "\n"


def manifest(version, url, description):
    """The extension's extension.json."""
    return json.dumps({"identifier": IDENTIFIER, "name": "Heritage Themes", "organization": "Heritage Themes",
                       "description": description, "version": version, "categories": ["themes"],
                       "repository": url, "bugs": f"{url}/issues", "license": "MIT"}, indent=2) + "\n"


def styles(p):
    """Element → dict(fg, bg) as #RRGGBB, for the build's contrast check: each syntax scope on bg and the window's
    texts on their backgrounds."""
    c = hexes(p)
    out = {scope: dict(fg=c[role], bg=c["bg"]) for scope, (role, _) in syntax(p).items()}
    for selector, properties in ui(p).items():
        if "color" in properties and "background-color" in properties and selector not in DECORATIVE:
            out[selector] = dict(fg=c[properties["color"]], bg=c[properties["background-color"]])
    out["meta.text"] = dict(fg=c["fg"], bg=c["bg"])
    return out


def parse(text):
    """selector → {property: value} of a stylesheet."""
    code = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    return {selector.strip(): dict(re.findall(r"([\w-]+)\s*:\s*([^;]+);", body))
            for selector, body in re.findall(r"([^{}]+)\{([^{}]*)\}", code)}
