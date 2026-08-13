---
name: humanize-prose
description: "Make AI-sounding writing read like a competent human wrote it — for both prevention (writing from scratch) and remediation (rewriting existing text). Use when drafting or cleaning up prose, docs, explanations, emails, or technical/algorithm write-ups that smell of AI: hedged openers, 'delve'/'tapestry'/'navigate the landscape', three-part listicle uniformity, thesis-restating intros, brochure tone, no real opinion. Covers 30+ AI tells (EN + Chinese AI-isms), a final 'obviously AI' self-critique pass, a no-fabrication fact-preservation rule, and voice-by-context guidance."
description_zh: "去除文字/说话的 AI 味：写作时预防 + 成文后改写（含技术/算法写作 + 中文 AI 腔 + 自我批判终遍 + 事实保全）"
description_en: "Remove AI smell from prose"
version: 1.4.0
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

## The 24 core AI Tells (scan for these)

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
   a stance and own it (but see *Voice by context* — not every text wants a stance).
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
21. **Narration of the trivial** — "we can see that the loop runs n times", "this
    function calculates the sum". State the non-obvious, skip the rest.
22. **Hiding the tradeoff** — describing an algorithm without its cost, failure mode,
    or when *not* to use it. Name the ugly case.
23. **Pseudo-generic abstraction** — "this approach can be applied to many
    scenarios" with no example. Give the worked example.
24. **No worked example / no code** — explaining an algorithm only in prose when a
    ten-line snippet would settle it. Show the work.

## Additional tells (Wikipedia / blader parity)

These come from Wikipedia's *Signs of AI writing* and close the gap with the
33-pattern humanizers. Most overlap with the core 24 but name the specific shape.

25. **Copula avoidance** — "serves as", "features", "boasts", "acts as" where "is" /
    "has" is plainer. "It serves as a cache" → "It's a cache."
26. **Negative parallelisms / tailing negations** — "It's not just X, it's Y",
    "…, no guessing." State the point directly.
27. **Synonym cycling** — repeating the same idea as "protagonist / main character /
    central figure / hero." Use the clearest word and repeat it.
28. **Rule of three padding** — "innovation, inspiration, and insights." Use the
    natural number of items.
29. **Boldface / emoji / curly-quote dressing** — `**OKRs**`, "🚀 Launch", `“quotes”`.
    Drop the decoration; plain text reads as more human.
30. **Chatbot artifacts** — "I hope this helps! Let me know if…", "Great question!
    You're absolutely right!" Respond directly; remove the filler.
31. **Signposting announcements** — "Let's dive in", "Here's what you need to know."
    Start with the content.
32. **Manufactured punchlines / aphorism formulas** — "Symmetry is the language of
    trust", staccato "No prior. No nostalgia." Use varied rhythm and a concrete claim.
33. **Conversational rhetorical openers** — "Honestly? It depends…" Fake-candid setups.
    Remove the setup.
34. **Significance inflation / promotional language** — "a pivotal moment",
    "breathtaking region", "plays a crucial role." State the plain fact; name a real
    source or cut the claim.
35. **Parenthetical asides** — shoving an explanation into parentheses
    ("caching helps (which is to say, it avoids recomputing the same value)") instead
    of just stating it. Humans fold the point into the sentence or put it right after:
    "caching avoids recomputing the same value." A parenthesis reads as "I couldn't
    decide where this belongs," which is the AI tell. Unpack the aside into the main
    clause; keep parentheses only for a true skip-able aside (a citation, a date).

## Chinese AI-isms (中文 AI 腔)

Chinese output has its own tells. Cut these:

- **值得一提 / 值得注意的是 / 值得一提的是** — fold the point into the sentence; don't
  announce it.
- **从某种意义上说 / 在某种程度上** — drop the hedge; say the qualified thing plainly.
- **综上所述 / 总而言之 / 总的来说** — end on a real take, not a recap.
- **不容忽视 / 至关重要 / 发挥着至关重要的作用 / 具有深远意义** — cut the boosterism;
  state the fact.
- **在当今…时代 / 在…的当下 / 随着…的发展** — drop the filler opener; start with the
  substance.
- **不言而喻 / 毫无疑问 / 毋庸置疑** — just say it; don't vouch for the obvious.
- **为…奠定了坚实基础 / 开启了…新篇章 / 注入了新的活力** — promotional; say what
  actually happened.
- **括号解释** —— 用括号塞补充说明（"这一点很重要（也就是说，X）"）。正常人把解释直接接在后面说，不塞进括号。把括号里的内容展开成一句话，或放在句后补充。

Before: "值得注意的是，随着人工智能的发展，这一技术发挥着至关重要的作用，不容忽视。"
After: "This technique matters, and the hype around it doesn't."

## Self-critique loop (the "obviously AI" audit)

