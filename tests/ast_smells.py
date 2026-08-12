#!/usr/bin/env python3
"""AST-based code-smell detectors for deaify (code-humanizer).

Supersedes the regex detectors in benchmark.py for *structural* smells that
text matching gets wrong:

  - magic constants written without digit separators (or bare, un-named)
  - reinvented stdlib: manual `pow` loop, manual dedup loop
  - over-abstracted single-method class (a class wrapping one trivial call)
  - generic / buzzword class names (Utility, Helper, Manager, ...)
  - vacuous error handling (bare except returning -1 / "An error occurred")
  - defensive deepcopy that the context does not need
  - generic variable names (arr, ans, tmp, data, result, ...)
  - narration comments that restate the code

Comments are not part of the AST, so narration comments are caught with the
`tokenize` module instead. Everything here is pure stdlib (ast, tokenize) so
it runs in CI with no dependencies.

A good remediation drives every count to 0.
"""

import ast
import io
import re
import tokenize

GENERIC_NAMES = {"arr", "ans", "tmp", "data", "result", "res", "val", "obj", "buf", "cnt"}
GENERIC_CLASS_SUFFIX = ("Utility", "Helper", "Manager", "Processor", "Handler", "Wrapper", "Base")

# Narration-comment tells (mirrors the prose "obvious"/"narration" tells).
NARRATION_PATTERNS = [
    r"\biterate\b", r"\bincrement\b", r"\bthis function\b", r"\bcalculates?\b",
    r"\bremoves? duplicate", r"\bfetches? the\b", r"\bhere we\b", r"\bnow we\b",
    r"\bwe (need to|must|can)\b", r"\bsimply\b", r"\bin order to\b",
]


def _narration_comments(source):
    cnt = 0
    try:
        toks = tokenize.generate_tokens(io.StringIO(source).readline)
    except Exception:
        return 0
    pats = [re.compile(p, re.I) for p in NARRATION_PATTERNS]
    for tok in toks:
        if tok.type == tokenize.COMMENT:
            if any(p.search(tok.string) for p in pats):
                cnt += 1
    return cnt


def detect(source):
    """Return a dict of smell-name -> hit count for the given Python source."""
    counts = {
        "magic_const": 0,
        "reinvented_pow": 0,
        "reinvented_unique": 0,
        "single_method_class": 0,
        "generic_class": 0,
        "vacuous_except": 0,
        "defensive_deepcopy": 0,
        "generic_names": 0,
        "narration_comment": 0,
    }
    try:
        tree = ast.parse(source)
    except SyntaxError:
        # Not valid Python (e.g. a TS/Go block leaked in) -> no AST smells.
        return counts

    for node in ast.walk(tree):
        # --- generic variable names (Load contexts only) ---
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
            if node.id in GENERIC_NAMES:
                counts["generic_names"] += 1

        # --- magic constants: int >= 1000, >=4 digits, no digit separator ---
        if isinstance(node, ast.Constant) and isinstance(node.value, int):
            if abs(node.value) >= 1000 and len(str(abs(node.value))) >= 4:
                seg = ast.get_source_segment(source, node) or ""
                if "_" not in seg:
                    counts["magic_const"] += 1

        # --- class-level smells ---
        if isinstance(node, ast.ClassDef):
            if node.name.endswith(GENERIC_CLASS_SUFFIX):
                counts["generic_class"] += 1
            methods = [
                n for n in node.body
                if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
                and not n.name.startswith("__")
            ]
            if len(methods) == 1:
                m = methods[0]
                if len(m.body) == 1 and isinstance(m.body[0], ast.Return) and \
                        isinstance(m.body[0].value, (ast.Call, ast.BinOp)):
                    counts["single_method_class"] += 1

        # --- vacuous error handling ---
        if isinstance(node, ast.Try):
            for h in node.handlers:
                for sub in h.body:
                    # `return -1` / `return None` style
                    if isinstance(sub, ast.Return) and (
                        sub.value is None
                        or isinstance(sub.value, ast.Constant)
                        or (isinstance(sub.value, ast.UnaryOp)
                            and isinstance(sub.value.operand, ast.Constant))
                    ):
                        counts["vacuous_except"] += 1
                    # `print("An error occurred")` style
                    if isinstance(sub, ast.Expr) and isinstance(sub.value, ast.Call):
                        fn = sub.value.func
                        if isinstance(fn, ast.Name) and fn.id in ("print", "logging"):
                            for a in sub.value.args:
                                if isinstance(a, ast.Constant) and isinstance(a.value, str) \
                                        and ("error" in a.value.lower()
                                             or "occurred" in a.value.lower()
                                             or "exception" in a.value.lower()):
                                    counts["vacuous_except"] += 1

        # --- defensive deepcopy ---
        if isinstance(node, ast.ImportFrom) and node.module == "copy":
            if any(a.name == "deepcopy" for a in node.names):
                counts["defensive_deepcopy"] += 1
        if isinstance(node, ast.Import):
            if any(a.name == "copy" for a in node.names):
                counts["defensive_deepcopy"] += 1

        # --- reinvented stdlib: manual pow loop ---
        if isinstance(node, ast.For):
            for sub in node.body:
                if isinstance(sub, ast.AugAssign) and isinstance(sub.op, ast.Mult):
                    counts["reinvented_pow"] += 1
                elif isinstance(sub, ast.Assign) and isinstance(sub.value, ast.BinOp) \
                        and isinstance(sub.value.op, ast.Mult):
                    counts["reinvented_pow"] += 1
                # reinvented unique: `if x not in acc: acc.append(x)`
                for sub2 in node.body:
                    if isinstance(sub2, ast.If) and isinstance(sub2.test, ast.Compare) \
                            and isinstance(sub2.test.ops[0], ast.NotIn):
                        for s3 in sub2.body:
                            if isinstance(s3, ast.Expr) and isinstance(s3.value, ast.Call):
                                fn = s3.value.func
                                if isinstance(fn, ast.Attribute) and fn.attr == "append":
                                    counts["reinvented_unique"] += 1

    counts["narration_comment"] = _narration_comments(source)
    return counts


def total(source):
    return sum(detect(source).values())


if __name__ == "__main__":
    import sys
    from pathlib import Path
    src = Path(sys.argv[1]).read_text(encoding="utf-8") if len(sys.argv) > 1 else ""
    res = detect(src)
    for k, v in res.items():
        if v:
            print(f"{k:22} {v}")
    print("TOTAL", sum(res.values()))
