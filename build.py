"""Builds the Heritage Themes plugin from every theme folder.

A theme folder is any top-level directory containing a theme.py (see heritage/__init__.py).
Run `python3 build.py`; output goes to build/.
"""
import html, json, os, re, shutil, zipfile
import xml.etree.ElementTree as ET

import heritage

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "build")
CHANGELOG = os.path.join(ROOT, "CHANGELOG.md")
VERSION = "1.0.0"
VENDOR_URL = "https://github.com/heritage-themes/heritage-themes"
PLUGIN_ICONS = ("pluginIcon.svg", "pluginIcon_dark.svg")


def change_notes():
    """HTML for the plugin's change notes: the CHANGELOG.md section for VERSION, else [Unreleased]."""
    with open(CHANGELOG) as f:
        text = f.read()
    for heading in (f"[{VERSION}]", "[Unreleased]"):
        match = re.search(rf"^## {re.escape(heading)}[^\n]*\n(.*?)(?=^## \[|\Z)", text, re.M | re.S)
        if match and match.group(1).strip():
            return changelog_html(match.group(1))
    raise SystemExit(f"CHANGELOG.md has no entries under [{VERSION}] or [Unreleased]")


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
    <p>Colour themes drawn from the colour traditions of different cultures.</p>
    <ul>
{blurbs}
    </ul>
  ]]></description>
  <change-notes><![CDATA[
    <b>{VERSION}</b>
{change_notes()}
  ]]></change-notes>
  <idea-version since-build="233"/>
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


def main():
    families = heritage.load_families()
    themes = [t for f in families for t in heritage.generate(f)]
    for key in ("slug", "id", "name"):
        values = [t[key] for t in themes]
        if len(values) != len(set(values)):
            raise SystemExit(f"duplicate theme {key}")

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


if __name__ == "__main__":
    main()
