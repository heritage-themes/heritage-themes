"""Colours the preview samples as Neovim draws them, for preview.py --nvim.

Usage: python screen.py CACHE_DIR PLUGIN_DIR < request.json

The request is {"schemes": [colour scheme name], "samples": [{"name", "code"}]}. The output is, per scheme, per sample,
the lines of [text, colour, font style] tokens that preview.py draws, with font styles as Shiki numbers them.

Neovim runs embedded with the plugin in PLUGIN_DIR, nvim-treesitter and its parsers, as a user who installed them has
it: each sample opens as a file, its filetype starts Tree-sitter highlighting, and the colours are read from the screen
that Neovim sends to its UI (:help ui-linegrid), so they are the colours Neovim draws. parsers.json pins nvim-treesitter
and every grammar to the revision that nvim-treesitter pins; the grammars are compiled with cc into CACHE_DIR on first
use. Loading a scheme fails the run when a highlight group keeps a colour of Neovim's default scheme.
"""
import hashlib, io, json, os, shutil, subprocess, sys, tarfile, tempfile, urllib.request

import msgpack

HERE = os.path.dirname(os.path.abspath(__file__))
ITALIC, BOLD, UNDERLINE = 1, 2, 4
COLUMNS, ROWS = 160, 40
REQUEST, RESPONSE, NOTIFICATION = 0, 1, 2
# A user's setup: Tree-sitter for every filetype with a parser, and a plain editor window.
SETUP = r"""
vim.api.nvim_create_autocmd("FileType", { callback = function() pcall(vim.treesitter.start) end })
vim.o.number, vim.o.relativenumber, vim.o.signcolumn, vim.o.cursorline = false, false, "no", false
vim.o.laststatus, vim.o.showtabline, vim.o.ruler, vim.o.showmode, vim.o.wrap = 0, 0, false, false, false
vim.opt.shortmess:append("IF")
"""
# The groups whose colours come from Neovim's default scheme rather than the scheme just loaded.
LEAKS = r"""
local scheme = ...
local file = vim.api.nvim_get_runtime_file("colors/" .. scheme .. ".lua", false)[1]
local text = table.concat(vim.fn.readfile(file), "\n")
local leaks = {}
for group, definition in pairs(vim.api.nvim_get_hl(0, {})) do
  if not definition.link and (definition.fg or definition.bg or definition.sp)
      and not text:find('hl("' .. group .. '"', 1, true) then
    table.insert(leaks, group)
  end
end
table.sort(leaks)
return leaks
"""
# Opens a sample and parses it with its injections, so the redraw that follows draws every highlight.
OPEN = r"""
local path = ...
vim.cmd.edit({ path, bang = true })
local buffer = vim.api.nvim_get_current_buf()
if not vim.treesitter.highlighter.active[buffer] then
  return "no Tree-sitter highlighting for filetype " .. vim.bo[buffer].filetype
end
vim.treesitter.get_parser(buffer):parse(true)
return ""
"""


def download(url, sha256):
    with urllib.request.urlopen(url) as response:
        data = response.read()
    if hashlib.sha256(data).hexdigest() != sha256:
        raise SystemExit(f"screen: {url} does not match its sha256 in parsers.json")
    return data


def cached(path, produce):
    """path, made by produce(path) when missing."""
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        produce(path + ".part")
        os.replace(path + ".part", path)
    return path


def extract(spec, path):
    """Extracts the pinned archive's top folder to path."""
    with tempfile.TemporaryDirectory() as tmp:
        with tarfile.open(fileobj=io.BytesIO(download(spec["url"], spec["sha256"]))) as archive:
            archive.extractall(tmp, filter="data")
        root, = os.listdir(tmp)
        shutil.move(os.path.join(tmp, root), path)


def compile_grammar(spec, path):
    """Compiles the grammar's parser and scanner into a shared library at path."""
    with tempfile.TemporaryDirectory() as tmp:
        extract(spec, os.path.join(tmp, "grammar"))
        src = os.path.join(tmp, "grammar", spec.get("path", ""), "src")
        sources = [os.path.join(src, name) for name in ("parser.c", "scanner.c")
                   if os.path.isfile(os.path.join(src, name))]
        subprocess.run(["cc", "-shared", "-fPIC", "-O2", "-std=c11", "-I", src, *sources, "-o", path], check=True)


def install(cache, site):
    """nvim-treesitter's folder, after compiling each grammar into site/parser as nvim-treesitter installs it."""
    with open(os.path.join(HERE, "parsers.json"), encoding="utf-8") as f:
        manifest = json.load(f)
    plugin = manifest["nvim-treesitter"]
    treesitter = cached(os.path.join(cache, "nvim-treesitter-" + plugin["sha256"][:16]), lambda p: extract(plugin, p))
    os.makedirs(os.path.join(site, "parser"))
    for name, spec in manifest["grammars"].items():
        key = hashlib.sha256(f"{spec['sha256']}/{spec.get('path', '')}".encode()).hexdigest()[:16]
        library = cached(os.path.join(cache, "grammars", f"{name}-{key}.so"), lambda p: compile_grammar(spec, p))
        shutil.copy(library, os.path.join(site, "parser", f"{name}.so"))
    return treesitter


