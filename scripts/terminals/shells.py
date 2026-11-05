"""Reads the screen of a Terminals theme in a shell, multiplexer or prompt, inside the heritage-terminals container.

Usage: python3 shells.py APP THEME FILES OUT.json [VARIANT]

APP is a module name of heritage/terminals, THEME the theme's file name stem, FILES the folder of the app's generated
files. VARIANT picks a Powerlevel10k configuration that the wizard writes (lean, classic or rainbow). The app starts in a
pseudo-terminal that reports 24-bit colour, in a fresh HOME with the theme installed as its README says, and the
sample command line is typed in without running it, so the shell highlights it. The output is the screen as rows of
cells [character, foreground, background, bold, italic, underline], read through the pyte terminal emulator once the
app has been quiet for QUIET seconds. A colour is #RRGGBB, "default" for the terminal's own colour, or the name pyte
gives one of the 16 ANSI colours, such as "brightgreen", which shows where an app uses the terminal's palette.
"""
import fcntl, json, os, pty, re, select, shutil, signal, struct, subprocess, sys, tempfile, termios, time

import pyte

COLUMNS, ROWS = 120, 30
QUIET, TIMEOUT = 1.5, 40

# Sample command lines, each with a keyword, a command, an option, a string, a variable, a number, a redirection,
# a pipe, a comment and an unknown command, in each shell's syntax.
LINES = {
    "fish": 'for f in *.txt; echo "file $f" --verbose 42 >/dev/null | cat; end; frobnicate # done',
    "zsh": 'if [[ -n $HOME ]]; then echo "home $HOME" \'raw\' --verbose 42 > /dev/null | cat; fi; frobnicate # done',
    "nushell": 'let n = 42; ls --all | where size > 1kb | get name; ^echo "home $env.HOME"; frobnicate # done',
    "powershell": 'if ($n -gt 42) { Get-ChildItem -Path "/tmp" | ForEach-Object { $_.Name } }; frobnicate # done',
}


# Control strings that pyte does not parse and prints as text: an operating system command other than a window title
# (OSC 0, 1 and 2), and device control, application program command, privacy message and start of string sequences,
# such as the session information that Zellij sends as a DCS and its graphics query as an APC.
CONTROL_STRING = re.compile(rb"\x1b(?:\](?![012];)|[P_^X])[^\x07\x1b]*(?:\x07|\x1b\\)")


class Screen(pyte.Screen):
    """A pyte screen that ignores the private graphic renditions and device status reports with which apps set
    keyboard modes or query the terminal, such as tmux's CSI ? 996 n, rather than failing on them."""
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


def copy(src, dest):
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    shutil.copy(src, dest)


def fish(home, stem, files, variant):
    copy(f"{files}/{stem}.theme", f"{home}/.config/fish/themes/{stem}.theme")
    write(f"{home}/.config/fish/config.fish",
          f"set -g fish_greeting\nfunction fish_prompt; echo -n '$ '; end\nfish_config theme choose {stem}\n")
    return ["/usr/bin/fish"], {}, LINES["fish"]


def zsh(home, stem, files, variant):
    copy(f"{files}/{stem}.zsh", f"{home}/.config/zsh/{stem}.zsh")
    write(f"{home}/.zshrc",
          "PS1='$ '\nsource /opt/zsh-autosuggestions/zsh-autosuggestions.zsh\n"
          f"source ~/.config/zsh/{stem}.zsh\n"
          "ZSH_HIGHLIGHT_HIGHLIGHTERS=(main brackets)\n"
          "source /opt/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh\n")
    return ["/usr/bin/zsh"], {}, LINES["zsh"]


def nushell(home, stem, files, variant):
    copy(f"{files}/{stem}.nu", f"{home}/.config/nushell/themes/{stem}.nu")
    write(f"{home}/.config/nushell/config.nu",
          f"$env.config.show_banner = false\n$env.PROMPT_COMMAND = {{|| '' }}\n$env.PROMPT_INDICATOR = ''\n"
          f"$env.PROMPT_COMMAND_RIGHT = ''\nsource ~/.config/nushell/themes/{stem}.nu\n")
    write(f"{home}/.config/nushell/env.nu", "")
    return ["/usr/local/bin/nu"], {}, LINES["nushell"]


