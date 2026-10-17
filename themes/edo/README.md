# Edo

Dark and light themes based on the muted dress colours of Edo-period Japan. Every syntax role has its own hue, and every hue is subdued. Provides two UI themes, **Edo Cha** and **Edo Nezumi**, each with a matching editor colour scheme.

![Preview](preview.png)

## Inspiration

Sumptuary laws of the Edo period (1603–1868) kept townspeople to brown (茶, *cha*), grey (鼠, *nezumi*) and indigo (藍, *ai*). Dyers answered with hundreds of faintly tinted, named shades, summed up as 四十八茶百鼠 ("forty-eight browns and a hundred greys"). Bright red silk (紅絹, *momi*) went inside, as a lining glimpsed at the cuff and hem (裏勝り, *ura-masari*). Edo gives each of the three permitted groups a share of the code.

| Colour | Group | Role |
| --- | --- | --- |
| 藍鼠 *ainezumi*, indigo grey | 藍 indigo | Keywords, annotations |
| 利休茶 *rikyūcha*, olive brown | 茶 brown | Strings |
| 芝翫茶 *shikancha*, red brown | 茶 brown | Numbers, constants |
| 利休鼠 *rikyū-nezumi*, green grey | 鼠 grey | Types |
| 藤鼠 *fuji-nezumi*, wisteria grey | 鼠 grey | Method declarations and calls |
| 梅鼠 *ume-nezumi*, plum grey | 鼠 grey | Fields |
| 銀鼠 *gin-nezumi*, silver grey | 鼠 grey | Plain text |
| 紅絹 *momi*, red silk | Lining | Caret, Spock labels, TODOs; buttons and the Run widget |

Edo Cha has a dark tea-brown ground; Edo Nezumi a pale grey one. Hex values are interpretations of the named shades, which vary between sources, adjusted for contrast against each background.

## Develop

The palettes are in `theme.py`. The colour mappings and the preview are shared by every theme family and live in [`heritage/`](../../heritage/). See the [root README](../../README.md) for build, preview and install steps.
