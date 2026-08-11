#!/usr/bin/env python3
"""Smell-density benchmark for deaify (code-humanizer).

Measures the skill's *effectiveness*, not just correctness: given an
AI-sounding BEFORE sample and its humanized AFTER, how many AI-smell
signals remain? A good remediation skill should drive this number down.

This is a lightweight, regex/string-based detector — good enough to track
trend over versions, not a substitute for a real linter or human review.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SAMPLE = ROOT / "examples" / "algorithm.py"


def extract_blocks(text):
    lines = text.splitlines()
    before, after, mode = [], [], None
    for ln in lines:
        if "BEFORE (AI-sounding)" in ln:
            mode = "before"
        elif "AFTER (humanized)" in ln:
            mode = "after"
        elif "VERIFY" in ln:
            mode = None
        elif mode == "before":
            before.append(ln)
        elif mode == "after":
            after.append(ln)
    return "\n".join(before), "\n".join(after)


# --- detectors: each returns an int count of smell signals in `code` ---

def d_reinvented_stdlib(code):
    # hand-rolled pow loop: `result = result * base` inside a for
    return len(re.findall(r"result\s*=\s*result\s*\*\s*base", code))

def d_unnamed_magic_const(code):
    # the bare MOD number without digit separators
    return len(re.findall(r"\b1000000007\b", code))

def d_narration_comment(code):
    pats = [r"iterate", r"increment", r"this function", r"calculates", r"removes duplicate"]
    cnt = 0
    for ln in code.splitlines():
        if "#" in ln:
            comment = ln.split("#", 1)[1]  # only the comment portion
            cnt += sum(1 for p in pats if re.search(p, comment, re.I))
    return cnt

def d_generic_names(code):
    # whole-word generic identifiers that carry no meaning
    return len(re.findall(r"\b(arr|ans|tmp|data|result)\b", code))

def d_single_method_class(code):
    # a class whose only real method is a thin wrapper (over-abstraction)
    return len(re.findall(r"class\s+\w+.*?def sort_data", code, re.S))

def d_vacuous_except(code):
    return len(re.findall(r'except\s+Exception.*?print\("An error occurred"\)', code, re.S))


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


def main():
    before, after = extract_blocks(SAMPLE.read_text(encoding="utf-8"))
    sb, sa = score(before), score(after)

    print("deaify smell-density benchmark (examples/algorithm.py)\n")
    print(f"{'smell':28} {'BEFORE':>8} {'AFTER':>8} {'Δ':>6}")
    print("-" * 52)
    tot_b = tot_a = 0
    for name in DETECTORS:
        b, a = sb[name], sa[name]
        tot_b += b
        tot_a += a
        arrow = "↓" if a < b else ("=" if a == b else "↑")
        print(f"{name:28} {b:>8} {a:>8} {arrow:>6}")
    print("-" * 52)
    print(f"{'TOTAL':28} {tot_b:>8} {tot_a:>8}")

    reduction = (1 - tot_a / tot_b) * 100 if tot_b else 0.0
    print(f"\nSmell-density reduction: {reduction:.0f}%  ({tot_b} → {tot_a} signals)")
    verdict = "EFFECTIVE" if reduction >= 70 else ("PARTIAL" if reduction >= 30 else "WEAK")
    print(f"Verdict: {verdict}")


if __name__ == "__main__":
    main()
