// Tokenises code samples with VS Code's TextMate grammars and colour themes, for preview.py --vscode.
//
// Reads {"themes": [VS Code theme JSON], "samples": [{"lang": Shiki language id, "code": text}]} from stdin.
// Writes one entry per theme, holding one entry per sample, holding one array per line of
// [text, "#RRGGBB", font style] tokens; the font style is Shiki's bit set: 1 italic, 2 bold, 4 underline.
import { createHighlighter } from 'shiki';

const chunks = [];
for await (const chunk of process.stdin) chunks.push(chunk);
const { themes, samples } = JSON.parse(Buffer.concat(chunks).toString('utf8'));
const highlighter = await createHighlighter({ themes, langs: [...new Set(samples.map(s => s.lang))] });
const out = themes.map(theme => samples.map(({ lang, code }) =>
  highlighter.codeToTokens(code, { lang, theme: theme.name }).tokens
    .map(line => line.map(t => [t.content, t.color, t.fontStyle]))));
process.stdout.write(JSON.stringify(out));
