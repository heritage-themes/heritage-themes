"""Style schemes for gedit, generated from a palette.

gedit colours code with libgedit-gtksourceview, a fork of GtkSourceView 4 for GTK 3 whose language definitions
(gedit.json, written by scripts/gedit/definitions.py) are older than those of GtkSourceView 5, and whose style schemes
take a format of their own (gtksourcestyleschemeparser.c): a required kind, no metadata, no author, no version, no
line-background, and underline_color for the underline's colour. The parser rejects a file with anything else.

The schemes colour code as heritage.gnome_text_editor does. A style takes the colours and font of the style of the same
id in GNOME Text Editor's scheme, as GtkSourceView 5 resolves it along its language's map-to chain, wherever the chain
of gedit's definitions would give it others: the definitions map Markdown's, reStructuredText's and MediaWiki's markup
to code styles, as def.lang has no markup styles. language_rules() sets the styles that GtkSourceView 5 has no style of
the same id for.

The scheme sets the editor's styles of libgedit-gtksourceview (gtksourcestyleschemecss.c, gtksourceview.c,
gtksourcebuffer.c, gtksourcesearchcontext.c, gtksourcespacedrawer.c) and of gedit's Quick Highlight plugin. gedit draws
its window in the desktop's GTK theme, which a scheme does not colour.

gedit uses one scheme while the desktop's style is light and another while it is dark, both chosen in its preferences,
which list every scheme and mark those whose kind does not suit the style. A theme's kind, light or dark, lets the user
choose it for either style.
"""
import json, os
from xml.sax.saxutils import quoteattr

from . import gnome_text_editor as gte
from .nvim import name  # noqa: F401 - the files take the names of Neovim's schemes

with open(os.path.join(os.path.dirname(__file__), "gedit.json"), encoding="utf-8") as f:
    DATA = json.load(f)
LANGUAGES = DATA["languages"]
DEFAULT_STYLES = tuple(f"def:{style}" for style in LANGUAGES["def"]["styles"])
# The styles of libgedit-gtksourceview's views and gedit's plugins that the scheme sets: the bookmarks plugin marks
# lines in the search-match colours, the Quick Highlight plugin other occurrences of the selected text in its own style.
EDITOR_STYLES = ("text", "selection", "selection-unfocused", "cursor", "current-line", "line-numbers",
                 "current-line-number", "bracket-match", "right-margin", "draw-spaces", "search-match",
                 "quick-highlight-match")
COLOUR_ATTRIBUTES = ("foreground", "background", "underline_color")


def language_rules(p):
    """(language, style ids, role, font) for the styles of gedit's definitions that GtkSourceView 5 has no style of
    the same id for, and whose chain gives a construct another role than the other targets give it."""
    kw = "bold" if p.get("kwBold", not p["dark"]) else ""
    return [
        # JavaScript's built-in properties as fields, and its future reserved words as keywords, as GtkSourceView 5's
        # js:built-in-property and js:reserved-word
        ("js", ("properties",), "field", ""),
        ("js", ("future-words",), "keyword", kw),
        # Markdown's code spans as strings, as GtkSourceView 5's markdown:code-span
        ("markdown", ("code",), "string", ""),
    ]


def resolve(languages, scheme, style_id):
    """The value that scheme gives style_id, along the map-to chain of languages, or None."""
    seen = set()
    while style_id is not None:
        if style_id in seen:
            raise ValueError(f"the map-to chain of {style_id} is circular")
        seen.add(style_id)
        if style_id in scheme:
            return scheme[style_id]
        language, _, item = style_id.partition(":")
        style_id = languages.get(language, {}).get("styles", {}).get(item)
    return None


def syntax_styles(p):
    """Style id → (role, font, background palette key or None): GNOME Text Editor's styles that gedit's definitions
    have, the styles whose chain gives them other colours than GNOME Text Editor's, then language_rules()."""
    reference = gte.syntax_styles(p)
    def known(style_id):
        language, _, item = style_id.partition(":")
        return item in LANGUAGES.get(language, {}).get("styles", {})
    out = {style_id: value for style_id, value in reference.items() if known(style_id)}
    for language, styles, role, font in language_rules(p):
        for item in styles:
            style_id = f"{language}:{item}"
            if not known(style_id):
                raise ValueError(f"{language} has no style {item!r}")
            if item in gte.LANGUAGES.get(language, {}).get("styles", {}):
                raise ValueError(f"{style_id} is in GtkSourceView 5, so it takes GNOME Text Editor's colours")
            if style_id in out:
                raise ValueError(f"{style_id} is set twice")
            out[style_id] = (role, font, None)
    # the shared styles, each wanted as GNOME Text Editor resolves it; setting one can change the styles that map to
    # it, so the pass repeats until every shared style resolves as wanted
    shared = {f"{language}:{item}": resolve(gte.LANGUAGES, reference, f"{language}:{item}")
              for language, styles in sorted(LANGUAGES.items()) for item in styles["styles"]
              if item in gte.LANGUAGES.get(language, {}).get("styles", {})}
    changed = True
    while changed:
        changed = False
        for style_id, wanted in shared.items():
            if wanted is not None and resolve(LANGUAGES, out, style_id) != wanted:
                out[style_id] = wanted
                changed = True
    return out


