"""Lapce colour theme generated from a palette: a TOML file of a plugin whose volt.toml lists every theme.

A theme has base colours, which the other tables name as $<name>, syntax colours, and UI colours. Lapce matches each
capture of its grammars' queries to the closest of the scopes it recognises (SCOPES, from lapce-core's style.rs) and
looks the scope up exactly, and takes the standard LSP semantic token types (TOKENS) as they are, so the theme sets
each of those, with the roles that the other targets give the constructs. Numbers, booleans and named constants all
reach the constant scope, which takes the number role, as numbers are the most common of them and Lapce's own themes
colour the scope as numbers. Lapce draws syntax in colour only, without font styles. The UI keys are every key of
Lapce's own dark theme, so none of its colours shows through, laid out as the Islands of the other targets: panels,
the activity bar, the status bar and popups on bgTool and surface, the editor and its active tab on bg.
"""
import re

from .nvim import name  # noqa: F401 - the theme files take the names of Neovim's schemes
from .terminals import colours as terminal_colours

PLUGIN = "heritage-themes"
# The scopes that Lapce 0.4 recognises (lapce-core/src/style.rs) → palette role.
SCOPES = {
    "constant": "number", "type": "type", "type.builtin": "keyword", "property": "field", "comment": "comment",
    "constructor": "type", "function": "call", "label": "label", "keyword": "keyword", "string": "string",
    "variable": "fg", "variable.other.member": "field", "operator": "op", "attribute": "annotation", "escape": "gold",
    "embedded": "fg", "symbol": "constant", "punctuation": "op", "punctuation.special": "op",
    "punctuation.delimiter": "op", "text": "fg", "text.literal": "string", "text.title": "method", "text.uri": "azure",
    "text.reference": "azure", "string.escape": "gold", "conceal": "muted", "none": "fg", "tag": "keyword",
    "markup.bold": "fg", "markup.italic": "fg", "markup.list": "keyword", "markup.quote": "doc",
    "markup.heading": "method", "markup.link.url": "call", "markup.link.label": "azure", "markup.link.text": "azure",
}
# LSP semantic token types, with the names of Lapce's own themes for them, → the role that heritage.vscode gives the
# matching semantic tokens; rainbow brackets in the ANSI colours.
TOKENS = {
    "namespace": "fg", "class": "type", "enum": "type", "interface": "type", "struct": "type", "structure": "type",
    "typeAlias": "type", "typeParameter": "typeParam", "parameter": "param", "enumMember": "constant",
    "enum-member": "constant", "event": "field", "field": "field", "method": "call", "function.method": "call",
    "macro": "annotation", "decorator": "annotation", "modifier": "keyword", "number": "number", "regexp": "string",
    "builtinType": "keyword", "selfKeyword": "keyword",
    "bracket.color.1": "ansiBlue", "bracket.color.2": "ansiMagenta", "bracket.color.3": "ansiGreen",
    "bracket.unpaired": "ansiRed",
}


def syntax(p):
    """Syntax key → palette role."""
    return {**SCOPES, **TOKENS}


def base(p):
    """Base colour name → #RRGGBB: the theme's surfaces and text, and the ANSI colours by name."""
    c = terminal_colours(p)
    hexes = {k: "#" + v for k, v in p.items() if isinstance(v, str) and re.fullmatch(r"[0-9A-F]{6}", v)}
    out = {name: colour for name, colour in zip(("black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"),
                                                c["ansi"][:8])}
    out.update({"grey": hexes["muted"], "orange": hexes["gold"], "purple": c["ansi"][5]})
    out.update({
        "primary-background": hexes["bg"], "secondary-background": hexes["bgTool"],
        "current-background": hexes["selection"], "text": hexes["fg"], "dim-text": hexes["muted"],
    })
    return out


