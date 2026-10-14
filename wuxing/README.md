# Wuxing

Dark and light themes based on Chinese colour symbolism and the Five Elements (Wuxing). Provides two UI themes, **Wuxing Night** and **Wuxing Day**, each with a matching editor colour scheme.

![Preview](preview.png)

## Inspiration

The palette draws on the Five Elements (五行) scheme of colour associations and on a few colours from Chinese decorative arts.

| Source | Colour | Role |
| --- | --- | --- |
| Fire | Red | Keywords |
| Wood | Green | Strings |
| Earth | Yellow | Types |
| Metal | Rice white (beige, not pure white) | Text and paper |
| Water | Indigo ink (not pure black) | Night background, day text |
| Gold | Gold | Caret, search results, Spock labels |
| Imperial purple | Purple | Fields |
| Azure | Blue | Methods |
| Turquoise | Turquoise | Annotations |
| Copper | Orange-brown | Numbers |
| Ink-wash grey | Grey | Comments |

## Develop

Palettes and all colour mappings are in `gen.py`. The root `build.py` includes the themes in the Heritage Themes plugin; see the [root README](../README.md) for build and install steps.

Generate a palette preview at `wuxing/build/preview.html`:

```bash
python3 wuxing/gen.py
```
