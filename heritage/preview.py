"""HTML preview of a theme family: one IDE window per theme, with a code sample per language.

Code colours and font styles come from heritage.scheme.attributes(), so the preview shows what the
editor scheme sets. Keys that the scheme leaves to a fallback resolve through FALLBACKS, which follows
the fallback chains of the bundled language plugins.
"""
import html, re

from .samples import SAMPLES
from .scheme import attributes, BOLD, ITALIC, BI, UNDER, WAVE, STRIKE, BOX, DOTTED

FONT_DIR = "fonts"
FONTS = [("Regular", 400, "normal"), ("Italic", 400, "italic"), ("Bold", 700, "normal"), ("BoldItalic", 700, "italic")]

ALIASES = dict(
    txt="TEXT", kw="DEFAULT_KEYWORD", st="DEFAULT_STRING", nu="DEFAULT_NUMBER", esc="DEFAULT_VALID_STRING_ESCAPE",
    cm="DEFAULT_LINE_COMMENT", bc="DEFAULT_BLOCK_COMMENT", doc="DEFAULT_DOC_COMMENT", dt="DEFAULT_DOC_COMMENT_TAG",
    ty="DEFAULT_CLASS_NAME", it="DEFAULT_INTERFACE_NAME", fn="DEFAULT_FUNCTION_DECLARATION",
    ca="DEFAULT_FUNCTION_CALL", fd="DEFAULT_INSTANCE_FIELD", co="DEFAULT_CONSTANT", an="DEFAULT_METADATA",
    pa="DEFAULT_PARAMETER", lb="DEFAULT_LABEL", op="DEFAULT_OPERATION_SIGN", todo="TODO_DEFAULT_ATTRIBUTES",
    ht="HTML_TAG", hn="HTML_TAG_NAME", ha="HTML_ATTRIBUTE_NAME", hv="HTML_ATTRIBUTE_VALUE",
    he="HTML_ENTITY_REFERENCE", hc="HTML_CUSTOM_TAG_NAME",
)
FALLBACKS = {
    "CSS.IDENT": "HTML_TAG_NAME", "CSS.TAG_NAME": "HTML_TAG_NAME", "CSS.FUNCTION": "HTML_TAG_NAME",
    "CSS.CLASS_NAME": "CSS.IDENT", "CSS.PSEUDO": "CSS.IDENT",
    "CSS.PROPERTY_NAME": "HTML_ATTRIBUTE_NAME", "CSS.PROPERTY_VALUE": "HTML_ATTRIBUTE_VALUE",
    "CSS.UNIT": "CSS.PROPERTY_VALUE", "CSS.NUMBER": "DEFAULT_NUMBER", "CSS.STRING": "DEFAULT_STRING",
    "CSS.COLON": "TEXT",
}
SWATCHES = ["bg", "fg", "keyword", "string", "type", "number", "method", "field", "annotation", "gold", "comment"]
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


def window(p):
    attrs = attributes(p)
    names = [name for name, _, _ in SAMPLES]
    variables = ";".join(f"--{k}:#{v}" for k, v in p.items() if isinstance(v, str) and re.fullmatch(r"[0-9A-F]{6}", v))
    swatches = "".join(f'<span title="{k}" style="background:#{p[k]}"></span>' for k in SWATCHES)
    tree = "".join(f'<div{" class=on" if i == 0 else ""}>{html.escape(n)}</div>' for i, n in enumerate(names))
    files = "".join(sample(p, attrs, *s) for s in SAMPLES)
    return (f'<section class="ide" style="{variables};--caret:#{p.get("caret", p["gold"])}">'
            f'<header class="bar"><b>{html.escape(p["name"])}</b><span class="swatches">{swatches}</span></header>'
            f'<div class="body"><nav class="side"><div class="root">orders</div>{tree}</nav>'
            f'<div class="files">{files}</div></div></section>')


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
  background:var(--bgUi);color:var(--fg)}}
.bar{{display:flex;gap:14px;align-items:center;padding:8px 12px;font-size:13px;color:var(--muted);
  border-bottom:1px solid var(--border)}}
.bar b{{color:var(--fg)}}
.swatches span{{display:inline-block;width:14px;height:14px;border-radius:3px;margin-right:3px;vertical-align:middle;
  box-shadow:0 0 0 1px #0003}}
.body{{display:flex}}
.side{{width:180px;flex-shrink:0;padding:8px 0;font-size:12.5px;background:var(--bgTool);color:var(--fg);
  border-right:1px solid var(--border)}}
.side div{{padding:3px 12px 3px 28px}} .side .root{{padding-left:12px;color:var(--muted)}}
.side .on{{background:var(--selection)}}
.files{{flex:1;min-width:0;display:grid;grid-template-columns:1fr 1fr;gap:1px;background:var(--border)}}
.file{{background:var(--bg);min-width:0}}
.tabs{{background:var(--bgUi);padding:6px 0 0 8px;border-bottom:1px solid var(--border)}}
.tab{{display:inline-block;padding:4px 10px;font-size:12px;background:var(--bg);border-bottom:2px solid var(--red)}}
pre{{margin:0;padding:8px 0;font:13px/1.55 "JetBrains Mono",ui-monospace,monospace;font-variant-ligatures:none;
  overflow-x:auto;color:var(--fg)}}
pre div{{padding:0 12px 0 0;white-space:pre}}
.gutter{{display:inline-block;width:4ch;margin-right:2ch;text-align:right;color:var(--lineNo)}}
.caret-row{{background:var(--caretRow)}} .caret-row .gutter{{color:var(--lineNoCaret)}}
.caret{{display:inline-block;width:0;height:1.2em;margin-left:-1px;vertical-align:text-bottom;
  border-left:2px solid var(--caret)}}
@media (max-width:900px){{.side{{display:none}} .files{{grid-template-columns:1fr}}}}
</style></head><body>{windows}</body></html>
"""
