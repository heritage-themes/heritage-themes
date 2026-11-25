"""Reads the screen of a terminal editor showing a sample with a Heritage theme, inside the heritage-editors container.

Usage: python3 screen.py EDITOR THEME FILES SAMPLE BACKGROUND FOREGROUND OUT.json

EDITOR is nano, amp, bat, delta or lazygit, THEME the theme's file name stem, FILES the folder of the editor's generated
files, SAMPLE the file to open, or for lazygit a file whose name is the view to show (files, commits or search), and
BACKGROUND and FOREGROUND the terminal's default colours as #RRGGBB, those of the matching Terminals theme. The editor
starts in a pseudo-terminal of 256 colours that reports 24-bit colour and answers queries for its default colours, in a
fresh HOME with the theme installed as its README says, and the screen is read through the pyte terminal emulator once
the editor has been quiet for QUIET seconds after each key that the view needs. The output is the screen as rows of
cells [character, foreground, background, bold, italic, underline]; a colour is #RRGGBB, "default" for the terminal's
own, or the name pyte gives one of the 16 ANSI colours.
"""
import fcntl, json, os, pty, re, select, shutil, signal, struct, subprocess, sys, tempfile, termios, time

import pyte

COLUMNS, ROWS = 88, 20
# delta prints a diff and exits: its screen is taller than the longest diff, and the rows below its output are dropped
DELTA_ROWS = 32
# lazygit lays out five panels beside the main view and needs a larger screen for them to show their rows
LAZYGIT_COLUMNS, LAZYGIT_ROWS = 120, 30
QUIET, TIMEOUT = 1.5, 30
# a query for the terminal's foreground (OSC 10) or background (OSC 11) colour, ended by BEL or ST
COLOUR_QUERY = re.compile(rb"\x1b\](1[01]);\?(?:\x07|\x1b\\)")
CONTROL_STRING = re.compile(rb"\x1b(?:\](?![012];)|[P_^X])[^\x07\x1b]*(?:\x07|\x1b\\)")
# the end of the output read so far when it stops inside an escape or a control string, which the next read completes
INCOMPLETE = re.compile(rb"\x1b(?:[\]P_^X][^\x07\x1b]*\x1b?)?$")


def indexed(attrs):
    """Graphic rendition parameters with each of the 16 ANSI colours given by its 256-colour index (38;5;N or 48;5;N,
    as tcell sends the bright ones) given by its own code instead, so pyte names it as the terminal's colour rather than
    taking xterm's default RGB for it."""
    result = []
    while attrs:
        if attrs[0] in (38, 48) and len(attrs) >= 3 and attrs[1] == 5 and attrs[2] < 16:
            base = (30 if attrs[0] == 38 else 40) if attrs[2] < 8 else (90 if attrs[0] == 38 else 100)
            result.append(base + attrs[2] % 8)
            attrs = attrs[3:]
        elif attrs[0] in (38, 48) and len(attrs) >= 2 and attrs[1] in (2, 5):
            size = 5 if attrs[1] == 2 else 3
            result += attrs[:size]
            attrs = attrs[size:]
        else:
            result.append(attrs.pop(0))
    return result


class Screen(pyte.Screen):
    """A pyte screen that ignores the private graphic renditions and device status reports with which editors set
    keyboard modes or query the terminal, rather than failing on them, and names the 16 ANSI colours however they are
    sent."""
    def select_graphic_rendition(self, *attrs, private=False):
        if not private:
            super().select_graphic_rendition(*indexed(list(attrs)))

    def report_device_status(self, mode, private=False):
        if not private:
            super().report_device_status(mode)


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def nano(home, stem, files, sample, background, foreground):
    # the scheme's lines after the syntax files in the nanorc, as the README says, with line numbers, the guide stripe
    # and the scroll indicator shown so their colours are on screen
    with open(f"{files}/{stem}.nanorc", encoding="utf-8") as f:
        scheme = f.read()
    write(f"{home}/.config/nano/nanorc", 'include "/usr/share/nano/*.nanorc"\n' + scheme
          + "set linenumbers\nset guidestripe 90\nset indicator\n")
    return ["/usr/bin/nano", "--", sample]


