# Adding a theme

Add a theme family, usually a dark and a light theme, to the Heritage Themes plugin. A family supplies only palettes; every colour mapping, the UI theme and the preview are shared code in `heritage/`.

## How a family is built

Any top-level folder with a `theme.py` is a theme family. `heritage.load_families()` finds it, so neither `build.py` nor `preview.py` needs a change for a new family. `theme.py` defines:

| Name | Content |
| --- | --- |
| `FAMILY` | Family name, for example `"Shuimo"`; shown in the plugin description |
| `BLURB` | One sentence for the plugin description: the tradition and its main syntax mappings |
| `THEMES` | One `dict(slug=..., id=..., palette=...)` per theme; `id` is a new UUID |

From each palette, `heritage/scheme.py` builds the editor colour scheme and `heritage/ui.py` builds the UI theme. `build.py` packs them into the plugin and writes a standalone `.icls` per theme. `slug`, `id` and `name` must be unique across all themes; `build.py` fails otherwise.

A change in `heritage/` changes every family. After one, render all previews and check each family.

## Create the folder

Create `<theme>/theme.py` in the shape of `shuimo/theme.py`: a docstring, a comment describing the colour tradition and the syntax roles it maps to, the palettes, then `FAMILY`, `BLURB` and `THEMES`.

Names follow one pattern:

| Item | Example |
| --- | --- |
| Folder | `shuimo` |
| `slug` | `ShuimoNight` |
| Palette `name` | `Shuimo Night` |

The second word of a theme name is its setting in the tradition: Night and Day for Shuimo, Ink and Paper for Danqing, Baluchari and Laal Paar for Bengal.

### Palette

A palette is a dict of six-digit uppercase hex values without `#`, plus metadata. The shared code reads keys directly, so a missing key raises `KeyError`. Both palettes of a family have identical keys.

| Group | Keys |
| --- | --- |
| Metadata | `name`, `dark`, `parent`, `parentTheme` |
| Surfaces | `bg` (editor), `bgUi`, `bgTool`, `surface` (popups, fields), `hover`, `border` |
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
| `parentTheme` | `"ExperimentalDark"` | `"ExperimentalLight"` |

Optional keys:

| Key | Default | Effect |
| --- | --- | --- |
| `caret` | value of `gold` | Caret colour |
| `kwBold` | bold in light themes, regular in dark | Whether keywords are bold |

Key names are roles, not colours. `gold`, `red` and `azure` are slots whose value can be any colour that fits the tradition. To see which editor and UI elements use a role, search for it in `heritage/scheme.py` and `heritage/ui.py`.

Constraints:

- `fileYellow` colours folders that IntelliJ marks as excluded, such as `node_modules`. Use a faint wash close to `bg`, never a saturated colour. A solid colour draws the Project view as coloured bars.
- `label` colours Spock labels (`given:`, `when:`, `then:`) as bold text with no background. It needs the same contrast against `bg` as the syntax roles.
- The `ansi*` keys colour ANSI output in the console and terminal. Each must read as the hue it names, whatever the family's syntax roles are, and meet 4.5:1 against `bg`.
- Avoid pure white and pure black for backgrounds and text, as the existing themes do.

## Check the result

```bash
python3 build.py                # prints build/heritage-themes-<version>.zip: <n> themes
python3 preview.py <theme>      # writes <theme>/build/preview.html
```

Open the preview in a browser. It shows each theme as an IDE window with a sample in Java, Kotlin, Groovy (Spock), Python, TypeScript, React (TSX), Vue, HTML, CSS, SQL, Go, Rust, C++, C, C#, shell, YAML, JSON, TOML and Markdown. Code colours come from the generated scheme, so the preview shows what the scheme sets. Check that:

- every syntax role is distinguishable and readable against `bg`
- the caret row, caret and Spock labels are visible
- no language sample has colours that clash with the palette

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

- `README.md`, in the same shape as `shuimo/README.md`:
  1. `# <Family>`
  2. One paragraph: dark and light themes based on the tradition, naming both UI themes and stating that each has a matching editor colour scheme
  3. `![Preview](preview.png)`
  4. `## Inspiration`: the colour tradition and a table mapping sources to syntax roles, in neutral descriptive language
  5. `## Develop`: the same paragraph as in `shuimo/README.md`
- `preview.png`, rendered with `python3 preview.py --png <theme>`. It needs Google Chrome or Chromium and ImageMagick. Every image has the same width; its height grows with the number of themes in the family.

## Register the theme

1. Add a row to the table in the root `README.md`: `` | [`<theme>/`](<theme>/) | <Theme A>, <Theme B> | ``.
2. Add a line under `### Added` in `[Unreleased]` in `CHANGELOG.md`: `- <Theme A> and <Theme B>, drawn from <tradition>.`
3. Run `python3 build.py` again.
4. Commit on `dev` as `feat(<theme>): add <Theme A> and <Theme B> themes`, limited to the theme folder, the root README row and the changelog entry. Releasing is described in [releasing.md](releasing.md).
