"""Powerlevel10k theme: a file that .zshrc sources after ~/.p10k.zsh, which recolours the configuration that the
p10k configure wizard wrote, whichever style it chose.

The wizard colours each segment with a 256-colour index, in the segment's colour parameters, in prompt strings such as
the frame of a two-line prompt, and in its my_git_formatter function, so the theme maps every index in all three to
the palette by its colour family: reds, yellows and oranges, greens, cyans, blues and magentas to the ANSI colours, and
greys by lightness. Text on a coloured background, as the rainbow style draws segments, takes bg, against which the
build checks the ANSI colours at 4.5:1. Dark grey and black backgrounds, as the classic style draws segments, take the
first of the frame, surface, hover, caret row and tool window colours on which the ANSI and text colours all reach
4.5:1. Values that are not colour indices or names, such as #RRGGBB colours set by hand, stay as they are.
"""
import colorsys, re

from . import colours, header, name, readable_background
from ..vim import xterm_colours

APP = "Powerlevel10k"
FOLDER = "powerlevel10k"
CATEGORY = "Prompts"
INSTALL = """Copy the files in `powerlevel10k` into `~/.config/powerlevel10k` and source a theme in `.zshrc` after \
`~/.p10k.zsh`, which `p10k configure` writes:

```zsh
[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh
source ~/.config/powerlevel10k/{stem}.zsh
```

The theme recolours the prompt that `p10k configure` set up, in the lean, classic or rainbow style: segments, their \
icons, separators, the frame of a two-line prompt and the Git status. The colours are 24-bit, so the terminal needs \
24-bit colour."""
# The 16 user-defined colours by meaning, which terminals redefine and so have no fixed RGB.
SYSTEM = ("black", "red", "green", "yellow", "blue", "magenta", "cyan", "light", "mid", "red", "green", "yellow",
          "blue", "magenta", "cyan", "white")
NAMES = ("black", "red", "green", "yellow", "blue", "magenta", "cyan", "white")
CHROMATIC = ("red", "yellow", "green", "cyan", "blue", "magenta")


def family(index):
    """The colour family of a 256-colour index: a hue, or black, dark, mid, light or white for greys."""
    if index < 16:
        return SYSTEM[index]
    r, g, b = (v / 255 for v in xterm_colours()[index])
    hue, lightness, saturation = colorsys.rgb_to_hls(r, g, b)
    if max(r, g, b) - min(r, g, b) < 0.12:
        return "black" if lightness < 0.12 else "dark" if lightness < 0.35 else "mid" if lightness < 0.7 else "light"
    degrees = hue * 360
    for limit, hue_family in ((20, "red"), (70, "yellow"), (165, "green"), (200, "cyan"), (260, "blue"),
                              (335, "magenta"), (360, "red")):
        if degrees < limit:
            return hue_family


def segment_background(p):
    """The background of the classic style's segments: the first that the ANSI colours, the text and the muted text
    are readable on."""
    return "#" + p[readable_background(p, [p["ansi" + f.title()] for f in CHROMATIC] + [p["fg"], p["muted"]])]


def mapping(p):
    """(foreground, background, text on) for every index: the colour a foreground or background takes, and the
    indices whose backgrounds carry text in bg."""
    c = colours(p)
    hues = {f: "#" + p["ansi" + f.title()] for f in CHROMATIC}
    foreground = {**hues, "black": c["bg"], "dark": c["muted"], "mid": c["muted"], "light": c["fg"],
                  "white": c["fg"]}
    segment = segment_background(p)
    background = {**hues, "black": segment, "dark": segment, "mid": c["muted"], "light": "#" + p["op"],
                  "white": "#" + p["op"]}
    fg, bg, on = {}, {}, set()
    for index in range(256):
        f = family(index)
        fg[index], bg[index] = foreground[f], background[f]
        if f in (*CHROMATIC, "mid", "light", "white"):
            on.add(index)
    return fg, bg, on


