"""RStudio editor themes generated from a palette: one .rstheme file for each Heritage theme.

An rstheme is a CSS file with two header comments, the theme's name and whether it is dark. RStudio draws its source
editors, its console, its R Markdown and Quarto visual editor and its Terminal tab from one theme, and tokenises code
with Ace, whose modes name each token with dotted types: the token `constant.numeric` is an element with the classes
`ace_constant` and `ace_numeric`. A theme colours those classes, the markers that Ace and RStudio draw behind the
text, and the 256 colours of the Terminal tab. RStudio draws the panes, toolbars and menus around them itself, dark or
light as the header says, and a theme sets none of their colours.

The rules are those of the theme files that RStudio itself compiles (`.rs.compile_theme`), with the colours of the
palette's roles: a rule that RStudio's own themes set is set here, and so is every class that RStudio reads back from
the page to colour its visual editor (`ace_node-selector`, `ace_comment-highlight`, `ace_foreign_line`,
`ace_find_line`, `ace_selected-word`, `ace_support ace_function` and the token classes). The token rules map the roles
that heritage.vscode and heritage.pygments give the matching constructs. Ace's modes give a construct one token type in
every language, so the same rule colours it in each: R's function calls are `support.function`, as Python's builtins
and the commands of a shell are, and keywords, storage types and `this` take the keyword colour. RStudio's R mode
tokenises roxygen tags, section headings and TODO comments as parts of a comment, and the rules below set them apart.
RStudio's C and C++ mode gives a preprocessor directive the token type `keyword.preproc`, which takes the directive
role.

A theme file is installed by copying it into RStudio's themes folder, or with the Add button under Tools | Global
Options | Appearance. RStudio lists a theme by the name in its header comment and keeps the file under the name that
the file has, so the name is the display name and the file name is the lower-case identifier that Neovim uses.
"""
import re

from .colour import distance
from .nvim import name as identifier, terminal as ansi
from .sublime import basename
from .terminals import contrast
from .vscode import mix

PREFIX = "Heritage "  # a theme's name in RStudio's list, so that the themes sit together among RStudio's own
# The patterns with which RStudio reads the header comments, one line each: the name, and the brightness, which it then
# reads as a boolean. A value ends at the first asterisk.
NAME_PATTERN = re.compile(r"rs-theme-name\s*:\s*([^\*]+?)\s*(?:\*|$)")
DARK_PATTERN = re.compile(r"rs-theme-is-dark\s*:\s*([^\*]+?)\s*(?:\*|$)")
# A colour that a theme writes: #RRGGBB, or #RRGGBBAA where the rainbow guides take an alpha, as RStudio's own do.
COLOUR = re.compile(r"#[0-9A-F]{6}(?:[0-9A-F]{2})?")
# The roles of the seven colours of the rainbow parentheses and indent guides, in the order of Ace's classes 0 to 6. The
# parentheses are text, so each is a syntax role.
RAINBOW = ("keyword", "number", "string", "type", "call", "method", "constant")
# The most that an Rmd or Quarto code chunk's background moves from the editor's background towards its text, as in
# RStudio's own themes: dark themes more, as a dark surface needs a larger step to be seen, in steps of CHUNK_STEP.
CHUNK_MIX = {True: 0.10, False: 0.05}
CHUNK_STEP = 0.005
# The least CIE76 distance between a chunk's background and the editor's, so that a chunk stands apart.
CHUNK_APART = 2
# The backgrounds that code is drawn on, as (palette role or "chunk", the label's suffix): the editor, its current line
# and a code chunk.
BACKGROUNDS = (("bg", ""), ("caretRow", " on the current line"), ("chunk", " on a chunk"))


def name(t):
    """The name of a theme dict from a theme.py in RStudio's list, for example "Heritage Holi Night (Dark)"."""
    return PREFIX + basename(t["palette"]["name"])


def filename(t):
    """The theme's file name, for example "heritage-holi-night-dark.rstheme"."""
    return identifier(t) + ".rstheme"


