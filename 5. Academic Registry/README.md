# Academic Registry
## CSE B.Sc · Policies, Scheduling, and Academic Records

This folder holds everything the *institution* knows about the degree: the rules, the timetables,
and the record of what has been earned. Course content lives elsewhere (under `0. Freshman/`,
`1. Sophomore/`, and so on); this folder never contains teaching material.

*(Formerly "5. CSE University Timetable" — renamed because scheduling is only about a third of what
it holds.)*

---

## Layout

```
5. Academic Registry/
├── 0. Institution/      The rules. Authoritative.
│   ├── UNIVERSITY POLICIES.md     <- the grade scale lives here, and only here
│   ├── GRADING STANDARDS.md       <- rubrics for psets, labs, exams, projects
│   ├── DEGREE REQUIREMENTS.md     <- 142-credit checklist by category
│   └── ACADEMIC CALENDAR.md
├── 1. Scheduling/       Timetables, room assignments, office hours, per year
│   ├── Year1 - Freshman/ … Year5 - Masters/
├── 2. Gradebook/        Score ledgers. One file per course.
│   └── Year1 Freshman/Fall/CS 101.md, MATH 141.md, …
├── 3. Transcript/       Derived records
│   └── TRANSCRIPT.md
├── 4. Submissions/      YOUR ANSWERS -- one sheet per assessment
│   └── Year1 Freshman/Fall/CS 101/   PS 1-11, Lab 0-11, Quiz 0-11,
│                                     Midterm 1-2, Final Exam, Project 1-2
└── tools/
    ├── gpa.py                     <- computes everything
    ├── make_answer_sheets.py      <- generates answer sheets from assessments
    └── GRADEBOOK SCHEMA.md        <- the file format, if you add a course
```

---

## How Grading Works Here

**One scale, one place.** `0. Institution/UNIVERSITY POLICIES.md` defines the 13-band letter scale
(A+ 4.0 … F 0.0). `tools/gpa.py` **parses that file at runtime** rather than hard-coding the scale,
so the policy document is genuinely the single source of truth. Change it there and every computed
grade follows.

**You enter scores. Nothing else.** In a gradebook file you fill in the **Earned** column and leave
everything else alone. Percentages, component subtotals, the course grade, the letter, GPA points,
semester GPA and CGPA are all derived.

**Blank ≠ zero.** An unmarked row is excluded from the average, so a mid-semester percentage reflects
what has actually been graded. Enter `0` for a real zero and `EX` to excuse an item.

---

## Usage

```bash
cd "5. Academic Registry"

python3 tools/gpa.py                   # print the report
python3 tools/gpa.py --write           # also refresh each gradebook's Computed block
python3 tools/gpa.py --sync --write    # pull graded scores from 4. Submissions/, then report
python3 tools/gpa.py --sync --dry-run  # preview what sync would change
python3 tools/gpa.py --self-test       # 38 verification checks
```

### Writing and grading

You write answers in `4. Submissions/`, not in the gradebook. The loop is:

1. **Write** in the answer sheet for that assessment
2. **Set** `status: submitted` in its frontmatter
3. **Ask me to grade it** — I mark against the instructor key and set `score:` / `status: graded`
4. **Run** `python3 tools/gpa.py --sync --write`

A sheet reaches the gradebook only when it is both `graded` and has a numeric score, so unfinished
work never leaks into your GPA. See `4. Submissions/README.md`.

Run `--self-test` after editing `gpa.py`. It checks the scale parse, every band boundary,
drop-lowest, excused and blank handling, unequal point maxima, heading-separator tolerance,
partial-term behaviour, and GPA aggregation against hand-computed fixtures.

---

## Current State

| Course | Cr | Gradebook | Weights source |
|---|---|---|---|
| CS 101 | 4 | complete — all 11 PS, 12 labs, 2 midterms, final, 2 projects, 12 quizzes | its syllabus ✅ |
| MATH 141 | 4 | complete — mirrors syllabus (content built through Week 7) | its syllabus ✅ |
| PROG 101 | 4 | **stub** | ⚠ no syllabus in vault |
| MATH 151 | 3 | **stub** | ⚠ no syllabus in vault |
| PHYS 141 | 4 | **stub** | ⚠ no syllabus in vault |
| CS 190 | 1 | **stub** | ⚠ no syllabus in vault |

The four stubs carry a single placeholder component so they stay parseable and visible, but they
contribute nothing to GPA until real weights are entered. They are marked
`status: awaiting-syllabus` in their frontmatter.

**Fall total: 20 credits.**

---

## Adding a Course

1. Copy an existing gradebook as a template and read `tools/GRADEBOOK SCHEMA.md`
2. Set the frontmatter (`course`, `title`, `credits`, `year`, `semester`)
3. Give each component a `## Name — NN%` heading; weights must sum to 100
4. Run `python3 tools/gpa.py` — it warns if they do not

---

*CSE B.Sc · Academic Registry*
