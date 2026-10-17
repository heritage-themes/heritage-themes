"""HTML preview of a theme family: one IDE window per theme, with a code sample per language.

Code colours and font styles come from heritage.scheme.attributes(), so the preview shows what the
editor scheme sets. Keys that the scheme leaves to a fallback resolve through FALLBACKS, which follows
the fallback chains of the bundled language plugins. The window chrome takes its colours from the
UI theme (CHROME), laid out as the Islands UI: the editor and tool windows as islands on the frame.
"""
import html, re

from .samples import SAMPLES
from .scheme import attributes, BOLD, ITALIC, BI, UNDER, WAVE, STRIKE, BOX, DOTTED
from .ui import theme

FONT_DIR = "fonts"
FONTS = [("Regular", 400, "normal"), ("Italic", 400, "italic"), ("Bold", 700, "normal"), ("BoldItalic", 700, "italic")]

ALIASES = dict(
    txt="TEXT", kw="DEFAULT_KEYWORD", st="DEFAULT_STRING", nu="DEFAULT_NUMBER", esc="DEFAULT_VALID_STRING_ESCAPE",
    cm="DEFAULT_LINE_COMMENT", bc="DEFAULT_BLOCK_COMMENT", doc="DEFAULT_DOC_COMMENT", dt="DEFAULT_DOC_COMMENT_TAG",
    ty="DEFAULT_CLASS_NAME", it="DEFAULT_INTERFACE_NAME", fn="DEFAULT_FUNCTION_DECLARATION",
    ca="DEFAULT_FUNCTION_CALL", fd="DEFAULT_INSTANCE_FIELD", co="DEFAULT_CONSTANT", an="DEFAULT_METADATA",
    pa="DEFAULT_PARAMETER", lb="DEFAULT_LABEL", op="DEFAULT_OPERATION_SIGN", todo="TODO_DEFAULT_ATTRIBUTES",
    ps="DEFAULT_PREDEFINED_SYMBOL",
    ht="HTML_TAG", hn="HTML_TAG_NAME", ha="HTML_ATTRIBUTE_NAME", hv="HTML_ATTRIBUTE_VALUE",
    he="HTML_ENTITY_REFERENCE", hc="HTML_CUSTOM_TAG_NAME",
)
FALLBACKS = {
    "CSS.IDENT": "HTML_TAG_NAME", "CSS.TAG_NAME": "HTML_TAG_NAME", "CSS.FUNCTION": "HTML_TAG_NAME",
    "CSS.CLASS_NAME": "CSS.IDENT", "CSS.PSEUDO": "CSS.IDENT",
    "CSS.PROPERTY_NAME": "HTML_ATTRIBUTE_NAME", "CSS.PROPERTY_VALUE": "HTML_ATTRIBUTE_VALUE",
    "CSS.UNIT": "CSS.PROPERTY_VALUE", "CSS.NUMBER": "DEFAULT_NUMBER", "CSS.STRING": "DEFAULT_STRING",
    "CSS.COLON": "TEXT",
    "KOTLIN_EXTENSION_FUNCTION_CALL": "DEFAULT_STATIC_METHOD",
    "BASH.VAR_DEF": "BASH.VAR_USE", "BASH.VAR_USE": "DEFAULT_GLOBAL_VARIABLE",
    "YAML_SCALAR_KEY": "DEFAULT_KEYWORD", "YAML_SCALAR_VALUE": "TEXT", "YAML_SCALAR_DSTRING": "DEFAULT_STRING",
    "YAML_COMMENT": "DEFAULT_DOC_COMMENT", "YAML_SIGN": "DEFAULT_OPERATION_SIGN",
    "JSON.PROPERTY_KEY": "DEFAULT_INSTANCE_FIELD", "JSON.STRING": "DEFAULT_STRING",
    "JSON.KEYWORD": "DEFAULT_KEYWORD", "JSON.NUMBER": "DEFAULT_NUMBER",
    **{f"MARKDOWN_{m}_MARKER": "DEFAULT_KEYWORD" for m in ("HEADER", "BOLD", "ITALIC", "LIST", "CODE_SPAN", "CODE_FENCE")},
    "MARKDOWN_CODE_SPAN": "DEFAULT_STRING", "MARKDOWN_CODE_FENCE": "DEFAULT_STRING",
    "MARKDOWN_CODE_FENCE_LANGUAGE": "DEFAULT_CONSTANT", "MARKDOWN_LINK_TEXT": "HYPERLINK_ATTRIBUTES",
    "MARKDOWN_LINK_DESTINATION": "DEFAULT_STATIC_METHOD",
}
SWATCHES = ["bg", "fg", "keyword", "string", "type", "number", "method", "field", "annotation", "gold", "comment"]
# CSS variable → UI theme key for the window chrome.
CHROME = {
    "frame": "MainWindow.background", "island": "ToolWindow.background", "editor": "EditorTabs.background",
    "underTabs": "EditorTabs.underTabsBorderColor", "tab": "EditorTabs.underlinedTabBackground",
    "tabBorder": "EditorTabs.underlinedBorderColor",
    "stripeOn": "ToolWindow.Button.selectedBackground", "stripeOnFg": "ToolWindow.Button.selectedForeground",
    "stripeFg": "ToolWindow.Button.foreground", "status": "StatusBar.background",
}
DECORATION = {UNDER: "underline", WAVE: "underline wavy", STRIKE: "line-through", DOTTED: "underline dotted"}