class Neovim:
    """An embedded Neovim with a UI attached, which keeps the screen grid that Neovim draws."""

    def __init__(self, runtimepath, home):
        env = dict(os.environ, HOME=home, XDG_CONFIG_HOME=os.path.join(home, "config"),
                   XDG_DATA_HOME=os.path.join(home, "data"), XDG_STATE_HOME=os.path.join(home, "state"),
                   XDG_CACHE_HOME=os.path.join(home, "cache"))
        self.process = subprocess.Popen(
            ["nvim", "--embed", "--clean", "-n", "-i", "NONE", "--cmd", "let g:loaded_matchparen = 1",
             "--cmd", "set rtp^=" + ",".join(path.replace(",", r"\,") for path in runtimepath)],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, env=env)
        self.unpacker = msgpack.Unpacker(raw=False, strict_map_key=False)
        self.ids, self.grid, self.attributes, self.default = 0, [], {}, (0, 0)

    def request(self, method, *args):
        self.ids += 1
        self.process.stdin.write(msgpack.packb([REQUEST, self.ids, method, list(args)]))
        self.process.stdin.flush()
        while True:
            for message in self.unpacker:
                if message[0] == RESPONSE and message[1] == self.ids:
                    if message[2]:
                        raise SystemExit(f"screen: {method} failed: {message[2]}")
                    return message[3]
                if message[0] == NOTIFICATION and message[1] == "redraw":
                    for event in message[2]:
                        for args_ in event[1:]:
                            getattr(self, "on_" + event[0], lambda *_: None)(*args_)
            data = os.read(self.process.stdout.fileno(), 1 << 16)
            if not data:
                raise SystemExit(f"screen: Neovim exited during {method}")
            self.unpacker.feed(data)

    def on_grid_resize(self, grid, width, height):
        self.grid = [[[" ", 0] for _ in range(width)] for _ in range(height)]

    def on_grid_clear(self, grid):
        for row in self.grid:
            row[:] = [[" ", 0] for _ in row]

    def on_grid_scroll(self, grid, top, bottom, left, right, rows, cols):
        moved = [row[left:right] for row in self.grid[top:bottom]]
        for i in range(top, bottom):
            if top <= i - rows < bottom:
                self.grid[i - rows][left:right] = [cell[:] for cell in moved[i - top]]

    def on_grid_line(self, grid, row, column, cells, wrap=False):
        attribute = 0
        for cell in cells:
            if len(cell) > 1:
                attribute = cell[1]
            for _ in range(cell[2] if len(cell) > 2 else 1):
                self.grid[row][column] = [cell[0], attribute]
                column += 1

    def on_hl_attr_define(self, id_, rgb, cterm, info):
        self.attributes[id_] = rgb

    def on_default_colors_set(self, foreground, background, special, cterm_foreground, cterm_background):
        self.default = (foreground, background)

    def tokens(self, lines):
        """The rows that hold lines as [text, colour, font style] tokens."""
        out = []
        for row, line in zip(self.grid, lines):
            tokens = []
            for text, attribute in row[:len(line)]:
                rgb = self.attributes.get(attribute, {})
                colour = "#{:06X}".format(rgb.get("foreground", self.default[0]))
                font = (ITALIC if rgb.get("italic") else 0) | (BOLD if rgb.get("bold") else 0) | \
                       (UNDERLINE if rgb.get("underline") else 0)
                if tokens and tokens[-1][1:] == [colour, font]:
                    tokens[-1][0] += text
                else:
                    tokens.append([text, colour, font])
            if "".join(t[0] for t in tokens) != line:
                raise SystemExit(f"screen: the screen shows {''.join(t[0] for t in tokens)!r} for {line!r}")
            out.append(tokens)
        return out


def main():
    cache, plugin = sys.argv[1:]
    request = json.load(sys.stdin)
    with tempfile.TemporaryDirectory() as tmp:
        site = os.path.join(tmp, "site")
        treesitter = install(cache, site)
        samples = []
        for sample in request["samples"]:
            path = os.path.join(tmp, "samples", sample["name"])
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8", newline="\n") as f:
                f.write(sample["code"] + "\n")
            samples.append((path, sample["code"].split("\n")))
        if max(len(lines) for _, lines in samples) >= ROWS:
            raise SystemExit(f"screen: a sample is taller than ROWS ({ROWS}); raise ROWS in {__file__}")
        nvim = Neovim([plugin, treesitter, os.path.join(treesitter, "runtime"), site], os.path.join(tmp, "home"))
        nvim.request("nvim_ui_attach", COLUMNS, ROWS, {"rgb": True, "ext_linegrid": True})
        nvim.request("nvim_exec_lua", SETUP, [])
        out = []
        for scheme in request["schemes"]:
            nvim.request("nvim_command", f"colorscheme {scheme}")
            leaks = nvim.request("nvim_exec_lua", LEAKS, [scheme])
            if leaks:
                raise SystemExit(f"screen: {scheme} leaves Neovim's default colours in {', '.join(leaks)}")
            files = []
            for path, lines in samples:
                problem = nvim.request("nvim_exec_lua", OPEN, [path])
                if problem:
                    raise SystemExit(f"screen: {os.path.basename(path)}: {problem}")
                nvim.request("nvim_command", "redraw!")
                files.append(nvim.tokens(lines))
            out.append(files)
        nvim.process.stdin.close()
        nvim.process.wait()
    json.dump(out, sys.stdout)


if __name__ == "__main__":
    main()
