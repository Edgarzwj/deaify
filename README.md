# deaify

Strip the AI smell off your code and writing, before you ship it and after.

`deaify` is three Agent Skills that fix the tells in LLM-generated **code and prose**. Most humanizer projects handle text only. Ponytail and Karpathy tell the model how not to write bloat. Nobody else takes code that *already* smells of AI and rewrites it to read like a person wrote it. That rewrite step is what `deaify` adds.

## The three skills

- **`code-no-slop`** — prevention for code. A superset of Ponytail's lazy ladder and Karpathy's four rules, plus the LLM-smells taxonomy. It tells the agent to write the smallest thing that works. Ships with Karpathy's real before/after examples (over-abstraction, drive-by refactors, test-first) and a pre-delivery self-audit.
- **`code-humanizer`** — remediation for code. It reads AI-smelling code and rewrites it, checking against 22 smells (15 general + 7 algorithm/systems specific), with before/after examples in JS/TS, Python, and Go. Before delivery it checks the smell density actually dropped.
- **`humanize-prose`** — the writing twin. Prevention and remediation for prose, 30+ tells (EN + Chinese AI-isms), including a technical/algorithm-writing track.

## Why the code-rewrite half matters

The interesting part is `code-humanizer`. Prevention tools (Ponytail, Karpathy) stop the model from *writing* bloat. They can't fix the 800-line file that already shipped. `deaify` does. And it's built for algorithm code first: reinvented stdlib calls (`pow`, `gcd`, `bisect`), unnamed magic constants (`1e9+7`, `eps`), line-by-line narration comments, one algorithm wrapped in a class, defensive `deepcopy`, `except: return -1`. A skill that doesn't help algorithm code isn't worth shipping. That's the bar.

`code-humanizer` also refuses to hand you rewritten code it hasn't verified. It runs the before/after and checks the output is identical (`tests/run_examples.py` does this on the bundled examples). Most skills skip that step.

## Install

Works anywhere an Agent Skills runtime scans a `skills/` directory: WorkBuddy, Claude Code, OpenCode, Cursor, Cline.

```bash
git clone https://github.com/Edgarzwj/deaify.git
cp -r deaify/skills/* ~/.workbuddy/skills/   # WorkBuddy, global
cp -r deaify/skills/* ~/.claude/skills/      # Claude Code, global
```

`code-no-slop` already contains Ponytail and Karpathy. Don't install those separately, or you inject the same guidance twice.

## Multi-agent adapters

Some tools read project rule files instead of a `skills/` directory. This repo ships adapters generated from the same source, so the rules work there too:

| File | Read by |
|------|---------|
| `AGENTS.md` | Claude Code, Codex, Gemini, OpenCode, Devin |
| `.cursor/rules/deaify.mdc` | Cursor |
| `.qoder/rules/deaify.md` | Qoder |
| `.windsurf/rules/deaify.md` | Windsurf |
| `.claude/CLAUDE.md` | Claude Code (project) |

You don't need to install any of those apps to ship these files. They're plain text the tool reads when it opens your project. The adapters are copies of the skill files, so regenerate them after editing a skill.

## Usage

- Prevention: keep `code-no-slop` on, or tell the agent "be lazy / simplest solution / yagni".
- Remediation: paste AI-generated code and say "humanize this / remove the AI smell". You get rewritten code plus a list mapping each edit to a smell number.

## Examples

- [`examples/algorithm.py`](examples/algorithm.py) — before/after produce identical output.
- [`examples/web.ts`](examples/web.ts) — TypeScript/JS before/after.
- [`examples/algorithm.go`](examples/algorithm.go) — Go before/after (smells #16–#22); `go run algorithm.go` prints both on the sample input.
- [`tests/run_examples.py`](tests/run_examples.py) — behavior check: `python tests/run_examples.py`.
- [`tests/benchmark.py`](tests/benchmark.py) — smell-density check: `python tests/benchmark.py`.
- [`tests/test_prose.py`](tests/test_prose.py) — prose tell-density check: `python tests/test_prose.py`.

## What it is and isn't

v1.4.0. Three skills, usable today as instructions for any LLM agent.

It makes a good agent less likely to write something that reads as generated. It won't fix logic that was wrong to begin with, and it is not a tool for beating AI detectors. We're after readable, human code, not undetectability.

## Attribution & license

Built on MIT-licensed and public work. See [ATTRIBUTION.md](ATTRIBUTION.md). MIT — see [LICENSE](LICENSE).

🇨🇳 [中文文档](readme_zh.md)
