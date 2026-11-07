"""Terminals: themes for terminal emulators, shells, multiplexers and prompts, generated from a palette.

Every app takes its colours from colours(), so a theme looks the same in each of them and in the terminals of the
other targets: the 16 ANSI colours as the Zed, VS Code and Neovim themes give them, on the editor's bg, with the caret
as the cursor and the editor's selection. Tab bars, status lines and borders follow the Islands layout of the other
targets: bars on the frame, the active tab on bg.

Each module in this package writes one app's files. A module defines:

    APP       the app's name
    FOLDER    the folder in the zip that the app's files go in
    CATEGORY  its section of the README, one of CATEGORIES
    INSTALL   its install instructions in Markdown, with {stem} and {label} for a theme's file name stem and name, and
              {light_stem} and {light_label} for a light theme's
    files(theme, source)  (file name, text) per file of a theme dict from a theme.py, source the URL of its family
    validate(theme, text) raises ValueError when the text that files gave is malformed or differs from the colours
    pairs(p)  (element, text colour, background, minimum contrast) for every text the app draws in the theme's colours

A module that writes several files for a theme defines validate_files(theme, files) in place of validate, with files a
dict of file name to text for the theme's files.

A module whose app reads one file for every theme returns no files from files() and defines combined(themes, source),
which returns that file's (file name, text) for the theme dicts, and validate_combined(themes, files), with files a
dict of file name to text.
"""
import importlib, re

from ..nvim import name as scheme_name, terminal as ansi
from ..vscode import luminance, mix

ANSI_NAMES = ("black", "red", "green", "yellow", "blue", "magenta", "cyan", "white")
# The apps' modules, in the order of the README: terminal emulators, shells, prompts, multiplexers.
APPS = ("kitty", "alacritty", "wezterm", "ghostty", "iterm2", "windows_terminal", "foot", "konsole", "terminator",
        "xterm", "st", "rio", "contour", "warp", "tabby", "hyper", "termux",
        "fish", "zsh", "nushell", "powershell",
        "starship", "oh_my_posh", "powerlevel10k",
        "tmux", "zellij")
CATEGORIES = ("Terminal emulators", "Shells", "Prompts", "Multiplexers")
AUTHOR = "Heritage Themes"
LICENCE = "MIT"


def modules():
    """The module of every app, in README order."""
    return [importlib.import_module(f"{__name__}.{app}") for app in APPS]


def name(theme):
    """The theme's name in file names and configuration, for example "heritage-holi-night", as Neovim lists it."""
    return scheme_name(theme)


def colours(p):
    """The colours of a palette that the terminal apps use, as #RRGGBB.

    ansi: the 16 ANSI colours, normal then bright. dim: the 8 normal ones moved 30% towards bg, for faint text.
    """
    c = {k: "#" + v for k, v in p.items() if isinstance(v, str) and re.fullmatch(r"[0-9A-F]{6}", v)}
    normal = ansi(p)
    return dict(
        bg=c["bg"], fg=c["fg"], muted=c["muted"], dim_fg=c["muted"], bright_fg=c["fg"],
        cursor=c.get("caret", c["gold"]), cursor_text=c["bg"],
        selection_bg=c["selection"], selection_fg=c["fg"],
        ansi=normal, dim=["#" + mix(colour[1:], p["bg"], 0.3) for colour in normal[:8]],
        # links, and search matches: every match on the search background, the focused one in reverse on gold
        link=c["azure"], match_bg=c["searchBg"], match_fg=c["fg"], focused_match_bg=c["gold"],
        focused_match_fg=c["bg"],
        # bars: the frame behind the tabs, with the active tab on bg like the editor's active tab
        bar_bg=c["frame"], bar_fg=c["muted"], active_tab_bg=c["bg"], active_tab_fg=c["fg"],
        inactive_tab_bg=c["frame"], inactive_tab_fg=c["muted"], hover_tab_bg=c["hover"],
        border=c["border"], active_border=c["ansiBlue"], bell=c["gold"],
        surface=c["surface"],
    )


def standard_pairs(p):
    """(element, text colour, background, minimum contrast) that every terminal emulator draws: text, the ANSI colours
    but black, which colours backgrounds and faint text, the cursor, the selection and search matches."""
    c = colours(p)
    return [("text", c["fg"], c["bg"], 4.5), ("bright text", c["bright_fg"], c["bg"], 4.5),
            *((f"colour {i}", colour, c["bg"], 4.5) for i, colour in enumerate(c["ansi"]) if i != 0),
            ("cursor", c["cursor"], c["bg"], 3), ("text under the cursor", c["cursor_text"], c["cursor"], 3),
            ("selection", c["selection_fg"], c["selection_bg"], 4.5), ("search match", c["match_fg"], c["match_bg"], 4.5),
            ("focused search match", c["focused_match_fg"], c["focused_match_bg"], 4.5), ("link", c["link"], c["bg"], 4.5)]


