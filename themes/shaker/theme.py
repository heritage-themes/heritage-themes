"""Shaker palettes. See heritage/__init__.py for what a theme.py defines."""

# Shaker: the paint of the Shaker villages of the United States, chosen by what a thing was for. The Millennial
# Laws had the meetinghouse painted white outside and a bluish shade within; at Hancock its walls are white
# plaster and its woodwork Prussian blue. Dwellings were painted red, shops pumpkin ochre with dark green
# window frames, dwelling floors a reddish yellow, and bedsteads green; the paint at Canterbury includes verdigris
# and chrome green. The meetinghouse gives the keywords, set bold: plaster white on the Prussian blue woodwork,
# Prussian blue on the plaster. The rest of the village gives the names and literals: Shaker red strings,
# pumpkin method declarations and calls, yellow ochre fields, chrome green types and annotations, and
# verdigris numbers and constants. Prussian has the meetinghouse woodwork as its ground; Plaster has its walls.
PRUSSIAN = dict(
    name="Shaker Prussian", dark=True, parent="Darcula", parentTheme="ExperimentalDark", kwBold=True,
    bg="0F1C28", bgUi="0C1720", bgTool="0E1A25", surface="172634", hover="1F3040",
    border="283A4C", fg="B8BEC2", muted="909AA2", disabled="4E5C68",
    caretRow="162432", selection="2A4258", selInactive="203446", lineNo="4E6070", lineNoCaret="EEEAE0",
    guide="1A2A38", guideSel="34485A",
    keyword="EEEAE0", string="EE7462", number="6CC4AA", type="9CC872", method="F09A50", call="F2AC70",
    field="E8D06A", constant="6CC4AA", annotation="9CC872", label="EE7462",
    comment="6A7C8C", doc="7E909E", docTag="A2B2BE", op="98A2AA", param="B8BEC2", typeParam="C0DE9E",
    gold="E8D06A", red="B23A2A", redText="FFF4EE", azure="8AB4E0", caret="EEEAE0",
    error="FF6B5E", warning="E8A33A", weak="8A8460",
    searchBg="4A4012", searchBorder="E8D06A", underCaret="263C50", writeCaret="4A2622",
    braceBg="2E4A60", todo="E8D06A",
    added="7FB070", modified="6A9AD8", deleted="D0605A",
    diffIns="17291E", diffMod="182A40", diffDel="34191C", diffConf="342E16", fileYellow="13202C",
    ansiRed="F07E6E", ansiGreen="8CC878", ansiYellow="EECC5A", ansiBlue="82AEF0", ansiMagenta="DE8AD0", ansiCyan="6CCCD0",
)
PLASTER = dict(
    name="Shaker Plaster", dark=False, parent="Default", parentTheme="ExperimentalLight", kwBold=True,
    bg="F5F3EE", bgUi="EAE7E0", bgTool="F0EEE8", surface="FBFAF7", hover="E0DCD3",
    border="D5D0C5", fg="34302C", muted="66625C", disabled="ABA69C",
    caretRow="EEEBE4", selection="D4DEEA", selInactive="E4E2DC", lineNo="A8A398", lineNoCaret="1F3F7A",
    guide="E6E3DC", guideSel="CBC6BA",
    keyword="1F3F7A", string="B02A22", number="0E6E5A", type="2E6A1A", method="A85A00", call="9A4E10",
    field="856000", constant="0E6E5A", annotation="2E6A1A", label="B02A22",
    comment="7A766C", doc="66625A", docTag="48443E", op="5E5A54", param="34302C", typeParam="245414",
    gold="856000", red="B02A22", redText="FFF5F0", azure="1F5A9A", caret="1F3F7A",
    error="C42020", warning="905800", weak="A8955E",
    searchBg="F2DE94", searchBorder="856000", underCaret="D6E0EC", writeCaret="F2D6CE",
    braceBg="CCD8E6", todo="B02A22",
    added="5E9A50", modified="4F7FC0", deleted="C05050",
    diffIns="DDEACB", diffMod="D8E2EE", diffDel="F2D6D2", diffConf="EEE0B4", fileYellow="F0EEE8",
    ansiRed="A3201E", ansiGreen="2D6B26", ansiYellow="7A5800", ansiBlue="1F55A8", ansiMagenta="8E2A90", ansiCyan="0A6A78",
)

FAMILY = "Shaker"
BLURB = ("The paint of the Shaker villages: bold meetinghouse keywords in plaster white or Prussian blue, Shaker "
         "red strings, pumpkin methods, yellow ochre fields, chrome green types and verdigris numbers.")
THEMES = [
    dict(slug="ShakerPrussian", id="e4188b6f-960e-495d-a2d8-0f04cc945f7d", palette=PRUSSIAN),
    dict(slug="ShakerPlaster", id="fad91d55-3f74-46cc-8386-a6df67cb483e", palette=PLASTER),
]
