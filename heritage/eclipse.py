"""Eclipse themes generated from a palette: one plugin with a CSS theme and a TextMate theme for each Heritage theme.

Eclipse's appearance themes are stylesheets that the plugin contributes to the org.eclipse.e4.ui.css.swt.theme
extension point. A stylesheet styles the workbench's widgets by their SWT classes and part identifiers, as Eclipse's
own dark theme does (org.eclipse.ui.themes), and sets the colour preferences of the editors and of the plugins that
contribute colours to Eclipse's own dark theme (JDT, debug, Ant, EGit, compare, the generic editor, LSP4E, TM4E's
bracket pairs, EclEmma and Mylyn) as IEclipsePreferences, which Eclipse applies when the theme is chosen. Those plugins contribute
their colours to Eclipse's dark theme by its identifier only, so the stylesheet sets each of them for the Heritage
theme. The other languages open in the generic editor, which TM4E highlights with TextMate grammars: the plugin also
contributes a TextMate theme of the same name and colours (heritage.amp's, which take the Sublime Text scheme's rules),
which the user chooses in TM4E's preferences, as TM4E reads its theme before an appearance theme's preferences
apply.

The layout follows the Islands of the other targets: the window, tool bars and status line on the frame, views on
bgTool, the editor on bg, fields and popups on surface. Eclipse prefers dark GTK widgets for a theme whose identifier
contains "dark", so a dark Heritage theme's identifier does.
"""
import io, re, zipfile

from . import amp
from .nvim import name  # noqa: F401 - the files take the names of Neovim's schemes
from .terminals import colours as terminal_colours, contrast
from .vscode import mix

BUNDLE = "heritage.themes.eclipse"


def theme_id(t):
    """The CSS theme's identifier, with "dark" in it for a dark theme, as Eclipse looks for."""
    return f"{BUNDLE}.{'dark' if t['palette']['dark'] else 'light'}.{name(t)}"


def tm4e_id(t):
    return f"{BUNDLE}.textmate.{name(t)}"


def rgb(colour):
    """Eclipse's r,g,b for #RRGGBB or RRGGBB."""
    colour = colour.lstrip("#")
    return ",".join(str(int(colour[i:i + 2], 16)) for i in (0, 2, 4))


def hexes(p):
    """Palette key or ANSI colour name (ansiBlack to ansiWhite) → #RRGGBB, with the diff character tints."""
    out = {k: "#" + v for k, v in p.items() if isinstance(v, str) and re.fullmatch(r"[0-9A-F]{6}", v)}
    out.update({f"ansi{n.title()}": colour for n, colour in zip(
        ("black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"), terminal_colours(p)["ansi"])})
    out["caret"] = "#" + p.get("caret", p["gold"])
    for key, base, accent in (("addedChar", "diffIns", "added"), ("deletedChar", "diffDel", "deleted")):
        out[key] = "#" + next((mix(p[base], p[accent], step / 20) for step in range(10, -1, -1)
                               if contrast(p["fg"], mix(p[base], p[accent], step / 20)) >= 4.5), p[base])
    return out


# The workbench colour definitions of Eclipse's dark theme (e4-dark_ide_colorextensions.css) → palette key.
COLOR_DEFINITIONS = {
    "DARK_BACKGROUND": "frame", "DARK_FOREGROUND": "fg",
    "INACTIVE_UNSELECTED_TABS_COLOR_START": "bgTool", "INACTIVE_UNSELECTED_TABS_COLOR_END": "bgTool",
    "INACTIVE_TAB_BG_START": "bgTool", "INACTIVE_TAB_BG_END": "bgTool",
    "INACTIVE_TAB_OUTER_KEYLINE_COLOR": "border", "INACTIVE_TAB_INNER_KEYLINE_COLOR": "border",
    "INACTIVE_TAB_OUTLINE_COLOR": "border", "INACTIVE_TAB_TEXT_COLOR": "muted",
    "INACTIVE_TAB_UNSELECTED_TEXT_COLOR": "muted", "INACTIVE_TAB_SELECTED_TEXT_COLOR": "fg",
    "ACTIVE_UNSELECTED_TABS_COLOR_START": "bgTool", "ACTIVE_UNSELECTED_TABS_COLOR_END": "bgTool",
    "ACTIVE_TAB_BG_START": "bgTool", "ACTIVE_TAB_BG_END": "bgTool",
    "ACTIVE_TAB_OUTER_KEYLINE_COLOR": "border", "ACTIVE_TAB_INNER_KEYLINE_COLOR": "border",
    "ACTIVE_TAB_OUTLINE_COLOR": "border", "ACTIVE_TAB_TEXT_COLOR": "fg",
    "ACTIVE_TAB_UNSELECTED_TEXT_COLOR": "muted", "ACTIVE_TAB_SELECTED_TEXT_COLOR": "fg",
    "ACTIVE_NOFOCUS_TAB_BG_START": "bgTool", "ACTIVE_NOFOCUS_TAB_BG_END": "bgTool",
    "ACTIVE_NOFOCUS_TAB_TEXT_COLOR": "muted", "ACTIVE_NOFOCUS_TAB_SELECTED_TEXT_COLOR": "fg",
    "LINK_COLOR": "azure",
}