def files(theme, source):
    p = theme["palette"]
    fg, bg, on = mapping(p)
    def table(values):
        return " ".join(f"{k} '{v}'" for k, v in values.items())
    lines = [
        *header(p, APP, source),
        "# Source this file in .zshrc after ~/.p10k.zsh.",
        "() {",
        "  emulate -L zsh -o extended_glob",
        f"  local -A fg=({table(fg)})",
        f"  local -A bg=({table(bg)})",
        f"  local -A names=({' '.join(f'{n} {i}' for i, n in enumerate(NAMES))})",
        f"  local -a on=({' '.join(str(i) for i in sorted(on))})",
        "  local -A original",
        "  local parameter value segment",
        "  # a colour index, from a number or one of the eight colour names",
        "  .heritage-index() { [[ $1 == <0-255> ]] && REPLY=$1 || REPLY=${names[$1]-} }",
        "  for parameter in ${(k)parameters[(I)POWERLEVEL9K_(|*_)BACKGROUND]}; do",
        "    .heritage-index ${(P)parameter}",
        "    [[ -n $REPLY ]] || continue",
        "    original[$parameter]=$REPLY",
        "    typeset -g $parameter=${bg[$REPLY]}",
        "    # a coloured segment without a foreground of its own draws its text and icon in the default black",
        "    if (( ${on[(Ie)$REPLY]} )) && [[ $parameter != POWERLEVEL9K_BACKGROUND ]] &&",
        "        (( ! ${+parameters[${parameter%_BACKGROUND}_FOREGROUND]} )); then",
        "      typeset -g ${parameter%_BACKGROUND}_FOREGROUND=0",
        "    fi",
        "  done",
        "  for parameter in ${(k)parameters[(I)POWERLEVEL9K_*_(FOREGROUND|COLOR)]}; do",
        "    .heritage-index ${(P)parameter}",
        "    [[ -n $REPLY ]] || continue",
        "    value=${fg[$REPLY]}",
        "    # the segment's background: the longest prefix of the name with a background, else the default one",
        "    segment=${${parameter%_(FOREGROUND|COLOR)}%_VISUAL_IDENTIFIER}",
        "    while [[ -n $segment && -z ${original[${segment}_BACKGROUND]-} ]]; do",
        "      [[ $segment == *_* ]] && segment=${segment%_*} || segment=",
        "    done",
        "    [[ -n $segment ]] || segment=POWERLEVEL9K",
        "    if (( ${on[(Ie)${original[${segment}_BACKGROUND]-x}]} )); then",
        f"      value='{colours(p)['bg']}'",
        "    fi",
        "    typeset -g $parameter=$value",
        "  done",
        "  # colours in prompt strings and in the Git formatter, as %<n>F, %F{<n>}, %<n>K and %K{<n>}",
        "  .heritage-recolour() {",
        "    REPLY=${1//(#b)%([0-9]##)F/%F{${fg[$match[1]]}}}",
        "    REPLY=${REPLY//(#b)%F[{]([0-9]##)[}]/%F{${fg[$match[1]]}}}",
        "    REPLY=${REPLY//(#b)%([0-9]##)K/%K{${bg[$match[1]]}}}",
        "    REPLY=${REPLY//(#b)%K[{]([0-9]##)[}]/%K{${bg[$match[1]]}}}",
        "  }",
        "  for parameter in ${(k)parameters[(I)POWERLEVEL9K_*]}; do",
        "    [[ ${parameters[$parameter]} == scalar* && ${(P)parameter} == *%* ]] || continue",
        "    .heritage-recolour ${(P)parameter}",
        "    typeset -g $parameter=$REPLY",
        "  done",
        "  if (( ${+functions[my_git_formatter]} )); then",
        "    .heritage-recolour ${functions[my_git_formatter]}",
        "    functions[my_git_formatter]=$REPLY",
        "  fi",
        "  unfunction .heritage-index .heritage-recolour",
        "}",
    ]
    return [(f"{name(theme)}.zsh", "\n".join(lines) + "\n")]


def validate(theme, text):
    p = theme["palette"]
    fg, bg, on = mapping(p)
    for array, values in (("fg", fg), ("bg", bg)):
        match = re.search(rf"^  local -A {array}=\((.*)\)$", text, re.M)
        if not match or dict(re.findall(r"(\d+) '(#[0-9A-F]{6})'", match[1])) != {str(k): v for k, v in values.items()}:
            raise ValueError(f"the {array} table differs from heritage.terminals.powerlevel10k.mapping")
    depth = 0
    for char in re.sub(r"'[^']*'|\"(?:\\.|[^\"\\])*\"", "", text):
        depth += {"{": 1, "}": -1, "(": 1, ")": -1}.get(char, 0)
        if depth < 0:
            break
    if depth:
        raise ValueError("has unbalanced braces or parentheses")


def pairs(p):
    c = colours(p)
    segment = segment_background(p)
    return [*(("text on " + f, c["bg"], "#" + p["ansi" + f.title()], 4.5) for f in CHROMATIC),
            *((f + " on the segment background", "#" + p["ansi" + f.title()], segment, 4.5) for f in CHROMATIC),
            ("text on the segment background", c["fg"], segment, 4.5),
            ("muted text on the segment background", c["muted"], segment, 4.5)]
