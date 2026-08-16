═════════════════════════════════════════════════════════════
# YEAR 1 PREREQUISITE AUDIT
### Freshman · Fall · Weeks 0–2 · All Six Courses
═════════════════════════════════════════════════════════════


> ⚠️ **Finding: assessed-before-taught is systemic in Weeks 0–2, not incidental.**
> Five of the six Fall courses declare `Prerequisites: None`. The opening
> problem sets do not honour that declaration. The largest single gap is
> **ten weeks** — PROG 101 PS 0 tests macro expansion semantics taught in Week 10.

**Audited:** 2026-08-16 · **Scope:** Freshman Fall, Weeks 0–2, 194 files (1.6 MB)
**Method:** every assignment, lab and quiz in Weeks 0–2 read against the
week-by-week lecture map of the full 13-week term, per course and across courses.
A concept counts as *taught* only where a lecture develops it — a passing mention,
a formula-sheet row, or a hint inside the assignment itself does not count.

---

## KEY

| Symbol | Meaning |
|--------|---------|
| 🔴 | Assessed before taught — gap of 3+ weeks |
| 🟠 | Assessed before taught — gap of 1–2 weeks |
| 🟡 | Due at the start of the very lecture that teaches it |
| 🔵 | Taught, but with under 48 hours of margin |
| ✅ | Correctly ordered, or explicitly scoped forward reference |

---

## 1 · The Declared Prerequisites

| Course | Syllabus states |
|--------|-----------------|
| CS 101 | None (concurrent: MATH 141 recommended) |
| PROG 101 | None (concurrent: CS 101 recommended) |
| MATH 151 | None |
| PHYS 141 | None (concurrent: MATH 141 strongly recommended) |
| CS 190 | None |
| MATH 141 | Precalculus / High School Calculus |

MATH 141 is the only course that declares an assumption, and it contradicts
itself internally: `Lecture 00 The Language of Mathematics` opens with
*"Prerequisites: None — this is the entry point"*, while `Lecture 01 Functions`
opens with *"Prerequisites: Precalculus / High School Algebra & Trigonometry"*.

The word doing the damage elsewhere is **concurrent**. Concurrent enrolment
guarantees only that the two courses run in the same term — it does not
guarantee the supporting material arrives *first*, and in the PHYS 141 / MATH 141
pairing it demonstrably does not.

---

## 2 · Findings, Ranked

| # | Where | Needs | Taught | Gap | Pts | |
|---|-------|-------|--------|-----|-----|---|
| 1 | PROG 101 PS 0 · P4 | macro expansion pitfalls `SQUARE(3+1)` | W10 | **10 wk** | 15 | 🔴 |
| 2 | PROG 101 PS 0 · P5 | recursion (`factorial`, `fibonacci`) | W9 | **9 wk** | 20 | 🔴 |
| 3 | PHYS 141 PS 1 · P3(b,c) | integration of `v(t)`, definite integral | MATH 141 W8–9 | **7 wk** | 5 | 🔴 |
| 4 | PROG 101 PS 0 · P4 | `malloc`/`free`, double-free | W6 | **6 wk** | — | 🔴 |
| 5 | PROG 101 PS 0 · P4 | pointers (`int *arr`) | W5 | **5 wk** | — | 🔴 |
| 6 | PROG 101 PS 0 · P4 | arrays | W4 | **4 wk** | — | 🔴 |
| 7 | MATH 141 PS 0 · P2(c) | proof by induction | MATH 151 W3 | **3 wk** | 2 | 🔴 |
| 8 | PHYS 141 PS 1 · P1(c,e) | differentiation (power rule) | MATH 141 W3–4 | **2–3 wk** | 30 | 🔴 |
| 9 | PROG 101 PS 0 · P3 | `for`/`while` loops | W2 | **2 wk** | 20 | 🟠 |
| 10 | PROG 101 PS 0 · P1 | shell scripting (`$1`, `${1%.c}`) | **never** | — | 10 | 🔴 |
| 11 | PROG 101 PS 1 · P3 | bitwise operators | W2 L01 (Tue) | same lecture | 20 | 🟡 |
| 12 | PROG 101 PS 1 · P4,P5 | loops | W2 L03 (Thu) | after due date | 35 | 🟡 |
| 13 | MATH 141 PS 1 · Part D | Intermediate Value Theorem | W2 L03 (Wed) | same lecture | 12 | 🟡 |
| 14 | MATH 141 PS 0 · P1(d),P10(e) | reference-triangle evaluation | table only | technique absent | 4 | 🟠 |
| 15 | CS 101 PS 1 · B7 | iteration (12-month schedule) | W2 L08 (Thu) | ~36 hrs | 16 | 🔵 |

