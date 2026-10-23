"""Colours the preview samples as Zed highlights them, for preview.py --zed.

Usage: python tokens.py CACHE_DIR < request.json

The request is {"themes": [Zed theme], "samples": [{"suffix", "code"}]}. The output is, per theme, per sample, the
lines of [text, colour, font style] tokens that preview.py draws, with font styles as Shiki numbers them.

languages.json pins every grammar and query to the release of Zed or of the language extension that ships it. The
grammars are compiled with cc into CACHE_DIR on first use. Highlighting follows Zed's syntax map: each capture
takes the theme's syntax key that is the longest dot-separated prefix of its name, and where captures overlap, the
one that starts last wins; at the same start, a capture of an injected language wins over its host's, and a later
pattern wins over an earlier one.
"""
import ctypes, hashlib, io, json, os, subprocess, sys, tarfile, tempfile, urllib.error, urllib.request

from tree_sitter import Language, Parser, Query, QueryCursor

HERE = os.path.dirname(os.path.abspath(__file__))
CAPSULE = ctypes.pythonapi.PyCapsule_New
CAPSULE.restype, CAPSULE.argtypes = ctypes.py_object, (ctypes.c_void_p, ctypes.c_char_p, ctypes.c_void_p)
ITALIC, BOLD = 1, 2


def download(url):
    with urllib.request.urlopen(url) as response:
        return response.read()


