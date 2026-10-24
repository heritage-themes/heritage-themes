# Adding a theme

Add a theme family, usually a dark and a light theme, to the Heritage Themes plugin. A family supplies only palettes; every colour mapping, the UI theme and the preview are shared code in `heritage/`.

## How a family is built

Any folder in `themes/` with a `theme.py` is a theme family. `heritage.load_families()` finds it, so neither `build.py` nor `preview.py` needs a change for a new family. `theme.py` defines:

| Name | Content |
| --- | --- |
| `FAMILY` | Family name, for example `"Shuimo"`; shown in the plugin description |
| `BLURB` | One sentence for the plugin description: the tradition and its main syntax mappings |
| `THEMES` | One `dict(slug=..., id=..., palette=...)` per theme; `id` is a new UUID |

From each palette, `heritage/scheme.py` builds the editor colour scheme, `heritage/ui.py` builds the UI theme, `heritage/vscode.py` builds the VS Code colour theme, `heritage/sublime.py` builds the Sublime Text colour scheme and UI theme, `heritage/zed.py` builds the Zed theme, and `heritage/nvim.py` builds the Neovim colour scheme and lualine theme. `build.py` packs the scheme and the UI theme into the JetBrains plugin, writes a standalone `.icls` per theme, adds the VS Code theme to the VS Code extension, the Sublime Text scheme and UI theme to the Sublime Text package, the family's Zed theme family file to the Zed extension, and the Neovim colour scheme, named `heritage-` and the `slug` in kebab case plus `-dark` or `-light` when the name ends in ` (Dark)` or ` (Light)`, to the Neovim plugin. `slug`, `id` and `name` must be unique across all themes; `build.py` fails otherwise.

A change in `heritage/` changes every family. After one, render all previews and check each family.

## Create the folder

Create `themes/<theme>/theme.py` in the shape of `themes/shuimo/theme.py`: a docstring, a comment describing the colour tradition and the syntax roles it maps to, the palettes, then `FAMILY`, `BLURB` and `THEMES`.

Names follow one pattern:

| Item | Example |
| --- | --- |
| Folder | `shuimo` |
| `slug` | `ShuimoNight` |
| Palette `name` | `Shuimo Night` |

The second word of a theme name is its setting in the tradition: Night and Day for Shuimo, Ink and Paper for Danqing, Baluchari and Laal Paar for Bengal.

A name that does not say Night or Day ends in ` (Dark)` or ` (Light)`, matching `dark`, so the IDE theme list shows the brightness: `Edo Cha (Dark)`, `Edo Nezumi (Light)`. The Neovim scheme names carry it too: `heritage-edo-cha-dark`, `heritage-edo-nezumi-light`. The `slug` omits the suffix.

### Palette

A palette is a dict of six-digit uppercase hex values without `#`, plus metadata. The shared code reads keys directly, so a missing key raises `KeyError`. Both palettes of a family have identical keys.

| Group | Keys |
| --- | --- |
| Metadata | `name`, `dark`, `parent` |
| Surfaces | `bg` (editor), `bgUi`, `bgTool`, `frame`, `surface` (popups, fields), `hover`, `border` |
| Text | `fg`, `muted`, `disabled` |
| Selection and caret | `caretRow`, `selection`, `selInactive` |
| Gutter | `lineNo`, `lineNoCaret`, `guide`, `guideSel` |
| Syntax | `keyword`, `string`, `number`, `type`, `method`, `call`, `field`, `constant`, `annotation`, `comment`, `doc`, `docTag`, `op`, `param`, `typeParam` |
| Spock labels | `label` |
| Accents | `gold`, `red`, `redText`, `azure` |
| Diagnostics | `error`, `warning`, `weak` |
| Highlighting | `searchBg`, `searchBorder`, `underCaret`, `writeCaret`, `braceBg`, `todo` |
| VCS and diff | `added`, `modified`, `deleted`, `diffIns`, `diffMod`, `diffDel`, `diffConf` |
| Project view | `fileYellow` |
| Console | `ansiRed`, `ansiGreen`, `ansiYellow`, `ansiBlue`, `ansiMagenta`, `ansiCyan` |

Metadata values:

| Key | Dark theme | Light theme |
| --- | --- | --- |
| `dark` | `True` | `False` |
| `parent` | `"Darcula"` | `"Default"` |

The UI theme inherits from Islands Dark or Islands Light, chosen by `dark`.

Optional keys:

| Key | Default | Effect |
| --- | --- | --- |
| `caret` | value of `gold` | Caret colour |
| `kwBold` | bold in light themes, regular in dark | Whether keywords are bold |

Key names are roles, not colours. `gold`, `red` and `azure` are slots whose value can be any colour that fits the tradition. To see which editor and UI elements use a role, search for it in `heritage/scheme.py` and `heritage/ui.py`.

Constraints:

