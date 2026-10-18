"""VS Code colour theme JSON generated from a palette.

tokenColors map TextMate scopes to the same palette roles that heritage.scheme gives the IntelliJ keys, so a
token reads alike in both IDEs. semanticTokenColors cover what language servers report and TextMate grammars
cannot tell apart, such as declarations from calls. colors map workbench keys to the roles heritage.ui gives the
matching IntelliJ UI keys: the frame behind the title bar, activity bar and status bar, the tool island behind
the side bar and panel, and the editor on bg.
"""

import math, re

TRANSPARENT = "#00000000"
SHADOW = {True: "#00000059", False: "#00000024"}


def rgb(hex_colour):
    return [int(hex_colour[i:i + 2], 16) for i in (0, 2, 4)]


def over(colour, base):
    """#RRGGBBAA that composites to colour over base with the lowest alpha, so layers below it stay visible."""
    c, b = rgb(colour), rgb(base)
    alpha = max((x - y) / (255 - y) if x > y else (y - x) / y if x < y else 0 for x, y in zip(c, b))
    a = max(1, math.ceil(alpha * 255 - 1e-9))
    src = [min(255, max(0, round((x - (1 - a / 255) * y) / (a / 255)))) for x, y in zip(c, b)]
    return "#" + "".join(f"{v:02X}" for v in src) + f"{a:02X}"


def luminance(hex_colour):
    r, g, b = (c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in (x / 255 for x in rgb(hex_colour)))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def mix(a, b, t):
    """a moved towards b by t, as six-digit hex."""
    return "".join(f"{round(x + (y - x) * t):02X}" for x, y in zip(rgb(a), rgb(b)))