def powershell(home, stem, files, variant):
    copy(f"{files}/{stem}.ps1", f"{home}/.config/powershell/themes/{stem}.ps1")
    write(f"{home}/.config/powershell/Microsoft.PowerShell_profile.ps1",
          f"function prompt {{ '$ ' }}\n. ~/.config/powershell/themes/{stem}.ps1\n")
    return ["/usr/local/bin/pwsh", "-NoLogo"], {"POWERSHELL_TELEMETRY_OPTOUT": "1",
                                                 "POWERSHELL_UPDATECHECK": "Off"}, LINES["powershell"]


def repository(home):
    """A Git repository with a commit, a modified file and an untracked one, for the prompts' Git segments."""
    folder = f"{home}/project"
    os.makedirs(folder)
    git = ["git", "-C", folder, "-c", "user.name=Heritage", "-c", "user.email=heritage@example.org"]
    subprocess.run([*git, "init", "-q", "-b", "master"], check=True)
    write(f"{folder}/README.md", "Heritage\n")
    subprocess.run([*git, "add", "."], check=True)
    subprocess.run([*git, "commit", "-qm", "Initial commit"], check=True)
    write(f"{folder}/README.md", "Heritage Themes\n")
    write(f"{folder}/notes.txt", "notes\n")
    return folder


def bash_prompt(home, init):
    """bash in the repository, with a failed command and a slow one run first so the prompts show their status and
    duration segments."""
    folder = repository(home)
    write(f"{home}/.bashrc", f"cd {folder}\n{init}\n")
    return ["/bin/bash", "-i"], {}, ["false\r", "sleep 3\r", 4.0]


def starship(home, stem, files, variant):
    copy(f"{files}/{stem}.toml", f"{home}/.config/starship.toml")
    return bash_prompt(home, 'eval "$(starship init bash)"')


def oh_my_posh(home, stem, files, variant):
    copy(f"{files}/{stem}.omp.json", f"{home}/.config/oh-my-posh/{stem}.omp.json")
    return bash_prompt(home, f'eval "$(oh-my-posh init bash --config ~/.config/oh-my-posh/{stem}.omp.json)"')


def powerlevel10k(home, stem, files, variant):
    # the configuration that p10k configure writes for the style, then the theme, as the README says
    folder = repository(home)
    copy(f"/opt/powerlevel10k/config/p10k-{variant}.zsh", f"{home}/.p10k.zsh")
    copy(f"{files}/{stem}.zsh", f"{home}/.config/powerlevel10k/{stem}.zsh")
    write(f"{home}/.zshrc",
          f"cd {folder}\nPOWERLEVEL9K_DISABLE_CONFIGURATION_WIZARD=true\n"
          "source /opt/powerlevel10k/powerlevel10k.zsh-theme\nsource ~/.p10k.zsh\n"
          f"source ~/.config/powerlevel10k/{stem}.zsh\n")
    return ["/usr/bin/zsh"], {}, ["false\r", "sleep 3\r", 4.0]


def tmux(home, stem, files, variant):
    # two windows, the second split, with a message showing, so the status line, both window styles, the pane
    # borders and the message style are on screen
    copy(f"{files}/{stem}.tmux", f"{home}/.config/tmux/{stem}.tmux")
    write(f"{home}/.config/tmux/tmux.conf", f"source-file ~/.config/tmux/{stem}.tmux\n")
    return (["/usr/bin/tmux", "-L", "heritage", "new-session", "-n", "editor", ";", "new-window", "-n", "shell", ";",
             "split-window", "-h"], {"SHELL": "/bin/sh"}, "")


