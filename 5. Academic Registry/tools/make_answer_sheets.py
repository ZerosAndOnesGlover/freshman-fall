#!/usr/bin/env python3
"""
Generate answer sheets from the real assessment files.

Reads each assessment in a course, extracts its question/part structure and
point values, and writes a matching answer sheet under "4. Submissions/",
grouped into "week<N>/" folders mirroring the course's own week layout.

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

FRESH = VAULT / "0. Freshman"

# Where each course's material lives.
COURSE_ROOTS = {
    "CS 101":   FRESH / "Fall" / "0. CS 101 - Computer Science I: Foundations of Computation",
    "PROG 101": FRESH / "Fall" / "1. PROG 101 - Programming I: Structured Programming in C",
    "MATH 141": FRESH / "Fall" / "2. MATH 141 - Calculus I: Limits, Derivatives, and Integrals",
    "MATH 151": FRESH / "Fall" / "3. MATH 151 - Discrete Mathematics for Computer Science",
    "PHYS 141": FRESH / "Fall" / "4. PHYS 141 - Physics I: Mechanics, Waves, and Thermodynamics",
    "CS 190":   FRESH / "Fall" / "5. CS 190 - CS Seminar: Profession, Ethics & Culture",
    "CS 102":   FRESH / "Spring" / "0. CS 102 - Computer Science II: Algorithms and Data Structures",
    "PROG 102": FRESH / "Spring" / "1. PROG 102 - Programming II: Object-Oriented Design and Data Structures in C++",
    "MATH 142": FRESH / "Spring" / "2. MATH 142 - Calculus II: Integration Techniques and Series",
    "ECE 110":  FRESH / "Spring" / "3. ECE 110 - Digital Logic & Circuit Design",
}

# Which gradebook year/semester folder each course is filed under, so a whole
# year can be generated with --year.
COURSE_TERMS = {
    "CS 101": ("Year1 Freshman", "Fall"),   "PROG 101": ("Year1 Freshman", "Fall"),
    "MATH 141": ("Year1 Freshman", "Fall"), "MATH 151": ("Year1 Freshman", "Fall"),
    "PHYS 141": ("Year1 Freshman", "Fall"), "CS 190": ("Year1 Freshman", "Fall"),
    "CS 102": ("Year1 Freshman", "Spring"), "PROG 102": ("Year1 Freshman", "Spring"),
    "MATH 142": ("Year1 Freshman", "Spring"), "ECE 110": ("Year1 Freshman", "Spring"),
}

# A gradebook Item label parses into (kind, number); each kind is written a
# different way across courses, so match any of its aliases as a filename stem.
KIND_ALIASES = {
    "PS":       ("PS", "Problem Set"),
    "Lab":      ("LAB", "Lab"),
    "Quiz":     ("QUIZ", "Quiz"),
    "Project":  ("PROJECT", "Project"),
    "Midterm":  ("MIDTERM", "Midterm"),
}

# Items whose source document is not named after the item at all.
BESPOKE = {
    "CS 190": {
        "Prep {n}":         "CS190 Week{n}/Prep Assignment.md",
        "Position Paper 1": "CS190 Week3/Position Paper 1.md",
        "Position Paper 2": "CS190 Week6/Position Paper 2.md",
        "Position Paper 3": "CS190 Week9/Position Paper 3.md",
        "Presentation":     "CS190 Week11/Presentation Brief.md",
        "Peer Feedback A":  "CS190 Week11/Peer Feedback Form.md",
        "Peer Feedback B":  "CS190 Week11/Peer Feedback Form.md",
        "Peer Feedback C":  "CS190 Week11/Peer Feedback Form.md",
        "Question Prep":    "CS190 Week12/Question Preparation.md",
        "Reflection":       "CS190 Week12/Course Reflection.md",
        # "Contribution" is scored by the instructor from seminar participation;
        # there is nothing for the student to submit, so it gets no sheet.
    },
}

NO_SHEET = {("CS 190", "Contribution")}

# CS 101's Quiz 0 is an orientation self-assessment: the gradebook lists it at
# 10 points so the row lines up with the other quizzes, but it is never marked
# and must stay out of every calculation. See "4. Submissions/README.md".
UNGRADED = {("CS 101", "Quiz 0")}

# Work the student does that carries no course weight and so has no row in the
# main gradebook — it is tracked in a separate "_<course> ... Record.md" file,
# which gpa.py deliberately ignores. Sheets are still generated (the work is
# real) but marked `ungraded`, so sync passes over them instead of failing to
# find a row.
# (record file, component, item prefix, label column, points column or None)
RECORDS = {
    "CS 102": [("_CS 102 Lab and Quiz Record.md", "Labs", "Lab", 0, None),
               ("_CS 102 Lab and Quiz Record.md", "Quizzes", "Quiz", 0, 3)],
    "PROG 102": [("_PROG 102 Quiz Record.md", "Quizzes", "Quiz", 0, 4)],
}

# Never treat these as an assessment the student writes on. Note "answer key"
# is NOT here: MATH 141/142 file each quiz as "QUIZ 03 With Answer Key.md",
# the paper and its key in one document, and that file IS the assessment.
SKIP = ("solutions", "instructor guide", "preview",
        "study guide", "reference sheet", "rubric", "schedule")

# PROG 101 carries an out-of-curriculum appendix that duplicates the Week 7
# numbering (Problem Set 7 / LAB 7 / QUIZ 7); it must never win a match.
SKIP_DIRS = ("solutions_instructor", "not in curriculum")

# Course material is filed as "<CODE> Week<N>/", and sheets mirror that as
# "week<N>/" so a week's answers sit together.
WEEK = re.compile(r"[Ww]eek\s*(\d+)")


def week_dir_for(src: Path, root: Path) -> str:
    """The 'week<N>' folder a sheet belongs in, from where its source lives."""
    m = WEEK.search(str(src.relative_to(root)))
    return f"week{int(m.group(1))}" if m else ""

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
    # ## Problem 3: A Multi-File Program (30 pts)          -- PROG 101
    re.compile(r"^##\s+(Problem\s+\d+)[:.]?\s*(.*?)\s*\((\d+)\s*(?:points?|pts?)\)", re.M),
    # ### Part A: Newton's First and Second Laws (Problems 1-7) — 35 pts   -- PHYS 141
    re.compile(r"^###\s+(Part\s+[A-Z])[:.]?\s*(.*?)\s*[—–-]\s*(\d+)\s*(?:points?|pts?)\s*$", re.M),
    # **Q1. (18 points)** Evaluate:                        -- MATH 142 sample papers
    re.compile(r"^\*\*(Q\d+)\.?\s*\((\d+)\s*(?:points?|pts?)\)\*\*\s*(.*?)$", re.M),
]

# "| A — short answer | 20 | 8-10 questions ... |" -- the CS 102 / PROG 102
# revision guides state the paper's shape as a table instead of as headings.
FORMAT_ROW = re.compile(
    r"^\|\s*\*{0,2}([A-D])\s*[—–-]\s*([^|*]+?)\*{0,2}\s*\|\s*\*{0,2}(\d+)\*{0,2}\s*\|", re.M)


def extract_format_table(text: str):
    """Sections from a revision guide's 'shape of the paper' table."""
    return [(f"Section {m.group(1)}", m.group(2).strip(), int(m.group(3)))
            for m in FORMAT_ROW.finditer(text)]


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


