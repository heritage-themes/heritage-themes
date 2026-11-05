"""Tabby colour schemes: one YAML file of entries for terminal.customColorSchemes in Tabby's config.yaml, which
Settings | Appearance | Colors lists alongside its own."""
from . import colours, standard_pairs, yaml as parse_yaml

APP = "Tabby"
FOLDER = "tabby"
CATEGORY = "Terminal emulators"
INSTALL = """Open Tabby's configuration with **Settings | Config file | Show config file**, add the entries in \
`tabby/heritage-themes.yaml` that you want under `terminal.customColorSchemes`, and restart Tabby. Then choose a \
scheme, for example **{label}**, under **Settings | Appearance | Colors**, which lists them with Tabby's own as \
Custom.

Each scheme colours the terminal, the cursor and selections."""


def scheme(p):
    c = colours(p)
    return {"name": p["name"], "foreground": c["fg"], "background": c["bg"], "cursor": c["cursor"],
            "cursorForeground": c["cursor_text"], "selection": c["selection_bg"],
            "selectionForeground": c["selection_fg"], "colors": c["ansi"]}


def files(theme, source):
    return []


def combined(themes, source):
    lines = [f"# Heritage Themes colour schemes for Tabby. Generated from {source}; changes here are overwritten.",
             "# Add the entries to terminal.customColorSchemes in config.yaml.",
             "terminal:", "  customColorSchemes:"]
    for t in themes:
        s = scheme(t["palette"])
        lines.append(f"    - name: '{s['name']}'")
        lines += [f"      {key}: '{value}'" for key, value in s.items() if key not in ("name", "colors")]
        lines.append("      colors:")
        lines += [f"        - '{colour}'" for colour in s["colors"]]
    return [("heritage-themes.yaml", "\n".join(lines) + "\n")]


def validate_combined(themes, files):
    (filename, text), = files.items()
    found = parse_yaml(text)["terminal"]["customColorSchemes"]
    if found != [scheme(t["palette"]) for t in themes]:
        raise ValueError("differs from heritage.terminals.tabby.scheme")


def pairs(p):
    return [pair for pair in standard_pairs(p) if "search" not in pair[0]]
