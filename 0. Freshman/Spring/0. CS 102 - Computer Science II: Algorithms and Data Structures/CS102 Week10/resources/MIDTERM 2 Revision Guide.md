# CS 102 · MIDTERM 2 — Revision Guide

**Sat:** Monday 29 March 2027, 18:00–19:15 · Week 10 (evening, VNC 100) · **Covers Weeks 5–9** · **Worth 12.5%** of the final grade

**75 minutes.** Closed book. **One handwritten sheet, one side**, of your own notes is permitted. No
calculators — every number on the paper is exact or is a complexity class.

*(Format and weight per the Course Overview Syllabus, identical to Midterm 1.)*

---

## Format

| section | marks | content |
| --- | --- | --- |
| A — short answer | 20 | 8–10 one-or-two-sentence questions across all five weeks |
| B — trace and compute | 25 | Execute algorithms by hand on small inputs |
| C — **proof** | 30 | Two proofs from the list below |
| D — design and judgement | 25 | Choose an algorithm for a stated problem and defend it |
| **Total** | **100** | **75 minutes** |

**Note the change from Midterm 1**: Section C is worth 30 rather than 25, and Section D 25 rather than
30. **Weeks 5–9 are the proof-heavy half of the course**, and the paper reflects that.

---

## What Is Examinable

### Week 5 — Shortest Paths

- Relaxation, the two invariants, and the **path-relaxation property**.
- Optimal substructure of shortest paths, and where it fails (negative cycles).
- **Negative edges** (Dijkstra breaks, the problem is fine) versus **negative cycles** (the problem is
  ill-posed).
- Topological order two ways; DAG shortest **and longest** paths in $\Theta(V+E)$.
- Dijkstra, its proof, and **the one inequality that needs non-negativity**.
- Bellman–Ford as a dynamic program; the $V-1$ bound; early termination; negative-cycle detection.
- Choosing among BFS / DAG / Dijkstra / Bellman–Ford.

**Not examinable:** Kosaraju's proof of correctness (the algorithm and the idea are), A\* internals.

### Week 6 — Minimum Spanning Trees

- The **cut property** and its proof; the **cycle property**; why "some" and "strictly" are
  load-bearing.
- Distinct weights $\Rightarrow$ unique MST, and why the converse fails.
- Prim and Kruskal, and **the one expression separating Prim from Dijkstra**.
- Why MST algorithms need no assumption about the sign of the weights.
- Union-find with union by rank and path compression; what $\alpha(n)$ is and is not.
- The MST is **not** a shortest-path tree; it **is** a minimax tree.

**Not examinable:** the proof of the $O(m\,\alpha(n))$ bound; Borůvka's algorithm in detail.

### Week 7 — Dynamic Programming I

- Optimal substructure **and** overlapping subproblems; a problem failing each.
- Memoisation versus tabulation, and **when the choice matters by orders of magnitude**.
- LCS and edit distance: recurrences **with base cases**, traceback, space optimisation.
- $D_{\text{indel}} = |a| + |b| - 2\,\mathrm{LCS}$, and why substitution breaks it.
- 0/1 knapsack; **why $\Theta(nW)$ is not polynomial**; the loop-direction bug.

### Week 8 — Dynamic Programming II

- Interval DP: the split recurrence, and **filling by increasing length**.
- Matrix chain; optimal BSTs and why balance is the wrong objective there.
- "Ending at $i$" as a state; LIS both ways; why `tails` is not an LIS.
- Coin change and canonical systems.
- DP on trees; bitmask DP and what it does **not** achieve.
- **Floyd–Warshall**: the meaning of $d^{(k)}$, the loop order, negative cycles, path reconstruction.

### Week 9 — Greedy

- The **greedy-choice property** (some optimal solution, not every one) and optimal substructure.
- The **exchange argument** template.
- Activity selection and three rules that fail.
- Scheduling: total completion time, maximum lateness, and why the key changes with the objective.
- Fractional versus 0/1 knapsack, and the word that separates them.
- **Huffman**: the algorithm, the two-part proof, the entropy bound.

---

## Proofs You Should Be Able to Reproduce

Section C draws **two** from this list. Every one was done in lecture and set on a problem set.

