"""Qt Creator theme and editor colour scheme generated from a palette.

A theme is a .creatortheme file in the user's themes folder, which colours Qt Creator's window, and names the editor
colour scheme, a style scheme XML file in the user's styles folder. Qt Creator reads a theme's includes only from the
theme's own folder, so the theme sets each of the colour roles of Qt Creator 20 itself (ROLES, from theme.h), from a
[Palette] of the theme's colours: the roles of the window, panels, output, terminal and version control by hand, and
those of Qt Design Studio by the part their names describe. The layout follows the Islands of the other targets: the
mode bar and status bar on the frame, panels on bgTool, the editor and the selected mode on bg, popups on surface.

The editor colour scheme sets each text style of Qt Creator 20 (STYLES, from texteditorconstants.cpp) to the role that
the other targets give the construct. Qt Creator colours C++ and QML with its code models and the other languages with
KSyntaxHighlighting's definitions, which it maps to the same styles.
"""
import colorsys, json, os, re
import xml.etree.ElementTree as ET

from .nvim import name  # noqa: F401 - the files take the names of Neovim's schemes
from .terminals import colours as terminal_colours, contrast
from .vscode import mix

# The colour roles of Qt Creator 20 (theme.h), which the theme sets every one of.
with open(os.path.join(os.path.dirname(__file__), "qtcreator.json"), encoding="utf-8") as f:
    ROLES = tuple(json.load(f)["roles"])
# The text styles of Qt Creator 20 (texteditorconstants.cpp, nameForStyle).
STYLES = (
    "Text", "Link", "Selection", "LineNumber", "SearchResult", "SearchResultAlt1", "SearchResultAlt2",
    "SearchResultContainingFunction", "SearchScope", "Parentheses", "ParenthesesMismatch", "AutoComplete",
    "CurrentLine", "CurrentLineNumber", "Occurrences", "Occurrences.Unused", "Occurrences.Rename", "Number", "String",
    "Type", "Concept", "Namespace", "Local", "Parameter", "Global", "Field", "Static", "VirtualMethod", "Function",
    "Keyword", "PrimitiveType", "Operator", "Overloaded Operator", "Punctuation", "Preprocessor", "Macro", "Label",
    "Attribute", "Comment", "Doxygen.Comment", "Doxygen.Tag", "VisualWhitespace", "QmlLocalId", "QmlExternalId",
    "QmlTypeId", "QmlRootObjectProperty", "QmlScopeObjectProperty", "QmlExternalObjectProperty", "JsScopeVar",
    "JsImportVar", "JsGlobalVar", "QmlStateName", "Binding", "DisabledCode", "AddedLine", "RemovedLine", "DiffFile",
    "DiffLocation", "DiffFileLine", "DiffContextLine", "DiffSourceLine", "DiffSourceChar", "DiffDestLine",
    "DiffDestChar", "LogChangeLine", "LogAuthorName", "LogCommitDate", "LogCommitHash", "LogCommitSubject",
    "LogDecoration", "Error", "ErrorContext", "Warning", "WarningContext", "Info", "InfoContext", "Declaration",
    "FunctionDefinition", "OutputArgument", "StaticMember", "CocoCodeAdded", "CocoPartiallyCovered",
    "CocoNotCovered", "CocoFullyCovered", "CocoManuallyValidated", "CocoDeadCode", "CocoExecutionCountTooLow",
    "CocoNotCoveredInfo", "CocoCoveredInfo", "CocoManuallyValidatedInfo",
)
# The flags of Qt Creator 20 (theme.h), as its own 2024 themes set them.
FLAGS = {"ComboBoxDrawTextShadow": "false", "DerivePaletteFromTheme": "true", "DrawIndicatorBranch": "true",
         "DrawSearchResultWidgetFrame": "false", "DrawTargetSelectorBottom": "false", "DrawToolBarHighlights": "false",
         "DrawToolBarBorders": "true", "FlatToolBars": "true", "FlatSideBarIcons": "true", "FlatProjectsMode": "true",
         "FlatMenuBar": "true", "ToolBarIconShadow": "false", "WindowColorAsBase": "false"}


