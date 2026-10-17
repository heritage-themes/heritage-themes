# Shaker

Dark and light themes based on the paint of the Shaker villages of the United States. Provides two UI themes, **Shaker Prussian** and **Shaker Plaster**, each with a matching editor colour scheme.

![Preview](preview.png)

## Inspiration

The Shakers chose the colour of a building or a piece of furniture by what it was for. The Millennial Laws had the meetinghouse painted white outside and "a bluish shade within", bedsteads painted green, and dwelling floors, if stained, "a reddish yellow". Paint was ground by hand from pigments in linseed oil: iron-oxide reds and ochres, chrome yellow, Prussian blue, verdigris and chrome green.

| Colour | Use | Role |
| --- | --- | --- |
| White plaster and Prussian blue | The meetinghouse: white walls, Prussian blue woodwork | Keywords, bold |
| Shaker red | Dwelling exteriors, drawer cases | Strings, Spock labels; buttons and the Run widget |
| Pumpkin ochre | Shops | Method declarations and calls |
| Yellow ochre | Floors, woodwork, the Round Stone Barn at Hancock | Fields |
| Chrome green | Bedsteads, window frames | Types, annotations |
| Verdigris | Paint at Canterbury | Numbers, constants |

Shaker Prussian has the meetinghouse woodwork as its ground, with keywords in plaster white. Shaker Plaster has the meetinghouse walls as its ground, with keywords in Prussian blue. Paint colours varied between villages and have darkened or been varnished over; hex values are interpretations of the restored colours, adjusted for contrast against each background.

## Develop

The palettes are in `theme.py`. The colour mappings and the preview are shared by every theme family and live in [`heritage/`](../../heritage/). See the [root README](../../README.md) for build, preview and install steps.
