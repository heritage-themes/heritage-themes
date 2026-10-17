"""Ainu palettes. See heritage/__init__.py for what a theme.py defines."""

# Ainu: the appliqué robes of Hokkaido. Kaparamip is indigo-dyed trade cotton with large curvilinear cut-outs
# of white cotton sewn on; attus is cloth woven from elm-bark fibre, with indigo cotton appliqué. Chain and
# couching stitches follow the pattern, and red cloth or thread marks the collar, cuffs and hem, the openings
# that the pattern guards against spirits. Ainu has four basic colour words, and each covers a range: kunne
# (dark, from black to navy), retar (light, from white to pale yellow and pale blue), hure (red, from pink to
# orange) and siwnin (from green to yellow and blue-violet). Keywords are the appliqué, set bold: retar white
# on the indigo, kunne indigo on the elm bark. Types take another tone of it. Hure red marks method
# declarations, the openings of the code, with lighter red calls. Siwnin gives green strings (the couching
# thread), yellow fields and blue-violet numbers, constants and annotations. Kaparamip has the indigo cotton
# as its ground; Attus has the elm-bark cloth.
KAPARAMIP = dict(
    name="Ainu Kaparamip (Dark)", dark=True, parent="Darcula", kwBold=True,
    bg="141A2D", bgUi="101524", bgTool="121829", frame="222B44", surface="1B2238", hover="242C45",
    border="2E3752", fg="B0B4C0", muted="959BB0", disabled="545B74",
    caretRow="1B2236", selection="2E3A5E", selInactive="242D48", lineNo="555D78", lineNoCaret="EE705E",
    guide="1E2539", guideSel="3A4462",
    keyword="F2EFE6", string="8CC78E", number="B49CF0", type="9FB8F4", method="EE705E", call="F49E8E",
    field="D6CE86", constant="B49CF0", annotation="B49CF0", label="EE705E",
    comment="6E7797", doc="8088A6", docTag="A3ABC6", op="9AA0B6", param="B0B4C0", typeParam="DCE3F8",
    gold="E2D48A", red="B23A2C", redText="FFF4F0", azure="A9BCF0", caret="EE705E",
    error="FF6B5E", warning="E3A33C", weak="8A8460",
    searchBg="4A4418", searchBorder="E2D48A", underCaret="2A3656", writeCaret="4A2630",
    braceBg="34406A", todo="EE705E",
    added="7FB070", modified="6A90D8", deleted="D0605A",
    diffIns="1A2A26", diffMod="1C2640", diffDel="3A1C26", diffConf="38341C", fileYellow="181E30",
    ansiRed="F07E6E", ansiGreen="8CC878", ansiYellow="EECC5A", ansiBlue="82AEF0", ansiMagenta="DE8AD0", ansiCyan="6CCCD0",
)
ATTUS = dict(
    name="Ainu Attus (Light)", dark=False, parent="Default", kwBold=True,
    bg="EEE6D4", bgUi="E3DAC6", bgTool="E9E1CE", frame="D7CCB6", surface="F6F1E6", hover="DBD1BC",
    border="CFC4AC", fg="34384A", muted="5C5C62", disabled="A8A08E",
    caretRow="E6DDC9", selection="D0D5E4", selInactive="DFDACD", lineNo="9F9682", lineNoCaret="B0281C",
    guide="E0D8C4", guideSel="C6BCA4",
    keyword="1E2A62", string="1F6E3A", number="6A3AA8", type="3A5296", method="B0281C", call="9A3A2E",
    field="6A5E00", constant="6A3AA8", annotation="6A3AA8", label="B0281C",
    comment="776F60", doc="5E5C50", docTag="44443E", op="55576A", param="34384A", typeParam="2A3E80",
    gold="7E6400", red="B0281C", redText="FFF5F0", azure="3A5296", caret="B0281C",
    error="C42020", warning="905800", weak="A8955E",
    searchBg="EED98E", searchBorder="7E6400", underCaret="D6DAE8", writeCaret="F2D0C8",
    braceBg="CCD2E6", todo="B0281C",
    added="5E9A50", modified="4F7FC0", deleted="C05050",
    diffIns="DCE8C8", diffMod="D6DEEC", diffDel="F2D4CE", diffConf="ECDDB0", fileYellow="EAE2CF",
    ansiRed="A3201E", ansiGreen="2D6B26", ansiYellow="7A5800", ansiBlue="1F55A8", ansiMagenta="8E2A90", ansiCyan="0A6A78",
)

FAMILY = "Ainu"
BLURB = ("The appliqué robes of the Ainu of Hokkaido: bold appliqué keywords, red method declarations at the "
         "openings, green thread strings, yellow fields and blue-violet numbers, on indigo cotton or elm-bark cloth.")
THEMES = [
    dict(slug="AinuKaparamip", id="4edc25cb-d80c-4af2-82ba-6f8276127bb4", palette=KAPARAMIP),
    dict(slug="AinuAttus", id="1f1050f2-6969-4aab-8070-def56d72bf77", palette=ATTUS),
]
