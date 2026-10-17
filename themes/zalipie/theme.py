"""Zalipie palettes. See heritage/__init__.py for what a theme.py defines."""

# Zalipie: the painted cottages of the village near Tarnów. The women first lightened soot-stained walls
# with lime (wapno) and dabbed lime spots on plinths blackened with soot in milk (sadza); the first
# paintings were black, white or brown, from lime, soot and clay (glina). Full-colour flowers came
# later, from powder paints mixed with milk. The early materials carry the structure: plain text in
# lime on soot or soot on lime, glina (clay) keywords, comments in soot thinned with lime. The flowers
# carry the names: róża (rose) methods, liście (leaves) strings, fiolet (violet) types, ultramaryna
# (ultramarine, the blue of window frames and blue flowers) fields, żółty (yellow) numbers and constants,
# błękit (sky blue, the painted stoves) annotations. Sadza is the soot plinth; Wapno is the lime-washed wall.
SADZA = dict(
    name="Zalipie Sadza (Dark)", dark=True, parent="Darcula",
    bg="1C1B1A", bgUi="171615", bgTool="1A1918", frame="2E2B28", surface="252321", hover="2E2C29",
    border="36332F", fg="E6E2DA", muted="938D84", disabled="5E5A54",
    caretRow="242220", selection="2D3954", selInactive="2C2F36", lineNo="5C5750", lineNoCaret="D6A47C",
    guide="262422", guideSel="3E3A35",
    keyword="D6A47C", string="94CC7A", number="EAD06C", type="C8A2EE", method="F27F92", call="F5A9B5",
    field="8EAEF5", constant="EAD06C", annotation="70C4E2", label="F27F92",
    comment="8F8A83", doc="A39D94", docTag="C2BCB1", op="B3AEA6", param="E6E2DA", typeParam="DCC4F4",
    gold="EAD06C", red="3456C8", redText="F6F4EE", azure="8EAEF5", caret="E6E2DA",
    error="FF6B5E", warning="E8A33A", weak="8A7D5C",
    searchBg="4A3D16", searchBorder="EAD06C", underCaret="21354A", writeCaret="47261F",
    braceBg="25402C", todo="EAD06C",
    added="6FAE68", modified="5E98D6", deleted="C8605A",
    diffIns="1C3020", diffMod="1A2A3C", diffDel="3E211C", diffConf="3A3218", fileYellow="26241E",
    ansiRed="F07E70", ansiGreen="95D27E", ansiYellow="EAD06C", ansiBlue="7FB0F5", ansiMagenta="D795D8", ansiCyan="6DCFD8",
)
WAPNO = dict(
    name="Zalipie Wapno (Light)", dark=False, parent="Default",
    bg="F2F4F3", bgUi="E6E9E8", bgTool="EDEFEE", frame="D6DAD9", surface="FAFBFB", hover="DDE1E0",
    border="D0D5D4", fg="242220", muted="6A6863", disabled="A6A8A4",
    caretRow="EAEDEC", selection="D2DCF0", selInactive="E0E3E4", lineNo="A2A6A3", lineNoCaret="8C4A22",
    guide="E2E6E5", guideSel="C6CCCA",
    keyword="8C4A22", string="2E6E1E", number="7A5C00", type="7430A8", method="B01E4A", call="94304E",
    field="2440B0", constant="7A5C00", annotation="0A6688", label="B01E4A",
    comment="7E7A74", doc="6A665F", docTag="4C4944", op="55534F", param="242220", typeParam="5A2C96",
    gold="8A6A00", red="2A48B8", redText="F7F8FA", azure="2A50B8", caret="242220",
    error="C42020", warning="9A5F00", weak="A8955E",
    searchBg="F0DC8A", searchBorder="8A6A00", underCaret="D4E2F0", writeCaret="F2D4D8",
    braceBg="D2E6CC", todo="8A5A00",
    added="5E9A50", modified="4F7FC0", deleted="C05050",
    diffIns="DDEACB", diffMod="D8E2EE", diffDel="F2D6D4", diffConf="EEE0B4", fileYellow="ECEDE2",
    ansiRed="A3201E", ansiGreen="2D6B26", ansiYellow="7A5800", ansiBlue="1F55A8", ansiMagenta="8E2A90", ansiCyan="0A6A78",
)

FAMILY = "Zalipie"
BLURB = ("The painted cottages of Zalipie: lime, soot and clay for text, keywords and comments, and the flowers "
         "for names, with rose methods, leaf-green strings and violet types, on a soot plinth or a lime-washed wall.")
THEMES = [
    dict(slug="ZalipieSadza", id="66e66352-3d07-4c83-82eb-537f5dec54e7", palette=SADZA),
    dict(slug="ZalipieWapno", id="233451a8-8d42-47a0-8f6a-7a6f67d57c7b", palette=WAPNO),
]
