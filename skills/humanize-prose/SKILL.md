---
name: humanize-prose
description: "Make AI-sounding writing read like a competent human wrote it — for both prevention (writing from scratch) and remediation (rewriting existing text). Use when drafting or cleaning up prose, docs, explanations, emails, or technical/algorithm write-ups that smell of AI: hedged openers, 'delve'/'tapestry'/'navigate the landscape', three-part listicle uniformity, thesis-restating intros, brochure tone, no real opinion. Covers 20+ AI tells with before/after examples, including a technical/algorithm-writing dimension."
description_zh: "去除文字/说话的 AI 味：写作时预防 + 成文后改写（含技术/算法写作）"
description_en: "Remove AI smell from prose"
version: 1.3.0
agent_created: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
display_name: "humanize-prose"
display_name_en: "humanize-prose"
visibility: "public"
---

# humanize-prose — Remove AI Smell From Writing

Act as an editor who has read one too many generated blog posts. Your job: make the
writing sound like a specific human with a point of view, not a brochure. This skill
covers **both** directions:

- **Prevention** — write human in the first place.
- **Remediation** — take existing AI-sounding text and rewrite it.

It is the prose twin of `code-humanizer` (code) and the writing twin of what
`code-no-slop` does for code. Pair all three: write lean (`code-no-slop`), de-AI
existing code (`code-humanizer`), de-AI existing prose (this skill).

## When to use

Trigger on any writing task — docs, explanations, summaries, emails, reports,
tutorials, or technical/algorithm write-ups — when the output smells of AI, or when
the user says "make this sound human", "remove the AI tone", "less corporate",
"too robotic", or "rewrite this like a person wrote it".

Do NOT use for code, comments, or commit messages — those are `code-humanizer` /
`code-no-slop`. Do not use to launder factual inaccuracies: humanizing is about
voice, not truth.

## The 20 AI Tells (scan for these)

A single tell is noise; *clusters* are a confession.

1. **Hedged openers** — "It's worth noting", "It is important to note", "It should be
   emphasized". Just say the thing.
2. **Filler transitions** — "Moreover", "Furthermore", "Additionally", "In today's
   fast-paced world", "In the realm of". Cut them; the sentence survives.
3. **Tells vocabulary** — "delve", "tapestry", "navigate the landscape", "unravel",
   "testament to", "game-changer", "underscore", "robust", "leverage" (as a verb),
   "holistic", "seamless". Each is a tell. Replace with the plain word.
4. **Thesis-restating intro** — opening paragraph that just summarizes what the piece
   will say. Start with the actual substance or a specific hook.
5. **Three-part listicle uniformity** — every section is exactly three bullets because
   three feels complete. Use two when two is enough; four when four is honest.
6. **"Not only… but also"** constructions. Flatten them.
7. **Em-dash overuse** — a dash between every other clause. One per paragraph, max.
   Use periods.
8. **Conclusion that restates the intro** — "In conclusion, as we have seen…". End on a
   forward point or a genuine take, not a recap.
9. **No first person, no opinion** — text that could have been written by no one. Pick
   a stance and own it.
10. **Vague nouns** — "solution", "approach", "landscape", "ecosystem", "journey".
    Name the specific thing.
11. **Robotic enumeration** — "First, … Second, … Third, …" when prose order would do.
12. **Balanced both-sides hedge** — "While X has advantages, Y also has merits." Take
    a position unless neutrality is the actual point.
13. **Apologetic qualifiers** — "somewhat", "relatively", "arguably", "to a certain
    extent". Drop unless precise.
14. **Synonym padding** — "utilize" for "use", "commence" for "start", "facilitate" for
    "help". Use the short word.
15. **Formulaic enthusiasm** — "exciting", "powerful", "incredible", "revolutionary"
    attached to ordinary things. Earn enthusiasm with specifics.
16. **Definition-by-apposition** — "X, a Y that Z, …" as the first sentence of every
    paragraph. Vary the opening.
17. **Passive voice default** — "It can be observed that" instead of "I see". Prefer
    active unless the actor is genuinely unknown.
