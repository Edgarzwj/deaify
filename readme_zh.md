# deaify — 给你的代码去 AI 味

> 既**预防**又**改写** AI 生成的代码。让大模型的输出读起来像靠谱的人类写的——包括算法和系统代码。

🇬🇧 English documentation: [README.md](README.md)

## 这是什么？

`deaify` 是一套包含三个 Agent Skill 的小工具集，专门对抗 AI 生成的**代码和文字**里那种“AI 味”。大多数 humanizer 项目只针对文字；Ponytail / Karpathy 只针对“写码前预防”。`deaify` 两个方向都覆盖——**预防**（写得精简、写得像人）和**改写**（把已有的 AI 味代码*和*文字重写得像人写的）——而且据我们所知，它是唯一一个做**代码改写**的打包 skill。

包含三个 skill：

- **`code-no-slop`** —— *预防*型。融合 Ponytail 的「懒人七级阶梯」+ Karpathy 四规则 + LLM Smells 研究分类，要求 Agent 只写最少能跑的代码、不要过度工程。**内置 Karpathy 真实的 before/after 案例**（过度抽象 / 顺手式重构 / 测试优先），含交付前自检门禁。
- **`code-humanizer`** —— *改写*型。拿已经 AI 味的代码，用 22 条「AI 代码气味」清单（15 条核心 + 7 条算法/系统扩展）检测并重写，带 JS/TS、Python 与 Go 的 before/after 示例，含交付前气味密度自检。
- **`humanize-prose`** —— 文字侧孪生。既预防（写作时就写人话）又改写（重写 AI 味的文字），含 24 条 AI 文字气味，并覆盖技术/算法写作维度。这就是你最初要的「说话 AI 味」那一半，对应 `code-humanizer` 的文字版。

## 为什么做这个（GitHub 上的空缺）

我们调研了 GitHub，现状如下：

- **文字 humanizer（很多）：** `blader/humanizer`（33 模式，~23k★）、中文移植版 `op7418/Humanizer`、`kakawaa/humanizer`、`Aboudjem/humanizer-skill` 等。全部只改*文字*。
- **代码预防（少数）：** `DietrichGebert/ponytail`（~93k★，反过度工程）、`forrestchang/andrej-karpathy-skills`（~98k★，四规则）、`caveman`（简洁文风）。这些只阻止 Agent *写出*臃肿代码。
- **代码改写（没找到）：** 没有任何打包 skill 拿*已有的* AI 生成代码去重写得像人。所谓「AI 代码气味」只存在于博客清单（`vibecodedetector`、LLM-smells 指南），不是可操作、可重写的 skill。

### 我们的突破 / 优势

1. **首个改写型代码 humanizer。** 区别于主流的「只预防」工具。预防是别写出臃肿；改写是清理已经上线的东西。
2. **算法 & 系统代码导向。** 多数 AI 代码讨论都是 Web/CRUD 味。我们明确覆盖算法气味：重造标准库（`pow`/`gcd`/`unique`/bisect）、未命名魔法常量（`1e9+7`、`eps`）、逐行废话注释、单算法过度抽象成类、防御性 `deepcopy`、空洞 `except: return -1`。*帮不到算法场景就不算好*——这是我们的底线。
3. **双层一体、一套理念。** 预防（`code-no-slop`，Ponytail + Karpathy + Saxena 的超集）+ 改写（`code-humanizer`）互相引用。
4. **验证纪律。** `code-humanizer` 强制要求改写后在交付前*执行/验证行为一致*——这是多数 skill 缺的具体质量门禁。可运行的 `tests/run_examples.py` 就是证明：它执行 `examples/algorithm.py`，重新核对 before/after 输出完全一致。
5. **现在也覆盖文字。** `humanize-prose` 补齐了最初的「说话 AI 味」那一半——写作的预防 + 改写，含技术/算法说明。和代码 skill 的关系，相当于 Ponytail 配上 `caveman`。
6. **诚实的边界。** 我们做的是可读性 / 人味，**不是**对抗 AI 检测器绕过。我们明说。

## 安装

