"""Bengal palettes. See heritage/__init__.py for what a theme.py defines."""

# Bengal: the silk and cotton of its looms and the colours of Durga Puja.
# Baluchari is the deep wine silk of Bishnupur, woven with figured borders;
# Laal Paar is the white cotton sari with a red border, worn for the Puja and sindoor khela.
# Aparajita (butterfly-pea) violet-blue keywords, Baluchari magenta strings, paddy-green methods,
# Bishnupur terracotta types, sorshe mustard fields, sindoor vermilion numbers,
# pukur (pond) teal constants, neel indigo annotations, mangrove-green type parameters,
# shankha conch-white text. The caret is the orange stem of the shiuli flower, and Spock labels
# are pola red, the colour of the coral bangle worn with the conch-shell shankha.
BALUCHARI = dict(
    name="Bengal Baluchari (Dark)", dark=True, parent="Darcula",
    bg="2A1220", bgUi="240E1B", bgTool="27101E", frame="3D2233", surface="341A2A", hover="3D2132",
    border="3F2335", fg="F2E8E0", muted="958590", disabled="695262",
    caretRow="311827", selection="4A2A42", selInactive="402439", lineNo="604558", lineNoCaret="FF9A3C",
    guide="351B2B", guideSel="52344A",
    keyword="B6B4FE", string="FD9AC6", number="FE8B7D", type="EBAF86", method="87D576", call="B4D7A2",
    field="DEC358", constant="58D4D0", annotation="6FC1F6", label="FF9592",
    comment="938189", doc="A6927E", docTag="C2AC8E", op="B8AEB2", param="F2E8E0", typeParam="A8EBDB",
    gold="F2C94C", red="B82030", redText="FFF6EE", azure="7EA6FF", caret="FF9A3C",
    error="FF5470", warning="F2A93A", weak="8C7B58",
    searchBg="4A3D18", searchBorder="F2C94C", underCaret="2E3352", writeCaret="4D2228",
    braceBg="2E4A3A", todo="F2C94C",
    added="68AC66", modified="6A8FDC", deleted="C85060",
    diffIns="1E3122", diffMod="1F2440", diffDel="3E1A22", diffConf="3B321A", fileYellow="372221",
    ansiRed="FF6B5E", ansiGreen="A6D17E", ansiYellow="F2C94C", ansiBlue="7EA6FF", ansiMagenta="E58AD0", ansiCyan="5CCFBE",
)
LAAL_PAAR = dict(
    name="Bengal Laal Paar (Light)", dark=False, parent="Default",
    bg="FBFAF7", bgUi="F1EEEA", bgTool="F6F4F0", frame="E3DDD8", surface="FFFFFF", hover="E9E4DE",
    border="E2D9D2", fg="201C1E", muted="6F676B", disabled="ABA4A6",
    caretRow="F5F1EC", selection="F6D5D2", selInactive="EAE4E3", lineNo="B0A8A6", lineNoCaret="C0202A",
    guide="EDE8E2", guideSel="D7CBC2",
    keyword="5D4EBB", string="9D396C", number="B22721", type="8E5225", method="217700", call="52743F",
    field="6F5C04", constant="047270", annotation="066B9A", label="A72530",
    comment="736C6E", doc="746048", docTag="5A4832", op="57525A", param="201C1E", typeParam="347D6F",
    gold="C09010", red="C0202A", redText="FFF8F2", azure="2847B0", caret="C0202A",
    error="D01E2E", warning="A86A00", weak="B0986A",
    searchBg="F5DC8C", searchBorder="C09010", underCaret="D8E0F5", writeCaret="F7D3D3",
    braceBg="CFE8CC", todo="7E5A00",
    added="5FA05A", modified="5A80D0", deleted="C85A5A",
    diffIns="E2F1DC", diffMod="DFE6F7", diffDel="FADCDC", diffConf="F6E8C4", fileYellow="F9F0D2",
    ansiRed="C0202A", ansiGreen="3C7A22", ansiYellow="7E5A00", ansiBlue="2847B0", ansiMagenta="A0287E", ansiCyan="00786A",
)

FAMILY = "Bengal"
BLURB = ("Bengal's looms and Durga Puja: aparajita keywords, Baluchari-magenta strings, paddy-green methods "
         "and terracotta types, on wine-dark Baluchari silk or a white laal paar sari with a red border.")
THEMES = [
    dict(slug="BengalBaluchari", id="aee4f47d-abd9-4f94-83c2-6e15d50e29fe", palette=BALUCHARI),
    dict(slug="BengalLaalPaar", id="94f7c678-47f2-4f1e-9a7d-35fb2cf42bd0", palette=LAAL_PAAR),
]
