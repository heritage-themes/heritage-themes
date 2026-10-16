"""Peru palettes. See heritage/__init__.py for what a theme.py defines."""

# Peru: the natural dyes of Andean weaving, as practised in Chinchero and the Sacred Valley.
# Two dark themes, each dyed through: Kulli is kulli sara, the purple corn (maiz morado) of chicha
# morada; Puka is the crimson of cochineal (cochinilla), the insect dye of the prickly-pear cactus.
# Syntax colours are the other dyes and Quechua colour words: q'olle yellow, ch'illka green,
# anqas blue from tara and quinsa k'ucho, willapi orange, cochineal pink, the turquoise and ochre
# bands of Winikunka (Rainbow Mountain), and yuraq alpaca white for text and Spock labels.
# None repeats the background's own hue: no purple on Kulli, no red on Puka.
KULLI = dict(
    name="Peru Kulli", dark=True, parent="Darcula", parentTheme="ExperimentalDark",
    bg="480F50", bgUi="3A0842", bgTool="410C49", surface="531C5C", hover="5D2966",
    border="5F3466", fg="F8ECE0", muted="CAABCF", disabled="916A97",
    caretRow="501959", selection="374573", selInactive="393C5F", lineNo="A17EA6", lineNoCaret="F4D660",
    guide="4E1D55", guideSel="6B3F72",
    keyword="F4D660", string="A2E694", number="FCA0A7", type="89C8FE", method="FFB66D", call="FED6AD",
    field="74DFDB", constant="B4E7FC", annotation="BCC29E", label="FBF4EA",
    comment="B9A1BF", doc="C7AFC4", docTag="E1C8DE", op="D7C8DA", param="F8ECE0", typeParam="7CFFDB",
    gold="F4D660", red="F4D660", redText="370040", azure="89C8FE", caret="F4D660",
    error="FF7979", warning="FEB354", weak="B2A572",
    searchBg="503D00", searchBorder="F4D660", underCaret="1D3F60", writeCaret="642629",
    braceBg="005559", todo="F4D660",
    added="79C77C", modified="73B0EE", deleted="EF7E80",
    diffIns="074029", diffMod="1E3761", diffDel="5D192E", diffConf="4E3A06", fileYellow="4B1F34",
    ansiRed="FF7E76", ansiGreen="93E195", ansiYellow="F4D660", ansiBlue="80BDFB", ansiMagenta="F19FD6", ansiCyan="73DFDF",
)
PUKA = dict(
    name="Peru Puka", dark=True, parent="Darcula", parentTheme="ExperimentalDark",
    bg="720041", bgUi="610036", bgTool="6A003C", surface="7F124C", hover="8A2656",
    border="89365B", fg="F8ECE0", muted="D8A8B9", disabled="A0667D",
    caretRow="7C0D49", selection="475585", selInactive="494C70", lineNo="AF7B8E", lineNoCaret="97ED9A",
    guide="781949", guideSel="964267",
    keyword="97ED9A", string="F0E395", number="FFC184", type="99D1FF", method="7AE6E5", call="BFF0EF",
    field="D9B3FF", constant="58D8AE", annotation="B4C694", label="FBF4EA",
    comment="D3ABB9", doc="DDBABE", docTag="F4D0D5", op="E9D0D8", param="F8ECE0", typeParam="DCBB50",
    gold="97ED9A", red="97ED9A", redText="5F0031", azure="99D1FF", caret="97ED9A",
    error="FFA4A4", warning="FFC469", weak="BFB17E",
    searchBg="614D10", searchBorder="97ED9A", underCaret="2E5072", writeCaret="743B1F",
    braceBg="1D676A", todo="97ED9A",
    added="79C77C", modified="73B0EE", deleted="FDA1A0",
    diffIns="1C5038", diffMod="2D4772", diffDel="54002E", diffConf="5F4A1A", fileYellow="6C1B30",
    ansiRed="FF9E96", ansiGreen="97ED9A", ansiYellow="F4E382", ansiBlue="92C9FF", ansiMagenta="E8B6F3", ansiCyan="7AE6E5",
)

FAMILY = "Peru"
BLURB = ("Andean natural dyes on two dyed-through grounds: q'olle-yellow keywords, ch'illka-green strings and "
         "anqas-blue types on purple corn, and ch'illka-green keywords with turquoise methods on cochineal crimson.")
THEMES = [
    dict(slug="PeruKulli", id="f55eb5b3-1aee-4667-8ba0-8149e397e5c7", palette=KULLI),
    dict(slug="PeruPuka", id="0aec8b65-c5f0-4e71-bfa3-822cd77bb7df", palette=PUKA),
]
