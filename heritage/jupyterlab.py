"""JupyterLab themes generated from a palette: one extension with a stylesheet for each Heritage theme.

JupyterLab draws every colour from CSS variables, --jp-*, that the active theme's stylesheet sets. A stylesheet here
sets every variable that JupyterLab's own dark theme sets (@jupyterlab/theme-dark-extension, style/variables.css), so
none of JupyterLab's colours shows through; the build compares the names with those of that package. Sizes, fonts and
elevations are the values of JupyterLab's themes (FIXED); every colour comes from the palette.

The layers follow the Islands of the other targets: the menu bar, tool bars and status bar on the frame, the notebook
and the side panels on bgTool, the cells' editors on bg, where the palette keeps every code role readable, and menus,
dialogs and fields on surface. The syntax colours are the --jp-mirror-editor-* variables that JupyterLab's CodeMirror
theme reads, with the roles that the other targets give the constructs. The ANSI colours of cell outputs, which
JupyterLab sets to fixed values, are the palette's terminal colours.

A dark theme sets the dark ink on the fills that JupyterLab draws text on (the brand, warning, error and info colours),
and a light theme the light ink, as JupyterLab's own themes do; the fills are moved from the palette colour as far as
it takes to read at 4.5:1 on that ink.

The extension is a JupyterLab federated extension: a small plugin that registers each theme with the theme manager,
built with JupyterLab's own builder, and the stylesheets as files beside it. It ships as a Python wheel on PyPI, which
pip installs into the environment that JupyterLab runs in.
"""
import json, re

from .nvim import name  # noqa: F401 - the files take the names of Neovim's schemes
from .terminals import colours as terminal_colours, contrast
from .vscode import mix
from .wheel import pack

EXTENSION = "jupyterlab-heritage-themes"  # the extension's npm name and its folder in share/jupyter/labextensions
DISTRIBUTION = "jupyterlab-heritage-themes"  # the wheel's project name on PyPI
VENDOR = "Heritage Themes"
# The oldest JupyterLab the extension is built for and tested with, and the version of @jupyterlab/apputils that it
# shares. JupyterLab 4.6.0 ships apputils 4.7.0. The builder derives the range of a shared package from the JupyterLab
# it targets, which is newer than this one, so the extension sets the range itself.
JUPYTERLAB = "4.6"
PYTHON = "3.10"  # what JupyterLab 4.6 requires
APPUTILS = "4.7.0"
APPUTILS_RANGE = f"^{APPUTILS}"
WHITE, BLACK = "FFFFFF", "000000"

