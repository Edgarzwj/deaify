#!/usr/bin/env python3
"""Behavior-preservation harness for deaify examples.

Proves the core claim of `code-humanizer`: the "humanized" rewrite is
behavior-identical to the original. Runs the standalone algorithm example and
re-checks the before/after pairs inline so a regression in the docs can't hide.
"""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def check(name, got, expected):
    assert got == expected, f"{name}: got {got!r}, expected {expected!r}"
    print(f"  ok  {name}: {got!r}")


# --- 1) standalone algorithm.py must pass on its own ---
def test_algorithm_py():
    r = subprocess.run(
        [sys.executable, str(ROOT / "examples" / "algorithm.py")],
        capture_output=True, text=True,
    )
    assert r.returncode == 0, f"algorithm.py failed:\n{r.stdout}\n{r.stderr}"
    print("  ok  examples/algorithm.py ran clean")


# --- 2) inline before/after pairs (mirror the SKILL.md examples) ---

# power / unique (#16 reinvented stdlib)
def power_before(base, exp):
    result = 1
    for _ in range(exp):
        result = result * base
    return result

def power_after(base, exp):
    return base ** exp

def unique_before(arr):
    result = []
    for x in arr:
        if x not in result:
            result.append(x)
    return result

def unique_after(items):
    return list(dict.fromkeys(items))

def sum_mod_before(data):
    MOD = 1000000007
    ans = 0
    for x in data:
        ans = (ans + x) % MOD
    return ans

def sum_mod_after(values):
    return sum(values) % 1_000_000_007


# parse_config (#10 over-engineered class -> function)
def parse_before(raw):
    import json
    class DataProcessor:
        def process(self, r):
            return json.loads(r)
    return DataProcessor().process(raw)

def parse_after(raw):
    import json
    return json.loads(raw)


def main():
    print("deaify behavior-preservation tests")
    test_algorithm_py()

    data = [3, 1, 3, 2, 2]
    big = [10**9, 10**9]

    check("power(2,10)", power_after(2, 10), power_before(2, 10))
    check("power(2,10)==1024", power_after(2, 10), 1024)
    check("unique", unique_after(data), unique_before(data))
    check("unique==[3,1,2]", unique_after(data), [3, 1, 2])
    check("sum_mod", sum_mod_after(big), sum_mod_before(big))
    check("sum_mod==999999993", sum_mod_after(big), 999999993)
    check("parse_config", parse_after('{"a":1}'), parse_before('{"a":1}'))

    print("ALL PASSED")


if __name__ == "__main__":
    main()
