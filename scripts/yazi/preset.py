#!/usr/bin/env python3
"""Writes heritage/yazi.json from the default themes of a yazi release.

Usage: scripts/yazi/preset.py VERSION OUT.json

For example, from the repository's root:

    python3 scripts/yazi/preset.py 26.9.1 heritage/yazi.json

yazi builds its default dark and light themes, yazi-config/preset/theme-dark.toml and theme-light.toml, into its
binary, so the script downloads them from the release's tag on GitHub. It writes:

- version: the release;
- styles: each section of the theme → the keys of its styles, the tables of fg, bg and modifiers that a flavor sets;
- filetype: the file type rules, each without its style, in order;
- icon: globs, dirs, files, exts and conds, each a list of the icon's selector (url, name or if), its glyph (text)
  and its colour in the dark theme (dark) and in the light theme (light), in order.
"""
import json, sys, tomllib, urllib.request

URL = "https://raw.githubusercontent.com/sxyazi/yazi/v{version}/yazi-config/preset/theme-{mode}.toml"
# Style attributes of a rule or a style table, as yazi-binding's StyleFlat reads them.
STYLE = {"fg", "bg", "bold", "dim", "italic", "underline", "blink", "blink_rapid", "reversed", "hidden", "crossed"}
# The key that selects each kind of icon.
SELECTORS = {"globs": "url", "dirs": "name", "files": "name", "exts": "name", "conds": "if"}


def preset(version, mode):
    with urllib.request.urlopen(URL.format(version=version, mode=mode), timeout=60) as response:
        return tomllib.loads(response.read().decode("utf-8"))


def main():
    version, out = sys.argv[1:3]
    dark, light = preset(version, "dark"), preset(version, "light")
    styles = {section: [key for key, value in table.items() if isinstance(value, dict) and set(value) <= STYLE]
              for section, table in dark.items() if section not in ("flavor", "filetype", "icon")}
    filetype = [{k: v for k, v in rule.items() if k not in STYLE} for rule in dark["filetype"]["rules"]]
    if filetype != [{k: v for k, v in rule.items() if k not in STYLE} for rule in light["filetype"]["rules"]]:
        raise SystemExit("the dark and light themes have different file type rules")
    icon = {}
    for kind, selector in SELECTORS.items():
        pairs = list(zip(dark["icon"][kind], light["icon"][kind], strict=True))
        if any(d[selector] != l[selector] or d["text"] != l["text"] for d, l in pairs):
            raise SystemExit(f"the dark and light themes have different {kind} icons")
        icon[kind] = [{selector: d[selector], "text": d["text"], "dark": d["fg"].upper(), "light": l["fg"].upper()}
                      for d, l in pairs]
    with open(out, "w", encoding="utf-8") as f:
        json.dump({"version": version, "styles": styles, "filetype": filetype, "icon": icon}, f, indent=1,
                  ensure_ascii=False)
        f.write("\n")


if __name__ == "__main__":
    main()
