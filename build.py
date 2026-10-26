"""Builds the Heritage Themes JetBrains plugin, VS Code extension, Visual Studio extension, Sublime Text package, Zed
extension, Neovim plugin, Notepad++ themes and Xcode themes from every theme folder.

A theme folder is any directory in themes/ containing a theme.py (see heritage/__init__.py).

Usage: python3 build.py [--vsix]
  --vsix  also pack the VS Code extension into a .vsix with vsce, pinned in scripts/vscode and installed there
          with npm ci on first use; needs Node.js 22 or later and npm

Output goes to build/.
"""
import argparse, html, json, os, plistlib, re, shutil, subprocess, tomllib, zipfile
import xml.etree.ElementTree as ET

import heritage

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "build")
CHANGELOG = os.path.join(ROOT, "CHANGELOG.md")
# One version for the JetBrains plugin, the VS Code extension, the Visual Studio extension, the Sublime Text package,
# the Zed extension, the Neovim plugin, the Notepad++ themes and the Xcode themes. A release publishes each product
# whose changelog has a section for it.
VERSION = "1.4.0"
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
ZED_CHANGELOG = os.path.join(ROOT, "zed", "CHANGELOG.md")
ZED_ID = "heritage-theme"  # the extension's ID in Zed's extension registry
ZED_REPOSITORY_URL = "https://github.com/heritage-themes/heritage-themes-zed"
ZED_HEX = re.compile(r"#[0-9A-F]{6}([0-9A-F]{2})?")
NVIM_CHANGELOG = os.path.join(ROOT, "nvim", "CHANGELOG.md")
NVIM_NAME = "heritage-themes.nvim"  # the plugin's repository, which plugin managers install from
NVIM_REPOSITORY_URL = f"https://github.com/heritage-themes/{NVIM_NAME}"
NVIM_HEX = re.compile(r"#[0-9A-F]{6}")
NOTEPADPP_CHANGELOG = os.path.join(ROOT, "notepadpp", "CHANGELOG.md")
NOTEPADPP_NAME = "heritage-themes-notepadpp"  # the folder in the zip
NOTEPADPP_PROLOG = '<?xml version="1.0" encoding="UTF-8" ?>'  # Notepad++'s Themes Collection requires it first
NOTEPADPP_HEX = re.compile(r"[0-9A-F]{6}")
XCODE_CHANGELOG = os.path.join(ROOT, "xcode", "CHANGELOG.md")
XCODE_NAME = "heritage-themes-xcode"  # the folder in the zip
XCODE_THEMES = "~/Library/Developer/Xcode/UserData/FontAndColorThemes"  # where Xcode looks for a user's themes
XCODE_FONT = re.compile(r"[.\w-]+ - \d+\.\d")
WINDOWS_NAME = re.compile(r'[^<>:"/\\|?*\x00-\x1f]+(?<![ .])')  # a file name that Windows accepts
# The extension's VSIX identity, which Visual Studio matches installed extensions and updates by, and which the
# Marketplace requires to be unique across all publishers; its internal name on the Marketplace, which also names the
# .vsix; and its display name, which differs from the VS Code extension's so that the two listings do not clash. The
# identity and the internal name are fixed once published.
VISUALSTUDIO_ID = "HeritageThemes.0e5e1c82-df1d-4bf5-b6f9-366c6f0bb488"
VISUALSTUDIO_ITEM = "heritage-themes-visualstudio"
VISUALSTUDIO_NAME = "Heritage Themes for Visual Studio"
VISUALSTUDIO_ICON = os.path.join(ROOT, "assets", "pluginIcon_dark.png")
# The editors the themes ship to, as the READMEs name them.
EDITORS = ("JetBrains IDEs", "VS Code", "Visual Studio", "Sublime Text", "Zed", "Neovim", "Notepad++", "Xcode")
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


def elsewhere(editor):
    """The editors other than editor, for the README of its product to name the others."""
    others = [e for e in EDITORS if e != editor]
    return ", ".join(others[:-1]) + " and " + others[-1]


def write_text(path, text):
    """Writes text as UTF-8 with LF line ends, so that the build writes the same bytes on every OS."""
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


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
    with open(CHANGELOG, encoding="utf-8") as f:
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

Each family's page describes its colour tradition. The same themes are available for {elsewhere("VS Code")}: see \
[Heritage Themes on GitHub]({VENDOR_URL}).

Report a problem or suggest a tradition on the [issue tracker]({VENDOR_URL}/issues). Include the theme, VS Code version, language and a screenshot.
"""


def build_vscode(families, themes):
    """Writes the VS Code extension's files to build/vscode and returns that folder."""
    directory = os.path.join(OUT, "vscode")
    os.makedirs(os.path.join(directory, "themes"))
    write_text(os.path.join(directory, "package.json"),
               json.dumps(vscode_manifest(themes), indent=2, ensure_ascii=False))
    write_text(os.path.join(directory, "README.md"), vscode_readme(families))
    shutil.copy(VSCODE_CHANGELOG, os.path.join(directory, "CHANGELOG.md"))
    shutil.copy(os.path.join(ROOT, "LICENSE"), os.path.join(directory, "LICENSE"))
    shutil.copy(VSCODE_ICON, os.path.join(directory, "icon.png"))
    for t in themes:
        write_text(os.path.join(directory, "themes", f"{t['slug']}-color-theme.json"),
                   json.dumps(t["vscode"], indent=2, ensure_ascii=False))
    return directory


def validate_vscode(directory, themes):
    """Fails the build when the extension manifest is incomplete or a contributed theme is missing or malformed."""
    with open(os.path.join(directory, "package.json"), encoding="utf-8") as f:
        manifest = json.load(f)
    for key in ("name", "displayName", "description", "version", "publisher", "license", "icon", "repository",
                "engines"):
        if not manifest.get(key):
            raise SystemExit(f"VS Code package.json: {key} is missing or empty")
    contributed = manifest["contributes"]["themes"]
    if len(contributed) != len(themes):
        raise SystemExit(f"VS Code package.json: {len(contributed)} themes for {len(themes)} themes")
    for entry in contributed:
        with open(os.path.join(directory, entry["path"]), encoding="utf-8") as f:
            data = json.load(f)
        if data["name"] != entry["label"] or (data["type"] == "dark") != (entry["uiTheme"] == "vs-dark"):
            raise SystemExit(f"VS Code theme {entry['path']} does not match its label or uiTheme")
    for name in ("README.md", "CHANGELOG.md", "LICENSE", manifest["icon"]):
        if not os.path.isfile(os.path.join(directory, name)):
            raise SystemExit(f"VS Code extension: {name} is missing")


