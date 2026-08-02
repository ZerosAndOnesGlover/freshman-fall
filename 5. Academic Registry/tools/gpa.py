#!/usr/bin/env python3
"""
Academic Registry -- GPA / CGPA calculator.

Parses the gradebook markdown files under "2. Gradebook/", computes each course
grade from its component weights, and reports semester GPA, cumulative GPA,
credits earned, and academic standing.

The letter-grade scale is READ FROM "0. Institution/UNIVERSITY POLICIES.md" so
that file remains the single source of truth. It is never duplicated here.

Usage:
    python3 tools/gpa.py                 # report only
    python3 tools/gpa.py --write         # also update each gradebook's COMPUTED block
    python3 tools/gpa.py --self-test     # run built-in verification fixtures
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
POLICY = ROOT / "0. Institution" / "UNIVERSITY POLICIES.md"
GRADEBOOK = ROOT / "2. Gradebook"

EXCUSED = {"EX", "EXC", "EXCUSED", "-", "--", "N/A", "NA"}


# --------------------------------------------------------------------------
# Grade scale, parsed from the policy file
# --------------------------------------------------------------------------

def load_scale(policy_path: Path = POLICY):
    """Return [(letter, points, low, high)] sorted high->low. Raises if unparseable."""
    if not policy_path.exists():
        raise FileNotFoundError(f"cannot find the grading scale: {policy_path}")

    text = policy_path.read_text(encoding="utf-8")
    rows = []
    # | A- | 3.7 | 90-92% | Excellent |   (hyphen, en dash or minus sign all accepted)
    pat = re.compile(
        r"^\|\s*([A-F][+−–\-]?)\s*\|\s*([0-9.]+)\s*\|\s*"
        r"(?:(\d+)\s*[–−\-]\s*(\d+)|<\s*(\d+))\s*%?\s*\|",
        re.MULTILINE,
    )
    for m in pat.finditer(text):
        letter = m.group(1).replace("−", "-").replace("–", "-")
        points = float(m.group(2))
        if m.group(5) is not None:          # the "< 60%" row
            low, high = 0.0, float(m.group(5)) - 1e-9
        else:
            low, high = float(m.group(3)), float(m.group(4))
        rows.append((letter, points, low, high))

    if not rows:
        raise ValueError(f"no grade-scale rows found in {policy_path}")
    rows.sort(key=lambda r: r[2], reverse=True)
    return rows


def pct_to_letter(pct: float, scale) -> tuple[str, float]:
    """Map a percentage to (letter, points).

    The published bands are integer ranges (90-92, then 93-96), so they leave
    gaps: 92.4 belongs to no stated band. We therefore award the highest band
    whose FLOOR the score reaches, which is the ordinary reading of "you need
    93 for an A" -- 92.99 is an A-, not an A, and not a fall-through to F.

    Scores above the top floor (extra credit taking a course past 100) get the
    best grade available rather than falling off the end.
    """
    p = round(pct, 2)
    for letter, points, low, _high in scale:      # sorted by floor, high -> low
        if p >= low:
            return letter, points
    return scale[-1][0], scale[-1][1]             # below every floor -> F


# --------------------------------------------------------------------------
# Gradebook parsing
# --------------------------------------------------------------------------

class Component:
    def __init__(self, name, weight, drop_lowest=0):
        self.name = name
        self.weight = weight
        self.drop_lowest = drop_lowest
        self.items = []          # (label, possible, earned|None, excused)

    @property
    def graded(self):
        return [(l, p, e) for (l, p, e, x) in self.items if e is not None and not x]

    def percent(self):
        """Component percentage, or None if nothing is graded yet."""
        g = self.graded
        if not g:
            return None
        ratios = sorted((e / p if p else 0.0) for (_, p, e) in g)
        # Drop the lowest N, but never drop the only remaining score.
        drop = min(self.drop_lowest, max(0, len(ratios) - 1))
        kept = ratios[drop:]
        return 100.0 * sum(kept) / len(kept)

    def is_complete(self, expected=None):
        return len(self.graded) == len(self.items)


class Course:
    def __init__(self, path):
        self.path = path
        self.meta = {}
        self.components = []
        self.formative = []
        self._parse()

    def _parse(self):
        text = self.path.read_text(encoding="utf-8")

        fm = re.match(r"^---\n(.*?)\n---\n", text, re.S)
        if fm:
            for line in fm.group(1).splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    self.meta[k.strip()] = v.strip().strip('"')

        # Sections look like:  ## Problem Sets — 30%, lowest 1 dropped
        #                      ## Quizzes — formative, 0% weight
        #
        # The separator may be an em dash, en dash, hyphen OR COLON. The vault's
        # markdown linter rewrites "Heading — text" to "Heading: text", so a
        # dash-only pattern silently stops matching after the linter runs and
        # every course reports zero components. Requiring a '%' in the qualifier
        # keeps ordinary colon-bearing titles (e.g. "## Computer Science I:
        # Foundations of Computation") from matching.
        head = re.compile(r"^##\s+(.+?)\s*[—–:-]{1,2}\s*([^\n]*%[^\n]*)$", re.MULTILINE)
        marks = list(head.finditer(text))
        for i, m in enumerate(marks):
            name, qualifier = m.group(1).strip(), m.group(2).strip()
            if name.lower() in ("component weights", "computed"):
                continue
            wm = re.search(r"(\d+(?:\.\d+)?)\s*%", qualifier)
            if not wm:
                continue
            weight = float(wm.group(1))
            dm = re.search(r"lowest\s+(\d+)\s+dropped", qualifier, re.I)
            comp = Component(name, weight, int(dm.group(1)) if dm else 0)

            body = text[m.end(): marks[i + 1].start() if i + 1 < len(marks) else len(text)]
            for row in re.finditer(r"^\|\s*([^|]+?)\s*\|[^|]*\|\s*([0-9.]+)\s*\|\s*([^|]*?)\s*\|",
                                   body, re.MULTILINE):
                label, possible, earned = row.group(1), row.group(2), row.group(3).strip()
                if label.lower() in ("item", "---") or set(label) <= set("-: "):
                    continue
                excused = earned.upper() in EXCUSED and earned != ""
                val = None
                if earned and not excused:
                    try:
                        val = float(earned)
                    except ValueError:
                        raise ValueError(
                            f"{self.path.name}: cannot read '{earned}' as a score for {label!r}"
                        )
                comp.items.append((label, float(possible), val, excused))

            (self.formative if weight == 0 else self.components).append(comp)

    # -- derived ----------------------------------------------------------
    @property
    def code(self):
        return self.meta.get("course", self.path.stem)

    @property
    def credits(self):
        return float(self.meta.get("credits", 0))

    def weight_total(self):
        return sum(c.weight for c in self.components)

    def percent(self):
        """Weighted course percentage over the components that have any marks."""
        num = den = 0.0
        for c in self.components:
            p = c.percent()
            if p is not None:
                num += p * c.weight
                den += c.weight
        return (num / den) if den else None

    def is_complete(self):
        return bool(self.components) and all(
            c.graded and len(c.graded) == len(c.items) for c in self.components
        )

    def graded_weight(self):
        return sum(c.weight for c in self.components if c.percent() is not None)


# --------------------------------------------------------------------------
# Reporting
# --------------------------------------------------------------------------

def standing(cgpa):
    if cgpa is None:
        return "--"
    if cgpa >= 3.7:
        return "Good Standing (Dean's List eligible)"
    if cgpa >= 2.0:
        return "Good Standing"
    if cgpa >= 1.5:
        return "Academic Probation"
    return "Academic Suspension review"


def collect(gradebook=GRADEBOOK):
    """Return {(year_dir, sem_dir): [Course]} for every gradebook file found."""
    out = {}
    if not gradebook.exists():
        return out
    for p in sorted(gradebook.rglob("*.md")):
        if p.name.upper().startswith(("README", "SEMESTER SUMMARY", "_")):
            continue
        try:
            c = Course(p)
        except Exception as exc:                       # noqa: BLE001
            print(f"  !! skipping {p.name}: {exc}", file=sys.stderr)
            continue
        if not c.components:
            continue
        key = (p.parent.parent.name, p.parent.name)
        out.setdefault(key, []).append(c)
    return out


def report(write=False):
    scale = load_scale()
    groups = collect()
    if not groups:
        print("No gradebook files found under '2. Gradebook/'.")
        return 0

    all_pts = all_cr = 0.0
    print(f"\n{'=' * 66}\n  ACADEMIC REGISTRY -- GPA REPORT\n{'=' * 66}")

    for (year, sem), courses in sorted(groups.items()):
        print(f"\n{year} / {sem}")
        print(f"  {'Course':<10} {'Cr':>3}  {'Graded':>7}  {'Pct':>7}  {'Ltr':>3}  {'Pts':>4}")
        print(f"  {'-'*10} {'-'*3}  {'-'*7}  {'-'*7}  {'-'*3}  {'-'*4}")

        sem_pts = sem_cr = 0.0
        for c in sorted(courses, key=lambda x: x.code):
            wt = c.weight_total()
            if abs(wt - 100.0) > 0.01:
                print(f"  !! {c.code}: component weights sum to {wt}%, not 100%", file=sys.stderr)
            pct = c.percent()
            gw = c.graded_weight()
            if pct is None:
                print(f"  {c.code:<10} {c.credits:>3.0f}  {'0%':>7}  {'--':>7}  {'--':>3}  {'--':>4}")
                continue
            letter, points = pct_to_letter(pct, scale)
            flag = "" if c.is_complete() else "  (partial)"
            print(f"  {c.code:<10} {c.credits:>3.0f}  {gw:>6.0f}%  {pct:>6.2f}%  {letter:>3}  {points:>4.1f}{flag}")
            if c.is_complete():
                sem_pts += points * c.credits
                sem_cr += c.credits
            if write:
                write_computed(c, pct, letter, points, scale)

        if sem_cr:
            print(f"  {'-'*40}\n  Semester GPA: {sem_pts/sem_cr:.2f}   ({sem_cr:.0f} credits completed)")
            all_pts += sem_pts
            all_cr += sem_cr
        else:
            print(f"  {'-'*40}\n  Semester GPA: --   (no course fully graded yet)")

    print(f"\n{'=' * 66}")
    if all_cr:
        cgpa = all_pts / all_cr
        print(f"  Cumulative GPA : {cgpa:.2f}")
        print(f"  Credits earned : {all_cr:.0f} / 142 required")
        print(f"  Standing       : {standing(cgpa)}")
    else:
        print("  Cumulative GPA : --  (no completed courses)")
    print(f"{'=' * 66}\n")
    return 0


def write_computed(course, pct, letter, points, scale):
    text = course.path.read_text(encoding="utf-8")
    lines = [
        "<!-- BEGIN COMPUTED -->",
        "## Computed",
        "",
        "*Generated by `tools/gpa.py`. Do not edit by hand.*",
        "",
        "| Component | Weight | Graded | Percent |",
        "|---|---|---|---|",
    ]
    for c in course.components:
        p = c.percent()
        lines.append(
            f"| {c.name} | {c.weight:g}% | {len(c.graded)}/{len(c.items)} | "
            + (f"{p:.2f}%" if p is not None else "--") + " |"
        )
    for c in course.formative:
        p = c.percent()
        lines.append(
            f"| {c.name} *(formative)* | 0% | {len(c.graded)}/{len(c.items)} | "
            + (f"{p:.2f}%" if p is not None else "--") + " |"
        )
    status = "complete" if course.is_complete() else f"partial ({course.graded_weight():.0f}% of weight graded)"
    lines += [
        "",
        f"**Course percentage:** {pct:.2f}%",
        f"**Letter grade:** {letter}",
        f"**GPA points:** {points:.1f}",
        f"**Credits:** {course.credits:.0f}",
        f"**Status:** {status}",
        "<!-- END COMPUTED -->",
    ]
    new = re.sub(r"<!-- BEGIN COMPUTED -->.*?<!-- END COMPUTED -->",
                 "\n".join(lines), text, flags=re.S)
    if new != text:
        course.path.write_text(new, encoding="utf-8")


# --------------------------------------------------------------------------
# Self-test
# --------------------------------------------------------------------------

def self_test():
    import tempfile
    ok = failed = 0

    def check(name, got, want):
        nonlocal ok, failed
        good = got == want or (isinstance(want, float) and isinstance(got, float)
                               and abs(got - want) < 1e-6)
        print(f"  {'PASS' if good else 'FAIL'}  {name}" + ("" if good else f"   got {got!r}, want {want!r}"))
        ok, failed = ok + good, failed + (not good)

    scale = load_scale()
    print("Scale parsed from UNIVERSITY POLICIES.md")
    check("13 bands found", len(scale), 13)
    check("A+ = 4.0", pct_to_letter(98, scale), ("A+", 4.0))
    check("93 -> A", pct_to_letter(93, scale), ("A", 4.0))
    check("92.99 -> A-", pct_to_letter(92.99, scale), ("A-", 3.7))
    check("90 -> A-", pct_to_letter(90, scale), ("A-", 3.7))
    check("68 -> D+ (university, not CS101 legacy D)", pct_to_letter(68, scale), ("D+", 1.3))
    check("63 -> D", pct_to_letter(63, scale), ("D", 1.0))
    check("60 -> D-", pct_to_letter(60, scale), ("D-", 0.7))
    check("59.99 -> F", pct_to_letter(59.99, scale), ("F", 0.0))
    check("0 -> F", pct_to_letter(0, scale), ("F", 0.0))

    print("\nComponent arithmetic")
    c = Component("PS", 30, drop_lowest=1)
    for i, (p, e) in enumerate([(100, 90), (100, 80), (100, 100), (100, 50)]):
        c.items.append((f"PS{i}", p, e, False))
    check("drop-lowest removes the 50", round(c.percent(), 4), 90.0)

    c2 = Component("PS", 30, drop_lowest=1)
    c2.items.append(("only", 100.0, 40.0, False))
    check("never drops the only score", c2.percent(), 40.0)

    c3 = Component("PS", 30, drop_lowest=0)
    c3.items += [("a", 100.0, 80.0, False), ("b", 100.0, None, False)]
    check("ungraded rows excluded, not zeroed", c3.percent(), 80.0)

    c4 = Component("PS", 30, drop_lowest=0)
    c4.items += [("a", 100.0, 80.0, False), ("b", 100.0, None, True)]
    check("excused rows excluded", c4.percent(), 80.0)

    c5 = Component("PS", 30, drop_lowest=0)
    c5.items += [("a", 100.0, 80.0, False), ("b", 100.0, 0.0, False)]
    check("explicit zero IS counted", c5.percent(), 40.0)

    c6 = Component("Mixed", 10, drop_lowest=0)
    c6.items += [("a", 167.0, 167.0, False), ("b", 100.0, 50.0, False)]
    check("unequal maxima weigh equally by ratio", c6.percent(), 75.0)

    print("\nEnd-to-end on a fixture course")
    fixture = """---
