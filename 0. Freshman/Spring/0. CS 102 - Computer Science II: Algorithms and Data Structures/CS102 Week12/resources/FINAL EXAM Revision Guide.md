# CS 102 · FINAL EXAM — Revision Guide

**Sat:** Wednesday 21 April 2027, 09:00–11:30 · finals week (VNC 100) · **Comprehensive — Weeks 0–12** · **Worth 20%** of the final grade

**150 minutes** — a mark a minute, written to be finishable in about 135. Closed book. **Two handwritten sheets** (both sides) of your own notes are permitted.
No calculators.

*(Format and weight per the Course Overview Syllabus.)*

---

## Format

| section | marks | content |
| --- | --- | --- |
| A — short answer | 25 | 10–12 one-or-two-sentence questions across the whole course |
| B — trace and compute | 30 | Execute algorithms by hand on small inputs |
| C — **proof** | 45 | Three proofs from the list below |
| D — design and judgement | 50 | Three scenarios: choose, justify, state what you assumed |
| **Total** | **150** | scaled to 20% of the course |

**Section D is worth a third of the paper.** It is not recall. You are given a problem with sizes, an
operation mix and a constraint, and asked what you would use, why, and **what your choice assumes**.

---

## What Is Examinable

Everything. It is a comprehensive paper. But the weighting follows the course:

| weeks | topic | approximate share |
| --- | --- | --- |
| 0–3 | analysis, trees, balanced BSTs, heaps | 20% |
| 4–6 | graphs: traversal, shortest paths, MSTs | 25% |
| 7–9 | dynamic programming, greedy | 25% |
| 10–11 | strings, geometry, spatial structures | 20% |
| 12 | NP-completeness and approximation | 10% |

**Not examinable:** the Cook–Levin proof; red-black insertion/deletion code; the $\alpha(n)$ bound's
proof; Ukkonen's algorithm; sweep-line implementation details; anything marked "not examinable" in a
lecture.

---

## The Proofs

Section C draws **three**. Every one was done in a lecture and set on a problem set.

**Analysis and amortisation**

1. `BUILD-HEAP` is $\Theta(n)$, including evaluating $\sum h/2^h$. *(L11)*
2. KMP is $\Theta(n+m)$, by the potential argument on $k$. *(L31)*
3. The monotone-chain hull scan is $\Theta(n)$ after sorting. *(L34)*

**Trees**

4. $N(h) = F(h+3) - 1$ and the AVL height bound. *(L08)*
5. A red-black tree has $h \le 2\log_2(n+1)$. *(L09)*
6. A rotation preserves the inorder sequence. *(L07)*

**Graphs**

7. BFS computes shortest paths, via queue monotonicity. *(L14)*
8. A digraph is cyclic **iff** DFS finds a back edge. *(L15)*
9. Dijkstra is correct for non-negative weights — **and name the step that uses it**. *(L17)*
10. Bellman–Ford is correct after $i$ rounds for paths of $\le i$ edges. *(L18)*
11. The **cut property**, by exchange. *(L19)*
12. Floyd–Warshall's recurrence, from the meaning of $d^{(k)}$. *(L27)*

**Dynamic programming and greedy**

13. Subpaths of shortest paths are shortest paths. *(L16)*
14. $D_{\text{indel}} = |a| + |b| - 2\,\mathrm{LCS}$. *(L23)*
15. Earliest-finish-time is optimal for activity selection. *(L28)*
16. Earliest-deadline-first minimises maximum lateness. *(L29)*
17. Huffman's greedy choice is safe. *(L30)*

**Approximation**

18. The matching-based vertex cover is a 2-approximation. *(L39)*
19. The MST tour is a 2-approximation for **metric** TSP. *(L39)*

**Most likely: 11, 15, 17, 19** — all four are exchange or bounding arguments of three or four
sentences. **If you can write those four you have covered Section C**, because the others share their
structure.

### The two templates

**Exchange argument** (greedy, MST, Huffman):
take an optimal solution, find the first disagreement with your algorithm, modify it to agree *without
making it worse*, repeat. **Step three is the proof; the rest is boilerplate.**

