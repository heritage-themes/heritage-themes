"""lazygit theme generated from a palette: a configuration file that sets gui.darkTheme for a dark theme or
gui.lightTheme for a light one, which the user lists after their own configuration file in LG_CONFIG_FILE.

lazygit asks the terminal whether its background is dark or light and applies the matching section, so a Night and a
Day theme listed together switch with the terminal. It draws on the terminal's own background and colours most list
text, such as file status, commit hashes and branch names, with the terminal's ANSI colours, which the matching theme
of the Terminals product takes from the same palette. The theme colours what lazygit lets a theme set: the focused
panel's border and title in ansiBlue, as the Terminals product colours a focused pane, the other panels' in muted, and
the focused one's while searching in gold, the search colour. Key hints in the bottom line take muted. The selected
row takes selection in the focused panel and selInactive in the others, and keeps its text colours, which the build
holds at 4.5:1 on both. A copied commit's hash is bg on azure, as the Terminals product draws the focused search match
in bg on an accent. Unstaged changes take ansiRed. Authors and the commit graph, which lazygit colours by author, take
ansiCyan, so lazygit draws no colour outside the palette. lazygit 0.66 reads the colours of a commit marked as the base
of a rebase but never draws them, so the theme leaves them out.
"""
from .nvim import name  # noqa: F401 - the theme's file is named as Neovim names a scheme

# The fields of lazygit's ThemeConfig, from pkg/config/user_config.go in lazygit 0.66.
THEME_FIELDS = ("activeBorderColor", "inactiveBorderColor", "searchingActiveBorderColor", "optionsTextColor",
                "selectedLineFgColor", "selectedLineBgColor", "inactiveViewSelectedLineBgColor",
                "cherryPickedCommitFgColor", "cherryPickedCommitBgColor", "markedBaseCommitFgColor",
                "markedBaseCommitBgColor", "unstagedChangesColor", "defaultFgColor", "authorColors",
                "branchColorPatterns")
# lazygit's attributes besides colours, from docs/Config.md.
ATTRIBUTES = ("bold", "default", "dim", "reverse", "underline", "strikethrough")


def section(p):
    """The gui section the theme sets: darkTheme for a dark palette, lightTheme for a light one."""
    return "darkTheme" if p["dark"] else "lightTheme"


def settings(p):
    """ThemeConfig field → list of colours and attributes, or for authorColors author → colour, as #RRGGBB."""
    def c(key):
        return "#" + p[key]
    return {
        "activeBorderColor": [c("ansiBlue"), "bold"],
        "inactiveBorderColor": [c("muted")],
        "searchingActiveBorderColor": [c("gold"), "bold"],
        "optionsTextColor": [c("muted")],
        "selectedLineBgColor": [c("selection")],
        "inactiveViewSelectedLineBgColor": [c("selInactive")],
        "cherryPickedCommitFgColor": [c("bg")],
        "cherryPickedCommitBgColor": [c("azure")],
        "unstagedChangesColor": [c("ansiRed")],
        "authorColors": {"*": c("ansiCyan")},
    }


def theme(p, source):
    """The themes/<theme>.yml file for a palette. source is the URL of the theme folder. Colours are quoted, as YAML
    reads an unquoted # as the start of a comment."""
    lines = [f"# {p['name']}: {source}", f"# Applies when the terminal has a {'dark' if p['dark'] else 'light'} "
             "background; needs lazygit 0.66 or later.", "gui:", f"  {section(p)}:"]
    for field, value in settings(p).items():
        lines.append(f"    {field}:")
        if isinstance(value, dict):
            lines += [f'      "{key}": "{colour}"' for key, colour in value.items()]
        else:
            lines += [f'      - "{item}"' if item.startswith("#") else f"      - {item}" for item in value]
    return "\n".join(lines) + "\n"


def styles(p):
    """Element → dict(fg, bg) as #RRGGBB, for the build's contrast check: the text that the theme colours, on the
    terminal's background or on the background the theme gives it, and the terminal's colours on the selected row."""
    s = settings(p)
    bg = "#" + p["bg"]
    result = {
        "focused panel title": dict(fg=s["activeBorderColor"][0], bg=bg),
        "panel title": dict(fg=s["inactiveBorderColor"][0], bg=bg),
        "panel title while searching": dict(fg=s["searchingActiveBorderColor"][0], bg=bg),
        "key hints": dict(fg=s["optionsTextColor"][0], bg=bg),
        "copied commit": dict(fg=s["cherryPickedCommitFgColor"][0], bg=s["cherryPickedCommitBgColor"][0]),
        "unstaged changes": dict(fg=s["unstagedChangesColor"][0], bg=bg),
        "authors": dict(fg=s["authorColors"]["*"], bg=bg),
    }
    for row, key in (("selected row", "selectedLineBgColor"), ("selected row of another panel",
                                                                "inactiveViewSelectedLineBgColor")):
        for role in ("fg", "ansiRed", "ansiGreen", "ansiYellow", "ansiBlue", "ansiMagenta", "ansiCyan"):
            result[f"{role} on the {row}"] = dict(fg="#" + p[role], bg=s[key][0])
    return result