def token_colors(p):
    """TextMate rules as (scope selectors, role, font style). The deepest matching scope wins, so a rule for a
    child scope, such as the quotes of a string, overrides the rule for its parent."""
    kw = "bold" if p.get("kwBold", not p["dark"]) else ""
    rules = []
    def s(scopes, role, font=""):
        rules.append((scopes, role, font))
    s("comment, punctuation.definition.comment", "comment", "italic")
    s("comment.block.documentation, comment.block.javadoc, string.quoted.docstring, "
      "comment.block.documentation punctuation.definition.comment, "
      "comment.block.javadoc punctuation.definition.comment, "
      "string.quoted.docstring punctuation.definition.string", "doc", "italic")
    s("keyword.other.documentation, storage.type.class.jsdoc, storage.type.class.doxygen", "docTag", "bold italic")
    s("keyword.codetag", "todo", "bold italic")
    s("string, punctuation.definition.string, string.regexp", "string")
    s("constant.character.escape, constant.other.placeholder, punctuation.definition.interpolation, "
      "string.regexp keyword, string.regexp punctuation.definition.group", "gold", "bold")
    s("constant.other.character-class.regexp, punctuation.definition.character-class.regexp", "number", "bold")
    s("invalid, invalid.illegal", "error")
    s("constant.numeric", "number")
    s("constant.language, variable.language", "keyword", kw)
    s("constant.other.caps, variable.other.enummember, support.constant, entity.name.function.preprocessor", "constant",
      "bold italic")
    s("keyword, storage.type, storage.modifier, keyword.operator.new, keyword.operator.expression, "
      "keyword.operator.word, keyword.operator.wordlike, keyword.operator.logical.python, keyword.operator.sizeof, "
      "keyword.operator.instanceof, keyword.operator.typeof, keyword.operator.delete, keyword.operator.in, "
      "keyword.operator.of, keyword.control.directive, punctuation.definition.directive, support.type.primitive, "
      "storage.type.primitive, storage.type.built-in, entity.name.type.primitive.rust, "
      "entity.name.type.numeric.rust", "keyword", kw)
    s("keyword.operator, punctuation, storage.type.function.arrow, meta.brace, storage.modifier.reference, "
      "storage.modifier.pointer", "op")
    s("variable.parameter.function.language.special.self, variable.language.special.self, "
      "variable.language.special.cls", "keyword", "italic")
    s("entity.name.type, entity.name.class, entity.other.inherited-class, support.class, support.type, "
      "entity.name.scope-resolution, storage.type.java, storage.type.generic.java, storage.type.object.array.java, "
      "storage.type.groovy, source.go storage.type", "type")
    s("entity.name.type.interface", "type", "italic")
    s("entity.name.type.namespace, entity.name.namespace, entity.name.type.package, entity.name.package", "fg")
    s("entity.name.type.lifetime, punctuation.definition.lifetime", "typeParam", "italic")
    s("entity.name.function", "method", "bold")
    s("meta.function-call entity.name.function, meta.method-call entity.name.function, meta.function-call.generic, "
      "meta.method-call meta.method, entity.name.function.call, entity.name.command, variable.function, "
      "support.function", "call")
    s("support.function.builtin, support.type.python, support.variable.magic.python", "call", "italic")
    s("meta.annotation, storage.type.annotation, punctuation.definition.annotation, meta.decorator, "
      "entity.name.function.decorator, punctuation.definition.decorator, entity.name.function.macro, "
      "support.macro, meta.attribute.rust, meta.attribute.rust entity.name.type, meta.attribute.rust punctuation, "
      "punctuation.definition.attribute.rust, punctuation.brackets.attribute.rust, entity.name.type.anchor.yaml, "
      "keyword.control.property.anchor.yaml, punctuation.definition.anchor.yaml, variable.other.alias.yaml",
      "annotation")
    s("variable", "fg")
    s("variable.parameter, entity.name.variable.parameter", "param")
    s("variable.other.property, variable.object.property, variable.other.object.property, variable.other.member, "
      "entity.name.variable.field, entity.name.variable.property, support.variable.property, "
      "constant.other.table-name.sql, support.type.property-name, punctuation.support.type.property-name, "
      "entity.other.attribute-name", "field")
    s("variable.parameter.function-call.python", "param", "italic")
    # shell variables, as IntelliJ's BASH.VAR_USE and BASH.VAR_DEF
    s("source.shell variable, source.shell variable.parameter, source.shell variable.other, "
      "punctuation.definition.variable.shell", "field", "italic")
    s("meta.shebang.shell, punctuation.definition.comment.shebang", "comment", "bold italic")
    s("storage.modifier.local.shell", "call", "italic")
    s("string.unquoted.argument.shell, constant.other.option", "fg")
    # HTML, XML, JSX
    s("entity.name.tag, punctuation.definition.tag, meta.tag.metadata.doctype, "
      "punctuation.separator.key-value.html, meta.tag.attributes keyword.operator.assignment", "keyword")
    s("meta.tag.custom entity.name.tag", "type")
    s("support.class.component, meta.tag.metadata.doctype entity.other.attribute-name", "keyword")
    s("constant.character.entity, punctuation.definition.entity.html", "gold")
    # CSS: selectors as IntelliJ's CSS.IDENT, property values as CSS.PROPERTY_VALUE
    s("source.css entity.other.attribute-name, source.css entity.name.tag, source.css support.function, "
      "punctuation.definition.entity.css", "keyword")
    s("constant.other.color, punctuation.definition.constant.css", "number")
    s("support.constant.property-value, support.constant.font-name, keyword.other.unit", "string")
    s("variable.parameter.url.css", "string", "underline")
    s("keyword.other.important", "keyword", "bold")
    s("punctuation.separator.key-value.css", "fg")
    # SQL
    s("constant.other.database-name.sql", "fg")
    # YAML: keys as keywords, plain scalars as text, comments as doc comments
    s("entity.name.tag.yaml", "keyword", kw)
    s("string.unquoted.plain.out.yaml, source.yaml constant.numeric, source.yaml constant.language", "fg")
    s("comment.line.number-sign.yaml, comment.line.number-sign.yaml punctuation.definition.comment", "doc", "italic")
    # TOML: keys and tables as keywords, booleans as predefined symbols
    s("entity.name.section.toml, variable.other.key.toml", "keyword", kw)
    s("constant.language.boolean.toml", "typeParam", "italic")
    # Markdown: headings take the declaration role, markers the keyword role
    s("markup.heading, entity.name.section.markdown", "method", "bold")
    s("punctuation.definition.heading, punctuation.definition.bold, punctuation.definition.italic, "
      "punctuation.definition.list.begin.markdown, punctuation.definition.raw.markdown, "
      "punctuation.definition.markdown", "keyword", kw)
    s("markup.bold", "fg", "bold")
    s("markup.italic", "fg", "italic")
    s("markup.inline.raw", "string")
    s("string.other.link.title.markdown, punctuation.definition.link.title", "azure", "underline")
    s("markup.underline.link", "call", "italic")
    s("fenced_code.block.language", "constant", "bold italic")
    s("meta.link.inline.markdown punctuation.definition.metadata", "fg")
    s("markup.quote", "doc", "italic")
    # diff files
    s("markup.inserted", "added")
    s("markup.deleted", "deleted")
    s("markup.changed", "modified")
    s("meta.diff.header, meta.diff.range", "keyword")
    return [{"scope": scopes, "settings": {"foreground": "#" + p[role], "fontStyle": font}}
            for scopes, role, font in rules]