---

## 3 · PROG 101 — The Worst Case

Week 0 lectures are `L01 Compilation Model`, `L02 Toolchain, Make, GDB`,
`L03 Hello World Deep-Dive`. **The string `for (` does not appear once in any
Week 0 lecture.** Problem Set 0 nevertheless requires:

| Problem | Pts | Requires | Taught in |
|---------|-----|----------|-----------|
| P1 Pipeline Inspector | 10 | bash scripting | never — hints only |
| P2 Info Printer | 15 | `#define`, `printf` width specs | ✅ W0 L03 |
| P3 Temperature Table | 20 | loops, `argc`/`argv`, `atof` | W2 / hints |
| P4 Error Hunt | 15 | arrays, pointers, `malloc`, macro semantics | W4, W5, W6, W10 |
| P5 GDB Investigation | 20 | recursion, function definition | W9, W3 |
| P6 Symbols Inspector | 20 | `nm`, symbol classes T/U/D/B | ✅ W0 L01 |

**65 of 100 points test material from Weeks 2–10.** Only P2 and P6 are
answerable from Week 0 instruction.

P5 is the sharpest case: it asks the student to *write* `factorial` and
`fibonacci` recursively in order to trace them under GDB. The GDB skill is
genuinely Week 0 material; the recursion needed to exercise it is Week 9. The
pedagogical intent is sound and the sequencing is not — a Week 0 GDB exercise
should trace a loop, or be handed a working recursive source file to trace.

The same shape repeats one week later. PS 1 is released end of Week 1 Thursday
and due **before Week 2 Lecture 1 (Tuesday)** — yet Problem 3 is a *Bitwise
Calculator* and Week 2 Lecture 1 is *Operators, Expressions, and Bit
Manipulation*. The set is collected in the hour before the lecture that teaches it.

One mitigating fact, in fairness: Week 1 lectures do *use* `for` loops and
`>>`/`&` in worked examples (`Lecture 01 Types Variables Memory.md:291`,
`Lecture 02 Integer Representation.md:224`) well before Week 2 formally teaches
them. Students are exposed. They are not instructed.

---

## 4 · PHYS 141 — The Worst Cross-Course Case

PS 1 is released Friday Week 1, due Friday Week 2. Part A is titled
*"Displacement, Velocity & the Derivative"* and is worth 30 points.

- **P1(c)** — "Find the instantaneous velocity v(t) by taking the derivative"
  of `x(t) = 4t³ − 9t² + 3`. The power rule is MATH 141 **Week 4**.
- **P3(b,c)** — "Find the position as a function of time by integration",
  then evaluate a definite integral. MATH 141 reaches Riemann sums and the
  definite integral in **Week 8** and the FTC in **Week 9**.

A student following the published schedule exactly cannot do Part A. This is
the clearest illustration of why `concurrent: MATH 141 strongly recommended`
is not a sufficient statement of the dependency — the physics needs Week 4 and
Week 8 calculus during Week 2.

---

## 5 · What Is Actually Fine

Recording these matters as much as the failures — three of them are the model
the rest should copy.

- ✅ **CS 101 is the reference implementation.** It needs `try/except` in Week 1
  but does not formally teach exceptions until Week 10, so
  `L06 Type System and REPL.md:197` says: *"We'll study `try/except` fully in
  Week 10. For now: know that `int()` and `float()` raise `ValueError` on
  invalid input, and this can be caught."* A scoped slice, plus a named week
  for the full treatment. **This is exactly the pattern the other courses need.**
- ✅ **MATH 151 Week 0 is fully self-contained.** PS 0 looks alarming — CNF, DNF,
  functional completeness, the Sheffer stroke — but every one is developed in
  `L02 Tautologies and Logical Laws`. No gap.
