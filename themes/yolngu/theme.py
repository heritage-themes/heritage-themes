"""Yolŋu palettes. See heritage/__init__.py for what a theme.py defines."""

# Yolŋu: the bark painting of north-east Arnhem Land. Pigments are ground from rock on a stone with water and
# fixative: miku' (dark red ochre), gangul (dark yellow ochre), galaŋarr' (yellowish-red clay), ratjpa
# (reddish-brown to purple haematite), gapaṉ (white clay) and gurrŋan' (charcoal black). Guwarguwarmirri, pure
# ochres mixed, gives pinks. Fine cross-hatching makes the surface bir'yun (shimmering). Miny'tji, the ancestral
# designs, belong to clans, so only the colours are used. Miku' red keywords, gangul yellow strings, galaŋarr'
# orange types, ratjpa fields, guwarguwarmirri pink numbers, constants and annotations, and method declarations
# and calls in the brightest mark: gapaṉ on the dark bark, gurrŋan' on the white clay. Every hue stays within
# the ochres. Galawu is the stringybark sheet painted on; Gapaṉ is the white clay ground.
GALAWU = dict(
    name="Yolŋu Galawu (Dark)", dark=True, parent="Darcula",
    bg="1F1712", bgUi="19120E", bgTool="1C1510", frame="34271E", surface="291F18", hover="33281F",
    border="3E3127", fg="AC9F90", muted="9B8E7E", disabled="5E5348",
    caretRow="281E17", selection="493326", selInactive="382A20", lineNo="5E5045", lineNoCaret="E25C4A",
    guide="291F18", guideSel="4A3C30",
    keyword="E25C4A", string="EAD072", number="F2A79C", type="F4A652", method="F8F2E6", call="EDE4D3",
    field="CF8FB4", constant="F2A79C", annotation="F2A79C", label="E25C4A",
    comment="85786A", doc="978A7A", docTag="B8AA98", op="A89C8E", param="AC9F90", typeParam="F6BE8A",
    gold="EAD072", red="B5402A", redText="FFF4EE", azure="F4A652",
    error="FF6B5E", warning="E8A33A", weak="8A7D5C",
    searchBg="4C3402", searchBorder="EAD072", underCaret="3C2E25", writeCaret="4E2620",
    braceBg="4E3A2A", todo="EAD072",
    added="7FAE60", modified="6A90C8", deleted="C8605A",
    diffIns="1F2A18", diffMod="1E2432", diffDel="3A1A18", diffConf="3A3018", fileYellow="241B15",
    ansiRed="F07E6E", ansiGreen="8CC878", ansiYellow="F0CC5A", ansiBlue="82AEF0", ansiMagenta="DE8AD0", ansiCyan="6CCCD0",
)
GAPAN = dict(
    name="Yolŋu Gapaṉ (Light)", dark=False, parent="Default",
    bg="F1EDE5", bgUi="E6E1D7", bgTool="ECE8DF", frame="D9D2C6", surface="F8F6F1", hover="DDD7CB",
    border="D2CBBE", fg="66594F", muted="645950", disabled="ABA297",
    caretRow="E8E3D9", selection="E8D4BA", selInactive="E2DCD2", lineNo="A89E92", lineNoCaret="A8281C",
    guide="E2DDD3", guideSel="C9C1B4",
    keyword="A8281C", string="7A5E00", number="AE3A52", type="A3520C", method="161210", call="2A2420",
    field="6E2E68", constant="AE3A52", annotation="AE3A52", label="A8281C",
    comment="7D7369", doc="675D54", docTag="4A4038", op="5E544B", param="66594F", typeParam="8A4A10",
    gold="7A5E00", red="A8281C", redText="FFF5F0", azure="A3520C", caret="A8281C",
    error="C42020", warning="905800", weak="A8955E",
    searchBg="F2DE94", searchBorder="7A5E00", underCaret="EAD9C4", writeCaret="F2D4CC",
    braceBg="E2C8AA", todo="A8281C",
    added="5E9A50", modified="4F7FC0", deleted="C05050",
    diffIns="DDEACB", diffMod="D8E2EE", diffDel="F2D6D2", diffConf="EEE0B4", fileYellow="ECE8E0",
    ansiRed="A3201E", ansiGreen="2D6B26", ansiYellow="7A5800", ansiBlue="1F55A8", ansiMagenta="8E2A90", ansiCyan="0A6A78",
)

FAMILY = "Yolŋu"
BLURB = ("The ochres of Yolŋu bark painting from north-east Arnhem Land: red keywords, yellow strings, orange "
         "types, haematite fields and pink numbers, with white or charcoal methods, on stringybark or white clay.")
THEMES = [
    dict(slug="YolnguGalawu", id="791b6b47-b798-459a-9235-23030d4e04f7", palette=GALAWU),
    dict(slug="YolnguGapan", id="9354d879-0cae-491c-9d7e-74a1f8c4e801", palette=GAPAN),
]