def widget_rules(p):
    """(selectors, {property: palette key or literal}) per rule, the selectors of Eclipse's dark theme."""
    window = ("Shell, Composite, ScrolledComposite, ExpandableComposite, Canvas, TabFolder, CLabel, Label, CoolBar, "
              "Sash, Group, RefactoringLocationControl, ChangeParametersControl, Link, FilteredTree, "
              "ProxyEntriesComposite, NonProxyHostsComposite, DelayedFilterCheckboxTree, Splitter, "
              "ScrolledPageContent, ViewForm, LaunchConfigurationFilteredTree, ContainerSelectionGroup, "
              "BrowseCatalogItem, EncodingSettings, ProgressMonitorPart, DocCommentOwnerComposite, NewServerComposite, "
              "NewManualServerComposite, ServerTypeComposite, FigureCanvas, DependenciesComposite, "
              "ListEditorComposite, WrappedPageBook, CompareStructureViewerSwitchingPane, "
              "CompareContentViewerSwitchingPane, QualifiedNameComponent, RefactoringStatusViewer, MessageLine, "
              "Button, Composite > *, Composite > * > *, Group > StyledText")
    part = (".MPart Composite, .MPart Composite > *, .MPart Composite > * > *, .MPart Label, .MPart ScrolledForm, "
            ".MPart Form, .MPart Section, .MPart FormText, .MPart Link, .MPart Sash, .MPart Button, .MPart Group, "
            ".MPart SashForm, .MPart Tree, .MPart FilteredTree, .MPart RegistryFilteredTree, "
            ".MPart PageSiteComposite, .MPart DependenciesComposite, .MPart Text[style~='SWT.READ_ONLY'], "
            ".MPart FigureCanvas, .MPart ListEditorComposite, .MPart ScrolledComposite, "
            ".MPart ScrolledComposite ProgressInfoItem, .MPart Form ScrolledPageBook, "
            ".MPart DependenciesComposite > SashForm > Section > *")
    field = {"background-color": "surface", "color": "fg"}
    return [
        # the window: dialogs, tool bars, the status line and the space between parts on the frame
        (window, {"background-color": "frame", "color": "fg"}),
        ("Button.disabled", {"color": "disabled"}),
        ("TabFolder > *, CTabFolder > *, TabFolder > Composite > *, CTabFolder > Composite > *, "
         "TabFolder > Composite > * > *", {"color": "fg"}),
        ("ToolBar", {"background-color": "inherit"}),
        # fields and popups on surface
        ("Combo, List, Text, Spinner, CCombo", field),
        ("Composite > StyledText, Shell [style~='SWT.DROP_DOWN'] > StyledText, SashForm > StyledText", field),
        ("Text[style~='SWT.SEARCH'], Text[style~='SWT.SEARCH'] + Label", field),
        ("Text[style~='SWT.READ_ONLY']", {"background-color": "frame", "color": "muted"}),
        ("Shell Tree, Shell Table, Shell List", {"background-color": "bgTool"}),
        ("DatePicker, DatePicker > Text, ScheduleDatePicker, ScheduleDatePicker > Text", field),
        ("ScrolledFormText, FormText", {"background-color": "bgTool", "color": "fg"}),
        ("Table, Tree, RegistryFilteredTree", {"background-color": "inherit", "color": "fg"}),
        ("Hyperlink, ImageHyperlink", {"background-color": "inherit", "color": "azure"}),
        ("ViewerPane, DrillDownComposite", {"background-color": "bgTool", "color": "fg"}),
        ("ProgressInfoItem, ProgressInfoItem > *, CompareViewerPane, CompareViewerPane > *",
         {"background-color": "inherit", "color": "fg"}),
        ("ProgressIndicator", {"background-color": "muted", "color": "fg"}),
        ("DiscoveryItem, DiscoveryItem Label, DiscoveryItem Composite", field),
        ("DiscoveryItem StyledText", {"background-color": "surface", "color": "muted"}),
        ("DiscoveryItem Link", {"background-color": "surface", "color": "azure"}),
        ("CatalogSwitcher, CatalogSwitcher > ScrolledComposite > Composite > Composite, CategoryItem",
         {"background-color": "bgTool", "color": "fg"}),
        ("GradientCanvas, GradientCanvas > Label", {"background-color": "frame", "color": "fg"}),
        ("GradientCanvas", {"background": "frame"}),
        ("CategoryItem > GradientCanvas, CategoryItem > GradientCanvas > Label",
         {"background-color": "frame", "color": "fg"}),
        ("CategoryItem > GradientCanvas", {"background": "frame", "background-image": "frame"}),
        ("WebSite", field),
        ("Form", {"background-color": "bgTool", "color": "fg", "text-background-color": "bgTool",
                  "tb-toggle-hover-color": "fg", "tb-toggle-color": "muted", "h-hover-full-color": "hover",
                  "h-hover-light-color": "hover", "h-bottom-keyline-2-color": "border",
                  "h-bottom-keyline-1-color": "border"}),
        ("FormHeading", {"background-color": "bgTool", "color": "fg"}),
        ("Section", {"background-color": "bgTool", "color": "fg", "background-color-titlebar": "frame",
                     "background-color-gradient-titlebar": "frame", "border-color-titlebar": "border",
                     "swt-titlebar-color": "fg", "tb-toggle-hover-color": "fg", "tb-toggle-color": "muted"}),
        ("Table, Tree", {"swt-header-color": "fg", "swt-header-background-color": "frame"}),
        ("Twistie", {"color": "muted"}),
        (".MPartSashContainer", {"background-color": "frame", "color": "fg"}),
        ("HeapStatus", {"background-color": "surface", "color": "fg"}),
        ("PageSiteComposite, PageSiteComposite > CImageLabel", {"color": "fg"}),
        ("PageSiteComposite > PropertyTable", {"background-color": "bgTool", "color": "fg"}),
        ("PageSiteComposite > PropertyTable:disabled", {"background-color": "frame", "color": "disabled"}),
        ("Link", {"swt-link-foreground-color": "azure"}),
        ("ExpandableComposite", {"swt-titlebar-color": "fg", "tb-toggle-hover-color": "fg",
                                 "tb-toggle-color": "muted"}),
        ("TabbedPropertyTitle > CLabel", {"color": "fg"}),
        ("TabbedPropertyTitle", {"swt-backgroundGradientStart-color": "frame",
                                 "swt-backgroundGradientEnd-color": "frame",
                                 "swt-backgroundBottomKeyline1-color": "border",
                                 "swt-backgroundBottomKeyline2-color": "border"}),
        ("TabbedPropertyList", {"swt-tabNormalShadow-color": "border", "swt-tabDarkShadow-color": "muted",
                                "swt-tabAreaBackground-color": "bgTool", "swt-tabBackground-color": "frame",
                                "color": "fg"}),
        # parts: views on bgTool, their fields on surface
        (".MPart", {"background-color": "bgTool", "color": "fg"}),
        (part, {"background-color": "bgTool", "color": "fg"}),
        (".MPart Section > Label", {"background-color": "bgTool", "color": "fg"}),
        (".MPart Table, .MPart Browser, .MPart OleFrame, .MPart ViewForm, .MPart ViewForm > CLabel, "
         ".MPart PageBook > Label, .MPart PageBook > SashForm", {"background-color": "bgTool", "color": "fg"}),
        (".MPart Section Tree", {"background-color": "bgTool", "color": "fg"}),
        (".MPart DatePicker, .MPart DatePicker > Text, .MPart ScheduleDatePicker, .MPart ScheduleDatePicker > Text, "
         ".MPart CCombo, .MPart Spinner, .MPart Composite > StyledText, .MPart PageBook > SashForm Label, "
         ".MPart SashForm > Text[style~='SWT.BORDER']", field),
        ("#org-eclipse-jdt-ui-SourceView StyledText, #org-eclipse-wst-jsdt-ui-SourceView StyledText",
         {"background-color": "bg"}),
        ("#org-eclipse-ui-console-ConsoleView .MPart > Composite, #org-eclipse-ui-console-ConsoleView .MPart "
         "StyledText, #org-eclipse-ui-console-ConsoleView .MPart PageBook Label",
         {"background-color": "bgTool", "color": "fg"}),
        ("#org-eclipse-e4-ui-compatibility-editor LayoutCanvas", {"background-color": "bg", "color": "fg"}),
        ("#org-eclipse-e4-ui-compatibility-editor Canvas, #org-eclipse-e4-ui-compatibility-editor Canvas > *",
         {"background-color": "bg"}),
        # tabs: views' tabs on bgTool, the editor's selected tab on bg, the red accent under the active tab
        ("CTabFolder Canvas", {"background-color": "bgTool", "color": "fg"}),
        (".MPartStack.active CTabFolder Canvas", {"background-color": "bgTool", "color": "fg"}),
        ("CTabItem.busy", {"color": "muted"}),
        ("StatusLine, ImageBasedFrame, #org-eclipse-ui-StatusLine, #org-eclipse-ui-StatusLine CLabel, "
         "#org-eclipse-ui-ProgressBar, #org-eclipse-ui-ProgressBar Canvas", {"color": "fg"}),
        (".DragFeedback", {"background-color": "border"}),
        (".ModifiedDragFeedback", {"background-color": "ansiBlue"}),
    ]


