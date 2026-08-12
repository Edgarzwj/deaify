#!/usr/bin/env python3
"""
Third-party AI-text-detector endorsement harness (gap #7).

Runs BEFORE/AFTER prose samples from tests/test_prose.SAMPLES through real
external AI detectors (GPTZero / Sapling / Writer) and reports the AI-probability
drop after humanizing. A bigger drop = stronger third-party endorsement that
the skill actually removes AI smell.

Keys come from the environment (never hard-coded):
  GPTZERO_API_KEY    -> https://gptzero.me  (v2 documents endpoint)
  SAPLING_API_KEY    -> https://sapling.ai  (v1/aidetect)
  WRITER_API_KEY     -> https://writer.com  (v1/trust)

Run with no keys:
  python3 tests/third_party_detector.py
  -> prints "SKIP (no API key)" and exits 0 (CI stays green).

Run with a key (e.g. GPTZero):
  GPTZERO_API_KEY=xxx python3 tests/third_party_detector.py
  -> prints per-sample AI-probability before/after and the reduction.

Pure stdlib (urllib). Network/API errors are reported but do not fail the run,
since the harness validates wiring, not the upstream service's availability.
"""

import json
import os
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from test_prose import SAMPLES  # (label, tells, before, after)


def _post(url, headers, payload):
    data = json.dumps(payload).encode()
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())


def _gptzero(text, key):
    out = _post(
        "https://api.gptzero.me/v2/text/documents",
        {"X-Api-Key": key, "Content-Type": "application/json"},
        {"document": text},
    )
    # v2 nests per-document; fall back across known shapes.
    if isinstance(out, dict):
        if "ai_probability" in out:
            return float(out["ai_probability"])
        if "results" in out and out["results"]:
            return float(out["results"][0].get("completely_generated_probability", 0.0))
    return float(out.get("ai_probability", 0.0))


def _sapling(text, key):
    out = _post(
        "https://api.sapling.ai/v1/aidetect",
        {"Content-Type": "application/json"},
        {"key": key, "text": text},
    )
    return float(out.get("score", 0.0))


def _writer(text, key):
    out = _post(
        "https://api.writer.com/v1/trust",
        {"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        {"text": text},
    )
    return float(out.get("score", 0.0))


DETECTORS = {
    "GPTZero": (lambda k: (lambda t: _gptzero(t, k))),
    "Sapling": (lambda k: (lambda t: _sapling(t, k))),
    "Writer":  (lambda k: (lambda t: _writer(t, k))),
}


def configured():
    out = {}
    for name in DETECTORS:
        env = f"{name.upper()}_API_KEY"
        if os.environ.get(env):
            out[name] = DETECTORS[name](os.environ[env])
    return out


def main():
    active = configured()
    if not active:
        print("SKIP (no third-party API key in env).")
        print("Set GPTZERO_API_KEY / SAPLING_API_KEY / WRITER_API_KEY to endorse.")
        print("EXIT 0")
        return

    print(f"Third-party AI-detector endorsement ({len(active)} detector(s) active)\n")
    total_red = 0.0
    n = 0
    for name, fn in active.items():
        print(f"== {name} (AI-probability, lower = more human) ==")
        for label, _tells, before, after in SAMPLES:
            try:
                b = fn(before)
                a = fn(after)
                red = (1 - a / b) * 100 if b > 0 else 0.0
                total_red += red
                n += 1
                print(f"  {label:28} {b:5.2f} -> {a:5.2f}  ({red:5.0f}% lower)")
            except Exception as e:  # network/auth/env issue, not a skill failure
                print(f"  {label:28} ERROR: {e}")
        print()

    if n:
        avg = total_red / n
        print(f"Average AI-probability reduction: {avg:.0f}%")
        verdict = "ENDORSED" if avg >= 30 else "WEAK"
        print(f"Verdict: {verdict}")
    print("DONE")


if __name__ == "__main__":
    main()