MARK = re.compile(r"«([^:»]+):([^»]*)»")
PLAIN = re.compile(r"(\s+)|(\w+)|(\S)")


def resolve(attrs, key):
    """The attribute for key, following FALLBACKS for keys the scheme does not set."""
    key = ALIASES.get(key, key)
    while key not in attrs:
        if key not in FALLBACKS:
            raise SystemExit(f"preview: the scheme does not set {key} and FALLBACKS has no entry for it")
        key = FALLBACKS[key]
    return attrs[key]


def style(p, a):
    css = [f"color:#{a['fg'] or p['fg']}"]
    if a["bg"] and a["bg"] != p["bg"]: css.append(f"background:#{a['bg']}")  # TEXT's bg would hide the caret row
    if a["font"] in (BOLD, BI): css.append("font-weight:700")
    if a["font"] in (ITALIC, BI): css.append("font-style:italic")
    if a["effect"] and a["etype"] == BOX: css.append(f"outline:1px solid #{a['effect']}")
    elif a["effect"]: css.append(f"text-decoration:{DECORATION[a['etype']]} #{a['effect']}")
    return ";".join(css)


def span(p, attrs, key, text):
    return f'<span style="{style(p, resolve(attrs, key))}">{html.escape(text)}</span>'


def highlight(p, attrs, line):
    """One sample line as HTML: marked spans as marked, unmarked words as TEXT, punctuation as operators."""
    out, pos = [], 0
    for m in [*MARK.finditer(line), None]:
        for ws, word, punct in PLAIN.findall(line[pos:m.start() if m else len(line)]):
            out.append(ws or span(p, attrs, "TEXT" if word else "op", word or punct))
        if m:
            out.append(span(p, attrs, m.group(1), m.group(2)))
            pos = m.end()
    return "".join(out)


def sample(p, attrs, name, caret, code):
    rows = []
    for i, line in enumerate(code.split("\n"), 1):
        row = ' class="caret-row"' if i == caret else ""
        tail = '<span class="caret"></span>' if i == caret else ""
        rows.append(f'<div{row}><span class="gutter">{i:>2}</span>{highlight(p, attrs, line)}{tail}</div>')
    return (f'<article class="file"><div class="tabs"><span class="tab">{html.escape(name)}</span></div>'
            f'<pre>{"".join(rows)}</pre></article>')


def chrome(p):
    """CSS variables for the window chrome, resolved from the UI theme."""
    t = theme(p, "")
    return ";".join(f"--{var}:{t['colors'].get(t['ui'][key], t['ui'][key])}" for var, key in CHROME.items())


