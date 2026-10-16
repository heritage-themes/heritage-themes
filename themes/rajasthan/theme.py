"""Rajasthan palettes. See heritage/__init__.py for what a theme.py defines."""

# Rajasthan: the colours of its cities, cloth and craft.
# Blue City is Jodhpur by night, its indigo-limewashed houses under the Mehrangarh fort;
# Pink City is Jaipur by day, its terracotta-pink sandstone around the Hawa Mahal.
# Each city is framed by the other: a saffron accent on the blue, a Jodhpur-blue accent on the pink.
# Kesariya saffron keywords (the Rajput turban), rani pink strings, bandhani red numbers,
# Jaisalmer golden-sandstone types, blue-pottery turquoise methods, leheriya green fields,
# indigo dabu-print constants, Jodhpur blue annotations, mehendi type parameters,
# Udaipur marble text. Spock labels are bold bandhani red.
BLUE = dict(
    name="Rajasthan Blue City", dark=True, parent="Darcula", parentTheme="ExperimentalDark",
    bg="13273C", bgUi="102235", bgTool="122539", surface="1B3148", hover="223A54",
    border="243E56", fg="F2EADF", muted="8F9AA3", disabled="5A6F85",
    caretRow="182E45", selection="2A4458", selInactive="233D5A", lineNo="4C6984", lineNoCaret="FF9F45",
    guide="1B3148", guideSel="36506B",
    keyword="FFA65F", string="FE99C7", number="FF958E", type="E5C68E", method="44D6D6", call="93D9D9",
    field="86D489", constant="C3AFFE", annotation="78C7FD", label="FF958E",
    comment="8C9194", doc="A89A80", docTag="C2B08E", op="B7B9B6", param="F2EADF", typeParam="CBDA96",
    gold="F2C75C", red="B5520F", redText="FFF4E6", azure="6CC0FF", caret="FF9F45",
    error="FF5A6A", warning="F5A93A", weak="8C7E58",
    searchBg="4A3E18", searchBorder="F2C75C", underCaret="24405A", writeCaret="4C2A2C",
    braceBg="2A4A40", todo="F2C75C",
    added="68A860", modified="4F9BD8", deleted="C0564A",
    diffIns="18302A", diffMod="15304A", diffDel="3A2028", diffConf="383218", fileYellow="283236",
    ansiRed="F2707A", ansiGreen="8FD47A", ansiYellow="F2C75C", ansiBlue="6CC0FF", ansiMagenta="E486D9", ansiCyan="4FD6C8",
)
PINK = dict(
    name="Rajasthan Pink City", dark=False, parent="Default", parentTheme="ExperimentalLight",
    bg="F6E6DF", bgUi="ECD2C6", bgTool="F0DBD1", surface="FAEEE8", hover="E4C6B8",
    border="DCBBAB", fg="2A2026", muted="75666A", disabled="AB9594",
    caretRow="F0DCD2", selection="CFE0F2", selInactive="E3D7D6", lineNo="AF9792", lineNoCaret="B34700",
    guide="EBD6CC", guideSel="D6B6A7",
    keyword="944F04", string="A0346C", number="AE2D2F", type="684A01", method="067272", call="1E7272",
    field="1A7728", constant="6A50A5", annotation="056A9D", label="A72629",
    comment="7D7072", doc="7A6450", docTag="5E4A38", op="5C5458", param="2A2026", typeParam="5E6A20",
    gold="C08A10", red="1D62B0", redText="FFF8F0", azure="1D62B0", caret="B34700",
    error="D01E2E", warning="A86800", weak="B0986A",
    searchBg="F5DA8A", searchBorder="C08A10", underCaret="D6E4F4", writeCaret="F5D3D3",
    braceBg="CFE8C8", todo="7F5800",
    added="5FA05A", modified="5A8AD0", deleted="C85A5A",
    diffIns="E0F0D8", diffMod="DCE7F5", diffDel="F8DADA", diffConf="F5E6C2", fileYellow="F5DEBD",
    ansiRed="B3203F", ansiGreen="377416", ansiYellow="7F5800", ansiBlue="1D62B0", ansiMagenta="A3207F", ansiCyan="067469",
)

FAMILY = "Rajasthan"
BLURB = ("The colours of Rajasthan's cities and cloth: kesariya-saffron keywords, rani-pink strings, "
         "golden-sandstone types and blue-pottery methods, on the blue houses of Jodhpur by night or the "
         "pink sandstone of Jaipur by day.")
THEMES = [
    dict(slug="RajasthanBlueCity", id="e5121026-cdd3-4fe3-bc84-55ede3e928af", palette=BLUE),
    dict(slug="RajasthanPinkCity", id="e3c73acc-13ec-4afb-8454-b314647b6acc", palette=PINK),
]