**Amortised / potential argument** (`BUILD-HEAP`, union-find, KMP, Kasai, hull scan):
identify a quantity that increases at most $n$ times in total, show the expensive operation strictly
decreases it, conclude the total work is bounded by the total increase.

---

## The Course's Thesis

Section D is built on one idea, and it appeared every single week:

> **Every algorithm is correct under an assumption. Know what yours guarantees, and what it assumed in
> order to guarantee it.**

| week | algorithm | assumption | what happens without it |
| --- | --- | --- | --- |
| 2 | `SortedList` beats AVL | small $n$, CPython | reverses in C |
| 3 | heap sort's $O(1)$ space | cache-resident | 1.6× slower than merge sort at $10^6$ |
| 4 | BFS is $\Theta(V+E)$ | operations, not time | 5× per-edge degradation on random graphs |
| 5 | Dijkstra | non-negative weights | wrong on 2.3% of instances |
| 5 | A\* | admissible heuristic | 51% of routes suboptimal, up to 75% too long |
| 6 | single-linkage clustering | separated clusters | recovers 67% |
| 7 | knapsack $\Theta(nW)$ | $W$ small | one extra bit doubles the time |
| 8 | Floyd–Warshall | `k` outermost | 4 of 6 orderings wrong ~35% of the time |
| 8 | greedy coin change | canonical denominations | wrong on 42% of targets |
| 9 | fewest-conflicts selection | *(nothing — it is wrong)* | survives 2,000 tests |
| 10 | Boyer–Moore is sublinear | large alphabet | worse than KMP on binary |
| 11 | convex hull | exact arithmetic | 19% of hulls have the wrong vertex count |
| 11 | k-d tree | low dimension | slower than a linear scan at $d = 16$ |
| 12 | MST TSP tour | triangle inequality | ratio 4.0, bound violated |

**Learn this table.** Not the numbers — the *shape*. Section D will hand you a scenario and ask which
algorithm and why, and the "why" is a statement about assumptions.

---

## How to Revise

**Do not reread the lectures.** In order of value:

1. **Write out proofs 11, 15, 17 and 19 from memory, on paper.** That is Section C.
2. **Hand-trace**, on 6-element inputs: an AVL insertion, `BUILD-HEAP`, BFS and DFS with timestamps,
   Dijkstra, Kruskal, an LCS table, a knapsack table, Floyd–Warshall, a KMP failure function, a
   monotone-chain hull. Section B is exactly this list.
3. **Reread the "Three Ideas Most Likely to Be Missed" in all thirteen READMEs.** That is about twelve
   pages and covers most of Section A.
4. **Rework PS 5 C, PS 8 E4, PS 9 A3, and PS 11 D.** Those four questions contain the course's
   methodological content: an algorithm that fails silently, a loop order that is wrong a third of the
   time, a greedy rule that survives testing and is wrong, and a proof that does not survive floating
   point.
5. **Fill your two sheets by writing, not copying.** The act of compressing the course onto two sides
   is most of the revision; the sheets themselves are a bonus.

### Your two sheets

Suggested contents, in priority order:

- the **two proof templates** above, written out;
- the **assumptions table**, one line each;
- the complexity table: every algorithm, its cost, and its precondition;
- the recurrences: $N(h)$, LCS, edit distance, knapsack, Floyd–Warshall, Bellman–Ford;
- index arithmetic for 0-indexed heaps, and the AVL rotation cases;
- the four DP state patterns: prefix, interval, "ending at $i$", subset.

**Do not copy code onto them.** You will not be asked to reproduce an implementation, and the space is
worth more spent on recurrences and preconditions.

---

## Practical

- **PROJECT 2 and PS 11 are both due Friday 16 April**, five days before the paper. **Plan the week,
  not the day.**
- Lab 12 is optional, self-paced revision (solutions Monday 19 April) — the best practice there is for
  Section D. It is not part of the lab gate, which Labs 0–11 decide.
- Past papers are on the course page. The two most recent match this syllabus; earlier ones predate the
  geometry week.
- The course retrospective in [[CS102 Week12/resources/Course Retrospective|Course Retrospective]] is not examinable and is worth twenty
  minutes after the exam.

---

*CS 102 · FINAL EXAM Revision Guide · © CSE Department*
