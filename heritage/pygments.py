"""Pygments styles generated from a palette: one style class for each Heritage theme, in one module.

A Pygments style sets a colour and a font style for each token type of its lexers, and the colours of the code block
that the formatters draw: the background, the highlighted lines and the line numbers. A token type takes the style of
its parent unless it sets one, so the rules below name only the types that differ from their parent. The roles are
those that heritage.vscode and heritage.textadept give the matching constructs: a lexer gives a construct one token
type in every language, as Textadept's lexers do, so HTML attributes take the field role, as in the other targets.
Preprocessor directives take the role that heritage.colour.directive gives them, as in VS Code.

The module ships as a wheel on PyPI. It registers each style under the pygments.styles entry point, which is how
Pygments finds a style by name in pygmentize, HtmlFormatter(style=...), Sphinx, MkDocs and every other program that
takes a Pygments style name. The wheel is pure Python, so it installs in any environment that has Pygments.
"""
import re

from .colour import directive
from .nvim import name  # noqa: F401 - a style takes the name of Neovim's scheme, so one name serves every app
from .wheel import pack

DISTRIBUTION = "heritage-themes-pygments"  # the wheel's project name on PyPI
MODULE = "heritage_themes_pygments"  # what a program imports to use a class, and the wheel's only module
VENDOR = "Heritage Themes"
# The oldest Pygments and Python that the module is tested with.
PYGMENTS = "2.14"
PYTHON = "3.8"
# The token types that a style sets, in the order that the generated module lists them. A rule gives the types, the
# palette role of their colour and a font style, which `bold` for keywords depends on the palette's kwBold.
TOKEN_TYPES = (
    "Token", "Error", "Comment", "Comment.Hashbang", "Comment.Preproc", "Comment.PreprocFile", "Comment.Special",
    "Keyword", "Name.Attribute", "Name.Builtin", "Name.Builtin.Pseudo", "Name.Class", "Name.Constant",
    "Name.Decorator", "Name.Entity", "Name.Exception", "Name.Function", "Name.Label", "Name.Namespace",
    "Name.Property", "Name.Tag", "Name.Variable", "Name.Variable.Class", "Name.Variable.Instance",
    "Name.Variable.Magic", "Literal.Date", "String", "String.Affix", "String.Doc", "String.Escape",
    "String.Interpol", "Number", "Operator", "Operator.Word", "Punctuation", "Generic.Deleted", "Generic.Emph",
    "Generic.EmphStrong", "Generic.Error", "Generic.Heading", "Generic.Inserted", "Generic.Output",
    "Generic.Prompt", "Generic.Strong", "Generic.Subheading", "Generic.Traceback")
IMPORTS = ("Comment", "Error", "Generic", "Keyword", "Literal", "Name", "Number", "Operator", "Punctuation", "String",
           "Token")
# The words of a style string that the generator writes: font styles that Pygments reads, then the colour.
STYLE = re.compile(r"((bold|italic|noitalic) )*#[0-9A-F]{6}")


def rules(p):
    """(token type, role, font style) for each of TOKEN_TYPES, in that order."""
    kw = "bold " if p.get("kwBold", not p["dark"]) else ""
    table = {
        "Token": ("fg", ""),
        "Error": ("ansiRed", ""),
        "Comment": ("comment", "italic"),
        "Comment.Hashbang": ("comment", "bold italic"),
        "Comment.Preproc": (directive(p), "noitalic"),
        "Comment.PreprocFile": ("string", "noitalic"),
        "Comment.Special": ("todo", "bold italic"),
        "Keyword": ("keyword", kw.strip()),
        "Name.Attribute": ("field", ""),
        "Name.Builtin": ("call", "italic"),
        "Name.Builtin.Pseudo": ("keyword", "italic"),
        "Name.Class": ("type", ""),
        "Name.Constant": ("constant", "bold italic"),
        "Name.Decorator": ("annotation", ""),
        "Name.Entity": ("gold", ""),
        "Name.Exception": ("type", ""),
        "Name.Function": ("method", "bold"),
        "Name.Label": ("label", ""),
        "Name.Namespace": ("fg", ""),
        "Name.Property": ("field", ""),
        "Name.Tag": ("keyword", kw.strip()),
        "Name.Variable": ("fg", ""),
        "Name.Variable.Class": ("field", ""),
        "Name.Variable.Instance": ("field", ""),
        "Name.Variable.Magic": ("call", "italic"),
        "Literal.Date": ("number", ""),
        "String": ("string", ""),
        "String.Affix": ("keyword", kw.strip()),
        "String.Doc": ("doc", "italic"),
        "String.Escape": ("gold", "bold"),
        "String.Interpol": ("gold", "bold"),
        "Number": ("number", ""),
        "Operator": ("op", ""),
        "Operator.Word": ("keyword", kw.strip()),
        "Punctuation": ("op", ""),
        "Generic.Deleted": ("ansiRed", ""),
        "Generic.Emph": ("fg", "italic"),
        "Generic.EmphStrong": ("fg", "bold italic"),
        "Generic.Error": ("ansiRed", ""),
        "Generic.Heading": ("method", "bold"),
        "Generic.Inserted": ("ansiGreen", ""),
        "Generic.Output": ("muted", ""),
        "Generic.Prompt": ("muted", "bold"),
        "Generic.Strong": ("fg", "bold"),
        "Generic.Subheading": ("method", ""),
        "Generic.Traceback": ("ansiRed", ""),
    }
    assert tuple(table) == TOKEN_TYPES
    return [(token, role, font) for token, (role, font) in table.items()]


