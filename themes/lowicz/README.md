# Łowicz

Dark and light themes based on the striped wool (*pasiak łowicki*) and layered paper cut-outs (*wycinanka łowicka*) of the Łowicz region in central Poland. Provides two UI themes, **Łowicz Wycinanka (Dark)** and **Łowicz Kodra (Light)**, each with a matching editor colour scheme.

![Preview](preview.png)

## Inspiration

The pasiak of the Księżacy, the people of the Łowicz region, alternates a wide ground stripe with sets of narrow stripes. The ground was dark red in the early 19th century and turned orange around 1900. The narrow stripes were shaded in greens and set off with cinnabar, white and violet; aniline dyes later brought emerald and other cool colours. Cut-outs are layered from the same bright papers, the largest piece first.

| Colour | Source | Role |
| --- | --- | --- |
| Pomarańczowy (orange) | The ground stripe from about 1900 | Keywords, caret, buttons and the Run widget |
| Zielony (green) | The narrow stripes | Strings |
| Szmaragdowy (emerald) | The cool stripes of the aniline dyes | Types |
| Fioletowy (violet) | The narrow stripes | Methods |
| Żółty (yellow) | The narrow stripes and the men's trousers | Fields |
| Cynober (cinnabar) | The narrow stripes | Numbers, constants, Spock labels |
| Różowy (pink) | The men's trousers | Annotations |
| Szary (grey) | A ground of the mid-20th century | Comments |

Łowicz Wycinanka (Dark), from *wycinanka* (cut-out), has the black template a cut-out is layered on as its ground. Łowicz Kodra (Light) is the long white paper strip along which cut-out village scenes are pasted. Stripe colours varied by parish and by decade; hex values are interpretations of the dyed wool and papers, adjusted for contrast against each background.

## Develop

The palettes are in `theme.py`. The colour mappings and the preview are shared by every theme family and live in [`heritage/`](../../heritage/). See the [root README](../../README.md) for build, preview and install steps.
