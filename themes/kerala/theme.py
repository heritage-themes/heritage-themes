"""Kerala palettes. See heritage/__init__.py for what a theme.py defines."""

# Kerala: the backwaters, the Kathakali stage and the kasavu loom.
# Backwaters is the palm-lined water at night, deep green under the brass lamp of an
# all-night Kathakali performance; Kasavu is the off-white handloom cotton with its gold zari border.
# Syntax colours come from Kathakali make-up and the land around it:
# kathi red keywords (the villain's red), zari gold strings, pacha green method declarations
# (the green face of the noble hero), kayal (backwater) teal types, laterite-orange numbers,
# lotus pink fields, kingfisher blue constants, kakkapoovu violet annotations,
# cardamom-green type parameters, chutti rice-paste white text. Spock labels are zari gold.
BACKWATERS = dict(
    name="Kerala Backwaters (Dark)", dark=True, parent="Darcula",
    bg="0F2219", bgUi="0C1C15", bgTool="0E1F17", frame="1F3226", surface="16291F", hover="1D3327",
    border="1F362A", fg="F0EADB", muted="8B988C", disabled="55655B",
    caretRow="14281E", selection="26443A", selInactive="1F3830", lineNo="465A50", lineNoCaret="E3B84A",
    guide="17291F", guideSel="2F4B3D",
    keyword="FF958E", string="E7BF57", number="FEA668", type="5AD5CB", method="7BD77F", call="AFD8A6",
    field="F89DC9", constant="85C4FF", annotation="C8AEFA", label="E7BF57",
    comment="7F8E84", doc="A39880", docTag="BFAF8C", op="B0B6AE", param="F0EADB", typeParam="E2DA9C",
    gold="E3B84A", red="B03A2E", redText="F5EEDE", azure="6CB8F5", caret="E3B84A",
    error="FF5A5F", warning="F0A535", weak="8A7F55",
    searchBg="46401A", searchBorder="E3B84A", underCaret="21403F", writeCaret="4A2826",
    braceBg="3A5530", todo="E3B84A",
    added="6BB070", modified="5B98D0", deleted="C25A4E",
    diffIns="1A3524", diffMod="162F3A", diffDel="3A2220", diffConf="38341A", fileYellow="222C19",
    ansiRed="F27560", ansiGreen="A8D67A", ansiYellow="EDCB5E", ansiBlue="6CB8F5", ansiMagenta="EC8EBA", ansiCyan="4FD1CC",
)
KASAVU = dict(
    name="Kerala Kasavu (Light)", dark=False, parent="Default",
    bg="F9F5E8", bgUi="EFE9D6", bgTool="F4EFDE", frame="E2D9BF", surface="FCF9EE", hover="E7DFC6",
    border="DACEAC", fg="1F2420", muted="5A615A", disabled="A5A797",
    caretRow="F2ECD9", selection="D4E8DA", selInactive="E2E5D8", lineNo="AAA58D", lineNoCaret="A07000",
    guide="EAE3CE", guideSel="D5C8A4",
    keyword="AE2D2F", string="745903", number="974C02", type="00736C", method="01791E", call="4D7544",
    field="983E6E", constant="0667AA", annotation="6E519D", label="6E5402",
    comment="6F766E", doc="72664A", docTag="5A4E32", op="565C56", param="1F2420", typeParam="79702E",
    gold="8B6C05", red="B0203A", redText="FFF8F2", azure="1060A8", caret="B0203A",
    error="D01E2E", warning="A86A00", weak="A8975E",
    searchBg="F5DE8E", searchBorder="B8900E", underCaret="D4E4F2", writeCaret="F5D3D6",
    braceBg="CDE8CF", todo="7A5A00",
    added="5FA060", modified="5A8CC8", deleted="C85A5A",
    diffIns="E0F0DA", diffMod="DCE8F4", diffDel="F8DCDC", diffConf="F5E8C4", fileYellow="F7EBC4",
    ansiRed="B0203A", ansiGreen="3A7A1E", ansiYellow="7A5A00", ansiBlue="1060A8", ansiMagenta="9C3A8A", ansiCyan="007A78",
)

FAMILY = "Kerala"
BLURB = ("Kerala's backwaters, Kathakali stage and kasavu loom: kathi-red keywords, zari-gold strings, "
         "pacha-green methods and backwater-teal types, on palm-dark water at night or off-white "
         "handloom with a gold border.")
THEMES = [
    dict(slug="KeralaBackwaters", id="8a5a38d8-3544-4838-b5be-7adc336f5bca", palette=BACKWATERS),
    dict(slug="KeralaKasavu", id="30fb18e8-21fd-4b51-b575-72c8bb92e312", palette=KASAVU),
]
