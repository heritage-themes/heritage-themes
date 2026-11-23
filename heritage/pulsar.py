"""Pulsar themes generated from a palette: a syntax theme and a UI theme for each theme, each its own package.

Pulsar lists a package as a theme when its package.json sets "theme" to "syntax" or "ui", and takes one of each, so a
theme ships as two packages that the user chooses together under Settings | Themes. Each package's index.less is
compiled by Pulsar with the variables of the active themes: syntax-variables.less of the syntax theme and
ui-variables.less of the UI theme, which other packages also import.

Syntax: Pulsar wraps each scope of a token in an element with a syntax--<part> class per dot-separated part, so a rule
for "entity.name.function" matches .syntax--entity.syntax--name.syntax--function. The innermost element that a rule
matches sets the colour, and among rules that match one element, the one with more classes wins, as the deeper scope
selector wins in TextMate. Pulsar's own Tree-sitter grammars name scopes in their own conventions, such as
support.other.function for a call and support.other.property for a field, so the rules here follow those scopes,
giving each the palette role that heritage.vscode gives the matching TextMate scope.

UI: the stylesheets in heritage/pulsar-ui are Pulsar's One UI theme with every colour taken from a variable, so that
ui_variables() colours the whole workspace from the palette: the tree view, docks, tab bar and status bar on bgTool,
the editor and its active tab on bg, popups and inputs on surface, and the workspace behind them on the frame. The
status bar stays on bgTool, as in One UI, because it shows Git's counts in the ANSI colours, which the build checks
at 4.5:1 on bgTool but not on the frame.
"""
import json, os, re

from .nvim import name
from .vscode import luminance, mix, over

UI_STYLES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pulsar-ui")
# The stylesheets in UI_STYLES, in the order of One UI's index.less, after ui-variables.less and ui-mixins.less.
UI_SHEETS = ("atom", "badges", "buttons", "docks", "editor", "git", "inputs", "lists", "messages", "nav",
             "notifications", "modal", "panels", "panes", "progress", "tabs", "text", "title-bar", "tooltips",
             "tree-view", "status-bar", "key-binding", "sites", "settings", "packages", "core", "config")
UI_NOTICE = ("The stylesheets in styles/, except ui-variables.less, are adapted from Pulsar's One UI theme:\n\n"
             "Copyright (c) 2022-2026 Pulsar-Edit\nOriginal work copyright (c) 2011-2022 GitHub Inc.\n\n"
             "Released under the MIT License, the same terms as above.\n")
# Pulsar's engine range that the packages declare: the modern Tree-sitter grammars, on by default since Pulsar 1.113.
ENGINES = ">=1.113.0 <2.0.0"
# The height of Electron's menu bar in scripts/editors/shoot.py's window, which pixel_palette() leaves out.
MENU_BAR = 28
# A rule sets every font property, so that one of a less specific rule that also matches, such as the keyword rule's
# bold on storage.type, does not show through.
PLAIN = {"font-weight": "normal", "font-style": "normal", "text-decoration": "none"}
FONTS = {"": PLAIN, "bold": {**PLAIN, "font-weight": "bold"}, "italic": {**PLAIN, "font-style": "italic"},
         "bold italic": {**PLAIN, "font-weight": "bold", "font-style": "italic"},
         "underline": {**PLAIN, "text-decoration": "underline"}}


def syntax_name(theme):
    """The syntax theme's package name, for example "heritage-shuimo-night-syntax"."""
    return f"{name(theme)}-syntax"


def ui_name(theme):
    """The UI theme's package name, for example "heritage-shuimo-night-ui"."""
    return f"{name(theme)}-ui"