def style_string(p, role, font):
    """The string that a style class gives a token type: the font styles, then the colour."""
    return f"{font} #{p[role]}".strip()


def class_name(t):
    """The style class of a theme dict from a theme.py, for example ShakerPrussianDarkStyle."""
    return "".join(part.title() for part in name(t).split("-")[1:]) + "Style"


def attributes(p):
    """(attribute, colour as #RRGGBB) of a style class beside its styles: the background, the highlighted lines and
    the line numbers. A highlighted line takes the current line's colour, the one other background that every code role
    is readable on."""
    return [("background_color", "#" + p["bg"]), ("highlight_color", "#" + p["caretRow"]),
            ("line_number_color", "#" + p["lineNo"]), ("line_number_background_color", "#" + p["bg"]),
            ("line_number_special_color", "#" + p["muted"]), ("line_number_special_background_color", "#" + p["bg"])]


def style_class(t, source):
    """The class of a theme dict from a theme.py as source text; source is the URL of the family's folder."""
    p = t["palette"]
    lines = [f"class {class_name(t)}(Style):", f'    """{p["name"]}: {source}"""', "",
             f'    name = "{name(t)}"']
    lines += [f'    {attribute} = "{colour}"' for attribute, colour in attributes(p)]
    lines += ["    styles = {"]
    lines += [f'        {token}: "{style_string(p, role, font)}",' for token, role, font in rules(p)]
    lines += ["    }"]
    return "\n".join(lines)


def module(themes):
    """The module's source text. themes is a list of (theme dict, URL of the family's folder)."""
    classes = [class_name(t) for t, _ in themes]
    names = ",\n".join(f'    "{c}"' for c in classes)
    return (f'"""Heritage Themes for Pygments: one style for each theme, registered under its name in the\n'
            f'pygments.styles entry point, for example "{name(themes[0][0])}", and importable from here by class\n'
            f'name, for example {classes[0]}.\n"""\n'
            f"from pygments.style import Style\n"
            f"from pygments.token import {', '.join(IMPORTS)}\n\n"
            f"__all__ = [\n{names},\n]\n\n\n" + "\n\n\n".join(style_class(t, source) for t, source in themes) + "\n")


def entry_points(themes):
    """entry_points.txt: each style's name, as Pygments looks it up, and the class that implements it."""
    lines = ["[pygments.styles]"] + [f"{name(t)} = {MODULE}:{class_name(t)}" for t in themes]
    return "\n".join(lines) + "\n"


def wheel_name(version):
    return f"{DISTRIBUTION.replace('-', '_')}-{version}-py3-none-any.whl"


def metadata(version, vendor_url, description):
    """The wheel's METADATA: the project's name, its requirements and its description."""
    headers = ["Metadata-Version: 2.1", f"Name: {DISTRIBUTION}", f"Version: {version}",
               "Summary: Heritage Themes for Pygments", f"Home-page: {vendor_url}", f"Author: {VENDOR}",
               "License: MIT", "Keywords: pygments,syntax highlighting,colour scheme,theme",
               "Classifier: Environment :: Plugins", "Classifier: Intended Audience :: Developers",
               "Classifier: License :: OSI Approved :: MIT License", "Classifier: Programming Language :: Python :: 3",
               "Classifier: Topic :: Software Development :: Documentation",
               "Classifier: Topic :: Text Processing :: Markup", f"Project-URL: Issues, {vendor_url}/issues",
               f"Requires-Python: >={PYTHON}", f"Requires-Dist: Pygments>={PYGMENTS}",
               "Description-Content-Type: text/markdown"]
    return "\n".join(headers) + "\n\n" + description


def wheel(themes, version, vendor_url, description, licence):
    """The wheel as bytes. themes is a list of (theme dict, URL of the family's folder)."""
    return pack(DISTRIBUTION, version, {f"{MODULE}.py": module(themes).encode("utf-8")},
                metadata(version, vendor_url, description), licence,
                {"entry_points.txt": entry_points([t for t, _ in themes]).encode("utf-8")})


def styles(p):
    """Element → dict(fg, bg) as #RRGGBB, for the build's contrast check: each token type's colour on the background
    and on the highlighted line."""
    out = {}
    for token, role, font in rules(p):
        out[token] = dict(fg="#" + p[role], bg="#" + p["bg"])
        out[f"{token} on a highlighted line"] = dict(fg="#" + p[role], bg="#" + p["caretRow"])
    return out
