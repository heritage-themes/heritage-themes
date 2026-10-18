"""Gujarat palettes. See heritage/__init__.py for what a theme.py defines."""

# Gujarat: Navratri nights, the white Rann of Kutch, patola silk and kite-filled Uttarayan skies.
# Navratri is the nine nights of garba, danced in mirror-worked (abhla) Kutchi cloth under the lights;
# Rann is the salt desert of Kutch, a cool white plain under a pale sky.
# Patola parrot-green keywords, patola red types, haldi turmeric methods, garba rani-pink strings,
# Kutch peacock turquoise numbers, kite-sky blue fields, lilac annotations, Uttarayan kite-orange
# constants, stepwell-sandstone type parameters. Spock labels and the Navratri caret are
# the silver glint of abhla mirrors.
NAVRATRI = dict(
    name="Gujarat Navratri (Dark)", dark=True, parent="Darcula",
    bg="18141F", bgUi="14101A", bgTool="16121D", frame="2C2438", surface="211B2A", hover="2A2334",
    border="2C2537", fg="F2ECE4", muted="938B9C", disabled="5E5768",
    caretRow="1E1926", selection="382E4C", selInactive="2D2639", lineNo="524A5E", lineNoCaret="E8F0F5",
    guide="221C2B", guideSel="3E3549",
    keyword="7FDC78", string="F28AC0", number="4FD1C9", type="FF7068", method="F5CF4A", call="E8D7A0",
    field="6FB8F5", constant="FFA04A", annotation="C7A0F0", label="BFD6EA",
    comment="8A8294", doc="A8957E", docTag="C4AD8C", op="B8B0BC", param="F2ECE4", typeParam="E3B08A",
    gold="F5CF4A", red="C0283A", redText="FFF4EE", azure="6FB8F5", caret="E8F0F5",
    error="FF5468", warning="F5A93A", weak="8C7B58",
    searchBg="4A3E18", searchBorder="F5CF4A", underCaret="2A3452", writeCaret="4C2230",
    braceBg="2D4A38", todo="F5CF4A",
    added="6BB070", modified="6A8FDC", deleted="C85060",
    diffIns="1E3024", diffMod="1E2440", diffDel="3C1A26", diffConf="3A3218", fileYellow="2A231D",
    ansiRed="FF7068", ansiGreen="7FDC78", ansiYellow="F5CF4A", ansiBlue="6FB8F5", ansiMagenta="F28AC0", ansiCyan="4FD1C9",
)
RANN = dict(
    name="Gujarat Rann (Light)", dark=False, parent="Default",
    bg="F5F7F8", bgUi="E6ECEF", bgTool="EDF1F3", frame="D1DCE2", surface="FFFFFF", hover="DAE2E7",
    border="D0D9DF", fg="1E2226", muted="56616B", disabled="A2ABB2",
    caretRow="EDF1F4", selection="F7DCE8", selInactive="E6E3EA", lineNo="A3ACB4", lineNoCaret="B0202A",
    guide="E5EAEE", guideSel="C9D3DA",
    keyword="2E7A1E", string="B0206A", number="00756E", type="B0202A", method="7A5800", call="6B5418",
    field="1A5FA8", constant="B04A00", annotation="7A3AB0", label="3A5A78",
    comment="67707A", doc="6E6248", docTag="564A2E", op="525A62", param="1E2226", typeParam="8A5530",
    gold="8C6D06", red="B0202A", redText="FFF6F4", azure="1A5FA8", caret="B0202A",
    error="D01E2E", warning="A86A00", weak="A8955E",
    searchBg="F5DC8C", searchBorder="B08A10", underCaret="D6E4F5", writeCaret="F7D6DC",
    braceBg="CDE8CF", todo="7A5800",
    added="5FA05A", modified="5A80D0", deleted="C85A5A",
    diffIns="E0F0DA", diffMod="DCE6F5", diffDel="F8DCDE", diffConf="F5E8C4", fileYellow="F5EED2",
    ansiRed="B0202A", ansiGreen="2E7A1E", ansiYellow="7A5800", ansiBlue="1A5FA8", ansiMagenta="B0206A", ansiCyan="00756E",
)

FAMILY = "Gujarat"
BLURB = ("Gujarat's Navratri, Rann of Kutch and patola silk: parrot-green keywords, patola-red types, "
         "turmeric methods and garba-pink strings, on a mirror-worked night or the white salt desert.")
THEMES = [
    dict(slug="GujaratNavratri", id="8c1c5a22-b165-4325-a140-a494c114f397", palette=NAVRATRI),
    dict(slug="GujaratRann", id="f28b26bf-f558-40a3-99ce-8649cf6f53af", palette=RANN),
]
