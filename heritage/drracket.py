"""DrRacket colour schemes generated from a palette: one Racket package that holds every Heritage theme.

DrRacket reads colour schemes from the `framework:color-schemes` key of the info.rkt file of each installed collection.
A scheme is a hash with a name, whether it is dark (`white-on-black-base?`) and a list of entries: each entry names one
of the colours or styles that DrRacket and its tools register, and gives a colour, and for a style also bold, italic,
underline and a background. DrRacket lists the dark schemes and the light ones apart, under Edit | Preferences | Colors
| Color Schemes, and keeps one choice for its dark mode and one for its light mode.

A scheme colours the definitions and interactions windows: the background, the text, the tokens of Racket's lexer, the
gutter, the matching parentheses, the REPL's values, output and errors, Check Syntax's identifiers, arrows and
highlights, test coverage, the stepper and the error highlights. DrRacket draws its window, toolbar, tabs, menus and
selection with the platform's GTK, Cocoa or Win32 theme, and on Linux also the current line's number, in the selection
colours.

The roles are those that the other products give the matching constructs. Racket's lexer gives every identifier the
symbol style and the head forms of its indentation table, such as define, lambda and let, the keyword style, so names
take the text colour and those forms the keyword colour. Literal numbers, booleans, characters and quote marks are
constants, which take the number colour. `#:` keywords take the constant colour in bold italic, as symbols do in the
Neovim plugin, and `#lang` lines and reader commands the directive colour. Check Syntax colours each identifier as either imported, which takes the
call colour, or lexically bound, which keeps the text colour. The REPL's values, output and errors take the ANSI blue,
magenta and red of the console, in the order of DrRacket's own blue, purple and red.

The package installs from the Racket package catalog, which reads it from a Git repository that holds it at its root.
"""
import re

from .terminals import contrast
from .vscode import mix

PACKAGE = "heritage-themes"  # the package's name in the Racket package catalog, and its collection
PREFIX = "Heritage "  # a scheme's name in DrRacket's list, so that the schemes sit together among other packages'
FONT = ("bold", "italic", "underline")

# name → role of each colour that DrRacket 9 registers, as `PLTSTDERR="info@color-scheme" drracket` logs them at start.
# The backgrounds are those of the matching Neovim and VS Code elements: braceBg behind a parenthesised expression whose
# parenthesis is at the caret, underCaret behind the identifiers bound to the one under the caret, writeCaret, the red
# tint of a write access, behind an error and a failed search, diffConf, the yellow conflict tint, behind a warning,
# diffIns behind a documented identifier and the stepper's redex, diffMod behind its reduct and diffDel behind an unused
# identifier and code that tests did not reach.
COLOURS = {
    "framework:basic-canvas-background": "bg",
    "framework:default-text-color": "fg",
    "framework:misspelled-text-color": "fg",
    "framework:paren-match-color": "braceBg",
    "framework:line-numbers": "lineNo",
    "framework:line-numbers-when-word-wrapping": "lineNo",
    "framework:line-numbers-current-line-number-foreground": "lineNoCaret",
    "framework:line-numbers-current-line-number-background": "caretRow",
    "framework:program-contour-current-location-bar": "selection",
    "framework:disabled-background-color": "bgUi",
    "framework:failed-search-background-color": "writeCaret",
    "framework:warning-background-color": "diffConf",
    "drracket:error-background-highlighting": "writeCaret",
    "drracket:gold-error-background-highlighting": "diffConf",
    "drracket:syncheck:matching-identifiers": "underCaret",
    "drracket:syncheck:document-identifier": "diffIns",
    "drracket:syncheck:unused-identifier": "diffDel",
    "drracket:syncheck:var-arrow": "azure",
    "drracket:syncheck:template-arrow": "ansiMagenta",
    "drracket:syncheck:tail-arrow": "gold",
    "drracket:syncheck:untacked": "bg",
    "stepper:redex-highlight-color": "diffIns",
    "stepper:reduct-highlight-color": "diffMod",
    "stepper:error-color": "ansiRed",
    "stepper:arrow-color": "ansiRed",
}
# The colours that DrRacket paints behind code. It shades the whole expression between matching parentheses and the
# whole of an erroneous or stepped expression, so any style can show on them; each is a highlight().
HIGHLIGHTS = {"framework:paren-match-color", "drracket:error-background-highlighting",
              "drracket:gold-error-background-highlighting", "drracket:syncheck:matching-identifiers",
              "drracket:syncheck:document-identifier", "drracket:syncheck:unused-identifier",
              "stepper:redex-highlight-color", "stepper:reduct-highlight-color"}