# The tokens that no palette colour sets, as JupyterLab's themes set them.
FIXED = {
    "shadow-umbra-color": "rgba(var(--jp-shadow-base-lightness), var(--jp-shadow-base-lightness), var(--jp-shadow-base-lightness), .2)",
    "shadow-penumbra-color": "rgba(var(--jp-shadow-base-lightness), var(--jp-shadow-base-lightness), var(--jp-shadow-base-lightness), .14)",
    "shadow-ambient-color": "rgba(var(--jp-shadow-base-lightness), var(--jp-shadow-base-lightness), var(--jp-shadow-base-lightness), .12)",
    "elevation-z0": "none",
    "elevation-z1": "0 2px 1px -1px var(--jp-shadow-umbra-color), 0 1px 1px 0 var(--jp-shadow-penumbra-color), 0 1px 3px 0 var(--jp-shadow-ambient-color)",
    "elevation-z2": "0 3px 1px -2px var(--jp-shadow-umbra-color), 0 2px 2px 0 var(--jp-shadow-penumbra-color), 0 1px 5px 0 var(--jp-shadow-ambient-color)",
    "elevation-z4": "0 2px 4px -1px var(--jp-shadow-umbra-color), 0 4px 5px 0 var(--jp-shadow-penumbra-color), 0 1px 10px 0 var(--jp-shadow-ambient-color)",
    "elevation-z6": "0 3px 5px -1px var(--jp-shadow-umbra-color), 0 6px 10px 0 var(--jp-shadow-penumbra-color), 0 1px 18px 0 var(--jp-shadow-ambient-color)",
    "elevation-z8": "0 5px 5px -3px var(--jp-shadow-umbra-color), 0 8px 10px 1px var(--jp-shadow-penumbra-color), 0 3px 14px 2px var(--jp-shadow-ambient-color)",
    "elevation-z12": "0 7px 8px -4px var(--jp-shadow-umbra-color), 0 12px 17px 2px var(--jp-shadow-penumbra-color), 0 5px 22px 4px var(--jp-shadow-ambient-color)",
    "elevation-z16": "0 8px 10px -5px var(--jp-shadow-umbra-color), 0 16px 24px 2px var(--jp-shadow-penumbra-color), 0 6px 30px 5px var(--jp-shadow-ambient-color)",
    "elevation-z20": "0 10px 13px -6px var(--jp-shadow-umbra-color), 0 20px 31px 3px var(--jp-shadow-penumbra-color), 0 8px 38px 7px var(--jp-shadow-ambient-color)",
    "elevation-z24": "0 11px 15px -7px var(--jp-shadow-umbra-color), 0 24px 38px 3px var(--jp-shadow-penumbra-color), 0 9px 46px 8px var(--jp-shadow-ambient-color)",
    "border-width": "1px",
    "border-radius": "2px",
    "ui-font-scale-factor": "1.2",
    "ui-font-size0": ".83333em",
    "ui-font-size1": "13px",
    "ui-font-size2": "1.2em",
    "ui-font-size3": "1.44em",
    "ui-font-family": 'system-ui, -apple-system, blinkmacsystemfont, "Segoe UI", helvetica, arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol"',
    "content-line-height": "1.6",
    "content-font-scale-factor": "1.2",
    "content-font-size0": ".83333em",
    "content-font-size1": "14px",
    "content-font-size2": "1.2em",
    "content-font-size3": "1.44em",
    "content-font-size4": "1.728em",
    "content-font-size5": "2.0736em",
    "content-presentation-font-size1": "17px",
    "content-heading-line-height": "1",
    "content-heading-margin-top": "1.2em",
    "content-heading-margin-bottom": ".8em",
    "content-heading-font-weight": "500",
    "content-font-family": 'system-ui, -apple-system, blinkmacsystemfont, "Segoe UI", helvetica, arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol"',
    "datagrid-font-size": "12px",
    "datagrid-font-family": "var(--jp-content-font-family)",
    "code-font-size": "13px",
    "code-line-height": "1.3077",
    "code-padding": "5px",
    "code-font-family-default": 'menlo, consolas, "DejaVu Sans Mono", monospace',
    "code-font-family": "var(--jp-code-font-family-default)",
    "code-presentation-font-size": "16px",
    "code-cursor-width0": "1.4px",
    "code-cursor-width1": "2px",
    "code-cursor-width2": "4px",
    "cell-padding": "5px",
    "cell-collapser-width": "8px",
    "cell-collapser-min-height": "20px",
    "cell-collapser-not-active-hover-opacity": ".6",
    "cell-prompt-width": "64px",
    "cell-prompt-font-family": "var(--jp-code-font-family-default)",
    "cell-prompt-letter-spacing": "0",
    "cell-prompt-opacity": "1",
    "cell-prompt-not-active-opacity": "1",
    "notebook-padding": "10px",
    "notebook-scroll-padding": "calc(100% - var(--jp-code-font-size) * var(--jp-code-line-height) - var(--jp-code-padding) - var(--jp-cell-padding) - 1px)",
    "editor-scroll-padding": "calc(100% - var(--jp-code-font-size) * var(--jp-code-line-height) - var(--jp-code-padding) - 1px)",
    "console-padding": "10px",
    "toolbar-micro-height": "8px",
    "toolbar-header-margin": "4px 4px 0 4px",
    "statusbar-height": "24px",
    "sidebar-min-width": "250px",
    "scrollbar-endpad": "3px",
    "scrollbar-thumb-margin": "3.5px",
    "scrollbar-thumb-radius": "9px",
    "focus-outline-width": "2px",
}
# The collaborators' cursor colours are JupyterLab's own: they tell users apart, not themes.
COLLABORATORS = {
    True: ("#ad4a00", "#7b6a00", "#007e00", "#008772", "#0079b9", "#8b45c6", "#be208b"),
    False: ("#ffad8e", "#dac83d", "#72dd76", "#00e4d0", "#45d4ff", "#e2b1ff", "#ff9de6"),
}
COMPLETER_ROLES = ("keyword", "method", "type", "string", "azure", "constant", "field", "muted", "annotation",
                   "typeParam")
