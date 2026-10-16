"""Wixárika palettes. See heritage/__init__.py for what a theme.py defines."""

# Wixárika: the yarn paintings (nierika) and beadwork of the Wixárika (Huichol) of the Sierra Madre Occidental,
# yarn and glass beads pressed into beeswax in saturated colours. The colours follow the five colours of maize,
# each tied to a point of the Wixárika world: taxawime (yellow, the east, Wirikuta, where the sun was born),
# yuawime (blue, the south, water and rain), ta+lawime (purple, the west), tuxame (white, the north, clouds)
# and tsayule (many colours, the centre). Red is the colour of the mother and of sacred places; green is
# hikuri, the peyote. Taxawime keywords, yuawime strings, ta+lawime fields, constants and numbers, red types,
# hikuri method declarations, calls and annotations. Haramara is the sea in the west, linked to black, where
# the sun sets; Wirikuta is the desert in the east, where it rises.
HARAMARA = dict(
    name="Wixárika Haramara", dark=True, parent="Darcula", parentTheme="ExperimentalDark",
    bg="121113", bgUi="0E0D0F", bgTool="100F11", surface="1B1A1D", hover="252428",
    border="2E2D32", fg="C4C2C8", muted="8A8890", disabled="56545A",
    caretRow="1B1A1D", selection="263650", selInactive="25282F", lineNo="504E55", lineNoCaret="F7D23E",
    guide="1F1E21", guideSel="3A393E",
    keyword="F7D23E", string="62AEFA", number="B592F7", type="F2607E", method="A8E04A", call="C2EB80",
    field="B592F7", constant="B592F7", annotation="C2EB80", label="F7D23E",
    comment="7A7882", doc="8C8A94", docTag="AEACB5", op="A09EA8", param="C4C2C8", typeParam="F79AAE",
    gold="F7D23E", red="C21E56", redText="FFF2F5", azure="62AEFA",
    error="FF6B6B", warning="E8A33A", weak="8A7D5C",
    searchBg="4A3E12", searchBorder="F7D23E", underCaret="1E2F47", writeCaret="4A1A28",
    braceBg="2A3F5C", todo="F7D23E",
    added="6FAE68", modified="5E8EE0", deleted="C8605A",
    diffIns="1B2C1E", diffMod="1A2636", diffDel="361C24", diffConf="36311A", fileYellow="1A191B",
    ansiRed="F07E70", ansiGreen="8CD47E", ansiYellow="F2CF5A", ansiBlue="7CB4F2", ansiMagenta="E08ADA", ansiCyan="6DCFD8",
)
WIRIKUTA = dict(
    name="Wixárika Wirikuta", dark=False, parent="Default", parentTheme="ExperimentalLight",
    bg="F5F1E6", bgUi="EAE5D8", bgTool="EFEBDF", surface="FBF9F3", hover="E2DDCF",
    border="D5CFBF", fg="3F3D38", muted="66625A", disabled="A9A498",
    caretRow="EEEADD", selection="CFDDF2", selInactive="E2E1DC", lineNo="A8A397", lineNoCaret="B0164F",
    guide="E5E0D3", guideSel="CBC5B5",
    keyword="946000", string="0F62C8", number="7A3FD0", type="C2185B", method="2F6800", call="457A08",
    field="7A3FD0", constant="7A3FD0", annotation="457A08", label="946000",
    comment="7E7A70", doc="6A665C", docTag="4D4A42", op="5E5B54", param="3F3D38", typeParam="A6304F",
    gold="946000", red="B0164F", redText="FFF4F7", azure="0F62C8", caret="B0164F",
    error="C42020", warning="9A5F00", weak="A8955E",
    searchBg="F4E08C", searchBorder="946000", underCaret="D4E2F2", writeCaret="F4D3DC",
    braceBg="C8DCF0", todo="B0164F",
    added="5E9A50", modified="4F7FC0", deleted="C05050",
    diffIns="DDEACB", diffMod="D8E2EE", diffDel="F2D6D8", diffConf="EEE0B4", fileYellow="EFEBDE",
    ansiRed="A3201E", ansiGreen="2D6B26", ansiYellow="7A5800", ansiBlue="1F55A8", ansiMagenta="8E2A90", ansiCyan="0A6A78",
)

FAMILY = "Wixárika"
BLURB = ("The yarn paintings and beadwork of the Wixárika (Huichol): the five colours of maize, with yellow "
         "keywords, blue strings, purple fields, red types and peyote-green methods, on the black of the western "
         "sea or the light of the eastern desert.")
THEMES = [
    dict(slug="WixarikaHaramara", id="c7e6c017-daa1-4023-ba6d-056d16bcd0ad", palette=HARAMARA),
    dict(slug="WixarikaWirikuta", id="2093f354-1dd1-43f1-806e-05d120021918", palette=WIRIKUTA),
]
