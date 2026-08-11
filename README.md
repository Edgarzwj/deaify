# deaify — Remove AI smell from your code

> Prevention **and** remediation for AI-generated code. Make LLM output read like a competent human wrote it — including algorithm and systems code.

[中文说明](#中文说明)

## What is this?

`deaify` is a small suite of three Agent Skills that fight the tell-tale signs of AI-generated **code and prose**. Most "humanizer" projects target text only; Ponytail/Karpathy target code-writing only. `deaify` covers both directions — **prevention** (write lean / write human) and **remediation** (rewrite existing AI-smelling code *and* prose) — and is, as far as we can tell, the only packaged skill that does **remediation on code**.

It contains three skills:

- **`code-no-slop`** — a *prevention* guard. Fuses Ponytail's 7-rung "lazy ladder" + Karpathy's four rules + the LLM-smells research taxonomy. Tells the agent to write the minimum that works and not over-engineer. **Bundles Karpathy's real worked before/after examples** (over-abstraction, surgical drive-by refactor, test-first). Has a pre-delivery self-audit gate.
- **`code-humanizer`** — a *remediation* skill. Takes code that already smells of AI and rewrites it to look human, using a 22-smell detection checklist (15 core + 7 algorithm/systems extended) with before/after examples (JS/TS + Python, plus a Go example). Has a smell-density self-check before delivery.
- **`humanize-prose`** — the *prose* twin. Covers both prevention (write human from scratch) and remediation (rewrite AI-sounding text), with 24 AI tells including a technical/algorithm-writing dimension. This is the "speaking AI smell" half of the original ask, and the writing counterpart to `code-humanizer`.

## Why this exists (the gap on GitHub)

We surveyed GitHub. The landscape:

- **Text humanizers (abundant):** `blader/humanizer` (33 patterns, ~23k★), the Chinese port `op7418/Humanizer`, `kakawaa/humanizer`, `Aboudjem/humanizer-skill`, etc. All rewrite *prose*.
- **Code prevention (a few):** `DietrichGebert/ponytail` (~93k★, anti-over-engineering), `forrestchang/andrej-karpathy-skills` (~98k★, four rules), `caveman` (terse prose). These stop the agent from *writing* bloat.
- **Code remediation (none we found):** no packaged skill takes *existing* AI-generated code and rewrites it to look human. "AI code smells" exist only as blog checklists (`vibecodedetector`, LLM-smells field guides), not as an actionable, rewritable skill.

### Our breakthrough / advantages

1. **First rewrite-type code humanizer.** Distinct from the dominant prevention-only tools. Prevention stops bloat; remediation cleans up what already shipped.
2. **Algorithm & systems-code focus.** Most AI-code discussion is web/CRUD-flavored. We explicitly cover algorithm tells: reinventing the stdlib (`pow`/`gcd`/`unique`/bisect), unnamed magic constants (`1e9+7`, `eps`), step-by-step narration comments, over-abstracting one algorithm into a class, defensive `deepcopy`, vacuous `except: return -1`. *If it doesn't help algorithm code, it isn't good enough* — that's our bar.
3. **Dual-layer, one coherent philosophy.** Prevention (`code-no-slop`, a superset of Ponytail + Karpathy + Saxena) and remediation (`code-humanizer`) cross-reference each other.
4. **Verification discipline.** `code-humanizer` mandates that rewrites be executed/verified behavior-preserving before delivery — a concrete quality gate most skills lack. A runnable `tests/run_examples.py` proves it: it executes `examples/algorithm.py` and re-checks before/after pairs for identical output.
5. **Now covers prose too.** `humanize-prose` closes the original "speaking AI smell" half — prevention + remediation for writing, including technical/algorithm explanations. Pairs with the code skills the way Ponytail pairs with `caveman`.
6. **Honest scope.** We target readability/humanness, **not** adversarial AI-detector evasion. We say so.

## Install

Works with any Agent Skills runtime that scans a `skills/` directory — WorkBuddy, Claude Code, OpenCode, Cursor, Cline, and friends.

```bash
git clone https://github.com/Edgarzwj/deaify.git

# WorkBuddy (global, all projects):
cp -r deaify/skills/* ~/.workbuddy/skills/

# Claude Code (global):
cp -r deaify/skills/* ~/.claude/skills/

# Project-scoped (travels with your repo): copy the two skill folders
# into your project's skills directory.
```

> Note: `code-no-slop` already includes Ponytail + Karpathy. **Do not** also install those separately — it would double-inject the same guidance.

## Portability — multi-agent adapters

`deaify` runs wherever an Agent Skills runtime scans `skills/` (WorkBuddy,
Claude Code, OpenCode, Cursor, Cline, …). For tools that instead read **project
rule files**, this repo also ships portable adapters generated from the same
source as the skills — so the rules work even without a skills runtime:

| File | Read by |
|------|---------|
| `AGENTS.md` | Claude Code, Codex, Gemini, OpenCode, Devin, and any AGENTS.md-aware agent |
| `.cursor/rules/deaify.mdc` | Cursor |
| `.qoder/rules/deaify.md` | Qoder |
| `.windsurf/rules/deaify.md` | Windsurf |
| `.claude/CLAUDE.md` | Claude Code (project-scoped) |

**You do NOT need to download any of those apps to author or ship these files** —
they are plain text/config that the tools read when they open your project. Just
copy the repo (or the relevant adapter file) into your project. To actually
*verify in-app* that a tool picks the rules up, you'd install the app
(e.g. `npm i -g opencode` for OpenCode, or download Qoder) — that's optional
testing, not a publishing requirement.

> Note: the adapters are a generated copy of `skills/*/SKILL.md`. If you edit a
> skill, regenerate the adapters so they stay in sync.

## Usage

- **Prevention:** keep `code-no-slop` active, or tell the agent "be lazy / simplest solution / yagni". It enforces the lazy ladder on every coding task. Intensity: `code-no-slop lite|full|ultra`.
- **Remediation:** paste AI-generated code and say "humanize this code / remove the AI smell / de-AI this". It returns rewritten code plus a changes list mapping each edit to a smell number.

## Examples

- [`examples/algorithm.py`](examples/algorithm.py) — verified: before/after produce identical outputs.
- [`examples/web.ts`](examples/web.ts) — TS/JS before/after.
- [`examples/algorithm.go`](examples/algorithm.go) — Go before/after for #16–#22 (`go run algorithm.go` prints both agreeing on the sample input).
- [`tests/run_examples.py`](tests/run_examples.py) — behavior-preservation harness; run `python tests/run_examples.py`.
- [`tests/benchmark.py`](tests/benchmark.py) — smell-density benchmark; run `python tests/benchmark.py` to measure how much AI smell a humanized rewrite removes (BEFORE → AFTER signal count).

## Status / honest caveats

- **v1.4.0.** Three skills (code-no-slop, code-humanizer, humanize-prose), all usable today as instructions for any LLM agent. `code-no-slop` now folds in Karpathy's **real worked examples** (from `forrestchang/andrej-karpathy-skills` EXAMPLES.md) so its four rules ship with concrete before/after, not just abstract bullet points.
- Validated on algorithm + web + prose samples. The code smell list (15 core + 7 algorithm/systems extended) and the prose tell list (24) are strong starting points, not exhaustive — we expect to extend them with real-world use.
- It is a prompt/skill, not a linter or a model. Quality depends on the underlying agent. It makes good agents better at not looking AI-generated; it will not fix fundamentally wrong logic.

## Attribution

This suite stands on the shoulders of several MIT-licensed and public resources. See [`ATTRIBUTION.md`](ATTRIBUTION.md).

## License

MIT — see [`LICENSE`](LICENSE).

---

## 中文说明

`deaify` 是一套覆盖**代码和文字**的 Agent Skill，同时做两件事：**预防**（写码/写作时别过度工程、写得像人）和**改写**（把已有的 AI 味代码和文字都改得像人写的）。

- `code-no-slop`：预防型（代码）。融合 Ponytail 的「懒人七级阶梯」+ Karpathy 四规则 + LLM Smells 研究，要求 Agent 只写最少能跑的代码；**内置 Karpathy 真实 before/after 案例**（过度抽象 / 顺手重构 / 测试优先）；含交付前自检门禁。
- `code-humanizer`：改写型（代码）。用 22 条「AI 代码气味」清单（15 条核心 + 7 条算法/系统）检测已有代码并重写，带 JS/TS、Python 与 Go 的 before/after，**含算法方向**；含交付前气味密度自检。
- `humanize-prose`：文字侧孪生。预防（写作时就写人话）+ 改写（重写 AI 味的文字），含 24 条 AI 文字气味，并覆盖技术/算法写作维度。这就是你最初要的「说话 AI 味」那一半，对应 `code-humanizer` 的文字版。

**为什么是突破**：GitHub 上 `humanizer` 类全是改文字的；Ponytail/Karpathy 是「写码前防过度工程」的预防型；而「把已有 AI 代码重写成人味」的**改写型 skill 之前没有**。我们补上了这个空缺，并且专门覆盖算法代码（重造标准库、未命名魔法常量、逐行废话注释、单算法过度抽象成类、防御性 deepcopy、空 `except` 返回 -1），现在又把文字侧也补齐——如果帮不到算法场景，那它就不算好，这是我们的底线。

用法、安装、示例见上文。

**多代理适配**：除了 `skills/`，本仓库还附带可移植适配器——`AGENTS.md`、`.cursor/rules/deaify.mdc`、`.qoder/rules/deaify.md`、`.windsurf/rules/deaify.md`、`.claude/CLAUDE.md`，把同一套规则喂给 Cursor / Qoder / Windsurf / OpenCode / Claude Code 等「读项目规则文件」的 Agent。**写这些文件不需要下载任何 App**，它们就是纯文本，App 打开项目时自动读取；下载 App 只是为了在 App 内实测规则是否被读到，可选。
