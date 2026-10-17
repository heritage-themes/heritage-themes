# Ainu

Dark and light themes based on the appliqué robes of the Ainu of Hokkaido, Japan. Provides two UI themes, **Ainu Kaparamip** and **Ainu Attus**, each with a matching editor colour scheme.

![Preview](preview.png)

## Inspiration

*Kaparamip* (カパラミㇷ゚, "thin garment") is a robe of indigo-dyed trade cotton with large curvilinear cut-outs of white cotton sewn on. *Attus* (アットゥㇱ) is cloth woven from the inner bark of the elm, decorated with indigo cotton appliqué. Chain and couching stitches follow the pattern, and red cloth or thread marks the collar, cuffs and hem, the openings that the pattern guards against spirits.

Ainu has four basic colour words, and each covers a range of colours. The themes give each word its syntax roles:

| Word | Range | Role |
| --- | --- | --- |
| *Kunne* (クンネ) | Dark: black to navy | The ground of Ainu Kaparamip; keywords and types in Ainu Attus |
| *Retar* (レタㇻ) | Light: white to pale yellow and pale blue | Keywords and types in Ainu Kaparamip |
| *Hure* (フレ) | Red: pink to orange | Method declarations and calls, Spock labels, caret; buttons and the Run widget |
| *Siwnin* (シウニン) | Green to yellow and blue-violet | Green strings, yellow fields, blue-violet numbers, constants and annotations |

Keywords are the appliqué, set bold: white cotton on the indigo, indigo cotton on the elm bark. Types take another tone of it. Red marks method declarations, the openings of the code. The green of the strings is the couching thread. Ainu Kaparamip has the indigo cotton as its ground; Ainu Attus has the elm-bark cloth. Hex values are interpretations of the dyed cotton, bark fibre and thread, adjusted for contrast against each background.

## Develop

The palettes are in `theme.py`. The colour mappings and the preview are shared by every theme family and live in [`heritage/`](../../heritage/). See the [root README](../../README.md) for build, preview and install steps.
