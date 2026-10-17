"""Złotnica palettes. See heritage/__init__.py for what a theme.py defines."""

# Złotnica (also złotogłów): the Kashubian bonnet (czepiec kaszubski), velvet embroidered in raised gold
# and silver thread, a craft of the Żukowo and Żarnowiec convents. Hierarchy by metal, tone and weight,
# not hue: gold for the structure (keywords deep gold, method declarations bright gold and bold, types
# pale gilded silver), silver for names (plain text mid silver, calls bright, fields dim). The other
# velvets of the bonnets add the only colour: szafir (sapphire) strings, bordowy (burgundy) numbers and
# constants, szmaragd (emerald) annotations. Aksamit is the dark green velvet of the bonnet;
# Płótno is the white linen of the napkins (serwety) embroidered with the bonnet patterns in gold thread.
AKSAMIT = dict(
    name="Złotnica Aksamit", dark=True, parent="Darcula", kwBold=False,
    bg="10201A", bgUi="0C1A15", bgTool="0E1D17", frame="1C3127", surface="172A22", hover="1F332A",
    border="243A30", fg="C6CBC4", muted="86948C", disabled="52625A",
    caretRow="152820", selection="24403A", selInactive="22352E", lineNo="4A5E54", lineNoCaret="E8C35E",
    guide="182C24", guideSel="2E463B",
    keyword="CFA64E", string="A9C2EC", number="E89CAE", type="E2C98A", method="F4D06A", call="ECEEE8",
    field="A2ADA6", constant="E89CAE", annotation="7ED1AA", label="F4D06A",
    comment="6F8A7D", doc="8A9C88", docTag="A9B9A2", op="98A49D", param="C6CBC4", typeParam="E2C98A",
    gold="E8C35E", red="8A6A1E", redText="FBF5E4", azure="A9C2EC", caret="E8C35E",
    error="FF7B7B", warning="E8A848", weak="8C8457",
    searchBg="463C14", searchBorder="E8C35E", underCaret="20383F", writeCaret="402630",
    braceBg="2A4A3A", todo="E8C35E",
    added="72B07A", modified="6E9CD2", deleted="CF6A6A",
    diffIns="183424", diffMod="172C38", diffDel="38202A", diffConf="35311A", fileYellow="1C2A1E",
    ansiRed="F08080", ansiGreen="8FD496", ansiYellow="E8C35E", ansiBlue="8DB4F0", ansiMagenta="DA9AD8", ansiCyan="74D0D0",
)
PLOTNO = dict(
    name="Złotnica Płótno", dark=False, parent="Default", kwBold=True,
    bg="F6F2E6", bgUi="ECE6D6", bgTool="F1ECDE", frame="DFD6C1", surface="FBF8F0", hover="E3DCC8",
    border="D9D0BA", fg="383B38", muted="6F6E68", disabled="ABA796",
    caretRow="EFEADB", selection="E5DDC0", selInactive="E6E3D8", lineNo="ABA48E", lineNoCaret="8A6400",
    guide="E6E0CF", guideSel="CCC2A8",
    keyword="8A6400", string="2A4F8E", number="8E2438", type="5E4C1C", method="6E4E00", call="0F1111",
    field="5C6460", constant="8E2438", annotation="16684C", label="8A6400",
    comment="878171", doc="6F6A55", docTag="514B36", op="5E5E58", param="383B38", typeParam="5E4C1C",
    gold="A07A10", red="7A5A08", redText="FCF7EA", azure="2A4F8E", caret="8A6400",
    error="C42020", warning="A86800", weak="A8955E",
    searchBg="F0DC8A", searchBorder="A07A10", underCaret="DCE3EA", writeCaret="F0D6D8",
    braceBg="D6E6D8", todo="7A5A08",
    added="5E9A50", modified="4F7FC0", deleted="C05050",
    diffIns="DDEACB", diffMod="D8E2EE", diffDel="F2D6D4", diffConf="EEE0B4", fileYellow="F0E9D2",
    ansiRed="A82A2A", ansiGreen="2F6B2F", ansiYellow="7A5800", ansiBlue="1F55A8", ansiMagenta="8E2A80", ansiCyan="0A6A70",
)

FAMILY = "Złotnica"
BLURB = ("The gold-and-silver embroidered bonnets of Kashubia: hierarchy by metal, tone and weight, with "
         "sapphire, burgundy and emerald velvet as the only colours, on green velvet or white linen.")
THEMES = [
    dict(slug="ZlotnicaAksamit", id="7a641ae2-a946-45fb-93a7-455df5788340", palette=AKSAMIT),
    dict(slug="ZlotnicaPlotno", id="b4451bbc-508c-48aa-b613-4914c2e37f61", palette=PLOTNO),
]
