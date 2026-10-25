"""Visual Studio theme .pkgdef generated from a palette.

A Visual Studio theme is a registry key under $RootKey$\\Themes, named by the theme's GUID, that a .pkgdef file in an
extension writes: the theme's name, the built-in theme it falls back to for a colour it does not set, and per colour
category a "Data" value holding the category's colours. The Data value is the record that Visual Studio's colour
compiler (VsixColorCompiler) writes; encode() and decode() follow the compiler in Microsoft's Theme Converter
(github.com/microsoft/theme-converter-for-vs, ThemeConverter/ColorCompiler).

visualstudio.json lists the colours of Visual Studio's built-in Dark and Light themes, with their values, and the
editor's display items with their defaults; scripts/visualstudio/tokens.py writes it from an installed Visual Studio.
A theme sets every colour of the Fluent categories (FLUENT), which colour the shell of Visual Studio 2026, and of the
editor categories (EDITOR), which colour code and the tool windows that show text, so that no colour of the built-in
theme shows through there; a colour that no rule covers fails the build. Each takes the palette role that the other
targets give the same surface or construct. The legacy categories in LEGACY, which older surfaces still read, follow
the Fluent colours they are closest to.
"""
import base64, functools, hashlib, json, os, re, struct, uuid, zipfile

from .vscode import luminance, mix

# The colour data version that Visual Studio reads.
DATA_VERSION = 11
# __VSCOLORTYPE: a colour is unset, an ARGB value, or Visual Studio's automatic colour (the editor's default text or
# background). The compiler writes a value after the type byte for these and the two that a theme does not use.
CT_INVALID, CT_RAW, CT_COLORINDEX, CT_SYSCOLOR, CT_AUTOMATIC = 0, 1, 2, 3, 5
VALUED = {CT_RAW, CT_COLORINDEX, CT_SYSCOLOR, CT_AUTOMATIC}
# The built-in themes that a Heritage theme falls back to, by palette["dark"].
DARK, LIGHT = "{1ded0138-47ce-435e-84ef-9ec1f439b749}", "{de3dbbcd-f642-433c-8353-8f1df4370aba}"
FALLBACK = {True: DARK, False: LIGHT}
BOM = "\ufeff"  # the colour compiler writes .pkgdef files as UTF-8 with a byte order mark


def swap(value):
    """0xAARRGGBB as 0xAABBGGRR and back: a raw colour is stored as the Windows COLORREF with alpha on top."""
    return (value & 0xFF00FF00) | (value & 0xFF) << 16 | (value >> 16 & 0xFF)


def encode(category, colours):
    """The Data value for a category: its GUID and colours as (name, background, foreground), each colour None or
    (type, value) with value eight hex digits: "AARRGGBB" for CT_RAW, the stored number for the other types."""
    body = struct.pack("<i", 1) + uuid.UUID(category).bytes_le + struct.pack("<i", len(colours))
    for name, background, foreground in colours:
        data = name.encode("utf-8")
        body += struct.pack("<i", len(data)) + data
        for colour in (background, foreground):
            if colour is None:
                body += bytes([CT_INVALID])
                continue
            kind, value = colour
            number = int(value, 16)
            body += bytes([kind]) + struct.pack("<I", swap(number) if kind == CT_RAW else number)
    header = struct.pack("<ii", 8 + len(body), DATA_VERSION)
    return header + body


def decode(data):
    """(version, [(category GUID, [(name, background, foreground)])]) for a Data value, the inverse of encode()."""
    size, version = struct.unpack_from("<ii", data, 0)
    if size != len(data):
        raise ValueError(f"colour data of {len(data)} bytes says {size}")
    position, categories = 8, []
    (count,) = struct.unpack_from("<i", data, position)
    position += 4
    for _ in range(count):
        category = str(uuid.UUID(bytes_le=data[position:position + 16]))
        (colour_count,) = struct.unpack_from("<i", data, position + 16)
        position += 20
        colours = []
        for _ in range(colour_count):
            (length,) = struct.unpack_from("<i", data, position)
            name = data[position + 4:position + 4 + length].decode("utf-8")
            position += 4 + length
            pair = []
            for _ in range(2):
                kind = data[position]
                position += 1
                if kind in VALUED:
                    (number,) = struct.unpack_from("<I", data, position)
                    position += 4
                    pair.append((kind, f"{swap(number) if kind == CT_RAW else number:08X}"))
                else:
                    pair.append(None)
            colours.append((name, *pair))
        categories.append((category, colours))
    if position != len(data):
        raise ValueError(f"colour data has {len(data) - position} bytes after its last colour")
    return version, categories


def sections(text):
    """[(key, [(value name, value)])] for the text of a .pkgdef file. A value name is "@" for the default value. A
    value is a str for a string, bytes for hex data and the text after = for any other type, such as dword:00000001.
    Lines starting with // are comments; a line ending in a backslash continues on the next."""
    out = []
    for line in re.sub(r"\\\r?\n\s*", "", text.lstrip(BOM)).splitlines():
        line = line.strip()
        if not line or line.startswith("//"):
            continue
        if line.startswith("["):
            out.append((line[1:-1], []))
            continue
        match = re.fullmatch(r'(@|"[^"]*")\s*=\s*(?:"(.*)"|hex:([0-9a-fA-F,\s]*)|(.*))', line)
        if not match or not out:
            raise ValueError(f"not a .pkgdef value: {line[:80]}")
        name, string, data, other = match.groups()
        value = string if string is not None else bytes.fromhex(re.sub(r"[,\s]", "", data)) if data is not None \
            else other
        out[-1][1].append((name.strip('"'), value))
    return out


def pkgdef(name, guid, fallback, categories, comment):
    """The .pkgdef text for a theme: categories as [(category name, category GUID, colours)], colours as for
    encode()."""
    key = f"$RootKey$\\Themes\\{{{guid}}}"
    lines = [f"// {line}" for line in comment.splitlines()]
    lines += ["", f"[{key}]", f'@="{name}"', f'"Name"="{name}"', f'"FallbackId"="{fallback}"']
    for category, category_guid, colours in categories:
        data = ",".join(f"{b:02x}" for b in encode(category_guid, colours))
        lines += ["", f"[{key}\\{category}]", f'"Data"=hex:{data}']
    return BOM + "\n".join(lines) + "\n"


DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "visualstudio.json")
with open(DATA, encoding="utf-8") as f:
    MODEL = json.load(f)
CATEGORIES = {c["name"]: c for c in MODEL["categories"]}
AUTOMATIC = "automatic"
ARGB = re.compile(r"[0-9A-F]{8}")


def contrast(a, b):
    """The WCAG contrast ratio of two six-digit hex colours."""
    x, y = luminance(a), luminance(b)
    return (max(x, y) + 0.05) / (min(x, y) + 0.05)


def readable(colour, towards, backgrounds, minimum=4.5):
    """colour moved towards another in steps of 5 % until it reads at minimum on every background."""
    for step in range(21):
        candidate = mix(colour, towards, step / 20)
        if all(contrast(candidate, b) >= minimum for b in backgrounds):
            return candidate
    return towards