- `frame` is the main window behind the editor and tool windows, which the Islands UI draws as rounded islands of `bg` and `bgTool`. Take it from the hue of `bg`: lighter than both `bg` and `bgTool` in a dark theme, darker in a light one, by at least 1.20:1. `build.py` fails otherwise.
- `fileYellow` colours folders that IntelliJ marks as excluded, such as `node_modules`. Use a faint wash close to `bg`, never a saturated colour. A solid colour draws the Project view as coloured bars.
- `label` colours Spock labels (`given:`, `when:`, `then:`) as bold text with no background. It needs the same contrast against `bg` as the syntax roles.
- The `ansi*` keys colour ANSI output in the console and terminal, and VCS file status in the Project view: `ansiGreen` added, `ansiBlue` modified, `ansiRed` unversioned, `ansiMagenta` merged. Each must read as the hue it names, whatever the family's syntax roles are.
- Roles meet WCAG AA against the backgrounds they are drawn on: 4.5:1 for text, 3:1 for comments, the caret and `gold` as the focus ring. `CONTRAST` in `build.py` lists the pairs; the build fails on one that falls short. `gold` also colours string escapes, so in a light theme it is a deep ochre rather than a bright yellow.
- Avoid pure white and pure black for backgrounds and text, as the existing themes do.

## Check the result

```bash
python3 build.py                # prints the plugin zip, the VS Code extension folder, the Sublime Text package, the Zed extension zip and the Neovim plugin zip, each with <n> themes
python3 preview.py <theme>      # writes themes/<theme>/build/preview.html
python3 preview.py --vscode <theme>   # writes themes/<theme>/build/preview-vscode.html
python3 preview.py --sublime <theme>  # writes themes/<theme>/build/preview-sublime.html
python3 preview.py --zed <theme>      # writes themes/<theme>/build/preview-zed.html
python3 preview.py --nvim <theme>     # writes themes/<theme>/build/preview-nvim.html
```

Open the preview in a browser. It shows each theme as an Islands IDE window, with the frame, the tool window and editor islands, and a sample in Java, Kotlin, Groovy (Spock), Python, TypeScript, React (TSX), Vue, HTML, CSS, SQL, Go, Rust, C++, C, C#, shell, YAML, JSON, TOML and Markdown. Code colours come from the generated scheme, so the preview shows what the scheme sets. Check that:

- every syntax role is distinguishable and readable against `bg`
- the caret row, caret and Spock labels are visible
- the frame sets the islands apart and stays in the family's colours
- no language sample has colours that clash with the palette
- the VS Code, Sublime Text, Zed and Neovim previews read like the IntelliJ one

In the IDE, install `build/heritage-themes-<version>.jar` through **Settings | Plugins | ⚙ | Install Plugin from Disk…**, restart, select each theme and also check the Project view, a diff, the console and a popup.

## Map a language-specific key

Language plugins define their own text attribute keys, which fall back to the `DEFAULT_*` keys mapped in `heritage/scheme.py`. A key that Darcula, Default or a plugin's `<additionalTextAttributes>` file colours explicitly ignores that fallback and keeps the IDE's colour in every theme. List such keys from installed IDEs:

```bash
scripts/parent_overrides.py ~/.local/share/JetBrains/Toolbox/apps/pycharm ~/.local/share/JetBrains/Toolbox/apps/webstorm
```

Map the ones that affect code to a palette role in `heritage/scheme.py`, in the section for that language. The script sees only the IDEs passed to it: keys from GoLand, CLion, Rider or RustRover need those IDEs.

A preview sample marks code with `«key:text»` in `heritage/samples.py`, using a key from the scheme or an alias from `ALIASES` in `heritage/preview.py`. A key the scheme does not set needs an entry in `FALLBACKS` there, following the plugin's own fallback chain.

## Add the documentation

Add these to the theme folder:

- `README.md`, in the same shape as `themes/shuimo/README.md`:
  1. `# <Family>`
  2. One paragraph: dark and light themes based on the tradition, naming both UI themes and stating that each has a matching editor colour scheme
  3. `![Preview](preview.png)`
  4. `## Inspiration`: the colour tradition and a table mapping sources to syntax roles, in neutral descriptive language
  5. `## Develop`: the same paragraph as in `themes/shuimo/README.md`
- `preview.png`, rendered with `python3 preview.py --png <theme>`. It needs Google Chrome or Chromium and ImageMagick. Every image has the same width; its height grows with the number of themes in the family.

## Register the theme

1. Add a row to the table in the root `README.md`: `` | [`themes/<theme>/`](themes/<theme>/) | <Theme A>, <Theme B> | <Country> | ``.
   `<Country>` is the country name only, even for a region inside it; a tradition that spans borders lists every country, separated by commas.
2. Add a line under `### Added` in `[Unreleased]` in each of `CHANGELOG.md`, `vscode/CHANGELOG.md`, `sublime/CHANGELOG.md`, `zed/CHANGELOG.md` and `nvim/CHANGELOG.md`: `- <Theme A> and <Theme B>, drawn from <tradition>.`
3. Run `python3 build.py` again.
4. Commit on `dev` as `feat(<theme>): add <Theme A> and <Theme B> themes`, limited to the theme folder, the root README row and the changelog entries. Releasing is described in [releasing.md](releasing.md).
