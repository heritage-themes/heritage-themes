# Heritage Themes for Vim Changelog

## [Unreleased]

### Changed

- No change to the themes beyond 1.7.0, which was not published. This version publishes them.

## [1.7.0] - 2026-11-05

### Fixed

- Code keeps WCAG AA contrast on the current line's highlight. In 33 themes, the code colours that fell just below 4.5:1 on it are a shade darker in light themes or lighter in dark ones.
- The current line's number in Kerala Kasavu (Light) reaches 4.5:1.

## [1.6.0] - 2026-11-03

### Added

- Colour schemes for Vim 9.0 and later, one for each Heritage theme. They colour the editor, syntax groups, the status line, tab line, tab panel, popup windows, the completion menu, diff mode, spelling and the terminal window from the theme's palette, in 24-bit colour with `termguicolors` and the nearest of 256 colours without it.
