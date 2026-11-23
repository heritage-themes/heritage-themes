"""Screenshots a GUI editor showing a sample with a Heritage theme, inside the heritage-editors container.

Usage: python3 shoot.py EDITOR THEME FILES SAMPLE OUT.png

EDITOR is a key of EDITORS, THEME the theme's file name stem, FILES the folder of the editor's generated files and
SAMPLE the file to open. The editor starts on Xvfb in a fresh HOME with the theme installed and chosen as its README
says, opens a copy of the sample, and its window is captured WAIT seconds later. The editor's output goes to
OUT.png.log.
"""
import os, re, shutil, signal, subprocess, sys, tempfile, time

DISPLAY = ":99"
FONT = "JetBrains Mono"
WIDTH, HEIGHT = 1100, 700


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def textadept(home, stem, files, sample):
    os.makedirs(f"{home}/.textadept/themes")
    shutil.copy(f"{files}/{stem}.lua", f"{home}/.textadept/themes/{stem}.lua")
    write(f"{home}/.textadept/init.lua",
          f"view:set_theme('{stem}', {{font = '{FONT}', size = 11}})\n"
          f"events.connect(events.INITIALIZED, function() ui.size = {{{WIDTH}, {HEIGHT}}} end)\n")
    return ["/opt/textadept/textadept", sample], {"QT_QPA_PLATFORM": "xcb"}


def lapce(home, stem, files, sample):
    # the plugin folder in Lapce's plugins folder and the theme chosen by its name in settings.toml, as the README says
    plugin = f"{home}/.local/share/lapce-stable/plugins/heritage-themes"
    shutil.copytree(f"{files}/heritage-themes", plugin)
    # grammars in Lapce's data folder and their queries in its configuration folder, where Lapce keeps them
    shutil.copytree("/opt/lapce-data/grammars", f"{home}/.local/share/lapce-stable/grammars")
    shutil.copytree("/opt/lapce-data/queries", f"{home}/.config/lapce-stable/queries")
    with open(f"{plugin}/themes/{stem}.toml", encoding="utf-8") as f:
        label = next(line for line in f if line.startswith("name = ")).split(" = ", 1)[1].strip()
    write(f"{home}/.config/lapce-stable/settings.toml",
          f'[core]\ncolor-theme = {label}\n\n[editor]\nfont-family = "{FONT}"\nfont-size = 13\n')
    return ["/opt/lapce/lapce", "--wait", "--new", sample], {}


def qtcreator(home, stem, files, sample):
    # the theme and colour scheme in the user's themes and styles folders, the theme chosen and the scheme chosen for
    # it, as the README says; Qt Creator keeps the scheme per theme in a map, which QSettings writes as Qt Creator does
    from PyQt6.QtCore import QSettings
    settings = f"{home}/.config/QtProject"
    os.makedirs(f"{settings}/qtcreator/themes")
    os.makedirs(f"{settings}/qtcreator/styles")
    shutil.copy(f"{files}/themes/{stem}.creatortheme", f"{settings}/qtcreator/themes/")
    shutil.copy(f"{files}/styles/{stem}.xml", f"{settings}/qtcreator/styles/")
    ini = QSettings(f"{settings}/QtCreator.ini", QSettings.Format.IniFormat)
    ini.setValue("Core/CreatorTheme", stem)
    ini.setValue("TextEditor/ColorSchemes", {stem: f"{settings}/qtcreator/styles/{stem}.xml"})
    ini.setValue("TextEditor/FontFamily", FONT)
    ini.setValue("TextEditor/FontSize", 11)
    ini.setValue("Welcome/ShowTour", False)
    ini.sync()
    return (["/usr/bin/qtcreator", "-settingspath", f"{home}/.config", "-noload", "Welcome", sample],
            {"QT_QPA_PLATFORM": "xcb"})


