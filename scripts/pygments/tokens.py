"""Colours the preview samples as Pygments highlights them, for preview.py --pygments.

Usage: python tokens.py < request.json

The request is {"themes": [{"name", "attributes", "rules"}], "samples": [{"name", "code"}]}. A theme gives the style's
name, as Pygments looks it up in the pygments.styles entry point, the colour that each class attribute should have, and
for each token type that the style sets, as {"Name.Function": [colour, font style]}, its colour and font style. The
output is, per theme, per sample, the lines of [text, colour, font style] tokens that preview.py draws, with font styles
as Shiki numbers them.

The script fails, listing every difference, when a style that Pygments loads by name does not give a token type or a
class attribute what the request expects, so a run checks the installed package against the palettes as Pygments reads
it.
"""
import json, sys

import pygments.token
from pygments.lexers import get_lexer_for_filename
from pygments.styles import get_style_by_name
from pygments.token import STANDARD_TYPES

ITALIC, BOLD, UNDERLINE = 1, 2, 4


def token_type(name):
    """The Pygments token type that a dotted name such as Name.Function stands for, resolved as the generated module
    imports its parts."""
    parts = name.split(".")
    node = getattr(pygments.token, parts[0])
    for part in parts[1:]:
        node = getattr(node, part)
    return node


def font_flag(fonts, ttype, word):
    """Whether a token type is set in the font style word, such as bold: its own style says so or a parent's does, and
    `no` before the word, as in noitalic, turns it off."""
    while ttype is not None:
        words = fonts.get(ttype, "").split()
        if word in words:
            return True
        if "no" + word in words:
            return False
        ttype = ttype.parent
    return False


def check(theme, style):
    """The differences between the style and what the request expects of it."""
    problems = []
    for attribute, colour in theme["attributes"].items():
        if getattr(style, attribute) != colour:
            problems.append(f"{theme['name']}: {attribute} is {getattr(style, attribute)}, expected {colour}")
    fonts = {token_type(name): font for name, (_, font) in theme["rules"].items()}
    for name, (colour, font) in theme["rules"].items():
        ttype = token_type(name)
        resolved = style.style_for_token(ttype)
        found = (f"#{resolved['color']}".upper(), resolved["bold"], resolved["italic"])
        expected = (colour.upper(), font_flag(fonts, ttype, "bold"), font_flag(fonts, ttype, "italic"))
        if found != expected:
            problems.append(f"{theme['name']}: {name} is {found}, expected {expected}")
    return problems


def tokens(style, lexer, code):
    """Lines of [text, colour, font style] for the code, coloured by the style."""
    lines, line = [], []
    for ttype, value in lexer.get_tokens(code):
        # a lexer may use a type that Pygments' styles do not list, such as YAML's Literal.Scalar.Plain; a formatter
        # draws it as its nearest ancestor that they list
        while ttype not in STANDARD_TYPES:
            ttype = ttype.parent
        resolved = style.style_for_token(ttype)
        font = (ITALIC if resolved["italic"] else 0) | (BOLD if resolved["bold"] else 0) \
            | (UNDERLINE if resolved["underline"] else 0)
        for i, part in enumerate(value.split("\n")):
            if i:
                lines.append(line)
                line = []
            if part:
                line.append([part, f"#{resolved['color']}", font])
    if line:
        lines.append(line)
    return lines


def main():
    request = json.load(sys.stdin)
    problems, output = [], []
    for theme in request["themes"]:
        style = get_style_by_name(theme["name"])
        problems += check(theme, style)
        output.append([tokens(style, get_lexer_for_filename(sample["name"], stripnl=False), sample["code"])
                       for sample in request["samples"]])
    if problems:
        sys.exit("\n".join(problems))
    json.dump(output, sys.stdout)


if __name__ == "__main__":
    main()