def chunk(p):
    """The background of a code chunk in an R Markdown or Quarto document: the editor's background moved towards its
    text by the largest step, up to CHUNK_MIX, at which every colour of the token rules keeps its contrast, 4.5:1 and
    3:1 for comments. The palette guarantees those on the editor's background and the current line only, so a fixed
    step takes roles below their minimum in many themes."""
    needed = {role: 3 if role == "comment" else 4.5 for _, role, _ in syntax(p)}
    needed["fg"] = 4.5
    steps = round(CHUNK_MIX[p["dark"]] / CHUNK_STEP)
    for i in range(steps, 0, -1):
        colour = mix(p["bg"], p["fg"], i * CHUNK_STEP)
        if all(contrast(p[role], colour) >= minimum for role, minimum in needed.items()):
            return colour
    return p["bg"]


def chunk_apart(p):
    """Whether a chunk's background is at least CHUNK_APART from the editor's, as CIE76 measures it."""
    return distance(p["bg"], chunk(p)) >= CHUNK_APART


def syntax(p):
    """(selectors, role, font style) of the token rules. Ace gives a token type one class for each of its dotted
    parts, so a selector of several classes matches every type that has them all. A rule with more classes overrides
    one with fewer, and of two rules with as many, the later wins: a rule for a part of a type, such as the quotes of a
    string, comes after the rule for the whole."""
    kw = "bold" if p.get("kwBold", not p["dark"]) else ""
    out = []
    def s(selectors, role, font=""):
        out.append((selectors, role, font))
    # words and punctuation
    s([".ace_keyword", ".ace_storage", ".ace_meta.ace_tag", ".ace_xml-pe", ".ace_xml_pe", ".ace_fenced_open",
       ".ace_support.ace_php_tag", ".ace_constant.ace_language"], "keyword", kw)
    s([".ace_keyword.ace_operator", ".ace_keyword.ace_bracket", ".ace_punctuation", ".ace_punctuaction", ".ace_paren",
       ".ace_lparen", ".ace_rparen"], "op")
    s([".ace_variable.ace_language"], "keyword", "italic")
    # names
    s([".ace_support.ace_function", ".ace_support.ace_buildin"], "call")
    s([".ace_support.ace_class", ".ace_support.ace_type", ".ace_entity.ace_name.ace_type", ".ace_meta.ace_type",
       ".ace_entity.ace_other.ace_inherited-class"], "type")
    s([".ace_entity.ace_name.ace_function"], "method", "bold")
    s([".ace_variable", ".ace_entity.ace_other.ace_attribute-name"], "field")
    s([".ace_variable.ace_parameter"], "param")
    s([".ace_storage.ace_type.ace_annotation", ".ace_variable.ace_macro", ".ace_meta.ace_preprocessor.ace_rust"],
      "annotation")
    s([".ace_keyword.ace_preproc", ".ace_meta.ace_preprocessor"], "directive")
    s([".ace_support.ace_constant", ".ace_constant", ".ace_constant.ace_other"], "constant", "bold italic")
    # literals
    s([".ace_string"], "string")
    s([".ace_constant.ace_numeric", ".ace_support.ace_date"], "number")
    s([".ace_constant.ace_character", ".ace_constant.ace_language.ace_escape", ".ace_constant.ace_character.ace_escape",
       ".ace_character.ace_escape", ".ace_escape", ".ace_regexp.ace_keyword", ".ace_paren.ace_quasi"], "gold", "bold")
    s([".ace_constant.ace_character.ace_entity", ".ace_constant.ace_language.ace_escape.ace_reference"], "gold")
    s([".ace_string.ace_regexp.ace_characterclass", ".ace_string.ace_regexp.ace_charachterclass"], "number", "bold")
    s([".ace_invalid", ".ace_error", ".ace_string.ace_invalid"], "ansiRed")
    s([".ace_invalid.ace_deprecated"], "ansiYellow", "underline")
    # comments: the generic rule first, then the parts of a comment that RStudio's R mode and the doc comment modes name
    s([".ace_comment"], "comment", "italic")
    s([".ace_comment.ace_shebang"], "comment", "bold italic")
    s([".ace_comment.ace_doc"], "doc", "italic")
    s([".ace_comment.ace_doc.ace_tag", ".ace_keyword.ace_virtual-comment"], "docTag", "bold italic")
    s([".ace_comment.ace_sectionhead"], "method", "bold")
    s([".ace_comment.ace_keyword.ace_operator"], "todo", "bold italic")
    # HTML and XML: attribute names are fields, the equals sign takes the tag's colour
    s([".ace_keyword.ace_operator.ace_attribute-equals", ".ace_keyword.ace_operator.ace_decl-attribute-equals"],
      "keyword", kw)
    # Markdown and the Markdown of R Markdown: headings, markers, emphasis, quotes, links and rules
    s([".ace_heading", ".ace_markup.ace_heading"], "method", "bold")
    s([".ace_markup.ace_list", ".ace_list"], "keyword", kw)
    # RStudio's Markdown mode gives emphasis the types of constants with the part `text`: constant.language.boolean.text
    # for *italic* and constant.numeric.text for **bold**
    s([".ace_string.ace_emphasis", ".ace_constant.ace_language.ace_text"], "fg", "italic")
    s([".ace_string.ace_strong", ".ace_constant.ace_numeric.ace_text"], "fg", "bold")
    s([".ace_string.ace_blockquote"], "doc", "italic")
    s([".ace_markup.ace_underline", ".ace_markup.ace_href", ".ace_url"], "azure", "underline")
    s([".ace_constant.ace_hr"], "muted")
    return out


