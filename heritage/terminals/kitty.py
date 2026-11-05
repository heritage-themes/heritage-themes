"""kitty theme: a kitty.conf fragment that kitten themes lists from ~/.config/kitty/themes by its name metadata."""
from . import AUTHOR, LICENCE, check_lines, colours, header, name, standard_pairs, tab_pairs

APP = "kitty"
FOLDER = "kitty"
CATEGORY = "Terminal emulators"
INSTALL = """Copy the files in `kitty` into `~/.config/kitty/themes`, then choose a theme with `kitten themes`, which \
lists the Heritage themes under **User**, or name one:

```bash
mkdir -p ~/.config/kitty/themes && cp kitty/*.conf ~/.config/kitty/themes/
kitten themes --reload-in=all "{label}"
```

Each theme colours the terminal, the tab bar, window borders, URLs and marks."""


def settings(p):
    """kitty.conf colour option → #RRGGBB."""
    c = colours(p)
    out = {
        "foreground": c["fg"], "background": c["bg"],
        "selection_foreground": c["selection_fg"], "selection_background": c["selection_bg"],
        "cursor": c["cursor"], "cursor_text_color": c["cursor_text"],
        "url_color": c["link"],
        "active_border_color": c["active_border"], "inactive_border_color": c["border"],
        "bell_border_color": c["bell"], "visual_bell_color": c["surface"],
        "wayland_titlebar_color": c["bar_bg"], "macos_titlebar_color": c["bar_bg"],
        "tab_bar_background": c["bar_bg"], "tab_bar_margin_color": c["bar_bg"],
        "active_tab_foreground": c["active_tab_fg"], "active_tab_background": c["active_tab_bg"],
        "inactive_tab_foreground": c["inactive_tab_fg"], "inactive_tab_background": c["inactive_tab_bg"],
        # marks: the search background, the selection, and gold in reverse, the focused search match
        "mark1_foreground": c["match_fg"], "mark1_background": c["match_bg"],
        "mark2_foreground": c["selection_fg"], "mark2_background": c["selection_bg"],
        "mark3_foreground": c["focused_match_fg"], "mark3_background": c["focused_match_bg"],
    }
    out.update({f"color{i}": colour for i, colour in enumerate(c["ansi"])})
    return out


def files(theme, source):
    p = theme["palette"]
    lines = [
        f"## name: {p['name']}",
        f"## author: {AUTHOR}",
        f"## license: {LICENCE}",
        f"## upstream: {source}",
        f"## blurb: {'Dark' if p['dark'] else 'Light'} theme from Heritage Themes.",
        "",
        *header(p, APP, source),
        "",
        *(f"{key} {value}" for key, value in settings(p).items()),
    ]
    return [(f"{name(theme)}.conf", "\n".join(lines) + "\n")]


def validate(theme, text):
    check_lines(text, r"\w+ #[0-9A-F]{6}")
    found = [line.split()[0] for line in text.splitlines() if line and not line.startswith("#")]
    if found != list(settings(theme["palette"])):
        raise ValueError("does not set the options of heritage.terminals.kitty.settings")
    if not text.startswith(f"## name: {theme['palette']['name']}\n"):
        raise ValueError("does not start with its name metadata")


def pairs(p):
    c = colours(p)
    return [*standard_pairs(p), *tab_pairs(p), ("mark 2", c["selection_fg"], c["selection_bg"], 4.5)]
