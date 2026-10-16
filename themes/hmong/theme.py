"""Hmong palettes. See heritage/__init__.py for what a theme.py defines."""

# Hmong: the pleated hemp skirt of the Blue, Green and Flower Hmong. Its middle band is batik (paj ntaub nraj
# ciab): beeswax lines resist the indigo, so the pattern stays white while repeated dips take the cloth from
# light blue to almost black. Bands of cross-stitch and appliqué (paj ntaub) in hot pink, lime green, orange
# and yellow frame it. Names take the tones of the batik: types the wax-resist line (white on the dark theme,
# the darkest indigo on the light one), method declarations and calls the light dip, fields a deeper dip.
# The cross-stitch adds the only colour: pink keywords, lime strings, orange numbers and constants, yellow
# annotations. Batik is the indigo-dyed band; Hemp is the undyed white hemp it is drawn on.
BATIK = dict(
    name="Hmong Batik", dark=True, parent="Darcula", parentTheme="ExperimentalDark",
    bg="111522", bgUi="0D111B", bgTool="0F131F", surface="181D2C", hover="202638",
    border="262D42", fg="C6CAD4", muted="878FA6", disabled="525A72",
    caretRow="171C2B", selection="283454", selInactive="222A40", lineNo="4A5370", lineNoCaret="FF85C2",
    guide="1A2030", guideSel="323B55",
    keyword="FF85C2", string="B8E06C", number="FFA45E", type="EFF1F7", method="9DB8F5", call="BBCDF7",
    field="7F98DA", constant="FFA45E", annotation="F2D152", label="FF85C2",
    comment="6C7794", doc="8590AE", docTag="A9B4D2", op="9AA2B8", param="C6CAD4", typeParam="D6DEF5",
    gold="F2D152", red="C21A6C", redText="FFF2F8", azure="9DB8F5", caret="FF85C2",
    error="FF6B6B", warning="E8A33A", weak="8A7D5C",
    searchBg="463C14", searchBorder="F2D152", underCaret="22305A", writeCaret="48203A",
    braceBg="2A3A62", todo="F2D152",
    added="6FAE68", modified="5E8EE0", deleted="C8605A",
    diffIns="1A2E22", diffMod="18243E", diffDel="3A1E2A", diffConf="36311A", fileYellow="1A1E28",
    ansiRed="F07E80", ansiGreen="98D47A", ansiYellow="F2D152", ansiBlue="86AEF5", ansiMagenta="E08ADA", ansiCyan="6DCFD8",
)
HEMP = dict(
    name="Hmong Hemp", dark=False, parent="Default", parentTheme="ExperimentalLight",
    bg="F2F0E9", bgUi="E7E4DB", bgTool="EEEBE3", surface="FAF9F4", hover="DFDBD0",
    border="D3CFC3", fg="302E2B", muted="68676A", disabled="A8A7A4",
    caretRow="EAE8E0", selection="D3DCF0", selInactive="E2E2E2", lineNo="A6A69E", lineNoCaret="AD1068",
    guide="E3E0D7", guideSel="C9C5BA",
    keyword="AD1068", string="3C780C", number="AE4A00", type="16245E", method="25489E", call="3253A8",
    field="5368A6", constant="AE4A00", annotation="7E5E00", label="AD1068",
    comment="767A88", doc="636A80", docTag="474F6C", op="55565E", param="302E2B", typeParam="2F3F80",
    gold="9A7400", red="AD1068", redText="FFF4F9", azure="25489E", caret="AD1068",
    error="C42020", warning="9A5F00", weak="A8955E",
    searchBg="F4E08C", searchBorder="9A7400", underCaret="D6E0F4", writeCaret="F6D4E4",
    braceBg="CFDAF2", todo="AD1068",
    added="5E9A50", modified="4F7FC0", deleted="C05050",
    diffIns="DDEACB", diffMod="D8E2EE", diffDel="F2D6DC", diffConf="EEE0B4", fileYellow="ECE9DF",
    ansiRed="A3201E", ansiGreen="2D6B26", ansiYellow="7A5800", ansiBlue="1F55A8", ansiMagenta="8E2A90", ansiCyan="0A6A78",
)

FAMILY = "Hmong"
BLURB = ("The batik and cross-stitch of the Hmong pleated skirt: names in the tones of indigo batik, with "
         "pink keywords, lime strings and orange numbers from the cross-stitch, on indigo or undyed hemp.")
THEMES = [
    dict(slug="HmongBatik", id="fc59d76d-60ad-47de-bef7-fe865ceb6046", palette=BATIK),
    dict(slug="HmongHemp", id="b5d1f012-0790-4e64-b599-9af562ec2bc4", palette=HEMP),
]
