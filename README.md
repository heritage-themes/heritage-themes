# Heritage Themes

Colour themes for IntelliJ-based IDEs, VS Code, Sublime Text, Zed and Neovim, each drawn from a culture's colour tradition. All themes ship in one JetBrains plugin (plugin ID `heritage.themes`), one VS Code extension (`heritage-themes.heritage-themes`), one Sublime Text package (`Heritage Themes`), one Zed extension (`heritage-theme`) and one Neovim plugin (`heritage-themes/heritage-themes.nvim`).

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

The extension also works in VS Code forks such as Cursor, Windsurf and VSCodium, which install from Open VSX.

### Sublime Text

Run **Package Control: Install Package** and choose **Heritage Themes**, then **UI: Select Color Scheme** and **UI: Select Theme**, choosing the same name in both. To install from the latest GitHub release instead, copy `heritage-themes-sublime-<version>.sublime-package` into the `Installed Packages` folder, which **Preferences: Browse Packages** shows beside `Packages`. Each colour scheme colours the editor; the UI theme of the same name extends the built-in Adaptive theme and colours the sidebar, tabs, panels and status bar to match. Sublime Text 4 is required.

### Zed

Install **Heritage Themes** from the Extensions page (**zed: extensions**), then choose a theme with **theme selector: toggle** (`Ctrl+K Ctrl+T`). To install from the latest GitHub release instead, unzip `heritage-themes-zed-<version>.zip`, run **zed: install dev extension** and select the unzipped `heritage-theme` folder. Each theme colours the editor, panels, tabs, title and status bars, terminal and popups.

### Neovim

