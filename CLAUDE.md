# Heritage Themes

Colour themes drawn from cultures' colour traditions, shipped to 25 apps and 26 terminal programs from one
repository. Each theme family is a folder in `themes/` with a `theme.py` that holds its palettes. Every colour
mapping, the UI theme and the previews are shared code in `heritage/`, one module per product.

- `python3 build.py` builds and validates every product. CI runs `python3 build.py --vsix --jupyterlab`.
- `python3 preview.py --help` lists the previews.
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
4. Commit on `dev` as `feat(<theme>): ...`, limited to the theme folder, the root README row and the changelog
   entries.

Distinctiveness: every family must look and read differently from every family in `themes/`.

- Compare the intended palette with each existing family: background hue, the hue of each syntax role and the
  overall impression. Two families that give the same roles the same hues are too similar, even if the cultures
  differ.
- Reach distinctiveness through the culture's own colours and how it assigns them to roles, never by shifting
  hues arbitrarily.
- If a concept is distinct only through colours that lose their connection to the culture, do not create it.
  Say that the theme does not make sense and name the families it collides with.

## Checking a theme

- Every UI colour reference resolves, and text roles meet WCAG AA against `bg`, with about 3:1 for comments.
  `build.py` enforces both.
- Fields and method calls are clearly distinct from plain text and from each other, unless the concept builds
  hierarchy from tone and weight rather than hue, as Shuimo does.
- The themes must look good in the most popular languages, not only Java: Kotlin, Groovy, Python, TypeScript,
  JSX and TSX, Vue, HTML, CSS, SQL, Go, Rust, C++, C, C#, shell, YAML, JSON, TOML and Markdown. The preview has a
  sample in each. Language-specific highlighting can fall back to the parent scheme and clash with the palette.
  Find the keys that the IDEs colour explicitly with `scripts/parent_overrides.py`; never guess key names.
- Preprocessor directives take the `directive` role in every product that can colour them, and stay apart from
  keywords and macro names.

## Adding an app

Each app the themes ship to is a target:

- A target is a generator in `heritage/<app>.py` that maps palette roles to the app's format, run and validated
  by `build.py`.
- Every target shares `VERSION` and the `v<version>` tag. It gets its own changelog, an entry in the product list
  in `scripts/release.sh`, a job in `publish.yml` and its last build attached to releases that leave it out.
  `docs/releasing.md` lists the steps.
- The theme checks apply to each target's output: WCAG contrast, distinct roles and a rendered preview.
- Before starting, find out how the app installs and distributes themes, and whether that fits a shared
  repository release. Tell the maintainer if it does not.

## Conventions

- UI themes cover the chrome: run widget, VCS log, banners, popups, welcome screen, plugin pages, tabs,
  scrollbars, buttons and progress bars. `heritage/ui.py` does this; do not cut it down.
- `fileYellow` is a faint wash close to `bg`, never a saturated colour.
- No pure black or pure white backgrounds unless the culture's palette demands it.
- Night is lighter and slightly desaturated. Day is deeper, so contrast holds.
- README Inspiration tables use neutral, descriptive language and the culture's own words for colours and
  concepts, with the original script where relevant. Say where hex values are interpretations of traditional
  colours.
- British English in docs.
