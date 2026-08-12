#!/usr/bin/env python3
"""Multi-language corpus regression test (gap #8).

Loads examples/corpus/{py,ts,go}/*.before.* and *.after.* pairs and confirms
every humanized AFTER has strictly fewer smells than its BEFORE, and the AFTER
is clean (0 smells). Python uses the true AST detectors (ast_smells); TypeScript
and Go use regex detectors (their AST needs tree-sitter, out of scope here).

Run:  python3 tests/test_corpus.py
Exit non-zero if any AFTER fails to beat its BEFORE or still smells.
"""

import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

from ast_smells import detect as detect_py

NARRATION_RE = re.compile(
    r"\biterate\b|\bincrement\b|\bthis function\b|\bcalculates?\b|"
    r"\bremoves? duplicate|\bfetches? the\b|\bhere we\b|\bnow we\b|"
    r"\bwe (need to|must|can)\b|\bsimply\b|\bin order to\b", re.I)

TS_DETECTORS = {
    "magic_const": re.compile(r"\b\d{6,}\b"),
    "generic_names": re.compile(r"\b(arr|ans|tmp|data|result|res)\b"),
    "vacuous_error": re.compile(r"An error occurred"),
    "generic_class": re.compile(r"class \w+(Utility|Helper|Manager|Processor)"),
    "narration_comment": NARRATION_RE,
    "reinvented_pow": re.compile(r"result\s*=\s*result\s*\*\s*base"),
    "reinvented_unique": re.compile(r"\.indexOf\([^)]*\)\s*===\s*-1"),
    "defensive_deepcopy": re.compile(r"JSON\.parse\(JSON\.stringify"),
}

GO_DETECTORS = {
    "magic_const": re.compile(r"\b\d{6,}\b"),
    "generic_names": re.compile(r"\b(arr|ans|tmp|data|result|res)\b"),
    "vacuous_error": re.compile(r"An error occurred"),
    "generic_class": re.compile(r"type \w+(Utility|Helper|Manager|Processor) struct"),
    "narration_comment": NARRATION_RE,
    "reinvented_pow": re.compile(r"result\s*\*=\s*base"),
    "reinvented_unique": re.compile(r"append\(result"),
    "defensive_deepcopy": re.compile(r"json\.Marshal"),
}


def detect_regex(code, dets):
    return {name: len(d.findall(code)) for name, d in dets.items()}


def load_pairs():
    pairs = []
    for lang, ext in (("py", "py"), ("ts", "ts"), ("go", "go")):
        d = ROOT / "examples" / "corpus" / lang
        befores = sorted(d.glob(f"*.before.{ext}"))
        for b in befores:
            a = b.with_name(b.name.replace(".before.", ".after."))
            pairs.append((lang, b.stem.replace(".before", ""), b, a))
    return pairs


def score(lang, code):
    if lang == "py":
        return detect_py(code)
    dets = TS_DETECTORS if lang == "ts" else GO_DETECTORS
    return detect_regex(code, dets)


def main():
    pairs = load_pairs()
    assert pairs, "no corpus pairs found"
    print(f"deaify multi-language corpus regression ({len(pairs)} pairs)\n")

    tot_b = tot_a = 0
    failures = []
    for lang, name, bpath, apath in pairs:
        before = bpath.read_text(encoding="utf-8")
        after = apath.read_text(encoding="utf-8")
        sb = score(lang, before)
        sa = score(lang, after)
        tb = sum(sb.values())
        ta = sum(sa.values())
        tot_b += tb
        tot_a += ta
        ok = (ta == 0 and tb > 0)
        if not ok:
            failures.append((lang, name, tb, ta))
        print(f"  [{lang}] {name:12} smells {tb:>3} -> {ta:<3}  [{'OK' if ok else 'FAIL'}]")

    red = (1 - tot_a / tot_b) * 100 if tot_b else 0.0
    print(f"\n  TOTAL smells {tot_b} -> {tot_a}  ({red:.0f}% reduction)")

    assert tot_b > 0, "corpus had no smells detected"
    assert tot_a == 0, f"AFTER blocks still smell: {failures}"
    assert red == 100.0, f"reduction {red:.0f}% < 100%"
    verdict = "GENERALIZES" if red >= 70 else "CHECK"
    print(f"Verdict: {verdict} (AST for py, regex for ts/go)")
    print("PASS")


if __name__ == "__main__":
    main()