def roles(p):
    """The palette's colours by role, with the colours derived from them that the rules name:

    white, black  what Fluent's white and black overlays become: the text colour over a dark theme and black under
                  it, the popup surface over a light theme and the text colour under it, so that overlays tint the
                  palette's surfaces as Fluent's tint its greys
    accentText    the button colour moved towards the text colour until it reads as text on every surface
    decorative*   the colour of each Decorative ramp, and its Alt with more contrast
    diff*Word     the changed words in a diff, the line's wash a third of the way to the change colour, as in
                  heritage.vscode
    heat1-5       the profiler's hot lines, washes of the terminal red that deepen with the heat
    """
    r = {k: v for k, v in p.items() if isinstance(v, str) and re.fullmatch(r"[0-9A-F]{6}", v)}
    r["caret"] = p.get("caret", p["gold"])
    r["white"], r["black"] = (p["fg"], "000000") if p["dark"] else (p["surface"], p["fg"])
    r["accentText"] = readable(p["red"], p["fg"], [p[k] for k in ("bg", "bgTool", "bgUi", "surface", "frame")])
    for hue, (role, other, share) in DECORATIVE.items():
        r[f"decorative{hue}"] = mix(r[role], r[other], share)
        r[f"decorative{hue}Alt"] = mix(r[f"decorative{hue}"], p["fg"], 0.3)
    r["diffInsWord"], r["diffDelWord"] = mix(p["diffIns"], p["added"], 0.35), mix(p["diffDel"], p["deleted"], 0.35)
    for i in range(1, 6):
        r[f"heat{i}"] = mix(p["bg"], p["ansiRed"], 0.06 * i)
    return r


def default(colour, p, channel):
    """The value that the built-in theme of the palette's brightness gives a channel of a visualstudio.json colour,
    or that of the other built-in theme when the first does not set the colour."""
    values = colour["dark" if p["dark"] else "light"] or colour["light" if p["dark"] else "dark"]
    return values[channel]


def resolve(spec, r, built_in):
    """(type, value) for a rule's spec: "role" is the role's colour, opaque; "role~" takes the alpha of the built-in
    colour, so that overlays and translucent states keep Fluent's strength; "role@AA" takes alpha AA; "automatic" is
    the editor's own text or background colour."""
    if spec == AUTOMATIC:
        return CT_AUTOMATIC, "00000000"
    if spec.endswith("~"):
        role, alpha = spec[:-1], built_in[:2] if built_in and ARGB.fullmatch(built_in) else "FF"
    elif "@" in spec:
        role, alpha = spec.split("@")
    else:
        role, alpha = spec, "FF"
    return CT_RAW, alpha + r[role]


def overlay(built_in):
    """The spec for a Fluent neutral: a white or black of the built-in theme, or a grey within 16 levels of either,
    which Fluent layers translucent or opaque over its greys; None for another colour."""
    if not built_in or not ARGB.fullmatch(built_in):
        return None
    channels = [int(built_in[i:i + 2], 16) for i in (2, 4, 6)]
    if min(channels) >= 0xF0 and max(channels) - min(channels) <= 0x10:
        return "white~"
    if max(channels) <= 0x10:
        return "black~"
    return None


# Fluent tokens of the shell. Any other token of Shell and ShellInternal is a translucent white or black in the
# built-in theme, which overlay() tints. The accent is the palette's button colour, as the other targets fill default
# buttons, progress bars and the mark of the selected tab with it; state colours are the ANSI colours, which read as
# their hue on every surface.
SHELL = {
    "AccentFillDefault": "red", "AccentFillSecondary": "red~", "AccentFillTertiary": "red~",
    "AccentFillSenary": "red~", "AccentFillAlt": "accentText",
    "AccentTextFillPrimary": "accentText", "AccentTextFillSecondary": "accentText",
    "AccentTextFillTertiary": "accentText", "AccentTextFillDisabled": "disabled",
    "TextOnAccentFillPrimary": "redText", "TextOnAccentFillSecondary": "redText~",
    "TextOnAccentFillDisabled": "disabled",
    # selected text in text boxes, which keeps its colour on the selection
    "AccentFillSelectedTextBackground": "selection", "AccentFillSelectedTextBackgroundSubtle": "selInactive",
    "TextOnAccentFillSelectedText": "fg",
    "TextFillPrimary": "fg", "TextFillSecondary": "muted", "TextFillTertiary": "muted", "TextFillDisabled": "disabled",
    "HyperlinkFillPrimary": "azure", "HyperlinkFillSecondary": "azure", "HyperlinkFillTertiary": "azure~",
    "HyperlinkFillDisabled": "disabled",
    # surfaces, from the window behind everything to the popups on top
    "SolidBackgroundFillBase": "bgUi", "SolidBackgroundFillBaseAlt": "frame", "SolidBackgroundFillSecondary": "bgUi",
    "SolidBackgroundFillTertiary": "bgTool", "SolidBackgroundFillQuaternary": "surface",
    "SolidBackgroundFillQuinary": "surface", "SolidBackgroundFillSenary": "surface",
    "SurfaceBackgroundFillDefault": "surface", "LayerFillDefault": "bgTool~",
    "ControlFillActiveInput": "surface~", "ControlSolidFillDefault": "surface",
    "ControlOnImageFillDefault": "surface~", "ControlOnImageFillDisabled": "surface~",
    "ControlOnImageFillSecondary": "surface", "ControlOnImageFillTertiary": "hover", "SmokeFillInverse": "surface~",
    "CardStrokeDefaultSolid": "border", "CardStrokeDefaultSolidAlt": "border", "DividerStrokeDefault": "border",
    "SurfaceStrokeDefault": "border",
    "FocusStrokeOuter": "gold",
    "SystemFillAttention": "ansiBlue", "SystemFillCaution": "ansiYellow", "SystemFillCritical": "ansiRed",
    "SystemFillSuccess": "ansiGreen", "SystemFillSolidNeutral": "muted",
    "SystemFillAttentionBackground": "diffMod", "SystemFillCautionBackground": "diffConf",
    "SystemFillCriticalBackground": "diffDel", "SystemFillSuccessBackground": "diffIns",
    "SystemFillSolidAttentionBackground": "surface", "SystemFillSolidNeutralBackground": "surface",
}
# The window frame, title bar, caption buttons and status bar. Visual Studio 2026 draws its tool windows and documents
# as islands on the environment background, as the Islands themes of the JetBrains IDEs do on the main window.
SHELL_INTERNAL = {
    "EnvironmentBackground": "frame", "EnvironmentBody": "frame", "EnvironmentBodyText": "fg",
    # the title bar and tabs of a tool window are part of its island
    "EnvironmentHeader": "bgTool", "EnvironmentHeaderInactive": "bgTool",
    "EnvironmentTab": "bgTool", "EnvironmentTabInactive": "bgTool",
    "EnvironmentBorder": "red", "EnvironmentBorderInactive": "border", "EnvironmentLogo": "red",
    "EnvironmentIndicator": "border", "EnvironmentLayeredBackground": "bgTool~",
    # The close button turns the terminal red on hover, with its cross in the editor background, which build.py holds
    # at 4.5:1 against it.
    "CaptionControlCloseFillPrimary": "ansiRed", "CaptionControlCloseFillSecondary": "ansiRed~",
    "CaptionControlCloseTextFillPrimary": "bg", "CaptionControlCloseTextFillSecondary": "bg~",
    # The status bar sits on the frame, as in the other targets. While building it takes the accent; while debugging
    # and loading a solution, the terminal yellow and blue, with text in the editor background.
    "StatusBarBackgroundFillRest": "frame", "StatusBarTextFillRest": "fg", "StatusBarTextFillDisabled": "disabled",
    "StatusBarBackgroundFillBuilding": "red", "StatusBarTextFillBuilding": "redText",
    "StatusBarBackgroundFillDebugging": "ansiYellow", "StatusBarTextFillDebugging": "bg",
    "StatusBarBackgroundFillSolutionLoading": "ansiBlue", "StatusBarTextFillSolutionLoading": "bg",
}
# Popups in the editor: Quick Info, signature help and completion.
EDITOR_OVERRIDE = {
    "PopupBackground": "surface", "PopupBorder": "border", "PopupHyperlink": "azure",
    "PopupSelectedBackground": "selection", "PopupSelectedText": "fg", "PopupShadow": "black~",
    "PopupSubtleText": "muted", "PopupText": "fg",
}
# ANSI colours in the terminal and in tool output. Visual Studio keeps Black and White readable on the theme's
# background, Black as the strongest text and White as a grey, and the bright colours a step further from it.
ANSI = {
    "Black": "fg", "BrightBlack": "fg", "White": "op", "BrightWhite": "muted",
    **{f"{bright}{hue}": f"ansi{hue}" for hue in ("Red", "Green", "Yellow", "Blue", "Magenta", "Cyan")
       for bright in ("", "Bright")},
}
# Decorative colours mark objects apart, such as charts and the tabs of colourised documents: one ramp per hue, a
# solid Primary, a PrimaryAlt with more contrast and translucent steps. Each hue takes the ANSI colour that reads as
# it, or the mix of two for a hue between them: (role, other role, share of the other).
DECORATIVE = {
    "Blue": ("ansiBlue", "ansiBlue", 0), "LightBlue": ("ansiBlue", "white", 0.3),
    "DarkBlue": ("ansiBlue", "black", 0.3),
    "Red": ("ansiRed", "ansiRed", 0), "DarkRed": ("ansiRed", "black", 0.3), "Pink": ("ansiMagenta", "ansiMagenta", 0),
    "Orange": ("ansiRed", "ansiYellow", 0.5), "Yellow": ("ansiYellow", "ansiYellow", 0),
    "Green": ("ansiGreen", "ansiGreen", 0), "Teal": ("ansiCyan", "ansiCyan", 0),
    "Purple": ("ansiMagenta", "ansiBlue", 0.5), "Grape": ("ansiMagenta", "ansiBlue", 0.3),
    "Lavender": ("ansiMagenta", "ansiBlue", 0.7),
    "Grey": ("disabled", "disabled", 0), "Neutral": ("op", "op", 0),
}
DECORATIVE_NAME = re.compile(r"(?P<hue>[A-Z][a-z]+(?:[A-Z][a-z]+)??)(?P<step>Primary(?:Alt)?|Secondary|Tertiary|"
                             r"Quaternary|Quinary|Senary|Septenary)")


