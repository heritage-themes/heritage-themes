"""Rajasthan palettes. See heritage/__init__.py for what a theme.py defines."""

# Rajasthan: the colours of its cities, cloth and craft.
# Blue City is Jodhpur by night, its indigo-limewashed houses under the Mehrangarh fort;
# Pink City is Jaipur by day, its terracotta-pink sandstone around the Hawa Mahal.
# Each city is framed by the other: a saffron accent on the blue, a Jodhpur-blue accent on the pink.
# Kesariya saffron keywords (the Rajput turban), Jaisalmer golden-sandstone methods,
# leheriya green strings, Jodhpur blue types, bandhani red numbers, rani pink fields,
# indigo dabu-print constants, blue-pottery turquoise annotations, mehendi type parameters,
# Udaipur marble text. Spock labels are bold bandhani red.
BLUE = dict(
    name="Rajasthan Blue City", dark=True, parent="Darcula", parentTheme="ExperimentalDark",
    bg="12212D", bgUi="0F1C26", bgTool="111F2A", surface="1A2B38", hover="213444",
    border="233746", fg="F2EADF", muted="8F9AA3", disabled="586773",
    caretRow="172836", selection="2A4458", selInactive="22374A", lineNo="4A6272", lineNoCaret="FF9F45",
    guide="1A2B38", guideSel="34495A",
    keyword="FF9F45", string="8FD47A", number="F2707A", type="6CC0FF", method="F2C75C", call="E3CB98",
    field="E486D9", constant="A9A2FF", annotation="4FD6C8", label="FF7A88",
    comment="8C9194", doc="A89A80", docTag="C2B08E", op="B7B9B6", param="F2EADF", typeParam="C4C66C",
    gold="F2C75C", red="B5520F", redText="FFF4E6", azure="6CC0FF", caret="FF9F45",
    error="FF5A6A", warning="F5A93A", weak="8C7E58",
    searchBg="4A3E18", searchBorder="F2C75C", underCaret="24405A", writeCaret="4C2A2C",
    braceBg="2A4A40", todo="F2C75C",
    added="68A860", modified="4F9BD8", deleted="C0564A",
    diffIns="18302A", diffMod="15304A", diffDel="3A2028", diffConf="383218", fileYellow="262B26",
    ansiRed="F2707A", ansiGreen="8FD47A", ansiYellow="F2C75C", ansiBlue="6CC0FF", ansiMagenta="E486D9", ansiCyan="4FD6C8",
)
PINK = dict(
    name="Rajasthan Pink City", dark=False, parent="Default", parentTheme="ExperimentalLight",
    bg="F9F0EC", bgUi="EFDCD3", bgTool="F3E5DE", surface="FDF8F5", hover="E7D0C5",
    border="DFC5B8", fg="2A2026", muted="75666A", disabled="AE9EA0",
    caretRow="F3E6DF", selection="CFE0F2", selInactive="E6E1E3", lineNo="B2A09E", lineNoCaret="B34700",
    guide="EEE0D9", guideSel="D9C0B4",
    keyword="B34700", string="3D7A1E", number="B3203F", type="1D62B0", method="7F5800", call="6E5418",
    field="A3207F", constant="3F3FA8", annotation="00796E", label="B3203F",
    comment="7D7072", doc="7A6450", docTag="5E4A38", op="5C5458", param="2A2026", typeParam="5E6E14",
    gold="C08A10", red="1D62B0", redText="FFF8F0", azure="1D62B0", caret="B34700",
    error="D01E2E", warning="A86800", weak="B0986A",
    searchBg="F5DA8A", searchBorder="C08A10", underCaret="D6E4F4", writeCaret="F5D3D3",
    braceBg="CFE8C8", todo="7F5800",
    added="5FA05A", modified="5A8AD0", deleted="C85A5A",
    diffIns="E0F0D8", diffMod="DCE7F5", diffDel="F8DADA", diffConf="F5E6C2", fileYellow="F8E8CA",
    ansiRed="B3203F", ansiGreen="3D7A1E", ansiYellow="7F5800", ansiBlue="1D62B0", ansiMagenta="A3207F", ansiCyan="00796E",
)

FAMILY = "Rajasthan"
BLURB = ("The colours of Rajasthan's cities and cloth: kesariya-saffron keywords, golden-sandstone methods, "
         "leheriya-green strings and Jodhpur-blue types, on the blue houses of Jodhpur by night or the "
         "pink sandstone of Jaipur by day.")
THEMES = [
    dict(slug="RajasthanBlueCity", id="e5121026-cdd3-4fe3-bc84-55ede3e928af", palette=BLUE),
    dict(slug="RajasthanPinkCity", id="e3c73acc-13ec-4afb-8454-b314647b6acc", palette=PINK),
]
