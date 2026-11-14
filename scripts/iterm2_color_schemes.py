#!/usr/bin/env python3
"""Writes every theme into a checkout of iTerm2-Color-Schemes (https://github.com/mbadolato/iTerm2-Color-Schemes), which
generates the schemes for Windows Terminal, Alacritty, kitty and 30 other apps and feeds windowsterminalthemes.dev.

For each theme it writes yaml/<theme name>.yml with the colours of the iTerm2 preset, and sets the theme's entry in
licenses.yml with the checkout's tools/set_license.py.

Usage: scripts/iterm2_color_schemes.py CHECKOUT
  CHECKOUT  the iTerm2-Color-Schemes checkout

Run it with a Python that has the checkout's requirements.txt installed, as set_license.py needs them.
"""
import json, os, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import heritage
from heritage.terminals import iterm2

URL = "https://github.com/heritage-themes/heritage-themes"
AUTHOR = f"Heritage Themes ({URL})"
LICENCE = "MIT"
# iTerm2 preset key → YAML key, in the order of the YAML file
KEYS = {f"Ansi {i} Color": f"color_{i + 1:02}" for i in range(16)}
KEYS.update({
    "Background Color": "background", "Foreground Color": "foreground", "Bold Color": "bold",
    "Cursor Color": "cursor", "Cursor Text Color": "cursor_text", "Cursor Guide Color": "cursor_guide",
    "Selection Color": "selection", "Selected Text Color": "selection_text",
    "Link Color": "link", "Underline Color": "underline", "Badge Color": "badge", "Tab Color": "tab",
})


def scheme(p):
    """The YAML source of a palette's scheme."""
    colours = iterm2.keys(p)
    if colours.keys() != KEYS.keys():
        raise ValueError(f"{p['name']}: iTerm2 keys differ from KEYS")
    lines = [f"name: {json.dumps(p['name'], ensure_ascii=False)}", f"author: {json.dumps(AUTHOR)}",
             f"variant: {json.dumps('dark' if p['dark'] else 'light')}", ""]
    lines += [f'{key}: "{colours[preset].lower()}"' for preset, key in KEYS.items()]
    return "\n".join(lines) + "\n"


def main(checkout):
    tools = os.path.join(checkout, "tools")
    if not os.path.isfile(os.path.join(tools, "set_license.py")):
        sys.exit(f"{checkout} is not an iTerm2-Color-Schemes checkout")
    for family in heritage.load_families():
        for theme in family.THEMES:
            p = theme["palette"]
            with open(os.path.join(checkout, "yaml", f"{p['name']}.yml"), "w", encoding="utf-8", newline="\n") as f:
                f.write(scheme(p))
            subprocess.run([sys.executable, "set_license.py", "set", p["name"], "--license", LICENCE, "--source", URL],
                           cwd=tools, check=True)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
