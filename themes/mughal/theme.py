"""Mughal palettes. See heritage/__init__.py for what a theme.py defines."""

# Mughal miniature painting (16th-17th c. ateliers of Akbar, Jahangir and Shah Jahan):
# precious pigments ground by hand and laid on burnished wasli paper. Each syntax role takes one:
# lajvard lapis-lazuli keywords, shangarf vermilion types, zar gold-leaf methods,
# zangar verdigris strings, peori Indian-yellow numbers, lac crimson fields,
# lapis-and-lac purple constants, azurite annotations, malachite type parameters.
# The canvas is a lamp-lit night scene or burnished wasli; the UI chrome takes the salmon-buff
# of the hashiya margins. Spock labels are gold lettering, and the primary
# accent is lapis ruled with gold, like the jadwal borders of an album page.
NIGHT = dict(
    name="Mughal Night", dark=True, parent="Darcula",
    bg="1D1A16", bgUi="181511", bgTool="1B1814", frame="302A22", surface="26221C", hover="2E2922",
    border="302A22", fg="EDE4D0", muted="8C8475", disabled="5E584D",
    caretRow="231F1A", selection="2E3352", selInactive="2A2A33", lineNo="544D42", lineNoCaret="E8C25E",
    guide="28241E", guideSel="433C31",
    keyword="8E9CFA", string="7CCBA6", number="F2A64A", type="F2785C", method="E8C25E", call="D9C79A",
    field="E592B4", constant="B99AF0", annotation="7CC6E6", label="F2D27A",
    comment="878072", doc="A0917A", docTag="BDA987", op="B3AB9C", param="EDE4D0", typeParam="A6D483",
    gold="E3BE5E", red="34419E", redText="F5EDDA", azure="7CC6E6", caret="E8C25E",
    error="F25A5A", warning="E8A33A", weak="8A7C55",
    searchBg="4A3D1A", searchBorder="E3BE5E", underCaret="2B3352", writeCaret="4A2824",
    braceBg="2D4636", todo="E8C25E",
    added="6BA36A", modified="6878D0", deleted="B5574A",
    diffIns="1E2E22", diffMod="1F2340", diffDel="37201C", diffConf="383019", fileYellow="2D2617",
    ansiRed="F2785C", ansiGreen="7CCBA6", ansiYellow="E8C25E", ansiBlue="8E9CFA", ansiMagenta="E592B4", ansiCyan="7CC6E6",
)
WASLI = dict(
    name="Mughal Wasli", dark=False, parent="Default",
    bg="F7F1E3", bgUi="ECDDCB", bgTool="F0E4D3", frame="E3CDB8", surface="FBF6EC", hover="E2D1BB",
    border="D9C6AE", fg="221F2B", muted="6F6676", disabled="A99E96",
    caretRow="F0E7D5", selection="D3D9F2", selInactive="E4E0E2", lineNo="AE9F92", lineNoCaret="2B3BA6",
    guide="EAE0CD", guideSel="D2BFA3",
    keyword="2B3BA6", string="1E6E55", number="A3500A", type="B0301E", method="7A5800", call="6E5520",
    field="992D82", constant="5E2F9A", annotation="136A8F", label="8A6400",
    comment="7A7068", doc="6E5E44", docTag="594A30", op="57505A", param="221F2B", typeParam="3E7A1E",
    gold="B8860B", red="2B3BA6", redText="FBF4E4", azure="136A8F", caret="2B3BA6",
    error="C8202F", warning="A86800", weak="A8975E",
    searchBg="F0D68A", searchBorder="B8860B", underCaret="D6DCF2", writeCaret="F2D2CC",
    braceBg="CDE4D6", todo="7A5800",
    added="5E9A5A", modified="5868C0", deleted="C0574B",
    diffIns="DDEBD6", diffMod="DADFF4", diffDel="F2D8D2", diffConf="EFE2BF", fileYellow="F5E8C4",
    ansiRed="B0301E", ansiGreen="1E6E55", ansiYellow="7A5800", ansiBlue="2B3BA6", ansiMagenta="992D82", ansiCyan="136A8F",
)

FAMILY = "Mughal"
BLURB = ("Mughal miniature painting: lapis-lazuli keywords, vermilion types, gold-leaf methods and "
         "verdigris strings on a lamp-lit night or burnished wasli paper, with Spock labels lettered "
         "in gold.")
THEMES = [
    dict(slug="MughalNight", id="6dbb510f-40e4-48e5-a8cc-24aed070ad86", palette=NIGHT),
    dict(slug="MughalWasli", id="4936cec7-a3b0-439a-9a27-3c8ac49ba973", palette=WASLI),
]
