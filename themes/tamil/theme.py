"""Tamil palettes. See heritage/__init__.py for what a theme.py defines."""

# Tamil Nadu: the kolam at the threshold, the palm-leaf manuscript and the Kanchipuram loom.
# Kolam is rice-flour white drawn at dawn on a dark granite threshold;
# Olai is the palm leaf (olai chuvadi) that carried Tamil literature, its letters blackened with lampblack.
# Syntax colours take the Tamil names of Kanchipuram silk shades:
# mayil kazhuthu (peacock neck) keywords, mambazham (mango) strings, kili pachai (parrot green) numbers,
# arakku (lac red) types, neelam (sapphire) methods, vadamalli (globe amaranth) fields,
# kathiri poo (brinjal flower) constants, maragatham (emerald) annotations,
# manthalir (tender mango leaf, copper pink) type parameters. Spock labels are kumkumam vermilion.
KOLAM = dict(
    name="Tamil Kolam (Dark)", dark=True, parent="Darcula",
    bg="181C1C", bgUi="141717", bgTool="161A1A", frame="272D2D", surface="202525", hover="283030",
    border="2A3131", fg="F2EFE6", muted="8D9592", disabled="59615F",
    caretRow="1E2323", selection="2A3E44", selInactive="253234", lineNo="4C5655", lineNoCaret="EBC35A",
    guide="202626", guideSel="3A4444",
    keyword="44D4E2", string="FFB348", number="92D36C", type="FE949D", method="9BBEFF", call="A8CEFF",
    field="F09BE8", constant="C9ACFF", annotation="7DDEB6", label="FF9878",
    comment="828B88", doc="A3987E", docTag="BFAF8E", op="B4B8B4", param="F2EFE6", typeParam="FEC5B2",
    gold="EBC35A", red="A82838", redText="FFF4EE", azure="7AA8F5", caret="EBC35A",
    error="FF5468", warning="F0A535", weak="8A7F58",
    searchBg="4A3E18", searchBorder="EBC35A", underCaret="22404A", writeCaret="4A2830",
    braceBg="2D4A3A", todo="EBC35A",
    added="68AC66", modified="5B98D0", deleted="C25A5A",
    diffIns="1A3324", diffMod="182C3A", diffDel="3C2024", diffConf="38331A", fileYellow="2A281B",
    ansiRed="EE6E80", ansiGreen="9CD86A", ansiYellow="EBC35A", ansiBlue="7AA8F5", ansiMagenta="D98AE0", ansiCyan="45C6D6",
)
OLAI = dict(
    name="Tamil Olai (Light)", dark=False, parent="Default",
    bg="F3EBD2", bgUi="E7DCBC", bgTool="EDE3C7", frame="DCCEA8", surface="F9F4E4", hover="DDD0AC",
    border="D4C59E", fg="1F1C16", muted="6A6352", disabled="A69C80",
    caretRow="ECE2C6", selection="CFE3E2", selInactive="E0E0D4", lineNo="A79A78", lineNoCaret="0B6672",
    guide="E5DAC0", guideSel="CDBD95",
    keyword="06717A", string="845500", number="3B7402", type="AD2B44", method="2F5EB9", call="456B9B",
    field="913B8C", constant="714CA7", annotation="007654", label="A23100",
    comment="746D5C", doc="6E6040", docTag="564A2E", op="56524A", param="1F1C16", typeParam="905B48",
    gold="B08A10", red="9C1F4A", redText="FFF6EE", azure="1F55A8", caret="0B6672",
    error="C41A2A", warning="A86A00", weak="A8955E",
    searchBg="F0D684", searchBorder="B08A10", underCaret="D0E6E8", writeCaret="F2D2CF",
    braceBg="CFE6C8", todo="7A5800",
    added="5E9A50", modified="4F7FC0", deleted="C05050",
    diffIns="DDEACB", diffMod="D8E2EE", diffDel="F2D6CC", diffConf="EEE0B4", fileYellow="F2E4B7",
    ansiRed="9C1F4A", ansiGreen="366A14", ansiYellow="7A5800", ansiBlue="1F55A8", ansiMagenta="8E2A90", ansiCyan="0B6672",
)

FAMILY = "Tamil"
BLURB = ("Tamil Nadu's kolam, palm-leaf manuscripts and Kanchipuram silk: peacock-neck keywords, mango "
         "strings, lac-red types and sapphire methods, on a dark granite threshold or a palm leaf.")
THEMES = [
    dict(slug="TamilKolam", id="2d46a768-9980-43b1-b7ec-196e2bb4b9ea", palette=KOLAM),
    dict(slug="TamilOlai", id="857b4b12-b716-4b39-bc9a-96261cde9846", palette=OLAI),
]