ANSI_NAMES = ("black", "red", "green", "yellow", "blue", "magenta", "cyan", "white")


def rgba(colour, alpha):
    return "rgba(%d,%d,%d,%s)" % (*(int(colour[i:i + 2], 16) for i in (0, 2, 4)), alpha)


def triple(colour):
    return ", ".join(str(int(colour[i:i + 2], 16)) for i in (0, 2, 4))


def legible(colour, ink, minimum=4.5):
    """colour, moved away from the ink as little as it takes to reach minimum:1 on it. The fill of text that
    JupyterLab draws in the ink."""
    away = WHITE if ink == BLACK else BLACK
    return next(mix(colour, away, step / 20) for step in range(21) if contrast(ink, mix(colour, away, step / 20)) >= minimum)


def darkened(colour, minimum):
    """colour, darkened as little as it takes to reach minimum:1 with white text, which the dialogs' buttons draw."""
    return legible(colour, WHITE, minimum)


def tinted(base, accent, texts, ceiling):
    """base with as much of accent as keeps every text at its minimum contrast, up to ceiling of it. texts are
    (colour, minimum) pairs."""
    return next((mix(base, accent, step / 20) for step in range(round(ceiling * 20), -1, -1)
                 if all(contrast(text, mix(base, accent, step / 20)) >= minimum for text, minimum in texts)), base)


def ramp(role, ink, tints=2):
    """The shades of a status colour: a darker one, the fill that the ink reads on, and tints of it."""
    fill = legible(role, ink)
    return [legible(mix(fill, BLACK, 0.25), ink), fill] + [mix(fill, WHITE, amount) for amount in (0.45, 0.8, 0.93)[:tints]]


def ink(p):
    """The text colour of the fills that JupyterLab draws text on: black on a dark theme's light fills, white on a
    light theme's dark ones."""
    return BLACK if p["dark"] else WHITE


def ansi_fills(p):
    """The 16 ANSI colours as RRGGBB, normal then bright."""
    return [colour[1:] for colour in terminal_colours(p)["ansi"]]


