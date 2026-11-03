"""Colours the preview samples as a terminal editor draws them, for preview.py --helix, --kakoune, --micro, --vim and
--emacs.

Usage: python screen.py EDITOR CACHE_DIR THEMES_DIR < request.json

EDITOR is helix, kakoune, micro, vim or emacs. The request is {"themes": [theme name], "samples": [{"name", "code"}]},
with each theme's file in THEMES_DIR as the editor names it. The output is, per theme, per sample, the lines of
[text, colour, font style] tokens that preview.py draws, with font styles as Shiki numbers them.

The editor runs as a user has it: Helix from the release pinned in helix.json with the grammars and queries it ships,
downloaded into CACHE_DIR on first use, and Kakoune, Micro, Vim and Emacs as installed, with the syntax files they
ship. Emacs ships no Tree-sitter grammars, so the grammars its Tree-sitter modes need for the samples that have no
other mode, pinned in emacs.json, are built into CACHE_DIR with cc on first use. Each sample opens in an editor of its
own, with a configuration of its own in a temporary home, in a pseudo-terminal that reports 24-bit colour, with no
gutter, cursor line, bracket matching or language servers, and the colours are read from the screen that the editor
draws, through the pyte terminal emulator, so they are the colours a terminal shows. The cursor sits past the end of
the last line, where it covers no code.

The run fails when the editor logs a problem, or draws code on a background other than the theme's or in a colour that
the theme does not set, as the editor's own colours show where a theme leaves a group out.
"""
import fcntl, hashlib, io, json, os, platform, pty, re, select, shutil, signal, struct, subprocess, sys, tarfile
import tempfile, termios, time, urllib.request

import pyte

HERE = os.path.dirname(os.path.abspath(__file__))
ITALIC, BOLD, UNDERLINE = 1, 2, 4
COLUMNS, ROWS = 160, 40
# The editor has drawn the sample once its output has been quiet this long, in seconds, the screen shows the sample on
# the theme's background and the editor has written its log; the run gives up after TIMEOUT.
QUIET, TIMEOUT = 0.5, 30
HEX = re.compile(r"(?:#|rgb:)([0-9A-Fa-f]{6})\b")
# A control sequence with intermediate bytes, such as the CSI 0 % m with which Vim probes the terminal. pyte drops the
# intermediates and so takes it for another sequence, CSI 0 m among them; none of them sets a colour. A sequence that a
# read cuts off waits for the next one.
INTERMEDIATE = re.compile(rb"\x1b\[[0-?]*[ -/]+[@-~]")
UNFINISHED = re.compile(rb"\x1b(\[[0-?]*[ -/]*)?$")


def manifest(name):
    with open(os.path.join(HERE, name), encoding="utf-8") as f:
        return json.load(f)


def download(url, sha256):
    """The bytes at url, which must match sha256."""
    with urllib.request.urlopen(url) as response:
        data = response.read()
    if hashlib.sha256(data).hexdigest() != sha256:
        raise SystemExit(f"screen: {url} does not match its sha256")
    return data


def installed(command, name):
    """The path of an editor's command on PATH."""
    path = shutil.which(command)
    if not path:
        raise SystemExit(f"screen: {name} is not installed; {command} is not on PATH")
    return path


def read(path):
    if not os.path.isfile(path):
        return ""
    with open(path, encoding="utf-8", errors="replace") as f:
        return f.read()


