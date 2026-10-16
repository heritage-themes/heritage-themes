# Shuimo

Dark and light themes based on Chinese ink-wash painting (水墨, *shuimo*). Hierarchy comes from ink tone and weight, not hue. Provides two UI themes, **Shuimo Night** and **Shuimo Day**, each with a matching editor colour scheme.

![Preview](preview.png)

## Inspiration

Ink-wash painting works with a single ink, diluted to many tones. The saying 墨分五色 ("ink has five shades") describes this range. Shuimo applies the idea to code: hierarchy comes from tone and weight.

| Element | Treatment |
| --- | --- |
| Declarations | Strongest tone, bold |
| Plain names | Mid tone |
| Keywords | Weaker tone |
| Strings | Indigo wash (花青) |
| Numbers, constants | Ochre wash (赭石) |
| Spock labels, caret, TODOs | Red seal (印章) |

The two washes follow the light-crimson (浅绛) style of landscape painting, which adds a little indigo and ochre to ink. Shuimo Night is ink-dark; Shuimo Day is pale paper.

## Develop

The palettes are in `theme.py`. The colour mappings and the preview are shared by every theme family and live in [`heritage/`](../../heritage/). See the [root README](../../README.md) for build, preview and install steps.
