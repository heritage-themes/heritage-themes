"""Godot editor themes generated from a palette: a text editor theme (.tet) for each Heritage theme, and the colours
that an editor plugin gives Godot to draw the rest of the editor from.

Godot draws its editor from three settings: a base colour, an accent colour and a contrast. It derives every panel,
button, tab and popup from the base colour by darkening it by multiples of the contrast, and its text and icons are
white or black with transparency. The Modern style that Godot uses by default draws the docks on the base colour, the
window behind them and the tab bars on the colour it calls surface_lowest, which is the base colour's HSV value lerped
towards black by 1.7 times the contrast, and the script editor on the background colour of the text editor theme. A
dark theme takes `surface` as the base colour and a light theme `bgUi`, and the contrast is the one that makes
surface_lowest as bright as `bgUi` in a dark theme and `bg` in a light one, so the window and the tab bars sit on the
palette's own background. A light theme's contrast is negative, as in Godot's own light presets, so that the lower
surfaces are lighter than the base colour. The accent colour is `gold`, the focus colour of the other targets.

The script editor takes its colours from a text editor theme: a ConfigFile with one `[color_theme]` section of
`text_editor/theme/highlighting/` settings without that prefix. Godot loads the theme that
`text_editor/theme/color_theme` names from the text_editor_themes folder of its configuration folder. The roles are
those that heritage.vscode gives the scopes of Godot's own GDScript grammar for VS Code: node paths, `$Node`
references and StringNames are escapes there and take `gold`, as format placeholders do, and the built-in types such
as `int` and `Vector2` take `type`. Godot has no bold or italic in the script editor. Godot draws selected text in
`text_selected_color` unless it is transparent, and it is, so that the selection keeps the code's colours.
"""
import re

from .sublime import basename
from .vscode import mix

PREFIX = "Heritage "  # a theme's name in Godot's list, so that the themes sit together among a user's own
FOLDER = "heritage_themes"  # the plugin's folder in a project's addons folder
HEX = re.compile(r"[0-9a-f]{6}([0-9a-f]{2})?")
TRANSPARENT = "00000000"
# The share of the contrast by which Godot's Modern style darkens the base colour into surface_lowest.
LOWEST = 1.7
# interface/theme/icon_and_font_color: Godot's names are for the colour of the icons and the text.
ICONS_LIGHT, ICONS_DARK = 2, 1

# Setting under text_editor/theme/highlighting/ → palette role. With MIXES and text_selected_color, these are every
# colour setting there in Godot 4.6 and 4.7; scripts/godot/settings.py checks them against an installed Godot.
ROLES = {
    "background_color": "bg",
    "text_color": "fg",
    "symbol_color": "op",
    "keyword_color": "keyword",
    "control_flow_keyword_color": "keyword",
    "base_type_color": "type",
    "engine_type_color": "type",
    "user_type_color": "type",
    "comment_color": "comment",
    "doc_comment_color": "doc",
    "string_color": "string",
    "string_placeholder_color": "gold",
    "number_color": "number",
    "function_color": "call",
    "member_variable_color": "field",
    "gdscript/function_definition_color": "method",
    "gdscript/global_function_color": "call",
    "gdscript/node_path_color": "gold",
    "gdscript/node_reference_color": "gold",
    "gdscript/string_name_color": "gold",
    "gdscript/annotation_color": "annotation",
    # the tags in comments: ALERT and the like, TODO and the like, NOTE and the like
    "comment_markers/critical_color": "ansiRed",
    "comment_markers/warning_color": "todo",
    "comment_markers/notice_color": "docTag",
    "caret_color": "caret",
    "caret_background_color": "bg",  # the text under a block caret
    "current_line_color": "caretRow",
    "selection_color": "selection",
    "word_highlighted_color": "underCaret",
    "search_result_color": "searchBg",
    "search_result_border_color": "searchBorder",
    "brace_mismatch_color": "ansiRed",  # the text of a bracket without its pair, as error text in the other targets
    "line_number_color": "lineNo",
    "line_length_guideline_color": "guide",
    "code_folding_color": "muted",
    "folded_code_region_color": "selInactive",
    "mark_color": "diffDel",  # a line with an error
    "warning_color": "diffConf",  # a line with a warning
    "bookmark_color": "azure",
    "breakpoint_color": "error",
    "executing_line_color": "warning",  # the line that the debugger stops on
    "completion_background_color": "surface",
    "completion_font_color": "fg",
    "completion_selected_color": "selection",
    # the letters of each suggestion that match the typed ones, a box the height of the row, so a quiet colour
    "completion_existing_color": "selInactive",
    "completion_scroll_color": "guideSel",
    "completion_scroll_hovered_color": "muted",
}
# Settings between two roles: setting → (role, role, share of the second). Godot marks almost every line whose types
# its parser checked, blank ones too, so their numbers keep the line number colour with a tint of the added colour, as
# Godot's own themes tint them green.
MIXES = {"safe_line_number_color": ("lineNo", "added", 0.5)}
# The settings whose text needs 3:1 only: comments, as in every target, and the caret, a shape.
LOW_CONTRAST = {"comment_color", "caret_color"}
# Text that no contrast is required of: line numbers, as in every target, and the fold arrows, which are icons.
DECORATIVE = {"line_number_color", "safe_line_number_color", "code_folding_color"}
# Text drawn on a background other than background_color and current_line_color: setting → background settings.
DRAWN_ON = {
    "completion_font_color": ("completion_background_color", "completion_selected_color",
                              "completion_existing_color"),
}
# Backgrounds that Godot draws plain text on, beside background_color and current_line_color.
TEXT_BACKGROUNDS = ("selection_color", "word_highlighted_color", "search_result_color", "folded_code_region_color",
                    "mark_color", "warning_color")
