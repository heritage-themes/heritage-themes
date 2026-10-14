"""Danqing palettes. See heritage/__init__.py for what a theme.py defines."""

# Danqing (丹青, "cinnabar and azurite" = Chinese painting): mineral pigments, not pastels.
# Deliberately breaks the usual green/yellow/blue syntax convention:
# cinnabar 朱砂 keywords, azurite 石青 types, gamboge 藤黄 methods, bamboo 竹青 strings,
# lotus-root 藕荷 fields, ochre 赭石 numbers, dai 黛 constants, malachite 石绿 annotations,
# ink 墨 on inkstone / xuan paper 宣纸, Spock labels as red seal stamps 印章.
INK = dict(
    name="Danqing Ink", dark=True, parent="Darcula", parentTheme="ExperimentalDark",
    bg="1B1D1B", bgUi="151716", bgTool="181A19", surface="232624", hover="2A2E2B",
    border="2C302D", fg="DCD6C8", muted="868A80", disabled="575C57",
    caretRow="202421", selection="2E3F45", selInactive="283335", lineNo="4B514C", lineNoCaret="F0643F",
    guide="252926", guideSel="3B423D",
    keyword="F0643F", string="A3B47E", number="C99A62", type="4FB3C9", method="E9B949", call="D9BE7E",
    field="CFA3C0", constant="A59FD2", annotation="6FBF9E", label="F6EEDF", labelBg="B8382A",
    comment="747B74", doc="8E9278", docTag="A9AB8A", op="A8A699", param="DCD6C8", typeParam="7FC4B6",
    gold="E9B949", red="B8382A", redText="F6EEDF", azure="4FB3C9", caret="F0643F",
    error="F25C54", warning="E6A23C", weak="8B8155",
    searchBg="4A3D18", searchBorder="E9B949", underCaret="263A3E", writeCaret="4A2622",
    braceBg="2F4A3E", todo="E9B949",
    added="6E9C5A", modified="4F93A8", deleted="A54A3E",
    diffIns="1F2E22", diffMod="1C2C31", diffDel="352021", diffConf="352E1C", fileYellow="29271C",
)
PAPER = dict(
    name="Danqing Paper", dark=False, parent="Default", parentTheme="ExperimentalLight",
    bg="EEEAE0", bgUi="E5E0D4", bgTool="E9E5DA", surface="F5F2EA", hover="DCD6C8",
    border="D2CBBB", fg="26282A", muted="6F6C64", disabled="A7A193",
    caretRow="E6E1D4", selection="C9DCE0", selInactive="DAE0DE", lineNo="A39D8B", lineNoCaret="B32D1E",
    guide="DDD7C9", guideSel="C5BCA7",
    keyword="B32D1E", string="4A6526", number="854E24", type="0F6680", method="7E5500", call="6F5210",
    field="7A3F6A", constant="4F4790", annotation="1A7353", label="F7EFE0", labelBg="B32D1E",
    comment="76736A", doc="676043", docTag="554D32", op="55534D", param="26282A", typeParam="0E6A62",
    gold="B8860B", red="B32D1E", redText="F7EFE0", azure="0F6680", caret="B32D1E",
    error="C8202F", warning="A86800", weak="A8975E",
    searchBg="EDD58A", searchBorder="B8860B", underCaret="CFE2E6", writeCaret="F0D2CB",
    braceBg="C8E0CF", todo="7E5500",
    added="5E9A5A", modified="4F8FA8", deleted="C0574B",
    diffIns="DDEBD6", diffMod="D7E6EA", diffDel="F2D8D2", diffConf="EFE2BF", fileYellow="E8E0C6",
)

FAMILY = "Danqing"
BLURB = ("Chinese painting pigments: cinnabar keywords, azurite types, gamboge methods and bamboo-green "
         "strings on inkstone or xuan paper, with Spock blocks marked like red seal stamps.")
THEMES = [
    dict(slug="DanqingInk", id="d9d7840f-7402-422e-869e-dfbb781ca059", palette=INK),
    dict(slug="DanqingPaper", id="50103e31-3b24-415b-9b54-00acf1e7b7e5", palette=PAPER),
]
