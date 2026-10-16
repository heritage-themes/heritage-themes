"""Holi palettes. See heritage/__init__.py for what a theme.py defines."""

# Holi (होली), the festival of colours, by night and by day:
# Holika Dahan, the bonfire eve, is ash and embers; Rangwali Holi, the day after, is gulal powder
# thrown over white cotton. Each syntax role takes one powder at full strength:
# gulabi pink keywords, kesari saffron strings, haldi turmeric numbers, hara green types,
# neela blue methods, jamuni purple fields, firozi turquoise constants, lal red annotations.
# Ember orange marks the caret; Spock labels are turmeric.
NIGHT = dict(
    name="Holi Night", dark=True, parent="Darcula", parentTheme="ExperimentalDark",
    bg="1D1C1B", bgUi="181716", bgTool="1B1A19", surface="262426", hover="2E2B2F",
    border="302D31", fg="ECE4DA", muted="8E8792", disabled="5F5A5E",
    caretRow="232123", selection="3B2D46", selInactive="302B33", lineNo="534E53", lineNoCaret="FF8A3D",
    guide="282628", guideSel="413C44",
    keyword="FF98CA", string="FFA65F", number="E8CA17", type="61DC6B", method="96C0FE", call="A2CFFF",
    field="D1A9FF", constant="06D8D9", annotation="FF6971", label="E8CA17",
    comment="7F7886", doc="A08F80", docTag="BCA78F", op="B6AEB7", param="ECE4DA", typeParam="77E3B7",
    gold="F5C842", red="C9356E", redText="FFF4EC", azure="72AAF6", caret="FF8A3D",
    error="FF5468", warning="F5A623", weak="8C7B55",
    searchBg="4A3A12", searchBorder="F5C842", underCaret="2B3552", writeCaret="4C2334",
    braceBg="2E4A3B", todo="F5C842",
    added="5FAE6A", modified="5C8FD6", deleted="C0506A",
    diffIns="1F3024", diffMod="1E2639", diffDel="3B1E29", diffConf="3A311C", fileYellow="2D2714",
    ansiRed="FF5468", ansiGreen="93D38C", ansiYellow="F5C842", ansiBlue="72AAF6", ansiMagenta="F2669C", ansiCyan="4FD0C2",
)
DAY = dict(
    name="Holi Day", dark=False, parent="Default", parentTheme="ExperimentalLight",
    bg="FBF9F5", bgUi="F1EDE6", bgTool="F6F3ED", surface="FFFFFC", hover="E9E3DA",
    border="DFD8CD", fg="2A2430", muted="736B77", disabled="ADA6B1",
    caretRow="F4EFE7", selection="F4D3E2", selInactive="EDE4EA", lineNo="B1A9B1", lineNoCaret="C2185B",
    guide="ECE6DD", guideSel="D4CABE",
    keyword="B00373", string="944F02", number="6D5D01", type="01791E", method="005DC9", call="316CA5",
    field="7D3BB6", constant="086B6C", annotation="AB042B", label="665800",
    comment="7D7580", doc="7A6650", docTag="5F4D38", op="5B5560", param="2A2430", typeParam="036F4F",
    gold="D4A017", red="C2185B", redText="FFF6F9", azure="1A5FB4", caret="E0600F",
    error="D0213A", warning="B86A00", weak="B3A06A",
    searchBg="FBE29A", searchBorder="D4A017", underCaret="D9E4F5", writeCaret="F7D6E1",
    braceBg="CDEBCF", todo="855800",
    added="5FA866", modified="6A8FD0", deleted="D0617A",
    diffIns="E1F2DD", diffMod="DFE8F7", diffDel="F9DCE4", diffConf="F7EAC6", fileYellow="FBF2D6",
    ansiRed="D0213A", ansiGreen="2E7A32", ansiYellow="855800", ansiBlue="1A5FB4", ansiMagenta="C2185B", ansiCyan="00756A",
)

FAMILY = "Holi"
BLURB = ("The Indian festival of colours at full strength: gulabi-pink keywords, saffron strings, green types "
         "and blue methods, thrown like gulal over the ash of the Holika bonfire or over white cotton.")
THEMES = [
    dict(slug="HoliNight", id="4ee35ddf-4a2d-4a84-8c43-77b05d0c9634", palette=NIGHT),
    dict(slug="HoliDay", id="5ad83549-5eab-48ed-9428-69910ffcc2b3", palette=DAY),
]