# Settings that are not text drawn on the editor's background.
NOT_TEXT = {"background_color", "caret_background_color", "current_line_color", "search_result_border_color",
            "line_length_guideline_color", "completion_background_color", "completion_selected_color",
            "completion_existing_color", "completion_scroll_color", "completion_scroll_hovered_color",
            "bookmark_color", "breakpoint_color", "executing_line_color", *TEXT_BACKGROUNDS}


def name(t):
    """The name of a theme dict from a theme.py in Godot's list, for example "Heritage Holi Night (Dark)". It is the
    .tet file's name too."""
    return PREFIX + basename(t["palette"]["name"])


def colour(p, role):
    """The rrggbb of a palette role, in lower case as Godot writes it. The caret falls back to gold, as in the other
    products."""
    return (p.get("caret", p["gold"]) if role == "caret" else p[role]).lower()


def colours(p):
    """Setting → rrggbb or rrggbbaa of a text editor theme."""
    mixed = {key: mix(p[a], p[b], t).lower() for key, (a, b, t) in MIXES.items()}
    return {**{key: colour(p, role) for key, role in ROLES.items()}, **mixed, "text_selected_color": TRANSPARENT}


def text_editor_theme(p, theme_name, source):
    """The .tet file for a palette. source is the URL of the theme folder."""
    lines = [f"; {theme_name}: a Heritage Themes text editor theme for Godot.",
             f"; Generated from {source}; changes here are overwritten.",
             "[color_theme]", ""]
    lines += [f'{key}="{value}"' for key, value in sorted(colours(p).items())]
    return "\n".join(lines) + "\n"


def value(hex_colour):
    """The HSV value of an rrggbb colour, as Godot's Color.get_v gives it."""
    return max(int(hex_colour[i:i + 2], 16) for i in (0, 2, 4)) / 255


def interface(p):
    """The base colour, accent colour and contrast that Godot draws the editor from, and the colour of its icons and
    text, as dict(base_color, accent_color, contrast, icon_and_font_color)."""
    base, lowest = ("surface", "bgUi") if p["dark"] else ("bgUi", "bg")
    return dict(base_color=colour(p, base), accent_color=colour(p, "gold"),
                contrast=round((1 - value(p[lowest]) / value(p[base])) / LOWEST, 2),
                icon_and_font_color=ICONS_LIGHT if p["dark"] else ICONS_DARK)


def themes_config(themes):
    """The plugin's themes.cfg: a section for each (name, palette) with the settings of interface()."""
    lines = ["; The editor colours of each Heritage theme: Godot's interface/theme/ settings.",
             "; Generated by Heritage Themes; changes here are overwritten."]
    for theme_name, p in themes:
        lines += ["", f"[{theme_name}]", ""]
        for key, setting in interface(p).items():
            lines.append(f'{key}="{setting}"' if isinstance(setting, str) else f"{key}={setting}")
    return "\n".join(lines) + "\n"


def plugin_config(version, description):
    """The plugin.cfg that Godot lists the plugin by."""
    return (f'[plugin]\n\nname="Heritage Themes"\ndescription="{description}"\nauthor="Heritage Themes"\n'
            f'version="{version}"\nscript="heritage_themes.gd"\n')


def parse(text):
    """section → {key: value} of a ConfigFile as Godot writes it: comments start with a semicolon, strings are quoted,
    and other values are numbers."""
    sections, current = {}, None
    for line in text.splitlines():
        if not line or line.startswith(";"):
            continue
        if header := re.fullmatch(r"\[([^\]]+)\]", line):
            current = sections.setdefault(header[1], {})
            continue
        key, raw = re.fullmatch(r"([A-Za-z0-9_/]+)=(.*)", line).groups()
        if raw.startswith('"'):
            parsed = re.fullmatch(r'"([^"\\]*)"', raw)[1]
        else:
            parsed = float(raw) if "." in raw else int(raw)
        current[key] = parsed
    return sections


def styles(p):
    """setting → dict(fg, bg) as #rrggbb for the build's contrast check: each text colour on each background that
    Godot draws it on, and plain text on the backgrounds of TEXT_BACKGROUNDS."""
    c = colours(p)
    out = {}
    for key, text in c.items():
        if key in NOT_TEXT or key == "text_selected_color":
            continue
        for background in DRAWN_ON.get(key, ("background_color", "current_line_color")):
            out[f"{key} on {background}"] = dict(fg="#" + text, bg="#" + c[background])
    for background in TEXT_BACKGROUNDS:
        out[f"text_color on {background}"] = dict(fg="#" + c["text_color"], bg="#" + c[background])
    return out


def low_contrast():
    """The keys of styles() that need 3:1 only."""
    return {f"{key} on {background}" for key in LOW_CONTRAST for background in ("background_color",
                                                                              "current_line_color")}


def decorative():
    """The keys of styles() that no contrast is required of."""
    return {f"{key} on {background}" for key in DECORATIVE for background in ("background_color",
                                                                           "current_line_color")}
