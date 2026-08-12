#!/usr/bin/env python3
"""AST smell test: confirm code-humanizer removes structural smells (gap #3).

Runs the AST detectors on examples/algorithm.py BEFORE/AFTER and asserts the
AFTER block has zero structural smells and the reduction is 100%.

Run:  python3 tests/test_ast.py
Exit non-zero if AFTER still smells or reduction < 100%.
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

from ast_smells import detect
from benchmark import extract_blocks


def main():
    text = (ROOT / "examples" / "algorithm.py").read_text(encoding="utf-8")
    before, after = extract_blocks(text)
    sb = detect(before)
    sa = detect(after)
    tb = sum(sb.values())
    ta = sum(sa.values())

    print("AST smell test (examples/algorithm.py)\n")
    for k in sb:
        ok = sb[k] >= sa[k]
        print(f"  {k:22} {sb[k]:>3} -> {sa[k]:<3}  [{'OK' if ok else 'FAIL'}]")
    red = (1 - ta / tb) * 100 if tb else 0.0
    print(f"\n  TOTAL {tb} -> {ta}  ({red:.0f}% reduction)")

    assert tb > 0, "BEFORE had no structural smells detected (corpus drift?)"
    assert ta == 0, f"AFTER still has structural smells: {sa}"
    assert red == 100.0, f"reduction {red:.0f}% < 100%"
    print("AST verdict: EFFECTIVE (100% structural smells removed)")
    print("PASS")


if __name__ == "__main__":
    main()
