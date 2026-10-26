"""Xcode themes generated from a palette: an .xcworkspacecolortheme for Xcode 27 and later, an .xccolortheme for
earlier releases.

Xcode looks for a user's themes in ~/Library/Developer/Xcode/UserData/FontAndColorThemes. Xcode 27 lists each
.xcworkspacecolortheme there by its file name under Settings > Appearance > Theme. Such a theme is a JSON recipe
(DVTWorkspaceThemeRecipe): the editor background, which Xcode 27 also draws its toolbar, jump bar and status bar in;
light or dark; the palette's primary and secondary tints, which colour the rest of the interface; and colour overrides
for the syntax roles, the selection, current line, caret and invisibles (RECIPE). Colours are Oklab in polar form
(lightness, chroma, hue in radians) in the sRGB gamut. Fonts are a setting of Xcode 27, not of a theme. Xcode refers to
a theme by a name-based UUID of its file name (recipe_id), which scripts/xcode/screen.py selects themes by. Xcode 27
lists an .xccolortheme only to import it, which changes its colours.

Xcode 26 and earlier list each .xccolortheme by its file name in Settings under Themes. Such a theme is a property list
that sets the colours and fonts of the source editor, the console and the documentation markup that Xcode renders, and
the colours of the markers in the editor's scroll bar; Xcode draws the rest of its window in the colours of the macOS
appearance. xcode.json lists the keys that Xcode's own Default themes set, and the syntax node types among them with
the names that Xcode's settings show; scripts/xcode/keys.py writes it from an installed Xcode. A theme sets exactly
those keys, so no colour of Xcode's default theme shows through, and a key that no rule covers fails the build. A
colour is "red green blue alpha" in sRGB, each from 0 to 1, and a font "<PostScript name> - <size>": SF Mono, which
Xcode bundles, at the weight and size of Xcode's Default themes, while the markup keeps the system fonts that those
themes give it. Xcode ignores the font of most identifier kinds ("font": false in xcode.json).

In both, each key takes the palette role that the other targets give the same construct. Xcode tells apart the
identifiers of the project and those of the SDK ("Other"), which the other targets do not, so both take one role.
"""
import json, math, os, plistlib, re, uuid

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "xcode.json")
with open(DATA, encoding="utf-8") as f:
    MODEL = json.load(f)

FONT_SIZE = 12.0  # as Xcode's Default (Dark) and Default (Light) set it
FONT = {"": "SFMono-Medium", "bold": "SFMono-Bold", "italic": "SFMono-MediumItalic",
        "bold italic": "SFMono-BoldItalic"}
