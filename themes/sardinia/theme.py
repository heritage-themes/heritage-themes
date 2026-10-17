"""Sardinia palettes. See heritage/__init__.py for what a theme.py defines."""

# Sardinia: the traditional dress of the Sardinian villages, black orbace and white linen with scarlet and saffron.
# Orbace is the island's fulled, hand-woven wool, mostly black or dyed scarlet with robbia (madder); the silk of
# Orgosolo's su lionzu headscarf is dyed with zafferano (saffron); indaco (indigo) dyes the skirt of Bosa and
# Desulo embroiders in red, yellow and blue. Zafferano keywords, scarlatto (scarlet orbace) strings,
# indaco (indigo, and the blue satin of the Desulo bonnet) methods, mallo di noce (walnut husk, the brown dye
# and the brown orbace) fields, corallo (red coral of the island's jewellery) numbers, constants and annotations,
# and the cloth itself for types: white linen on the dark theme, black orbace on the light one.
# Orbace is the black wool of the cloaks and skirts; Camisa is sa camisa, the white linen shirt.
ORBACE = dict(
    name="Sardinia Orbace", dark=True, parent="Darcula",
    bg="1A1817", bgUi="151312", bgTool="181615", frame="2D2925", surface="23201E", hover="2C2826",
    border="34302C", fg="D3CCC1", muted="978E82", disabled="5E5852",
    caretRow="23201E", selection="2C3854", selInactive="2B2A2E", lineNo="5B544D", lineNoCaret="F0B23E",
    guide="252220", guideSel="3C3733",
    keyword="F0B23E", string="EE6B5B", number="F4A38F", type="F2EEE6", method="8EADF2", call="AFC5F2",
    field="C2A68C", constant="F4A38F", annotation="F4A38F", label="F0B23E",
    comment="857D72", doc="9B9284", docTag="C2B6A4", op="ADA69B", param="D3CCC1", typeParam="F2D49A",
    gold="F0B23E", red="B42A1E", redText="FBF5EA", azure="8EADF2", caret="F0B23E",
    error="FF6B5E", warning="E8A33A", weak="8A7D5C",
    searchBg="4A3A14", searchBorder="F0B23E", underCaret="22304A", writeCaret="47241F",
    braceBg="283752", todo="F0B23E",
    added="6FAE68", modified="5E98D6", deleted="C8605A",
    diffIns="1C3020", diffMod="1A2A3C", diffDel="3E211C", diffConf="3A3218", fileYellow="211E1A",
    ansiRed="F07E70", ansiGreen="95D27E", ansiYellow="F0B23E", ansiBlue="7FB0F5", ansiMagenta="D795D8", ansiCyan="6DCFD8",
)
CAMISA = dict(
    name="Sardinia Camisa", dark=False, parent="Default",
    bg="F7F4EC", bgUi="ECE8DD", bgTool="F2EEE5", frame="DED8CA", surface="FCFAF5", hover="E4DED1",
    border="D9D2C4", fg="2B2724", muted="6E675E", disabled="ABA498",
    caretRow="F0ECE2", selection="D6E0F2", selInactive="E6E2DA", lineNo="AAA396", lineNoCaret="8A5600",
    guide="E7E2D7", guideSel="CDC5B5",
    keyword="8A5600", string="B0261C", number="A3365A", type="141210", method="1F4A9C", call="34599E",
    field="734634", constant="A3365A", annotation="A3365A", label="8A5600",
    comment="847C70", doc="6E6450", docTag="524A38", op="57514A", param="2B2724", typeParam="6E4E00",
    gold="9A6A00", red="A41E14", redText="FBF6EC", azure="1F4A9C", caret="8A5600",
    error="C42020", warning="A86800", weak="A8955E",
    searchBg="F2DC8A", searchBorder="9A6A00", underCaret="D4E0F2", writeCaret="F2D4CC",
    braceBg="D0DCF0", todo="8A5600",
    added="5E9A50", modified="4F7FC0", deleted="C05050",
    diffIns="DDEACB", diffMod="D8E2EE", diffDel="F2D6D4", diffConf="EEE0B4", fileYellow="EFEADC",
    ansiRed="A3201E", ansiGreen="2D6B26", ansiYellow="7A5800", ansiBlue="1F55A8", ansiMagenta="8E2A90", ansiCyan="0A6A78",
)

FAMILY = "Sardinia"
BLURB = ("The traditional dress of Sardinia: saffron keywords and scarlet strings from the dyed silk and wool, "
         "indigo methods, walnut-brown fields and coral numbers, on black orbace or white linen.")
THEMES = [
    dict(slug="SardiniaOrbace", id="967cabaa-d995-4cb5-b29f-83a8c55d06c4", palette=ORBACE),
    dict(slug="SardiniaCamisa", id="3ca63e63-1b62-4848-a55c-623ff8eb9b6c", palette=CAMISA),
]