class Helix:
    """Helix 25.07, from the release pinned in helix.json."""
    def __init__(self, cache):
        spec = manifest("helix.json")
        machine = {"amd64": "x86_64", "arm64": "aarch64"}.get(platform.machine().lower(), platform.machine().lower())
        system = {"Linux": "linux", "Darwin": "macos"}.get(platform.system(), platform.system().lower())
        key = f"{machine}-{system}"
        if key not in spec["releases"]:
            raise SystemExit(f"screen: helix.json has no Helix {spec['helix']} for {key}")
        self.folder = os.path.join(cache, "helix", f"helix-{spec['helix']}-{key}")
        if not os.path.isfile(os.path.join(self.folder, "hx")):
            data = download(spec["releases"][key]["url"], spec["releases"][key]["sha256"])
            os.makedirs(os.path.dirname(self.folder), exist_ok=True)
            with tempfile.TemporaryDirectory(dir=os.path.dirname(self.folder)) as tmp:
                with tarfile.open(fileobj=io.BytesIO(data)) as archive:
                    archive.extractall(tmp, filter="data")
                root, = os.listdir(tmp)
                shutil.rmtree(self.folder, ignore_errors=True)
                shutil.move(os.path.join(tmp, root), self.folder)

    def theme_file(self, theme):
        return f"{theme}.toml"

    def background(self, text):
        return re.search(r'^"ui.background" = \{[^}]*bg = "#(\w+)"', text, re.M)[1]

    def setup(self, home, theme_path, theme):
        config = os.path.join(home, "config", "helix")
        os.makedirs(os.path.join(config, "themes"))
        shutil.copy(theme_path, os.path.join(config, "themes"))
        with open(os.path.join(config, "config.toml"), "w", encoding="utf-8") as f:
            f.write(f'theme = "{theme}"\n\n[editor]\ngutters = []\ntrue-color = true\n\n[editor.lsp]\nenable = false\n')

    def command(self, home, path, lines):
        env = dict(HELIX_RUNTIME=os.path.join(self.folder, "runtime"))
        return [os.path.join(self.folder, "hx"), f"{path}:{len(lines)}:{len(lines[-1]) + 1}"], env

    def ready(self, home):
        return True  # Helix writes its log only when it has something to log

    def problems(self, home, screen):
        log = read(os.path.join(home, "cache", "helix", "helix.log"))
        return [line for line in log.splitlines() if " WARN " in line or " ERROR " in line]


class Kakoune:
    """Kakoune as installed, with the language scripts it ships; KAKOUNE_CONFIG_DIR holds the user's part."""
    def __init__(self, cache):
        self.kak = installed("kak", "Kakoune")

    def theme_file(self, theme):
        return f"{theme}.kak"

    def background(self, text):
        return re.search(r"^set-face global Default rgb:\w+,rgb:(\w+)", text, re.M)[1]

    def setup(self, home, theme_path, theme):
        config = os.path.join(home, "config", "kak")
        os.makedirs(os.path.join(config, "colors"))
        shutil.copy(theme_path, os.path.join(config, "colors"))
        log = os.path.join(home, "debug.txt")
        with open(os.path.join(config, "kakrc"), "w", encoding="utf-8") as f:
            # The changelog that Kakoune shows in an information box on its first start would cover the code. The
            # *debug* buffer holds the errors of scripts, written out once the window shows.
            f.write(f"colorscheme {theme}\n"
                    "set-option global startup_info_version 99999999\n"
                    "set-option global ui_options terminal_assistant=none\n"
                    f"hook global WinDisplay .* %{{ evaluate-commands -buffer *debug* %{{ write -force {log} }} }}\n")

    def command(self, home, path, lines):
        env = dict(KAKOUNE_CONFIG_DIR=os.path.join(home, "config", "kak"))
        return [self.kak, f"+{len(lines)}:{len(lines[-1]) + 1}", path], env

    def ready(self, home):
        return os.path.isfile(os.path.join(home, "debug.txt"))

    def problems(self, home, screen):
        log = read(os.path.join(home, "debug.txt"))
        return [line for line in log.splitlines() if re.search(r"error|no such|unknown", line, re.I)]


class Micro:
    """Micro as installed, with the syntax files built into it."""
    def __init__(self, cache):
        self.micro = installed("micro", "Micro")

    def theme_file(self, theme):
        return f"{theme}.micro"

    def background(self, text):
        return re.search(r'^color-link default "#\w+,#(\w+)"', text, re.M)[1]

    def setup(self, home, theme_path, theme):
        config = os.path.join(home, "config", "micro")
        os.makedirs(os.path.join(config, "colorschemes"))
        shutil.copy(theme_path, os.path.join(config, "colorschemes"))
        settings = dict(colorscheme=theme, ruler=False, cursorline=False, matchbrace=False, diffgutter=False,
                        statusline=True, savecursor=False, saveundo=False)
        with open(os.path.join(config, "settings.json"), "w", encoding="utf-8") as f:
            json.dump(settings, f)

    def command(self, home, path, lines):
        env = dict(MICRO_CONFIG_HOME=os.path.join(home, "config", "micro"))
        return [self.micro, f"+{len(lines)}:{len(lines[-1]) + 1}", path], env

    def ready(self, home):
        return True  # Micro shows its problems on the screen

    def problems(self, home, screen):
        # Micro shows a problem with a colour scheme in the message line, the last row of the screen.
        message = "".join(screen[ROWS - 1][x].data for x in range(COLUMNS)).strip()
        return [message] if message else []


