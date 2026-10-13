import json, os, re, html, zipfile, shutil

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "build")
shutil.rmtree(OUT, ignore_errors=True)
os.makedirs(f"{OUT}/plugin/META-INF"); os.makedirs(f"{OUT}/plugin/themes")

# ---------------------------------------------------------------- palettes
# Five Elements: Fire=red (keywords), Wood=qing/green (strings), Earth=yellow (types),
# Metal=white -> rice/beige instead of pure white, Water=black -> indigo ink instead of pure black.
# Gold = prosperity (caret, search, Spock labels), purple = Forbidden City (fields),
# azure/blue = trust (methods), turquoise = imperial decorative arts (annotations),
# copper = metals table (numbers), ink-wash grey = restraint (comments).
NIGHT = dict(
    name="Wuxing Night", dark=True, parent="Darcula", parentTheme="ExperimentalDark",
    bg="171B26", bgUi="13161F", bgTool="151923", surface="1E2332", hover="242A3B",
    border="262C3D", fg="E6DCC8", muted="8A8577", disabled="5C5F6B",
    caretRow="1C2130", selection="2D3754", selInactive="252C40", lineNo="4A5064", lineNoCaret="C9A24A",
    guide="232838", guideSel="3A4258",
    keyword="E8705F", string="8CC88E", number="E39A62", type="F0D47A", method="74B4E6", call="9AC6EA",
    field="C59BE3", constant="B48CE6", annotation="45BFC8", label="E8BE52", labelBg="352E1B",
    comment="6F7789", doc="9E8C70", docTag="B8A27C", op="B9B09E", param="E6DCC8", typeParam="7FD3C9",
    gold="D9A93F", red="C8473A", redText="F3E7D3", azure="74B4E6",
    error="F0536A", warning="E8A13A", weak="8A7A50",
    searchBg="4A3E1C", searchBorder="D9A93F", underCaret="2C3A55", writeCaret="4A2B2E",
    braceBg="3A4A3A", todo="E2B84C",
    added="4C8A57", modified="5878B0", deleted="9A4A44",
    diffIns="20331F", diffMod="1D2840", diffDel="3A1E22", diffConf="3A3020",
)
DAY = dict(
    name="Wuxing Day", dark=False, parent="Default", parentTheme="ExperimentalLight",
    bg="F6F0E1", bgUi="EDE5D2", bgTool="F0E9D8", surface="FBF7EC", hover="E4DAC3",
    border="D9CEB6", fg="2B3040", muted="7A7566", disabled="ADA694",
    caretRow="EFE6D1", selection="D3DBEE", selInactive="E0E2E6", lineNo="B3AA94", lineNoCaret="A0700A",
    guide="E6DDC8", guideSel="CDBF9F",
    keyword="B0362B", string="2A7244", number="A04A15", type="6E5A10", method="1F5FA8", call="2F6DB0",
    field="7B3FA6", constant="6A2F96", annotation="0A7480", label="7A5200", labelBg="F2E1B0",
    comment="7E7C72", doc="7D6845", docTag="6E5A3A", op="5A5A5A", param="2B3040", typeParam="0F7A72",
    gold="C8962A", red="B0362B", redText="FBF3E4", azure="1F5FA8",
    error="D0283E", warning="C27A00", weak="B3A06A",
    searchBg="F3D98A", searchBorder="C8962A", underCaret="D6E2F2", writeCaret="F2D6D0",
    braceBg="CFE6CF", todo="8A5E00",
    added="6AA672", modified="6C8CC4", deleted="C46A60",
    diffIns="E2F0DC", diffMod="DDE6F4", diffDel="F5DCD8", diffConf="F3E6C4",
)

# ---------------------------------------------------------------- editor scheme
def attr(fg=None, bg=None, font=0, effect=None, etype=None, stripe=None):
    return dict(fg=fg, bg=bg, font=font, effect=effect, etype=etype, stripe=stripe)

BOLD, ITALIC, BI = 1, 2, 3
UNDER, WAVE, STRIKE, BOX = 1, 2, 3, 0

