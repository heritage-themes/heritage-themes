# Themes for JetBrains

Colour themes for IntelliJ-based IDEs. Each top-level folder is one theme family, built as its own IDE plugin.

| Folder | Themes |
| --- | --- |
| [`wuxing/`](wuxing/) | Wuxing Day, Wuxing Night |

## Layout

```text
<theme>/
  gen.py        generates the editor schemes, theme JSON, plugin.xml and jar into build/
  README.md     what the theme is, how to build and install it
  assets/       plugin icons (pluginIcon.svg, pluginIcon_dark.svg)
  preview.png   screenshot used by the README
  build/        generated, not tracked
```

Only sources are tracked. Jars and `.icls` files are build output; publish them as release assets.

## Git workflow

- `master` is always releasable. Work on short-lived branches (`<theme>/<topic>`) and merge them into `master`.
- Commit subjects start with the theme folder: `wuxing: soften comment contrast`. Use `repo:` for changes outside any theme.
- Keep a commit within one theme.
- Tag each release `<theme>/v<version>` (for example `wuxing/v1.0.1`). The version matches `<version>` in that theme's `plugin.xml`.

## Add a theme

1. Create `<theme>/` with its own `gen.py`, `README.md` and `preview.png`.
2. Give the plugin a unique id in its `plugin.xml`.
3. Add `assets/pluginIcon.svg` and `assets/pluginIcon_dark.svg`.
4. Add a row to the table above.

## Licence

[MIT](LICENSE)