def syntax_rules(p):
    """(scope selector, role, font) per rule, in the order of the stylesheet. A selector is a comma-separated list of
    scopes, each a space-separated chain of ancestors, with > for a direct child, as TextMate writes them. A later
    rule overrides an earlier one with the same number of classes."""
    kw = "bold" if p.get("kwBold", not p["dark"]) else ""
    rules = []
    def s(scopes, role, font=""):
        rules.append((scopes, role, font))
    # the defaults: names, keywords, operators and punctuation
    s("variable, entity.name.type.module, entity.name.package, support.object.package, support.other.object, "
      "constant.other.database-name", "fg")
    s("keyword, storage.type, storage.modifier, constant.language, keyword.operator.new, keyword.operator.as, "
      "keyword.operator.instanceof, keyword.operator.typeof, keyword.operator.delete, keyword.operator.in, "
      "keyword.operator.of, keyword.operator.word, keyword.operator.expression, keyword.operator.logical.python, "
      "keyword.operator.sizeof, support.type.builtin.auto, storage.type.builtin", "keyword", kw)
    s("keyword.operator, punctuation, storage.type.arrow, storage.type.function.arrow, punctuation.other.arrow",
      "op")
    s("variable.language", "keyword", kw)
    s("variable.language.self, variable.language.cls, variable.language.this, variable.language.super",
      "keyword", "italic")
    # preprocessor directives, such as C's #include and its #
    s("keyword.control.directive, punctuation.definition.directive", "directive")
    # literals
    s("constant.numeric", "number")
    s("constant.other.enum, constant.preprocessor, support.constant, variable.declaration.enum", "constant",
      "bold italic")
    s("string, punctuation.definition.string", "string")
    s("constant.character.escape, constant.other.placeholder, punctuation.section.embedded, "
      "punctuation.definition.template-expression, string.regexp keyword, string.regexp punctuation.definition.group",
      "gold", "bold")
    s("string.regexp constant.other.character-class, string.regexp constant.other.character-class punctuation",
      "number", "bold")
    # types: class names, and the type names that the grammars scope as storage.type.other or support.storage.type;
    # Java scopes a class name as storage.type.java and its primitives as storage.type.<kind>.java
    s("entity.name.type, entity.name.class, entity.other.inherited-class, support.class, support.type, "
      "support.object.builtin, support.storage.type, support.storage.other.type, support.other.storage.type, "
      "support.other.class, storage.type.other, storage.type.class-type, support.other.namespace, "
      "support.type.constructor, source.java storage.type", "type")
    s("source.java storage.type.integral, source.java storage.type.float, source.java storage.type.boolean, "
      "source.java storage.type.void, source.java storage.type.enum, source.java storage.type.generic.wildcard, "
      "support.storage.type.builtin, support.storage.type.predefined", "keyword", kw)
    s("source.java storage.type.function.arrow", "op")
    # Python's built-in types, as its other built-ins
    s("source.python support.storage.type", "call", "italic")
    s("entity.name.type.interface", "type", "italic")
    s("support.type.exception", "type")
    # Rust's lifetimes
    s("keyword.operator.lifetime, source.rust storage.modifier.label", "typeParam", "italic")
    # functions: declarations, calls and built-ins
    s("entity.name.function", "method", "bold")
    s("support.other.function, support.function, support.other.function.method, support.function.method.builtin",
      "call")
    s("support.function.builtin, support.function.c99, support.function.magic, support.variable.magic", "call",
      "italic")
    # annotations, decorators, attributes and macros
    s("storage.type.annotation, storage.type.annotation punctuation, support.type.annotation, "
      "support.other.function.decorator, entity.name.function.macro, entity.name.function.preprocessor, "
      "source.rust entity.other.attribute-name, source.rust entity.other.attribute-name punctuation, "
      "source.rust entity.other.attribute-name support.class, entity.name.type.anchor, "
      "entity.name.type.anchor punctuation", "annotation")
    s("entity.name.label, support.other.label", "label", "bold")
    # parameters and fields
    s("variable.parameter", "param")
    s("meta.function-call.arguments variable.parameter", "param", "italic")
    s("variable.other.member, variable.other.property, variable.other.object.property, variable.other.readwrite.member, "
      "variable.other.declaration.member, variable.declaration.field, support.other.property, support.property.builtin, "
      "support.storage.other.property, entity.name.property, entity.other.attribute-name, constant.other.property, "
      "constant.other.table-name, support.type.property-name, meta.class.body > variable.other.declaration, "
      "meta.structure.key string, meta.structure.key punctuation.definition.string", "field")
    # shell: variables as IntelliJ's BASH.VAR_USE, local as a built-in command
    s("source.shell variable, source.shell variable punctuation.definition.variable", "field", "italic")
    s("source.shell storage.modifier.local", "call", "italic")
    s("source.shell keyword.operator.test", "fg")
    # HTML, XML, JSX
    s("entity.name.tag, punctuation.definition.tag, entity.name.tag punctuation", "keyword")
    s("constant.character.entity, constant.character.entity punctuation", "gold")
    # CSS: selectors as IntelliJ's CSS.IDENT, property values as CSS.PROPERTY_VALUE
    s("source.css entity.other.attribute-name, source.css entity.other.attribute-name punctuation, "
      "source.css entity.name.tag, source.css support.function", "keyword")
    s("constant.other.color, constant.other.color punctuation", "number")
    s("support.constant.property-value, keyword.other.unit, constant.numeric keyword.other.unit", "string")
    s("source.css keyword.control.important", "keyword", "bold")
    # YAML: keys as keywords, plain scalars as text
    s("source.yaml entity.name.tag", "keyword", kw)
    s("source.yaml string.unquoted, source.yaml constant.numeric, source.yaml constant.language", "fg")
    # TOML: keys and tables as keywords, booleans as predefined symbols
    s("source.toml entity.name.section, source.toml entity.name.section punctuation, source.toml variable.other.key",
      "keyword", kw)
    s("source.toml constant.language.boolean", "typeParam", "italic")
    # Markdown: headings take the declaration role, markers the keyword role
    s("markup.heading, markup.heading punctuation", "method", "bold")
    s("punctuation.definition.emphasis, punctuation.definition.list-item, markup.list punctuation.definition, "
      "markup.raw punctuation.definition, punctuation.definition.heading", "keyword", kw)
    s("markup.bold", "fg", "bold")
    s("markup.italic", "fg", "italic")
    s("markup.raw", "string")
    s("source.gfm string.unquoted, markup.link string", "azure", "underline")
    s("markup.underline.link", "call", "italic")
    s("source.gfm storage.modifier.language", "constant", "bold italic")
    s("markup.quote, markup.quote punctuation", "doc", "italic")
    # diff files
    s("markup.inserted, markup.inserted punctuation", "ansiGreen")
    s("markup.deleted, markup.deleted punctuation", "ansiRed")
    s("markup.changed, markup.changed punctuation", "ansiBlue")
    # comments last, so that nothing inside a comment takes a code role
    s("comment, comment punctuation", "comment", "italic")
    s("comment.block.documentation, comment.block.documentation punctuation, comment.line.documentation", "doc",
      "italic")
    s("comment.block.documentation storage.type.class, comment.block.documentation keyword, "
      "comment.block.documentation entity.name.tag, comment.block.documentation variable.other.jsdoc",
      "docTag", "bold italic")
    s("comment todo, comment keyword.todo", "todo", "bold italic")
    s("invalid.illegal, invalid.deprecated", "ansiRed")
    return rules