# --- the gradebook is authoritative for what is assessed -------------------
#
# Every sheet's `assessment`, `component` and `possible` are read straight from
# the gradebook row they will sync into, so the join key cannot drift and a
# score can never exceed what the gradebook allows. The source document is used
# only for the shape of the answer sheet.

GB_ROW = re.compile(r"^\|\s*([^|]+?)\s*\|([^|]*)\|\s*([0-9.]+)\s*\|([^|]*)\|\s*$")
GB_HEAD = re.compile(r"^##\s+(.+?)\s*(?:[—:–-]\s*[\d.]+%.*)?$")


def gradebook_items(book: Path):
    """[(item, component, possible, topic)] for every syncable row."""
    items, comp = [], None
    for line in book.read_text(encoding="utf-8").splitlines():
        h = GB_HEAD.match(line)
        if h and not line.startswith("## Component Weights") and "credits" not in line:
            comp = re.split(r"\s+[—–:-]\s+\d", h.group(1))[0].strip()
            comp = re.sub(r"[:—–-]?\s*(formative.*|\d+%.*)$", "", comp).strip()
        m = GB_ROW.match(line)
        if m and comp and m.group(1) not in ("Item", "Component"):
            items.append((m.group(1).strip(), comp, float(m.group(3)), m.group(2).strip()))
    return items


def record_items(course: str, year: str, sem: str):
    """[(item, component, possible)] for 0%-weight work tracked outside the gradebook."""
    out = []
    for fname, comp, want, label_col, pts_col in RECORDS.get(course, []):
        book = REG / "2. Gradebook" / year / sem / fname
        if not book.exists():
            continue
        for line in book.read_text(encoding="utf-8").splitlines():
            if not line.startswith("|"):
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) <= max(label_col, pts_col or 0):
                continue
            if not re.match(rf"^{want}\s+\d+$", cells[label_col]):
                continue
            pts = 100.0
            if pts_col is not None and re.fullmatch(r"[0-9.]+", cells[pts_col]):
                pts = float(cells[pts_col])
            out.append((cells[label_col], comp, pts))
    return out


ITEM = re.compile(r"^(PS|Lab|Quiz|Project|Midterm|Prep)\s+(\d+)$")