def cached(cache, name, produce):
    """The path of name in cache, made by produce(path) when missing."""
    path = os.path.join(cache, name)
    if not os.path.isfile(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        produce(path + ".part")
        os.replace(path + ".part", path)
    return path


def compile_grammar(spec, path):
    """Compiles the grammar's parser and scanner from its pinned source archive into a shared library at path."""
    data = download(spec["url"])
    if hashlib.sha256(data).hexdigest() != spec["sha256"]:
        raise SystemExit(f"tokens: {spec['url']} does not match its sha256 in languages.json")
    with tempfile.TemporaryDirectory() as tmp:
        with tarfile.open(fileobj=io.BytesIO(data)) as archive:
            archive.extractall(tmp, filter="data")
        root, = os.listdir(tmp)
        src = os.path.join(tmp, root, spec.get("path", ""), "src")
        sources = [os.path.join(src, name) for name in ("parser.c", "scanner.c")
                   if os.path.isfile(os.path.join(src, name))]
        subprocess.run(["cc", "-shared", "-fPIC", "-O2", "-std=c11", "-I", src, *sources, "-o", path], check=True)


def query(cache, base, name, language, required):
    """The compiled query base/name, or None when an optional one does not exist."""
    def fetch(path):
        try:
            text = download(f"{base}/{name}")
        except urllib.error.HTTPError as e:
            if e.code != 404 or required:
                raise SystemExit(f"tokens: cannot download {base}/{name}: {e}")
            text = b""
        with open(path, "wb") as f:
            f.write(text)
    path = cached(cache, os.path.join("queries", hashlib.sha256(base.encode()).hexdigest()[:16], name), fetch)
    with open(path, encoding="utf-8") as f:
        text = f.read()
    return Query(language, text) if text.strip() else None


class Languages:
    def __init__(self, cache):
        with open(os.path.join(HERE, "languages.json")) as f:
            manifest = json.load(f)
        self.cache, self.specs, self.grammars, self.loaded = cache, manifest["grammars"], {}, {}
        self.configs = manifest["languages"]

    def grammar(self, name):
        if name not in self.grammars:
            spec = self.specs[name]
            key = hashlib.sha256(f"{spec['sha256']}/{spec.get('path', '')}".encode()).hexdigest()[:16]
            library = ctypes.cdll.LoadLibrary(
                cached(self.cache, os.path.join("grammars", f"{name}-{key}.so"), lambda p: compile_grammar(spec, p)))
            function = getattr(library, f"tree_sitter_{name}")
            function.restype = ctypes.c_void_p
            self.grammars[name] = Language(CAPSULE(function(), b"tree_sitter.Language", None))
        return self.grammars[name]

    def find(self, name):
        """The language Zed picks for an injection or file: by name, code fence name or file suffix."""
        name = name.lower()
        for config in self.configs:
            if name in (config["name"].lower(), config.get("fence"), *config["suffixes"]):
                if config["name"] not in self.loaded:
                    language = self.grammar(config["grammar"])
                    self.loaded[config["name"]] = (
                        language, query(self.cache, config["queries"], "highlights.scm", language, True),
                        query(self.cache, config["queries"], "injections.scm", language, False))
                return self.loaded[config["name"]]
        return None


def captures(languages, language, source, ranges=None, depth=0):
    """(start, depth, pattern, end, capture name) of every capture in the layer and the layers injected into it. As in
    Zed, an injection parses the content nodes of a match, children included, as one layer, and a combined injection
    parses the content of all its matches as one layer per language."""
    grammar, highlights, injections = language
    parser = Parser(grammar)
    if ranges is not None:
        parser.included_ranges = ranges
    root = parser.parse(source).root_node
    out = [(node.start_byte, depth, pattern, node.end_byte, name)
           for pattern, match in QueryCursor(highlights).matches(root)
           for name, nodes in match.items() if not name.startswith("_") for node in nodes]
    if injections is None:
        return out
    combined = {}
    for pattern, match in QueryCursor(injections).matches(root):
        settings = injections.pattern_settings(pattern)
        nodes = match.get("injection.content") or match.get("content")
        named = match.get("injection.language") or match.get("language")
        name = named[0].text.decode().rpartition(".")[2] if named else \
            settings.get("injection.language") or settings.get("language")
        injected = languages.find(name) if name and nodes else None
        if injected is None:
            continue
        content = sorted((node.range for node in nodes), key=lambda r: r.start_byte)
        if "injection.combined" in settings:
            combined.setdefault(id(injected), (injected, []))[1].extend(content)
        else:
            out += captures(languages, injected, source, content, depth + 1)
    for injected, content in combined.values():
        out += captures(languages, injected, source, sorted(content, key=lambda r: r.start_byte), depth + 1)
    return out


def style_of(syntax, name):
    """The syntax style for a capture name: the longest key that is a dot-separated prefix of it."""
    while name:
        if name in syntax:
            return syntax[name]
        name = name.rpartition(".")[0]
    return None


def tokens(languages, theme, suffix, code):
    style = theme["style"]
    syntax, foreground = style["syntax"], style["editor.foreground"][:7]
    source = (code + "\n").encode()  # a file ends with a newline, which some grammars need to close the last block
    language = languages.find(suffix)
    if language is None:
        raise SystemExit(f"tokens: no language in languages.json for .{suffix}")
    painted = [None] * len(source)
    for start, _, _, end, name in sorted(captures(languages, language, source), key=lambda c: c[:3]):
        found = style_of(syntax, name)
        if found:
            painted[start:end] = [found] * (end - start)
    lines, line, pos = [], [], 0
    while pos <= len(source):
        if pos == len(source) or source[pos] == ord("\n"):
            lines.append(line)
            line, pos = [], pos + 1
            continue
        end = pos
        while end < len(source) and source[end] != ord("\n") and painted[end] is painted[pos]:
            end += 1
        found = painted[pos] or {}
        font = (ITALIC if found.get("font_style") == "italic" else 0) | \
               (BOLD if (found.get("font_weight") or 400) >= 700 else 0)
        line.append([source[pos:end].decode(), (found.get("color") or foreground)[:7], font])
        pos = end
    return lines[:-1]


def main():
    cache = sys.argv[1]
    request = json.load(sys.stdin)
    languages = Languages(cache)
    out = [[tokens(languages, theme, s["suffix"], s["code"]) for s in request["samples"]]
           for theme in request["themes"]]
    json.dump(out, sys.stdout)


if __name__ == "__main__":
    main()