def tab_rules():
    """The tab styles of Eclipse's dark theme, whose colours name the workbench colour definitions."""
    renderer = ("url('bundleclass://org.eclipse.e4.ui.workbench.renderers.swt/"
                "org.eclipse.e4.ui.workbench.renderers.swt.CTabRendering')")
    d = "'#org-eclipse-ui-workbench-{}'".format
    return [
        ("#org-eclipse-ui-editorss", {"swt-tab-height": "8px"}),
        (".MPartStack", {"font-family": "'#org-eclipse-ui-workbench-TAB_TEXT_FONT'", "swt-tab-renderer": renderer,
                         "swt-selected-tab-highlight": "{muted}", "swt-selected-highlight-top": "false",
                         "swt-draw-custom-tab-content-background": "true",
                         "swt-unselected-hot-tab-color-background": "{hover}"}),
        (".MPartStack.active", {"swt-selected-tab-highlight": "{red}", "swt-selected-highlight-top": "false"}),
        ("CTabFolder", {"color": d("INACTIVE_TAB_TEXT_COLOR"), "swt-tab-renderer": renderer,
                        "swt-tab-outline": d("ACTIVE_TAB_OUTLINE_COLOR"),
                        "swt-outer-keyline-color": d("ACTIVE_TAB_OUTER_KEYLINE_COLOR"),
                        "swt-unselected-tabs-color": f"{d('ACTIVE_UNSELECTED_TABS_COLOR_START')} "
                                                     f"{d('ACTIVE_UNSELECTED_TABS_COLOR_END')} 100% 100%",
                        "swt-selected-tab-fill": d("ACTIVE_TAB_BG_END"),
                        "swt-unselected-hot-tab-color-background": "{hover}",
                        "swt-selected-tab-highlight": "none"}),
        ("CTabFolder[style~='SWT.DOWN'][style~='SWT.BOTTOM']", {
            "swt-tab-renderer": renderer, "swt-unselected-hot-tab-color-background": "{hover}",
            "swt-selected-tab-highlight": "{muted}", "swt-selected-highlight-top": "true"}),
        (".MPartStack.active CTabFolder[style~='SWT.DOWN'][style~='SWT.BOTTOM']", {
            "swt-selected-tab-highlight": "{red}", "swt-selected-highlight-top": "true"}),
        ("CTabFolder.active", {"swt-selected-tab-highlight": "{red}", "swt-selected-highlight-top": "false"}),
        ("CTabItem, CTabItem CLabel", {"background-color": d("ACTIVE_TAB_BG_END"),
                                       "color": d("INACTIVE_TAB_UNSELECTED_TEXT_COLOR")}),
        ("CTabItem:selected, CTabItem:selected CLabel", {"color": d("INACTIVE_TAB_SELECTED_TEXT_COLOR")}),
        (".MPartStack.active > CTabItem, .MPartStack.active > CTabItem CLabel", {
            "background-color": d("ACTIVE_TAB_BG_END"), "color": d("ACTIVE_TAB_UNSELECTED_TEXT_COLOR")}),
        (".MPartStack.active > CTabItem:selected, .MPartStack.active > CTabItem:selected CLabel", {
            "color": d("ACTIVE_TAB_SELECTED_TEXT_COLOR")}),
        (".MPartStack.active.noFocus > CTabItem:selected", {"color": d("ACTIVE_NOFOCUS_TAB_SELECTED_TEXT_COLOR")}),
        ("CTabFolder > Composite#ToolbarComposite", {"background-color": d("ACTIVE_TAB_BG_END")}),
        ("CTabFolder.MArea CTabItem, CTabFolder.MArea CTabItem CLabel", {"background-color": d("DARK_BACKGROUND")}),
        # the editor area: the selected tab on the editor's bg
        ("#org-eclipse-ui-editorss CTabItem:selected", {"color": "{fg}"}),
        ("#org-eclipse-ui-editorss CTabFolder", {"swt-selected-tab-fill": "{bg}", "swt-selected-highlight-top": "true",
                                                 "swt-draw-custom-tab-content-background": "true",
                                                 "swt-unselected-hot-tab-color-background": "{hover}"}),
        ("#org-eclipse-ui-editorss CTabFolder.active", {"swt-selected-tab-highlight": "{red}",
                                                        "swt-selected-highlight-top": "true"}),
    ]


