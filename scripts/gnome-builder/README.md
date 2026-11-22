# GNOME Builder test project

`setup.sh [DIR] [--open]` creates a project in `DIR` (default `~/heritage-builder-test`) with the files below,
committed in an earlier state so that the working tree differs from `HEAD`. `--open` starts Builder on it.
Install the schemes first: `cp build/gnome-text-editor/styles/*.xml ~/.local/share/gtksourceview-5/styles/`.

| To see | Open | Do |
| --- | --- | --- |
| Error, warning, deprecated and unused underlines, gutter icons | `diagnostics.c` | Wait for the diagnostics: two errors in `main`, a format warning, a deprecated call and an unused variable in `warnings` |
| Added, changed and removed lines in the gutter | `main.c` | None: the line numbers' margin shows them against `HEAD` |
| Comment alert | `main.c` | None: `TODO` on line 3 |
| Quick highlight | `main.c` | Double-click `square`, then `Shift+Left`, `Shift+Right` |
| Link to a definition | `main.c` | Hold `Ctrl` over `square` in `sum_of_squares` and wait for the popover |
| Breakpoint | `main.c` | Click a line number; right-click it for a count point |
| Line the debugger stopped at | `main.c` | Set a breakpoint on line 23, choose **Run with Debugger** from the run menu |
| XML tag match and outline labels | `window.ui` | Put the caret in a tag, open the symbol outline in the status bar |