def scheme(p):
    a = {}
    def s(keys, v):
        for k in keys.split(): a[k] = v
    s("TEXT", attr(p["fg"], p["bg"]))
    s("DEFAULT_KEYWORD JAVA_KEYWORD GROOVY_KEYWORD KOTLIN_KEYWORD", attr(p["keyword"], font=BOLD if not p["dark"] else 0))
    s("DEFAULT_STRING JAVA_STRING GROOVY_STRING", attr(p["string"]))
    s("DEFAULT_NUMBER JAVA_NUMBER", attr(p["number"]))
    s("DEFAULT_LINE_COMMENT JAVA_LINE_COMMENT DEFAULT_BLOCK_COMMENT JAVA_BLOCK_COMMENT", attr(p["comment"], font=ITALIC))
    s("DEFAULT_DOC_COMMENT JAVA_DOC_COMMENT", attr(p["doc"], font=ITALIC))
    s("DEFAULT_DOC_COMMENT_TAG JAVA_DOC_TAG", attr(p["docTag"], font=BI))
    s("DEFAULT_DOC_MARKUP JAVA_DOC_MARKUP", attr(p["docTag"]))
    s("DEFAULT_CLASS_NAME CLASS_NAME_ATTRIBUTES ENUM_NAME_ATTRIBUTES ANONYMOUS_CLASS_NAME_ATTRIBUTES ABSTRACT_CLASS_NAME_ATTRIBUTES DEFAULT_CLASS_REFERENCE",
      attr(p["type"]))
    s("DEFAULT_INTERFACE_NAME INTERFACE_NAME_ATTRIBUTES", attr(p["type"], font=ITALIC))
    s("TYPE_PARAMETER_NAME_ATTRIBUTES", attr(p["typeParam"], font=BOLD))
    s("DEFAULT_FUNCTION_DECLARATION METHOD_DECLARATION_ATTRIBUTES CONSTRUCTOR_DECLARATION_ATTRIBUTES",
      attr(p["method"], font=BOLD))
    s("DEFAULT_FUNCTION_CALL METHOD_CALL_ATTRIBUTES CONSTRUCTOR_CALL_ATTRIBUTES", attr(p["call"]))
    s("DEFAULT_STATIC_METHOD STATIC_METHOD_ATTRIBUTES", attr(p["call"], font=ITALIC))
    s("DEFAULT_INSTANCE_FIELD INSTANCE_FIELD_ATTRIBUTES", attr(p["field"]))
    s("DEFAULT_STATIC_FIELD STATIC_FIELD_ATTRIBUTES", attr(p["field"], font=ITALIC))
    s("DEFAULT_CONSTANT STATIC_FINAL_FIELD_ATTRIBUTES ENUM_CONST", attr(p["constant"], font=BI))
    s("DEFAULT_METADATA ANNOTATION_NAME_ATTRIBUTES", attr(p["annotation"]))
    s("ANNOTATION_ATTRIBUTE_NAME_ATTRIBUTES", attr(p["annotation"], font=ITALIC))
    s("DEFAULT_LABEL", attr(p["label"], p["labelBg"], BOLD))
    s("DEFAULT_PARAMETER PARAMETER_ATTRIBUTES", attr(p["param"]))
    s("DEFAULT_LOCAL_VARIABLE LOCAL_VARIABLE_ATTRIBUTES", attr(p["fg"]))
    s("DEFAULT_REASSIGNED_LOCAL_VARIABLE REASSIGNED_LOCAL_VARIABLE_ATTRIBUTES DEFAULT_REASSIGNED_PARAMETER REASSIGNED_PARAMETER_ATTRIBUTES",
      attr(effect=p["muted"], etype=UNDER))
    s("DEFAULT_OPERATION_SIGN JAVA_OPERATION_SIGN DEFAULT_BRACES JAVA_BRACES DEFAULT_PARENTHS JAVA_PARENTH DEFAULT_BRACKETS JAVA_BRACKETS DEFAULT_DOT JAVA_DOT DEFAULT_COMMA JAVA_COMMA DEFAULT_SEMICOLON JAVA_SEMICOLON",
      attr(p["op"]))
    s("DEFAULT_VALID_STRING_ESCAPE JAVA_VALID_STRING_ESCAPE", attr(p["gold"], font=BOLD))
    s("DEFAULT_INVALID_STRING_ESCAPE JAVA_INVALID_STRING_ESCAPE", attr(p["error"], effect=p["error"], etype=WAVE))
    s("DEFAULT_TAG", attr(p["keyword"])); s("DEFAULT_ATTRIBUTE", attr(p["field"]))
    s("DEFAULT_ENTITY", attr(p["gold"])); s("DEFAULT_PREDEFINED_SYMBOL", attr(p["typeParam"], font=ITALIC))
    # highlighting
    s("ERRORS_ATTRIBUTES", attr(effect=p["error"], etype=WAVE, stripe=p["error"]))
    s("WRONG_REFERENCES_ATTRIBUTES", attr(p["error"], font=BOLD))
    s("WARNING_ATTRIBUTES", attr(effect=p["warning"], etype=WAVE, stripe=p["warning"]))
    s("WEAK_WARNING_ATTRIBUTES", attr(effect=p["weak"], etype=WAVE, stripe=p["weak"]))
    s("DEPRECATED_ATTRIBUTES MARKED_FOR_REMOVAL_ATTRIBUTES", attr(effect=p["muted"], etype=STRIKE))
    s("NOT_USED_ELEMENT_ATTRIBUTES", attr(p["disabled"]))
    s("TODO_DEFAULT_ATTRIBUTES", attr(p["todo"], font=BI, stripe=p["todo"]))
    s("SEARCH_RESULT_ATTRIBUTES TEXT_SEARCH_RESULT_ATTRIBUTES", attr(bg=p["searchBg"], effect=p["searchBorder"], etype=BOX, stripe=p["gold"]))
    s("WRITE_SEARCH_RESULT_ATTRIBUTES", attr(bg=p["writeCaret"], stripe=p["red"]))
    s("IDENTIFIER_UNDER_CARET_ATTRIBUTES", attr(bg=p["underCaret"], stripe=p["azure"]))
    s("WRITE_IDENTIFIER_UNDER_CARET_ATTRIBUTES", attr(bg=p["writeCaret"], stripe=p["red"]))
    s("MATCHED_BRACE_ATTRIBUTES", attr(bg=p["braceBg"], font=BOLD))
    s("UNMATCHED_BRACE_ATTRIBUTES", attr(bg=p["writeCaret"], effect=p["error"], etype=WAVE))
    s("HYPERLINK_ATTRIBUTES CTRL_CLICKABLE", attr(p["azure"], effect=p["azure"], etype=UNDER))
    s("FOLLOWED_HYPERLINK_ATTRIBUTES", attr(p["field"], effect=p["field"], etype=UNDER))
    s("INLINE_PARAMETER_HINT", attr(p["muted"], p["caretRow"]))
    s("INLINE_PARAMETER_HINT_HIGHLIGHTED", attr(p["fg"], p["selection"]))
    s("INLINE_PARAMETER_HINT_CURRENT", attr(p["fg"], p["hover"]))
    s("BREAKPOINT_ATTRIBUTES", attr(bg=p["diffDel"], stripe=p["red"]))
    s("EXECUTIONPOINT_ATTRIBUTES", attr(bg=p["diffMod"], stripe=p["azure"]))
    s("FOLDED_TEXT_ATTRIBUTES", attr(p["muted"], p["surface"]))
    # console & logs
    s("CONSOLE_NORMAL_OUTPUT", attr(p["fg"])); s("CONSOLE_SYSTEM_OUTPUT", attr(p["muted"]))
    s("CONSOLE_ERROR_OUTPUT LOG_ERROR_OUTPUT", attr(p["error"]))
    s("LOG_WARNING_OUTPUT", attr(p["warning"])); s("CONSOLE_USER_INPUT", attr(p["string"], font=ITALIC))
    for k, v in dict(RED="keyword", GREEN="string", YELLOW="label", BLUE="method", MAGENTA="field", CYAN="annotation").items():
        s(f"CONSOLE_{k}_OUTPUT CONSOLE_{k}_BRIGHT_OUTPUT", attr(p[v]))
    s("CONSOLE_BLACK_OUTPUT", attr(p["disabled"])); s("CONSOLE_DARKGRAY_OUTPUT", attr(p["muted"]))
    s("CONSOLE_GRAY_OUTPUT", attr(p["op"])); s("CONSOLE_WHITE_OUTPUT", attr(p["fg"]))
    # diff
    s("DIFF_INSERTED", attr(bg=p["diffIns"], stripe=p["added"]))
    s("DIFF_MODIFIED", attr(bg=p["diffMod"], stripe=p["modified"]))
    s("DIFF_DELETED", attr(bg=p["diffDel"], stripe=p["deleted"]))
    s("DIFF_CONFLICT", attr(bg=p["diffConf"], stripe=p["gold"]))

    colors = dict(
        CARET_COLOR=p["gold"], CARET_ROW_COLOR=p["caretRow"], SELECTION_BACKGROUND=p["selection"],
        SELECTION_FOREGROUND="", LINE_NUMBERS_COLOR=p["lineNo"], LINE_NUMBER_ON_CARET_ROW_COLOR=p["lineNoCaret"],
        GUTTER_BACKGROUND=p["bg"], INDENT_GUIDE=p["guide"], SELECTED_INDENT_GUIDE=p["guideSel"],
        VISUAL_INDENT_GUIDE=p["guide"], RIGHT_MARGIN_COLOR=p["guide"], WHITESPACES=p["guide"],
        SOFT_WRAP_SIGN_COLOR=p["lineNo"], METHOD_SEPARATORS_COLOR=p["guide"], TEARLINE_COLOR=p["guide"],
        SELECTED_TEARLINE_COLOR=p["guideSel"], CONSOLE_BACKGROUND_KEY=p["bgTool"], DOCUMENTATION_COLOR=p["surface"],
        LOOKUP_COLOR=p["surface"], INFORMATION_HINT=p["surface"], QUESTION_HINT=p["surface"], ERROR_HINT=p["diffDel"],
        ANNOTATIONS_COLOR=p["muted"], ADDED_LINES_COLOR=p["added"], MODIFIED_LINES_COLOR=p["modified"],
        DELETED_LINES_COLOR=p["deleted"], WHITESPACES_MODIFIED_LINES_COLOR=p["weak"],
        IGNORED_ADDED_LINES_BORDER_COLOR=p["added"], IGNORED_MODIFIED_LINES_BORDER_COLOR=p["modified"],
        IGNORED_DELETED_LINES_BORDER_COLOR=p["deleted"], NOTIFICATION_BACKGROUND=p["surface"],
        FILESTATUS_MODIFIED=p["method"], FILESTATUS_ADDED=p["string"], FILESTATUS_UNKNOWN=p["number"],
        FILESTATUS_DELETED=p["muted"], FILESTATUS_IDEA_FILESTATUS_IGNORED=p["disabled"],
        FILESTATUS_MERGED=p["field"], FILESTATUS_addedOutside=p["string"], FILESTATUS_modifiedOutside=p["method"],
        BREADCRUMBS_DEFAULT=p["muted"], BREADCRUMBS_HOVERED=p["fg"], BREADCRUMBS_CURRENT=p["gold"],
        ScrollBar_Mac_thumbColor=None,
    )
    colors.pop("ScrollBar_Mac_thumbColor")
    L = [f'<scheme name="{p["name"]}" version="142" parent_scheme="{p["parent"]}">',
         '  <metaInfo><property name="ide">idea</property></metaInfo>', '  <colors>']
    for k, v in colors.items():
        L.append(f'    <option name="{k}" value="{v}" />')
    L += ['  </colors>', '  <attributes>']
    for k, v in a.items():
        L.append(f'    <option name="{k}">'); L.append('      <value>')
        if v["fg"]: L.append(f'        <option name="FOREGROUND" value="{v["fg"]}" />')
        if v["bg"]: L.append(f'        <option name="BACKGROUND" value="{v["bg"]}" />')
        if v["font"]: L.append(f'        <option name="FONT_TYPE" value="{v["font"]}" />')
        if v["effect"]:
            L.append(f'        <option name="EFFECT_COLOR" value="{v["effect"]}" />')
            L.append(f'        <option name="EFFECT_TYPE" value="{v["etype"]}" />')
        if v["stripe"]: L.append(f'        <option name="ERROR_STRIPE_COLOR" value="{v["stripe"]}" />')
        L.append('      </value>'); L.append('    </option>')
    L += ['  </attributes>', '</scheme>', '']
    return "\n".join(L)

