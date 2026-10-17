"""Aizome palettes. See heritage/__init__.py for what a theme.py defines."""

# Aizome (藍染, indigo dyeing): "藍四十八色" - indigo has forty-eight colours, one for each depth of dipping,
# from 甕覗 kamenozoki ("a peek into the vat") through 浅葱 asagi, 縹 hanada and 紺 kon to 褐 kachi, the
# near-black indigo worn under armour. One hue only; hierarchy by depth of dye, as in Shuimo. Declarations
# take the undyed white of sashiko thread, bold; types the palest dip; plain names hanada; keywords and
# punctuation recede to 藍鼠 ainezumi grey indigo. The shallow vats lean green and the deep ones violet:
# asagi for strings, pale 水浅葱 mizuasagi for fields, kon for numbers and constants. Kachi is the ground
# at night, kamenozoki by day.
KACHI = dict(
    name="Aizome Kachi", dark=True, parent="Darcula", parentTheme="ExperimentalDark", kwBold=False,
    bg="0B1421", bgUi="070E1A", bgTool="09121E", surface="121C2B", hover="192435",
    border="1F2939", fg="A3BED6", muted="76889B", disabled="445160",
    caretRow="101A28", selection="1F344E", selInactive="19273A", lineNo="404E60", lineNoCaret="DFEAF1",
    guide="151E2C", guideSel="2A3647",
    keyword="788FA7", string="75BFC8", number="A0A5E0", type="C1DCEB", method="E9F2F7", call="A3BED6",
    field="A9D3DB", constant="A0A5E0", annotation="788FA7", label="DFEAF1",
    comment="5B6E83", doc="688499", docTag="83A3BB", op="788FA7", param="A3BED6", typeParam="75BFC8",
    gold="75BFC8", red="2D5786", redText="ECF3F8", azure="75BFC8", caret="E9F2F7",
    error="EB635E", warning="E1A447", weak="657E90",
    searchBg="084551", searchBorder="75BFC8", underCaret="163045", writeCaret="2F3058",
    braceBg="233F5B", todo="C1DCEB",
    added="5D9669", modified="5B8ABB", deleted="B75B55",
    diffIns="0C281D", diffMod="0F2336", diffDel="361717", diffConf="2E220B", fileYellow="1D190F",
    ansiRed="E66E68", ansiGreen="73BB83", ansiYellow="DCBA5C", ansiBlue="73A9E1", ansiMagenta="CC8BC5", ansiCyan="60BFC4",
)
KAMENOZOKI = dict(
    name="Aizome Kamenozoki", dark=False, parent="Default", parentTheme="ExperimentalLight", kwBold=False,
    bg="E7F2F7", bgUi="DCE9EF", bgTool="E1EDF3", surface="F1F8FB", hover="D0DFE7",
    border="C3D4DD", fg="213651", muted="586B80", disabled="97A7B3",
    caretRow="DCEBF1", selection="BDD8EC", selInactive="D1E3EE", lineNo="8EA1B0", lineNoCaret="132139",
    guide="D6E4EA", guideSel="B2C4CF",
    keyword="576B7F", string="186575", number="4B4D8B", type="111F37", method="0A152A", call="213651",
    field="214D62", constant="4B4D8B", annotation="576B7F", label="111F37",
    comment="6E8393", doc="547084", docTag="38536A", op="596B7D", param="213651", typeParam="186575",
    gold="186575", red="23436C", redText="F0F6F9", azure="186575", caret="111F37",
    error="BA2B2E", warning="955E00", weak="89A2B5",
    searchBg="ABDBE1", searchBorder="186575", underCaret="C7DEF0", writeCaret="D4D4F2",
    braceBg="B9D1E7", todo="111F37",
    added="579766", modified="4F7EAE", deleted="BB5752",
    diffIns="D2ECDD", diffMod="D3E6F6", diffDel="FBDCDB", diffConf="F2E3C3", fileYellow="EFEBDD",
    ansiRed="AC3031", ansiGreen="246E3A", ansiYellow="7D5E07", ansiBlue="255691", ansiMagenta="793974", ansiCyan="086A73",
)

FAMILY = "Aizome"
BLURB = ("Japanese indigo dyeing in a single hue: hierarchy by depth of dye, with sashiko-white declarations, "
         "green-leaning asagi strings and violet-leaning kon numbers.")
THEMES = [
    dict(slug="AizomeKachi", id="8263d4a6-7210-4bad-9983-be44482c4137", palette=KACHI),
    dict(slug="AizomeKamenozoki", id="165eb83b-5971-4ff7-ade4-2c61d35dcbc6", palette=KAMENOZOKI),
]
