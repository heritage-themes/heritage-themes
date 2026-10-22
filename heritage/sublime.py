"""Sublime Text colour scheme and UI theme generated from a palette.

The scheme's rules map the same palette roles as heritage.vscode to scopes. Sublime Text's syntaxes follow the scope
naming of TextMate grammars, so the generic rules are the VS Code token rules; rules() adds the scopes in which
Sublime Text's own syntaxes differ. The scheme names every palette colour as a variable and refers to it as
var(role), so a user override in Packages/User can change a colour once.

The UI theme extends Sublime Text's built-in Adaptive theme, which derives the interface from the colour scheme's
background. Its rules come after Adaptive's, so they take precedence, and give the surfaces and text the palette
roles that heritage.vscode gives the matching workbench keys. Icons, buttons and scroll bars keep Adaptive's
translucent white or black, which takes the hue of the surface below. Theme rules can read only a few colours from
the scheme, so the theme carries the palette's colours as hex values and pairs with the scheme of the same name.
"""
import re, unicodedata

from . import vscode

AUTHOR = "Heritage Themes"
VARIABLE = re.compile(r"var\((\w+)\)")
# Letters that Unicode normalisation does not reduce to ASCII, in the Latin spellings the themes use.
TRANSLITERATION = str.maketrans({"Ł": "L", "ł": "l", "ŋ": "ng", "ṉ": "n"})


def basename(name):
    """The name of a theme's files without the extension, in ASCII so that the color_scheme and theme settings read
    the same on every file system, for example "Lowicz Wycinanka (Dark)"."""
    ascii_name = unicodedata.normalize("NFKD", name.translate(TRANSLITERATION)).encode("ascii", "ignore").decode()
    if not re.fullmatch(r"[A-Za-z0-9 ()]+", ascii_name):
        raise SystemExit(f"sublime: {name!r} becomes {ascii_name!r}; extend TRANSLITERATION or rename the theme")
    return ascii_name


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


# Palette role of each surface of the UI theme. The editor, the selected tab joined to it and the text inputs take bg
# from the scheme. The title bar, sidebar, tab bar, panels and status bar form the frame around them, as the main
# window does in the Islands UI; bgTool is too close to bg to set apart the sidebar or a panel's inputs, which
# adjoin them. Popups take surface.
SURFACES = dict(title="frame", sidebar="frame", tabs="frame", panel="frame", status="frame", popup="surface")
# Settings values of Adaptive's rules for the rounded and square tab styles, which draw tabs on the tab bar's tint;
# the angled style tints the tab bar from the scheme background instead.
FLAT_TABS = {"file_tab_style": ["", "rounded", "square"]}