适用于任何会扫描 `skills/` 目录的 Agent Skills 运行时——WorkBuddy、Claude Code、OpenCode、Cursor、Cline 等。

```bash
git clone https://github.com/Edgarzwj/deaify.git

# WorkBuddy（全局，所有项目）：
cp -r deaify/skills/* ~/.workbuddy/skills/

# Claude Code（全局）：
cp -r deaify/skills/* ~/.claude/skills/

# 项目级（跟着仓库走）：把两个 skill 文件夹拷进你项目的 skills 目录。
```

> 注意：`code-no-slop` 已经包含了 Ponytail + Karpathy。**不要**再单独安装它们——会重复注入同一套指引。

## 多代理适配（可移植）

`deaify` 在任何会扫描 `skills/` 的运行时都能跑（WorkBuddy、Claude Code、OpenCode、Cursor、Cline……）。对于那些改为读取**项目规则文件**的工具，本仓库还附带了从 skill 同源生成的便携适配器——即使没有 skills 运行时，规则也能生效：

| 文件 | 被谁读取 |
|------|---------|
| `AGENTS.md` | Claude Code、Codex、Gemini、OpenCode、Devin，以及任何支持 AGENTS.md 的 Agent |
| `.cursor/rules/deaify.mdc` | Cursor |
| `.qoder/rules/deaify.md` | Qoder |
| `.windsurf/rules/deaify.md` | Windsurf |
| `.claude/CLAUDE.md` | Claude Code（项目级） |

**写这些文件不需要下载任何 App** —— 它们都是纯文本/配置，工具打开项目时自动读取。把仓库（或相关适配器文件）拷进项目即可。要*在 App 内实测*规则是否被读到，才需要装 App（例如 `npm i -g opencode` 装 OpenCode，或下载 Qoder）——那是可选的测试，不是发布要求。

> 注意：适配器是 `skills/*/SKILL.md` 的生成副本。如果你改了 skill，记得重新生成适配器以保持同步。

## 用法

- **预防：** 保持 `code-no-slop` 启用，或对 Agent 说「be lazy / 用最简方案 / yagni」。它会在每个编码任务上强制执行懒人阶梯。强度：`code-no-slop lite|full|ultra`。
- **改写：** 贴一段 AI 生成的代码，说「humanize this code / 去掉 AI 味 / 去 AI 化」。它会返回重写后的代码，外加一张改动清单，把每处编辑对应到气味编号。

## 示例

- [`examples/algorithm.py`](examples/algorithm.py) —— 已验证：before/after 输出完全一致。
- [`examples/web.ts`](examples/web.ts) —— TS/JS 的 before/after。
- [`examples/algorithm.go`](examples/algorithm.go) —— Go 的 before/after，对应 #16–#22（`go run algorithm.go` 会在示例输入上打印两份一致的结果）。
- [`tests/run_examples.py`](tests/run_examples.py) —— 行为一致性测试；运行 `python tests/run_examples.py`。
- [`tests/benchmark.py`](tests/benchmark.py) —— 气味密度基准；运行 `python tests/benchmark.py` 衡量一次人性化重写去掉了多少 AI 味（BEFORE → AFTER 信号数）。

## 状态 / 诚实说明

- **v1.4.0.** 三个 skill（code-no-slop、code-humanizer、humanize-prose）现在都能用，作为任意 LLM Agent 的指令。`code-no-slop` 现已并入 Karpathy 的**真实 worked examples**（来自 `forrestchang/andrej-karpathy-skills` 的 EXAMPLES.md），让它的四条规则带上具体 before/after，而不是只有抽象要点。
- 已在算法 + Web + 文字样本上验证。代码气味清单（15 核心 + 7 算法/系统扩展）和文字气味清单（24 条）是扎实的起点，而非穷尽——我们预期会在真实使用中继续扩充。
- 它是 prompt/skill，不是 linter 或模型。质量取决于底层 Agent。它让好 Agent 更不像 AI 生成；它修不了根上就错的逻辑。

## 出处

本套件立足于多个 MIT 许可及公开资源。详见 [`ATTRIBUTION.md`](ATTRIBUTION.md)。

## 许可证

MIT —— 详见 [`LICENSE`](LICENSE)。