class Vim:
    """Vim as installed, with the syntax files it ships, in 'termguicolors'."""
    def __init__(self, cache):
        self.vim = installed("vim", "Vim")

    def theme_file(self, theme):
        return f"{theme}.vim"

    def background(self, text):
        return re.search(r"^hi Normal .*guibg=#(\w+)", text, re.M)[1]

    def setup(self, home, theme_path, theme):
        colors = os.path.join(home, ".vim", "colors")
        os.makedirs(colors)
        shutil.copy(theme_path, colors)
        log = os.path.join(home, "messages.txt")
        with open(os.path.join(home, ".vim", "vimrc"), "w", encoding="utf-8") as f:
            # matchparen would highlight a bracket under the cursor. The messages, which hold the errors of scripts,
            # are written out once Vim has started.
            f.write("set nocompatible termguicolors laststatus=0 noruler noshowmode shortmess+=I\n"
                    "let g:loaded_matchparen = 1\n"
                    "filetype plugin on\nsyntax on\n"
                    f"colorscheme {theme}\n"
                    f"autocmd VimEnter * call writefile(split(execute('messages'), \"\\n\"), '{log}')\n")

    def command(self, home, path, lines):
        return [self.vim, "-i", "NONE", f"+call cursor({len(lines)}, {len(lines[-1]) + 1})", path], {}

    def ready(self, home):
        return os.path.isfile(os.path.join(home, "messages.txt"))

    def problems(self, home, screen):
        log = read(os.path.join(home, "messages.txt"))
        return [line for line in log.splitlines() if re.match(r"E\d+:|Error", line)]


class Emacs:
    """Emacs as installed, in a terminal, with the major modes it ships. Samples in a language that Emacs has a
    Tree-sitter mode for and no other mode open in the Tree-sitter mode, with the grammar pinned in emacs.json."""
    def __init__(self, cache):
        self.emacs = installed("emacs", "Emacs")
        spec = manifest("emacs.json")
        self.grammars = os.path.join(cache, "emacs", "grammars")
        self.modes = spec["modes"]
        for language, grammar in spec["grammars"].items():
            suffix = ".dylib" if platform.system() == "Darwin" else ".so"  # as Emacs looks for it
            library = os.path.join(self.grammars, f"libtree-sitter-{language}{suffix}")
            if not os.path.isfile(library):
                self.build(language, grammar, library)

    def build(self, language, grammar, library):
        """Compiles a grammar's parser into the library that Emacs loads for the language."""
        cc = installed("cc", "A C compiler")
        data = download(grammar["url"], grammar["sha256"])
        os.makedirs(self.grammars, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=self.grammars) as tmp:
            with tarfile.open(fileobj=io.BytesIO(data)) as archive:
                archive.extractall(tmp, filter="data")
            root, = os.listdir(tmp)
            src = os.path.join(tmp, root, grammar["src"])
            sources = [os.path.join(src, name) for name in ("parser.c", "scanner.c")
                       if os.path.isfile(os.path.join(src, name))]
            subprocess.run([cc, "-shared", "-fPIC", "-O2", "-I", src, *sources, "-o", library + ".tmp"], check=True)
            os.replace(library + ".tmp", library)

    def theme_file(self, theme):
        return f"{theme}-theme.el"

    def background(self, text):
        return re.search(r"^ '\(default \(\(t \(.*:background \"#(\w+)\"", text, re.M)[1]

    def setup(self, home, theme_path, theme):
        themes = os.path.join(home, "themes")
        os.makedirs(themes)
        shutil.copy(theme_path, themes)
        log = os.path.join(home, "messages.txt")
        modes = "\n".join(f'(add-to-list \'auto-mode-alist \'("\\\\.{suffix}\\\\\'" . {mode}))'
                          for suffix, mode in self.modes.items())
        with open(os.path.join(home, "init.el"), "w", encoding="utf-8") as f:
            # The menu bar would take the first row, and show-paren-mode would highlight a bracket by the cursor;
            # css-mode draws a colour such as #B03A2E on that colour, which is the sample's, not the theme's.
            # *Messages* holds the errors of redisplay and font-lock, written out once Emacs is idle.
            f.write(f"""(setq inhibit-startup-screen t)
(menu-bar-mode -1)
(show-paren-mode -1)
(setq css-fontify-colors nil)
(setq treesit-extra-load-path '("{self.grammars}"))
{modes}
(add-to-list 'custom-theme-load-path "{themes}")
(load-theme '{theme} t)
(run-with-idle-timer 0.3 nil
  (lambda () (with-current-buffer "*Messages*" (write-region nil nil "{log}"))))
""")

    def command(self, home, path, lines):
        return [self.emacs, "-nw", "-Q", "-l", os.path.join(home, "init.el"),
                f"+{len(lines)}:{len(lines[-1]) + 1}", path], {}

    def ready(self, home):
        return os.path.isfile(os.path.join(home, "messages.txt"))

    def problems(self, home, screen):
        log = read(os.path.join(home, "messages.txt"))
        return [line for line in log.splitlines() if re.search(r"error|warning|invalid|not found", line, re.I)]


