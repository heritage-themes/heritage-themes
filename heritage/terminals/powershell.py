"""PowerShell theme: a script that the profile dot-sources, setting PSReadLine's colours of the command line and, in
PowerShell 7.2 and later, the $PSStyle colours of formatted output, errors and file listings. Colours are ANSI escape
sequences in 24-bit colour, which Windows PowerShell 5.1 with PSReadLine 2 also accepts."""
import re

from . import check_lines, colours, header, name
from .roles import colour, role_pairs, shell_roles

APP = "PowerShell"
FOLDER = "powershell"
CATEGORY = "Shells"
INSTALL = """Copy the files in `powershell` into a `themes` folder beside your profile, which `$PROFILE` names, and \
dot-source a theme in the profile:

```powershell
. (Join-Path (Split-Path $PROFILE) themes/{stem}.ps1)
```

Each theme colours the command line of PSReadLine 2.2 or later (tokens, the selection and predictions) and, in \
PowerShell 7.2 or later, the `$PSStyle` colours of tables, errors, warnings, progress bars and file listings."""
SGR = {"bold": "1", "italic": "3", "underline": "4"}
# PSReadLine 2.3 colour → shell role
TOKENS = {
    "Command": "command", "Comment": "comment", "Default": "default", "Keyword": "keyword", "Member": "member",
    "Number": "number", "Operator": "operator", "Parameter": "option", "String": "string", "Type": "type",
    "Variable": "variable", "Error": "error", "InlinePrediction": "suggestion",
}


def sequence(fg=None, bg=None, styles=()):
    """The ANSI escape sequence for colours and font styles, as PowerShell source using $e for the escape character."""
    parts = [SGR[s] for s in styles]
    if fg:
        parts.append("38;2;" + ";".join(str(int(fg[i:i + 2], 16)) for i in (1, 3, 5)))
    if bg:
        parts.append("48;2;" + ";".join(str(int(bg[i:i + 2], 16)) for i in (1, 3, 5)))
    return f'"${{e}}[{";".join(parts)}m"'


def psreadline(p):
    c = colours(p)
    out = {}
    for key, role in TOKENS.items():
        value, styles = colour(p, role)
        out[key] = sequence(value, styles=styles)
    out.update({
        "ContinuationPrompt": sequence(c["muted"]), "Emphasis": sequence(c["ansi"][4], styles=("bold",)),
        "Selection": sequence(c["selection_fg"], c["selection_bg"]),
        "ListPrediction": sequence(c["ansi"][3]), "ListPredictionSelected": sequence(bg=c["selection_bg"]),
        "ListPredictionTooltip": sequence(c["muted"], styles=("italic",)),
    })
    return out


def psstyle(p):
    """$PSStyle property path → sequence."""
    c = colours(p)
    green, red, yellow, blue, magenta, cyan = (c["ansi"][i] for i in (2, 1, 3, 4, 5, 6))
    return {
        "Formatting.FormatAccent": sequence(green, styles=("bold",)),
        "Formatting.TableHeader": sequence(green, styles=("bold",)),
        "Formatting.CustomTableHeaderLabel": sequence(green, styles=("bold", "italic")),
        "Formatting.ErrorAccent": sequence(cyan, styles=("bold",)),
        "Formatting.Error": sequence(red), "Formatting.Warning": sequence(yellow),
        "Formatting.Verbose": sequence(yellow), "Formatting.Debug": sequence(yellow),
        "Formatting.FeedbackName": sequence(yellow), "Formatting.FeedbackText": sequence(cyan),
        "Formatting.FeedbackAction": sequence(blue),
        "FileInfo.Directory": sequence(blue, styles=("bold",)), "FileInfo.SymbolicLink": sequence(cyan),
        "FileInfo.Executable": sequence(green, styles=("bold",)),
        "Progress.Style": sequence(magenta),
    }


def files(theme, source):
    """Each colour is set on its own, inside try, because PowerShell and PSReadLine versions differ in which keys and
    properties they have, and one unknown name would otherwise stop the whole block. The errors of unknown names are
    removed from $Error again."""
    p = theme["palette"]
    lines = [
        *header(p, APP, source),
        "$e = [char]27",
        "$errors = $Error.Count",
        "$readLine = @{",
        *(f"    {key} = {value}" for key, value in psreadline(p).items()),
        "}",
        "foreach ($key in $readLine.Keys) {",
        "    try { Set-PSReadLineOption -Colors @{ $key = $readLine[$key] } -ErrorAction Stop } catch {}",
        "}",
        "if ($PSStyle) {",
        *(f"    try {{ $PSStyle.{key} = {value} }} catch {{}}" for key, value in psstyle(p).items()),
        "}",
        "while ($Error.Count -gt $errors) { $Error.RemoveAt(0) }",
        "Remove-Variable e, errors, readLine",
    ]
    return [(f"{name(theme)}.ps1", "\n".join(lines) + "\n")]


def validate(theme, text):
    check_lines(text, r'\$e = \[char\]27|\$errors = \$Error\.Count|\$readLine = @\{|\}|'
                      r'foreach \(\$key in \$readLine\.Keys\) \{|'
                      r'    try \{ Set-PSReadLineOption -Colors @\{ \$key = \$readLine\[\$key\] \} '
                      r'-ErrorAction Stop \} catch \{\}|'
                      r'if \(\$PSStyle\) \{|    try \{ \$PSStyle\.[\w.]+ = "\$\{e\}\[[\d;]+m" \} catch \{\}|'
                      r'while \(\$Error\.Count -gt \$errors\) \{ \$Error\.RemoveAt\(0\) \}|'
                      r'Remove-Variable e, errors, readLine|    \w+ = "\$\{e\}\[[\d;]+m"')
    p = theme["palette"]
    found = dict(re.findall(r"^    (\w+) = (.*)$", text, re.M))
    styles = dict(re.findall(r'^    try \{ \$PSStyle\.([\w.]+) = (.*) \} catch \{\}$', text, re.M))
    if found != psreadline(p) or styles != psstyle(p):
        raise ValueError("differs from heritage.terminals.powershell.psreadline and psstyle")


def pairs(p):
    c = colours(p)
    return [*role_pairs(p, (r for r in shell_roles(p) if r in TOKENS.values())),
            ("selection", c["selection_fg"], c["selection_bg"], 4.5), ("list prediction", c["ansi"][3], c["bg"], 4.5)]