def palette(p):
    """[Palette] name → aarrggbb: the palette's colours that the theme names, and the terminal colours."""
    keys = ("bg", "bgTool", "bgUi", "frame", "surface", "hover", "border", "fg", "muted", "disabled", "selection",
            "selInactive", "caretRow", "searchBg", "searchBorder", "red", "redText", "azure", "gold", "keyword",
            "type", "method", "field", "annotation", "constant", "string", "added", "modified", "deleted")
    out = {key: "ff" + p[key].lower() for key in keys}
    for name_, colour in zip(("black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"),
                             terminal_colours(p)["ansi"]):
        out[f"ansi_{name_}"] = "ff" + colour[1:].lower()
    out["ansi_bright_black"] = "ff" + p["muted"].lower()
    out["ansi_bright_white"] = "ff" + p["fg"].lower()
    # translucent layers: the overlay behind code model icons, and accents faded towards bg for the design tokens
    out["overlay"] = "b3" + p["bg"].lower()
    for key in ("ansiBlue", "ansiYellow", "ansiGreen", "ansiRed"):
        out[f"{key}_muted"] = "ff" + mix(p[key], p["bg"], 0.45).lower()
        out[f"{key}_subtle"] = "ff" + mix(p[key], p["bg"], 0.75).lower()
    return out