class Screen(pyte.Screen):
    """A pyte screen that erases as a terminal does, and ignores the private graphic renditions which set keyboard
    modes, such as the CSI > 4;2 m with which Vim asks for xterm's modifyOtherKeys, rather than failing on them."""
    def select_graphic_rendition(self, *attrs, private=False):
        if not private:
            super().select_graphic_rendition(*attrs)

    def erase_in_display(self, how=0, *args, **kwargs):
        """pyte erases only the cells that have been written, so a screen cleared before anything is drawn on it keeps
        the default background. Vim and Emacs clear the screen in the editor's background and draw only text on it."""
        super().erase_in_display(how, *args, **kwargs)
        rows = {0: range(self.cursor.y + 1, self.lines), 1: range(self.cursor.y), 2: range(self.lines),
                3: range(self.lines)}.get(how, range(0))
        for y in rows:
            for x in range(self.columns):
                self.buffer[y][x] = self.cursor.attrs


EDITORS = {"helix": Helix, "kakoune": Kakoune, "micro": Micro, "vim": Vim, "emacs": Emacs}


def shows(buffer, lines, background):
    """Whether the screen shows lines from its first row, with every character on the background."""
    for y, line in enumerate(lines):
        cells = [cell for cell in (buffer[y][x] for x in range(COLUMNS)) if cell.data][:len(line)]
        if "".join(cell.data for cell in cells) != line or any(cell.bg != background for cell in cells):
            return False
    return True


def draw(argv, extra, home, name, ready):
    """The screen that the editor draws, started with argv and extra environment in home, as a pyte screen's buffer,
    once the editor has been quiet for QUIET and ready(buffer) holds."""
    screen = Screen(COLUMNS, ROWS)
    stream = pyte.ByteStream(screen)
    env = dict(os.environ, HOME=home, XDG_CONFIG_HOME=os.path.join(home, "config"),
               XDG_CACHE_HOME=os.path.join(home, "cache"), XDG_DATA_HOME=os.path.join(home, "data"),
               XDG_STATE_HOME=os.path.join(home, "state"), XDG_RUNTIME_DIR=os.path.join(home, "run"),
               TERM="xterm-256color", COLORTERM="truecolor", **extra)
    os.makedirs(env["XDG_RUNTIME_DIR"], mode=0o700, exist_ok=True)
    pid, fd = pty.fork()
    if pid == 0:
        os.chdir(home)
        os.execve(argv[0], argv, env)
    try:
        fcntl.ioctl(fd, termios.TIOCSWINSZ, struct.pack("HHHH", ROWS, COLUMNS, 0, 0))
        # pyte answers the terminal queries an editor sends at start, such as the device attributes.
        screen.write_process_input = lambda data: os.write(fd, data.encode())
        start = last = time.monotonic()
        pending = b""
        while time.monotonic() - last < QUIET or not ready(screen.buffer):
            if time.monotonic() - start > TIMEOUT:
                if not ready(screen.buffer):
                    break  # tokens and problems report what the screen shows
                raise SystemExit(f"screen: the editor did not finish drawing {name}")
            if select.select([fd], [], [], 0.05)[0]:
                try:
                    data = os.read(fd, 1 << 16)
                except OSError:
                    raise SystemExit(f"screen: the editor exited while drawing {name}")
                data = pending + data
                cut = UNFINISHED.search(data)
                data, pending = (data[:cut.start()], data[cut.start():]) if cut else (data, b"")
                stream.feed(INTERMEDIATE.sub(b"", data))
                last = time.monotonic()
    finally:
        os.kill(pid, signal.SIGKILL)
        os.waitpid(pid, 0)
        os.close(fd)
    return screen.buffer


