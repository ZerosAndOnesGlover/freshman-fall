# CS 102 — Lab 2
## BST versus AVL on Sorted Input

**Week 2 · 2-hour lab session · 40 points**
**Deliverable:** `lab2.py` and `RESULTS.md`. In-lab checkoff by your TA.

> **Labs carry no direct weight** in CS 102, but **you must satisfactorily complete at least 10 of
> the 13 labs to pass the course.** See the syllabus.

---

## Purpose

Lecture 07 opened with a table showing a plain BST reaching height 99,999 on sorted input while an
AVL tree reached 16. **This lab makes you produce that table**, and then makes you find the point
where the practical consequence actually bites.

You may reuse your PS 2 code. If PS 2 is not finished, the AVL insertion in Lecture 08 is complete
and correct — use it, and say so in `RESULTS.md`. **The measurement is the assessed work here, not
the tree.**

---

## Part A — Instrument (10 pts)

**A1.** *(3)* A plain BST with iterative `insert` and `search`, and a `height(t)` that is **iterative**
(an explicit stack). A recursive height on a degenerate tree of 100,000 nodes overflows the stack, and
finding that out at the wrong moment costs you half the lab.

**A2.** *(3)* An AVL tree with a **global rotation counter**. Report both the total rotations for a
build and the maximum for any single insertion.

**A3.** *(4)* `check_avl(t)` from PS 2 B3, called after the last insertion of every build. **Do not
measure a structure you have not verified** — Lab 0 made this point and this lab is where ignoring it
gets expensive.

---

## Part B — Heights (10 pts)

**B1.** *(5)* Build the AVL tree from the sorted keys $0 \dots n-1$ for
$n \in \{1000, 10000, 100000\}$, and the plain BST for $n \in \{1000, 10000\}$ **only**.
Tabulate: BST height, AVL height, $\lceil\log_2(n+1)\rceil - 1$, AVL total rotations.

> **Do not build the plain BST at $n = 100{,}000$ from sorted input.** It is $\Theta(n^2)$ — around
> $5\times10^9$ pointer steps — **307 seconds** on the reference machine, and it will eat your lab session.
> Put the height in the table anyway; you can state it exactly without running anything, and doing so
> is part of B1.

**B2.** *(5)* Repeat with **random** keys at the same three sizes, averaged over 5 seeds. Tabulate BST
height, AVL height, AVL total rotations.

Two questions to answer in `RESULTS.md`:

- In B1, how does the AVL height compare to $\lceil\log_2(n+1)\rceil - 1$? Is that a coincidence?
- In B2, how much does balancing buy you? **Less than you expect** — say how much, and why.

---

## Part C — Time (12 pts)

**C1.** *(6)* Time the **build** from sorted input for $n \in \{1000, 2000, 4000, 8000, 16000\}$, both
structures. Report milliseconds and the doubling ratio for each.

You should see two clearly different ratios. Name the complexity class each one indicates.

> Do not push the BST past $n = 16{,}000$ without checking the clock first. It is quadratic; the run
> at $n = 16{,}000$ took **7.2 seconds** on the reference machine, so $n = 64{,}000$ would take about
> two minutes.

**C2.** *(6)* Fix the trees built from sorted input at $n = 8{,}000$ and time **2,000 random
successful searches** in each. Report both times and the ratio.

---

## Part D — Find the Crossover (8 pts)

This is the part that matters.

**D1.** *(4)* At small $n$, the AVL tree is **slower** than the plain BST on sorted input — it does
the same work plus rotations and height bookkeeping. Find, by measurement, the smallest $n$ at which
the AVL build becomes faster. Search over $n = 10, 20, 50, 100, 200, 500, \dots$ and use a best-of-5
timing at each.

**D2.** *(4)* Answer both:

- Is that crossover a property of the two algorithms, or of your machine and Python? Justify.
- Suppose you are writing a library and you do not know how many keys callers will insert. Does D1's
  answer change what you ship? Say why.

---

## Submission

- `lab2.py` — runnable end to end, producing every table.
- `RESULTS.md` — the tables from B, C, D, and your answers. **Include your machine and Python
  version**, as in Lab 0.

---

## Marking

| Part | Points | Focus |
| --- | --- | --- |
| A | 10 | Correct instrumentation, verified before measurement |
| B | 10 | Heights, sorted and random |
| C | 12 | Timings and doubling ratios |
| D | 8 | The crossover, and what it does and does not mean |
| **Total** | **40** | |

---

## Reference Numbers

From the machine these notes were prepared on (Python 3.14, x86-64 Linux). **Your timings will
differ. Your heights and rotation counts should not** — they are deterministic given the input.

| $n$ (sorted) | BST height | AVL height | perfect | AVL rotations |
| --- | --- | --- | --- | --- |
| 1,000 | 999 | 9 | 9 | 990 |
| 10,000 | 9,999 | 13 | 13 | 9,986 |
| 100,000 | 99,999 | 16 | 16 | 99,983 |

Build times, **best of 3 runs**:

| $n$ (sorted) | BST build | AVL build |
| --- | --- | --- |
| 1,000 | 36.6 ms | 6.4 ms |
| 4,000 | 470.2 ms | 27.6 ms |
| 16,000 | 7237.0 ms | 138.7 ms |

**If your heights disagree with this table, you have a bug — find it before you time anything.** A
BST height that is not exactly $n-1$ on sorted input means your insert is not doing what you think.

---

## A Note on What This Lab Is Really Testing

The headline result — 7.2 seconds against 0.14 — is not the interesting part. You were told that in
lecture and you would have believed it without measuring.

**Part D is the interesting part.** Balancing is not free, and there is a range of $n$ where it is a
straightforward loss. Knowing that range for your own machine is what separates "I use AVL trees
because they are $O(\log n)$" from an engineering judgement.

---

*CS 102 · Week 2 · Lab 2 · © CSE Department*