# ---------------------------------------------------------------- UI theme
def theme(p, slug):
    c = {k: "#" + v for k, v in p.items() if isinstance(v, str) and re.fullmatch(r"[0-9A-F]{6}", v)}
    ui = {
        "*": {
            "background": "bgUi", "foreground": "fg", "infoForeground": "muted",
            "disabledForeground": "disabled", "inactiveForeground": "muted",
            "selectionBackground": "selection", "selectionForeground": "fg",
            "selectionInactiveBackground": "selInactive", "selectionBackgroundInactive": "selInactive",
            "lightSelectionBackground": "selInactive", "hoverBackground": "hover",
            "borderColor": "border", "separatorColor": "border",
            "focusColor": "gold", "focusedBorderColor": "gold",
            "acceleratorForeground": "muted", "acceleratorSelectionForeground": "fg",
        },
        "MainWindow.background": "bgUi",
        "MainToolbar.background": "bgUi", "MainToolbar.inactiveBackground": "bgUi",
        "MainToolbar.Icon.hoverBackground": "hover", "MainToolbar.Dropdown.hoverBackground": "hover",
        "ToolWindow.background": "bgTool",
        "ToolWindow.Header.background": "bgTool", "ToolWindow.Header.inactiveBackground": "bgTool",
        "ToolWindow.HeaderTab.selectedInactiveBackground": "selInactive",
        "ToolWindow.HeaderTab.underlineColor": "red",
        "ToolWindow.Button.selectedBackground": "selection", "ToolWindow.Button.hoverBackground": "hover",
        "ToolWindow.Stripe.background": "bgUi",
        "StatusBar.background": "bgUi", "StatusBar.borderColor": "border",
        "StatusBar.Widget.hoverBackground": "hover", "StatusBar.Breadcrumbs.selectionBackground": "selection",
        "EditorTabs.background": "bg", "EditorTabs.underlinedTabBackground": "bg",
        "EditorTabs.underlineColor": "red", "EditorTabs.inactiveUnderlineColor": "gold",
        "EditorTabs.hoverBackground": "hover", "EditorTabs.borderColor": "border",
        "EditorTabs.underlineHeight": 2,
        "DefaultTabs.underlineColor": "red", "DefaultTabs.inactiveUnderlineColor": "gold",
        "DefaultTabs.hoverBackground": "hover", "DefaultTabs.background": "bgUi",
        "TabbedPane.underlineColor": "red", "TabbedPane.focusColor": "selInactive",
        "Editor.background": "bg", "Editor.foreground": "fg",
        "EditorPane.background": "bg", "EditorPane.inactiveBackground": "bg",
        "Panel.background": "bgUi", "SidePanel.background": "bgTool",
        "Tree.background": "bgTool", "Tree.selectionBackground": "selection",
        "Tree.selectionInactiveBackground": "selInactive",
        "List.background": "bgTool", "List.selectionBackground": "selection",
        "List.selectionInactiveBackground": "selInactive",
        "Table.background": "bgTool", "Table.selectionBackground": "selection",
        "Table.stripeColor": "caretRow", "Table.gridColor": "border",
        "Popup.background": "surface", "Popup.borderColor": "border",
        "Popup.Header.activeBackground": "surface", "Popup.Header.inactiveBackground": "surface",
        "PopupMenu.background": "surface", "Menu.background": "surface", "MenuItem.background": "surface",
        "MenuItem.selectionBackground": "selection", "Menu.selectionBackground": "selection",
        "ToolTip.background": "surface", "ToolTip.borderColor": "border",
        "Notification.background": "surface", "Notification.borderColor": "border",
        "SearchEverywhere.Tab.selectedBackground": "selection", "SearchEverywhere.SearchField.background": "surface",
        "SearchEverywhere.Header.background": "surface", "SearchEverywhere.List.separatorForeground": "muted",
        "SearchMatch.startBackground": "gold", "SearchMatch.endBackground": "gold",
        "TextField.background": "surface", "TextArea.background": "surface",
        "PasswordField.background": "surface", "FormattedTextField.background": "surface",
        "ComboBox.background": "surface", "ComboBox.nonEditableBackground": "surface",
        "ComboBox.ArrowButton.nonEditableBackground": "surface", "ComboBox.selectionBackground": "selection",
        "Component.borderColor": "border", "Component.focusColor": "gold",
        "Component.focusedBorderColor": "gold", "Component.errorFocusColor": "error",
        "Component.inactiveErrorFocusColor": "deleted", "Component.warningFocusColor": "warning",
        "Button.startBackground": "surface", "Button.endBackground": "surface",
        "Button.startBorderColor": "border", "Button.endBorderColor": "border",
        "Button.default.startBackground": "red", "Button.default.endBackground": "red",
        "Button.default.foreground": "redText", "Button.default.startBorderColor": "gold",
        "Button.default.endBorderColor": "gold", "Button.default.focusedBorderColor": "gold",
        "Button.default.focusColor": "gold",
        "ActionButton.hoverBackground": "hover", "ActionButton.pressedBackground": "selection",
        "ActionButton.hoverBorderColor": "hover", "ActionButton.pressedBorderColor": "selection",
        "Link.activeForeground": "azure", "Link.hoverForeground": "azure", "Link.pressedForeground": "gold",
        "Link.visitedForeground": "field",
        "ProgressBar.progressColor": "red", "ProgressBar.indeterminateStartColor": "red",
        "ProgressBar.indeterminateEndColor": "gold", "ProgressBar.trackColor": "border",
        "ProgressBar.passedColor": "string", "ProgressBar.failedColor": "error",
        "Counter.background": "red", "Counter.foreground": "redText",
        "CheckBox.background": "bgUi", "RadioButton.background": "bgUi",
        "Separator.separatorColor": "border",
        "ScrollBar.thumbColor": "guideSel", "ScrollBar.hoverThumbColor": "lineNo",
        "ScrollBar.Mac.thumbColor": "guideSel", "ScrollBar.Mac.hoverThumbColor": "lineNo",
        "ScrollBar.Transparent.thumbColor": "guideSel", "ScrollBar.Mac.Transparent.thumbColor": "guideSel",
        "RunWidget.background": "red", "RunWidget.foreground": "redText",
        "RunWidget.runningBackground": "string", "RunWidget.stopBackground": "error",
        "VersionControl.Log.Commit.currentBranchBackground": "caretRow",
        "VersionControl.Log.Commit.hoveredBackground": "hover",
        "VersionControl.RefLabel.backgroundBase": "gold",
        "FileColor.Yellow": "labelBg", "FileColor.Green": "diffIns", "FileColor.Blue": "diffMod",
        "FileColor.Rose": "diffDel", "FileColor.Orange": "diffConf", "FileColor.Violet": "selInactive",
        "Banner.infoBackground": "diffMod", "Banner.warningBackground": "diffConf",
        "Banner.errorBackground": "diffDel", "Banner.successBackground": "diffIns",
        "ValidationTooltip.errorBackground": "diffDel", "ValidationTooltip.warningBackground": "diffConf",
        "WelcomeScreen.background": "bgUi", "WelcomeScreen.SidePanel.background": "bgTool",
        "WelcomeScreen.Projects.selectionBackground": "selection",
        "Plugins.background": "bgUi", "Plugins.SearchField.background": "surface",
        "Plugins.Button.installForeground": "red", "Plugins.Button.installBorderColor": "red",
        "Plugins.Button.installFillBackground": "red", "Plugins.Button.installFillForeground": "redText",
        "Plugins.Tab.selectedBackground": "selection", "Plugins.lightSelectionBackground": "selInactive",
        "NavBar.borderColor": "border",
        "DragAndDrop.areaBackground": "selInactive", "DragAndDrop.borderColor": "gold",
    }
    return {
        "name": p["name"], "dark": p["dark"], "author": "Wuxing Themes",
        "parentTheme": p["parentTheme"],
        "editorScheme": f"/themes/{slug}.xml",
        "colors": c, "ui": ui,
    }

