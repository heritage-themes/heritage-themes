#!/usr/bin/env python3
"""Writes heritage/gnome_text_editor.json from the GtkSourceView 5 library that GNOME Text Editor uses.

Usage: scripts/gnome-text-editor/definitions.py OUT.json

Run it where GtkSourceView 5 and PyGObject are installed, for example in the editors image of preview.py:

    podman build -t localhost/heritage-editors scripts/editors
    podman run --rm --userns=keep-id -v "$PWD:/repo:Z" localhost/heritage-editors \\
        python3 /repo/scripts/gnome-text-editor/definitions.py /repo/heritage/gnome_text_editor.json

The library holds its language definitions as GResources, which it registers when it loads, so the script reads them
as the library ships them. It writes:

- version: the library's version;
- languages: the id of each language definition → its name, and the id of each of its styles → the style it maps to
  (map-to), or null for a style that takes no colour unless a scheme sets it.
"""
import json, sys
import xml.etree.ElementTree as ET

import gi

gi.require_version("GtkSource", "5")
from gi.repository import Gio, GtkSource  # noqa: E402

ROOT = "/org/gnome/gtksourceview/language-specs/"
NAMESPACE = "{http://www.gnome.org/gtksourceview/language/2.0}"  # absent from most files, present in a few


def tag(element):
    return element.tag.removeprefix(NAMESPACE)


def main():
    out = sys.argv[1]
    GtkSource.init()
    version = f"{GtkSource.get_major_version()}.{GtkSource.get_minor_version()}.{GtkSource.get_micro_version()}"
    languages = {}
    for name in sorted(Gio.resources_enumerate_children(ROOT, Gio.ResourceLookupFlags.NONE)):
        if not name.endswith(".lang"):
            continue
        data = Gio.resources_lookup_data(ROOT + name, Gio.ResourceLookupFlags.NONE).get_data()
        root = ET.fromstring(data)
        if root.attrib.get("version") != "2.0":
            continue  # testv1.lang, in the format of version 1, which GtkSourceView 5 does not load
        styles = {}
        for element in root.iter():
            if tag(element) == "style" and "id" in element.attrib:
                styles[element.attrib["id"]] = element.attrib.get("map-to")
        label = root.attrib.get("name") or root.attrib.get("_name")
        languages[root.attrib["id"]] = dict(name=label, styles=styles)
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        json.dump(dict(version=version, languages=languages), f, indent=1, ensure_ascii=False)
        f.write("\n")
    print(f"{out}: GtkSourceView {version}, {len(languages)} languages")


if __name__ == "__main__":
    main()