def zellij(home, stem, files, variant):
    # two panes running a command with the terminal's echo off, between the tab bar and the status bar, so the screen
    # shows both frame styles and no terminal replies that arrive late and would be echoed into a shell
    copy(f"{files}/{stem}.kdl", f"{home}/.config/zellij/themes/{stem}.kdl")
    write(f"{home}/.config/zellij/config.kdl",
          f'theme "{stem}"\nshow_startup_tips false\nshow_release_notes false\ndefault_shell "/bin/sh"\n')
    def pane(title):
        return f'pane name="{title}" command="sh" {{ args "-c" "stty -echo; exec sleep 600"; }}'
    write(f"{home}/.config/zellij/layouts/sample.kdl",
          "layout {\n"
          "    pane size=1 borderless=true { plugin location=\"zellij:tab-bar\"; }\n"
          "    pane split_direction=\"vertical\" {\n"
          f"        {pane('Heritage Themes')}\n        {pane(stem)}\n"
          "    }\n"
          "    pane size=2 borderless=true { plugin location=\"zellij:status-bar\"; }\n"
          "}\n")
    return ["/usr/local/bin/zellij", "--layout", "sample"], {"SHELL": "/bin/sh"}, ""


# Screen rows per app; the multiplexers fill the screen, so they get a short one.
SCREEN_ROWS = {"tmux": 14, "zellij": 14}


APPS = dict(fish=fish, zsh=zsh, nushell=nushell, powershell=powershell, starship=starship, oh_my_posh=oh_my_posh,
            powerlevel10k=powerlevel10k, tmux=tmux, zellij=zellij)


def run(argv, env, keys, quiet, rows=ROWS):
    screen = Screen(COLUMNS, rows)
    stream = pyte.ByteStream(screen)
    pid, fd = pty.fork()
    if pid == 0:
        os.chdir(env["HOME"])
        os.execve(argv[0], argv, env)
    fcntl.ioctl(fd, termios.TIOCSWINSZ, struct.pack("HHHH", rows, COLUMNS, 0, 0))
    # pyte answers terminal queries; a multiplexer would pass the answers on to the shell in its pane as typed text
    screen.write_process_input = (lambda data: None) if quiet else (lambda data: os.write(fd, data.encode()))
    def pump(seconds):
        """Reads output until it has been quiet for seconds."""
        start = last = time.monotonic()
        while time.monotonic() - last < seconds and time.monotonic() - start < TIMEOUT:
            if select.select([fd], [], [], 0.05)[0]:
                try:
                    data = os.read(fd, 1 << 16)
                except OSError:
                    return
                stream.feed(CONTROL_STRING.sub(b"", data))
                last = time.monotonic()
    try:
        pump(QUIET * 2)
        for key in keys:
            if isinstance(key, float):
                pump(key)  # a pause, as for a command that runs that long
            else:
                os.write(fd, key.encode())
                pump(0.05)
        pump(QUIET)
    finally:
        os.kill(pid, signal.SIGKILL)
        os.waitpid(pid, 0)
        os.close(fd)
    def colour(value, default):
        return default if value == "default" else "#" + value.upper() if len(value) == 6 else value
    return [[[cell.data, colour(cell.fg, "default"), colour(cell.bg, "default"), cell.bold, cell.italics,
              cell.underscore] for cell in (screen.buffer[y][x] for x in range(COLUMNS))] for y in range(rows)]


def main():
    app, stem, files, out = sys.argv[1:5]
    variant = sys.argv[5] if len(sys.argv) > 5 else None
    home = tempfile.mkdtemp(prefix="home-")
    env = dict(os.environ, HOME=home, XDG_CONFIG_HOME=f"{home}/.config", XDG_DATA_HOME=f"{home}/.local/share",
               XDG_CACHE_HOME=f"{home}/.cache", XDG_STATE_HOME=f"{home}/.local/state", TERM="xterm-256color",
               COLORTERM="truecolor", LANG="C.UTF-8")
    argv, extra, keys = APPS[app](home, stem, files, variant)
    env.update(extra)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(run(argv, env, keys, app in SCREEN_ROWS, SCREEN_ROWS.get(app, ROWS)), f)


if __name__ == "__main__":
    main()
