"""btop theme generated from a palette: a .theme file of theme[key]="#RRGGBB" lines, which btop lists in its options
when it is in btop's user themes folder.

btop draws on the theme's background, so the theme sets bg and fg. Box titles take fg, and the shortcut letter in each
title takes label, the accent each family gives its labels. The selected process takes selection, as a selected row
does in every target. Box outlines take muted, as lazygit's panel borders do, and the dividers within boxes border, the
palette's colour for separators. Text that btop dims, which is the text of disabled items and, with btop's default
process gradient, the rows of the process list as they get further from the selection, takes comment, the palette's
de-emphasised text, so the dimmest row still reads at 3:1. Graph backgrounds and the empty part of meters take it too,
as btop's own default theme draws them in that colour. Text on graphs takes muted.

Graphs whose colour warns take the terminal colours of the Terminals product, as most TUI apps draw levels: load and
the process list's cpu, memory and thread values from ansiGreen through ansiYellow to ansiRed, temperatures from
ansiBlue through ansiMagenta to ansiRed. Graphs whose colour only tells series apart take the family's syntax colours,
so each tradition shows in them: memory and disk meters in one colour each (used constant, available string, cached
type, free directive), and download keyword and upload call. The build holds the series of each box SERIES_APART
apart. btop draws the steps between a gradient's colours itself; gradient() computes them as btop 1.4 does, so the
build and the preview check them. The banner of the process list and a followed process take bg on an ANSI colour, as
the Terminals product draws highlights: following ansiBlue, paused ansiYellow, and both ansiMagenta.
"""
from .nvim import name  # noqa: F401 - the theme's file is named as Neovim names a scheme

# Every key that btop 1.4 reads from a theme, from Default_theme in src/btop_theme.cpp. btop ignores any other key and
# takes the default theme's colour for a key the file leaves out.
KEYS = ("main_bg", "main_fg", "title", "hi_fg", "selected_bg", "selected_fg", "inactive_fg", "graph_text", "meter_bg",
        "proc_misc", "cpu_box", "mem_box", "net_box", "proc_box", "div_line", "temp_start", "temp_mid", "temp_end",
        "cpu_start", "cpu_mid", "cpu_end", "free_start", "free_mid", "free_end", "cached_start", "cached_mid",
        "cached_end", "available_start", "available_mid", "available_end", "used_start", "used_mid", "used_end",
        "download_start", "download_mid", "download_end", "upload_start", "upload_mid", "upload_end",
        "process_start", "process_mid", "process_end", "proc_pause_bg", "proc_follow_bg", "proc_banner_bg",
        "proc_banner_fg", "followed_bg", "followed_fg")
# The gradients of a theme, which btop draws from their _start, _mid and _end keys.
GRADIENTS = ("temp", "cpu", "free", "cached", "available", "used", "download", "upload", "process")
# The gradients whose colours btop draws as text, held to 4.5:1 rather than the 3:1 of graphics: per-core load and
# temperatures beside the core list, and the process list's values. proc and proc_color, which btop makes from other
# keys, fade the process list towards inactive_fg and are held to its 3:1.
TEXT_GRADIENTS = ("cpu", "temp", "process")
# The gradients drawn side by side in one box, whose colours tell series apart, and the least CIE76 distance between
# any two of them: the memory and disk meters, and the network graphs.
SERIES = (("used", "available", "cached", "free"), ("download", "upload"))
SERIES_APART = 15


def settings(p):
    """btop key → palette role, or None for the _mid and _end of a gradient of one colour, which btop leaves empty."""
    def gradient(*roles):
        return dict(zip(("start", "mid", "end"), (*roles, None, None)))
    gradients = dict(
        temp=gradient("ansiBlue", "ansiMagenta", "ansiRed"),
        cpu=gradient("ansiGreen", "ansiYellow", "ansiRed"),
        free=gradient("directive"), cached=gradient("type"), available=gradient("string"),
        used=gradient("constant"), download=gradient("keyword"), upload=gradient("call"),
        process=gradient("ansiGreen", "ansiYellow", "ansiRed"),
    )
    return {
        "main_bg": "bg", "main_fg": "fg", "title": "fg", "hi_fg": "label",
        "selected_bg": "selection", "selected_fg": "fg",
        "inactive_fg": "comment", "graph_text": "muted", "meter_bg": "comment", "proc_misc": "ansiGreen",
        "cpu_box": "muted", "mem_box": "muted", "net_box": "muted", "proc_box": "muted", "div_line": "border",
        **{f"{g}_{part}": role for g, parts in gradients.items() for part, role in parts.items()},
        "proc_pause_bg": "ansiYellow", "proc_follow_bg": "ansiBlue", "proc_banner_bg": "ansiMagenta",
        "proc_banner_fg": "bg", "followed_bg": "ansiBlue", "followed_fg": "bg",
    }


