# Gradebook File Schema

The format `tools/gpa.py` expects. Deviating breaks parsing, usually silently, so follow it.

---

## 1. Frontmatter (required)

```yaml
---
course: CS 101
title: "Computer Science I: Foundations of Computation"
credits: 4
year: 1
semester: Fall
status: in-progress
---
```

`course` and `credits` are load-bearing — `credits` weights the course in GPA, and a missing value
defaults to 0, silently excluding it. `status` is informational (`in-progress`, `complete`,
`awaiting-syllabus`).

## 2. Component sections

Each weighted component is an `##` heading carrying its weight:

```markdown
## Problem Sets — 30%, lowest 1 dropped
## Midterm Exam 1 — 15%
## Quizzes — formative, 0% weight
```

- The separator may be an em dash, en dash, hyphen, **or colon**.
  The vault's markdown linter rewrites `Heading — text` to `Heading: text`, so the parser accepts
  both. A qualifier must contain a `%`, which is what stops an ordinary colon-bearing title such as
  `## Computer Science I: Foundations of Computation` from being read as a component.
- The weight is the first `NN%` in the qualifier.
- `lowest N dropped` anywhere in the qualifier enables drop-lowest.
- **Weight 0 marks a component formative**: recorded and reported, excluded from the grade.
- Weighted components must sum to **100%**. `gpa.py` warns on stderr if they do not.
- `## Component Weights` and `## Computed` are reserved and skipped.

## 3. Item tables

Exactly four columns, in this order:

```markdown
| Item | Topic | Possible | Earned |
|---|---|---|---|
| PS 1 | Data Types and Expressions | 100 | 88 |
| PS 2 | Control Flow | 100 | |
```

| Column | Meaning |
|---|---|
| **Item** | Label. Must not be `Item` or a separator row |
| **Topic** | Free text, ignored by the parser |
| **Possible** | Points available. Required, numeric |
| **Earned** | **The only column you edit** |

### Earned values

| You write | Meaning |
|---|---|
| `88` | 88 points earned |
| `0` | A genuine zero — **counted**, drags the average down |
| *(blank)* | Not yet marked — **excluded**, not treated as zero |
| `EX` | Excused — excluded. Also `EXC`, `EXCUSED`, `-`, `--`, `N/A` |

Anything else raises a clear error naming the file and item rather than failing silently.

## 4. The computed block

```markdown
<!-- BEGIN COMPUTED -->
...
<!-- END COMPUTED -->
```

Overwritten wholesale by `gpa.py --write`. Never edit inside it. The markers must both be present or
the write is skipped.

---

## Rules the parser applies

**Items weigh equally within a component, by ratio.** A 167-point PS and a 100-point PS each count
once — the component percentage is the mean of `earned/possible`, not `sum(earned)/sum(possible)`.
This matters: under the sum method a large assignment would quietly dominate.

**Drop-lowest never drops the only score.** With one graded item and `lowest 1 dropped`, that item
stands. Otherwise the component would have nothing left.

**Drop-lowest ranks by ratio, not raw points.** 150/167 (89.8%) outranks 88/100 (88%).

**A component with no graded items returns nothing** and is excluded from the course percentage
along with its weight — so a mid-term percentage is computed over graded weight only, not diluted by
work not yet done.

**A course counts toward GPA only when every item in every weighted component is graded.** Partial
courses are shown with their running percentage and flagged `(partial)`, but are excluded from
semester GPA and CGPA.

**Letter banding.** The published bands are integer ranges (90–92, then 93–96) and so leave gaps.
A score is awarded the highest band whose **floor** it reaches: 92.99 is an A−, not an A, and not a
fall-through to F. Scores above 100 (extra credit) get the top band.

---

*Academic Registry · tools*

---

## Answer sheets and score sync

Scores do not have to be typed into the gradebook by hand. `4. Submissions/` holds one answer sheet
per assessment, and:

```bash
python3 tools/gpa.py --sync --write
```

copies each sheet's `score:` into the matching gradebook row, joining on the sheet's `assessment:`
field against the row's **Item** label. A sheet is only copied when it has `status: graded` *and* a
numeric score.

The sync refuses to act and reports on stderr when a score exceeds the row's Possible, when no row
matches the label, or when the score is not a number. Use `--dry-run` to preview.

Point totals in both files are derived from the assessment documents themselves by
`tools/make_answer_sheets.py`, in this order of trust: an explicit `**Total:** N points` line, then
a `## Total: N points` heading, then a rubric table's `| **Total** | **N** |` row, then the sum of
Section or Part headings, then the sum of question headings, then 100 for holistically graded work.

*Order matters.* PS 1's question headings sum to 72, but its rubric table says 92 — not every scored
item carries a parenthesised point value.