def decorative(name, built_in):
    """The spec for a Decorative colour: the ramp's colour, which roles() derives, at the built-in step's alpha."""
    match = DECORATIVE_NAME.fullmatch(name)
    if not match or match["hue"] not in DECORATIVE:
        return None
    return overlay(built_in) or f"decorative{match['hue']}{'Alt' if match['step'] == 'PrimaryAlt' else ''}~"


# Legacy categories: the feature-specific tokens of the themes before Visual Studio 2026, which its older surfaces still
# read. These cover the shell and the controls that every feature shares; designers and diagnostics tools keep the
# built-in theme's colours, which mark data rather than surfaces.
LEGACY = ("Environment", "CommonControls", "CommonDocument", "CommonDocumentCard", "SearchControl", "UserNotifications",
          "ThemedDialog", "ThemedUtilityDialog", "ThemedAcceleratedDialog", "UnthemedDialog", "TreeView", "Header",
          "InfoBar", "NotificationBubble", "InformationBadge", "NavigateTo", "VSSearch", "Find", "ProgressBar",
          "ListViewGrid", "DetailsView", "NewProjectDialog", "StartPage", "UserInformation", "Chat", "AI",
          "VersionControl", "TeamExplorer")
# The base that the built-in themes lay their translucent colours on (their SolidBackgroundFillBase), to compare
# colours as they show.
SHOWN_ON = {"dark": "202020", "light": "F3F3F3"}


def shown(value, base):
    """An "AARRGGBB" value as it shows over base, as (r, g, b), or None for a colour that is not raw."""
    if not value or not ARGB.fullmatch(value):
        return None
    alpha = int(value[:2], 16) / 255
    return tuple(round(int(value[i:i + 2], 16) * alpha + int(base[i - 2:i], 16) * (1 - alpha)) for i in (2, 4, 6))


def fluent_candidates():
    """[(category, name, channel, {theme: shown colour})] for the Fluent colours that legacy colours map to: every raw
    colour of the Fluent categories except the Decorative greys, which mark data, not surfaces."""
    out = []
    for category in MODEL["categories"]:
        if category["name"] not in FLUENT:
            continue
        for colour in category["colours"]:
            if category["name"] == "Decorative" and colour["name"].startswith(("Grey", "Neutral")):
                continue
            for channel in (0, 1):
                looks = {t: shown((colour[t] or [None, None])[channel], SHOWN_ON[t]) for t in SHOWN_ON}
                if all(looks.values()):
                    out.append((category["name"], colour["name"], channel, looks))
    return out


@functools.cache
def nearest_fluent():
    """{(category, name, channel): (Fluent category, name, channel)} for each raw colour of the LEGACY categories: the
    Fluent colour that shows closest to it in the built-in Dark and Light themes together. A legacy colour then takes
    the palette colour that the Fluent one takes, so the older surfaces follow the theme as the new ones do."""
    candidates = fluent_candidates()
    out = {}
    for category in MODEL["categories"]:
        if category["name"] not in LEGACY:
            continue
        for colour in category["colours"]:
            for channel in (0, 1):
                looks = {t: shown((colour[t] or [None, None])[channel], SHOWN_ON[t]) for t in SHOWN_ON}
                looks = {t: c for t, c in looks.items() if c}
                if not looks:
                    continue
                def distance(candidate):
                    return sum(sum((a - b) ** 2 for a, b in zip(c, candidate[3][t])) ** 0.5 for t, c in looks.items())
                best = min(candidates, key=distance)
                out[category["name"], colour["name"], channel] = best[:3]
    return out



def legacy_colour(category, colour, channel, p, r, built_in):
    """(type, value) for a channel of a legacy colour, or None to leave the built-in theme's: the palette colour of its
    nearest Fluent colour, made opaque on the palette's window colour where the legacy colour is opaque, or with the
    legacy colour's alpha where it is translucent."""
    target = nearest_fluent().get((category, colour["name"], channel))
    if target is None:
        return None
    fluent_category, fluent_name, fluent_channel = target
    fluent = next(c for c in CATEGORIES[fluent_category]["colours"] if c["name"] == fluent_name)
    fluent_built_in = default(fluent, p, fluent_channel)
    kind, value = resolve(shell_rule(fluent_category, fluent_name, r, fluent_built_in), r, fluent_built_in)
    if built_in.startswith("FF"):
        return kind, "FF" + "".join(f"{v:02X}" for v in shown(value, p["bgUi"]))
    return kind, built_in[:2] + value[2:]


def shell_rule(category, name, r, built_in):
    """The spec for a colour of a Fluent category, or None when no rule covers it."""
    if category == "Decorative":
        return decorative(name, built_in)
    table = {"Shell": SHELL, "ShellInternal": SHELL_INTERNAL, "EditorOverride": EDITOR_OVERRIDE, "Ansi": ANSI}[category]
    return table.get(name) or overlay(built_in)


