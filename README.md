# Heritage Themes

Colour themes for IntelliJ-based IDEs, VS Code, Visual Studio, Sublime Text, Zed, Neovim, Notepad++, Xcode, Helix, Kakoune, Micro, Vim, GNU Emacs, Nano, Textadept, Lapce, Qt Creator, Amp, Eclipse, Nova, JupyterLab, Pygments, Spyder and Thonny, and for 26 terminal emulators, shells, prompts and multiplexers, each drawn from a culture's colour tradition. All themes ship in one JetBrains plugin (plugin ID `heritage.themes`), one VS Code extension (`heritage-themes.heritage-themes`), one Visual Studio extension (`heritage-themes.heritage-themes-visualstudio`), one Sublime Text package (`Heritage Themes`), one Zed extension (`heritage-theme`), one Neovim plugin (`heritage-themes/heritage-themes.nvim`), one JupyterLab extension (`jupyterlab-heritage-themes` on PyPI), one Pygments package (`heritage-themes-pygments` on PyPI), one Thonny plugin (`thonny-heritage-themes` on PyPI) and a zip for each other app on the [latest GitHub release](https://github.com/heritage-themes/heritage-themes/releases/latest), named `heritage-themes-<app>-<version>.zip`: `notepadpp`, `xcode`, `helix`, `kakoune`, `micro`, `vim`, `emacs`, `nano`, `textadept`, `lapce`, `qtcreator`, `amp`, `eclipse`, `nova` and `terminals`. Every GitHub release carries the current build of every product, and a file name shows the version of its build, so a release can hold builds of different versions; the release notes list the products that the release changes.

| Folder | Themes | Country |
| --- | --- | --- |
| [`themes/ainu/`](themes/ainu/) | Ainu Attus (Light), Ainu Kaparamip (Dark) | Japan |
| [`themes/aizome/`](themes/aizome/) | Aizome Kachi (Dark), Aizome Kamenozoki (Light) | Japan |
| [`themes/bengal/`](themes/bengal/) | Bengal Baluchari (Dark), Bengal Laal Paar (Light) | India, Bangladesh |
| [`themes/danqing/`](themes/danqing/) | Danqing Ink (Dark), Danqing Paper (Light) | China |
| [`themes/edo/`](themes/edo/) | Edo Cha (Dark), Edo Nezumi (Light) | Japan |
| [`themes/gujarat/`](themes/gujarat/) | Gujarat Navratri (Dark), Gujarat Rann (Light) | India |
| [`themes/hmong/`](themes/hmong/) | Hmong Batik (Dark), Hmong Hemp (Light) | Vietnam, Laos, Thailand, China |
| [`themes/holi/`](themes/holi/) | Holi Day, Holi Night | India |
| [`themes/kalaallisuut/`](themes/kalaallisuut/) | Kalaallisuut Qaqortoq (Light), Kalaallisuut Qernertoq (Dark) | Greenland |
| [`themes/kalamkari/`](themes/kalamkari/) | Kalamkari Cotton (Light), Kalamkari Indigo (Dark) | India |
| [`themes/kashubia/`](themes/kashubia/) | Kashubia Niebò (Light), Kashubia Zemia (Dark) | Poland |
| [`themes/kerala/`](themes/kerala/) | Kerala Backwaters (Dark), Kerala Kasavu (Light) | India |
| [`themes/lowicz/`](themes/lowicz/) | Łowicz Kodra (Light), Łowicz Wycinanka (Dark) | Poland |
| [`themes/maramures/`](themes/maramures/) | Maramureș Cânepă (Light), Maramureș Zadie (Dark) | Romania |
| [`themes/maya/`](themes/maya/) | Maya Corte (Dark), Maya Huipil (Light) | Guatemala |
| [`themes/morocco/`](themes/morocco/) | Morocco Majorelle (Dark), Morocco Marrakech (Dark), Morocco Zellige (Dark) | Morocco |
| [`themes/mudhif/`](themes/mudhif/) | Mudhif Qasab (Light), Mudhif Qir (Dark) | Iraq |
| [`themes/mughal/`](themes/mughal/) | Mughal Night, Mughal Wasli (Light) | India, Pakistan |
| [`themes/ndebele/`](themes/ndebele/) | Ndebele Mhlophe (Light), Ndebele Nzima (Dark) | South Africa |
| [`themes/peru/`](themes/peru/) | Peru Kulli (Dark), Peru Puka (Dark) | Peru |
| [`themes/podhale/`](themes/podhale/) | Podhale Kłobuk (Dark), Podhale Sukno (Light) | Poland |
| [`themes/punjab/`](themes/punjab/) | Punjab Basant (Light), Punjab Phulkari (Dark) | India, Pakistan |
| [`themes/rajasthan/`](themes/rajasthan/) | Rajasthan Blue City (Dark), Rajasthan Pink City (Light) | India |
| [`themes/sardinia/`](themes/sardinia/) | Sardinia Camisa (Light), Sardinia Orbace (Dark) | Italy |
| [`themes/shaker/`](themes/shaker/) | Shaker Plaster (Light), Shaker Prussian (Dark) | United States |
| [`themes/shuimo/`](themes/shuimo/) | Shuimo Day, Shuimo Night | China |
| [`themes/tamil/`](themes/tamil/) | Tamil Kolam (Dark), Tamil Olai (Light) | India |
| [`themes/wixarika/`](themes/wixarika/) | Wixárika Haramara (Dark), Wixárika Wirikuta (Light) | Mexico |
| [`themes/wuxing/`](themes/wuxing/) | Wuxing Day, Wuxing Night | China |
| [`themes/yolngu/`](themes/yolngu/) | Yolŋu Galawu (Dark), Yolŋu Gapaṉ (Light) | Australia |
| [`themes/zalipie/`](themes/zalipie/) | Zalipie Sadza (Dark), Zalipie Wapno (Light) | Poland |
| [`themes/zlotnica/`](themes/zlotnica/) | Złotnica Aksamit (Dark), Złotnica Płótno (Light) | Poland |

