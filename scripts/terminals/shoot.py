"""Screenshots a Terminals theme in a terminal emulator, inside the heritage-terminals container.

Usage: python3 shoot.py APP THEME FILES OUT.png

APP is a module name of heritage/terminals, THEME the theme's file name stem (heritage-holi-night) and display name
joined by a tab, FILES the folder of the app's generated files. The emulator starts in a fresh HOME with only the theme
installed as its README says, runs sample.sh, and its window is captured once it has drawn the test card, WAIT seconds
after it starts. X11 emulators draw on Xvfb; foot draws on a headless Sway. The app's output goes to OUT.png.log.
"""
import os, re, shutil, signal, subprocess, sys, tempfile, time

HERE = os.path.dirname(os.path.abspath(__file__))
SAMPLE = os.path.join(HERE, "sample.sh")
WIDTH, HEIGHT = 1100, 520
DISPLAY = ":99"
FONT = "JetBrains Mono"


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def copy(src, dest):
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    shutil.copy(src, dest)


def kitty(home, stem, label, files):
    copy(f"{files}/{stem}.conf", f"{home}/.config/kitty/themes/{stem}.conf")
    write(f"{home}/.config/kitty/kitty.conf",
          f"include themes/{stem}.conf\nfont_family {FONT}\nfont_size 11\nremember_window_size no\n"
          f"initial_window_width {WIDTH}\ninitial_window_height {HEIGHT}\ntab_bar_min_tabs 1\n"
          "linux_display_server x11\n")
    return ["kitty", "--title", label, "sh", SAMPLE, label], {}


def alacritty(home, stem, label, files):
    copy(f"{files}/{stem}.toml", f"{home}/.config/alacritty/themes/{stem}.toml")
    write(f"{home}/.config/alacritty/alacritty.toml",
          f'[general]\nimport = ["~/.config/alacritty/themes/{stem}.toml"]\n\n'
          f'[font]\nsize = 11\nnormal = {{ family = "{FONT}" }}\n\n'
          "[window]\ndimensions = { columns = 120, lines = 26 }\n")
    return ["alacritty", "-e", "sh", SAMPLE, label], {}


def wezterm(home, stem, label, files):
    copy(f"{files}/{stem}.toml", f"{home}/.config/wezterm/colors/{stem}.toml")
    write(f"{home}/.config/wezterm/wezterm.lua",
          f'return {{ color_scheme = "{label}", front_end = "Software", font = require("wezterm").font("{FONT}"),\n'
          "  font_size = 11, initial_cols = 120, initial_rows = 24, use_fancy_tab_bar = false,\n"
          "  hide_tab_bar_if_only_one_tab = false, enable_wayland = false }\n")
    return ["wezterm", "--config-file", f"{home}/.config/wezterm/wezterm.lua", "start", "--always-new-process", "--",
            "sh", SAMPLE, label], {}


def ghostty(home, stem, label, files):
    copy(f"{files}/{stem}", f"{home}/.config/ghostty/themes/{stem}")
    write(f"{home}/.config/ghostty/config",
          f"theme = {stem}\nfont-family = {FONT}\nfont-size = 11\nwindow-width = 120\nwindow-height = 24\n"
          "gtk-single-instance = false\nwindow-decoration = none\n")
    return ["ghostty", "-e", "sh", SAMPLE, label], {}


def rio(home, stem, label, files):
    copy(f"{files}/{stem}.toml", f"{home}/.config/rio/themes/{stem}.toml")
    write(f"{home}/.config/rio/config.toml",
          f'theme = "{stem}"\n\n[fonts]\nsize = 15\nfamily = "{FONT}"\n\n'
          f'[window]\nwidth = {WIDTH}\nheight = {HEIGHT}\ncolorspace = "srgb"\n\n'
          f'[shell]\nprogram = "sh"\nargs = ["{SAMPLE}", "{label}"]\n')
    return ["rio"], {}