def rainbow(p):
    """The seven colours of the rainbow parentheses and indent guides, as #RRGGBB."""
    return ["#" + p[role] for role in RAINBOW]


def terminal_colours():
    """The 240 colours of the xterm 256-colour palette that follow its 16 colours: a 6 x 6 x 6 colour cube and a
    ramp of 24 greys. They are the same in every theme, as in RStudio's own."""
    levels = (0, 95, 135, 175, 215, 255)
    cube = [(r, g, b) for r in levels for g in levels for b in levels]
    ramp = [(8 + 10 * i,) * 3 for i in range(24)]
    return ["#%02X%02X%02X" % rgb for rgb in cube + ramp]


def blocks(p):
    """(selectors, declarations) of every rule of a theme in file order; declarations is a list of (property, value)."""
    c = {k: "#" + v for k, v in p.items() if isinstance(v, str) and re.fullmatch(r"[0-9A-F]{6}", v)}
    c["caret"] = "#" + p.get("caret", p["gold"])
    c["chunk"] = "#" + chunk(p)
    out = []
    def b(selectors, *declarations):
        out.append((selectors if isinstance(selectors, list) else [selectors], list(declarations)))
    # the editor, the gutter and what Ace draws behind the text
    b(".ace_gutter", ("background", c["bg"]), ("color", c["lineNo"]))
    b(".ace_print-margin", ("width", "1px"), ("background", c["guide"]))
    b([".ace_editor", ".ace_editor_theme .profvis-flamegraph", ".ace_editor_theme"],
      ("background-color", c["bg"]), ("color", c["fg"]))
    b(".ace_cursor", ("color", c["caret"]))
    b(".ace_marker-layer .ace_selection", ("background", c["selection"]))
    b(".ace_selection.ace_start", ("box-shadow", f"0 0 3px 0px {c['bg']}"), ("border-radius", "2px"))
    b(".ace_marker-layer .ace_active-line", ("background", c["caretRow"]))
    b(".ace_gutter-active-line", ("background-color", c["caretRow"]), ("color", c["lineNoCaret"]))
    b(".ace_marker-layer .ace_selected-word", ("background", c["underCaret"]), ("border", f"1px solid {c['selection']}"))
    b(".ace_bracket", ("margin", "0 !important"), ("border", "0 !important"), ("background-color", c["braceBg"]))
    b(".ace_fold", ("background-color", c["hover"]), ("border-color", c["muted"]))
    b(".ace_invisible", ("color", c["guide"]))
    for selector, role in ((".ace_indent-guide", "guide"), (".ace_indent-guide-active", "guideSel")):
        b(selector, ("background", f"linear-gradient(to left, {c[role]} 1px, transparent 1px, transparent)"))
    for selectors, role, font in syntax(p):
        # CSS cascades each property on its own, so every rule sets the font style and weight: a rule with more classes
        # then resets what one with fewer sets, as bold keywords do not make their operators bold
        words = font.split()
        declarations = [("color", c[role]), ("font-style", "italic" if "italic" in words else "normal"),
                        ("font-weight", "bold" if "bold" in words else "normal")]
        if "underline" in words:
            declarations.append(("text-decoration", "underline"))
        b(selectors, *declarations)
    # Julia's brackets are tokens of the type keyword.bracket, which have the class that the matching-bracket marker has
    b(".ace_keyword.ace_bracket", ("background-color", "transparent"))
    for i, colour in enumerate(rainbow(p)):
        b(f".ace_paren_color_{i}", ("color", colour))
    # markers that RStudio draws, and that its visual editor reads back to colour code chunks, finds and selections
    b(".nocolor.ace_editor .ace_line span", ("color", f"{c['keyword']} !important"))
    for selector, colour in ((".ace_foreign_line", c["chunk"]), (".ace_active_debug_line", c["diffMod"]),
                             (".ace_find_line", c["border"])):
        b(f".ace_marker-layer {selector}", ("position", "absolute"), ("z-index", "-1"), ("background-color", colour))
    b(".ace_node-selector", ("background-color", c["gold"]))
    b(".ace_comment-highlight", ("color", c["fg"]), ("background-color", c["searchBg"]))
    b(".ace_console_error", ("background-color", c["writeCaret"]))
    # the Terminal tab
    b(".terminal", ("background-color", c["bg"]), ("color", c["fg"]), ("font-feature-settings", '"liga" 0'),
      ("position", "relative"), ("user-select", "none"), ("-ms-user-select", "none"), ("-webkit-user-select", "none"))
    b(".terminal.xterm-cursor-style-block.focus:not(.xterm-cursor-blink-on) .terminal-cursor",
      ("background-color", c["caret"]), ("color", c["bg"]))
    b([".terminal.focus.xterm-cursor-style-bar:not(.xterm-cursor-blink-on) .terminal-cursor::before",
       ".terminal.focus.xterm-cursor-style-underline:not(.xterm-cursor-blink-on) .terminal-cursor::before"],
      ("content", "''"), ("position", "absolute"), ("background-color", c["caret"]))
    b(".terminal:not(.focus) .terminal-cursor", ("outline", f"1px solid {c['caret']}"), ("outline-offset", "-1px"))
    b(".terminal .xterm-selection div", ("position", "absolute"), ("background-color", c["fg"]))
    b(".terminal .xterm-viewport", ("background-color", c["bg"]), ("overflow-y", "scroll"))
    b(".xtermInvertColor", ("color", c["bg"]))
    b(".xtermInvertBgColor", ("background-color", c["fg"]))
    for selector, declaration in ((".xtermBold", ("font-weight", "bold")), (".xtermBlur", ("filter", "brightness(75%)")),
                                  (".xtermUnderline", ("text-decoration", "underline")),
                                  (".xtermBlink", ("text-decoration", "blink")),
                                  (".xtermHidden", ("visibility", "hidden")), (".xtermItalic", ("font-style", "italic")),
                                  (".xtermStrike", ("text-decoration", "line-through"))):
        b(selector, declaration)
    for i, colour in enumerate(ansi(p) + terminal_colours()):
        b(f".xtermColor{i}", ("color", f"{colour} !important"))
        b(f".xtermBgColor{i}", ("background-color", colour))
    # rules that RStudio's themes share: links in a dark editor, the layers of the editor and the rainbow guides
    if p["dark"]:
        b(".editor_dark.ace_editor_theme a", ("color", f"{c['azure']} !important"))
    for selector, z in ((".ace_layer", "3"), (".ace_layer.ace_print-margin-layer", "2"),
                        (".ace_layer.ace_marker-layer", "1")):
        b(selector, ("z-index", z))
    if p["dark"]:
        b(".rstudio-themes-dark-menus .ace_editor.ace_autocomplete", ("background", c["surface"]),
          ("border", f"solid 1px {c['border']} !important"), ("color", c["fg"]))
        b([".rstudio-themes-dark-menus .ace_editor.ace_autocomplete .ace_marker-layer .ace_active-line",
           ".rstudio-themes-dark-menus .ace_editor.ace_autocomplete .ace_marker-layer .ace_line-hover"],
          ("background", c["selection"]), ("border", "none"))
    for kind in ("guides", "fills"):
        for i, colour in enumerate(rainbow(p)):
            gradient = (f"linear-gradient(to left, {colour}BB 1px, transparent 1px, transparent)" if kind == "guides"
                        else f"linear-gradient(to left, {colour}BB 1px, {colour}77 1px, {colour}77)")
            b(f".rstudio_rainbow_indent_{kind} .ace_line .ace_indent-guide:nth-child(7n+{i + 1})",
              ("background", gradient))
    return out


