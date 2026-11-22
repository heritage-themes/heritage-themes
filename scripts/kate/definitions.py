#!/usr/bin/env python3
"""Writes heritage/kate.json from the KSyntaxHighlighting library that Kate uses.

Usage: scripts/kate/definitions.py OUT.json

Run it where KSyntaxHighlighting and PyQt6 are installed, for example in the editors image of preview.py:

    podman build -t localhost/heritage-editors scripts/editors
    podman run --rm --userns=keep-id -v "$PWD:/repo:Z" localhost/heritage-editors \\
        python3 /repo/scripts/kate/definitions.py /repo/heritage/kate.json

The library holds its syntax definitions and themes as Qt resources, which it registers when it loads, so the script
reads the definitions as the library ships them, with those that its build generates from templates, such as the
Jinja and PHP variants. It writes:

- version: the library's version, from the file name of the shared library;
- text_styles and editor_colours: the keys of a theme's text-styles and editor-colors, which every bundled theme sets,
  in the order of Breeze Dark, the library's default dark theme;
- definitions: the name of each definition → the name of each of its items → the default style it takes;
- hard_coded: the colours that an item sets itself (color, selColor, backgroundColor, selBackgroundColor), which a
  theme replaces only through custom-styles;
- bundled: the name of each bundled theme → its BackgroundColor and TextSelection, by which Kate matches a theme to
  the window's colour scheme.
"""
import ctypes, glob, json, re, sys
import xml.etree.ElementTree as ET

from PyQt6.QtCore import QDirIterator, QFile, QIODevice

ROOT = ":/org.kde.syntax-highlighting"
COLOURS = ("color", "selColor", "backgroundColor", "selBackgroundColor")


def library():
    """The path of the shared library, loaded so that it registers its resources."""
    candidates = sorted(glob.glob("/usr/lib*/libKF6SyntaxHighlighting.so.6.*"))
    if not candidates:
        raise SystemExit("definitions: KSyntaxHighlighting 6 is not installed")
    ctypes.CDLL(candidates[-1], mode=ctypes.RTLD_GLOBAL)
    return candidates[-1]


def resources(folder):
    """Path → bytes of each resource in a folder of the library's resources."""
    out = {}
    iterator = QDirIterator(f"{ROOT}/{folder}")
    while iterator.hasNext():
        path = iterator.next()
        f = QFile(path)
        if not f.open(QIODevice.OpenModeFlag.ReadOnly):
            raise SystemExit(f"definitions: cannot read {path}")
        out[path] = bytes(f.readAll())
        f.close()
    return out


def main():
    out = sys.argv[1]
    version = re.search(r"\.so\.(\d+\.\d+\.\d+)$", library())[1]
    themes = {path.rsplit("/", 1)[1]: json.loads(data) for path, data in resources("themes").items()
              if path.endswith(".theme")}
    breeze = themes["breeze-dark.theme"]
    text_styles, editor_colours = list(breeze["text-styles"]), list(breeze["editor-colors"])
    for name, theme in themes.items():
        if set(theme["text-styles"]) != set(text_styles) or set(theme["editor-colors"]) != set(editor_colours):
            raise SystemExit(f"definitions: {name} sets other keys than breeze-dark.theme")
    definitions, hard_coded = {}, {}
    for path, data in resources("syntax").items():
        if not path.endswith(".xml"):
            continue
        root = ET.fromstring(data)
        name = root.get("name")
        if name in definitions:
            raise SystemExit(f"definitions: {name} is defined twice")
        items = {}
        for item in root.iter("itemData"):
            style = item.get("defStyleNum", "dsNormal")[2:]
            if style not in text_styles:
                raise SystemExit(f"definitions: {name} {item.get('name')} takes {style}, which no theme sets")
            items[item.get("name")] = style
            colours = {key: item.get(key) for key in COLOURS if item.get(key)}
            if colours:
                hard_coded.setdefault(name, {})[item.get("name")] = colours
        definitions[name] = items
    if not definitions:
        raise SystemExit("definitions: the library holds no syntax definitions")
    bundled = {theme["metadata"]["name"]: [theme["editor-colors"][key].lower()
                                           for key in ("BackgroundColor", "TextSelection")]
               for theme in themes.values()}
    data = dict(source=f"KSyntaxHighlighting {version}, the definitions and themes it ships", version=version,
                text_styles=text_styles, editor_colours=editor_colours, definitions=dict(sorted(definitions.items())),
                hard_coded=dict(sorted(hard_coded.items())), bundled=dict(sorted(bundled.items())))
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print(f"{out}: {len(definitions)} definitions, {sum(len(v) for v in hard_coded.values())} items with colours "
          f"of their own")


if __name__ == "__main__":
    main()
