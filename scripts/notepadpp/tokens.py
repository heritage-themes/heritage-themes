"""Colours the preview samples as Notepad++ highlights them, for preview.py --notepadpp.

Usage: python tokens.py CACHE_DIR < request.json

The request is {"themes": [Notepad++ theme XML], "samples": [{"suffix", "code"}]}. The output is, per theme, per
sample, the lines of [text, colour, font style] tokens that preview.py draws, with font styles as Shiki numbers them.

source.json pins the Notepad++ source, which carries the Lexilla that Notepad++ builds with. Its lexers and the test
document of Lexilla's own tests are compiled with c++ into style.cxx's driver in CACHE_DIR on first use. lexers.json
gives each sample suffix what Notepad++ sets for the language it opens the file as (see ScintillaEditView.cpp): the
lexer, the keyword lists from langs.model.xml, the lexer properties and the LexerTypes of the theme whose styles
apply. A suffix without a lexer opens as Normal Text. Colours follow Notepad++: every style starts as the theme's
Default Style, then takes its WordsStyle; a WordsStyle without COLORSTYLE_FOREGROUND in colorStyle keeps the Default
Style's text colour.
"""
import concurrent.futures, hashlib, io, json, os, re, shutil, subprocess, sys, tarfile, tempfile, urllib.request
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(os.environ.get("XDG_CACHE_HOME") or os.path.expanduser("~/.cache"), "heritage-themes",
                     "notepadpp")
# The parts of the source that the driver and scripts/notepadpp/styles.py read.
PARTS = ("lexilla/", "scintilla/include/", "PowerEditor/src/langs.model.xml", "PowerEditor/src/stylers.model.xml")
DEFAULT_STYLE = 32  # STYLE_DEFAULT, the Default Style of GlobalStyles
COLORSTYLE_FOREGROUND = 1
# Notepad++ fontStyle bits to Shiki's.
FONT = ((1, 2), (2, 1), (4, 4))
DRIVER = "style.exe" if os.name == "nt" else "style"


def pin():
    with open(os.path.join(HERE, "source.json"), encoding="utf-8") as f:
        return json.load(f)


def source_tree(cache):
    """The folder in cache that holds PARTS of the pinned source, downloaded and extracted on first use."""
    spec = pin()
    tree = os.path.join(cache, spec["sha256"][:16], "source")
    if os.path.isdir(tree):
        return tree
    with urllib.request.urlopen(spec["url"]) as response:
        data = response.read()
    if hashlib.sha256(data).hexdigest() != spec["sha256"]:
        raise SystemExit(f"tokens: {spec['url']} does not match its sha256 in source.json")
    with tempfile.TemporaryDirectory(dir=cache if os.path.isdir(cache) else None) as tmp:
        with tarfile.open(fileobj=io.BytesIO(data)) as archive:
            members = [m for m in archive.getmembers()
                       if m.name.partition("/")[2].startswith(PARTS) and (m.isfile() or m.isdir())]
            archive.extractall(tmp, members=members, filter="data")
        root, = os.listdir(tmp)
        os.makedirs(os.path.dirname(tree), exist_ok=True)
        shutil.move(os.path.join(tmp, root), tree)
    return tree


def lexer_sources(lexilla):
    """The lexer files that define a lexer in Lexilla's catalogue. Notepad++ keeps lexers of its own in the same
    folder and registers them itself; those need Windows and are left out."""
    with open(os.path.join(lexilla, "src", "Lexilla.cxx"), encoding="utf-8") as f:
        catalogue = set(re.findall(r"^extern const LexerModule (lm\w+);", f.read(), re.M))
    folder = os.path.join(lexilla, "lexers")
    sources = []
    for name in sorted(os.listdir(folder)):
        if name.endswith(".cxx"):
            with open(os.path.join(folder, name), encoding="utf-8", errors="replace") as f:
                defined = set(re.findall(r"\bLexerModule\s+(lm\w+)\s*\(", f.read()))
            if defined & catalogue:
                sources.append(os.path.join(folder, name))
    return sources


