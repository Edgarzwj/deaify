#!/usr/bin/env python3
"""
Regenerate the multi-agent adapter files from the three skills/ SKILL.md files.

Adapters are plain-text copies of the skills so non-WorkBuddy agents
(AGENTS.md, Cursor, Qoder, Windsurf, Claude) get the same de-AI rules. They are
*generated*, not hand-edited: edit the skills, then re-run this script.

Run:  python3 gen_adapters.py
"""

import os

ROOT = os.path.dirname(os.path.abspath(__file__))
SKILLS = ["code-no-slop", "code-humanizer", "humanize-prose"]
NOTE = "> Generated from skills/. Edit the skills, then re-run gen_adapters.py."

# (relative output path, file header written before the first skill block)
ADAPTERS = {
    "AGENTS.md": "# deaify \u2014 Agent Rules\n\n",
    ".claude/CLAUDE.md": "# deaify \u2014 Project Rules\n\n",
    ".qoder/rules/deaify.md": "# deaify \u2014 Qoder Rules\n\n",
    ".windsurf/rules/deaify.md": "# deaify \u2014 Windsurf Rules\n\n",
    ".cursor/rules/deaify.mdc": (
        "---\n"
        "description: deaify \u2014 remove AI smell from code and prose (prevention + remediation)\n"
        "globs: **/*\n"
        "alwaysApply: true\n"
        "---\n\n"
        "# deaify \u2014 Cursor Rules\n\n"
    ),
}


def skill_body(name: str) -> str:
    path = os.path.join(ROOT, "skills", name, "SKILL.md")
    with open(path, encoding="utf-8") as f:
        text = f.read()
    # Strip YAML frontmatter (--- ... ---) if present.
    if text.startswith("---"):
        idx = text.find("\n---", 3)
        if idx != -1:
            rest = text[idx + 4:]
            text = rest.lstrip("\n")
    return text.lstrip("\n")


def build() -> str:
    out = NOTE + "\n"
    first = True
    for name in SKILLS:
        body = skill_body(name)
        block = f"# {name}\n\n{body}"
        if first:
            out += block
            first = False
        else:
            # Horizontal-rule separator between skill blocks (matches existing layout).
            out += f"\n---\n\n{block}"
    return out + "\n"


def main() -> None:
    body = build()
    for rel, header in ADAPTERS.items():
        path = os.path.join(ROOT, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(header + body)
        print(f"wrote {rel}  ({len(header) + len(body)} bytes)")


if __name__ == "__main__":
    main()
