"""Danqing palettes. See heritage/__init__.py for what a theme.py defines."""

# Danqing (丹青, "cinnabar and azurite" = Chinese painting): mineral pigments, not pastels.
# The blue-green landscape (青绿山水) leads: azurite 石青 keywords and malachite 石绿 strings,
# with cinnabar 朱砂 method declarations and its paler top layer 朱膘 for calls,
# gamboge 藤黄 types, carmine 胭脂 numbers, dai 黛 fields, lotus-root 藕荷 constants,
# ochre 赭石 annotations, second-grade azurite 二青 type parameters,
# ink 墨 on inkstone / aged xuan paper 宣纸, Spock labels in seal-paste red 印泥.
INK = dict(
    name="Danqing Ink", dark=True, parent="Darcula", parentTheme="ExperimentalDark",
    bg="1B1D1B", bgUi="151716", bgTool="181A19", surface="232624", hover="2A2E2B",
    border="2C302D", fg="DCD6C8", muted="868A80", disabled="575C57",
    caretRow="202421", selection="2E3F45", selInactive="283335", lineNo="4B514C", lineNoCaret="F0643F",
    guide="252926", guideSel="3B423D",
    keyword="80C5FF", string="6FD5B0", number="EC7C99", type="E0C766", method="FFA28A", call="FFB7A0",
    field="C2B1F8", constant="E9B4DC", annotation="CD9D73", label="FE8B7D",
    comment="747B74", doc="8E9278", docTag="A9AB8A", op="A8A699", param="DCD6C8", typeParam="9BDDEE",
    gold="E9B949", red="B8382A", redText="F6EEDF", azure="4FB3C9", caret="F0643F",
    error="F25C54", warning="E6A23C", weak="8B8155",
    searchBg="4A3D18", searchBorder="E9B949", underCaret="263A3E", writeCaret="4A2622",
    braceBg="2F4A3E", todo="E9B949",
    added="6E9C5A", modified="4F93A8", deleted="A54A3E",
    diffIns="1F2E22", diffMod="1C2C31", diffDel="352021", diffConf="352E1C", fileYellow="29271C",
    ansiRed="F0643F", ansiGreen="A3B47E", ansiYellow="E9B949", ansiBlue="4FB3C9", ansiMagenta="CFA3C0", ansiCyan="7FC4B6",
)
PAPER = dict(
    name="Danqing Paper", dark=False, parent="Default", parentTheme="ExperimentalLight",
    bg="ECE5D4", bgUi="E3DBC8", bgTool="E7E0CE", surface="F3EDDE", hover="DAD1BC",
    border="D0C6AF", fg="26282A", muted="67655D", disabled="A59C88",
    caretRow="E4DCC8", selection="C9DCE0", selInactive="D8DBD2", lineNo="A19880", lineNoCaret="B32D1E",
    guide="DBD2BD", guideSel="C3B79B",
    keyword="0568A4", string="057357", number="9C284F", type="766202", method="A9371B", call="9C4E36",
    field="68559B", constant="85527A", annotation="724313", label="A01F1B",
    comment="76736A", doc="676043", docTag="554D32", op="55534D", param="26282A", typeParam="216E7F",
    gold="B8860B", red="B32D1E", redText="F7EFE0", azure="0F6680", caret="B32D1E",
    error="C8202F", warning="8F5800", weak="A8975E",
    searchBg="EDD58A", searchBorder="B8860B", underCaret="CFE2E6", writeCaret="F0D2CB",
    braceBg="C8E0CF", todo="7E5500",
    added="5E9A5A", modified="4F8FA8", deleted="C0574B",
    diffIns="DDEBD6", diffMod="D7E6EA", diffDel="F2D8D2", diffConf="EFE2BF", fileYellow="E6DBBA",
    ansiRed="B32D1E", ansiGreen="4A6526", ansiYellow="7E5500", ansiBlue="0F6680", ansiMagenta="7A3F6A", ansiCyan="0E6A62",
)

FAMILY = "Danqing"
BLURB = ("Chinese painting pigments, led by the blue-green landscape: azurite keywords, malachite strings, "
         "cinnabar methods and gamboge types on inkstone or aged xuan paper, with Spock blocks marked like red "
         "seal stamps.")
THEMES = [
    dict(slug="DanqingInk", id="d9d7840f-7402-422e-869e-dfbb781ca059", palette=INK),
    dict(slug="DanqingPaper", id="50103e31-3b24-415b-9b54-00acf1e7b7e5", palette=PAPER),
]