18. **No specifics, no numbers** — claims with zero concrete detail. Add a name, a
    count, a date, a measurement.
19. **All-caps-free but emoji-free corporate calm** — uniformly moderate tone, nothing
    surprising. Let one sentence be sharp.
20. **Explaining the obvious** — "we can see that", "as shown above", "it is clear
    that". Trust the reader.

### Technical & algorithm writing (extra tells)

Docs, tutorials, and algorithm explanations have their own tells:

21. **Narration of the trivial** — "we can see that the loop runs n times", "this
    function calculates the sum". State the non-obvious, skip the rest.
22. **Hiding the tradeoff** — describing an algorithm without its cost, failure mode,
    or when *not* to use it. Name the ugly case.
23. **Pseudo-generic abstraction** — "this approach can be applied to many
    scenarios" with no example. Give the worked example.
24. **No worked example / no code** — explaining an algorithm only in prose when a
    ten-line snippet would settle it. Show the work.

## Prevention — write human from scratch

- **Write to one specific person.** Picture the teammate who asked. Sound like you
  talking to them, not like a manual.
- **State an opinion.** Humans have one. "I'd use X here because Y" beats "X and Y are
  both valid approaches."
- **Use specifics.** Names, numbers, the actual thing. Kill "solution"/"approach".
- **Vary sentence length on purpose.** Short sentences are fine. A wall of same-length
  sentences is a tell.
- **Cut transitions that add nothing.** "Moreover" rarely earns its place.
- **For algorithm/technical writing:** show the math or code, name the tradeoff, admit
  the ugly case, and give a worked example. Don't narrate what the reader can see.

## Remediation — rewrite existing text

1. Read the text. Preserve its meaning and facts exactly; change only the voice.
2. Mark every tell instance (cite the number from the list above).
3. Rewrite: specifics over vague nouns, active over passive, an opinion over a hedge,
   periods over em-dashes, two points over a forced three.
4. **Verify by reading aloud.** If it sounds like a LinkedIn post or a brochure, it
   still smells — rewrite. The test is ears, not rules.

## Output Format

For remediation, provide:
1. The rewritten text.
2. A short "changes" list mapping edits to tell numbers
   (e.g. "- #3 replaced 'delve' → 'look'; - #1 cut 'It's worth noting'; - #18 added
   the actual benchmark number").
3. If read-aloud check was done, a one-line note: "read aloud: no brochure tone left."

## Before / After Examples

### Tell #1 + #3 + #8 (generic intro)

Before (AI-sounding):
> It is important to note that caching is a powerful technique that can leverage
> significant performance gains. In today's fast-paced world, many developers delve
> into caching to unlock its potential. In conclusion, as we have seen, caching
> matters.

After (humanized):
> Cache the slow thing once and most of your latency disappears. The trick is knowing
> what's actually slow — profile before you cache, or you'll memoize the wrong call.

Changes: #1 dropped "It is important to note"; #3 cut "powerful", "leverage",
"delve", "unlock its potential"; #8 ended on a real point instead of a recap.

### Tell #21 + #22 + #24 (algorithm write-up)

Before (AI-sounding):
> This function demonstrates a binary search approach. We can see that it efficiently
> finds the target by repeatedly dividing the search space. This approach can be
> applied to many scenarios where fast lookup is desired.

After (humanized):
> `bisect_left` finds the insertion point in O(log n). Use it when the list is sorted
> and you're searching repeatedly — for a one-off lookup on unsorted data, a linear
> scan is simpler and faster to read. Don't reach for it on a list you'll sort just to
> search once.

Changes: #21 cut "we can see that"; #22 named the cost (O(log n)) and the failure
mode (don't sort just to search); #24 gave the worked example; #10 replaced
"approach"/"scenarios" with specifics.

## Pairing

This skill handles prose. For code, use `code-humanizer` (existing code) and
`code-no-slop` (writing new code). Together they cover the full "de-AI" surface:
what you say, what you write, and what you build.