def roles(p):
    """Colour role → [Palette] name or aarrggbb, for the roles that the theme sets by hand."""
    out = {
        # the window: the frame around the panels, panels on bgTool, the editor on bg, popups on surface
        "BackgroundColorDark": "frame", "BackgroundColorHover": "hover", "BackgroundColorNormal": "bgTool",
        "BackgroundColorSelected": "selection", "BackgroundColorDisabled": "bgUi",
        "BadgeLabelBackgroundColorChecked": "bgTool", "BadgeLabelBackgroundColorUnchecked": "selection",
        "BadgeLabelTextColorChecked": "fg", "BadgeLabelTextColorUnchecked": "fg", "ComboBoxTextColor": "fg",
        "DetailsWidgetBackgroundColor": "surface", "DockWidgetResizeHandleColor": "frame",
        "EditorPlaceholderColor": "bg", "FancyToolBarSeparatorColor": "border",
        "FancyTabBarSelectedBackgroundColor": "bg", "FancyTabWidgetDisabledSelectedTextColor": "disabled",
        "FancyTabWidgetDisabledUnselectedTextColor": "disabled", "FancyTabWidgetEnabledSelectedTextColor": "fg",
        "FancyTabWidgetEnabledUnselectedTextColor": "muted", "FancyToolButtonHoverColor": "hover",
        "FancyToolButtonSelectedColor": "selection", "FancyToolButtonHighlightColor": "fg",
        "InfoBarBackground": "surface", "InfoBarText": "fg", "MenuBarItemTextColorDisabled": "disabled",
        "MenuBarItemTextColorNormal": "fg", "MenuItemTextColorDisabled": "disabled", "MenuItemTextColorNormal": "fg",
        "MiniProjectTargetSelectorBackgroundColor": "surface", "MiniProjectTargetSelectorBorderColor": "border",
        "MiniProjectTargetSelectorTextColor": "fg", "OutputPaneButtonFlashColor": "red",
        "OutputPaneToggleButtonTextColorChecked": "fg", "OutputPaneToggleButtonTextColorUnchecked": "muted",
        "PanelStatusBarBackgroundColor": "frame", "PanelTextColorDark": "fg", "PanelTextColorMid": "muted",
        "PanelTextColorLight": "fg", "ProgressBarColorError": "ansi_red", "ProgressBarColorFinished": "ansi_green",
        "ProgressBarColorNormal": "ansi_blue", "ProgressBarTitleColor": "fg", "ProgressBarBackgroundColor": "bgUi",
        "SplitterColor": "frame", "TextColorDisabled": "disabled", "TextColorError": "ansi_red",
        "TextColorHighlightBackground": "searchBg", "TextColorLink": "azure", "TextColorNormal": "fg",
        # Qt's palette, which DerivePaletteFromTheme gives every widget
        "PaletteWindow": "bgTool", "PaletteWindowText": "fg", "PaletteBase": "bg", "PaletteAlternateBase": "bgUi",
        "PaletteToolTipBase": "surface", "PaletteToolTipText": "fg", "PaletteText": "fg", "PaletteButton": "surface",
        "PaletteButtonText": "fg", "PaletteBrightText": "redText", "PaletteHighlight": "selection",
        "PaletteHighlightedText": "fg", "PaletteLink": "azure", "PaletteLinkVisited": "ansi_magenta",
        "PaletteLight": "hover", "PaletteMidlight": "border", "PaletteDark": "frame", "PaletteMid": "border",
        "PaletteShadow": "frame", "PalettePlaceholderText": "muted", "PaletteAccent": "ansi_blue",
        # icons
        "IconsBaseColor": "muted", "IconsDisabledColor": "disabled", "IconsInfoColor": "ansi_blue",
        "IconsInfoToolBarColor": "ansi_blue", "IconsWarningColor": "ansi_yellow",
        "IconsWarningToolBarColor": "ansi_yellow", "IconsErrorColor": "ansi_red", "IconsErrorToolBarColor": "ansi_red",
        "IconsRunColor": "ansi_green", "IconsRunToolBarColor": "ansi_green", "IconsStopColor": "ansi_red",
        "IconsStopToolBarColor": "ansi_red", "IconsInterruptColor": "ansi_blue",
        "IconsInterruptToolBarColor": "ansi_blue", "IconsDebugColor": "ansi_magenta",
        "IconsNavigationArrowsColor": "ansi_blue", "IconsBuildHammerHandleColor": "muted",
        "IconsBuildHammerHeadColor": "fg",
        # code model icons in the roles of the constructs they stand for
        "IconsCodeModelKeywordColor": "keyword", "IconsCodeModelClassColor": "type",
        "IconsCodeModelStructColor": "type", "IconsCodeModelFunctionColor": "method",
        "IconsCodeModelVariableColor": "field", "IconsCodeModelEnumColor": "type",
        "IconsCodeModelMacroColor": "annotation", "IconsCodeModelAttributeColor": "annotation",
        "IconsCodeModelUniformColor": "constant", "IconsCodeModelVaryingColor": "string",
        "IconsCodeModelOverlayBackgroundColor": "overlay", "IconsCodeModelOverlayForegroundColor": "fg",
        "CodeModel_Error_TextMarkColor": "ansi_red", "CodeModel_Warning_TextMarkColor": "ansi_yellow",
        "CodeModel_Info_TextMarkColor": "azure",
        # output panes in the terminal colours, which the build checks as text on bg and bgTool
        "OutputPanes_DebugTextColor": "fg", "OutputPanes_ErrorMessageTextColor": "ansi_red",
        "OutputPanes_MessageOutput": "ansi_cyan", "OutputPanes_NormalMessageTextColor": "ansi_cyan",
        "OutputPanes_StdErrTextColor": "ansi_red", "OutputPanes_StdOutTextColor": "fg",
        "OutputPanes_WarningMessageTextColor": "ansi_yellow", "OutputPanes_TestPassTextColor": "ansi_green",
        "OutputPanes_TestFailTextColor": "ansi_red", "OutputPanes_TestXFailTextColor": "ansi_green",
        "OutputPanes_TestXPassTextColor": "ansi_red", "OutputPanes_TestSkipTextColor": "muted",
        "OutputPanes_TestWarnTextColor": "ansi_yellow", "OutputPanes_TestFatalTextColor": "ansi_red",
        "OutputPanes_TestDebugTextColor": "ansi_cyan", "OutputPanes_SearchResultBackgroundColor": "searchBg",
        "Debugger_LogWindow_LogInput": "ansi_cyan", "Debugger_LogWindow_LogStatus": "ansi_green",
        "Debugger_LogWindow_LogTime": "muted", "Debugger_WatchItem_ValueNormal": "fg",
        "Debugger_WatchItem_ValueInvalid": "disabled", "Debugger_WatchItem_ValueChanged": "ansi_red",
        "Timeline_TextColor": "fg", "Timeline_BackgroundColor1": "bg", "Timeline_BackgroundColor2": "bgUi",
        "Timeline_DividerColor": "border", "Timeline_HighlightColor": "ansi_blue",
        "Timeline_PanelBackgroundColor": "bgTool", "Timeline_PanelHeaderColor": "frame", "Timeline_HandleColor": "muted",
        "Timeline_RangeColor": "selection",
        # version control in the colours that the other targets give file status
        "VcsBase_FileStatusUnknown_TextColor": "fg", "VcsBase_FileUntracked_TextColor": "ansi_red",
        "VcsBase_FileAdded_TextColor": "ansi_green", "VcsBase_FileModified_TextColor": "ansi_blue",
        "VcsBase_FileDeleted_TextColor": "muted", "VcsBase_FileRenamed_TextColor": "ansi_cyan",
        "VcsBase_FileUnmerged_TextColor": "ansi_magenta",
        "Bookmarks_TextMarkColor": "ansi_blue", "TextEditor_SearchResult_ScrollBarColor": "searchBorder",
        "TextEditor_Selection_ScrollBarColor": "selection", "TextEditor_CurrentLine_ScrollBarColor": "muted",
        "Debugger_Breakpoint_TextMarkColor": "ansi_red", "Navigator_DefaultColor": "fg",
        "Navigator_3DColor": "ansi_blue", "Navigator_2DColor": "ansi_green", "Navigator_MaterialColor": "ansi_magenta",
        "ProjectExplorer_TaskError_TextMarkColor": "ansi_red", "ProjectExplorer_TaskWarn_TextMarkColor": "ansi_yellow",
        "DspillTextEdit": "fg",
        # the terminal, on bgTool as in the other targets' terminal panels
        "TerminalForeground": "fg", "TerminalBackground": "bgTool", "TerminalSelection": "selection",
        "TerminalFindMatch": "searchBg",
        "ChatUserMessageBackground": "surface", "ChatToolCallBackground": "bgUi", "ChatPlanBackground": "bgTool",
        # Qt Quick Designer
        "QmlDesigner_BackgroundColor": "bgTool", "QmlDesigner_HighlightColor": "ansi_blue",
        "QmlDesigner_FormEditorSelectionColor": "ansi_blue", "QmlDesigner_FormEditorForegroundColor": "fg",
        "QmlDesigner_BackgroundColorDarker": "frame", "QmlDesigner_BackgroundColorDarkAlternate": "bgUi",
        "QmlDesigner_TabLight": "fg", "QmlDesigner_TabDark": "frame", "QmlDesigner_ButtonColor": "surface",
        "QmlDesigner_BorderColor": "border", "QmlDesigner_FormeditorBackgroundColor": "bg",
        "QmlDesigner_AlternateBackgroundColor": "bgUi", "QmlDesigner_ScrollBarHandleColor": "muted",
        # the design tokens of Qt Creator's 2024 themes
        "Token_Basic_Black": "frame", "Token_Basic_White": "fg", "Token_Accent_Default": "ansi_blue",
        "Token_Accent_Muted": "ansiBlue_muted", "Token_Accent_Subtle": "ansiBlue_subtle",
        "Token_Background_Default": "bgTool", "Token_Background_Muted": "bgUi", "Token_Background_Subtle": "surface",
        "Token_Foreground_Default": "muted", "Token_Foreground_Muted": "border", "Token_Foreground_Subtle": "hover",
        "Token_Text_Default": "fg", "Token_Text_Muted": "muted", "Token_Text_Subtle": "disabled",
        "Token_Text_Accent": "ansi_blue", "Token_Text_On_Accent": "bg", "Token_Stroke_Strong": "fg",
        "Token_Stroke_Muted": "muted", "Token_Stroke_Subtle": "border",
        "Token_Notification_Alert_Default": "ansi_yellow", "Token_Notification_Alert_Muted": "ansiYellow_muted",
        "Token_Notification_Alert_Subtle": "ansiYellow_subtle", "Token_Notification_Success_Default": "ansi_green",
        "Token_Notification_Success_Muted": "ansiGreen_muted", "Token_Notification_Success_Subtle": "ansiGreen_subtle",
        "Token_Notification_Neutral_Default": "ansi_blue", "Token_Notification_Neutral_Muted": "ansiBlue_muted",
        "Token_Notification_Neutral_Subtle": "ansiBlue_subtle", "Token_Notification_Danger_Default": "ansi_red",
        "Token_Notification_Danger_Muted": "ansiRed_muted", "Token_Notification_Danger_Subtle": "ansiRed_subtle",
        "Token_Gradient01_Start": "ansi_blue", "Token_Gradient01_End": "ansi_magenta",
        "Token_Gradient02_Start": "ansi_green", "Token_Gradient02_End": "ansi_cyan",
    }
    for i, colour in enumerate(("black", "red", "green", "yellow", "blue", "magenta", "cyan", "white")):
        out[f"TerminalAnsi{i}"] = f"ansi_{colour}"
        out[f"TerminalAnsi{i + 8}"] = {"black": "ansi_bright_black", "white": "ansi_bright_white"}.get(
            colour, f"ansi_{colour}")
    # a role's disabled form: text in the disabled colour, surfaces as they are
    for role in [r for r in out if r.startswith("Palette") and r != "PaletteAccent"]:
        out[f"{role}Disabled"] = "disabled" if role.endswith("Text") else out[role]
    out["PaletteAccentDisabled"] = "disabled"
    return out


