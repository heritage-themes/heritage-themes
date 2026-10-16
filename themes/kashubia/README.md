# Kashubia

Dark and light themes based on the seven colours of Kashubian embroidery (*haft kaszubski*) from northern Poland, as fixed by the Żukowo school. Provides two UI themes, **Kashubia Zemia** and **Kashubia Niebò**, each with a matching editor colour scheme.

![Preview](preview.png)

## Inspiration

Żukowo embroidery keeps to seven colours, with the blues always dominant. Each colour is read as part of the Kashubian landscape:

| Colour | Meaning | Role |
| --- | --- | --- |
| Chabrowy (cornflower blue) | The lakes | Keywords, caret |
| Granatowy (navy blue) | The sea | Types, buttons and the Run widget |
| Jasny niebieski (light blue) | The sky | Methods |
| Żółty (yellow; Kashubian *żôłti*) | The sun and ripening grain | Strings |
| Zielony (green; Kashubian *zelony*) | Forests and meadows | Fields (forest), type parameters (meadow) |
| Czerwony (red) | The blood shed in defence of the land | Numbers, constants, Spock labels |
| Czarny (black; Kashubian *czôrny*) | The earth waiting to be sown | Ground of Kashubia Zemia, text of Kashubia Niebò; comments in the brown of the same earth (Kashubian *bruny*) |

Annotations take amber (*bursztyn*), which the yellow also stands for, from the Baltic shore of Kashubia.

Kashubia Zemia (Kashubian *zemia*, earth) has the dark soil as its ground. Kashubia Niebò (Kashubian *niebò*, sky) is daylight on white linen (*białe płótno*), the cloth the embroidery is worked on. Some sources count brown beside or in place of black as the colour of the earth; the table follows the Żukowo set. Hex values are interpretations of the traditional colours, adjusted for contrast against each background.

## Develop

The palettes are in `theme.py`. The colour mappings and the preview are shared by every theme family and live in [`heritage/`](../../heritage/). See the [root README](../../README.md) for build, preview and install steps.
