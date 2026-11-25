# Heritage Themes for GNU Emacs Changelog

## [Unreleased]

### Fixed

- The terminal colours keep WCAG AA contrast on the selection, in focused and unfocused views. In 40 themes the red, green, yellow, blue, magenta or cyan that fell short is a shade lighter in dark themes or darker in light ones, with its hue kept.
- ANSI black is the background of the terminal panel, so black text on the other terminal colours, as lazygit draws search matches, keeps WCAG AA contrast. Bright black stays the colour of faint text.

## [1.24.0] - 2026-11-24

### Fixed

- Code and text keep WCAG AA contrast on the theme's green and red highlight backgrounds, as on added and removed lines in diffs, merge conflicts and highlights. In 44 themes those backgrounds are a shade lighter in light themes or darker in dark ones, with their hue and depth of colour kept.

## [1.11.1] - 2026-11-14

### Fixed

- Preprocessor directives, such as C and C++ `#include` and `#define`, no longer take the keyword colour. They take a colour of their own, which also stands apart from comments, in C, C++ and the other modes that use `font-lock-preprocessor-face`.

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

## [1.6.0] - 2026-11-03

### Added

- Themes for GNU Emacs 29.1 and later, one for each Heritage theme. They colour Emacs itself, font-lock and the Tree-sitter modes, and the packages that ship with Emacs, among them Org, Dired, Eglot, Flymake, diff and Ediff, from the theme's palette.
