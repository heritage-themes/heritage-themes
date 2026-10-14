Heritage Themes is one JetBrains plugin with colour themes drawn from cultures' colour traditions. Each theme
family is a folder with a `theme.py` holding its palettes; all colour mappings, the UI theme and the preview
are shared code in `heritage/`. `python3 build.py` builds and validates the plugin. Work on `dev`; see the
root README for layout, previews and the git workflow.

## Adding a new culture-based theme

When adding a theme, follow docs/adding-a-theme.md (folder layout, `theme.py`, palette keys, README, preview,
registration). If it disagrees with the most recently added theme folder, tell me which one is out of date.

Workflow:

1. If no culture is named, pick one where colour carries real meaning. Research it with web search and prefer
   named traditional colours and concrete systems (rank colours, seasonal layers, pigments, dyes).
2. Propose 1-4 concepts, each a Night/Day pair, and let me choose unless I said "do all".
3. Create each family as described in docs/adding-a-theme.md: `theme.py`, `README.md`, `preview.png`. There is
   no `build.py` registration (it discovers `theme.py` files itself); register by adding the root `README.md`
   table row and the `CHANGELOG.md` `[Unreleased]` entry.
4. Run `python3 build.py`, then `python3 preview.py --png <theme>` to render the preview page and
   `preview.png`. Look at the rendered PNG yourself. Stop there: do not install the jar in the IDE or do the
   manual IDE checks; I do those. Do not send me the jar.
5. Check before finishing: every UI colour reference resolves; text roles meet WCAG AA against `bg` (comments
   may be about 3:1); fields and method calls are clearly distinct from plain text and from each other, unless
   the concept builds hierarchy from tone and weight rather than hue, as Shuimo does.
6. Commit on `dev` as `feat(<theme>): ...`, limited to the new theme folder, the root README row and the
   changelog entry.

Language coverage:

The themes must look good in the most popular languages, not only Java: Java, Kotlin, Groovy, Python,
JavaScript, TypeScript, JSX/TSX, Vue, HTML, CSS, SQL, Go, Rust, C++, C, C#, shell, and the config and docs
formats YAML, JSON, TOML and Markdown. The generic syntax roles carry most of this, but language-specific
highlighting (HTML tags and attributes, CSS properties and selectors, SQL keywords and functions, Python
decorators, Rust lifetimes and macros, C/C++ preprocessor directives, TypeScript types, Go package names, and
so on) can fall back to the parent scheme (Darcula or Default) and clash with the palette. The preview has a
sample in each of these languages, coloured from the generated scheme; check every sample in the rendered
PNG. Where a colour clashes or is hard to read, change the mapping in `heritage/scheme.py`, never per
family, and render every family's preview again, since the change affects them all. Find keys that the IDEs
colour explicitly with `scripts/parent_overrides.py`; never guess key names.

Conventions:

- UI themes cover the chrome (run widget, VCS log, banners, popups, welcome screen, plugin pages, tabs,
  scrollbars, buttons, progress bars), not only the editor. `heritage/ui.py` does this; do not cut it down.
- `fileYellow` is a faint wash close to `bg`, never a saturated colour.
- No pure black or pure white backgrounds unless the culture's palette demands it.
- Night: lighter, slightly desaturated colours. Day: deeper colours, so contrast holds.
- README Inspiration table: neutral, descriptive language. Use the culture's own words for colours and
  concepts, with the original script where relevant.
- Hex values are interpretations of traditional colours; say so in the README where it matters.
- British English in docs.