for p, slug in [(NIGHT, "WuxingNight"), (DAY, "WuxingDay")]:
    xml = scheme(p)
    open(f"{OUT}/plugin/themes/{slug}.xml", "w").write(xml)
    open(f"{OUT}/{p['name']}.icls", "w").write(xml)
    json.dump(theme(p, slug), open(f"{OUT}/plugin/themes/{slug}.theme.json", "w"), indent=2)

open(f"{OUT}/plugin/META-INF/plugin.xml", "w").write("""<idea-plugin>
  <id>wuxing.themes</id>
  <name>Wuxing Themes</name>
  <version>1.0.0</version>
  <vendor>Wuxing Themes</vendor>
  <description><![CDATA[
    Dark and light themes built on Chinese colour symbolism and the Five Elements (Wuxing):
    vermilion keywords (Fire), jade strings (Wood), imperial-yellow types (Earth), a rice-paper or
    indigo-ink canvas in place of stark white and black (Metal and Water), gold for prosperity,
    Forbidden City purple for fields and turquoise for annotations.
  ]]></description>
  <change-notes><![CDATA[
    <b>1.0.0</b>: Initial release with Wuxing Night and Wuxing Day.
  ]]></change-notes>
  <idea-version since-build="233"/>
  <depends>com.intellij.modules.platform</depends>
  <extensions defaultExtensionNs="com.intellij">
    <themeProvider id="93584a5e-9007-4988-b46f-2262fc35943a" path="/themes/WuxingNight.theme.json"/>
    <themeProvider id="4b15b1a7-f789-4a43-851a-8b3f5bb0a4cf" path="/themes/WuxingDay.theme.json"/>
  </extensions>
</idea-plugin>
""")