# Words in the names of Qt Design Studio's roles → the [Palette] name of the part they describe, the first match
# winning: states before parts, parts before the general background.
DESIGN_STUDIO = (
    ("error|danger|red", "ansi_red"), ("warning|alert|amber", "ansi_yellow"),
    ("green|success|running", "ansi_green"), ("disabled|blocked|unimported", "disabled"),
    ("placeholder", "muted"), ("inactive(?:text|icon)", "muted"),
    ("textselection(?!edtext)", "selection"), ("text|label|icon", "fg"),
    ("selection|selected|interaction|focus|highlight|current|activetrack|accent|indicator|link|primary", "selection"),
    ("hover|press", "hover"), ("outline|border|stroke|separator|splitter|divider|axis|branch|track", "border"),
    ("handle|scrollbar", "muted"), ("tooltip|popup|popout", "surface"),
    ("statusbar|toolbar|titlebar|dock|tabcontainer|welcome|header", "frame"),
    ("overlay", "overlay"), ("action|binding|alias|keyframe|jit|connection", "ansi_blue"),
    ("foreground|forground|white", "fg"), ("black", "frame"),
    ("background|base|panel|state|thumbnail|pill|control|tab|navigator|table|section|item|color|neutral", "bgTool"),
)


def design_studio(role):
    """The [Palette] name for a role of Qt Design Studio, by the words of its name."""
    key = role.lower().replace("_", "")
    for words, colour in DESIGN_STUDIO:
        if re.search(words, key):
            return colour
    raise ValueError(f"no colour for {role}")


