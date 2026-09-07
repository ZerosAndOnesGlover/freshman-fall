# CS 102 · Lab 12 — Solutions and Checkoff Notes
## A TSP Approximation

**INSTRUCTOR / TA COPY — not for distribution**

---

## Before the Session

**This is the last lab, in final-exam week, with Project 2 and PS 11 both due Friday.** Students will
be at capacity.

Two administrative things to do **before** anything else:

1. **Check the lab register.** Anyone at nine completed labs must pass this one to progress. Tell them
   individually and at the start, not at the end.
2. **Say that Parts A–B are the compulsory core.** A student who completes A and B has passed the lab;
   C and D are where the marks and the content are, but nobody should fail progression because they ran
   out of time in exam week.

**Compute cost:** A2's $n = 20$ run takes about **15 seconds** and is the only slow step. Have students
launch it first and do Part B while it runs. **Warn them not to try $n = 24$** — it is about four
minutes and adds nothing.

---

## Part A — Exact, and the Wall (10)

### A1 (4), A2 (3) — machine-dependent

| $n$ | $2^n n^2$ | time |
| --- | --- | --- |
| 8 | 16,384 | 0.001 s |
| 12 | 589,824 | 0.022 s |
| 16 | 16,777,216 | 0.590 s |
| 20 | 419,430,400 | **14.8 s** |

*Mark the **ratios**, not the seconds. Each step of 4 in $n$ should multiply the time by roughly 25–30.*

### A3 (3)

Extrapolated: $n = 25$ ≈ **12 minutes**; $n = 30$ ≈ **9.5 hours**; $n = 40$ ≈ **2 years**.

*(These follow from the $n = 20$ timing and are machine-dependent; the orders of magnitude are not.)*

**The 1,000× machine**: the largest $n$ with $2^n n^2 \le 1000 \cdot 2^{40} \cdot 40^2$ is $n = 49$ —
**nine more cities**.

Expected observation: a thousandfold speedup buys about $\log_2 1000 \approx 10$ additional cities,
slightly fewer once the $n^2$ factor is included.
**That is the difference between exponential and polynomial growth**, and it is why the problem is not
solved by waiting for better hardware.

*3 requires the arithmetic. "It doesn't help much" without a number is 1.*

---

## Part B — The MST 2-Approximation (12)

### B1 (5), B2 (4) — deterministic ratios

| quantity | reference |
| --- | --- |
| worst approx / optimal | **1.3509** |
| instances exceeding 2× | **0** |
| worst MST / optimal | **0.8286** |

*Accept ratios within a few per cent from a different generator; the two structural facts — **no**
violations of 2×, and MST/optimal **never above 1** — must hold exactly. A student reporting MST/optimal
above 1 has a bug in their MST, not their tour.*

### B3 (3)

1. $\mathrm{MST} \le \mathrm{OPT}$ — deleting an edge from an optimal tour leaves a spanning tree.
2. The full preorder walk costs $2\cdot\mathrm{MST}$ — every tree edge is traversed twice.
3. **Shortcutting does not increase the cost — this is the triangle inequality.**

*The mark is for correctly identifying step 3. Students often point at step 1.*

---

## Part C — Break the Guarantee (8)

### C1 (4) — deterministic

| quantity | reference |
| --- | --- |
| worst ratio | **4.000** |
| exceeded 2× | **42 of 2,000** |

*Note it is only ~2% of instances. A student who runs 100 instances may see none and conclude the bound
still holds — worth a comment: this is the same "rare failure" phenomenon as Week 5's Dijkstra.*

### C2 (4) — the assessed question

**(a) (2)** **Step 3.** Shortcutting past a visited city replaces a path with a direct edge, and only
the triangle inequality guarantees the direct edge is no longer. Without it the shortcut can be
arbitrarily worse.

**(b) (2)** The measurement establishes that **this** algorithm exceeds 2× on **these** instances. The
theorem establishes that **no** polynomial algorithm achieves **any** constant factor on general TSP
unless P = NP — a statement about every algorithm that could ever be written, which no amount of
measurement could produce.

*(b) is the graded idea and it is the course's closing distinction: measurement refutes a specific
claim; a theorem rules out a whole space of possibilities. 2 for making that distinction; 1 for "the
theorem is more general".*

---

## Part D — A Heuristic With No Guarantee (10)

### D1 (4), D2 (3) — deterministic

| method | mean ratio | worst ratio | reached optimum |
| --- | --- | --- | --- |
| MST 2-approximation | 1.1145 | 1.3205 | — |
| **+ 2-opt** | **1.0051** | **1.1290** | **167 of 200** |

*A student whose 2-opt does not improve on the MST tour has an inequality backwards or is not
reversing the segment. A student whose 2-opt produces an invalid tour is reversing the wrong slice —
check the tour is still a permutation.*

### D3 (3) — the closing question

**(a) (2)** **No, 2-opt has no approximation guarantee**; there are instances where its local optimum is
arbitrarily far from optimal.

The D2 table establishes that 2-opt was excellent **on 200 metric instances of at most 10 cities**. It
establishes **nothing** about any other instance — and in particular nothing about the large instances
you would actually use it on, where exhaustive comparison is impossible by construction.

**(b) (1)** Ship **both**, or ship the approximation. Report the heuristic's tour as the answer *and*
the 2-approximation's bound as the guarantee: "here is a tour; it is provably within 2× of optimal."

*Accept "ship 2-opt but report the MST bound alongside it" as the best answer — that is what production
solvers do. Reject "ship 2-opt, it's better" without qualification: the question is what you can
**tell the user**.*

---

## Checkoff Checklist

1. A1 verified against brute force before any timing.
2. B2's MST/optimal ratio never exceeds 1.
3. B3 identifies **step 3** as the triangle inequality.
4. C1 uses at least 1,000 non-metric instances — 100 will show no violations.
5. D3(a) says 2-opt has **no** guarantee, and says what the table does not establish.

---

## Marking Summary

| Part | Points |
| --- | --- |
| A | 10 |
| B | 12 |
| C | 8 |
| D | 10 |
| **Total** | **40** |

**Progression: 10 of 13 labs required.** This is the last one. Confirm every student's count before
they leave the room, and record it the same day.

---

## Note for the Final Lecture

This is the last piece of practical work in CS 102, and Part D is the right place to end.

The measurement says the heuristic wins on everything measurable: half a per cent above optimal against
eleven, and the exact answer 84% of the time. The recommendation is still to carry the algorithm with
the theorem — **not because it performs better, but because it is the only one you can say anything
about**.

Part C is the same point from the other side. The proof has three steps; remove the triangle inequality
and nothing else, and the worst ratio goes from 1.35 to 4.0. **The guarantee was never a property of
the code.**

Both halves are the course's thesis in its final form, and it is worth saying out loud in the last
lecture:

> **Every algorithm in this course is correct under an assumption. Knowing what yours guarantees, and
> what it assumed in order to guarantee it, is what the subject consists of.**

The retrospective in [[CS102 Week12/resources/Course Retrospective|Course Retrospective]] develops this and is worth pointing students
at once the exam is behind them.

---

*CS 102 · Week 12 · Lab 12 Solutions · © CSE Department*