course: TEST 100
credits: 3
---
## Exams — 60%

| Item | T | Possible | Earned |
|---|---|---|---|
| Mid | x | 100 | 85 |
| Fin | x | 100 | 95 |

## Homework — 40%, lowest 1 dropped

| Item | T | Possible | Earned |
|---|---|---|---|
| H1 | x | 100 | 100 |
| H2 | x | 100 | 60 |

<!-- BEGIN COMPUTED -->
<!-- END COMPUTED -->
"""
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "TEST 100.md"
        p.write_text(fixture, encoding="utf-8")
        course = Course(p)
        check("two weighted components parsed", len(course.components), 2)
        check("weights sum to 100", course.weight_total(), 100.0)
        check("exams = 90%", round(course.components[0].percent(), 4), 90.0)
        check("homework drops the 60", round(course.components[1].percent(), 4), 100.0)
        # 90*0.6 + 100*0.4 = 94.0
        check("course = 94.00%", round(course.percent(), 4), 94.0)
        check("94 -> A", pct_to_letter(course.percent(), scale), ("A", 4.0))
        check("course is complete", course.is_complete(), True)

    print("\nSeparator tolerance (the vault linter rewrites em dashes to colons)")
    for sep, desc in [("—", "em dash"), ("–", "en dash"), ("-", "hyphen"), (":", "colon")]:
        src = f"""---
