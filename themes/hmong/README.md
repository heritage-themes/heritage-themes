# Hmong

Dark and light themes based on the pleated hemp skirt of the Hmong of Vietnam, Laos, Thailand and southern China: indigo batik framed by bands of bright cross-stitch. Provides two UI themes, **Hmong Batik** and **Hmong Hemp**, each with a matching editor colour scheme.

![Preview](preview.png)

## Inspiration

Blue, Green and Flower Hmong women draw batik (*paj ntaub nraj ciab*) on white hemp with beeswax, then dip the cloth in indigo several times. The wax resists the dye, so the pattern stays white while the cloth deepens from light blue to almost black; boiling removes the wax. On a Flower Hmong skirt the batik band is framed by bands of cross-stitch and appliqué (*paj ntaub*, flower cloth) in hot pink, lime green, orange and yellow.

The themes build their structure from the tones of the batik and take their colour from the cross-stitch.

| Colour | Source | Role |
| --- | --- | --- |
| Wax-resist line | The undyed line left by the wax | Types (Hmong Batik) |
| Darkest indigo | Cloth dipped many times | Types (Hmong Hemp) |
| Light indigo | Cloth dipped once or twice | Method declarations and calls, links |
| Mid indigo | Cloth dipped several times | Fields |
| Hot pink | Cross-stitch and appliqué | Keywords, caret, Spock labels, buttons and the Run widget |
| Lime green | Cross-stitch | Strings |
| Orange | Cross-stitch | Numbers, constants |
| Yellow | Cross-stitch | Annotations |

Hmong Batik has the indigo-dyed cloth as its ground. Hmong Hemp has the undyed white hemp that the batik is drawn on. Hex values are interpretations of the dyed cloth and thread, adjusted for contrast against each background.

## Develop

The palettes are in `theme.py`. The colour mappings and the preview are shared by every theme family and live in [`heritage/`](../../heritage/). See the [root README](../../README.md) for build, preview and install steps.
