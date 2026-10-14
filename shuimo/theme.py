"""Shuimo palettes. See heritage/__init__.py for what a theme.py defines."""

# Shuimo (水墨, ink-wash painting): "墨分五色" - ink has five shades. Hierarchy by tone and weight,
# not hue: declarations darkest + bold, plain names mid ink, keywords recede to lighter ink.
# Only the two washes of 浅绛 landscape painting add colour: 花青 indigo (strings) and 赭石 ochre
# (numbers, constants), plus the red seal 印章 for Spock labels, caret and TODO.
SHN = dict(
    name="Shuimo Night", dark=True, parent="Darcula", parentTheme="ExperimentalDark", kwBold=False,
    bg="171716", bgUi="121211", bgTool="151514", surface="1F1F1E", hover="272725",
    border="2A2A28", fg="C8C6C0", muted="85837D", disabled="55544F",
    caretRow="1D1D1C", selection="2C333A", selInactive="262A2E", lineNo="4A4945", lineNoCaret="D5584A",
    guide="232322", guideSel="3A3A37",
    keyword="8E8C86", string="8FAAC2", number="C49A72", type="C8C6C0", method="F3F1EB", call="C8C6C0",
    field="C8C6C0", constant="C49A72", annotation="8E8C86", label="F3EBDF", labelBg="B03A2E",
    comment="6E6D67", doc="7E8C99", docTag="9AA8B5", op="8E8C86", param="C8C6C0", typeParam="8FAAC2",
    gold="C9A24E", red="B03A2E", redText="F3EBDF", azure="8FAAC2", caret="D5584A",
    error="E8584E", warning="D99A3A", weak="7D7660",
    searchBg="3B3524", searchBorder="C9A24E", underCaret="25313B", writeCaret="3E2422",
    braceBg="2D3A44", todo="D5584A",
    added="5F8A5A", modified="5C7F9C", deleted="9A4A40",
    diffIns="1D291C", diffMod="1B242C", diffDel="31201E", diffConf="302A1B", fileYellow="24221B",
)
SHD = dict(
    name="Shuimo Day", dark=False, parent="Default", parentTheme="ExperimentalLight", kwBold=False,
    bg="F4F3EF", bgUi="ECEBE6", bgTool="F0EFEA", surface="FAF9F6", hover="E2E0DA",
    border="D8D6CF", fg="2A2A28", muted="77756F", disabled="ADABA4",
    caretRow="ECEAE4", selection="D9DEE3", selInactive="E3E4E3", lineNo="AEACA5", lineNoCaret="B03A2E",
    guide="E3E1DB", guideSel="C9C6BE",
    keyword="66645F", string="3D5F7A", number="8A5530", type="2A2A28", method="111111", call="2A2A28",
    field="2A2A28", constant="8A5530", annotation="66645F", label="F7F2EA", labelBg="B03A2E",
    comment="85837C", doc="62717E", docTag="4F5E6B", op="6C6A64", param="2A2A28", typeParam="3D5F7A",
    gold="9A7420", red="B03A2E", redText="F7F2EA", azure="3D5F7A", caret="B03A2E",
    error="C42B2B", warning="A86B00", weak="A39A7A",
    searchBg="E8DDB8", searchBorder="9A7420", underCaret="DCE3EA", writeCaret="F0D8D3",
    braceBg="D5DDE4", todo="B03A2E",
    added="6E9A6A", modified="6F8FAA", deleted="B8655A",
    diffIns="E1EBDD", diffMod="DDE5EC", diffDel="F2DEDA", diffConf="EEE4C8", fileYellow="EFEADA",
)

FAMILY = "Shuimo"
BLURB = ("Chinese ink-wash painting: hierarchy by ink tone and weight rather than hue, with indigo and ochre "
         "washes and a red seal as the only accents.")
THEMES = [
    dict(slug="ShuimoNight", id="d0198ed2-7c27-4292-aaa9-223f5e940357", palette=SHN),
    dict(slug="ShuimoDay", id="d01fd083-b939-4c37-8ab7-1d93400fd3a3", palette=SHD),
]