def resolve(p, token):
    """property → value that CSS gives an element with the classes of a token type, for the rules of a theme that are
    made of classes only: for each property the value of the rule with the most classes, and of two with as many, of
    the later one."""
    classes = {f"ace_{part}" for part in token.split(".")}
    winner = {}
    for order, (selectors, declarations) in enumerate(blocks(p)):
        for selector in selectors:
            if not re.fullmatch(r"(?:\.ace_[\w\-]+)+", selector):
                continue
            wanted = set(re.findall(r"ace_[\w\-]+", selector))
            if wanted <= classes:
                for prop, value in declarations:
                    if prop not in winner or (len(wanted), order) >= winner[prop][0]:
                        winner[prop] = ((len(wanted), order), value)
    return {prop: value for prop, (_, value) in winner.items()}


def cases(p):
    """(token type, role, font style) that resolve() must give each of these token types, which are those of the
    languages that RStudio's users write most. A rule with more classes must reset the font that a rule with fewer
    sets, so that bold keywords do not make their operators bold and constants do not make numbers italic."""
    kw = "bold" if p.get("kwBold", not p["dark"]) else ""
    return [
        ("keyword", "keyword", kw), ("keyword.control", "keyword", kw), ("storage.type", "keyword", kw),
        ("storage.modifier", "keyword", kw), ("constant.language", "keyword", kw),
        ("constant.language.boolean", "keyword", kw), ("meta.tag", "keyword", kw),
        ("keyword.operator.attribute-equals", "keyword", kw), ("markup.list", "keyword", kw),
        ("list.markup.keyword.operator", "keyword", kw), ("fenced_open", "keyword", kw),
        ("keyword.operator", "op", ""), ("paren.keyword.operator", "op", ""), ("keyword.operator.infix", "op", ""),
        ("punctuation.keyword.operator", "op", ""), ("paren.lparen", "op", ""), ("punctuation.operator", "op", ""),
        ("keyword.bracket", "op", ""), ("constant.numeric", "number", ""), ("support.date", "number", ""),
        ("string", "string", ""), ("string.quoted.double", "string", ""), ("string.regexp", "string", ""),
        ("punctuation.definition.string.begin", "string", ""), ("string.end", "string", ""),
        ("identifier.support.function", "call", ""), ("support.function", "call", ""),
        ("identifier.support.class", "type", ""), ("support.type", "type", ""), ("entity.name.type", "type", ""),
        ("entity.name.function", "method", "bold"), ("variable", "field", ""),
        ("entity.other.attribute-name", "field", ""), ("variable.parameter", "param", ""),
        ("variable.language", "keyword", "italic"), ("variable.macro", "annotation", ""),
        ("storage.type.annotation", "annotation", ""), ("keyword.preproc", "directive", ""),
        ("constant", "constant", "bold italic"), ("support.constant", "constant", "bold italic"),
        ("constant.other", "constant", "bold italic"), ("constant.character.escape", "gold", "bold"),
        ("constant.language.escape", "gold", "bold"), ("regexp.keyword.operator", "gold", "bold"),
        ("constant.character.entity", "gold", ""), ("string.regexp.characterclass", "number", "bold"),
        ("comment", "comment", "italic"), ("punctuation.definition.comment", "comment", "italic"),
        ("comment.shebang", "comment", "bold italic"), ("comment.doc", "doc", "italic"),
        ("comment.doc.tag", "docTag", "bold italic"), ("keyword.virtual-comment", "docTag", "bold italic"),
        ("comment.sectionhead", "method", "bold"), ("comment.keyword.operator", "todo", "bold italic"),
        ("markup.heading", "method", "bold"), ("heading", "method", "bold"), ("string.emphasis", "fg", "italic"),
        ("string.strong", "fg", "bold"), ("constant.language.boolean.text", "fg", "italic"),
        ("constant.numeric.text", "fg", "bold"), ("string.blockquote", "doc", "italic"), ("url", "azure", "underline"),
        ("markup.href", "azure", "underline"),
        ("invalid", "ansiRed", ""), ("invalid.deprecated", "ansiYellow", "underline"),
    ]


