"""Edo palettes. See heritage/__init__.py for what a theme.py defines."""

# Edo: "四十八茶百鼠" - forty-eight browns and a hundred greys. Sumptuary laws kept townspeople to brown (茶),
# grey (鼠) and indigo (藍), and dyers answered with hundreds of named, faintly tinted shades. Every role
# has its own hue, all of them muted. Indigo gives the keywords and annotations (藍鼠, 御納戸). Browns give
# the literals: 利休茶 rikyūcha strings, 芝翫茶 shikancha numbers and constants. Greys give the names:
# 利休鼠 rikyū-nezumi types, 藤鼠 fuji-nezumi method declarations and calls, 梅鼠 ume-nezumi fields, and
# 銀鼠 gin-nezumi plain text. The red silk lining (紅絹 momi) hidden inside sober kimono (裏勝り) marks
# the caret, Spock labels and TODOs. Cha has a tea-brown ground; Nezumi a pale grey one.
CHA = dict(
    name="Edo Cha", dark=True, parent="Darcula",
    bg="191410", bgUi="130E0B", bgTool="17110D", frame="2D261F", surface="221C17", hover="2A241E",
    border="2F2923", fg="C2BDB5", muted="8E8881", disabled="57514C",
    caretRow="1F1915", selection="2A3741", selInactive="202930", lineNo="564E48", lineNoCaret="E8605B",
    guide="241E1A", guideSel="3E3631",
    keyword="86AAC4", string="BEB182", number="CD967E", type="96BBA6", method="CABCE6", call="BFB4D7",
    field="CE9FB0", constant="CD967E", annotation="86AAC4", label="E8605B",
    comment="7C736A", doc="8E8576", docTag="A89D86", op="97918A", param="C2BDB5", typeParam="96BBA6",
    gold="D0A260", red="AF3C3A", redText="FCF3ED", azure="86AAC4", caret="E8605B",
    error="EB635E", warning="E1A447", weak="847967",
    searchBg="4A371B", searchBorder="D0A260", underCaret="20303B", writeCaret="492826",
    braceBg="2C404E", todo="E8605B",
    added="5D9669", modified="5C8BB3", deleted="B75B55",
    diffIns="17261A", diffMod="15232F", diffDel="32191A", diffConf="2D220F", fileYellow="1F1A13",
    ansiRed="E66E68", ansiGreen="7ABA7C", ansiYellow="DCBA5C", ansiBlue="73ABDA", ansiMagenta="C88EC3", ansiCyan="6CBEC2",
)
NEZUMI = dict(
    name="Edo Nezumi", dark=False, parent="Default", kwBold=False,
    bg="F2F0EC", bgUi="E9E6E1", bgTool="EEEBE6", frame="DAD5CF", surface="F9F6F3", hover="E0DCD6",
    border="D5D0CA", fg="3A342F", muted="6E6862", disabled="A9A49E",
    caretRow="EBE7E2", selection="C9DAE7", selInactive="D9E3EA", lineNo="A39D97", lineNoCaret="BA2B2E",
    guide="E4E1DC", guideSel="C6C0B9",
    keyword="2D5A78", string="6B5D27", number="8C482F", type="335D47", method="4E3D6C", call="52456B",
    field="784157", constant="8C482F", annotation="2D5A78", label="BA2B2E",
    comment="877F77", doc="746A5C", docTag="5A4E3A", op="68625C", param="3A342F", typeParam="335D47",
    gold="9A6418", red="B02A2D", redText="FCF8F4", azure="2D5A78", caret="BA2B2E",
    error="BA2B2E", warning="955E00", weak="A89D8A",
    searchBg="EAD5AB", searchBorder="9A6418", underCaret="D0E1ED", writeCaret="F5D6D2",
    braceBg="C0D4E3", todo="BA2B2E",
    added="579766", modified="507FA7", deleted="BB5752",
    diffIns="D7EBDA", diffMod="D7E7F5", diffDel="F8DDDC", diffConf="F1E3C7", fileYellow="EEE9DF",
    ansiRed="AC3031", ansiGreen="2F6D34", ansiYellow="7D5E07", ansiBlue="23588A", ansiMagenta="793974", ansiCyan="086A73",
)

FAMILY = "Edo"
BLURB = ("The forty-eight browns and hundred greys of Edo-period dress: muted indigo keywords, brown "
         "literals, tinted-grey names, and a hidden red lining for the caret and labels.")
THEMES = [
    dict(slug="EdoCha", id="db360c2e-196b-46ce-882f-48ffd06a2b82", palette=CHA),
    dict(slug="EdoNezumi", id="90795073-c6d4-4547-a23e-a6ab150c1498", palette=NEZUMI),
]