# The stylesheet of Mylyn WikiText's preview tab, which opens README files: the rules of Mylyn's css/default.css with
# the palette's colours, on one line and without "=" or quotes, as Eclipse reads a preference up to its last "=".
PREVIEW_CSS = " ".join(f"{selectors} {{ {declarations} }}" for selectors, declarations in (
    ("*", "font-family: Arial, Helvetica, sans-serif;"),
    ("html, body", "color: {fg}; background-color: {bg};"),
    ("h1", "font-size: 120%; font-weight: bold; color: {method};"),
    ("h2", "font-size: 110%; font-weight: bold; color: {method};"),
    ("h3", "font-size: 105%; font-weight: bold; color: {method};"),
    ("h4", "font-weight: bold; color: {method};"),
    ("h5", "font-size: 90%; font-weight: bold; color: {method};"),
    ("h6", "font-size: 80%; font-weight: bold; color: {method};"),
    ("b, strong, dt", "font-weight: bold;"),
    ("i, cite, em, var, dfn", "font-style: italic;"),
    ("mark", "color: {fg}; background-color: {searchBg};"),
    ("code", "font-family: monospace; color: {string};"),
    ("pre, tt", "font-family: monospace;"),
    ("ins", "text-decoration: underline;"),
    ("del", "text-decoration: line-through;"),
    ("sup", "font-size: smaller; vertical-align: super;"),
    ("sub", "font-size: smaller; vertical-align: sub;"),
    ("a", "text-decoration: underline; color: {azure};"),
    ("sup a", "text-decoration: none;"),
    ("blockquote, q", "color: {doc}; font-style: italic;"),
    ("h1.editorPreview, h2.editorPreview, h3.editorPreview, h4.editorPreview",
     "padding-bottom: 0.3em; font-size: 1.75em; border-bottom: 1px solid {border};"),
    ("pre.editorPreview", "padding: 16px; overflow: auto; line-height: 1.45; color: {string}; "
                          "background-color: {surface}; border-radius: 3px;"),
    ("table.editorPreview", "border-collapse: collapse; border-spacing: 0; border-color: {border};"),
    ("tr.editorPreview td.editorPreview", "border: 1px solid {border}; padding: 6px 13px;"),
    ("tr.editorPreview th.editorPreview", "border: 1px solid {border}; padding: 6px 13px; "
                                          "background-color: {bgTool};"),
))
# The preview's texts on their backgrounds, for the contrast check.
PREVIEW_TEXTS = (("preview text", "fg", "bg"), ("preview heading", "method", "bg"), ("preview code", "string", "bg"),
                 ("preview code block", "string", "surface"), ("preview link", "azure", "bg"), ("preview quote", "doc", "bg"),
                 ("preview mark", "fg", "searchBg"), ("preview table header", "fg", "bgTool"))


