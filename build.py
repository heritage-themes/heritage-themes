"""Builds the Heritage Themes JetBrains plugin, VS Code extension and Sublime Text package from every theme folder.

A theme folder is any directory in themes/ containing a theme.py (see heritage/__init__.py).

Usage: python3 build.py [--vsix]
  --vsix  also pack the VS Code extension into a .vsix with vsce, pinned in scripts/vscode and installed there
          with npm ci on first use; needs Node.js 22 or later and npm

Output goes to build/.
"""
import argparse, html, json, os, re, shutil, subprocess, zipfile
import xml.etree.ElementTree as ET

import heritage

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "build")
CHANGELOG = os.path.join(ROOT, "CHANGELOG.md")
# One version for the JetBrains plugin, the VS Code extension and the Sublime Text package. A release publishes each
# product whose changelog has a section for it; see docs/releasing.md.
VERSION = "1.3.0"
VENDOR_URL = "https://github.com/heritage-themes/heritage-themes"
DESCRIPTION = "Colour themes drawn from the colour traditions of different cultures."
PLUGIN_ICONS = ("pluginIcon.svg", "pluginIcon_dark.svg")
SINCE_BUILD = "253"  # 2025.3, the first release with the Islands Dark and Islands Light parent themes
VSCODE_CHANGELOG = os.path.join(ROOT, "vscode", "CHANGELOG.md")
VSCODE_PUBLISHER = "heritage-themes"
VSCODE_NAME = "heritage-themes"
VSCODE_ENGINE = "^1.75.0"
VSCODE_IMAGES_URL = "https://raw.githubusercontent.com/heritage-themes/heritage-themes/master/docs"
VSCODE_SPONSOR_URL = "https://buymeacoffee.com/heritagethemes"
VSCODE_SCREENSHOTS = [("holi-night", "Holi Night"), ("kalamkari-cotton", "Kalamkari Cotton (Light)"),
                      ("sardinia-orbace", "Sardinia Orbace (Dark)"), ("wixarika-wirikuta", "Wixárika Wirikuta (Light)")]
VSCODE_ICON = os.path.join(ROOT, "assets", "pluginIcon_dark.png")  # the Marketplace needs a PNG of 128x128 or more
VSCODE_TOOLS = os.path.join(ROOT, "scripts", "vscode")
SUBLIME_CHANGELOG = os.path.join(ROOT, "sublime", "CHANGELOG.md")
SUBLIME_NAME = "Heritage Themes"  # the package's folder in Packages/, so the colour_scheme paths contain it
SUBLIME_REPOSITORY_URL = "https://github.com/heritage-themes/heritage-themes-sublime"
SUBLIME_FONT_STYLES = {"bold", "italic", "underline"}
# Islands guidance: the main window is lighter than the islands in dark themes, darker in light ones, by this ratio.
FRAME_CONTRAST = 1.20
ANSI = tuple(f"ansi{c}" for c in ("Red", "Green", "Yellow", "Blue", "Magenta", "Cyan"))
# WCAG 2.2 AA minimums for palette roles in every app: 4.5:1 for text, 3:1 for comments, focus rings and the caret.
# (foreground roles, background roles, minimum)
CONTRAST = (
    (("fg", "muted"), ("bg", "bgTool", "bgUi", "surface", "caretRow", "frame"), 4.5),
    (("keyword", "string", "number", "type", "method", "call", "field", "constant", "annotation", "doc", "docTag",
      "op", "param", "typeParam", "label", "gold", "azure") + ANSI, ("bg",), 4.5),
    (("comment",), ("bg",), 3),
    (ANSI, ("bgTool",), 4.5),  # console and terminal
    (("fg",), ("hover", "selection", "selInactive", "searchBg"), 4.5),
    (("ansiBlue",), ("selection",), 4.5),  # VS Code match highlights in a selected list row
    (("ansiBlue", "azure"), ("surface",), 4.5),  # Sublime Text quick panel matches and links in popups
    (("redText",), ("red",), 4.5),
    (("gold",), ("bgTool", "bgUi", "surface"), 3),  # IntelliJ focus ring
    (("caret",), ("bg", "caretRow"), 3),
)