def tokens(buffer, lines, background, colours, name):
    """The rows that hold lines as [text, colour, font style] tokens. Whitespace joins the token before it, as it shows
    no colour."""
    out = []
    for y, line in enumerate(lines):
        cells = [buffer[y][x] for x in range(COLUMNS)]
        cells = [cell for cell in cells if cell.data][:len(line)]  # a wide character leaves an empty cell after it
        row = []
        for cell in cells:
            if cell.bg != background:
                raise SystemExit(f"screen: {name} line {y + 1} is drawn on {cell.bg}, not the theme's #{background}")
            if not cell.data.isspace() and cell.fg not in colours:
                raise SystemExit(f"screen: {name} line {y + 1} draws {cell.data!r} in {cell.fg}, which the theme "
                                 f"does not set")
            colour = "#" + cell.fg.upper()
            font = (ITALIC if cell.italics else 0) | (BOLD if cell.bold else 0) | (UNDERLINE if cell.underscore else 0)
            if row and (cell.data.isspace() or row[-1][1:] == [colour, font]):
                row[-1][0] += cell.data
            else:
                row.append([cell.data, colour, font])
        if "".join(t[0] for t in row) != line:
            raise SystemExit(f"screen: the screen shows {''.join(t[0] for t in row)!r} for {line!r} in {name}")
        out.append(row)
    return out


def main():
    editor_name, cache, themes = sys.argv[1:]
    request = json.load(sys.stdin)
    editor = EDITORS[editor_name](cache)
    with tempfile.TemporaryDirectory() as tmp:
        samples = []
        for sample in request["samples"]:
            path = os.path.join(tmp, "samples", sample["name"])
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8", newline="\n") as f:
                f.write(sample["code"] + "\n")
            lines = sample["code"].split("\n")
            if len(lines) > ROWS - 3 or max(map(len, lines)) >= COLUMNS:
                raise SystemExit(f"screen: {sample['name']} does not fit in {COLUMNS}x{ROWS - 3}; raise them in "
                                 f"{__file__}")
            samples.append((path, lines))
        out = []
        for theme in request["themes"]:
            theme_path = os.path.join(themes, editor.theme_file(theme))
            text = read(theme_path)
            colours = {c.lower() for c in HEX.findall(text)}
            background = editor.background(text).lower()
            files = []
            for i, (path, lines) in enumerate(samples):
                home = os.path.join(tmp, "home", theme, str(i))
                os.makedirs(home)
                editor.setup(home, theme_path, theme)
                argv, extra = editor.command(home, path, lines)
                name = f"{theme} {os.path.basename(path)}"
                buffer = draw(argv, extra, home, name,
                              lambda b: shows(b, lines, background) and editor.ready(home))
                if not editor.ready(home):
                    raise SystemExit(f"screen: {editor_name} wrote no log for {name}")
                problems = editor.problems(home, buffer)
                if problems:
                    raise SystemExit(f"screen: {editor_name} logged for {name}:\n" + "\n".join(problems))
                files.append(tokens(buffer, lines, background, colours, name))
            out.append(files)
    json.dump(out, sys.stdout)


if __name__ == "__main__":
    main()
