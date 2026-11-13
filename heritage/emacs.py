"""GNU Emacs theme generated from a palette.

A theme sets faces: the faces of Emacs itself, the font-lock faces that major modes highlight code with, and the faces
of the packages that ship with Emacs 29 and later that a user meets day to day. The font-lock faces map to the palette
roles that heritage.zed gives the matching Tree-sitter captures: declarations take the method role and calls the call
role, as the Tree-sitter modes of Emacs 29 tell them apart with font-lock-function-name-face and
font-lock-function-call-face. A mode's own face is set where its default gives a construct a role other than the one
the other targets give it, as with Java annotations in c-annotation-face.

A theme's face replaces the face's default spec, so every face whose default carries colours is set and none of
Emacs's own colours shows through; preview.py --emacs fails when one does in a sample.

The faces follow the Islands layout of the other targets: the mode line, header line, tab bar and tab line on the
frame, the editor on bg, and tooltips, menus and code blocks on surface. Emacs draws the colours of a theme in a
terminal without 24-bit colour in the nearest colours it has.
"""
import re

from .nvim import name  # noqa: F401 - Emacs lists a theme by the same name as Neovim
from .vscode import mix

# The face attributes the theme uses, by their keyword in a face spec.
ATTRIBUTES = ("foreground", "background", "weight", "slant", "underline", "strike-through", "box", "extend",
              "inherit", "inverse-video")
FONTS = {"": {}, "bold": {"weight": "bold"}, "italic": {"slant": "italic"},
         "bold italic": {"weight": "bold", "slant": "italic"}}
# Faces drawn as rules, borders, fringe marks or filler rather than text, so the contrast check leaves them out.
DECORATIVE = {"fringe", "line-number", "line-number-current-line", "line-number-major-tick", "line-number-minor-tick",
              "fill-column-indicator", "vertical-border", "window-divider", "window-divider-first-pixel",
              "window-divider-last-pixel", "child-frame-border", "scroll-bar", "org-hide", "diff-indicator-added",
              "diff-indicator-removed", "diff-indicator-changed", "whitespace-space", "whitespace-hspace",
              "whitespace-tab", "whitespace-newline", "bookmark-face", "completions-group-separator", "separator-line",
              # the terminal's colours, whose roles the build checks against bg with the palette
              *(f"ansi-color-{b}{c}" for b in ("", "bright-") for c in ("black", "red", "green", "yellow", "blue",
                                                                        "magenta", "cyan", "white"))}
# Faces held to 3:1 rather than 4.5:1: comments, the cursor, which the build checks as the caret, and the lines that
# take the comment role: Org's keyword, drawer and source block lines and the separator of a message.
LOW_CONTRAST = {"font-lock-comment-face", "cursor", "org-block-begin-line", "org-block-end-line",
                "org-document-info-keyword", "org-meta-line", "org-drawer", "message-separator"}
# Faces without a background of their own that Emacs draws on the background of other faces rather than on default's,
# with the minimum contrast on each: the version control state and the state of a compilation in the mode line.
DRAWN_ON = {face: (("mode-line", 4.5), ("mode-line-inactive", 4.5)) for face in (
    *(f"vc-{state}-state" for state in ("up-to-date", "edited", "locally-added", "conflict", "removed", "missing",
                                         "needs-update", "locked")),
    "compilation-mode-line-exit", "compilation-mode-line-fail", "compilation-mode-line-run")}


