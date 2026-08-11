# deaify

给你的代码和文字去 AI 味——写之前防，写之后改。

`deaify` 是三个 Agent Skill，专门修 LLM 生成的**代码和文字**里的 AI 痕迹。大多数 humanizer 只管文字；Ponytail 和 Karpathy 教模型"别写出臃肿代码"。没有一个工具会拿**已经** AI 味的代码，重写得像人写的。这一步就是 `deaify` 补上的。

## 三个 skill

- **`code-no-slop`** —— 代码预防。Ponytail 懒人阶梯 + Karpathy 四规则的超集，外加 LLM Smells 分类。让 Agent 只写最小能跑的东西。内置 Karpathy 真实 before/after（过度抽象、顺手重构、测试优先），含交付前自检。
- **`code-humanizer`** —— 代码改写。读一段 AI 味的代码并重写，对照 22 条气味（15 通用 + 7 算法/系统），带 JS/TS、Python、Go 的 before/after，交付前检查气味密度确实下降了。
- **`humanize-prose`** —— 文字孪生。文字的预防 + 改写，30+ 条痕迹（英文 + 中文 AI 腔），含技术/算法写作轨道。

## 为什么"代码改写"这半块重要

有意思的是 `code-humanizer`。Ponytail、Karpathy 这类预防工具，是阻止模型*写出*臃肿；它们修不了那坨已经上线的 800 行文件。`deaify` 能。而且它先做算法代码：重造标准库（`pow`/`gcd`/`bisect`）、未命名魔法常量（`1e9+7`、`eps`）、逐行废话注释、单算法包成类、防御性 `deepcopy`、`except: return -1`。一个 skill 帮不到算法场景，就不值得发。这是底线。

`code-humanizer` 也不会把没验证过的重写丢给你。它跑一遍 before/after，确认输出一致（`tests/run_examples.py` 在自带示例上做这件事）。多数 skill 跳过了这一步。

## 安装

只要 Agent Skills 运行时能扫 `skills/` 目录就行：WorkBuddy、Claude Code、OpenCode、Cursor、Cline。

```bash
git clone https://github.com/Edgarzwj/deaify.git
cp -r deaify/skills/* ~/.workbuddy/skills/   # WorkBuddy，全局
cp -r deaify/skills/* ~/.claude/skills/      # Claude Code，全局
```

`code-no-slop` 已经包含 Ponytail 和 Karpathy，别再单独装，否则同一套指引注入两遍。

## 多代理适配

有些工具读的是"项目规则文件"而不是 `skills/` 目录。本仓库附带同源生成的适配器，规则在这些工具里也能用：

| 文件 | 被谁读取 |
|------|---------|
| `AGENTS.md` | Claude Code、Codex、Gemini、OpenCode、Devin |
| `.cursor/rules/deaify.mdc` | Cursor |
| `.qoder/rules/deaify.md` | Qoder |
| `.windsurf/rules/deaify.md` | Windsurf |
| `.claude/CLAUDE.md` | Claude Code（项目级） |

写这些文件不需要装任何 App，它们就是纯文本，工具打开项目时自动读。适配器是 skill 文件的副本，改了 skill 记得重新生成。

## 用法

- 预防：保持 `code-no-slop` 开启，或对 Agent 说"be lazy / 用最简方案 / yagni"。
- 改写：贴一段 AI 代码，说"humanize this / 去掉 AI 味"。你会拿到重写后的代码，外加一张把每处编辑对应到气味编号的清单。

## 示例

- [`examples/algorithm.py`](examples/algorithm.py) —— before/after 输出一致。
- [`examples/web.ts`](examples/web.ts) —— TS/JS 的 before/after。
- [`examples/algorithm.go`](examples/algorithm.go) —— Go 的 before/after（气味 #16–#22）；`go run algorithm.go` 会在示例输入上打印两份。
- [`tests/run_examples.py`](tests/run_examples.py) —— 行为校验：`python tests/run_examples.py`。
- [`tests/benchmark.py`](tests/benchmark.py) —— 气味密度校验：`python tests/benchmark.py`。
- [`tests/test_prose.py`](tests/test_prose.py) —— 文字痕迹密度校验：`python tests/test_prose.py`。

## 它是什么，不是什么

v1.4.0。三个 skill，现在就能当任意 LLM Agent 的指令用。

它让好 Agent 更不容易写出"读起来像生成"的东西。它修不了本来逻辑就错的部分，也不是用来绕过 AI 检测器的。我们要的是可读、像人的代码——不是"检测不出来"。

## 出处与许可

基于 MIT 许可及公开成果。详见 [ATTRIBUTION.md](ATTRIBUTION.md)。MIT——详见 [LICENSE](LICENSE)。

🇬🇧 [English](README.md)
