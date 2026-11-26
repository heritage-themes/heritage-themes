"""yazi flavor generated from a palette: a <name>.yazi folder with flavor.toml, the styles of yazi's interface, and
tmtheme.xml, the TextMate theme that yazi highlights code previews with. yazi reads a flavor from its flavors folder
when theme.toml names it as the dark or the light flavor, and picks one of the two by the terminal's background.

yazi draws on the terminal's own background, and its pop-ups clear their area to it, so the flavor sets no background of
its own and reads as intended in a terminal that runs the matching theme of the Terminals product, whose ANSI colours it
takes where yazi's default theme takes the terminal's. Files take the colours that the Neovim and Helix targets give a
file browser, except folders: executables ansiGreen, images ansiYellow, audio and video ansiMagenta, archives ansiRed,
documents ansiCyan, broken links ansiRed, and other files the text colour. Folders, their icons and the current folder's
path take the flavor's accent, and folder names are bold, as ls draws them, which sets them apart from a file type of a
similar hue. The accent is a syntax role that accent() picks, so that each family shows its own colours: the ANSI
colours of most palettes are close to the standard terminal hues and alike across families. The icons that yazi draws by
a file's kind, and the icons of its named folders, take the same colours. The icons of file types keep their hue: each
takes the colour of ICON_ROLES nearest to its colour in yazi's default theme, the dark one for a dark palette and the
light one for a light palette, as yazi's default colours fail 3:1 on several palettes.

The hovered file takes selection, and the hovered row of the parent folder selInactive, as a selected row does in every
target; so do the selected entry of every list and the selected text of the input. Modes take bg on a colour, as the
mode names of the Helix target do: normal the accent, select ansiMagenta and unset ansiRed, and the second segment of
each mode the colour on selInactive. Pop-up borders and titles, and the tabs, take the accent. Separators take border,
and text that only frames other text takes muted. A task's progress bar fills in ansiGreen, or ansiRed when the task
failed, on selInactive, and its label takes no colour: yazi draws it in the bar's colours swapped over the filled part,
as its default theme does.

yazi.json holds what the flavor takes from yazi's default themes: the keys of their styles, their file type rules and
their icons. scripts/yazi/preset.py writes it from a yazi release.
"""
import json, os

from .colour import contrast, distance
from .nvim import name  # noqa: F401 - a flavor is named as Neovim names a scheme
from .textmate import rules  # noqa: F401 - the build checks the code preview against them
from . import textmate

with open(os.path.join(os.path.dirname(__file__), "yazi.json"), encoding="utf-8") as f:
    PRESET = json.load(f)
VERSION = PRESET["version"]
# The attributes of a style that yazi reads besides fg and bg, from yazi-binding's StyleFlat.
MODIFIERS = ("bold", "dim", "italic", "underline", "blink", "blink_rapid", "reversed", "hidden", "crossed")
# The roles that the flavor's accent chooses from, in order: the palette's syntax roles, led by keyword, then ansiBlue,
# which every palette holds on its rows. The accent is the first that suits; see accent().
ACCENTS = ("keyword", "type", "method", "string", "constant", "field", "number", "label", "call", "directive",
           "typeParam", "annotation", "ansiBlue")
# The least CIE76 distance between the accent and the text colour, so that folders stand apart from other files.
ACCENT_DISTANCE = 25
# The roles that the icons of file types choose from: the ANSI colours and the two text colours.
ICON_ROLES = ("ansiRed", "ansiGreen", "ansiYellow", "ansiBlue", "ansiMagenta", "ansiCyan", "fg", "muted")
# The style of each file type rule of yazi's default themes, in their order, as palette roles; the first rule that
# matches a file styles its name. The flavor's rules replace the default ones, so they keep each of them, and add one
# for other files.
FILETYPES = (dict(fg="ansiYellow"), dict(fg="ansiMagenta"), dict(fg="ansiRed"), dict(fg="ansiCyan"), dict(fg="muted"),
             dict(fg="ansiRed"), dict(fg="ansiGreen"), dict(fg="ansiRed"), dict(fg="ansiRed"), dict(fg="accent", bold=True))
OTHER_FILES = ({"url": "*"}, dict(fg="fg"))
# The role of the icon of each kind of file that yazi's default themes draw by kind (conds). Orphaned links and missing
# files take ansiRed, as their names do; links muted, as their target is shown after the name; devices, pipes, sockets
# and sticky folders ansiYellow, as yazi's default themes draw them yellow.
CONDS = {"orphan": "ansiRed", "link": "muted", "block": "ansiYellow", "char": "ansiYellow", "fifo": "ansiYellow",
         "sock": "ansiYellow", "sticky": "ansiYellow", "dummy": "ansiRed", "dir & hovered": "accent",
         "dir": "accent", "exec": "ansiGreen", "!dir": "fg"}


