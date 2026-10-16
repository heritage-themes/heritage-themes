"""Punjab palettes. See heritage/__init__.py for what a theme.py defines."""

# Punjab: phulkari embroidery and the mustard fields of Basant.
# Phulkari is darning-stitch embroidery in floss silk (pat) on handspun khaddar, here dyed a deep
# madder rust; Basant is the spring festival when the sarson (mustard) fields flower yellow.
# Syntax colours are the pat silks and the fields: sunehri golden-silk keywords,
# santri orange-silk methods, sarson-saag green strings, neela blue-silk types,
# lal crimson-silk numbers, gulabi magenta-silk fields, jamni purple-silk constants,
# firozi turquoise annotations (the parandi hair tassel), young-wheat type parameters,
# chitta white-thread text. Spock labels are rose, like a parandi tassel,
# and the primary accent is the golden thread itself.
PHULKARI = dict(
    name="Punjab Phulkari", dark=True, parent="Darcula", parentTheme="ExperimentalDark",
    bg="241612", bgUi="1E120F", bgTool="211411", surface="2E1D18", hover="37241E",
    border="3A2620", fg="F4EBDD", muted="9A8B83", disabled="64554E",
    caretRow="2B1B16", selection="4A3324", selInactive="3A2A22", lineNo="5C4840", lineNoCaret="F7C548",
    guide="2E1D18", guideSel="4A362E",
    keyword="F7C548", string="9ED46A", number="FF7A72", type="7FA8F5", method="FF9E4A", call="F2C49A",
    field="F08AC8", constant="B49CF5", annotation="4FD0C8", label="FF8FB0",
    comment="958780", doc="A8937C", docTag="C4AD8C", op="BBB0A8", param="F4EBDD", typeParam="C9D67A",
    gold="F7C548", red="D9A21E", redText="241612", azure="7FA8F5", caret="F7C548",
    error="FF5468", warning="F5A93A", weak="8C7B58",
    searchBg="4D3D16", searchBorder="F7C548", underCaret="2E3550", writeCaret="4D2420",
    braceBg="33482E", todo="F7C548",
    added="6BAA5E", modified="6A8FD8", deleted="C8564A",
    diffIns="203020", diffMod="222640", diffDel="3E1C1C", diffConf="3E3218", fileYellow="322413",
    ansiRed="FF7A72", ansiGreen="9ED46A", ansiYellow="F7C548", ansiBlue="7FA8F5", ansiMagenta="F08AC8", ansiCyan="4FD0C8",
)
BASANT = dict(
    name="Punjab Basant", dark=False, parent="Default", parentTheme="ExperimentalLight",
    bg="FAF5DC", bgUi="E8EDD3", bgTool="EFF1DC", surface="FFFCEC", hover="DDE3C4",
    border="D2D9B6", fg="22241A", muted="666A55", disabled="A3A68E",
    caretRow="F3EDCF", selection="D6E4F5", selInactive="E4E6DA", lineNo="A8A68A", lineNoCaret="7A5200",
    guide="ECE7CC", guideSel="CFD3AE",
    keyword="7A5200", string="3A7018", number="B0202E", type="1F55A8", method="B04600", call="8A4A1A",
    field="A3207A", constant="5A35A8", annotation="00756E", label="B0205A",
    comment="73705C", doc="6E6040", docTag="564A2E", op="55564A", param="22241A", typeParam="5E6A10",
    gold="B08A10", red="8A6300", redText="FFFCEC", azure="1F55A8", caret="B04600",
    error="C41A2A", warning="A86A00", weak="A8955E",
    searchBg="F0CF66", searchBorder="B08A10", underCaret="D6E4F5", writeCaret="F5D5CF",
    braceBg="CDE6C2", todo="7A5200",
    added="5E9A50", modified="4F7FC0", deleted="C05050",
    diffIns="E0EDCC", diffMod="DCE6F2", diffDel="F5DCD2", diffConf="F2E4B4", fileYellow="F6E8B3",
    ansiRed="B0202E", ansiGreen="3A7018", ansiYellow="7A5200", ansiBlue="1F55A8", ansiMagenta="A3207A", ansiCyan="00756E",
)

FAMILY = "Punjab"
BLURB = ("Punjab's phulkari embroidery and Basant mustard fields: golden-silk keywords, orange-silk methods, "
         "saag-green strings and blue-silk types, on madder-rust khaddar or a field of flowering mustard.")
THEMES = [
    dict(slug="PunjabPhulkari", id="afefce75-2071-465d-a55d-b6c485e97b1f", palette=PHULKARI),
    dict(slug="PunjabBasant", id="41989a12-7a91-4442-b3f3-2fb3c000f61d", palette=BASANT),
]