FLUENT = ("Shell", "ShellInternal", "Decorative", "EditorOverride", "Ansi")

# Editor colours: (names, background, foreground) per category, names a regular expression that matches the whole
# name. The first rule that matches a name sets it; a channel without a spec keeps the built-in "automatic", the
# editor's own text or background colour. Code takes the roles that heritage.vscode gives the same constructs; marks
# laid over code take the palette's washes, so the code keeps its colours on them.
CODE = [
    # text and the editor around it
    (r"Plain Text", "bg", "fg"),
    (r"Selected Text", "selection", None), (r"Inactive Selected Text", "selInactive", None),
    (r"Matched Selected Text", "underCaret", None),
    (r"Line Number", "bg", "lineNo"), (r"Selected Line Number", "bg", "lineNoCaret"),
    (r"Visible Whitespace|Word Wrap Glyph", "bg", "guide"), (r"Indicator Margin|Suggestion Margin", "bg", "fg"),
    (r"CurrentLineActiveFormat", "caretRow", "caretRow"), (r"Block Structure Adornments", "guide", None),
    (r"outlining\.chevron\.(collapsed|expanded)", "bg", "muted"), (r"outlining\.verticalrule", None, "guide"),
    (r"outlining\.collapsehintadornment", "surface", "fg"),
    (r"StickyScroll Background", "bg", None),
    (r"(inline|inlay) hints( parameter| type)?|CppInlineHintsFormat", "caretRow", "muted"),
    (r"LightBulb Action Display Text Suffix|hinted suggestion", None, "muted"),
    (r"urlformat|NavigableSymbolFormat", None, "azure"),
    # code
    (r"Keyword|keyword - control|C/C\+\+ User Keywords|Preprocessor Keyword|Cpp(Control)?KeywordSyntacticTokenFormat|"
     r"CppNewDeleteSemanticTokenFormat|XSLT Keyword|Markup Node", None, "keyword"),
    (r"((HTML|XML|XAML|CSS) )?Comment|regex - comment", None, "comment"),
    (r"XML Doc Comment|XML Doc Tag|xml doc comment - (text|delimiter|comment|entity reference|processing instruction|"
     r"cdata section|attribute quotes|attribute value)|XmlDoc(Comment|Tag)ClassificationFormat", None, "doc"),
    (r"xml doc comment - (name|attribute name)|XML Doc Attribute|XmlDocAttributeClassificationFormat", None, "docTag"),
    (r"String|String\(C# @ Verbatim\)|string - verbatim|regex - text|regex - self escaped character|"
     r"CppString(Delimiter)?CharacterSyntacticTokenFormat|CppUDLStringSemanticTokenFormat", None, "string"),
    (r"string - escape character|regex - other escape|CppStringEscapeCharacterSyntacticTokenFormat|"
     r"regex - (anchor|quantifier|grouping|alternation)", None, "gold"),
    (r"regex - character class", None, "number"),
    (r"Number|CppUDLNumberSemanticTokenFormat", None, "number"),
    (r"Operator|punctuation|operator - overloaded|Cpp(Member)?OperatorSemanticTokenFormat|"
     r"brace pair level (one|two|three)", None, "op"),
    (r"Identifier|Text|Literal|local name|CppLocalVariableSemanticTokenFormat|CppUDLRawSemanticTokenFormat|"
     r"CppNamespaceSemanticTokenFormat|CppGlobalVariableSemanticTokenFormat|preprocessor text", None, "fg"),
    (r"Excluded Code|VBExcludedCodeClassificationFormat|Stale Code", None, "muted"),
    (r"User Types(\((Value types|Delegates|Enums|Interfaces)\))?|Type|class name|struct name|delegate name|"
     r"module name|enum name|interface name|VBUserTypeClassificationFormat|"
     r"Cpp(ClassTemplate|Enum|GenericType|RefType|Type|ValueType)SemanticTokenFormat", "bg", "type"),
    (r"User Types\(Type parameters\)|type parameter name", None, "typeParam"),
    (r"Method|method name|extension method name|"
     r"Cpp(Function|FunctionTemplate|MemberFunction|StaticMemberFunction)SemanticTokenFormat", None, "call"),
    (r"Cpp(MemberField|StaticMemberField|Property|Event)SemanticTokenFormat", None, "field"),
    (r"parameter name|CppParameterSemanticTokenFormat", None, "param"),
    (r"CppLabelSemanticTokenFormat", None, "label"),
    (r"CppMacroSemanticTokenFormat|CppAttributesSyntacticTokenFormat", None, "annotation"),
    # markup: tags as keywords, attributes as fields and their values as strings, as in heritage.vscode
    (r"(HTML|XML|XAML) (Element Name|Name|Keyword|Tag Delimiter|Delimiter|Operator)|"
     r"Xml(Name|Delimiter)ClassificationFormat|xml literal - (name|delimiter)", None, "keyword"),
    (r"(HTML|XML|XAML) Attribute( Name)?|Markup Attribute|Xml AttributeName|XmlAttributeNameClassificationFormat|"
     r"xml literal - attribute name|XAML Markup Extension Parameter Name", None, "field"),
    (r"(HTML|XML|XAML) Attribute (Value|Quotes)|Markup Attribute Value|"
     r"XmlAttribute(Value|Quotes)ClassificationFormat|xml literal - attribute (value|quotes)|"
     r"(XML|XAML) CData Section|XmlCDataSectionClassificationFormat|xml literal - cdata section|"
     r"XAML Markup Extension Parameter Value", None, "string"),
    (r"(XML|XAML) Text|XmlTextClassificationFormat|xml literal - text", None, "fg"),
    (r"(XML|XAML) Processing Instruction|XmlProcessingInstructionClassificationFormat|"
     r"xml literal - processing instruction", None, "annotation"),
    (r"XAML Markup Extension Class", None, "type"),
    (r"HTML Entity|xml literal - entity reference", None, "gold"),
    (r"XmlCommentClassificationFormat|xml literal - comment", None, "comment"),
    (r"xml literal - embedded expression|XmlEmbeddedExpressionClassificationFormat", "caretRow", "fg"),
    (r"HTML Server-Side Script|Razor ?Code", "caretRow", "fg"),
    (r"RazorDirective|RazorDirectiveAttribute|RazorTransition", "bg", "keyword"),
    (r"Razor(TagHelper|Component)(Element|Attribute)", None, "type"),
    (r"HtmlClientTemplateValueFormatDefinition", None, "annotation"),
    # style sheets: selectors as keywords, properties as fields, values as strings, as in heritage.vscode
    (r"CSS (Keyword|Selector)|(Less|Scss)(Css)?KeywordFormat", None, "keyword"),
    (r"CSS Property Name", None, "field"), (r"CSS (Property|String) Value", None, "string"),
    (r"(Less|Scss)(Css)?Mixin(Declaration|Reference)Format|LessCssNamespaceReferenceFormat", None, "call"),
    (r"(Less|Scss)(Css)?Variable(Declaration|Reference)(Classification)?Format", None, "field"),
    (r"JSON Property Name", None, "field"),
    # SQL
    (r"SQL Operator", None, "op"), (r"SQL String", None, "string"),
    (r"SQL (Stored Procedure|System Function)", None, "call"), (r"SQL System Table", None, "type"),
    (r"SQLCMD Command", "caretRow", "keyword"),
    (r"VBScript (Keyword|Function Block Start)", "bg", "keyword"), (r"VBScript Comment", "bg", "comment"),
    (r"VBScript Operator", "bg", "op"), (r"VBScript Number", "bg", "number"), (r"VBScript String", "bg", "string"),
    (r"VBScript Identifier", "bg", "fg"),
    # diagnostics: squiggles in the palette's diagnostic colours
    (r"Error Message", "error", "error"),  # a squiggle marker, which draws its line in both colours
    (r"syntax error|compiler error|other error|Error|FileLineClassificationFormat|"
     r"Roslyn - Interactive Window Error Output", None, "error"),
    (r"compiler warning", None, "warning"), (r"information|Edit and Continue", None, "weak"),
    (r"inline diagnostics - syntax error", "diffDel", "fg"),
    (r"inline diagnostics - compiler warning", "diffConf", "fg"),
    (r"inline diagnostics - Edit and Continue", "diffMod", "fg"),
    (r"mismatched brace|BidirectionalTextControlCharacter", "bg", "error"),
    (r"Memory Changed|Register Data Changed", None, "ansiRed"), (r"Memory Address|Register NAT", None, "muted"),
    (r"Memory Unreadable", "caretRow", "muted"),
    (r"Roslyn - Interactive Window Output|SourceLineClassificationFormat", None, "fg"),
    (r"InstructionLineClassificationFormat", None, "muted"),
    (r"Symbol(Definition|Line)ClassificationFormat", None, "call"),
    (r"SymbolReferenceClassificationFormat", None, "field"),
    (r"RegularExpressionClassificationFormat", "bg", "string"),
    # highlights laid over code
    (r"brace matching|Brace Matching \(Rectangle\)", "braceBg", None),
    (r"MarkerFormatDefinition/(HighlightedReference|HighlightedDefinition|CppHighlightedDefinition)",
     "underCaret", "fg"),
    (r"MarkerFormatDefinition/HighlightedWrittenReference", "writeCaret", "fg"),
    (r"MarkerFormatDefinition/FindHighlight|Expression Hover Highlight", "searchBg", "fg"),
    (r"MarkerFormatDefinition/ScopeHighlight", "caretRow", "guide"),
    (r"MarkerFormatDefinition/(CommentHighlight|CommentMark)", "selInactive", None),
    (r"Peek Background", "surface", None), (r"Peek Background Unfocused", "bgTool", None),
    (r"Peek Focused Border", None, "gold"), (r"Peek Highlighted Text", "searchBg", None),
    (r"Peek Highlighted Text Unfocused", "selInactive", None), (r"Peek Label Text", None, "fg"),
    (r"Knockout Region", "caretRow", None),
    # the scroll bar's map of the document
    (r"OverviewMarginBackground", "bg", None), (r"OverviewMarginVisible", "guideSel", "guideSel"),
    (r"OverviewMarginCaret", None, "caret"), (r"OverviewMarginCollapsedRegion", "muted", None),
    (r"OverviewMarginScrollButtons", "bg", "muted"), (r"OverviewMarginScrollButtonsMouseOver", "bg", "fg"),
    (r"OverviewMarginScrollButtonsMouseDown", "bg", "gold"),
    (r"MarkerFormatDefinition/SelectedTextInScrollBar", "guideSel", None),
    (r"MarkerFormatDefinition/BookmarkInScrollBar", "gold", None),
    (r"MarkerFormatDefinition/BreakpointInScrollBar", "red", None),
    # changes: the gutter marks and the diff and merge views
    (r"Track Changes before save|Track modifications in documents under source control", "modified", None),
    (r"Track Changes after save|Track additions in documents under source control", "added", None),
    (r"Track deletions in documents under source control", "deleted", None),
    (r"Track reverted changes", "ansiCyan", None),
    (r"deltadiff\.add\.line", "diffIns", None), (r"deltadiff\.remove\.line", "diffDel", None),
    (r"deltadiff\.add\.word", "diffInsWord", "added"), (r"deltadiff\.remove\.word", "diffDelWord", "deleted"),
    (r"deltadiff\.overview\.color", "bg", "border"),
    (r"mergeEditor\.(AcceptedLine|AcceptedSimilarLine)", "diffIns", "fg"),
    (r"mergeEditor\.(ConflictLine|ConflictMismatchLine)", "diffDel", "fg"),
    (r"mergeEditor\.NotAcceptedLine", "bg", "fg"), (r"mergeEditor\.(Conflict)?NegativeSpace", "caretRow", "fg"),
    (r"mergeEditor\.DeletedNegativeSpace", "diffDel", "fg"), (r"mergeEditor\.MarginIndicator", "modified", "fg"),
    (r"mergeEditor\.ConflictMarginIndicator", "deleted", "fg"), (r"mergeEditor\.SelectionBox", "selection", "fg"),
    (r"mergeEditor\.WordDiffBoxAccepted", "diffInsWord", "black~"),
    (r"mergeEditor\.WordDiffBoxConflict", "diffDelWord", "black~"),
    # debugging: the current statement in the debugger's wash, breakpoints in the button colour, as in heritage.vscode
    (r"Current Statement( \(new context\)| \(historical mode\))?|RoslynActiveStatementTag", "diffConf", "fg"),
    (r"Call Return( \(historical mode\))?", "diffMod", "fg"),
    (r"Breakpoint( - (Advanced|Dependent|Mapped|Temporary))? \((Enabled|Warning)\)", "diffDel", "fg"),
    (r"Breakpoint( - (Advanced|Dependent|Mapped|Temporary))? \(Error\)", "diffDel", "error"),
    (r"Breakpoint( - (Dependent|Temporary))? \(Disabled\)|Breakpoint - Selected", None, "muted"),
    (r"Tracepoint( - (Advanced|Dependent|Mapped))? \((Enabled|Disabled)\)", None, "gold"),
    (r"Tracepoint( - (Advanced|Dependent|Mapped))? \(Error\)", None, "error"),
    (r"Tracepoint( - (Advanced|Dependent|Mapped))? \(Warning\)", None, "warning"),
    # code review, analysis, rename, snippets and the other marks of the language services
    (r"CodeReview\.(Selected|Unselected)Comment\.AnchorPoint", "diffMod", "azure"),
    (r"CodeAnalysis(CurrentStatement|KeyEvent|Warning|LineTrace)Selection", "diffConf", "diffConf"),
    (r"RenameTrackingTag", None, "muted"), (r"RoslynRenameFixupTag", None, "ansiGreen"),
    (r"RoslynRenameFieldBackgroundAndBorderTag", "selInactive", "border"),
    (r"RoslynPreviewWarningTag", None, "warning"),
    (r"roslyn test code", "caretRow", None), (r"roslyn test code markdown", None, "ansiMagenta"),
    (r"Test Summary - (Default|Header|Label|No Source)", None, "fg"),
    (r"Test Summary - (Diagnostic|Stack)", None, "ansiRed"),
    (r"Bookmark|Visual Basic Read Only Marker", "diffConf", None), (r"Read-Only Region", "caretRow", "fg"),
    (r"Code Snippet Field", "selInactive", None), (r"Code Snippet Field \(Selected\)", "selection", "fg"),
    (r"Code Snippet Dependent Field|Refactoring Dependent Field", None, "muted"),
    (r"Refactoring Background|Definition Window Background", "bg", "fg"),
    (r"Refactoring Current Field", "underCaret", "fg"), (r"Definition Window Current Match", None, "gold"),
    (r"Smart Tag", None, "gold"), (r"Task List Shortcut", "selInactive", "fg"),
    (r"Warning Lines Path", "diffConf", "fg"), (r"Current List Location", "selection", "fg"),
    (r"Coverage Touched Area", "diffIns", "fg"), (r"Coverage Partially Touched Area", "diffConf", "fg"),
    (r"Coverage Not Touched Area", "diffDel", "fg"),
    *((f"Sampling Hot Line {i}", f"heat{i}", "fg") for i in range(1, 6)),
    # Display items that the language services define in code, with no colour in the built-in themes' .pkgdef files.
    # C#, Visual Basic and C++ symbols, as heritage.vscode colours the same semantic tokens.
    (r"field name|property name|event name", None, "field"),
    (r"enum member name|constant name", None, "constant"),
    (r"record class name|record struct name|array name|pointer name|function pointer name", None, "type"),
    (r"namespace name|static symbol|Inline Rename Field Text|Memory Data|Register Data", None, "fg"),
    (r"label name", None, "label"),
    (r"Function|StreamAnalytics - BuiltInFunction|FSharp\.Function", None, "call"),
    (r"FSharp\.MutableVar", None, "field"), (r"FSharp\.Printf", None, "gold"),
    (r"FSharp\.DisposableType", None, "type"),
    (r"FSharp\.Disposable(LocalValue|TopLevelValue)", None, "fg"),
    # JSON, as heritage.vscode: keys as fields
    (r"json - property name", None, "field"), (r"json - string", None, "string"), (r"json - number", None, "number"),
    (r"json - keyword", None, "keyword"), (r"json - comment", None, "comment"),
    (r"json - (punctuation|operator|array|object)", None, "op"), (r"json - text", None, "fg"),
    (r"json - constructor name", None, "call"),
    (r"vsMarkdown_url", None, "azure"),
    (r"HtmlClientTemplateSeparatorFormatDefinition", None, "keyword"),
    (r"HtmlClientTemplateTagFormatDefinition", None, "annotation"),
    # U-SQL, by what each item colours
    (r"U-SQL - Keyword", None, "keyword"), (r"U-SQL - String", None, "string"), (r"U-SQL - Comment", None, "comment"),
    (r"U-SQL - Number", None, "number"), (r"U-SQL - ClassName", None, "type"),
    (r"U-SQL - BuiltInFunction", None, "call"),
    (r"U-SQL - (Identifier|Text)", None, "fg"), (r"U-SQL - Parameter", None, "param"),
    (r"U-SQL - Preprocess", None, "annotation"), (r"U-SQL - Error", None, "error"),
    # the Python interactive window's console colours, as the terminal's
    (r"Python Interactive - (Black|White)", None, "fg"), (r"Python Interactive - Gray", None, "op"),
    (r"Python Interactive - DarkGray", None, "muted"),
    *((rf"Python Interactive - (Dark)?{hue}", None, f"ansi{hue}")
      for hue in ("Red", "Green", "Yellow", "Blue", "Magenta", "Cyan")),
    (r"Interactive Window Error Output", None, "error"),
    # the caret and the editor's own marks
    (r"Caret \(Primary\)", None, "caret"), (r"Caret \(Secondary\)", None, "ansiBlue"),
    (r"Brace Matching \(Highlight\)", "braceBg", None), (r"BraceCompletionClosingBrace", "selInactive", None),
    (r"Collapsible Text \((Collapsed|Expanded)\)", "bg", "muted"),
    (r"SpeculativeTextClassificationFormatDefinition|UnnecessaryCodeDiagnostic", None, "muted"),
    (r"StickyScrollLineHighlightFormat", "hover", "fg"), (r"Selected Text in High Contrast", "selection", "fg"),
    (r"MarkerFormatDefinition/(Filtered)?ScrollBarComment", "comment", None),
    (r"MarkerFormatDefinition/VerticalHighlight", "caretRow", None),
    (r"Peek History Hovered", "hover", None), (r"Peek History Selected", "selection", None),
    (r"PeekFormatDefinition/(EOIMark|PeekMark)", "azure", None),
    (r"RoslynConflictTag|RoslynRenameConflictTag", None, "error"), (r"TextMate\.Classifier", "bg", None),
    (r"data\.tools\.diff\.add\.line", "diffIns", None), (r"data\.tools\.diff\.remove\.line", "diffDel", None),
    (r"data\.tools\.diff\.add\.word", "diffInsWord", None), (r"data\.tools\.diff\.remove\.word", "diffDelWord", None),
    (r"SQL DML Marker", "bg", "keyword"), (r"Bookmark \(Disabled\)", "caretRow", None),
    # debugging, as the breakpoints and current statement above
    (r"Breakpoint( - (Advanced|Mapped))? \(Disabled\)|Breakpoint Group( - Dependent)? \(Disabled\)", "bg", "muted"),
    (r"Breakpoint Group( - Dependent)? \(Enabled\)", "bg", "fg"),
    (r"(Logpoint|Snappoint)( - Advanced)? \((Enabled|Alert|Dashed|Checked|Warning)\)", "diffMod", "fg"),
    (r"(Logpoint|Snappoint)( - Advanced)? \(Disabled\)", "bg", "muted"),
    (r"(Logpoint|Snappoint)( - Advanced)? \(Error\)", "diffMod", "error"),
    (r"Call Return \(new context\)", "diffMod", "fg"),
    (r"Branch Condition Highlight \(True\)", "diffIns", None),
    (r"Branch Condition Highlight \(False\)", "diffDel", None),
    (r"Executing Thread IPs?", "bg", "muted"),
    (r"Stack Frame \(Critical\)", "diffDel", "fg"), (r"Stack Frame \(Warning\)", "diffConf", "fg"),
]
# The tool windows that show text: output, find results, the interactive windows and grids, on the tool window colour.
TEXT_VIEWS = [
    (r"Plain Text|Console Output Text|Grid Cell", "bgTool", "fg"), (r"Header Row", "bgUi", "fg"),
    (r"Selected Text|Selected Cell|Current List Location", "selection", "fg"),
    (r"Inactive Selected Text|Inactive Selected Cell", "selInactive", "fg"),
    (r"Null Value Cell|OutputVerbose|Console Input Text", "bgTool", "muted"),
    (r"OutputError|Console Error Text", "bgTool", "ansiRed"), (r"Console Warning Text", "bgTool", "ansiYellow"),
    (r"OutputHeading|Console Info Text", "bgTool", "ansiBlue"), (r"urlformat", "bgTool", "azure"),
    (r"inlay hints (parameter|type)", "caretRow", "muted"),
    (r"outlining\.chevron\.(collapsed|expanded)", "bgTool", "muted"), (r"outlining\.verticalrule", None, "guide"),
    (r"outlining\.collapsehintadornment", "surface", "fg"),
    (r"ChangedText", None, "ansiRed"),
    (r"Different content", "bgTool", "ansiRed"), (r"Not Downloaded", "bgTool", "muted"),
    (r"Even Row Items|Odd Row Items|Identical content|Source Only|Target Only", "bgTool", "fg"),
]
# CodeLens and the controls of its popups.
CODE_LENS = [
    (r"IndicatorSeparator|IndicatorText|IndicatorTextDisabled", None, "muted"),
    (r"IndicatorTextHovered", None, "azure"), (r"IndicatorTextSelected", None, "fg"),
    (r"ActionLink|ActionLinkItem|ActionLinkItemHover|ActionLinkItemSelectedNotFocused", "azure", "azure"),
    (r"ActionLinkDisabled|ActionLinkItemDisabled", "disabled", "disabled"), (r"ActionLinkItemSelected", None, "fg"),
    (r"BodyText|ItemHoverText|TextHover|TextSelected|YouAreHereText", "fg", None),
    (r"GrayText|GrayTextHover|HeaderText|SubduedText", "muted", None),
    (r"ChartAxis|ChartTickMark|ChartSplitter|FileIndicatorPanelBorder|SubduedBorder", "border", None),
    (r"DiffViewHighlight", "selInactive", None), (r"ItemSelectedText", "selection", "fg"),
    (r"Popup", "surface", "fg"), (r"PopupBorder", "border", None), (r"PopupHover", "hover", None),
    (r"PopupPinButtonHover", "hover", "fg"), (r"PopupPinButtonMouseDown", "selection", "fg"),
    (r"PopupSelected", "selection", None), (r"PopupSelectedInactive", "selInactive", "fg"),
    (r"RankedItemsFirst", "ansiMagenta", None), (r"RankedItemsSecond", "ansiBlue", None),
    (r"RankedItemsThird", "ansiGreen", None), (r"RankedItemsFourth", "ansiCyan", None),
    (r"RankedItemsFifth", "muted", None), (r"YouAreHereBackground", "red", None),
]
EDITOR = {
    "Text Editor Text Manager Items": CODE, "Text Editor Language Service Items": CODE,
    "Text Editor MEF Items": CODE, "Text Editor Text Marker Items": CODE,
    "Editor Tooltip": [(r"Plain Text", "surface", "fg")],
    "Output Window": TEXT_VIEWS, "Find Results": TEXT_VIEWS, "Immediate Window": TEXT_VIEWS,
    "Command Window": TEXT_VIEWS, "Package Manager Console": TEXT_VIEWS, "FSharpInteractive": TEXT_VIEWS,
    "WebClient Diagnostic Tools": TEXT_VIEWS, "SQL Results - Text": TEXT_VIEWS, "SQL Results - Grid": TEXT_VIEWS,
    "Locals": TEXT_VIEWS, "Autos": TEXT_VIEWS, "Watch": TEXT_VIEWS, "Folder Difference": TEXT_VIEWS,
    "Performance Tips": [(r"Selected Text", None, "azure")],
    "CodeSense": CODE_LENS, "CodeSenseControls": CODE_LENS,
}
EDITOR_RULES = {category: [(re.compile(names), background, foreground) for names, background, foreground in rules]
                for category, rules in EDITOR.items()}