## Install

### JetBrains IDEs

Install **Heritage Themes** from **Settings | Plugins | Marketplace**; it is published on the JetBrains Marketplace. Then choose a theme under **Settings | Appearance & Behavior | Appearance | Theme**.

To install from the [latest GitHub release](https://github.com/heritage-themes/heritage-themes/releases/latest) instead:

- Plugin: `heritage-themes-<version>-signed.zip`. Choose **Settings | Plugins | ⚙ | Install Plugin from Disk…**, select the zip and restart.
- Editor colour scheme only: an `.icls` file. Choose **Settings | Editor | Color Scheme | ⚙ | Import Scheme…** and select the file.

The themes work in IntelliJ-based IDEs version 2025.3 or later, such as IntelliJ IDEA, PyCharm, WebStorm and Android Studio.

Every theme uses the Islands UI: the editor and tool windows sit as rounded islands on the main window. Choosing a Heritage theme always applies it; choose another theme for a different layout. The Classic UI plugin is not tested.

### VS Code

Install **Heritage Themes** from the Extensions view; it is published on the VS Marketplace and Open VSX. Then choose a theme with **Preferences: Color Theme** (`Ctrl+K Ctrl+T`). To install from the latest GitHub release instead, run **Extensions: Install from VSIX…** and select `heritage-themes-vscode-<version>.vsix`.

The extension also works in VS Code forks such as Cursor, Windsurf and VSCodium, which install from Open VSX.

### Visual Studio

Install **Heritage Themes for Visual Studio** from **Extensions | Manage Extensions**; it is published on the VS Marketplace. Restart Visual Studio, then choose a theme under **Tools | Theme**. To install from the latest GitHub release instead, open `heritage-themes-visualstudio-<version>.vsix`, which runs the VSIX Installer, and restart Visual Studio.

Visual Studio 2026 is required. Each theme colours the window, tool windows, tabs, menus, dialogs, status bar and terminal, and the editor in every language that Visual Studio highlights. A Visual Studio theme sets colours only, so keywords and comments keep the regular font.

Visual Studio colours only the roles that its language services and grammars classify, so some languages show fewer of the palette's colours than the same theme in VS Code or an IntelliJ-based IDE:

| Languages | Colours |
| --- | --- |
| C#, C, C++, HTML, CSS, JSON, SQL, Vue, YAML, Markdown | Every role the language has: keywords, types, functions, fields, attributes or tags, strings, numbers and comments. |
| TypeScript, JSX and TSX | Keywords, types, strings, regular expressions, numbers, comments and JSX tags and attributes. Function and property names take the plain text colour. |
| Python | Keywords, types, strings, numbers and comments. Function names take the plain text colour, decorators the type colour. |
| Java, Groovy | Keywords, types, strings, numbers and comments. Fields, constants, annotations and calls take the plain text colour. |
| Go, Rust, shell | Keywords, types, strings, numbers and comments. A function declaration takes the type colour and a call the plain text colour; Rust attributes take the plain text colour. |
| Kotlin, TOML | No colours: Visual Studio has no grammar for them, so they open as plain text. |

A function declaration and a call have separate colours in the palette, and Visual Studio classifies them alike, so both take the call colour in C# and C++.

### Sublime Text

Run **Package Control: Install Package** and choose **Heritage Themes**, then **UI: Select Color Scheme** and **UI: Select Theme**, choosing the same name in both. To install from the latest GitHub release instead, copy `heritage-themes-sublime-<version>.sublime-package` into the `Installed Packages` folder, which **Preferences: Browse Packages** shows beside `Packages`. Each colour scheme colours the editor; the UI theme of the same name extends the built-in Adaptive theme and colours the sidebar, tabs, panels and status bar to match. Sublime Text 4 is required.

### Zed

Install **Heritage Themes** from the Extensions page (**zed: extensions**), then choose a theme with **theme selector: toggle** (`Ctrl+K Ctrl+T`). To install from the latest GitHub release instead, unzip `heritage-themes-zed-<version>.zip`, run **zed: install dev extension** and select the unzipped `heritage-theme` folder. Each theme colours the editor, panels, tabs, title and status bars, terminal and popups.

### Neovim

Install `heritage-themes/heritage-themes.nvim` with a plugin manager, for example with [lazy.nvim](https://github.com/folke/lazy.nvim):

```lua
{ "heritage-themes/heritage-themes.nvim", lazy = false, priority = 1000 }
```

Then choose a theme with `:colorscheme heritage-<theme>`, for example `:colorscheme heritage-holi-night`; press `Tab` after `heritage-` to list them. To install from the latest GitHub release instead, unzip `heritage-themes-nvim-<version>.zip` into `~/.local/share/nvim/site/pack/heritage/start/`. Each colour scheme colours the editor, Tree-sitter and LSP semantic highlights, diagnostics, the status line, tab line, floating windows, the completion menu, diff mode and the terminal; it comes with a lualine theme of the same name and colours the signs of gitsigns.nvim. Neovim 0.10 or later in a terminal with 24-bit colour is required.

### Notepad++

Download `heritage-themes-notepadpp-<version>.zip` from the [latest GitHub release](https://github.com/heritage-themes/heritage-themes/releases/latest) and copy the files in its `themes` folder into `%AppData%\Notepad++\themes` (for a portable Notepad++, the `themes` folder beside `notepad++.exe`). Restart Notepad++ and choose a theme under **Settings | Style Configurator… | Select theme**. Notepad++ keeps one theme for Light Mode and one for Dark Mode: choose a dark theme while **Settings | Preferences… | Dark Mode** is on. Each theme colours every language Notepad++ highlights, the caret, current line, selection, margins, fold markers, highlights, the document map and the bar on the active tab, and in Light Mode the tabs' text. Notepad++ draws its menu bar, toolbar, dialogs and, in Dark Mode, its tabs in its own Dark Mode colours. It has no lexer for Kotlin or Groovy, and colours Markdown with a user-defined language that keeps its own colours.

### Xcode

Download `heritage-themes-xcode-<version>.zip` from the [latest GitHub release](https://github.com/heritage-themes/heritage-themes/releases/latest) and copy the files in its `themes` folder into `~/Library/Developer/Xcode/UserData/FontAndColorThemes`, creating the folder if it does not exist. Restart Xcode and choose a theme under **Xcode | Settings… | Appearance | Theme | Choose…** in Xcode 27 and later, or under **Xcode | Settings… | Themes** in Xcode 26 and earlier. Each theme comes as an `.xcworkspacecolortheme` file for Xcode 27 and an `.xccolortheme` file for earlier releases; do not import the `.xccolortheme` into Xcode 27 with **Import Classic Theme**, which changes its colours. Xcode keeps one theme for the light appearance and one for the dark appearance.

In Xcode 27, each theme colours the editor and the toolbar, jump bar and status bar, which Xcode draws in the editor's background, and tints the rest of the window; fonts are a setting of Xcode 27 that the themes leave as they are. In Xcode 26 and earlier, each theme colours the editor, the console and the rendered documentation, and sets the editor font to SF Mono; Xcode draws the rest of its window in the macOS appearance. Xcode colours Swift with its language service, and Objective-C, C and C++ in a project; it colours the other languages it ships a grammar for with fewer roles, opens Markdown in a rendered editor and HTML beside a live preview, and has no grammar for Kotlin, Groovy, Go, Rust, C# or Vue, which open as plain text.

### Helix

Download `heritage-themes-helix-<version>.zip` from the [latest GitHub release](https://github.com/heritage-themes/heritage-themes/releases/latest) and copy the files in its `themes` folder into `~/.config/helix/themes` (`%AppData%\helix\themes` on Windows), creating the folder if it does not exist. Choose a theme with `theme = "heritage_holi_night"` at the top of `config.toml`, or try one with `:theme heritage_` and `Tab`. The themes need a terminal with 24-bit colour; Helix falls back to its default theme when it does not detect one, which `true-color = true` under `[editor]` overrides. Each theme colours the editor, the gutter, cursors, selections, diagnostics, the status line, buffer line, pickers, popups, the completion menu, inlay hints and jump labels. The cursor takes the colour of the mode, and so does the mode name in the status line with `color-modes = true` under `[editor]`. Helix gives a construct one capture in every language, so function declarations and calls share the call colour, Python decorators take it too, and Rust lifetimes take the label colour.

### Kakoune

Download `heritage-themes-kakoune-<version>.zip` from the [latest GitHub release](https://github.com/heritage-themes/heritage-themes/releases/latest) and copy the files in its `colors` folder into `~/.config/kak/colors`, creating the folder if it does not exist. Choose a scheme with `colorscheme heritage-holi-night` in `kakrc`, or try one with `:colorscheme heritage-` and `Tab`. The schemes need a terminal with 24-bit colour. Each scheme colours the editor, selections, cursors, line numbers, menus, information boxes, diagnostics, the status line and the prompt. Kakoune's language scripts give each construct one of a few faces shared by every language: Java annotations, Rust attributes and C's `#include` share the keyword colour, and Python decorators, HTML attribute names and YAML keys the annotation colour. Kakoune ships no script for C#.

### Micro

Download `heritage-themes-micro-<version>.zip` from the [latest GitHub release](https://github.com/heritage-themes/heritage-themes/releases/latest) and copy the files in its `colorschemes` folder into `~/.config/micro/colorschemes`, creating the folder if it does not exist. Press `Ctrl-e` and choose a scheme with `set colorscheme heritage-holi-night`. Micro draws the schemes in 24-bit colour when the terminal reports it in `COLORTERM`, and in the nearest of 256 colours otherwise; set `truecolor` to `on` for a terminal with 24-bit colour that does not report it. Each scheme colours the editor, selections, line numbers, the cursor line, search matches, the gutter's marks, the status line, the tab bar, split dividers and the completion menu. Micro's syntax files name their groups after Vim's and use them as each language needs, so a group can cover different constructs in different languages.

### Vim

Download `heritage-themes-vim-<version>.zip` from the [latest GitHub release](https://github.com/heritage-themes/heritage-themes/releases/latest) and unzip it into `~/.vim/pack/heritage/start/` (`~/vimfiles/pack/heritage/start/` on Windows). Choose a scheme with `colorscheme heritage-holi-night` in your `vimrc`, after `set termguicolors`, or try one with `:colorscheme heritage-` and `Tab`. The schemes need Vim 9.0 or later; without `termguicolors`, a terminal draws them in the nearest of 256 colours. Each scheme colours the editor, the syntax groups of `:help group-name`, the status line, tab line, tab panel, popup windows, the completion menu, diff mode, spelling, the GUI's menus and tooltips, and the terminal window. Where a syntax file links a construct to a group of another role, the scheme sets the language's group: Java annotations, Python decorators and Rust attributes take the annotation colour, and Rust lifetimes the type parameter colour. For Neovim, use the Neovim plugin.

### GNU Emacs

Download `heritage-themes-emacs-<version>.zip` from the [latest GitHub release](https://github.com/heritage-themes/heritage-themes/releases/latest), copy the files in its `themes` folder into `~/.emacs.d/themes`, and load a theme in your init file:

```elisp
(add-to-list 'custom-theme-load-path (locate-user-emacs-file "themes/"))
(load-theme 'heritage-holi-night t)
```

The themes need Emacs 29.1 or later. Each theme colours Emacs itself (the editor, mode line, header line, tab bar, tab line, minibuffer, search, completion, menus and tooltips) and the packages that ship with Emacs: font-lock and the Tree-sitter modes, compilation, Flymake, Flyspell, Eglot, diff, smerge and Ediff, Dired, Eshell, Org, outlines, Info, whitespace-mode, which-key, xref, Ido, hi-lock, EWW, message composition, Customize and the terminal colours. Emacs 30 opens Kotlin, Groovy, Vue and Markdown as plain text, and colours Go, Rust, TypeScript and YAML once their Tree-sitter grammars are installed with `M-x treesit-install-language-grammar`. The modes without Tree-sitter colour a declared name in one face, so fields, HTML attribute names and local variables take the field colour where they are declared.

### Nano

Download `heritage-themes-nano-<version>.zip` from the [latest GitHub release](https://github.com/heritage-themes/heritage-themes/releases/latest) and add a scheme's lines to `~/.config/nano/nanorc`, after the syntax files, as the zip's README shows; nano reads interface colours only from that file, not from files it includes. The schemes need GNU nano 7.0 or later in a terminal with 256 colours that runs the matching Terminals theme. Each scheme colours nano's title bar, mini bar, status bar, prompts, selection, search matches, line numbers and help lines; code takes the palette's ANSI colours from the terminal theme, in the roles that nano's syntax files give them. A few syntax files, such as those for SQL and YAML, also name nano's own extended colours, which keep their colours in every theme.

### Textadept

Download `heritage-themes-textadept-<version>.zip` from the [latest GitHub release](https://github.com/heritage-themes/heritage-themes/releases/latest), copy the files in its `themes` folder into `~/.textadept/themes`, and choose a theme in `~/.textadept/init.lua` with `view:set_theme('heritage-holi-night')`. The themes need Textadept 12 or later. Each theme colours the editor: code, line numbers, the fold margin, the caret and current line, selections, brace matches, call tips, markers and indicators. Textadept draws its menus, tabs and status bar with Qt or GTK in the system's colours.

### Lapce

Download `heritage-themes-lapce-<version>.zip` from the [latest GitHub release](https://github.com/heritage-themes/heritage-themes/releases/latest), copy the `heritage-themes` folder into Lapce's `plugins` folder (`~/.local/share/lapce-stable/plugins` on Linux), restart Lapce and choose a theme with **Settings | Color Theme**. The themes need Lapce 0.4 or later. Each theme colours the editor, tab bar, panels, activity bar, status bar, palette, completion, hover, inlay hints, source control marks and the terminal. Lapce matches its grammars' captures to a fixed list of scopes, so numbers, booleans and named constants share the number colour, and it draws code without bold or italic.

### Qt Creator

Download `heritage-themes-qtcreator-<version>.zip` from the [latest GitHub release](https://github.com/heritage-themes/heritage-themes/releases/latest), copy its `themes` and `styles` folders into `~/.config/QtProject/qtcreator` (`%AppData%\QtProject\qtcreator` on Windows), choose a theme under **Preferences | Environment | Interface | Theme**, restart Qt Creator, and choose the colour scheme of the same name under **Preferences | Text Editor | Font & Colors**. The themes need Qt Creator 20 or later. Each theme colours the window, panels, output panes, the terminal, version control and the debugger; the colour scheme colours the editor, with C++ and QML from Qt Creator's code models and other languages from KSyntaxHighlighting, which downloads the definitions it lacks, such as C#'s, when asked.

### Amp

Download `heritage-themes-amp-<version>.zip` from the [latest GitHub release](https://github.com/heritage-themes/heritage-themes/releases/latest), copy the files in its `themes` folder into `~/.config/amp/themes`, and name a theme in `~/.config/amp/config.yml` with `theme: heritage-holi-night`. The themes need Amp 0.7 or later. Amp draws text on the terminal's background, so run it in a terminal with 24-bit colour that runs the matching Terminals theme. Each theme colours code, the current line and the status bar, with the rules of the Sublime Text colour schemes; Amp has no syntax for Kotlin, TypeScript, TSX, Vue or TOML.

### Eclipse

Download `heritage-themes-eclipse-<version>.zip` from the [latest GitHub release](https://github.com/heritage-themes/heritage-themes/releases/latest), copy the plugin jar into the `dropins` folder of your Eclipse installation, restart Eclipse, choose a theme under **Window | Preferences | General | Appearance | Theme** and restart again. For the languages that open in the generic editor, such as Python, Go or YAML, choose the TextMate theme of the same name under **Window | Preferences | TextMate | Theme**. The plugin needs Eclipse 2026-09 or later. Each theme colours the window, views, tabs, forms and status line, and the editors: Java with JDT's semantic highlighting, Ant, the console, EGit, compare, Mylyn's tasks and markup editors with their preview, and EclEmma. Eclipse draws scroll bars, buttons and selections in lists and trees with the system's widgets.

### Nova

Download `heritage-themes-nova-<version>.zip` from the [latest GitHub release](https://github.com/heritage-themes/heritage-themes/releases/latest), double-click `Heritage Themes.novaextension` to install it, and choose a theme under **Nova | Settings | Themes**. Each theme colours the window, title bar, buttons, text fields, the editor, code and the terminal.

### JupyterLab

Run `pip install jupyterlab-heritage-themes` in the environment that JupyterLab runs in, restart JupyterLab, reload it in the browser and choose a theme under **Settings | Theme**. The extension needs JupyterLab 4.6 or later, or Notebook 7.6 or later, which installs it the same way. Each theme colours the menu bar, tabs, side panels, dialogs and menus, notebooks with their cells and outputs, including the ANSI colours of tracebacks, and the code of notebooks, consoles and text editors.

### Pygments

Run `pip install heritage-themes-pygments` in the environment that has Pygments. Each theme is then a Pygments style named after it, such as `heritage-holi-night`: pass the name to `pygmentize -O style=`, to `HtmlFormatter(style=...)`, to Sphinx's `pygments_style` or to any other program that takes a Pygments style name. The package needs Pygments 2.14 or later and Python 3.8 or later. A style colours the tokens of Pygments' lexers, the background, the highlighted lines and the line numbers.

### Spyder

Download `heritage-themes-spyder-<version>.zip` from the [latest GitHub release](https://github.com/heritage-themes/heritage-themes/releases/latest), close Spyder, run `python3 install.py` from the unzipped folder, start Spyder and choose a theme under **Preferences | Appearance | Syntax highlighting theme**. The themes need Spyder 6. The installer adds them to the `spyder.ini` of Spyder from your package manager, pip or conda, and of the Flatpak. Each theme colours the editor and the IPython console: code, the current line and cell, the other occurrences of the word under the caret, bracket matches, links and the side areas. Spyder draws its menus, tabs and panes in its own light or dark interface, draws line numbers in a fixed grey, and its **Create new theme** button fails while a Heritage theme is installed.

### Thonny

In Thonny 4.0 or later, choose **Tools | Manage plug-ins**, search for `thonny-heritage-themes`, install it and restart Thonny. Then choose **Tools | Options | Theme & Font**, pick the same theme, such as `Heritage Holi Night`, as **UI theme** and as **Syntax theme**, and restart Thonny again. The UI theme colours the window; the syntax theme colours the editor and the shell, including the debugger's boxes and ANSI colours. Thonny draws its toolbar icons and the assistant's pages itself.

### Terminals

Download `heritage-themes-terminals-<version>.zip` from the [latest GitHub release](https://github.com/heritage-themes/heritage-themes/releases/latest). It has a folder for each app and a README with each app's install steps:

| Kind | Apps |
| --- | --- |
| Terminal emulators | kitty, Alacritty, WezTerm, Ghostty, iTerm2, Windows Terminal, foot, Konsole, Terminator, XTerm, st, Rio, Contour, Warp, Tabby, Hyper, Termux |
| Shells | fish, zsh (with zsh-syntax-highlighting and zsh-autosuggestions), Nushell, PowerShell |
| Prompts | Starship, Oh My Posh, Powerlevel10k |
| Multiplexers | tmux, Zellij |

The terminal emulator themes give the 16 ANSI colours the values of the editors' terminals, with tab bars, cursors, selections and search matches in the palette's colours. The shells, prompts and multiplexers set text colours over the terminal's background, so use them in a terminal with 24-bit colour that runs the same theme. The shells colour the command line in the syntax roles of the editor themes; the prompts recolour Starship's palette, give Oh My Posh a plain prompt and a powerline prompt with filled segments (which needs a Nerd Font), and recolour a Powerlevel10k configuration from `p10k configure`.

## Report an issue

Report a colour, contrast or readability problem, or suggest a new tradition, on the [issue tracker](https://github.com/heritage-themes/heritage-themes/issues). The bug form asks for the theme, editor and version, language and a screenshot; a report with these can be reproduced.

## Licence

[MIT](LICENSE)