LINE_SPACING = 1.1  # Xcode's default line spacing
# "kw" stands for the keyword font: bold where the palette's keywords are bold.
KW = "kw"
# xcode.syntax.<key>: (role, font), in the order of Xcode's settings.
SYNTAX = {
    "plain": ("fg", ""),
    "comment": ("comment", "italic"),
    "comment.doc": ("doc", "italic"),
    "comment.doc.keyword": ("docTag", "bold italic"),
    "markup.code": ("docTag", ""),  # code in documentation markup, as IntelliJ's DEFAULT_DOC_MARKUP
    "markup.aside.kind": ("docTag", "bold"),  # "- Note:", "- Parameter:" in documentation markup
    "mark": ("todo", "bold italic"),  # MARK:, TODO: and FIXME: comments
    "string": ("string", ""),
    "character": ("string", ""),
    "number": ("number", ""),
    "keyword": ("keyword", KW),
    "preprocessor": ("keyword", KW),
    "url": ("azure", ""),
    "attribute": ("annotation", ""),
    "declaration.type": ("type", ""),
    "declaration.other": ("method", "bold"),  # the names of functions, properties and variables where declared
    "identifier.class": ("type", ""),
    "identifier.class.system": ("type", ""),
    "identifier.type": ("type", ""),
    "identifier.type.system": ("type", ""),
    "identifier.function": ("call", ""),
    "identifier.function.system": ("call", ""),
    "identifier.variable": ("field", ""),
    "identifier.variable.system": ("field", ""),
    "identifier.constant": ("constant", ""),
    "identifier.constant.system": ("constant", ""),
    "identifier.macro": ("annotation", ""),
    "identifier.macro.system": ("annotation", ""),
}
# Text colours of the console, which is drawn on bgTool as the other targets draw their consoles and terminals, and
# their fonts, in the weights of Xcode's Default themes. The colours are those that read at 4.5:1 on bgTool in every
# palette: what the user types takes the terminal green.
CONSOLE = {
    "DVTConsoleDebuggerInputText": ("ansiGreen", "bold"),
    "DVTConsoleDebuggerOutputText": ("fg", ""),
    "DVTConsoleDebuggerPromptText": ("muted", "bold"),
    "DVTConsoleExectuableInputText": ("ansiGreen", ""),  # Xcode's own spelling
    "DVTConsoleExectuableOutputText": ("fg", "bold"),
}
# Documentation markup, rendered in playgrounds and Quick Help on the editor background: (colour role, font).
MARKUP = {
    "Normal": ("fg", ".AppleSystemUIFont - 10.0"),
    "Emphasis": ("fg", ".AppleSystemUIFontItalic - 10.0"),
    "Strong": ("fg", ".AppleSystemUIFontBold - 10.0"),
    "Link": ("azure", ".AppleSystemUIFont - 10.0"),
    "InlineCode": ("string", None),
    "PrimaryHeading": ("method", ".AppleSystemUIFont - 24.0"),  # headings take the declaration role
    "SecondaryHeading": ("method", ".AppleSystemUIFont - 18.0"),
    "OtherHeading": ("method", ".AppleSystemUIFont - 14.0"),
}
MARKUP_CODE_FONT = "SFMono-Regular - 10.0"
# Markers in the editor's scroll bar. Breakpoints and analyser results are blue and runtime issues purple in Xcode,
# whose gutter draws breakpoints in the system blue; the terminal colours keep those hues.
MARKERS = {
    "Error": "error", "Warning": "warning", "Analyzer": "ansiBlue", "RuntimeIssue": "ansiMagenta",
    "Breakpoint": "ansiBlue", "Diff": "modified", "DiffConflict": "gold",
}
# The interface tints of a recipe: Xcode's settings call primary the Foreground and secondary the Background of the
# palette. They take the accent that the other targets give buttons and badges, and the editor background.
PRIMARY, SECONDARY = "red", "bg"
HEX = re.compile(r"[0-9A-F]{6}")
COLOUR = re.compile(r"(0|1|0\.\d{1,6}) (0|1|0\.\d{1,6}) (0|1|0\.\d{1,6}) 1")


def colour(hex_colour):
    """The Xcode colour for a six-digit hex colour, opaque."""
    channels = (int(hex_colour[i:i + 2], 16) / 255 for i in (0, 2, 4))
    return " ".join(f"{c:.6f}".rstrip("0").rstrip(".") for c in channels) + " 1"


def hex_colour(value):
    """The six-digit hex colour of an opaque Xcode colour, the inverse of colour()."""
    match = COLOUR.fullmatch(value)
    if not match:
        raise ValueError(f"{value!r} is not an opaque Xcode colour")
    return "".join(f"{round(float(c) * 255):02X}" for c in match.groups())


def font(p, style):
    """The Xcode font for a style of SYNTAX or CONSOLE, with "kw" as the palette's keyword font."""
    if style == KW:
        style = "bold" if p.get("kwBold", not p["dark"]) else ""
    return f"{FONT[style]} - {FONT_SIZE:.1f}"