def window(p):
    attrs = attributes(p)
    names = [name for name, _, _ in SAMPLES]
    variables = ";".join(f"--{k}:#{v}" for k, v in p.items() if isinstance(v, str) and re.fullmatch(r"[0-9A-F]{6}", v))
    swatches = "".join(f'<span title="{k}" style="background:#{p[k]}"></span>' for k in SWATCHES)
    tree = "".join(f'<div{" class=on" if i == 0 else ""}>{html.escape(n)}</div>' for i, n in enumerate(names))
    files = "".join(sample(p, attrs, *s) for s in SAMPLES)
    return (f'<section class="ide" style="{variables};{chrome(p)};--caret:#{p.get("caret", p["gold"])}">'
            f'<header class="bar"><b>{html.escape(p["name"])}</b><span class="swatches">{swatches}</span></header>'
            f'<div class="body"><div class="stripe"><i class="on"></i><i></i><i></i></div>'
            f'<nav class="side"><div class="root">orders</div>{tree}</nav>'
            f'<div class="files">{files}</div></div>'
            f'<footer class="status">orders › src › {html.escape(names[0])}</footer></section>')


def page(family):
    """The preview page for every theme in the family."""
    faces = "".join(
        f'@font-face{{font-family:"JetBrains Mono";font-weight:{w};font-style:{s};'
        f'src:url("{FONT_DIR}/JetBrainsMono-{n}.woff2") format("woff2"),local("JetBrains Mono")}}' for n, w, s in FONTS)
    windows = "".join(window(t["palette"]) for t in family.THEMES)
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{html.escape(family.FAMILY)} Preview</title>
<meta name="viewport" content="width=device-width,initial-scale=1"><style>
{faces}
body{{margin:0;padding:24px;font-family:system-ui,sans-serif}}
.ide{{max-width:1280px;margin:0 auto 24px;border:1px solid var(--border);border-radius:10px;overflow:hidden;
  background:var(--frame);color:var(--fg)}}
.bar{{display:flex;gap:14px;align-items:center;padding:8px 12px;font-size:13px;color:var(--muted)}}
.bar b{{color:var(--fg)}}
.swatches span{{display:inline-block;width:14px;height:14px;border-radius:3px;margin-right:3px;vertical-align:middle;
  box-shadow:0 0 0 1px #0003}}
.body{{display:flex;gap:5px;padding:0 5px 0 0}}
.stripe{{width:34px;flex-shrink:0;display:flex;flex-direction:column;align-items:center;gap:6px;padding-top:2px}}
.stripe i{{width:26px;height:26px;border-radius:6px;position:relative}}
.stripe i::after{{content:"";position:absolute;inset:8px 7px;border:1.5px solid var(--stripeFg);border-radius:2px}}
.stripe .on{{background:var(--stripeOn)}} .stripe .on::after{{border-color:var(--stripeOnFg)}}
.side{{width:180px;flex-shrink:0;padding:8px 0;font-size:12.5px;background:var(--island);color:var(--fg);
  border-radius:10px;overflow:hidden}}
.side div{{padding:3px 12px 3px 28px}} .side .root{{padding-left:12px;color:var(--muted)}}
.side .on{{background:var(--selection)}}
.files{{flex:1;min-width:0;display:grid;grid-template-columns:1fr 1fr;gap:5px}}
.file{{background:var(--bg);min-width:0;border-radius:10px;overflow:hidden}}
.tabs{{background:var(--editor);padding:5px 0 5px 6px;border-bottom:1px solid var(--underTabs)}}
.tab{{display:inline-block;padding:3px 9px;font-size:12px;background:var(--tab);
  border:1px solid var(--tabBorder);border-radius:6px}}
.status{{padding:5px 12px;font-size:12px;color:var(--muted);background:var(--status)}}
pre{{margin:0;padding:8px 0;font:13px/1.55 "JetBrains Mono",ui-monospace,monospace;font-variant-ligatures:none;
  overflow-x:auto;color:var(--fg)}}
pre div{{padding:0 12px 0 0;white-space:pre}}
.gutter{{display:inline-block;width:4ch;margin-right:2ch;text-align:right;color:var(--lineNo)}}
.caret-row{{background:var(--caretRow)}} .caret-row .gutter{{color:var(--lineNoCaret)}}
.caret{{display:inline-block;width:0;height:1.2em;margin-left:-1px;vertical-align:text-bottom;
  border-left:2px solid var(--caret)}}
@media (max-width:900px){{.side,.stripe{{display:none}} .body{{padding-left:5px}} .files{{grid-template-columns:1fr}}}}
</style></head><body>{windows}</body></html>
"""
