# Heritage Themes

Colour themes drawn from cultures' colour traditions, shipped to many apps and terminal programs from one
repository. Each theme family is a folder in `themes/` with a `theme.py` that holds its palettes. Every colour
mapping, the UI theme and the previews are shared code in `heritage/`, one module per product.

- `python3 build.py` builds and validates every product. CI runs `python3 build.py --vsix --jupyterlab`.
- Work on `dev`. `master` receives commits only when a release is cut; see `docs/releasing.md`.

## Palettes are the only source of colour

Never add per-family or per-app colours. A mapping that looks wrong for one family changes in `heritage/` and
every family's preview is rendered again, because the change affects them all.

## Adding a theme

Follow `docs/adding-a-theme.md`. If it disagrees with the most recently added theme folder, say which one is
out of date.

1. If no culture is named, pick one where colour carries real meaning. Research it and prefer named traditional
   colours and concrete systems: rank colours, seasonal layers, pigments, dyes.
2. Check each concept for distinctiveness. Propose one to four concepts, each a Night and Day pair, and let the
   maintainer choose unless told "do all". Drop a concept that fails the check and say why.
3. Create each family as the guide describes, then run `python3 build.py` and `python3 preview.py --png <theme>`.
   Look at the rendered PNG. Stop there: the maintainer installs the jar and does the manual IDE checks. Do not
   send the jar.

Distinctiveness: every family must look and read differently from every family in `themes/`.

- Compare the intended palette with each existing family: background hue, the hue of each syntax role and the
  overall impression. Two families that give the same roles the same hues are too similar, even if the cultures
  differ.
- Reach distinctiveness through the culture's own colours and how it assigns them to roles. If a concept is
  distinct only through hues shifted away from the culture's colours, do not create it. Say that the theme does
  not make sense and name the families it collides with.

## Checking a theme

- Contrast is enforced by `build.py`; comments need about 3:1.
- Fields and method calls are clearly distinct from plain text and from each other, unless the concept builds
  hierarchy from tone and weight rather than hue, as Shuimo does.
- The themes must look good in the most popular languages, not only Java. Language-specific highlighting can
  fall back to the parent scheme and clash with the palette. Find the keys that the IDEs colour explicitly with
  `scripts/parent_overrides.py`; never guess key names.

## Adding an app

Each app the themes ship to is a target: a generator in `heritage/<app>.py` that maps palette roles to the app's
format, run and validated by `build.py`. `docs/releasing.md` lists the release steps for a new product.

- The theme checks apply to each target's output: WCAG contrast, distinct roles and a rendered preview.
- Before starting, find out how the app installs and distributes themes, and whether that fits a shared
  repository release. Tell the maintainer if it does not.

## Conventions

- `heritage/ui.py` covers the whole UI chrome; do not cut it down.
- No pure black or white backgrounds unless the culture's palette demands it.
- Night is lighter and slightly desaturated. Day is deeper, so contrast holds.
- README Inspiration tables use neutral, descriptive language and the culture's own words for colours and
  concepts, with the original script where relevant. Say where hex values are interpretations of traditional
  colours.
- British English in docs.
