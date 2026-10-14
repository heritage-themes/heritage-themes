#!/usr/bin/env python3
"""Lists text attributes that installed IDEs colour explicitly and the shared scheme does not set.

It reads the platform's Darcula and Default schemes and every file that a plugin adds to them with
<additionalTextAttributes>, which is what the IDE itself loads.

Usage: scripts/parent_overrides.py IDE_DIR [IDE_DIR ...]
  IDE_DIR  an IDE installation, for example ~/.local/share/JetBrains/Toolbox/apps/pycharm

A key listed here keeps its Darcula or Default colour in every theme, because an explicit parent
value takes precedence over the key's fallback to a DEFAULT_* key. Map the ones that matter in
heritage/scheme.py.
"""
import glob, os, re, sys, zipfile
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import heritage
from heritage.scheme import attributes

PLATFORM = "DefaultColorSchemesManager.xml"
PARENTS = ("Darcula", "Default")
# Plugins add attributes to a bundled scheme with <additionalTextAttributes scheme="..." file="..."/>.
ADDITION = re.compile(rb"<additionalTextAttributes\b[^>]*>")
ATTRIBUTE = re.compile(rb'\b(scheme|file)="([^"]+)"')


def values(option):
    value = option.find("value")
    return {o.get("name"): o.get("value") for o in value.findall("option") if o.get("value")} if value is not None else {}


def jars(ide_dirs):
    for ide in ide_dirs:
        for path in sorted(glob.glob(os.path.join(ide, "**", "*.jar"), recursive=True)):
            try:
                with zipfile.ZipFile(path) as z:
                    yield z
            except zipfile.BadZipFile:
                continue


def scan(ide_dirs):
    """{parent: {key: (source, values)}} from the platform schemes and every plugin addition to them."""
    found = {parent: {} for parent in PARENTS}
    additions = {}  # file path in a jar → parent scheme
    for z in jars(ide_dirs):
        for name in z.namelist():
            if name == PLATFORM:
                for scheme in ET.fromstring(z.read(name)).findall("scheme"):
                    if scheme.get("name") in PARENTS and scheme.find("attributes") is not None:
                        for o in scheme.find("attributes").findall("option"):
                            found[scheme.get("name")].setdefault(o.get("name"), ("platform", values(o)))
            elif name.endswith(".xml") and (name.startswith("META-INF/") or "/" not in name):
                for tag in ADDITION.findall(z.read(name)):
                    a = {k.decode(): v.decode() for k, v in ATTRIBUTE.findall(tag)}
                    if a.get("scheme") in PARENTS and "file" in a:
                        additions[a["file"].lstrip("/")] = a["scheme"]
    for z in jars(ide_dirs):
        for name in set(z.namelist()) & set(additions):
            for o in ET.fromstring(z.read(name)).findall("option"):
                found[additions[name]].setdefault(o.get("name"), (os.path.basename(name)[:-4], values(o)))
    return found


def main():
    if len(sys.argv) < 2:
        raise SystemExit(__doc__.strip())
    family = heritage.load_families()[0]
    mapped = set(attributes(family.THEMES[0]["palette"]))
    for parent, keys in scan(sys.argv[1:]).items():
        print(f"# {parent}")
        for key, (source, v) in sorted(keys.items()):
            if key not in mapped and v:
                print(f"{key:55} {source:30} {' '.join(f'{k}={x}' for k, x in v.items())}")


if __name__ == "__main__":
    main()