def pack_vsix(directory, themes):
    """Packs the extension with the pinned vsce and returns the .vsix path."""
    vsce = os.path.join(VSCODE_TOOLS, "node_modules", ".bin", "vsce.cmd" if os.name == "nt" else "vsce")
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

Each family's page describes its colour tradition. The same themes are available for {elsewhere("Sublime Text")}: \
see [Heritage Themes on GitHub]({VENDOR_URL}).

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
            write_text(os.path.join(directory, filename), json.dumps(document, indent=2, ensure_ascii=False) + "\n")
    write_text(os.path.join(directory, "README.md"), sublime_readme(families))
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
        with open(os.path.join(directory, name), encoding="utf-8") as f:
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
    with open(os.path.join(directory, f"{name}.sublime-theme"), encoding="utf-8") as f:
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


def zip_entry(name):
    """A zip entry for a file with a fixed time and Unix permissions, so that the same sources give the same entries on
    every OS."""
    info = zipfile.ZipInfo(name, date_time=(2020, 1, 1, 0, 0, 0))
    info.compress_type, info.external_attr, info.create_system = zipfile.ZIP_DEFLATED, 0o644 << 16, 3
    return info


def pack_sublime(directory):
    """Zips the package into a .sublime-package, which Sublime Text loads from Installed Packages, and returns its
    path. The entries are sorted and carry a fixed time, so the same sources give the same bytes."""
    package = os.path.join(OUT, f"{VSCODE_NAME}-sublime-{VERSION}.sublime-package")
    with zipfile.ZipFile(package, "w", zipfile.ZIP_DEFLATED) as z:
        for name in sorted(os.listdir(directory)):
            info = zip_entry(name)
            with open(os.path.join(directory, name), "rb") as f:
                z.writestr(info, f.read())
    return package


def zed_manifest():
    return f"""id = "{ZED_ID}"
name = "Heritage Themes"
version = "{VERSION}"
schema_version = 1
authors = ["Heritage Themes"]
description = "{DESCRIPTION}"
repository = "{ZED_REPOSITORY_URL}"
"""


def zed_readme(families):
    """The extension repository's README. Links are absolute, as the repository holds the build only."""
    rows = "\n".join(f"| [{f.FAMILY}]({VENDOR_URL}/tree/master/themes/{heritage.folder(f)}) "
                     f"| {', '.join(t['palette']['name'] for t in f.THEMES)} | {f.BLURB} |" for f in families)
    count = sum(len(f.THEMES) for f in families)
    return f"""# Heritage Themes

{DESCRIPTION} {count} dark and light themes in {len(families)} families; each family maps the named colours of one \
tradition to syntax roles.

This repository holds the Zed extension that [Heritage Themes]({VENDOR_URL}) generates for each release. Report \
problems and make changes there.

## Install

Open the Extensions page (**zed: extensions**), search for **Heritage Themes** and install it. Choose a theme with \
**theme selector: toggle** (`Ctrl+K Ctrl+T`; `Cmd+K Cmd+T` on macOS). To follow the system appearance, name a theme \
for each appearance in your settings:

```json
{{
  "theme": {{
    "mode": "system",
    "dark": "Holi Night",
    "light": "Kalamkari Cotton (Light)"
  }}
}}
```

## Languages

Zed colours code by the Tree-sitter captures of each language's queries. A capture names the construct, not the \
language, so the themes colour a construct alike in every language: annotations, Rust attributes and HTML attribute \
names share the annotation colour, and keys in YAML, TOML and JSON take the field colour.

## Themes

| Family | Themes | Tradition |
| --- | --- | --- |
{rows}

Each family's page describes its colour tradition. The same themes are available for {elsewhere("Zed")}: see \
[Heritage Themes on GitHub]({VENDOR_URL}).

Report a problem or suggest a tradition on the [issue tracker]({VENDOR_URL}/issues). Include the theme, Zed version, \
language and a screenshot.
"""


def build_zed(families):
    """Writes the Zed extension's files to build/zed and returns that folder."""
    directory = os.path.join(OUT, "zed")
    os.makedirs(os.path.join(directory, "themes"))
    write_text(os.path.join(directory, "extension.toml"), zed_manifest())
    for family in families:
        document = heritage.zed.family(family.FAMILY, [t["palette"] for t in family.THEMES])
        write_text(os.path.join(directory, "themes", f"{heritage.folder(family)}.json"),
                   json.dumps(document, indent=2, ensure_ascii=False) + "\n")
    write_text(os.path.join(directory, "README.md"), zed_readme(families))
    shutil.copy(ZED_CHANGELOG, os.path.join(directory, "CHANGELOG.md"))
    shutil.copy(os.path.join(ROOT, "LICENSE"), os.path.join(directory, "LICENSE"))
    return directory


def validate_zed(directory, themes):
    """Fails the build when the extension manifest is incomplete, or when a theme is malformed, has a colour that is not
    hex or has a syntax colour that is unreadable on the editor background."""
    for name in ("README.md", "CHANGELOG.md", "LICENSE"):
        if not os.path.isfile(os.path.join(directory, name)):
            raise SystemExit(f"Zed extension: {name} is missing")
    with open(os.path.join(directory, "extension.toml"), "rb") as f:
        manifest = tomllib.load(f)
    for key in ("id", "name", "version", "schema_version", "authors", "description", "repository"):
        if not manifest.get(key):
            raise SystemExit(f"Zed extension.toml: {key} is missing or empty")
    if manifest["version"] != VERSION:
        raise SystemExit(f"Zed extension.toml: version {manifest['version']} is not {VERSION}")
    names = {t["name"]: t["dark"] for t in themes}
    found = []
    for filename in sorted(os.listdir(os.path.join(directory, "themes"))):
        with open(os.path.join(directory, "themes", filename), encoding="utf-8") as f:
            family = json.load(f)
        for theme in family["themes"]:
            name, style = theme["name"], theme["style"]
            found.append(name)
            if name not in names or (theme["appearance"] == "dark") != names[name]:
                raise SystemExit(f"Zed {filename}: {name} does not match a palette's name or appearance")
            colours = [v for k, v in style.items()
                       if k not in ("syntax", "players", "accents", "background.appearance")]
            colours += style["accents"] + [v for player in style["players"] for v in player.values()]
            colours += [s["color"] for s in style["syntax"].values()]
            for value in colours:
                if value is not None and not ZED_HEX.fullmatch(value):
                    raise SystemExit(f"Zed {filename}: {name} has {value!r}, which is not a hex colour")
            background = style["editor.background"][1:]
            for key, s in style["syntax"].items():
                if not set(s) <= {"color", "font_style", "font_weight"} or s.get("font_style", "italic") != "italic" \
                        or s.get("font_weight", 700) != 700:
                    raise SystemExit(f"Zed {filename}: {name} has an unknown syntax style for {key}: {s}")
                minimum = 3 if key.startswith("comment") else 4.5
                ratio = contrast(s["color"][1:], background)
                if ratio < minimum:
                    raise SystemExit(f"Zed {filename}: {name} {key} is {ratio:.2f}:1 on the editor background, "
                                     f"needs {minimum}:1")
    if sorted(found) != sorted(names):
        raise SystemExit(f"Zed extension: {len(found)} themes for {len(names)} themes")


