"""fish theme: a .theme file in ~/.config/fish/themes, applied with fish_config theme choose or save."""
from . import check_lines, colours, header, name
from .roles import colour, role_pairs, shell_roles

APP = "fish"
FOLDER = "fish"
CATEGORY = "Shells"
INSTALL = """Copy the files in `fish` into `~/.config/fish/themes`, then choose and keep a theme; fish 3.4 or later \
lists them with `fish_config theme list`:

```fish
mkdir -p ~/.config/fish/themes && cp fish/*.theme ~/.config/fish/themes/
fish_config theme save {stem}
```

Each theme colours the command line (commands, keywords, options, strings, variables, redirections, comments and \
errors), autosuggestions, the selection, search matches and the completion pager."""
FLAGS = {"bold": "--bold", "italic": "--italics", "underline": "--underline"}


def style(p, role):
    value, styles = colour(p, role)
    return " ".join([value[1:], *(FLAGS[s] for s in styles)])


def variables(p):
    """fish colour variable → value, in the order of fish's own themes."""
    c = {k: v[1:] for k, v in colours(p).items() if isinstance(v, str)}
    return {
        "fish_color_normal": style(p, "default"),
        "fish_color_autosuggestion": style(p, "suggestion"),
        "fish_color_cancel": "--reverse",
        "fish_color_command": style(p, "command"),
        "fish_color_comment": style(p, "comment"),
        "fish_color_cwd": p["ansiGreen"],
        "fish_color_cwd_root": p["ansiRed"],
        "fish_color_end": style(p, "separator"),
        "fish_color_error": style(p, "error"),
        "fish_color_escape": style(p, "escape"),
        "fish_color_history_current": "--bold",
        "fish_color_host": c["fg"],
        "fish_color_host_remote": p["ansiYellow"],
        "fish_color_keyword": style(p, "keyword"),
        "fish_color_operator": style(p, "variable"),  # variable expansions and globs
        "fish_color_option": style(p, "option"),
        "fish_color_param": style(p, "parameter"),
        "fish_color_quote": style(p, "string"),
        "fish_color_redirection": style(p, "redirection"),
        "fish_color_search_match": f"--background={c['match_bg']}",
        "fish_color_selection": f"{c['selection_fg']} --background={c['selection_bg']}",
        "fish_color_status": p["ansiRed"],
        "fish_color_user": p["ansiGreen"],
        "fish_color_valid_path": "--underline",
        # the pager: completions in the text colour with the typed prefix in the match colour of the other targets
        "fish_pager_color_completion": c["fg"],
        "fish_pager_color_description": f"{c['muted']} --italics",
        "fish_pager_color_prefix": f"{p['ansiBlue']} --bold --underline",
        "fish_pager_color_progress": f"{c['fg']} --background={c['selection_bg']} --bold",
        "fish_pager_color_selected_background": f"--background={c['selection_bg']}",
    }


def files(theme, source):
    p = theme["palette"]
    lines = [f"# name: {p['name']}", f"# url: {source}", "", f"# preferred_background: {p['bg']}",
             *header(p, APP, source), *(f"{key} {value}" for key, value in variables(p).items())]
    return [(f"{name(theme)}.theme", "\n".join(lines) + "\n")]


def validate(theme, text):
    check_lines(text, r"fish_(?:pager_)?color_\w+(?: (?:[0-9A-F]{6}|--\w+(?:=[0-9A-F]{6})?))+")
    found = dict(line.split(" ", 1) for line in text.splitlines() if line.startswith("fish_"))
    if found != variables(theme["palette"]):
        raise ValueError("differs from heritage.terminals.fish.variables")


def pairs(p):
    c = colours(p)
    return [*role_pairs(p, shell_roles(p)), ("selection", c["selection_fg"], c["selection_bg"], 4.5),
            ("pager progress", c["fg"], c["selection_bg"], 4.5), ("pager prefix", "#" + p["ansiBlue"], c["bg"], 4.5)]
