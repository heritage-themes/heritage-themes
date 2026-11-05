"""tmux theme: a file that tmux.conf sources with source-file. The status line sits on the frame with the current
window on bg, as the other targets draw tab bars; menus, popups and messages sit on surface. tmux 3.8 draws its own
defaults from the dark-theme-* or light-theme-* colours, which the theme sets too, so the parts it does not style follow
the palette; earlier releases skip those options, as set -q ignores an unknown option."""
import re

from . import check_lines, colours, header, name

APP = "tmux"
FOLDER = "tmux"
CATEGORY = "Multiplexers"
INSTALL = """Copy the files in `tmux` into `~/.config/tmux` and source a theme in `tmux.conf`, then reload the \
configuration with `tmux source-file ~/.config/tmux/tmux.conf`:

```tmux
source-file ~/.config/tmux/{stem}.tmux
```

Each theme colours the status line, window list, pane borders, messages, copy mode, the clock, pane numbers, popups \
and menus; tmux 3.8 and later also draw their own defaults in the theme's colours. tmux shows the colours in 24-bit \
when it knows that the terminal has it, which `set -as terminal-features ',*:RGB'` in `tmux.conf` tells it."""
# tmux 3.8 theme colour → palette colour. The theme's black and white are the text on its colours and the text colour,
# as tmux's own styles use them: black on the green status line, white on dark grey menus.
THEME_COLOURS = {"black": "bg", "white": "fg", "light-grey": "muted", "dark-grey": "surface", "green": "ansiGreen",
                 "yellow": "ansiYellow", "red": "ansiRed", "blue": "ansiBlue", "cyan": "ansiCyan",
                 "magenta": "ansiMagenta"}


def styles(p):
    """(option, value, since) per style option; since is the first tmux release with the option, for set -q."""
    c = colours(p)
    def s(fg=None, bg=None, *attributes):
        return ",".join([*(f"fg={fg}",) * bool(fg), *(f"bg={bg}",) * bool(bg), *attributes])
    return [
        ("status-style", s(c["fg"], c["bar_bg"]), "1.9"),
        ("status-left-style", s(c["active_tab_fg"], c["bar_bg"], "bold"), "1.9"),
        ("status-right-style", s(c["bar_fg"], c["bar_bg"]), "1.9"),
        ("window-status-style", s(c["inactive_tab_fg"], c["inactive_tab_bg"]), "1.9"),
        ("window-status-current-style", s(c["active_tab_fg"], c["active_tab_bg"], "bold"), "1.9"),
        ("window-status-last-style", s(c["fg"], c["inactive_tab_bg"]), "1.9"),
        # a window with activity or a bell in the ANSI colour, with text in bg, as tmux's reverse video draws them
        ("window-status-activity-style", s(c["bg"], c["ansi"][3]), "1.9"),
        ("window-status-bell-style", s(c["bg"], c["ansi"][1], "bold"), "1.9"),
        ("pane-border-style", s(c["border"]), "1.9"),
        ("pane-active-border-style", s(c["active_border"]), "1.9"),
        ("message-style", s(c["fg"], c["surface"]), "1.9"),
        ("message-command-style", s(c["fg"], c["surface"]), "1.9"),
        ("mode-style", s(c["selection_fg"], c["selection_bg"]), "1.9"),
        ("display-panes-colour", c["muted"], "1.0"),
        ("display-panes-active-colour", c["active_border"], "1.0"),
        ("clock-mode-colour", c["active_border"], "1.0"),
        ("copy-mode-match-style", s(c["match_fg"], c["match_bg"]), "3.2"),
        ("copy-mode-current-match-style", s(c["focused_match_fg"], c["focused_match_bg"]), "3.2"),
        ("copy-mode-mark-style", s(c["fg"], "#" + p["underCaret"]), "3.2"),
        ("popup-style", s(c["fg"], c["surface"]), "3.3"),
        ("popup-border-style", s(c["border"], c["surface"]), "3.3"),
        ("menu-style", s(c["fg"], c["surface"]), "3.4"),
        ("menu-selected-style", s(c["selection_fg"], c["selection_bg"]), "3.4"),
        ("menu-border-style", s(c["border"], c["surface"]), "3.4"),
    ]


def files(theme, source):
    p = theme["palette"]
    mode = "dark" if p["dark"] else "light"
    lines = [*header(p, APP, source), "",
             f"# tmux 3.8 and later: the {mode} theme colours, which tmux's own styles use",
             *(f'set -gq {mode}-theme-{key} "#{p[role]}"' for key, role in THEME_COLOURS.items()), "",
             "# the status line, panes, messages, copy mode, popups and menus"]
    for option, value, since in styles(p):
        flags = "-g" if tuple(map(int, since.split("."))) < (3, 2) else "-gq"
        lines.append(f'set {flags} {option} "{value}"')
    return [(f"{name(theme)}.tmux", "\n".join(lines) + "\n")]


def validate(theme, text):
    check_lines(text, r'set -gq? [\w-]+ "(?:#[0-9A-F]{6}|(?:fg=#[0-9A-F]{6})?,?(?:bg=#[0-9A-F]{6})?(?:,\w+)*)"')
    p = theme["palette"]
    found = dict(re.findall(r'^set -gq? ([\w-]+) "([^"]*)"$', text, re.M))
    mode = "dark" if p["dark"] else "light"
    expected = {f"{mode}-theme-{key}": f"#{p[role]}" for key, role in THEME_COLOURS.items()}
    expected.update({option: value for option, value, since in styles(p)})
    if found != expected:
        raise ValueError("differs from heritage.terminals.tmux.styles")


def pairs(p):
    """Each style that sets text and a background, the theme colours that tmux 3.8 draws as text on another of them,
    and the clock and pane numbers on bg."""
    out = []
    for option, value, since in styles(p):
        style = dict(part.split("=") for part in value.split(",") if "=" in part)
        if "fg" in style and "bg" in style and option not in ("popup-border-style", "menu-border-style"):
            out.append((option, style["fg"], style["bg"], 4.5))
    c = colours(p)
    out += [("clock", c["active_border"], c["bg"], 4.5)]
    out += [(f"theme black on theme {key}", "#" + p["bg"], "#" + p[role], 4.5)
            for key, role in THEME_COLOURS.items() if key not in ("black", "white", "dark-grey", "light-grey")]
    out += [("theme white on theme dark grey", "#" + p["fg"], "#" + p["surface"], 4.5)]
    return out