def selector(scope):
    """The CSS selector for a scope selector without commas, for example "source.css entity.name.tag"."""
    return " ".join(part if part == ">" else "".join(f".syntax--{piece}" for piece in part.split("."))
                    for part in scope.split())


def declarations(colour, font):
    return "; ".join(f"{k}: {v}" for k, v in {"color": colour, **FONTS[font]}.items())


def syntax_less(p):
    """styles/syntax.less: one rule per entry of syntax_rules()."""
    out = ["// Syntax: the palette role of each scope that Pulsar's grammars give a token.\n"]
    for scopes, role, font in syntax_rules(p):
        selectors = ",\n".join(selector(scope.strip()) for scope in scopes.split(","))
        out.append(f"{selectors} {{ {declarations('#' + p[role], font)}; }}\n")
    return "\n".join(out)


def hexes(p):
    return {k: "#" + v for k, v in p.items() if isinstance(v, str) and re.fullmatch(r"[0-9A-F]{6}", v)}


def cursor_line(p):
    """The current line's background, a layer over bg that lets the selection and highlights below it show."""
    return over(p["caretRow"], p["bg"])


def syntax_variables(p):
    """styles/syntax-variables.less: the variables that Pulsar documents for syntax themes and that other packages
    import, such as git-diff and the terminal packages."""
    c = hexes(p)
    ansi = {name: c["ansi" + name.title()] for name in ("red", "green", "yellow", "blue", "magenta", "cyan")}
    variables = {
        "syntax-text-color": c["fg"], "syntax-cursor-color": "#" + p.get("caret", p["gold"]),
        "syntax-selection-color": c["selection"], "syntax-selection-flash-color": c["searchBorder"],
        "syntax-background-color": c["bg"],
        "syntax-wrap-guide-color": c["guide"], "syntax-indent-guide-color": c["guide"],
        "syntax-invisible-character-color": c["guide"],
        "syntax-result-marker-color": c["searchBg"], "syntax-result-marker-color-selected": c["searchBorder"],
        "syntax-gutter-text-color": c["lineNo"], "syntax-gutter-text-color-selected": c["lineNoCaret"],
        "syntax-gutter-background-color": c["bg"], "syntax-gutter-background-color-selected": c["caretRow"],
        "syntax-color-renamed": c["modified"], "syntax-color-added": c["added"],
        "syntax-color-modified": c["modified"], "syntax-color-removed": c["deleted"],
        "syntax-color-variable": c["fg"], "syntax-color-constant": c["constant"], "syntax-color-property": c["field"],
        "syntax-color-value": c["string"], "syntax-color-function": c["call"], "syntax-color-method": c["method"],
        "syntax-color-class": c["type"], "syntax-color-keyword": c["keyword"], "syntax-color-tag": c["keyword"],
        "syntax-color-attribute": c["field"], "syntax-color-import": c["keyword"], "syntax-color-snippet": c["string"],
        "terminal-text-color": c["fg"], "terminal-background-color": c["bg"],
        "terminal-selection-background-color": c["selection"], "terminal-selection-text-color": c["fg"],
        "terminal-cursor-color": "#" + p.get("caret", p["gold"]),
        "terminal-result-marker-color": c["searchBg"], "terminal-result-marker-color-selected": c["searchBorder"],
        "terminal-color-black": c["disabled"], "terminal-color-white": c["op"],
        **{f"terminal-color-{n}": colour for n, colour in ansi.items()},
        "terminal-color-bright-black": c["muted"], "terminal-color-bright-white": c["fg"],
        **{f"terminal-color-bright-{n}": colour for n, colour in ansi.items()},
    }
    return ("// The variables that Pulsar documents for syntax themes, which other packages import.\n\n"
            + "".join(f"@{k}: {v};\n" for k, v in variables.items()))


