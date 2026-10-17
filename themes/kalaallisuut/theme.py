"""Kalaallisuut palettes. See heritage/__init__.py for what a theme.py defines."""

# Kalaallisuut: the West Greenlandic national dress, whose colours mark a woman's age and marital status, a
# custom credited to the Moravian missionaries. The anorak is pink for a girl at her confirmation, red once she
# is married and darker after children; married women and widows wear blue. Young women wear white kamiks,
# older women yellow or dark blue ones. Festive dress is black sealskin and white: the men's white anorak
# (qaqortumaartoq, "dressed in white") over black trousers. The bead collar has a central band of white, red
# and blue, edged with green. The life stages give the names and literals: red (aappaluttoq) keywords, the
# confirmation pink strings, yellow (sungaartoq) kamik numbers and constants, blue (tungujortoq) anorak types.
# Method declarations and calls take the green bead edging; fields take the black and white of festive
# dress, set against greyer plain text. Qernertoq ("black") has black sealskin as its ground; Qaqortoq ("white")
# has the white kamik.
QERNERTOQ = dict(
    name="Kalaallisuut Qernertoq", dark=True, parent="Darcula", parentTheme="ExperimentalDark",
    bg="13171C", bgUi="0F1317", bgTool="11151A", surface="1A1F26", hover="222831",
    border="2A313A", fg="A3AAB3", muted="8C939C", disabled="4C545E",
    caretRow="1A1F26", selection="2C3646", selInactive="222A36", lineNo="4E5762", lineNoCaret="F0F2F4",
    guide="1E242C", guideSel="343D48",
    keyword="EE6E6E", string="F2A6C6", number="E6C462", type="8AB2EE", method="8ED292", call="A6DCA8",
    field="EEF0F2", constant="E6C462", annotation="8AB2EE", label="EE6E6E",
    comment="68717C", doc="7A8591", docTag="A0AAB5", op="959DA7", param="A3AAB3", typeParam="B6CFF4",
    gold="E6C462", red="B8323A", redText="FFF2F2", azure="8AB2EE", caret="F2F3F5",
    error="FF6B6B", warning="E8A33A", weak="8A8460",
    searchBg="4A4012", searchBorder="E6C462", underCaret="263446", writeCaret="4A2228",
    braceBg="2E3E56", todo="E6C462",
    added="7FB070", modified="6A9AD8", deleted="D0605A",
    diffIns="17291E", diffMod="182A40", diffDel="34191C", diffConf="342E16", fileYellow="171C21",
    ansiRed="F07E7E", ansiGreen="8CC878", ansiYellow="EECC5A", ansiBlue="82AEF0", ansiMagenta="DE8AD0", ansiCyan="6CCCD0",
)
QAQORTOQ = dict(
    name="Kalaallisuut Qaqortoq", dark=False, parent="Default", parentTheme="ExperimentalLight",
    bg="F3F3F0", bgUi="E8E8E4", bgTool="EEEEEA", surface="FAFAF8", hover="DEDED8",
    border="D2D2CC", fg="43474E", muted="686C72", disabled="ACADA8",
    caretRow="ECECE8", selection="D4DCEA", selInactive="E2E3E2", lineNo="A8AAA6", lineNoCaret="B0222C",
    guide="E4E4E0", guideSel="CACAC4",
    keyword="B0222C", string="B33382", number="7E5E00", type="1F4E9E", method="1E6426", call="2A6E30",
    field="141619", constant="7E5E00", annotation="1F4E9E", label="B0222C",
    comment="7A7D82", doc="666A70", docTag="484C52", op="5C6066", param="43474E", typeParam="173E80",
    gold="7E5E00", red="B0222C", redText="FFF4F4", azure="1F55A8", caret="B0222C",
    error="C42020", warning="905800", weak="A8955E",
    searchBg="F2DE94", searchBorder="7E5E00", underCaret="D6E0EC", writeCaret="F2D6D6",
    braceBg="CCD8E6", todo="B0222C",
    added="5E9A50", modified="4F7FC0", deleted="C05050",
    diffIns="DDEACB", diffMod="D8E2EE", diffDel="F2D6D2", diffConf="EEE0B4", fileYellow="EEEEE8",
    ansiRed="A3201E", ansiGreen="2D6B26", ansiYellow="7A5800", ansiBlue="1F55A8", ansiMagenta="8E2A90", ansiCyan="0A6A78",
)

FAMILY = "Kalaallisuut"
BLURB = ("The West Greenlandic national dress and its colours for age and marital status: red keywords, "
         "confirmation pink strings, yellow kamik numbers, blue anorak types, green bead methods and "
         "black-and-white fields.")
THEMES = [
    dict(slug="KalaallisuutQernertoq", id="21837d5e-13c8-4007-953a-29105e8b83a6", palette=QERNERTOQ),
    dict(slug="KalaallisuutQaqortoq", id="cad5c910-8654-4ee8-875b-4878fc05e287", palette=QAQORTOQ),
]