- ✅ **MATH 151 PS 2** reaches for infinitely-many-primes-of-form-4k+3 and the
  irrationality of √2+√3, but scaffolds both with explicit hints and builds on
  divisibility introduced in `L06 Direct Proof`. Hard, not unfair.
- ✅ **PHYS 141 PS 0 Q15** forward-references polar derivatives and *says so
  in the question*: "a topic we will cover formally in Week 2".
- ✅ **MATH 141 PS 2** is correctly ordered — released Wednesday Week 2, after
  IVT is lectured that same morning, due Week 3.
- ✅ **MATH 141 PS 1 Part A2** (Squeeze Theorem) is taught in Week 1, not assumed.
- ✅ **PROG 101 PS 0 P6** (`nm`, symbol classes) is genuinely Week 0 material,
  taught in `Lecture 01 Compilation Model.md:303`.
- ✅ **CS 190** carries no technical prerequisite load in Weeks 0–2.

---

## 6 · The Structural Cause

Two distinct mechanisms produce every 🔴 and 🟡 above.

**(a) Week 0 is doing two incompatible jobs.** MATH 141 frames Week 0 as
*"recalibration, not remediation"* — which presumes the material is already in
place. The other four treat Week 0 as orientation. The problem sets were
written to the harder framing across the board, so PROG 101 got a Week 0 set
pitched at a student who has already finished the course.

**(b) "Due at the start of class" collides with the lecture in that class.**
MATH 141 PS 1 (Part D, IVT) and PROG 101 PS 1 (Problem 3, bitwise) are both
collected at the beginning of the exact lecture that delivers their content.
This is a calendar error, not a curriculum error, and it is the cheapest to fix.

**A third, milder symptom:** where a course knows it is reaching ahead, it
compensates by putting instruction in the assignment's Hints block rather than
in a lecture — see PROG 101 PS 0 P1 and P3. This works for a motivated student
and silently fails everyone else, because hints are not revisable material and
do not appear in any reading guide.

---

## 7 · Recommendations

| Priority | Action | Fixes |
|----------|--------|-------|
| 1 | Move PROG 101 PS 0 P4 and P5 to Weeks 6 and 9; replace with pipeline/Make/GDB-on-a-loop exercises | #1, #2, #4, #5, #6 |
| 2 | Re-date MATH 141 PS 1 and PROG 101 PS 1 to fall due *after* the lecture that teaches their content | #11, #12, #13 |
| 3 | Add a PROG 101 Week 0 lecture segment on shell scripting, or drop P1 | #10 |
| 4 | Defer PHYS 141 PS 1 Part A calculus items to Week 4, or supply the two derivative/integral rules inline in the CS 101 style | #3, #8 |
| 5 | Rewrite MATH 141 PS 0 P2(c) to ask for a conjecture and a pattern, not a proof by induction | #7 |
| 6 | Replace `Prerequisites: None` with an honest **Assumed Background** block per course, generated from this audit | all |

Recommendation 6 is the durable one. The other five are patches; an accurate
`Assumed Background` block is what stops the next set of Week 0 material from
reintroducing the same problem.

---

## 8 · Metadata Errata Found While Auditing

Not prerequisite issues, but they surfaced during the sweep and should be fixed.

- **MATH 141 release-date contradiction.** `Problem Set 1.md` states
  *"Released: Wednesday, Week 1"*, but `MATH141 Week2/lectures/Lecture 01
  Continuity.md:250` — a **Monday** lecture — states *"Problem Set 1 released
  today (Wednesday)."* The footer is internally inconsistent on its own terms.
  Resolving it matters: under the PS header PS 1 Part D is unteachable, under
  the lecture footer it is correctly ordered. **The PS header is currently
  treated as authoritative, so finding #13 stands.**
- **MATH 151 lecture-numbering drift.** PS 0 D1 cites *"the laws from Lecture
  0.3"* and `L02` line 318 cites *"Exercise 4 of Lecture 0.2"*, but the files
  are `L00`, `L01`, `L02`. Prose uses 1-based numbering, filenames 0-based.

---

*Audit covers Freshman Fall only. Freshman Spring and Sophomore Year are unaudited;
the Week 0 framing problem in §6(a) is likely to recur wherever a Week 0 exists.*
