#!/usr/bin/env python3
"""Writes heritage/xcode.json, the keys that an Xcode theme sets, from an installed Xcode.

Usage: scripts/xcode/keys.py [XCODE]
  XCODE  the Xcode app to read; default: the one that xcode-select names, else /Applications/Xcode.app

It reads every copy of Xcode's own Default (Dark) and Default (Light) themes that Xcode bundles: the keys that any of
them sets, as the newer copies set a few that the older ones leave out, and the syntax node types they colour, which
all of them share, each with the name that Xcode's settings show and whether Xcode lets a theme set its font, from
Built-in Syntax Types.xcsynspec. Run it after updating Xcode; the build then fails on each key that heritage/xcode.py
does not set or that Xcode no longer has.
"""
import glob, json, os, plistlib, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "heritage", "xcode.json")
DEFAULTS = ("Default (Dark).xccolortheme", "Default (Light).xccolortheme")
SPEC = "Contents/SharedFrameworks/SourceModel.framework/Versions/A/Resources/LanguageSpecifications/" \
       "Built-in Syntax Types.xcsynspec"


def xcode_app():
    """The Xcode app named on the command line, else the one of the active developer directory, else the default."""
    if len(sys.argv) > 1:
        return sys.argv[1]
    result = subprocess.run(["xcode-select", "-p"], capture_output=True, text=True)
    developer = result.stdout.strip()
    if developer.endswith(".app/Contents/Developer"):
        return developer.removesuffix("/Contents/Developer")
    return "/Applications/Xcode.app"


def read_plist(path):
    """A property list in any of the formats that plutil reads; the syntax spec is an old-style ASCII plist, which
    plistlib does not read."""
    data = subprocess.run(["plutil", "-convert", "xml1", "-o", "-", path], check=True, capture_output=True).stdout
    return plistlib.loads(data)


def main():
    app = xcode_app()
    with open(os.path.join(app, "Contents", "version.plist"), "rb") as f:
        version = plistlib.load(f)
    themes = [path for name in DEFAULTS for path in glob.glob(os.path.join(app, "Contents", "**", name),
                                                                recursive=True)]
    if not themes:
        raise SystemExit(f"keys.py: {app} has no {' or '.join(DEFAULTS)}")
    keys, syntaxes = set(), set()
    for path in themes:
        theme = read_plist(path)
        syntax = tuple(sorted(theme["DVTSourceTextSyntaxColors"]))
        if tuple(sorted(theme["DVTSourceTextSyntaxFonts"])) != syntax:
            raise SystemExit(f"keys.py: {path} sets fonts for other syntax keys than colours")
        keys.update(theme)
        syntaxes.add(syntax)
    if len(syntaxes) != 1:
        raise SystemExit("keys.py: Xcode's Default themes do not all colour the same syntax keys")
    (syntax,) = syntaxes
    spec = {entry["Identifier"]: entry for entry in read_plist(os.path.join(app, SPEC))}
    nodes = []
    for key in syntax:
        if key not in spec or "Name" not in spec[key]:
            raise SystemExit(f"keys.py: {key} has no name in Built-in Syntax Types.xcsynspec")
        nodes.append({"key": key, "name": spec[key]["Name"], "font": spec[key].get("CanSetFont", "YES") == "YES"})
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps({"xcode": version["CFBundleShortVersionString"], "build": version["ProductBuildVersion"],
                            "keys": sorted(keys)}, ensure_ascii=False)[:-1] + ',\n "syntax": [\n'
                + ",\n".join(f"  {json.dumps(node, ensure_ascii=False)}" for node in nodes) + "]}\n")
    print(f"{OUT}: Xcode {version['CFBundleShortVersionString']}, {len(keys)} keys, {len(nodes)} syntax keys")


if __name__ == "__main__":
    main()
