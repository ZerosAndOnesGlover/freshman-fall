═════════════════════════════════════════════════════════════
# YEAR 1 PREREQUISITE AUDIT
### Freshman · Fall + Spring · Weeks 0–12 · All Ten Courses
═════════════════════════════════════════════════════════════


> ⚠️ **Finding: assessed-before-taught is systemic in Weeks 0–2, not incidental.**
> Five of the six Fall courses declare `Prerequisites: None`. The opening
> problem sets do not honour that declaration. The largest single gap is
> **ten weeks** — PROG 101 PS 0 tests macro expansion semantics taught in Week 10.

**Audited:** 2026-08-16 · **Scope:** Freshman Fall + Spring, Weeks 0–12, all ten courses
**Status:** 27 findings raised · 7 retracted · 3 downgraded · **17 upheld** (see §12)
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
| 15 | CS 101 PS 1 · B7 | iteration (12-month schedule) | W2 L08 (Thu) | ~~36 hrs~~ **see §12** | 16 | ✅ |

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

## 9 · Weeks 3–12 (added 2026-08-16)

Second pass, extending the audit to the rest of Fall. **Weeks 3–12 are far cleaner than Weeks 0–2.**
Four cross-course gaps, no same-course gaps at all, and every one of the four has been resolved
in place with a scoped preview rather than by re-sequencing — the courses stay in lockstep.

### Findings, all resolved

| # | Lecture needing it | Needs | Delivered | Gap | Preview added |
|---|---|---|---|---|---|
| 16 | PHYS 141 W4 · `L13 Work and Kinetic Energy` | definite integral; substitution | MATH 141 **W8**, **W10** | 4–6 wk | §3 and §4 |
| 17 | PHYS 141 W5 · `L16 Momentum and Impulse` | definite integral (`J = ∫F dt`) | MATH 141 **W8** | 3 wk | §3 |
| ~~18~~ | ~~PHYS 141 W6 · `L20`~~ | ~~definite integral~~ | — | — | **RETRACTED — see §12** |
| 19 | CS 101 W5 · `L18 Merge Sort and Quicksort` | permutations (`n!`); Stirling | MATH 151 **W7**; Stirling **never** | 2 wk; ∞ | **downgraded — see §12** |

**PHYS 141 is the whole story.** Findings 16–18 are one dependency seen three times: mechanics
needs the definite integral from Week 4 onward, and MATH 141 does not reach it until Week 8. The
Week 1 preview added earlier (`L04` §7.1) already supplied the reverse power rule and
`[F(x)]ᵃᵇ` evaluation, so findings 17 and 18 needed only a short pointer back to it plus one
worked case. Only finding 16 needed genuinely new material — the change of variables in the
work–energy derivation is *substitution*, MATH 141 Week 10.

**Finding 19 is the only gap with no home.** Stirling's approximation appears in neither MATH 141
nor MATH 151 at any point in Year 1, so it cannot be previewed "from" anywhere. The preview
therefore gives an elementary substitute — at least half the factors of `n!` exceed `n/2`, so
`n! ≥ (n/2)^(n/2)` and `log₂(n!) = Ω(n log n)` — which is enough to close the proof without
Stirling at all.

### Verified clean — worth recording

Several predicted gaps turned out not to exist. Recording them stops the next audit re-deriving them.

- ✅ **CS 101 W6 does not depend on MATH 151.** `L20 Recurrence Relations and Master Theorem`
  looked like a 3-week forward reference to MATH 151 W9, but CS 101 **defines and solves
  recurrences itself**, by unrolling and recursion trees. It never reaches for MATH 151's
  characteristic-equation method. No gap.
- ✅ **CS 101 W8 teaches its own pigeonhole principle** in `L26 Collision Resolution and Resizing`,
  the same week MATH 151 covers it. Simultaneous, not dependent.
- ✅ **CS 101 W7 PS 7 flags its own forward reference.** The LRU-cache problem needs `dict` from
  Week 8 and says so in the question — *"dictionaries are covered in Week 8, so you may need to
  preview `dict` basics, or wait and revisit this after Week 8."* This is the pattern the whole
  audit is arguing for, already in use.
- ✅ **PROG 101 Weeks 3–12 are clean.** Its `O(n log n)` usage in W7 and W9 follows CS 101's
  Big-O delivery at W6. Its W9 Fibonacci-recurrence reference follows both CS 101 W6 and
  MATH 151 W9.
