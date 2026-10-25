#!/usr/bin/env python3
"""Writes heritage/visualstudio.json, the colours that a Visual Studio theme sets, from an installed Visual Studio.

Usage: scripts/visualstudio/tokens.py

Start the Visual Studio to read, alone, then run it. It reads every .pkgdef file of the installation and collects each
colour that the built-in Dark or Light theme sets: its category, its name, and its background and foreground in both
themes. A category is keyed by its GUID; several .pkgdef files can add colours to one category under different key
names, as the language services do to Text Editor MEF Items.

The language services define most of the editor's display items in code, such as the field and property names of C#,
which no .pkgdef lists. items.ps1 reads every display item of the editor categories from the running Visual Studio
under its Dark and Light themes, switching between them and restoring the theme. A colour that a .pkgdef sets keeps
that value, which carries its alpha; the running Visual Studio gives the others and resolves indexed colours.

The JSON records the Visual Studio version and workloads it was read from. Run it on Windows after updating Visual
Studio, with the workloads that WORKLOADS lists, so that the build fails on each new colour that
heritage/visualstudio.py does not map.
"""
import collections, json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, ROOT)
from heritage import visualstudio  # noqa: E402

OUT = os.path.join(ROOT, "heritage", "visualstudio.json")
VSWHERE = os.path.join(os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)"),
                       "Microsoft Visual Studio", "Installer", "vswhere.exe")
# The workloads whose language services colour the editor in the languages that the themes cover: C# and Visual Basic,
# C and C++, Python, the web languages, and SQL.
WORKLOADS = ("Microsoft.VisualStudio.Workload.CoreEditor", "Microsoft.VisualStudio.Workload.ManagedDesktop",
             "Microsoft.VisualStudio.Workload.NativeDesktop", "Microsoft.VisualStudio.Workload.Python",
             "Microsoft.VisualStudio.Workload.NetWeb", "Microsoft.VisualStudio.Workload.Data")
THEMES = {visualstudio.DARK: "dark", visualstudio.LIGHT: "light"}
# The categories of the editor's display items: MEF classification formats, language service items, the text manager's
# items such as plain text and the selection, and text markers.
EDITOR = ("75a05685-00a8-4ded-bae5-e7a50bfa929a", "e0187991-b458-4f7e-8ca9-42c9a573b56c",
          "58e96763-1d3b-4e05-b6ba-ff7115fd0b7b", "ff349800-ea43-46c1-8c98-878e78f46501")
WINDOW = ("FFFFFFFF", "FF000000")  # the Windows window colour and window text colour: background, foreground
EDITOR_NAMES = {"75a05685-00a8-4ded-bae5-e7a50bfa929a": "Text Editor MEF Items",
                "e0187991-b458-4f7e-8ca9-42c9a573b56c": "Text Editor Language Service Items",
                "58e96763-1d3b-4e05-b6ba-ff7115fd0b7b": "Text Editor Text Manager Items",
                "ff349800-ea43-46c1-8c98-878e78f46501": "Text Editor Text Marker Items"}
KEY = re.compile(r"\$RootKey\$\\Themes\\(\{[0-9a-fA-F-]{36}\})\\([^\\]+)", re.I)


def installation():
    """vswhere's description of the installation whose Visual Studio runs."""
    running = subprocess.run(["powershell", "-NoProfile", "-Command", "(Get-Process devenv).Path"],
                             capture_output=True, encoding="utf-8").stdout.splitlines()
    if len(running) != 1:
        raise SystemExit("tokens: start the Visual Studio to read, alone")
    found = json.loads(subprocess.run([VSWHERE, "-all", "-format", "json", "-include", "packages", "-utf8"],
                                      check=True, capture_output=True, encoding="utf-8").stdout)
    found = [i for i in found if os.path.normcase(i["productPath"]) == os.path.normcase(running[0])]
    if not found:
        raise SystemExit(f"tokens: vswhere does not list {running[0]}")
    return found[0]


