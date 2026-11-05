"""Nushell theme: a file that config.nu sources, setting $env.config.color_config: the shapes of the command line and
the colours of values in tables."""
import re

from . import check_lines, colours, header, name
from .roles import colour, role_pairs, shell_roles

APP = "Nushell"
FOLDER = "nushell"
CATEGORY = "Shells"
INSTALL = """Copy the files in `nushell` into a `themes` folder in Nushell's configuration folder, which \
`$nu.default-config-dir` names, and source a theme at the end of `config.nu`:

```nu
const theme = ($nu.default-config-dir | path join themes {stem}.nu)
source $theme
```

Each theme colours the command line, the values in tables and `explore`, hints, search results and the selection. \
The prompt keeps the colours of your own prompt configuration."""
ATTRIBUTES = {"bold": "b", "italic": "i", "underline": "u"}
# Nushell 0.116 shape → shell role
SHAPES = {
    "shape_binary": "number", "shape_block": "operator", "shape_bool": "glob",
    "shape_closure": "operator", "shape_custom": "default", "shape_datetime": "number", "shape_directory": "path",
    "shape_external": "command", "shape_external_resolved": "command", "shape_externalarg": "parameter",
    "shape_filepath": "path", "shape_flag": "option", "shape_float": "number", "shape_glob_interpolation": "escape",
    "shape_globpattern": "glob", "shape_int": "number", "shape_internalcall": "builtin", "shape_keyword": "keyword",
    "shape_list": "operator", "shape_literal": "glob", "shape_match_pattern": "glob", "shape_nothing": "glob",
    "shape_operator": "operator", "shape_pipe": "separator", "shape_range": "operator",
    "shape_raw_string": "string", "shape_record": "operator", "shape_redirection": "redirection",
    "shape_signature": "type", "shape_string": "string", "shape_string_interpolation": "escape",
    "shape_table": "operator", "shape_vardecl": "variable", "shape_variable": "variable",
}


def style(fg, attributes=(), bg=None):
    """A Nushell style record."""
    fields = [f'fg: "{fg}"']
    if bg:
        fields.append(f'bg: "{bg}"')
    if attributes:
        fields.append(f'attr: "{"".join(ATTRIBUTES[a] for a in attributes)}"')
    return "{ " + ", ".join(fields) + " }"


def color_config(p):
    """color_config key → Nushell style record."""
    c = colours(p)
    def role(name):
        value, styles = colour(p, name)
        return style(value, styles)
    out = {
        # values in tables, in the text colour except where a type has a role: true and false take the constant role
        # as on the command line, row numbers and headers the green of the ANSI colours
        "separator": style(c["muted"]), "leading_trailing_space_bg": f'{{ bg: "{c["surface"]}" }}',
        "header": style(c["ansi"][2], ["bold"]), "empty": style(c["ansi"][4]),
        "bool": style("#" + p["constant"]), "int": style(c["fg"]), "filesize": style(c["ansi"][6]),
        "duration": style(c["fg"]), "datetime": style(c["ansi"][5]), "range": style(c["fg"]),
        "float": style(c["fg"]), "string": style(c["fg"]), "nothing": style(c["fg"]), "binary": style(c["fg"]),
        "cell-path": style(c["fg"]), "row_index": style(c["ansi"][2], ["bold"]), "record": style(c["fg"]),
        "list": style(c["fg"]), "block": style(c["fg"]), "closure": style(c["fg"]), "glob": style(c["fg"]),
        "hints": style(c["muted"]),
        "search_result": style(c["match_fg"], bg=c["match_bg"]),
        "semver": style(c["ansi"][6], ["bold"]), "semver-range": style(c["ansi"][6], ["bold"]),
        # bytes in hex dumps by kind, as Nushell's own colours sort them
        "binary_null_char": style(c["muted"]), "binary_printable": style(c["ansi"][6], ["bold"]),
        "binary_whitespace": style(c["ansi"][2], ["bold"]), "binary_ascii_other": style(c["ansi"][5], ["bold"]),
        "binary_non_ascii": style(c["ansi"][3], ["bold"]),
        # explore's selection, and the cell under its cursor
        "selection": f'{{ fg: "{c["selection_fg"]}", bg: "{c["selection_bg"]}" }}',
        "selection_cursor": style(c["selection_fg"], ["bold"], c["selection_bg"]),
        "shape_garbage": style("#" + p["redText"], ["bold"], "#" + p["red"]),
        "shape_matching_brackets": '{ attr: "u" }',
    }
    out.update({key: role(value) for key, value in SHAPES.items()})
    return out


def files(theme, source):
    p = theme["palette"]
    lines = [*header(p, APP, source), "$env.config.color_config = {",
             *(f"    {key}: {value}" for key, value in color_config(p).items()), "}"]
    return [(f"{name(theme)}.nu", "\n".join(lines) + "\n")]


def validate(theme, text):
    check_lines(text, r'\$env\.config\.color_config = \{|\}|    [\w-]+: \{(?: \w+: "[#0-9A-Fa-z]+",?)+ \}')
    found = dict(re.findall(r"^    ([\w-]+): (\{.*\})$", text, re.M))
    if found != color_config(theme["palette"]):
        raise ValueError("differs from heritage.terminals.nushell.color_config")


def pairs(p):
    c = colours(p)
    return [*role_pairs(p, shell_roles(p)), ("header", c["ansi"][2], c["bg"], 4.5),
            ("search result", c["match_fg"], c["match_bg"], 4.5),
            ("selection", c["selection_fg"], c["selection_bg"], 4.5),
            ("garbage", "#" + p["redText"], "#" + p["red"], 4.5)]