def preferences(t):
    """(node, pseudo attribute, {key: value}, whether colours are r,g,b) per IEclipsePreferences rule, with colours as
    palette keys in braces."""
    p = t["palette"]
    kw_bold = "true" if p.get("kwBold", not p["dark"]) else "false"
    def jdt(key, role, enabled=True, bold=False, italic=False, underline=False, strikethrough=False):
        prefix = f"semanticHighlighting.{key}"
        return {f"{prefix}.color": "{" + role + "}", f"{prefix}.enabled": str(enabled).lower(),
                f"{prefix}.bold": str(bold).lower(), f"{prefix}.italic": str(italic).lower(),
                f"{prefix}.underline": str(underline).lower(), f"{prefix}.strikethrough": str(strikethrough).lower()}
    editors = {
        "AbstractTextEditor.Color.Background.SystemDefault": "false",
        "AbstractTextEditor.Color.Foreground.SystemDefault": "false",
        "AbstractTextEditor.Color.SelectionBackground.SystemDefault": "false",
        "AbstractTextEditor.Color.SelectionForeground.SystemDefault": "false",
        "AbstractTextEditor.Color.Background": "{bg}", "AbstractTextEditor.Color.Foreground": "{fg}",
        "AbstractTextEditor.Color.SelectionBackground": "{selection}",
        "AbstractTextEditor.Color.SelectionForeground": "{fg}", "AbstractTextEditor.Color.FindScope": "{selInactive}",
        "asOccurencesIndicationColor": "{underCaret}", "breakpointIndicationColor": "{ansiBlue}",
        "currentIPColor": "{diffConf}", "currentLineColor": "{caretRow}", "deletionIndicationColor": "{deleted}",
        "filteredSearchResultIndicationColor": "{selInactive}", "hyperlinkColor": "{azure}",
        "hyperlinkColor.SystemDefault": "false", "infoIndicationColor": "{azure}", "lineNumberColor": "{lineNo}",
        "linked.slave.color": "{ansiBlue}", "matchingTagIndicationColor": "{braceBg}",
        "occurrenceIndicationColor": "{underCaret}", "overrideIndicatorColor": "{muted}",
        "printMarginColor": "{guide}", "searchResultHighlighting": "true", "searchResultIndication": "true",
        "searchResultIndicationColor": "{searchBg}", "searchResultTextStyle": "BOX",
        "secondaryIPColor": "{diffMod}", "spellingIndicationColor": "{warning}",
        "writeOccurrenceIndicationColor": "{writeCaret}", "errorIndicationColor": "{error}",
        "warningIndicationColor": "{warning}", "org.eclipse.ui.editors.stickyLinesSeparatorColor": "{border}",
        # the generic editor, LSP4E, TM4E's bracket pairs, compare and EclEmma, which add to this node
        "TextOccurrenceIndicationColor": "{underCaret}", "LSP4EReadOccurrenceIndicationColor": "{underCaret}",
        "LSP4EWriteOccurrenceIndicationColor": "{writeCaret}", "LSP4ETextOccurrenceIndicationColor": "{underCaret}",
        "TM4EMatchingPairColor": "{braceBg}", "inlineDiffColor": "{diffIns}",
        "detailedInlineDiffColor": "{addedChar}", "deletionInlineDiffColor": "{diffDel}",
        "detailedDeletionInlineDiffColor": "{deletedChar}", "fullcoverage_color": "{diffIns}",
        "partialcoverage_color": "{diffConf}", "nocoverage_color": "{diffDel}",
    }
    workbench = {
        "ACTIVE_HYPERLINK_COLOR": "{azure}", "CONFLICTING_COLOR": "{ansiMagenta}",
        "CONTENT_ASSIST_BACKGROUND_COLOR": "{surface}", "CONTENT_ASSIST_FOREGROUND_COLOR": "{fg}",
        "org.eclipse.ui.workbench.INFORMATION_BACKGROUND": "{surface}",
        "org.eclipse.ui.workbench.INFORMATION_FOREGROUND": "{fg}",
        "org.eclipse.ui.workbench.HOVER_BACKGROUND": "{surface}", "org.eclipse.ui.workbench.HOVER_FOREGROUND": "{fg}",
        "org.eclipse.ui.workbench.FORM_HEADING_ERROR_COLOR": "{ansiRed}",
        "org.eclipse.ui.workbench.FORM_HEADING_WARNING_COLOR": "{ansiYellow}",
        "org.eclipse.ui.workbench.FORM_HEADING_INFO_COLOR": "{muted}",
        "ERROR_COLOR": "{ansiRed}", "HYPERLINK_COLOR": "{azure}", "INCOMING_COLOR": "{ansiBlue}",
        "OUTGOING_COLOR": "{fg}", "RESOLVED_COLOR": "{ansiGreen}", "EDITION_COLOR": "{fg}",
        "org.eclipse.search.ui.match.highlight": "{ansiYellow}",
        "org.eclipse.ui.editors.rangeIndicatorColor": "{guideSel}",
        "org.eclipse.jface.REVISION_NEWEST_COLOR": "{diffIns}", "org.eclipse.jface.REVISION_OLDEST_COLOR": "{bgTool}",
        "org.eclipse.ui.editors.inlineAnnotationColor": "{muted}",
        # JDT, EGit and Mylyn's colours in the workbench's node
        "org.eclipse.jdt.ui.ColoredLabels.inherited": "{muted}", "org.eclipse.jdt.ui.Javadoc.backgroundColor": "{surface}",
        "org.eclipse.jdt.ui.Javadoc.foregroundColor": "{fg}",
        "org.eclipse.jdt.ui.ColoredLabels.writeaccess_highlight": "{writeCaret}",
        "org.eclipse.egit.ui.CommitMessageCommentColor": "{comment}",
        "org.eclipse.egit.ui.DiffAddBackgroundColor": "{diffIns}", "org.eclipse.egit.ui.DiffAddForegroundColor": "{fg}",
        "org.eclipse.egit.ui.DiffHeadlineBackgroundColor": "{frame}",
        "org.eclipse.egit.ui.DiffHeadlineForegroundColor": "{fg}",
        "org.eclipse.egit.ui.DiffHunkBackgroundColor": "{diffMod}", "org.eclipse.egit.ui.DiffHunkForegroundColor": "{fg}",
        "org.eclipse.egit.ui.DiffRemoveBackgroundColor": "{diffDel}",
        "org.eclipse.egit.ui.DiffRemoveForegroundColor": "{fg}",
        "org.eclipse.egit.ui.IgnoredResourceBackgroundColor": "{bgTool}",
        "org.eclipse.egit.ui.IgnoredResourceForegroundColor": "{muted}",
        "org.eclipse.egit.ui.UncommittedChangeBackgroundColor": "{bgTool}",
        "org.eclipse.egit.ui.UncommittedChangeForegroundColor": "{ansiBlue}",
        "org.eclipse.mylyn.tasks.ui.colors.foreground.today.scheduled": "{ansiBlue}",
        "org.eclipse.mylyn.tasks.ui.colors.foreground.past.scheduled": "{ansiBlue}",
        "org.eclipse.mylyn.tasks.ui.colors.foreground.thisweek.scheduled": "{muted}",
        "org.eclipse.mylyn.tasks.ui.colors.foreground.task.active": "{ansiMagenta}",
        "org.eclipse.mylyn.tasks.ui.colors.category.gradient.start": "{frame}",
        "org.eclipse.mylyn.tasks.ui.colors.category.gradient.end": "{bgTool}",
        "org.eclipse.mylyn.tasks.ui.color.text.quoted": "{doc}",
    }
    java = {
        "content_assist_completion_replacement_background": "{searchBg}",
        "content_assist_completion_replacement_foreground": "{fg}",
        "content_assist_parameters_background": "{surface}", "content_assist_parameters_foreground": "{fg}",
        "content_assist_proposals_background": "{surface}", "content_assist_proposals_foreground": "{fg}",
        "java_bracket": "{op}", "java_comment_task_tag": "{todo}", "java_comment_task_tag_bold": "true",
        "java_default": "{fg}", "java_doc_default": "{doc}", "java_doc_default_italic": "true",
        "java_doc_keyword": "{docTag}", "java_doc_keyword_bold": "true", "java_doc_link": "{azure}",
        "java_doc_tag": "{docTag}", "java_keyword": "{keyword}", "java_keyword_bold": kw_bold,
        "java_keyword_return": "{keyword}", "java_keyword_return_bold": kw_bold,
        "java_multi_line_comment": "{comment}", "java_multi_line_comment_italic": "true",
        "java_operator": "{op}", "java_single_line_comment": "{comment}", "java_single_line_comment_italic": "true",
        "java_string": "{string}", "matchingBracketsColor": "{muted}", "sourceHoverBackgroundColor": "{surface}",
        "pf_coloring_argument": "{constant}", "pf_coloring_assignment": "{op}", "pf_coloring_comment": "{comment}",
        "pf_coloring_key": "{field}", "pf_coloring_value": "{string}",
        "javadocElementsStyling.darkModeDefaultColors": "true" if p["dark"] else "false",
        **jdt("abstractClass", "type", italic=True), **jdt("abstractMethodInvocation", "call", italic=True),
        **jdt("annotation", "annotation"), **jdt("annotationElementReference", "param"),
        **jdt("autoboxing", "fg", enabled=False), **jdt("class", "type"),
        **jdt("deprecatedMember", "muted", strikethrough=True), **jdt("enum", "type"), **jdt("field", "field"),
        **jdt("inheritedField", "field"), **jdt("inheritedMethodInvocation", "call"),
        **jdt("interface", "type", italic=True), **jdt("localVariable", "fg"),
        **jdt("localVariableDeclaration", "fg"), **jdt("method", "call"),
        **jdt("methodDeclarationName", "method", bold=True), **jdt("number", "number"),
        **jdt("parameterVariable", "param"), **jdt("staticField", "field", italic=True),
        **jdt("staticFinalField", "constant", bold=True, italic=True),
        **jdt("staticMethodInvocation", "call", italic=True), **jdt("typeArgument", "type"),
        **jdt("typeParameter", "typeParam", bold=True), **jdt("restrictedKeywords", "keyword",
                                                              bold=kw_bold == "true"),
    }
    debug = {
        "org.eclipse.debug.ui.MemoryHistoryKnownColor": "{fg}", "org.eclipse.debug.ui.MemoryHistoryUnknownColor":
            "{muted}", "org.eclipse.debug.ui.PREF_CHANGED_VALUE_BACKGROUND": "{diffConf}",
        "org.eclipse.debug.ui.changedDebugElement": "{ansiRed}", "org.eclipse.debug.ui.consoleBackground": "{bgTool}",
        "org.eclipse.debug.ui.errorColor": "{ansiRed}", "org.eclipse.debug.ui.inColor": "{ansiGreen}",
        "org.eclipse.debug.ui.outColor": "{fg}",
    }
    ant = {
        "org.eclipse.ant.ui.commentsColor": "{comment}", "org.eclipse.ant.ui.commentsColor_italic": "true",
        "org.eclipse.ant.ui.constantStringsColor": "{string}", "org.eclipse.ant.ui.dtdColor": "{keyword}",
        "org.eclipse.ant.ui.processingInstructionsColor": "{annotation}",
        "org.eclipse.ant.ui.tagsColor": "{keyword}", "org.eclipse.ant.ui.tagsColor_bold": kw_bold,
        "org.eclipse.ant.ui.textColor": "{fg}", "org.eclipse.ant.ui.debugColor": "{fg}",
        "org.eclipse.ant.ui.errorColor": "{ansiRed}", "org.eclipse.ant.ui.informationColor": "{azure}",
    }
    generic = {"matchingBracketsColor": "{muted}"}
    wikitext = {f"block-h{i}": f"{size}font-weight: bold; color: {{method}};" for i, size in enumerate(
        ("font-size: 120%; ", "font-size: 110%; ", "font-size: 105%; ", "", "font-size: 90%; ", "font-size: 80%; "), 1)}
    wikitext.update({"phrase-code": "font-family: monospace; color: {string};",
                     "block-bc": "font-family: monospace; color: {string};", "preview.css": PREVIEW_CSS})
    # colours as Eclipse's r,g,b, but Mylyn WikiText's, which are CSS declarations
    return [(node, "heritage-themes", values, node != "org-eclipse-mylyn-wikitext-ui") for node, values in (
        ("org-eclipse-ui-editors", editors), ("org-eclipse-ui-workbench", workbench), ("org-eclipse-jdt-ui", java),
        ("org-eclipse-debug-ui", debug), ("org-eclipse-ant-ui", ant), ("org-eclipse-ui-genericeditor", generic),
        ("org-eclipse-mylyn-wikitext-ui", wikitext))]