def kate(home, stem, files, sample):
    # the theme and window colour scheme in the user's data folder and the scheme chosen under Settings | Window
    # Color Scheme, as the README says; the editor's theme is left at Kate's default, Follow System Color Scheme,
    # which chooses the theme of the same name, so a preview that shows another theme shows that the pairing fails
    data = f"{home}/.local/share"
    os.makedirs(f"{data}/org.kde.syntax-highlighting/themes")
    os.makedirs(f"{data}/color-schemes")
    shutil.copy(f"{files}/themes/{stem}.theme", f"{data}/org.kde.syntax-highlighting/themes/")
    shutil.copy(f"{files}/color-schemes/{stem}.colors", f"{data}/color-schemes/")
    write(f"{home}/.config/katerc",
          f"[UiSettings]\nColorScheme={stem}\n\n"
          f"[KTextEditor Renderer]\nText Font={FONT},11,-1,5,400,0,0,0,0,0,0,0,0,0,0,1\n\n"
          "[General]\nShow welcome view for new window=false\n")
    return ["/usr/bin/kate", "--new", sample], {"QT_QPA_PLATFORM": "xcb"}


def gnome_text_editor(home, stem, files, sample):
    # the style scheme in the user's GtkSourceView styles folder and chosen under Preferences | Appearance, as the README
    # says, with the desktop's style forced to the scheme's, as a desktop in that style would set it; GNOME Text
    # Editor keeps its settings in GSettings, here in the key file that the keyfile backend reads; line numbers and the
    # current line's highlight on, so that the preview shows their colours
    os.makedirs(f"{home}/.local/share/gtksourceview-5/styles")
    shutil.copy(f"{files}/styles/{stem}.xml", f"{home}/.local/share/gtksourceview-5/styles/")
    with open(f"{files}/styles/{stem}.xml", encoding="utf-8") as f:
        dark = '<property name="variant">dark</property>' in f.read()
    write(f"{home}/.config/glib-2.0/settings/keyfile",
          f"[org/gnome/TextEditor]\nstyle-scheme='{stem}'\nstyle-variant='{'dark' if dark else 'light'}'\n"
          f"restore-session=false\nuse-system-font=false\ncustom-font='{FONT} 11'\nshow-line-numbers=true\n"
          "highlight-current-line=true\n")
    return (["/usr/bin/gnome-text-editor", "--standalone", sample],
            {"GSETTINGS_BACKEND": "keyfile", "GDK_BACKEND": "x11", "GTK_A11Y": "none"})


def gedit(home, stem, files, sample):
    # the style scheme in the user's libgedit-gtksourceview styles folder and chosen under Preferences | Font & Colors
    # for the style it suits, as the README says, with gedit's style forced to the scheme's, as a desktop in that style
    # would set it; gedit keeps its settings in GSettings, here in the key file that the keyfile backend reads; line
    # numbers and the current line's highlight are on by default
    os.makedirs(f"{home}/.local/share/libgedit-gtksourceview-300/styles")
    shutil.copy(f"{files}/styles/{stem}.xml", f"{home}/.local/share/libgedit-gtksourceview-300/styles/")
    with open(f"{files}/styles/{stem}.xml", encoding="utf-8") as f:
        variant = re.search(r'kind="(light|dark)"', f.read()).group(1)
    write(f"{home}/.config/glib-2.0/settings/keyfile",
          f"[org/gnome/gedit/preferences/editor]\nstyle-scheme-for-{variant}-theme-variant='{stem}'\n"
          f"use-default-font=false\neditor-font='{FONT} 11'\n\n"
          f"[org/gnome/gedit/preferences/ui]\ntheme-variant='{variant}'\n")
    return (["/usr/bin/gedit", "--standalone", sample],
            {"GSETTINGS_BACKEND": "keyfile", "GDK_BACKEND": "x11", "GTK_A11Y": "none"})