def editor_less(p):
    """styles/editor.less: the editor's background, text, current line, selection, cursor, guides, gutter and the
    markers of find and bracket matching."""
    c = hexes(p)
    return f"""// The editor: background, current line, selection, cursor, guides, gutter and markers.

atom-text-editor {{
  background-color: @syntax-background-color;
  color: @syntax-text-color;

  // above the selection and highlights, which show through it
  .line.cursor-line {{
    background-color: {cursor_line(p)};
  }}

  .cursor {{
    border-left: 2px solid @syntax-cursor-color;
  }}

  .selection .region {{
    background-color: @syntax-selection-color;
  }}

  .bracket-matcher .region {{
    background-color: {c["braceBg"]};
    border: none;
  }}

  .invisible-character,
  .indent-guide {{
    color: @syntax-invisible-character-color;
  }}

  .wrap-guide {{
    background-color: @syntax-wrap-guide-color;
  }}

  .find-result .region.region.region,
  .current-result .region.region.region {{
    border-radius: 2px;
    background-color: @syntax-result-marker-color;
  }}
  .find-result .region.region.region {{
    border: 1px solid transparent;
  }}
  .current-result .region.region.region {{
    border: 1px solid @syntax-result-marker-color-selected;
  }}

  .highlights .highlight.selection .region {{
    background-color: {c["selInactive"]};
  }}

  .gutter {{
    background-color: @syntax-background-color;

    .line-number {{
      color: @syntax-gutter-text-color;
      -webkit-font-smoothing: antialiased;

      &.cursor-line {{
        color: @syntax-gutter-text-color-selected;
        background-color: @syntax-gutter-background-color-selected;
      }}

      .icon-right {{
        color: @syntax-gutter-text-color;
      }}
    }}
  }}

  .gutter .line-number.folded,
  .gutter .line-number:after,
  .fold-marker:after {{
    color: @syntax-gutter-text-color-selected;
  }}
}}
"""


