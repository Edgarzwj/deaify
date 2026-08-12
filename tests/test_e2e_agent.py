#!/usr/bin/env python3
"""End-to-end agent remediation test (gap #4).

Proves the real workflow, not a synthetic one: a capable agent (the LLM that
runs this repo's skills) reads `code-humanizer`'s SKILL.md, rewrites an UNSEEN
AI-smelling snippet, and the output is verified to be (a) smell-free under the
AST detector and (b) behavior-preserving against the original.

The BEFORE/AFTER pair under examples/e2e/ was produced by the agent following
the skill; this test locks the result so a regression is caught in CI. To run
a fresh end-to-end pass, delete examples/e2e/agent_after.py and have an agent
regenerate it from agent_before.py + the skill, then re-run this test.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tests"))
from ast_smells import detect, total  # noqa: E402

E2E = ROOT / "examples" / "e2e"
BEFORE = (E2E / "agent_before.py").read_text(encoding="utf-8")
AFTER = (E2E / "agent_after.py").read_text(encoding="utf-8")


def load(src):
    ns = {}
    exec(compile(src, "<e2e>", "exec"), ns)
    return ns


def main():
    # 1) Smell gate — the agent rewrite must drive every count to 0.
    before_smells = total(BEFORE)
    after_smells = total(AFTER)
    print("BEFORE smells:", before_smells, detect(BEFORE))
    print("AFTER  smells:", after_smells, detect(AFTER))
    assert before_smells > 0, "expected the input to contain AI smells"
    assert after_smells == 0, f"agent rewrite must be clean, got {detect(AFTER)}"

    # 2) Behavior preservation — identical outputs, including edge cases.
    b = load(BEFORE)
    a = load(AFTER)

    modpow_cases = [(2, 10, 1000), (3, 3, 5), (5, 0, 7), (2, 100, 1_000_000_007)]
    for base, exp, mod in modpow_cases:
        got = b["MathHelper"]().mod_pow(base, exp, mod)
        want = a["mod_pow"](base, exp, mod)
        assert got == want, f"mod_pow{base, exp, mod}: {got} != {want}"

    hash_cases = [[2, 3, 4], [], [10**9, 10**9], [7], [1, 1, 1, 1]]
    for vals in hash_cases:
        got = b["secure_hash"](vals)
        want = a["secure_hash"](vals)
        assert got == want, f"secure_hash({vals}): {got} != {want}"

    print("E2E OK: agent-driven rewrite is smell-free AND behavior-preserving.")


if __name__ == "__main__":
    main()