One draft is never enough. After writing or rewriting, do a **second pass** and ask,
out loud: *"What here would only an LLM write?"* Then kill what you find.

Checklist:
1. Could any sentence have been emitted by any model with no knowledge of the topic?
   If yes, cut or rewrite it with something specific.
2. Any leftover tell from the lists above — em-dash between clauses, "delve",
   "It is worth noting", a forced three-item list, a hedge opener, a parenthetical
   aside (#35), a Chinese AI-ism?
3. Did I add anything not in the source? (See fact-preservation below.) If yes, remove
   it — that's not humanizing, that's inventing.
4. Is the voice right for the context? (See voice-by-context.) A neutral doc that I
   "gave an opinion" to is now *wrong*, not human.

Then rewrite once more to fix what the audit caught. The first pass removes the loud
tells; the audit pass removes the ones that survive a careful read.

## Fact-preservation rule (no-fabrication)

Humanizing changes *voice*, never *truth*.

- Never invent facts, names, dates, statistics, or citations that are not in the
  source text.
- Specificity (a real number, a real name) must come from the source or the author.
  If it's missing, **ask** — don't guess to make the prose "concrete."
- Do not "correct" facts or add confidence the source lacks. The Wikipedia patterns
  are about wording, not accuracy.
- If a rewrite needs a detail to land (e.g. a date in an example), mark it as a
  placeholder for the author, like the blader skill does — never fill it from memory.

## Voice by context

Not every text wants a personality. Apply the stance/opinion tells (#9) only where
voice is wanted:

- **Voice wanted** — blog, opinion, personal, marketing copy, anything addressed to a
  reader as a person. Take a stance, use first person, vary rhythm.
- **Voice not wanted** — technical docs, reference material, neutral reporting,
  academic prose. Stay neutral; *dropping* personality here is correct. Do NOT force a
  hot take into a doc that should be flat — a neutral sentence is the right call, and
  tell #9 does not apply.

This resolves the tension: the goal is *human*, which for a reference doc means
*clean and neutral*, not *opinionated*.

## Prevention — write human from scratch

- **Write to one specific person.** Picture the teammate who asked. Sound like you
  talking to them, not like a manual.
- **State an opinion** (where voice is wanted). "I'd use X here because Y" beats
  "X and Y are both valid approaches."
- **Use specifics.** Names, numbers, the actual thing. Kill "solution"/"approach".
- **Vary sentence length on purpose.** Short sentences are fine. A wall of same-length
  sentences is a tell.
- **Cut transitions that add nothing.** "Moreover" rarely earns its place.
- **For algorithm/technical writing:** show the math or code, name the tradeoff, admit
  the ugly case, and give a worked example. Don't narrate what the reader can see.

## Remediation — rewrite existing text

1. Read the text. Preserve its meaning and facts exactly; change only the voice.
2. Mark every tell instance (cite the number from the lists above).
3. Rewrite: specifics over vague nouns, active over passive, an opinion over a hedge,
   periods over em-dashes, two points over a forced three. Apply the Chinese-isms and
   additional tells where present.
4. **Fact-check:** confirm you added nothing not in the source (no-fabrication rule).
5. **Self-critique pass:** re-read and ask "what here would only an LLM write?", then
   rewrite once more to kill leftovers.
6. **Verify by reading aloud.** If it sounds like a LinkedIn post or a brochure, it
   still smells — rewrite. The test is ears, not rules.

## Output Format

For remediation, provide:
1. The rewritten text.
2. A short "changes" list mapping edits to tell numbers
   (e.g. "- #3 replaced 'delve' → 'look'; - #1 cut 'It's worth noting'; - #18 added
   the actual benchmark number; - #30 removed the 'Hope this helps!' closer").
3. A one-line note: "fact-check: no invented details" and, if read-aloud was done,
   "read aloud: no brochure tone left."

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

### Tell #30 + Chinese AI-isms (chatbot closer + 中文腔)

Before (AI-sounding):
> I hope this helps! Let me know if you have any questions. 值得注意的是，随着人工智能的发展，这一方法发挥着至关重要的作用，不容忽视。

After (humanized):
> This method works; tell me if it breaks on your data. It matters, but the hype
> around it doesn't.

Changes: #30 removed the "Hope this helps!" closer; Chinese-isms cut "值得注意的是",
"随着…的发展", "发挥着至关重要的作用", "不容忽视".

### Tell #35 (parenthetical aside)

Before (AI-sounding):
> Caching helps (which is to say, it avoids recomputing the same value), and (as a
> bonus) it also cuts memory use.

After (humanized):
> Caching avoids recomputing the same value and cuts memory use.

Changes: #35 unpacked both parenthetical asides into the main clause; no information lost.

## Pairing

This skill handles prose. For code, use `code-humanizer` (existing code) and
`code-no-slop` (writing new code). Together they cover the full "de-AI" surface:
what you say, what you write, and what you build.
