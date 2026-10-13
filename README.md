# Heritage Themes

Colour themes for IntelliJ-based IDEs, each drawn from a culture's colour tradition. All themes ship in one plugin, `heritage.themes`.

| Folder | Themes |
| --- | --- |
| [`danqing/`](danqing/) | Danqing Ink, Danqing Paper |
| [`wuxing/`](wuxing/) | Wuxing Day, Wuxing Night |

## Build

Requires Python 3.

```bash
python3 build.py
```

Output in `build/`:

| Path | Content |
| --- | --- |
| `heritage-themes-<version>.jar` | Installable plugin containing every theme |
| `schemes/*.icls` | Standalone editor colour schemes |

## Install

- Plugin: **Settings | Plugins | ⚙ | Install Plugin from Disk…**, select the jar, restart the IDE, then choose a theme under **Settings | Appearance & Behavior | Appearance | Theme**.
- Editor scheme only: **Settings | Editor | Color Scheme | ⚙ | Import Scheme…**, select an `.icls` file.

## Layout

```text
build.py        builds the plugin from every theme folder; holds the plugin version and change notes
assets/         plugin icons (pluginIcon.svg, pluginIcon_dark.svg)
<theme>/
  gen.py        palettes and colour mappings; exposes FAMILY, BLURB and generate()
  README.md     what the theme is
  preview.png   screenshot used by the README
build/          generated, not tracked
```

Only sources are tracked. Jars and `.icls` files are build output; publish them as release assets.

## Git workflow

- `master` is always releasable. Work on short-lived branches (`<theme>/<topic>`) and merge them into `master`.
- Commit subjects start with the theme folder: `wuxing: soften comment contrast`. Use `repo:` for changes outside any theme.
- Keep a commit within one theme.
- Tag each release `v<version>` (for example `v1.1.0`). The version matches `VERSION` in `build.py`. One release ships every theme.

## Add a theme

1. Create `<theme>/` with a `gen.py` that defines `FAMILY`, `BLURB` and `generate()`. `generate()` returns one dict per theme with `slug`, `id` (a new UUID), `name`, `scheme` (editor scheme XML) and `theme` (theme JSON as a dict). `slug`, `id` and `name` must be unique across all themes.
2. Add `README.md` and `preview.png` to the folder.
3. Add a row to the table above.
4. Update `VERSION` and `CHANGE_NOTES` in `build.py` when releasing.

## Licence

[MIT](LICENSE)
