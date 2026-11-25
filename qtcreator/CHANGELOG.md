# Heritage Themes for Qt Creator Changelog

## [Unreleased]

### Fixed

- The terminal colours keep WCAG AA contrast on the selection, in focused and unfocused views. In 40 themes the red, green, yellow, blue, magenta or cyan that fell short is a shade lighter in dark themes or darker in light ones, with its hue kept.
- ANSI black is the background of the terminal panel, so black text on the other terminal colours, as lazygit draws search matches, keeps WCAG AA contrast. Bright black stays the colour of faint text.

## [1.24.0] - 2026-11-24

### Fixed

- Code and text keep WCAG AA contrast on the theme's green and red highlight backgrounds, as on added and removed lines in diffs and code coverage. In 44 themes those backgrounds are a shade lighter in light themes or darker in dark ones, with their hue and depth of colour kept.

## [1.11.1] - 2026-11-14

### Fixed

- Preprocessor directives, such as C and C++ `#include` and `#define`, no longer take the keyword colour. They take a colour of their own, which also stands apart from comments.

## [1.7.3] - 2026-11-05

### Changed

- No change to the themes beyond 1.7.0, which was not published. This version publishes them.

## [1.7.2] - 2026-11-05

### Changed

- No change to the themes beyond 1.7.0, which was not published. This version publishes them.

## [1.7.1] - 2026-11-05

### Changed

- No change to the themes beyond 1.7.0, which was not published. This version publishes them.

## [1.7.0] - 2026-11-05

### Added

- Themes for Qt Creator, one for each Heritage theme, each with an editor colour scheme of the same name. They colour the window, panels, output panes, the terminal, version control and the debugger, and the editor's code, line numbers, selections, search results, diagnostics, diffs and code coverage from the theme's palette.
