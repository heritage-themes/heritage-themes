# Danqing

Dark and light themes based on the mineral pigments of Chinese painting (丹青, "cinnabar and azurite"). Provides two UI themes, **Danqing Ink** and **Danqing Paper**, each with a matching editor colour scheme.

![Preview](preview.png)

## Inspiration

The palette follows the mineral and plant pigments used in traditional Chinese painting. Each pigment colours one syntax role:

| Pigment | What it is | Role |
| --- | --- | --- |
| Cinnabar (朱砂) | Red-orange mineral, mercury sulphide | Keywords |
| Azurite (石青) | Deep blue copper mineral | Types |
| Gamboge (藤黄) | Yellow tree resin | Methods |
| Bamboo green (竹青) | Soft green named after bamboo skin | Strings |
| Lotus-root (藕荷) | Pale mauve named after lotus root | Fields |
| Ochre (赭石) | Red-brown iron-rich earth | Numbers |
| Dai (黛) | Blue-black pigment | Constants |
| Malachite (石绿) | Green copper mineral | Annotations |

Danqing Ink uses the dark tone of ink on an inkstone as its ground. Danqing Paper uses the warm off-white of xuan paper. Spock labels are red seal stamps. The mapping departs from the usual green, yellow and blue syntax convention to keep the saturation of mineral pigments.

## Develop

Palettes and all colour mappings are in `gen.py`. The root `build.py` includes the themes in the Heritage Themes plugin; see the [root README](../README.md) for build and install steps.

Generate a palette preview at `danqing/build/preview.html`:

```bash
python3 danqing/gen.py
```
