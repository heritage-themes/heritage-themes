"""Kalamkari palettes. See heritage/__init__.py for what a theme.py defines."""

# Kalamkari (कलमकारी, "pen work"): cotton hand-painted with a bamboo kalam and natural dyes,
# as in Srikalahasti and Machilipatnam. Every colour is a dye the craft uses, kept as muted as the dyes:
# madder-over-indigo aubergine keywords, neel indigo types, chay (madder root) red methods with
# alum-madder rose calls, myrobalan (harad) yellow strings, catechu (kattha) brown numbers,
# indigo-over-myrobalan green fields, iron-saddened myrobalan olive constants,
# indigo-wash teal annotations. The canvas is a vat of indigo or unbleached cotton;
# text is kasimi, the iron-black outline ink. Spock labels are bold madder red.
INDIGO = dict(
    name="Kalamkari Indigo", dark=True, parent="Darcula", parentTheme="ExperimentalDark",
    bg="141C34", bgUi="11182D", bgTool="131A30", surface="1B243F", hover="222C4B",
    border="253152", fg="EDE3CF", muted="878DA2", disabled="565F7E",
    caretRow="18213D", selection="2C3B5E", selInactive="232E50", lineNo="485477", lineNoCaret="EE7A63",
    guide="1E2742", guideSel="364267",
    keyword="E3A6DD", string="E2C97D", number="D09B77", type="A7BAFF", method="F69C8D", call="F9BDB7",
    field="9BCE90", constant="A5A976", annotation="96DCE4", label="F69C8D",
    comment="7B8299", doc="9A9180", docTag="B6AB92", op="ADAAA6", param="EDE3CF", typeParam="A0E1CE",
    gold="EAB84A", red="A8402F", redText="F6ECD8", azure="93AAEB", caret="EAB84A",
    error="F2556B", warning="E5A33C", weak="877D5A",
    searchBg="48401C", searchBorder="EAB84A", underCaret="27375A", writeCaret="4A2A2E",
    braceBg="2C4A44", todo="EAB84A",
    added="6A9E64", modified="5E82C8", deleted="B0544A",
    diffIns="1A2E2A", diffMod="1B2645", diffDel="36202A", diffConf="35301E", fileYellow="262A30",
    ansiRed="EE7A63", ansiGreen="A9C47F", ansiYellow="EAC46A", ansiBlue="93AAEB", ansiMagenta="DE8FB0", ansiCyan="6EC6B6",
)
COTTON = dict(
    name="Kalamkari Cotton", dark=False, parent="Default", parentTheme="ExperimentalLight",
    bg="F0E6CC", bgUi="E6DABC", bgTool="EBE0C4", surface="F6EED9", hover="DDCFAE",
    border="D4C5A2", fg="2A2218", muted="6C6252", disabled="A69879",
    caretRow="E8DCBE", selection="CBD5EA", selInactive="DCD8C7", lineNo="A3936F", lineNoCaret="A3301F",
    guide="DFD2B3", guideSel="C7B58E",
    keyword="864A81", string="786101", number="77441D", type="4E5EA2", method="9C4437", call="905752",
    field="3E7232", constant="494B12", annotation="1C7078", label="963E32",
    comment="776D5B", doc="6A5E3F", docTag="564B2F", op="595145", param="2A2218", typeParam="297161",
    gold="B07D12", red="A3301F", redText="F8EFDE", azure="27408A", caret="A3301F",
    error="C42032", warning="A86A00", weak="A8955E",
    searchBg="EDD28A", searchBorder="B07D12", underCaret="D2DBEE", writeCaret="F0D0C6",
    braceBg="CFE0C8", todo="745200",
    added="5E9450", modified="4F6FB0", deleted="B8503E",
    diffIns="DCE8CF", diffMod="D8DFEF", diffDel="F2D6CC", diffConf="EEE0BA", fileYellow="EEDEB1",
    ansiRed="A3301F", ansiGreen="46672A", ansiYellow="745200", ansiBlue="27408A", ansiMagenta="892C5A", ansiCyan="1D6B63",
)

FAMILY = "Kalamkari"
BLURB = ("Indian hand-painted textiles and their natural dyes, kept muted: aubergine keywords, indigo types, "
         "madder methods and myrobalan strings on a vat of indigo or unbleached cotton, outlined in iron-black ink.")
THEMES = [
    dict(slug="KalamkariIndigo", id="38228301-5b31-4f08-b600-6a8b54623b39", palette=INDIGO),
    dict(slug="KalamkariCotton", id="58015413-fe1b-41a3-9df8-34ecc477def0", palette=COTTON),
]
