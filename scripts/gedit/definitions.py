#!/usr/bin/env python3
"""Writes heritage/gedit.json from the libgedit-gtksourceview library that gedit uses.

Usage: scripts/gedit/definitions.py OUT.json

Run it where gedit is installed from a distribution that packages libgedit-gtksourceview with RPM, for example in the
editors image of preview.py:

    podman build -t localhost/heritage-editors scripts/editors
    podman run --rm --userns=keep-id -v "$PWD:/repo:Z" localhost/heritage-editors \\
        python3 /repo/scripts/gedit/definitions.py /repo/heritage/gedit.json

The library installs its language definitions as files in its data folder. The script writes:

- version: the library's version;
- languages: the id of each language definition → its name, and the id of each of its styles → the style it maps to
  (map-to), or null for a style that takes no colour unless a scheme sets it.
"""
import glob, json, os, subprocess, sys
import xml.etree.ElementTree as ET

PACKAGE = "libgedit-gtksourceview"
SPECS = "/usr/share/libgedit-gtksourceview-300/language-specs"
NAMESPACE = "{http://www.gnome.org/gtksourceview/language/2.0}"  # absent from most files, present in a few


def tag(element):
    return element.tag.removeprefix(NAMESPACE)


def main():
    out = sys.argv[1]
    version = subprocess.run(["rpm", "-q", "--queryformat", "%{VERSION}", PACKAGE], check=True, capture_output=True,
                             text=True).stdout.strip()
    languages = {}
    for path in sorted(glob.glob(os.path.join(SPECS, "*.lang"))):
        root = ET.parse(path).getroot()
        if root.attrib.get("version") != "2.0":
            raise SystemExit(f"{path}: not in the format of version 2.0")
        styles = {}
        for element in root.iter():
            if tag(element) == "style" and "id" in element.attrib:
                styles[element.attrib["id"]] = element.attrib.get("map-to")
        label = root.attrib.get("name") or root.attrib.get("_name")
        languages[root.attrib["id"]] = dict(name=label, styles=styles)
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        json.dump(dict(version=version, languages=languages), f, indent=1, ensure_ascii=False)
        f.write("\n")
    print(f"{out}: {PACKAGE} {version}, {len(languages)} languages")


if __name__ == "__main__":
    main()
