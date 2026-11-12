"""Thonny themes generated from a palette: a UI theme and a syntax theme for each Heritage theme, in one plugin.

Thonny keeps the colours of its window and of its code apart. A UI theme sets the ttk colours of the window: frames,
tabs, buttons, scrollbars, entries, trees and menus. A syntax theme sets the Tk tags of the editor and the shell: the
text and its background, the gutter, the current line, the selection, one colour for each kind of token that Thonny's
own highlighter finds, the shell's output, the debugger's focus boxes and the 24 ANSI colours that a program can print.
Thonny lists the two kinds separately under Tools | Options | Theme & Font, so a Heritage theme is two choices of the
same name.

The roles are those that heritage.spyder, heritage.pygments and heritage.vscode give the matching constructs. Thonny
colours keywords, builtins, numbers, comments, strings, the name after def and class, and function and method calls; it
gives every other name the text colour, so only those take a role. A syntax theme names the tags that it sets. Thonny's
Default Light or Default Dark theme sets the rest: the borders and relief of the debugger's boxes, the fonts of the
shell and the underline of links.

A UI theme is Thonny's own `clean` theme, called with the palette's colours. Its parent is Clean Dark for a dark
theme, so that Thonny treats the window as dark, as it does for the icons of its help pages and of the tab close
button, and Enhanced Clam for a light one.

The plugin ships as a wheel on PyPI and on the GitHub release. Thonny's plug-in manager installs it into the
`thonnycontrib` namespace package, from which Thonny loads every plugin, so the wheel holds one module there.
"""
import inspect, re

from .nvim import terminal
from .vscode import mix
from .wheel import pack

DISTRIBUTION = "thonny-heritage-themes"  # the wheel's project name on PyPI; Thonny's plug-in manager lists thonny-*
PACKAGE = "heritage_themes"  # the plugin's module in thonnycontrib
VENDOR = "Heritage Themes"
PREFIX = "Heritage "  # a theme's name in Thonny's lists, so that the themes sit together among its own
# The oldest Thonny and Python that the plugin is tested with.
THONNY = "4.0"
PYTHON = "3.8"
# The roles of the 24 ANSI colours: Thonny's black, red, green, yellow, blue, magenta, cyan and white, then the same
# eight bright, then the same eight dim.
ANSI_NAMES = ("black", "red", "green", "yellow", "blue", "magenta", "cyan", "white")
HEX = re.compile(r"#[0-9A-F]{6}")


def name(t):
    """The name of a theme dict from a theme.py in Thonny's lists, for example "Heritage Holi Night"."""
    return PREFIX + t["palette"]["name"]


def ui(p):
    """The colours of a UI theme, as #RRGGBB, in the order of the plugin's ui_theme. Windows and toolbars are on bgUi,
    the editor's colour is bg, tabs, buttons and scrollbars are the frame colour, and what the pointer is over or what
    is selected takes the selection colour, with the text colour on it. Menus are on the surface colour that the IDE's
    popups use."""
    return tuple("#" + p[role] for role in ("bgUi", "bg", "frame", "selection", "selInactive", "fg", "disabled",
                                            "surface"))


def ansi_colours(p):
    """The 24 colours that Thonny gives its ANSI names, as #RRGGBB, in ANSI_NAMES order for normal, bright and dim: the
    terminal products' colours, with the dim ones moved 30% towards bg."""
    colours = terminal(p)
    return tuple(colours + ["#" + mix(colour[1:], p["bg"], 0.3) for colour in colours[:8]])