# The colours that DrRacket draws text in on the editor's background, and the other backgrounds that it draws text on,
# with the colour of that text. The rest are arrows, bars and the editor's own background.
TEXT_COLOURS = {"framework:default-text-color", "framework:misspelled-text-color",
                "framework:line-numbers-current-line-number-foreground"}
TEXT_ON = {"framework:line-numbers-current-line-number-background":
           "framework:line-numbers-current-line-number-foreground",
           "framework:failed-search-background-color": "framework:default-text-color",
           "framework:disabled-background-color": "framework:default-text-color"}
# The line numbers, which are decorative in every target.
DECORATIVE = {"framework:line-numbers", "framework:line-numbers-when-word-wrapping"}
# The styles that need 3:1 only: comments, as in every target.
LOW_CONTRAST = {"framework:syntax-color:scheme:comment"}
HIGHLIGHT_STEP = 0.01


def keyword_font(p):
    """Keywords are bold in light themes, as in the JetBrains schemes, unless the palette sets kwBold."""
    return ("bold",) if p.get("kwBold", not p["dark"]) else ()


def styles(p):
    """name → (role, font, background role) of each style that DrRacket 9 registers. font is a tuple of FONT."""
    return {
        "framework:syntax-color:scheme:symbol": ("fg", (), None),
        "framework:syntax-color:scheme:keyword": ("keyword", keyword_font(p), None),
        "framework:syntax-color:scheme:comment": ("comment", ("italic",), None),
        "framework:syntax-color:scheme:string": ("string", (), None),
        "framework:syntax-color:scheme:text": ("fg", (), None),
        "framework:syntax-color:scheme:constant": ("number", (), None),
        "framework:syntax-color:scheme:hash-colon-keyword": ("constant", ("bold", "italic"), None),
        "framework:syntax-color:scheme:parenthesis": ("op", (), None),
        "framework:syntax-color:scheme:other": ("directive", (), None),
        "framework:syntax-color:scheme:error": ("ansiRed", ("underline",), None),
        "drracket:read-eval-print-loop:value-color": ("ansiBlue", (), None),
        "drracket:read-eval-print-loop:out-color": ("ansiMagenta", (), None),
        "drracket:read-eval-print-loop:error-color": ("ansiRed", ("italic",), None),
        "drracket:language-name-and-memory-use-at-top-of-interactions": ("muted", (), None),
        "drracket:check-syntax:lexically-bound": ("fg", (), None),
        "drracket:check-syntax:imported": ("call", (), None),
        "drracket:check-syntax:set!d": ("fg", ("underline",), None),
        "drracket:check-syntax:free-variable": ("ansiRed", ("underline",), None),
        "drracket:check-syntax:unused-require": ("muted", (), None),
        "drracket:check-syntax:my-obligation-style-pref": ("ansiRed", (), None),
        "drracket:check-syntax:their-obligation-style-pref": ("ansiGreen", (), None),
        "drracket:check-syntax:unk-obligation-style-pref": ("fg", (), None),
        "drracket:check-syntax:both-obligation-style-pref": ("ansiYellow", (), None),
        "plt:module-language:test-coverage-on": ("fg", (), None),
        "plt:module-language:test-coverage-off": ("fg", (), "diffDel"),
        "plt:htdp:test-coverage-on": ("fg", (), None),
        "plt:htdp:test-coverage-off": ("fg", (), "diffDel"),
    }


