#!/usr/bin/env python3
"""Captures the code samples as Xcode draws them in each theme of a folder, for preview.py --xcode.

Usage: screen.py <cache> <themes> <samples> <out> <width> <theme JSON>
  cache    folder for the compiled capture helper
  themes   folder with the .xcworkspacecolortheme files
  samples  folder with the sample files
  out      folder for the captures: <out>/<theme>/<sample>.png
  width    the width in points of each editor
  theme JSON  [{"name": ..., "background": "RRGGBB", "line": "RRGGBB"}, ...]: per theme, its file name without the
           extension and the colours of its editor background and current line

It prints {theme: {sample: scale}} as JSON: the pixels per point of each capture.

Xcode keeps its settings in the user's defaults domain, which no launch option moves, so screen.py runs only while
Xcode is closed. It saves the domain, removes the theme and font settings from it so that the samples show in Xcode's
default fonts, and restores the saved domain at the end, whatever happens. Each theme gets an Xcode of its own, started
with a temporary home (CFFIXED_USER_HOME) for the files Xcode writes, the themes folder in place of the user's
(DVTUserThemesDirectoryOverride) and the theme for both appearances (DVTWorkspaceThemeSettings), all as launch
arguments, which Xcode does not save. It opens each sample on its own, so that Swift has the colours of Xcode's
language service, with line wrapping, the minimap and live issues off and a caret that does not blink. It sizes each
window to the width, which puts the preview that Xcode shows beside HTML under it instead, and brings each window to the
front, so that it shows its caret, before it captures it with screencapture. Sizing and bringing to the front need
Accessibility permission for the terminal, and screencapture needs Screen Recording permission and an unlocked screen;
caffeinate keeps the display awake meanwhile, so that it does not lock. capture.swift crops the editor out of each
capture.
"""
import json, os, plistlib, subprocess, sys, tempfile, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
from heritage.xcode import recipe_id  # noqa: E402

DOMAIN = "com.apple.dt.Xcode"
# Settings that change how the editor looks and that a user can have set: the theme, fonts and cursor.
LOOK = ("DVTWorkspace", "DVTSourceEditorCursor")
SETTLE = 25  # seconds for the language services to colour the samples once their windows are open
RAISE = 1  # seconds for a window to draw itself as the key window
BORDER = 4  # points of the window's border beside the editor, which capture.swift crops off


def xcode_app():
    """The Xcode app of the active developer directory, else /Applications/Xcode.app."""
    result = subprocess.run(["xcode-select", "-p"], capture_output=True, text=True)
    developer = result.stdout.strip()
    return developer.removesuffix("/Contents/Developer") if developer.endswith(".app/Contents/Developer") \
        else "/Applications/Xcode.app"


def running():
    """The process IDs of the running Xcodes."""
    result = subprocess.run(["pgrep", "-x", "Xcode"], capture_output=True, text=True)
    return [int(pid) for pid in result.stdout.split()]


def locked():
    """Whether the screen of the console user is locked, when macOS draws no windows that screencapture can take."""
    root = plistlib.loads(subprocess.run(["ioreg", "-n", "Root", "-d1", "-a"], check=True,
                                         capture_output=True).stdout)
    return any(user.get("CGSSessionScreenIsLocked", False) for user in root.get("IOConsoleUsers", []))


def helper(cache, app):
    """The capture helper, compiled from capture.swift into cache when the source is newer."""
    source, binary = os.path.join(HERE, "capture.swift"), os.path.join(cache, "capture")
    if not os.path.isfile(binary) or os.path.getmtime(binary) < os.path.getmtime(source):
        os.makedirs(cache, exist_ok=True)
        env = dict(os.environ, DEVELOPER_DIR=os.path.join(app, "Contents", "Developer"))
        subprocess.run(["xcrun", "swiftc", "-O", source, "-o", binary], check=True, env=env)
    return binary


def defaults(*args, **kwargs):
    return subprocess.run(["defaults", *args], check=True, capture_output=True, **kwargs)


def save_domain():
    """The user's Xcode defaults as plist bytes, or None when the domain is empty."""
    result = subprocess.run(["defaults", "export", DOMAIN, "-"], capture_output=True)
    return result.stdout if result.returncode == 0 and result.stdout else None


def restore_domain(saved):
    """Puts back the saved defaults, removing every key that Xcode added since."""
    subprocess.run(["defaults", "delete", DOMAIN], capture_output=True)
    if saved is not None:
        defaults("import", DOMAIN, "-", input=saved)


def selection(name):
    """DVTWorkspaceThemeSettings for the theme of that file name, in both appearances, as Xcode stores it."""
    recipe = {"savedRecipe": {"_0": recipe_id(name)}}
    return json.dumps({"dark": recipe, "light": recipe}, separators=(",", ":")).encode()


