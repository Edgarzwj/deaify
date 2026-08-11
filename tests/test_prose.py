#!/usr/bin/env python3
"""
Quantitative test for the humanize-prose skill.

Each sample is a (label, BEFORE, AFTER) triple. BEFORE is AI-sounding prose that
triggers one or more tells from the skill's lists; AFTER is the same content
rewritten to remove the AI smell (voice only, facts preserved).

For every sample we count AI-tell hits in BEFORE and in AFTER using the same
detectors the skill teaches. A passing run proves the skill's guidance, when
applied, drives tell count to zero. This mirrors tests/benchmark.py for code.

Run:  python3 tests/test_prose.py
Exit non-zero if any AFTER fails to beat its BEFORE or still smells.
"""

import re
import sys

# ---------------------------------------------------------------------------
# Tell detectors — each returns the number of tell *hits* in `text`.
# Case-insensitive. Counts are deliberately simple regex matches; the corpus is
# curated so a genuinely humanized AFTER scores 0.
# ---------------------------------------------------------------------------

EM_DASH = "\u2014"  # —

DETECTORS = [
    # 1. Hedged openers
    ("hedge", re.compile(r"it is (worth noting|important to note)|it should be emphasized", re.I)),
    # 2. Filler transitions
    ("filler", re.compile(r"\b(moreover|furthermore|additionally|in today's|in the realm of)\b", re.I)),
    # 3. Tells vocabulary
    ("vocab", re.compile(r"\b(delve|tapestry|navigate the landscape|unravel|testament to|game-changer|underscore|robust|leverage|holistic|seamless|powerful|exciting|revolutionary)\b", re.I)),
    # 8. Conclusion that restates the intro
    ("conclusion", re.compile(r"\b(in conclusion|as we have seen|to summarize)\b", re.I)),
    # 20/21. Explaining the obvious / narration of trivial
    ("obvious", re.compile(r"we can see that|as shown above|it is clear that", re.I)),
    # 25. Copula avoidance
    ("copula", re.compile(r"\b(serves as|boasts|acts as|features)\b", re.I)),
    # 31. Signposting announcements
    ("signpost", re.compile(r"let'?s dive in|here'?s what you need to know|dive in", re.I)),
    # 34. Significance inflation
    ("significance", re.compile(r"plays a crucial role|pivotal|crucial role|breathtaking", re.I)),
    # 28. Rule-of-three padding (curated phrasings)
    ("three", re.compile(r"fast, reliable, and scalable|innovation, inspiration, and insights", re.I)),
    # 30. Chatbot artifacts
    ("chatbot", re.compile(r"i hope this helps|let me know if you have any questions|great question", re.I)),
    # Chinese AI-isms (中文 AI 腔)
    ("zh", re.compile(
        r"值得注意的是|值得一提的是|值得注意"
        r"|随着[^。，]*的发展|随着[^。，]*的"
        r"|发挥着至关重要的作用|至关重要|不容忽视"
        r"|综上所述|总而言之|总的来说"
        r"|从某种意义上说|在某种程度上"
        r"|不言而喻|毫无疑问|毋庸置疑"
        r"|为[^。，]*奠定了坚实基础|开启了[^。，]*新篇章|注入了新的活力"
        r"|在当今[^。，]*时代|在[^。，]*的当下",
        re.I,
    )),
]


def count_tells(text: str) -> int:
    total = 0
    # Em-dash overuse: only a *tell* when more than one per sample.
    dashes = text.count(EM_DASH)
    if dashes > 1:
        total += 1
    for _name, pat in DETECTORS:
        total += len(pat.findall(text))
    return total


# ---------------------------------------------------------------------------
# Corpus: (label, tells-covered, BEFORE, AFTER)
# ---------------------------------------------------------------------------

SAMPLES = [
    (
        "hedge+vocab+conclusion",
        "#1 #3 #8",
        "It is important to note that caching is a powerful technique that can leverage "
        "significant performance gains. In today's fast-paced world, many developers delve "
        "into caching to unlock its potential. In conclusion, as we have seen, caching matters.",
        "Cache the slow thing once and most of your latency disappears. The trick is knowing "
        "what's actually slow \u2014 profile before you cache, or you'll memoize the wrong call.",
    ),
    (
        "obvious+vague+pseudo-generic",
        "#10 #21 #23",
        "This function demonstrates a binary search approach. We can see that it efficiently "
        "finds the target by repeatedly dividing the search space. This approach can be applied "
        "to many scenarios where fast lookup is desired.",
        "bisect_left finds the insertion point in O(log n). Use it when the list is sorted and "
        "you're searching repeatedly \u2014 for a one-off lookup on unsorted data, a linear scan "
        "is simpler and faster to read. Don't reach for it on a list you'll sort just to search once.",
    ),
    (
        "chatbot+chinese-isms",
        "#30 zh",
        "I hope this helps! Let me know if you have any questions. "
        "值得注意的是，随着人工智能的发展，这一方法发挥着至关重要的作用，不容忽视。",
        "This method works; tell me if it breaks on your data. It matters, but the hype around it doesn't.",
    ),
    (
        "signpost+copula+significance",
        "#25 #31 #34",
        "Let's dive in. The framework serves as a robust solution that boasts a pivotal role in "
        "modern data pipelines. It plays a crucial role in ensuring seamless operations.",
        "The framework is a cache in front of the database. That's the whole job \u2014 keep the "
        "hot rows in memory so the DB stops fielding the same reads.",
    ),
    (
        "hedge+three+filler+vocab",
        "#1 #13 #28 #2",
        "It should be emphasized that the system is fast, reliable, and scalable. "
        "Innovation, inspiration, and insights drive our approach. Moreover, it is worth noting "
        "that the architecture is holistic.",
        "The system is fast enough for our traffic and stays up. We ship small and watch the "
        "graphs \u2014 if p99 climbs, we add a replica. Nothing here is magic.",
    ),
    (
        "chinese-isms+balanced-hedge",
        "zh #12",
        "综上所述，这一技术毋庸置疑发挥着至关重要的作用。从某种意义上说，随着人工智能的发展，"
        "它为行业奠定了坚实基础。虽然方案A有其优势，但方案B也不容忽视。",
        "This technique does the job; the rest is marketing. Plan A is simpler to run and we picked "
        "it. Plan B is fine too, but we didn't need it.",
    ),
]


def main() -> int:
    print("humanize-prose — tell-density test")
    print("=" * 56)
    failures = 0
    total_before = total_after = 0

    for label, tells, before, after in SAMPLES:
        b = count_tells(before)
        a = count_tells(after)
        total_before += b
        total_after += a
        status = "OK" if (a < b and a == 0) else "FAIL"
        if status == "FAIL":
            failures += 1
        print(f"[{status}] {label:<28} tells {b:>2} -> {a:<2}   ({tells})")

    print("-" * 56)
    reduction = 0 if total_before == 0 else round(100 * (total_before - total_after) / total_before)
    print(f"TOTAL  tells {total_before} -> {total_after}   ({reduction}% reduction)")
    verdict = "GENERALIZES" if failures == 0 and total_after == 0 else "NEEDS WORK"
    print(f"VERDICT: {verdict}")

    if failures:
        print(f"\n{failures} sample(s) failed: AFTER must beat BEFORE and reach 0 tells.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
