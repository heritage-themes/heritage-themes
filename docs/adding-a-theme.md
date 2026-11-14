# Adding a theme

Add a theme family, usually a dark and a light theme. A family supplies only palettes; every colour mapping, the UI theme and the previews are shared code in `heritage/`, so a new family appears in every product without a change to `build.py` or `preview.py`.

## How a family is built

Any folder in `themes/` with a `theme.py` is a theme family. `heritage.load_families()` finds it. `theme.py` defines:

| Name | Content |
| --- | --- |
| `FAMILY` | Family name, for example `"Shuimo"`; shown in the plugin description |
| `BLURB` | One sentence for the plugin description: the tradition and its main syntax mappings |
| `THEMES` | One `dict(slug=..., id=..., palette=...)` per theme; `id` is a new UUID |

`slug`, `id` and `name` must be unique across all themes; `build.py` fails otherwise. One module per product in `heritage/` turns each palette into that product's theme files, and `build.py` packs and validates them. `heritage/__init__.py` imports every module.

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

A name that does not say Night or Day ends in ` (Dark)` or ` (Light)`, matching `dark`, so every theme list shows the brightness: `Edo Cha (Dark)`, `Edo Nezumi (Light)`. Products that name a theme by a lower-case identifier carry it too: `heritage-edo-cha-dark`, `heritage_edo_nezumi_light`. The `slug` omits the suffix.

Notepad++ and Xcode list a theme by its file name, so the palette `name` is a Windows file name: none of `< > : " / \ | ? *`, and no trailing space or full stop. `build.py` fails otherwise.

### Palette

A palette is a dict of six-digit uppercase hex values without `#`, plus metadata. The shared code reads keys directly, so a missing key raises `KeyError`. Both palettes of a family have identical keys.

| Group | Keys |
| --- | --- |
| Metadata | `name`, `dark`, `parent` |
| Surfaces | `bg` (editor), `bgUi`, `bgTool`, `frame`, `surface` (popups, fields), `hover`, `border` |
| Text | `fg`, `muted`, `disabled` |
| Selection and caret | `caretRow`, `selection`, `selInactive` |
| Gutter | `lineNo`, `lineNoCaret`, `guide`, `guideSel` |
| Syntax | `keyword`, `string`, `number`, `type`, `method`, `call`, `field`, `constant`, `annotation`, `directive`, `comment`, `doc`, `docTag`, `op`, `param`, `typeParam` |
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

Key names are roles, not colours. `gold`, `red` and `azure` are slots whose value can be any colour that fits the tradition. To see which elements use a role, search for it in `heritage/`.

Constraints, all enforced by `build.py`:

- `frame` is the main window behind the editor and tool windows, which the Islands UI draws as rounded islands of `bg` and `bgTool`. Take it from the hue of `bg`: lighter than both `bg` and `bgTool` in a dark theme, darker in a light one, by at least 1.20:1.
- `directive` colours preprocessor directives such as C and C++ `#include` and `#define`. It is at least 20 CIELAB units (CIE76) from `keyword`, `annotation`, `constant`, `comment`, `muted` and `fg`, so a directive stands apart from keywords, macro names, comments, excluded code and plain text. A mix of two of the palette's own colours usually fits. The JetBrains scheme has no key for directives; the other products use it.
- `fileYellow` colours folders that IntelliJ marks as excluded, such as `node_modules`. Use a faint wash close to `bg`, never a saturated colour. A solid colour draws the Project view as coloured bars.
- `label` colours Spock labels (`given:`, `when:`, `then:`) as bold text with no background. It needs the same contrast against `bg` as the syntax roles.
- The `ansi*` keys colour ANSI output in the console and terminals, and VCS file status in the Project view: `ansiGreen` added, `ansiBlue` modified, `ansiRed` unversioned, `ansiMagenta` merged. Each must read as the hue it names, whatever the family's syntax roles are.
- Roles meet WCAG AA against the backgrounds they are drawn on: 4.5:1 for text, 3:1 for comments, the caret and `gold` as the focus ring. `CONTRAST` in `build.py` lists the pairs. `gold` also colours string escapes, so in a light theme it is a deep ochre rather than a bright yellow.
- Avoid pure white and pure black for backgrounds and text, as the existing themes do.

## Check the result

```bash
python3 build.py                     # builds and validates every product; prints each archive with its theme count
python3 build.py --vsix --jupyterlab # also packs the VS Code extension and the JupyterLab wheel, as CI does
python3 preview.py <theme>           # writes themes/<theme>/build/preview.html, the JetBrains preview
python3 preview.py --<product> <theme>  # the preview of another product, for example --vscode or --helix
python3 preview.py --help            # lists the products
```

Some previews need the product or a tool on the machine: Visual Studio needs Windows, Xcode needs macOS, and the terminal and editor previews need Linux and Podman. A preview that cannot run says what it needs.

Open the preview in a browser. The JetBrains preview shows each theme as an Islands IDE window, with the frame, the tool window and editor islands, and a sample in Java, Kotlin, Groovy (Spock), Python, TypeScript, React (TSX), Vue, HTML, CSS, SQL, Go, Rust, C++, C, C#, shell, YAML, JSON, TOML and Markdown. Code colours come from the generated files, so the preview shows what they set. Check that:

- every syntax role is distinguishable and readable against `bg`
- the caret row, caret and Spock labels are visible
- the frame sets the islands apart and stays in the family's colours
- no language sample has colours that clash with the palette
- the C and C++ samples draw directives in a colour that differs from keywords and macro names
- the previews of the other products read like the JetBrains one

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
2. Add a line under `### Added` in `[Unreleased]` in the changelog of every product. `docs/releasing.md` lists them. The line reads `- <Theme A> and <Theme B>, drawn from <tradition>.`
3. Run `python3 build.py` again.
4. Commit on `dev` as `feat(<theme>): add <Theme A> and <Theme B> themes`, limited to the theme folder, the root README row and the changelog entries.
