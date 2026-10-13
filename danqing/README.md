# Danqing

Dark and light themes based on the mineral pigments of Chinese painting (丹青, "cinnabar and azurite"). Provides two UI themes, **Danqing Ink** and **Danqing Paper**, each with a matching editor colour scheme.

![Preview](preview.png)

## Develop

Palettes and all colour mappings are in `gen.py`. The root `build.py` includes the themes in the Heritage Themes plugin; see the [root README](../README.md) for build and install steps.

Generate a palette preview at `danqing/build/preview.html`:

```bash
python3 danqing/gen.py
```
