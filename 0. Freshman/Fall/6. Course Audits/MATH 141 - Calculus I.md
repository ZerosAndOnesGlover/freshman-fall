# MATH 141 — Calculus I: Limits, Derivatives, and Integrals — Course Audit

**Question:** Do the quizzes, problem sets, and labs of each week require knowledge that the lectures have not yet taught at the time the work is completed?

**Method:** For each week (0–12), lectures, reference sheet, overview, problem set, lab, and quiz were read. A *gap* is material required by an assignment/lab/quiz but not present in that week's or any earlier week's lectures. Reference/cheat sheets count as acceptable formula coverage (noted where relevant). Quizzes cover the *previous* week by design — fine unless a quiz needs something taught later. Computational tools (Python, bisection, Simpson, sympy/scipy) are flagged where assumed but never demonstrated.

**Conventions in use:** Problem Set N released Wednesday of Week N, due Wednesday of Week N+1 "at the start of class" (the due window intentionally spans the following week's Monday/Tuesday lectures — documented only for PS1). Lectures run Monday–Wednesday. Labs run Friday. Quizzes run Monday morning.

---

## Week 0 — Algebra and Selected Topics Review
**Lectures cover:** Algebra, functions, graphs (review; no lecture files — materials only).
**Deliverables require:** PS 0 mostly algebra/functions review; LAB 00 includes a forward-looking derivative-preview question.
**GAPS:**
- `Problem Set 0.md` #2c is a two-part **"proof by induction"** problem — induction is never taught anywhere in this course.
- The LAB 00 derivative-preview item is explicitly a preview.
**Verdict:** Minor stretch (induction in PS 0 #2c is the one genuinely unsupported method).

## Week 1 — Limits
**Lectures cover:** L01 limit intuition/one-sided; L02 limit laws, ε-δ, continuity; L03 *infinite limits/limits at infinity* (the Week 1 Overview instead describes Wednesday as continuity + IVT).
**Deliverables require:** PS 1 limits/laws/squeeze (aligned); Part D IVT/continuity extension. LAB 01 (Friday W1, graded): discontinuity types, continuous extension, IVT, bisection, absolute max/min claims.
**GAPS:**
- **LAB 01 requires Week-2 material** (discontinuity classification, continuous extension, IVT, bisection, EVT-flavored claims) completed Friday of Week 1, before any Week-2 lecture. Mitigation: `Week 1 Reference Sheet.md` carries those statements.
- PS 1 is rescued by a documented re-date pushing Part D to Friday of Week 2 (after the IVT lecture).
**Verdict:** Significant gaps (with reference-sheet mitigation).

## Week 2 — Continuity and the Intermediate Value Theorem
**Lectures cover:** L01 Continuity, L02 Types of Discontinuity, L03 IVT.
**GAPS:** LAB 02 assumes Python's `fractions.Fraction` with no introduction (minor tool note). No conceptual gaps.
**Verdict:** Aligned (minor tool note).

## Week 3 — The Definition of the Derivative
**Lectures cover (definition-only week):** L01 derivative definition, L02 derivative as a function, L03 differentiability/continuity. **No differentiation rules are taught in Week 3.**
**Deliverables require:**
- **PS 3 Part B (36 pts, the largest part)** applies the power, product, quotient, chain, exponential and trig rules; Part F1 needs the product rule; Part G is a quotient-rule *proof*.
- **LAB 03 (graded, Friday W3):** power/sum rules, product-rule verification with trig values, `x^(2/3)` fractional-power rule, **concavity/inflection reasoning (a Week-7 topic)**.
**GAPS:**
- **PS 3 Part B requires the differentiation rules taught Week 4 (Mon/Tue)** — feasible only because the due time is Wednesday morning of Week 4, after the W4 lectures.
- **LAB 03 is the sharpest instance of a lab completing before its material's lectures:** rules, trig derivative values, and concavity (Week 7) are all required Friday W3.
- `Week 3 Overview.md` and `Week 3 Reference Sheet.md` **advertise the full rule table, chain rule, and exponential/e trig derivatives as Week 3 content**; the sheet's own schedule puts rules on Wednesday W3 while L03 is actually — and L01 itself says "Next: Tuesday — Differentiation Rules," contradicting the actual Tuesday lecture. The sheet's "(ln x)': 1/x … (Next week)" note proves the deferral was known at authoring time but never reflected in schedules.
**Verdict:** Significant gaps (rules-heavy PS 3 Part B + graded LAB 03 land before the rules are taught; concavity in LAB 03 is Week 7). Mitigation: reference sheet carries the formulas.

## Week 4 — Differentiation Rules, Chain Rule, Higher Derivatives
**Lectures cover:** L01 rules (Mon), L02 chain rule (Tue), L03 higher derivatives/rates (Wed).
**GAPS:** PS 4 A6 (`ln(x²+1)`) needs `(ln x)' = 1/x`, present only in the Week 4 Reference Sheet (never taught in lectures) — minor, the sheet provides it. Doc slip: W4 L02 header claims "Problem Set 2 … Due: Wednesday, Week 3" (off-by-two).
**Verdict:** Aligned (one minor ln note + doc slip).

## Week 5 — Implicit Differentiation, Logs & Inverse Trig, Related Rates
**Lectures cover:** L01 implicit, L02 log-diff + inverse trig, L03 related rates.
**GAPS:** None material (F2 previews `F_x, F_y` notation with the formula given inline — minor). Doc slips: W5 L03 header due-date off-by-one.
**Verdict:** Aligned.

## Week 6 — Extrema, MVT, L'Hôpital's Rule
**Lectures cover:** L01 extrema/EVT/critical points/closed-interval method, L02 Rolle/MVT, L03 L'Hôpital.
**Deliverables require:**
- **PS 6 Parts C (derivative tests, concavity, inflection), D (Second Derivative Test), E (curve sketching) = Week 7 L01/L02 content** — feasible only because the deadline is the week-7 Wednesday morning window (tightest such window in the course).
- **LAB 06 (Friday W6):** Part 3 f/f'/f'' interplay and concavity; Part 4 Second Derivative Test + failure mode — **all taught Monday of Week 7, after the Friday lab**.
**GAPS:**
- LAB 06's curve-shape/second-derivative content is Week 7 L01 material. Mitigation: `Week 6 Reference Sheet.md` carries the full "Shape of a Graph" content.
- Both the W6 reference sheet's schedule and L01's own note advertise I/D and Derivative Tests a week early vs. the actual lectures.
**Verdict:** Significant stretch (LAB 06); PS 6 C–E rescued by the due-after-Mon/Tue cadence but is the tightest window.

## Week 7 — Shape of the Graph, Curve Sketching, Applied Optimization
**Lectures cover:** L01 shape tests + concavity, L02 curve sketching, L03 applied optimization.
**GAPS:** None material. Doc slips in L01/L03 headers (PS numbers / due weeks off).
**Verdict:** Aligned.

## Week 8 — Riemann Sums, the Definite Integral, and Its Properties
**Lectures cover:** L01 Riemann sums, L02 definite integral, L03 properties.
**PS 8** goes out of its way to **exclude the FTC** ("The FTC is not on this problem set"), so nothing requires Week 9. LAB 08 gives its midpoint code inline.
**GAPS:** None material. Doc slips (W8 L02 says derivative MVT is "Week 4" — it is Week 6; footer promises "Wednesday — The Fundamental Theorem of Calculus," but Wednesday is Properties).
**Verdict:** Aligned.

## Week 9 — The Fundamental Theorem of Calculus
**Lectures cover:** L01 FTC 1 + proof, L02 FTC 2 / evaluation, L03 accumulation / functions defined by integrals.
**GAPS:**
- **LAB 09 Part 1A asks students to "implement Simpson's rule" with no formula given anywhere.** Lectures only name-drop Simpson (W8 L01, W9 L01 CS-connections; W11 sheet); the lab offers no code (contrast LAB 08's midpoint code). A student must know/derive Simpson's rule or substitute a midpoint integrator. Minor but a genuine "tool never demonstrated" gap.
- Doc slips (W9 L01 header PS/due mislabels).
**Verdict:** Aligned (minor Simpson's gap in LAB 09; doc mislabels).

## Week 10 — Substitution, Symmetry, Integration by Parts
**Lectures cover:** L01 substitution, L02 substitution + symmetry (with proofs), L03 parts/LIATE.
**LAB 10:** tabular method is **taught fully inside the lab** (L03 L03 explicitly defers it there) — fine.
**GAPS:** None material. (PS 10 totals 157 + 4 bonus points vs. the usual 100 — a rubric inconsistency, not a content gap. The W10 sheet advertises trig integrals/trig substitution "next week," which never appears in Week 11 — deferred to MATH 142.)
**Verdict:** Aligned (rubric and doc inconsistencies only).

## Week 11 — Applications of Integration
**Lectures cover:** L01 area between curves, L02 volumes disks/washers, L03 shells + accumulation/work.
**GAPS:** None.
**Verdict:** Aligned.

## Week 12 — Review, Taylor Preview, Final Preparation
**Lectures cover:** L01 review/synthesis, L02 Taylor polynomials **preview**, L03 final prep.
**Deliverables:** PS 12 optional/ungraded (comprehensive revision, solutions provided, no Taylor); LAB 12 ungraded; final exam comprehensive Weeks 0–12 with Taylor marked a preview and its coefficient an allowed note item.
**GAPS:** None — review/preview by design.
**Verdict:** Aligned.

---

# End-to-End Summary

Four recurring patterns:

1. **Reference sheets and overviews advertise pacing one week ahead of the actual lectures.** Concrete instances: Week 3 (rule table / chain / exp-derivatives scheduled for Wednesday W3, actually taught Week 4; the sheet's own "(Next week)" tag on `(ln x)'` shows the deferral was known); Week 6 (I/D and First/Second Derivative Tests scheduled Wednesday W6, actually taught Monday W7). The sheets *do* provide the formulas, functioning as a mitigation.

2. **Graded Friday labs frequently require material taught the following Monday/Tuesday.** LAB 01 (W1) needs W2's discontinuity/IVT/bisection; LAB 03 (W3) needs W4's rules + a W7 concavity idea; LAB 06 (W6) needs W7's curve-shape/second-derivative content. This is the only category where a graded deliverable is indisputably completed before the teaching — and it is inconsistent (labs 04,05,07,08,10,11,09 all land after their material), so a scheduling defect rather than a policy.

3. **The PS_N due-window design does most of the heavy lifting.** PS released Wed of week N, due Wed of week N+1 deliberately spans the following Mon/Tue lectures — what makes PS 3 Part B and PS 6 C–E feasible in practice. The tightest window is PS 6 C–E; the only true misses are the graded Friday labs (pattern 2).

4. **Pervasive off-by-one metadata.** Lecture headers and sheet schedules repeatedly mislabel PS numbers and due weeks (e.g., "Problem Set 6 released today" in W9 L01; "PS7 Released" in the W10 sheet; "Due: Wednesday, Week 3/4/6/8" in W4–W7 headers). Doesn't affect grading but misleads students planning their week.

**Tool note.** Numerical methods (bisection, central differences, Simpson, Riemann integrators) are celebrated but never taught — labs hand over code stubs. The one place this becomes a real requirement is LAB 09 Part 1A (Simpson's rule, no formula). `fractions.Fraction` (LAB 02) and random sampling (LAB 08) similarly assumed.

**Bottom line:** Weeks 2, 4, 5, 7, 8, 9, 10, 11, 12 aligned (allowing the small noted items). Weeks 1, 3, 6 contain the only real sequencing gaps: **Week 3 is the worst** (rules advertised as taught, yet PS 3's largest part and the graded LAB 03 require them before/at the start of Week 4 — and LAB 03 even touches Week-7 concavity), **Week 1** (LAB 01 needs Week-2 material), **Week 6** (LAB 06 needs Week-7 curve-shape content, rescued only by the reference sheet).
---

# Verification and Fixes (2026-09-21)

Each claim was checked against the lecture bodies. Every problem set and lab was then cut back so it uses
only its own week and earlier weeks. That is stricter than the "due next Wednesday" window this audit
allowed. Every problem set is now 100 points and carries a "What this uses" box.

| Claim | Verdict and fix |
|---|---|
| W0 PS 0 #2c needs induction | **Upheld.** Replaced; 6(a) limit replaced by "put h = 0"; bonus removed |
| W1 Lab 01 needs Week 2 (discontinuity types, IVT, bisection) | **Upheld.** Parts 2 and 4 removed |
| W1 PS 1 Part D (IVT) rescued by a re-date | **Upheld, fixed differently.** Part D and the continuity items removed; PS 1 rebuilt to 100 |
| W3 PS 3 Part B needs the Week 4 rules | **Upheld.** PS 3 rewritten definition-only. The old key also wrongly said $x^2\sin(1/x)$ is not differentiable at 0 — it is |
| W3 Lab 03 needs rules and concavity | **Upheld.** Rule items switched to the definition; concavity removed |
| W3 overview / reference sheet advertise rules | **Upheld.** Schedule corrected; rule table marked "Preview — Week 4" |
| W4 PS 4 A6 needs $(\ln x)'$ (Week 5) | **Upheld.** Changed to $\sqrt{x^2+1}$ |
| W5 aligned | **Confirmed.** But PS 5 was 140 points; cut to 100. F2 needed partial derivatives, which are never taught; removed. The A2 key never finished $y''$; now $-18/(2y-x)^3$ (SymPy) |
| W6 PS 6 C–E (Week 7) | **Upheld.** Removed. Also found: PS 6 had **no L'Hôpital questions** though Lecture 03 teaches it; a L'Hôpital part was added. The D2 key's "proof" was not a proof; rewritten |
| W6 Lab 06 Parts 3–4 (Week 7) | **Upheld.** Part 3 now uses $f$ and $f'$ only; Part 4 is L'Hôpital numerically |
| W6 reference sheet carries Week 7 shape content | **Upheld.** Shape sections moved to the Week 7 sheet; L'Hôpital moved to Week 6, where it is taught |
| W7 aligned | **Confirmed.** But PS 7 was 167 points, 50 of them L'Hôpital (Week 6); cut to 100. The Week 7 Overview described Monday as L'Hôpital; corrected |
| W8 aligned | **Confirmed.** Dated only |
| W9 Lab 09 Simpson's rule | **Upheld.** 1A now reuses the Lab 08 midpoint rule (printed in the lab); every key value recomputed |
| W10 PS 10 157 + 4 points | **Upheld.** Cut to 100 (no bonus). The W10 sheet promised trig integrals "next week"; corrected |
| W11–12 aligned | **Confirmed.** Dated only |
| Off-by-one metadata in lecture headers | **Upheld.** Seven headers fixed (W2, W4, W5, W7 ×2, W9, W10) and seven reference-sheet schedules re-labelled |

**Also found and fixed:**

- **Answer keys inside student handouts.** PS 2, PS 4, PS 9 and PS 11 printed their full keys below the
  questions. Each key was moved to `solutions_instructor/PS N Solutions Instructor Only.md`.
- **Dates.** All work is now dated from Monday 21 September 2026:
  - Lectures: Mon–Wed 11:00.
  - Quizzes: Mon 11:00–11:15.
  - Problem sets: released Wed 12:00, due the next Wed 11:00.
  - Labs: Fri 15:00–16:50, a new slot added to the timetable, with reports due Mon 17:00.
  - Lab 00: Fri 25 September.

**Left for you to decide (flagged in the files):**

1. **Final-exam format.** The Week 12 materials say 3 hours with one side of A4. The syllabus and the
   registry say 150 minutes (09:00–11:30, Wed 23 Dec) with a 2-page sheet.
2. **Exam weights.** The syllabus and gradebook use 15/15/20; the Year 1 Assessment Calendar says
   20/20/40.
3. **Holidays on MATH days.** Lab 09 falls on Fri 27 Nov, the day after Thanksgiving, and PS 7 is released
   on Veterans Day (Wed 11 Nov).
4. **Ungraded work listed as graded.** Lab 00 and Lab 12 are ungraded by their own text but are listed at
   100 points in the gradebook. I marked them "leave blank".

---

# Workload and Tools Rework (2026-09-26)

The 2026-09-21 pass fixed untaught *mathematics* but left two faults, which the student reported on
starting Lab 00:

1. **Untaught tools.** Lab 00 used `numpy` and `matplotlib` (no course teaches them). Later labs asked for
   loops and functions before CS 101 had taught them, or said "Python (optional)" and then required code.
2. **Volume.** Problem sets ran 17–27 parts, and labs 15–26 questions with reflections, against a 110-minute
   session.

**Standard applied** (chosen by the student):
- **Problem sets:** about 3 hours, roughly 8 problems and 15 parts, 100 points.
- **Labs:** fit the session, with at most 30 minutes of write-up.
- **Quizzes:** 15 minutes.
- **Tools:**
  - Graphs in Desmos. Lab 00 has a how-to table.
  - Computation in plain Python, using only what CS 101 lectures have taught by the lab's date (CS 101
    lectures run Wed/Thu/Fri 09:00):
    - W0: REPL arithmetic.
    - W1: `math`.
    - W2: `if`, `while`, `for` over a list.
    - W3 on: `def`, `lambda`.
  - No `numpy`, `matplotlib`, `sympy` or `fractions`.
- **No repeats.** Where a problem set and its lab shared a problem, the problem stays in one of them only.

| Week | Problem set | Lab | Also found |
|---|---|---|---|
| 0 | 12 → 8 problems (35 → 16 parts) | numpy/matplotlib → Desmos + REPL arithmetic; 12 questions | Quiz 00 diagnostic 50 → 12 questions. Lab key worked $x^2$ at $x=3$, not the lab's $x=1$ |
| 1 | 11 → 8 (≈22 → 12 parts, 2 ε-δ proofs) | 15 → 11 questions, `math` only | Q3b said Desmos draws a filled dot at 0 |
| 2 | 14 → 8 | "implement, then take a tolerance" (a function, W3) → supplied `while` loop; 7 questions | Lab bisected the PS's own cubic; now $x^3-2x-5$ |
| 3 | 11 → 7 | ≈25 → 9 questions with `def` | Lab's numerical part used $\sin'=\cos$ (Week 4) → $\sqrt x$ |
| 4 | 18 → 14 parts | 11 → 6 questions | Lab repeated PS 4 A1, A8 and the whole motion part; marginal-cost "what controls the error" needed Taylor (W12) |
| 5 | ≈27 → 13 parts | ≈26 → 7 questions | Folium point $(2,2)$ not on $x^3+y^3=6xy$; now $(3,3)$ |
| 6 | ≈26 → 12 parts (midterm week) | ≈25 → 7 questions | Lab classified max/min (First Derivative Test, W7); lab re-used PS L'Hôpital limits |
| 7 | 13 → 7 problems (2 sketches) | ≈20 → 6 questions, 1 sketch | Grid search was "run mentally" |
| 8 | 15 → 8 problems (10 parts) | 25 → 6 questions | Average-value key used the FTC (W9); now $2x+1$ by geometry. `random.uniform` explained in the lab |
| 9 | 13 → 8 | 15 → 6 questions | Three PS problems repeated the lab |
| 10 | 25 → 14 parts (midterm week) | ≈20 → 6 questions | Lab pointed to a PS integral that did not exist |
| 11 | 13 → 9 | 2B removed | Four PS problems repeated the lab; "Simpson's rule in ten lines" (never taught) in the lab and the W11 sheet |
| 12 | unchanged (optional 3-hour mock) | Part 1 now one Part of PS 12 | The lab asked for the whole 3-hour PS 12 in 45 minutes |

Quizzes 01–12 were checked and left alone: each is 5–7 short items in 15 minutes.

Answer sheets in `4. Submissions` were regenerated only where still `not-started` and unchanged since
the last submissions commit. PS and lab headings are now `## Problem N` / `### Question N (pts)`, so
each sheet has one box per problem.
