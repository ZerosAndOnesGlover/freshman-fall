# CS 102 · Computer Science II — Algorithms and Data Structures
## Week 9: Greedy Algorithms

**Assessment for this course (overall):** Problem Sets 35%, Midterms 25%, Final 20%, Projects 20%
**This week's deliverables:** **PS 9** (released Fri 26 Mar 10:00, due **Fri 2 Apr 17:00**), Lab 9 (**Tue 30 Mar**, 15:00), **Quiz 9** (Mon 22 Mar, 09:00) — which covers Week 8.
**PROJECT 1 IS DUE FRIDAY 26 MARCH, 17:00** — 10% of the course.
**MIDTERM 2 is Monday 29 March, 18:00–19:15** (Week 10), covering Weeks 5–9.

---

### Why This Week Exists

Dynamic programming considers every option and remembers the results. A **greedy** algorithm makes one
choice, commits to it, and never reconsiders — no table, usually one sort and one pass. **When greedy
works it is strictly better.**

The difficulty is entirely in the "when", and you have already watched it fail:

> **Week 8**, coin change with $[1, 5, 6, 9]$. Greedy takes the largest coin that fits. For $T = 11$ it
> takes $9{+}1{+}1$; the optimum is $5{+}6$. It is wrong for **84 of the first 199 targets** — and
> right on every real currency, because currencies are designed so that it is.

**Nothing in the code distinguishes the two cases.** So this week is not about writing greedy
algorithms — it is about **proving** them, and the proof is the deliverable.

The technique is the **exchange argument**, and you have met it twice: Week 5's Dijkstra correctness
and Week 6's cut property are both this shape. Take an optimal solution, find where it first disagrees
with greedy, and show you can make it agree without making it worse.

### Learning Objectives

By the end of Week 9, you should be able to:

1. State the **greedy-choice property** and optimal substructure, and say which one DP also needs.
2. Write an exchange argument: what is exchanged, why it is legal, why it is no worse.
3. Prove earliest-finish-time optimal for activity selection, and break three rival rules.
4. Choose the sorting key from the **objective**, and prove it — for total completion time, for
   maximum lateness, and for fractional knapsack.
5. Identify the single word in a problem statement that makes greedy work or fail.
6. Implement Huffman coding with a heap, and encode and decode with real bit packing.
7. Prove Huffman optimal in two parts, and state the product whose sign settles Part 1.
8. State the entropy bound $H \le \bar\ell < H+1$ and construct a case where the overhead is nearly 1.
9. Say what Huffman's optimality is optimality *relative to*.

### This Week's Materials

| File | Purpose |
| --- | --- |
| [[L28 The Greedy Paradigm and Exchange Arguments]] | The paradigm, the template, activity selection, and three rules that fail |
| [[L29 Scheduling and Fractional Knapsack]] | Three exchange arguments, and where divisibility is load-bearing |
| [[L30 Huffman Coding]] | The algorithm, the two-part proof, entropy, and real measurements |
| [[PS 9 Greedy Algorithms and Huffman]] | 100 points, due Fri 2 Apr 17:00 |
| [[CS102 Week9/assignments/QUIZ 9 Week 9 Monday\|QUIZ 9 Week 9 Monday]] | 20 points, formative — **covers Week 8** |
| [[LAB 9 Compressing a File with Huffman]] | A real codec, and three results the theory does not predict |
| [[CS102 Week9/resources/Reading Guide Week 9\|Reading Guide Week 9]] | CLRS §15.1–15.3, with §15.2 flagged as the section that matters |
| `solutions_instructor/` | PS 9 and Lab 9 solutions — instructor only |

### The Three Ideas Most Likely to Be Missed

**1. A greedy rule can pass 2,000 tests and be wrong.** For activity selection, the "fewest conflicts"
rule was optimal on **all 2,000** random instances. Finding a counterexample took about **43,000**
randomised trials and needed **ten** intervals; none exists with six or fewer. **Testing refutes greedy
rules cheaply and can never establish one.** That asymmetry is the week.

**2. The sorting key follows the objective, not the input.** Shortest-duration-first is *provably
optimal* for minimising total completion time and *wrong on 62%* of instances for minimising maximum
lateness. Same jobs, same machine, same code shape — only the objective changed.

**3. Huffman is optimal, and loses to `gzip` by 2×.** Measured on Lab 9's corpus: Huffman gives
**86,136 bytes**, `zlib` gives **44,208**. `zlib` uses the same Huffman — it wins because LZ77 runs
first and sees repeated *words*, which Huffman cannot, because it assumes symbols are independent.
**Optimality is always relative to a model**, and an optimal algorithm for the wrong model loses to a
decent one for the right model.

### One Word, Two Problems

| problem | greedy | why |
| --- | --- | --- |
| **fractional** knapsack | **optimal** | you can move $\varepsilon$ of weight, so the bag is always exactly full |
| **0/1** knapsack | suboptimal on **11%**, worst ratio **0.412**, and unboundedly bad in general | an item is indivisible; the exchange is unavailable |

With $W = N$ and items $(1,2)$ and $(N,N)$, greedy achieves **2** against an optimum of **$N$**. Greedy
on 0/1 knapsack has **no** approximation guarantee — not a poor constant, none at all. One word in the
problem statement separates a $\Theta(n\log n)$ provably-optimal algorithm from an NP-complete problem.

### A Note on the Measurements

**Counts are deterministic** — every failure count, every verification total, and every figure in
Lab 9. The Huffman codec's output is deterministic in *size* but not in the specific codewords: ties
give different trees with identical total cost, so mark bit counts and not bit strings.

The entropy bound was checked on 2,000 distributions with **0 violations on each side**, and Huffman
landed **0.029 bits per character** above the floor on the Lab 9 corpus — far better than the
guaranteed +1.

### Connections

**Back:** The exchange argument is **Week 6**'s cut property and **Week 5**'s Dijkstra proof, now named.
Huffman is built on **Week 3**'s priority queue. Coin change and its failure are **Week 8**. Fractional
against 0/1 knapsack closes the loop with **Week 7**, where the indivisible version needed a DP.

**Forward:** **MIDTERM 2 (Week 10)** covers Weeks 5–9 and will ask for an exchange argument — four of
those five weeks contain one. **Week 10**'s string algorithms use Huffman-compressed data as a running
example. **Week 12** returns to greedy in the approximation setting: when the greedy-choice property
fails you settle for a provable ratio instead, which is the sequel to this week's unbounded gap on 0/1
knapsack, and Week 6's MST supplies the 2-approximation for TSP.

---

*CS 102 · Week 9 · © CSE Department*