def driver(tree, cache):
    """The compiled driver for the pinned source, built with c++ on first use."""
    path = os.path.join(cache, pin()["sha256"][:16], DRIVER)
    if os.path.isfile(path):
        return path
    lexilla = os.path.join(tree, "lexilla")
    sources = [*lexer_sources(lexilla),
               *(os.path.join(lexilla, "lexlib", n) for n in sorted(os.listdir(os.path.join(lexilla, "lexlib")))
                 if n.endswith(".cxx")),
               os.path.join(lexilla, "src", "Lexilla.cxx"), os.path.join(lexilla, "test", "TestDocument.cxx"),
               os.path.join(HERE, "style.cxx")]
    flags = ["-std=c++17", "-O1", "-w", "-DNDEBUG", "-DLEXILLA_NO_EXPORT",
             *(f"-I{os.path.join(tree, *d)}" for d in (("scintilla", "include"), ("lexilla", "include"),
                                                       ("lexilla", "lexlib"), ("lexilla", "test")))]
    with tempfile.TemporaryDirectory() as tmp:
        def compile_one(numbered):
            i, source = numbered
            obj = os.path.join(tmp, f"{i}.o")
            result = subprocess.run(["c++", *flags, "-c", source, "-o", obj], capture_output=True, text=True)
            if result.returncode:
                raise SystemExit(f"tokens: c++ failed on {source}:\n{result.stderr}")
            return obj
        with concurrent.futures.ThreadPoolExecutor(os.cpu_count()) as pool:
            objects = list(pool.map(compile_one, enumerate(sources)))
        # On Windows the C++ runtime is a DLL beside the compiler; linking it in lets the cached driver run without the
        # compiler on PATH.
        subprocess.run(["c++", *objects, *(["-static"] if os.name == "nt" else []), "-o", path + ".part"], check=True)
    os.replace(path + ".part", path)
    return path


def keyword_lists(tree):
    """(language, keyword class) to the words of langs.model.xml."""
    root = ET.parse(os.path.join(tree, "PowerEditor", "src", "langs.model.xml")).getroot()
    return {(language.get("name"), k.get("name")): " ".join((k.text or "").split())
            for language in root.iter("Language") for k in language.iter("Keywords")}


def styles(program, spec, words, code):
    """The style of each character of code under the lexer and settings in spec."""
    data = code.encode("utf-8")
    keywords = [f"{i} {words.get(tuple(source), '')}" for i, source in spec["keywords"].items()]
    request = "\n".join([spec["lexer"], str(len(spec["properties"])),
                         *(f"{k}={v}" for k, v in spec["properties"].items()), str(len(keywords)), *keywords,
                         str(len(data))]).encode("utf-8") + b"\n" + data
    result = subprocess.run([program], input=request, capture_output=True)
    if result.returncode:
        raise SystemExit(f"tokens: the driver failed on {spec['lexer']}:\n{result.stderr.decode()}")
    per_byte = [int(s) for s in result.stdout.split()]
    out, position = [], 0
    for character in code:
        out.append(per_byte[position])
        position += len(character.encode("utf-8"))
    return out


def palette(theme, stylers):
    """Style number to (colour, Shiki font style) for a file whose language uses the LexerTypes in stylers."""
    root = ET.fromstring(theme)
    default = next(w for w in root.iter("WidgetStyle") if int(w.get("styleID")) == DEFAULT_STYLE
                   and w.get("name") == "Default Style")
    def font(style):
        bits = int(style.get("fontStyle") or 0)
        return sum(shiki for npp, shiki in FONT if bits & npp)
    base = ("#" + default.get("fgColor"), font(default))
    table = {}
    lexers = {lexer.get("name"): lexer for lexer in root.iter("LexerType")}
    for name in stylers:
        for style in lexers[name].iter("WordsStyle"):
            foreground = int(style.get("colorStyle", "3")) & COLORSTYLE_FOREGROUND
            table[int(style.get("styleID"))] = ("#" + style.get("fgColor") if foreground else base[0], font(style))
    return base, table


def tokens(code, numbers, base, table):
    """Lines of [text, colour, font style] runs."""
    lines, line, run = [], [], None
    for character, number in zip(code, numbers if numbers else [DEFAULT_STYLE] * len(code)):
        if character == "\n":
            lines.append(line)
            line, run = [], None
            continue
        colour, font = table.get(number, base)
        if run and run[1] == colour and run[2] == font:
            run[0] += character
        else:
            run = [character, colour, font]
            line.append(run)
    lines.append(line)
    return lines


def main():
    cache = sys.argv[1]
    os.makedirs(cache, exist_ok=True)
    request = json.load(sys.stdin)
    with open(os.path.join(HERE, "lexers.json"), encoding="utf-8") as f:
        specs = json.load(f)
    tree = source_tree(cache)
    program, words = driver(tree, cache), keyword_lists(tree)
    styled = []
    for sample in request["samples"]:
        spec = specs.get(sample["suffix"])
        if spec is None:
            raise SystemExit(f"tokens: lexers.json has no entry for .{sample['suffix']}")
        styled.append((spec, styles(program, spec, words, sample["code"]) if spec["lexer"] else None))
    out = []
    for theme in request["themes"]:
        files = []
        for sample, (spec, numbers) in zip(request["samples"], styled):
            base, table = palette(theme, spec.get("stylers", []))
            files.append(tokens(sample["code"], numbers, base, table))
        out.append(files)
    json.dump(out, sys.stdout)


if __name__ == "__main__":
    main()
