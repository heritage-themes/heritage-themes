"""eza theme generated from a palette: a theme.yml file, which eza reads from its configuration folder, or from the folder
that EZA_CONFIG_DIR names.

eza draws on the terminal's own background, so the theme sets no background except where eza's default theme fills one,
and reads as intended in a terminal that runs the matching theme of the Terminals product. The theme keeps the look of
eza's default theme and takes each of its colours from the palette: where eza's default takes one of the terminal's
ANSI colours, the theme takes the palette's ANSI role of that colour, which the Terminals theme gives the terminal too.
Two exceptions give each family its own colours, as the ANSI colours of most palettes are close to the standard
terminal hues and alike across families: folders and mount points take the accent, the syntax role that
heritage.yazi.accent() picks for a file browser's folders, and dates take a second syntax role, which date() picks to
stand apart from the accent, the text colour and the colours of the users and sizes beside the dates. The accent is
often one of the palette's ANSI colours, so folder names are the only bold file names, as in the yazi flavors: eza's
default theme also draws executables, source files, keys, video, lossless audio, build files and devices bold, and the
theme draws them regular, so that a folder stands apart from a file of the same hue. Text that eza's
default theme draws dimmed or in dark grey, such as punctuation, ignored files and the colons of a security context,
takes muted, the palette's secondary text, as terminals draw dimmed and dark grey text differently. A file with more
than one hard link has its link count in bg on ansiYellow, where eza's default draws red on yellow.

Every style sets bold, dimmed and underline, because eza applies the theme on top of its default theme and keeps each
attribute that a style leaves out. Styles that eza's default theme draws in the terminal's text colour, such as the
names of plain files, set no colour.

eza ignores the whole file when it is not valid YAML or a value has the wrong type, and ignores keys it does not know,
so the theme keeps to the keys of KEYS. eza applies LS_COLORS and EZA_COLORS over the theme, so the theme applies only
where neither is set.
"""
from .colour import contrast, distance
from .fzf import POINTERS
from .nvim import name  # noqa: F401 - the theme's file is named as Neovim names a scheme
from .yazi import accent

# The first release that reads a theme file, whose keys and colour values are those of the tested one, and the one the
# previews run.
MINIMUM_VERSION, TESTED_VERSION = "0.19.2", "0.23.5"
# The keys of eza's theme file, from UiStylesOverride and the structs it holds in src/options/config.rs of eza 0.23.5,
# in their order: a section → its keys, or None for a key that holds a style. filenames and extensions, which map
# names to styles and icons, are left out, as the theme sets none.
KEYS = {
    "filekinds": ("normal", "directory", "symlink", "pipe", "block_device", "char_device", "socket", "special",
                  "executable", "mount_point"),
    "perms": ("user_read", "user_write", "user_execute_file", "user_execute_other", "group_read", "group_write",
              "group_execute", "other_read", "other_write", "other_execute", "special_user_file", "special_other",
              "attribute"),
    "size": ("major", "minor", "number_byte", "number_kilo", "number_mega", "number_giga", "number_huge", "unit_byte",
             "unit_kilo", "unit_mega", "unit_giga", "unit_huge"),
    "users": ("user_you", "user_root", "user_other", "group_yours", "group_other", "group_root"),
    "links": ("normal", "multi_link_file"),
    "git": ("new", "modified", "deleted", "renamed", "typechange", "ignored", "conflicted"),
    "git_repo": ("branch_main", "branch_other", "git_clean", "git_dirty"),
    "security_context": {"none": None, "selinux": ("colon", "user", "role", "typ", "range")},
    "file_type": ("image", "video", "music", "lossless", "crypto", "document", "compressed", "temp", "compiled",
                  "build", "source"),
    "punctuation": None, "date": None, "inode": None, "blocks": None, "header": None, "octal": None, "flags": None,
    "symlink_path": None, "control_char": None, "broken_symlink": None, "broken_path_overlay": None,
}
# The attributes that every style sets: those that eza's default theme uses, which a style would otherwise keep.
ATTRIBUTES = ("bold", "dimmed", "underline")
# The least CIE76 distance between the colour of dates and the accent, the text colour, ansiYellow, which eza draws
# your user and group in, and ansiGreen, which it draws small sizes in.
DATE_DISTANCE = 25


def date(p):
    """The palette role of dates: the first of fzf's POINTERS that reads at 4.5:1 on bg and stands DATE_DISTANCE
    apart from the accent, the text colour, ansiYellow and ansiGreen. A palette with no such role, one that builds its
    hierarchy from tone rather than hue, takes the accent."""
    taken = (p[accent(p)], p["fg"], p["ansiYellow"], p["ansiGreen"])
    def fits(role):
        return (role in p and contrast(p[role], p["bg"]) >= 4.5
                and all(distance(p[role], colour) >= DATE_DISTANCE for colour in taken))
    return next((role for role in POINTERS if fits(role)), accent(p))