for icon in ("pluginIcon.svg", "pluginIcon_dark.svg"):
    shutil.copy(os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", icon), f"{OUT}/plugin/META-INF/{icon}")

with zipfile.ZipFile(f"{OUT}/wuxing-themes-1.0.0.jar", "w", zipfile.ZIP_DEFLATED) as z:
    for root, _, files in os.walk(f"{OUT}/plugin"):
        for f in files:
            full = os.path.join(root, f)
            z.write(full, os.path.relpath(full, f"{OUT}/plugin"))

# ---------------------------------------------------------------- preview
JAVA = '''/** Handles orders. @since 1.0 */
@Controller("/orders")
public class OrderController {
    private static final int MAX_ITEMS = 42;
    private final OrderService orderService;

    public OrderController(OrderService orderService) {
        this.orderService = orderService;
    }

    @Get("/{id}")
    public Optional<Order> find(@PathVariable Long id) {
        // TODO: add caching
        return orderService.findById(id, "eur\\n");
    }
}'''
GROOVY = '''class OrderControllerSpec extends Specification {

    @Inject OrderService orderService

    def "returns order when it exists"() {
        given:
        def order = new Order(7L, 3)

        when:
        def result = orderService.findById(7L)

        then:
        result.present
        result.get().quantity == 3
    }
}'''
KW = set("public private static final class return extends new def if else void int long this".split())
FIELDS = {"orderService", "present", "quantity"}
def hl(code):
    out = []
    tok = re.compile(r'(/\*\*.*?\*/)|(//[^\n]*)|("(?:\\.|[^"])*")|(@\w+)|\b(given|when|then):|(\b\d+L?\b)|(\b[A-Za-z_]\w*\b)(\s*\()?|(\s+|.)', re.S)
    for m in tok.finditer(code):
        doc, com, st, ann, lab, num, word, paren, other = m.groups()
        e = html.escape
        if doc:
            d = e(doc).replace("@since", '<span class="dt">@since</span>'); out.append(f'<span class="doc">{d}</span>')
        elif com:
            c = e(com).replace("TODO", '<span class="todo">TODO</span>'); out.append(f'<span class="cm">{c}</span>')
        elif st:
            s = e(st).replace("\\n", '<span class="esc">\\n</span>'); out.append(f'<span class="st">{s}</span>')
        elif ann: out.append(f'<span class="an">{e(ann)}</span>')
        elif lab: out.append(f'<span class="lb">{lab}:</span>')
        elif num: out.append(f'<span class="nu">{num}</span>')
        elif word:
            if word in KW: cls = "kw"
            elif word.isupper() and len(word) > 1: cls = "co"
            elif word[0].isupper(): cls = "ty"
            elif paren: cls = "md" if word in ("find", "OrderController") else "ca"
            elif word in FIELDS: cls = "fd"
            else: cls = ""
            out.append(f'<span class="{cls}">{word}</span>' if cls else word)
            if paren: out.append(e(paren))
        else:
            out.append(f'<span class="op">{e(other)}</span>' if other.strip() else other)
    return "".join(out)

def css(p, sel):
    h = lambda k: "#" + p[k]
    return f"""{sel}{{background:{h('bgUi')};color:{h('fg')};border-color:{h('border')}}}
{sel} .bar{{background:{h('bgUi')};border-bottom:1px solid {h('border')};color:{h('muted')}}}
{sel} .tab{{background:{h('bg')};color:{h('fg')};border-bottom:2px solid {h('red')}}}
{sel} .btn{{background:{h('red')};color:{h('redText')};border:1px solid {h('gold')}}}
{sel} .side{{background:{h('bgTool')};border-right:1px solid {h('border')};color:{h('muted')}}}
{sel} .side .on{{background:{h('selection')};color:{h('fg')}}}
{sel} pre{{background:{h('bg')}}}
{sel} .gut{{color:{h('lineNo')}}} {sel} .row{{background:{h('caretRow')}}} {sel} .row .gut{{color:{h('lineNoCaret')}}}
{sel} .caret{{border-left:2px solid {h('gold')}}}
{sel} .kw{{color:{h('keyword')};{'font-weight:600' if not p['dark'] else ''}}} {sel} .st{{color:{h('string')}}}
{sel} .nu{{color:{h('number')}}} {sel} .ty{{color:{h('type')}}} {sel} .md{{color:{h('method')};font-weight:600}}
{sel} .ca{{color:{h('call')}}} {sel} .fd{{color:{h('field')}}} {sel} .co{{color:{h('constant')};font-style:italic;font-weight:600}}
{sel} .an{{color:{h('annotation')}}} {sel} .lb{{color:{h('label')};background:{h('labelBg')};font-weight:600}}
{sel} .cm{{color:{h('comment')};font-style:italic}} {sel} .doc{{color:{h('doc')};font-style:italic}}
{sel} .dt{{color:{h('docTag')};font-weight:600}} {sel} .todo{{color:{h('todo')};font-weight:600}}
{sel} .esc{{color:{h('gold')};font-weight:600}} {sel} .op{{color:{h('op')}}}
{sel} .sw span{{background:var(--c)}}
"""

def pane(p, cls):
    def code(src, caret_line):
        lines = hl(src).split("\n")
        rows = []
        for i, l in enumerate(lines, 1):
            r = ' class="row"' if i == caret_line else ""
            rows.append(f'<div{r}><span class="gut">{i:>2}</span>  {l}</div>')
        return "<pre>" + "".join(rows) + "</pre>"
    sw = "".join(f'<span title="{k}" style="--c:#{p[k]}"></span>' for k in
                 ["bg", "fg", "keyword", "string", "type", "number", "method", "field", "annotation", "gold", "comment"])
    return f'''<section class="ide {cls}">
  <div class="bar"><b>{p["name"]}</b><span class="sw">{sw}</span><span class="btn">▶ Run</span></div>
  <div class="body"><div class="side"><div>src</div><div class="on">OrderController</div><div>OrderService</div><div>OrderControllerSpec</div></div>
  <div class="ed"><div class="tabs"><span class="tab">OrderController.java</span></div>{code(JAVA, 13)}
  <div class="tabs"><span class="tab">OrderControllerSpec.groovy</span></div>{code(GROOVY, 6)}</div></div>
</section>'''

page = f"""<!doctype html><html><head><meta charset="utf-8"><title>Wuxing Themes Preview</title>
<meta name="viewport" content="width=device-width,initial-scale=1"><style>
body{{margin:0;padding:16px;background:#888;font-family:system-ui,sans-serif}}
.ide{{border:1px solid;border-radius:10px;overflow:hidden;margin:0 auto 20px;max-width:900px}}
.bar{{display:flex;gap:14px;align-items:center;padding:8px 12px;font-size:13px}}
.btn{{margin-left:auto;padding:3px 12px;border-radius:5px;font-size:12px}}
.sw span{{display:inline-block;width:14px;height:14px;border-radius:3px;margin-right:3px;vertical-align:middle;box-shadow:0 0 0 1px #0003}}
.body{{display:flex}} .side{{width:170px;font-size:12.5px;padding:8px 0;flex-shrink:0}} .side div{{padding:3px 12px}}
.ed{{flex:1;min-width:0}} .tabs{{padding:6px 0 0 8px}} .tab{{display:inline-block;padding:4px 10px;font-size:12px}}
pre{{margin:0;padding:8px 0;font:13px/1.55 'JetBrains Mono',ui-monospace,Menlo,monospace;overflow-x:auto}}
pre div{{padding:0 12px;white-space:pre}}
@media (max-width:640px){{.side{{display:none}}}}
{css(NIGHT, '.night')}{css(DAY, '.day')}
</style></head><body>{pane(NIGHT, 'night')}{pane(DAY, 'day')}</body></html>"""
open(f"{OUT}/preview.html", "w").write(page)
print("ok")