def roles(p):
    """Every colour key of the theme to its palette role, and the text keys to the background role they are drawn on,
    for the contrast check: (colours, text) with text as {key: background role}."""
    colours = {
        "DVTSourceTextBackground": "bg", "DVTSourceTextCurrentLineHighlightColor": "caretRow",
        "DVTSourceTextInsertionPointColor": "caret", "DVTSourceTextSelectionColor": "selection",
        "DVTSourceTextInvisiblesColor": "guide", "DVTSourceTextBlockDimBackgroundColor": "muted",
        "DVTDebuggerInstructionPointerColor": "diffMod",
        "DVTConsoleTextBackgroundColor": "bgTool", "DVTConsoleTextSelectionColor": "selection",
        "DVTConsoleTextInsertionPointColor": "caret",
        "DVTMarkupTextBackgroundColor": "bg", "DVTMarkupTextBorderColor": "border",
        **{f"{key}Color": role for key, (role, _) in CONSOLE.items()},
        **{f"DVTMarkupText{key}Color": role for key, (role, _) in MARKUP.items()},
        **{f"DVTScrollbarMarker{key}Color": role for key, role in MARKERS.items()},
    }
    text = {**{f"{key}Color": "bgTool" for key in CONSOLE},
            **{f"DVTMarkupText{key}Color": "bg" for key in MARKUP}}
    return colours, text


def theme(p):
    """The .xccolortheme property list for a palette, as a dict."""
    r = dict(p, caret=p.get("caret", p["gold"]))
    colours, _ = roles(p)
    out = {key: colour(r[role]) for key, role in colours.items()}
    out.update({f"{key}Font": font(p, style) for key, (_, style) in CONSOLE.items()})
    out.update({f"DVTMarkupText{key}Font": face for key, (_, face) in MARKUP.items() if face})
    out["DVTMarkupTextCodeFont"] = MARKUP_CODE_FONT
    out["DVTSourceTextSyntaxColors"] = {f"xcode.syntax.{key}": colour(r[role]) for key, (role, _) in SYNTAX.items()}
    out["DVTSourceTextSyntaxFonts"] = {f"xcode.syntax.{key}": font(p, style) for key, (_, style) in SYNTAX.items()}
    out["DVTFontAndColorVersion"] = 1
    out["DVTLineSpacing"] = LINE_SPACING
    return out


def check(t):
    """Raises ValueError when the theme t, a dict as theme() returns, does not set exactly the keys of xcode.json."""
    syntax = [node["key"] for node in MODEL["syntax"]]
    for found, expected, what in ((t, MODEL["keys"], "keys"),
                                  (t["DVTSourceTextSyntaxColors"], syntax, "syntax colours"),
                                  (t["DVTSourceTextSyntaxFonts"], syntax, "syntax fonts")):
        missing, unknown = sorted(set(expected) - set(found)), sorted(set(found) - set(expected))
        if missing or unknown:
            raise ValueError(f"the {what} differ from xcode.json: missing {missing}, unknown {unknown}")


def document(p):
    """The .xccolortheme file for a palette: an XML property list with sorted keys, as Xcode writes one."""
    t = theme(p)
    check(t)
    return plistlib.dumps(t, sort_keys=True)


# The namespace of the name-based UUID by which Xcode 27 refers to a theme in its folder: uuid5 of the file name
# without its extension (DVTWorkspaceSavedRecipeStore).
RECIPE_NAMESPACE = uuid.UUID("B1FE9A0C-7E4D-4D5E-9C5F-1D7B2A0E63A1")
# palette.colorOverrides of a recipe: key: (kind, role). A "color" is opaque; a "colorWithOpacity" is a background
# that Xcode draws under text.
RECIPE = {
    "plainText": ("color", "fg"),
    "keyword": ("color", "keyword"),
    "keyword.attribute": ("color", "annotation"),
    "preprocessor": ("color", "keyword"),
    "preprocessor.macro": ("color", "annotation"),
    "preprocessor.macroSystem": ("color", "annotation"),
    "string": ("color", "string"),
    "string.regex": ("color", "string"),
    "number": ("color", "number"),
    "number.character": ("color", "string"),
    "link": ("color", "azure"),
    "comment": ("color", "comment"),
    "commentEmphasized": ("color", "todo"),  # MARK:, TODO: and FIXME: comments
    "markdown": ("color", "doc"),  # documentation comments
    "markdownEmphasized": ("color", "docTag"),  # their keywords, such as "- Parameter"
    "typeDeclaration": ("color", "type"),
    "memberDeclaration": ("color", "method"),  # the names of functions, properties and variables where declared
    "projectType": ("color", "type"),
    "projectType.class": ("color", "type"),
    "projectType.type": ("color", "type"),
    "otherType": ("color", "type"),
    "otherType.class": ("color", "type"),
    "otherType.type": ("color", "type"),
    "projectMember": ("color", "call"),
    "projectMember.function": ("color", "call"),
    "projectMember.constant": ("color", "constant"),
    "projectMember.variable": ("color", "field"),
    "otherMember": ("color", "call"),
    "otherMember.function": ("color", "call"),
    "otherMember.constant": ("color", "constant"),
    "otherMember.variable": ("color", "field"),
    "selectedTextBackgroundColor": ("colorWithOpacity", "selection"),
    "currentLineHighlight": ("colorWithOpacity", "caretRow"),
    "insertionPointColor": ("color", "caret"),
    "invisibles": ("color", "guide"),
}


