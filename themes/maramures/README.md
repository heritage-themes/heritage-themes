# Maramureș

Dark and light themes based on the festive dress of Maramureș, Romania. Provides two UI themes, **Maramureș Zadie** and **Maramureș Cânepă**, each with a matching editor colour scheme.

![Preview](preview.png)

## Inspiration

Women's festive dress in Maramureș is a white hemp (*cânepă*) shirt worn with two woollen aprons, *zadie*, striped in black and a colour that shows the wearer's village and age. Girls wear black and pumpkin-flower yellow, married women black and red, and some villages add thin stripes of blue. The flowered skirt (*sumnă*) that took over the aprons' role keeps the code: vivid flowers for unmarried women, paler ones after 35, a single dark colour after 50 (brown, dark blue or dark green), and black with small flowers in old age. Waistcoats are brown leather.

| Colour | Use | Role |
| --- | --- | --- |
| Red | The married woman's *zadie* | Keywords, Spock labels; buttons and the Run widget |
| Pumpkin-flower yellow | The girl's *zadie* | Strings |
| Blue | Thin stripes of the *zadie* | Numbers, constants, annotations |
| Dark green | The *sumnă* after 50 | Types |
| Rose | The flowers of the *sumnă* | Method declarations and calls |
| Brown leather | Waistcoats | Fields |

Maramureș Zadie has the black wool of the aprons as its ground; Maramureș Cânepă has the white hemp of the shirt. Stripe colours and widths differ from village to village. Hex values are interpretations of the dyed wool, cloth and leather, adjusted for contrast against each background.

## Develop

The palettes are in `theme.py`. The colour mappings and the preview are shared by every theme family and live in [`heritage/`](../../heritage/). See the [root README](../../README.md) for build, preview and install steps.
