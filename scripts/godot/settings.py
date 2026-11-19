#!/usr/bin/env python3
"""Lists the colour settings of a Godot editor's text editor themes, and checks them against heritage/godot.py.

Usage: scripts/godot/settings.py [GODOT]

GODOT is the Godot executable, `godot` on the PATH by default. The script starts its editor once without a window, in
a temporary project with its own configuration, data and cache folders, so that it writes its default editor settings
there and leaves the user's untouched. It reads the `text_editor/theme/highlighting/` settings whose names hold
`color`, which are the ones that Godot loads from a .tet file, and prints two lists:

- the settings that heritage/godot.py does not set, which keep Godot's default colours in every theme;
- the settings that heritage/godot.py sets and Godot does not have, which Godot ignores.

The exit status is 1 when either list is not empty.
"""
import os, re, subprocess, sys, tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

from heritage import godot  # noqa: E402

PREFIX = "text_editor/theme/highlighting/"


def settings(executable):
    """The names, without PREFIX, of the highlighting colour settings that the editor writes to its settings file."""
    with tempfile.TemporaryDirectory() as tmp:
        project = os.path.join(tmp, "project")
        os.makedirs(project)
        with open(os.path.join(project, "project.godot"), "w", encoding="utf-8") as f:
            f.write("config_version=5\n")
        env = dict(os.environ, **{f"XDG_{name}_HOME": os.path.join(tmp, name.lower())
                                  for name in ("CONFIG", "DATA", "CACHE")})
        subprocess.run([executable, "--headless", "--editor", "--quit", "--path", project], env=env, check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=300)
        folder = os.path.join(tmp, "config", "godot")
        files = [name for name in os.listdir(folder) if re.fullmatch(r"editor_settings-[\d.]+\.tres", name)]
        if len(files) != 1:
            raise SystemExit(f"{folder} holds {files}, not one editor settings file")
        with open(os.path.join(folder, files[0]), encoding="utf-8") as f:
            text = f.read()
    return {key for key in re.findall(rf"^{re.escape(PREFIX)}(\S+) = ", text, re.M) if "color" in key}


def main(argv):
    found = settings(argv[0] if argv else "godot")
    ours = set(godot.ROLES) | set(godot.MIXES) | {"text_selected_color"}
    unset, unknown = sorted(found - ours), sorted(ours - found)
    print(f"{len(found)} colour settings; not set by heritage/godot.py: {len(unset)}")
    for key in unset:
        print(f"  {key}")
    print(f"Set by heritage/godot.py and not in Godot: {len(unknown)}")
    for key in unknown:
        print(f"  {key}")
    return 1 if unset or unknown else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
