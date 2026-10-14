"""Editor colour scheme XML generated from a palette."""

def attr(fg=None, bg=None, font=0, effect=None, etype=None, stripe=None):
    return dict(fg=fg, bg=bg, font=font, effect=effect, etype=etype, stripe=stripe)

BOLD, ITALIC, BI = 1, 2, 3
UNDER, WAVE, STRIKE, BOX, DOTTED = 1, 2, 3, 0, 5

def attributes(p):
    """Text attributes by attribute key, in scheme order."""
    a = {}
    def s(keys, v):
        for k in keys.split(): a[k] = v
    s("TEXT", attr(p["fg"], p["bg"]))
    s("DEFAULT_KEYWORD JAVA_KEYWORD GROOVY_KEYWORD KOTLIN_KEYWORD", attr(p["keyword"], font=BOLD if p.get("kwBold", not p["dark"]) else 0))
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
    s("DEFAULT_IDENTIFIER", attr(p["fg"])); s("DEFAULT_DOC_COMMENT_TAG_VALUE", attr(p["docTag"]))
    s("DEFAULT_GLOBAL_VARIABLE", attr(p["field"], font=ITALIC))
    s("DEFAULT_HIGHLIGHTED_REFERENCE", attr(effect=p["azure"], etype=UNDER))
    s("BAD_CHARACTER", attr(effect=p["error"], etype=WAVE))
    s("IMPLICIT_ANONYMOUS_CLASS_PARAMETER_ATTRIBUTES", attr(p["param"], effect=p["param"], etype=UNDER))
    s("TEMPLATE_VARIABLE_ATTRIBUTES", attr(p["field"]))
    # Language-specific keys fall back to the DEFAULT_* keys above unless the parent scheme or a bundled
    # language plugin colours them explicitly. Those explicit ones are overridden here; list them with
    # scripts/parent_overrides.py.
    # HTML, XML: the DEFAULT_TAG, DEFAULT_ATTRIBUTE and DEFAULT_ENTITY roles
    s("HTML_TAG HTML_TAG_NAME XML_TAG XML_TAG_NAME XML_PROLOGUE", attr(p["keyword"]))
    s("HTML_CUSTOM_TAG_NAME XML_CUSTOM_TAG_NAME", attr(p["type"]))
    s("HTML_ATTRIBUTE_NAME XML_ATTRIBUTE_NAME", attr(p["field"])); s("HTML_ATTRIBUTE_VALUE", attr(p["string"]))
    s("HTML_ENTITY_REFERENCE XML_ENTITY_REFERENCE", attr(p["gold"]))
    # CSS, Sass, Less
    s("CSS.COLOR", attr(p["number"])); s("CSS.URL", attr(p["string"], effect=p["string"], etype=UNDER))
    s("CSS.IMPORTANT", attr(p["keyword"], font=BOLD))
    s("SASS_RULE SASS_DIRECTIVE", attr(p["keyword"])); s("SASS_ATTRIBUTE", attr(p["field"]))
    s("SASS_VARIABLE LESS_VARIABLE", attr(p["field"], font=ITALIC)); s("SASS_CONSTANT", attr(p["constant"]))
    s("SASS_MIXIN", attr(p["call"])); s("SASS_COMMENT", attr(p["comment"], font=ITALIC))
    # regular expressions, in any language
    s("REGEXP.META REGEXP.ESC_CHARACTER REGEXP.QUOTE_CHARACTER", attr(p["gold"], font=BOLD))
    s("REGEXP.CHAR_CLASS", attr(p["number"], font=BOLD)); s("REGEXP.REDUNDANT_ESCAPE", attr(p["muted"]))
    s("REGEXP.BRACES REGEXP.BRACKETS REGEXP.PARENTHS", attr(p["op"]))
    s("REGEXP_MATCHED_GROUPS", attr(bg=p["underCaret"]))
    # JavaScript, TypeScript
    s("JS.REGEXP", attr(p["string"])); s("JS.LOCAL_VARIABLE", attr(p["fg"])); s("JS.PARAMETER", attr(p["param"]))
    s("JS.GLOBAL_VARIABLE", attr(p["field"], font=ITALIC))
    s("JS.GLOBAL_FUNCTION JS.INSTANCE_MEMBER_FUNCTION", attr(p["call"]))
    s("TS.TYPE_PARAMETER", attr(p["typeParam"], font=BOLD)); s("TS.TYPE_GUARD", attr(bg=p["diffIns"]))
    s("NG.SIGNAL", attr(p["call"]))
    # Kotlin
    s("KOTLIN_TYPE_PARAMETER", attr(p["typeParam"], font=BOLD))
    s("KOTLIN_NAMED_ARGUMENT KOTLIN_CONTEXT_ARGUMENT", attr(p["param"], font=ITALIC))
    s("KOTLIN_CLOSURE_DEFAULT_PARAMETER", attr(p["param"], font=BOLD))
    s("KOTLIN_BACKING_FIELD_VARIABLE", attr(p["field"], font=BOLD))
    s("KOTLIN_PACKAGE_FUNCTION_CALL", attr(p["call"], font=ITALIC))
    s("KOTLIN_DYNAMIC_FUNCTION_CALL", attr(p["call"], font=BI)); s("KOTLIN_DYNAMIC_PROPERTY_CALL", attr(p["field"], font=BI))
    s("KOTLIN_FUNCTION_LITERAL_BRACES_AND_ARROW", attr(p["op"], font=BOLD))
    s("KOTLIN_LABEL", attr(p["annotation"], font=ITALIC))
    s("KOTLIN_MUTABLE_VARIABLE", attr(effect=p["muted"], etype=UNDER))
    s("KOTLIN_SMART_CAST_VALUE KOTLIN_SMART_CAST_RECEIVER KOTLIN_SMART_CONSTANT", attr(bg=p["diffIns"]))
    s("KOTLIN_PROPERTY_WITH_BACKING_FIELD", attr(bg=p["selInactive"]))
    s("KOTLIN_RESOLVED_TO_ERROR", attr(effect=p["error"], etype=BOX, stripe=p["error"]))
    # Python
    s("PY.BUILTIN_NAME PY.PREDEFINED_USAGE", attr(p["call"], font=ITALIC))
    s("PY.PREDEFINED_DEFINITION", attr(p["method"], font=BOLD))
    s("PY.SELF_PARAMETER", attr(p["keyword"], font=ITALIC)); s("PY.KEYWORD_ARGUMENT", attr(p["param"], font=ITALIC))
    s("PY.STRING.B", attr(p["string"]))
    # SQL
    s("SQL_OUTER_QUERY_COLUMN", attr(p["field"], effect=p["field"], etype=UNDER)); s("SQL_SYNTHETIC_ENTITY", attr(p["call"]))
    # Groovy keys contain spaces, so they are set directly
    a["Static property reference ID"] = attr(p["field"], font=ITALIC)
    a["List/map to object conversion"] = attr(p["call"], font=BOLD)
    a["Unresolved reference access"] = attr(p["muted"], effect=p["muted"], etype=DOTTED)
    # Rust
    s("org.rust.FUNCTION_CALL org.rust.METHOD_CALL", attr(p["call"])); s("org.rust.MACRO", attr(p["annotation"]))
    s("org.rust.LIFETIME", attr(p["typeParam"], font=ITALIC)); s("org.rust.TYPE_PARAMETER", attr(p["typeParam"], font=BOLD))
    s("org.rust.MUT_BINDING org.rust.MUT_PARAMETER", attr(effect=p["muted"], etype=UNDER))
    s("org.rust.DIMMED_TEXT org.rust.CFG_DISABLED_CODE", attr(p["disabled"]))
    s("org.rust.GENERATED_ITEM", attr(p["muted"])); s("org.rust.UNSAFE_CODE", attr(bg=p["writeCaret"]))
    # properties, YAML
    s("PROPERTIES.KEY", attr(p["field"])); s("PROPERTIES.KEY_VALUE_SEPARATOR", attr(p["op"]))
    s("PROPERTIES.INVALID_STRING_ESCAPE", attr(p["error"], effect=p["error"], etype=WAVE))
    s("YAML_ANCHOR", attr(p["annotation"]))
    # shell
    s("BASH.SHEBANG", attr(p["comment"], font=BI))
    s("BASH.EXTERNAL_COMMAND BASH.FUNCTION_CALL", attr(p["call"])); s("BASH.INTERNAL_COMMAND", attr(p["call"], font=ITALIC))
    s("BASH.FUNCTION_DEF_NAME", attr(p["method"], font=BOLD))
    s("BASH.HERE_DOC_START BASH.HERE_DOC_END", attr(p["keyword"], font=BOLD)); s("BASH.BINARY_DATA", attr(bg=p["surface"]))
    # Markdown: headings take the declaration role
    s(" ".join(f"MARKDOWN_HEADER_LEVEL_{i}" for i in range(1, 7)) + " MARKDOWN_HEADER", attr(p["method"], font=BOLD))
    s("MARKDOWN_HEADER_BOLD MARKDOWN_BOLD", attr(font=BOLD)); s("MARKDOWN_ITALIC", attr(font=ITALIC))
    s("MARKDOWN_REFERENCE_LINK", attr(p["azure"]))
    # custom file types
    s("CUSTOM_KEYWORD1_ATTRIBUTES", attr(p["keyword"])); s("CUSTOM_KEYWORD2_ATTRIBUTES", attr(p["type"]))
    s("CUSTOM_KEYWORD3_ATTRIBUTES", attr(p["call"])); s("CUSTOM_KEYWORD4_ATTRIBUTES", attr(p["field"]))
    s("CUSTOM_STRING_ATTRIBUTES", attr(p["string"])); s("CUSTOM_NUMBER_ATTRIBUTES", attr(p["number"]))
    s("CUSTOM_LINE_COMMENT_ATTRIBUTES CUSTOM_MULTI_LINE_COMMENT_ATTRIBUTES", attr(p["comment"], font=ITALIC))
    s("CUSTOM_VALID_STRING_ESCAPE_ATTRIBUTES", attr(p["gold"], font=BOLD))
    s("CUSTOM_INVALID_STRING_ESCAPE_ATTRIBUTES", attr(p["error"], effect=p["error"], etype=WAVE))
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
    s("INLAY_DEFAULT", attr(p["muted"], p["caretRow"])); s("INLAY_TEXT_WITHOUT_BACKGROUND", attr(p["muted"]))
    s("INLINE_SUGGESTION", attr(p["muted"], font=ITALIC)); s("INJECTED_LANGUAGE_FRAGMENT", attr(bg=p["surface"]))
    s("INFO_ATTRIBUTES", attr(effect=p["weak"], etype=WAVE, stripe=p["weak"]))
    s("TYPO", attr(effect=p["added"], etype=WAVE))
    s("BREADCRUMBS_DEFAULT BREADCRUMBS_INACTIVE", attr(p["muted"]))
    s("BREADCRUMBS_HOVERED", attr(p["fg"], p["hover"])); s("BREADCRUMBS_CURRENT", attr(p["gold"], p["selInactive"]))
    # console & logs
    s("CONSOLE_NORMAL_OUTPUT", attr(p["fg"])); s("CONSOLE_SYSTEM_OUTPUT", attr(p["muted"]))
    s("CONSOLE_ERROR_OUTPUT LOG_ERROR_OUTPUT", attr(p["error"]))
    s("LOG_WARNING_OUTPUT", attr(p["warning"])); s("CONSOLE_USER_INPUT", attr(p["string"], font=ITALIC))
    s("LOG_INFO_OUTPUT", attr(p["string"])); s("LOG_DEBUG_OUTPUT LOG_VERBOSE_OUTPUT", attr(p["muted"]))
    s("LOG_EXPIRED_ENTRY", attr(p["disabled"]))
    for k, v in dict(RED="keyword", GREEN="string", YELLOW="label", BLUE="method", MAGENTA="field", CYAN="annotation").items():
        s(f"CONSOLE_{k}_OUTPUT CONSOLE_{k}_BRIGHT_OUTPUT", attr(p[v]))
    s("CONSOLE_BLACK_OUTPUT", attr(p["disabled"])); s("CONSOLE_DARKGRAY_OUTPUT", attr(p["muted"]))
    s("CONSOLE_GRAY_OUTPUT", attr(p["op"])); s("CONSOLE_WHITE_OUTPUT", attr(p["fg"]))
    # diff
    s("DIFF_INSERTED", attr(bg=p["diffIns"], stripe=p["added"]))
    s("DIFF_MODIFIED", attr(bg=p["diffMod"], stripe=p["modified"]))
    s("DIFF_DELETED", attr(bg=p["diffDel"], stripe=p["deleted"]))
    s("DIFF_CONFLICT", attr(bg=p["diffConf"], stripe=p["gold"]))
    return a

def colors(p):
    """Editor colours by colour key, in scheme order."""
    return dict(
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
    )

def scheme(p):
    """The editor colour scheme XML, used both inside the plugin and as a standalone .icls file."""
    L = [f'<scheme name="{p["name"]}" version="142" parent_scheme="{p["parent"]}">',
         '  <metaInfo><property name="ide">idea</property></metaInfo>', '  <colors>']
    for k, v in colors(p).items():
        L.append(f'    <option name="{k}" value="{v}" />')
    L += ['  </colors>', '  <attributes>']
    for k, v in attributes(p).items():
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