def fill(value, colours, rgb_format):
    """A value with its palette keys in braces filled in as #RRGGBB, or as r,g,b in preferences."""
    def one(match):
        colour = colours[match[1]]
        return rgb(colour) if rgb_format else colour
    return re.sub(r"\{(\w+)\}", one, value)


def stylesheet(t, source):
    """The css/<theme>.css stylesheet for a theme dict. source is the URL of the theme folder."""
    p = t["palette"]
    c = hexes(p)
    lines = [f"/* {p['name']}: a Heritage Themes theme for Eclipse. Generated from {source}; changes here are "
             "overwritten. */", "",
             '@import url("platform:/plugin/org.eclipse.ui.themes/css/common/e4_globalstyle.css");', "",
             "ThemesExtension { color-definition:",
             ",\n".join(f"    '#org-eclipse-ui-workbench-{key}'" for key in COLOR_DEFINITIONS) + ";", "}", ""]
    for key, role in COLOR_DEFINITIONS.items():
        lines += [f"ColorDefinition#org-eclipse-ui-workbench-{key} {{", f"    color: {c[role]};",
                  "    category: '#org-eclipse-ui-presentation-default';",
                  f"    label: url('platform:/plugin/org.eclipse.ui.themes?message={key}');", "}"]
    for selectors, properties in widget_rules(p):
        lines += ["", ",\n".join(s.strip() for s in selectors.split(",")) + " {",
                  *(f"    {prop}: {c.get(value, value)};" for prop, value in properties.items()), "}"]
    for selectors, properties in tab_rules():
        lines += ["", ",\n".join(s.strip() for s in selectors.split(",")) + " {",
                  *(f"    {prop}: {fill(value, c, False)};" for prop, value in properties.items()), "}"]
    for node, pseudo, values, rgb_format in preferences(t):
        lines += ["", f"IEclipsePreferences#{node}:{pseudo} {{", "    preferences:",
                  *(f"        '{key}={fill(value, c, rgb_format)}'" for key, value in values.items()), "}"]
    return "\n".join(lines) + "\n"


