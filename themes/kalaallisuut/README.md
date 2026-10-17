# Kalaallisuut

Dark and light themes based on the West Greenlandic national dress, *kalaallisuut*. Provides two UI themes, **Kalaallisuut Qernertoq (Dark)** and **Kalaallisuut Qaqortoq (Light)**, each with a matching editor colour scheme.

![Preview](preview.png)

## Inspiration

The colours of a woman's *kalaallisuut* show her age and marital status, a custom credited to the Moravian missionaries. The anorak is pink at confirmation, red after marriage and darker after children; married women and widows wear blue. Young women wear white kamiks, older women yellow or dark blue ones. The glass-bead collar has a central band of white, red and blue, edged with green. Festive dress pairs black sealskin with white: the men's white anorak over black trousers is called *qaqortumaartoq*, "dressed in white".

| Colour | Use | Role |
| --- | --- | --- |
| Red, *aappaluttoq* | The married woman's anorak | Keywords, Spock labels; buttons and the Run widget |
| Pink | The confirmation anorak | Strings |
| Yellow, *sungaartoq* | An older woman's kamiks | Numbers, constants |
| Blue, *tungujortoq* | The anorak of married women and widows | Types, annotations |
| Green, *qorsuk* | The edging of the bead collar | Method declarations and calls |
| White, *qaqortoq*, and black, *qernertoq* | Kamiks, festive anorak, sealskin trousers | Fields, against greyer plain text |

Kalaallisuut Qernertoq (Dark) has black sealskin as its ground; Kalaallisuut Qaqortoq (Light) has the white kamik. The colour rules vary between regions and families. Hex values are interpretations of the dyed cloth, beads and skin, adjusted for contrast against each background.

## Develop

The palettes are in `theme.py`. The colour mappings and the preview are shared by every theme family and live in [`heritage/`](../../heritage/). See the [root README](../../README.md) for build, preview and install steps.
