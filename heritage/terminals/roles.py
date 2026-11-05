"""Palette roles of command-line syntax, shared by the shell themes (fish, zsh, Nushell, PowerShell).

A command line takes the roles that the editor themes give the matching constructs in shell scripts: commands the
call role, keywords the keyword role, strings, numbers and comments their own, options and arguments the parameter
role, variables the field role, and redirections, pipes and separators the operator role. Errors take ansiRed, which
the build checks at 4.5:1 against bg, autosuggestions the muted text colour.
"""

# role → (palette key, font styles)
def shell_roles(p):
    kw = ("bold",) if p.get("kwBold", not p["dark"]) else ()
    return {
        "command": ("call", ()), "builtin": ("call", ("italic",)), "function": ("method", ()),
        "alias": ("call", ("underline",)), "keyword": ("keyword", kw), "string": ("string", ()),
        "escape": ("gold", ("bold",)), "number": ("number", ()), "comment": ("comment", ("italic",)),
        "parameter": ("param", ()), "option": ("param", ()), "variable": ("field", ()),
        "operator": ("op", ()), "redirection": ("op", ("bold",)), "separator": ("op", ()),
        "glob": ("constant", ()), "path": ("fg", ("underline",)), "type": ("type", ()), "member": ("field", ()),
        "error": ("ansiRed", ("bold",)), "suggestion": ("muted", ()), "default": ("fg", ()),
    }


def colour(p, role):
    """The #RRGGBB colour and font styles of a shell role."""
    key, styles = shell_roles(p)[role]
    return "#" + p[key], styles


def role_pairs(p, roles):
    """(element, text colour, bg, minimum) for shell roles: comments at 3:1, the rest at 4.5:1."""
    return [(role, colour(p, role)[0], "#" + p["bg"], 3 if role == "comment" else 4.5) for role in roles]
