# Ndebele

Dark and light themes based on the house painting of the Ndebele of South Africa: flat geometric fills inside heavy black outlines on a white lime-washed wall. Provides two UI themes, **Ndebele Nzima (Dark)** and **Ndebele Mhlophe (Light)**, each with a matching editor colour scheme.

![Preview](preview.png)

## Inspiration

Ndzundza Ndebele women paint the walls of the homestead with geometric panels. The wall is first lime-washed white, every shape is drawn with a heavy black outline, and each shape is filled flat with one colour. The early paintings used earth pigments (ochre, red clay, soot and lime); later walls use red and dark red, yellow to gold, sky blue, green and pink. The panels and their colours echo the patterns of Ndebele beadwork.

The themes take their structure from the outline and their colour from the fills.

| Colour | isiNdebele | Role |
| --- | --- | --- |
| Black outline | *nzima* | Keywords, bold (Ndebele Mhlophe); the ground of Ndebele Nzima (Dark) |
| White lime-wash | *mhlophe* | Keywords, bold (Ndebele Nzima); the ground of Ndebele Mhlophe (Light) |
| Sky blue | *hlaza kwesibhakabhaka* | Types, links |
| Green | *hlaza* | Method declarations and calls, Markdown headings |
| Yellow to gold | *surulani* | Strings |
| Red | *bomvu* | Fields, caret |
| Dark red | *bomvu* | Buttons and the Run widget |
| Pink | | Numbers, constants, annotations |

HTML and XML tags take the outline colour, so markup reads as outlines with coloured attributes and values. Hex values are interpretations of the painted colours, adjusted for contrast against each background.

## Develop

The palettes are in `theme.py`. The colour mappings and the preview are shared by every theme family and live in [`heritage/`](../../heritage/). See the [root README](../../README.md) for build, preview and install steps.
