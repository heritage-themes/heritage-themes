"""Builds the Heritage Themes JetBrains plugin, VS Code extension, Visual Studio extension, Sublime Text package, Zed
extension, Neovim plugin, and the Notepad++, Xcode, Helix, Kakoune, Micro, Vim and Emacs themes from every theme
folder.

A theme folder is any directory in themes/ containing a theme.py (see heritage/__init__.py).

Usage: python3 build.py [--vsix]
  --vsix  also pack the VS Code extension into a .vsix with vsce, pinned in scripts/vscode and installed there
          with npm ci on first use; needs Node.js 22 or later and npm

Output goes to build/.
"""
import argparse, configparser, html, json, os, plistlib, re, shutil, subprocess, tomllib, zipfile
import xml.etree.ElementTree as ET

import heritage

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "build")
CHANGELOG = os.path.join(ROOT, "CHANGELOG.md")
# One version for the JetBrains plugin, the VS Code extension, the Visual Studio extension, the Sublime Text package,
# the Zed extension, the Neovim plugin, and the Notepad++, Xcode, Helix, Kakoune, Micro, Vim and Emacs themes. A
# release publishes each product whose changelog has a section for it.
VERSION = "1.7.3"
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
HELIX_CHANGELOG = os.path.join(ROOT, "helix", "CHANGELOG.md")
HELIX_NAME = "heritage-themes-helix"  # the folder in the zip
HELIX_HEX = re.compile(r"#[0-9A-F]{6}")
# A Kakoune face: up to three colours, then attributes. A Micro style: font styles, then fg and an optional bg. A Vim
# :highlight command with the attributes that heritage.vim sets.
KAKOUNE_FACE = re.compile(r"(default|rgb:[0-9A-F]{6})(,(default|rgb:[0-9A-F]{6})){0,2}(\+[bicudrsFf]+)?")
MICRO_STYLE = re.compile(r"((bold|italic|underline|reverse) )*#[0-9A-F]{6}(,#[0-9A-F]{6})?")
TERMINALS_NAME = "heritage-themes-terminals"  # the folder in the zip
VIM_HIGHLIGHT = re.compile(r"hi \w+( (guifg|guibg|guisp)=(#[0-9A-F]{6}|NONE)"
                           r"| (ctermfg|ctermbg|ctermul)=(1[6-9]|[2-9]\d|1\d\d|2[0-4]\d|25[0-5]|NONE)"
                           r"| (gui|cterm)=(NONE|[a-z]+(,[a-z]+)*)| term=NONE)+")
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
EDITORS = ("JetBrains IDEs", "VS Code", "Visual Studio", "Sublime Text", "Zed", "Neovim", "Notepad++", "Xcode",
           "Helix", "Kakoune", "Micro", "Vim", "Emacs", "Nano", "Textadept", "Lapce", "Qt Creator", "Amp", "Eclipse", "Nova", "terminals")
