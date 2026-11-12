#!/usr/bin/env python3
"""Installs or removes the Heritage Themes syntax highlighting themes in Spyder.

Spyder keeps a theme as options in the [appearance] section of its spyder.ini and lists it in `custom_names`, so
installing a theme writes its options and adds its name to that list. Spyder rewrites spyder.ini when it closes, so
close Spyder before running this script.

    python3 install.py                      install every theme
    python3 install.py heritage-holi-night  install the named themes only
    python3 install.py --remove             remove every Heritage theme
    python3 install.py --list               list the themes in this folder

The script finds the spyder.ini of a Spyder from your package manager, pip or conda, and of the Flatpak. Name another
one with --config. It needs Python 3.8 or later and nothing else.
"""
import argparse
import ast
import configparser
import os
import shutil
import sys
import tempfile

SECTION = "appearance"
REGISTRY = "custom_names"  # Spyder's list of the themes that its users made, which it lets them edit and delete
PREFIX = "heritage-"
HERE = os.path.dirname(os.path.abspath(__file__))
# What Spyder selects when the selected theme goes away, as it does when its own Delete theme button removes one.
FALLBACK = {True: "spyder/dark", False: "spyder"}


def spyder_ini(directory):
    return os.path.join(directory, "config", "spyder.ini")


def config_paths(environ=None, home=None, platform=None):
    """The spyder.ini files that Spyder 6 may read, as (label, path) pairs, whether or not they exist."""
    environ = os.environ if environ is None else environ
    home = os.path.expanduser("~") if home is None else home
    platform = sys.platform if platform is None else platform
    if environ.get("SPYDER_CONFDIR"):  # Spyder uses this folder alone when it is set
        return [("SPYDER_CONFDIR", spyder_ini(os.path.abspath(environ["SPYDER_CONFDIR"])))]
    paths = []
    if platform.startswith("linux"):
        xdg = environ.get("XDG_CONFIG_HOME") or os.path.join(home, ".config")
        paths.append(("Spyder", spyder_ini(os.path.join(xdg, "spyder-py3"))))
        flatpak = os.path.join(home, ".var", "app", "org.spyder_ide.spyder", "config", "spyder-py3")
        paths.append(("Spyder (Flatpak)", spyder_ini(flatpak)))
    else:
        paths.append(("Spyder", spyder_ini(os.path.join(home, ".spyder-py3"))))
    return paths


def new_parser():
    """A parser that reads and writes the file as Spyder does."""
    return configparser.ConfigParser(interpolation=None)


def read_themes(folder):
    """name → [(option, value)] for each *.ini in folder, in file name order. An option is `<name>/<key>`."""
    themes = {}
    for filename in sorted(os.listdir(folder)):
        if not filename.endswith(".ini"):
            continue
        parser = new_parser()
        with open(os.path.join(folder, filename), encoding="utf-8") as f:
            parser.read_file(f)
        options = list(parser.items(SECTION))
        names = {option.split("/")[0] for option, _ in options}
        if len(names) != 1 or not next(iter(names)).startswith(PREFIX):
            raise SystemExit(f"{filename}: not a Heritage theme file")
        themes[names.pop()] = options
    return themes


def registered(parser):
    """The names in custom_names, or an empty list when the option is missing."""
    text = parser.get(SECTION, REGISTRY, fallback="[]")
    try:
        names = ast.literal_eval(text)
    except (ValueError, SyntaxError):
        names = None
    if not isinstance(names, list) or not all(isinstance(name, str) for name in names):
        raise SystemExit(f"{REGISTRY} in spyder.ini is not a list of names: {text!r}. Fix it, or remove the line and "
                         "start Spyder, then run this script again.")
    return names


def dark(colour):
    """Whether a #RRGGBB colour is dark."""
    r, g, b = (int(colour[i:i + 2], 16) for i in (1, 3, 5))
    return 0.299 * r + 0.587 * g + 0.114 * b < 128