def tags(p):
    """tag → options of a syntax theme, without the ANSI colours: Thonny's tags, in the order the plugin lists them."""
    bold = "BoldEditorFont" if p.get("kwBold", not p["dark"]) else "EditorFont"
    fg, bg, caret_row = "#" + p["fg"], "#" + p["bg"], "#" + p["caretRow"]
    c = {role: "#" + p[role] for role in (
        "method", "call", "type", "string", "number", "comment", "keyword", "muted", "constant", "azure",
        "ansiRed", "braceBg", "underCaret", "selInactive", "searchBg", "gold", "writeCaret", "selection", "lineNo",
        "diffConf", "diffIns", "diffDel", "diffMod")}
    string = {"foreground": c["string"], "font": "EditorFont"}
    return {
        "TEXT": {"foreground": fg, "insertbackground": "#" + p.get("caret", p["gold"]), "background": bg,
                 "inactiveselectbackground": c["selInactive"]},
        "GUTTER": {"foreground": c["lineNo"], "background": bg},
        "breakpoint": {"foreground": c["ansiRed"]},
        "current_line": {"background": caret_row},
        "sel": {"foreground": fg, "background": c["selection"]},
        "definition": {"foreground": c["method"], "font": "BoldEditorFont"},
        "class_definition": {"foreground": c["type"], "font": "EditorFont"},
        "function_definition": {"foreground": c["method"], "font": "BoldEditorFont"},
        "string": string,
        "string3": dict(string),
        "open_string": {**string, "background": c["writeCaret"]},
        "open_string3": {**string, "background": c["writeCaret"]},
        "tab": {"background": c["diffConf"]},
        "keyword": {"foreground": c["keyword"], "font": bold},
        "builtin": {"foreground": c["call"], "font": "ItalicEditorFont"},
        "number": {"foreground": c["number"]},
        "comment": {"foreground": c["comment"], "font": "ItalicEditorFont"},
        "magic": {"foreground": c["keyword"], "font": bold},
        "function_call": {"foreground": c["call"]},
        "method_call": {"foreground": c["call"]},
        "welcome": {"foreground": c["muted"]},
        "prompt": {"foreground": c["muted"], "font": "BoldEditorFont"},
        "stdin": {"foreground": c["azure"]},
        "stdout": {"foreground": fg},
        "stderr": {"foreground": c["ansiRed"]},
        "value": {"foreground": c["constant"]},
        "hyperlink": {"foreground": c["azure"]},
        "surrounding_parens": {"foreground": fg, "background": c["braceBg"], "font": "BoldEditorFont"},
        "unclosed_expression": {"background": caret_row},
        "found": {"foreground": "", "background": c["searchBg"], "underline": False},
        "current_found": {"foreground": bg, "background": c["gold"]},
        "matched_name": {"background": c["underCaret"]},
        "active_focus": {"background": c["diffConf"]},
        "completed_focus": {"background": c["diffIns"]},
        "exception_focus": {"background": c["diffDel"]},
        "expression_box": {"foreground": fg, "background": c["diffMod"]},
    }


def ansi_tags(colours, fg, muted, bg):
    """tag → options of the ANSI colours: a foreground and a background tag for each name that a program can print.
    colours is the 24 colours of ansi_colours, in the order of ANSI_NAMES for normal, bright and dim. The names fore and
    back are the colours of the text and of its background: fg, fg and muted for fore, and bg for back."""
    names = ("black", "red", "green", "yellow", "blue", "magenta", "cyan", "white")
    out = {}
    for group, prefix in enumerate(("", "bright_", "dim_")):
        for ansi_name, colour in zip(names, colours[group * 8:group * 8 + 8]):
            out[f"{prefix}{ansi_name}_fg"] = {"foreground": colour}
            out[f"{prefix}{ansi_name}_bg"] = {"background": colour}
        fore = muted if prefix == "dim_" else fg
        out[f"{prefix}fore_fg"] = {"foreground": fore}
        out[f"{prefix}fore_bg"] = {"background": fore}
        out[f"{prefix}back_fg"] = {"foreground": bg}
        out[f"{prefix}back_bg"] = {"background": bg}
    return out


def ground(p):
    """The fg, muted and bg arguments of ansi_tags for a palette, as #RRGGBB."""
    return "#" + p["fg"], "#" + p["muted"], "#" + p["bg"]