# Islands guidance: the main window is lighter than the islands in dark themes, darker in light ones, by this ratio.
FRAME_CONTRAST = 1.20
ANSI = tuple(f"ansi{c}" for c in ("Red", "Green", "Yellow", "Blue", "Magenta", "Cyan"))
# WCAG 2.2 AA minimums for palette roles in every app: 4.5:1 for text, 3:1 for comments, focus rings and the caret.
# (foreground roles, background roles, minimum)
CONTRAST = (
    (("fg", "muted"), ("bg", "bgTool", "bgUi", "surface", "caretRow", "frame"), 4.5),
    # code shows on the editor's background and on the current line
    (("keyword", "string", "number", "type", "method", "call", "field", "constant", "annotation", "doc", "docTag",
      "op", "param", "typeParam", "label", "gold", "azure") + ANSI, ("bg", "caretRow"), 4.5),
    (("comment",), ("bg", "caretRow"), 3),
    (("lineNoCaret",), ("bg", "caretRow"), 4.5),  # the current line's number, on the gutter and on the current line
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

Update with `:Lazy update {NVIM_NAME}`. lazy.nvim records the installed commit in `lazy-lock.json`; commit that file \
to keep every machine on the same version.

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


def helix_readme(families):
    """The README in the zip. Links are absolute, as the zip holds the build only."""
    rows = "\n".join(f"| [{f.FAMILY}]({VENDOR_URL}/tree/master/themes/{heritage.folder(f)}) "
                     f"| {', '.join(f'`{heritage.helix.name(t)}`' for t in f.THEMES)} | {f.BLURB} |" for f in families)
    count = sum(len(f.THEMES) for f in families)
    return f"""# Heritage Themes for Helix

{DESCRIPTION} {count} dark and light themes in {len(families)} families; each family maps the named colours of one \
tradition to syntax roles.

## Install

1. Copy the files in `themes` into the `themes` folder of your Helix configuration: `~/.config/helix/themes` on \
Linux and macOS, `%AppData%\\helix\\themes` on Windows. Create the folder if it does not exist. In a terminal, from \
the unzipped folder:

   ```bash
   mkdir -p ~/.config/helix/themes
   cp themes/* ~/.config/helix/themes/
   ```

2. Choose a theme at the top of `config.toml`, or try one with `:theme heritage_` and `Tab`:

   ```toml
   theme = "heritage_holi_night"
   ```

The themes use 24-bit colour. Helix falls back to its default theme when it does not detect a terminal with 24-bit \
colour; if your terminal has it, set `true-color = true` under `[editor]`.

## What is coloured

Each theme colours the editor, the gutter, cursors, selections, diagnostics, the status line, buffer line, pickers, \
popups, the completion menu, inlay hints and jump labels. The cursor takes the colour of the mode, and so does the \
mode name in the status line with `color-modes = true` under `[editor]`.

## Languages

Helix colours code by the Tree-sitter captures of the queries it ships. A capture names the construct, not the \
language, so the themes colour a construct alike in every language: keys in YAML, TOML and JSON take the field \
colour, Java annotations and HTML attribute names the annotation colour, and Rust lifetimes the label colour. Helix \
gives function declarations and calls one capture, so both take the call colour, and Python decorators take it too.

To change a colour, make a theme of your own that inherits one of these, in the same `themes` folder:

```toml
inherits = "heritage_holi_night"
"comment" = {{ fg = "#808080", modifiers = ["italic"] }}
```

## Themes

| Family | Themes | Tradition |
| --- | --- | --- |
{rows}

Each family's page describes its colour tradition. The same themes are available for {elsewhere("Helix")}: see \
[Heritage Themes on GitHub]({VENDOR_URL}).

Report a problem or suggest a tradition on the [issue tracker]({VENDOR_URL}/issues). Include the theme, Helix \
version, terminal, language and a screenshot.
"""


def build_helix(families):
    """Writes the Helix themes to build/helix/themes, one file per theme named as Helix lists it, and returns
    build/helix."""
    directory = os.path.join(OUT, "helix")
    os.makedirs(os.path.join(directory, "themes"))
    for family in families:
        source = f"{VENDOR_URL}/tree/master/themes/{heritage.folder(family)}"
        for t in family.THEMES:
            write_text(os.path.join(directory, "themes", f"{heritage.helix.name(t)}.toml"),
                       heritage.helix.theme(t["palette"], source))
    write_text(os.path.join(directory, "README.md"), helix_readme(families))
    shutil.copy(HELIX_CHANGELOG, os.path.join(directory, "CHANGELOG.md"))
    shutil.copy(os.path.join(ROOT, "LICENSE"), os.path.join(directory, "LICENSE"))
    return directory


def validate_helix(directory, families):
    """Fails the build when the README, changelog, licence or the file of a theme is missing, a theme leaves out a UI
    key that Helix looks up, has a malformed style, or has a text colour that is unreadable on its background."""
    for name in ("README.md", "CHANGELOG.md", "LICENSE"):
        if not os.path.isfile(os.path.join(directory, name)):
            raise SystemExit(f"Helix themes: {name} is missing")
    expected = set()
    for family in families:
        for t in family.THEMES:
            name = heritage.helix.name(t)
            if not re.fullmatch(r"heritage(_[a-z]+)+", name):
                raise SystemExit(f"Helix: {name} is not a lower-case ASCII theme name")
            expected.add(f"{name}.toml")
            validate_helix_theme(os.path.join(directory, "themes", f"{name}.toml"), name)
    found = set(os.listdir(os.path.join(directory, "themes")))
    if found != expected:
        raise SystemExit(f"Helix themes: {len(found)} files for {len(expected)} themes")


def validate_helix_theme(path, name):
    """Fails the build when the theme file is not TOML, leaves out a key of heritage.helix.UI_KEYS, has a style
    attribute, colour, modifier or underline style that Helix does not accept, or has a text colour below 4.5:1 (3:1
    for comments, the caret and the status line's diagnostic marks) on a background Helix draws it on."""
    def fail(message):
        raise SystemExit(f"Helix {name}: {message}")
    with open(path, "rb") as f:
        styles = tomllib.load(f)
    missing = [key for key in heritage.helix.UI_KEYS if key not in styles]
    if missing:
        fail(f"leaves out {', '.join(missing)}")
    for key, style in styles.items():
        if not isinstance(style, dict) or not style or not set(style) <= set(heritage.helix.ATTRIBUTES):
            fail(f"{key} has {style!r}")
        underline = style.get("underline", {})
        colours = [style.get("fg"), style.get("bg"), underline.get("color")]
        if not all(c is None or HELIX_HEX.fullmatch(c) for c in colours) \
                or not set(style.get("modifiers", [])) <= set(heritage.helix.MODIFIERS) \
                or not set(underline) <= {"color", "style"} \
                or underline.get("style", "line") not in heritage.helix.UNDERLINES:
            fail(f"{key} has {style!r}")
        if "fg" not in style or key in heritage.helix.DECORATIVE:
            continue
        minimum = 3 if key in heritage.helix.LOW_CONTRAST else 4.5
        backgrounds = [(style["bg"], minimum)] if "bg" in style else \
            [(styles[k]["bg"], m) for k, m in heritage.helix.DRAWN_ON.get(key, (("ui.background", minimum),))]
        for background, minimum in backgrounds:
            ratio = contrast(style["fg"][1:], background[1:])
            if ratio < minimum:
                fail(f"{key} is {ratio:.2f}:1 on {background}, needs {minimum}:1")


def pack_helix(directory):
    """Zips the themes, README, changelog and licence into a folder, and returns the zip's path."""
    return pack_folder(directory, os.path.join(OUT, f"{HELIX_NAME}-{VERSION}.zip"), HELIX_NAME)


def theme_rows(families, name):
    """The rows of a README's table of families, with each family's themes as name gives them."""
    return "\n".join(f"| [{f.FAMILY}]({VENDOR_URL}/tree/master/themes/{heritage.folder(f)}) "
                     f"| {', '.join(f'`{name(t)}`' for t in f.THEMES)} | {f.BLURB} |" for f in families)


def readme_footer(families, editor, heading, report):
    """The table of families and the links that end the README of a product."""
    return f"""## {heading}

| Family | {heading} | Tradition |
| --- | --- | --- |
{theme_rows(families, TERMINAL_NAMES[editor])}

Each family's page describes its colour tradition. The same themes are available for {elsewhere(editor)}: see \
[Heritage Themes on GitHub]({VENDOR_URL}).

Report a problem or suggest a tradition on the [issue tracker]({VENDOR_URL}/issues). Include {report} and a \
screenshot.
"""


def check_styles(label, styles, fg, bg, default, decorative, low_contrast, drawn_on):
    """Fails the build when a style's text colour is below 4.5:1 (3:1 for low_contrast) on the background it is drawn
    on: its own bg, else those of drawn_on ((key, minimum) pairs), else the bg of default. fg and bg name the colour
    attributes of a style."""
    for key, style in styles.items():
        if fg not in style or key in decorative:
            continue
        minimum = 3 if key in low_contrast else 4.5
        backgrounds = [(style[bg], minimum)] if bg in style else \
            [(styles[k][bg], m) for k, m in drawn_on.get(key, ((default, minimum),))]
        for background, needed in backgrounds:
            ratio = contrast(style[fg][1:], background[1:])
            if ratio < needed:
                raise SystemExit(f"{label}: {key} is {ratio:.2f}:1 on {background}, needs {needed}:1")


def check_files(label, directory, folder, expected):
    """Fails the build when the README, changelog or licence is missing, or folder holds other files than expected."""
    for name in ("README.md", "CHANGELOG.md", "LICENSE"):
        if not os.path.isfile(os.path.join(directory, name)):
            raise SystemExit(f"{label}: {name} is missing")
    found = set(os.listdir(os.path.join(directory, folder)))
    if found != expected:
        raise SystemExit(f"{label}: {len(found)} files in {folder} for {len(expected)} themes")


def build_themes(families, editor, folder, files):
    """Writes each theme's file to build/<editor>/<folder>, with the README, changelog and licence, and returns
    build/<editor>. files gives a theme dict and the URL of its family's folder as (file name, text)."""
    directory = os.path.join(OUT, editor.lower())
    os.makedirs(os.path.join(directory, folder))
    for family in families:
        source = f"{VENDOR_URL}/tree/master/themes/{heritage.folder(family)}"
        for t in family.THEMES:
            filename, text = files(t, source)
            write_text(os.path.join(directory, folder, filename), text)
    write_text(os.path.join(directory, "README.md"), TERMINAL_READMES[editor](families))
    shutil.copy(os.path.join(ROOT, editor.lower(), "CHANGELOG.md"), os.path.join(directory, "CHANGELOG.md"))
    shutil.copy(os.path.join(ROOT, "LICENSE"), os.path.join(directory, "LICENSE"))
    return directory


def kakoune_readme(families):
    """The README in the zip. Links are absolute, as the zip holds the build only."""
    count = sum(len(f.THEMES) for f in families)
    return f"""# Heritage Themes for Kakoune

{DESCRIPTION} {count} dark and light colour schemes in {len(families)} families; each family maps the named colours \
of one tradition to syntax roles.

## Install

1. Copy the files in `colors` into `~/.config/kak/colors`, creating the folder if it does not exist. In a terminal, \
from the unzipped folder:

   ```bash
   mkdir -p ~/.config/kak/colors
   cp colors/* ~/.config/kak/colors/
   ```

2. Choose a scheme in `~/.config/kak/kakrc`, or try one with `:colorscheme heritage-` and `Tab`:

   ```kak
   colorscheme heritage-holi-night
   ```

The schemes need a terminal with 24-bit colour.

## What is coloured

Each scheme sets Kakoune's built-in faces: the editor, selections, cursors, line numbers, menus, information boxes, \
diagnostics, the status line and the prompt.

## Languages

Kakoune's language scripts give each construct one of a few faces, shared by every language. `meta` takes the keyword \
colour, so Java annotations, Rust attributes, C's `#include` and Python's `import` share it; `attribute` takes the \
annotation colour, so Python decorators, HTML attribute names, YAML keys and Java's modifiers share that. Python's \
script colours built-in functions but neither other calls nor the names of the functions you declare. Diffs and \
Git views use the terminal's own colours. Kakoune ships no script for C# and opens it as plain text.

To change a face, set it after the scheme in `kakrc`:

```kak
colorscheme heritage-holi-night
set-face global comment rgb:808080+i
```

{readme_footer(families, "Kakoune", "Colour schemes", "the colour scheme, Kakoune version, terminal, language")}"""


def validate_kakoune(directory, families):
    """Fails the build when a file is missing, a scheme leaves out a face of heritage.kakoune, has a malformed face, or
    has a text colour that is unreadable on its background."""
    expected = set()
    for family in families:
        for t in family.THEMES:
            name, p = heritage.kakoune.name(t), t["palette"]
            expected.add(f"{name}.kak")
            label = f"Kakoune {name}"
            with open(os.path.join(directory, "colors", f"{name}.kak"), encoding="utf-8") as f:
                faces = dict(re.fullmatch(r"set-face global (\w+) (\S+)", line).groups()
                             for line in f.read().splitlines() if line.startswith("set-face"))
            missing = [k for k in heritage.kakoune.UI_FACES + heritage.kakoune.SYNTAX_FACES if k not in faces]
            if missing:
                raise SystemExit(f"{label}: leaves out {', '.join(missing)}")
            for key, value in faces.items():
                if not KAKOUNE_FACE.fullmatch(value):
                    raise SystemExit(f"{label}: {key} has {value!r}")
            styles = heritage.kakoune.styles(p)
            check_styles(label, styles, "fg", "bg", "Default", heritage.kakoune.DECORATIVE,
                         heritage.kakoune.LOW_CONTRAST, heritage.kakoune.DRAWN_ON)
    check_files("Kakoune colour schemes", directory, "colors", expected)


def micro_readme(families):
    """The README in the zip. Links are absolute, as the zip holds the build only."""
    count = sum(len(f.THEMES) for f in families)
    return f"""# Heritage Themes for Micro

{DESCRIPTION} {count} dark and light colour schemes in {len(families)} families; each family maps the named colours \
of one tradition to syntax roles.

## Install

1. Copy the files in `colorschemes` into `~/.config/micro/colorschemes`, creating the folder if it does not exist. \
In a terminal, from the unzipped folder:

   ```bash
   mkdir -p ~/.config/micro/colorschemes
   cp colorschemes/* ~/.config/micro/colorschemes/
   ```

2. Press `Ctrl-e` in Micro and choose a scheme, or try one with `set colorscheme heritage-` and `Tab`:

   ```text
   set colorscheme heritage-holi-night
   ```

Micro draws the schemes in 24-bit colour when the terminal reports it in `COLORTERM`, and in the nearest of 256 \
colours otherwise. Set `truecolor` to `on` if your terminal has 24-bit colour and does not report it.

## What is coloured

Each scheme colours the editor, selections, line numbers, the cursor line, search and brace matches, the gutter's \
diagnostics and version control marks, the status line, the tab bar, split dividers and the completion menu.

## Languages

Micro's syntax files name their groups after Vim's and use them as each language needs, so a group can cover \
different constructs in different languages: `identifier` marks Python's built-in functions as well as HTML attribute \
names, and Java's syntax file files its modifiers under `type`. Python's syntax file colours a function's name where \
it is declared and built-in functions where they are called, but not calls to other functions.

To change a group, make a scheme of your own that includes one of these, in the same `colorschemes` folder:

```text
include "heritage-holi-night"
color-link comment "italic #808080"
```

{readme_footer(families, "Micro", "Colour schemes", "the colour scheme, Micro version, terminal, language")}"""


def validate_micro(directory, families):
    """Fails the build when a file is missing, a scheme leaves out a group of heritage.micro.UI_GROUPS, does not set
    default first, has a malformed style, or has a text colour that is unreadable on its background."""
    expected = set()
    for family in families:
        for t in family.THEMES:
            name, p = heritage.micro.name(t), t["palette"]
            expected.add(f"{name}.micro")
            label = f"Micro {name}"
            with open(os.path.join(directory, "colorschemes", f"{name}.micro"), encoding="utf-8") as f:
                links = [re.fullmatch(r'color-link ([\w.-]+) "([^"]+)"', line).groups()
                         for line in f.read().splitlines() if line.startswith("color-link")]
            groups = dict(links)
            if links[0][0] != "default":
                raise SystemExit(f"{label}: default is not the first group")
            missing = [g for g in heritage.micro.UI_GROUPS if g not in groups]
            if missing:
                raise SystemExit(f"{label}: leaves out {', '.join(missing)}")
            for group, value in groups.items():
                if not MICRO_STYLE.fullmatch(value):
                    raise SystemExit(f"{label}: {group} has {value!r}")
            check_styles(label, heritage.micro.styles(p), "fg", "bg", "default", heritage.micro.DECORATIVE,
                         heritage.micro.LOW_CONTRAST, {})
    check_files("Micro colour schemes", directory, "colorschemes", expected)


def vim_readme(families):
    """The README in the zip. Links are absolute, as the zip holds the build only."""
    count = sum(len(f.THEMES) for f in families)
    return f"""# Heritage Themes for Vim

{DESCRIPTION} {count} dark and light colour schemes in {len(families)} families; each family maps the named colours \
of one tradition to syntax roles. For Neovim, use the [Neovim plugin](https://github.com/heritage-themes/\
heritage-themes.nvim).

## Install

The schemes need Vim 9.0 or later.

1. Unzip `heritage-themes-vim-<version>.zip` into `~/.vim/pack/heritage/start/` (`~/vimfiles/pack/heritage/start/` \
on Windows), creating the folder if it does not exist:

   ```bash
   mkdir -p ~/.vim/pack/heritage/start
   unzip heritage-themes-vim-<version>.zip -d ~/.vim/pack/heritage/start/
   ```

2. Choose a scheme in your `vimrc`, or try one with `:colorscheme heritage-` and `Tab`:

   ```vim
   set termguicolors
   colorscheme heritage-holi-night
   ```

`termguicolors` draws the schemes in 24-bit colour, which most terminals have. Without it, a terminal draws them in \
the nearest of 256 colours. gVim draws them in 24-bit colour either way. Each scheme sets `background` to its own \
brightness.

## What is coloured

Each scheme colours the editor, the syntax groups of `:help group-name`, the status line, tab line, tab panel, popup \
windows, the completion menu, diff mode, spelling, the GUI's menus and tooltips, and the terminal window.

## Languages

Vim's syntax files link their groups to the groups of `:help group-name`, so a construct takes the colour of the group \
its syntax file links it to. Where that differs from the other editors, the scheme sets the language's own group: Java \
annotations, Python decorators and Rust attributes take the annotation colour, Rust lifetimes the type parameter \
colour, function names in declarations the declaration colour, and the methods of TypeScript's standard library the \
call colour.

Most of Vim's syntax files colour few function names. Python's and TypeScript's colour declarations, but calls only to \
built-ins and the standard library. The Kotlin, C, C++ and C# syntax files colour none. Go's colours declarations when \
`go_highlight_functions` is set and calls when `go_highlight_function_calls` is set; Java's colours declarations when \
`java_highlight_functions` is set:

```vim
let g:go_highlight_functions = 1
let g:go_highlight_function_calls = 1
let g:java_highlight_functions = 'style'
```

To change a group, set it in a `ColorScheme` autocommand, so that it survives switching schemes:

```vim
autocmd ColorScheme heritage-* highlight Comment guifg=#808080 gui=italic
```

{readme_footer(families, "Vim", "Colour schemes", "the colour scheme, Vim version, terminal, language")}"""


def validate_vim(directory, families):
    """Fails the build when a file is missing, a highlight definition is malformed, a scheme does not set its
    colors_name or a text colour is unreadable on the background it is drawn on."""
    expected = set()
    for family in families:
        for t in family.THEMES:
            scheme, p = heritage.vim.name(t), t["palette"]
            expected.add(f"{scheme}.vim")
            label = f"Vim {scheme}"
            groups = heritage.vim.highlights(p)
            for group, definition in groups.items():
                if not re.fullmatch(r"[A-Za-z0-9_]+", group):
                    raise SystemExit(f"{label}: {group!r} is not a valid group name")
                for key, value in definition.items():
                    if not ((key in heritage.vim.COLOURS and NVIM_HEX.fullmatch(value)) or
                            (key in heritage.vim.FLAGS and value is True)):
                        raise SystemExit(f"{label}: {group} has {key} = {value!r}")
            check_styles(label, groups, "fg", "bg", "Normal", heritage.vim.DECORATIVE, heritage.vim.LOW_CONTRAST, {})
            with open(os.path.join(directory, "colors", f"{scheme}.vim"), encoding="utf-8") as f:
                text = f.read()
            if f"let g:colors_name = '{scheme}'" not in text:
                raise SystemExit(f"Vim colors/{scheme}.vim does not set its colors_name")
            for line in text.splitlines():
                if line.startswith("hi ") and line != "hi clear" and not VIM_HIGHLIGHT.fullmatch(line):
                    raise SystemExit(f"Vim colors/{scheme}.vim has {line!r}")
    check_files("Vim colour schemes", directory, "colors", expected)


def emacs_readme(families):
    """The README in the zip. Links are absolute, as the zip holds the build only."""
    count = sum(len(f.THEMES) for f in families)
    return f"""# Heritage Themes for GNU Emacs

{DESCRIPTION} {count} dark and light themes in {len(families)} families; each family maps the named colours of one \
tradition to syntax roles.

## Install

The themes need Emacs 29.1 or later.

1. Copy the files in `themes` into a `themes` folder in your Emacs directory, `~/.emacs.d/themes` or \
`~/.config/emacs/themes`, creating it if it does not exist:

   ```bash
   mkdir -p ~/.emacs.d/themes
   cp themes/* ~/.emacs.d/themes/
   ```

2. Add the folder to the theme path and load a theme in your init file:

   ```elisp
   (add-to-list 'custom-theme-load-path (locate-user-emacs-file "themes/"))
   (load-theme 'heritage-holi-night t)
   ```

Try a theme with `M-x load-theme RET heritage-` and `Tab`. In a terminal, Emacs draws the themes in 24-bit colour \
when the terminal reports it in `COLORTERM`, and in the nearest colours it has otherwise.

## What is coloured

Each theme colours Emacs itself (the editor, mode line, header line, tab bar, tab line, minibuffer, search, \
completion, menus and tooltips) and the packages that ship with Emacs: font-lock and the Tree-sitter modes, \
compilation, Flymake, Flyspell, Eglot, diff, smerge and Ediff, Dired, Eshell, Org, outlines, Info, whitespace-mode, \
which-key, xref, Ido, hi-lock, EWW, message composition, Customize and the terminal colours.

## Languages

Emacs colours a language once it has a major mode for it. Emacs 30 opens Kotlin, Groovy, Vue and Markdown as plain \
text, and colours Go, Rust, TypeScript and YAML once you install their Tree-sitter grammars with \
`M-x treesit-install-language-grammar`. Function calls take the call colour in the Tree-sitter modes when \
`treesit-font-lock-level` is 4, and are plain in the other modes. The modes without Tree-sitter colour a declared name \
in one face, so fields, HTML attribute names and local variables take the field colour where they are declared; HTML \
tag names take the declaration colour.

To change a face, set it after the theme in your init file:

```elisp
(custom-theme-set-faces 'heritage-holi-night
 '(font-lock-comment-face ((t (:foreground "#808080" :slant italic)))))
```

{readme_footer(families, "Emacs", "Themes", "the theme, Emacs version, whether in a terminal or a window, language")}"""


def validate_emacs(directory, families):
    """Fails the build when a file is missing, a theme sets an attribute that heritage.emacs does not allow or a colour
    that is not hex, its Lisp is unbalanced, or a text colour is unreadable on the background it is drawn on."""
    expected = set()
    for family in families:
        for t in family.THEMES:
            name, p = heritage.emacs.name(t), t["palette"]
            expected.add(f"{name}-theme.el")
            label = f"Emacs {name}"
            faces = heritage.emacs.faces(p)
            for face, attributes in faces.items():
                if not set(attributes) <= set(heritage.emacs.ATTRIBUTES):
                    raise SystemExit(f"{label}: {face} has {attributes}")
                for key in ("foreground", "background"):
                    if key in attributes and not NVIM_HEX.fullmatch(attributes[key]):
                        raise SystemExit(f"{label}: {face} has {key} {attributes[key]!r}")
            check_styles(label, faces, "foreground", "background", "default", heritage.emacs.DECORATIVE,
                         heritage.emacs.LOW_CONTRAST, heritage.emacs.DRAWN_ON)
            with open(os.path.join(directory, "themes", f"{name}-theme.el"), encoding="utf-8") as f:
                code = re.sub(r'"(\\.|[^"\\])*"|;[^\n]*', "", f.read())
            depth = 0
            for char in code:
                depth += {"(": 1, ")": -1}.get(char, 0)
                if depth < 0:
                    break
            if depth or f"(deftheme {name}" not in code or f"(provide-theme '{name})" not in code:
                raise SystemExit(f"Emacs themes/{name}-theme.el is not a balanced theme definition of {name}")
    check_files("Emacs themes", directory, "themes", expected)


def nano_readme(families):
    """The README in the zip. Links are absolute, as the zip holds the build only."""
    count = sum(len(f.THEMES) for f in families)
    return f"""# Heritage Themes for Nano

{DESCRIPTION} {count} dark and light colour schemes in {len(families)} families; each family maps the named colours \
of one tradition to syntax roles.

## Install

The schemes need GNU nano 7.0 or later in a terminal with 256 colours, which runs the matching theme of the \
[Heritage Themes for terminals]({VENDOR_URL}/releases/latest).

Nano reads interface colours only from the nanorc file itself, not from files it includes, so a scheme's lines go \
into `~/.config/nano/nanorc`, after the syntax files. In a terminal, from the unzipped folder:

```bash
mkdir -p ~/.config/nano
echo 'include "/usr/share/nano/*.nanorc"' >> ~/.config/nano/nanorc
cat schemes/heritage-holi-night.nanorc >> ~/.config/nano/nanorc
```

Many systems include the syntax files in `/etc/nanorc` already; the `echo` line is needed where they do not. To \
change schemes, replace the scheme's `set` lines in the nanorc file with another scheme's.

## What is coloured

Each scheme colours nano's interface: the title bar, the mini bar, the status bar, error messages, prompts, the \
selection, search matches, the guide stripe, the scroll indicator, line numbers and the help lines. Nano's syntax \
files colour code with the terminal's 16 colours by name, so code takes the palette's ANSI colours from the matching \
terminal theme, in the roles that each syntax file gives them, as do the scheme's text colours. The surfaces that are \
no terminal colour, such as the title bar, take the nearest of the 256 colours that nano reaches, on which their text \
stays readable. A few syntax files, such as those for SQL, YAML and Lua, also name nano's own extended colours, such \
as `sky` and `lagoon`, which keep their colours in every theme.

{readme_footer(families, "Nano", "Colour schemes", "the colour scheme, nano version, terminal, language")}"""


def validate_nano(directory, families):
    """Fails the build when a file is missing, a scheme leaves out an option of heritage.nano.OPTIONS or differs from
    heritage.nano.options, or text is unreadable on the colour it is drawn on."""
    expected = set()
    for family in families:
        for t in family.THEMES:
            name, p = heritage.nano.name(t), t["palette"]
            expected.add(f"{name}.nanorc")
            label = f"Nano {name}"
            with open(os.path.join(directory, "schemes", f"{name}.nanorc"), encoding="utf-8") as f:
                found = heritage.nano.parse(f.read())
            if found != {option: heritage.nano.value(*spec) for option, spec in heritage.nano.options(p).items()}:
                raise SystemExit(f"{label}: differs from heritage.nano.options")
            if set(found) != set(heritage.nano.OPTIONS):
                raise SystemExit(f"{label}: does not set exactly the options of heritage.nano.OPTIONS")
            check_styles(label, heritage.nano.styles(p), "fg", "bg", "functioncolor", heritage.nano.DECORATIVE,
                         set(), {})
    check_files("Nano colour schemes", directory, "schemes", expected)


def textadept_readme(families):
    """The README in the zip. Links are absolute, as the zip holds the build only."""
    count = sum(len(f.THEMES) for f in families)
    return f"""# Heritage Themes for Textadept

{DESCRIPTION} {count} dark and light themes in {len(families)} families; each family maps the named colours of one \
tradition to syntax roles.

## Install

The themes need Textadept 12 or later.

1. Copy the files in `themes` into `~/.textadept/themes`, creating the folder if it does not exist. In a terminal, \
from the unzipped folder:

   ```bash
   mkdir -p ~/.textadept/themes
   cp themes/* ~/.textadept/themes/
   ```

2. Choose a theme in `~/.textadept/init.lua`, with the font of your choice:

   ```lua
   if UI ~= 'terminal' then
   \tview:set_theme('heritage-holi-night', {{font = 'Monospace', size = 11}})
   end
   ```

Try a theme without restarting with `reset()` in the Lua command entry after changing `init.lua`.

## What is coloured

Each theme colours the editor: code in every language that Textadept's lexers highlight, the line numbers and fold \
margin, the caret and caret line, selections, brace matches, call tips, bookmarks, warning and error markers, search \
and highlight indicators, the long line marker and ANSI output. Textadept draws its menus, tabs, status bar and \
dialogs with Qt or GTK in the system's colours, which a theme cannot change.

## Languages

Textadept's lexers give a construct one tag in every language, so preprocessor directives such as C's `#include` take \
the keyword colour, and attributes take the annotation colour, which covers HTML attribute names and Java annotations \
alike. Function calls take the call colour where a lexer tags them, and a function's name where it is declared takes \
the text colour.

{readme_footer(families, "Textadept", "Themes", "the theme, Textadept version, Qt, GTK or terminal, language")}"""


def validate_textadept(directory, families):
    """Fails the build when a file is missing, a theme leaves out a lexer tag of heritage.textadept.TAGS, its colours
    differ from heritage.textadept.colours, or a text colour is unreadable on the background it is drawn on."""
    expected = set()
    for family in families:
        for t in family.THEMES:
            name, p = heritage.textadept.name(t), t["palette"]
            expected.add(f"{name}.lua")
            label = f"Textadept {name}"
            with open(os.path.join(directory, "themes", f"{name}.lua"), encoding="utf-8") as f:
                text = f.read()
            if heritage.textadept.parse_colours(text) != heritage.textadept.colours(p):
                raise SystemExit(f"{label}: colours differ from heritage.textadept.colours")
            tags = set(re.findall(r"^styles\[lexer\.(\w+)\] = ", text, re.M))
            if tags != set(heritage.textadept.TAGS):
                raise SystemExit(f"{label}: sets the tags {sorted(tags ^ set(heritage.textadept.TAGS))} wrongly")
            if text.count("{") != text.count("}") or not text.endswith("ui.find.entry_font = font .. ' ' .. size\n"):
                raise SystemExit(f"{label}: is not a complete theme")
            check_styles(label, heritage.textadept.styles(p), "fg", "bg", "STYLE_DEFAULT", set(),
                         {"lexer.COMMENT"}, {})
    check_files("Textadept themes", directory, "themes", expected)


def lapce_readme(families):
    """The README in the zip. Links are absolute, as the zip holds the build only."""
    count = sum(len(f.THEMES) for f in families)
    return f"""# Heritage Themes for Lapce

{DESCRIPTION} {count} dark and light colour themes in {len(families)} families; each family maps the named colours \
of one tradition to syntax roles.

## Install

The themes come as one plugin and need Lapce 0.4 or later.

1. Copy the `{heritage.lapce.PLUGIN}` folder into Lapce's `plugins` folder: \
`~/.local/share/lapce-stable/plugins` on Linux, `~/Library/Application Support/dev.lapce.Lapce-Stable/plugins` on \
macOS and `%LocalAppData%\\lapce\\Lapce-Stable\\data\\plugins` on Windows. On Linux, from the unzipped folder:

   ```bash
   mkdir -p ~/.local/share/lapce-stable/plugins
   cp -r {heritage.lapce.PLUGIN} ~/.local/share/lapce-stable/plugins/
   ```

2. Restart Lapce and choose a theme, for example **Holi Night**, with **Settings | Color Theme**, or in \
`settings.toml`:

   ```toml
   [core]
   color-theme = "Holi Night"
   ```

## What is coloured

Each theme colours the editor, the tab bar, panels, the activity bar, the status bar with its modal modes, the \
palette, completion, hover and inlay hints, error lens, source control marks, the debugger, the plugin list and the \
terminal.

## Languages

Lapce matches the captures of its Tree-sitter grammars to a fixed list of scopes, so numbers, booleans and named \
constants share the number colour, and function declarations and calls the call colour; a language server's semantic \
tokens tell more constructs apart. Lapce draws code in colour only, without bold or italic. It colours code once it \
has its grammars, which it downloads from the release of `lapce/tree-sitter-grammars` that matches its version.

{readme_footer(families, "Lapce", "Themes", "the theme, Lapce version, language, whether a language server runs")}"""


def build_lapce(families):
    """Writes the plugin to build/lapce/<plugin>, with the README, changelog and licence beside it, and returns
    build/lapce."""
    directory = os.path.join(OUT, "lapce")
    plugin = os.path.join(directory, heritage.lapce.PLUGIN)
    os.makedirs(os.path.join(plugin, "themes"))
    themes = [t for f in families for t in f.THEMES]
    for family in families:
        source = f"{VENDOR_URL}/tree/master/themes/{heritage.folder(family)}"
        for t in family.THEMES:
            write_text(os.path.join(plugin, "themes", f"{heritage.lapce.name(t)}.toml"),
                       heritage.lapce.theme(t["palette"], source))
    write_text(os.path.join(plugin, "volt.toml"), heritage.lapce.volt(themes, VERSION, VENDOR_URL))
    write_text(os.path.join(directory, "README.md"), lapce_readme(families))
    shutil.copy(os.path.join(ROOT, "lapce", "CHANGELOG.md"), os.path.join(directory, "CHANGELOG.md"))
    shutil.copy(os.path.join(ROOT, "LICENSE"), os.path.join(directory, "LICENSE"))
    return directory


def validate_lapce(directory, families):
    """Fails the build when volt.toml does not list exactly the theme files, a theme does not parse, its keys or
    colours differ from heritage.lapce, or a text colour is unreadable on the background it is drawn on."""
    plugin = os.path.join(directory, heritage.lapce.PLUGIN)
    with open(os.path.join(plugin, "volt.toml"), "rb") as f:
        volt = tomllib.load(f)
    themes = [t for f in families for t in f.THEMES]
    listed = [f"themes/{heritage.lapce.name(t)}.toml" for t in themes]
    if volt["color-themes"] != listed or volt["name"] != heritage.lapce.PLUGIN or volt["version"] != VERSION:
        raise SystemExit("Lapce volt.toml does not name the plugin, its version and every theme file")
    if set(os.listdir(os.path.join(plugin, "themes"))) != {os.path.basename(path) for path in listed}:
        raise SystemExit("Lapce themes: the themes folder holds other files than volt.toml lists")
    names = set()
    for t in themes:
        p, label = t["palette"], f"Lapce {heritage.lapce.name(t)}"
        with open(os.path.join(plugin, "themes", f"{heritage.lapce.name(t)}.toml"), "rb") as f:
            data = tomllib.load(f)["color-theme"]
        names.add(data["name"])
        if data["base"] != heritage.lapce.base(p) or data["ui"] != heritage.lapce.ui(p) or \
                data["syntax"] != {key: "#" + p[role] for key, role in heritage.lapce.syntax(p).items()}:
            raise SystemExit(f"{label}: differs from heritage.lapce")
        for value in [*data["base"].values(), *data["ui"].values(), *data["syntax"].values()]:
            if not re.fullmatch(r"#[0-9A-F]{6}([0-9A-F]{2})?", value):
                raise SystemExit(f"{label}: {value!r} is not a colour")
        check_styles(label, heritage.lapce.styles(p), "fg", "bg", "syntax none", set(), {"syntax comment"}, {})
    if len(names) != len(themes):
        raise SystemExit("Lapce themes: two themes have the same name")
    for name in ("README.md", "CHANGELOG.md", "LICENSE"):
        if not os.path.isfile(os.path.join(directory, name)):
            raise SystemExit(f"Lapce themes: {name} is missing")


def qtcreator_readme(families):
    """The README in the zip. Links are absolute, as the zip holds the build only."""
    count = sum(len(f.THEMES) for f in families)
    return f"""# Heritage Themes for Qt Creator

{DESCRIPTION} {count} dark and light themes in {len(families)} families, each with an editor colour scheme of the \
same name; each family maps the named colours of one tradition to syntax roles.

## Install

The themes need Qt Creator 20 or later.

1. Copy the files in `themes` into the `themes` folder and the files in `styles` into the `styles` folder of Qt \
Creator's settings, creating the folders if they do not exist: `~/.config/QtProject/qtcreator` on Linux and macOS, \
`%AppData%\\QtProject\\qtcreator` on Windows. On Linux and macOS, from the unzipped folder:

   ```bash
   mkdir -p ~/.config/QtProject/qtcreator/themes ~/.config/QtProject/qtcreator/styles
   cp themes/* ~/.config/QtProject/qtcreator/themes/
   cp styles/* ~/.config/QtProject/qtcreator/styles/
   ```

2. Choose a theme, for example **Holi Night**, under **Preferences | Environment | Interface | Theme**, and restart \
Qt Creator.

3. Choose the colour scheme of the same name under **Preferences | Text Editor | Font & Colors | Color Scheme**. Qt \
Creator keeps a colour scheme for each theme, so it comes back with the theme.

## What is coloured

Each theme colours Qt Creator's window: the mode bar, panels, tool bars, tabs, menus, the locator, output panes, the \
terminal, version control, the debugger, the profiler's timeline, icons of the code model, Qt Quick Designer and Qt \
Design Studio's panels. The colour scheme colours the editor: code, the line numbers and current line, selections, \
search results, parenthesis matches, occurrences, diagnostics, diffs, version control logs and code coverage.

## Languages

Qt Creator colours C++ and QML with its code models, which tell declarations, fields, parameters, globals, statics and \
virtual methods apart, and the other languages with KSyntaxHighlighting's definitions, which give fewer roles: a \
language's keywords, types, strings, numbers and comments.

{readme_footer(families, "Qt Creator", "Themes", "the theme, Qt Creator version, language")}"""


def build_qtcreator(families):
    """Writes the themes and colour schemes to build/qtcreator, with the README, changelog and licence, and returns
    build/qtcreator."""
    directory = os.path.join(OUT, "qtcreator")
    for folder in ("themes", "styles"):
        os.makedirs(os.path.join(directory, folder))
    for family in families:
        source = f"{VENDOR_URL}/tree/master/themes/{heritage.folder(family)}"
        for t in family.THEMES:
            name = heritage.qtcreator.name(t)
            write_text(os.path.join(directory, "themes", f"{name}.creatortheme"), heritage.qtcreator.theme(t, source))
            write_text(os.path.join(directory, "styles", f"{name}.xml"), heritage.qtcreator.scheme(t, source))
    write_text(os.path.join(directory, "README.md"), qtcreator_readme(families))
    shutil.copy(os.path.join(ROOT, "qtcreator", "CHANGELOG.md"), os.path.join(directory, "CHANGELOG.md"))
    shutil.copy(os.path.join(ROOT, "LICENSE"), os.path.join(directory, "LICENSE"))
    return directory


def validate_qtcreator(directory, families):
    """Fails the build when a theme leaves out a colour role of Qt Creator or names a colour that its palette lacks,
    a colour scheme leaves out a text style or does not parse, or a text colour is unreadable on its background."""
    themes, schemes = set(), set()
    for family in families:
        for t in family.THEMES:
            name, p = heritage.qtcreator.name(t), t["palette"]
            label = f"Qt Creator {name}"
            themes.add(f"{name}.creatortheme")
            schemes.add(f"{name}.xml")
            parser = configparser.ConfigParser(interpolation=None, comment_prefixes=(";",))
            parser.optionxform = str
            parser.read(os.path.join(directory, "themes", f"{name}.creatortheme"), encoding="utf-8")
            palette = dict(parser["Palette"])
            for value in palette.values():
                if not re.fullmatch(r"[0-9a-f]{8}", value):
                    raise SystemExit(f"{label}: palette colour {value!r} is not aarrggbb")
            colours = dict(parser["Colors"])
            if set(colours) != set(heritage.qtcreator.ROLES):
                raise SystemExit(f"{label}: sets {len(colours)} of the {len(heritage.qtcreator.ROLES)} colour roles")
            for role, value in colours.items():
                if value not in palette and not re.fullmatch(r"[0-9a-f]{8}", value):
                    raise SystemExit(f"{label}: {role} names {value!r}, which the palette lacks")
            if parser["General"]["DefaultTextEditorColorScheme"] != f"{name}.xml" or \
                    parser["General"]["ThemeName"] != p["name"]:
                raise SystemExit(f"{label}: does not name its colour scheme and the theme")
            root = ET.parse(os.path.join(directory, "styles", f"{name}.xml")).getroot()
            styles = {element.get("name") for element in root.iter("style")}
            if styles != set(heritage.qtcreator.STYLES) or root.get("name") != p["name"]:
                raise SystemExit(f"{label}: the colour scheme does not set exactly the text styles of Qt Creator")
            for element in root.iter("style"):
                for key in ("foreground", "background", "underlineColor"):
                    if element.get(key) is not None and not re.fullmatch(r"#[0-9a-f]{6}", element.get(key)):
                        raise SystemExit(f"{label}: {element.get('name')} has {key} {element.get(key)!r}")
            check_styles(label, heritage.qtcreator.styles(p), "fg", "bg", "Text", set(), {"Comment"}, {})
    for folder, expected in (("themes", themes), ("styles", schemes)):
        check_files("Qt Creator themes", directory, folder, expected)


def amp_readme(families):
    """The README in the zip. Links are absolute, as the zip holds the build only."""
    count = sum(len(f.THEMES) for f in families)
    return f"""# Heritage Themes for Amp

{DESCRIPTION} {count} dark and light themes in {len(families)} families; each family maps the named colours of one \
tradition to syntax roles.

## Install

The themes need Amp 0.7 or later in a terminal with 24-bit colour, which runs the matching theme of the \
[Heritage Themes for terminals]({VENDOR_URL}/releases/latest).

1. Copy the files in `themes` into the `themes` folder of Amp's configuration folder, `~/.config/amp` on Linux, \
creating it if it does not exist. In a terminal, from the unzipped folder:

   ```bash
   mkdir -p ~/.config/amp/themes
   cp themes/* ~/.config/amp/themes/
   ```

2. Name a theme in `~/.config/amp/config.yml`, which `Ctrl-A` then **application::display_preferences** opens:

   ```yaml
   theme: heritage-holi-night
   ```

## What is coloured

Each theme colours code, the current line and the status bar. Amp draws text on the terminal's own background, which \
the matching terminal theme gives the theme's background, and its mode indicators in colours of its own.

## Languages

Amp highlights code with the Sublime Text syntaxes it bundles, which tell constructs apart as Sublime Text does, so \
the themes take the rules of the Sublime Text colour schemes. It has no syntax for Kotlin, TypeScript, TSX, Vue or \
TOML, which open as plain text.

{readme_footer(families, "Amp", "Themes", "the theme, Amp version, terminal, language")}"""


def validate_amp(directory, families):
    """Fails the build when a file is missing, a theme does not parse or differs from heritage.amp, or a rule's colour
    is unreadable on the background."""
    expected = set()
    for family in families:
        for t in family.THEMES:
            name, p = heritage.amp.name(t), t["palette"]
            expected.add(f"{name}.tmTheme")
            label = f"Amp {name}"
            with open(os.path.join(directory, "themes", f"{name}.tmTheme"), "rb") as f:
                data = plistlib.load(f)
            if data["settings"][0]["settings"] != heritage.amp.settings(p) or data["name"] != p["name"]:
                raise SystemExit(f"{label}: the global settings differ from heritage.amp.settings")
            found = [(r["scope"], r["settings"]["foreground"], r["settings"]["fontStyle"]) for r in data["settings"][1:]]
            if found != [(scope, colour, font) for _, scope, colour, font in heritage.amp.rules(p)]:
                raise SystemExit(f"{label}: the rules differ from heritage.amp.rules")
            check_styles(label, heritage.amp.styles(p), "fg", "bg", None, set(),
                         {k for k in heritage.amp.styles(p) if "comment" in k.split(" (")[0]}, {})
    check_files("Amp themes", directory, "themes", expected)


def eclipse_readme(families):
    """The README in the zip. Links are absolute, as the zip holds the build only."""
    count = sum(len(f.THEMES) for f in families)
    return f"""# Heritage Themes for Eclipse

{DESCRIPTION} {count} dark and light themes in {len(families)} families, in one plugin; each family maps the named \
colours of one tradition to syntax roles.

## Install

The plugin needs Eclipse 2026-09 (4.41) or later.

1. Copy `{heritage.eclipse.jar_name(VERSION)}` into the `dropins` folder of your Eclipse installation, beside \
`plugins`, and restart Eclipse.

2. Choose a theme, for example **Holi Night**, under **Window | Preferences | General | Appearance | Theme** (on \
macOS, **Eclipse | Settings…**), and restart Eclipse.

3. For the languages that open in the generic editor, such as Python, Go, Rust or YAML, choose the TextMate theme of \
the same name under **Window | Preferences | TextMate | Theme**, as the default for dark or light appearance as the \
theme is.

## What is coloured

Each theme colours the window, tool bars, views, tabs, forms, dialogs and the status line, and the editors: text, \
the current line, selections, line numbers, occurrences, search results, annotations and hovers; Java, with JDT's \
semantic highlighting, Javadoc and properties files; Ant files; the console; EGit's diffs, history and staging; \
compare; Mylyn's tasks and its markup editors with their preview, which opens README files; and EclEmma's coverage. \
The TextMate theme colours every language that TM4E highlights. Eclipse draws scroll bars, buttons and the selection \
in lists and trees with the system's widgets.

## Languages

JDT colours Java with its semantic highlighting, which tells classes, interfaces, fields, static fields, constants, \
parameters, locals and method declarations apart in a Java project. TM4E colours the other languages with TextMate \
grammars and the TextMate theme, which take the rules of the Sublime Text colour schemes.

{readme_footer(families, "Eclipse", "Themes", "the theme, Eclipse version and package, language")}"""


def build_eclipse(families):
    """Writes the plugin jar to build/eclipse, with the README, changelog and licence, and returns build/eclipse."""
    directory = os.path.join(OUT, "eclipse")
    os.makedirs(directory)
    themes = [t for f in families for t in f.THEMES]
    sources = {t["slug"]: f"{VENDOR_URL}/tree/master/themes/{heritage.folder(f)}" for f in families for t in f.THEMES}
    with open(os.path.join(directory, heritage.eclipse.jar_name(VERSION)), "wb") as f:
        f.write(heritage.eclipse.jar(themes, VERSION, "Heritage Themes", sources))
    write_text(os.path.join(directory, "README.md"), eclipse_readme(families))
    shutil.copy(os.path.join(ROOT, "eclipse", "CHANGELOG.md"), os.path.join(directory, "CHANGELOG.md"))
    shutil.copy(os.path.join(ROOT, "LICENSE"), os.path.join(directory, "LICENSE"))
    return directory


def validate_eclipse(directory, families):
    """Fails the build when the jar's manifest, plugin.xml, stylesheets or TextMate themes are missing or malformed,
    a stylesheet sets a colour its palette lacks or leaves a brace open, or a text colour is unreadable."""
    themes = [t for f in families for t in f.THEMES]
    with zipfile.ZipFile(os.path.join(directory, heritage.eclipse.jar_name(VERSION))) as z:
        names = set(z.namelist())
        expected = {"META-INF/MANIFEST.MF", "plugin.xml"} | \
            {f"css/{heritage.eclipse.name(t)}.css" for t in themes} | \
            {f"textmate/{heritage.eclipse.name(t)}.tmTheme" for t in themes}
        if names != expected:
            raise SystemExit(f"Eclipse plugin: holds {sorted(names ^ expected)[:5]} wrongly")
        manifest = z.read("META-INF/MANIFEST.MF").decode()
        if f"Bundle-SymbolicName: {heritage.eclipse.BUNDLE};singleton:=true" not in manifest or \
                f"Bundle-Version: {VERSION}" not in manifest:
            raise SystemExit("Eclipse plugin: the manifest does not name the bundle and its version")
        root = ET.fromstring(z.read("plugin.xml"))
        css = {e.get("id"): e.get("basestylesheeturi") for e in root.iter("theme") if e.get("basestylesheeturi")}
        tm = {e.get("id"): e.get("path") for e in root.iter("theme") if e.get("path")}
        if css != {heritage.eclipse.theme_id(t): f"css/{heritage.eclipse.name(t)}.css" for t in themes} or \
                tm != {heritage.eclipse.tm4e_id(t): f"textmate/{heritage.eclipse.name(t)}.tmTheme" for t in themes}:
            raise SystemExit("Eclipse plugin: plugin.xml does not contribute every theme")
        for t in themes:
            p, label = t["palette"], f"Eclipse {heritage.eclipse.name(t)}"
            text = z.read(f"css/{heritage.eclipse.name(t)}.css").decode()
            code = re.sub(r"/\*.*?\*/|'[^']*'|\"[^\"]*\"", "", text, flags=re.S)
            if code.count("{") != code.count("}"):
                raise SystemExit(f"{label}: the stylesheet's braces do not balance")
            colours = {v.upper() for v in heritage.eclipse.hexes(p).values()}
            # Eclipse splits a preference at its last "=", and a value runs to the end of its line
            for preference in re.findall(r"^\s*'([^'\n]*)'$", text, flags=re.M):
                if preference.count("=") != 1:
                    raise SystemExit(f"{label}: the preference {preference[:60]!r} has no single '='")
            for colour in re.findall(r"#[0-9A-Fa-f]{6}\b", re.sub(r"/\*.*?\*/", "", text, flags=re.S)):
                if colour.upper() not in colours:
                    raise SystemExit(f"{label}: the stylesheet sets {colour}, which the palette lacks")
            for value in re.findall(r"=(\d+,\d+,\d+)'", text):
                if "#" + "".join(f"{int(v):02X}" for v in value.split(",")) not in colours:
                    raise SystemExit(f"{label}: a preference sets {value}, which the palette lacks")
            plistlib.loads(z.read(f"textmate/{heritage.eclipse.name(t)}.tmTheme"))
            check_styles(label, heritage.eclipse.styles(p), "fg", "bg", "editor text", set(), {"Java comment"}, {})
    for name in ("README.md", "CHANGELOG.md", "LICENSE"):
        if not os.path.isfile(os.path.join(directory, name)):
            raise SystemExit(f"Eclipse plugin: {name} is missing")


def nova_readme(families):
    """The README in the zip, which is also the extension's README in Nova. Links are absolute."""
    count = sum(len(f.THEMES) for f in families)
    return f"""# Heritage Themes for Nova

{DESCRIPTION} {count} dark and light themes in {len(families)} families, in one extension; each family maps the \
named colours of one tradition to syntax roles.

## Install

Double-click `{heritage.nova.FOLDER}` in the unzipped folder, which installs the extension in Nova, then choose a \
theme, for example **Holi Night**, under **Nova | Settings | Themes**, for the light or dark appearance or both.

## What is coloured

Each theme colours the window, the title bar, buttons, text fields, the editor with its gutter, cursor, selection and \
indent guides, code in every language that Nova's grammars highlight, and the terminal.

{readme_footer(families, "Nova", "Themes", "the theme, Nova version, language")}"""


def build_nova(families):
    """Writes the extension to build/nova/<extension>, with the README, changelog and licence in it and beside it,
    and returns build/nova."""
    directory = os.path.join(OUT, "nova")
    extension = os.path.join(directory, heritage.nova.FOLDER)
    os.makedirs(os.path.join(extension, "Themes"))
    for family in families:
        source = f"{VENDOR_URL}/tree/master/themes/{heritage.folder(family)}"
        for t in family.THEMES:
            write_text(os.path.join(extension, heritage.nova.file_name(t)), heritage.nova.theme(t, source))
    write_text(os.path.join(extension, "extension.json"), heritage.nova.manifest(VERSION, VENDOR_URL, DESCRIPTION))
    for folder in (directory, extension):
        write_text(os.path.join(folder, "README.md"), nova_readme(families))
        shutil.copy(os.path.join(ROOT, "nova", "CHANGELOG.md"), os.path.join(folder, "CHANGELOG.md"))
        shutil.copy(os.path.join(ROOT, "LICENSE"), os.path.join(folder, "LICENSE"))
    return directory


def validate_nova(directory, families):
    """Fails the build when a theme is missing, a stylesheet differs from heritage.nova or names a colour that is not
    #RRGGBB, the manifest is malformed, or a text colour is unreadable on its background."""
    extension = os.path.join(directory, heritage.nova.FOLDER)
    with open(os.path.join(extension, "extension.json"), encoding="utf-8") as f:
        manifest = json.load(f)
    if manifest["identifier"] != heritage.nova.IDENTIFIER or manifest["version"] != VERSION or \
            manifest["categories"] != ["themes"]:
        raise SystemExit("Nova extension: extension.json does not name the extension, its version and category")
    themes = [t for f in families for t in f.THEMES]
    expected = {os.path.basename(heritage.nova.file_name(t)) for t in themes}
    if len(expected) != len(themes):
        raise SystemExit("Nova themes: two themes have the same file name")
    for t in themes:
        p, label = t["palette"], f"Nova {t['palette']['name']}"
        if not WINDOWS_NAME.fullmatch(p["name"]):
            raise SystemExit(f"{label}: the name is no file name")
        with open(os.path.join(extension, heritage.nova.file_name(t)), encoding="utf-8") as f:
            parsed = heritage.nova.parse(f.read())
        if len(parsed) != len(heritage.nova.ui(p)) + len(heritage.nova.syntax(p)) + 16:
            raise SystemExit(f"{label}: the stylesheet does not set every selector of heritage.nova")
        for selector, properties in parsed.items():
            for prop, value in properties.items():
                if prop.endswith("color") and not prop.startswith("-theme-") and \
                        not re.fullmatch(r"#[0-9A-F]{6}", value):
                    raise SystemExit(f"{label}: {selector} has {prop} {value!r}")
        check_styles(label, heritage.nova.styles(p), "fg", "bg", "meta.text", set(), {"comment"}, {})
    check_files("Nova themes", extension, "Themes", expected)


# Product → its themes' names in READMEs, the README writer, and the folder its theme files go in.
TERMINAL_NAMES = {"terminals": heritage.terminals.name, "Nano": heritage.nano.name, "Lapce": heritage.lapce.name,
                  "Qt Creator": heritage.qtcreator.name, "Amp": heritage.amp.name, "Eclipse": heritage.eclipse.name,
                  "Nova": lambda t: t["palette"]["name"],
                  "Textadept": heritage.textadept.name, "Kakoune": heritage.kakoune.name, "Micro": heritage.micro.name,
                  "Vim": heritage.vim.name,
                  "Emacs": heritage.emacs.name}
TERMINAL_READMES = {"Nano": nano_readme, "Textadept": textadept_readme, "Amp": amp_readme, "Kakoune": kakoune_readme, "Micro": micro_readme, "Vim": vim_readme, "Emacs": emacs_readme}


def terminals_readme(families):
    """The README in the zip. Links are absolute, as the zip holds the build only."""
    count = sum(len(f.THEMES) for f in families)
    modules = heritage.terminals.modules()
    # the examples name Holi's themes, as the other products' READMEs do
    dark, light = (next(t for f in families for t in f.THEMES if t["slug"] == slug) for slug in ("HoliNight", "HoliDay"))
    def install(module):
        text = module.INSTALL
        for key, value in (("{stem}", heritage.terminals.name(dark)), ("{label}", dark["palette"]["name"]),
                           ("{light_stem}", heritage.terminals.name(light)),
                           ("{light_label}", light["palette"]["name"])):
            text = text.replace(key, value)
        return text
    sections = []
    for category in heritage.terminals.CATEGORIES:
        sections.append(f"## {category}")
        sections += [f"### {m.APP}\n\n{install(m)}" for m in modules if m.CATEGORY == category]
    sections = "\n\n".join(sections)
    contents = ", ".join(f"[{m.APP}](#{re.sub(r'[^a-z0-9 -]', '', m.APP.lower()).replace(' ', '-')})"
                         for m in modules)
    return f"""# Heritage Themes for terminals

{DESCRIPTION} {count} dark and light themes in {len(families)} families, for {len(modules)} terminal emulators, \
shells, prompts and multiplexers: {contents}.

Each app has a folder of its own. A theme's file takes the name that the table at the end gives it, \
`{heritage.terminals.name(dark)}` for **{dark["palette"]["name"]}**, or the theme's name where the app lists a theme \
by its file name.

The shells, prompts and multiplexers set text colours over the terminal's own background, so they read as \
intended in a terminal that runs the same theme, and need a terminal with 24-bit colour.

{sections}

## The terminal colours

Every terminal emulator theme gives the 16 ANSI colours the same values, as the terminals of the editor themes do. \
Red, green, yellow, blue, magenta and cyan are the theme's ANSI colours, alike in their normal and bright forms. \
Black is the theme's faint text colour and bright black its muted text; white is the operator colour and bright \
white the text colour. In a light theme, black is therefore light and white dark, so that every colour reads on \
the light background, as the colours of the dark theme do on the dark one.

{readme_footer(families, "terminals", "Themes", "the theme, the app and its version, the terminal")}"""


def build_terminals(families):
    """Writes every app's files to build/terminals/<folder>, with the README, changelog and licence, and returns
    build/terminals."""
    directory = os.path.join(OUT, "terminals")
    themes = [t for f in families for t in f.THEMES]
    sources = {t["slug"]: f"{VENDOR_URL}/tree/master/themes/{heritage.folder(f)}" for f in families for t in f.THEMES}
    for module in heritage.terminals.modules():
        os.makedirs(os.path.join(directory, module.FOLDER))
        files = [entry for t in themes for entry in module.files(t, sources[t["slug"]])]
        if hasattr(module, "combined"):
            files += module.combined(themes, VENDOR_URL)
        for filename, text in files:
            path = os.path.join(directory, module.FOLDER, filename)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            write_text(path, text)
    write_text(os.path.join(directory, "README.md"), terminals_readme(families))
    shutil.copy(os.path.join(ROOT, "terminals", "CHANGELOG.md"), os.path.join(directory, "CHANGELOG.md"))
    shutil.copy(os.path.join(ROOT, "LICENSE"), os.path.join(directory, "LICENSE"))
    return directory


def validate_terminals(directory, families):
    """Fails the build when an app's folder holds other files than its module writes, a file does not parse or differs
    from the colours its module gives, or a text colour of an app is below its minimum contrast on its background."""
    themes = [t for f in families for t in f.THEMES]
    for module in heritage.terminals.modules():
        folder = os.path.join(directory, module.FOLDER)
        found = {os.path.relpath(os.path.join(root, name), folder).replace(os.sep, "/")
                 for root, _, names in os.walk(folder) for name in names}
        expected = {filename for t in themes for filename, _ in module.files(t, "")}
        if hasattr(module, "combined"):
            expected |= {filename for filename, _ in module.combined(themes, "")}
        if found != expected:
            raise SystemExit(f"{module.APP}: {len(found)} files in {module.FOLDER} for {len(expected)} expected")
        def read(filename):
            with open(os.path.join(folder, filename), encoding="utf-8") as f:
                return f.read()
        try:
            if hasattr(module, "combined"):
                module.validate_combined(themes, {filename: read(filename)
                                                  for filename, _ in module.combined(themes, "")})
            else:
                for t in themes:
                    (filename, _), = module.files(t, "")
                    module.validate(t, read(filename))
        except (ValueError, KeyError) as error:
            raise SystemExit(f"{module.APP}: {error}")
        for t in themes:
            for element, text, background, minimum in module.pairs(t["palette"]):
                ratio = contrast(text[1:], background[1:])
                if ratio < minimum:
                    raise SystemExit(f"{module.APP} {t['palette']['name']}: {element} is {ratio:.2f}:1 "
                                     f"({text} on {background}), needs {minimum}:1")
    for name in ("README.md", "CHANGELOG.md", "LICENSE"):
        if not os.path.isfile(os.path.join(directory, name)):
            raise SystemExit(f"Terminals: {name} is missing")


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
    <Tags>theme;color theme;dark theme;light theme;culture;heritage</Tags>
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
    # the limits of the VSIX schema 2.0 reference, and of VsixPublisher for a single tag
    metadata = {tag: root.find(f"v:Metadata/v:{tag}", namespace).text for tag in ("DisplayName", "Description", "Tags")}
    limits = {"Id": (identity.get("Id"), 100), "Publisher": (identity.get("Publisher") or "", 100),
              "DisplayName": (metadata["DisplayName"], 50), "Description": (metadata["Description"], 1000),
              "Tags": (metadata["Tags"], 100)}
    for name, (value, limit) in limits.items():
        if len(value) > limit:
            raise SystemExit(f"Visual Studio extension.vsixmanifest: {name} has {len(value)} characters, the limit is {limit}")
    for tag in metadata["Tags"].split(";"):
        if not tag.strip() or len(tag) > 50 or "," in tag:
            raise SystemExit(f"Visual Studio extension.vsixmanifest: the tag {tag!r} is not one tag of 1 to 50 characters; "
                             "<Tags> separates tags with semicolons")
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
                                                 "plugin, and the Notepad++, Xcode, Helix, Kakoune, Micro, Vim and "
                                                 "Emacs themes.")
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
    helix_themes = build_helix(families)
    validate_helix(helix_themes, families)
    print(f"{pack_helix(helix_themes)}: {len(themes)} themes", flush=True)
    for editor, folder, files, validate_themes in (
            ("Kakoune", "colors", lambda t, source: (f"{heritage.kakoune.name(t)}.kak",
                                                      heritage.kakoune.colorscheme(t["palette"], source)),
             validate_kakoune),
            ("Micro", "colorschemes", lambda t, source: (f"{heritage.micro.name(t)}.micro",
                                                          heritage.micro.colorscheme(t["palette"], source)),
             validate_micro),
            ("Vim", "colors", lambda t, source: (f"{heritage.vim.name(t)}.vim",
                                                  heritage.vim.colorscheme(t["palette"], heritage.vim.name(t), source)),
             validate_vim),
            ("Emacs", "themes", lambda t, source: (f"{heritage.emacs.name(t)}-theme.el",
                                                    heritage.emacs.theme(t["palette"], heritage.emacs.name(t), source,
                                                                         VENDOR_URL)),
             validate_emacs),
            ("Nano", "schemes", lambda t, source: (f"{heritage.nano.name(t)}.nanorc",
                                                    heritage.nano.colorscheme(t["palette"], source)),
             validate_nano),
            ("Textadept", "themes", lambda t, source: (f"{heritage.textadept.name(t)}.lua",
                                                        heritage.textadept.theme(t["palette"], source)),
             validate_textadept),
            ("Amp", "themes", lambda t, source: (f"{heritage.amp.name(t)}.tmTheme",
                                                  heritage.amp.theme(t["palette"], source)),
             validate_amp)):
        directory = build_themes(families, editor, folder, files)
        validate_themes(directory, families)
        name = f"{VSCODE_NAME}-{editor.lower()}"
        print(f"{pack_folder(directory, os.path.join(OUT, f'{name}-{VERSION}.zip'), name)}: {len(themes)} themes",
              flush=True)
    nova = build_nova(families)
    validate_nova(nova, families)
    print(f"{pack_folder(nova, os.path.join(OUT, f'{VSCODE_NAME}-nova-{VERSION}.zip'), f'{VSCODE_NAME}-nova')}: "
          f"{len(themes)} themes", flush=True)
    eclipse = build_eclipse(families)
    validate_eclipse(eclipse, families)
    print(f"{pack_folder(eclipse, os.path.join(OUT, f'{VSCODE_NAME}-eclipse-{VERSION}.zip'), f'{VSCODE_NAME}-eclipse')}: "
          f"{len(themes)} themes", flush=True)
    qtcreator = build_qtcreator(families)
    validate_qtcreator(qtcreator, families)
    print(f"{pack_folder(qtcreator, os.path.join(OUT, f'{VSCODE_NAME}-qtcreator-{VERSION}.zip'), f'{VSCODE_NAME}-qtcreator')}: "
          f"{len(themes)} themes", flush=True)
    lapce = build_lapce(families)
    validate_lapce(lapce, families)
    print(f"{pack_folder(lapce, os.path.join(OUT, f'{VSCODE_NAME}-lapce-{VERSION}.zip'), f'{VSCODE_NAME}-lapce')}: "
          f"{len(themes)} themes", flush=True)
    terminals = build_terminals(families)
    validate_terminals(terminals, families)
    package = os.path.join(OUT, f"{TERMINALS_NAME}-{VERSION}.zip")
    print(f"{pack_folder(terminals, package, TERMINALS_NAME)}: {len(themes)} themes for "
          f"{len(heritage.terminals.APPS)} apps", flush=True)
    if args.vsix:
        print(f"{pack_vsix(extension, themes)}: {len(themes)} themes")


if __name__ == "__main__":
    main()