def textmate(t, source):
    """The TextMate theme for TM4E, as heritage.amp writes it."""
    return amp.theme(t["palette"], source)


def plugin_xml(themes):
    """The plugin.xml, contributing each CSS theme to Eclipse and each TextMate theme to TM4E."""
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<?eclipse version="3.4"?>', "<plugin>",
             '   <extension point="org.eclipse.e4.ui.css.swt.theme">']
    for t in themes:
        lines.append(f'      <theme id="{theme_id(t)}" label="{xml_text(t["palette"]["name"])}" '
                     f'basestylesheeturi="css/{name(t)}.css"/>')
    lines += ["   </extension>", '   <extension point="org.eclipse.tm4e.ui.themes">']
    for t in themes:
        lines.append(f'      <theme id="{tm4e_id(t)}" name="{xml_text(t["palette"]["name"])}" '
                     f'path="textmate/{name(t)}.tmTheme" dark="{str(t["palette"]["dark"]).lower()}"/>')
    lines += ["   </extension>", "</plugin>"]
    return "\n".join(lines) + "\n"


def xml_text(value):
    return value.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;")


def theme_ids(themes):
    """The lines of the file that tells the preview each theme's identifiers: stem, CSS theme, TextMate theme and
    whether it is dark, separated by tabs."""
    return "".join(f"{name(t)}\t{theme_id(t)}\t{tm4e_id(t)}\t{'dark' if t['palette']['dark'] else 'light'}\n"
                   for t in themes)


