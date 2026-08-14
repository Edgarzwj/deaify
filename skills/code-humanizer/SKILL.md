---
name: code-humanizer
description: "Rewrite AI-flavored code to read like it was written by a competent human, including algorithm and systems code. Use when given existing code that looks machine-generated — over-commented, generically named, over-defensive, over-abstracted, or uniformly structured — and asked to 'humanize', 'de-AI', 'make this less AI-generated', or 'remove the AI smell' from code. Detects 23 AI code smells (15 core + 7 algorithm/systems extended + 1 fake-header-comment) and rewrites them with verified before/after examples across JS/TS and Python."
description_zh: "去除代码的 AI 味：把 AI 生成的代码改得像人写的（含算法/系统代码）"
description_en: "Remove AI smell from code"
version: 1.0.0
agent_created: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
display_name: "code-humanizer"
display_name_en: "code-humanizer"
visibility: "public"
---

# code-humanizer — Remove AI Smell From Code

Act as a senior engineer reviewing code that an LLM clearly wrote, and rewrite it so it reads like a competent human authored it. Preserve behavior exactly; change only what makes the code look machine-generated.

This skill is the *remediation* counterpart to `code-no-slop` (which prevents over-engineering while writing). Use this one on code that already exists and already smells of AI.

## When to use

Trigger when the user pastes code and asks to "humanize this code", "remove the AI smell", "make this less AI-generated", "de-AI this", or when code exhibits the smells below. Also useful as a final pass before committing AI-generated code.

Do NOT use for prose, comments, or commit messages — that is the `humanizer` skill's job.

## The 15 AI Code Smells

Scan for these patterns. A single instance is noise; *clusters* are a confession.

> For **algorithm / systems / numeric** code, also scan the extended smells **#16–#22** in the next section — they are part of the same scan, not optional.

1. **Explicit boolean check** — `if (user.isValid === true)` → `if (user.isValid)`.
2. **Tutorial variable names** — `foo`, `bar`, `baz`, `tmp`, `data`, `result`, `obj`, `arr` in production code. Rename to tell a story.
3. **Zombie code** — commented-out alternative implementations or dead drafts left behind. Delete them.
4. **One-size-fits-all error log** — `catch (e) { console.error("An error occurred:", e); }`. Include what failed and why.
5. **Regurgitated docs** — comments copied from MDN/docs (`// The map() method creates a new array...`). Delete; the code is self-explanatory.
6. **Over-defensive null check** — `if (data && data.user && data.user.profile && data.user.profile.id)` when the type system already guarantees it. Trust the types.
7. **Premature optimization** — caching/memoization for a function that runs once. Remove until a profiler says otherwise.
8. **Ghost variables** — variables declared and assigned but never used. Remove.
9. **Copy-paste repetition** — same logic 3+ times instead of a loop or helper. Extract.
10. **Over-engineered class** — a `UserProcessor` class with a constructor and one method, instead of a plain function. Inline it.
11. **Default switch case** — a `default` that throws when all enum values are already covered. Drop it (or keep only if genuinely reachable).
12. **Magic number** — `86400000` instead of `const DAY_IN_MS = 86_400_000`. Name it.
13. **Unused import** — `import { useEffect } from "react"` never used. Remove.
14. **Generic TODO** — `// TODO: implement error handling`. The AI knew it should be there but was lazy; either implement it or delete the note.
15. **Soulless formatting** — wall-of-text with no breathing room, every function the same length, zero rhythm. Break it up; let simple parts be simple.

### Extended smells — algorithm & systems code (#16–#22)

The 15 above are web/CRUD-flavored. When the code is algorithm, numeric, or systems code, also scan for these. *Clusters* of them are the confession.

