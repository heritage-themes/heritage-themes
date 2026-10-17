# Danqing

Dark and light themes based on the mineral pigments of Chinese painting (丹青, "cinnabar and azurite"). Provides two UI themes, **Danqing Ink (Dark)** and **Danqing Paper (Light)**, each with a matching editor colour scheme.

![Preview](preview.png)

## Inspiration

The palette follows the mineral and plant pigments used in traditional Chinese painting. Each pigment colours one syntax role:

| Pigment | What it is | Role |
| --- | --- | --- |
| Azurite (石青) | Deep blue copper mineral | Keywords |
| Malachite (石绿) | Green copper mineral | Strings |
| Cinnabar (朱砂) | Red-orange mineral, mercury sulphide | Method declarations |
| Zhubiao (朱膘) | Paler top layer of ground cinnabar | Method calls |
| Gamboge (藤黄) | Yellow tree resin | Types |
| Ochre (赭石) | Red-brown iron-rich earth | Annotations |
| Lotus-root (藕荷) | Pale mauve named after lotus root | Constants |
| Dai (黛) | Blue-black pigment | Fields |
| Carmine (胭脂) | Crimson plant and insect dye | Numbers |
| Second azurite (二青) | Lighter grade of ground azurite | Type parameters |

Danqing Ink (Dark) uses the dark tone of ink on an inkstone as its ground. Danqing Paper (Light) uses the warm off-white of xuan paper. Spock labels are the red of seal paste (印泥). Azurite and malachite lead the palette, as in blue-green landscape painting (青绿山水). Hex values are interpretations of the traditional pigments, adjusted for contrast against each background.

## Develop

The palettes are in `theme.py`. The colour mappings and the preview are shared by every theme family and live in [`heritage/`](../../heritage/). See the [root README](../../README.md) for build, preview and install steps.