def contour(home, stem, label, files):
    config = f"{home}/.config/contour/contour.yml"
    generated = subprocess.run(["contour", "generate", "config", "to", "/dev/stdout"], capture_output=True,
                               text=True, env=dict(os.environ, HOME=home)).stdout
    with open(f"{files}/{stem}.yml", encoding="utf-8") as f:
        scheme = f.read().split("color_schemes:\n", 1)[1]
    generated = generated.replace("        colors: default", f"        colors: {stem}")
    generated = generated.replace("color_schemes:\n", "color_schemes:\n" + scheme, 1)
    generated = generated.replace("family: monospace", f'family: "{FONT}"')
    # Contour scales its font by the screen's DPI, so a smaller size matches the other emulators' text
    generated = re.sub(r"(\n        font:\n(?:.*\n)*?            size: )\d+", r"\g<1>9", generated, count=1)
    generated = generated.replace("        shell: /bin/bash", "        shell: sh")
    generated = generated.replace("        arguments: []", f'        arguments: ["{SAMPLE}", "{label}"]')
    write(config, generated)
    return ["contour", "config", config], {}


def konsole(home, stem, label, files):
    copy(f"{files}/{stem}.colorscheme", f"{home}/.local/share/konsole/{stem}.colorscheme")
    write(f"{home}/.local/share/konsole/Heritage.profile",
          f"[Appearance]\nColorScheme={stem}\nFont={FONT},11,-1,5,400,0,0,0,0,0,0,0,0,0,0,1\n\n"
          "[General]\nName=Heritage\nParent=FALLBACK/\nTerminalColumns=120\nTerminalRows=24\n")
    write(f"{home}/.config/konsolerc", "[Desktop Entry]\nDefaultProfile=Heritage.profile\n")
    return ["konsole", "--profile", "Heritage", "-e", "sh", SAMPLE, label], {"QT_QPA_PLATFORM": "xcb"}


def xterm(home, stem, label, files):
    subprocess.run(["xrdb", "-merge", f"{files}/{stem}.Xresources"], check=True)
    return ["xterm", "-fa", FONT, "-fs", "11", "-geometry", "120x24", "-e", "sh", SAMPLE, label], {}


def terminator(home, stem, label, files):
    # The theme's file is the [global_config] and [profiles] sections that the README has users merge into the config;
    # the profile also gets the font, as a user's own profile would have one.
    with open(f"{files}/{stem}.config", encoding="utf-8") as f:
        profile = f.read()
    write(f"{home}/.config/terminator/config",
          profile.replace("[global_config]\n", "[global_config]\n  suppress_multiple_term_dialog = True\n", 1)
          + f"    font = {FONT} 11\n    use_system_font = False\n"
          "[layouts]\n  [[default]]\n    [[[window0]]]\n      type = Window\n      parent = \"\"\n"
          f"      size = {WIDTH}, {HEIGHT}\n    [[[child1]]]\n      type = Terminal\n      parent = window0\n"
          f"      profile = {label}\n")
    return ["terminator", "--no-dbus", "-u", "-p", label, "-x", "sh", SAMPLE, label], {}


def st(home, stem, label, files):
    # st compiles its colours in: the theme's block replaces the colour block of config.def.h, as the README says.
    source = f"{home}/st"
    shutil.copytree("/opt/st-src", source)
    with open(f"{source}/config.def.h", encoding="utf-8") as f:
        config = f.read()
    with open(f"{files}/{stem}.h", encoding="utf-8") as f:
        block = f.read()
    start = config.index("static const char *colorname[]")
    end = config.index("static unsigned int defaultrcs = 257;") + len("static unsigned int defaultrcs = 257;")
    config = config[:start] + block + config[end:]
    config = re.sub(r'static char \*font = "[^"]*";', f'static char *font = "{FONT}:pixelsize=15:antialias=true";',
                    config)
    write(f"{source}/config.h", config)
    subprocess.run(["make", "-C", source, "st"], check=True, capture_output=True)
    return [f"{source}/st", "-g", "120x24", "-e", "sh", SAMPLE, label], {}


