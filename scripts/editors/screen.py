"""Reads the screen of a terminal editor showing a sample with a Heritage theme, inside the heritage-editors container.

Usage: python3 screen.py EDITOR THEME FILES SAMPLE OUT.json

EDITOR is nano or amp, THEME the theme's file name stem, FILES the folder of the editor's generated files and SAMPLE the
file to open. The editor starts in a pseudo-terminal of 256 colours that reports 24-bit colour, in a fresh HOME with the
theme installed as its README says, and the screen is read through the pyte terminal emulator once the editor has been
quiet for QUIET seconds. The output is the screen as rows of cells [character, foreground, background, bold, italic,
underline]; a colour is #RRGGBB, "default" for the terminal's own, or the name pyte gives one of the 16 ANSI colours.
"""
import fcntl, json, os, pty, re, select, shutil, signal, struct, sys, tempfile, termios, time

import pyte

COLUMNS, ROWS = 88, 20
QUIET, TIMEOUT = 1.5, 30
CONTROL_STRING = re.compile(rb"\x1b(?:\](?![012];)|[P_^X])[^\x07\x1b]*(?:\x07|\x1b\\)")


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


def nano(home, stem, files, sample):
    # the scheme's lines after the syntax files in the nanorc, as the README says, with line numbers, the guide stripe
    # and the scroll indicator shown so their colours are on screen
    with open(f"{files}/{stem}.nanorc", encoding="utf-8") as f:
        scheme = f.read()
    write(f"{home}/.config/nano/nanorc", 'include "/usr/share/nano/*.nanorc"\n' + scheme
          + "set linenumbers\nset guidestripe 90\nset indicator\n")
    return ["/usr/bin/nano", "--", sample]


def amp(home, stem, files, sample):
    # the theme in Amp's themes folder and named in its config.yml, as the README says
    os.makedirs(f"{home}/.config/amp/themes")
    shutil.copy(f"{files}/{stem}.tmTheme", f"{home}/.config/amp/themes/")
    write(f"{home}/.config/amp/config.yml", f"theme: {stem}\n")
    return ["/usr/local/bin/amp", sample]


EDITORS = dict(nano=nano, amp=amp)


def run(argv, env):
    screen = Screen(COLUMNS, ROWS)
    stream = pyte.ByteStream(screen)
    pid, fd = pty.fork()
    if pid == 0:
        os.chdir(env["HOME"])
        os.execve(argv[0], argv, env)
    fcntl.ioctl(fd, termios.TIOCSWINSZ, struct.pack("HHHH", ROWS, COLUMNS, 0, 0))
    screen.write_process_input = lambda data: os.write(fd, data.encode())
    start = last = time.monotonic()
    try:
        while time.monotonic() - last < QUIET and time.monotonic() - start < TIMEOUT:
            if select.select([fd], [], [], 0.05)[0]:
                try:
                    data = os.read(fd, 1 << 16)
                except OSError:
                    break
                stream.feed(CONTROL_STRING.sub(b"", data))
                last = time.monotonic()
    finally:
        os.kill(pid, signal.SIGKILL)
        os.waitpid(pid, 0)
        os.close(fd)
    def colour(value):
        return "#" + value.upper() if re.fullmatch(r"[0-9a-fA-F]{6}", value) else value
    return [[[cell.data, colour(cell.fg), colour(cell.bg), cell.bold, cell.italics, cell.underscore]
             for cell in (screen.buffer[y][x] for x in range(COLUMNS))] for y in range(ROWS)]


def main():
    editor, stem, files, sample, out = sys.argv[1:6]
    home = tempfile.mkdtemp(prefix="home-")
    env = dict(os.environ, HOME=home, XDG_CONFIG_HOME=f"{home}/.config", XDG_DATA_HOME=f"{home}/.local/share",
               XDG_CACHE_HOME=f"{home}/.cache", TERM="xterm-256color", COLORTERM="truecolor", LANG="C.UTF-8")
    # a copy in the home folder, which the editor can write to, so it opens without a read-only warning
    shutil.copy(sample, home)
    argv = EDITORS[editor](home, stem, files, os.path.join(home, os.path.basename(sample)))
    with open(out, "w", encoding="utf-8") as f:
        json.dump(run(argv, env), f)


if __name__ == "__main__":
    main()