def pack_zed(directory):
    """Zips the extension into a folder that Zed installs with zed: install dev extension, and returns the zip's path.
    The entries are sorted and carry a fixed time, so the same sources give the same bytes."""
    return pack_folder(directory, os.path.join(OUT, f"{VSCODE_NAME}-zed-{VERSION}.zip"), ZED_ID)


def pack_folder(directory, package, folder):
    """Zips the files under directory into package, in a folder of that name, and returns package."""
    with zipfile.ZipFile(package, "w", zipfile.ZIP_DEFLATED) as z:
        for root, folders, files in os.walk(directory):
            folders.sort()
            for name in sorted(files):
                path = os.path.join(root, name)
                with open(path, "rb") as f:
                    z.writestr(zip_entry(os.path.join(folder, os.path.relpath(path, directory))), f.read())
    return package


def nvim_readme(families):
    """The plugin repository's README. Links are absolute, as the repository holds the build only."""
    rows = "\n".join(f"| [{f.FAMILY}]({VENDOR_URL}/tree/master/themes/{heritage.folder(f)}) "
                     f"| {', '.join(f'`{heritage.nvim.name(t)}`' for t in f.THEMES)} | {f.BLURB} |" for f in families)
    count = sum(len(f.THEMES) for f in families)
    repository = NVIM_REPOSITORY_URL.removeprefix("https://github.com/")
    return f"""# Heritage Themes

{DESCRIPTION} {count} dark and light colour schemes in {len(families)} families; each family maps the named colours \
of one tradition to syntax roles.

This repository holds the Neovim plugin that [Heritage Themes]({VENDOR_URL}) generates for each release. Report \
problems and make changes there.

## Install

The plugin needs Neovim 0.10 or later and a terminal with 24-bit colour, for which Neovim turns on `termguicolors` \
itself.

With [lazy.nvim](https://github.com/folke/lazy.nvim):

```lua
{{
  "{repository}",
  lazy = false,
  priority = 1000,
  config = function()
    vim.cmd.colorscheme("heritage-holi-night")
  end,
}}
```

With `vim.pack`, built into Neovim 0.12:

```lua
vim.pack.add({{ "{NVIM_REPOSITORY_URL}" }})
vim.cmd.colorscheme("heritage-holi-night")
```

Without a plugin manager, unzip `heritage-themes-nvim-<version>.zip` from the \
[latest release]({VENDOR_URL}/releases/latest) into `~/.local/share/nvim/site/pack/heritage/start/`.

Run `:colorscheme heritage-` and press `Tab` to list the schemes. Each scheme sets `background` to its own \
brightness.

## What is coloured

Each scheme colours the editor, Tree-sitter captures, LSP semantic tokens, diagnostics, the status line, tab line, \
window bar, floating windows, the completion menu, diff mode and the terminal. It also colours the signs of \
[gitsigns.nvim](https://github.com/lewis6991/gitsigns.nvim), and ships a \
[lualine](https://github.com/nvim-lualine/lualine.nvim) theme of the same name, which lualine's default `auto` theme \
loads.

Code is coloured by Tree-sitter once a parser for its language is installed, for example with \
[nvim-treesitter](https://github.com/nvim-treesitter/nvim-treesitter). The groups follow the capture names of \
nvim-treesitter's queries, so a construct takes one colour in every language: keys in YAML, TOML and JSON take the \
field colour, and decorators, annotations and attributes the annotation colour.

To change a group, set it in a `ColorScheme` autocommand, so that it survives switching schemes:

```lua
vim.api.nvim_create_autocmd("ColorScheme", {{
  pattern = "heritage-*",
  callback = function()
    vim.api.nvim_set_hl(0, "Comment", {{ fg = "#808080", italic = true }})
  end,
}})
```

## Colour schemes

| Family | Colour schemes | Tradition |
| --- | --- | --- |
{rows}

Each family's page describes its colour tradition. The same themes are available for {elsewhere("Neovim")}: see \
[Heritage Themes on GitHub]({VENDOR_URL}).

Report a problem or suggest a tradition on the [issue tracker]({VENDOR_URL}/issues). Include the colour scheme, \
Neovim version, language and a screenshot.
"""


def build_nvim(families):
    """Writes the Neovim plugin's files to build/nvim and returns that folder."""
    directory = os.path.join(OUT, "nvim")
    os.makedirs(os.path.join(directory, "colors"))
    os.makedirs(os.path.join(directory, "lua", "lualine", "themes"))
    for family in families:
        source = f"{VENDOR_URL}/tree/master/themes/{heritage.folder(family)}"
        for t in family.THEMES:
            scheme = heritage.nvim.name(t)
            write_text(os.path.join(directory, "colors", f"{scheme}.lua"),
                       heritage.nvim.colorscheme(t["palette"], scheme, source))
            write_text(os.path.join(directory, "lua", "lualine", "themes", f"{scheme}.lua"),
                       heritage.nvim.lualine_theme(t["palette"], source))
    write_text(os.path.join(directory, "README.md"), nvim_readme(families))
    shutil.copy(NVIM_CHANGELOG, os.path.join(directory, "CHANGELOG.md"))
    shutil.copy(os.path.join(ROOT, "LICENSE"), os.path.join(directory, "LICENSE"))
    return directory