def semantic_token_colors(p):
    """Semantic token rules: type, then modifiers. A rule with more modifiers wins over one with fewer."""
    kw = "bold" if p.get("kwBold", not p["dark"]) else ""
    def t(role, font=""):
        return {"foreground": "#" + p[role], "fontStyle": font}
    return {
        "namespace": t("fg"),
        "class": t("type"), "struct": t("type"), "enum": t("type"), "type": t("type"),
        "interface": t("type", "italic"), "typeParameter": t("typeParam", "bold"),
        "enumMember": t("constant", "bold italic"),
        "function": t("call"), "method": t("call"), "method.static": t("call", "italic"),
        "function.declaration": t("method", "bold"), "method.declaration": t("method", "bold"),
        "function.definition": t("method", "bold"), "method.definition": t("method", "bold"),
        "method.static.declaration": t("method", "bold"),
        "property": t("field"), "property.readonly": t("field"), "property.static": t("field", "italic"),
        "property.static.readonly": t("constant", "bold italic"),
        "parameter": t("param"), "variable": t("fg"), "variable.readonly": t("fg"),
        "decorator": t("annotation"), "macro": t("annotation"), "label": t("label", "bold"),
        # Language-specific types: Pylance's self and cls, rust-analyzer's lifetimes, keywords and attributes
        "selfParameter": t("keyword", "italic"), "clsParameter": t("keyword", "italic"),
        "selfKeyword": t("keyword", kw), "builtinType": t("keyword", kw), "lifetime": t("typeParam", "italic"),
        "attribute": t("annotation"), "builtinAttribute": t("annotation"),
        "formatSpecifier": t("gold", "bold"), "escapeSequence": t("gold", "bold"),
    }