def oklch(hex_colour):
    """(lightness, chroma, hue in radians from 0 to 2π) of a six-digit sRGB hex colour in Oklab's polar form, which
    Xcode 27 stores colours in. The hue of a grey is 0."""
    def linear(c):
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (linear(int(hex_colour[i:i + 2], 16) / 255) for i in (0, 2, 4))
    l, m, s = (math.copysign(abs(x) ** (1 / 3), x) for x in (
        0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b,
        0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b,
        0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b))
    lightness = 0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s
    a = 1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s
    b_ = 0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s
    chroma = math.hypot(a, b_)
    return lightness, chroma, math.atan2(b_, a) % (2 * math.pi) if chroma > 1e-9 else 0.0


def srgb(lightness, chroma, hue):
    """The six-digit sRGB hex colour of an Oklab colour in polar form, the inverse of oklch()."""
    a, b = chroma * math.cos(hue), chroma * math.sin(hue)
    l, m, s = (x ** 3 for x in (lightness + 0.3963377774 * a + 0.2158037573 * b,
                                lightness - 0.1055613458 * a - 0.0638541728 * b,
                                lightness - 0.0894841775 * a - 1.2914855480 * b))
    channels = (4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
                -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
                -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s)
    def gamma(c):
        c = min(max(c, 0.0), 1.0)
        return 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055
    return "".join(f"{round(gamma(c) * 255):02X}" for c in channels)


def recipe_colour(hex_colour):
    """A recipe colour for a six-digit sRGB hex colour, opaque."""
    lightness, chroma, hue = oklch(hex_colour)
    return {"chroma": {"exact": chroma}, "gamut": "sRGB", "hue": {"radians": hue}, "lightness": {"exact": lightness},
            "opacity": 1}


def recipe(p):
    """The Xcode 27 theme for a palette, as the dict of its .xcworkspacecolortheme file."""
    r = dict(p, caret=p.get("caret", p["gold"]))
    return {"fileVersion": 1, "recipe": {
        "background": {"customColor": recipe_colour(r["bg"])},
        "colorScheme": "dark" if p["dark"] else "light",
        "palette": {
            "colorOverrides": {key: {kind: recipe_colour(r[role])} for key, (kind, role) in RECIPE.items()},
            "primary": {"custom": recipe_colour(r[PRIMARY])},
            "secondary": {"custom": recipe_colour(r[SECONDARY])},
        },
    }, "showsInAllColorSchemes": True}  # as Xcode writes the themes it imports


def recipe_id(name):
    """The UUID by which Xcode 27 refers to the theme in the file of that name, without its extension."""
    return str(uuid.uuid5(RECIPE_NAMESPACE, name)).upper()


def recipe_document(p):
    """The .xcworkspacecolortheme file for a palette: JSON with sorted keys, indented as Xcode writes it."""
    return (json.dumps(recipe(p), indent=2, sort_keys=True, separators=(",", " : ")) + "\n").encode("utf-8")