def quit_xcode():
    """Asks every running Xcode, which is the preview's own as main() starts only while none runs, to quit, and waits
    until all have."""
    for pid in running():
        subprocess.run(["osascript", "-l", "JavaScript", "-e",
                        f'ObjC.import("AppKit"); $.NSRunningApplication.runningApplicationWithProcessIdentifier({pid})'
                        f'.terminate'], capture_output=True)
    for _ in range(60):
        if not running():
            return
        time.sleep(1)
    raise SystemExit(f"screen.py: Xcode {', '.join(map(str, running()))} did not quit")


def windows(binary, pid):
    """{title: (window ID, width in points)} for the windows of the Xcode with that process ID."""
    out = subprocess.run([binary, "windows", str(pid)], check=True, capture_output=True, text=True).stdout
    found = {}
    for line in out.splitlines():
        number, width, _, title = line.split("\t", 3)
        found[title] = (int(number), int(width))
    return found


def capture_theme(app, binary, home, themes, samples, width, theme, out):
    """Starts Xcode on the samples in the theme, saves the editor of each sample to out/<sample>.png, quits and returns
    {sample: scale}."""
    names = sorted(os.listdir(samples))
    arguments = ["-DVTUserThemesDirectoryOverride", themes,
                 "-DVTWorkspaceThemeSettings", f"<{selection(theme['name']).hex()}>",
                 "-ApplePersistenceIgnoreState", "YES", "-DVTTextEditorWrapsLines", "NO",
                 "-DVTTextShowMinimap", "NO", "-IDEEnableLiveIssues", "NO",
                 # Milliseconds per blink; SourceEditor takes only a number, which a launch argument gives as a plist.
                 "-NSTextInsertionPointBlinkPeriod", "<real>100000000</real>"]
    subprocess.run(["open", "-n", "-F", "-a", app, "--env", f"CFFIXED_USER_HOME={home}", "--args", *arguments,
                    *(os.path.join(samples, n) for n in names)], check=True)
    try:
        for _ in range(120):
            pids = running()
            if pids and set(names) <= set(windows(binary, pids[0])):
                pid = pids[0]
                break
            time.sleep(1)
        else:
            raise SystemExit(f"screen.py: Xcode did not open every sample in {theme['name']}")
        for name in names:
            subprocess.run([binary, "resize", str(pid), name, str(int(width) + BORDER)], check=True)
        time.sleep(SETTLE)
        found = windows(binary, pid)
        os.makedirs(out, exist_ok=True)
        scales = {}
        with tempfile.TemporaryDirectory() as tmp:
            for name in names:
                subprocess.run([binary, "raise", str(pid), name], check=True)
                time.sleep(RAISE)
                number, window_width = found[name]
                shot = os.path.join(tmp, f"{name}.png")
                subprocess.run(["screencapture", "-x", "-o", f"-l{number}", shot], check=True)
                result = subprocess.run([binary, "crop", shot, os.path.join(out, f"{name}.png"), str(window_width),
                                         theme["background"], theme["line"]], capture_output=True, text=True)
                if result.returncode:
                    # The window capture stays for a look at what the crop did not recognise.
                    kept = os.path.join(out, f"{name}.window.png")
                    os.replace(shot, kept)
                    raise SystemExit(f"screen.py: {name} in {theme['name']}: {result.stderr.strip()}; the window "
                                     f"capture is {kept}")
                scales[name] = int(result.stdout)
        return scales
    finally:
        quit_xcode()


def main():
    if len(sys.argv) != 7:
        raise SystemExit(__doc__)
    cache, themes, samples, out, width, request = sys.argv[1:]
    if running():
        raise SystemExit("screen.py: quit Xcode first; the preview runs an Xcode of its own and restores Xcode's "
                         "settings afterwards")
    if locked():
        raise SystemExit("screen.py: unlock the screen first; macOS does not draw windows while it is locked")
    # Keeps the display awake until this process ends, so that the screen does not lock during the captures.
    subprocess.Popen(["caffeinate", "-d", "-w", str(os.getpid())])
    app = xcode_app()
    binary = helper(cache, app)
    saved = save_domain()
    try:
        if saved is not None:
            for key in plistlib.loads(saved):
                if key.startswith(LOOK):
                    defaults("delete", DOMAIN, key)
        scales = {}
        for theme in json.loads(request):
            with tempfile.TemporaryDirectory() as home:
                scales[theme["name"]] = capture_theme(app, binary, home, themes, samples, width, theme,
                                                      os.path.join(out, theme["name"]))
        print(json.dumps(scales))
    finally:
        try:
            quit_xcode()
        finally:
            restore_domain(saved)


if __name__ == "__main__":
    main()