def syntax_rules(p):
    """(face, role, font style) per font-lock face and per mode's own code face."""
    kw = "bold" if p.get("kwBold", not p["dark"]) else ""
    rules = []
    def s(faces, role, font=""):
        rules.extend((face, role, font) for face in faces.split())
    s("font-lock-comment-face", "comment", "italic")
    s("font-lock-doc-face", "doc", "italic")
    s("font-lock-doc-markup-face", "docTag", "bold italic")
    s("font-lock-string-face font-lock-regexp-face", "string")
    s("font-lock-escape-face font-lock-regexp-grouping-backslash font-lock-regexp-grouping-construct", "gold", "bold")
    s("font-lock-number-face", "number")
    s("font-lock-keyword-face", "keyword", kw)
    s("font-lock-preprocessor-face", "directive")
    s("font-lock-builtin-face", "call", "italic")
    s("font-lock-constant-face", "constant", "bold italic")
    s("font-lock-type-face", "type")
    s("font-lock-function-name-face", "method", "bold")
    s("font-lock-function-call-face", "call")
    # Variable names are coloured where they are declared, which in the modes without Tree-sitter covers fields, HTML
    # attributes and shell assignments as well as local variables, so they take the field role; uses stay plain.
    s("font-lock-variable-use-face", "fg")
    s("font-lock-variable-name-face font-lock-property-name-face font-lock-property-use-face", "field")
    s("font-lock-operator-face font-lock-punctuation-face font-lock-bracket-face font-lock-delimiter-face "
      "font-lock-misc-punctuation-face font-lock-negation-char-face", "op")
    s("font-lock-warning-face", "ansiYellow", "bold")
    # modes' own faces
    s("c-annotation-face", "annotation")  # Java annotations, which cc-mode draws as constants by default
    s("typescript-ts-jsx-tag-face", "keyword", kw)  # JSX tags, which take the call face by default
    s("typescript-ts-jsx-attribute-face", "field")  # JSX attributes, which take the constant face by default
    s("css-selector", "keyword", kw)
    s("css-property", "field")
    s("css-proprietary-property", "field", "italic")
    s("sh-heredoc", "string")
    s("sh-quoted-exec", "call")
    s("sh-escaped-newline", "gold", "bold")
    return rules


