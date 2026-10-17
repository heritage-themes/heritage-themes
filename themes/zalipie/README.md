# Zalipie

Dark and light themes based on the painted cottages of Zalipie, a village near Tarnów in southern Poland. The early materials, lime, soot and clay, carry the text; the painted flowers carry the names. Provides two UI themes, **Zalipie Sadza (Dark)** and **Zalipie Wapno (Light)**, each with a matching editor colour scheme.

![Preview](preview.png)

## Inspiration

The women of Zalipie lightened soot-stained walls with lime and dabbed lime spots on plinths blackened with soot mixed in milk. The first paintings were black, white or brown, from lime, soot and clay. Flowers in full colour came later, painted with powder paints mixed with milk.

| Element | Source | Role |
| --- | --- | --- |
| Wapno, sadza (lime, soot) | The first black-and-white paintings | Plain text: lime on soot, soot on lime |
| Glina (clay) | The first brown paintings | Keywords |
| Szarość (grey) | Soot-stained walls before whitewashing | Comments |
| Róża (rose) | The central flower of a bouquet | Methods, Spock labels |
| Liście (leaves) | Leaves and stems | Strings |
| Ultramaryna (ultramarine) | Window frames and blue flowers | Fields, buttons and the Run widget |
| Fiolet (violet) | Violet flowers | Types |
| Żółty (yellow) | Yellow flowers and flower centres | Numbers, constants |
| Błękit (sky blue) | The painted stoves | Annotations |

Zalipie Sadza (Dark), from *sadza* (soot), has the soot-blackened plinth as its ground. Zalipie Wapno (Light), from *wapno* (lime), is the lime-washed wall the flowers are painted on. Each painter chooses her own flowers and colours; hex values are interpretations of the paints, adjusted for contrast against each background.

## Develop

The palettes are in `theme.py`. The colour mappings and the preview are shared by every theme family and live in [`heritage/`](../../heritage/). See the [root README](../../README.md) for build, preview and install steps.