16. **Reinvented stdlib** — a hand-rolled `pow` / `gcd` / `unique` / `bisect` / `heap` / `shuffle` / `clamp` when `**` / `math.gcd` / `dict.fromkeys` / `bisect` / `heapq` / `random.shuffle` / `max(min(...))` already exist. Use the built-in.
17. **Unnamed magic constant** — `1000000007` instead of `MOD = 1_000_000_007`; bare `1e-9` / `10**18` instead of `EPS` / `INF`. Name it and use digit separators.
18. **Narration comment** — `# increment i` above `i += 1`, or a comment that restates the next line. The code is the comment; delete it.
19. **Tutorial names in hot loops** — `arr` / `res` / `ans` / `tmp1` / `tmp2` for things with a real name (`items` / `counts` / `prefix` / `carry`). Note: `i` / `j` in tight numeric loops are fine; the smell is meaningless `tmp*` or `data` / `result`.
20. **Over-abstracted single algorithm** — a `SortStrategy` / `MathUtility` class with one method that just calls `sorted`. Inline it to a function.
21. **Defensive deep copy** — `copy.deepcopy` on every mutation when a shallow copy or none suffices. Copy only what you actually mutate.
22. **Vacuous error handling** — `except Exception: print("An error occurred"); return -1`. Handle the specific failure or let it propagate; do not swallow and invent a sentinel.
23. **Fake header comment** — a comment at the very top of a function or file that
    merely announces what the code does (`// This function calculates the power of a
    number using a loop`). It reads as a label stuck on for show, not help. Delete it.
    A *genuine* explanatory comment — one that states *why* a non-obvious choice was
    made, or warns of a trap — is welcome, but place it next to the line it explains,
    never as a banner above the whole block.

## Process