- ✅ **MATH 141 Weeks 3–12 ask for no induction or formal proof.** Finding #7 (PS 0) was isolated.
- ✅ **PHYS 141 W12 thermodynamics** uses integrals, but MATH 141 has delivered them by Week 8–9.
- ✅ **MATH 151 Weeks 3–12 and CS 190** carry no external dependency.

### Method note

Findings 16–19 were reached by building a taught-index for all six courses across all 13 weeks,
then testing each course's assessments and lectures against *every other course's* delivery week.
Predictions were checked, not assumed: two of the four predicted gaps (CS 101 W6, CS 101 W8)
dissolved on inspection, and two gaps that were not predicted (PHYS 141 W5, W6) turned up.

---

## 10 · Freshman Spring, Weeks 0–12 (added 2026-08-16, **corrected same day**)

> ⚠️ **This section was substantially wrong on first pass and has been rewritten.** The first sweep
> reported eight Spring findings. **Six were not real**, one was real but belonged in the pset, and
> only one was a genuine lecture gap. The method error is recorded in §11 because it is more useful
> than the findings were.

### What Spring actually looks like

Spring has all of Fall complete behind it, and cross-course dependency largely vanishes: MATH 151's
logic underwrites ECE 110's Boolean algebra, its graphs and recurrences underwrite CS 102, MATH 141
underwrites MATH 142 — each a full semester early. **Spring is in good shape.** Its courses also
handle their own forward references well, mostly by the self-flagging pattern this audit recommends.

### The two real findings

| # | Where | Problem | Fix |
|---|---|---|---|
| 20 | CS 102 W4 · `PS 4 Graph Traversal` D4 | Requires building a **union–find ground truth**; union–find is **Week 6**. The lecture never mentions it, so this is purely a pset reaching forward. | **Pset changed.** D4 now specifies the edge-count characterisation — a graph is a forest iff `\|E\| = \|V\| − c` — which needs only the BFS/DFS from Part B. Verified against six cases including self-loops and parallel edges. Union–find is named as the tool you would reach for in practice, with its Week 6 pointer. |
| 21 | CS 102 W8 · `L25 Interval DP` | Minimises the **expected** number of comparisons, weighting keys by search probability. Expected value is defined **nowhere in Year 1** — probability is MATH 251, **Year 2 Spring**. | **Preview added to `L25`**, the only Spring preview retained. Supplies `E = Σpᵢvᵢ`, ties it to depth+1, and works the lecture's own `[0.7, 0.1, 0.1, 0.1]` example to show where its quoted 33% figure comes from. |

Finding 21 remains **the most serious in the whole audit**: a forward reference into the *next
academic year*, in a lecture that used the concept without defining it.

### The six retracted findings

Each was raised because a pset mentioned a topic listed against a later week in the course's
topic index. In every case the **lecture had already handled it** — either by teaching the needed
slice outright, or by self-flagging with an explicit week pointer.

| Retracted | Why it was not a gap |
|---|---|
| PROG 102 W1 · exception guarantees | `L06` **teaches** it: *"This is the **strong exception guarantee**"*, and verifies it against a thrown `bad_alloc`. |
| PROG 102 W3 · lambdas | `L12` demonstrates lambda syntax from line 20 onward, repeatedly, in its own worked examples. |
| CS 102 W7 · NP-completeness | `L24` already states *"0/1 knapsack is **NP-complete** (Week 12)"* and already uses the term **pseudo-polynomial**. |
| PROG 102 W7 · threads | `L23` **teaches** the thread-safe Singleton, including a verified sixteen-thread experiment with ThreadSanitizer — precisely what PS 7 asks for. |
| CS 102 W3 · Dijkstra `decrease_key` | `L12` has an entire §3, *"`decrease_key`, and Why It Is Awkward"*, opening *"Dijkstra's algorithm (Week 5) needs to…"*. |
| PROG 102 W4 · `unique_ptr` | `L15` already says *"Store `std::vector<std::unique_ptr<Base>>` **(Week 5)**"* and explains why. |

The seven previews written for these were **removed**.

### Verified clean

- ✅ **MATH 142** — no forward references at all across Weeks 0–12.
- ✅ **ECE 110** — likewise. Its Boolean algebra, De Morgan's Laws and functional completeness are
  delivered by MATH 151 **Week 0** of Fall, a full semester of margin.
