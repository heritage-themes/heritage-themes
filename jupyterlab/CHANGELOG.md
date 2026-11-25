# Heritage Themes for JupyterLab Changelog

## [Unreleased]

## [1.25.0] - 2026-11-25

### Fixed

- The terminal colours keep WCAG AA contrast on the selection, in focused and unfocused views. In 40 themes the red, green, yellow, blue, magenta or cyan that fell short is a shade lighter in dark themes or darker in light ones, with its hue kept.
- ANSI black is the background of the terminal panel, so black text on the other terminal colours, as lazygit draws search matches, keeps WCAG AA contrast. Bright black stays the colour of faint text.

## [1.9.0] - 2026-11-11

### Added

- Support for Notebook 7.6 and later: the themes colour its file page and notebooks, and the extension installs the same way.

## [1.8.1] - 2026-11-10

### Added

- Themes for JupyterLab 4.6 and later, one for each Heritage theme, in one extension on PyPI, `jupyterlab-heritage-themes`. They colour the menu bar, tabs, tool bars, side panels, dialogs, notebooks with their cells and outputs, including the ANSI colours of tracebacks, and the code of notebooks, consoles and text editors from the theme's palette.