def amp(home, stem, files, sample, background, foreground):
    # the theme in Amp's themes folder and named in its config.yml, as the README says
    os.makedirs(f"{home}/.config/amp/themes")
    shutil.copy(f"{files}/{stem}.tmTheme", f"{home}/.config/amp/themes/")
    write(f"{home}/.config/amp/config.yml", f"theme: {stem}\n")
    return ["/usr/local/bin/amp", sample]


def luminance(colour):
    def channel(c):
        c /= 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (channel(int(colour[i:i + 2], 16)) for i in (1, 3, 5))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def bat(home, stem, files, sample, background, foreground):
    # the theme in bat's themes folder with the cache rebuilt, and named in the configuration file as the dark or the
    # light theme, as the README says: dark when the terminal's background is darker than its text, as bat judges it.
    # The other slot names bat's ansi theme, whose named colours the check rejects, so the screen shows the theme only
    # when bat matches it to the terminal. The third line is highlighted to show lineHighlight. Every sample fits one
    # screen, so the output is what bat's pager, less -F, prints.
    themes = f"{home}/.config/bat/themes"
    os.makedirs(themes)
    shutil.copy(f"{files}/{stem}.tmTheme", themes)
    dark = luminance(background) < luminance(foreground)
    write(f"{home}/.config/bat/config", f'--theme-dark="{stem if dark else "ansi"}"\n'
                                        f'--theme-light="{"ansi" if dark else stem}"\n--highlight-line=3\n--paging=never\n')
    subprocess.run(["/usr/local/bin/bat", "cache", "--build"], env=dict(os.environ, HOME=home,
                   XDG_CONFIG_HOME=f"{home}/.config", XDG_CACHE_HOME=f"{home}/.cache"), check=True,
                   capture_output=True)
    return ["/usr/local/bin/bat", os.path.basename(sample)]


def delta(home, stem, files, sample, background, foreground):
    # the bat themes installed as for bat, and the features file included from Git's configuration with delta as Git's
    # pager and the theme's feature named, as the README says, with line numbers on so their styles are on screen.
    # git diff shows the sample against an earlier version committed in a repository in the home folder: the earlier
    # version lacks the first line after the first that is not blank, which shows as added, and changes the last other
    # line with digits, each digit one higher, or else the last other word of two letters or more, reversed, which shows
    # as a changed line whose changed words are marked.
    env = dict(os.environ, HOME=home, XDG_CONFIG_HOME=f"{home}/.config", XDG_CACHE_HOME=f"{home}/.cache")
    os.makedirs(f"{home}/.config/bat/themes")
    shutil.copy(f"{files}/{stem}.tmTheme", f"{home}/.config/bat/themes")
    subprocess.run(["/usr/local/bin/bat", "cache", "--build"], env=env, check=True, capture_output=True)
    os.makedirs(f"{home}/.config/delta")
    shutil.copy(f"{files}/heritage-themes.gitconfig", f"{home}/.config/delta")
    write(f"{home}/.gitconfig", "[include]\n    path = ~/.config/delta/heritage-themes.gitconfig\n"
                                "[core]\n    pager = /usr/local/bin/delta\n"
                                f"[delta]\n    features = {stem}\n    line-numbers = true\n    paging = never\n"
                                "[user]\n    name = Heritage\n    email = heritage@localhost\n")
    with open(sample, encoding="utf-8") as f:
        text = f.read()
    lines = text.splitlines(keepends=True)
    added = next(i for i, line in enumerate(lines) if i and line.strip())
    def change(line):
        if re.search(r"[0-9]", line):
            return re.sub(r"[0-9]", lambda m: str((int(m[0]) + 1) % 10), line)
        word = list(re.finditer(r"[A-Za-z]{2,}", line))[-1]
        return line[:word.start()] + word[0][::-1] + line[word.end():]
    candidates = [i for i, line in enumerate(lines) if i != added and re.search(r"[A-Za-z]{2,}", line)]
    changed = max([i for i in candidates if re.search(r"[0-9]", lines[i])] or candidates)
    write(sample, "".join(change(line) if i == changed else line for i, line in enumerate(lines) if i != added))
    name = os.path.basename(sample)
    for command in (["init", "-q"], ["add", name], ["commit", "-q", "-m", "Earlier version"]):
        subprocess.run(["/usr/bin/git", *command], cwd=home, env=env, check=True, capture_output=True)
    write(sample, text)
    return ["/usr/bin/git", "diff"]


