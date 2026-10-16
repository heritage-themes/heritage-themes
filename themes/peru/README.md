# Peru

Two dark themes based on the natural dyes of Andean weaving, as practised in Chinchero and the Sacred Valley, each painting the whole IDE in a dyed-through ground. Provides two UI themes, **Peru Kulli** and **Peru Puka**, each with a matching editor colour scheme.

![Preview](preview.png)

## Inspiration

Peru Kulli is *kulli sara*, the purple corn (maíz morado) of chicha morada. Peru Puka (*puka*, red) is the crimson of cochineal (cochinilla), the insect dye gathered from the prickly-pear cactus. The syntax colours are the other dyes of the weavers' palette and the Quechua colour words:

| Colour | Source | Peru Kulli | Peru Puka |
| --- | --- | --- | --- |
| Q'olle yellow (*q'illu*) | Flowers of the q'olle shrub (*Buddleja coriacea*) | Keywords, caret, Run button | Strings |
| Ch'illka green (*q'umir*) | Leaves of the ch'illka shrub (*Baccharis*) | Strings | Keywords, caret, Run button |
| Ch'illka ochre | Ch'illka, which also dyes ochres | Annotations | Annotations |
| Anqas blue | Tara pods and quinsa k'ucho leaves | Types | Types |
| Willapi orange | Quechua word for orange | Methods | Numbers |
| Cochineal pink | Cochineal shifted with lime juice | Numbers | |
| Winikunka turquoise | Mineral bands of Rainbow Mountain | Fields, type parameters | Methods, constants |
| Kulli violet | Purple corn | | Fields |
| Yuraq white | Undyed alpaca | Text, Spock labels | Text, Spock labels |

No syntax colour uses the hue of its ground: no purple on Peru Kulli and no red on Peru Puka. Hex values are interpretations of the traditional colours, adjusted for contrast against each background.

## Develop

The palettes are in `theme.py`. The colour mappings and the preview are shared by every theme family and live in [`heritage/`](../../heritage/). See the [root README](../../README.md) for build, preview and install steps.
