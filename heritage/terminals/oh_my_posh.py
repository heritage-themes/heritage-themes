"""Oh My Posh theme: a configuration with the theme's palette and a prompt that uses it. The palette names the ANSI
colours and the theme's text, muted, background and surface colours, so a configuration of the user's own can take
them by copying the palette and naming the colours as p:<name>. The prompt shows the folder, the Git branch and status,
the duration of a slow command and the exit status of a failed one, then the prompt character on a line of its own."""
import json, re

from . import ANSI_NAMES, colours, name, standard_pairs

APP = "Oh My Posh"
FOLDER = "oh-my-posh"
CATEGORY = "Prompts"
INSTALL = """Copy the files in `oh-my-posh` into `~/.config/oh-my-posh` and start Oh My Posh with a theme in your \
shell's profile, for example in `.bashrc`:

```bash
eval "$(oh-my-posh init bash --config ~/.config/oh-my-posh/{stem}.omp.json)"
```

Each theme is a prompt with the folder, the Git branch and status, the duration of a slow command and the exit status \
of a failed one, with the prompt character on a line of its own. To give a configuration of your own the theme's \
colours, copy the theme's `palette` into it and name the colours as `p:blue`, `p:text` and so on."""
SCHEMA = "https://raw.githubusercontent.com/JanDeDobbeleer/oh-my-posh/main/themes/schema.json"


def palette(p):
    c = colours(p)
    out = dict(zip(ANSI_NAMES, c["ansi"][:8]))
    out.update({f"bright-{n}": colour for n, colour in zip(ANSI_NAMES, c["ansi"][8:])})
    out.update({"text": c["fg"], "muted": c["muted"], "background": c["bg"], "surface": c["surface"]})
    return out


def config(p, source):
    def segment(kind, colour, template, **properties):
        out = {"type": kind, "style": "plain", "foreground": f"p:{colour}", "template": template}
        if properties:
            out["properties"] = properties
        return out
    return {
        "$schema": SCHEMA,
        "version": 3,
        "final_space": True,
        "palette": palette(p),
        "blocks": [
            {"type": "prompt", "alignment": "left", "segments": [
                segment("path", "blue", "{{ .Path }} ", style="full"),
                {**segment("git", "magenta", "{{ .HEAD }}{{ if .Working.Changed }} *{{ end }} ",
                           fetch_status=True),
                 "foreground_templates": ["{{ if or (.Working.Changed) (.Staging.Changed) }}p:yellow{{ end }}"]},
                segment("executiontime", "yellow", "{{ .FormattedMs }} ", threshold=2000, style="austin"),
                segment("status", "red", "{{ if gt .Code 0 }}✘ {{ .Code }}{{ end }} "),
            ]},
            {"type": "prompt", "alignment": "left", "newline": True, "segments": [
                {**segment("text", "green", "❯"),
                 "foreground_templates": ["{{ if gt .Code 0 }}p:red{{ end }}"]},
            ]},
        ],
        "transient_prompt": {"foreground": "p:green", "foreground_templates": ["{{ if gt .Code 0 }}p:red{{ end }}"],
                             "template": "❯ "},
    }


def files(theme, source):
    p = theme["palette"]
    data = {"$schema": SCHEMA, "$comment": f"{p['name']}: a Heritage Themes theme for {APP}. Generated from {source}; "
                                           "changes here are overwritten.",
            **{k: v for k, v in config(p, source).items() if k != "$schema"}}
    return [(f"{name(theme)}.omp.json", json.dumps(data, indent=2, ensure_ascii=False) + "\n")]


def validate(theme, text):
    data = json.loads(text)
    if {k: v for k, v in data.items() if k != "$comment"} != config(theme["palette"], ""):
        raise ValueError("differs from heritage.terminals.oh_my_posh.config")
    colours_ = set(re.findall(r"p:([\w-]+)", text))
    if not colours_ <= set(data["palette"]):
        raise ValueError(f"names colours the palette lacks: {sorted(colours_ - set(data['palette']))}")


def pairs(p):
    return [pair for pair in standard_pairs(p) if pair[0] == "text" or pair[0].startswith("colour")]