def validate_nvim(directory, families):
    """Fails the build when a colour scheme or lualine theme is missing, a highlight definition is malformed or names an
    undefined group, or a text colour is unreadable on the background it is drawn on."""
    for name in ("README.md", "CHANGELOG.md", "LICENSE"):
        if not os.path.isfile(os.path.join(directory, name)):
            raise SystemExit(f"Neovim plugin: {name} is missing")
    expected = set()
    for family in families:
        for t in family.THEMES:
            scheme, p = heritage.nvim.name(t), t["palette"]
            if not re.fullmatch(r"heritage(-[a-z]+)+", scheme):
                raise SystemExit(f"Neovim: {scheme} is not a lower-case ASCII colour scheme name")
            expected.add(scheme)
            groups = heritage.nvim.highlights(p)
            for group, definition in groups.items():
                if not re.fullmatch(r"[A-Za-z0-9_.@-]+", group):
                    raise SystemExit(f"Neovim {scheme}: {group!r} is not a valid group name")
                for key, value in definition.items():
                    valid = (key in heritage.nvim.COLOURS and NVIM_HEX.fullmatch(value)) or \
                            (key in heritage.nvim.FLAGS and value is True) or \
                            (key == "blend" and isinstance(value, int) and 0 <= value <= 100)
                    if not valid:
                        raise SystemExit(f"Neovim {scheme}: {group} has {key} = {value!r}")
                if "fg" in definition and group not in heritage.nvim.DECORATIVE:
                    background = definition.get("bg", groups["Normal"]["bg"])
                    minimum = 3 if group in heritage.nvim.LOW_CONTRAST else 4.5
                    ratio = contrast(definition["fg"][1:], background[1:])
                    if ratio < minimum:
                        raise SystemExit(f"Neovim {scheme}: {group} is {ratio:.2f}:1 on its background, "
                                         f"needs {minimum}:1")
            for mode, sections in heritage.nvim.lualine(p).items():
                for section, colours in sections.items():
                    ratio = contrast(colours["fg"][1:], colours["bg"][1:])
                    if ratio < 4.5:
                        raise SystemExit(f"Neovim {scheme}: lualine {mode}.{section} is {ratio:.2f}:1, needs 4.5:1")
            terminal = heritage.nvim.terminal(p)
            if len(terminal) != 16 or not all(NVIM_HEX.fullmatch(v) for v in terminal):
                raise SystemExit(f"Neovim {scheme}: the terminal needs 16 hex colours")
            with open(os.path.join(directory, "colors", f"{scheme}.lua"), encoding="utf-8") as f:
                if f"vim.g.colors_name = \"{scheme}\"" not in f.read():
                    raise SystemExit(f"Neovim colors/{scheme}.lua does not set its colors_name")
    for folder in ("colors", os.path.join("lua", "lualine", "themes")):
        found = {name.removesuffix(".lua") for name in os.listdir(os.path.join(directory, folder))}
        if found != expected:
            raise SystemExit(f"Neovim {folder}: {len(found)} files for {len(expected)} themes")


def pack_nvim(directory):
    """Zips the plugin into a folder that Neovim loads from a pack/*/start directory, and returns the zip's path. The
    entries are sorted and carry a fixed time, so the same sources give the same bytes."""
    return pack_folder(directory, os.path.join(OUT, f"{VSCODE_NAME}-nvim-{VERSION}.zip"), NVIM_NAME)


def notepadpp_readme(families):
    """The README in the zip. Links are absolute, as the zip holds the build only."""
    rows = "\n".join(f"| [{f.FAMILY}]({VENDOR_URL}/tree/master/themes/{heritage.folder(f)}) "
                     f"| {', '.join(t['palette']['name'] for t in f.THEMES)} | {f.BLURB} |" for f in families)
    count = sum(len(f.THEMES) for f in families)
    model = heritage.notepadpp.MODEL
    return f"""# Heritage Themes for Notepad++

{DESCRIPTION} {count} dark and light themes in {len(families)} families; each family maps the named colours of one \
tradition to syntax roles.

## Install

1. Copy the files in `themes` into the `themes` folder of your Notepad++ settings: `%AppData%\\Notepad++\\themes` \
for an installed Notepad++, or the `themes` folder beside `notepad++.exe` for a portable one. Create the folder if it \
does not exist.
2. Restart Notepad++ and choose a theme under **Settings | Style Configurator… | Select theme**.

**Settings | Import | Import Style Themes…** installs the files you select instead, into the `themes` folder of the \
Notepad++ installation, which can need Notepad++ to run as administrator.

Notepad++ keeps one theme for Light Mode and one for Dark Mode, set under **Settings | Preferences… | Dark Mode**: \
choose a dark theme while Dark Mode is on and a light theme while it is off.

## What is coloured

Each theme sets every style of every language that Notepad++ {model["notepad++"]} lists, and the editor around the \
text: the caret, current line, selection, margins, fold markers, find and mark highlights, brace matching, the \
document map and the bar that marks the active tab. In Light Mode it also colours the text of the tabs and the \
background of the inactive ones. Notepad++ draws the menu bar, toolbar, dialogs and, in Dark Mode, the tabs from its \
own Dark Mode colours, which a theme cannot set; to bring them closer to a theme, choose the **Customized** tone \
under **Settings | Preferences… | Dark Mode**.

## Languages

Notepad++ colours each language with its own lexer, so the themes give each lexer's styles the role of the construct \
they mark: keywords, strings, numbers, types, functions, fields, annotations and comments take the same colours as \
in the other editors. Notepad++ has no lexer for Kotlin or Groovy, which open as plain text, and colours Markdown \
with a user-defined language that keeps its own colours. A style that a later Notepad++ adds takes the theme's text \
colour until a release of the themes sets it.

## Themes

| Family | Themes | Tradition |
| --- | --- | --- |
{rows}

Each family's page describes its colour tradition. The same themes are available for {elsewhere("Notepad++")}: see \
[Heritage Themes on GitHub]({VENDOR_URL}).

Report a problem or suggest a tradition on the [issue tracker]({VENDOR_URL}/issues). Include the theme, Notepad++ \
version, language and a screenshot.
"""


