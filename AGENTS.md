# deaify -- remove AI smell from code & prose

Apply these rules whenever you write or review code, or write/rewrite prose.
The full skills live in `skills/`; this file is the portable copy for agents
that read project rule files (Claude Code, Cursor, Qoder, Windsurf, OpenCode,
Codex, ...). Keep it in sync with skills/*/SKILL.md.

## A. Writing code -- code-no-slop (prevention)

Act as a lazy senior dev: write the minimum that works.

**Lazy ladder** (stop at the first rung that holds):
1. Does it need to exist? Skip speculative code (YAGNI).
2. Already in this codebase? Reuse it.
3. Stdlib does it? Use it.
4. Native platform feature covers it? Use it (e.g. `<input type=date>` over a picker lib).
5. An installed dependency solves it? Use it.
6. Can it be one line? One line.
7. Only then: the minimum code that works.

**Karpathy's four rules:** think before coding (state assumptions); simplicity first
(no speculative abstraction); surgical changes (touch only what's asked); goal-driven
(verifiable goals, then verify).

**LLM-smell extra rules:** never hallucinate packages/APIs (verify imports exist);
no fake modularity (inline single-use helpers); no fake complexity (uneven code length is fine).

**Algorithm/systems code:** use the math stdlib (`**`, `math.gcd`, `bisect`, `heapq`)
not reimplementations; name magic constants (`MOD = 1_000_000_007`); no narration
comments (`# increment i`); don't class-ify one algorithm; don't `deepcopy` defensively.

**Pre-delivery self-audit:** read the diff (every line traces to the request?); ladder
check (no reinvented stdlib); algorithm check; no invented deps; lean check (explanation <= code).

## B. Rewriting existing code -- code-humanizer (remediation)

Rewrite AI-smelling code to read human; **preserve behavior exactly**.

**Scan for these smells** (a single instance is noise; clusters are a confession):
1. Explicit boolean check (`if (x === true)`)
2. Tutorial names (`foo/bar/tmp/data/result/obj/arr`)
3. Zombie / commented-out code
4. One-size error log (`console.error("An error occurred")`)
5. Regurgitated docs (comments copied from MDN)
6. Over-defensive null chains
7. Premature optimization (caching a once-run fn)
8. Ghost variables (declared, never used)
9. Copy-paste repetition (3+ duplicates)
10. Over-engineered class (one-method wrapper)
11. Default switch that throws on a covered enum
12. Magic number (`86400000` unnamed)
13. Unused import
14. Generic TODO
15. Soulless formatting (every fn the same length)
16. Reinvented stdlib (`pow`/`gcd`/`unique`/`bisect`/`heap`)
17. Unnamed magic constant (`1e9+7`, `10**18`)
18. Narration comment
19. Tutorial names in hot loops (`tmp1`/`ans`)
20. Over-abstracted single algorithm (class around `sorted`)
21. Defensive deepcopy
22. Vacuous error handling (`except: return -1`)

**Process:** read; cite smell numbers; rewrite idiomatically; **verify behavior-preserving**
(run or trace, incl. edge cases: empty input, overflow, modulo wrap); present code + a
changes list mapping edits to smell numbers.

**Smell-density self-check:** one fix on a 200-line file is suspicious -- rescan; confirm
behavior; read top-to-bottom; if nothing changed, say "already clean".

## C. Writing/rewriting prose -- humanize-prose (prevention + remediation)

**24 AI tells:** hedged openers ("It's worth noting"); filler transitions
("Moreover"/"Furthermore"); tell vocabulary (delve/tapestry/leverage/robust/holistic);
thesis-restating intro; 3-part listicle uniformity; "not only ... but also"; em-dash
overuse; recap conclusion; no opinion; vague nouns (solution/approach/landscape);
robotic enumeration; both-sides hedge; apologetic qualifiers; synonym padding
(utilize -> use); formulaic enthusiasm; definition-by-apposition; passive default; no
specifics/numbers; uniform tone; explaining the obvious; *[tech]* narration of trivial;
hiding the tradeoff; pseudo-generic abstraction; no worked example/code.

**Prevention:** write to one specific person; state an opinion; use specifics (names,
numbers); vary sentence length; cut filler transitions.
**Remediation:** preserve meaning, change only voice; **read aloud** -- if it sounds like
a brochure / LinkedIn post, rewrite.

## Pairing

`code-no-slop` (write lean) + `code-humanizer` (de-AI existing code) + `humanize-prose`
(de-AI prose). Do not use these to launder factual inaccuracies.
