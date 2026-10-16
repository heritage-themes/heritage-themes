"""Holi palettes. See heritage/__init__.py for what a theme.py defines."""

# Holi (होली), the festival of colours, by night and by day:
# Holika Dahan, the bonfire eve, is ash and embers; Rangwali Holi, the day after, is gulal powder
# thrown over white cotton. Each syntax role takes one powder:
# gulabi pink keywords, haldi turmeric methods, hara green strings, neela blue types,
# kesari saffron numbers, jamuni purple fields, indigo constants, firozi turquoise annotations.
# Ember orange marks the caret; Spock labels are turmeric.
NIGHT = dict(
    name="Holi Night", dark=True, parent="Darcula", parentTheme="ExperimentalDark",
    bg="1C1A1F", bgUi="17151A", bgTool="1A181D", surface="25222A", hover="2D2933",
    border="2F2B35", fg="ECE4DA", muted="8E8792", disabled="5E5863",
    caretRow="221F27", selection="3B2D46", selInactive="2F2937", lineNo="524C58", lineNoCaret="FF8A3D",
    guide="27242C", guideSel="403A48",
    keyword="F2669C", string="93D38C", number="FF9F5A", type="72AAF6", method="F5C842", call="E6CF8C",
    field="C69CF0", constant="9D93F7", annotation="4FD0C2", label="FFD45C",
    comment="7F7886", doc="A08F80", docTag="BCA78F", op="B6AEB7", param="ECE4DA", typeParam="7FD8E2",
    gold="F5C842", red="C9356E", redText="FFF4EC", azure="72AAF6", caret="FF8A3D",
    error="FF5468", warning="F5A623", weak="8C7B55",
    searchBg="4A3A12", searchBorder="F5C842", underCaret="2B3552", writeCaret="4C2334",
    braceBg="2E4A3B", todo="F5C842",
    added="5FAE6A", modified="5C8FD6", deleted="C0506A",
    diffIns="1F3024", diffMod="1E2639", diffDel="3B1E29", diffConf="3A311C", fileYellow="2C251A",
    ansiRed="FF5468", ansiGreen="93D38C", ansiYellow="F5C842", ansiBlue="72AAF6", ansiMagenta="F2669C", ansiCyan="4FD0C2",
)
DAY = dict(
    name="Holi Day", dark=False, parent="Default", parentTheme="ExperimentalLight",
    bg="FAF7F2", bgUi="F0EBE3", bgTool="F5F1EA", surface="FFFDF9", hover="E8E1D7",
    border="DED6CA", fg="2A2430", muted="736B77", disabled="ACA4AE",
    caretRow="F3EDE4", selection="F4D3E2", selInactive="ECE2E7", lineNo="B0A7AE", lineNoCaret="C2185B",
    guide="EBE4DA", guideSel="D3C8BB",
    keyword="C2185B", string="2E7A32", number="B4460C", type="1A5FB4", method="855800", call="74580F",
    field="8236A8", constant="4338A8", annotation="00756A", label="6E4A00",
    comment="7D7580", doc="7A6650", docTag="5F4D38", op="5B5560", param="2A2430", typeParam="0E6F8A",
    gold="D4A017", red="C2185B", redText="FFF6F9", azure="1A5FB4", caret="E0600F",
    error="D0213A", warning="B86A00", weak="B3A06A",
    searchBg="FBE29A", searchBorder="D4A017", underCaret="D9E4F5", writeCaret="F7D6E1",
    braceBg="CDEBCF", todo="855800",
    added="5FA866", modified="6A8FD0", deleted="D0617A",
    diffIns="E1F2DD", diffMod="DFE8F7", diffDel="F9DCE4", diffConf="F7EAC6", fileYellow="FAF0D3",
    ansiRed="D0213A", ansiGreen="2E7A32", ansiYellow="855800", ansiBlue="1A5FB4", ansiMagenta="C2185B", ansiCyan="00756A",
)

FAMILY = "Holi"
BLURB = ("The Indian festival of colours: gulabi-pink keywords, turmeric methods, green strings and "
         "blue types, thrown like gulal over the ash of the Holika bonfire or over white cotton.")
THEMES = [
    dict(slug="HoliNight", id="4ee35ddf-4a2d-4a84-8c43-77b05d0c9634", palette=NIGHT),
    dict(slug="HoliDay", id="5ad83549-5eab-48ed-9428-69910ffcc2b3", palette=DAY),
]