def git(home, env, *args):
    subprocess.run(["/usr/bin/git", *args], cwd=home, env=env, check=True, capture_output=True)


# lazygit's view → the keys that show it: the files panel as lazygit opens; the commits panel with the newest commit
# copied for a cherry-pick and the third marked as the base of a rebase, which lazygit marks with a row of its own, the
# selection then on the second; and a search of the commits panel, which lazygit draws with the searching border
LAZYGIT_KEYS = {"files": [], "commits": ["4", "C", "j", "j", "B", "k"], "search": ["4", "/", *"tile", "\r"]}


def lazygit(home, stem, files, sample, background, foreground):
    # the theme in a themes folder of lazygit's configuration folder and listed after config.yml in LG_CONFIG_FILE, as
    # the README says; config.yml holds settings of the user's own that keep the screen the same on every run. The
    # repository has commits by two authors, three pushed to a remote and two not, a branch and a tag, and a staged, an
    # unstaged and an untracked file, so the panels show each kind of row that lazygit colours.
    env = dict(os.environ, HOME=home, XDG_CONFIG_HOME=f"{home}/.config", GIT_CONFIG_NOSYSTEM="1")
    config = f"{home}/.config/lazygit"
    os.makedirs(f"{config}/themes")
    shutil.copy(f"{files}/{stem}.yml", f"{config}/themes")
    write(f"{config}/config.yml", "disableStartupPopups: true\nupdate:\n  method: never\ngit:\n  autoFetch: false\n"
                                  "gui:\n  showRandomTip: false\n  showCommandLog: false\n  timeFormat: 02 Jan 06\n")
    write(f"{home}/.gitconfig", "[user]\n    name = Ada Weaver\n    email = ada@localhost\n"
                                "[init]\n    defaultBranch = master\n[advice]\n    detachedHead = false\n")
    os.remove(sample)
    repo = f"{home}/repo"
    os.makedirs(repo)
    git(repo, env, "init", "-q")
    git(home, env, "init", "-q", "--bare", "origin.git")
    def commit(message, path, text, author="Ada Weaver <ada@localhost>", day=1):
        write(f"{repo}/{path}", text)
        git(repo, env, "add", path)
        stamp = f"2026-11-{day:02d}T10:00:00"
        git(repo, dict(env, GIT_AUTHOR_DATE=stamp, GIT_COMMITTER_DATE=stamp), "commit", "-q", "--author", author,
            "-m", message)
    commit("Add the loom pattern", "pattern.py", "WARP = 12\nWEFT = 24\n", day=1)
    commit("Describe the tiles", "README.md", "# Tiles\n\nGlazed tiles in five colours.\n",
           "Bilal Potter <bilal@localhost>", day=2)
    commit("Count the tile colours", "tiles.py", "COLOURS = 5\n", day=3)
    git(repo, env, "tag", "v1.0")
    git(repo, env, "remote", "add", "origin", f"{home}/origin.git")
    git(repo, env, "push", "-q", "-u", "origin", "master")
    git(repo, env, "switch", "-q", "-c", "feature/glaze")
    commit("Add a glaze", "glaze.py", "GLAZE = 'cobalt'\n", "Bilal Potter <bilal@localhost>", day=4)
    git(repo, env, "switch", "-q", "master")
    commit("Widen the warp", "pattern.py", "WARP = 16\nWEFT = 24\n", day=5)
    commit("Add a sixth tile colour", "tiles.py", "COLOURS = 6\n", "Bilal Potter <bilal@localhost>", day=6)
    write(f"{repo}/pattern.py", "WARP = 16\nWEFT = 32\nTWILL = True\n")
    write(f"{repo}/README.md", "# Tiles\n\nGlazed tiles in six colours.\n")
    git(repo, env, "add", "README.md")
    write(f"{repo}/notes.txt", "Fire at 1200 degrees.\n")
    themes = ",".join(f"{config}/{name}" for name in ("config.yml", f"themes/{stem}.yml"))
    keys = LAZYGIT_KEYS[os.path.basename(sample)]
    return ["/usr/bin/env", f"LG_CONFIG_FILE={themes}", "/usr/bin/lazygit", "--path", repo], keys


