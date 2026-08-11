#!/usr/bin/env python3
"""Smell-density + conciseness benchmark for deaify (code-humanizer).

Measures *effectiveness*, not just correctness: given an AI-sounding BEFORE
sample and its humanized AFTER, how many AI-smell signals remain, and how many
lines did the rewrite shed? A good remediation skill drives both numbers down.

Cross-language (Python / TypeScript / Go). The detectors are lightweight
regex/string checks — fine for tracking trend across versions, not a substitute
for a real linter or human review.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SAMPLES = [
    ("Python", "py", ROOT / "examples" / "algorithm.py"),
    ("TypeScript", "ts", ROOT / "examples" / "web.ts"),
    ("Go", "go", ROOT / "examples" / "algorithm.go"),
]


def extract_blocks(text):
    before, after, mode = [], [], None
    for ln in text.splitlines():
        if "BEFORE (AI-sounding)" in ln:
            mode = "before"
        elif "AFTER (humanized)" in ln:
            mode = "after"
        elif "VERIFY" in ln or "func main" in ln or "__name__" in ln:
            # stop the AFTER block before test/main scaffolding leaks in
            mode = None
        elif mode == "before":
            before.append(ln)
        elif mode == "after":
            after.append(ln)
    return "\n".join(before), "\n".join(after)


# --- detectors: each returns an int count of smell signals in `code` ---

def d_reinvented_stdlib(code):
    # hand-rolled pow loop: `result = result * base`
    return len(re.findall(r"result\s*=\s*result\s*\*\s*base", code))

def d_unnamed_magic_const(code):
    # bare MOD / ms constants without digit separators or a name
    return len(re.findall(r"\b1000000007\b|\b86400000\b", code))

def d_narration_comment(code):
    pats = [r"iterate", r"increment", r"this function", r"calculates",
            r"removes duplicate", r"fetches the user"]
    cnt = 0
    for ln in code.splitlines():
        if "#" in ln:
            comment = ln.split("#", 1)[1]
        elif "//" in ln:
            comment = ln.split("//", 1)[1]
        else:
            continue
        cnt += sum(1 for p in pats if re.search(p, comment, re.I))
    return cnt

def d_generic_names(code):
    return len(re.findall(r"\b(arr|ans|tmp|data|result)\b", code))

def d_single_method_class(code):
    return len(re.findall(r"class\s+\w+.*?def sort_data", code, re.S))

def d_vacuous_except(code):
    # identical boilerplate message in both Python and TS samples
    return len(re.findall(r"An error occurred", code))


DETECTORS = {
    "#16 reinvented stdlib": d_reinvented_stdlib,
    "#17 unnamed magic const": d_unnamed_magic_const,
    "#18 narration comment": d_narration_comment,
    "#2  generic names": d_generic_names,
    "#20 single-method class": d_single_method_class,
    "#22 vacuous except": d_vacuous_except,
}


def score(code):
    return {name: det(code) for name, det in DETECTORS.items()}


def loc(code, lang):
    """Count code lines: drop blanks and pure-comment lines."""
    n = 0
    for ln in code.splitlines():
        s = ln.strip()
        if not s:
            continue
        if lang == "py" and s.startswith("#"):
            continue
        if lang in ("ts", "go") and s.startswith("//"):
            continue
        n += 1
    return n


def main():
    print("deaify smell-density + conciseness benchmark\n")
    tot_b = tot_a = loc_b = loc_a = 0

    for name, lang, path in SAMPLES:
        before, after = extract_blocks(path.read_text(encoding="utf-8"))
        sb, sa = score(before), score(after)
        lb, la = loc(before, lang), loc(after, lang)
        tb, ta = sum(sb.values()), sum(sa.values())
        tot_b += tb; tot_a += ta; loc_b += lb; loc_a += la

        red = (1 - ta / tb) * 100 if tb else 0.0
        lred = (1 - la / lb) * 100 if lb else 0.0
        verdict = "EFFECTIVE" if red >= 70 else ("PARTIAL" if red >= 30 else "WEAK")
        print(f"== {name} ({path.name}) ==")
        print(f"  smell signals : {tb:>3} -> {ta:<3}  ({red:>5.0f}% reduction)  [{verdict}]")
        print(f"  code lines    : {lb:>3} -> {la:<3}  ({lred:>5.0f}% shorter)")

    print()
    sred = (1 - tot_a / tot_b) * 100 if tot_b else 0.0
    lred = (1 - loc_a / loc_b) * 100 if loc_b else 0.0
    print(f"TOTAL smell signals : {tot_b} -> {tot_a}  ({sred:.0f}% reduction)")
    print(f"TOTAL code lines    : {loc_b} -> {loc_a}  ({lred:.0f}% shorter)")
    verdict = "GENERALIZES" if sred >= 70 and lred > 0 else "CHECK"
    print(f"Verdict: {verdict}")


if __name__ == "__main__":
    main()