def syntax_index():
    return ('// The syntax theme: the variables, the editor and the syntax rules.\n\n'
            '@import "styles/syntax-variables.less";\n@import "styles/editor.less";\n@import "styles/syntax.less";\n')


def text_on(background, p):
    """fg or bg, whichever reads better on background, for text on a coloured button or badge."""
    def ratio(a, b):
        x, y = luminance(a), luminance(b)
        return (max(x, y) + 0.05) / (min(x, y) + 0.05)
    return "#" + max((p["fg"], p["bg"]), key=lambda t: ratio(t, background))


def ui_variables(p):
    """styles/ui-variables.less: the variables that Pulsar documents for UI themes, which other packages import, and
    those that the One UI stylesheets in heritage/pulsar-ui use."""
    c = hexes(p)
    # hover moves a coloured button away from its text, so the text keeps its contrast
    def hover(key, text):
        return "#" + mix(p[key], "000000" if luminance(text[1:]) > luminance(p[key]) else "FFFFFF", 0.12)
    states = {"info": ("diffMod", "ansiBlue"), "success": ("diffIns", "ansiGreen"),
              "warning": ("diffConf", "ansiYellow"), "error": ("diffDel", "ansiRed")}
    variables = {
        # text. Text that names a state takes the ANSI colours, which read as their hue at 4.5:1 or more.
        "text-color": c["fg"], "text-color-subtle": c["muted"], "text-color-highlight": c["fg"],
        "text-color-selected": c["fg"],
        **{f"text-color-{state}": c[text] for state, (_, text) in states.items()},
        # backgrounds of states: the diff tints, with text on them in fg
        **{f"background-color-{state}": c[tint] for state, (tint, _) in states.items()},
        "background-color-highlight": c["hover"], "background-color-selected": c["selection"],
        "app-background-color": c["frame"],
        "base-background-color": c["bg"], "base-border-color": c["border"],
        # components
        "pane-item-background-color": c["bg"], "pane-item-border-color": c["border"],
        "input-background-color": c["surface"], "input-border-color": c["border"],
        "tool-panel-background-color": c["bgTool"], "tool-panel-border-color": c["border"],
        "inset-panel-background-color": c["surface"], "inset-panel-border-color": c["border"],
        "panel-heading-background-color": c["bgTool"], "panel-heading-border-color": c["border"],
        "overlay-background-color": c["surface"], "overlay-border-color": c["border"],
        "button-background-color": c["surface"], "button-background-color-hover": c["hover"],
        "button-background-color-selected": c["red"], "button-border-color": c["border"],
        "tab-bar-background-color": c["bgTool"], "tab-bar-border-color": c["border"],
        "tab-background-color": c["bgTool"], "tab-background-color-active": c["bg"], "tab-border-color": c["border"],
        "tree-view-background-color": c["bgTool"], "tree-view-border-color": c["border"],
        # collaborators' colours, as Zed's players
        "ui-site-color-1": c["ansiBlue"], "ui-site-color-2": c["ansiGreen"], "ui-site-color-3": c["ansiYellow"],
        "ui-site-color-4": c["ansiMagenta"], "ui-site-color-5": c["ansiCyan"],
        # One UI's own variables
        "ui-light": "false" if p["dark"] else "true",
        "text-color-faded": c["disabled"],
        "text-color-added": c["ansiGreen"], "text-color-ignored": c["muted"], "text-color-modified": c["ansiYellow"],
        "text-color-removed": c["ansiRed"], "text-color-renamed": c["ansiBlue"],
        "level-1-color": c["surface"], "level-2-color": c["bg"], "level-3-color": c["bgTool"],
        "level-3-color-hover": c["hover"], "level-3-color-active": c["selInactive"],
        # the accent: focus rings and small markers in ansiBlue, as VS Code's focus border; filled buttons, badges
        # and the progress bar in red with redText, as the other targets' buttons
        "accent-color": c["ansiBlue"], "accent-text-color": c["bg"],
        "accent-bg-color": c["red"], "accent-bg-text-color": c["redText"], "accent-only-text-color": c["ansiBlue"],
        "badge-background-color": c["selInactive"],
        "button-text-color-selected": c["redText"], "button-border-color-selected": c["red"],
        "button-background-color-primary-hover": hover("red", c["redText"]), "button-text-color-primary": c["redText"],
        **{f"button-background-color-{state}-hover": hover(tint, c["fg"]) for state, (tint, _) in states.items()},
        **{f"button-text-color-{state}": c["fg"] for state in states},
        "checkbox-background-color": c["red"],
        "input-background-color-focus": c["surface"], "input-selection-color": c["selInactive"],
        "input-selection-color-focus": c["selection"],
        "input-background-color-valid": c["diffIns"], "input-background-color-invalid": c["diffDel"],
        "overlay-backdrop-color": c["frame"], "overlay-backdrop-opacity": ".75",
        "progress-background-color": c["red"],
        "scrollbar-color": c["guideSel"], "scrollbar-background-color": c["bgTool"],
        "scrollbar-color-editor": c["guideSel"], "scrollbar-background-color-editor": c["bg"],
        "tab-text-color": c["muted"], "tab-text-color-active": c["fg"], "tab-text-color-editor": c["fg"],
        "tab-text-color-editor-deleted": c["ansiRed"], "tab-background-color-editor": c["bg"],
        "tab-inactive-status-added": c["ansiGreen"], "tab-inactive-status-modified": c["ansiYellow"],
        "tab-inactive-status-deleted": c["ansiRed"],
        "tooltip-background-color": c["surface"], "tooltip-text-color": c["fg"],
        "tooltip-text-key-color": c["surface"], "tooltip-background-key-color": c["fg"],
        "settings-list-background-color": c["bgTool"],
        "theme-config-box-shadow": f"inset 0 0 0 1px {c['border']}",
        "theme-config-box-shadow-selected": f"inset 0 0 0 1px {c['border']}",
        "theme-config-border-selected": c["ansiBlue"],
    }
    sizes = """
// Sizes, as One UI's
@font-size:               12px;
@input-font-size:         14px;
@disclosure-arrow-size:   12px;
@component-padding:       10px;
@component-icon-padding:  5px;
@component-icon-size:     16px;
@component-line-height:   25px;
@component-border-radius: 3px;
@tab-height:              30px;
@font-family: system-ui;
@ui-size:                 1em;
@ui-input-size:           (@ui-size*1.15);
@ui-padding:              (@ui-size*1.5);
@ui-padding-pane:         (@ui-size*.5);
@ui-padding-icon:         (@ui-padding/3.3);
@ui-line-height:          (@ui-size*2);
@ui-tab-height:           (@ui-size*2.5);
"""
    return ("// The variables that Pulsar documents for UI themes, which other packages import, and One UI's own.\n\n"
            + "".join(f"@{k}: {v};\n" for k, v in variables.items()) + sizes)


