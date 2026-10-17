"""Podhale palettes. See heritage/__init__.py for what a theme.py defines."""

# Podhale: the costume of the Highlanders (górale) below the Tatras, crimson, black and off-white.
# The parzenica on the white woollen trousers began as a cord loop, first in red, then red with navy;
# green, pink and blue were added later. Czerwień (crimson, the first cord and the band of the hat)
# keywords, granat (navy, the second cord) strings, zieleń (green) fields, niebieski (blue) types,
# róż (pink, from the cucha embroidery) annotations, korale (red coral beads) numbers and constants,
# mosiądz (brass, the buckles of the shepherd's belt and the shirt clasp) methods.
# Kłobuk is the black felt hat with its red band and white shells; Sukno is the white broadcloth
# of the trousers and the cucha.
KLOBUK = dict(
    name="Podhale Kłobuk (Dark)", dark=True, parent="Darcula",
    bg="161413", bgUi="121010", bgTool="141211", frame="2A2622", surface="1F1C1A", hover="292522",
    border="302B28", fg="ECE5D8", muted="968E82", disabled="5C5650",
    caretRow="1F1C1A", selection="3E2228", selInactive="2E2626", lineNo="58514A", lineNoCaret="F05C74",
    guide="221F1D", guideSel="3A3431",
    keyword="F05C74", string="93A6EE", number="F48C6A", type="72C4E0", method="E2B95E", call="EBCF94",
    field="8CCB7E", constant="F48C6A", annotation="EE9CCB", label="F05C74",
    comment="8C8478", doc="A0968A", docTag="C2B6A4", op="B2AAA0", param="ECE5D8", typeParam="A6DCEC",
    gold="E2B95E", red="B01E38", redText="FBF5EA", azure="93A6EE", caret="F05C74",
    error="FF6B5E", warning="E8A33A", weak="8A7D5C",
    searchBg="4A3D16", searchBorder="E2B95E", underCaret="21354A", writeCaret="47261F",
    braceBg="25402C", todo="E2B95E",
    added="6FAE68", modified="5E98D6", deleted="C8605A",
    diffIns="1C3020", diffMod="1A2A3C", diffDel="3E211C", diffConf="3A3218", fileYellow="221E19",
    ansiRed="F07E70", ansiGreen="95D27E", ansiYellow="E2B95E", ansiBlue="7FB0F5", ansiMagenta="D795D8", ansiCyan="6DCFD8",
)
SUKNO = dict(
    name="Podhale Sukno (Light)", dark=False, parent="Default",
    bg="F5F1E8", bgUi="EAE5D9", bgTool="F0EBE1", frame="DCD6C7", surface="FBF9F4", hover="E1DBCD",
    border="D6CFC0", fg="1C1A18", muted="6C665E", disabled="A9A296",
    caretRow="EEE9DE", selection="F0D6D6", selInactive="E5E0DA", lineNo="A8A194", lineNoCaret="B0102E",
    guide="E5E0D4", guideSel="CBC3B2",
    keyword="B0102E", string="223A92", number="B03C1C", type="06648A", method="7A5800", call="6A5420",
    field="2C6A22", constant="B03C1C", annotation="A02878", label="B0102E",
    comment="857C70", doc="6E6450", docTag="524A38", op="55504A", param="1C1A18", typeParam="1A6E8E",
    gold="9A7400", red="A0102A", redText="FBF6EC", azure="223A92", caret="B0102E",
    error="C42020", warning="A86800", weak="A8955E",
    searchBg="F0DC8A", searchBorder="9A7400", underCaret="D4E2F0", writeCaret="F2D4CC",
    braceBg="D2E6CC", todo="8A5A00",
    added="5E9A50", modified="4F7FC0", deleted="C05050",
    diffIns="DDEACB", diffMod="D8E2EE", diffDel="F2D6D4", diffConf="EEE0B4", fileYellow="EFE9D8",
    ansiRed="A3201E", ansiGreen="2D6B26", ansiYellow="7A5800", ansiBlue="1F55A8", ansiMagenta="8E2A90", ansiCyan="0A6A78",
)

FAMILY = "Podhale"
BLURB = ("The Highlander costume of Podhale: crimson keywords and navy strings from the cords of the parzenica, "
         "brass methods, green fields, blue types and coral numbers, on a black felt hat or white broadcloth.")
THEMES = [
    dict(slug="PodhaleKlobuk", id="abe5827b-9565-42bf-a9e7-b0542d9a9b61", palette=KLOBUK),
    dict(slug="PodhaleSukno", id="08ce4afd-37f1-4c51-b30f-398d9710d689", palette=SUKNO),
]
