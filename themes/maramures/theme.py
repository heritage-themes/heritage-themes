"""Maramureș palettes. See heritage/__init__.py for what a theme.py defines."""

# Maramureș: the festive dress of northern Romania, white hemp (cânepă) worn with two woollen aprons (zadie)
# striped in black and a colour that marks the wearer's village and age. Girls wear black and pumpkin-flower
# yellow, married women black and red; some villages add thin stripes of blue. The flowered skirt (sumnă) that
# took over the aprons' role keeps the code: vivid flowers for unmarried women, paler ones after 35, a single
# dark colour (brown, dark blue, dark green) after 50, black with small flowers in old age. Waistcoats are brown
# leather. The apron gives the keywords and literals: married red keywords, pumpkin-flower strings, blue-stripe
# numbers and constants. The skirt gives the names: dark green types, the flowers of the sumnă for method
# declarations and calls, and the waistcoat leather for fields. Zadie has the black wool of the aprons as its
# ground; Cânepă has the white hemp of the shirt.
ZADIE = dict(
    name="Maramureș Zadie (Dark)", dark=True, parent="Darcula",
    bg="141312", bgUi="100F0E", bgTool="121110", frame="272622", surface="1C1B19", hover="252321",
    border="2D2A27", fg="C2BCB0", muted="958F85", disabled="56524C",
    caretRow="1C1A18", selection="38322C", selInactive="2A2622", lineNo="56514A", lineNoCaret="EE6A5E",
    guide="201E1C", guideSel="3A3632",
    keyword="EE6A5E", string="EBAA4C", number="88AAEA", type="7CBE8A", method="EE96B2", call="F2B0C6",
    field="C9A27C", constant="88AAEA", annotation="88AAEA", label="EE6A5E",
    comment="776F68", doc="898079", docTag="ACA398", op="9F988E", param="C2BCB0", typeParam="A8D8B2",
    gold="EBAA4C", red="B2302A", redText="FFF4EE", azure="88AAEA", caret="EBAA4C",
    error="FF6B5E", warning="E8A33A", weak="8A8460",
    searchBg="4A3A12", searchBorder="EBAA4C", underCaret="27303E", writeCaret="4A2622",
    braceBg="343C4E", todo="EBAA4C",
    added="7FB070", modified="6A9AD8", deleted="D0605A",
    diffIns="17291E", diffMod="182A40", diffDel="34191C", diffConf="342E16", fileYellow="191716",
    ansiRed="F07E6E", ansiGreen="8CC878", ansiYellow="EECC5A", ansiBlue="82AEF0", ansiMagenta="DE8AD0", ansiCyan="6CCCD0",
)
CANEPA = dict(
    name="Maramureș Cânepă (Light)", dark=False, parent="Default",
    bg="F2EEE4", bgUi="E8E2D6", bgTool="EEE9DE", frame="DCD3C5", surface="F9F7F1", hover="DFD9CB",
    border="D3CCBE", fg="2E2A26", muted="68625A", disabled="ACA598",
    caretRow="EBE6DA", selection="D8DCE6", selInactive="E4E0D6", lineNo="A8A194", lineNoCaret="B0261E",
    guide="E4DFD4", guideSel="CBC4B6",
    keyword="B0261E", string="9A5400", number="1F55A8", type="1E6634", method="A42E6E", call="963064",
    field="784E2C", constant="1F55A8", annotation="1F55A8", label="B0261E",
    comment="7E776E", doc="69625A", docTag="4A443E", op="605A52", param="2E2A26", typeParam="17512A",
    gold="9A5400", red="B0261E", redText="FFF5F0", azure="1F55A8", caret="B0261E",
    error="C42020", warning="905800", weak="A8955E",
    searchBg="F2DA98", searchBorder="9A5400", underCaret="D8E0EC", writeCaret="F2D6CE",
    braceBg="CCD6E6", todo="B0261E",
    added="5E9A50", modified="4F7FC0", deleted="C05050",
    diffIns="DDEACB", diffMod="D8E2EE", diffDel="F2D6D2", diffConf="EEE0B4", fileYellow="EEEAE0",
    ansiRed="A3201E", ansiGreen="2D6B26", ansiYellow="7A5800", ansiBlue="1F55A8", ansiMagenta="8E2A90", ansiCyan="0A6A78",
)

FAMILY = "Maramureș"
BLURB = ("The striped aprons and flowered skirts of Maramureș, coloured by age: married red keywords, "
         "pumpkin-flower strings, blue numbers, dark green types, rose methods and leather-brown fields.")
THEMES = [
    dict(slug="MaramuresZadie", id="30124136-21e7-4921-bc0e-0bd260ab19bf", palette=ZADIE),
    dict(slug="MaramuresCanepa", id="57e86876-9be3-44f4-8838-3eedcf0a9324", palette=CANEPA),
]
