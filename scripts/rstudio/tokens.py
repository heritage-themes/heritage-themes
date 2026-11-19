#!/usr/bin/env python3
"""Lists the token types that the Ace modes of an RStudio installation emit, and checks them against the token rules
of heritage/rstudio.py.

Usage: scripts/rstudio/tokens.py RSTUDIO_DIR [--all]

RSTUDIO_DIR is a folder that holds www/rstudio, where RStudio keeps its compiled editor, at any depth: the folder that
RStudio is installed in, or an unpacked Linux archive. The script reads the token types that the modes name in their
rules, which Ace turns into the classes of the elements it draws: the type `constant.numeric` becomes the classes
`ace_constant` and `ace_numeric`. A rule's selector matches a type that has all of its classes.

It prints three lists:

- the token types that no rule colours, which take the editor's text colour, for the modes of the most used languages,
  or for all modes with --all;
- the selectors of the token rules that match no type, which RStudio never emits;
- the selectors of the rules for markers, the gutter and the rest of the editor that a token type also matches, which
  draws that token with the marker's colours.

The exit status is 1 when a token rule's selector matches no type.

The script reads the compiled editor with regular expressions, so it finds the types that a mode writes literally and
those of its keyword tables, not those that a mode computes, and it adds the suffix that RStudio's R mode gives the
tokens of roxygen text.
"""
import collections, glob, os, re, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

import heritage  # noqa: E402
from heritage import rstudio  # noqa: E402

# The modes of the languages that RStudio's users write most, which the checks and the default listing cover.
POPULAR = ("r", "rmarkdown", "markdown", "python", "c_cpp", "sql", "pgsql", "mysql", "javascript", "typescript", "html",
           "css", "scss", "less", "yaml", "json", "sh", "java", "julia", "stan", "rust", "golang", "tex", "latex", "sweave",
           "rdoc", "rhtml", "xml", "toml", "dockerfile", "makefile", "powershell", "ruby", "php", "csharp", "scala",
           "swift", "lua", "perl", "diff", "ini", "properties")
# Types that take the editor's text colour by design: whitespace, plain words and the markers of empty lines.
PLAIN = {"text", "identifier", "identifer", "empty", "empty_line", "indent", "whitespace", "newline", "nospell",
         "nospell.text", "nospell.", "text.nospell", "term", "text.xml", "text.whitespace.xml", "invisible"}
MODE = re.compile(r'define\("((?:ace/)?mode/[a-z0-9_]+)_highlight_rules"')
TYPE = re.compile(r"[a-z][a-z0-9_.\-]*")


def bundles(directory):
    """The compiled editor files that hold the modes."""
    found = glob.glob(os.path.join(directory, "**", "www", "rstudio", "*.cache.js"), recursive=True)
    if not found:
        sys.exit(f"{directory} has no www/rstudio folder with the compiled editor")
    return [path for path in found if "highlight_rules" in open(path, encoding="utf-8", errors="replace").read()]


def types(directory):
    """type → set of modes that emit it."""
    found = collections.defaultdict(set)
    for path in bundles(directory):
        text = open(path, encoding="utf-8", errors="replace").read()
        starts = [(m.start(), m.group(1).split("/")[-1]) for m in MODE.finditer(text)]
        for (start, mode), nxt in zip(starts, starts[1:] + [(len(text), None)]):
            end = text.find('define("', start + 10)
            body = text[start:min(nxt[0], end if end != -1 else nxt[0])]
            for m in re.finditer(r'(?:token|defaultToken)\s*:\s*("(?:[^"\\]|\\.)*"|\[[^\]]*\])', body):
                # a list of types may be written as one string that the mode splits on spaces
                for written in re.findall(r'"((?:[^"\\]|\\.)*)"', m.group(1)):
                    for token in written.split(" "):
                        if TYPE.fullmatch(token):
                            found[token].add(mode)
            for m in re.finditer(r'createKeywordMapper\(\{(.{0,3000}?)\},\s*"([a-z.\-_]+)"', body, re.S):
                for token in re.findall(r'"([a-z][a-z.\-_]*)"\s*:\s*"', m.group(1)) + [m.group(2)]:
                    found[token].add(mode)
    # RStudio's R mode embeds the roxygen rules with this suffix on every token
    for token in [t for t, modes in found.items() if "rdoc" in modes]:
        found[token + ".virtual-comment"].add("r")
    return found


def classes(selector):
    """The set of class names of a selector of compound classes such as .ace_keyword.ace_operator."""
    return set(re.findall(r"\.ace_([A-Za-z0-9_\-]+)", selector))


def main():
    arguments = [a for a in sys.argv[1:] if a != "--all"]
    if len(arguments) != 1:
        sys.exit(__doc__)
    found = types(arguments[0])
    everything = "--all" in sys.argv
    p = heritage.load_families()[0].THEMES[0]["palette"]
    selectors = {s for rule in rstudio.syntax(p) for s in rule[0]}
    sets = {s: classes(s) for s in selectors}
    dead = sorted(s for s, wanted in sets.items() if not any(wanted <= set(t.split(".")) for t in found))
    uncovered = collections.defaultdict(list)
    for token, modes in sorted(found.items()):
        shown = modes if everything else modes & set(POPULAR)
        if not shown or token in PLAIN or any(wanted <= set(token.split(".")) for wanted in sets.values()):
            continue
        uncovered[token] = sorted(shown)
    print(f"{len(found)} token types in {len({m for v in found.values() for m in v})} modes")
    print(f"\n{len(uncovered)} types that no rule colours"
          + ("" if everything else " in the most used languages (--all lists every mode)") + ":")
    for token, modes in uncovered.items():
        print(f"  {token:50} {', '.join(modes[:8])}{' ...' if len(modes) > 8 else ''}")
    print(f"\n{len(dead)} selectors that match no type:")
    for selector in dead:
        print(f"  {selector}")
    markers = sorted({s for rule, _ in rstudio.blocks(p) for s in rule
                      if re.fullmatch(r"(?:\.ace_[\w\-]+)+", s) and s not in selectors})
    clashes = {s: sorted(t for t in found if classes(s) <= set(t.split("."))) for s in markers}
    clashes = {s: types_ for s, types_ in clashes.items() if types_}
    print(f"\n{len(clashes)} marker selectors that a token type also matches:")
    for selector, matching in clashes.items():
        print(f"  {selector:40} {', '.join(matching[:6])}")
    return 1 if dead else 0


if __name__ == "__main__":
    sys.exit(main())
