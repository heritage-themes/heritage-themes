"""Łowicz palettes. See heritage/__init__.py for what a theme.py defines."""

# Łowicz: the striped wool (pasiak łowicki) of the Księżacy and the layered paper cut-outs (wycinanka
# łowicka) cut in the same colours. The pasiak alternates a wide ground stripe with sets of narrow
# stripes; its ground turned from red to orange around 1900, and the narrow stripes were shaded in greens
# and enriched with cinnabar, white and violet. Pomarańczowy (orange, the ground) keywords, zielony
# (green) strings, szmaragdowy (emerald) types, fioletowy (violet) methods, żółty (yellow) fields,
# cynober (cinnabar) numbers and constants, różowy (pink, also a colour of the men's trousers)
# annotations, szary (grey) comments. Wycinanka is the black template a cut-out is layered on;
# Kodra is the long white paper strip the cut-out village scenes are pasted along.
WYCINANKA = dict(
    name="Łowicz Wycinanka", dark=True, parent="Darcula", parentTheme="ExperimentalDark",
    bg="171616", bgUi="121111", bgTool="141313", surface="201F1E", hover="2A2827",
    border="312E2C", fg="EEEBE4", muted="9A958C", disabled="5E5A55",
    caretRow="201E1C", selection="3A3128", selInactive="2C2926", lineNo="58544E", lineNoCaret="F49A48",
    guide="232120", guideSel="3B3733",
    keyword="F49A48", string="A6D66E", number="F7786A", type="4FD0A6", method="C9A2F5", call="C9B0F5",
    field="EDD660", constant="F7786A", annotation="F290C8", label="F7786A",
    comment="8E897F", doc="A39C8C", docTag="C4BBA6", op="B5B0A8", param="EEEBE4", typeParam="92E0C4",
    gold="EDD660", red="B04A10", redText="FFF8F0", azure="80BEF5", caret="F49A48",
    error="FF6B5E", warning="E8A33A", weak="8A7D5C",
    searchBg="4A3D16", searchBorder="EDD660", underCaret="22354A", writeCaret="47261F",
    braceBg="25402C", todo="EDD660",
    added="6FAE68", modified="5E98D6", deleted="C8605A",
    diffIns="1C3020", diffMod="1A2A3C", diffDel="3E211C", diffConf="3A3218", fileYellow="221F1A",
    ansiRed="F07E70", ansiGreen="95D27E", ansiYellow="EDD660", ansiBlue="7FB0F5", ansiMagenta="D795D8", ansiCyan="6DCFD8",
)
KODRA = dict(
    name="Łowicz Kodra", dark=False, parent="Default", parentTheme="ExperimentalLight",
    bg="F8F7F3", bgUi="EDEBE5", bgTool="F2F0EB", surface="FDFCFA", hover="E4E1D9",
    border="D8D4CA", fg="1E1D1B", muted="6C6862", disabled="A9A49B",
    caretRow="F0EEE8", selection="F3DDC6", selInactive="E6E3DC", lineNo="A8A398", lineNoCaret="AE4A00",
    guide="E7E4DC", guideSel="CCC6BA",
    keyword="AE4A00", string="3C7412", number="C0281A", type="00775A", method="7230B8", call="5E3A94",
    field="806200", constant="C0281A", annotation="A8287A", label="C0281A",
    comment="837E75", doc="6E6650", docTag="524B38", op="55524C", param="1E1D1B", typeParam="1A7058",
    gold="9A7400", red="B04A00", redText="FFF9F2", azure="1F64B4", caret="AE4A00",
    error="C42020", warning="A86800", weak="A8955E",
    searchBg="F0DC8A", searchBorder="9A7400", underCaret="D4E2F0", writeCaret="F2D4CC",
    braceBg="D2E6CC", todo="8A5A00",
    added="5E9A50", modified="4F7FC0", deleted="C05050",
    diffIns="DDEACB", diffMod="D8E2EE", diffDel="F2D6CC", diffConf="EEE0B4", fileYellow="F1EDDF",
    ansiRed="A3201E", ansiGreen="2D6B26", ansiYellow="7A5800", ansiBlue="1F55A8", ansiMagenta="8E2A90", ansiCyan="0A6A78",
)

FAMILY = "Łowicz"
BLURB = ("The striped wool and layered paper cut-outs of Łowicz: orange keywords, green strings, emerald types "
         "and violet methods with yellow fields and cinnabar numbers, on a black template or a white paper strip.")
THEMES = [
    dict(slug="LowiczWycinanka", id="b3e62f34-826f-4189-b390-59c012e6c37b", palette=WYCINANKA),
    dict(slug="LowiczKodra", id="25a2ba09-da18-46d9-97d2-d822c33b8204", palette=KODRA),
]
