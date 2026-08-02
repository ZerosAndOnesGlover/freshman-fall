#!/usr/bin/env python3
"""
Generate answer sheets from the real assessment files.

Reads each assessment in a course, extracts its question/part structure and
point values, and writes a matching answer sheet under "4. Submissions/".

The `assessment:` field in each sheet's frontmatter is set to EXACTLY the Item
label used in the gradebook, so `gpa.py --sync` can carry scores across without
any name mapping.

Usage:
    python3 tools/make_answer_sheets.py --course "CS 101" --year "Year1 Freshman" --sem Fall
    python3 tools/make_answer_sheets.py ... --force     # overwrite existing sheets
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REG = Path(__file__).resolve().parent.parent
VAULT = REG.parent

# Where each course's material lives, and which gradebook component each
# filename prefix belongs to.
COURSE_ROOTS = {
    "CS 101": VAULT / "0. Freshman" / "Fall" / "0. CS 101 - Computer Science I: Foundations of Computation",
}

# (glob, gradebook component, label builder)
KINDS = [
    ("PS *.md",       "Problem Sets",   lambda n: f"PS {n}"),
    ("LAB *.md",      "Labs",           lambda n: f"Lab {n}"),
    ("QUIZ *.md",     "Quizzes",        lambda n: f"Quiz {n}"),
    ("PROJECT *.md",  "Projects",       lambda n: f"Project {n}"),
    ("MIDTERM *.md",  "Midterm Exam",   lambda n: f"Midterm {n}"),
    ("FINAL *.md",    "Final Exam",     lambda n: "Final Exam"),
]

SKIP = ("solution", "instructor guide", "answer key")

# Question headings we know how to extract, most specific first.
PATTERNS = [
    # ### A1: Immutability and Cost (7 points)
    re.compile(r"^###\s+([A-Z]\d+)[:.]?\s*(.*?)\s*\((\d+)\s*(?:points?|pts?)\)", re.M),
    # ### Question 3 (2 points)
    re.compile(r"^###\s+(Question\s+\d+)\s*\((\d+)\s*(?:points?|pts?)\)()", re.M),
    # ### 2.1 (8 points) Trace this code...
    re.compile(r"^###\s+(\d+\.\d+)\s*\((\d+)\s*(?:points?|pts?)\)\s*(.*?)$", re.M),
    # ## Part C: Applied — Log Analyser (12 points)
    re.compile(r"^##\s+(Part\s+[A-Z])[:.]?\s*(.*?)\s*\((\d+)\s*(?:bonus\s+)?(?:points?|pts?)\)", re.M),
]


def extract_parts(text: str):
    """Return [(label, title, points)] in document order, de-duplicated."""
    found = {}
    for pat in PATTERNS:
        for m in pat.finditer(text):
            g = m.groups()
            # normalise: some patterns put points in group 2, others group 3
            if g[1].isdigit():
                label, title, pts = g[0], (g[2] or "").strip(), int(g[1])
            else:
                label, title, pts = g[0], (g[1] or "").strip(), int(g[2])
            found.setdefault(m.start(), (label.strip(), title, pts))
    return [found[k] for k in sorted(found)]


def total_points(text: str, parts):
    """Authoritative point total, in decreasing order of trust.

    1. An explicit "**Total:** N points" line.
    2. A rubric table's "| **Total** | **N** |" row.
    3. The sum of Part-level headings, else the sum of question headings.
    4. 100, for holistically graded work (labs, projects) that states no total.

    Order matters: PS 1's part headings sum to 72 but its rubric table says 92,
    because not every scored item carries a parenthesised point value.
    """
    for pat in (r"\*\*Total:?\*\*:?\s*(\d+)\s*points?",
                r"\*\*Total:\s*(\d+)\s*points?\*\*",
                r"^#{1,4}\s*Total:\s*(\d+)\s*points?"):     # Midterm 1 states it as a heading
        m = re.search(pat, text, re.I | re.M)
        if m:
            return int(m.group(1))

    # Section-level headers, used by Midterm 2 (5 x 20 = 100).
    sections = [int(x) for x in
                re.findall(r"^##\s+Section\s+\d+[^(\n]*\((\d+)\s*points?\)", text, re.M)]
    if sections:
        return sum(sections)

    m = re.search(r"\|\s*\*\*Total\*\*\s*\|\s*\*\*(\d+)\*\*", text)
    if m:
        return int(m.group(1))

    part_heads = [int(x) for x in
                  re.findall(r"^##\s+Part\s+[A-Z][^(\n]*\((\d+)\s*points?\)", text, re.M)]
    if part_heads:
        return sum(part_heads)

    q_heads = [int(x) for x in
               re.findall(r"^###\s+[A-Z]?\d+(?:\.\d+)?[:.]?[^(\n]*\((\d+)\s*points?\)", text, re.M)]
    if q_heads:
        return sum(q_heads)

    return 100


def sheet_for(src: Path, label: str, component: str, course: str):
    text = src.read_text(encoding="utf-8")
    parts = extract_parts(text)
    possible = total_points(text, parts)

    out = [
        "---",
        f"assessment: {label}",
        f"course: {course}",
        f"component: {component}",
        f"possible: {possible}",
        "score:",
        "status: not-started",
        "started:",
        "submitted:",
        f'source: "{src.name}"',
        "---",
        "",
        f"# {course} — {label}",
        f"## Answer Sheet",
        "",
        f"**Assessment:** `{src.name}`",
        f"**Points available:** {possible}",
        "",
        "> Write your answers under each heading. Leave the **Marks** lines alone — they are filled",
        "> in during grading. When you are done, set `status: submitted` in the frontmatter above.",
        "",
        "---",
        "",
    ]

    if parts:
        for lbl, title, pts in parts:
            head = f"### {lbl}" + (f" — {title}" if title else "") + f"  ({pts} points)"
            out += [head, "", "**Your answer:**", "", "", "", f"*Marks: ___ / {pts}*", "", "---", ""]
    else:
        out += ["### Answer", "", "**Your answer:**", "", "", "",
                f"*Marks: ___ / {possible}*", "", "---", ""]

    out += [
        "## Grading Summary",
        "",
        "*Filled in by the grader.*",
        "",
        "| | |",
        "|---|---|",
        f"| **Score** | ___ / {possible} |",
        "| **Percent** | ___ |",
        "| **Graded** | ___ |",
        "",
        "**Feedback:**",
        "",
        "",
    ]
    return "\n".join(out), possible, len(parts)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--course", required=True)
    ap.add_argument("--year", required=True)
    ap.add_argument("--sem", required=True)
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()

    root = COURSE_ROOTS.get(a.course)
    if not root or not root.exists():
        print(f"Unknown or missing course root for {a.course!r}", file=sys.stderr)
        return 1

    dest = REG / "4. Submissions" / a.year / a.sem / a.course
    dest.mkdir(parents=True, exist_ok=True)

    made = skipped = 0
    index = []
    for glob, component, mk in KINDS:
        for src in sorted(root.rglob(glob)):
            low = src.name.lower()
            if any(s in low for s in SKIP) or "solutions_instructor" in str(src):
                continue
            m = re.search(r"\b(\d+)\b", src.name)
            num = m.group(1) if m else "1"
            label = mk(num)
            comp = f"{component} {num}" if component == "Midterm Exam" else component
            fname = label.replace(" ", " ") + ".md"
            target = dest / fname
            if target.exists() and not a.force:
                skipped += 1
                index.append((label, comp, "exists"))
                continue
            body, possible, nparts = sheet_for(src, label, comp, a.course)
            target.write_text(body, encoding="utf-8")
            made += 1
            index.append((label, comp, f"{possible} pts, {nparts} parts"))

    print(f"  created {made}, skipped {skipped} (use --force to overwrite)")
    for lbl, comp, info in index:
        print(f"    {lbl:<12} {comp:<16} {info}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
