# Heritage Themes

Colour themes for IntelliJ-based IDEs and VS Code, each drawn from a culture's colour tradition. All themes ship in one JetBrains plugin (plugin ID `heritage.themes`) and one VS Code extension (`heritage-themes.heritage-themes`).

| Folder | Themes | Country |
| --- | --- | --- |
| [`themes/ainu/`](themes/ainu/) | Ainu Attus (Light), Ainu Kaparamip (Dark) | Japan |
| [`themes/aizome/`](themes/aizome/) | Aizome Kachi (Dark), Aizome Kamenozoki (Light) | Japan |
| [`themes/bengal/`](themes/bengal/) | Bengal Baluchari (Dark), Bengal Laal Paar (Light) | India, Bangladesh |
| [`themes/danqing/`](themes/danqing/) | Danqing Ink (Dark), Danqing Paper (Light) | China |
| [`themes/edo/`](themes/edo/) | Edo Cha (Dark), Edo Nezumi (Light) | Japan |
| [`themes/gujarat/`](themes/gujarat/) | Gujarat Navratri (Dark), Gujarat Rann (Light) | India |
| [`themes/hmong/`](themes/hmong/) | Hmong Batik (Dark), Hmong Hemp (Light) | Vietnam, Laos, Thailand, China |
| [`themes/holi/`](themes/holi/) | Holi Day, Holi Night | India |
| [`themes/kalaallisuut/`](themes/kalaallisuut/) | Kalaallisuut Qaqortoq (Light), Kalaallisuut Qernertoq (Dark) | Greenland |
| [`themes/kalamkari/`](themes/kalamkari/) | Kalamkari Cotton (Light), Kalamkari Indigo (Dark) | India |
| [`themes/kashubia/`](themes/kashubia/) | Kashubia Niebò (Light), Kashubia Zemia (Dark) | Poland |
| [`themes/kerala/`](themes/kerala/) | Kerala Backwaters (Dark), Kerala Kasavu (Light) | India |
| [`themes/lowicz/`](themes/lowicz/) | Łowicz Kodra (Light), Łowicz Wycinanka (Dark) | Poland |
| [`themes/maramures/`](themes/maramures/) | Maramureș Cânepă (Light), Maramureș Zadie (Dark) | Romania |
| [`themes/maya/`](themes/maya/) | Maya Corte (Dark), Maya Huipil (Light) | Guatemala |
| [`themes/morocco/`](themes/morocco/) | Morocco Majorelle (Dark), Morocco Marrakech (Dark), Morocco Zellige (Dark) | Morocco |
| [`themes/mudhif/`](themes/mudhif/) | Mudhif Qasab (Light), Mudhif Qir (Dark) | Iraq |
| [`themes/mughal/`](themes/mughal/) | Mughal Night, Mughal Wasli (Light) | India, Pakistan |
| [`themes/ndebele/`](themes/ndebele/) | Ndebele Mhlophe (Light), Ndebele Nzima (Dark) | South Africa |
| [`themes/peru/`](themes/peru/) | Peru Kulli (Dark), Peru Puka (Dark) | Peru |
| [`themes/podhale/`](themes/podhale/) | Podhale Kłobuk (Dark), Podhale Sukno (Light) | Poland |
| [`themes/punjab/`](themes/punjab/) | Punjab Basant (Light), Punjab Phulkari (Dark) | India, Pakistan |
| [`themes/rajasthan/`](themes/rajasthan/) | Rajasthan Blue City (Dark), Rajasthan Pink City (Light) | India |
| [`themes/sardinia/`](themes/sardinia/) | Sardinia Camisa (Light), Sardinia Orbace (Dark) | Italy |
| [`themes/shaker/`](themes/shaker/) | Shaker Plaster (Light), Shaker Prussian (Dark) | United States |
| [`themes/shuimo/`](themes/shuimo/) | Shuimo Day, Shuimo Night | China |
| [`themes/tamil/`](themes/tamil/) | Tamil Kolam (Dark), Tamil Olai (Light) | India |
| [`themes/wixarika/`](themes/wixarika/) | Wixárika Haramara (Dark), Wixárika Wirikuta (Light) | Mexico |
| [`themes/wuxing/`](themes/wuxing/) | Wuxing Day, Wuxing Night | China |
| [`themes/yolngu/`](themes/yolngu/) | Yolŋu Galawu (Dark), Yolŋu Gapaṉ (Light) | Australia |
| [`themes/zalipie/`](themes/zalipie/) | Zalipie Sadza (Dark), Zalipie Wapno (Light) | Poland |
| [`themes/zlotnica/`](themes/zlotnica/) | Złotnica Aksamit (Dark), Złotnica Płótno (Light) | Poland |

## Install

### JetBrains IDEs

Install **Heritage Themes** from **Settings | Plugins | Marketplace**; it is published on the JetBrains Marketplace. Then choose a theme under **Settings | Appearance & Behavior | Appearance | Theme**.