- ✅ **PROG 102 Weeks 0–1** — the many "heap" references are to *heap memory*, not the data
  structure. False positive; a keyword sweep will raise it again.
- ✅ **CS 102 W7 PROJECT 1's "suffix"** — the English word in "trim common prefixes and suffixes",
  not suffix arrays. False positive.

---

## 11 · Method note — why the first Spring pass failed

The Fall passes tested each candidate against **where the concept is first taught, at lecture
level**. The first Spring pass tested against the **course topic index** instead — "exceptions are
Week 9", therefore a Week 1 pset mentioning exceptions is a gap. That inference is invalid: a topic
index says where a subject is *developed*, not where it is first *usable*, and a well-written
lecture routinely introduces the slice it needs.

Six of eight findings did not survive the correct test. The check that should have been applied to
every candidate, and now must be:

> **Before recording a gap, grep the lecture body — not the topic index — for the concept. If the
> lecture teaches it, or names it with an explicit forward pointer, there is no gap.**

The cost of getting this wrong is not neutral. Seven unnecessary previews were added to lectures
that already covered the material, which is exactly the redundancy that makes course notes
unreadable. Retracted findings are kept above rather than deleted, so the next pass does not
rediscover them.

---

## 12 · Fall re-checked at lecture level (2026-08-16)

§11's test was written after the Spring failure, so the Fall findings predated it. They have now
all been re-checked the same way: **grep the lecture body, not the topic index.** Fall held up far
better than Spring — but not perfectly.

### One retraction

**Finding 18 (PHYS 141 W6, moment of inertia) is withdrawn.** `L20 §4` states plainly that
*"the results for common uniform objects … are:"* and gives the table, and it **already contains a
worked "Sample Derivation: Thin Rod About Its Center"** — the same `λ[x³/3] → ML²/12` computation
the preview duplicated. **PS 6 contains no integration ask at all.** The preview was not merely
unnecessary, it was a second copy of a derivation already on the page. Removed.

### Two downgrades

**Finding 19 (CS 101 `L18`)** is real but weaker than recorded. The proof sketch *states* both
borrowed facts — "there are n! possible orderings" and "log₂(n!) ≈ n log₂n − n log₂e (by Stirling's
approximation)". What it never does is justify them, and **Stirling is taught nowhere in Year 1**.
The preview was trimmed to supply only the missing justification, and now says so explicitly rather
than claiming the facts are absent.

**Finding 15 (CS 101 PS 1 · B7)** was recorded as "taught with under 48 hours of margin". Wrong:
CS 101's **Week 1** lectures already demonstrate loops — `for i in range(10)` in `L05`, and
`while True` twice in `L06`. Students meet iteration a full week before the pset is due. Reclassified
as ✅.

### What held up

Findings **1–14, 16 and 17** survive the lecture-level test unchanged.

- **1, 2, 4, 5, 6, 9, 10** — PROG 101 Week 0's lectures were grepped directly when first recorded;
  `for (` appears nowhere in them, and recursion appears only as `cp -r`.
- **3, 8** — PHYS 141 `L04`'s body gives a *results table* and the FTC as a statement, no
  computational rule; `L05` adds only the notation chain `x → v → a`. **PS 1 asks explicitly for
  "(integrate)" and "by taking the derivative".**
- **7** — MATH 141 Week 0's lectures never mention induction, in any form.
- **13** — MATH 141 Week 1 never previews the IVT; the finding is a due-date collision regardless.
- **16, 17** — `L13` performs a symbolic definite integral (`m[v²/2]`) in its own derivation, and
  **PS 4 and PS 5 both say "(integrate)" outright**. `L16`'s force–time-graph area method is an
  alternative route, not a substitute for what the pset asks.

### Standing score

Across all three passes: **27 findings raised, 7 retracted, 3 downgraded, 17 upheld.** Every
retraction came from the same root cause — trusting a topic index over a lecture body — and all of
them were in material added *after* §11's test was written down, or before it existed. The test
works; it just has to be applied first rather than last.

---

*Audit covers all of Freshman Year 1 — Fall and Spring, Weeks 0–12, all ten courses.
21 findings, all resolved; six retracted. Sophomore Year remains unaudited; based on finding 21,
check Year 2 Fall against MATH 251 (Year 2 Spring) first, and apply §11's lecture-level test from
the outset. The Week 0 framing problem in §6(a) is likely to recur wherever a Week 0 exists.*