def theme(p, theme_name, source):
    """The text of a theme's .rstheme file. source is the URL of the family's folder."""
    lines = [f"/* rs-theme-name: {theme_name} */",
             f"/* rs-theme-is-dark: {'TRUE' if p['dark'] else 'FALSE'} */",
             f"/* {p['name']}: a Heritage Themes editor theme for RStudio. Generated from {source}; changes here are "
             f"overwritten. */"]
    for selectors, declarations in blocks(p):
        lines.append(",\n".join(selectors) + " {")
        lines.extend(f"  {prop}: {value};" for prop, value in declarations)
        lines.append("}")
    return "\n".join(lines) + "\n"


def parse(text):
    """(name, dark, blocks) of a theme file: the name and brightness that RStudio reads from the header, None for a
    brightness that is not TRUE or FALSE, and the rules as blocks() gives them. It reads only the layout that theme()
    writes, so a file that differs in form fails to match."""
    def header(pattern):
        return next((m[1] for m in map(pattern.search, text.splitlines()) if m), None)
    theme_name, dark = header(NAME_PATTERN), header(DARK_PATTERN)
    body = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    rules = []
    for selectors, declarations in re.findall(r"^([^{}\n][^{}]*?) \{\n((?:  [^\n]+;\n)*)\}$", body, re.M):
        rules.append((selectors.split(",\n"),
                      [tuple(d[2:-1].split(": ", 1)) for d in declarations.splitlines()]))
    return theme_name, {"TRUE": True, "FALSE": False}.get(dark), rules