def display_items():
    """{(theme, category GUID, name): [background, foreground]} for the editor's display items in the running Visual
    Studio, each colour "FFRRGGBB", "automatic" or None."""
    run = subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File",
                          os.path.join(HERE, "items.ps1"), "-Categories", ",".join(EDITOR)],
                         capture_output=True, encoding="utf-8")
    if run.returncode:
        raise SystemExit(f"tokens: items.ps1 failed:\n{run.stderr or run.stdout}")
    lines = run.stdout.splitlines()
    def colour(text):
        return None if text == "-" else text if text == "automatic" else "FF" + text
    items = {}
    for line in lines:
        theme, category, name, foreground, background = line.split("\t")
        items[theme, category, name] = [colour(background), colour(foreground)]
    if not items:
        raise SystemExit("tokens: items.ps1 read no display items")
    # The storage gives an item that does not set a colour the plain text's: the item follows plain text, as an
    # automatic colour does. Automatic plain text is the Windows window colour and window text colour.
    for (theme, category, name), pair in items.items():
        plain = [WINDOW[i] if c == "automatic" else c
                 for i, c in enumerate(items[theme, EDITOR[2], "Plain Text"])]
        if name != "Plain Text":
            items[theme, category, name] = ["automatic" if c == p else c for c, p in zip(pair, plain)]
    return items


def value(colour):
    """A colour of visualstudio.decode() as the JSON records it: "AARRGGBB" for a raw colour, "automatic", "index:N"
    for an index into the editor's colour table, "system:N" for a Windows system colour, or None."""
    if colour is None:
        return None
    kind, argb = colour
    return {visualstudio.CT_RAW: argb, visualstudio.CT_AUTOMATIC: "automatic",
            visualstudio.CT_COLORINDEX: f"index:{int(argb, 16)}",
            visualstudio.CT_SYSCOLOR: f"system:{int(argb, 16)}"}[kind]


def main():
    vs = installation()
    workloads = sorted(p["id"] for p in vs["packages"] if p["id"].startswith("Microsoft.VisualStudio.Workload."))
    missing = [w for w in WORKLOADS if w not in workloads]
    if missing:
        raise SystemExit(f"tokens: {vs['installationPath']} lacks the workloads {', '.join(missing)}")
    categories = {}  # GUID: {"names": key names, "colours": {name: {"dark": [bg, fg], "light": [bg, fg]}}}
    for folder, _, files in os.walk(vs["installationPath"]):
        for filename in sorted(files):
            if not filename.lower().endswith(".pkgdef"):
                continue
            with open(os.path.join(folder, filename), encoding="utf-8-sig", errors="replace") as f:
                text = f.read()
            if "\\Themes\\" not in text:
                continue
            for key, values in visualstudio.sections(text):
                match = KEY.fullmatch(key)
                theme = THEMES.get(match.group(1).lower()) if match else None
                if theme is None:
                    continue
                for name, data in values:
                    if name != "Data":
                        continue
                    for guid, colours in visualstudio.decode(data)[1]:
                        category = categories.setdefault(guid, {"names": collections.Counter(), "colours": {}})
                        category["names"][match.group(2)] += len(colours)
                        for colour, background, foreground in colours:
                            category["colours"].setdefault(colour, {})[theme] = [value(background), value(foreground)]
    # The editor's display items: a channel that no .pkgdef sets, or sets to an indexed colour, takes the value that
    # the running Visual Studio gives it.
    for (theme, guid, name), pair in display_items().items():
        category = categories.setdefault(guid, {"names": collections.Counter({EDITOR_NAMES[guid]: 0}), "colours": {}})
        stored = category["colours"].setdefault(name, {}).get(theme) or [None, None]
        category["colours"][name][theme] = [s if s is not None and not s.startswith(("index:", "system:")) else p
                                            for s, p in zip(stored, pair)]
    for category in categories.values():
        # the key name under which the .pkgdef files set the most of the category's colours
        category["name"] = min(category["names"].items(), key=lambda n: (-n[1], n[0]))[0]
    def line(item):
        return json.dumps(item, ensure_ascii=False)
    # One colour per line, so that a new Visual Studio shows in the diff as the colours it adds or changes.
    blocks = []
    for guid, category in sorted(categories.items(), key=lambda c: c[1]["name"].lower()):
        colours = ",\n".join(f"    {line({'name': name, **{t: c.get(t) for t in ('dark', 'light')}})}"
                             for name, c in sorted(category["colours"].items(), key=lambda c: c[0].lower()))
        blocks.append(f'  {{"name": {line(category["name"])}, "guid": {line(guid)}, "colours": [\n{colours}]}}')
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(f'{{"visualstudio": {line(vs["catalog"]["productDisplayVersion"])}, '
                f'"workloads": {line(workloads)},\n "categories": [\n' + ",\n".join(blocks) + "]}\n")
    print(f"{OUT}: {len(categories)} categories, {sum(len(c['colours']) for c in categories.values())} colours")


if __name__ == "__main__":
    main()
