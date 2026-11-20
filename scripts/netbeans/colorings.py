#!/usr/bin/env python3
"""Reads the Fonts & Colors colourings that a NetBeans installation defines, which heritage/netbeans.py mirrors.

Usage: scripts/netbeans/colorings.py NETBEANS_DIR [--write]

NETBEANS_DIR is the folder that NetBeans is installed in, the one with the platform and ide clusters, for example
/usr/lib/apache-netbeans or the files/netbeans folder of the Flatpak. The script reads the layer of every module and
collects the colourings of the default profile, NetBeans: the base token categories, the highlights, the annotations
and the token colourings of each language, with the colouring each inherits from and whether it sets a colour of its
own. A language that the default profile leaves out but NetBeans' FlatLaf Dark profile colours, such as Markdown, comes
from that profile.

NetBeans keeps a colouring of a module's profile only when the default profile defines one of that name for the
language, so a profile's language files name the default profile's colourings, and a colouring that inherits from
another of its language must find it in the same file.

Without --write, the script compares the installation with heritage/netbeans.json and lists the colourings that one
has and the other lacks, and exits with status 1 when they differ. With --write, it writes heritage/netbeans.json.
"""
import glob, json, os, posixpath, re, sys, zipfile
import xml.etree.ElementTree as ET

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
REFERENCE = os.path.join(ROOT, "heritage", "netbeans.json")
DEFAULT_PROFILE = "NetBeans"
FALLBACK_PROFILE = "FlatLafDark"  # NetBeans' own dark profile, for the languages the default profile leaves out
COLOURS = ("foreColor", "bgColor", "underline", "waveUnderlined", "strikeThrough")
# Entities that layers declare in their DTD and that the parser does not know; they name nothing that this script reads.
ENTITY = re.compile(rb"&(?!(?:amp|lt|gt|quot|apos|#\d+|#x[0-9a-fA-F]+);)[\w.-]+;")


def colourings(text):
    """[name, default, whether it sets a colour] of the fontcolor elements of a Fonts & Colors file."""
    root = ET.fromstring(re.sub(rb"<!DOCTYPE[^>]*>", b"", text))
    return [[e.get("name"), e.get("default"), any(e.get(a) for a in COLOURS)] for e in root.iter("fontcolor")]


def files(netbeans):
    """{(MIME path, profile, coloring type): [[name, default, coloured]]} of every module layer. The base MIME path is
    ""; the coloring type is that of the file, "token" for a language's file."""
    out = {}
    jars = sorted(glob.glob(os.path.join(netbeans, "*", "modules", "*.jar")))
    if not jars:
        sys.exit(f"{netbeans} has no cluster with modules")
    for jar in jars:
        with zipfile.ZipFile(jar) as z:
            for layer in [n for n in z.namelist() if n.endswith("layer.xml")]:
                try:
                    root = ET.fromstring(ENTITY.sub(b"", z.read(layer)))
                except ET.ParseError as e:
                    sys.exit(f"{jar}!{layer}: {e}")
                walk(root, [], z, posixpath.dirname(layer), out)
    return out


def walk(element, path, z, base, out):
    for child in element:
        if child.tag == "folder":
            walk(child, path + [child.get("name")], z, base, out)
            continue
        if child.tag != "file" or path[:1] != ["Editors"] or "FontsColors" not in path or not child.get("url"):
            continue
        i = path.index("FontsColors")
        if len(path) != i + 3 or path[i + 2] != "Defaults":
            continue
        url = re.sub(r"^nbres(loc)?:", "", child.get("url"))
        name = url[1:] if url.startswith("/") else posixpath.normpath(posixpath.join(base, url))
        kind = next((a.get("stringvalue") for a in child.findall("attr")
                     if a.get("name") == "nbeditor-settings-ColoringType"), None) or "token"
        key = ("/".join(path[1:i]), path[i + 1], kind)
        out.setdefault(key, []).extend(colourings(z.read(name)))


def reference(netbeans, version):
    """The data of heritage/netbeans.json."""
    found = files(netbeans)
    def merged(mime, profile, kind):
        seen = {}
        for name, default, coloured in found.get((mime, profile, kind), []):
            seen[name] = [name, default, coloured or seen.get(name, [None, None, False])[2]]
        return list(seen.values())
    languages = {}
    for mime in sorted({m for m, _, _ in found if m}):
        own = merged(mime, DEFAULT_PROFILE, "token")
        languages[mime] = own or merged(mime, FALLBACK_PROFILE, "token")
    return {
        "source": f"Fonts & Colors files of the module layers of Apache NetBeans {version}, read by "
                  f"scripts/netbeans/colorings.py: the {DEFAULT_PROFILE} profile, and {FALLBACK_PROFILE} for the "
                  f"languages that {DEFAULT_PROFILE} leaves out",
        "base": {kind: merged("", DEFAULT_PROFILE, kind) for kind in ("token", "highlight", "annotation")},
        "languages": {mime: entries for mime, entries in languages.items() if entries},
    }


def dumps(data):
    """data as JSON with one colouring to a line, so that a change to NetBeans' colourings reads as a short diff."""
    def section(entries):
        return "{\n" + ",\n".join(f'  {json.dumps(key)}: [\n' + ",\n".join(f"   {json.dumps(e)}" for e in value) + "\n  ]"
                                   for key, value in entries.items()) + "\n }"
    return (f'{{\n "source": {json.dumps(data["source"])},\n "base": {section(data["base"])},\n'
            f' "languages": {section(data["languages"])}\n}}\n')


def version(netbeans):
    """NetBeans' version from the build number file of its platform cluster, for example "32"."""
    for path in glob.glob(os.path.join(netbeans, "platform", "core", "locale", "core_nb*.jar")) + \
            glob.glob(os.path.join(netbeans, "nb", "core", "locale", "core_nb*.jar")):
        with zipfile.ZipFile(path) as z:
            for name in z.namelist():
                if name.endswith("Bundle_nb.properties"):
                    match = re.search(rb"currentVersion=Apache NetBeans IDE (\S+)", z.read(name))
                    if match:
                        return match.group(1).decode()
    return "unknown"


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) != 1:
        sys.exit(__doc__.split("\n\n")[1])
    data = reference(args[0], version(args[0]))
    if "--write" in sys.argv:
        with open(REFERENCE, "w", encoding="utf-8", newline="\n") as f:
            f.write(dumps(data))
        print(f"{REFERENCE}: {len(data['languages'])} languages")
        return
    with open(REFERENCE, encoding="utf-8") as f:
        known = json.load(f)
    differences = 0
    for section in ("base", "languages"):
        for key in sorted(set(data[section]) | set(known[section])):
            have = {tuple(e) for e in data[section].get(key, [])}
            kept = {tuple(e) for e in known[section].get(key, [])}
            for e in sorted(have - kept, key=str):
                print(f"{section} {key or 'base'}: NetBeans has {e}")
            for e in sorted(kept - have, key=str):
                print(f"{section} {key or 'base'}: heritage/netbeans.json has {e}")
            differences += len(have ^ kept)
    print(f"{differences} differences")
    sys.exit(1 if differences else 0)


if __name__ == "__main__":
    main()
