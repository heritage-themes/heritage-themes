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
- Roles meet WCAG AA against the backgrounds they are drawn on: 4.5:1 for text, 3:1 for comments, the caret and `gold` as the focus ring. `CONTRAST` in `build.py` lists the pairs. Diffs draw code on `diffIns` and `diffDel`, so the syntax roles need 4.5:1 on them too; reach it by changing their lightness, not their hue. lazygit keeps the `ansi*` colours on its selected rows, so they need 4.5:1 on `selection` and `selInactive` as well. `gold` also colours string escapes, so in a light theme it is a deep ochre rather than a bright yellow.
- Avoid pure white and pure black for backgrounds and text, as the existing themes do, unless the tradition's palette demands it.

## Check the result

```bash
python3 build.py                     # builds and validates every product; prints each archive with its theme count
python3 build.py --vsix --jupyterlab --netbeans # also packs the VS Code extension, the JupyterLab wheel and the NBM, as CI does
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

## Check the RStudio token rules

RStudio colours code by Ace token types, which every language shares. `syntax()` in `heritage/rstudio.py` maps them to palette roles. List the token types of an installed RStudio that no rule colours, and the selectors that match no type:

```bash
scripts/rstudio/tokens.py <RStudio folder>
```

Add a selector only for a type that the script lists, and run `python3 build.py`: it resolves a table of token types in every theme (`cases()` in `heritage/rstudio.py`) and fails when a rule with more classes does not reset the font of one with fewer.

## Check the Godot settings

A Godot text editor theme sets the colour settings under `text_editor/theme/highlighting/`. `ROLES` and `MIXES` in
`heritage/godot.py` map them to palette roles. List the settings of an installed Godot that the map leaves out, and
those it sets that Godot does not have:

```bash
scripts/godot/settings.py [<Godot executable>]
```

It runs the editor once without a window, in temporary folders, and exits with 1 when either list is not empty.

## Check the NetBeans colourings

`heritage/netbeans.py` writes each language's colourings with the names and inheritance of NetBeans' default profile,
which `heritage/netbeans.json` records; NetBeans ignores a colouring that its default profile does not define. After a
NetBeans release, compare the record with an installation, and write it again when they differ:

```bash
scripts/netbeans/colorings.py <NetBeans folder>          # lists the differences, exit status 1 when there are any
scripts/netbeans/colorings.py <NetBeans folder> --write  # writes heritage/netbeans.json
```

The NetBeans folder is the one with the `platform` and `ide` clusters, for example `files/netbeans` in the Flatpak's
location (`flatpak info --show-location org.apache.netbeans`). `python3 build.py` then fails for every colouring that
NetBeans colours itself and `overrides()` does not give a role.

## Check the DrRacket colour names

`COLOURS` and `styles()` in `heritage/drracket.py` map the colour and style names that DrRacket registers to palette
roles; DrRacket ignores a name it does not register. After a DrRacket release, start it with the colour-scheme log on
and compare the `color-names` and `style-names` that it prints with the map:

```bash
PLTSTDERR="info@color-scheme error" drracket                                   # a native installation
flatpak run --env=PLTSTDERR="info@color-scheme error" org.racket_lang.Racket    # the Flatpak
```

## Test the DrRacket schemes locally

Build the package, install the zip as a copy and pick a scheme in DrRacket:

```bash
python3 build.py
raco pkg remove heritage-themes    # skip when it is not installed
raco pkg install --copy --name heritage-themes build/heritage-themes-drracket-<version>.zip
raco pkg show heritage-themes      # Source names the zip
```

Restart DrRacket and choose a scheme under **Edit | Preferences | Colors | Color Schemes**. DrRacket keeps one scheme
for light mode and one for dark mode: set **Color Mode** to always light or always dark, or the scheme of the other
mode stays on screen. Open a `.rkt` file, click **Run**, enter `(car 1)` in the REPL for an error, click
**Check Syntax** and put the caret on an identifier.

Install a copy, not a link: `raco` compiles a linked package inside its folder, and `build.py` deletes `build/` on
every run. A link to a folder that the Flatpak mounts read-only fails to compile.

With the Flatpak, `raco` is `flatpak run --command=raco org.racket_lang.Racket`, and the package reads only folders
that it has been given. Add `--filesystem=<heritage-themes folder>:ro` to the command. Set `PLTUSERHOME=<empty folder>`
on `raco` and on DrRacket to test without touching the installed preferences and packages.

## Check the Kate definition rules

Kate colours code by KSyntaxHighlighting's default styles. `language_rules()` in `heritage/kate.py` names items of the library's syntax definitions, which `heritage/kate.json` lists with the colours that some items set themselves. Rewrite the file from the library in the editors image after a KDE Frameworks update:

```bash
podman build -t localhost/heritage-editors scripts/editors
podman run --rm --userns=keep-id -v "$PWD:/repo:Z" localhost/heritage-editors \
    python3 /repo/scripts/kate/definitions.py /repo/heritage/kate.json