def ui(p):
    """Face to attributes, with #-prefixed colours, for every face that is not a code face."""
    c = {k: "#" + v for k, v in p.items() if isinstance(v, str) and re.fullmatch(r"[0-9A-F]{6}", v)}
    caret = "#" + p.get("caret", p["gold"])
    kw = {"weight": "bold"} if p.get("kwBold", not p["dark"]) else {}
    def wash(key):
        """Halfway from bg to the palette colour."""
        return "#" + mix(p["bg"], p[key], 0.5)
    def deepen(key, towards):
        """The diff background moved towards its gutter colour, for the changed text in a changed line."""
        return "#" + mix(p[key], p[towards], 0.35)
    def f(foreground=None, background=None, **attributes):
        """A face's attributes; font names a style of FONTS."""
        out = {k: v for k, v in dict(foreground=foreground, background=background).items() if v}
        out.update(FONTS[attributes.pop("font", "")])
        out.update({k.replace("_", "-"): v for k, v in attributes.items()})
        return out
    def wave(colour):
        return f(underline={"style": "wave", "color": colour})
    bold, heading = f(weight="bold"), f(c["method"], font="bold")
    faces = {
        # editor
        "default": f(c["fg"], c["bg"]), "cursor": f(background=caret), "mouse": f(background=caret),
        "fringe": f(c["lineNo"], c["bg"]),
        "region": f(background=c["selection"], extend=True),
        "secondary-selection": f(background=c["selInactive"], extend=True),
        "highlight": f(background=c["hover"]), "hl-line": f(background=c["caretRow"], extend=True),
        "shadow": f(c["muted"]), "link": f(c["azure"], underline=True), "link-visited": f(c["field"], underline=True),
        "button": f(inherit="link"),
        "error": f(c["ansiRed"], font="bold"), "warning": f(c["ansiYellow"], font="bold"),
        "success": f(c["ansiGreen"], font="bold"),
        "escape-glyph": f(c["gold"]), "homoglyph": f(c["gold"]), "glyphless-char": f(c["muted"]),
        "nobreak-space": f(c["gold"], underline=True), "nobreak-hyphen": f(c["gold"]),
        "trailing-whitespace": f(background=c["writeCaret"]),
        "line-number": f(c["lineNo"], c["bg"]), "line-number-current-line": f(c["lineNoCaret"], c["bg"]),
        "line-number-major-tick": f(c["lineNoCaret"], c["bg"], font="bold"),
        "line-number-minor-tick": f(c["lineNo"], c["bg"], font="bold"),
        "fill-column-indicator": f(c["guide"]),
        "vertical-border": f(c["border"]), "window-divider": f(c["border"]),
        "window-divider-first-pixel": f(c["border"]), "window-divider-last-pixel": f(c["border"]),
        "child-frame-border": f(background=c["border"]), "scroll-bar": f(c["guideSel"], c["bg"]),
        "bookmark-face": f(c["gold"]),
        "help-key-binding": f(c["ansiBlue"], c["surface"], box={"line-width": -1, "color": c["border"]}),
        "help-argument-name": f(c["param"], font="italic"),
        "minibuffer-prompt": f(c["ansiBlue"], font="bold"),
        # search and matching
        "isearch": f(c["fg"], c["searchBg"], font="bold"), "isearch-group-1": f(c["fg"], c["searchBg"], font="bold"),
        "isearch-group-2": f(background=wash("searchBg")), "isearch-fail": f(c["redText"], c["red"]),
        "lazy-highlight": f(background=wash("searchBg")), "match": f(background=wash("searchBg")),
        "query-replace": f(inherit="isearch"),
        "show-paren-match": f(background=c["braceBg"], font="bold"),
        "show-paren-match-expression": f(background=c["braceBg"]),
        "show-paren-mismatch": f(c["redText"], c["red"]),
        "next-error": f(background=c["selection"], extend=True),
        "next-error-message": f(background=c["caretRow"], extend=True),
        "pulse-highlight-start-face": f(background=c["searchBg"]),
        "pulse-highlight-face": f(background=c["searchBg"], extend=True),
        "blink-matching-paren-offscreen": f(background=c["braceBg"], font="bold"),
        # hi-lock: the highlights that M-s h . and highlight-regexp give, on the palette's highlight backgrounds,
        # and in the ANSI colours for the bold ones
        **{face: f(c["fg"], c[k]) for face, k in (
            ("hi-yellow", "searchBg"), ("hi-pink", "diffDel"), ("hi-green", "diffIns"), ("hi-blue", "diffMod"),
            ("hi-salmon", "writeCaret"), ("hi-aquamarine", "underCaret"))},
        **{face: f(c[k], font="bold") for face, k in (
            ("hi-red-b", "ansiRed"), ("hi-green-b", "ansiGreen"), ("hi-blue-b", "ansiBlue"))},
        # frame: mode line, header line, tab bar and tab line. The current tab joins the editor, as in the Zed theme.
        "mode-line": f(c["fg"], c["frame"]), "mode-line-active": f(inherit="mode-line"),
        "mode-line-inactive": f(c["muted"], c["frame"]), "mode-line-highlight": f(background=c["hover"]),
        "mode-line-buffer-id": bold, "mode-line-emphasis": bold,
        "header-line": f(c["fg"], c["frame"]), "header-line-highlight": f(background=c["hover"]),
        "tab-bar": f(c["muted"], c["frame"]), "tab-bar-tab": f(c["fg"], c["bg"], font="bold"),
        "tab-bar-tab-inactive": f(c["muted"], c["frame"]),
        "tab-bar-tab-group-current": f(c["fg"], c["frame"], font="bold"),
        "tab-bar-tab-group-inactive": f(c["muted"], c["frame"]),
        "tab-bar-tab-ungrouped": f(c["muted"], c["frame"]),
        "tab-line": f(c["muted"], c["frame"]), "tab-line-tab": f(c["fg"], c["bg"]),
        "tab-line-tab-current": f(c["fg"], c["bg"], font="bold"), "tab-line-tab-inactive": f(c["muted"], c["frame"]),
        "tab-line-tab-inactive-alternate": f(c["muted"], c["frame"]), "tab-line-highlight": f(background=c["hover"]),
        "tab-line-tab-special": f(font="italic"), "tab-line-tab-modified": f(font="italic"),
        "tab-line-tab-group": f(c["muted"], c["frame"], font="bold"), "tab-line-close-highlight": f(c["fg"], c["hover"]),
        "vc-up-to-date-state": f(c["fg"]), "vc-edited-state": f(c["fg"], font="bold"),
        "vc-locally-added-state": f(c["fg"], font="bold"), "vc-conflict-state": f(c["fg"], font="bold"),
        "vc-removed-state": f(c["fg"], font="bold"), "vc-missing-state": f(c["fg"], font="bold"),
        "vc-needs-update-state": f(c["fg"], font="bold"), "vc-locked-state": f(c["fg"], font="bold"),
        # popups: tooltips, menus and completion. Matches take ansiBlue, as VS Code's lists do.
        "tooltip": f(c["fg"], c["surface"]), "menu": f(c["fg"], c["surface"]),
        "tty-menu-enabled-face": f(c["fg"], c["surface"]), "tty-menu-disabled-face": f(c["muted"], c["surface"]),
        "tty-menu-selected-face": f(c["fg"], c["selection"]),
        "completions-common-part": f(c["ansiBlue"], font="bold"), "completions-first-difference": bold,
        "completions-annotations": f(c["muted"], font="italic"),
        "completions-highlight": f(background=c["selection"], extend=True),
        "completions-group-title": f(c["muted"], font="italic"),
        "completions-group-separator": f(c["muted"], strike_through=True),
        "completion-preview-common": f(c["muted"], underline=True),
        "icomplete-first-match": f(c["ansiBlue"], font="bold"),
        "icomplete-selected-match": f(background=c["selection"]),
        "ido-first-match": f(c["ansiBlue"], font="bold"), "ido-only-match": f(c["ansiGreen"], font="bold"),
        "ido-subdir": f(c["ansiBlue"]), "ido-virtual": f(c["muted"]), "ido-indicator": f(c["redText"], c["red"]),
        "ido-incomplete-regexp": f(c["ansiYellow"]),
        "which-key-key-face": f(c["ansiBlue"], font="bold"), "which-key-separator-face": f(c["muted"]),
        "which-key-note-face": f(c["muted"]), "which-key-command-description-face": f(c["fg"]),
        "which-key-local-map-description-face": f(c["fg"]), "which-key-group-description-face": f(c["keyword"], **kw),
        "which-key-special-key-face": f(c["ansiBlue"], font="bold"),
        "which-key-highlighted-command-face": f(c["fg"], underline=True),
        "which-key-docstring-face": f(c["doc"], font="italic"),
        "xref-file-header": f(c["ansiBlue"], font="bold"), "xref-line-number": f(c["muted"]),
        "xref-match": f(background=wash("searchBg")),
        # diagnostics. Messages take the ANSI colours, which the build checks at 4.5:1 against bg; undercurls take the
        # diagnostic colours of the other targets.
        "flymake-error": wave(c["error"]), "flymake-warning": wave(c["warning"]), "flymake-note": wave(c["azure"]),
        "flymake-error-echo": f(c["ansiRed"]), "flymake-warning-echo": f(c["ansiYellow"]),
        "flymake-note-echo": f(c["ansiBlue"]),
        "flymake-error-echo-at-eol": f(c["ansiRed"], font="italic"),
        "flymake-warning-echo-at-eol": f(c["ansiYellow"], font="italic"),
        "flymake-note-echo-at-eol": f(c["ansiBlue"], font="italic"),
        "flyspell-incorrect": wave(c["error"]), "flyspell-duplicate": wave(c["warning"]),
        "compilation-error": f(c["ansiRed"], font="bold"), "compilation-warning": f(c["ansiYellow"], font="bold"),
        "compilation-info": f(c["ansiGreen"], font="bold"), "compilation-line-number": f(c["muted"]),
        "compilation-column-number": f(c["muted"]),
        "compilation-mode-line-exit": f(c["fg"], font="bold"), "compilation-mode-line-fail": f(c["fg"], font="bold"),
        "compilation-mode-line-run": f(c["fg"], font="bold"),
        "eglot-highlight-symbol-face": f(background=c["underCaret"]),
        "eglot-inlay-hint-face": f(c["muted"], c["caretRow"]),
        "eglot-diagnostic-tag-unnecessary-face": f(c["muted"], font="italic"),
        "eglot-diagnostic-tag-deprecated-face": f(strike_through=True),
        # diff, merge and ediff: backgrounds in the diff colours of the other targets, changed text deeper
        "diff-header": f(c["fg"], c["surface"]), "diff-file-header": f(c["fg"], c["surface"], font="bold"),
        "diff-index": f(c["fg"], c["surface"], font="bold"), "diff-hunk-header": f(c["muted"], c["caretRow"]),
        "diff-function": f(c["muted"], c["caretRow"]), "diff-context": f(c["fg"]),
        "diff-added": f(background=c["diffIns"], extend=True), "diff-removed": f(background=c["diffDel"], extend=True),
        "diff-changed": f(background=c["diffMod"], extend=True),
        "diff-changed-unspecified": f(background=c["diffMod"], extend=True),
        "diff-refine-added": f(background=deepen("diffIns", "added")),
        "diff-refine-removed": f(background=deepen("diffDel", "deleted")),
        "diff-refine-changed": f(background=deepen("diffMod", "modified")),
        "diff-indicator-added": f(c["added"]), "diff-indicator-removed": f(c["deleted"]),
        "diff-indicator-changed": f(c["modified"]),
        "diff-nonexistent": f(c["fg"], c["diffDel"], font="bold"), "diff-error": f(c["redText"], c["red"]),
        "smerge-upper": f(background=c["diffDel"], extend=True), "smerge-lower": f(background=c["diffIns"], extend=True),
        "smerge-base": f(background=c["diffMod"], extend=True), "smerge-markers": f(c["muted"], c["surface"]),
        "smerge-refined-added": f(background=deepen("diffIns", "added")),
        "smerge-refined-removed": f(background=deepen("diffDel", "deleted")),
        **{f"ediff-current-diff-{s}": f(background=c[k], extend=True)
           for s, k in (("A", "diffDel"), ("B", "diffIns"), ("C", "diffMod"), ("Ancestor", "diffConf"))},
        **{f"ediff-fine-diff-{s}": f(background=deepen(k, t))
           for s, k, t in (("A", "diffDel", "deleted"), ("B", "diffIns", "added"), ("C", "diffMod", "modified"),
                           ("Ancestor", "diffConf", "gold"))},
        **{f"ediff-even-diff-{s}": f(background=c["surface"]) for s in ("A", "B", "C", "Ancestor")},
        **{f"ediff-odd-diff-{s}": f(background=c["caretRow"]) for s in ("A", "B", "C", "Ancestor")},
        # files: dired and eshell, in the colours that Neovim gives directories and the terminal's ANSI colours
        "dired-header": heading, "dired-directory": f(c["ansiBlue"], font="bold"), "dired-symlink": f(c["ansiCyan"]),
        "dired-broken-symlink": f(c["redText"], c["red"]), "dired-mark": f(c["gold"], font="bold"),
        "dired-marked": f(c["gold"], font="bold"), "dired-flagged": f(c["ansiRed"], font="bold"),
        "dired-perm-write": f(c["muted"]), "dired-set-id": f(c["ansiRed"]), "dired-special": f(c["ansiMagenta"]),
        "dired-ignored": f(c["muted"]), "dired-warning": f(c["ansiYellow"], font="bold"),
        "eshell-prompt": f(c["ansiBlue"], font="bold"), "eshell-ls-directory": f(c["ansiBlue"], font="bold"),
        "eshell-ls-symlink": f(c["ansiCyan"]), "eshell-ls-executable": f(c["ansiGreen"]),
        "eshell-ls-missing": f(c["ansiRed"]), "eshell-ls-archive": f(c["ansiMagenta"]),
        "eshell-ls-special": f(c["ansiMagenta"]), "eshell-ls-backup": f(c["muted"]), "eshell-ls-clutter": f(c["muted"]),
        "eshell-ls-product": f(c["muted"]), "eshell-ls-readonly": f(c["muted"]), "eshell-ls-unreadable": f(c["muted"]),
        # documents: outlines, Org and Info. Headings take the declaration role, as Markdown headings do.
        **{f"outline-{level}": heading for level in range(1, 9)},
        "org-document-title": heading, "org-document-info": f(c["doc"]), "org-document-info-keyword": f(c["comment"]),
        "org-meta-line": f(c["comment"]), "org-drawer": f(c["comment"]), "org-special-keyword": f(c["keyword"], **kw),
        "org-property-value": f(c["fg"]),
        "org-block": f(background=c["surface"], extend=True),
        "org-block-begin-line": f(c["comment"], c["surface"], font="italic", extend=True),
        "org-block-end-line": f(c["comment"], c["surface"], font="italic", extend=True),
        "org-code": f(c["string"]), "org-verbatim": f(c["string"]),
        "org-quote": f(c["doc"], font="italic"), "org-verse": f(c["doc"], font="italic"),
        "org-link": f(inherit="link"), "org-footnote": f(c["azure"]), "org-target": f(underline=True),
        "org-date": f(c["call"], underline=True), "org-sexp-date": f(c["call"]), "org-macro": f(c["annotation"]),
        "org-todo": f(c["todo"], font="bold"), "org-done": f(c["ansiGreen"], font="bold"),
        "org-headline-done": f(c["muted"]), "org-priority": f(c["gold"]), "org-tag": f(c["muted"]),
        "org-table": f(c["fg"]), "org-formula": f(c["number"]), "org-checkbox": f(c["op"], font="bold"),
        "org-list-dt": bold, "org-ellipsis": f(c["muted"]), "org-hide": f(c["bg"]),
        "org-warning": f(c["ansiRed"], font="bold"), "org-headline-todo": f(c["fg"]),
        "org-table-header": f(c["fg"], c["surface"], font="bold"), "org-column": f(background=c["surface"]),
        "org-column-title": f(c["fg"], c["surface"], font="bold"), "org-date-selected": f(c["fg"], c["selection"]),
        "org-latex-and-related": f(c["annotation"]), "org-clock-overlay": f(c["fg"], c["surface"]),
        "org-mode-line-clock-overrun": f(c["redText"], c["red"]), "org-dispatcher-highlight": f(c["gold"], font="bold"),
        "org-agenda-structure": heading, "org-agenda-date": f(c["ansiBlue"]),
        "org-agenda-date-today": f(c["ansiBlue"], font="bold"), "org-agenda-date-weekend": f(c["ansiBlue"], font="italic"),
        "org-agenda-done": f(c["muted"]), "org-time-grid": f(c["muted"]),
        "org-agenda-dimmed-todo-face": f(c["muted"]), "org-agenda-restriction-lock": f(c["fg"], c["surface"]),
        "org-scheduled": f(c["ansiGreen"]), "org-scheduled-today": f(c["ansiGreen"], font="bold"),
        "org-scheduled-previously": f(c["ansiYellow"]), "org-upcoming-deadline": f(c["ansiYellow"]),
        **{f"info-title-{level}": heading for level in range(1, 5)},
        "info-menu-header": bold, "info-node": f(c["method"], font="bold italic"), "info-menu-star": f(c["gold"]),
        "info-xref": f(inherit="link"), "info-xref-visited": f(inherit="link-visited"),
        "info-header-xref": f(inherit="link"), "info-header-node": f(c["fg"], font="bold"),
        "Info-quoted": f(c["string"]),
        # whitespace-mode: marks in the indent guide colour, problems on the write highlight
        **{face: f(c["guide"]) for face in ("whitespace-space", "whitespace-hspace", "whitespace-tab",
                                             "whitespace-newline")},
        **{face: f(background=c["writeCaret"]) for face in (
            "whitespace-trailing", "whitespace-line", "whitespace-empty", "whitespace-indentation",
            "whitespace-big-indent", "whitespace-space-after-tab", "whitespace-space-before-tab",
            "whitespace-missing-newline-at-eof")},
        # Customize and its widgets
        "custom-group-tag": heading, "custom-variable-tag": f(c["method"], font="bold"), "custom-face-tag": bold,
        "custom-state": f(c["ansiGreen"]), "custom-documentation": f(c["doc"]),
        "custom-comment": f(c["fg"], c["surface"]), "custom-comment-tag": f(c["muted"]),
        "custom-link": f(inherit="link"), "custom-invalid": f(c["redText"], c["red"]),
        "custom-rogue": f(c["ansiRed"]), "custom-variable-obsolete": f(c["muted"]),
        "custom-modified": f(c["fg"], c["diffMod"]), "custom-set": f(c["fg"], c["diffIns"]),
        "custom-changed": f(c["fg"], c["diffMod"]), "custom-themed": f(c["fg"], c["diffConf"]),
        "custom-button": f(c["fg"], c["surface"], box={"line-width": 1, "color": c["border"]}),
        "custom-button-mouse": f(c["fg"], c["hover"], box={"line-width": 1, "color": c["border"]}),
        "custom-button-pressed": f(c["fg"], c["selection"], box={"line-width": 1, "color": c["border"]}),
        "custom-button-unraised": f(c["fg"], underline=True),
        "widget-field": f(c["fg"], c["surface"], extend=True), "widget-single-line-field": f(c["fg"], c["surface"]),
        "custom-button-pressed-unraised": f(c["field"], underline=True), "custom-group-tag-1": heading,
        "widget-button": bold, "widget-button-pressed": f(c["ansiRed"]), "widget-documentation": f(c["doc"]),
        "widget-inactive": f(c["muted"]),
        "icon-button": f(c["fg"], c["surface"], box={"line-width": 1, "color": c["border"]}),
        "separator-line": f(background=c["border"]), "tool-bar": f(c["fg"], c["frame"]),
        # EWW and shr: web pages and HTML mail
        **{f"eww-form-{kind}": f(c["fg"], c["surface"], box={"line-width": 1, "color": c["border"]})
           for kind in ("checkbox", "file", "select", "submit", "text", "textarea")},
        "eww-valid-certificate": f(c["ansiGreen"], font="bold"), "eww-invalid-certificate": f(c["ansiRed"], font="bold"),
        "shr-mark": f(c["fg"], c["searchBg"]), "shr-selected-link": f(c["fg"], c["selection"], underline=True),
        # mail composition: header names take the field role, the subject the declaration role, quoted text the doc
        # role
        "message-header-name": f(c["field"]), "message-header-subject": f(c["method"], font="bold"),
        "message-header-to": f(c["fg"], font="bold"), "message-header-cc": f(c["fg"]),
        "message-header-newsgroups": f(c["fg"], font="bold"), "message-header-other": f(c["string"]),
        "message-header-xheader": f(c["muted"]), "message-separator": f(c["comment"]),
        "message-mml": f(c["annotation"]), "mm-command-output": f(c["ansiGreen"]),
        **{f"message-cited-text-{level}": f(c["doc"], font="italic") for level in range(1, 5)},
        # calendar, debugging and tests
        "diary": f(c["ansiYellow"]), "holiday": f(c["fg"], c["diffConf"]),
        "edebug-disabled-breakpoint": f(c["muted"], c["diffDel"]),
        "elisp-shorthand-font-lock-face": f(c["annotation"], font="italic"),
        "ert-test-result-expected": f(c["fg"], c["diffIns"]), "ert-test-result-unexpected": f(c["fg"], c["diffDel"]),
    }
    # the terminal's 16 colours, as the Neovim scheme gives them; Emacs draws ANSI output, in shell and compilation
    # buffers among others, with these faces
    colours = ("black", "red", "green", "yellow", "blue", "magenta", "cyan", "white")
    terminal = ["#" + v for v in [p["disabled"], *(p["ansi" + n] for n in ("Red", "Green", "Yellow", "Blue",
                                                                          "Magenta", "Cyan")), p["op"]]]
    bright = ["#" + p["muted"], *terminal[1:7], "#" + p["fg"]]
    for colour, normal, light in zip(colours, terminal, bright):
        faces[f"ansi-color-{colour}"] = f(normal, normal)
        faces[f"ansi-color-bright-{colour}"] = f(light, light)
    return faces


