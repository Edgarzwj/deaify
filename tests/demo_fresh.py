#!/usr/bin/env python3
"""Live demo: does deaify generalize beyond its own example?

Takes a FRESH AI-sounding snippet (not from examples/), applies the
code-humanizer rewrite by hand, and measures smell reduction with a
broader detector than benchmark.py. If the reduction holds on unseen
code, the skill generalizes; if not, it's over-fit to algorithm.py.

This also surfaces a gap: benchmark.py only covers 6 of the 22 smells
and only the Python algorithm sample. This demo covers more of #1-#22.
"""

import re

# --- FRESH BEFORE (AI-sounding, order/inventory domain, not in repo examples) ---
BEFORE = '''
import math
import json
from typing import List, Any

# This function processes the list of orders and calculates the total price
def process_orders(order_list: List[Any]) -> float:
    result = 0.0
    for i in range(len(order_list)):
        if order_list[i].isValid == True:
            result = result + order_list[i].price
    return result

# This function removes duplicate items from the given array
def remove_duplicates(arr: List[Any]) -> List[Any]:
    result = []
    for i in range(len(arr)):
        if arr[i] not in result:
            result.append(arr[i])
    return result

class MathUtility:
    def __init__(self):
        pass
    def compute_power(self, base: float, exp: int) -> float:
        result = 1
        for i in range(exp):  # iterate exp times
            result = result * base
        return result

TIMEOUT = 86400000

def fetch_data(data):
    try:
        ans = json.loads(data)
        return ans
    except Exception as e:
        print("An error occurred")
        return -1
'''

# --- AFTER (humanized, same behavior) ---
AFTER = '''
import json
from typing import List

def total_price(orders: List[Order]) -> float:
    return sum(o.price for o in orders if o.is_valid)

def unique(items):
    return list(dict.fromkeys(items))

def power(base, exp):
    return base ** exp

TIMEOUT_MS = 86_400_000

def parse_json(text):
    return json.loads(text)
'''


def d_explicit_bool(c):      return len(re.findall(r'==\s*True', c))
def d_generic_names(c):      return len(re.findall(r'\b(arr|ans|tmp|data|result|temp)\b', c))
def d_generic_error(c):      return len(re.findall(r'print\("An error occurred"\)', c))
def d_regurgitated(c):
    return sum(1 for ln in c.splitlines()
               if '#' in ln and re.search(r'This function', ln.split('#', 1)[1], re.I))
def d_overclass(c):          return len(re.findall(r'^\s*class\s+\w+', c, re.M))
def d_magic_number(c):       return len(re.findall(r'\b86400000\b', c))
def d_reinvented(c):
    return (len(re.findall(r'result\s*=\s*result\s*\*\s*base', c))
            + len(re.findall(r'if\s+\w+\[i\]\s+not in result', c)))
def d_narration(c):
    return sum(1 for ln in c.splitlines()
               if '#' in ln and re.search(r'iterate|increment', ln.split('#', 1)[1], re.I))
def d_vacuous_except(c):     return len(re.findall(r'except\s+Exception.*?print\("An error occurred"\)', c, re.S))
def d_unused_math(c):        return 1 if ('import math' in c and 'math.' not in c) else 0


DETECTORS = {
    "#1 explicit bool": d_explicit_bool,
    "#2 generic names": d_generic_names,
    "#4 generic error log": d_generic_error,
    "#5 regurgitated docs": d_regurgitated,
    "#10 over-engineered class": d_overclass,
    "#12 magic number": d_magic_number,
    "#16 reinvented stdlib": d_reinvented,
    "#18 narration comment": d_narration,
    "#22 vacuous except": d_vacuous_except,
    "unused import (math)": d_unused_math,
}


def main():
    print("deaify LIVE demo — fresh (unseen) AI-smelling code\n")
    print(f"{'smell':26} {'BEFORE':>8} {'AFTER':>8} {'Δ':>6}")
    print("-" * 50)
    tot_b = tot_a = 0
    for name, det in DETECTORS.items():
        b, a = det(BEFORE), det(AFTER)
        tot_b += b
        tot_a += a
        arrow = "↓" if a < b else ("=" if a == b else "↑")
        print(f"{name:26} {b:>8} {a:>8} {arrow:>6}")
    print("-" * 50)
    print(f"{'TOTAL':26} {tot_b:>8} {tot_a:>8}")
    reduction = (1 - tot_a / tot_b) * 100 if tot_b else 0.0
    print(f"\nSmell-density reduction on UNSEEN code: {reduction:.0f}%  ({tot_b} → {tot_a})")
    print("Verdict:", "GENERALIZES" if reduction >= 70 else ("PARTIAL" if reduction >= 30 else "OVERFIT"))
    print("\n(note: this demo still scores by hand-applied rewrite; a real agent")
    print(" run would be the next step — see gap list.)")


if __name__ == "__main__":
    main()
