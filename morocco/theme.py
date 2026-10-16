"""Morocco palettes. See heritage/__init__.py for what a theme.py defines."""

# Morocco: three walls. Unlike the other families, which sit on near-neutral dark or cream
# backgrounds, each theme here is painted in a saturated Moroccan building colour:
# Majorelle is the ultramarine of Jacques Majorelle's Marrakech garden, with its yellow pots and cactus green;
# Marrakech is the red clay (pise) of the medina walls, against palm green and the turquoise of its doors;
# Zellige is the deep jade of glazed mosaic tile, with saffron, henna and cobalt in the pattern.
# Syntax colours are lightened so they hold 4.5:1 on these vivid grounds, and none repeats the
# background's own hue, which would vibrate or vanish. Spock labels are bold off-white, like whitewash.
MAJORELLE = dict(
    name="Morocco Majorelle", dark=True, parent="Darcula", parentTheme="ExperimentalDark",
    bg="161F66", bgUi="101757", bgTool="131B5E", surface="212C80", hover="2A3796",
    border="2F3C94", fg="F4EEDD", muted="9AA4E0", disabled="6471BC",
    caretRow="1B2677", selection="2C3B92", selInactive="2D3A93", lineNo="7581CC", lineNoCaret="F6C945",
    guide="1E2873", guideSel="3C4CAA",
    keyword="F6C945", string="86E0A0", number="FFA866", type="FF9A7C", method="4FE0D4", call="9FE9E2",
    field="D6A6F5", constant="A9BDFF", annotation="FF8FBF", label="FAF7EF",
    comment="98A3E0", doc="B8B4DA", docTag="CEC8E6", op="BFC6EE", param="F4EEDD", typeParam="D4E57A",
    gold="F6C945", red="F6C945", redText="161F66", azure="8FB0FF", caret="F6C945",
    error="FF6B7E", warning="F6A93B", weak="B0A25C",
    searchBg="4E4323", searchBorder="F6C945", underCaret="28399B", writeCaret="5A2750",
    braceBg="224760", todo="F6C945",
    added="5FBF86", modified="6A8FFF", deleted="E0607A",
    diffIns="1A4A55", diffMod="27399B", diffDel="5A2150", diffConf="4A4428", fileYellow="2A2C4F",
    ansiRed="FF7A8A", ansiGreen="86E0A0", ansiYellow="F6C945", ansiBlue="8FB0FF", ansiMagenta="FF8FBF", ansiCyan="4FE0D4",
)
MARRAKECH = dict(
    name="Morocco Marrakech", dark=True, parent="Darcula", parentTheme="ExperimentalDark",
    bg="4F1D14", bgUi="3F160E", bgTool="47190F", surface="63291C", hover="72321F",
    border="7A3A28", fg="F7EDDE", muted="D0A593", disabled="9A6C5A",
    caretRow="5A2218", selection="374A50", selInactive="4A4649", lineNo="B07C68", lineNoCaret="FFD84D",
    guide="5C2A1E", guideSel="8A4E3A",
    keyword="5FDDD2", string="A6E6A0", number="FFA97A", type="8FB8FF", method="FFD84D", call="EFD08C",
    field="F5A3C0", constant="C9B2FF", annotation="D2EE6A", label="FAF7EF",
    comment="C79C8A", doc="D2B49A", docTag="E0C8AE", op="D8BFB0", param="F7EDDE", typeParam="7FD6F0",
    gold="FFD84D", red="5FDDD2", redText="3F160E", azure="8FC6FF", caret="FFD84D",
    error="FF7B8E", warning="FFB040", weak="B8A060",
    searchBg="53460A", searchBorder="FFD84D", underCaret="314B52", writeCaret="7A2A2E",
    braceBg="364D36", todo="FFD84D",
    added="6FC27A", modified="6FA8E8", deleted="F07A7A",
    diffIns="2C4A2A", diffMod="24465E", diffDel="7A2424", diffConf="574401", fileYellow="502B10",
    ansiRed="FFA0A0", ansiGreen="A6E6A0", ansiYellow="FFD84D", ansiBlue="8FC6FF", ansiMagenta="F5A3C0", ansiCyan="5FDDD2",
)
ZELLIGE = dict(
    name="Morocco Zellige", dark=True, parent="Darcula", parentTheme="ExperimentalDark",
    bg="0A4036", bgUi="062F25", bgTool="07372B", surface="115144", hover="186050",
    border="1D6656", fg="F1F0E3", muted="97CDBE", disabled="5E9A89",
    caretRow="0F4B3E", selection="35466E", selInactive="39485D", lineNo="6AA898", lineNoCaret="FFE27A",
    guide="0F4A3D", guideSel="2A7864",
    keyword="FFA48C", string="6EE3DA", number="FFAA6A", type="93B8FF", method="FFE27A", call="ECD68A",
    field="D2A8F2", constant="C4F2B8", annotation="FF9EC4", label="FAF7EF",
    comment="86BFB0", doc="A9C9B8", docTag="C2DAC8", op="B5D8CD", param="F1F0E3", typeParam="E8D27A",
    gold="FFE27A", red="FFA48C", redText="063327", azure="8FC6FF", caret="FFE27A",
    error="FF7B8E", warning="FFB040", weak="B8A868",
    searchBg="534613", searchBorder="FFE27A", underCaret="184C66", writeCaret="6A2A34",
    braceBg="4E3F69", todo="FFE27A",
    added="6FD08A", modified="6FA8F0", deleted="F07A8A",
    diffIns="073014", diffMod="324961", diffDel="6A2A34", diffConf="544527", fileYellow="24422A",
    ansiRed="FFA48C", ansiGreen="9EEBA8", ansiYellow="FFE27A", ansiBlue="93B8FF", ansiMagenta="F5A3D0", ansiCyan="6EE3DA",
)

FAMILY = "Morocco"
BLURB = ("Three Moroccan walls on saturated backgrounds: Majorelle ultramarine with yellow pots, "
         "Marrakech red clay with turquoise doors, and zellige jade with saffron and cobalt tile.")
THEMES = [
    dict(slug="MoroccoMajorelle", id="7410eb88-9e01-4890-b63b-8e880915cd40", palette=MAJORELLE),
    dict(slug="MoroccoMarrakech", id="7c6a0584-934c-4228-8a68-d6f24db2a686", palette=MARRAKECH),
    dict(slug="MoroccoZellige", id="5e37ba01-17de-4a5c-a825-10f32a9c4405", palette=ZELLIGE),
]