def colour_roles(p):
    """Every colour role of ROLES → [Palette] name or aarrggbb."""
    explicit = roles(p)
    unknown = set(explicit) - set(ROLES)
    if unknown:
        raise ValueError(f"roles that Qt Creator does not have: {sorted(unknown)}")
    return {role: explicit.get(role) or design_studio(role) for role in ROLES}


def theme(t, source):
    """The themes/<theme>.creatortheme file for a theme dict. source is the URL of the theme folder."""
    p = t["palette"]
    colours = colour_roles(p)
    lines = [
        f"; {p['name']}: a Heritage Themes theme for Qt Creator.",
        f"; Generated from {source}; changes here are overwritten.",
        "[General]",
        f"ThemeName={p['name']}",
        "PreferredStyles=",
        f"DefaultTextEditorColorScheme={name(t)}.xml",
        "DefaultToolbarStyle=Relaxed",
        "",
        "[Palette]",
        *(f"{key}={value}" for key, value in palette(p).items()),
        "",
        "[Colors]",
        *(f"{role}={colour}" for role, colour in colours.items()),
        "",
        "[Flags]",
        *(f"{flag}={value}" for flag, value in FLAGS.items()),
        f"DarkUserInterface={'true' if p['dark'] else 'false'}",
    ]
    return "\n".join(lines) + "\n"


