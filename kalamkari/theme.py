"""Kalamkari palettes. See heritage/__init__.py for what a theme.py defines."""

# Kalamkari (कलमकारी, "pen work"): cotton hand-painted with a bamboo kalam and natural dyes,
# as in Srikalahasti and Machilipatnam. Every colour is a dye the craft uses:
# madder/chay root red keywords, neel indigo types, myrobalan (harad) yellow methods,
# indigo-over-myrobalan green strings, catechu (kattha) rust numbers, lac crimson fields,
# madder-over-indigo violet constants, indigo-wash teal annotations.
# The canvas is a vat of indigo or unbleached cotton; text is kasimi, the iron-black outline ink.
# Spock labels are bold madder red.
INDIGO = dict(
    name="Kalamkari Indigo", dark=True, parent="Darcula", parentTheme="ExperimentalDark",
    bg="141B2B", bgUi="111724", bgTool="131927", surface="1B2336", hover="222B41",
    border="253048", fg="EDE3CF", muted="878DA2", disabled="565D73",
    caretRow="182034", selection="2C3B5E", selInactive="232D46", lineNo="48526C", lineNoCaret="EE7A63",
    guide="1E2639", guideSel="36415D",
    keyword="EE7A63", string="A9C47F", number="DB9F6E", type="93AAEB", method="EAC46A", call="D8C595",
    field="DE8FB0", constant="B3A3E6", annotation="6EC6B6", label="F2917C",
    comment="7B8299", doc="9A9180", docTag="B6AB92", op="ADAAA6", param="EDE3CF", typeParam="80CFC9",
    gold="EAB84A", red="A8402F", redText="F6ECD8", azure="93AAEB", caret="EAB84A",
    error="F2556B", warning="E5A33C", weak="877D5A",
    searchBg="48401C", searchBorder="EAB84A", underCaret="27375A", writeCaret="4A2A2E",
    braceBg="2C4A44", todo="EAB84A",
    added="6A9E64", modified="5E82C8", deleted="B0544A",
    diffIns="1A2E2A", diffMod="1B2645", diffDel="36202A", diffConf="35301E", fileYellow="262826",
    ansiRed="EE7A63", ansiGreen="A9C47F", ansiYellow="EAC46A", ansiBlue="93AAEB", ansiMagenta="DE8FB0", ansiCyan="6EC6B6",
)
COTTON = dict(
    name="Kalamkari Cotton", dark=False, parent="Default", parentTheme="ExperimentalLight",
    bg="F2EAD8", bgUi="E8DEC8", bgTool="EDE4D0", surface="F8F2E5", hover="DFD3BA",
    border="D6C9AE", fg="2A2218", muted="6C6252", disabled="A89C84",
    caretRow="EAE0CA", selection="CBD5EA", selInactive="DEDCD3", lineNo="A5977B", lineNoCaret="A3301F",
    guide="E1D6BF", guideSel="C9B99A",
    keyword="A3301F", string="46672A", number="8E481B", type="27408A", method="745200", call="68521A",
    field="892C5A", constant="533E8C", annotation="1D6B63", label="A3301F",
    comment="776D5B", doc="6A5E3F", docTag="564B2F", op="595145", param="2A2218", typeParam="1F6676",
    gold="B07D12", red="A3301F", redText="F8EFDE", azure="27408A", caret="A3301F",
    error="C42032", warning="A86A00", weak="A8955E",
    searchBg="EDD28A", searchBorder="B07D12", underCaret="D2DBEE", writeCaret="F0D0C6",
    braceBg="CFE0C8", todo="745200",
    added="5E9450", modified="4F6FB0", deleted="B8503E",
    diffIns="DCE8CF", diffMod="D8DFEF", diffDel="F2D6CC", diffConf="EEE0BA", fileYellow="F0E2BD",
    ansiRed="A3301F", ansiGreen="46672A", ansiYellow="745200", ansiBlue="27408A", ansiMagenta="892C5A", ansiCyan="1D6B63",
)

FAMILY = "Kalamkari"
BLURB = ("Indian hand-painted textiles and their natural dyes: madder keywords, indigo types, myrobalan "
         "methods and overdyed-green strings on a vat of indigo or unbleached cotton, outlined in iron-black ink.")
THEMES = [
    dict(slug="KalamkariIndigo", id="38228301-5b31-4f08-b600-6a8b54623b39", palette=INDIGO),
    dict(slug="KalamkariCotton", id="58015413-fe1b-41a3-9df8-34ecc477def0", palette=COTTON),
]