def find_source(course: str, root: Path, item: str):
    """The assessment document a gradebook item is written against, or None."""
    bespoke = BESPOKE.get(course, {})
    m = ITEM.match(item)
    if m and f"{m.group(1)} {{n}}" in bespoke:
        p = root / bespoke[f"{m.group(1)} {{n}}"].format(n=int(m.group(2)))
        return p if p.exists() else None
    if item in bespoke:
        p = root / bespoke[item]
        return p if p.exists() else None

    if item == "Final Exam":
        stems, num = ("FINAL EXAM", "FINAL"), None
    elif m:
        stems, num = KIND_ALIASES[m.group(1)], int(m.group(2))
    elif item == "Midterm":                      # PHYS 141 has a single midterm
        stems, num = ("MIDTERM",), None
    else:
        return None

    hits = []
    for p in root.rglob("*.md"):
        rel = str(p.relative_to(root)).lower()
        if any(d in rel for d in SKIP_DIRS) or any(s in p.name.lower() for s in SKIP):
            continue
        for stem in stems:
            # "PS 3 Induction.md", "Problem Set 3.md", "LAB 03 ....md"
            pat = rf"^{re.escape(stem)}\s+0*{num}\b" if num is not None else rf"^{re.escape(stem)}\b"
            if re.match(pat, p.name, re.I):
                hits.append(p)
                break
    if not hits:
        return None
    # Prefer a real assessment over a revision guide when both exist.
    hits.sort(key=lambda p: ("resources" in str(p).lower(), len(str(p))))
    return hits[0]


def sheet_for(src, label: str, component: str, course: str, possible: float,
              status: str = "not-started", ungraded: str = ""):
    """Build one answer sheet. `possible` comes from the gradebook, not the source.

    `src` may be None when the gradebook assesses something the vault has no
    document for yet; the sheet is still written, with a single answer block, so
    the item is not silently missing from the registry.

    `ungraded` is the reason the work is not marked; when set, `possible` is
    zeroed and the status becomes `ungraded`, which `gpa.py --sync` passes over.
    """
    if ungraded:
        possible, status = 0, "ungraded"
    text = src.read_text(encoding="utf-8") if src else ""
    parts = extract_parts(text)
    shape = "parts"
    if not parts:
        parts = extract_format_table(text)
        shape = "format-table" if parts else "single"

    poss = f"{possible:g}"
    # An ungraded sheet still shows the paper's own marks, so the self-assessment
    # is answerable; only the gradebook-facing `possible` is zeroed.
    marks = f"{total_points(text, parts):g}" if ungraded else poss
    out = [
        "---",
        f"assessment: {label}",
        f"course: {course}",
        f"component: {component}",
        f"possible: {poss}",
        "score:",
        f"status: {status}",
        "started:",
        "submitted:",
        f'source: "{src.name}"' if src else "source:",
        "---",
        "",
        f"# {course} · {label}",
        f"## Answer Sheet",
        "",
        f"**Assessment:** `{src.name}`" if src else
        "**Assessment:** *no source document in the vault yet — see the gradebook row*",
        f"**Points available:** {ungraded}" if ungraded else f"**Points available:** {poss}",
        "",
        "> Write your answers under each heading. Leave the **Marks** lines alone — they are filled",
        "> in during grading. When you are done, set `status: submitted` in the frontmatter above.",
        "",
        "---",
        "",
    ]

    if shape.startswith("single"):
        out += ["### Answer", "", "**Your answer:**", "", "", "",
                f"*Marks: ___ / {marks}*", "", "---", ""]
    else:
        for lbl, title, pts in parts:
            head = f"### {lbl}" + (f" — {title}" if title else "") + f"  ({pts} points)"
            out += [head, "", "**Your answer:**", "", "", "", f"*Marks: ___ / {pts}*", "", "---", ""]

    out += [
        "## Grading Summary",
        "",
        "*Filled in by the grader.*",
        "",
        "| | |",
        "|---|---|",
        f"| **Score** | ___ / {marks} |",
        "| **Percent** | ___ |",
        "| **Graded** | ___ |",
        "",
        "**Feedback:**",
        "",
        "",
    ]
    return "\n".join(out), shape, len(parts)


COVERS = re.compile(r"Weeks?\s*(\d+)\s*[–—-]\s*(\d+)")
LAST_WEEK = 12