course: SEP TEST
credits: 1
---
## Exams {sep} 100%

| Item | T | Possible | Earned |
|---|---|---|---|
| E1 | x | 100 | 70 |
"""
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "S.md"
            p.write_text(src, encoding="utf-8")
            c = Course(p)
            check(f"{desc} separator parses", len(c.components), 1)

    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "T.md"
        p.write_text("""---
course: TITLE TEST
credits: 1
---
## Computer Science I: Foundations of Computation · 4 credits

## Exams: 100%

| Item | T | Possible | Earned |
|---|---|---|---|
| E1 | x | 100 | 70 |
""", encoding="utf-8")
        c = Course(p)
        check("colon-bearing title is not mistaken for a component", len(c.components), 1)
        check("that component is the real one", c.components[0].name, "Exams")

    print("\nPartial-term behaviour")
    partial = fixture.replace("| Fin | x | 100 | 95 |", "| Fin | x | 100 | |")
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "P.md"
        p.write_text(partial, encoding="utf-8")
        c = Course(p)
        check("exams now 85% (ungraded final ignored)", round(c.components[0].percent(), 4), 85.0)
        check("course = 91.00%", round(c.percent(), 4), 91.0)
        check("flagged incomplete", c.is_complete(), False)
        check("graded weight is still 100%", c.graded_weight(), 100.0)

    print("\nGPA aggregation")
    check("4cr@3.7 + 3cr@4.0 -> 3.83", round((4 * 3.7 + 3 * 4.0) / 7, 2), 3.83)
    check("standing at 3.7", standing(3.7), "Good Standing (Dean's List eligible)")
    check("standing at 2.0", standing(2.0), "Good Standing")
    check("standing at 1.7", standing(1.7), "Academic Probation")
    check("standing at 1.2", standing(1.2), "Academic Suspension review")

    print(f"\n{ok}/{ok+failed} checks passing")
    return 0 if failed == 0 else 1


SUBMISSIONS = ROOT / "4. Submissions"


def read_frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}
    out = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            out[k.strip()] = v.strip().strip('"')
    return out


def sync(dry_run=False):
    """Carry graded scores from answer sheets into the gradebooks.

    An answer sheet contributes only when its frontmatter has BOTH a numeric
    `score:` and `status: graded`. Anything else is left alone, so a sheet that
    is merely written but not yet marked never lands in the gradebook.
    """
    if not SUBMISSIONS.exists():
        print("No '4. Submissions/' folder; nothing to sync.")
        return 0

    # course code -> gradebook path
    books = {}
    for p in GRADEBOOK.rglob("*.md"):
        fm = read_frontmatter(p)
        if fm.get("course"):
            books[fm["course"]] = p

    applied, skipped, problems = 0, 0, []
    for sheet in sorted(SUBMISSIONS.rglob("*.md")):
        if sheet.name.upper().startswith("README"):
            continue
        fm = read_frontmatter(sheet)
        course, item, raw = fm.get("course"), fm.get("assessment"), fm.get("score", "")
        if not (course and item):
            continue
        if fm.get("status") != "graded" or not raw:
            skipped += 1
            continue
        try:
            score = float(raw)
        except ValueError:
            problems.append(f"{sheet.name}: score {raw!r} is not a number")
            continue
        book = books.get(course)
        if not book:
            problems.append(f"{sheet.name}: no gradebook for course {course!r}")
            continue

        text = book.read_text(encoding="utf-8")
        pat = re.compile(rf"^\|\s*{re.escape(item)}\s*\|([^|]*)\|\s*([0-9.]+)\s*\|([^|]*)\|$", re.M)
        m = pat.search(text)
        if not m:
            problems.append(f"{sheet.name}: no row labelled {item!r} in {book.name}")
            continue
        possible = float(m.group(2))
        if score > possible:
            problems.append(f"{sheet.name}: score {score:g} exceeds possible {possible:g}")
            continue
        existing = m.group(3).strip()
        if existing == f"{score:g}":
            skipped += 1
            continue
        if dry_run:
            print(f"  would set {course} / {item} = {score:g} / {possible:g}"
                  + (f"  (was {existing})" if existing else ""))
        else:
            text = pat.sub(lambda mm: f"| {item} |{mm.group(1)}| {mm.group(2)} | {score:g} |",
                           text, count=1)
            book.write_text(text, encoding="utf-8")
            print(f"  {course} / {item} = {score:g} / {possible:g}"
                  + (f"  (was {existing})" if existing else ""))
        applied += 1

    print(f"\n  {'would apply' if dry_run else 'applied'} {applied}, "
          f"skipped {skipped} (not graded, or unchanged)")
    for p in problems:
        print(f"  !! {p}", file=sys.stderr)
    return 1 if problems else 0


def main():
    ap = argparse.ArgumentParser(description="Compute GPA and CGPA from the gradebook.")
    ap.add_argument("--write", action="store_true", help="update each gradebook's COMPUTED block")
    ap.add_argument("--sync", action="store_true",
                    help="copy graded scores from '4. Submissions/' into the gradebooks")
    ap.add_argument("--dry-run", action="store_true", help="with --sync, show changes without writing")
    ap.add_argument("--self-test", action="store_true", help="run verification fixtures")
    args = ap.parse_args()

    if args.self_test:
        return self_test()
    if args.sync:
        rc = sync(dry_run=args.dry_run)
        if args.dry_run:
            return rc
        print()
    return report(write=args.write)


if __name__ == "__main__":
    sys.exit(main())
