# Yolŋu

Dark and light themes based on the ochres of Yolŋu bark painting from north-east Arnhem Land, Australia. Provides two UI themes, **Yolŋu Galawu (Dark)** and **Yolŋu Gapaṉ (Light)**, each with a matching editor colour scheme.

![Preview](preview.png)

## Inspiration

Yolŋu artists paint on *galawu*, sheets of stringybark (*gaḏayka'*), with pigments ground from rock on a stone and mixed with water and fixative. The four primary colours are red, yellow, white and black; *guwarguwarmirri*, pure ochres mixed, gives further shades such as pink. Fine cross-hatching makes the painted surface *bir'yun*: shimmering, like light on water. The themes take only the colours; *miny'tji*, the ancestral designs, belong to particular clans.

| Colour | Name | Role |
| --- | --- | --- |
| Dark red ochre | *miku'* | Keywords, Spock labels; buttons and the Run widget |
| Dark yellow ochre | *gangul* | Strings |
| Yellowish-red clay | *galaŋarr'* | Types, links |
| Reddish-brown to purple haematite | *ratjpa* | Fields |
| Mixed ochres, pink | *guwarguwarmirri* | Numbers, constants, annotations |
| White clay | *gapaṉ* | Method declarations and calls in Yolŋu Galawu (Dark); the ground of Yolŋu Gapaṉ (Light) |
| Charcoal black | *gurrŋan'* | Method declarations and calls in Yolŋu Gapaṉ (Light) |

Yolŋu Galawu (Dark) has the dark stringybark as its ground; Yolŋu Gapaṉ (Light) has white clay. Every syntax colour stays within the ochres. Ochres vary by site and by artist; hex values are interpretations of the pigments, adjusted for contrast against each background. Yolŋu words follow the [Yolŋu Matha dictionary](https://yolngudictionary.cdu.edu.au/) of Charles Darwin University.

## Develop

The palettes are in `theme.py`. The colour mappings and the preview are shared by every theme family and live in [`heritage/`](../../heritage/). See the [root README](../../README.md) for build, preview and install steps.