def colour_groups(p):
    """(comment, {variable without --jp-: value}) in the order of the stylesheet."""
    h = lambda role: "#" + p[role]
    text = ink(p)
    inverse = ("#000", "#000", rgba(BLACK, ".5"), rgba(BLACK, ".3")) if p["dark"] else \
        ("#fff", "#fff", rgba(WHITE, ".7"), rgba(WHITE, ".5"))
    brand = ramp(p["gold"], text, 3)
    accent, warn, error, info = (ramp(p[role], text) for role in ("added", "warning", "error", "string"))
    accept, danger, reject = (tuple(darkened(p[role], minimum) for minimum in (4.6, 6, 8))
                              for role in ("azure", "error", "muted"))
    badge = darkened(p["azure"], 4.6)
    # An error output's tint tells stderr from stdout. Its text keeps 4.5:1 and the ANSI red of a traceback 3:1, so
    # that a palette with little room for the red still has a tint.
    error_background = tinted(p["bgTool"], p["error"], ((p["fg"], 4.5), (p["ansiRed"], 3)), 0.3)
    selected = tinted(p["bgTool"], p["gold"], ((p["fg"], 4.5),), 0.2)
    glow = "inset 0 0 2px " + rgba(p["gold"], ".5")
    return [
        ("Layers: the notebook and side panels, menus, rows under the pointer, the chrome", {
            "layout-color0": h("bgTool"), "layout-color1": h("surface"), "layout-color2": h("hover"),
            "layout-color3": h("frame"), "layout-color4": h("lineNo"),
            "inverse-layout-color0": h("fg"), "inverse-layout-color1": h("fg"), "inverse-layout-color2": h("fg"),
            "inverse-layout-color3": h("muted"), "inverse-layout-color4": h("muted"),
            "border-color0": h("lineNo"), "border-color1": h("border"), "border-color2": h("hover"),
            "border-color3": h("surface"), "inverse-border-color": h("lineNo"),
            "shadow-base-lightness": "32" if p["dark"] else "0",
        }),
        ("Text", {
            "ui-font-color0": h("fg"), "ui-font-color1": h("fg"), "ui-font-color2": h("muted"),
            "ui-font-color3": h("disabled"),
            "ui-inverse-font-color0": inverse[0], "ui-inverse-font-color1": inverse[1],
            "ui-inverse-font-color2": inverse[2], "ui-inverse-font-color3": inverse[3],
            "content-font-color0": h("fg"), "content-font-color1": h("fg"), "content-font-color2": h("muted"),
            "content-font-color3": h("disabled"),
            "content-link-color": h("azure"), "content-link-visited-color": h("constant"),
            "content-link-hover-color": h("typeParam"),
        }),
        ("Brand, accent, warning, error, success and info", {
            **{f"{n}-color{i}": "#" + shade for n, shades in (("brand", brand), ("accent", accent), ("warn", warn),
                                                              ("error", error), ("success", accent),
                                                              ("info", info))
               for i, shade in enumerate(shades)},
        }),
        ("Cells and the notebook", {
            "cell-editor-background": h("bg"), "cell-editor-border-color": h("border"),
            "cell-editor-box-shadow": glow, "cell-editor-active-background": h("bg"),
            "cell-editor-active-border-color": h("gold"),
            "cell-prompt-not-active-font-color": h("muted"), "cell-inprompt-font-color": h("azure"),
            "cell-outprompt-font-color": h("keyword"),
            "notebook-select-background": h("surface"), "notebook-multiselected-color": "#" + selected,
            "rendermime-error-background": "#" + error_background,
            "rendermime-table-row-background": h("surface"), "rendermime-table-row-hover-background": h("hover"),
            "dialog-background": rgba(p["bg"], ".6") if p["dark"] else rgba(p["fg"], ".25"),
        }),
        ("Tool bars, fields and the editor", {
            "toolbar-border-color": h("border"), "toolbar-background": h("frame"),
            "toolbar-box-shadow": "0 0 2px 0 " + (rgba(BLACK, ".8") if p["dark"] else rgba(BLACK, ".24")),
            "toolbar-active-background": h("bgTool"),
            "input-box-shadow": glow, "input-active-background": h("bg"), "input-hover-background": h("hover"),
            "input-background": h("surface"), "input-border-color": h("lineNo"),
            "input-active-border-color": h("gold"), "input-active-box-shadow-color": rgba(p["gold"], ".3"),
            "editor-selected-background": h("selInactive"), "editor-selected-focused-background": h("selection"),
            "editor-cursor-color": "#" + p.get("caret", p["gold"]),
        }),
        ("Syntax", {
            "mirror-editor-keyword-color": h("keyword"), "mirror-editor-atom-color": h("constant"),
            "mirror-editor-number-color": h("number"), "mirror-editor-def-color": h("method"),
            "mirror-editor-variable-color": h("param"), "mirror-editor-variable-2-color": h("call"),
            "mirror-editor-variable-3-color": h("type"), "mirror-editor-punctuation-color": h("op"),
            "mirror-editor-property-color": h("field"), "mirror-editor-operator-color": h("op"),
            "mirror-editor-comment-color": h("comment"), "mirror-editor-string-color": h("string"),
            "mirror-editor-string-2-color": h("label"), "mirror-editor-meta-color": h("annotation"),
            "mirror-editor-qualifier-color": h("muted"), "mirror-editor-builtin-color": h("type"),
            "mirror-editor-bracket-color": h("op"), "mirror-editor-tag-color": h("keyword"),
            "mirror-editor-attribute-color": h("typeParam"), "mirror-editor-header-color": h("gold"),
            "mirror-editor-quote-color": h("doc"), "mirror-editor-link-color": h("azure"),
            "mirror-editor-error-color": h("error"), "mirror-editor-hr-color": h("muted"),
        }),
        ("Search, scroll bars, collaborators and charts", {
            "search-selected-match-background-color": h("gold"), "search-selected-match-color": h("bg"),
            "search-unselected-match-background-color": h("searchBg"), "search-unselected-match-color": h("fg"),
            "scrollbar-background-color": h("surface"), "scrollbar-thumb-color": triple(p["muted"]),
            **{f"collaborator-color{i}": colour for i, colour in enumerate(COLLABORATORS[p["dark"]], 1)},
            "vega-background": h("fg") if p["dark"] else h("bg"),
        }),
        ("Icons and switches", {
            "icon-contrast-color0": h("constant"), "icon-contrast-color1": h("type"),
            "icon-contrast-color2": h("field"), "icon-contrast-color3": h("azure"),
            "jupyter-icon-color": "#f37626", "notebook-icon-color": "#f37626", "json-icon-color": h("warning"),
            "console-icon-background-color": "#" + badge, "console-icon-color": "#fff",
            "terminal-icon-background-color": h("fg"), "terminal-icon-color": h("bg"),
            "text-editor-icon-color": h("fg"), "inspector-icon-color": h("fg"),
            "switch-color": h("lineNo"), "switch-true-position-color": h("gold"),
            "focus-outline-color": h("gold"),
        }),
        ("Buttons: the dialogs draw white text on these", {
            "shortcuts-button-background": "var(--jp-brand-color2)" if p["dark"] else "var(--jp-brand-color3)",
            "shortcuts-button-hover-background": "var(--jp-brand-color1)" if p["dark"] else "var(--jp-brand-color2)",
            **{f"{n}-color-{state}": "#" + fill for n, fills in (("accept", accept), ("warn", danger),
                                                                 ("reject", reject))
               for state, fill in zip(("normal", "hover", "active"), fills)},
        }),
    ]


