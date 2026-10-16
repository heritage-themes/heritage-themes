"""Bengal palettes. See heritage/__init__.py for what a theme.py defines."""

# Bengal: the silk and cotton of its looms and the colours of Durga Puja.
# Baluchari is the deep wine silk of Bishnupur, woven with figured borders;
# Laal Paar is the white cotton sari with a red border, worn for the Puja and sindoor khela.
# Sindoor vermilion keywords, sorshe mustard methods, paddy-green strings,
# aparajita (butterfly-pea) blue types, Bishnupur terracotta numbers, Baluchari magenta fields,
# Baluchari violet constants, pond teal annotations, mangrove-green type parameters,
# shankha conch-white text. The caret is the orange stem of the shiuli flower, and Spock labels
# are pola red, the colour of the coral bangle worn with the conch-shell shankha.
BALUCHARI = dict(
    name="Bengal Baluchari", dark=True, parent="Darcula", parentTheme="ExperimentalDark",
    bg="251319", bgUi="1F0F14", bgTool="221117", surface="2F1B23", hover="38222B",
    border="3A242D", fg="F2E8E0", muted="958590", disabled="62525A",
    caretRow="2C1920", selection="4A2A42", selInactive="3A2532", lineNo="5A4650", lineNoCaret="FF9A3C",
    guide="301C24", guideSel="4C3542",
    keyword="FF6B5E", string="A6D17E", number="F09A6A", type="7EA6FF", method="F2C94C", call="E6CF96",
    field="E58AD0", constant="B4A0FF", annotation="5CCFBE", label="FF8078",
    comment="938189", doc="A6927E", docTag="C2AC8E", op="B8AEB2", param="F2E8E0", typeParam="8ED8A8",
    gold="F2C94C", red="B82030", redText="FFF6EE", azure="7EA6FF", caret="FF9A3C",
    error="FF5470", warning="F2A93A", weak="8C7B58",
    searchBg="4A3D18", searchBorder="F2C94C", underCaret="2E3352", writeCaret="4D2228",
    braceBg="2E4A3A", todo="F2C94C",
    added="68AC66", modified="6A8FDC", deleted="C85060",
    diffIns="1E3122", diffMod="1F2440", diffDel="3E1A22", diffConf="3B321A", fileYellow="322219",
    ansiRed="FF6B5E", ansiGreen="A6D17E", ansiYellow="F2C94C", ansiBlue="7EA6FF", ansiMagenta="E58AD0", ansiCyan="5CCFBE",
)
LAAL_PAAR = dict(
    name="Bengal Laal Paar", dark=False, parent="Default", parentTheme="ExperimentalLight",
    bg="FBFAF7", bgUi="F1EEEA", bgTool="F6F4F0", surface="FFFFFF", hover="E9E4DE",
    border="E2D9D2", fg="201C1E", muted="6F676B", disabled="ABA4A6",
    caretRow="F5F1EC", selection="F6D5D2", selInactive="EAE4E3", lineNo="B0A8A6", lineNoCaret="C0202A",
    guide="EDE8E2", guideSel="D7CBC2",
    keyword="C0202A", string="3C7A22", number="B04A16", type="2847B0", method="7E5A00", call="6E5418",
    field="A0287E", constant="5A35A8", annotation="00786A", label="C0202A",
    comment="736C6E", doc="746048", docTag="5A4832", op="57525A", param="201C1E", typeParam="1E7A5A",
    gold="C09010", red="C0202A", redText="FFF8F2", azure="2847B0", caret="C0202A",
    error="D01E2E", warning="A86A00", weak="B0986A",
    searchBg="F5DC8C", searchBorder="C09010", underCaret="D8E0F5", writeCaret="F7D3D3",
    braceBg="CFE8CC", todo="7E5A00",
    added="5FA05A", modified="5A80D0", deleted="C85A5A",
    diffIns="E2F1DC", diffMod="DFE6F7", diffDel="FADCDC", diffConf="F6E8C4", fileYellow="F9F0D2",
    ansiRed="C0202A", ansiGreen="3C7A22", ansiYellow="7E5A00", ansiBlue="2847B0", ansiMagenta="A0287E", ansiCyan="00786A",
)

FAMILY = "Bengal"
BLURB = ("Bengal's looms and Durga Puja: sindoor keywords, mustard methods, paddy-green strings and "
         "aparajita-blue types, on wine-dark Baluchari silk or a white laal paar sari with a red border.")
THEMES = [
    dict(slug="BengalBaluchari", id="aee4f47d-abd9-4f94-83c2-6e15d50e29fe", palette=BALUCHARI),
    dict(slug="BengalLaalPaar", id="94f7c678-47f2-4f1e-9a7d-35fb2cf42bd0", palette=LAAL_PAAR),
]