def geany(home, stem, files, sample):
    # the colour scheme in the user's colorschemes folder and chosen under View | Change Color Scheme, as the README
    # says, which Geany keeps in geany.conf; the side bar, message window and toolbar hidden and no session restored,
    # so that the window shows the editor and its tab
    os.makedirs(f"{home}/.config/geany/colorschemes")
    shutil.copy(f"{files}/colorschemes/{stem}.conf", f"{home}/.config/geany/colorschemes/")
    write(f"{home}/.config/geany/geany.conf",
          f"[geany]\ncolor_scheme={stem}.conf\neditor_font={FONT} 11\npref_main_load_session=false\n"
          f"sidebar_visible=false\nmsgwindow_visible=false\npref_toolbar_show=false\n"
          f"geometry=0;0;{WIDTH};{HEIGHT};0\n")
    return ["/usr/bin/geany", "--new-instance", sample], {"GDK_BACKEND": "x11", "GTK_A11Y": "none"}


def eclipse(home, stem, files, sample):
    # the plugin in a dropins folder, the appearance theme and the TextMate theme of the same name chosen in the
    # workspace's preferences and the welcome page off, as a user chooses the themes once in the preferences
    os.makedirs(f"{home}/dropins")
    for jar in os.listdir(f"{files}/eclipse"):
        shutil.copy(f"{files}/eclipse/{jar}", f"{home}/dropins/")
    with open(f"{files}/{THEME_IDS}", encoding="utf-8") as f:
        theme, textmate, brightness = next(line.split("\t")[1:] for line in f.read().splitlines()
                                           if line.split("\t")[0] == stem)
    settings = f"{home}/workspace/.metadata/.plugins/org.eclipse.core.runtime/.settings"
    write(f"{settings}/org.eclipse.e4.ui.css.swt.theme.prefs", f"eclipse.preferences.version=1\nthemeid={theme}\n")
    write(f"{settings}/org.eclipse.tm4e.ui.prefs", "eclipse.preferences.version=1\n"
          f"org.eclipse.tm4e.ui.themes.default{brightness.title()}Theme={textmate}\n")
    write(f"{settings}/org.eclipse.ui.prefs", "eclipse.preferences.version=1\nshowIntro=false\n")
    write(f"{settings}/org.eclipse.ui.editors.prefs", "eclipse.preferences.version=1\nlineNumberRuler=true\n")
    write(f"{settings}/org.eclipse.jface.prefs",
          f"eclipse.preferences.version=1\norg.eclipse.jface.textfont=1|{FONT}|11.0|0|GTK|1|;\n")
    return (["/opt/eclipse/eclipse", "-data", f"{home}/workspace", "-nosplash", "--launcher.openFile", sample,
             "-vmargs", f"-Dorg.eclipse.equinox.p2.reconciler.dropins.directory={home}/dropins",
             f"-Dosgi.configuration.area={home}/configuration"], {"GDK_BACKEND": "x11"})


def pulsar(home, stem, files, sample):
    # the theme's UI and syntax packages in the packages folder of Pulsar's home and chosen under Settings | Themes,
    # which Pulsar keeps in config.cson, as the README says; the sample opened in a project folder of its own, so that
    # the tree view shows it. The welcome page, change log and the GitHub package's Git panel, which first runs open,
    # are off, so that the window shows the tree view, the editor and the status bar. Electron's GPU process does not
    # start on Xvfb, and Pulsar paints nothing until it is off.
    atom_home = f"{home}/.pulsar"
    for kind in ("ui", "syntax"):
        shutil.copytree(f"{files}/packages/{stem}-{kind}", f"{atom_home}/packages/{stem}-{kind}")
    write(f"{atom_home}/config.cson",
          f'"*":\n  core:\n    telemetryConsent: "no"\n    disabledPackages: ["github"]\n'
          f'    themes: ["{stem}-ui", "{stem}-syntax"]\n'
          f'  editor:\n    fontFamily: "{FONT}"\n    fontSize: 14\n'
          f'  welcome:\n    showOnStartup: false\n    showChangeLog: false\n')
    write(f"{atom_home}/init.js", f"atom.packages.onDidActivateInitialPackages(() => {{\n"
                                  f"  atom.setPosition(0, 0);\n  atom.setSize({WIDTH}, {HEIGHT});\n}});\n")
    project = f"{home}/project"
    os.makedirs(project)
    shutil.move(sample, project)
    return (["/opt/Pulsar/pulsar", "--no-sandbox", "--disable-gpu", "--foreground", project,
             f"{project}/{os.path.basename(sample)}"], {"ATOM_HOME": atom_home})