EDITORS = dict(nano=nano, amp=amp, bat=bat, delta=delta, lazygit=lazygit)


def colour_reply(code, colour):
    """The answer to a colour query, as xterm gives it: each channel as four hex digits."""
    return f"\x1b]{code};rgb:" + "/".join(colour[i:i + 2].lower() * 2 for i in (1, 3, 5)) + "\x1b\\"


def run(argv, env, background, foreground, rows, columns=COLUMNS, keys=()):
    """The screen once the program has been quiet for QUIET seconds after each of keys, sent in turn."""
    keys = list(keys)
    screen = Screen(columns, rows)
    stream = pyte.ByteStream(screen)
    pid, fd = pty.fork()
    if pid == 0:
        os.chdir(env["HOME"])
        os.execve(argv[0], argv, env)
    fcntl.ioctl(fd, termios.TIOCSWINSZ, struct.pack("HHHH", rows, columns, 0, 0))
    screen.write_process_input = lambda data: os.write(fd, data.encode())
    start = last = time.monotonic()
    pending = b""
    try:
        while time.monotonic() - start < TIMEOUT:
            if time.monotonic() - last >= QUIET:
                if not keys:
                    break
                os.write(fd, keys.pop(0).encode())
                last = time.monotonic()
            if select.select([fd], [], [], 0.05)[0]:
                try:
                    pending += os.read(fd, 1 << 16)
                except OSError:
                    break
                # a query or control string can arrive over two reads: keep its start until the rest arrives
                cut = INCOMPLETE.search(pending)
                data, pending = (pending[:cut.start()], pending[cut.start():]) if cut else (pending, b"")
                # answer colour queries before feeding the rest, whose device attributes query pyte answers, so the
                # replies arrive in the order a terminal sends them
                for code in COLOUR_QUERY.findall(data):
                    os.write(fd, colour_reply(code.decode(), foreground if code == b"10" else background).encode())
                stream.feed(CONTROL_STRING.sub(b"", data))
                last = time.monotonic()
    finally:
        os.kill(pid, signal.SIGKILL)
        os.waitpid(pid, 0)
        os.close(fd)
    def colour(value):
        return "#" + value.upper() if re.fullmatch(r"[0-9a-fA-F]{6}", value) else value
    return [[[cell.data, colour(cell.fg), colour(cell.bg), cell.bold, cell.italics, cell.underscore]
             for cell in (screen.buffer[y][x] for x in range(columns))] for y in range(rows)]


def main():
    editor, stem, files, sample, background, foreground, out = sys.argv[1:8]
    home = tempfile.mkdtemp(prefix="home-")
    env = dict(os.environ, HOME=home, XDG_CONFIG_HOME=f"{home}/.config", XDG_DATA_HOME=f"{home}/.local/share",
               XDG_CACHE_HOME=f"{home}/.cache", TERM="xterm-256color", COLORTERM="truecolor", LANG="C.UTF-8")
    # a copy in the home folder, which the editor can write to, so it opens without a read-only warning
    shutil.copy(sample, home)
    argv = EDITORS[editor](home, stem, files, os.path.join(home, os.path.basename(sample)), background,
                           foreground)
    if editor == "lazygit":
        argv, keys = argv
        rows = run(argv, env, background, foreground, LAZYGIT_ROWS, LAZYGIT_COLUMNS, keys)
    else:
        rows = run(argv, env, background, foreground, DELTA_ROWS if editor == "delta" else ROWS)
    if editor == "delta":
        while rows and all(char == " " and bg == "default" for char, fg, bg, *_ in rows[-1]):
            rows.pop()
        # the output and the row the cursor ends on must fit, or the screen has scrolled the first rows away
        if len(rows) >= DELTA_ROWS - 1:
            raise SystemExit(f"delta: the diff of {os.path.basename(sample)} needs more than {DELTA_ROWS} rows")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(rows, f)


if __name__ == "__main__":
    main()
