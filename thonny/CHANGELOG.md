# Heritage Themes for Thonny Changelog

## [Unreleased]

### Fixed

- The terminal colours keep WCAG AA contrast on the selection, in focused and unfocused views. In 40 themes the red, green, yellow, blue, magenta or cyan that fell short is a shade lighter in dark themes or darker in light ones, with its hue kept.
- ANSI black is the background of the terminal panel, so black text on the other terminal colours, as lazygit draws search matches, keeps WCAG AA contrast. Bright black stays the colour of faint text.

## [1.24.0] - 2026-11-24

### Fixed

- Code and text keep WCAG AA contrast on the theme's green and red highlight backgrounds, as on the shell's completed and failed commands. In 44 themes those backgrounds are a shade lighter in light themes or darker in dark ones, with their hue and depth of colour kept.

## [1.10.0] - 2026-11-12

### Added

- A UI theme and a syntax theme for Thonny 4.0 and later, one of each for every Heritage theme, in one plugin on PyPI, `thonny-heritage-themes`. Install it under Tools | Manage plug-ins and choose a theme of the same name as UI theme and as syntax theme under Tools | Options | Theme & Font. The UI theme colours the window; the syntax theme colours the editor and the shell: code, the current line, the selection, other occurrences of a name, found text, brackets, an unclosed string, the shell's output and errors, ANSI colours and the debugger's boxes.
