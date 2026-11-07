"""Oh My Posh theme: two configurations with the theme's palette and a prompt that uses it. The palette names the ANSI
colours and the theme's text, muted, background and surface colours, so a configuration of the user's own can take
them by copying the palette and naming the colours as p:<name>. The prompt shows the folder, the Git branch and status,
the duration of a slow command and the exit status of a failed one, then the prompt character on a line of its own.
The plain configuration colours the text of each segment; the powerline one fills each segment with an ANSI colour,
in the theme's background colour for text, and joins the segments with arrows."""
import json, re

from . import ANSI_NAMES, colours, name, standard_pairs

APP = "Oh My Posh"
FOLDER = "oh-my-posh"
CATEGORY = "Prompts"
INSTALL = """Copy the files in `oh-my-posh` into `~/.config/oh-my-posh` and start Oh My Posh with a theme in your \
shell's profile, for example in `.bashrc`. Each theme comes in two prompts. The plain prompt colours the text:

```bash
eval "$(oh-my-posh init bash --config ~/.config/oh-my-posh/{stem}.omp.json)"
```

The powerline prompt fills each segment with a colour and joins the segments with arrows, which needs a \
[Nerd Font](https://www.nerdfonts.com) in the terminal:

```bash
eval "$(oh-my-posh init bash --config ~/.config/oh-my-posh/{stem}-powerline.omp.json)"
```

Both show the folder, the Git branch and status, the duration of a slow command and the exit status of a failed one, \
with the prompt character on a line of its own. To give a configuration of your own the theme's colours, copy the \
theme's `palette` into it and name the colours as `p:blue`, `p:text` and so on."""
SCHEMA = "https://raw.githubusercontent.com/JanDeDobbeleer/oh-my-posh/main/themes/schema.json"
ARROW = "\ue0b0"
# The text on the powerline segments' coloured backgrounds: the build checks the ANSI colours at 4.5:1 on it.
BACKGROUND_TEXT = "background"
# The ANSI colours that fill the powerline segments, the git segment's yellow when the repository is dirty.
FILLS = ("blue", "green", "yellow", "magenta", "red")
STYLES = (("plain", ""), ("powerline", "-powerline"))


def palette(p):
    c = colours(p)
    out = dict(zip(ANSI_NAMES, c["ansi"][:8]))
    out.update({f"bright-{n}": colour for n, colour in zip(ANSI_NAMES, c["ansi"][8:])})
    out.update({"text": c["fg"], "muted": c["muted"], "background": c["bg"], "surface": c["surface"]})
    return out


def segment(kind, colour, template, **properties):
    out = {"type": kind, "style": "plain", "foreground": f"p:{colour}", "template": template}
    if properties:
        out["properties"] = properties
    return out


def powerline(kind, colour, template, **properties):
    """A segment filled with an ANSI colour, with text in the theme's background colour and an arrow after it."""
    out = {"type": kind, "style": "powerline", "powerline_symbol": ARROW, "foreground": f"p:{BACKGROUND_TEXT}",
           "background": f"p:{colour}", "template": template}
    if properties:
        out["properties"] = properties
    return out


def prompt(segments):
    """The first line of the prompt, and below it the prompt character, red after a failed command."""
    return [
        {"type": "prompt", "alignment": "left", "segments": segments},
        {"type": "prompt", "alignment": "left", "newline": True, "segments": [
            {**segment("text", "green", "❯"), "foreground_templates": ["{{ if gt .Code 0 }}p:red{{ end }}"]},
        ]},
    ]


def config(p, source, style="plain"):
    """The configuration of a style, plain or powerline."""
    if style == "powerline":
        # Neighbouring segments differ in colour, as the git segment turns yellow in a dirty repository and the arrows
        # between them would vanish otherwise.
        segments = [
            powerline("path", "blue", " {{ .Path }} ", style="full"),
            {**powerline("git", "green", " {{ .HEAD }}{{ if .Working.Changed }} *{{ end }} ", fetch_status=True),
             "background_templates": ["{{ if or (.Working.Changed) (.Staging.Changed) }}p:yellow{{ end }}"]},
            powerline("executiontime", "magenta", " {{ .FormattedMs }} ", threshold=2000, style="austin"),
            powerline("status", "red", " ✘ {{ .Code }} "),
        ]
    else:
        segments = [
            segment("path", "blue", "{{ .Path }} ", style="full"),
            {**segment("git", "magenta", "{{ .HEAD }}{{ if .Working.Changed }} *{{ end }} ", fetch_status=True),
             "foreground_templates": ["{{ if or (.Working.Changed) (.Staging.Changed) }}p:yellow{{ end }}"]},
            segment("executiontime", "yellow", "{{ .FormattedMs }} ", threshold=2000, style="austin"),
            segment("status", "red", "{{ if gt .Code 0 }}✘ {{ .Code }}{{ end }} "),
        ]
    return {
        "$schema": SCHEMA,
        "version": 3,
        "final_space": True,
        "palette": palette(p),
        "blocks": prompt(segments),
        "transient_prompt": {"foreground": "p:green", "foreground_templates": ["{{ if gt .Code 0 }}p:red{{ end }}"],
                             "template": "❯ "},
    }


def files(theme, source):
    p = theme["palette"]
    out = []
    for style, suffix in STYLES:
        data = {"$schema": SCHEMA, "$comment": f"{p['name']}: a Heritage Themes theme for {APP}. Generated from "
                                               f"{source}; changes here are overwritten.",
                **{k: v for k, v in config(p, source, style).items() if k != "$schema"}}
        out.append((f"{name(theme)}{suffix}.omp.json", json.dumps(data, indent=2, ensure_ascii=False) + "\n"))
    return out


def validate_files(theme, files):
    """files: file name → text, for the theme's files."""
    for style, suffix in STYLES:
        filename = f"{name(theme)}{suffix}.omp.json"
        text = files[filename]
        try:
            data = json.loads(text)
            if {k: v for k, v in data.items() if k != "$comment"} != config(theme["palette"], "", style):
                raise ValueError("differs from heritage.terminals.oh_my_posh.config")
            colours_ = set(re.findall(r"p:([\w-]+)", text))
            if not colours_ <= set(data["palette"]):
                raise ValueError(f"names colours the palette lacks: {sorted(colours_ - set(data['palette']))}")
        except ValueError as error:
            raise ValueError(f"{filename}: {error}")


def pairs(p):
    colour_of = palette(p)
    fills = [(f"powerline text on {colour}", colour_of[BACKGROUND_TEXT], colour_of[colour], 4.5) for colour in FILLS]
    return [pair for pair in standard_pairs(p) if pair[0] == "text" or pair[0].startswith("colour")] + fills