def faces(p):
    """Every face of the theme: the faces of ui first, then code faces."""
    out = ui(p)
    for face, role, font in syntax_rules(p):
        if face in out:
            raise ValueError(f"{face} is set twice")
        out[face] = dict(foreground="#" + p[role], **FONTS[font])
    return out


def lisp(value):
    """An Emacs Lisp literal for a face attribute's value: a string, t, a symbol, a number or a plist."""
    if value is True:
        return "t"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, dict):
        return "(" + " ".join(f":{k} {lisp(v)}" for k, v in value.items()) + ")"
    if re.fullmatch(r"[a-z-]+", value):
        return value  # a symbol, such as bold or wave, or a face to inherit
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def theme(p, theme_name, source, url):
    """The <theme_name>-theme.el file for a palette. source is the URL of the theme folder, url the project's."""
    file = f"{theme_name}-theme.el"
    specs = "\n".join(f" '({face} ((t {lisp(attributes)})))" for face, attributes in faces(p).items())
    return f""";;; {file} --- {p['name']}, a Heritage Themes theme  -*- lexical-binding: t; -*-

;; URL: {url}
;; Package-Requires: ((emacs "29.1"))

;;; Commentary:

;; {p['name']}: a Heritage Themes theme for GNU Emacs.
;; Generated from {source}; changes here are overwritten.

;;; Code:

(deftheme {theme_name}
  "{p['name']}: a Heritage Themes theme."
  :background-mode '{'dark' if p['dark'] else 'light'}
  :kind 'color-scheme
  :family 'heritage)

(custom-theme-set-faces
 '{theme_name}
{specs})

(provide-theme '{theme_name})

;;; {file} ends here
"""
