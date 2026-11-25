# Heritage Themes for Visual Studio Changelog

## [Unreleased]

## [1.25.0] - 2026-11-25

### Fixed

- The terminal colours keep WCAG AA contrast on the selection, in focused and unfocused views. In 40 themes the red, green, yellow, blue, magenta or cyan that fell short is a shade lighter in dark themes or darker in light ones, with its hue kept.

## [1.24.0] - 2026-11-24

### Fixed

- Code and text keep WCAG AA contrast on the theme's green and red highlight backgrounds, as on added and removed lines in diffs and merges, breakpoints and code coverage. In 44 themes those backgrounds are a shade lighter in light themes or darker in dark ones, with their hue and depth of colour kept.

## [1.11.1] - 2026-11-14

### Fixed

- Preprocessor directives, such as C and C++ `#include` and `#define`, no longer take the keyword colour. They take a colour of their own, which also stands apart from the macro a `#define` names, from comments and from excluded code.

## [1.8.2] - 2026-11-10

### Fixed

- C++ enum members take the constant colour, as in C#, instead of the type colour, so they stand apart from the enum's name.

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

### Fixed

- Code keeps WCAG AA contrast on the current line's highlight. In 33 themes, the code colours that fell just below 4.5:1 on it are a shade darker in light themes or lighter in dark ones.
- The current line's number in Kerala Kasavu (Light) reaches 4.5:1.

## [1.4.0] - 2026-10-25

### Added

- Themes for Visual Studio 2026, one for each Heritage theme. They colour the window, tool windows, tabs, menus, dialogs, status bar and terminal through Visual Studio's Fluent colour tokens, and the editor in every language it highlights, from the theme's palette.