def editor_rule(category, name, channel, built_in):
    """The spec for a channel of an editor colour, or None when no rule covers it."""
    for names, *specs in EDITOR_RULES[category]:
        if names.fullmatch(name):
            spec = specs[channel]
            return AUTOMATIC if spec is None and built_in == AUTOMATIC else spec
    return None


def colours(p):
    """[(category name, category GUID, colours)] for a palette, colours as for encode(). Raises ValueError for a
    colour that no rule covers."""
    r, out, missing = roles(p), [], []
    for category in MODEL["categories"]:
        if category["name"] not in FLUENT + tuple(EDITOR) + LEGACY:
            continue
        entries = []
        for colour in category["colours"]:
            pair = []
            for channel in (0, 1):
                built_in = default(colour, p, channel)
                if category["name"] in LEGACY:
                    # an automatic or indexed legacy colour keeps the built-in theme's, which follows the palette
                    raw = built_in is not None and ARGB.fullmatch(built_in)
                    pair.append(legacy_colour(category["name"], colour, channel, p, r, built_in) if raw else None)
                    continue
                if built_in is None:
                    pair.append(None)
                    continue
                if category["name"] in FLUENT:
                    spec = shell_rule(category["name"], colour["name"], r, built_in)
                else:
                    spec = editor_rule(category["name"], colour["name"], channel, built_in)
                if spec is None:
                    missing.append(f"{category['name']}/{colour['name']}/{('background', 'foreground')[channel]}")
                    pair.append(None)
                    continue
                pair.append(resolve(spec, r, built_in))
            if any(pair):
                entries.append((colour["name"], *pair))
        if entries:
            out.append((category["name"], category["guid"], entries))
    if missing:
        raise ValueError("no rule for the Visual Studio colours " + "; ".join(missing))
    return out


