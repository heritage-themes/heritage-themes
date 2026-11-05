"""zsh theme: a file that .zshrc sources, setting zle_highlight, which colours the region, search matches and pasted
text of zsh's own line editor, and the styles of zsh-syntax-highlighting and zsh-autosuggestions when they are loaded.
The file sets zsh-syntax-highlighting's styles in an associative array that the plugin keeps, so it can be sourced
before or after the plugin."""
import re

from . import check_lines, colours, header, name
from .roles import colour, role_pairs, shell_roles

APP = "zsh"
FOLDER = "zsh"
CATEGORY = "Shells"
INSTALL = """Copy the files in `zsh` into `~/.config/zsh` and source a theme in `.zshrc`, before or after the plugins:

```zsh
source ~/.config/zsh/{stem}.zsh
```

Each theme colours zsh's line editor (the region, search matches and pasted text) and, when they are loaded, the \
command line of [zsh-syntax-highlighting](https://github.com/zsh-users/zsh-syntax-highlighting), with its bracket \
highlighter, and the suggestions of [zsh-autosuggestions](https://github.com/zsh-users/zsh-autosuggestions). zsh \
treats `#` on the command line as a comment only with `setopt interactive_comments`."""
# zsh-syntax-highlighting 0.8 style → shell role. The styles that the plugin leaves uncoloured by default
# (assign, named-fd, numeric-fd, the substitutions themselves) keep the default text colour.
STYLES = {
    "default": "default", "unknown-token": "error", "reserved-word": "keyword", "alias": "alias",
    "suffix-alias": "alias", "global-alias": "alias", "builtin": "builtin", "function": "function",
    "command": "command", "precommand": "builtin", "commandseparator": "separator", "hashed-command": "command",
    "autodirectory": "path", "path": "path", "path_pathseparator": "path", "path_prefix": "path",
    "path_prefix_pathseparator": "path", "globbing": "glob", "history-expansion": "glob",
    "command-substitution-delimiter": "operator", "process-substitution-delimiter": "operator",
    "arithmetic-expansion": "number", "single-hyphen-option": "option", "double-hyphen-option": "option",
    "back-quoted-argument-delimiter": "operator", "single-quoted-argument": "string",
    "double-quoted-argument": "string", "dollar-quoted-argument": "string", "rc-quote": "escape",
    "dollar-double-quoted-argument": "variable", "back-double-quoted-argument": "escape",
    "back-dollar-quoted-argument": "escape", "redirection": "redirection", "comment": "comment", "arg0": "command",
}
FLAGS = {"bold": "bold", "italic": "italic", "underline": "underline"}
# the bracket highlighter: nesting levels in the ANSI colours, as the other targets colour rainbow brackets
BRACKETS = ("ansiBlue", "ansiMagenta", "ansiGreen", "ansiYellow", "ansiCyan")


def style(p, role):
    value, styles = colour(p, role)
    return ",".join([f"fg={value}", *(FLAGS[s] for s in styles)])


def styles(p):
    """zsh-syntax-highlighting style → value."""
    c = colours(p)
    out = {key: style(p, role) for key, role in STYLES.items()}
    out["bracket-error"] = f"fg={c['ansi'][1]},bold"
    out.update({f"bracket-level-{i}": f"fg=#{p[key]},bold" for i, key in enumerate(BRACKETS, 1)})
    out["cursor-matchingbracket"] = f"bg=#{p['braceBg']}"
    return out


def zle(p):
    """zle_highlight entries: the region in the selection colours, search matches on the search background."""
    c = colours(p)
    return [f"region:fg={c['selection_fg']},bg={c['selection_bg']}",
            f"isearch:fg={c['match_fg']},bg={c['match_bg']}", f"paste:fg={c['fg']},bg={c['selection_bg']}",
            f"suffix:fg={c['muted']},bold", "special:standout"]


def files(theme, source):
    p = theme["palette"]
    lines = [
        *header(p, APP, source),
        "",
        "zle_highlight=(" + " ".join(f"'{entry}'" for entry in zle(p)) + ")",
        "",
        "# zsh-syntax-highlighting",
        "typeset -gA ZSH_HIGHLIGHT_STYLES",
        *(f"ZSH_HIGHLIGHT_STYLES[{key}]='{value}'" for key, value in styles(p).items()),
        "",
        "# zsh-autosuggestions",
        f"typeset -g ZSH_AUTOSUGGEST_HIGHLIGHT_STYLE='{style(p, 'suggestion')}'",
    ]
    return [(f"{name(theme)}.zsh", "\n".join(lines) + "\n")]


def validate(theme, text):
    check_lines(text, r"zle_highlight=\(.*\)|typeset -gA? ZSH_\w+(?:='[^']*')?|ZSH_HIGHLIGHT_STYLES\[[\w-]+\]='[^']*'")
    p = theme["palette"]
    found = dict(re.findall(r"^ZSH_HIGHLIGHT_STYLES\[([\w-]+)\]='([^']*)'$", text, re.M))
    if found != styles(p):
        raise ValueError("differs from heritage.terminals.zsh.styles")
    if re.findall(r"'([^']*)'", re.search(r"^zle_highlight=\((.*)\)$", text, re.M)[1]) != zle(p):
        raise ValueError("zle_highlight differs from heritage.terminals.zsh.zle")


def pairs(p):
    c = colours(p)
    return [*role_pairs(p, shell_roles(p)), ("region", c["selection_fg"], c["selection_bg"], 4.5),
            ("search match", c["match_fg"], c["match_bg"], 4.5),
            *((f"bracket level {i}", f"#{p[key]}", c["bg"], 4.5) for i, key in enumerate(BRACKETS, 1))]