def luminance(hex_colour):
    channels = [int(hex_colour[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    r, g, b = (c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in channels)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    x, y = luminance(a), luminance(b)
    return (max(x, y) + 0.05) / (min(x, y) + 0.05)


def check_frame(palette):
    """Fails the build when the frame does not stand apart from the editor and tool windows as Islands needs."""
    for key in ("bg", "bgTool"):
        ratio = contrast(palette["frame"], palette[key])
        lighter = luminance(palette["frame"]) > luminance(palette[key])
        if lighter != palette["dark"] or ratio < FRAME_CONTRAST:
            side = "lighter" if palette["dark"] else "darker"
            raise SystemExit(f"{palette['name']}: frame must be {side} than {key} by {FRAME_CONTRAST:.2f}:1, "
                             f"is {ratio:.2f}:1 {'lighter' if lighter else 'darker'}")


def check_contrast(palette):
    """Fails the build when a palette role falls below its CONTRAST minimum against a background it is drawn on."""
    p = dict(palette, caret=palette.get("caret", palette["gold"]))
    failures = [f"{fg} on {bg} is {contrast(p[fg], p[bg]):.2f}:1, needs {minimum}:1"
                for fgs, bgs, minimum in CONTRAST for fg in fgs for bg in bgs if contrast(p[fg], p[bg]) < minimum]
    if failures:
        raise SystemExit(f"{palette['name']}: " + "; ".join(failures))


def check_references(t):
    """Fails the build when a UI colour names a colour the theme does not define."""
    colours = t["theme"]["colors"]
    for key, value in t["theme"]["ui"].items():
        for name in value.values() if isinstance(value, dict) else [value]:
            if isinstance(name, str) and not name.startswith("#") and name not in colours:
                raise SystemExit(f"{t['name']}: UI key {key} names undefined colour {name}")


def change_notes():
    """HTML for the plugin's change notes: the CHANGELOG.md section for VERSION, else [Unreleased], else the newest
    released section, which is the plugin's version when VERSION is a release that left the plugin out."""
    with open(CHANGELOG) as f:
        text = f.read()
    sections = re.findall(r"^## \[([^\]]+)\][^\n]*\n(.*?)(?=^## \[|\Z)", text, re.M | re.S)
    entries = {label: body for label, body in sections if body.strip()}
    released = [label for label, _ in sections if label in entries and label != "Unreleased"]
    for label in (VERSION, "Unreleased", *released[:1]):
        if label in entries:
            return f"<b>{VERSION if label == 'Unreleased' else label}</b>\n{changelog_html(entries[label])}"
    raise SystemExit(f"CHANGELOG.md has no entries under [{VERSION}], [Unreleased] or a released version")


def changelog_html(section):
    out, in_list = [], False
    for line in section.strip().splitlines():
        if line.startswith("- "):
            if not in_list:
                out.append("<ul>")
                in_list = True
            out.append(f"<li>{html.escape(line[2:].strip())}</li>")
        elif line.startswith("  ") and in_list and line.strip():
            out[-1] = out[-1][:-5] + " " + html.escape(line.strip()) + "</li>"
        else:
            if in_list:
                out.append("</ul>")
                in_list = False
            if line.startswith("### "):
                out.append(f"<b>{html.escape(line[4:].strip())}</b>")
    if in_list:
        out.append("</ul>")
    return "\n".join(out)


def plugin_xml(families, themes):
    blurbs = "\n".join(f"      <li><b>{f.FAMILY}</b>: {f.BLURB}</li>" for f in families)
    providers = "\n".join(
        f'    <themeProvider id="{t["id"]}" path="/themes/{t["slug"]}.theme.json"/>' for t in themes)
    return f"""<idea-plugin>
  <id>heritage.themes</id>
  <name>Heritage Themes</name>
  <version>{VERSION}</version>
  <vendor url="{VENDOR_URL}">Heritage Themes</vendor>
  <description><![CDATA[
    <p>{DESCRIPTION}</p>
    <p>Requires an IntelliJ-based IDE, version 2025.3 or later. Every theme uses the Islands UI: the editor and tool windows sit as rounded islands on the main window.</p>
    <ul>
{blurbs}
    </ul>
    <p>Report problems and suggest traditions on the <a href="{VENDOR_URL}/issues">issue tracker</a>.</p>
  ]]></description>
  <change-notes><![CDATA[
    {change_notes()}
  ]]></change-notes>
  <idea-version since-build="{SINCE_BUILD}"/>
  <depends>com.intellij.modules.platform</depends>
  <extensions defaultExtensionNs="com.intellij">
{providers}
  </extensions>
</idea-plugin>
"""


def validate(jar, themes):
    """Fails the build when the jar's descriptor, icons or theme files are malformed or missing."""
    with zipfile.ZipFile(jar) as z:
        names = set(z.namelist())
        descriptor = ET.fromstring(z.read("META-INF/plugin.xml"))
        for tag in ("id", "name", "version", "vendor", "description", "change-notes"):
            element = descriptor.find(tag)
            if element is None or not "".join(element.itertext()).strip():
                raise SystemExit(f"plugin.xml: <{tag}> is missing or empty")
        providers = descriptor.findall("extensions/themeProvider")
        if len(providers) != len(themes):
            raise SystemExit(f"plugin.xml: {len(providers)} themeProviders for {len(themes)} themes")
        for provider in providers:
            path = provider.get("path").lstrip("/")
            if path not in names:
                raise SystemExit(f"plugin.xml: themeProvider path {path} is not in the jar")
            json.loads(z.read(path))
        for t in themes:
            ET.fromstring(z.read(f"themes/{t['slug']}.xml"))
        for icon in PLUGIN_ICONS:
            ET.fromstring(z.read(f"META-INF/{icon}"))


def vscode_manifest(themes):
    return {
        "name": VSCODE_NAME, "displayName": "Heritage Themes", "description": DESCRIPTION,
        "version": VERSION, "publisher": VSCODE_PUBLISHER, "license": "MIT", "icon": "icon.png",
        "repository": {"type": "git", "url": f"{VENDOR_URL}.git"}, "homepage": VENDOR_URL,
        "bugs": {"url": f"{VENDOR_URL}/issues"}, "sponsor": {"url": VSCODE_SPONSOR_URL},
        "engines": {"vscode": VSCODE_ENGINE},
        "categories": ["Themes"],
        "keywords": ["theme", "color theme", "dark theme", "light theme", "culture", "heritage"],
        "files": ["themes", "icon.png", "CHANGELOG.md", "LICENSE"],  # vsce adds package.json and README.md
        "contributes": {"themes": [
            {"label": t["name"], "uiTheme": "vs-dark" if t["dark"] else "vs",
             "path": f"./themes/{t['slug']}-color-theme.json"} for t in themes]},
    }


def vscode_readme(families):
    """The Marketplace page. Links are absolute: the Marketplace does not resolve paths in the repository."""
    rows = "\n".join(f"| [{f.FAMILY}]({VENDOR_URL}/tree/master/themes/{heritage.folder(f)}) "
                     f"| {', '.join(t['palette']['name'] for t in f.THEMES)} | {f.BLURB} |" for f in families)
    count = sum(len(f.THEMES) for f in families)
    images = "\n\n".join(f"![{name}]({VSCODE_IMAGES_URL}/vscode-{slug}.png)" for slug, name in VSCODE_SCREENSHOTS)
    return f"""# Heritage Themes

{DESCRIPTION} {count} dark and light themes in {len(families)} families; each family maps the named colours of \
one tradition to syntax roles.

Choose a theme with **Preferences: Color Theme** (`Ctrl+K Ctrl+T`; `Cmd+K Cmd+T` on macOS).

{images}

| Family | Themes | Tradition |
| --- | --- | --- |
{rows}

Each family's page describes its colour tradition. The same themes are available for JetBrains IDEs: see \
[Heritage Themes on GitHub]({VENDOR_URL}).

Report a problem or suggest a tradition on the [issue tracker]({VENDOR_URL}/issues). Include the theme, VS Code version, language and a screenshot.
"""


def build_vscode(families, themes):
    """Writes the VS Code extension's files to build/vscode and returns that folder."""
    directory = os.path.join(OUT, "vscode")
    os.makedirs(os.path.join(directory, "themes"))
    with open(os.path.join(directory, "package.json"), "w") as f:
        json.dump(vscode_manifest(themes), f, indent=2, ensure_ascii=False)
    with open(os.path.join(directory, "README.md"), "w") as f:
        f.write(vscode_readme(families))
    shutil.copy(VSCODE_CHANGELOG, os.path.join(directory, "CHANGELOG.md"))
    shutil.copy(os.path.join(ROOT, "LICENSE"), os.path.join(directory, "LICENSE"))
    shutil.copy(VSCODE_ICON, os.path.join(directory, "icon.png"))
    for t in themes:
        with open(os.path.join(directory, "themes", f"{t['slug']}-color-theme.json"), "w") as f:
            json.dump(t["vscode"], f, indent=2, ensure_ascii=False)
    return directory


def validate_vscode(directory, themes):
    """Fails the build when the extension manifest is incomplete or a contributed theme is missing or malformed."""
    with open(os.path.join(directory, "package.json")) as f:
        manifest = json.load(f)
    for key in ("name", "displayName", "description", "version", "publisher", "license", "icon", "repository",
                "engines"):
        if not manifest.get(key):
            raise SystemExit(f"VS Code package.json: {key} is missing or empty")
    contributed = manifest["contributes"]["themes"]
    if len(contributed) != len(themes):
        raise SystemExit(f"VS Code package.json: {len(contributed)} themes for {len(themes)} themes")
    for entry in contributed:
        with open(os.path.join(directory, entry["path"])) as f:
            data = json.load(f)
        if data["name"] != entry["label"] or (data["type"] == "dark") != (entry["uiTheme"] == "vs-dark"):
            raise SystemExit(f"VS Code theme {entry['path']} does not match its label or uiTheme")
    for name in ("README.md", "CHANGELOG.md", "LICENSE", manifest["icon"]):
        if not os.path.isfile(os.path.join(directory, name)):
            raise SystemExit(f"VS Code extension: {name} is missing")


def pack_vsix(directory, themes):
    """Packs the extension with the pinned vsce and returns the .vsix path."""
    vsce = os.path.join(VSCODE_TOOLS, "node_modules", ".bin", "vsce")
    if not os.path.isfile(vsce):
        npm = shutil.which("npm")
        if not npm:
            raise SystemExit("build: --vsix needs Node.js and npm")
        subprocess.run([npm, "ci", "--no-audit", "--no-fund"], cwd=VSCODE_TOOLS, check=True)
    vsix = os.path.join(OUT, f"{VSCODE_NAME}-vscode-{VERSION}.vsix")
    # stdin is closed so that a vsce confirmation prompt fails the build instead of waiting for input
    subprocess.run([vsce, "package", "--no-dependencies", "--out", vsix], cwd=directory, check=True,
                   stdin=subprocess.DEVNULL)
    with zipfile.ZipFile(vsix) as z:
        packed = {n for n in z.namelist() if n.startswith("extension/themes/")}
    if len(packed) != len(themes):
        raise SystemExit(f"{vsix}: {len(packed)} theme files for {len(themes)} themes")
    return vsix


def sublime_readme(families):
    """The package's README. Links are absolute: Package Control shows it on packagecontrol.io."""
    rows = "\n".join(f"| [{f.FAMILY}]({VENDOR_URL}/tree/master/themes/{heritage.folder(f)}) "
                     f"| {', '.join(t['palette']['name'] for t in f.THEMES)} | {f.BLURB} |" for f in families)
    count = sum(len(f.THEMES) for f in families)
    return f"""# Heritage Themes

{DESCRIPTION} {count} dark and light colour schemes in {len(families)} families; each family maps the named \
colours of one tradition to syntax roles.

Each colour scheme colours the editor. The UI theme of the same name colours the sidebar, tabs, panels, status bar \
and popups to match; it extends Sublime Text's built-in Adaptive theme. A scheme also works on its own with any \
other theme.

## Install

Open the Command Palette (`Ctrl+Shift+P`; `Cmd+Shift+P` on macOS), run **Package Control: Install Package** and \
choose **{SUBLIME_NAME}**. To install without Package Control, download `heritage-themes-sublime-<version>.sublime-package` \
from the [latest release]({VENDOR_URL}/releases/latest) into the `Installed Packages` folder, which **Preferences: \
Browse Packages** shows beside `Packages`.

## Choose a scheme and theme

Run **UI: Select Color Scheme** and choose a scheme under **{SUBLIME_NAME}**, then **UI: Select Theme** and choose \
the theme of the same name. The theme carries its scheme's colours, so pair each theme with its own scheme. To \
follow the system appearance, set both settings to `auto` and name a pair for each appearance in **Preferences: \
Settings**:

```json
{{
    "color_scheme": "auto",
    "dark_color_scheme": "Packages/{SUBLIME_NAME}/Holi Night.sublime-color-scheme",
    "light_color_scheme": "Packages/{SUBLIME_NAME}/Kalamkari Cotton (Light).sublime-color-scheme",
    "theme": "auto",
    "dark_theme": "Holi Night.sublime-theme",
    "light_theme": "Kalamkari Cotton (Light).sublime-theme"
}}
```

Every colour is a variable at the top of its scheme file. To change one, copy the scheme file into `Packages/User` \
under the same name and override the variable there.

## Languages

The colours follow the scope names of Sublime Text's built-in syntaxes. A language that Sublime Text does not ship, \
such as Kotlin, TOML or Vue, takes the scopes of the syntax package you install for it, and its colours depend on \
how closely that package follows [Sublime Text's scope naming](https://www.sublimetext.com/docs/scope_naming.html).

## Schemes

| Family | Schemes | Tradition |
| --- | --- | --- |
{rows}

Each family's page describes its colour tradition. The same themes are available for JetBrains IDEs and VS Code: see \
[Heritage Themes on GitHub]({VENDOR_URL}).

Report a problem or suggest a tradition on the [issue tracker]({VENDOR_URL}/issues). Include the scheme, Sublime Text \
build, syntax and a screenshot.
"""


def build_sublime(families, themes):
    """Writes the Sublime Text package's files to build/sublime and returns that folder."""
    directory = os.path.join(OUT, "sublime")
    os.makedirs(directory)
    names = [heritage.sublime.basename(t["name"]) for t in themes]
    if len(names) != len(set(names)):
        raise SystemExit("sublime: two themes have the same file name")
    for name, t in zip(names, themes):
        for filename, document in ((f"{name}.sublime-color-scheme", t["sublime"]),
                                   (f"{name}.sublime-theme", t["sublime_theme"]),
                                   (f"Widget - {name}.sublime-settings", heritage.sublime.widget_settings())):
            with open(os.path.join(directory, filename), "w") as f:
                json.dump(document, f, indent=2, ensure_ascii=False)
                f.write("\n")
    with open(os.path.join(directory, "README.md"), "w") as f:
        f.write(sublime_readme(families))
    shutil.copy(SUBLIME_CHANGELOG, os.path.join(directory, "CHANGELOG.md"))
    shutil.copy(os.path.join(ROOT, "LICENSE"), os.path.join(directory, "LICENSE"))
    return directory


def validate_sublime(directory, themes):
    """Fails the build when a colour scheme is malformed, names an undefined variable or has a rule that is
    unreadable on the background, or when a scheme lacks its UI theme and widget settings."""
    for name in ("README.md", "CHANGELOG.md", "LICENSE"):
        if not os.path.isfile(os.path.join(directory, name)):
            raise SystemExit(f"Sublime package: {name} is missing")
    schemes = sorted(n for n in os.listdir(directory) if n.endswith(".sublime-color-scheme"))
    if len(schemes) != len(themes):
        raise SystemExit(f"Sublime package: {len(schemes)} colour schemes for {len(themes)} themes")
    for name in schemes:
        validate_sublime_theme(directory, name.removesuffix(".sublime-color-scheme"))
    for name in schemes:
        with open(os.path.join(directory, name)) as f:
            scheme = json.load(f)
        variables, colours = scheme["variables"], []
        def colour(value):
            match = heritage.sublime.VARIABLE.fullmatch(value)
            if match and match.group(1) not in variables:
                raise SystemExit(f"{name}: names undefined variable {match.group(1)}")
            colours.append(heritage.sublime.resolve(value, scheme))
            return colours[-1]
        for key, value in scheme["globals"].items():
            if not key.endswith("_options"):
                colour(value)
        background = colour(scheme["globals"]["background"])
        for rule in scheme["rules"]:
            if not rule.get("scope") or not rule.get("foreground"):
                raise SystemExit(f"{name}: a rule needs a scope and a foreground: {rule}")
            if not set(rule.get("font_style", "").split()) <= SUBLIME_FONT_STYLES:
                raise SystemExit(f"{name}: unknown font_style in {rule}")
            foreground = colour(rule["foreground"])
            minimum = 3 if foreground == variables["comment"] else 4.5
            ratio = contrast(foreground[1:], background[1:])
            if ratio < minimum:
                raise SystemExit(f"{name}: {rule['scope']} is {ratio:.2f}:1 on the background, needs {minimum}:1")
        for value in colours:
            if not re.fullmatch(r"#[0-9A-Fa-f]{6}([0-9A-Fa-f]{2})?", value):
                raise SystemExit(f"{name}: {value} is not a hex colour")


def validate_sublime_theme(directory, name):
    """Fails the build when the UI theme or widget settings of the scheme of that name are missing or malformed."""
    for filename in (f"{name}.sublime-theme", f"Widget - {name}.sublime-settings"):
        if not os.path.isfile(os.path.join(directory, filename)):
            raise SystemExit(f"Sublime package: {filename} is missing")
    with open(os.path.join(directory, f"{name}.sublime-theme")) as f:
        theme = json.load(f)
    if theme.get("extends") != "Adaptive.sublime-theme" or not theme.get("rules"):
        raise SystemExit(f"{name}.sublime-theme: must extend Adaptive.sublime-theme and add rules")
    for rule in theme["rules"]:
        if not rule.get("class"):
            raise SystemExit(f"{name}.sublime-theme: a rule needs a class: {rule}")
        for key, value in rule.items():
            if (key.endswith(("fg", "tint", "color", "_modifier")) or key == "bg") and value != "transparent" \
                    and not re.fullmatch(r"#[0-9A-F]{6}", value):
                raise SystemExit(f"{name}.sublime-theme: {key} {value!r} is not a hex colour")


def pack_sublime(directory):
    """Zips the package into a .sublime-package, which Sublime Text loads from Installed Packages, and returns its
    path. The entries are sorted and carry a fixed time, so the same sources give the same bytes."""
    package = os.path.join(OUT, f"{VSCODE_NAME}-sublime-{VERSION}.sublime-package")
    with zipfile.ZipFile(package, "w", zipfile.ZIP_DEFLATED) as z:
        for name in sorted(os.listdir(directory)):
            info = zipfile.ZipInfo(name, date_time=(2020, 1, 1, 0, 0, 0))
            info.compress_type, info.external_attr = zipfile.ZIP_DEFLATED, 0o644 << 16
            with open(os.path.join(directory, name), "rb") as f:
                z.writestr(info, f.read())
    return package


def main():
    parser = argparse.ArgumentParser(description="Build the JetBrains plugin, the VS Code extension and the Sublime "
                                                 "Text package.")
    parser.add_argument("--vsix", action="store_true", help="also pack the VS Code extension with vsce")
    args = parser.parse_args()
    families = heritage.load_families()
    themes = [t for f in families for t in heritage.generate(f)]
    for key in ("slug", "id", "name"):
        values = [t[key] for t in themes]
        if len(values) != len(set(values)):
            raise SystemExit(f"duplicate theme {key}")
    for f in families:
        for t in f.THEMES:
            check_frame(t["palette"])
            check_contrast(t["palette"])
    for t in themes:
        check_references(t)

    shutil.rmtree(OUT, ignore_errors=True)
    os.makedirs(os.path.join(OUT, "schemes"))
    jar = os.path.join(OUT, f"heritage-themes-{VERSION}.jar")
    with zipfile.ZipFile(jar, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("META-INF/plugin.xml", plugin_xml(families, themes))
        for icon in PLUGIN_ICONS:
            z.write(os.path.join(ROOT, "assets", icon), f"META-INF/{icon}")
        for t in themes:
            z.writestr(f"themes/{t['slug']}.xml", t["scheme"])
            z.writestr(f"themes/{t['slug']}.theme.json", json.dumps(t["theme"], indent=2))
            with open(os.path.join(OUT, "schemes", f"{t['name']}.icls"), "w") as f:
                f.write(t["scheme"])
    validate(jar, themes)
    archive = os.path.join(OUT, f"heritage-themes-{VERSION}.zip")
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(jar, f"heritage-themes/lib/{os.path.basename(jar)}")
    print(f"{archive}: {len(themes)} themes")
    extension = build_vscode(families, themes)
    validate_vscode(extension, themes)
    print(f"{extension}: {len(themes)} themes", flush=True)
    package = build_sublime(families, themes)
    validate_sublime(package, themes)
    print(f"{pack_sublime(package)}: {len(themes)} themes", flush=True)
    if args.vsix:
        print(f"{pack_vsix(extension, themes)}: {len(themes)} themes")


if __name__ == "__main__":
    main()