def ui_index(package):
    """index.less: One UI's, with the variables of this theme."""
    sheets = "".join(f'@import "styles/{sheet}.less";\n' for sheet in UI_SHEETS)
    return (f"// The UI theme: One UI's stylesheets coloured by this theme's variables.\n\n"
            f'@ui-theme-name: {package};\n\n@import "styles/ui-variables.less";\n@import "styles/ui-mixins.less";\n'
            f'@import "octicon-mixins.less";\n\n{sheets}')


def package_json(theme, kind, version, description, repository):
    package = syntax_name(theme) if kind == "syntax" else ui_name(theme)
    brightness = "dark" if theme["palette"]["dark"] else "light"
    return json.dumps({
        "name": package, "theme": kind, "version": version, "description": description,
        "keywords": [brightness, kind, "heritage"], "repository": repository, "license": "MIT",
        "engines": {"atom": ENGINES},
    }, indent=2, ensure_ascii=False) + "\n"


def syntax_package(theme, version, description, repository):
    """(path, text) per file of the syntax theme package, without its README and licence."""
    p = theme["palette"]
    return [("package.json", package_json(theme, "syntax", version, description, repository)),
            ("index.less", syntax_index()),
            ("styles/syntax-variables.less", syntax_variables(p)),
            ("styles/editor.less", editor_less(p)),
            ("styles/syntax.less", syntax_less(p))]