1. **Dijkstra is correct for non-negative weights** — and identify the step that uses it. *(L17)*
2. **Bellman–Ford after $i$ rounds is correct for paths of $\le i$ edges**, by induction. *(L18)*
3. **DAG shortest paths in topological order** are correct. *(L16)*
4. **The cut property**, by exchange. *(L19)*
5. **The cycle property.** *(L19)*
6. **Distinct weights imply a unique MST.** *(L19)*
7. **Subpaths of shortest paths are shortest paths.** *(L16)*
8. **`BUILD-HEAP` is $\Theta(n)$** — carried from Midterm 1, still examinable. *(L11)*
9. **$D_{\text{indel}}(a,b) = |a|+|b|-2\,\mathrm{LCS}(a,b)$.** *(L23)*
10. **Floyd–Warshall's recurrence**, from the meaning of $d^{(k)}$. *(L27)*
11. **Earliest-finish-time is optimal** for activity selection, by exchange. *(L28)*
12. **Shortest-processing-time minimises total completion time**, by adjacent exchange. *(L29)*
13. **Earliest-deadline-first minimises maximum lateness**, by adjacent exchange. *(L29)*
14. **Fractional knapsack greedy is optimal**, by exchange. *(L29)*
15. **Huffman's greedy choice is safe** — the two least frequent symbols may be deepest siblings.
    *(L30)*

**Proofs 4, 11 and 15 are the most likely to appear.** All three are exchange arguments; if you can
write one properly you can write all of them, and **that single skill is the highest-value thing to
revise.**

### The exchange-argument template

1. Let $G$ be greedy's output and $O$ an optimal solution. Find the **first** place they differ.
2. **Modify $O$** to agree with greedy there. *Show the modification is legal and does not make $O$
   worse.*
3. $O'$ is still optimal and agrees with greedy one step further.
4. Repeat; after finitely many steps $O$ becomes $G$. $\square$

**Step 2 is the entire proof.** Steps 1, 3 and 4 are identical every time and can be written from
memory. If you are stuck in an exam, write 1, 3 and 4 first and then think about 2 — you will have the
structure on the page and marks for it.

---

## The Numbers Worth Carrying

You will not be asked to recall a measurement. You may be asked what one *implies*.

| fact | shape |
| --- | --- |
| Dijkstra with a heap | $O((V+E)\log V)$ — worse than $\Theta(V^2)$ on dense graphs |
| Bellman–Ford rounds needed | the graph's **hop-diameter**, $\Theta(\log V)$ on random graphs |
| Dijkstra on negative edges | wrong on ~2% of instances — **silently** |
| union-find, both optimisations | $\alpha(n) \le 4$ for any storable $n$; not a constant |
| 0/1 knapsack | $\Theta(nW)$ — one extra **bit** of $W$ doubles the time |
| memoisation vs tabulation | same complexity; up to **1,242×** difference in work |
| Floyd–Warshall loop order | 4 of 6 orderings wrong on ~35% of graphs |
| greedy coin change on $[1,5,6,9]$ | wrong on 42% of targets |
| Huffman | $H \le \bar\ell < H+1$ |

---

## The Idea the Second Half Has Repeated

Every week from 5 to 9 contains an algorithm that is **correct under an assumption** and fails
silently without it:

| week | algorithm | assumption | failure rate when violated |
| --- | --- | --- | --- |
| 5 | Dijkstra | non-negative weights | 2.3% of instances |
| 5 | A\* (Lab) | admissible heuristic | 51% of queries |
| 6 | single-linkage clustering | separated clusters | recovers 67% |
| 8 | greedy coin change | canonical denominations | 42% of targets |
| 9 | fewest-conflicts selection | *(none — it is simply wrong)* | survives 2,000 tests |

**Section D will give you a problem and ask which algorithm applies and why.** The "why" is a statement
about assumptions, and it is where the marks are.

---

## How to Revise

**Do not reread the lectures.** In order of value:

1. **Write out proofs 4, 11 and 15 from memory, on paper.** If you can do those three, Section C is
   safe.
2. **Hand-trace** Dijkstra, Bellman–Ford, Kruskal, an LCS table, a knapsack table, and Floyd–Warshall
   on 5-vertex or 6-character inputs. Section B is exactly this.
3. **Rework PS 5 Part C, Lab 8 Part B (the loop order), and PS 9 Part A3** without your solutions. Those three questions
   contain the second half's whole methodological point.
4. Reread the "Three Ideas Most Likely to Be Missed" in each week's README — five short sections,
   covering most of Section A.
5. Only then reread lecture material, and only what your own attempts showed you needed.

---

## Practical

- **Lecture 31 (the morning of the paper)** runs as normal and its material is **not** on this paper.
- **Quiz 10 runs that Monday at 09:00** as usual and covers Week 9 — the same material as Section A here.
- **PS 9 is due Friday 2 April**, after the paper; **PS 10 is released that same Friday**.
- **PROJECT 2 is assigned that Monday** and due Friday 16 April. Do not start it before the midterm.
- Past papers are on the course page.

---

*CS 102 · MIDTERM 2 Revision Guide · © CSE Department*