def settings(p):
    """Section → key → style, a dict of fg and bg as palette roles and of modifiers as True."""
    def on(colour, **modifiers):
        """Text in bg on colour, as a mode name or a count is drawn."""
        return dict(fg="bg", bg=colour, **modifiers)
    def selected(**modifiers):
        return dict(fg="fg", bg="selection", **modifiers)
    def mode(colour):
        return {"main": on(colour, bold=True), "alt": dict(fg=colour, bg="selInactive")}
    modes = {name: mode(colour) for name, colour in (("normal", "accent"), ("select", "ansiMagenta"),
                                                    ("unset", "ansiRed"))}
    border = dict(fg="accent")
    return {
        "app": {"overall": {}},
        "mgr": {
            "cwd": dict(fg="accent", bold=True),
            "find_keyword": dict(fg="ansiYellow", bold=True, italic=True, underline=True),
            "find_position": dict(fg="ansiMagenta", bold=True, italic=True),
            "symlink_target": dict(italic=True),
            "marker_copied": dict(fg="ansiGreen", bg="ansiGreen"), "marker_cut": dict(fg="ansiRed", bg="ansiRed"),
            "marker_marked": dict(fg="ansiCyan", bg="ansiCyan"),
            "marker_selected": dict(fg="ansiYellow", bg="ansiYellow"),
            "count_copied": on("ansiGreen"), "count_cut": on("ansiRed"), "count_selected": on("ansiYellow"),
            "border_style": dict(fg="border"),
        },
        "tabs": {"active": on("accent", bold=True), "inactive": dict(fg="accent", bg="selInactive")},
        "mode": {f"{name}_{part}": style for name, parts in modes.items() for part, style in parts.items()},
        "indicator": {"parent": dict(bg="selInactive"), "current": dict(bg="selection"),
                      "preview": dict(underline=True)},
        "status": {
            "overall": {}, "perm_sep": dict(fg="muted"), "perm_type": dict(fg="ansiGreen"),
            "perm_read": dict(fg="ansiYellow"), "perm_write": dict(fg="ansiRed"), "perm_exec": dict(fg="ansiCyan"),
            "progress_label": dict(bold=True), "progress_normal": dict(fg="ansiGreen", bg="selInactive"),
            "progress_error": dict(fg="ansiRed", bg="selInactive"),
        },
        "which": {"border": border, "mask": {}, "cand": dict(fg="ansiCyan"), "rest": dict(fg="muted"),
                  "desc": dict(fg="ansiMagenta"), "separator_style": dict(fg="muted")},
        "confirm": {"border": border, "title": border, "body": {}, "list": {}, "btn_yes": selected(bold=True),
                    "btn_no": {}},
        "spot": {"border": border, "title": border, "tbl_col": dict(fg="accent"), "tbl_cell": selected()},
        "notify": {"title_info": dict(fg="ansiGreen"), "title_warn": dict(fg="ansiYellow"),
                   "title_error": dict(fg="ansiRed")},
        "pick": {"border": border, "active": selected(bold=True), "inactive": {}},
        "input": {"border": border, "title": {}, "value": {}, "selected": selected()},
        "cmp": {"border": border, "active": selected(), "inactive": {}},
        "tasks": {"border": border, "title": {}, "hovered": selected(bold=True)},
        "help": {"border": border, "chord": dict(fg="ansiCyan"), "action": {}, "hovered": selected(bold=True)},
    }


def accent(p):
    """The palette role of the flavor's accent: the first of ACCENTS that reads at 4.5:1 on bg, selection and
    selInactive, holds bg at 4.5:1 on it, and stands apart from the text colour."""
    def fits(role):
        return (min(contrast(p[role], p[bg]) for bg in ("bg", "selection", "selInactive")) >= 4.5
                and contrast(p["bg"], p[role]) >= 4.5 and distance(p[role], p["fg"]) >= ACCENT_DISTANCE)
    role = next((role for role in ACCENTS if fits(role)), None)
    if role is None:
        raise ValueError(f"{p['name']}: no role of ACCENTS suits yazi's accent")
    return role


def colours(p):
    """Each palette role as #RRGGBB, and accent as the colour of the flavor's accent."""
    c = {role: "#" + value for role, value in p.items() if isinstance(value, str) and len(value) == 6}
    return c | {"accent": c[accent(p)]}


def resolve(p, style):
    """A style with its roles as #RRGGBB."""
    c = colours(p)
    return {k: c[v] if k in ("fg", "bg") else v for k, v in style.items()}