def ui(p):
    """UI key → colour value, a $base name or #RRGGBB, with #RRGGBBAA for layers."""
    c = {k: "#" + v for k, v in p.items() if isinstance(v, str) and re.fullmatch(r"[0-9A-F]{6}", v)}
    t = terminal_colours(p)
    caret = "#" + p.get("caret", p["gold"])
    def layer(key, alpha):
        return c[key] + alpha
    def mode(colour):
        return {"background": colour, "foreground": c["bg"]}
    out = {
        "lapce.error": t["ansi"][1], "lapce.warn": t["ansi"][3], "lapce.dropdown_shadow": "#00000040",
        "lapce.border": c["border"], "lapce.scroll_bar": layer("muted", "66"),
        "lapce.button.primary.background": c["ansiBlue"], "lapce.button.primary.foreground": c["bg"],
        "lapce.tab.active.background": c["bg"], "lapce.tab.active.foreground": c["fg"],
        "lapce.tab.active.underline": c["red"],
        "lapce.tab.inactive.background": c["bgTool"], "lapce.tab.inactive.foreground": c["muted"],
        "lapce.tab.inactive.underline": c["bgTool"], "lapce.tab.separator": c["border"],
        "lapce.icon.active": c["fg"], "lapce.icon.inactive": c["muted"],
        "lapce.remote.icon": c["bg"], "lapce.remote.local": c["ansiBlue"], "lapce.remote.connected": c["ansiGreen"],
        "lapce.remote.connecting": c["ansiYellow"], "lapce.remote.disconnected": c["ansiRed"],
        "lapce.plugin.name": c["fg"], "lapce.plugin.description": c["fg"], "lapce.plugin.author": c["muted"],
        "editor.background": c["bg"], "editor.foreground": c["fg"], "editor.dim": c["muted"],
        "editor.focus": c["fg"], "editor.caret": caret, "editor.selection": c["selection"],
        "editor.current_line": c["caretRow"], "editor.debug_break_line": layer("diffConf", "CC"),
        "editor.link": c["azure"], "editor.visible_whitespace": c["guide"], "editor.indent_guide": c["guide"],
        "editor.drag_drop_background": layer("selection", "88"), "editor.drag_drop_tab_background": layer("hover", "88"),
        "editor.sticky_header_background": c["bg"],
        "inlay_hint.foreground": c["muted"], "inlay_hint.background": c["surface"],
        "error_lens.error.foreground": t["ansi"][1], "error_lens.error.background": c["diffDel"],
        "error_lens.warning.foreground": t["ansi"][3], "error_lens.warning.background": c["diffConf"],
        "error_lens.other.foreground": c["muted"], "error_lens.other.background": c["surface"],
        "completion_lens.foreground": c["muted"],
        "source_control.added": c["added"], "source_control.removed": c["deleted"],
        "source_control.modified": c["modified"],
        "tooltip.background": c["surface"], "tooltip.foreground": c["fg"],
        "palette.background": c["surface"], "palette.foreground": c["fg"],
        "palette.current.background": c["selection"], "palette.current.foreground": c["fg"],
        "completion.background": c["surface"], "completion.current": c["selection"],
        "hover.background": c["surface"],
        "activity.background": c["frame"], "activity.current": c["bgTool"],
        "debug.breakpoint": c["ansiRed"], "debug.breakpoint.hover": layer("ansiRed", "66"),
        "panel.background": c["bgTool"], "panel.foreground": c["fg"], "panel.foreground.dim": c["muted"],
        "panel.current.background": c["selection"], "panel.current.foreground": c["fg"],
        "panel.current.foreground.dim": c["muted"], "panel.hovered.background": c["hover"],
        "panel.hovered.active.background": c["selInactive"], "panel.hovered.foreground": c["fg"],
        "panel.hovered.foreground.dim": c["muted"],
        "status.background": c["frame"], "status.foreground": c["fg"],
        **{f"status.modal.{name}.{part}": colour for name, colour in (
            ("normal", c["ansiBlue"]), ("insert", c["ansiGreen"]), ("visual", c["ansiMagenta"]),
            ("terminal", c["ansiCyan"])) for part, colour in mode(colour).items()},
        "markdown.blockquote": c["doc"],
        "terminal.cursor": caret, "terminal.foreground": c["fg"], "terminal.background": c["bgTool"],
        **{f"terminal.{n}": colour for n, colour in zip(("black", "red", "green", "yellow", "blue", "magenta", "cyan",
                                                           "white"), t["ansi"][:8])},
        **{f"terminal.bright_{n}": colour for n, colour in zip(("black", "red", "green", "yellow", "blue", "magenta",
                                                                  "cyan", "white"), t["ansi"][8:])},
    }
    return out


