"""Screenshots Termux themes in the Android emulator and checks the pixels against the theme.

Usage: python3 shoot.py FILES OUT_DIR [STEM ...]

FILES is the folder of generated files (build/terminals/termux), OUT_DIR receives one PNG per theme. Without STEMs it
shoots every theme in FILES. The emulator must be running (scripts/termux/setup.sh starts it) with Termux installed.

For each theme the colours file is installed as the README says, ~/.termux/colors.properties, applied with the same
broadcast as termux-reload-settings, and sample.sh is run. The screenshot is then checked with
scripts/terminals/check.py, and the cursor must fill its block in the theme's cursor colour. Exits 1 when a theme fails.
"""
import os, re, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
CHECK = os.path.join(HERE, "..", "terminals", "check.py")
SAMPLE = os.path.join(HERE, "sample.sh")
PACKAGE = "com.termux"
HOME = "files/home"
STAGING = "/data/local/tmp"
MIN_CURSOR_PIXELS = 300  # a cell is about 24 by 38 pixels on the 1080 by 2400 screen the AVD has
DRAW_SECONDS = 1.5


def adb(*args, **kwargs):
    return subprocess.run(["adb", *args], check=True, **kwargs)


def run_as(script):
    adb("shell", "run-as", PACKAGE, "sh", "-c", f"'{script}'", stdout=subprocess.DEVNULL)


def push(local, name):
    adb("push", local, f"{STAGING}/{name}", stdout=subprocess.DEVNULL)


def screenshot(path):
    with open(path, "wb") as f:
        adb("exec-out", "screencap", "-p", stdout=f)


def parse(path):
    found = dict(line.split("=") for line in open(path, encoding="utf-8").read().splitlines()
                 if line and not line.startswith("#"))
    return found["background"], found["cursor"], [found[f"color{i}"] for i in range(16)]


def histogram(path):
    out = subprocess.run(["magick", path, "-format", "%c", "histogram:info:-"], capture_output=True, text=True,
                         check=True).stdout
    return {"#" + m[2]: int(m[1]) for m in (re.match(r"\s*(\d+):.*?#([0-9A-F]{6})", line) for line in out.splitlines())
            if m}


def type_command(text):
    adb("shell", "input", "text", text)
    adb("shell", "input", "keyevent", "KEYCODE_ENTER")


def main():
    files, out_dir, *stems = sys.argv[1:]
    stems = stems or sorted(f[:-len(".properties")] for f in os.listdir(files) if f.endswith(".properties"))
    os.makedirs(out_dir, exist_ok=True)
    push(SAMPLE, "sample.sh")
    run_as(f"mkdir -p {HOME}/.termux && cp {STAGING}/sample.sh {HOME}/sample.sh && "
           f"echo \"clear; sh sample.sh \\\"\\$(cat label)\\\"\" > {HOME}/go")
    adb("shell", "input", "keyevent", "KEYCODE_WAKEUP")
    adb("shell", "wm", "dismiss-keyguard")
    adb("shell", "am", "start", "-n", f"{PACKAGE}/.app.TermuxActivity", stdout=subprocess.DEVNULL)
    time.sleep(2)
    failed = 0
    for stem in stems:
        source = os.path.join(files, f"{stem}.properties")
        bg, cursor, ansi = parse(source)
        push(source, "colors.properties")
        run_as(f"cp {STAGING}/colors.properties {HOME}/.termux/colors.properties && echo {stem} > {HOME}/label")
        adb("shell", "am", "broadcast", "--user", "0", "-a", "com.termux.app.reload_style", PACKAGE,
            stdout=subprocess.DEVNULL)
        type_command("sh%sgo")
        time.sleep(DRAW_SECONDS)
        shot = os.path.join(out_dir, f"{stem}.png")
        screenshot(shot)
        problems = subprocess.run([sys.executable, CHECK, shot, bg, *ansi], capture_output=True, text=True).stdout
        if histogram(shot).get(cursor.upper(), 0) < MIN_CURSOR_PIXELS:
            problems += f"{shot}: cursor {cursor.upper()} is not drawn\n"
        print(problems.rstrip() if problems else f"ok  {stem}", flush=True)
        failed += bool(problems)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
