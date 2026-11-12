#!/usr/bin/env python3
"""Installs or removes the Heritage Themes highlighting themes in IDLE.

IDLE keeps a custom theme as a section of config-highlight.cfg in its user configuration folder, `.idlerc` in your home
folder, so installing a theme adds its section to that file. IDLE reads the file when it starts and rewrites it when you
apply a change in its Configure IDLE dialog, so close IDLE before running this script.

    python3 install.py                      install every theme
    python3 install.py "Heritage Holi Night"          install the named themes only
    python3 install.py --remove             remove every Heritage theme
    python3 install.py --list               list the themes in this folder

It needs Python 3.8 or later and nothing else, and works on the .idlerc of the user that runs it. Name another folder
with --config.
"""
import argparse
import configparser
import os
import shutil
import sys
import tempfile

PREFIX = "Heritage "
HIGHLIGHT = "config-highlight.cfg"
MAIN = "config-main.cfg"
HERE = os.path.dirname(os.path.abspath(__file__))
# What IDLE shows when the selected custom theme goes away, as it does when its own Delete Custom Theme button removes
# one: IDLE Classic, its default, which is light. A dark IDLE theme exists, so a dark theme falls back to that.
FALLBACK = {True: "IDLE Dark", False: "IDLE Classic"}


def new_parser():
    """A parser that reads and writes a file as IDLE does: only = separates an option from its value."""
    return configparser.ConfigParser(delimiters=("=",), comment_prefixes=("#",), interpolation=None, strict=False)


def read_file(path):
    parser = new_parser()
    if os.path.isfile(path):
        with open(path, encoding="utf-8") as f:
            parser.read_file(f)
    return parser


def read_themes(folder):
    """name → [(option, value)] for each *.cfg in folder, in file name order."""
    themes = {}
    for filename in sorted(os.listdir(folder)):
        if not filename.endswith(".cfg"):
            continue
        parser = read_file(os.path.join(folder, filename))
        if len(parser.sections()) != 1 or not parser.sections()[0].startswith(PREFIX):
            raise SystemExit(f"{filename}: not a Heritage theme file")
        themes[parser.sections()[0]] = list(parser.items(parser.sections()[0]))
    return themes


def config_dir():
    """The folder of IDLE's user configuration: .idlerc in the home folder, as IDLE finds it."""
    return os.path.join(os.path.expanduser("~"), ".idlerc")


def dark(colour):
    """Whether a #RRGGBB colour is dark."""
    r, g, b = (int(colour[i:i + 2], 16) for i in (1, 3, 5))
    return 0.299 * r + 0.587 * g + 0.114 * b < 128


def write(parser, path):
    """Writes parser's content to path in one step, and saves the previous file as path + .bak."""
    if os.path.isfile(path):
        shutil.copy2(path, path + ".bak")
    handle, temporary = tempfile.mkstemp(dir=os.path.dirname(path), prefix=os.path.basename(path) + ".",
                                         suffix=".new")
    try:
        with os.fdopen(handle, "w", encoding="utf-8") as f:
            parser.write(f)
        os.replace(temporary, path)
    except BaseException:
        os.unlink(temporary)
        raise


def install(folder, themes):
    """Writes each theme as a section of the config-highlight.cfg in folder, replacing a section of the same name."""
    path = os.path.join(folder, HIGHLIGHT)
    parser = read_file(path)
    for name, options in themes.items():
        parser.remove_section(name)
        parser.add_section(name)
        for option, value in options:
            parser.set(name, option, value)
    os.makedirs(folder, exist_ok=True)
    write(parser, path)


def remove(folder, wanted):
    """Removes the named themes, or every Heritage theme, from the config-highlight.cfg in folder. Returns the names
    removed."""
    path = os.path.join(folder, HIGHLIGHT)
    parser = read_file(path)
    gone = [n for n in parser.sections() if n.startswith(PREFIX) and (wanted is None or n in wanted)]
    if not gone:
        return gone
    main_path = os.path.join(folder, MAIN)
    main = read_file(main_path)
    # An IDLE with a custom theme selected has `default = 0` and the theme's name under `name`.
    selected = main.get("Theme", "name", fallback=None)
    if selected in gone and not main.getboolean("Theme", "default", fallback=True):
        background = parser.get(selected, "normal-background", fallback="#ffffff")
        main.set("Theme", "default", "1")
        main.set("Theme", "name", "")
        main.set("Theme", "name2", FALLBACK[dark(background)])
        write(main, main_path)
    for name in gone:
        parser.remove_section(name)
    if parser.sections():
        write(parser, path)
    else:  # IDLE deletes a configuration file that has no sections, so an empty one is not kept either
        shutil.copy2(path, path + ".bak")
        os.remove(path)
    return gone


def count(n):
    return f"{n} theme" + ("" if n == 1 else "s")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Install or remove the Heritage Themes highlighting themes in IDLE. "
                                             "Close IDLE first.")
    ap.add_argument("themes", nargs="*", metavar="THEME", help="theme names, such as 'Heritage Holi Night'; every "
                                                               "theme when none is given")
    ap.add_argument("--remove", action="store_true", help="remove the themes instead of installing them")
    ap.add_argument("--list", action="store_true", help="list the themes and stop")
    ap.add_argument("--config", metavar="DIR", help="IDLE's user configuration folder. Default: .idlerc in your home "
                                                    "folder")
    args = ap.parse_args(argv)
    available = read_themes(os.path.join(HERE, "themes"))
    unknown = [n for n in args.themes if n not in available]
    if unknown and not args.remove:
        raise SystemExit(f"Unknown theme {', '.join(unknown)}. Run with --list for the names.")
    if args.list:
        print("\n".join(available))
        return 0
    folder = os.path.abspath(args.config) if args.config else config_dir()
    if args.remove:
        gone = remove(folder, set(args.themes) if args.themes else None)
        print(f"Removed {count(len(gone))} from {os.path.join(folder, HIGHLIGHT)}")
    else:
        chosen = {n: available[n] for n in args.themes} if args.themes else available
        install(folder, chosen)
        print(f"Installed {count(len(chosen))} into {os.path.join(folder, HIGHLIGHT)}")
        print("Start IDLE and choose a theme under Options | Configure IDLE | Highlights | a Custom Theme.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
