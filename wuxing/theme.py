"""Wuxing palettes. See heritage/__init__.py for what a theme.py defines."""

# Five Elements: Fire=red (keywords), Wood=qing/green (strings), Earth=yellow (types),
# Metal=white -> rice/beige instead of pure white, Water=black -> indigo ink instead of pure black.
# Gold = prosperity (caret, search, Spock labels), purple = Forbidden City (fields),
# azure/blue = trust (methods), turquoise = imperial decorative arts (annotations),
# copper = metals table (numbers), ink-wash grey = restraint (comments).
NIGHT = dict(
    name="Wuxing Night", dark=True, parent="Darcula", parentTheme="ExperimentalDark",
    bg="171B26", bgUi="13161F", bgTool="151923", surface="1E2332", hover="242A3B",
    border="262C3D", fg="E6DCC8", muted="8A8577", disabled="5C5F6B",
    caretRow="1C2130", selection="2D3754", selInactive="252C40", lineNo="4A5064", lineNoCaret="C9A24A",
    guide="232838", guideSel="3A4258",
    keyword="E8705F", string="8CC88E", number="E39A62", type="F0D47A", method="74B4E6", call="9AC6EA",
    field="C59BE3", constant="B48CE6", annotation="45BFC8", label="E8BE52",
    comment="6F7789", doc="9E8C70", docTag="B8A27C", op="B9B09E", param="E6DCC8", typeParam="7FD3C9",
    gold="D9A93F", red="C8473A", redText="F3E7D3", azure="74B4E6",
    error="F0536A", warning="E8A13A", weak="8A7A50",
    searchBg="4A3E1C", searchBorder="D9A93F", underCaret="2C3A55", writeCaret="4A2B2E",
    braceBg="3A4A3A", todo="E2B84C",
    added="4C8A57", modified="5878B0", deleted="9A4A44",
    diffIns="20331F", diffMod="1D2840", diffDel="3A1E22", diffConf="3A3020", fileYellow="352E1B",
)
DAY = dict(
    name="Wuxing Day", dark=False, parent="Default", parentTheme="ExperimentalLight",
    bg="F6F0E1", bgUi="EDE5D2", bgTool="F0E9D8", surface="FBF7EC", hover="E4DAC3",
    border="D9CEB6", fg="2B3040", muted="7A7566", disabled="ADA694",
    caretRow="EFE6D1", selection="D3DBEE", selInactive="E0E2E6", lineNo="B3AA94", lineNoCaret="A0700A",
    guide="E6DDC8", guideSel="CDBF9F",
    keyword="B0362B", string="2A7244", number="A04A15", type="6E5A10", method="1F5FA8", call="2F6DB0",
    field="7B3FA6", constant="6A2F96", annotation="0A7480", label="7A5200",
    comment="7E7C72", doc="7D6845", docTag="6E5A3A", op="5A5A5A", param="2B3040", typeParam="0F7A72",
    gold="C8962A", red="B0362B", redText="FBF3E4", azure="1F5FA8",
    error="D0283E", warning="C27A00", weak="B3A06A",
    searchBg="F3D98A", searchBorder="C8962A", underCaret="D6E2F2", writeCaret="F2D6D0",
    braceBg="CFE6CF", todo="8A5E00",
    added="6AA672", modified="6C8CC4", deleted="C46A60",
    diffIns="E2F0DC", diffMod="DDE6F4", diffDel="F5DCD8", diffConf="F3E6C4", fileYellow="F2E1B0",
)

FAMILY = "Wuxing"
BLURB = ("Chinese colour symbolism and the Five Elements: vermilion keywords (Fire), jade strings (Wood), "
         "imperial-yellow types (Earth), and a rice-paper or indigo-ink canvas in place of stark white and "
         "black (Metal and Water).")
THEMES = [
    dict(slug="WuxingNight", id="93584a5e-9007-4988-b46f-2262fc35943a", palette=NIGHT),
    dict(slug="WuxingDay", id="4b15b1a7-f789-4a43-851a-8b3f5bb0a4cf", palette=DAY),
]
