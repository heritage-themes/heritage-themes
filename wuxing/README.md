# Wuxing

Dark and light themes based on Chinese colour symbolism and the Five Elements (Wuxing). Provides two UI themes, **Wuxing Night** and **Wuxing Day**, each with a matching editor colour scheme.

![Preview](preview.png)

## Develop

Palettes and all colour mappings are in `gen.py`. The root `build.py` includes the themes in the Heritage Themes plugin; see the [root README](../README.md) for build and install steps.

Generate a palette preview at `wuxing/build/preview.html`:

```bash
python3 wuxing/gen.py
```