def build_notepadpp(families):
    """Writes the Notepad++ themes to build/notepadpp/themes, one file per theme named as Notepad++ lists it, and
    returns build/notepadpp."""
    directory = os.path.join(OUT, "notepadpp")
    os.makedirs(os.path.join(directory, "themes"))
    for family in families:
        source = f"{VENDOR_URL}/tree/master/themes/{heritage.folder(family)}"
        for t in family.THEMES:
            write_text(os.path.join(directory, "themes", f"{t['palette']['name']}.xml"),
                       heritage.notepadpp.theme(t["palette"], source))
    write_text(os.path.join(directory, "README.md"), notepadpp_readme(families))
    shutil.copy(NOTEPADPP_CHANGELOG, os.path.join(directory, "CHANGELOG.md"))
    shutil.copy(os.path.join(ROOT, "LICENSE"), os.path.join(directory, "LICENSE"))
    return directory


def validate_notepadpp(directory, families):
    """Fails the build when the README, changelog, licence or the file of a theme is missing or a theme is malformed."""
    for name in ("README.md", "CHANGELOG.md", "LICENSE"):
        if not os.path.isfile(os.path.join(directory, name)):
            raise SystemExit(f"Notepad++ themes: {name} is missing")
    expected = set()
    for family in families:
        for t in family.THEMES:
            p = t["palette"]
            if not WINDOWS_NAME.fullmatch(p["name"]):
                raise SystemExit(f"Notepad++: {p['name']!r} is not a Windows file name")
            expected.add(f"{p['name']}.xml")
            validate_notepadpp_theme(os.path.join(directory, "themes", f"{p['name']}.xml"), p)
    found = set(os.listdir(os.path.join(directory, "themes")))
    if found != expected:
        raise SystemExit(f"Notepad++ themes: {len(found)} files for {len(expected)} themes")


def validate_notepadpp_theme(path, p):
    """Fails the build when the theme file does not start with its XML declaration, leaves out or misnames a style of
    notepadpp.json, has a colour that is not hex or a font style that is not one, or has a text style that is
    unreadable on its background."""
    model, name = heritage.notepadpp.MODEL, os.path.basename(path)
    def fail(message):
        raise SystemExit(f"Notepad++ {name}: {message}")
    with open(path, "rb") as f:
        data = f.read()
    if not data.startswith(NOTEPADPP_PROLOG.encode()):
        fail(f"does not start with {NOTEPADPP_PROLOG}")
    root = ET.fromstring(data)
    if root.tag != "NotepadPlus" or root.get("modelDate") != str(model["modelDate"]):
        fail(f"the root is not <NotepadPlus modelDate=\"{model['modelDate']}\">")
    widgets = root.findall("GlobalStyles/WidgetStyle")
    if [(w.get("name"), int(w.get("styleID"))) for w in widgets] != [(w["name"], w["id"]) for w in model["widgets"]]:
        fail("the GlobalStyles are not those of notepadpp.json")
    styles = {w.get("name"): w for w in widgets}
    # The matched brace is a state marker on one character, held to 3:1 as the caret is; the other targets draw it
    # on braceBg in the colour of the bracket.
    pairs = [(widget, styles[widget].get("fgColor"), styles[widget].get("bgColor"), minimum)
             for widget, minimum in (("Default Style", 4.5), ("Brace highlight style", 3), ("Bad brace colour", 4.5),
                                     ("Inactive tabs", 4.5), ("Selected text colour", 4.5))]
    lexers = root.findall("LexerStyles/LexerType")
    if [x.get("name") for x in lexers] != [x["name"] for x in model["lexers"]]:
        fail("the LexerTypes are not those of notepadpp.json")
    for lexer, spec in zip(lexers, model["lexers"]):
        words = lexer.findall("WordsStyle")
        if [(w.get("name"), int(w.get("styleID"))) for w in words] != [(s["name"], s["id"]) for s in spec["styles"]]:
            fail(f"the styles of {spec['name']} are not those of notepadpp.json")
        for w in words:
            if w.get("fgColor") is None or heritage.notepadpp.decorative(spec["name"], w.get("name")):
                continue
            # A style with COLORSTYLE_FOREGROUND alone is drawn on the Default Style's background.
            own = w.get("colorStyle") != str(heritage.notepadpp.COLORSTYLE_FOREGROUND)
            background = w.get("bgColor") if own else styles["Default Style"].get("bgColor")
            minimum = 3 if w.get("fgColor") == p["comment"] else 4.5
            pairs.append((f"{spec['name']} {w.get('name')}", w.get("fgColor"), background, minimum))
    for element in root.iter():
        for key in ("fgColor", "bgColor"):
            if element.get(key) is not None and not NOTEPADPP_HEX.fullmatch(element.get(key)):
                fail(f"{element.get('name')} has {key} {element.get(key)!r}")
        if element.get("fontStyle") not in (None, *map(str, range(8))):
            fail(f"{element.get('name')} has fontStyle {element.get('fontStyle')!r}")
    for style, fg, bg, minimum in pairs:
        ratio = contrast(fg, bg)
        if ratio < minimum:
            fail(f"{style} is {ratio:.2f}:1 on its background, needs {minimum}:1")


def pack_notepadpp(directory):
    """Zips the themes, README, changelog and licence into a folder, and returns the zip's path. A zip keeps the file
    names, which Notepad++ lists the themes by; GitHub would rename loose release files to ASCII without spaces."""
    return pack_folder(directory, os.path.join(OUT, f"{NOTEPADPP_NAME}-{VERSION}.zip"), NOTEPADPP_NAME)


