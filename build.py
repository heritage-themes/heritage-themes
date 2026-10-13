"""Builds the Heritage Themes plugin from every theme folder.

A theme folder is any top-level directory containing a gen.py that provides FAMILY, BLURB and
generate(). Run `python3 build.py`; output goes to build/.
"""
import importlib.util, json, os, shutil, zipfile

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "build")
VERSION = "1.0.0"
CHANGE_NOTES = "Initial release with Wuxing Night and Wuxing Day."
PLUGIN_ICONS = ("pluginIcon.svg", "pluginIcon_dark.svg")


def load_families():
    families = []
    for name in sorted(os.listdir(ROOT)):
        path = os.path.join(ROOT, name, "gen.py")
        if not os.path.isfile(path):
            continue
        spec = importlib.util.spec_from_file_location(f"heritage_{name}", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        families.append(module)
    return families


def plugin_xml(families, themes):
    blurbs = "\n".join(f"      <li><b>{f.FAMILY}</b>: {f.BLURB}</li>" for f in families)
    providers = "\n".join(
        f'    <themeProvider id="{t["id"]}" path="/themes/{t["slug"]}.theme.json"/>' for t in themes)
    return f"""<idea-plugin>
  <id>heritage.themes</id>
  <name>Heritage Themes</name>
  <version>{VERSION}</version>
  <vendor>Heritage Themes</vendor>
  <description><![CDATA[
    <p>Colour themes drawn from the colour traditions of different cultures.</p>
    <ul>
{blurbs}
    </ul>
  ]]></description>
  <change-notes><![CDATA[
    <b>{VERSION}</b>: {CHANGE_NOTES}
  ]]></change-notes>
  <idea-version since-build="233"/>
  <depends>com.intellij.modules.platform</depends>
  <extensions defaultExtensionNs="com.intellij">
{providers}
  </extensions>
</idea-plugin>
"""


def main():
    families = load_families()
    themes = [t for f in families for t in f.generate()]
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
    print(f"{jar}: {len(themes)} themes")


if __name__ == "__main__":
    main()