def ui_theme(p):
    """The .sublime-theme document for a palette. Each text colour it sets, on each palette colour it sets below
    that text, is a pair in build.py's CONTRAST, so the build checks it."""
    c = {k: "#" + v for k, v in p.items() if isinstance(v, str) and re.fullmatch(r"[0-9A-F]{6}", v)}
    surface = {k: c[role] for k, role in SURFACES.items()}
    def selected(cls, tint):
        return {"class": cls, "attributes": ["selected"], "layer0.tint": tint, "layer0.opacity": 1.0}
    def label(cls, fg, match, selected_fg):
        return {"class": cls, "fg": fg, "match_fg": match, "selected_fg": selected_fg, "selected_match_fg": match}
    rules = [
        # frame: title bar, tab bar, status bar and sidebar
        {"class": "title_bar", "settings": ["themed_title_bar"], "bg": surface["title"], "fg": c["fg"],
         "style": "dark" if p["dark"] else "light"},
        {"class": "tabset_control", "settings": FLAT_TABS, "layer0.tint": surface["tabs"]},
        {"class": "tab_control", "settings": FLAT_TABS, "layer0.tint": surface["tabs"]},
        {"class": "tabset_control", "settings": {"file_tab_style": "angled"}, "tint_modifier": surface["tabs"]},
        {"class": "tab_label", "fg": c["muted"], "opacity": 1.0},
        {"class": "tab_label", "parents": [{"class": "tab_control", "attributes": ["hover"]}], "fg": c["fg"]},
        {"class": "tab_label", "parents": [{"class": "tab_control", "attributes": ["selected"]}], "fg": c["fg"]},
        {"class": "grid_layout_control", "border_color": surface["tabs"]},
        {"class": "status_bar", "layer0.tint": surface["status"], "layer1.tint": c["border"]},
        {"class": "sidebar_container", "layer0.tint": surface["sidebar"], "layer0.opacity": 1.0},
        {"class": "tree_row", "attributes": ["selectable", "hover"], "layer0.tint": c["hover"],
         "layer0.opacity": 1.0},
        selected("tree_row", c["selection"]),
        {"class": "sidebar_heading", "fg": c["muted"], "shadow_color": "transparent"},
        {"class": "sidebar_label", "fg": c["fg"]},
        {"class": "sidebar_label", "parents": [{"class": "file_system_entry", "attributes": ["ignored"]}],
         "fg": c["muted"]},
        *({"class": "sidebar_label", "parents": [{"class": "tree_row", "attributes": [state]}], "fg": c["fg"]}
          for state in ("hover", "selected")),
        # panels: find, replace, console and output
        {"class": "panel_control", "layer0.tint": surface["panel"], "layer1.tint": c["border"]},
        {"class": "switch_project_panel_cancel_container", "layer0.tint": surface["panel"]},
        {"class": "label_control", "fg": c["fg"]},
        {"class": "label_control", "parents": [{"class": "status_bar"}], "shadow_color": "transparent"},
        {"class": "vcs_branch_icon", "layer0.tint": c["muted"]},
        {"class": "vcs_changes_annotation", "color": c["muted"], "border_color": c["muted"]},
        {"class": "progress_bar_control", "layer0.tint": c["border"], "layer0.opacity": 1.0},
        {"class": "progress_gauge_control", "layer0.tint": c["red"], "layer0.opacity": 1.0},
        # popups: Goto Anything, the Command Palette, auto-complete, tool tips and dialogs. Matches take ansiBlue,
        # as VS Code's lists do.
        {"class": "overlay_control", "layer0.tint": surface["popup"]},
        {"class": "quick_panel", "layer0.tint": surface["popup"]},
        selected("quick_panel_row", c["selection"]),
        selected("mini_quick_panel_row", c["selection"]),
        label("quick_panel_label", c["fg"], c["ansiBlue"], c["fg"]),
        label("quick_panel_path_label", c["muted"], c["ansiBlue"], c["fg"]),
        {"class": "quick_panel_label hint", "fg": c["muted"], "selected_fg": c["fg"]},
        {"class": "auto_complete", "tint_modifier": surface["popup"]},
        {"class": "auto_complete_detail_pane", "tint_modifier": surface["popup"]},
        selected("table_row", c["selection"]),
        {"class": "tool_tip_control", "layer0.tint": surface["popup"]},
        {"class": "tool_tip_label_control", "fg": c["fg"]},
        {"class": "dialog", "layer0.tint": surface["popup"]},
        {"class": "title_label_control", "fg": c["fg"]},
        {"class": "link_label", "fg": c["azure"]},
    ]
    # Adaptive dims inactive panes and text inputs towards its own tab bar colour; dim them towards the frame.
    dim = f"blend({surface['tabs']} 70%)"
    variables = {f"{kind}_{tone}_modifier": dim for kind, tones in (
        ("sheet", ("dark", "medium_dark", "medium", "light")), ("text_widget", ("dark", "light"))) for tone in tones}
    return {"extends": "Adaptive.sublime-theme", "variables": variables, "rules": rules}


def widget_settings():
    """The theme's Widget - <name>.sublime-settings, which Sublime Text reads for the text inputs of the theme of
    that name: Adaptive's own."""
    return {"draw_shadows": False}
