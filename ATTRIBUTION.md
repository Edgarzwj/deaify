# Attribution

`deaify` is a derivative/adaptation that fuses several MIT-licensed and public
resources. We did not invent the underlying ideas; we assembled and extended
them into the first *remediation-type* code humanizer with an algorithm focus.

## Direct sources incorporated

- **Ponytail** — `DietrichGebert/ponytail` (MIT). The 7-rung "lazy ladder",
  intensity levels (lite/full/ultra), `ponytail:` ceiling comments, and
  "bug fix = root cause". → lives in `code-no-slop`.
- **andrej-karpathy-skills** — `forrestchang/andrej-karpathy-skills` (MIT).
  The four behavioral rules (think-first, simplicity, surgical changes,
  goal-driven) **plus its real worked EXAMPLES** (over-abstraction, surgical
  drive-by refactor, test-first) — folded verbatim-adapted into `code-no-slop`'s
  "Karpathy's Four Rules" section.
- **Saxena "LLM Smells" taxonomy** — field guide / research on fake modularity,
  fake complexity, and hallucinated package/API names. → three extra preventive
  rules in `code-no-slop`.

## Inspiration / basis

- **Wikipedia "Signs of AI writing"** (WikiProject AI Cleanup) — the conceptual
  parent of every "humanizer"; the framing of detecting *clusters* of tells
  rather than isolated signals. This is the direct basis of `humanize-prose`'s
  20 core tells (hedged openers, tell vocabulary, em-dash overuse, recap
  conclusions, no opinion, vague nouns).
- **vibecodedetector.com "15 AI Code Smells"** — the basis of the 15 core + 7
  extended (algorithm/systems) smell checklist in `code-humanizer`.
- **blader/humanizer** and the wider humanizer ecosystem — proved the
  "humanize" pattern works and set the quality bar for before/after examples.
- **Ponytail + `caveman` pairing** — the ecosystem pattern of pairing a
  code-guard with a prose-guard. `deaify` mirrors this: `code-no-slop` +
  `code-humanizer` (code) alongside `humanize-prose` (prose).

## What we added (the novel part)

1. A *rewrite-type* code humanizer (`code-humanizer`) — distinct from
   prevention-only tools.
2. Explicit **algorithm & systems-code** coverage: reinvented stdlib, unnamed
   constants, narration comments, over-abstraction of single algorithms,
   defensive deepcopy, vacuous error handling.
3. A verification mandate: rewrites must be executed/verified
   behavior-preserving before delivery — backed by a runnable
   `tests/run_examples.py` harness.
4. A **prose** skill (`humanize-prose`) covering both prevention and
   remediation of AI-sounding writing, including a technical/algorithm-writing
   dimension — closing the original "speaking AI smell" half of the ask.

All upstream works retain their original licenses; this suite is MIT.
