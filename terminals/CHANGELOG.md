# Heritage Themes for terminals Changelog

## [Unreleased]

### Changed

- Termux: the install instructions create `~/.termux` first and say that the extra keys row stays black.
- iTerm2: the install instructions explain that, with **Use separate colors for light and dark mode** on, a preset sets only the mode chosen under **Editing**, and how to set a Night and Day pair that follows the system's appearance.

## [1.8.0] - 2026-11-07

### Added

- A powerline prompt for Oh My Posh, `<theme>-powerline.omp.json`, with a filled segment in an ANSI colour for the folder, the Git branch and status, the duration of a slow command and the exit status of a failed one, joined by arrows.

### Fixed

- PowerShell: a colour name that a version of PowerShell or PSReadLine does not know no longer stops the theme from setting the colours after it, and leaves no errors in `$Error`.

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

- Themes for 26 terminal emulators, shells, prompts and multiplexers, one for each Heritage theme: kitty, Alacritty, WezTerm, Ghostty, iTerm2, Windows Terminal, foot, Konsole, Terminator, XTerm, st, Rio, Contour, Warp, Tabby, Hyper and Termux; fish, zsh, Nushell and PowerShell; Starship, Oh My Posh and Powerlevel10k; tmux and Zellij. The terminal emulators take the 16 ANSI colours of the editor themes' terminals; the shells colour the command line in the editor themes' syntax roles.