def filetypes(p):
    """The rules of [filetype]: yazi's default selectors with the flavor's styles, then the rule for other files."""
    return [dict(selector, **resolve(p, style))
            for selector, style in [*zip(PRESET["filetype"], FILETYPES, strict=True), OTHER_FILES]]


def icon_role(p, colour):
    """The role of ICON_ROLES nearest to an icon's colour in yazi's default theme, #RRGGBB."""
    return min(ICON_ROLES, key=lambda role: distance(p[role], colour[1:]))


def icons(p):
    """The [icon] lists that the flavor puts before yazi's own, each icon of yazi's default themes with its colour."""
    mode, c = "dark" if p["dark"] else "light", colours(p)
    def role(kind, icon):
        if kind == "conds":
            return CONDS[icon["if"]]
        return "accent" if kind == "dirs" else icon_role(p, icon[mode])
    return {f"prepend_{kind}": [{k: v for k, v in icon.items() if k not in ("dark", "light")}
                                | {"fg": c[role(kind, icon)]} for icon in found]
            for kind, found in PRESET["icon"].items() if found}


def toml(value):
    """A TOML literal for a string, a bool, an inline table of them, or a list of inline tables."""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=False)
    if isinstance(value, list):
        return "[\n" + "".join(f"\t{toml(v)},\n" for v in value) + "]"
    return "{ " + ", ".join(f"{k} = {toml(v)}" for k, v in value.items()) + " }" if value else "{}"


def flavor(p, source):
    """The flavor.toml of a palette. source is the URL of the theme folder."""
    lines = [f"# {p['name']}: a Heritage Themes flavor for yazi.",
             f"# Generated from {source}; changes here are overwritten."]
    for section, styles in settings(p).items():
        lines += ["", f"[{section}]", *(f"{key} = {toml(resolve(p, style))}" for key, style in styles.items())]
    lines += ["", "[filetype]", f"rules = {toml(filetypes(p))}", "", "[icon]",
              *(f"{key} = {toml(value)}" for key, value in icons(p).items())]
    return "\n".join(lines) + "\n"


def styles(p):
    """(element, fg, bg, minimum contrast) for the build's contrast check, as #RRGGBB: text at 4.5:1 and graphics at 3:1
    on the background that yazi draws them on. Without a bg of its own, a style stands on the terminal's background,
    bg, and so do pop-ups, which clear their area to it. A row's text and icon also stand on the hovered row's
    background, selection in the current folder and selInactive in the parent. Separators are left out; markers and
    icons are graphics, and code comments and the names of files that a remote file system no longer has are dimmed
    text, all held to 3:1."""
    c = colours(p)
    out = []
    def check(element, fg, backgrounds, minimum=4.5):
        out.extend((element, fg, bg, minimum) for bg in backgrounds)
    on_row = (c["bg"], c["selection"], c["selInactive"])
    graphics = {("mgr", key) for key in ("marker_copied", "marker_cut", "marker_marked", "marker_selected")}
    # text on its own background, or on the hovered row where yazi draws it there: matches of a find, and the keys of
    # the help menu
    on_hover = {("mgr", "find_keyword"): on_row, ("mgr", "find_position"): on_row, ("help", "chord"): on_row[:2]}
    for section, keys in settings(p).items():
        for key, style in keys.items():
            if "fg" not in style or (section, key) == ("mgr", "border_style"):
                continue
            fg = c[style["fg"]]
            if (section, key) in graphics:
                check(f"{section}.{key}", fg, (c["bg"],), 3)
            elif "bg" in style:
                check(f"{section}.{key}", fg, (c[style["bg"]],))
                if section == "status" and key.startswith("progress_"):
                    check(f"{section}.progress_label on {key}", c[style["bg"]], (fg,))
            else:
                check(f"{section}.{key}", fg, on_hover.get((section, key), (c["bg"],)))
    # files that a remote file system no longer has are dimmed, as comments are, and held to 3:1
    for rule in filetypes(p):
        check(f"filetype {rule.get('mime') or rule['url']}{' ' + rule['is'] if 'is' in rule else ''}", rule["fg"],
              on_row, 3 if rule["fg"] == c["muted"] else 4.5)
    for kind, found in icons(p).items():
        for icon in found:
            check(f"icon {kind} {next(iter(icon.values()))}", icon["fg"], on_row, 3)
    for name, style in textmate.styles(p).items():
        check(f"preview {name}", style["fg"], (style["bg"],), 3 if "comment" in name.split(" (")[0] else 4.5)
    return out


def tmtheme(p, source):
    """The tmtheme.xml of a palette, which yazi colours code previews with. yazi draws only the rules' foregrounds."""
    return textmate.theme(p, source, "yazi", textmate.settings(p))