def text_styles(p):
    """Text style → attributes: foreground and background as palette keys, bold and italic, and underlineColor as a
    palette key with underlineStyle. Mixin styles (Declaration, FunctionDefinition and others) add to the style of
    the construct, so they set what they change."""
    kw = {"bold": True} if p.get("kwBold", not p["dark"]) else {}
    def f(fg=None, bg=None, **flags):
        return {**({"foreground": fg} if fg else {}), **({"background": bg} if bg else {}), **flags}
    def underline(colour, style):
        return {"underlineColor": colour, "underlineStyle": style}
    return {
        "Text": f("fg", "bg"), "Link": f("azure", underline=True),
        "Selection": f(bg="selection"), "LineNumber": f("lineNo", "bg"),
        "SearchResult": f(bg="searchBg"), "SearchResultAlt1": f(bg="underCaret"), "SearchResultAlt2": f(bg="writeCaret"),
        "SearchResultContainingFunction": f("fg", "caretRow"), "SearchScope": f(bg="selInactive"),
        # a matching parenthesis in bold blue, as the terminal targets draw brace matches on bg
        "Parentheses": f("ansiBlue", bold=True), "ParenthesesMismatch": f("redText", "red"),
        "AutoComplete": f(bg="selInactive"), "CurrentLine": f(bg="caretRow"),
        "CurrentLineNumber": f("lineNoCaret", bold=True),
        "Occurrences": f(bg="underCaret"), "Occurrences.Unused": f("muted", italic=True),
        "Occurrences.Rename": f(bg="writeCaret"),
        "Number": f("number"), "String": f("string"), "Type": f("type"), "Concept": f("type", italic=True),
        "Namespace": f("fg"), "Local": f("fg"), "Parameter": f("param"), "Global": f("field", italic=True),
        "Field": f("field"), "Static": f("field", italic=True), "VirtualMethod": f(italic=True), "Function": f("call"),
        "Keyword": f("keyword", **kw), "PrimitiveType": f("keyword", **kw), "Operator": f("op"),
        "Overloaded Operator": f("op"), "Punctuation": f("op"), "Preprocessor": f("keyword", **kw),
        "Macro": f("annotation"), "Label": f("label", bold=True), "Attribute": f("annotation"),
        "Comment": f("comment", italic=True), "Doxygen.Comment": f("doc", italic=True),
        "Doxygen.Tag": f("docTag", bold=True, italic=True), "VisualWhitespace": f("guide"),
        "QmlLocalId": f("field", italic=True), "QmlExternalId": f("field", italic=True), "QmlTypeId": f("type"),
        "QmlRootObjectProperty": f("field"), "QmlScopeObjectProperty": f("field"),
        "QmlExternalObjectProperty": f("field", italic=True), "JsScopeVar": f("fg"), "JsImportVar": f("type"),
        "JsGlobalVar": f("field", italic=True), "QmlStateName": f("string"), "Binding": f("call"),
        "DisabledCode": f("muted"),
        # diffs in the console colours and the diff backgrounds of the other targets
        "AddedLine": f("ansiGreen"), "RemovedLine": f("ansiRed"), "DiffFile": f("ansiBlue", bold=True),
        "DiffLocation": f("ansiCyan"), "DiffFileLine": f("fg", "diffMod"), "DiffContextLine": f("fg", "caretRow"),
        "DiffSourceLine": f("fg", "diffDel"), "DiffSourceChar": f("fg", "deletedChar"),
        "DiffDestLine": f("fg", "diffIns"), "DiffDestChar": f("fg", "addedChar"),
        "LogChangeLine": f("ansiRed"), "LogAuthorName": f("ansiMagenta"), "LogCommitDate": f("ansiBlue"),
        "LogCommitHash": f("ansiYellow"), "LogCommitSubject": f("fg"), "LogDecoration": f("ansiCyan"),
        # diagnostics as underlines in the diagnostic colours
        "Error": underline("error", "WaveUnderline"), "ErrorContext": underline("error", "DotLine"),
        "Warning": underline("warning", "WaveUnderline"), "WarningContext": underline("warning", "DotLine"),
        "Info": underline("azure", "DashUnderline"), "InfoContext": underline("azure", "DotLine"),
        "Declaration": f(bold=True), "FunctionDefinition": f("method", bold=True), "OutputArgument": f(italic=True),
        "StaticMember": f(italic=True),
        # code coverage of Coco as the diff backgrounds
        "CocoCodeAdded": f(bg="diffIns"), "CocoPartiallyCovered": f(bg="diffConf"), "CocoNotCovered": f(bg="diffDel"),
        "CocoFullyCovered": f(bg="diffIns"), "CocoManuallyValidated": f(bg="diffMod"), "CocoDeadCode": f("muted"),
        "CocoExecutionCountTooLow": f(bg="diffConf"), "CocoNotCoveredInfo": underline("error", "DotLine"),
        "CocoCoveredInfo": underline("added", "DotLine"), "CocoManuallyValidatedInfo": underline("modified", "DotLine"),
    }


