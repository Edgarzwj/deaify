# deaify — Remove AI smell from your code

> Prevention **and** remediation for AI-generated code. Make LLM output read like a competent human wrote it — including algorithm and systems code.

[中文说明](#中文说明)

## What is this?

`deaify` is a small suite of two Agent Skills that fight the specific tell-tale signs of AI-generated **code** (not prose). Almost every "humanizer" project on GitHub targets text/writing; this one targets *code*, and — as far as we can tell — is the only packaged skill that does **remediation** (rewrite existing AI-smelling code) on top of **prevention** (write lean in the first place).

It contains two skills:

- **`code-no-slop`** — a *prevention* guard. Fuses Ponytail's 7-rung "lazy ladder" + Karpathy's four rules + the LLM-smells research taxonomy. Tells the agent to write the minimum that works and not over-engineer.
- **`code-humanizer`** — a *remediation* skill. Takes code that already smells of AI and rewrites it to look human, using a 22-smell detection checklist (15 core + 7 algorithm/systems extended) with before/after examples (JS/TS + Python, including algorithm code).

## Why this exists (the gap on GitHub)

We surveyed GitHub. The landscape:

- **Text humanizers (abundant):** `blader/humanizer` (33 patterns, ~23k★), the Chinese port `op7418/Humanizer`, `kakawaa/humanizer`, `Aboudjem/humanizer-skill`, etc. All rewrite *prose*.
- **Code prevention (a few):** `DietrichGebert/ponytail` (~93k★, anti-over-engineering), `forrestchang/andrej-karpathy-skills` (~98k★, four rules), `caveman` (terse prose). These stop the agent from *writing* bloat.
- **Code remediation (none we found):** no packaged skill takes *existing* AI-generated code and rewrites it to look human. "AI code smells" exist only as blog checklists (`vibecodedetector`, LLM-smells field guides), not as an actionable, rewritable skill.

### Our breakthrough / advantages

1. **First rewrite-type code humanizer.** Distinct from the dominant prevention-only tools. Prevention stops bloat; remediation cleans up what already shipped.
2. **Algorithm & systems-code focus.** Most AI-code discussion is web/CRUD-flavored. We explicitly cover algorithm tells: reinventing the stdlib (`pow`/`gcd`/`unique`/bisect), unnamed magic constants (`1e9+7`, `eps`), step-by-step narration comments, over-abstracting one algorithm into a class, defensive `deepcopy`, vacuous `except: return -1`. *If it doesn't help algorithm code, it isn't good enough* — that's our bar.
3. **Dual-layer, one coherent philosophy.** Prevention (`code-no-slop`, a superset of Ponytail + Karpathy + Saxena) and remediation (`code-humanizer`) cross-reference each other.
4. **Verification discipline.** `code-humanizer` mandates that rewrites be executed/verified behavior-preserving before delivery — a concrete quality gate most skills lack.
5. **Honest scope.** We target readability/humanness, **not** adversarial AI-detector evasion. We say so.

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

## Usage

- **Prevention:** keep `code-no-slop` active, or tell the agent "be lazy / simplest solution / yagni". It enforces the lazy ladder on every coding task. Intensity: `code-no-slop lite|full|ultra`.
- **Remediation:** paste AI-generated code and say "humanize this code / remove the AI smell / de-AI this". It returns rewritten code plus a changes list mapping each edit to a smell number.

## Examples

- [`examples/algorithm.py`](examples/algorithm.py) — verified: before/after produce identical outputs.
- [`examples/web.ts`](examples/web.ts) — TS/JS before/after.

## Status / honest caveats

- **v1.1.0.** Usable today as instructions for any LLM agent.
- Validated on algorithm + web samples. The smell list (15 core + 7 algorithm/systems extended) is a strong starting point, not exhaustive — we expect to extend it with real-world use.
- It is a prompt/skill, not a linter or a model. Quality depends on the underlying agent. It makes good agents better at not looking AI-generated; it will not fix fundamentally wrong logic.

## Attribution

This suite stands on the shoulders of several MIT-licensed and public resources. See [`ATTRIBUTION.md`](ATTRIBUTION.md).

## License

MIT — see [`LICENSE`](LICENSE).

---

## 中文说明

`deaify` 是一套**针对代码（而非文字）**的 Agent Skill，同时做两件事：**预防**（写码时别过度工程）和**改写**（把已有的 AI 味代码改得像人写的）。

- `code-no-slop`：预防型。融合 Ponytail 的「懒人七级阶梯」+ Karpathy 四规则 + LLM Smells 研究，要求 Agent 只写最少能跑的代码。
- `code-humanizer`：改写型。用 22 条「AI 代码气味」清单（15 条核心 + 7 条算法/系统）检测已有代码并重写，带 JS/TS 与 Python 的 before/after，**含算法方向**。

**为什么是突破**：GitHub 上 `humanizer` 类全是改文字的；Ponytail/Karpathy 是「写码前防过度工程」的预防型；而「把已有 AI 代码重写成人味」的**改写型 skill 目前没有**。我们补上了这个空缺，并且专门覆盖算法代码（重造标准库、未命名魔法常量、逐行废话注释、单算法过度抽象成类、防御性 deepcopy、空 `except` 返回 -1）。如果帮不到算法场景，那它就不算好——这是我们的底线。

用法、安装、示例见上文。
