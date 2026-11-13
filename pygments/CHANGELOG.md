# Heritage Themes for Pygments Changelog

## [Unreleased]

### Fixed

- Preprocessor directives (`Comment.Preproc`), such as C and C++ `#include` and `#define`, no longer take the keyword colour. They take the annotation colour, or the constant colour in the seven themes whose annotation colour is the keyword's or too near it, so a directive stands apart from `class` and `public`.

## [1.9.0] - 2026-11-11

### Added

- Styles for Pygments 2.14 and later, one for each Heritage theme, in one package on PyPI, `heritage-themes-pygments`. Each style registers under its name, such as `heritage-holi-night`, so `pygmentize`, `HtmlFormatter(style=...)`, Sphinx and every other program that takes a Pygments style name finds it. A style colours the tokens of Pygments' lexers, the background, the highlighted lines and the line numbers from the theme's palette.
