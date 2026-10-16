# Kalamkari

Dark and light themes based on Kalamkari (కలంకారి, "pen work"), the craft of painting cotton by hand with a bamboo pen and natural dyes, as practised in Srikalahasti and Machilipatnam. Provides two UI themes, **Kalamkari Indigo** and **Kalamkari Cotton**, each with a matching editor colour scheme.

![Preview](preview.png)

## Inspiration

Every colour is a dye or mordant the craft uses, kept as muted as the dyes:

| Dye | What it is | Role |
| --- | --- | --- |
| Madder over indigo | Indigo overdyed with madder, aubergine | Keywords |
| Indigo (neel) | Leaf dye from the indigo vat | Types |
| Madder (chay root) | Root dye, red on an alum mordant | Method declarations, Spock labels |
| Alum madder | Madder on a light alum mordant, rose | Method calls |
| Myrobalan (harad) | Fruit of the myrobalan tree, yellow | Strings |
| Catechu (kattha) | Acacia extract, brown | Numbers |
| Indigo over myrobalan | Yellow overdyed with indigo, green | Fields |
| Iron-saddened myrobalan | Myrobalan yellow dulled with iron, olive | Constants |
| Indigo wash | Light indigo, teal | Annotations |
| Kasimi | Iron-black outline ink | Text on Kalamkari Cotton |

Kalamkari Indigo sets the code on cloth from the indigo vat. Kalamkari Cotton sets it on unbleached cotton. Hex values are interpretations of the traditional colours, adjusted for contrast against each background.

## Develop

The palettes are in `theme.py`. The colour mappings and the preview are shared by every theme family and live in [`heritage/`](../../heritage/). See the [root README](../../README.md) for build, preview and install steps.