def minimums(p):
    """role → the contrast that the colour of each style needs on any background behind code: 4.5:1, 3:1 for
    comments."""
    out = {}
    for key, (role, _, _) in styles(p).items():
        out[role] = max(out.get(role, 0), 3 if key in LOW_CONTRAST else 4.5)
    return out


def highlight(p, role):
    """A background behind code: the editor's background moved towards the palette role by the largest step at which
    every style keeps its contrast. The palette guarantees that contrast on the editor's background and the current
    line only, and DrRacket shades whole expressions, so the role's own colour takes some roles below it."""
    needed = minimums(p)
    for i in range(round(1 / HIGHLIGHT_STEP), -1, -1):
        colour = mix(p["bg"], p[role], i * HIGHLIGHT_STEP)
        if all(contrast(p[r], colour) >= minimum for r, minimum in needed.items()):
            return colour
    raise SystemExit(f"DrRacket {p['name']}: a style is below its contrast on the editor's background")


def name(t):
    """The name of a theme dict from a theme.py in DrRacket's list, for example "Heritage Holi Night"."""
    return PREFIX + t["palette"]["name"]


def entries(p):
    """name → (#RRGGBB, font, background #RRGGBB or None) of every colour and style of a scheme, colours first. A
    colour has no font and no background."""
    out = {key: (highlight(p, role) if key in HIGHLIGHTS else p[role], (), None) for key, role in COLOURS.items()}
    for key, (role, font, background) in styles(p).items():
        out[key] = (p[role], font, highlight(p, background) if background else None)
    return out


def vector(colour):
    """The vector that DrRacket reads as a colour, for example #(23 23 22)."""
    return "#(" + " ".join(str(int(colour[i:i + 2], 16)) for i in (0, 2, 4)) + ")"


def scheme(p, scheme_name):
    """The hash of one colour scheme in info.rkt."""
    lines = []
    for key, (colour, font, background) in entries(p).items():
        props = [vector(colour), *font, *([f"#s(background {vector(background)})"] if background else [])]
        lines.append(f"({key} {' '.join(props)})")
    colours = "\n        ".join(lines)
    return (f"(hash 'name {racket_string(scheme_name)}\n"
            f"      'white-on-black-base? {'#t' if p['dark'] else '#f'}\n"
            f"      'colors\n"
            f"      '({colours}))")


def racket_string(text):
    """A Racket string literal."""
    return '"' + text.replace("\\", "\\\\").replace('"', '\\"') + '"'


def racket_version(version):
    """The version in Racket's form, which drops a trailing .0 after the minor number: 1.15.0 is 1.15."""
    parts = version.split(".")
    while len(parts) > 2 and parts[-1] == "0":
        parts.pop()
    return ".".join(parts)


def info(themes, version, description, source):
    """The package's info.rkt: the collection, the package metadata and every theme's colour scheme. themes is a list
    of (scheme name, palette)."""
    schemes = "\n".join("   " + scheme(p, scheme_name).replace("\n", "\n   ") for scheme_name, p in themes)
    return f""";; Heritage Themes: colour schemes for DrRacket.
;; Generated from {source}; changes here are overwritten.
#lang info

(define collection {racket_string(PACKAGE)})
(define pkg-desc {racket_string(description)})
(define version {racket_string(racket_version(version))})
(define license 'MIT)
(define deps '("base"))

(define framework:color-schemes
  (list
{schemes}))
"""


class Symbol(str):
    """A Racket symbol, as read by read()."""


QUOTE = object()  # a quote mark that read() has met and not yet applied to the datum after it


TOKEN = re.compile(r'\s+|;[^\n]*|#lang [^\n]*|(#s\(|#\(|\(|\)|\'|"(?:[^"\\]|\\.)*"|[^\s()\'";]+)')