def xcode_readme(families):
    """The README in the zip. Links are absolute, as the zip holds the build only."""
    rows = "\n".join(f"| [{f.FAMILY}]({VENDOR_URL}/tree/master/themes/{heritage.folder(f)}) "
                     f"| {', '.join(t['palette']['name'] for t in f.THEMES)} | {f.BLURB} |" for f in families)
    count = sum(len(f.THEMES) for f in families)
    return f"""# Heritage Themes for Xcode

{DESCRIPTION} {count} dark and light themes in {len(families)} families; each family maps the named colours of one \
tradition to syntax roles.

## Install

Each theme comes as an `.xcworkspacecolortheme` file for Xcode 27 and later, and an `.xccolortheme` file for Xcode 26 \
and earlier.

1. Copy the files in `themes` into `{XCODE_THEMES}`, creating the folder if it does not exist. In Terminal, from the \
unzipped folder:

   ```bash
   mkdir -p {XCODE_THEMES}
   cp themes/* {XCODE_THEMES}/
   ```

2. Restart Xcode. In Xcode 27, choose a theme under **Xcode | Settings… | Appearance | Theme | Choose…**; in \
Xcode 26 and earlier, under **Xcode | Settings… | Themes**.

Xcode keeps one theme for the light appearance and one for the dark appearance: choose a dark theme while Xcode \
appears dark and a light theme while it appears light.

Do not import an `.xccolortheme` file into Xcode 27 with **Import Classic Theme**: Xcode 27 changes its colours as it \
converts it. Choose the `.xcworkspacecolortheme` file of the same name instead.

## What is coloured

In Xcode 27, each theme colours the editor and the toolbar, jump bar and status bar, which Xcode draws in the editor's \
background, and tints the rest of the window. Fonts are a setting of Xcode 27, under **Appearance | Fonts**, which the \
themes leave as they are.

In Xcode 26 and earlier, each theme colours the source editor, the console and the documentation markup that Xcode \
renders, and the markers in the editor's scroll bar; Xcode draws the rest of its window in the colours of the macOS \
appearance. A theme also sets the editor's font: SF Mono, at the weight and size of Xcode's default themes, with \
keywords in bold where the theme's keywords are bold, and comments in italic.

## Languages

Xcode colours Swift with its language service, which tells project and SDK names apart; the themes give both the same \
colour, the one that types, functions, properties and constants take in the other editors. Objective-C, C and C++ \
take these colours in a project, and only their keywords, strings, numbers, comments and preprocessor directives in a \
file that Xcode opens on its own. Xcode colours JavaScript, TypeScript, Python, Java, SQL, HTML, CSS, JSON, YAML, \
TOML and shell scripts with its own grammars, which mark fewer roles, and opens Markdown in a rendered editor that \
takes the theme's text and link colours. It has no grammar for Kotlin, Groovy, Go, Rust, C# or Vue, which open as \
plain text.

## Themes

| Family | Themes | Tradition |
| --- | --- | --- |
{rows}

Each family's page describes its colour tradition. The same themes are available for {elsewhere("Xcode")}: see \
[Heritage Themes on GitHub]({VENDOR_URL}).

Report a problem or suggest a tradition on the [issue tracker]({VENDOR_URL}/issues). Include the theme, Xcode version, \
language and a screenshot.
"""


def build_xcode(families):
    """Writes the Xcode themes to build/xcode/themes, an .xcworkspacecolortheme and an .xccolortheme per theme named as
    Xcode lists it, and returns build/xcode."""
    directory = os.path.join(OUT, "xcode")
    os.makedirs(os.path.join(directory, "themes"))
    for family in families:
        for t in family.THEMES:
            name = t["palette"]["name"]
            for extension, document in ((".xcworkspacecolortheme", heritage.xcode.recipe_document),
                                        (".xccolortheme", heritage.xcode.document)):
                with open(os.path.join(directory, "themes", name + extension), "wb") as f:
                    f.write(document(t["palette"]))
    write_text(os.path.join(directory, "README.md"), xcode_readme(families))
    shutil.copy(XCODE_CHANGELOG, os.path.join(directory, "CHANGELOG.md"))
    shutil.copy(os.path.join(ROOT, "LICENSE"), os.path.join(directory, "LICENSE"))
    return directory


def validate_xcode(directory, families):
    """Fails the build when the README, changelog, licence or a file of a theme is missing, two themes share a recipe
    ID, or a theme file fails validate_xcode_recipe or validate_xcode_theme."""
    for name in ("README.md", "CHANGELOG.md", "LICENSE"):
        if not os.path.isfile(os.path.join(directory, name)):
            raise SystemExit(f"Xcode themes: {name} is missing")
    expected, ids = set(), set()
    for family in families:
        for t in family.THEMES:
            p = t["palette"]
            if not WINDOWS_NAME.fullmatch(p["name"]):
                raise SystemExit(f"Xcode: {p['name']!r} is not a file name that macOS and Windows accept")
            if heritage.xcode.recipe_id(p["name"]) in ids:
                raise SystemExit(f"Xcode: the recipe ID of {p['name']} is not unique")
            ids.add(heritage.xcode.recipe_id(p["name"]))
            expected |= {f"{p['name']}.xcworkspacecolortheme", f"{p['name']}.xccolortheme"}
            validate_xcode_recipe(os.path.join(directory, "themes", f"{p['name']}.xcworkspacecolortheme"), p)
            validate_xcode_theme(os.path.join(directory, "themes", f"{p['name']}.xccolortheme"), p)
    found = set(os.listdir(os.path.join(directory, "themes")))
    if found != expected:
        raise SystemExit(f"Xcode themes: {len(found)} files for {len(expected)} themes")


def validate_xcode_recipe(path, p):
    """Fails the build when the recipe file is malformed, does not set exactly the colour overrides of
    heritage.xcode.RECIPE, has a colour that is not an opaque sRGB colour of its palette role, or has a text colour
    that is unreadable on the editor background."""
    name = os.path.basename(path)
    def fail(message):
        raise SystemExit(f"Xcode {name}: {message}")
    with open(path, encoding="utf-8") as f:
        document = json.load(f)
    if set(document) != {"fileVersion", "recipe", "showsInAllColorSchemes"} or document["fileVersion"] != 1:
        fail("is not a version 1 recipe file")
    recipe = document["recipe"]
    if set(recipe) != {"background", "colorScheme", "palette"} or \
            recipe["colorScheme"] != ("dark" if p["dark"] else "light"):
        fail("does not set the background, palette and its palette's colour scheme")
    palette, overrides = recipe["palette"], recipe["palette"]["colorOverrides"]
    if set(palette) != {"colorOverrides", "primary", "secondary"} or set(overrides) != set(heritage.xcode.RECIPE):
        fail("does not set exactly the tints and colour overrides of heritage.xcode.RECIPE")
    r = dict(p, caret=p.get("caret", p["gold"]))
    colours = {"background": (recipe["background"], "customColor", "bg"),
               "primary": (palette["primary"], "custom", heritage.xcode.PRIMARY),
               "secondary": (palette["secondary"], "custom", heritage.xcode.SECONDARY),
               **{key: (overrides[key], kind, role) for key, (kind, role) in heritage.xcode.RECIPE.items()}}
    hexes = {}
    for key, (holder, kind, role) in colours.items():
        if set(holder) != {kind}:
            fail(f"{key} is not a {kind}")
        value = holder[kind]
        if set(value) != {"chroma", "gamut", "hue", "lightness", "opacity"} or value["gamut"] != "sRGB" \
                or value["opacity"] != 1:
            fail(f"{key} is not an opaque sRGB colour")
        hexes[key] = heritage.xcode.srgb(value["lightness"]["exact"], value["chroma"]["exact"], value["hue"]["radians"])
        if hexes[key] != r[role]:
            fail(f"{key} is #{hexes[key]}, not #{r[role]} of {role}")
    for key, (kind, role) in heritage.xcode.RECIPE.items():
        if kind == "color" and key != "invisibles":
            minimum = 3 if key in ("comment", "insertionPointColor") else 4.5
            ratio = contrast(hexes[key], hexes["background"])
            if ratio < minimum:
                fail(f"{key} is {ratio:.2f}:1 on the background, needs {minimum}:1")


