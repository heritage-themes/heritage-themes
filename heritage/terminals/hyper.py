"""Hyper plugin: one local plugin with every theme, which ~/.hyper_plugins/local/heritage-themes holds and
.hyper.js turns on with localPlugins and chooses a theme of with config.heritageTheme."""
import json, re

from . import colours, name, standard_pairs, tab_pairs

APP = "Hyper"
FOLDER = "hyper"
CATEGORY = "Terminal emulators"
INSTALL = """The themes come as one local plugin. Copy the `heritage-themes` folder in `hyper` into the \
`.hyper_plugins/local` folder beside Hyper's configuration file, which **Edit | Preferences…** opens: \
`~/.hyper_plugins/local` on macOS and Linux, `$XDG_CONFIG_HOME/hyper/.hyper_plugins/local` when `XDG_CONFIG_HOME` \
is set, and `%AppData%\\Hyper\\.hyper_plugins\\local` on Windows. Then turn the plugin on and choose a theme in \
`.hyper.js`:

```js
module.exports = {
  config: {
    heritageTheme: "{stem}",
    // the rest of your configuration
  },
  localPlugins: ["heritage-themes"],
};
```

Each theme colours the terminal, the cursor, selections, borders, the tab bar and the split dividers."""
PLUGIN = "heritage-themes"
NAMES = ("black", "red", "green", "yellow", "blue", "magenta", "cyan", "white")


def config(p):
    """The Hyper config keys a theme sets."""
    c = colours(p)
    selection = c["selection_bg"]
    return {
        "backgroundColor": c["bg"], "foregroundColor": c["fg"], "borderColor": c["border"],
        "cursorColor": c["cursor"], "cursorAccentColor": c["cursor_text"], "selectionColor": selection,
        "colors": {**dict(zip(NAMES, c["ansi"][:8])),
                   **{"light" + n.title(): colour for n, colour in zip(NAMES, c["ansi"][8:])}},
        # the tab bar on the frame with the active tab on bg, as in the other terminals
        "css": (f".header_header, .tabs_nav, .tabs_list {{ background-color: {c['bar_bg']} !important; }}\n"
                f".tabs_title, .tab_tab {{ color: {c['inactive_tab_fg']} !important; "
                f"border-color: {c['border']} !important; }}\n"
                f".tab_tab:hover {{ background-color: {c['hover_tab_bg']} !important; }}\n"
                f".tab_active {{ background-color: {c['active_tab_bg']} !important; "
                f"color: {c['active_tab_fg']} !important; }}\n"
                f".tab_textActive .tab_textInner {{ color: {c['active_tab_fg']} !important; }}\n"
                f".splitpane_divider {{ background-color: {c['border']} !important; }}\n"),
    }


def files(theme, source):
    return []


def combined(themes, source):
    data = {name(t): config(t["palette"]) for t in themes}
    index = "\n".join([
        f"// Heritage Themes for Hyper. Generated from {source}; changes here are overwritten.",
        "// Choose a theme with config.heritageTheme in .hyper.js, for example \"heritage-holi-night\".",
        '"use strict";',
        "",
        f"const THEMES = {json.dumps(data, indent=2, ensure_ascii=False)};",
        "",
        "exports.decorateConfig = (config) => {",
        "  const theme = THEMES[config.heritageTheme];",
        "  if (!theme) {",
        "    if (config.heritageTheme) {",
        "      console.error(`heritage-themes: no theme named ${config.heritageTheme}`);",
        "    }",
        "    return config;",
        "  }",
        "  return Object.assign({}, config, theme, {",
        "    colors: Object.assign({}, config.colors, theme.colors),",
        "    css: `${config.css || \"\"}\\n${theme.css}`,",
        "  });",
        "};",
        "",
    ])
    package = json.dumps({"name": PLUGIN, "version": "1.0.0", "description": "Heritage Themes for Hyper",
                          "main": "index.js", "license": "MIT", "keywords": ["hyper", "hyper-theme"]}, indent=2)
    return [(f"{PLUGIN}/index.js", index), (f"{PLUGIN}/package.json", package + "\n")]


def validate_combined(themes, files):
    index, package = files[f"{PLUGIN}/index.js"], json.loads(files[f"{PLUGIN}/package.json"])
    match = re.search(r"^const THEMES = (\{.*?\n\});$", index, re.M | re.S)
    if not match or json.loads(match[1]) != {name(t): config(t["palette"]) for t in themes}:
        raise ValueError("the THEMES of index.js differ from heritage.terminals.hyper.config")
    if package["main"] != "index.js" or package["name"] != PLUGIN:
        raise ValueError("package.json does not name the plugin and its index.js")


def pairs(p):
    return [*(pair for pair in standard_pairs(p) if "search" not in pair[0]), *tab_pairs(p)]