def syntax(p):
    """tag → options of a syntax theme: its own tags, then the ANSI colours."""
    return {**tags(p), **ansi_tags(ansi_colours(p), *ground(p))}


# The plugin module: the generated table of themes, and the code that registers them. {table} is the table, and
# {ansi_tags} the source of ansi_tags above, so that the plugin and the build use one function.
PLUGIN = '''"""Heritage Themes for Thonny: a UI theme and a syntax theme for each theme, such as "{example}".

Choose them under Tools | Options | Theme & Font. Generated from
{source}; changes here are overwritten.
"""
from functools import partial

from thonny import get_workbench

# name -> (dark, UI colours, tags, ANSI colours, fg, muted and bg)
# The UI colours are the arguments of ui_theme, in order. The tags are those of Thonny's highlighter, the shell and the
# debugger that a theme sets. The 24 ANSI colours are normal, bright and dim, each in the order black, red, green,
# yellow, blue, magenta, cyan and white.
THEMES = {{
{table}}}


{ansi_tags}


def ui_theme(frame_background, text_background, normal_detail, high_detail, low_detail, foreground, low_foreground,
             menu_background):
    """The settings of a UI theme: Thonny's clean theme, with the menus on one background and a selected menu entry on
    the colour of the other selections instead of in the text colour."""
    from thonny.plugins.clean_ui_themes import clean

    settings = clean(frame_background=frame_background, text_background=text_background, normal_detail=normal_detail,
                     high_detail=high_detail, low_detail=low_detail, normal_foreground=foreground,
                     high_foreground=foreground, low_foreground=low_foreground)
    settings["Menubar"]["configure"].update(activebackground=high_detail, activeforeground=foreground)
    settings["Menu"]["configure"].update(background=menu_background, foreground=foreground,
                                         activebackground=high_detail, activeforeground=foreground,
                                         selectcolor=foreground)
    return settings


def syntax_theme(tags, ansi_colours, fg, muted, bg):
    """The settings of a syntax theme: a copy of its tags, then the ANSI colours."""
    settings = {{tag: dict(options) for tag, options in tags.items()}}
    settings.update(ansi_tags(ansi_colours, fg, muted, bg))
    return settings


def load_plugin():
    workbench = get_workbench()
    for name, (dark, ui, tags, ansi_colours, ground) in THEMES.items():
        workbench.add_ui_theme(name, "Clean Dark" if dark else "Enhanced Clam", partial(ui_theme, *ui))
        workbench.add_syntax_theme(name, "Default Dark" if dark else "Default Light",
                                   partial(syntax_theme, tags, ansi_colours, *ground))
'''


def literal(value, indent=0):
    """A Python literal for a str, bool, tuple or dict of them, with one dict entry to a line past the first level."""
    pad = " " * indent
    if isinstance(value, bool):
        return repr(value)
    if isinstance(value, str):
        return f'"{value}"'
    if isinstance(value, tuple):
        return "(" + ", ".join(literal(v) for v in value) + ")"
    if isinstance(value, dict):
        if indent >= 12:
            return "{" + ", ".join(f"{literal(k)}: {literal(v)}" for k, v in value.items()) + "}"
        lines = (f"{pad}    {literal(k)}: {literal(v, indent + 4)},\n" for k, v in value.items())
        return "{\n" + "".join(lines) + pad + "}"
    raise TypeError(value)


def rows(colours):
    """The 24 ANSI colours as a tuple literal of three lines, one for each of normal, bright and dim."""
    lines = (literal(tuple(colours[i:i + 8])) for i in (0, 8, 16))
    return "(\n" + "".join(f"            {line[1:-1]},\n" for line in lines) + "        )"


def table(themes):
    """The THEMES table's entries as source text. themes is a list of theme dicts from a theme.py."""
    out = []
    for t in themes:
        p = t["palette"]
        out.append(f"    {literal(name(t))}: (\n        {literal(p['dark'])},\n        {literal(ui(p))},\n"
                   f"        {literal(tags(p), 8)},\n        {rows(ansi_colours(p))},\n"
                   f"        {literal(ground(p))},\n    ),\n")
    return "".join(out)


