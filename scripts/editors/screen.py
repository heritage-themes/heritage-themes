"""Reads the screen of a terminal editor showing a sample with a Heritage theme, inside the heritage-editors container.

Usage: python3 screen.py EDITOR THEME FILES SAMPLE BACKGROUND FOREGROUND OUT.json

EDITOR is nano, amp, bat or delta, THEME the theme's file name stem, FILES the folder of the editor's generated files, SAMPLE
the file to open, and BACKGROUND and FOREGROUND the terminal's default colours as #RRGGBB, those of the matching
Terminals theme. The editor starts in a pseudo-terminal of 256 colours that reports 24-bit colour and answers queries
for its default colours, in a fresh HOME with the theme installed as its README says, and the screen is read through
the pyte terminal emulator once the editor has been quiet for QUIET seconds. The output is the screen as rows of cells
[character, foreground, background, bold, italic, underline]; a colour is #RRGGBB, "default" for the terminal's own,
or the name pyte gives one of the 16 ANSI colours.
"""
import fcntl, json, os, pty, re, select, shutil, signal, struct, subprocess, sys, tempfile, termios, time

import pyte

COLUMNS, ROWS = 88, 20
# delta prints a diff and exits: its screen is taller than the longest diff, and the rows below its output are dropped
DELTA_ROWS = 32
QUIET, TIMEOUT = 1.5, 30
# a query for the terminal's foreground (OSC 10) or background (OSC 11) colour, ended by BEL or ST
COLOUR_QUERY = re.compile(rb"\x1b\](1[01]);\?(?:\x07|\x1b\\)")
CONTROL_STRING = re.compile(rb"\x1b(?:\](?![012];)|[P_^X])[^\x07\x1b]*(?:\x07|\x1b\\)")
# the end of the output read so far when it stops inside an escape or a control string, which the next read completes
INCOMPLETE = re.compile(rb"\x1b(?:[\]P_^X][^\x07\x1b]*\x1b?)?$")


class Screen(pyte.Screen):
    """A pyte screen that ignores the private graphic renditions and device status reports with which editors set
    keyboard modes or query the terminal, rather than failing on them."""
    def select_graphic_rendition(self, *attrs, private=False):
        if not private:
            super().select_graphic_rendition(*attrs)

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


EDITORS = dict(nano=nano, amp=amp, bat=bat, delta=delta)


def colour_reply(code, colour):
    """The answer to a colour query, as xterm gives it: each channel as four hex digits."""
    return f"\x1b]{code};rgb:" + "/".join(colour[i:i + 2].lower() * 2 for i in (1, 3, 5)) + "\x1b\\"


def run(argv, env, background, foreground, rows):
    screen = Screen(COLUMNS, rows)
    stream = pyte.ByteStream(screen)
    pid, fd = pty.fork()
    if pid == 0:
        os.chdir(env["HOME"])
        os.execve(argv[0], argv, env)
    fcntl.ioctl(fd, termios.TIOCSWINSZ, struct.pack("HHHH", rows, COLUMNS, 0, 0))
    screen.write_process_input = lambda data: os.write(fd, data.encode())
    start = last = time.monotonic()
    pending = b""
    try:
        while time.monotonic() - last < QUIET and time.monotonic() - start < TIMEOUT:
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
             for cell in (screen.buffer[y][x] for x in range(COLUMNS))] for y in range(rows)]


def main():
    editor, stem, files, sample, background, foreground, out = sys.argv[1:8]
    home = tempfile.mkdtemp(prefix="home-")
    env = dict(os.environ, HOME=home, XDG_CONFIG_HOME=f"{home}/.config", XDG_DATA_HOME=f"{home}/.local/share",
               XDG_CACHE_HOME=f"{home}/.cache", TERM="xterm-256color", COLORTERM="truecolor", LANG="C.UTF-8")
    # a copy in the home folder, which the editor can write to, so it opens without a read-only warning
    shutil.copy(sample, home)
    argv = EDITORS[editor](home, stem, files, os.path.join(home, os.path.basename(sample)), background,
                           foreground)
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