def validate_xcode_theme(path, p):
    """Fails the build when the theme file is malformed, sets other keys than xcode.json, has a colour or font that is
    not one, or has a syntax, console or markup text colour that is unreadable on its background."""
    name = os.path.basename(path)
    def fail(message):
        raise SystemExit(f"Xcode {name}: {message}")
    with open(path, "rb") as f:
        theme = plistlib.load(f)
    try:
        heritage.xcode.check(theme)
    except ValueError as e:
        fail(str(e))
    syntax_colours, syntax_fonts = theme["DVTSourceTextSyntaxColors"], theme["DVTSourceTextSyntaxFonts"]
    colours = {k: v for k, v in theme.items() if k.endswith("Color") or k == "DVTSourceTextBackground"}
    fonts = {k: v for k, v in theme.items() if k.endswith("Font")}
    if set(theme) - set(colours) - set(fonts) != {"DVTSourceTextSyntaxColors", "DVTSourceTextSyntaxFonts",
                                                    "DVTFontAndColorVersion", "DVTLineSpacing"}:
        fail("has a key that is neither a colour nor a font")
    hexes = {}
    for key, value in [*colours.items(), *syntax_colours.items()]:
        try:
            hexes[key] = heritage.xcode.hex_colour(value)
        except (TypeError, ValueError):
            fail(f"{key} has {value!r}, which is not an opaque Xcode colour")
    for key, value in [*fonts.items(), *syntax_fonts.items()]:
        if not isinstance(value, str) or not XCODE_FONT.fullmatch(value):
            fail(f"{key} has {value!r}, which is not an Xcode font")
    _, text = heritage.xcode.roles(p)
    backgrounds = {"bg": hexes["DVTSourceTextBackground"], "bgTool": hexes["DVTConsoleTextBackgroundColor"]}
    pairs = [(key, hexes[key], backgrounds[role], 4.5) for key, role in text.items()]
    pairs += [(key, hexes[key], backgrounds["bg"], 3 if key == "xcode.syntax.comment" else 4.5)
              for key in syntax_colours]
    for key, fg, bg, minimum in pairs:
        ratio = contrast(fg, bg)
        if ratio < minimum:
            fail(f"{key} is {ratio:.2f}:1 on its background, needs {minimum}:1")


def pack_xcode(directory):
    """Zips the themes, README, changelog and licence into a folder, and returns the zip's path. A zip keeps the file
    names, which Xcode lists the themes by; GitHub would rename loose release files to ASCII without spaces."""
    return pack_folder(directory, os.path.join(OUT, f"{XCODE_NAME}-{VERSION}.zip"), XCODE_NAME)


def visualstudio_description(themes):
    """The extension's description in Visual Studio's Extension Manager."""
    return f"{DESCRIPTION} {len(themes)} dark and light themes, each drawn from the named colours of one tradition."


def visualstudio_readme(families):
    """The Marketplace page. Links are absolute: the Marketplace does not resolve paths in the repository."""
    rows = "\n".join(f"| [{f.FAMILY}]({VENDOR_URL}/tree/master/themes/{heritage.folder(f)}) "
                     f"| {', '.join(t['palette']['name'] for t in f.THEMES)} | {f.BLURB} |" for f in families)
    count = sum(len(f.THEMES) for f in families)
    return f"""# Heritage Themes

{DESCRIPTION} {count} dark and light themes in {len(families)} families; each family maps the named colours of \
one tradition to syntax roles.

Choose a theme under **Tools | Theme**, or under **Tools | Options | Environment | Visual Experience | Color theme**. \
The themes need Visual Studio 2026. Visual Studio has no language service for some languages, so they show \nfewer colours than in other editors: see [the language table]({VENDOR_URL}#visual-studio).

| Family | Themes | Tradition |
| --- | --- | --- |
{rows}

Each family's page describes its colour tradition. The same themes are available for {elsewhere("Visual Studio")}: \
see [Heritage Themes on GitHub]({VENDOR_URL}).

Report a problem or suggest a tradition on the [issue tracker]({VENDOR_URL}/issues). Include the theme, Visual Studio \
version, language and a screenshot.
"""


def visualstudio_publish_manifest():
    """The Marketplace listing that VsixPublisher reads with the .vsix; the rest comes from extension.vsixmanifest."""
    return {"$schema": "http://json.schemastore.org/vsix-publish", "categories": ["theme"],
            "identity": {"internalName": VISUALSTUDIO_ITEM}, "overview": "README.md", "priceCategory": "free",
            "publisher": VSCODE_PUBLISHER, "private": False, "qna": True, "repo": VENDOR_URL}