def tint(p, base, accent):
    """The diff background base moved towards accent as far as the text stays at 4.5:1 on it, in steps of 5%, for
    the characters that a diff changes within a changed line."""
    for step in range(10, -1, -1):
        colour = mix(p[base], p[accent], step / 20)
        if contrast(p["fg"], colour) >= 4.5:
            return colour
    return p[base]


def hexes(p):
    """Palette key, ANSI colour name (ansiBlack to ansiWhite) or diff character tint → #RRGGBB."""
    out = {k: "#" + v for k, v in p.items() if isinstance(v, str) and re.fullmatch(r"[0-9A-F]{6}", v)}
    out["addedChar"] = "#" + tint(p, "diffIns", "added")
    out["deletedChar"] = "#" + tint(p, "diffDel", "deleted")
    out.update({f"ansi{n.title()}": colour for n, colour in zip(
        ("black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"), terminal_colours(p)["ansi"])})
    return out


def scheme(t, source):
    """The styles/<theme>.xml editor colour scheme for a theme dict."""
    p = t["palette"]
    colours = hexes(p)
    root = ET.Element("style-scheme", version="1.0", name=p["name"])
    root.append(ET.Comment(f" {p['name']}: a Heritage Themes colour scheme for Qt Creator. Generated from {source}; "
                           "changes here are overwritten. "))
    for style, attributes in text_styles(p).items():
        element = ET.SubElement(root, "style", name=style)
        for key, value in attributes.items():
            if key in ("foreground", "background", "underlineColor"):
                value = colours[value].lower()
            element.set(key, str(value).lower() if isinstance(value, bool) else value)
    ET.indent(root)
    return '<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(root, encoding="unicode") + "\n"