def editor_styles(p):
    """Editor style → dict of the style's attributes, as palette keys for colours: GNOME Text Editor's, and the
    occurrences of the selected text in the text colour on the identifier-under-caret wash, as GNOME Builder draws
    them."""
    reference = gte.editor_styles(p) | gte.builder_styles(p)
    out = {style_id: reference[style_id] for style_id in EDITOR_STYLES}
    return {style_id: {key.replace("underline-color", "underline_color"): value for key, value in attributes.items()}
            for style_id, attributes in out.items()}


def syntax_attributes(p, role, font, background=None):
    """GNOME Text Editor's attributes of a syntax style, with gedit's name for the underline's colour."""
    return {key.replace("underline-color", "underline_color"): value
            for key, value in gte.syntax_attributes(p, role, font, background).items()}


def scheme(t, source):
    """The styles/<theme>.xml file for a theme dict; source is the URL of the theme folder."""
    p = t["palette"]
    c = gte.hexes(p)
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             f"<!-- {p['name']}: a Heritage Themes style scheme for gedit. Generated from {source}; changes here are "
             "overwritten. SPDX-License-Identifier: MIT -->",
             f'<style-scheme id={quoteattr(name(t))} name={quoteattr(p["name"])} '
             f'kind="{"dark" if p["dark"] else "light"}">',
             f"  <description>{p['name']}: colours drawn from a culture's colour tradition.</description>"]

    def style(style_id, attributes):
        attrs = " ".join(f"{key}={quoteattr(value)}" for key, value in attributes.items())
        lines.append(f"  <style name={quoteattr(style_id)} {attrs}/>")
    for style_id, attributes in editor_styles(p).items():
        style(style_id, {k: c[v] if k in COLOUR_ATTRIBUTES else v for k, v in attributes.items()})
    for style_id, (role, font, background) in syntax_styles(p).items():
        style(style_id, syntax_attributes(p, role, font, background))
    lines.append("</style-scheme>")
    return "\n".join(lines) + "\n"


def styles(p):
    """Element → dict(fg, bg) as #rrggbb, for the build's contrast check: each syntax style on the background it is
    drawn on, bg unless it sets one, and on the current line, and the editor's text on its highlights."""
    c = gte.hexes(p)
    out = {}
    for style_id, (role, font, background) in syntax_styles(p).items():
        out[style_id] = dict(fg=c[role], bg=c[background or "bg"])
        if not background:
            out[f"{style_id} on the current line"] = dict(fg=c[role], bg=c["caretRow"])
    editor = editor_styles(p)
    for element, fg, style_id in (("found text", "fg", "search-match"), ("matching bracket", "fg", "bracket-match"),
                                  ("selected text", "fg", "selection"),
                                  ("occurrence of the selected text", "fg", "quick-highlight-match"),
                                  ("current line number", "lineNoCaret", "current-line-number")):
        out[element] = dict(fg=c[fg], bg=c[editor[style_id]["background"]])
    return out


def low_contrast(p):
    """The elements of styles() held to 3:1: the syntax styles in the roles of gte.LOW_CONTRAST_ROLES, and the one
    character that the bracket match draws its background behind, as in heritage.kate."""
    out = {"matching bracket"}
    for style_id, (role, *_) in syntax_styles(p).items():
        if role in gte.LOW_CONTRAST_ROLES:
            out |= {style_id, f"{style_id} on the current line"}
    return out


def pixel_palette(p):
    """What scripts/editors/pixels.py checks a screenshot against: the editor, cropped from the window that
    scripts/editors/shoot.py opens at 1100x700, with the header bar and status bar left out, where gedit draws its GTK
    theme."""
    colours = {colour.upper() for colour in gte.hexes(p).values()}
    backgrounds = ["#" + p[k] for k in ("caretRow", "selection", "selInactive", "diffConf", "searchBg", "braceBg",
                                        "underCaret")]
    return dict(background="#" + p["bg"], backgrounds=backgrounds, foregrounds=sorted(colours), crop=[52, 34, 6, 6])