def week_of(item: str, src, root: Path, topic: str = "") -> str:
    """Where the sheet is filed.

    Exams are filed in the week they are sat, which the gradebook states as the
    coverage they close off: a paper covering Weeks 0-5 is sat in Week 6, and a
    comprehensive final in the last week. That is checked against the two
    courses whose exams do have documents — CS 101 and PROG 101 both sit
    Midterm 1 in Week 6 — and against CS 102's guide, which covers Weeks 0-4 and
    is sat in Week 5. Everything else follows its source document's own week,
    falling back to the item number, which is how weekly work is numbered.
    """
    is_exam = item.startswith(("Midterm", "Final"))
    if is_exam:
        if "comprehensive" in topic.lower():
            return f"week{LAST_WEEK}"
        m = COVERS.search(topic)
        if m:
            return f"week{min(int(m.group(2)) + 1, LAST_WEEK)}"
    if src:
        w = week_dir_for(src, root)
        if w:
            return w
    m = ITEM.match(item)
    return f"week{int(m.group(2))}" if m and not is_exam else ""


def course_folder(root: Path, term: Path, course: str) -> Path:
    """Submissions mirror the vault's course ordering: "0. CS 101", "1. PROG 101".

    The number is the one the course's own folder carries in "0. Freshman/",
    so the two trees stay in step without a second list to maintain. An
    existing folder wins whatever it is called, so a course that was filed
    before the numbering is not duplicated under a new name.
    """
    for p in (term.iterdir() if term.is_dir() else []):
        if p.is_dir() and re.sub(r"^\d+\.\s*", "", p.name) == course:
            return p
    m = re.match(r"(\d+)\.", root.name)
    return term / (f"{m.group(1)}. {course}" if m else course)


def week_folder(dest: Path, name: str) -> Path:
    """Reuse a week folder that already exists under another capitalisation.

    PROG 101's repo was started by hand with "Week0/"; creating "week0/" beside
    it on a case-sensitive filesystem would split one week across two folders.
    """
    if name and dest.is_dir():
        for p in dest.iterdir():
            if p.is_dir() and p.name.lower() == name.lower():
                return p
    return dest / name


def build_course(course: str, year: str, sem: str, force: bool):
    root = COURSE_ROOTS.get(course)
    book = REG / "2. Gradebook" / year / sem / f"{course}.md"
    if not root or not root.exists():
        print(f"  !! unknown or missing course root for {course!r}")
        return 0, 0, 0
    if not book.exists():
        print(f"  !! no gradebook at {book}")
        return 0, 0, 0

    # (item, component, possible, topic, reason-it-is-ungraded-or-"")
    orientation = "none — this is an ungraded orientation self-assessment"
    no_weight = "not graded — this work carries no course weight"
    work = [(i, c, p, t, orientation if (course, i) in UNGRADED else "")
            for i, c, p, t in gradebook_items(book) if (course, i) not in NO_SHEET]
    work += [(i, c, p, "", no_weight) for i, c, p in record_items(course, year, sem)]

    # A course whose material has not been built yet has nothing to write
    # against; say so rather than filling the registry with empty sheets.
    if work and not any(find_source(course, root, i) for i, _c, _p, _t, _u in work):
        print(f"  {course:<9} SKIPPED — no assessment documents exist in the vault yet "
              f"({len(work)} gradebook items)")
        return 0, 0, 0

    dest = course_folder(root, REG / "4. Submissions" / year / sem, course)
    made = skipped = nosrc = 0
    for item, comp, possible, topic, ungraded in work:
        src = find_source(course, root, item)
        fname = f"{item}.md"
        target = week_folder(dest, week_of(item, src, root, topic)) / fname
        existing = [p for p in dest.rglob(fname) if p.is_file()]
        if existing and not force:
            skipped += 1
            continue
        for p in existing:
            if p != target:              # --force: don't leave the old copy behind
                p.unlink()
        target.parent.mkdir(parents=True, exist_ok=True)
        body, _shape, _n = sheet_for(src, item, comp, course, possible,
                                     ungraded=ungraded)
        target.write_text(body, encoding="utf-8")
        made += 1
        if not src:
            nosrc += 1
            print(f"     no source document for {item}")
    print(f"  {course:<9} created {made}, skipped {skipped}"
          + (f", {nosrc} without a source document" if nosrc else ""))
    return made, skipped, nosrc


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--course", help="one course; omit with --all-year to do the whole year")
    ap.add_argument("--year", required=True)
    ap.add_argument("--sem")
    ap.add_argument("--all-year", action="store_true",
                    help="build every course the year's gradebook lists")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()

    if a.all_year:
        courses = [(c, y, s) for c, (y, s) in sorted(COURSE_TERMS.items()) if y == a.year]
        if not courses:
            print(f"No courses known for year {a.year!r}", file=sys.stderr)
            return 1
    else:
        if not (a.course and a.sem):
            print("--course and --sem are required without --all-year", file=sys.stderr)
            return 1
        courses = [(a.course, a.year, a.sem)]

    total = 0
    for course, year, sem in courses:
        made, _s, _n = build_course(course, year, sem, a.force)
        total += made
    print(f"\n  {total} sheets written")
    return 0


if __name__ == "__main__":
    sys.exit(main())