def foot(home, stem, label, files):
    copy(f"{files}/{stem}.ini", f"{home}/.config/foot/themes/{stem}.ini")
    with open(f"{files}/{stem}.ini", encoding="utf-8") as f:
        light = "[colors-light]" in f.read()
    write(f"{home}/.config/foot/foot.ini",
          f"[main]\ninclude=~/.config/foot/themes/{stem}.ini\n" + ("initial-color-theme=light\n" if light else "")
          + f"font={FONT}:size=11\ninitial-window-size-chars=120x24\n")
    return ["foot", "sh", SAMPLE, label], {}


def hyper(home, stem, label, files):
    # Hyper reads $XDG_CONFIG_HOME/hyper when XDG_CONFIG_HOME is set, as it is here, and the home folder otherwise
    shutil.copytree(f"{files}/heritage-themes", f"{home}/.config/hyper/.hyper_plugins/local/heritage-themes")
    write(f"{home}/.config/hyper/.hyper.js",
          "module.exports = {\n  config: {\n"
          f'    heritageTheme: "{stem}",\n    fontFamily: "{FONT}", fontSize: 14,\n'
          f'    shell: "/bin/sh", shellArgs: ["{SAMPLE}", "{label}"],\n'
          f"    updateChannel: \"stable\", disableAutoUpdates: true, webGLRenderer: false, windowSize: [{WIDTH}, {HEIGHT}],\n"
          "  },\n  plugins: [],\n  localPlugins: [\"heritage-themes\"],\n};\n")
    return ["/opt/hyper/hyper", "--no-sandbox", "--disable-gpu"], {}


def tabby(home, stem, label, files):
    import yaml
    with open(f"{files}/heritage-themes.yaml", encoding="utf-8") as f:
        schemes = yaml.safe_load(f)["terminal"]["customColorSchemes"]
    scheme, = (s for s in schemes if s["name"] == label)
    config = {"version": 6, "enableAnalytics": False, "enableWelcomeTab": False,
              "terminal": {"colorScheme": scheme, "lightColorScheme": scheme, "customColorSchemes": schemes,
                           "font": FONT, "fontSize": 14, "profile": "local:custom:heritage"},
              "profiles": [{"id": "local:custom:heritage", "type": "local", "name": "Sample",
                            "options": {"command": "/bin/sh", "args": [SAMPLE, label], "env": {}, "cwd": ""}}],
              "appearance": {"colorSchemeMode": "dark"},
              "pluginBlacklist": [], "hotkeys": {}}
    write(f"{home}/.config/tabby/config.yaml", yaml.safe_dump(config, allow_unicode=True))
    return ["/opt/tabby/tabby", "--no-sandbox", "--disable-gpu"], {}


def warp(home, stem, label, files):
    # The preferences mark onboarding as done, which a user does once with Warp's welcome screens, and a launch
    # configuration runs the test card in Warp's first tab.
    theme = f"{home}/.local/share/warp-terminal/themes/{stem}.yaml"
    copy(f"{files}/{stem}.yaml", theme)
    write(f"{home}/.config/warp-terminal/settings.toml",
          f'[appearance.themes]\ntheme = {{ custom = {{ name = "{label}", path = "{theme}" }} }}\n\n'
          f'[appearance.text]\nfont_name = "{FONT}"\n')
    write(f"{home}/.config/warp-terminal/user_preferences.json",
          '{"prefs": {"SettingsFileMigrationComplete": "true", "HasCompletedOnboarding": "true"}}\n')
    write(f"{home}/.local/share/warp-terminal/launch_configurations/sample.yaml",
          "name: Sample\nwindows:\n  - tabs:\n      - layout:\n          cwd: /tmp\n          commands:\n"
          f"            - exec: sh {SAMPLE} '{label}'\n")
    return ["warp-terminal", "warp://launch/sample.yaml"], {"SHELL": "/bin/bash"}


