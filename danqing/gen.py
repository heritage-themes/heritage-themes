import json, os, re, html

# ---------------------------------------------------------------- palettes
# Danqing (丹青, "cinnabar and azurite" = Chinese painting): mineral pigments, not pastels.
# Deliberately breaks the usual green/yellow/blue syntax convention:
# cinnabar 朱砂 keywords, azurite 石青 types, gamboge 藤黄 methods, bamboo 竹青 strings,
# lotus-root 藕荷 fields, ochre 赭石 numbers, dai 黛 constants, malachite 石绿 annotations,
# ink 墨 on inkstone / xuan paper 宣纸, Spock labels as red seal stamps 印章.
INK = dict(
    name="Danqing Ink", dark=True, parent="Darcula", parentTheme="ExperimentalDark",
    bg="1B1D1B", bgUi="151716", bgTool="181A19", surface="232624", hover="2A2E2B",
    border="2C302D", fg="DCD6C8", muted="868A80", disabled="575C57",
    caretRow="202421", selection="2E3F45", selInactive="283335", lineNo="4B514C", lineNoCaret="F0643F",
    guide="252926", guideSel="3B423D",
    keyword="F0643F", string="A3B47E", number="C99A62", type="4FB3C9", method="E9B949", call="D9BE7E",
    field="CFA3C0", constant="A59FD2", annotation="6FBF9E", label="F6EEDF", labelBg="B8382A",
    comment="747B74", doc="8E9278", docTag="A9AB8A", op="A8A699", param="DCD6C8", typeParam="7FC4B6",
    gold="E9B949", red="B8382A", redText="F6EEDF", azure="4FB3C9", caret="F0643F",
    error="F25C54", warning="E6A23C", weak="8B8155",
    searchBg="4A3D18", searchBorder="E9B949", underCaret="263A3E", writeCaret="4A2622",
    braceBg="2F4A3E", todo="E9B949",
    added="6E9C5A", modified="4F93A8", deleted="A54A3E",
    diffIns="1F2E22", diffMod="1C2C31", diffDel="352021", diffConf="352E1C", fileYellow="29271C",
)
PAPER = dict(
    name="Danqing Paper", dark=False, parent="Default", parentTheme="ExperimentalLight",
    bg="EEEAE0", bgUi="E5E0D4", bgTool="E9E5DA", surface="F5F2EA", hover="DCD6C8",
    border="D2CBBB", fg="26282A", muted="6F6C64", disabled="A7A193",
    caretRow="E6E1D4", selection="C9DCE0", selInactive="DAE0DE", lineNo="A39D8B", lineNoCaret="B32D1E",
    guide="DDD7C9", guideSel="C5BCA7",
    keyword="B32D1E", string="4A6526", number="854E24", type="0F6680", method="7E5500", call="6F5210",
    field="7A3F6A", constant="4F4790", annotation="1A7353", label="F7EFE0", labelBg="B32D1E",
    comment="76736A", doc="676043", docTag="554D32", op="55534D", param="26282A", typeParam="0E6A62",
    gold="B8860B", red="B32D1E", redText="F7EFE0", azure="0F6680", caret="B32D1E",
    error="C8202F", warning="A86800", weak="A8975E",
    searchBg="EDD58A", searchBorder="B8860B", underCaret="CFE2E6", writeCaret="F0D2CB",
    braceBg="C8E0CF", todo="7E5500",
    added="5E9A5A", modified="4F8FA8", deleted="C0574B",
    diffIns="DDEBD6", diffMod="D7E6EA", diffDel="F2D8D2", diffConf="EFE2BF", fileYellow="E8E0C6",
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
        CARET_COLOR=p.get("caret", p["gold"]), CARET_ROW_COLOR=p["caretRow"], SELECTION_BACKGROUND=p["selection"],
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
        "FileColor.Yellow": "fileYellow", "FileColor.Green": "diffIns", "FileColor.Blue": "diffMod",
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
        "name": p["name"], "dark": p["dark"], "author": "Heritage Themes",
        "parentTheme": p["parentTheme"],
        "editorScheme": f"/themes/{slug}.xml",
        "colors": c, "ui": ui,
    }

# ---------------------------------------------------------------- bundle contract
# build.py in the repository root imports FAMILY, BLURB and generate() from every theme folder.
FAMILY = "Danqing"
BLURB = ("Chinese painting pigments: cinnabar keywords, azurite types, gamboge methods and bamboo-green "
         "strings on inkstone or xuan paper, with Spock blocks marked like red seal stamps.")
THEMES = [
    dict(slug="DanqingInk", id="d9d7840f-7402-422e-869e-dfbb781ca059", palette=INK),
    dict(slug="DanqingPaper", id="50103e31-3b24-415b-9b54-00acf1e7b7e5", palette=PAPER),
]

def generate():
    return [dict(slug=t["slug"], id=t["id"], name=t["palette"]["name"],
                 scheme=scheme(t["palette"]), theme=theme(t["palette"], t["slug"])) for t in THEMES]

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
  <div class="bar"><b>{p["name"]}</b><span class="sw">{sw}</span></div>
  <div class="body"><div class="side"><div>src</div><div class="on">OrderController</div><div>OrderService</div><div>OrderControllerSpec</div></div>
  <div class="ed"><div class="tabs"><span class="tab">OrderController.java</span></div>{code(JAVA, 13)}
  <div class="tabs"><span class="tab">OrderControllerSpec.groovy</span></div>{code(GROOVY, 6)}</div></div>
</section>'''

def preview():
    return f"""<!doctype html><html><head><meta charset="utf-8"><title>Danqing Preview</title>
<meta name="viewport" content="width=device-width,initial-scale=1"><style>
body{{margin:0;padding:16px;background:#888;font-family:system-ui,sans-serif}}
.ide{{border:1px solid;border-radius:10px;overflow:hidden;margin:0 auto 20px;max-width:900px}}
.bar{{display:flex;gap:14px;align-items:center;padding:8px 12px;font-size:13px}}
.sw span{{display:inline-block;width:14px;height:14px;border-radius:3px;margin-right:3px;vertical-align:middle;box-shadow:0 0 0 1px #0003}}
.body{{display:flex}} .side{{width:170px;font-size:12.5px;padding:8px 0;flex-shrink:0}} .side div{{padding:3px 12px}}
.ed{{flex:1;min-width:0}} .tabs{{padding:6px 0 0 8px}} .tab{{display:inline-block;padding:4px 10px;font-size:12px}}
pre{{margin:0;padding:8px 0;font:13px/1.55 'JetBrains Mono',ui-monospace,Menlo,monospace;overflow-x:auto}}
pre div{{padding:0 12px;white-space:pre}}
@media (max-width:640px){{.side{{display:none}}}}
{css(INK, '.ink')}{css(PAPER, '.paper')}
</style></head><body>{pane(INK, 'ink')}{pane(PAPER, 'paper')}</body></html>"""

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "build")
    os.makedirs(out, exist_ok=True)
    open(os.path.join(out, "preview.html"), "w").write(preview())
    print("ok")
