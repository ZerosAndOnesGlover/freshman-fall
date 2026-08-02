# CS 102 · Lab and Quiz Record
## Not part of the course grade

> **This file is deliberately outside the gradebook's weighted components.** Both labs and quizzes
> carry **0% weight** — the curriculum's assessment line (*Problem Sets 35%, Midterms 25%, Final 20%,
> Projects 20%*) sums to 100% without them.
>
> The leading underscore in the filename keeps this file out of `tools/gpa.py`'s course scan. Do not
> rename it without checking `collect()` in that script.

---

## Why This Is a Separate File

An earlier draft put these tables at the bottom of `CS 102.md`, under an unweighted subheading. The
gradebook parser reads a component's items from its heading until the **next `##` heading that
contains a percentage** — and an unweighted subheading has none. The eleven quiz rows were therefore
silently absorbed into **Project 2**, which reported 12 items instead of 1.

It did not change any computed grade, because the rows were blank. **It would have** as soon as
anyone entered a quiz mark. Keeping unweighted records in their own file removes the failure mode
rather than relying on nobody filling in a row.

---

## Labs — Completion Gate

**A student must satisfactorily complete at least 10 of the 13 labs to pass CS 102**, regardless of
weighted average. Mark `✓`, `partial`, or leave blank.

| Lab | Week | Topic | Complete? |
|---|---|---|---|
| Lab 0 | 0 | Implement and benchmark three CS 101 sorts | |
| Lab 1 | 1 | Visualise tree traversals interactively | |
| Lab 2 | 2 | BST vs AVL on sorted input | |
| Lab 3 | 3 | Heap sort against merge sort | |
| Lab 4 | 4 | BFS/DFS on social network data | |
| Lab 5 | 5 | Route planning on a real road network | |
| Lab 6 | 6 | Network cable layout optimiser | |
| Lab 7 | 7 | Visualise DP tables filling | |
| Lab 8 | 8 | Floyd–Warshall | |
| Lab 9 | 9 | Compress a file with Huffman coding | |
| Lab 10 | 10 | Plagiarism detector | |
| Lab 11 | 11 | 2D nearest-neighbour searcher | |
| Lab 12 | 12 | TSP approximation | |

**Labs completed:** ____ / 13 &nbsp;&nbsp; **Gate met (≥ 10):** ☐

---

## Quizzes — Formative

15 minutes at the start of Monday's lecture. **Quiz *N* covers Week *N−1*.** Marked out of 20 and
returned, so that a gap shows up before an exam makes it expensive.

| Quiz | Week given | Covers | Out of | Score |
|---|---|---|---|---|
| Quiz 1 | 1 | Week 0 — review, algorithm design process | 20 | |
| Quiz 2 | 2 | Week 1 — binary trees and BSTs | 20 | |
| Quiz 3 | 3 | Week 2 — balanced BSTs | 20 | |
| Quiz 4 | 4 | Week 3 — heaps and priority queues | 20 | |
| Quiz 5 | 5 | Week 4 — graph representations and traversals | 20 | |
| Quiz 6 | 6 | Week 5 — shortest paths | 20 | |
| Quiz 7 | 7 | Week 6 — minimum spanning trees | 20 | |
| Quiz 8 | 8 | Week 7 — dynamic programming principles | 20 | |
| Quiz 9 | 9 | Week 8 — dynamic programming applications | 20 | |
| Quiz 10 | 10 | Week 9 — greedy algorithms | 20 | |
| Quiz 11 | 11 | Week 10 — string algorithms | 20 | |

*There is no Quiz 0 (Week 0 has no preceding week) and no Quiz 12 (Week 12 is the final exam week).*

---

*CS 102 · Lab and Quiz Record · © CSE Department*