To install from the [latest GitHub release](https://github.com/heritage-themes/heritage-themes/releases/latest) instead:

- Plugin: `heritage-themes-<version>-signed.zip`. Choose **Settings | Plugins | ⚙ | Install Plugin from Disk…**, select the zip and restart.
- Editor colour scheme only: an `.icls` file. Choose **Settings | Editor | Color Scheme | ⚙ | Import Scheme…** and select the file.

The themes work in IntelliJ-based IDEs version 2025.3 or later, such as IntelliJ IDEA, PyCharm, WebStorm and Android Studio.

Every theme uses the Islands UI: the editor and tool windows sit as rounded islands on the main window. Choosing a Heritage theme always applies it; choose another theme for a different layout. The Classic UI plugin is not tested.

### VS Code

Install **Heritage Themes** from the Extensions view; it is published on the VS Marketplace and Open VSX. Then choose a theme with **Preferences: Color Theme** (`Ctrl+K Ctrl+T`). To install from the latest GitHub release instead, run **Extensions: Install from VSIX…** and select `heritage-themes-vscode-<version>.vsix`.

## Build from source

Requires Python 3. `--vsix` also needs Node.js 22 or later and npm; it installs vsce, pinned in `scripts/vscode/`, on first use.

```bash
python3 build.py          # JetBrains plugin and VS Code extension folder
python3 build.py --vsix   # also pack the VS Code extension
```

Output in `build/`:

| Path | Content |
| --- | --- |
| `heritage-themes-<version>.jar` | The plugin: descriptor, every theme and the plugin icons. Install this in the IDE |
| `heritage-themes-<version>.zip` | The same jar inside a `heritage-themes/lib/` folder, the layout the Marketplace expects for an uploaded plugin. Its themes are identical to the jar's |
| `schemes/*.icls` | Standalone editor colour schemes |
| `vscode/` | The VS Code extension: `package.json`, README, changelog and one colour theme per theme |
| `heritage-themes-vscode-<version>.vsix` | The VS Code extension packed by `--vsix`. Install this in VS Code |

Install the jar, an `.icls` file or the `.vsix` as described under [Install](#install).

## Preview

```bash
python3 preview.py              # every theme: themes/<theme>/build/preview.html
python3 preview.py shuimo       # one theme
python3 preview.py --png        # also render themes/<theme>/preview.png
python3 preview.py --vscode     # VS Code preview: themes/<theme>/build/preview-vscode.html
```

The page shows each theme as an IDE window with a code sample per language, coloured from the generated editor scheme. It downloads JetBrains Mono once into `~/.cache/heritage-themes`. `--png` needs Google Chrome or Chromium (or the `CHROME` environment variable) and ImageMagick.

`--vscode` colours the samples with VS Code's TextMate grammars and the generated VS Code theme, through Shiki pinned in `scripts/shiki/`. It needs Node.js and npm, and installs Shiki there on first use. It shows TextMate colours only: semantic highlighting needs a language server. With `--png` it writes `preview-vscode.png` next to the page.

## Layout

```text
build.py        builds the plugin and the VS Code extension from every theme folder; holds their shared version
preview.py      writes theme previews and renders the README images
heritage/       code shared by every theme family
  __init__.py   finds the theme folders in themes/; the theme.py contract
  scheme.py     editor colour scheme: palette roles to text attributes
  ui.py         UI theme: palette roles to UI keys
  vscode.py     VS Code colour theme: palette roles to TextMate scopes, semantic tokens and workbench keys
  preview.py    preview page
  samples.py    code samples shown in the preview
CHANGELOG.md    JetBrains plugin release notes; the plugin's change notes come from it
vscode/         CHANGELOG.md: VS Code extension release notes
assets/         plugin icons (pluginIcon.svg, pluginIcon_dark.svg)
scripts/        release.sh, parent_overrides.py; shiki/ tokenises the VS Code preview; vscode/ packs and publishes the extension
docs/           releasing.md, adding-a-theme.md
.github/        Build and Publish workflows; ISSUE_TEMPLATE/ holds the issue forms
themes/<theme>/
  theme.py      palettes; defines FAMILY, BLURB and THEMES
  README.md     what the theme is
  preview.png   README image, rendered by preview.py --png
build/          generated, not tracked
```

Only sources are tracked. Jars, zips, `.icls` and `.vsix` files are build output; the publish workflows attach them to each GitHub release.

## Git workflow

- Work on `dev`. `master` receives commits only when `scripts/release.sh` cuts a release.
- Commit subjects follow [Conventional Commits](https://www.conventionalcommits.org/), with the theme folder as the scope for a change to one theme: `fix(wuxing): soften comment contrast`. Changes outside the theme folders use a scope such as `heritage`, `build` or `ci`, or none.
- Keep a commit within one theme folder.
- `scripts/release.sh` tags each release `v<version>`, which publishes it. The JetBrains plugin and the VS Code extension share the version, `VERSION` in `build.py`; a release publishes each product with changelog entries. One release ships every theme. See [docs/releasing.md](docs/releasing.md).

## Add a theme

See [docs/adding-a-theme.md](docs/adding-a-theme.md).

## Report an issue

Report a colour, contrast or readability problem, or suggest a new tradition, on the [issue tracker](https://github.com/heritage-themes/heritage-themes/issues). The bug form asks for the theme, editor and version, language and a screenshot; a report with these can be reproduced.

## Licence

[MIT](LICENSE)