def colours(p):
    """Every variable the palette sets, without the --jp- prefix."""
    return {name_: value for _, group in colour_groups(p) for name_, value in group.items()}


def variables(p):
    """Variable → value for a palette: JupyterLab's fixed tokens, then the colours."""
    return {**FIXED, **colours(p)}


def completer(p):
    """The completer's type badges, in the palette's hues."""
    return ["transparent"] + ["#" + p[role] for role in COMPLETER_ROLES]


def ansi_rules(p):
    """JupyterLab's ANSI classes for cell outputs, which it sets to fixed colours, in the palette's terminal colours."""
    fills = ansi_fills(p)
    rules = []
    for index, colour_name in enumerate(ANSI_NAMES):
        normal, intense = "#" + fills[index], "#" + fills[index + 8]
        for suffix, value in ((colour_name, normal), (f"{colour_name}-intense", intense)):
            rules.append((f".jp-RenderedText pre .ansi-{suffix}-fg", f"color: {value};"))
            rules.append((f".jp-RenderedText pre .ansi-{suffix}-bg", f"background-color: {value};"))
    return rules


# The colours that JupyterLab draws and no theme sets: the Python file icon in the file browser, white, which the logo
# and the buttons' text use, and black, which the logo uses and the shadows of menus and dialogs, translucent black,
# blend with every colour.
ICON_COLOURS = ("#FFFFFF", "#000000", "#FFD43B", "#306998", "#E4D1A7")