# The categories whose text is drawn on one background, by its role: the editor's for code, the tool window's for
# output. A foreground on it is held to 4.5:1, or to 3:1 for comments and for the marks drawn in LOW_CONTRAST roles,
# such as squiggles and change bars, as for focus rings. Lines, gutter numbers and the weak-warning wave in NOT_TEXT are
# faint by design, as in the other targets.
READABLE = {"Text Editor Text Manager Items": "bg", "Text Editor Language Service Items": "bg",
            "Text Editor MEF Items": "bg", "Text Editor Text Marker Items": "bg", "Output Window": "bgTool",
            "Find Results": "bgTool", "Immediate Window": "bgTool", "Command Window": "bgTool",
            "Package Manager Console": "bgTool"}
LOW_CONTRAST = {"comment", "caret", "warning", "error", "added", "deleted", "modified", "red"}
NOT_TEXT = {"guide", "guideSel", "border", "caretRow", "lineNo", "lineNoCaret", "disabled", "weak"}


def check(text, p, guid):
    """Fails with SystemExit when the .pkgdef text of a palette's theme does not register the theme under guid with
    its name and fallback, does not hold exactly the colours that colours() gives it, sets a colour that
    visualstudio.json lacks, or draws code or tool output in a colour that is unreadable on its background. Returns
    the theme's GUID."""
    def fail(message):
        raise SystemExit(f"Visual Studio {p['name']}: {message}")
    key = f"$RootKey$\\Themes\\{{{guid}}}"
    found = sections(text)
    if not found or found[0][0] != key or dict(found[0][1]) != {"@": p["name"], "Name": p["name"],
                                                                "FallbackId": FALLBACK[p["dark"]]}:
        fail(f"the theme is not registered as [{key}] with its name and fallback")
    decoded = {}
    for section, values in found[1:]:
        category = section.removeprefix(key + "\\")
        if not section.startswith(key + "\\") or [name for name, _ in values] != ["Data"]:
            fail(f"{section} is not a colour category of the theme")
        version, records = decode(values[0][1])
        if version != DATA_VERSION or len(records) != 1 or records[0][0] != CATEGORIES[category]["guid"]:
            fail(f"the data of {category} is not version {DATA_VERSION} of its category alone")
        decoded[category] = records[0][1]
    expected = {name: entries for name, _, entries in colours(p)}
    if decoded != expected:
        fail("the colour data does not decode to the colours that heritage.visualstudio gives the theme")
    for category, entries in decoded.items():
        known = {c["name"] for c in CATEGORIES[category]["colours"]}
        for name, *pair in entries:
            if name not in known:
                fail(f"{category}/{name} is not a colour of visualstudio.json")
            for colour in pair:
                if colour and colour[0] == CT_RAW and not ARGB.fullmatch(colour[1]):
                    fail(f"{category}/{name} has {colour[1]!r}")
    r = roles(p)
    for category, background in READABLE.items():
        for colour in CATEGORIES[category]["colours"]:
            if default(colour, p, 1) is None:
                continue
            specs = [editor_rule(category, colour["name"], channel, default(colour, p, channel)) for channel in (0, 1)]
            if specs[0] not in (None, AUTOMATIC, background) or specs[1] in (None, AUTOMATIC) or \
                    specs[1] in NOT_TEXT or "@" in specs[1] or specs[1].endswith("~"):
                continue  # drawn on a background of its own, translucent or not text
            minimum = 3 if specs[1] in LOW_CONTRAST else 4.5
            ratio = contrast(r[specs[1]], p[background])
            if ratio < minimum:
                fail(f"{category}/{colour['name']} is {ratio:.2f}:1 on {background}, needs {minimum}:1")
    return guid