def read(text):
    """The top-level forms of a Racket file, for the forms that info.rkt uses: a list is a list, 'x is
    [Symbol("quote"), x], a vector #(...) is a tuple, a prefab #s(...) is ("#s", ...), a string is a str, #t and #f
    are booleans, an integer is an int and any other atom is a Symbol."""
    stack = [[]]
    position = 0
    while position < len(text):
        match = TOKEN.match(text, position)
        if not match:
            raise ValueError(f"cannot read {text[position:position + 20]!r}")
        position, token = match.end(), match[1]
        if token is None:
            continue
        if token in ("(", "#(", "#s("):
            stack.append([token])
            continue
        if token == ")":
            if len(stack) < 2:
                raise ValueError("unbalanced )")
            opener, *items = stack.pop()
            value = items if opener == "(" else tuple(items) if opener == "#(" else ("#s", *items)
        elif token == "'":
            stack[-1].append(QUOTE)
            continue
        elif token.startswith('"'):
            value = re.sub(r"\\(.)", r"\1", token[1:-1])
        elif token in ("#t", "#f"):
            value = token == "#t"
        elif re.fullmatch(r"-?\d+", token):
            value = int(token)
        else:
            value = Symbol(token)
        while stack[-1] and stack[-1][-1] is QUOTE:
            stack[-1].pop()
            value = [Symbol("quote"), value]
        stack[-1].append(value)
    if len(stack) != 1 or QUOTE in stack[0]:
        raise ValueError("unbalanced ( or a quote mark without a datum")
    return stack[0]


def unquote(value):
    """The datum of a quoted form."""
    if isinstance(value, list) and len(value) == 2 and value[0] == "quote":
        return value[1]
    raise ValueError(f"expected a quoted datum, got {value!r}")


def colour(value):
    """The #RRGGBB, without #, of a colour vector."""
    if not (isinstance(value, tuple) and len(value) == 3 and all(isinstance(v, int) and 0 <= v <= 255 for v in value)):
        raise ValueError(f"{value!r} is not a colour vector of three bytes")
    return "".join(f"{v:02X}" for v in value)


def parse(text):
    """(definitions, schemes) of an info.rkt: definitions is name → value of each define but the schemes, and schemes is
    scheme name → (dark, name → (#RRGGBB, font, background #RRGGBB or None)), in the form of entries()."""
    definitions, schemes = {}, {}
    for form in read(text):
        if not (isinstance(form, list) and len(form) == 3 and form[0] == "define" and isinstance(form[1], Symbol)):
            raise ValueError(f"expected (define name value), got {form!r}")
        if form[1] != "framework:color-schemes":
            definitions[str(form[1])] = form[2]
            continue
        if not (isinstance(form[2], list) and form[2][0] == "list"):
            raise ValueError("framework:color-schemes is not a (list ...)")
        for item in form[2][1:]:
            if not (isinstance(item, list) and item[0] == "hash" and len(item) % 2 == 1):
                raise ValueError(f"expected (hash key value ...), got {item!r}")
            fields = {unquote(k): v for k, v in zip(item[1::2], item[2::2])}
            if set(fields) != {"name", "white-on-black-base?", "colors"}:
                raise ValueError(f"a scheme has the keys {sorted(fields)}")
            colours = {}
            for line in unquote(fields["colors"]):
                key, *props = line
                fg, font, background = None, [], None
                for prop in props:
                    if isinstance(prop, Symbol) and prop in FONT:
                        font.append(str(prop))
                    elif isinstance(prop, tuple) and prop[:1] == ("#s",):
                        if len(prop) != 3 or prop[1] != "background":
                            raise ValueError(f"{key}: {prop!r} is not a background")
                        background = colour(prop[2])
                    else:
                        fg = colour(prop)
                if str(key) in colours:
                    raise ValueError(f"{key} is set twice")
                colours[str(key)] = (fg, tuple(font), background)
            schemes[fields["name"]] = (fields["white-on-black-base?"], colours)
    return definitions, schemes