def module(themes, source):
    """The plugin module's source text. themes is a list of theme dicts from a theme.py, and source the URL of the
    repository."""
    return PLUGIN.format(example=name(themes[0]), source=source, table=table(themes),
                         ansi_tags=inspect.getsource(ansi_tags).rstrip())


def wheel_name(version):
    return f"{DISTRIBUTION.replace('-', '_')}-{version}-py3-none-any.whl"


def metadata(version, vendor_url, description):
    """The wheel's METADATA: the project's name, its requirements and its description. Thonny's plug-in manager
    refuses a thonny-* project that does not name the Thonny it needs, and lists the project by its summary."""
    headers = ["Metadata-Version: 2.1", f"Name: {DISTRIBUTION}", f"Version: {version}",
               "Summary: Heritage Themes for Thonny", f"Home-page: {vendor_url}", f"Author: {VENDOR}",
               "License: MIT", "Keywords: thonny,thonny-plugin,syntax highlighting,colour scheme,theme",
               "Classifier: Environment :: Plugins", "Classifier: Intended Audience :: Education",
               "Classifier: Intended Audience :: Developers", "Classifier: License :: OSI Approved :: MIT License",
               "Classifier: Programming Language :: Python :: 3", f"Project-URL: Issues, {vendor_url}/issues",
               f"Requires-Python: >={PYTHON}", f"Requires-Dist: thonny>={THONNY}",
               "Description-Content-Type: text/markdown"]
    return "\n".join(headers) + "\n\n" + description


def wheel(themes, version, vendor_url, description, licence):
    """The wheel as bytes. themes is a list of theme dicts from a theme.py."""
    return pack(DISTRIBUTION, version, {f"thonnycontrib/{PACKAGE}/__init__.py": module(themes, vendor_url).encode()},
                metadata(version, vendor_url, description), licence)


# The tags that no text sits on, or that only mark a place: line numbers, and the tab character's highlight.
DECORATIVE = {"GUTTER", "tab"}
# The styles that need 3:1 only: comments, as in every target; the caret; the open string, an error that Thonny paints
# over the string until it is closed, in 15 themes where the string colour is below 4.5:1 on the red tint; and the
# character that a bracket highlight sits on.
LOW_CONTRAST = {"comment", "comment on current line", "caret", "open_string", "open_string3", "surrounding_parens"}


def styles(p):
    """Element → dict(fg, bg) as #RRGGBB, for the build's contrast check. A tag with a colour is checked on its own
    background, else on the editor's and on the current line's; a tag with only a background is checked with the text
    colour on it; the 16 ANSI foreground colours that are not black are checked on the editor's background."""
    out, text = {}, tags(p)
    bg, line = text["TEXT"]["background"], text["current_line"]["background"]
    fg = text["TEXT"]["foreground"]
    for tag, options in text.items():
        if tag in DECORATIVE or tag == "current_line":
            continue
        if options.get("foreground"):
            if "background" in options:
                out[tag] = dict(fg=options["foreground"], bg=options["background"])
            else:
                out[tag] = dict(fg=options["foreground"], bg=bg)
                out[f"{tag} on current line"] = dict(fg=options["foreground"], bg=line)
        elif "background" in options:
            out[f"text on {tag}"] = dict(fg=fg, bg=options["background"])
    out["caret"] = dict(fg=text["TEXT"]["insertbackground"], bg=bg)
    out["text on inactive selection"] = dict(fg=fg, bg=text["TEXT"]["inactiveselectbackground"])
    ansi = ansi_colours(p)
    for i, ansi_name in enumerate(ANSI_NAMES):
        for group, prefix in ((0, ""), (1, "bright_")):
            if (group, i) != (0, 0):
                out[f"{prefix}{ansi_name}_fg"] = dict(fg=ansi[group * 8 + i], bg=bg)
    return out