def workbench(p):
    """Workbench colour keys to #-prefixed colours."""
    c = {k: "#" + v for k, v in p.items() if isinstance(v, str) and re.fullmatch(r"[0-9A-F]{6}", v)}
    bg = p["bg"]
    # Hover moves the button colour away from its text, so the text keeps its contrast.
    red_hover = "#" + mix(p["red"], "000000" if luminance(p["redText"]) > luminance(p["red"]) else "FFFFFF", 0.12)
    def layer(key, base=bg):
        return over(p[key], base)
    def wash(key):
        """Halfway from bg to the palette colour, as a layer over bg."""
        return over(mix(bg, p[key], 0.5), bg)
    return {
        # base. Text that names a state takes the ANSI colours, which read as their hue at 4.5:1 or more against bg.
        # Focus outlines and match highlights take ansiBlue, as VS Code's own themes do; gold falls below the 3:1
        # that a focus indicator needs in some light themes.
        "foreground": c["fg"], "disabledForeground": c["disabled"], "descriptionForeground": c["muted"],
        "errorForeground": c["ansiRed"], "icon.foreground": c["muted"], "focusBorder": c["ansiBlue"],
        "selection.background": c["selection"], "widget.border": c["border"], "widget.shadow": SHADOW[p["dark"]],
        "sash.hoverBorder": c["gold"],
        "toolbar.hoverBackground": c["hover"], "toolbar.activeBackground": c["selection"],
        "textLink.foreground": c["azure"], "textLink.activeForeground": c["azure"],
        "textPreformat.foreground": c["string"], "textPreformat.background": c["surface"],
        "textBlockQuote.background": c["surface"], "textBlockQuote.border": c["border"],
        "textCodeBlock.background": c["surface"], "textSeparator.foreground": c["border"],
        # buttons and inputs
        "button.background": c["red"], "button.foreground": c["redText"],
        "button.hoverBackground": red_hover, "button.border": TRANSPARENT,
        "button.separator": c["redText"] + "66",
        "button.secondaryBackground": c["surface"], "button.secondaryForeground": c["fg"],
        "button.secondaryHoverBackground": c["hover"],
        "checkbox.background": c["surface"], "checkbox.foreground": c["fg"], "checkbox.border": c["border"],
        "dropdown.background": c["surface"], "dropdown.listBackground": c["surface"],
        "dropdown.border": c["border"], "dropdown.foreground": c["fg"],
        "input.background": c["surface"], "input.border": c["border"], "input.foreground": c["fg"],
        "input.placeholderForeground": c["muted"],
        "inputOption.activeBackground": c["selInactive"], "inputOption.activeBorder": c["ansiBlue"],
        "inputOption.activeForeground": c["fg"], "inputOption.hoverBackground": c["hover"],
        "inputValidation.errorBackground": c["diffDel"], "inputValidation.errorBorder": c["error"],
        "inputValidation.warningBackground": c["diffConf"], "inputValidation.warningBorder": c["warning"],
        "inputValidation.infoBackground": c["diffMod"], "inputValidation.infoBorder": c["azure"],
        "keybindingLabel.background": c["surface"], "keybindingLabel.foreground": c["fg"],
        "keybindingLabel.border": c["border"], "keybindingLabel.bottomBorder": c["border"],
        "badge.background": c["red"], "badge.foreground": c["redText"],
        "progressBar.background": c["red"],
        "scrollbar.shadow": TRANSPARENT, "scrollbarSlider.background": c["guideSel"] + "99",
        "scrollbarSlider.hoverBackground": c["lineNo"] + "99", "scrollbarSlider.activeBackground": c["lineNo"] + "CC",
        # lists and trees
        "list.activeSelectionBackground": c["selection"], "list.inactiveSelectionBackground": c["selInactive"],
        "list.hoverBackground": c["hover"],
        "list.focusBackground": c["selInactive"], "list.focusOutline": c["ansiBlue"],
        "list.inactiveFocusOutline": TRANSPARENT, "list.highlightForeground": c["ansiBlue"],
        "list.focusHighlightForeground": c["ansiBlue"], "list.dropBackground": c["selInactive"],
        "list.errorForeground": c["ansiRed"], "list.warningForeground": c["ansiYellow"],
        "list.invalidItemForeground": c["ansiRed"], "list.deemphasizedForeground": c["muted"],
        "tree.indentGuidesStroke": c["guideSel"], "tree.inactiveIndentGuidesStroke": c["guide"],
        # frame: title bar, activity bar, status bar
        "titleBar.activeBackground": c["frame"], "titleBar.inactiveBackground": c["frame"],
        "titleBar.activeForeground": c["fg"], "titleBar.inactiveForeground": c["muted"], "titleBar.border": TRANSPARENT,
        "commandCenter.background": c["surface"], "commandCenter.foreground": c["fg"],
        "commandCenter.activeBackground": c["hover"], "commandCenter.activeForeground": c["fg"],
        "commandCenter.border": c["border"], "commandCenter.activeBorder": c["border"],
        "menubar.selectionBackground": c["hover"], "menubar.selectionForeground": c["fg"],
        "activityBar.background": c["frame"], "activityBar.foreground": c["fg"],
        "activityBar.inactiveForeground": c["muted"], "activityBar.border": TRANSPARENT,
        "activityBar.activeBorder": c["red"], "activityBar.activeBackground": TRANSPARENT,
        "activityBarBadge.background": c["red"], "activityBarBadge.foreground": c["redText"],
        "activityBarTop.foreground": c["fg"], "activityBarTop.inactiveForeground": c["muted"],
        "activityBarTop.activeBorder": c["red"],
        "statusBar.background": c["frame"], "statusBar.foreground": c["fg"], "statusBar.border": TRANSPARENT,
        "statusBar.noFolderBackground": c["frame"], "statusBar.noFolderForeground": c["fg"],
        "statusBar.debuggingBackground": c["red"], "statusBar.debuggingForeground": c["redText"],
        "statusBar.focusBorder": c["ansiBlue"], "statusBarItem.hoverBackground": c["hover"],
        "statusBarItem.activeBackground": c["selection"], "statusBarItem.focusBorder": c["ansiBlue"],
        "statusBarItem.remoteBackground": c["red"], "statusBarItem.remoteForeground": c["redText"],
        "statusBarItem.remoteHoverBackground": red_hover,
        "statusBarItem.prominentBackground": c["selInactive"], "statusBarItem.prominentHoverBackground": c["hover"],
        "statusBarItem.errorBackground": c["red"], "statusBarItem.errorForeground": c["redText"],
        "statusBarItem.warningBackground": c["diffConf"], "statusBarItem.warningForeground": c["fg"],
        # tool island: side bar and panel
        "sideBar.background": c["bgTool"], "sideBar.foreground": c["fg"], "sideBar.border": c["border"],
        "sideBarTitle.foreground": c["fg"], "sideBarSectionHeader.background": c["bgTool"],
        "sideBarSectionHeader.foreground": c["fg"], "sideBarSectionHeader.border": c["border"],
        "panel.background": c["bgTool"], "panel.border": c["border"],
        "panelTitle.activeForeground": c["fg"], "panelTitle.inactiveForeground": c["muted"],
        "panelTitle.activeBorder": c["red"], "panelSectionHeader.background": c["bgTool"],
        "panelInput.border": c["border"], "outputView.background": c["bgTool"],
        "terminal.background": c["bgTool"], "terminal.foreground": c["fg"],
        "terminal.selectionBackground": c["selection"], "terminalCursor.foreground": "#" + p.get("caret", p["gold"]),
        "terminal.ansiBlack": c["disabled"], "terminal.ansiBrightBlack": c["muted"],
        "terminal.ansiWhite": c["op"], "terminal.ansiBrightWhite": c["fg"],
        **{f"terminal.ansi{bright}{k}": c["ansi" + k] for k in ("Red", "Green", "Yellow", "Blue", "Magenta", "Cyan")
           for bright in ("", "Bright")},
        # editor groups and tabs
        "editorGroup.border": c["border"], "editorGroup.dropBackground": layer("selInactive"),
        "editorGroupHeader.tabsBackground": c["bg"], "editorGroupHeader.tabsBorder": c["border"],
        "editorGroupHeader.noTabsBackground": c["bg"],
        "tab.activeBackground": c["selInactive"], "tab.activeForeground": c["fg"],
        "tab.inactiveBackground": c["bg"], "tab.inactiveForeground": c["muted"],
        "tab.unfocusedActiveBackground": c["hover"], "tab.unfocusedActiveForeground": c["fg"],
        "tab.unfocusedInactiveBackground": c["bg"], "tab.unfocusedInactiveForeground": c["muted"],
        "tab.hoverBackground": c["hover"], "tab.unfocusedHoverBackground": c["hover"], "tab.border": c["bg"],
        "tab.activeBorder": c["red"], "tab.unfocusedActiveBorder": c["gold"], "tab.activeBorderTop": TRANSPARENT,
        "tab.activeModifiedBorder": c["modified"], "tab.inactiveModifiedBorder": c["modified"],
        "breadcrumb.background": c["bg"], "breadcrumb.foreground": c["muted"],
        "breadcrumb.focusForeground": c["fg"], "breadcrumb.activeSelectionForeground": c["fg"],
        "breadcrumbPicker.background": c["surface"],
        # editor
        "editor.background": c["bg"], "editor.foreground": c["fg"],
        "editorCursor.foreground": "#" + p.get("caret", p["gold"]),
        "editor.lineHighlightBackground": c["caretRow"], "editor.lineHighlightBorder": TRANSPARENT,
        "editor.selectionBackground": c["selection"], "editor.inactiveSelectionBackground": layer("selInactive"),
        "editor.selectionHighlightBackground": layer("underCaret"),
        "editor.wordHighlightBackground": layer("underCaret"),
        "editor.wordHighlightTextBackground": layer("underCaret"),
        "editor.wordHighlightStrongBackground": layer("writeCaret"),
        "editor.findMatchBackground": layer("searchBg"), "editor.findMatchBorder": c["searchBorder"],
        "editor.findMatchHighlightBackground": layer("searchBg"),
        "editor.findRangeHighlightBackground": layer("caretRow"),
        "editor.hoverHighlightBackground": layer("underCaret"), "editor.rangeHighlightBackground": layer("caretRow"),
        "editor.linkedEditingBackground": layer("underCaret"),
        "editorLineNumber.foreground": c["lineNo"], "editorLineNumber.activeForeground": c["lineNoCaret"],
        "editorIndentGuide.background1": c["guide"], "editorIndentGuide.activeBackground1": c["guideSel"],
        "editorWhitespace.foreground": c["guide"], "editorRuler.foreground": c["guide"],
        "editorCodeLens.foreground": c["muted"], "editorLink.activeForeground": c["azure"],
        "editorBracketMatch.background": layer("braceBg"), "editorBracketMatch.border": TRANSPARENT,
        # pair colours would bring hues the palette does not have, so brackets keep the operator role
        **{f"editorBracketHighlight.foreground{i}": c["op"] for i in range(1, 7)},
        "editorBracketHighlight.unexpectedBracket.foreground": c["error"],
        "editorInlayHint.foreground": c["muted"], "editorInlayHint.background": layer("caretRow"),
        "editorGhostText.foreground": c["muted"], "editorLightBulb.foreground": c["gold"],
        "editorLightBulbAutoFix.foreground": c["azure"], "editorLightBulbAi.foreground": c["gold"],
        "editorError.foreground": c["error"], "editorWarning.foreground": c["warning"],
        "editorInfo.foreground": c["weak"], "editorHint.foreground": c["weak"],
        "editorUnnecessaryCode.opacity": "#000000A0" if p["dark"] else "#00000090",
        "editorGutter.background": c["bg"], "editorGutter.addedBackground": c["added"],
        "editorGutter.modifiedBackground": c["modified"], "editorGutter.deletedBackground": c["deleted"],
        "editorOverviewRuler.border": TRANSPARENT, "editorOverviewRuler.addedForeground": c["added"],
        "editorOverviewRuler.modifiedForeground": c["modified"], "editorOverviewRuler.deletedForeground": c["deleted"],
        "editorOverviewRuler.errorForeground": c["error"], "editorOverviewRuler.warningForeground": c["warning"],
        "editorOverviewRuler.infoForeground": c["weak"], "editorOverviewRuler.findMatchForeground": c["gold"],
        "editorOverviewRuler.selectionHighlightForeground": c["azure"],
        "editorOverviewRuler.wordHighlightForeground": c["azure"],
        "editorOverviewRuler.wordHighlightStrongForeground": c["red"],
        "editorOverviewRuler.bracketMatchForeground": c["guideSel"],
        "minimapGutter.addedBackground": c["added"], "minimapGutter.modifiedBackground": c["modified"],
        "minimapGutter.deletedBackground": c["deleted"], "minimap.findMatchHighlight": c["gold"],
        "minimap.selectionHighlight": c["selection"], "minimap.errorHighlight": c["error"],
        "minimap.warningHighlight": c["warning"],
        "editorStickyScroll.background": c["bg"], "editorStickyScrollHover.background": c["hover"],
        "editorStickyScroll.shadow": SHADOW[p["dark"]],
        # editor widgets: find, suggest, hover, peek
        "editorWidget.background": c["surface"], "editorWidget.foreground": c["fg"],
        "editorWidget.border": c["border"], "editorWidget.resizeBorder": c["gold"],
        "editorSuggestWidget.background": c["surface"], "editorSuggestWidget.border": c["border"],
        "editorSuggestWidget.foreground": c["fg"], "editorSuggestWidget.selectedBackground": c["selection"],
        "editorSuggestWidget.selectedForeground": c["fg"], "editorSuggestWidget.highlightForeground": c["ansiBlue"],
        "editorSuggestWidget.focusHighlightForeground": c["ansiBlue"],
        "editorHoverWidget.background": c["surface"], "editorHoverWidget.border": c["border"],
        "editorHoverWidget.statusBarBackground": c["surface"],
        "editorMarkerNavigation.background": c["surface"], "editorMarkerNavigationError.background": c["error"],
        "editorMarkerNavigationWarning.background": c["warning"], "editorMarkerNavigationInfo.background": c["weak"],
        "peekView.border": c["gold"], "peekViewTitle.background": c["surface"],
        "peekViewTitleLabel.foreground": c["fg"], "peekViewTitleDescription.foreground": c["muted"],
        "peekViewEditor.background": c["surface"], "peekViewEditorGutter.background": c["surface"],
        "peekViewEditor.matchHighlightBackground": layer("searchBg", p["surface"]),
        "peekViewResult.background": c["bgTool"], "peekViewResult.fileForeground": c["fg"],
        "peekViewResult.lineForeground": c["muted"], "peekViewResult.selectionBackground": c["selection"],
        "peekViewResult.selectionForeground": c["fg"],
        "peekViewResult.matchHighlightBackground": layer("searchBg", p["bgTool"]),
        # diff and merge
        "diffEditor.insertedLineBackground": layer("diffIns"), "diffEditor.removedLineBackground": layer("diffDel"),
        "diffEditor.insertedTextBackground": over(mix(p["diffIns"], p["added"], 0.35), p["diffIns"]),
        "diffEditor.removedTextBackground": over(mix(p["diffDel"], p["deleted"], 0.35), p["diffDel"]),
        "diffEditor.diagonalFill": c["border"], "diffEditor.border": c["border"],
        "diffEditorGutter.insertedLineBackground": layer("diffIns"),
        "diffEditorGutter.removedLineBackground": layer("diffDel"),
        "diffEditorOverview.insertedForeground": c["added"], "diffEditorOverview.removedForeground": c["deleted"],
        "merge.currentHeaderBackground": layer("diffIns"), "merge.currentContentBackground": wash("diffIns"),
        "merge.incomingHeaderBackground": layer("diffMod"), "merge.incomingContentBackground": wash("diffMod"),
        "merge.commonHeaderBackground": layer("diffConf"), "merge.commonContentBackground": wash("diffConf"),
        "merge.border": c["border"],
        # source control
        "gitDecoration.addedResourceForeground": c["ansiGreen"],
        "gitDecoration.modifiedResourceForeground": c["ansiBlue"],
        "gitDecoration.untrackedResourceForeground": c["ansiRed"],
        "gitDecoration.conflictingResourceForeground": c["ansiMagenta"],
        "gitDecoration.deletedResourceForeground": c["muted"],
        "gitDecoration.ignoredResourceForeground": c["muted"],
        "gitDecoration.stageModifiedResourceForeground": c["ansiBlue"],
        "gitDecoration.stageDeletedResourceForeground": c["muted"],
        "gitDecoration.renamedResourceForeground": c["ansiBlue"],
        "gitDecoration.submoduleResourceForeground": c["muted"],
        # popups: menus, quick input, notifications
        "menu.background": c["surface"], "menu.foreground": c["fg"], "menu.border": c["border"],
        "menu.selectionBackground": c["selection"], "menu.selectionForeground": c["fg"],
        "menu.separatorBackground": c["border"],
        "quickInput.background": c["surface"], "quickInput.foreground": c["fg"],
        "quickInputList.focusBackground": c["selection"], "quickInputList.focusForeground": c["fg"],
        "quickInputTitle.background": c["surface"],
        "pickerGroup.foreground": c["ansiBlue"], "pickerGroup.border": c["border"],
        "notifications.background": c["surface"], "notifications.foreground": c["fg"],
        "notifications.border": c["border"], "notificationCenterHeader.background": c["surface"],
        "notificationCenter.border": c["border"], "notificationToast.border": c["border"],
        "notificationLink.foreground": c["azure"], "notificationsErrorIcon.foreground": c["error"],
        "notificationsWarningIcon.foreground": c["warning"], "notificationsInfoIcon.foreground": c["azure"],
        "settings.headerForeground": c["fg"], "settings.modifiedItemIndicator": c["gold"],
        "settings.focusedRowBackground": c["caretRow"], "settings.rowHoverBackground": c["caretRow"],
        "welcomePage.tileBackground": c["surface"], "welcomePage.tileHoverBackground": c["hover"],
        "welcomePage.tileBorder": c["border"], "walkThrough.embeddedEditorBackground": c["surface"],
        "extensionButton.background": c["red"], "extensionButton.foreground": c["redText"],
        "extensionButton.hoverBackground": red_hover,
        "extensionButton.prominentBackground": c["red"], "extensionButton.prominentForeground": c["redText"],
        "extensionButton.prominentHoverBackground": red_hover,
        "extensionBadge.remoteBackground": c["red"], "extensionBadge.remoteForeground": c["redText"],
        "extensionIcon.starForeground": c["gold"],
        # debugging and testing
        "debugToolBar.background": c["surface"], "debugToolBar.border": c["border"],
        "editor.stackFrameHighlightBackground": layer("diffMod"),
        "editor.focusedStackFrameHighlightBackground": layer("diffIns"),
        "debugIcon.breakpointForeground": c["red"], "debugIcon.breakpointCurrentStackframeForeground": c["gold"],
        "debugConsole.infoForeground": c["string"], "debugConsole.warningForeground": c["warning"],
        "debugConsole.errorForeground": c["error"], "debugConsole.sourceForeground": c["muted"],
        "testing.iconPassed": c["ansiGreen"], "testing.iconFailed": c["error"], "testing.iconErrored": c["error"],
        "testing.iconQueued": c["warning"], "testing.iconSkipped": c["muted"], "testing.iconUnset": c["muted"],
        "charts.foreground": c["fg"], "charts.lines": c["border"], "charts.red": c["ansiRed"],
        "charts.blue": c["ansiBlue"], "charts.yellow": c["ansiYellow"], "charts.orange": c["warning"],
        "charts.green": c["ansiGreen"], "charts.purple": c["ansiMagenta"],
    }


def theme(p):
    """The VS Code colour theme for a palette."""
    return {
        "$schema": "vscode://schemas/color-theme",
        "name": p["name"], "type": "dark" if p["dark"] else "light", "semanticHighlighting": True,
        "colors": workbench(p), "tokenColors": token_colors(p), "semanticTokenColors": semantic_token_colors(p),
    }