def tab_pairs(p):
    c = colours(p)
    return [("active tab", c["active_tab_fg"], c["active_tab_bg"], 4.5),
            ("inactive tab", c["inactive_tab_fg"], c["inactive_tab_bg"], 4.5),
            ("tab under the pointer", c["fg"], c["hover_tab_bg"], 4.5)]


HEX = re.compile(r"#[0-9A-F]{6}")
# Backgrounds for bars and segments drawn beside bg, from the most to the least set apart from it.
BAR_BACKGROUNDS = ("frame", "surface", "hover", "caretRow", "bgTool")


def contrast(a, b):
    """WCAG contrast ratio of two #RRGGBB or RRGGBB colours."""
    x, y = sorted((luminance(a.lstrip("#")), luminance(b.lstrip("#"))), reverse=True)
    return (x + 0.05) / (y + 0.05)


def readable_background(p, texts, after=None):
    """The palette key of the first of BAR_BACKGROUNDS on which every text colour reaches 4.5:1. With after, the
    first that follows that key in BAR_BACKGROUNDS and differs from its colour, for a part drawn on that one. The build
    checks the ANSI colours at 4.5:1 on bgTool, so there is always one for them but the last."""
    candidates = BAR_BACKGROUNDS
    if after:
        candidates = [k for k in BAR_BACKGROUNDS[BAR_BACKGROUNDS.index(after) + 1:] if p[k] != p[after]]
    for key in candidates:
        if all(contrast(text, p[key]) >= 4.5 for text in texts):
            return key
    raise ValueError(f"{p['name']}: no background in {candidates} reaches 4.5:1 for {texts}")


def check_lines(text, pattern, comment="#"):
    """Raises ValueError for the first line that is neither empty, a comment nor a match of pattern."""
    for number, line in enumerate(text.splitlines(), 1):
        if line.strip() and not line.lstrip().startswith(comment) and not re.fullmatch(pattern, line):
            raise ValueError(f"line {number} is malformed: {line!r}")


def yaml(text):
    """The nested dicts, lists and strings of the block YAML that these modules write: mappings and sequences by
    indentation, single-quoted or plain scalars, and comments. The standard library has no YAML parser, and the build
    runs on it alone. Raises ValueError for anything else."""
    lines = [(len(line) - len(line.lstrip(" ")), line.strip(), number)
             for number, line in enumerate(text.splitlines(), 1) if line.strip() and not line.lstrip().startswith("#")]
    def scalar(value, number):
        if value.startswith("'"):
            if not re.fullmatch(r"'(?:[^']|'')*'", value):
                raise ValueError(f"line {number}: unterminated string {value!r}")
            return value[1:-1].replace("''", "'")
        if re.search(r"[:#'\"{}\[\]]", value):
            raise ValueError(f"line {number}: unquoted {value!r}")
        return value
    def block(i, indent):
        """Parses lines from i at indent; returns (value, next i)."""
        if lines[i][1].startswith("- "):
            items = []
            while i < len(lines) and lines[i][0] == indent and lines[i][1].startswith("- "):
                rest = lines[i][1][2:]
                if re.match(r"[\w-]+:", rest):
                    # a mapping that starts on the item's line, continuing at the indent of its first key
                    lines[i] = (indent + 2, rest, lines[i][2])
                    value, i = block(i, indent + 2)
                else:
                    value, i = scalar(rest, lines[i][2]), i + 1
                items.append(value)
            return items, i
        mapping = {}
        while i < len(lines) and lines[i][0] == indent:
            match = re.fullmatch(r"([\w-]+):(?: (.*))?", lines[i][1])
            if not match:
                raise ValueError(f"line {lines[i][2]}: not a key: {lines[i][1]!r}")
            key, value = match.groups()
            if key in mapping:
                raise ValueError(f"line {lines[i][2]}: {key} is set twice")
            if value:
                mapping[key], i = scalar(value, lines[i][2]), i + 1
            elif i + 1 < len(lines) and lines[i + 1][0] > indent:
                mapping[key], i = block(i + 1, lines[i + 1][0])
            else:
                raise ValueError(f"line {lines[i][2]}: {key} has no value")
        return mapping, i
    if not lines:
        raise ValueError("empty")
    value, end = block(0, lines[0][0])
    if end != len(lines):
        raise ValueError(f"line {lines[end][2]} is indented wrongly")
    return value


def header(p, app, source, comment="#"):
    """The comment lines that open a generated file."""
    return [f"{comment} {p['name']}: a Heritage Themes colour scheme for {app}.",
            f"{comment} Generated from {source}; changes here are overwritten."]