def write(parser, path):
    """Saves a backup of the file as path + .bak, then writes parser's content to it in one step."""
    shutil.copy2(path, path + ".bak")
    handle, temporary = tempfile.mkstemp(dir=os.path.dirname(path), prefix="spyder.ini.", suffix=".new")
    try:
        with os.fdopen(handle, "w", encoding="utf-8") as f:
            parser.write(f)
        os.replace(temporary, path)
    except BaseException:
        os.unlink(temporary)
        raise


def load(path):
    parser = new_parser()
    with open(path, encoding="utf-8") as f:
        parser.read_file(f)
    if not parser.has_section(SECTION):
        parser.add_section(SECTION)
    return parser


def drop(parser, name):
    for option in [o for o in parser.options(SECTION) if o.startswith(name + "/")]:
        parser.remove_option(SECTION, option)


def install(path, themes):
    """Writes each theme's options to the spyder.ini at path and lists the theme in custom_names."""
    parser = load(path)
    names = registered(parser)
    for name, options in themes.items():
        drop(parser, name)
        for option, value in options:
            parser.set(SECTION, option, value)
        if name not in names:
            names.append(name)
    parser.set(SECTION, REGISTRY, repr(names))
    write(parser, path)


def remove(path, wanted):
    """Removes the named themes, or every Heritage theme, from the spyder.ini at path. Returns the names removed."""
    parser = load(path)
    names = registered(parser)
    gone = [n for n in names if n.startswith(PREFIX) and (wanted is None or n in wanted)]
    for name in gone:
        if parser.get(SECTION, "selected", fallback=None) == name:
            background = parser.get(SECTION, name + "/background", fallback="#000000")
            parser.set(SECTION, "selected", FALLBACK[dark(background)])
        drop(parser, name)
    parser.set(SECTION, REGISTRY, repr([n for n in names if n not in gone]))
    if gone:
        write(parser, path)
    return gone


def count(n):
    return f"{n} theme" + ("" if n == 1 else "s")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Install or remove the Heritage Themes syntax highlighting themes in "
                                             "Spyder. Close Spyder first.")
    ap.add_argument("themes", nargs="*", metavar="THEME", help="theme names, such as heritage-holi-night; "
                                                               "every theme when none is given")
    ap.add_argument("--remove", action="store_true", help="remove the themes instead of installing them")
    ap.add_argument("--list", action="store_true", help="list the themes and stop")
    ap.add_argument("--config", action="append", metavar="PATH", help="the spyder.ini to change; repeat for more than "
                                                                      "one. Default: the ones that exist")
    args = ap.parse_args(argv)
    available = read_themes(os.path.join(HERE, "themes"))
    unknown = [n for n in args.themes if n not in available]
    if unknown and not args.remove:
        raise SystemExit(f"Unknown theme {', '.join(unknown)}. Run with --list for the names.")
    if args.list:
        for name, options in available.items():
            print(f"{name}  {dict(options)[name + '/name']}")
        return 0
    if args.config:
        targets = [("--config", os.path.abspath(path)) for path in args.config]
        missing = [path for _, path in targets if not os.path.isfile(path)]
        if missing:
            raise SystemExit(f"Cannot find {', '.join(missing)}.")
    else:
        targets = [(label, path) for label, path in config_paths() if os.path.isfile(path)]
        if not targets:
            searched = "\n".join(f"  {path}" for _, path in config_paths())
            raise SystemExit("Cannot find a spyder.ini. Start Spyder once so that it creates its settings, close it "
                             f"and run this script again, or name the file with --config. Looked in:\n{searched}")
    for label, path in targets:
        if args.remove:
            gone = remove(path, set(args.themes) if args.themes else None)
            print(f"{label}: removed {count(len(gone))} from {path}")
        else:
            chosen = {n: available[n] for n in args.themes} if args.themes else available
            install(path, chosen)
            print(f"{label}: installed {count(len(chosen))} into {path}")
    if not args.remove:
        print("Start Spyder and choose a theme under Preferences | Appearance | Syntax highlighting theme.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
