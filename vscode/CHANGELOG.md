# Heritage Themes for VS Code Changelog

## [Unreleased]

### Fixed

- The terminal colours keep WCAG AA contrast on the selection, in focused and unfocused views. In 40 themes the red, green, yellow, blue, magenta or cyan that fell short is a shade lighter in dark themes or darker in light ones, with its hue kept.
- ANSI black is the background of the terminal panel, so black text on the other terminal colours, as lazygit draws search matches, keeps WCAG AA contrast. Bright black stays the colour of faint text.

## [1.24.0] - 2026-11-24

### Fixed

- Code and text keep WCAG AA contrast on the theme's green and red highlight backgrounds, as on added and removed lines in the diff editor and input validation messages. In 44 themes those backgrounds are a shade lighter in light themes or darker in dark ones, with their hue and depth of colour kept.

## [1.22.0] - 2026-11-23

### Added

- Arduino IDE 2 support: the extension loads from Arduino IDE's `plugins` folder. The themes also colour the check mark on the selected board in the toolbar and the Serial Monitor's warning bar, whose text otherwise falls below 4.5:1 in 29 of the 65 themes.

## [1.11.1] - 2026-11-14

### Fixed

- Preprocessor directives, such as C and C++ `#include` and `#define`, no longer take the keyword colour. They take a colour of their own, which also stands apart from the macro a `#define` names and from comments.

## [1.7.3] - 2026-11-05

### Changed

- No change to the themes. Versions 1.7.0 to 1.7.2 did not get a GitHub release, and 1.7.3 publishes the same themes there.

## [1.7.2] - 2026-11-05

### Changed

- No change to the themes. Versions 1.7.0 and 1.7.1 did not get a GitHub release, and 1.7.2 publishes the same themes there.

## [1.7.1] - 2026-11-05

### Changed

- No change to the themes. Version 1.7.0 did not get a GitHub release, and 1.7.1 publishes the same themes there.

## [1.7.0] - 2026-11-05

### Fixed

- Code keeps WCAG AA contrast on the current line's highlight. In 33 themes, the code colours that fell just below 4.5:1 on it are a shade darker in light themes or lighter in dark ones.
- The current line's number in Kerala Kasavu (Light) reaches 4.5:1.
- Inserted, deleted and changed lines in diffs and Markdown, and invalid code, use the theme's terminal green, red or blue, which reach 4.5:1 in every theme.

## [1.2.1] - 2026-10-20

### Fixed

- Sponsor button on the Marketplace page linked to a Buy Me a Coffee page that does not exist.

## [1.2.0] - 2026-10-20

### Added

- Screenshots of four themes on the Marketplace page.

## [1.1.0] - 2026-10-20

### Added

- Sponsor button on the Marketplace page, linking to Buy Me a Coffee.

## [1.0.1] - 2026-10-19

### Fixed

- Publish the extension to the Visual Studio Marketplace. Version 1.0.0 reached Open VSX only.

## [1.0.0] - 2026-10-19

### Added

- Dark and light colour themes for VS Code, drawn from the colour traditions of 32 cultures. Each colours the workbench, TextMate scopes and semantic tokens from the same palettes as the JetBrains themes.