# A VSIX of themes for Visual Studio 2026, whose themes build on the Fluent colour tokens that earlier versions do not
# read. It needs only the core editor, which every edition has.
VERSIONS = "[18.0,19.0)"
CORE_EDITOR = ("Microsoft.VisualStudio.Component.CoreEditor", "18.0")
# The media types of the files in a VSIX, which the Open Packaging Conventions require it to list.
CONTENT_TYPES = {"vsixmanifest": "text/xml", "pkgdef": "text/plain", "png": "application/octet-stream",
                 "txt": "text/plain", "json": "application/json"}
# The files of a VSIX that describe it rather than install: the package's media types and the two setup manifests.
SETUP_FILES = ("[Content_Types].xml", "manifest.json", "catalog.json")


def vsix_manifest(identity, version, name, description, slugs, metadata):
    """extension.vsixmanifest: the extension's identity, the Visual Studio versions it installs in and the .pkgdef of
    each theme, which Visual Studio merges into its registry. metadata is further Metadata elements."""
    assets = "\n".join(f'    <Asset Type="Microsoft.VisualStudio.VsPackage" Path="themes\\{slug}.pkgdef" />'
                       for slug in slugs)
    targets = "\n".join(f"""    <InstallationTarget Id="Microsoft.VisualStudio.Community" Version="{VERSIONS}">
      <ProductArchitecture>{architecture}</ProductArchitecture>
    </InstallationTarget>""" for architecture in ("amd64", "arm64"))
    editor, editor_version = CORE_EDITOR
    return f"""<?xml version="1.0" encoding="utf-8"?>
<PackageManifest Version="2.0.0" xmlns="http://schemas.microsoft.com/developer/vsx-schema/2011">
  <Metadata>
    <Identity Id="{identity}" Version="{version}" Language="en-US" Publisher="Heritage Themes" />
    <DisplayName>{name}</DisplayName>
    <Description xml:space="preserve">{description}</Description>
{metadata}  </Metadata>
  <Installation>
{targets}
  </Installation>
  <Prerequisites>
    <Prerequisite Id="{editor}" Version="[{editor_version},)" DisplayName="Visual Studio core editor" />
  </Prerequisites>
  <Assets>
{assets}
  </Assets>
</PackageManifest>
"""


