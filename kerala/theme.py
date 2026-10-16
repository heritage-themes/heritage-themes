"""Kerala palettes. See heritage/__init__.py for what a theme.py defines."""

# Kerala: the backwaters, the Kathakali stage and the kasavu loom.
# Backwaters is the palm-lined water at night, deep green under the brass lamp of an
# all-night Kathakali performance; Kasavu is the off-white handloom cotton with its gold zari border.
# Syntax colours come from Kathakali make-up and the land around it:
# kathi red keywords (the villain's red), zari gold methods, banana-leaf green strings,
# kingfisher blue types, laterite-orange numbers, lotus pink fields, kakkapoovu violet constants,
# backwater teal annotations, cardamom-green type parameters, chutti rice-paste white text.
# Spock labels are zari gold.
BACKWATERS = dict(
    name="Kerala Backwaters", dark=True, parent="Darcula", parentTheme="ExperimentalDark",
    bg="0F2219", bgUi="0C1C15", bgTool="0E1F17", surface="16291F", hover="1D3327",
    border="1F362A", fg="F0EADB", muted="879488", disabled="55655B",
    caretRow="14281E", selection="26443A", selInactive="1F3830", lineNo="465A50", lineNoCaret="E3B84A",
    guide="17291F", guideSel="2F4B3D",
    keyword="F27560", string="A8D67A", number="F5A05A", type="6CB8F5", method="EDCB5E", call="DCCB9C",
    field="EC8EBA", constant="B49CF2", annotation="4FD1CC", label="E3B84A",
    comment="7F8E84", doc="A39880", docTag="BFAF8C", op="B0B6AE", param="F0EADB", typeParam="7ED9A4",
    gold="E3B84A", red="B03A2E", redText="F5EEDE", azure="6CB8F5", caret="E3B84A",
    error="FF5A5F", warning="F0A535", weak="8A7F55",
    searchBg="46401A", searchBorder="E3B84A", underCaret="21403F", writeCaret="4A2826",
    braceBg="3A5530", todo="E3B84A",
    added="6BB070", modified="5B98D0", deleted="C25A4E",
    diffIns="1A3524", diffMod="162F3A", diffDel="3A2220", diffConf="38341A", fileYellow="222C19",
    ansiRed="F27560", ansiGreen="A8D67A", ansiYellow="EDCB5E", ansiBlue="6CB8F5", ansiMagenta="EC8EBA", ansiCyan="4FD1CC",
)
KASAVU = dict(
    name="Kerala Kasavu", dark=False, parent="Default", parentTheme="ExperimentalLight",
    bg="FCFAF4", bgUi="F2EEE2", bgTool="F7F4EA", surface="FFFEFA", hover="EAE4D2",
    border="DDD3B8", fg="1F2420", muted="6B726B", disabled="A8ACA2",
    caretRow="F5F1E5", selection="D4E8DA", selInactive="E5EAE4", lineNo="ADAA98", lineNoCaret="A07000",
    guide="EDE8DA", guideSel="D8CDB0",
    keyword="B0203A", string="3A7A1E", number="B04A0C", type="1060A8", method="7A5A00", call="6B5418",
    field="9C3A8A", constant="5A3AA8", annotation="007A78", label="8A6500",
    comment="6F766E", doc="72664A", docTag="5A4E32", op="565C56", param="1F2420", typeParam="1E7A4A",
    gold="B8900E", red="B0203A", redText="FFF8F2", azure="1060A8", caret="B0203A",
    error="D01E2E", warning="A86A00", weak="A8975E",
    searchBg="F5DE8E", searchBorder="B8900E", underCaret="D4E4F2", writeCaret="F5D3D6",
    braceBg="CDE8CF", todo="7A5A00",
    added="5FA060", modified="5A8CC8", deleted="C85A5A",
    diffIns="E0F0DA", diffMod="DCE8F4", diffDel="F8DCDC", diffConf="F5E8C4", fileYellow="FAF0D0",
    ansiRed="B0203A", ansiGreen="3A7A1E", ansiYellow="7A5A00", ansiBlue="1060A8", ansiMagenta="9C3A8A", ansiCyan="007A78",
)

FAMILY = "Kerala"
BLURB = ("Kerala's backwaters, Kathakali stage and kasavu loom: kathi-red keywords, zari-gold methods, "
         "banana-leaf strings and kingfisher-blue types, on palm-dark water at night or off-white "
         "handloom with a gold border.")
THEMES = [
    dict(slug="KeralaBackwaters", id="8a5a38d8-3544-4838-b5be-7adc336f5bca", palette=BACKWATERS),
    dict(slug="KeralaKasavu", id="30fb18e8-21fd-4b51-b575-72c8bb92e312", palette=KASAVU),
]