def ui_package(theme, version, description, repository):
    """(path, text) per file of the UI theme package, without its README and licence."""
    files = [("package.json", package_json(theme, "ui", version, description, repository)),
             ("index.less", ui_index(ui_name(theme))),
             ("styles/ui-variables.less", ui_variables(theme["palette"]))]
    for sheet in ("ui-mixins", *UI_SHEETS):
        with open(os.path.join(UI_STYLES, f"{sheet}.less"), encoding="utf-8") as f:
            files.append((f"styles/{sheet}.less", f.read()))
    return files


def package_readme(theme, kind, source):
    """The README of one package, which Pulsar's package registry requires and shows."""
    p = theme["palette"]
    other = ui_name(theme) if kind == "syntax" else syntax_name(theme)
    part = "the editor: code, the gutter, the cursor, selections and find results" if kind == "syntax" else \
        "the workspace: the tree view, tabs, panels, the status bar, dialogs and the settings"
    return f"""# {p["name"]}, {"syntax" if kind == "syntax" else "UI"} theme

A Heritage Themes {"syntax" if kind == "syntax" else "UI"} theme for Pulsar. It colours {part}. \
Install `{other}` with it and choose both under **Settings | Themes**.

The palette and the tradition it comes from are described at {source}.
"""


def packages(theme, version, repository, source, licence=""):
    """(package name, [(path, text)]) for the syntax and UI theme packages of a theme, with their READMEs and, when
    licence is given, their licences. source is the URL of the theme family's page."""
    p = theme["palette"]
    description = f"{p['name']}: a Heritage Themes colour theme drawn from a culture's colour tradition."
    syntax = syntax_package(theme, version, description, repository) + [("README.md",
                                                                          package_readme(theme, "syntax", source))]
    ui = ui_package(theme, version, description, repository) + [("README.md", package_readme(theme, "ui", source))]
    if licence:
        syntax.append(("LICENSE", licence))
        ui.append(("LICENSE", f"{licence}\n{UI_NOTICE}"))
    return [(syntax_name(theme), syntax), (ui_name(theme), ui)]


def pixel_palette(p):
    """What scripts/editors/pixels.py checks a screenshot against: the window that scripts/editors/shoot.py opens at
    1100x700, without the menu bar, which Electron draws in the GTK theme's colours. The current line is a layer
    over the editor, so the bracket match below it shows as their blend."""
    c = hexes(p)
    layer = cursor_line(p)
    alpha = int(layer[7:9], 16) / 255
    def under_cursor_line(key):
        top = [int(layer[i:i + 2], 16) for i in (1, 3, 5)]
        base = [int(p[key][i:i + 2], 16) for i in (0, 2, 4)]
        return "#" + "".join(f"{round(t * alpha + b * (1 - alpha)):02X}" for t, b in zip(top, base))
    backgrounds = [c[k] for k in ("bgTool", "frame", "surface", "caretRow", "selection", "selInactive", "hover",
                                  "border", "braceBg", "searchBg", "red", "diffIns", "diffDel", "diffMod", "diffConf")]
    backgrounds += [under_cursor_line(k) for k in ("braceBg", "selection", "searchBg")]
    return dict(background=c["bg"], backgrounds=backgrounds, foregrounds=sorted(set(c.values())),
                crop=[MENU_BAR, 0, 0, 0])