def build_visualstudio(families):
    """Writes the files of the Visual Studio extension's VSIX to build/visualstudio, and its Marketplace listing to
    build/visualstudio-marketplace, and returns both folders."""
    directory, listing = os.path.join(OUT, "visualstudio"), os.path.join(OUT, "visualstudio-marketplace")
    os.makedirs(directory)
    os.makedirs(listing)
    shutil.copy(VISUALSTUDIO_ICON, os.path.join(directory, "icon.png"))
    shutil.copy(os.path.join(ROOT, "LICENSE"), os.path.join(directory, "LICENSE.txt"))
    themes = [(t["slug"], t["id"], t["palette"], f"{VENDOR_URL}/tree/master/themes/{heritage.folder(family)}")
              for family in families for t in family.THEMES]
    metadata = f"""    <MoreInfo>{VENDOR_URL}</MoreInfo>
    <License>LICENSE.txt</License>
    <ReleaseNotes>{VENDOR_URL}/blob/master/visualstudio/CHANGELOG.md</ReleaseNotes>
    <Icon>icon.png</Icon>
    <Tags>theme, color theme, dark theme, light theme, culture, heritage</Tags>
"""
    heritage.visualstudio.package(directory, VISUALSTUDIO_ID, VERSION, VISUALSTUDIO_NAME,
                                  visualstudio_description(themes), themes, metadata)
    write_text(os.path.join(listing, "README.md"), visualstudio_readme(families))
    write_text(os.path.join(listing, "publishManifest.json"),
               json.dumps(visualstudio_publish_manifest(), indent=2) + "\n")
    return directory, listing


def validate_visualstudio(directory, listing, families):
    """Fails the build when the VSIX manifest is incomplete or does not list exactly the themes' .pkgdef files, a file
    lacks a media type, or a theme does not decode to the categories and colours that heritage.visualstudio gives it,
    sets a colour that visualstudio.json does not have, or has text that is unreadable on its background."""
    namespace = {"v": "http://schemas.microsoft.com/developer/vsx-schema/2011"}
    root = ET.parse(os.path.join(directory, "extension.vsixmanifest")).getroot()
    identity = root.find("v:Metadata/v:Identity", namespace)
    if identity is None or identity.get("Id") != VISUALSTUDIO_ID or identity.get("Version") != VERSION:
        raise SystemExit(f"Visual Studio extension.vsixmanifest: the Identity is not {VISUALSTUDIO_ID} {VERSION}")
    for tag in ("DisplayName", "Description", "MoreInfo", "License", "Icon", "Tags"):
        element = root.find(f"v:Metadata/v:{tag}", namespace)
        if element is None or not (element.text or "").strip():
            raise SystemExit(f"Visual Studio extension.vsixmanifest: <{tag}> is missing or empty")
    for tag in ("License", "Icon"):
        if not os.path.isfile(os.path.join(directory, root.find(f"v:Metadata/v:{tag}", namespace).text)):
            raise SystemExit(f"Visual Studio extension: the {tag} file is missing")
    assets = [a.get("Path").replace("\\", "/") for a in root.findall("v:Assets/v:Asset", namespace)]
    expected = [f"themes/{t['slug']}.pkgdef" for family in families for t in family.THEMES]
    if sorted(assets) != sorted(expected) or sorted(os.listdir(os.path.join(directory, "themes"))) != \
            sorted(os.path.basename(a) for a in expected):
        raise SystemExit(f"Visual Studio extension: {len(assets)} assets for {len(expected)} themes")
    for folder, _, files in os.walk(directory):
        for name in files:
            if name != "[Content_Types].xml" and name.rpartition(".")[2] not in heritage.visualstudio.CONTENT_TYPES:
                raise SystemExit(f"Visual Studio extension: {name} has no media type in [Content_Types].xml")
    with open(os.path.join(listing, "publishManifest.json"), encoding="utf-8") as f:
        publish = json.load(f)
    if not os.path.isfile(os.path.join(listing, publish["overview"])):
        raise SystemExit("Visual Studio Marketplace listing: the overview is missing")
    guids = set()
    for family in families:
        for t in family.THEMES:
            path = os.path.join(directory, "themes", f"{t['slug']}.pkgdef")
            with open(path, encoding="utf-8") as f:
                text = f.read()
            if not text.startswith(heritage.visualstudio.BOM):
                raise SystemExit(f"Visual Studio {t['slug']}.pkgdef: does not start with a byte order mark")
            guid = heritage.visualstudio.check(text, t["palette"], t["id"])
            if guid in guids:
                raise SystemExit(f"Visual Studio {t['slug']}.pkgdef: the theme GUID {guid} is not unique")
            guids.add(guid)


def pack_visualstudio(directory):
    """Zips the extension into a .vsix and returns its path. The entries are sorted and carry a fixed time, so the same
    sources give the same bytes."""
    return heritage.visualstudio.pack(directory, os.path.join(OUT, f"{VISUALSTUDIO_ITEM}-{VERSION}.vsix"), zip_entry)


def main():
    parser = argparse.ArgumentParser(description="Build the JetBrains plugin, the VS Code extension, the Visual Studio "
                                                 "extension, the Sublime Text package, the Zed extension, the Neovim "
                                                 "plugin, the Notepad++ themes and the Xcode themes.")
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
            write_text(os.path.join(OUT, "schemes", f"{t['name']}.icls"), t["scheme"])
    validate(jar, themes)
    archive = os.path.join(OUT, f"heritage-themes-{VERSION}.zip")
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(jar, f"heritage-themes/lib/{os.path.basename(jar)}")
    print(f"{archive}: {len(themes)} themes")
    extension = build_vscode(families, themes)
    validate_vscode(extension, themes)
    print(f"{extension}: {len(themes)} themes", flush=True)
    visualstudio_extension, visualstudio_listing = build_visualstudio(families)
    validate_visualstudio(visualstudio_extension, visualstudio_listing, families)
    print(f"{pack_visualstudio(visualstudio_extension)}: {len(themes)} themes", flush=True)
    package = build_sublime(families, themes)
    validate_sublime(package, themes)
    print(f"{pack_sublime(package)}: {len(themes)} themes", flush=True)
    zed_extension = build_zed(families)
    validate_zed(zed_extension, themes)
    print(f"{pack_zed(zed_extension)}: {len(themes)} themes", flush=True)
    nvim_plugin = build_nvim(families)
    validate_nvim(nvim_plugin, families)
    print(f"{pack_nvim(nvim_plugin)}: {len(themes)} themes", flush=True)
    notepadpp_themes = build_notepadpp(families)
    validate_notepadpp(notepadpp_themes, families)
    print(f"{pack_notepadpp(notepadpp_themes)}: {len(themes)} themes", flush=True)
    xcode_themes = build_xcode(families)
    validate_xcode(xcode_themes, families)
    print(f"{pack_xcode(xcode_themes)}: {len(themes)} themes", flush=True)
    if args.vsix:
        print(f"{pack_vsix(extension, themes)}: {len(themes)} themes")


if __name__ == "__main__":
    main()
