"""Ndebele palettes. See heritage/__init__.py for what a theme.py defines."""

# Ndebele: the painted homesteads of the Ndzundza Ndebele of South Africa. Women paint geometric panels on a
# lime-washed white wall, draw a heavy black outline round every shape and fill it flat with colour: red and
# dark red (bomvu), yellow to gold (surulani), sky blue (hlaza kwesibhakabhaka), green (hlaza) and pink. The
# structure of the code is the outline: keywords are drawn in black (nzima) on the white wall, or in white
# (mhlophe) on the black ground, and set bold. The fills colour the names and literals: sky-blue types, green
# method declarations and calls, yellow strings, red fields, pink numbers, constants and annotations. Nzima has
# the black outline paint as its ground; Mhlophe has the white lime-wash.
NZIMA = dict(
    name="Ndebele Nzima (Dark)", dark=True, parent="Darcula", kwBold=True,
    bg="161615", bgUi="111110", bgTool="141413", frame="282824", surface="1E1E1C", hover="272725",
    border="30302D", fg="BDBBB3", muted="8A8880", disabled="565550",
    caretRow="1D1D1B", selection="2C3A4A", selInactive="262B32", lineNo="51504B", lineNoCaret="F07A68",
    guide="20201E", guideSel="3A3A36",
    keyword="F5F3EC", string="F2CF5A", number="F49AC6", type="7CC0F2", method="80CB78", call="A6DA9F",
    field="F07A68", constant="F49AC6", annotation="F49AC6", label="F5F3EC",
    comment="7F7D75", doc="8E8C84", docTag="AFADA5", op="A19F97", param="BDBBB3", typeParam="AAD6F6",
    gold="F2CF5A", red="B8302A", redText="FFF4EF", azure="7CC0F2", caret="F07A68",
    error="FF6B6B", warning="E8A33A", weak="8A7D5C",
    searchBg="4A3E12", searchBorder="F2CF5A", underCaret="1E3247", writeCaret="4A1F20",
    braceBg="2A4258", todo="F2CF5A",
    added="6FAE68", modified="5E8EE0", deleted="C8605A",
    diffIns="1B2C1E", diffMod="1A2636", diffDel="361C1E", diffConf="36311A", fileYellow="1C1C19",
    ansiRed="F07E70", ansiGreen="8CD47E", ansiYellow="F2CF5A", ansiBlue="7CB4F2", ansiMagenta="E08ADA", ansiCyan="6DCFD8",
)
MHLOPHE = dict(
    name="Ndebele Mhlophe (Light)", dark=False, parent="Default", kwBold=True,
    bg="F4F2EC", bgUi="E9E7E0", bgTool="EFEDE6", frame="D9D7CF", surface="FBFAF6", hover="E0DDD5",
    border="D4D1C8", fg="46453F", muted="6C6A64", disabled="A9A7A0",
    caretRow="ECEAE3", selection="CFDFF0", selInactive="E0E1E2", lineNo="A8A69E", lineNoCaret="B42A1E",
    guide="E4E2DA", guideSel="C9C6BD",
    keyword="141413", string="8A5E00", number="AE2E72", type="1662A6", method="22742A", call="3A7A3C",
    field="B42A1E", constant="AE2E72", annotation="AE2E72", label="141413",
    comment="78766E", doc="65635C", docTag="4A4943", op="5E5C56", param="46453F", typeParam="2C5C90",
    gold="8F6C00", red="A8241C", redText="FFF5F0", azure="1662A6", caret="B42A1E",
    error="C42020", warning="9A5F00", weak="A8955E",
    searchBg="F4E08C", searchBorder="8F6C00", underCaret="D4E2F2", writeCaret="F4D6D2",
    braceBg="C8DCF0", todo="B42A1E",
    added="5E9A50", modified="4F7FC0", deleted="C05050",
    diffIns="DDEACB", diffMod="D8E2EE", diffDel="F2D6D2", diffConf="EEE0B4", fileYellow="EEECE4",
    ansiRed="A3201E", ansiGreen="2D6B26", ansiYellow="7A5800", ansiBlue="1F55A8", ansiMagenta="8E2A90", ansiCyan="0A6A78",
)

FAMILY = "Ndebele"
BLURB = ("The painted walls of the Ndebele homestead: keywords drawn as the black outline, with sky-blue types, "
         "green methods, yellow strings and pink fields as the flat fills, on black paint or white lime-wash.")
THEMES = [
    dict(slug="NdebeleNzima", id="524b83b3-a3f1-46a9-9534-c184817a11b9", palette=NZIMA),
    dict(slug="NdebeleMhlophe", id="947e1560-5627-46f7-9506-b969ae7f1cab", palette=MHLOPHE),
]
