# Heritage Themes

Colour themes for IntelliJ-based IDEs, each drawn from a culture's colour tradition. All themes ship in one plugin (plugin ID `heritage.themes`).

| Folder | Themes |
| --- | --- |
| [`bengal/`](bengal/) | Bengal Baluchari, Bengal Laal Paar |
| [`danqing/`](danqing/) | Danqing Ink, Danqing Paper |
| [`holi/`](holi/) | Holi Day, Holi Night |
| [`kalamkari/`](kalamkari/) | Kalamkari Cotton, Kalamkari Indigo |
| [`kerala/`](kerala/) | Kerala Backwaters, Kerala Kasavu |
| [`mughal/`](mughal/) | Mughal Night, Mughal Wasli |
| [`punjab/`](punjab/) | Punjab Basant, Punjab Phulkari |
| [`rajasthan/`](rajasthan/) | Rajasthan Blue City, Rajasthan Pink City |
| [`shuimo/`](shuimo/) | Shuimo Day, Shuimo Night |
| [`tamil/`](tamil/) | Tamil Kolam, Tamil Olai |
| [`wuxing/`](wuxing/) | Wuxing Day, Wuxing Night |

## Install

Download from the [GitHub releases](https://github.com/heritage-themes/heritage-themes/releases) page:

- Plugin: `heritage-themes-<version>.jar`. In the IDE choose **Settings | Plugins | ⚙ | Install Plugin from Disk…**, select the jar and restart. Then choose a theme under **Settings | Appearance & Behavior | Appearance | Theme**.
- Editor colour scheme only: an `.icls` file. Choose **Settings | Editor | Color Scheme | ⚙ | Import Scheme…** and select the file.

The themes work in IntelliJ-based IDEs, such as IntelliJ IDEA, PyCharm, WebStorm and Android Studio.

## Build from source

Requires Python 3.

```bash
python3 build.py
```

Output in `build/`:

| Path | Content |
| --- | --- |
| `heritage-themes-<version>.jar` | Installable plugin containing every theme |
| `heritage-themes-<version>.zip` | The jar in plugin layout, for the Marketplace |
| `schemes/*.icls` | Standalone editor colour schemes |

Install the jar or an `.icls` file as described under [Install](#install).

## Preview

```bash
python3 preview.py              # every theme: <theme>/build/preview.html
python3 preview.py shuimo       # one theme
python3 preview.py --png        # also render <theme>/preview.png
```

The page shows each theme as an IDE window with a code sample per language, coloured from the generated editor scheme. It downloads JetBrains Mono once into `~/.cache/heritage-themes`. `--png` needs Google Chrome or Chromium (or the `CHROME` environment variable) and ImageMagick.

## Layout

```text
build.py        builds the plugin from every theme folder; holds the plugin version
preview.py      writes theme previews and renders the README images
heritage/       code shared by every theme family
  __init__.py   finds theme folders; the theme.py contract
  scheme.py     editor colour scheme: palette roles to text attributes
  ui.py         UI theme: palette roles to UI keys
  preview.py    preview page
  samples.py    code samples shown in the preview
CHANGELOG.md    release notes; the plugin's change notes come from it
assets/         plugin icons (pluginIcon.svg, pluginIcon_dark.svg)
scripts/        release.sh, parent_overrides.py
docs/           releasing.md, adding-a-theme.md
.github/        Build and Publish workflows
<theme>/
  theme.py      palettes; defines FAMILY, BLURB and THEMES
  README.md     what the theme is
  preview.png   README image, rendered by preview.py --png
build/          generated, not tracked
```

Only sources are tracked. Jars, zips and `.icls` files are build output; the Publish workflow attaches them to each GitHub release.

## Git workflow

- Work on `dev`. `master` receives commits only when `scripts/release.sh` cuts a release.
- Commit subjects follow [Conventional Commits](https://www.conventionalcommits.org/), with the theme folder as the scope for a change to one theme: `fix(wuxing): soften comment contrast`. Changes outside the theme folders use a scope such as `heritage`, `build` or `ci`, or none.
- Keep a commit within one theme folder.
- `scripts/release.sh` tags each release `v<version>`, which publishes it. The version matches `VERSION` in `build.py`. One release ships every theme. See [docs/releasing.md](docs/releasing.md).

## Add a theme

See [docs/adding-a-theme.md](docs/adding-a-theme.md).

## Licence

[MIT](LICENSE)
