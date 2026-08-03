# CS 102 · Course Retrospective

**Not examinable. Read it after the final.**

---

## What You Built

Thirteen weeks, thirty-nine lectures, eleven problem sets, thirteen labs and two projects. Laid out
plainly, the inventory is larger than it felt:

| you can now | from |
| --- | --- |
| analyse an algorithm's cost and **measure** whether the analysis predicts reality | Week 0 |
| implement and reason about BSTs, AVL trees, red-black trees, B-trees | Weeks 1–2 |
| implement heaps and priority queues, and prove the linear build | Week 3 |
| traverse graphs, classify edges, find components and cycles | Week 4 |
| compute shortest paths under four different assumptions | Week 5 |
| build minimum spanning trees and disjoint-set structures | Week 6 |
| recognise and design dynamic programs | Weeks 7–8 |
| prove greedy algorithms correct by exchange | Week 9 |
| match strings four ways and index a fixed text | Week 10 |
| compute geometric predicates and spatial indices | Week 11 |
| **recognise when to stop looking for a fast algorithm** | Week 12 |

Plus a working `diff` and a working search engine, which are real programs.

---

## The Six Things Worth Keeping

Most of the algorithms above you will look up when you need them. These six are the residue — the part
that stays after the details go.

### 1. The weakest sufficient invariant is the right one

Week 2 counted the tree shapes each balance condition permits: size-balance allows **1** shape at
$n = 7$, AVL allows **17**, and only the second can be repaired in $O(1)$. Week 3's heap is weaker
still, and that is what buys the $\Theta(n)$ build and the pointer-free layout.

**Stronger invariants are more expensive to maintain, not more useful.** Ask what you actually need.

### 2. Asymptotics do not tell you which implementation is faster

This appeared **six** times, always with the same cause and always surprising in the moment:

| week | the asymptotically worse thing won |
| --- | --- |
| 2 | `SortedList` beat a hand-written AVL tree by 16× |
| 3 | `sorted()` beat `heapq.merge` by 2.4× |
| 6 | Kruskal beat Prim on dense graphs; union-find cost 1.8× the sort |
| 8 | Floyd–Warshall never beat $V$ Dijkstras, even on complete graphs |
| 10 | sorting suffixes directly beat prefix doubling below $n \approx 10^4$ |
| 11 | brute-force scan beat a k-d tree from 16 dimensions up |

**Complexity tells you the shape of the curve. It does not tell you where you are on it**, and it says
nothing about whether the inner loop is compiled.

### 3. A bound is a count of operations, not a promise about time

BFS is $\Theta(V+E)$ and its cost per edge grew **5×** on random graphs and **1.5×** on grids across the
same size range. `sift_down` doubles its memory stride at every step. Memory locality is not in the
notation and it is often the thing that decides.

### 4. Testing refutes; only proof establishes

The sharpest demonstration in the course: for activity selection, the **fewest-conflicts** rule is
optimal on all 2,000 random instances anyone would generate — and it is wrong. Breaking it took about
43,000 randomised trials and needed ten intervals.

Alongside it: Dijkstra silently wrong on 2.3% of negative-weight instances; greedy coin change wrong on
42% of targets for $[1,5,6,9]$; four of six Floyd–Warshall loop orderings wrong a third of the time.

**None of these is visible in the code, and none is caught by a small test suite.** An exchange
argument is three sentences and it is the only thing that settles the question.

### 5. Verify against something independent — and check the verifier

Twice this term the *reference implementation* was the broken component: PS 4's circular check of the
parenthesis theorem, and PS 10's longest-repeated-substring reference built on `str.count`, which
counts non-overlapping occurrences and disagrees with the correct answer on **22%** of random strings.

**"My two implementations disagree" does not tell you which one to fix.**

### 6. Every algorithm is correct under an assumption

The thesis. Dijkstra guarantees a shortest path *given non-negative weights*. Kruskal guarantees an MST
*given the cut property*. Huffman guarantees an optimal code *given independent symbols and integer
bits*. A convex hull guarantees the right polygon *given exact arithmetic* — and gets **19%** of them
wrong in floating point. The MST tour is within 2× *given the triangle inequality* — and reaches 4×
without it.

**Knowing what your algorithm guarantees, and what it assumed in order to guarantee it, is what the
subject consists of.**

---

## What Was Deliberately Uncomfortable

Several things in this course were designed to be annoying, and it is worth saying why.

**You were asked to break your own code.** PS 5 Part C had you find the input on which your Dijkstra
fails. PS 9 Part A3 had you spend real effort breaking a rule that looks correct. PS 11 Part D had you
establish that your working convex hull is wrong on realistic input. **This is the habit that
distinguishes an engineer from someone who writes code that passes.**

**You were told the textbook advice and then shown it failing.** "Prim for dense graphs" lost every
measurement. "Kruskal's cost is dominated by the sort" is asymptotically true and measurably false.
Received wisdom is a hypothesis.

**Proofs were marked as proofs.** From Week 9 onward, a correct answer with no argument scored about a
third. That was not pedantry — it is the only part of the work that transfers to a problem nobody has
solved for you.

---

## What Comes Next

| course | connection |
| --- | --- |
| **CS 250 Discrete Mathematics** | the proof techniques used here, done properly |
| **CS 301 Theory of Computation** | Week 12 expanded: automata, decidability, complexity classes |
| **CS 310 Databases** | B-trees (Week 2), external sorting, query planning as optimisation |
| **CS 320 Operating Systems** | scheduling (Week 9), caches (the whole term's second theme) |
| **CS 340 Machine Learning** | k-d trees and the curse of dimensionality (Week 11), optimisation |
| **CS 350 Networks** | shortest paths (Week 5) as routing protocols |
| **CS 401 Advanced Algorithms** | randomisation, amortisation, approximation, LP duality |

**Week 12 is the doorway to most of them.** Complexity theory is the subject that says which of these
problems anyone will ever solve efficiently.

---

## If You Take One Thing

Twelve weeks ago the question was *how do I make this faster*.

It is now:

> **What does my algorithm guarantee, on what inputs, under what assumptions — and how would I know if
> those assumptions stopped holding?**

That question is worth more than every algorithm in the syllabus, because the algorithms are all
written down somewhere and the question is not.

---

*CS 102 · Course Retrospective · © CSE Department*