1. Read the input code carefully. Preserve its runtime behavior — do not change logic, only presentation and structure.
2. Identify every smell instance (cite the number from the list above).
3. Rewrite each problematic section. Prefer idiomatic, language-native conventions.
4. Ensure the result:
   - Uses specific, meaningful names over generic ones.
   - Comments explain *why*, never *what* the code already says. Never open a function
     or file with a comment that just narrates its purpose — that banner is the fakest
     possible comment (#23). Put a real explanation next to the line it explains.
   - Has defensive code only where the type system does not already guarantee safety.
   - Varies structure naturally (not every function 15–20 lines, not every block wrapped in a class).
   - Has no dead code, no unused imports, no fake TODOs.
5. **Verify before delivering.** The rewrite must be behavior-preserving. For non-trivial changes, run both the original and the humanized version on a few representative inputs and assert equal outputs. For algorithm code, include edge cases — empty input, maximum/overflow values, modulo wrap — not just the happy path. Never ship a rewrite you have not executed or at least traced by hand.
6. Present the humanized code.

## Output Format

Provide:
1. The rewritten code.
2. A short bulleted "changes" list mapping each edit to a smell number (e.g. "- #4 renamed `data` → `orders`; - #13 removed unused import").
3. If verification was run, a one-line note: "verified: original and rewrite match on inputs X, Y, Z".

## Before / After Examples

### Smell #1 + #2 + #4 + #5 (JS/TS)

Before (AI-sounding):
```ts
// The function fetches the user from the API and returns the user object
function getUserData(userId: string) {
  try {
    const data = fetchUser(userId);
    if (data.isValid === true) {
      return data;
    }
  } catch (error) {
    console.error("An error occurred:", error);
  }
}
```

After (humanized):
```ts
function getUser(userId: string): User | undefined {
  try {
    const user = fetchUser(userId);
    return user.isValid ? user : undefined;
  } catch (error) {
    console.error(`Failed to load user ${userId}:`, error);
    return undefined;
  }
}
```
Changes: #1 dropped `=== true`; #2 renamed `data` → `user`, `getUserData` → `getUser`; #4 error log now says what failed; #5 deleted the MDN-style comment. **Behavior preserved** — both the original and the rewrite return `undefined` for an invalid user or on error, so the contract is unchanged.

### Smell #10 + #8 + #13 (Python)

Before (AI-sounding):
```python
import os
import json
from typing import Any

class DataProcessor:
    def __init__(self):
        pass

    def process(self, raw: str) -> Any:
        result = json.loads(raw)
        temp = result
        return temp
```

After (humanized):
```python
import json

def parse_config(raw: str) -> dict:
    return json.loads(raw)
```
Changes: #10 replaced the class with a function; #8 removed the unused `temp`; #13 removed unused `os` import; dropped the empty `__init__`.

### Smell #6 + #12 (JS)

Before (AI-sounding):
```js
if (data && data.user && data.user.profile && data.user.profile.id) {
  const ms = 86400000;
  schedule(data.user.profile.id, ms);
}
```

After (humanized):
```js
const DAY_IN_MS = 86_400_000;
if (user?.profile?.id) {
  schedule(user.profile.id, DAY_IN_MS);
}
```
Changes: #6 collapsed the defensive chain to optional chaining (assuming types guarantee `user`); #12 named the magic number.

### Algorithm & Dev Code (verified example)

The 15 core smells above are web/CRUD-flavored. The algorithm & systems tells are now part of the scan as **#16–#22** above — do not treat them as separate. Below is a verified before/after showing those smells removed.

Before (AI-sounding, algorithm):
```python
import math

# This function calculates the power of a number using a loop
def calculate_power(base, exp):
    result = 1
    for i in range(exp):  # iterate exp times
        result = result * base
    return result

# This function removes duplicate elements from a list
def remove_duplicates(arr):
    result = []
    for i in range(len(arr)):
        if arr[i] not in result:
            result.append(arr[i])
    return result

class SortUtility:
    def __init__(self):
        pass
    def sort_data(self, data):
        return sorted(data)

MOD = 1000000007

def solve(data):
    try:
        ans = 0
        for i in range(len(data)):
            ans = (ans + data[i]) % MOD
        return ans
    except Exception as e:
        print("An error occurred")
        return -1
```

After (humanized):
```python
def power(base, exp):
    return base ** exp

def unique(items):
    return list(dict.fromkeys(items))

MOD = 1_000_000_007

def sum_mod(values):
    return sum(values) % MOD
```

Changes: reinvented `pow` (stdlib) → `**`; reinvented `unique` → `dict.fromkeys` (order-preserving, same behavior); `SortUtility` class (#10) inlined; `MOD` magic number (#12) named with digit separators; `solve`'s broad `except` + generic print (#4) removed — the normal path returns `sum(values) % MOD`, identical to before; generic `arr`/`data`/`ans`/`i` (#2) → `items`/`values`; the fake header comments at the top of `calculate_power`/`remove_duplicates` (#23) were deleted.

**Verified:** this rewrite was executed and asserted against the original on sample inputs — `power(2, 10) == 1024`, `unique([3, 1, 3, 2, 2]) == [3, 1, 2]`, `sum_mod([10**9, 10**9]) == 999999993` — outputs match, confirming the skill's "preserve behavior" rule holds.

**Cross-language:** the same tells appear in Go, Rust, C++, and beyond. A Go before/after for #16–#22 lives in `examples/algorithm.go` — `go run algorithm.go` prints both versions agreeing on the sample input. The smells are language-agnostic; only the idioms differ (`map[int]struct{}` over a hand-rolled dedup loop, named `const mod = 1_000_000_007`, no narration comments).

## Smell-density self-check (before you deliver)

Do not ship because it "looks better". Run this gate:

1. Count distinct smell numbers you fixed. **One fix on a 200-line file is suspicious** — either the code was already clean (say so, don't invent work) or you missed a cluster. Go back and scan #1–#23 again.
2. Confirm behavior preservation: original and rewrite produce identical output on the inputs you care about, **including edge cases** (empty, max/overflow, modulo wrap). If you did not run or trace it, you have not verified.
3. Read the result top-to-bottom once. Does any function still read like a template? Any comment that restates the next line, or a banner comment at the top that just narrates intent (#23)? Any `tmp`/`data`/`result` with a real name hiding? If yes, fix before delivering.
4. If nothing substantive changed, say "this is already clean" — the honest answer is sometimes zero edits.

## Add Soul, Not Just Remove Smells

Sterile, uniform code is as obvious as slop. Good human code:
- Matches the surrounding project's style and naming, even if you would do it differently.
- Uses the language's idioms (list comprehensions in Python, array methods in JS, pattern matching where natural).
- In algorithm code, uses `i`/`j` freely in tight loops but gives real names to everything that carries meaning; reaches for `itertools`, `functools`, `bisect`, `heapq` instead of reimplementing them.
- Leaves a deliberate, minimal check on non-trivial logic (an assert or a tiny test), not a full suite.
- Does not over-explain; a good name is worth three comments.

Pair this skill with `code-no-slop` so future code is written lean in the first place, and with `humanizer` for any prose, comments, or commit messages that still smell of AI.
