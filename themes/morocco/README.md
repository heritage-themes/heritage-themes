# Morocco

Three dark themes based on the colours of Moroccan walls, each painting the whole IDE in a saturated wall colour. Provides three UI themes, **Morocco Majorelle**, **Morocco Marrakech** and **Morocco Zellige**, each with a matching editor colour scheme.

![Preview](preview.png)

## Inspiration

Each theme takes one wall and the colours set against it:

| Theme | Wall | Syntax colours |
| --- | --- | --- |
| Morocco Majorelle | Majorelle blue, the ultramarine of Jacques Majorelle's garden in Marrakech | Yellow of its pots for keywords and the Run button, cactus green for strings |
| Morocco Marrakech | Red clay (pisé) of the medina walls of Marrakech (مراكش) | Turquoise of its doors for keywords and the Run button, mint-tea green for strings |
| Morocco Zellige | Deep jade of glazed mosaic tile, zellige (الزليج) | Poppy coral for keywords and the Run button, tile turquoise for strings, cobalt for types |

No syntax colour uses the hue of its wall, which would vibrate or vanish against it. Spock labels are bold off-white, like whitewash. Hex values are interpretations of the traditional colours, adjusted for contrast against each background.

## Develop

The palettes are in `theme.py`. The colour mappings and the preview are shared by every theme family and live in [`heritage/`](../../heritage/). See the [root README](../../README.md) for build, preview and install steps.