def pixel_palette(p, dimmed=False, page="bgTool"):
    """What scripts/editors/pixels.py checks a screenshot of JupyterLab against: every colour the stylesheet sets, which
    is every colour JupyterLab draws, ICON_COLOURS, and the layers that text sits on, among them the fills of the
    dialogs' buttons and ICON_COLOURS, which the edges of icons and shadows blend with. The notebook, the editor and the
    menu are drawn on bgTool, and Notebook 7's file page on surface, which is the page layer that most of a screenshot
    shows. With dimmed, the page is drawn under a dialog's backdrop, so each colour also appears
    blended with it."""
    hexes = {value.upper() for value in colours(p).values() if re.fullmatch(r"#[0-9A-Fa-f]{6}", value)}
    hexes |= {"#" + c.upper() for c in ansi_fills(p)} | {"#" + p[k] for k in ("bg", "fg")} | set(ICON_COLOURS)
    layers = ["#" + p[k] for k in ("bg", "frame", "surface", "caretRow", "selection", "hover")]
    layers += [colours(p)["rendermime-error-background"], *ICON_COLOURS]
    layers += [value.upper() for key, value in colours(p).items()
               if re.fullmatch(r"(accept|warn|reject)-color-(normal|hover|active)", key)]
    background = "#" + p[page]
    if dimmed:
        red, green, blue, alpha = re.fullmatch(r"rgba\((\d+),(\d+),(\d+),([\d.]+)\)",
                                              colours(p)["dialog-background"]).groups()
        backdrop, alpha = (int(red), int(green), int(blue)), float(alpha)

        def under(colour):
            return "#%02X%02X%02X" % tuple(round(int(colour[i:i + 2], 16) * (1 - alpha) + c * alpha)
                                           for i, c in zip((1, 3, 5), backdrop))
        hexes |= {under(c) for c in hexes}
        layers += [under(c) for c in layers] + [under(background)]
        background = under(background)
    # Chrome rounds each blend with the backdrop by itself, so the dimmed background is within 2 of the computed one
    return dict(background=background, backgrounds=layers, foregrounds=sorted(hexes), crop=[0, 0, 0, 0],
                rounding=2 if dimmed else 0)


def stylesheet(t, source):
    """The stylesheet of a theme dict. source is the URL of the theme folder."""
    p = t["palette"]
    lines = [f"/* {p['name']}: a Heritage Themes theme for JupyterLab. Generated from {source}; changes here are "
             "overwritten. */", ":root {", "  /* JupyterLab's sizes, fonts and elevations */"]
    lines += [f"  --jp-{key}: {value};" for key, value in FIXED.items()]
    for comment, group in colour_groups(p):
        lines += [f"  /* {comment} */"] + [f"  --jp-{key}: {value};" for key, value in group.items()]
    lines += ["}", "", ".jp-Completer {"]
    lines += [f"  --jp-completer-type-background{i}: {value};" for i, value in enumerate(completer(p))]
    lines += ["}", "", "/* The monospace elements of rendered content use the code font */",
              ".jp-ThemedContainer tt,\n.jp-ThemedContainer code,\n.jp-ThemedContainer kbd,\n"
              ".jp-ThemedContainer samp,\n.jp-ThemedContainer pre {",
              "  font-family: var(--jp-code-font-family);", "  font-size: var(--jp-code-font-size);",
              "  line-height: var(--jp-code-line-height);", "}", "", "/* ANSI colours in cell outputs */"]
    for selector, declaration in ansi_rules(p):
        lines += [f"{selector} {{", f"  {declaration}", "}"]
    if p["dark"]:
        lines += ["", "/* Yellow text on a yellow background in a traceback is unreadable */",
                  ":where(.jp-RenderedText[data-mime-type='application/vnd.jupyter.stderr'] pre .ansi-yellow-bg) {",
                  "  color: black;", "}"]
    return "\n".join(lines) + "\n"