def settings(p):
    """Section → key → style, or key → style for a key that holds one, in the order of KEYS. A style is a dict of fg
    and bg as palette roles and of attributes as True; eza's default theme gives each its colours and attributes."""
    def s(fg=None, **attributes):
        return ({"fg": fg} if fg else {}) | attributes
    folder = accent(p)
    return {
        "filekinds": {
            "normal": s(), "directory": s(folder, bold=True), "symlink": s("ansiCyan"), "pipe": s("ansiYellow"),
            "block_device": s("ansiYellow"), "char_device": s("ansiYellow"), "socket": s("ansiRed"),
            "special": s("ansiYellow"), "executable": s("ansiGreen"),
            "mount_point": s(folder, bold=True, underline=True),
        },
        "perms": {
            "user_read": s("ansiYellow", bold=True), "user_write": s("ansiRed", bold=True),
            "user_execute_file": s("ansiGreen", bold=True, underline=True),
            "user_execute_other": s("ansiGreen", bold=True),
            "group_read": s("ansiYellow"), "group_write": s("ansiRed"), "group_execute": s("ansiGreen"),
            "other_read": s("ansiYellow"), "other_write": s("ansiRed"), "other_execute": s("ansiGreen"),
            "special_user_file": s("ansiMagenta"), "special_other": s("ansiMagenta"), "attribute": s(),
        },
        "size": {
            "major": s("ansiGreen", bold=True), "minor": s("ansiGreen"),
            "number_byte": s("ansiGreen"), "number_kilo": s("ansiGreen", bold=True), "number_mega": s("ansiYellow"),
            "number_giga": s("ansiRed"), "number_huge": s("ansiMagenta"),
            "unit_byte": s("ansiGreen"), "unit_kilo": s("ansiGreen", bold=True), "unit_mega": s("ansiYellow"),
            "unit_giga": s("ansiRed"), "unit_huge": s("ansiMagenta"),
        },
        "users": {
            "user_you": s("ansiYellow", bold=True), "user_root": s(), "user_other": s(),
            "group_yours": s("ansiYellow", bold=True), "group_other": s(), "group_root": s(),
        },
        "links": {"normal": s("ansiRed", bold=True), "multi_link_file": s("bg") | {"bg": "ansiYellow"}},
        "git": {
            "new": s("ansiGreen"), "modified": s("ansiBlue"), "deleted": s("ansiRed"), "renamed": s("ansiYellow"),
            "typechange": s("ansiMagenta"), "ignored": s("muted"), "conflicted": s("ansiRed"),
        },
        "git_repo": {"branch_main": s("ansiGreen"), "branch_other": s("ansiYellow"), "git_clean": s("ansiGreen"),
                     "git_dirty": s("ansiYellow", bold=True)},
        "security_context": {
            "none": s(),
            "selinux": {"colon": s("muted"), "user": s("ansiBlue"), "role": s("ansiGreen"), "typ": s("ansiYellow"),
                        "range": s("ansiCyan")},
        },
        "file_type": {
            "image": s("ansiMagenta"), "video": s("ansiMagenta"), "music": s("ansiCyan"), "lossless": s("ansiCyan"),
            "crypto": s("ansiGreen"), "document": s("ansiGreen"), "compressed": s("ansiRed"), "temp": s("muted"),
            "compiled": s("ansiYellow"), "build": s("ansiYellow", underline=True), "source": s("ansiYellow"),
        },
        "punctuation": s("muted", bold=True), "date": s(date(p)), "inode": s("ansiMagenta"), "blocks": s("ansiCyan"),
        "header": s(underline=True), "octal": s("ansiMagenta"), "flags": s(),
        "symlink_path": s("ansiCyan"), "control_char": s("ansiRed"), "broken_symlink": s("ansiRed"),
        "broken_path_overlay": s(underline=True),
    }


def entries(p):
    """((section, ..., key), style) for every style of settings(), in order."""
    def walk(path, value):
        if any(isinstance(v, dict) for v in value.values()):
            for key, inner in value.items():
                yield from walk((*path, key), inner)
        else:
            yield path, value
    return list(walk((), settings(p)))


def resolve(p, style):
    """eza's fields of a style: foreground and background as #RRGGBB, and is_bold, is_dimmed and is_underline."""
    fields = {field: "#" + p[style[key]] for key, field in (("fg", "foreground"), ("bg", "background"))
              if key in style}
    return fields | {f"is_{a}": style.get(a, False) for a in ATTRIBUTES}


def flow(fields):
    """A YAML flow mapping of a style's fields. Colours are quoted, as YAML reads an unquoted # as a comment."""
    return "{ " + ", ".join(f'{k}: "{v}"' if isinstance(v, str) else f"{k}: {str(v).lower()}"
                            for k, v in fields.items()) + " }"


def theme(p, source):
    """The themes/<theme>.yml file for a palette, which the user links to as theme.yml. source is the URL of the theme
    folder."""
    lines = [f"# {p['name']}: {source}",
             f"# For a terminal with a {'dark' if p['dark'] else 'light'} background; needs eza {MINIMUM_VERSION} or "
             "later.", "colourful: true"]
    opened = ()
    for path, style in entries(p):
        for depth, section in enumerate(path[:-1]):
            if opened[:depth + 1] != path[:depth + 1]:
                lines += [""] * (depth == 0) + [f"{'  ' * depth}{section}:"]
        if len(path) == 1 and len(opened) > 1:
            lines.append("")
        opened = path
        lines.append(f"{'  ' * (len(path) - 1)}{path[-1]}: {flow(resolve(p, style))}")
    return "\n".join(lines) + "\n"


def styles(p):
    """(element, foreground, background, minimum contrast) as #RRGGBB, for the build's check: text at 4.5:1 on the
    terminal's background, which is bg in the matching Terminals theme, or on the background a style sets. A style
    with no colour of its own draws in the terminal's text colour."""
    out = []
    for path, style in entries(p):
        fg, bg = p[style.get("fg", "fg")], p[style.get("bg", "bg")]
        out.append((".".join(path), "#" + fg, "#" + bg, 4.5))
    return out