Install `heritage-themes/heritage-themes.nvim` with a plugin manager, for example with [lazy.nvim](https://github.com/folke/lazy.nvim):

```lua
{ "heritage-themes/heritage-themes.nvim", lazy = false, priority = 1000 }
```

Then choose a theme with `:colorscheme heritage-<theme>`, for example `:colorscheme heritage-holi-night`; press `Tab` after `heritage-` to list them. To install from the latest GitHub release instead, unzip `heritage-themes-nvim-<version>.zip` into `~/.local/share/nvim/site/pack/heritage/start/`. Each colour scheme colours the editor, Tree-sitter and LSP semantic highlights, diagnostics, the status line, tab line, floating windows, the completion menu, diff mode and the terminal; it comes with a lualine theme of the same name and colours the signs of gitsigns.nvim. Neovim 0.10 or later in a terminal with 24-bit colour is required.

## Build from source

Requires Python 3. `--vsix` also needs Node.js 22 or later and npm; it installs vsce, pinned in `scripts/vscode/`, on first use.

```bash
python3 build.py          # JetBrains plugin, VS Code extension folder, Sublime Text package, Zed extension and Neovim plugin
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
| `sublime/` | The Sublime Text package: per theme a `.sublime-color-scheme`, a `.sublime-theme` and its `Widget - <name>.sublime-settings`, plus README, changelog and licence. The release publishes this folder to the package repository |
| `heritage-themes-sublime-<version>.sublime-package` | The same files packed as a zip. Install this in Sublime Text |
| `zed/` | The Zed extension: `extension.toml`, one theme family file per theme folder in `themes/`, README, changelog and licence. The release publishes this folder to the extension repository |
| `heritage-themes-zed-<version>.zip` | The same files in a `heritage-theme/` folder. Unzip it and install the folder in Zed |
| `nvim/` | The Neovim plugin: one colour scheme per theme in `colors/`, one lualine theme per theme in `lua/lualine/themes/`, README, changelog and licence. The release publishes this folder to the plugin repository |
| `heritage-themes-nvim-<version>.zip` | The same files in a `heritage-themes.nvim/` folder. Unzip it into a `pack/*/start/` folder of Neovim |

Install the jar, an `.icls` file, the `.vsix`, the `.sublime-package`, the Zed extension or the Neovim plugin as described under [Install](#install).

## Preview

```bash
python3 preview.py              # every theme: themes/<theme>/build/preview.html
python3 preview.py shuimo       # one theme
python3 preview.py --png        # also render themes/<theme>/preview.png
python3 preview.py --vscode     # VS Code preview: themes/<theme>/build/preview-vscode.html
python3 preview.py --sublime    # Sublime Text preview: themes/<theme>/build/preview-sublime.html
python3 preview.py --zed        # Zed preview: themes/<theme>/build/preview-zed.html
python3 preview.py --nvim       # Neovim preview: themes/<theme>/build/preview-nvim.html
```

The page shows each theme as an IDE window with a code sample per language, coloured from the generated editor scheme. It downloads JetBrains Mono once into `~/.cache/heritage-themes`. `--png` needs Google Chrome or Chromium (or the `CHROME` environment variable) and ImageMagick.

`--vscode` colours the samples with VS Code's TextMate grammars and the generated VS Code theme, through Shiki pinned in `scripts/shiki/`. It needs Node.js and npm, and installs Shiki there on first use. It shows TextMate colours only: semantic highlighting needs a language server. With `--png` it writes `preview-vscode.png` next to the page.

`--sublime` tokenises the samples with [bat](https://github.com/sharkdp/bat), which bundles Sublime Text's syntaxes, and colours them with the generated scheme. It needs `bat` (`batcat` on Debian and Ubuntu) and shows the editor only. bat's syntaxes are close to, not identical with, the ones in the installed Sublime Text, and Sublime Text does not ship Kotlin, TOML or Vue. With `--png` it writes `preview-sublime.png` next to the page.

`--zed` colours the samples with the Tree-sitter grammars and highlight queries that Zed and its language extensions ship, pinned in `scripts/zed/languages.json`, and the generated Zed theme. It needs a C compiler (`cc`): it creates a virtual environment with py-tree-sitter in `scripts/zed/.venv` and compiles the grammars into `~/.cache/heritage-themes/zed` on first use. Zed's language servers can add semantic colours that the page does not show. With `--png` it writes `preview-zed.png` next to the page.

`--nvim` shows the samples as Neovim draws them: it runs Neovim embedded with the theme's colour schemes and nvim-treesitter, opens each sample and reads the colours from the screen Neovim sends to its UI. It needs Neovim and a C compiler (`cc`): it creates a virtual environment with msgpack in `scripts/nvim/.venv`, and downloads nvim-treesitter and compiles the grammars, pinned in `scripts/nvim/parsers.json`, into `~/.cache/heritage-themes/nvim` on first use. It fails when a colour scheme leaves a highlight group with a colour of Neovim's default scheme. Language servers can add semantic colours that the page does not show. With `--png` it writes `preview-nvim.png` next to the page.

## Layout

```text
build.py        builds the plugin, the VS Code extension, the Sublime Text package, the Zed extension and the Neovim plugin
                from every theme folder; holds their shared version
preview.py      writes theme previews and renders the README images
heritage/       code shared by every theme family
  __init__.py   finds the theme folders in themes/; the theme.py contract
  scheme.py     editor colour scheme: palette roles to text attributes
  ui.py         UI theme: palette roles to UI keys
  vscode.py     VS Code colour theme: palette roles to TextMate scopes, semantic tokens and workbench keys
  sublime.py    Sublime Text colour scheme: the VS Code scopes plus the scopes Sublime Text's syntaxes name differently;
                UI theme: rules over Adaptive that give its surfaces and text palette roles
  zed.py        Zed theme: palette roles to Tree-sitter captures and UI keys
  nvim.py       Neovim colour scheme: palette roles to highlight groups, Tree-sitter captures and LSP semantic tokens;
                lualine theme
  preview.py    preview page
  samples.py    code samples shown in the preview
CHANGELOG.md    JetBrains plugin release notes; the plugin's change notes come from it
vscode/         CHANGELOG.md: VS Code extension release notes
sublime/        CHANGELOG.md: Sublime Text package release notes
zed/            CHANGELOG.md: Zed extension release notes
nvim/           CHANGELOG.md: Neovim plugin release notes
assets/         plugin icons (pluginIcon.svg, pluginIcon_dark.svg)
scripts/        release.sh, parent_overrides.py; shiki/ tokenises the VS Code preview; vscode/ packs and publishes the extension;
                zed/ colours the Zed preview; nvim/ draws the Neovim preview
docs/           releasing.md, adding-a-theme.md
.github/        Build and Publish workflows; ISSUE_TEMPLATE/ holds the issue forms
themes/<theme>/
  theme.py      palettes; defines FAMILY, BLURB and THEMES
  README.md     what the theme is
  preview.png   README image, rendered by preview.py --png
build/          generated, not tracked
```

Only sources are tracked. Jars, zips, `.icls`, `.vsix`, `.sublime-package` and Neovim `.lua` files are build output; the publish workflows attach them to each GitHub release.

## Git workflow

- Work on `dev`. `master` receives commits only when `scripts/release.sh` cuts a release.
- Commit subjects follow [Conventional Commits](https://www.conventionalcommits.org/), with the theme folder as the scope for a change to one theme: `fix(wuxing): soften comment contrast`. Changes outside the theme folders use a scope such as `heritage`, `build` or `ci`, or none.
- Keep a commit within one theme folder.
- `scripts/release.sh` tags each release `v<version>`, which publishes it. The JetBrains plugin, the VS Code extension, the Sublime Text package, the Zed extension and the Neovim plugin share the version, `VERSION` in `build.py`; a release publishes each product with changelog entries. One release ships every theme. See [docs/releasing.md](docs/releasing.md).

## Add a theme

See [docs/adding-a-theme.md](docs/adding-a-theme.md).

## Report an issue

Report a colour, contrast or readability problem, or suggest a new tradition, on the [issue tracker](https://github.com/heritage-themes/heritage-themes/issues). The bug form asks for the theme, editor and version, language and a screenshot; a report with these can be reproduced.

## Licence

[MIT](LICENSE)