def content_types():
    """[Content_Types].xml: the media type of each file extension in the VSIX."""
    defaults = "".join(f'<Default Extension="{extension}" ContentType="{kind}" />'
                       for extension, kind in CONTENT_TYPES.items())
    return ('<?xml version="1.0" encoding="utf-8"?>'
            f'<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">{defaults}</Types>\n')


def setup_manifests(directory, identity, version, name, description):
    """{file name: JSON text} for manifest.json and catalog.json, the setup manifests that Visual Studio's installer
    requires in a VSIX besides extension.vsixmanifest, as the Visual Studio SDK writes them: the files in directory that
    the extension installs, their size, its prerequisite and the folder it installs in for all users. The SDK names
    that folder at random; a name derived from the identity keeps the build reproducible."""
    files = sorted("/" + os.path.relpath(os.path.join(root, f), directory).replace(os.sep, "/")
                   for root, _, names in os.walk(directory) for f in names if f not in SETUP_FILES)
    size = sum(os.path.getsize(os.path.join(directory, f[1:])) for f in files)
    digest = base64.b32encode(hashlib.sha256(identity.encode()).digest()).decode().lower()
    folder = f"[installdir]\\Common7\\IDE\\Extensions\\{digest[:8]}.{digest[8:11]}"
    editor, editor_version = CORE_EDITOR
    manifest = {"id": identity, "version": version, "type": "Vsix", "vsixId": identity, "extensionDir": folder,
                "files": [{"fileName": f, "sha256": None} for f in files], "installSizes": {"targetDrive": size},
                "dependencies": {editor: editor_version}}
    catalog = {"manifestVersion": "1.1", "info": {"id": f"{identity},version={version}", "manifestType": "Extension"},
               "packages": [
                   {"id": f"Component.{identity}", "version": version, "type": "Component", "extension": True,
                    "dependencies": {identity: version, editor: editor_version},
                    "localizedResources": [{"language": "en-US", "title": name, "description": description}]},
                   {"id": identity, "version": version, "type": "Vsix",
                    "payloads": [{"fileName": f"{identity}-{version}.vsix", "size": size}], "vsixId": identity,
                    "extensionDir": folder, "installSizes": {"targetDrive": size}}]}
    return {f: json.dumps(document, ensure_ascii=False, separators=(",", ":"))
            for f, document in (("manifest.json", manifest), ("catalog.json", catalog))}


def package(directory, identity, version, name, description, themes, metadata=""):
    """Writes the files of a VSIX of themes to directory, which holds the files that metadata names: a .pkgdef per
    theme in themes/, extension.vsixmanifest, [Content_Types].xml and the setup manifests. themes is a list of
    (slug, GUID, palette, source URL)."""
    def save(path, text):
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
    os.makedirs(os.path.join(directory, "themes"), exist_ok=True)
    for slug, guid, p, source in themes:
        save(os.path.join(directory, "themes", f"{slug}.pkgdef"), theme(p, guid, source))
    save(os.path.join(directory, "extension.vsixmanifest"),
         vsix_manifest(identity, version, name, description, [slug for slug, *_ in themes], metadata))
    save(os.path.join(directory, "[Content_Types].xml"), content_types())
    for f, text in setup_manifests(directory, identity, version, name, description).items():
        save(os.path.join(directory, f), text)


def pack(directory, path, entry):
    """Zips the files of directory into the .vsix at path, an Open Packaging Conventions package, with entry(name)
    making each zip entry, and returns path."""
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for root, folders, files in os.walk(directory):
            folders.sort()
            for f in sorted(files):
                with open(os.path.join(root, f), "rb") as source:
                    z.writestr(entry(os.path.relpath(os.path.join(root, f), directory).replace(os.sep, "/")),
                               source.read())
    return path


def setting_id(name):
    """The ID that Visual Studio gives a theme in settings.json (environment.visualExperience.colorTheme): its name in
    lower case, with its words joined by hyphens and without brackets."""
    return "-".join(re.findall(r"[^\s()]+", name.lower()))


def theme(p, guid, source):
    """The .pkgdef for a palette: a theme with the GUID guid that falls back to the built-in theme of its brightness.
    source is the URL of the theme folder."""
    return pkgdef(p["name"], guid, FALLBACK[p["dark"]], colours(p),
                  f"{p['name']}: a Heritage Themes theme for Visual Studio.\n"
                  f"Generated from {source}; changes here are overwritten.")
