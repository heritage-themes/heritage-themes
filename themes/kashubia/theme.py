"""Kashubia palettes. See heritage/__init__.py for what a theme.py defines."""

# Kashubia: the seven colours of Kashubian embroidery (haft kaszubski) as fixed by the Żukowo school.
# Three blues lead, as they always do in Żukowo work: chabrowy (cornflower, the lakes) keywords,
# granatowy (navy, the sea) types, jasny niebieski (light blue, the sky) methods. Żółty (the sun and
# ripening grain) strings, zielony (forests and meadows) fields and type parameters, czerwony (the blood
# shed for the land) numbers, constants and Spock labels, amber (bursztyn) of the Baltic shore annotations,
# czarny (black, the earth) ground and text, with comments in the brown of the same earth.
# Zemia (earth) is the black soil waiting to be sown; Niebò (sky) is daylight on white linen
# (białe płótno), the cloth the embroidery is worked on.
ZEMIA = dict(
    name="Kashubia Zemia", dark=True, parent="Darcula", parentTheme="ExperimentalDark",
    bg="1C1814", bgUi="171410", bgTool="1A1612", surface="25201B", hover="2E2822",
    border="352E27", fg="EEE8DC", muted="9A9184", disabled="625A50",
    caretRow="231E19", selection="263A52", selInactive="2A3038", lineNo="5C5349", lineNoCaret="959FFF",
    guide="27221C", guideSel="403830",
    keyword="959FFF", string="E6C35C", number="F28B7A", type="52B0EA", method="AEE0FA", call="8EC8EC",
    field="92CC7E", constant="F28B7A", annotation="E3A062", label="FF9C88",
    comment="938575", doc="A3967E", docTag="C0B190", op="B8B0A4", param="EEE8DC", typeParam="C3DC8A",
    gold="E6C35C", red="3456B8", redText="F6F2EA", azure="7FB6F0", caret="959FFF",
    error="FF6B5E", warning="E8A33A", weak="8A7D5C",
    searchBg="4A3D16", searchBorder="E6C35C", underCaret="21354A", writeCaret="47261F",
    braceBg="25402C", todo="E6C35C",
    added="6FAE68", modified="5E98D6", deleted="C8605A",
    diffIns="1C3020", diffMod="1A2A3C", diffDel="3E211C", diffConf="3A3218", fileYellow="29241A",
    ansiRed="F07E70", ansiGreen="95D27E", ansiYellow="E6C35C", ansiBlue="7FB0F5", ansiMagenta="D795D8", ansiCyan="6DCFD8",
)
NIEBO = dict(
    name="Kashubia Niebò", dark=False, parent="Default", parentTheme="ExperimentalLight",
    bg="F5F2EA", bgUi="EAE6DA", bgTool="EFEBE1", surface="FBF9F4", hover="E0DBCD",
    border="D6D0C1", fg="1E1F24", muted="6C6860", disabled="A8A296",
    caretRow="EDE9DE", selection="D3DEEE", selInactive="E1E3E6", lineNo="A8A294", lineNoCaret="3045C4",
    guide="E5E1D5", guideSel="CBC4B3",
    keyword="3045C4", string="7A5C00", number="B0262C", type="1C4890", method="006C93", call="2C6A86",
    field="2D6B26", constant="B0262C", annotation="9A5410", label="A3201E",
    comment="7A6B58", doc="6E6040", docTag="54492F", op="55524C", param="1E1F24", typeParam="507810",
    gold="9A7400", red="26449E", redText="F7F4EC", azure="1F5BB0", caret="3045C4",
    error="C42020", warning="A86800", weak="A8955E",
    searchBg="F0DC8A", searchBorder="9A7400", underCaret="D4E2F0", writeCaret="F2D4CC",
    braceBg="D2E6CC", todo="8A5A00",
    added="5E9A50", modified="4F7FC0", deleted="C05050",
    diffIns="DDEACB", diffMod="D8E2EE", diffDel="F2D6CC", diffConf="EEE0B4", fileYellow="EFE8D4",
    ansiRed="A3201E", ansiGreen="2D6B26", ansiYellow="7A5800", ansiBlue="1F55A8", ansiMagenta="8E2A90", ansiCyan="0A6A78",
)

FAMILY = "Kashubia"
BLURB = ("The seven colours of Kashubian embroidery: cornflower keywords, navy types and light-blue methods "
         "under yellow strings, green fields and red numbers, on black earth or white linen.")
THEMES = [
    dict(slug="KashubiaZemia", id="dba31767-58f3-4b12-96ad-819305c6ab47", palette=ZEMIA),
    dict(slug="KashubiaNiebo", id="6b90b829-21ba-4232-950e-026a49eecf1f", palette=NIEBO),
]