```

`python3 build.py` then fails on a rule that names an item the library lacks, and on an item whose own colours no theme replaces.

## Check the GNOME Text Editor style rules

GNOME Text Editor colours code by GtkSourceView's styles. `language_rules()` in `heritage/gnome_text_editor.py` names styles of the library's language definitions, which `heritage/gnome_text_editor.json` lists with the style each maps to. Rewrite the file from the library in the editors image after a GtkSourceView update:

```bash
podman build -t localhost/heritage-editors scripts/editors
podman run --rm --userns=keep-id -v "$PWD:/repo:Z" localhost/heritage-editors \
    python3 /repo/scripts/gnome-text-editor/definitions.py /repo/heritage/gnome_text_editor.json
```

`python3 build.py` then fails on a rule or scheme style that names a style the library lacks.

## Check the gedit style rules

gedit colours code by the styles of libgedit-gtksourceview, whose language definitions `heritage/gedit.json` lists. A gedit scheme gives each style the colours of GNOME Text Editor's style of the same id; `language_rules()` in `heritage/gedit.py` sets the styles that GtkSourceView 5 lacks. Rewrite the file from the library in the editors image after a gedit update:

```bash
podman build -t localhost/heritage-editors scripts/editors
podman run --rm --userns=keep-id -v "$PWD:/repo:Z" localhost/heritage-editors \
    python3 /repo/scripts/gedit/definitions.py /repo/heritage/gedit.json
```

`python3 build.py` then fails on a rule or scheme style that names a style the library lacks.

## Check the yazi defaults

A yazi flavor sets every style key of yazi's default themes, keeps their file type rules and recolours their icons, all of which `heritage/yazi.json` lists. Rewrite the file from a yazi release after a yazi update:

```bash
python3 scripts/yazi/preset.py <version> heritage/yazi.json
```

`python3 build.py` then fails on a style key that `settings()` in `heritage/yazi.py` lacks or sets beyond yazi's, and on a file type rule that `FILETYPES` does not cover.

## Check the Geany named styles

A Geany scheme sets every named style of Geany's `filetypes.common`, which `NAMED_STYLES` in `heritage/geany.py` lists. After a Geany update, compare the two in the editors image; the command prints nothing when they match:

```bash
podman build -t localhost/heritage-editors scripts/editors
podman run --rm --userns=keep-id -v "$PWD:/repo:Z" -w /repo localhost/heritage-editors python3 -c '
import configparser, heritage.geany as g
c = configparser.ConfigParser(delimiters=("=",), comment_prefixes=("#",), interpolation=None, strict=False)
c.optionxform = str
c.read("/usr/share/geany/filedefs/filetypes.common")
print(sorted(set(c["named_styles"]) ^ set(g.NAMED_STYLES)) or "", end="")'
```

## Check the Pulsar UI stylesheets

A Pulsar UI theme takes the stylesheets in `heritage/pulsar-ui`, which are Pulsar's One UI stylesheets (`packages/one-dark-ui/styles` in Pulsar's repository) with every computed colour replaced by a variable that `ui_variables()` in `heritage/pulsar.py` sets from the palette. After a Pulsar update, compare them with the release's and carry its changes over, keeping the variables:

```bash
git clone --depth 1 --branch v<version> https://github.com/pulsar-edit/pulsar /tmp/pulsar
diff -r /tmp/pulsar/packages/one-dark-ui/styles heritage/pulsar-ui
```

`python3 build.py` fails on a variable that no stylesheet defines and on a colour that is not `#RRGGBB`. `python3 preview.py --pulsar` fails on a colour that is not the palette's.

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
