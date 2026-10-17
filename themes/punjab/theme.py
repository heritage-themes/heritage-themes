"""Punjab palettes. See heritage/__init__.py for what a theme.py defines."""

# Punjab: phulkari embroidery and the mustard fields of Basant.
# Phulkari is darning-stitch embroidery in floss silk (pat) on handspun khaddar, here dyed a deep
# madder rust; Basant is the spring festival when the sarson (mustard) fields flower yellow.
# Golden and orange silk lead, as in bagh phulkari: sunehri golden-silk keywords,
# santri orange-silk methods, firozi turquoise strings (the paranda hair tassel),
# sarson-saag green types, neela blue-silk numbers, gulabi magenta-silk fields,
# jamni purple-silk constants, lal crimson-silk annotations, asmani sky-blue type parameters,
# chitta white-thread text. Spock labels are rose, like a paranda tassel,
# and the primary accent is the golden thread itself.
PHULKARI = dict(
    name="Punjab Phulkari (Dark)", dark=True, parent="Darcula",
    bg="241612", bgUi="1E120F", bgTool="211411", frame="3A251F", surface="2E1D18", hover="37241E",
    border="3A2620", fg="F4EBDD", muted="9A8B83", disabled="64554E",
    caretRow="2B1B16", selection="4A3324", selInactive="3A2A22", lineNo="5C4840", lineNoCaret="F7C548",
    guide="2E1D18", guideSel="4A362E",
    keyword="EAC33F", string="58D4D0", number="91C1FF", type="8BD47B", method="FF9A5F", call="F2B998",
    field="F999DA", constant="C9ACFF", annotation="FF9595", label="FB9DC2",
    comment="958780", doc="A8937C", docTag="C4AD8C", op="BBB0A8", param="F4EBDD", typeParam="A1DFF5",
    gold="F7C548", red="D9A21E", redText="241612", azure="7FA8F5", caret="F7C548",
    error="FF5468", warning="F5A93A", weak="8C7B58",
    searchBg="4D3D16", searchBorder="F7C548", underCaret="2E3550", writeCaret="4D2420",
    braceBg="33482E", todo="F7C548",
    added="6BAA5E", modified="6A8FD8", deleted="C8564A",
    diffIns="203020", diffMod="222640", diffDel="3E1C1C", diffConf="3E3218", fileYellow="322413",
    ansiRed="FF7A72", ansiGreen="9ED46A", ansiYellow="F7C548", ansiBlue="7FA8F5", ansiMagenta="F08AC8", ansiCyan="4FD0C8",
)
BASANT = dict(
    name="Punjab Basant (Light)", dark=False, parent="Default",
    bg="F8F1D2", bgUi="E6E9C9", bgTool="EDEDD2", frame="C9DCBB", surface="FDF8E2", hover="DBDFBA",
    border="D0D5AC", fg="22241A", muted="666A55", disabled="A1A285",
    caretRow="F1E9C5", selection="D6E4F5", selInactive="E2E2D0", lineNo="A6A281", lineNoCaret="7A5200",
    guide="EAE3C2", guideSel="CDCFA4",
    keyword="6E5803", string="047270", number="1E63B2", type="27770D", method="A44C03", call="975F3C",
    field="99377E", constant="714CA7", annotation="AD2C3A", label="9A3D67",
    comment="73705C", doc="6E6040", docTag="564A2E", op="55564A", param="22241A", typeParam="2E748A",
    gold="B08A10", red="8A6300", redText="FFFCEC", azure="1F55A8", caret="B04600",
    error="C41A2A", warning="A86A00", weak="A8955E",
    searchBg="F0CF66", searchBorder="B08A10", underCaret="D6E4F5", writeCaret="F5D5CF",
    braceBg="CDE6C2", todo="7A5200",
    added="5E9A50", modified="4F7FC0", deleted="C05050",
    diffIns="E0EDCC", diffMod="DCE6F2", diffDel="F5DCD2", diffConf="F2E4B4", fileYellow="F4E4A9",
    ansiRed="B0202E", ansiGreen="3A7018", ansiYellow="7A5200", ansiBlue="1F55A8", ansiMagenta="A3207A", ansiCyan="00756E",
)

FAMILY = "Punjab"
BLURB = ("Punjab's phulkari embroidery and Basant mustard fields: golden-silk keywords, orange-silk methods, "
         "turquoise strings and saag-green types, on madder-rust khaddar or a field of flowering mustard.")
THEMES = [
    dict(slug="PunjabPhulkari", id="afefce75-2071-465d-a55d-b6c485e97b1f", palette=PHULKARI),
    dict(slug="PunjabBasant", id="41989a12-7a91-4442-b3f3-2fb3c000f61d", palette=BASANT),
]
