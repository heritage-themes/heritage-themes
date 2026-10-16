# Holi

Dark and light themes based on Holi (होली), the Indian festival of colours. Provides two UI themes, **Holi Night** and **Holi Day**, each with a matching editor colour scheme.

![Preview](preview.png)

## Inspiration

Each syntax role takes one colour of gulal (गुलाल), the powder thrown at Holi, at full strength:

| Colour | Meaning | Role |
| --- | --- | --- |
| Gulabi (गुलाबी) | Pink | Keywords |
| Kesari (केसरी) | Saffron | Strings |
| Haldi (हल्दी) | Turmeric yellow | Numbers, Spock labels |
| Hara (हरा) | Green | Types |
| Neela (नीला) | Blue | Methods |
| Jamuni (जामुनी) | Purple of the jamun fruit | Fields |
| Firozi (फ़िरोज़ी) | Turquoise | Constants |
| Lal (लाल) | Red | Annotations |
| Ember | Holika bonfire | Caret on Holi Night |

Holi Night is Holika Dahan (होलिका दहन), the bonfire eve: ash and embers. Holi Day is Rangwali Holi, the day after, when gulal is thrown over white cotton. Hex values are interpretations of the traditional colours, adjusted for contrast against each background.

## Develop

The palettes are in `theme.py`. The colour mappings and the preview are shared by every theme family and live in [`heritage/`](../heritage/). See the [root README](../README.md) for build, preview and install steps.