def quote(value):
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def theme(p, source):
    """The themes/<theme>.toml file for a palette. source is the URL of the theme folder."""
    lines = [
        f"# {p['name']}: a Heritage Themes colour theme for Lapce.",
        f"# Generated from {source}; changes here are overwritten.",
        "",
        "[color-theme]",
        f"name = {quote(p['name'])}",
        "",
        "[color-theme.base]",
        *(f"{key} = {quote(value)}" for key, value in base(p).items()),
        "",
        "[color-theme.syntax]",
        *(f"{quote(key)} = {quote('#' + p[role])}" for key, role in syntax(p).items()),
        "",
        "[color-theme.ui]",
        *(f"{quote(key)} = {quote(value)}" for key, value in ui(p).items()),
    ]
    return "\n".join(lines) + "\n"


def volt(themes, version, url):
    """The plugin's volt.toml, which lists the theme files."""
    files = ", ".join(quote(f"themes/{name(t)}.toml") for t in themes)
    return "\n".join([
        f"name = {quote(PLUGIN)}",
        f"version = {quote(version)}",
        'author = "heritage-themes"',
        'display-name = "Heritage Themes"',
        'description = "Colour themes drawn from the colour traditions of different cultures."',
        f"repository = {quote(url)}",
        f"color-themes = [{files}]",
    ]) + "\n"


def styles(p):
    """Element → dict(fg, bg) for the build's contrast check: each syntax role on the editor's background, and the UI
    texts on the surfaces they are drawn on."""
    u = ui(p)
    out = {f"syntax {key}": dict(fg="#" + p[role], bg="#" + p["bg"]) for key, role in syntax(p).items()}
    for prefix in ("lapce.tab.active", "lapce.tab.inactive", "palette", "palette.current", "panel", "panel.current",
                   "panel.hovered", "tooltip", "status", "terminal"):
        out[prefix] = dict(fg=u[f"{prefix}.foreground"], bg=u[f"{prefix}.background"])
    out["completion"] = dict(fg="#" + p["fg"], bg=u["completion.background"])
    out["inlay hint"] = dict(fg=u["inlay_hint.foreground"], bg=u["inlay_hint.background"])
    out["primary button"] = dict(fg=u["lapce.button.primary.foreground"], bg=u["lapce.button.primary.background"])
    for mode in ("normal", "insert", "visual", "terminal"):
        out[f"{mode} mode"] = dict(fg=u[f"status.modal.{mode}.foreground"], bg=u[f"status.modal.{mode}.background"])
    return out


def pixel_palette(p):
    """What scripts/editors/pixels.py checks a screenshot against: every colour the theme draws, and the backgrounds
    that text sits on. Lapce draws its whole window in the theme's colours, so nothing is cropped."""
    colours = {"#" + v for v in p.values() if isinstance(v, str) and re.fullmatch(r"[0-9A-F]{6}", v)}
    colours |= set(terminal_colours(p)["ansi"])
    return dict(background="#" + p["bg"],
                backgrounds=["#" + p[k] for k in ("bgTool", "frame", "surface", "caretRow", "selection", "hover")],
                foregrounds=sorted(colours), crop=[0, 0, 0, 0])
