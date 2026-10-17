# Aizome

Dark and light themes based on Japanese indigo dyeing (藍染, *aizome*). The whole palette is a single hue; hierarchy comes from the depth of the dye. Provides two UI themes, **Aizome Kachi** and **Aizome Kamenozoki**, each with a matching editor colour scheme.

![Preview](preview.png)

## Inspiration

Indigo dyers speak of 藍四十八色 ("indigo has forty-eight colours"): each extra dip in the vat gives a deeper, named shade, from 甕覗 *kamenozoki* ("a peek into the vat"), the palest, to 褐 *kachi-iro*, the near-black indigo worn under armour. Shallow shades lean green, deep ones violet. Aizome applies the scale to code.

| Shade | Treatment |
| --- | --- |
| Undyed sashiko thread (刺し子) | Declarations, bold; caret, Spock labels |
| 甕覗 *kamenozoki*, palest dip | Types |
| 縹 *hanada*, mid indigo | Plain names, method calls |
| 水浅葱 *mizuasagi*, pale asagi | Fields |
| 浅葱 *asagi*, green-leaning | Strings |
| 紺 *kon*, violet-leaning | Numbers, constants |
| 藍鼠 *ainezumi*, grey indigo | Keywords, punctuation, annotations |
| 藍 *ai*, deep indigo | Comments |

Aizome Kachi has *kachi-iro* as its ground; Aizome Kamenozoki has the palest dip. Errors, warnings and diffs keep their usual colours. Hex values are interpretations of dyed cloth, adjusted for contrast against each background.

## Develop

The palettes are in `theme.py`. The colour mappings and the preview are shared by every theme family and live in [`heritage/`](../../heritage/). See the [root README](../../README.md) for build, preview and install steps.