def styles(p):
    """label → dict(fg, bg) as #RRGGBB, for the build's contrast check: each token rule's colour on the editor's
    background, on the current line and on a code chunk; the editor's text on each highlight that Ace and RStudio draw
    behind it; the caret and the terminal's colours on its background."""
    c = {k: "#" + v for k, v in p.items() if isinstance(v, str) and re.fullmatch(r"[0-9A-F]{6}", v)}
    c["chunk"] = "#" + chunk(p)
    out = {}
    for selectors, role, _ in syntax(p):
        for background, where in BACKGROUNDS:
            label = selectors[0] + where
            assert label not in out, f"two token rules start with {selectors[0]}"
            out[label] = dict(fg=c[role], bg=c[background])
    for background in ("caretRow", "chunk", "selection", "underCaret", "braceBg", "searchBg", "border", "hover",
                       "writeCaret"):
        out[f"text on {background}"] = dict(fg=c["fg"], bg=c[background])
    out["line number of the current line"] = dict(fg=c["lineNoCaret"], bg=c["caretRow"])
    caret = "#" + p.get("caret", p["gold"])
    out["caret"] = dict(fg=caret, bg=c["bg"])
    out["text under the terminal cursor"] = dict(fg=c["bg"], bg=caret)
    out["link"] = dict(fg=c["azure"], bg=c["bg"])
    for i, colour in enumerate(rainbow(p)):
        out[f"rainbow parenthesis {i}"] = dict(fg=colour, bg=c["bg"])
    for i, colour in enumerate(ansi(p)):
        if i:  # black colours backgrounds and faint text
            out[f"terminal colour {i}"] = dict(fg=colour, bg=c["bg"])
    return out


def low_contrast(p):
    """The labels of styles() that need 3:1 only: comments, as in every target, the caret and the text under the
    terminal's block cursor, the one character that a highlight draws a bracket on, and text on the line that marks an
    error."""
    labels = {"caret", "text under the terminal cursor", "text on braceBg", "text on border"}
    for selectors, role, _ in syntax(p):
        if role == "comment":
            labels.update(selectors[0] + where for _, where in BACKGROUNDS)
    return labels


# The label that no contrast is required of: the terminal's bright black, which draws faint text.
DECORATIVE = {"terminal colour 8"}
