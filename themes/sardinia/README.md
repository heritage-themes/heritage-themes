# Sardinia

Dark and light themes based on the traditional dress of Sardinia, Italy: black and scarlet orbace, white linen, saffron-dyed silk and indigo. Provides two UI themes, **Sardinia Orbace (Dark)** and **Sardinia Camisa (Light)**, each with a matching editor colour scheme.

![Preview](preview.png)

## Inspiration

Village dress across the island is built from orbace, a hand-woven wool fulled in water mills, often black or dyed red with madder, and the white linen shirt worn beneath it. The dyes come from plants: madder for red, saffron for yellow, indigo for blue, walnut husk for brown. Desulo embroiders the scarlet wool of its festive dress in red, yellow and blue silk, and Orgosolo dyes the silk of its headscarf with saffron.

| Colour | Source | Role |
| --- | --- | --- |
| Zafferano (saffron) | *Su lionzu*, the silk headscarf of Orgosolo | Keywords, caret, Spock labels |
| Scarlatto (scarlet) | Orbace dyed with *robbia* (madder); the bonnet of Desulo | Strings, buttons and the Run widget |
| Indaco (indigo) | The skirt of Bosa; the blue satin of the Desulo bonnet | Methods, links |
| Mallo di noce (walnut husk) | The brown dye and brown orbace | Fields |
| Corallo (coral) | Red coral in Sardinian jewellery | Numbers, constants, annotations |
| Lino (linen) and orbace | *Sa camisa*, the white linen shirt; black orbace | Types |

Sardinia Orbace (Dark) has black orbace, the cloth of cloaks and skirts, as its ground, with white linen for types. Sardinia Camisa (Light) is the white linen of *sa camisa*, with black orbace for types. Hex values are interpretations of the dyed cloth, silk and coral, adjusted for contrast against each background.

## Develop

The palettes are in `theme.py`. The colour mappings and the preview are shared by every theme family and live in [`heritage/`](../../heritage/). See the [root README](../../README.md) for build, preview and install steps.
