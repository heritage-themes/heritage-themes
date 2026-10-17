# Mudhif

Dark and light themes based on the *mudhif* (مضيف), the reed guest house of the Marsh Arabs of southern Iraq. Hierarchy comes from the tone and weight of one reed colour, not from hue. Provides two UI themes, **Mudhif Qir (Dark)** and **Mudhif Qasab (Light)**, each with a matching editor colour scheme.

![Preview](preview.png)

## Inspiration

A mudhif is a vault of bundled reed (*qasab*, قصب) arches covered in reed mats, with a coffee hearth in the middle. Gertrude Bell described one as "a perfectly regular and exquisitely constructed yellow tunnel", lit by a willow fire and "fading away into a golden gloom". The Marsh Arabs' canoes, the *mashoof*, are waterproofed with black bitumen, *qir* (قير).

| Element | Treatment |
| --- | --- |
| Method declarations | Palest peeled reed, bold |
| Keywords | Gold of the bundled arches, bold |
| Types | Old amber reed |
| Method calls | A stronger tone than the straw of plain text |
| Fields | A deeper gold than plain text |
| Annotations | Dim reed |
| Strings | Green of new reed shoots |
| Numbers, constants, Spock labels | Willow fire on the hearth |

Mudhif Qir (Dark) has the bitumen black of the mashoof as its ground; Mudhif Qasab (Light) has the peeled reed. Hex values are interpretations of reed, bitumen and firelight, adjusted for contrast against each background.

## Develop

The palettes are in `theme.py`. The colour mappings and the preview are shared by every theme family and live in [`heritage/`](../../heritage/). See the [root README](../../README.md) for build, preview and install steps.
