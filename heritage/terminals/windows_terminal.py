"""Windows Terminal colour schemes: one JSON fragment extension with every scheme, which Windows Terminal reads from
%LocalAppData%\\Microsoft\\Windows Terminal\\Fragments\\<app>. A fragment adds profiles and colour schemes only, so the
tab row keeps Windows Terminal's own theme."""
import json

from . import HEX, colours, standard_pairs

APP = "Windows Terminal"
FOLDER = "windows-terminal"
CATEGORY = "Terminal emulators"
INSTALL = """Copy `windows-terminal\\heritage-themes.json` into a folder named `Heritage Themes` in \
`%LocalAppData%\\Microsoft\\Windows Terminal\\Fragments`, creating the folders if they do not exist, and restart \
Windows Terminal. In PowerShell, from the unzipped folder:

```powershell
$fragments = "$env:LOCALAPPDATA\\Microsoft\\Windows Terminal\\Fragments\\Heritage Themes"
New-Item -ItemType Directory -Force $fragments | Out-Null
Copy-Item windows-terminal\\heritage-themes.json $fragments
```

Then choose a scheme, for example **{label}**, under **Settings | Profiles | Appearance | Color scheme**. Each scheme \
colours the terminal, the cursor and selections; Windows Terminal keeps its own tab row, as a fragment adds colour \
schemes only."""
NAMES = ("black", "red", "green", "yellow", "blue", "purple", "cyan", "white")


def scheme(p):
    c = colours(p)
    out = {"name": p["name"], "background": c["bg"], "foreground": c["fg"], "cursorColor": c["cursor"],
           "selectionBackground": c["selection_bg"]}
    out.update(zip(NAMES, c["ansi"][:8]))
    out.update({"bright" + n.title(): colour for n, colour in zip(NAMES, c["ansi"][8:])})
    return out


def files(theme, source):
    return []


def combined(themes, source):
    return [("heritage-themes.json", json.dumps({"schemes": [scheme(t["palette"]) for t in themes]}, indent=2,
                                                 ensure_ascii=False) + "\n")]


def validate_combined(themes, files):
    (filename, text), = files.items()
    schemes = json.loads(text)["schemes"]
    if schemes != [scheme(t["palette"]) for t in themes]:
        raise ValueError("differs from heritage.terminals.windows_terminal.scheme")
    for s in schemes:
        if not all(HEX.fullmatch(v) for k, v in s.items() if k != "name"):
            raise ValueError(f"{s['name']} has a colour that is not #RRGGBB")


def pairs(p):
    return standard_pairs(p)
