"""Mudhif palettes. See heritage/__init__.py for what a theme.py defines."""

# Mudhif: the reed guest house of the Marsh Arabs (Ma'dan) of southern Iraq, a vault of bundled reed (qasab)
# arches covered in reed mats. Gertrude Bell called it "a perfectly regular and exquisitely constructed yellow
# tunnel", lit by a willow fire on the coffee hearth and "fading away into a golden gloom". Hierarchy comes from
# the tone and weight of one reed colour, not from hue: method declarations in the palest peeled reed, bold;
# keywords in the gold of the bundled arches; types in old amber reed; calls a stronger tone than the plain
# straw text, fields a deeper gold. Only two colours come from outside the hall: the green of new reed shoots
# for strings, and the willow fire for numbers, constants and Spock labels. Qir has the bitumen black of the
# tarred mashoof canoes as its ground; Qasab has the peeled reed.
QIR = dict(
    name="Mudhif Qir (Dark)", dark=True, parent="Darcula", kwBold=True,
    bg="17140E", bgUi="13100B", bgTool="15120D", frame="2B261D", surface="1F1B14", hover="28231A",
    border="2F2920", fg="C2B596", muted="978C72", disabled="554D3E",
    caretRow="1E1A13", selection="3A3220", selInactive="2C2619", lineNo="5A5140", lineNoCaret="E2B44A",
    guide="221E16", guideSel="3A3326",
    keyword="E2B44A", string="AAC46C", number="EC8250", type="D69A52", method="F4E8C6", call="E2D6B4",
    field="B39458", constant="EC8250", annotation="A8915E", label="EC8250",
    comment="776E5C", doc="877D68", docTag="ABA084", op="A09478", param="C2B596", typeParam="E8C080",
    gold="E2B44A", red="A8562A", redText="FFF4E6", azure="A8BCD0", caret="E2B44A",
    error="FF6B5E", warning="E8A33A", weak="8A8460",
    searchBg="4A3E14", searchBorder="E2B44A", underCaret="2E3226", writeCaret="4A2A1C",
    braceBg="3E3622", todo="EC8250",
    added="7FB070", modified="6A9AD8", deleted="D0605A",
    diffIns="1A2616", diffMod="1A2232", diffDel="33191A", diffConf="352C14", fileYellow="1B1811",
    ansiRed="F07E6E", ansiGreen="8CC878", ansiYellow="EECC5A", ansiBlue="82AEF0", ansiMagenta="DE8AD0", ansiCyan="6CCCD0",
)
QASAB = dict(
    name="Mudhif Qasab (Light)", dark=False, parent="Default", kwBold=True,
    bg="F4EEDC", bgUi="EAE2CC", bgTool="F0E9D5", frame="DED3B9", surface="FAF6EA", hover="E2D8BE",
    border="D6CBAE", fg="463C28", muted="665A40", disabled="ADA180",
    caretRow="EDE5CF", selection="E2D4A8", selInactive="E8DEC2", lineNo="AA9E80", lineNoCaret="7A5600",
    guide="E6DEC6", guideSel="CCC0A0",
    keyword="7A5600", string="3E6A12", number="B0461A", type="8A4A10", method="241A08", call="2E2614",
    field="6A5420", constant="B0461A", annotation="6E6040", label="B0461A",
    comment="887E66", doc="72684E", docTag="54492E", op="665C44", param="463C28", typeParam="6E3A0A",
    gold="7A5600", red="A8461A", redText="FFF6EC", azure="3A5E86", caret="7A5600",
    error="C42020", warning="905800", weak="A8955E",
    searchBg="EED690", searchBorder="7A5600", underCaret="E0DCC4", writeCaret="F2D8C8",
    braceBg="DCD0A8", todo="B0461A",
    added="5E9A50", modified="4F7FC0", deleted="C05050",
    diffIns="DFE8C6", diffMod="DCE0E2", diffDel="F2D8CC", diffConf="EEDDA8", fileYellow="F0E9D3",
    ansiRed="A3201E", ansiGreen="2D6B26", ansiYellow="7A5800", ansiBlue="1F55A8", ansiMagenta="8E2A90", ansiCyan="0A6A78",
)

FAMILY = "Mudhif"
BLURB = ("The reed guest house of the Marsh Arabs of Iraq: hierarchy from the tone and weight of reed gold, with "
         "green reed shoots for strings and the willow fire for numbers.")
THEMES = [
    dict(slug="MudhifQir", id="8bed8026-dbf9-45f8-8ac3-679bc2f387a5", palette=QIR),
    dict(slug="MudhifQasab", id="cbbec009-8a20-4082-a6b5-eb5ca71a8018", palette=QASAB),
]
