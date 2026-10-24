#!/usr/bin/env python3
"""Writes heritage/notepadpp.json, the lexers and styles that a Notepad++ theme sets, from the pinned Notepad++.

Usage: scripts/notepadpp/styles.py

It reads stylers.model.xml of the Notepad++ source that source.json pins: every LexerType with its WordsStyles, and
the WidgetStyles of GlobalStyles with the colour and font attributes each one has. Run it after moving the pin to a
new Notepad++ release; the build then fails on each new style that heritage/notepadpp.py does not map.
"""
import json, os, sys
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from tokens import CACHE, source_tree  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.dirname(HERE)), "heritage", "notepadpp.json")
# WidgetStyle attributes that a theme sets, in the order Notepad++ writes them.
ATTRIBUTES = ("fgColor", "bgColor", "fontName", "fontStyle", "fontSize")


def main():
    tree = source_tree(CACHE)
    with open(os.path.join(HERE, "source.json"), encoding="utf-8") as f:
        version = json.load(f)["notepad++"]
    root = ET.parse(os.path.join(tree, "PowerEditor", "src", "stylers.model.xml")).getroot()
    lexers = [{"name": lexer.get("name"), "desc": lexer.get("desc"), "ext": lexer.get("ext", ""),
               "styles": [{"id": int(style.get("styleID")), "name": style.get("name"),
                           **({"keywordClass": style.get("keywordClass")} if style.get("keywordClass") else {})}
                          for style in lexer.iter("WordsStyle")]}
              for lexer in root.find("LexerStyles").iter("LexerType")]
    widgets = [{"name": style.get("name"), "id": int(style.get("styleID")),
                "attributes": [a for a in ATTRIBUTES if a in style.attrib]}
               for style in root.find("GlobalStyles").iter("WidgetStyle")]
    def line(value):
        return json.dumps(value, ensure_ascii=False)
    # One style per line, so that a new pin shows in the diff as the styles it adds or changes.
    lexer_lines = ",\n".join(
        f'  {line({k: v for k, v in lexer.items() if k != "styles"})[:-1]}, "styles": [\n'
        + ",\n".join(f"    {line(style)}" for style in lexer["styles"]) + "]}" for lexer in lexers)
    widget_lines = ",\n".join(f"  {line(widget)}" for widget in widgets)
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(f'{{"notepad++": {line(version)}, "modelDate": {int(root.get("modelDate"))},\n'
                f' "lexers": [\n{lexer_lines}],\n "widgets": [\n{widget_lines}]}}\n')
    print(f"{OUT}: {len(lexers)} lexers, {sum(len(l['styles']) for l in lexers)} styles, {len(widgets)} widget styles")


if __name__ == "__main__":
    main()