def styles(p):
    """Element → dict(fg, bg) as #RRGGBB, for the build's contrast check: the code, the text on each layer, and the
    text on the fills that JupyterLab draws it on."""
    c = colours(p)
    text = ink(p)
    out = {f"code {role}": dict(fg="#" + p[role], bg="#" + p["bg"])
           for role in ("keyword", "string", "number", "type", "method", "call", "field", "constant", "annotation",
                        "param", "typeParam", "op", "doc", "azure", "label")}
    out["code comment"] = dict(fg="#" + p["comment"], bg="#" + p["bg"])
    out["code on the caret row"] = dict(fg="#" + p["keyword"], bg="#" + p["caretRow"])
    for element, fg, bg in (("editor text", "fg", "bg"), ("notebook text", "fg", "bgTool"),
                            ("muted notebook text", "muted", "bgTool"), ("panel text", "fg", "surface"),
                            ("muted panel text", "muted", "surface"), ("chrome text", "fg", "frame"),
                            ("muted chrome text", "muted", "frame"), ("hovered text", "fg", "hover"),
                            ("selected text", "fg", "selection"), ("unfocused selection", "fg", "selInactive"),
                            ("link", "azure", "bgTool"), ("input prompt", "azure", "bgTool"),
                            ("output prompt", "keyword", "bgTool"), ("search match", "fg", "searchBg"),
                            ("selected search match", "bg", "gold")):
        out[element] = dict(fg="#" + p[fg], bg="#" + p[bg])
    for index, colour_name in enumerate(ANSI_NAMES):
        if colour_name != "black":
            out[f"ANSI {colour_name}"] = dict(fg="#" + ansi_fills(p)[index], bg="#" + p["bgTool"])
            out[f"ANSI intense {colour_name}"] = dict(fg="#" + ansi_fills(p)[index + 8], bg="#" + p["bgTool"])
    out["text on an error output"] = dict(fg="#" + p["fg"], bg=c["rendermime-error-background"])
    out["red text on an error output"] = dict(fg="#" + p["ansiRed"], bg=c["rendermime-error-background"])
    out["text on selected cells"] = dict(fg="#" + p["fg"], bg=c["notebook-multiselected-color"])
    for status in ("brand", "accent", "warn", "error", "info"):
        out[f"{status} fill"] = dict(fg="#" + text, bg=c[f"{status}-color1"])
    for state in ("normal", "hover", "active"):
        for button in ("accept", "warn", "reject"):
            out[f"{button} button {state}"] = dict(fg="#FFFFFF", bg=c[f"{button}-color-{state}"])
    out["console icon"] = dict(fg="#FFFFFF", bg=c["console-icon-background-color"])
    for i, value in enumerate(completer(p)[1:], 1):
        out[f"completer badge {i}"] = dict(fg="#" + text, bg=value)
    return out


def plugin_source(themes):
    """src/index.ts, which registers every theme with JupyterLab's theme manager."""
    entries = ",\n".join(f"  [{json.dumps(t['palette']['name'])}, {str(not t['palette']['dark']).lower()}, "
                         f"{json.dumps(name(t))}]" for t in themes)
    return f"""import {{ JupyterFrontEndPlugin }} from '@jupyterlab/application';
import {{ IThemeManager }} from '@jupyterlab/apputils';

/** Each theme's name, whether it is light, and its stylesheet in this extension's themes folder. */
const THEMES: [string, boolean, string][] = [
{entries}
];

/**
 * Registers the Heritage Themes with JupyterLab's theme manager. The manager loads a theme's stylesheet when the user
 * chooses it and removes it when they choose another.
 */
const plugin: JupyterFrontEndPlugin<void> = {{
  id: '{EXTENSION}:plugin',
  description: 'Heritage Themes',
  autoStart: true,
  requires: [IThemeManager],
  activate: (_app, manager: IThemeManager) => {{
    for (const [name, isLight, file] of THEMES) {{
      const style = `{EXTENSION}/${{file}}.css`;
      manager.register({{
        name,
        isLight,
        themeScrollbars: true,
        load: () => manager.loadCSS(style),
        unload: () => Promise.resolve(undefined)
      }});
    }}
  }}
}};

export default plugin;
"""