def colours(p):
    """btop key → #RRGGBB, or "" for an empty _mid or _end."""
    return {key: "#" + p[role] if role else "" for key, role in settings(p).items()}


def theme(p, source):
    """The .theme file for a palette, in KEYS order. source is the URL of the theme folder."""
    c = colours(p)
    lines = [f"# {p['name']}: a Heritage Themes colour theme for btop.",
             f"# Generated from {source}; changes here are overwritten."]
    lines += [f'theme[{key}]="{c[key]}"' for key in KEYS]
    return "\n".join(lines) + "\n"


def gradient(start, mid, end):
    """The 101 colours, as #RRGGBB, of a btop gradient from #RRGGBB colours, mid and end "" when unset, computed as
    generateGradients in btop 1.4's src/btop_theme.cpp does: integer steps from start to mid and from mid to end, or
    from start to end without mid, and start alone without end."""
    if not end:
        return [start.upper()] * 101
    stops = [[int(c[i:i + 2], 16) for i in (1, 3, 5)] if c else None for c in (start, mid, end)]
    span = 50 if stops[1] else 100
    result = [[0, 0, 0] for _ in range(101)]
    for channel in range(3):
        first, last, offset = 0, 1 if span == 50 else 2, 0
        for i in range(101):
            # C++ integer division truncates towards zero
            delta = (i - offset) * (stops[last][channel] - stops[first][channel])
            result[i][channel] = stops[first][channel] + int(delta / span)
            if i == span:
                first, last, offset = first + 1, last + 1, 50
    return ["#%02X%02X%02X" % tuple(rgb) for rgb in result]


def gradients(p):
    """Gradient name → its 101 colours, for each gradient that btop draws: those of GRADIENTS, and proc and
    proc_color, which btop makes from main_fg, inactive_fg and process_start for the process list."""
    c = colours(p)
    result = {g: gradient(c[f"{g}_start"], c[f"{g}_mid"], c[f"{g}_end"]) for g in GRADIENTS}
    result["proc"] = gradient(c["main_fg"], "", c["inactive_fg"])
    result["proc_color"] = gradient(c["inactive_fg"], "", c["process_start"])
    return result


def styles(p):
    """(element, foreground, background, minimum contrast) for the build's check: text at 4.5:1, dimmed text and
    graphics at 3:1, and every step of every gradient on bg, at 4.5:1 for those of TEXT_GRADIENTS."""
    c = colours(p)
    bg = c["main_bg"]
    pairs = [("text", c["main_fg"], bg, 4.5), ("box title", c["title"], bg, 4.5),
             ("shortcut letter", c["hi_fg"], bg, 4.5), ("selected process", c["selected_fg"], c["selected_bg"], 4.5),
             ("text on graphs", c["graph_text"], bg, 4.5), ("dimmed text", c["inactive_fg"], bg, 3),
             ("empty meter", c["meter_bg"], bg, 3), ("process details", c["proc_misc"], bg, 4.5),
             *((f"{key} outline", c[key], bg, 3) for key in ("cpu_box", "mem_box", "net_box", "proc_box")),
             *((f"banner on {key}", c["proc_banner_fg"], c[key], 4.5)
               for key in ("proc_pause_bg", "proc_follow_bg", "proc_banner_bg")),
             ("followed process", c["followed_fg"], c["followed_bg"], 4.5)]
    for name, colours_ in gradients(p).items():
        minimum = 4.5 if name in TEXT_GRADIENTS else 3
        pairs += [(f"{name} gradient step {i}", colour, bg, minimum) for i, colour in enumerate(colours_)]
    return pairs