def manifest(version, vendor):
    """META-INF/MANIFEST.MF of the bundle: Eclipse loads its extensions as a singleton, and TM4E's is optional."""
    lines = ["Manifest-Version: 1.0", "Bundle-ManifestVersion: 2", "Bundle-Name: Heritage Themes",
             f"Bundle-SymbolicName: {BUNDLE};singleton:=true", f"Bundle-Version: {version}",
             f"Bundle-Vendor: {vendor}",
             "Require-Bundle: org.eclipse.e4.ui.css.swt.theme,", " org.eclipse.tm4e.ui;resolution:=optional",
             "Bundle-RequiredExecutionEnvironment: JavaSE-21", "Automatic-Module-Name: heritage.themes.eclipse", ""]
    return "\r\n".join(lines) + "\r\n"


def styles(p):
    """Element → dict(fg, bg) as #RRGGBB, for the build's contrast check: the Java colours and the window's texts."""
    c = hexes(p)
    roles = ("keyword", "string", "number", "type", "call", "method", "field", "constant", "annotation", "param",
             "typeParam", "op", "doc", "docTag", "azure")
    out = {f"Java {role}": dict(fg=c[role], bg=c["bg"]) for role in roles}
    out["Java comment"] = dict(fg=c["comment"], bg=c["bg"])
    for element, fg, bg in (("editor text", "fg", "bg"), ("view text", "fg", "bgTool"), ("muted view text", "muted",
                                                                                          "bgTool"),
                            ("window text", "fg", "frame"), ("field text", "fg", "surface"),
                            ("selected text", "fg", "selection"), ("tab text", "muted", "bgTool"),
                            ("editor tab", "fg", "bg"), ("link", "azure", "bgTool"),
                            ("added text", "fg", "diffIns"), ("deleted text", "fg", "diffDel"),
                            ("changed character", "fg", "addedChar"), ("deleted character", "fg", "deletedChar"),
                            *PREVIEW_TEXTS):
        out[element] = dict(fg=c[fg], bg=c[bg])
    return out


def ruler_shades(p):
    """The outlines and fills of the marks that the overview ruler beside the editor draws for each annotation colour
    the theme sets, as getColor of jface's OverviewRuler derives them: the colour blended 20% and 75% towards white
    when it and the ruler are both bright (its isDark), towards black when both are not, and towards the ruler's
    background otherwise."""
    def bright(rgb):
        grey = rgb[0] if rgb[0] == rgb[1] == rgb[2] else 0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2] + 0.5
        return grey > 128
    c = hexes(p)
    ruler = tuple(int(p["bg"][i:i + 2], 16) for i in (0, 2, 4))
    out = set()
    for node, _, values, _ in preferences({"palette": p}):
        if node != "org-eclipse-ui-editors":
            continue
        for key, value in values.items():
            if not key.endswith("IndicationColor"):
                continue
            colour = fill(value, c, False)
            base = tuple(int(colour[i:i + 2], 16) for i in (1, 3, 5))
            towards = ((255, 255, 255) if bright(base) and bright(ruler) else
                       (0, 0, 0) if not bright(base) and not bright(ruler) else ruler)
            for scale in (0.2, 0.75):
                out.add("#" + "".join(f"{int(x + (y - x) * scale + 0.5):02X}" for x, y in zip(base, towards)))
    return sorted(out)


def pixel_palette(p):
    """What scripts/editors/pixels.py checks a screenshot against: the editor area of the window that
    scripts/editors/shoot.py opens, whose gutter and tab icons Eclipse draws with images of its own."""
    colours = {"#" + v for v in p.values() if isinstance(v, str) and re.fullmatch(r"[0-9A-F]{6}", v)}
    colours |= set(terminal_colours(p)["ansi"])
    return dict(background="#" + p["bg"],
                backgrounds=["#" + p[k] for k in ("bgTool", "frame", "surface", "caretRow", "selection", "hover",
                                                  "underCaret", "searchBg", "braceBg")] + ruler_shades(p),
                foregrounds=sorted(colours), crop=[128, 185, 312, 215])


def jar_name(version):
    """The plugin's file name, as Eclipse names bundles: the symbolic name and the version."""
    return f"{BUNDLE}_{version}.jar"


def jar(themes, version, vendor, sources):
    """The plugin jar for theme dicts, with every entry dated as the other zips date theirs. sources maps a theme's
    slug to the URL of its family's folder."""
    entries = [("META-INF/MANIFEST.MF", manifest(version, vendor)), ("plugin.xml", plugin_xml(themes))]
    for t in themes:
        source = sources.get(t["slug"], "") if isinstance(sources, dict) else sources
        entries += [(f"css/{name(t)}.css", stylesheet(t, source)), (f"textmate/{name(t)}.tmTheme", textmate(t, source))]
    out = io.BytesIO()
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for path, text in entries:
            info = zipfile.ZipInfo(path, (2020, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, text.encode("utf-8"))
    return out.getvalue()