def package_json(version, vendor_url):
    """The extension's package.json for the builder: the plugin's entry point, and the range of apputils that the
    host must provide."""
    return json.dumps({
        "name": EXTENSION, "version": version, "description": "Heritage Themes for JupyterLab",
        "keywords": ["jupyter", "jupyterlab", "jupyterlab-extension", "theme"], "homepage": vendor_url,
        "license": "MIT", "author": VENDOR, "main": "lib/index.js", "types": "lib/index.d.ts",
        # a range that the host's version satisfies, which `jupyter labextension list` checks
        "dependencies": {"@jupyterlab/apputils": APPUTILS_RANGE},
        "jupyterlab": {"extension": True, "outputDir": "labextension",
                       "sharedPackages": {"@jupyterlab/apputils": {"requiredVersion": APPUTILS_RANGE}}},
    }, indent=2) + "\n"


def tsconfig():
    return json.dumps({
        "compilerOptions": {"allowSyntheticDefaultImports": True, "declaration": True, "esModuleInterop": True,
                            "module": "esnext", "moduleResolution": "node", "noEmitOnError": True,
                            "noImplicitAny": True, "noUnusedLocals": True, "outDir": "lib", "rootDir": "src",
                            "strict": True, "target": "ES2018"},
        "include": ["src/**/*"],
    }, indent=2) + "\n"


def install_json():
    """install.json, which tells `jupyter labextension list` and the extension manager how the extension was
    installed."""
    return json.dumps({"packageManager": "python", "packageName": DISTRIBUTION,
                       "uninstallInstructions": "Use your Python package manager (pip, conda, etc.) to uninstall "
                                                f"the package {DISTRIBUTION}"}, indent=2) + "\n"


def wheel_name(version):
    return f"{DISTRIBUTION.replace('-', '_')}-{version}-py3-none-any.whl"


def metadata(version, vendor_url, description):
    """The wheel's METADATA: the project's name, its requirement on JupyterLab and its description."""
    headers = ["Metadata-Version: 2.1", f"Name: {DISTRIBUTION}", f"Version: {version}",
               "Summary: Heritage Themes for JupyterLab", f"Home-page: {vendor_url}", f"Author: {VENDOR}",
               "License: MIT", "Classifier: License :: OSI Approved :: MIT License",
               "Classifier: Framework :: Jupyter", "Classifier: Framework :: Jupyter :: JupyterLab",
               "Classifier: Framework :: Jupyter :: JupyterLab :: 4",
               "Classifier: Framework :: Jupyter :: JupyterLab :: Extensions",
               "Classifier: Framework :: Jupyter :: JupyterLab :: Extensions :: Prebuilt",
               "Classifier: Framework :: Jupyter :: JupyterLab :: Extensions :: Themes",
               "Classifier: Programming Language :: Python :: 3", f"Project-URL: Issues, {vendor_url}/issues",
               f"Requires-Python: >={PYTHON}", f"Requires-Dist: jupyterlab>={JUPYTERLAB}", "Requires-Dist: jupyterlab<5",
               "Description-Content-Type: text/markdown"]
    return "\n".join(headers) + "\n\n" + description


def wheel(files, version, vendor_url, description, licence):
    """The wheel as bytes. files maps a path in the extension's folder to its bytes; pip installs the extension under
    share/jupyter/labextensions, where JupyterLab looks for it."""
    data = f"{DISTRIBUTION.replace('-', '_')}-{version}.data/data/share/jupyter/labextensions/{EXTENSION}"
    return pack(DISTRIBUTION, version, {f"{data}/{path}": content for path, content in files.items()},
                metadata(version, vendor_url, description), licence)
