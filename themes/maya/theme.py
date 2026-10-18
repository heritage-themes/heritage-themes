"""Maya palettes. See heritage/__init__.py for what a theme.py defines."""

# Maya: the backstrap-woven dress (traje) of the Maya towns of the Guatemalan highlands, where the huipil and the
# corte identify a woman's town. Brocade is woven in red, yellow, green and purple on a white cotton huipil; the
# corte is jaspe, cotton tie-dyed in añil (indigo). The colours are read through the K'iche' colour roads:
# kaq (red, the east), saq (white, the north), q'eq (black, the west), q'än (yellow, the south) and räx
# (green-blue, the centre, the road of life). Räx green keywords, kaq red strings, q'än yellow types, morado
# (purple) method declarations and calls, añil fields, and räx sky blue for numbers, constants and annotations.
# Corte is the indigo jaspe skirt; Huipil is the white cotton blouse.
CORTE = dict(
    name="Maya Corte (Dark)", dark=True, parent="Darcula",
    bg="13162A", bgUi="0F1222", bgTool="111426", frame="222742", surface="1A1E35", hover="232842",
    border="2B3150", fg="C8CADA", muted="888EAA", disabled="535973",
    caretRow="1A1E34", selection="2C3760", selInactive="242A44", lineNo="4C5374", lineNoCaret="62D29B",
    guide="1B1F35", guideSel="343B5C",
    keyword="62D29B", string="F2706E", number="6CC8F0", type="F0CF5C", method="C391F2", call="D2AEF5",
    field="8EA2F5", constant="6CC8F0", annotation="6CC8F0", label="62D29B",
    comment="6E7598", doc="8189AA", docTag="A5ACCB", op="9A9FB8", param="C8CADA", typeParam="F6DE8E",
    gold="F0CF5C", red="B8262E", redText="FFF2F0", azure="6CC8F0",
    error="FF6B6B", warning="E8A33A", weak="8A7D5C",
    searchBg="4A3E12", searchBorder="F0CF5C", underCaret="22305A", writeCaret="4A1E2A",
    braceBg="2E3E6A", todo="F0CF5C",
    added="6FAE68", modified="5E8EE0", deleted="C8605A",
    diffIns="1A2C26", diffMod="1C2440", diffDel="3A1C26", diffConf="36311A", fileYellow="181B2E",
    ansiRed="F07E70", ansiGreen="8CD47E", ansiYellow="F2CF5A", ansiBlue="7CB4F2", ansiMagenta="E08ADA", ansiCyan="6DCFD8",
)
HUIPIL = dict(
    name="Maya Huipil (Light)", dark=False, parent="Default",
    bg="F6F4EE", bgUi="EBE8E0", bgTool="F0EEE7", frame="DDD8CE", surface="FCFBF8", hover="E2DFD6",
    border="D5D1C6", fg="403E39", muted="615E57", disabled="A9A69E",
    caretRow="EDEBE4", selection="D2DCF2", selInactive="E2E2E4", lineNo="A8A59C", lineNoCaret="0E7A4E",
    guide="E5E3DB", guideSel="CAC6BC",
    keyword="0E7A4E", string="B3201F", number="0B6E9C", type="946000", method="7A35B0", call="8A4CBC",
    field="2A44A8", constant="0B6E9C", annotation="0B6E9C", label="0E7A4E",
    comment="7A776E", doc="66635B", docTag="4A4842", op="5E5C55", param="403E39", typeParam="7A5C14",
    gold="946000", red="A8201E", redText="FFF5F0", azure="0B6E9C", caret="A8201E",
    error="C42020", warning="9A5F00", weak="A8955E",
    searchBg="F4E08C", searchBorder="946000", underCaret="D6DEF4", writeCaret="F4D6D2",
    braceBg="C8D4F0", todo="A8201E",
    added="5E9A50", modified="4F7FC0", deleted="C05050",
    diffIns="DDEACB", diffMod="D8E2EE", diffDel="F2D6D2", diffConf="EEE0B4", fileYellow="EFEDE5",
    ansiRed="A3201E", ansiGreen="2D6B26", ansiYellow="7A5800", ansiBlue="1F55A8", ansiMagenta="8E2A90", ansiCyan="0A6A78",
)

FAMILY = "Maya"
BLURB = ("The town dress of the Guatemalan Maya read through the K'iche' colour roads: green keywords, red "
         "strings, yellow types, purple methods and indigo fields, on the jaspe corte or the white huipil.")
THEMES = [
    dict(slug="MayaCorte", id="24b13e6d-75b5-48f2-9095-e462962abb0d", palette=CORTE),
    dict(slug="MayaHuipil", id="727e84fe-aff0-4dbd-9bc9-339743512962", palette=HUIPIL),
]