def styles(p):
    """Element → dict(fg, bg) as #RRGGBB, for the build's contrast check: each text style with a foreground on the
    background it is drawn on, bg unless it sets one, and the window's text on its surfaces."""
    colours = hexes(p)
    out = {style: dict(fg=colours[a["foreground"]], bg=colours[a.get("background", "bg")])
           for style, a in text_styles(p).items()
           if "foreground" in a and style not in ("LineNumber", "CurrentLineNumber", "VisualWhitespace")}
    for element, fg, bg in (("panel text", "fg", "bgTool"), ("muted panel text", "muted", "bgTool"),
                            ("mode bar text", "muted", "frame"), ("selected mode", "fg", "bg"),
                            ("popup text", "fg", "surface"), ("selected item", "fg", "selection"),
                            ("status bar text", "fg", "frame"), ("terminal text", "fg", "bgTool")):
        out[element] = dict(fg=colours[fg], bg=colours[bg])
    return out


def scroll_bar_shades(p):
    """The shades that Qt's Fusion style paints a scroll bar with: the gradients of the groove and handle on a light
    palette, from the Button colour (surface) as QFusionStylePrivate::buttonColor and the CC_ScrollBar code of
    qfusionstyle.cpp derive them; and on a dark palette the handle's flat fill and the groove, lightened from the
    editor's background."""
    def hsv(colour):
        return colorsys.rgb_to_hsv(*(int(colour[i:i + 2], 16) / 255 for i in (0, 2, 4)))
    def hex_(h, s, v):
        return "#" + "".join(f"{round(c * 255):02X}" for c in colorsys.hsv_to_rgb(h, s, v))
    def lighter(h, s, v, factor):
        v *= factor / 100
        return (h, max(0.0, s - (v - 1)), 1.0) if v > 1 else (h, s, v)
    surface = p["surface"]
    r, g, b = (int(surface[i:i + 2], 16) for i in (0, 2, 4))
    grey = (r * 11 + g * 16 + b * 5) // 32  # qGray
    h, s, v = lighter(*hsv(surface), 100 + max(1, (180 - grey) // 6))
    button = (h, s * 0.75, v)
    start = colorsys.hsv_to_rgb(*lighter(*button, 118))
    stop = colorsys.hsv_to_rgb(*button)
    middle = "#" + "".join(f"{round((0.4 * x + 0.6 * y) * 255):02X}" for x, y in zip(start, stop))  # mergedColors 40
    return [hex_(*button), hex_(*lighter(*button, 108)), hex_(h, s * 0.75, v * 100 / 105),
            hex_(h, s * 0.75, v * 100 / 107), middle,
            *(hex_(*lighter(*hsv(p["bg"]), factor)) for factor in (155, 157))]


def pixel_palette(p):
    """What scripts/editors/pixels.py checks a screenshot against: the editor, cropped from the window that
    scripts/editors/shoot.py opens at 1100x700, whose mode bar, panels, tool bar and file icons Qt Creator draws with
    images of its own."""
    colours = {"#" + v for v in p.values() if isinstance(v, str) and re.fullmatch(r"[0-9A-F]{6}", v)}
    colours |= set(terminal_colours(p)["ansi"])
    return dict(background="#" + p["bg"],
                backgrounds=["#" + p[k] for k in ("bgTool", "frame", "surface", "caretRow", "selection", "hover",
                                                  "bgUi", "underCaret")] + scroll_bar_shades(p),
                foregrounds=sorted(colours), crop=[84, 22, 312, 14],
                # Qt draws the text cursor by inverting the background
                allowed=["#" + "".join(f"{255 - int(p['bg'][i:i + 2], 16):02X}" for i in (0, 2, 4))])