EDITORS = {"textadept": textadept, "lapce": lapce, "qtcreator": qtcreator, "kate": kate,
           "gnome-text-editor": gnome_text_editor, "gedit": gedit, "geany": geany, "eclipse": eclipse,
           "pulsar": pulsar}
# The file beside the eclipse folder that names each theme's identifier, stem=identifier per line.
THEME_IDS = "eclipse-theme-ids.txt"
WAIT = {"textadept": 5, "lapce": 12, "qtcreator": 15, "kate": 8, "gnome-text-editor": 6, "gedit": 6, "geany": 5, "eclipse": 10,
        "pulsar": 8}
# Editors whose window title names the open file, with the most seconds to wait for it before WAIT.
TITLED = {"eclipse": 180, "pulsar": 120}
# Samples that an editor opens as a project, by the name they are opened under instead.
RENAME = {("qtcreator", "Cargo.toml"): "settings.toml"}
# Window classes of the editors that shoot.py resizes to WIDTH x HEIGHT.
RESIZE = {"lapce": "lapce", "qtcreator": "qtcreator", "kate": "kate", "gnome-text-editor": "gnome-text-editor",
          "gedit": "gedit", "geany": "geany", "eclipse": "Eclipse"}


def main():
    editor, stem, files, sample, out = sys.argv[1:6]
    home = tempfile.mkdtemp(prefix="home-")
    # a copy that the editor can write to, under a name that it opens as a file rather than as a project
    copy = os.path.join(home, RENAME.get((editor, os.path.basename(sample)), os.path.basename(sample)))
    shutil.copy(sample, copy)
    sample = copy
    env = dict(os.environ, HOME=home, XDG_CONFIG_HOME=f"{home}/.config", XDG_DATA_HOME=f"{home}/.local/share",
               XDG_CACHE_HOME=f"{home}/.cache", XDG_RUNTIME_DIR=tempfile.mkdtemp(prefix="run-"), DISPLAY=DISPLAY,
               LIBGL_ALWAYS_SOFTWARE="1", NO_AT_BRIDGE="1", LANG="C.UTF-8")
    os.chmod(env["XDG_RUNTIME_DIR"], 0o700)
    with open(f"{out}.log", "w") as log:
        server = subprocess.Popen(["Xvfb", DISPLAY, "-screen", "0", "1280x800x24", "-nolisten", "tcp", "-noreset"],
                                  stdout=log, stderr=log)
        try:
            for _ in range(50):
                if os.path.exists("/tmp/.X11-unix/X99"):
                    break
                time.sleep(0.1)
            command, extra = EDITORS[editor](home, stem, files, sample)
            app = subprocess.Popen(command, env={**env, **extra}, stdout=log, stderr=log, start_new_session=True,
                                   cwd=home)
            if editor in TITLED:
                # until the window's title names the sample, which the editor shows once it has opened the file
                end = time.time() + TITLED[editor]
                while time.time() < end and app.poll() is None and subprocess.run(
                        ["xdotool", "search", "--name", re.escape(os.path.basename(sample))], env=env,
                        capture_output=True).returncode:
                    time.sleep(1)
            time.sleep(WAIT.get(editor, 8))
            if app.poll() is not None:
                raise SystemExit(f"shoot: {editor} exited with {app.returncode}; see {out}.log")
            if editor in RESIZE:
                # an editor that opens at a size of its own, made the size of the others
                subprocess.run(["xdotool", "search", "--sync", "--onlyvisible", "--class", RESIZE[editor],
                                "windowsize", str(WIDTH), str(HEIGHT)], env=env, check=True, capture_output=True)
                time.sleep(2)
            subprocess.run(["import", "-window", "root", out], env=env, check=True)
            subprocess.run(["magick", out, "-bordercolor", "#000000", "-border", "1", "-fuzz", "0", "-trim",
                            "+repage", out], check=True)
            os.killpg(app.pid, signal.SIGTERM)
        finally:
            server.terminate()


if __name__ == "__main__":
    main()