# Seconds after start before the screenshot: Electron apps take longer to start, and Warp to start its shell session.
WAIT = {"hyper": 15, "tabby": 15, "warp": 50}

APPS = dict(kitty=kitty, alacritty=alacritty, wezterm=wezterm, ghostty=ghostty, rio=rio, contour=contour,
            konsole=konsole, xterm=xterm, terminator=terminator, st=st, foot=foot, hyper=hyper, tabby=tabby,
            warp=warp)


def wait_for(predicate, timeout):
    end = time.time() + timeout
    while time.time() < end:
        if predicate():
            return True
        time.sleep(0.2)
    return False


def main():
    app, theme, files, out = sys.argv[1:5]
    stem, label = theme.split("\t")
    home = tempfile.mkdtemp(prefix="home-")
    env = dict(os.environ, HOME=home, XDG_CONFIG_HOME=f"{home}/.config", XDG_DATA_HOME=f"{home}/.local/share",
               XDG_CACHE_HOME=f"{home}/.cache", XDG_RUNTIME_DIR=tempfile.mkdtemp(prefix="run-"),
               LIBGL_ALWAYS_SOFTWARE="1", TERM="xterm-256color", NO_AT_BRIDGE="1")
    os.chmod(env["XDG_RUNTIME_DIR"], 0o700)
    log = open(f"{out}.log", "w")
    servers = []
    try:
        if app == "foot":
            sway = f"{home}/.config/sway/config"
            # foot floats at the size it asks for, as the X11 emulators open, rather than tiling the output
            write(sway, "output HEADLESS-1 resolution 1280x1000\ndefault_border none\n"
                        "for_window [app_id=\"foot\"] floating enable\n")
            env.update(WLR_BACKENDS="headless", WLR_RENDERER="pixman", WLR_LIBINPUT_NO_DEVICES="1")
            servers.append(subprocess.Popen(["sway", "-c", sway], env=env, stdout=log, stderr=log))
            if not wait_for(lambda: any(n.startswith("wayland-") and not n.endswith(".lock")
                                        for n in os.listdir(env["XDG_RUNTIME_DIR"])), 15):
                raise SystemExit("shoot: sway did not start")
            env["WAYLAND_DISPLAY"] = next(n for n in os.listdir(env["XDG_RUNTIME_DIR"])
                                          if n.startswith("wayland-") and not n.endswith(".lock"))
        else:
            servers.append(subprocess.Popen(["Xvfb", DISPLAY, "-screen", "0", "1280x1000x24", "-nolisten", "tcp", "-noreset"],
                                            stdout=log, stderr=log))
            env["DISPLAY"] = DISPLAY
            os.environ["DISPLAY"] = DISPLAY
            if not wait_for(lambda: subprocess.run(["xdpyinfo"], capture_output=True, env=env).returncode == 0
                            if shutil.which("xdpyinfo") else os.path.exists("/tmp/.X11-unix/X99"), 15):
                raise SystemExit("shoot: Xvfb did not start")
        os.environ.update(HOME=home)
        command, extra = APPS[app](home, stem, label, files)
        env.update(extra)
        terminal = subprocess.Popen(command, env=env, stdout=log, stderr=log, start_new_session=True)
        time.sleep(WAIT.get(app, 6))
        if terminal.poll() is not None:
            raise SystemExit(f"shoot: {app} exited with {terminal.returncode}; see {out}.log")
        if app == "foot":
            subprocess.run(["grim", out], env=env, check=True)
        else:
            subprocess.run(["import", "-window", "root", out], env=env, check=True)
        # the window alone: the screen around it is the black of an empty X root or Sway output, and no theme's
        # background is pure black
        subprocess.run(["magick", out, "-bordercolor", "#000000", "-border", "1", "-fuzz", "0", "-trim", "+repage",
                        out], check=True)
        os.killpg(terminal.pid, signal.SIGTERM)
    finally:
        for server in servers:
            server.terminate()
        log.close()


if __name__ == "__main__":
    main()
