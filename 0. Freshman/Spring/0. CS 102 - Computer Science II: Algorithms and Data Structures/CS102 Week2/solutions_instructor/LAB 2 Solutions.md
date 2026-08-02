# CS 102 — Lab 2: Solutions and Checkoff Guide
## Instructor Copy — Not for Distribution

**40 points.** Reference machine: Python 3.14.2, x86-64 Linux. All timings **best of 3 runs**.

---

## Checkoff Priorities

In a two-hour session most students will finish A–C. **Part D is where the learning is**, so if the
room is running behind, tell them at the 75-minute mark to stop tuning C and start D.

The three things to look at over a student's shoulder:

1. **Is `height` iterative?** A recursive height on a 100,000-node degenerate tree raises
   `RecursionError`, and students lose 20 minutes to it. Catch this in the first ten minutes.
2. **Did they run `check_avl` before timing?** Lab 0 made this point and this is the lab where
   ignoring it produces a plausible-looking table of meaningless numbers.
3. **Are they trying to build the plain BST at $n = 100{,}000$?** Stop them — see below.

---

## Part A — Instrument (10 pts)

Reference code is `ps2_ref.py` plus a rotation counter. Nothing new.

**A1 (3):** iterative `insert`, iterative `search`, **iterative `height`**. Deduct 2 for a recursive
`height`; it is explicitly called out in the handout.

**A2 (3):** global counter incremented in both rotation functions. Must report **both** the total for
a build and the maximum for a single insertion.

**A3 (4):** `check_avl` actually invoked. A student who has the function and never calls it gets 1.

---

## Part B — Heights (10 pts)

| $n$ (sorted) | BST $h$ | AVL $h$ | perfect | AVL rotations |
| --- | --- | --- | --- | --- |
| 1,000 | 999 | 9 | 9 | 990 |
| 10,000 | 9,999 | 13 | 13 | 9,986 |
| 100,000 | 99,999 † | 16 | 16 | 99,983 |

† **Not built.** Each insertion walks the whole right spine, so $h = n-1$ by construction. A
student who reports having measured this either used a different structure or is guessing — ask them
how long it took. *(For reference: measured directly, the $n = 32{,}000$ build takes 33.1 s and the
$n = 100{,}000$ build takes 307.5 s.)*

| $n$ (random, mean of 5) | BST $h$ | AVL $h$ | AVL rotations |
| --- | --- | --- | --- |
| 1,000 | 20.0 | 11.0 | 698 |
| 10,000 | 29.8 | 15.0 | 6,987 |
| 100,000 | 39.8 | 19.0 | 69,742 |

### B1 (5) / B2 (5) — the two questions

**"How does the AVL height compare to $\lceil\log_2(n+1)\rceil-1$? Is that a coincidence?"**

It is **equal** at all three sizes. Not a coincidence: sorted input drives every rebalance into the
RR case, and repeatedly rotating left as a right spine grows produces the most even shape available.
**The worst case for the BST is close to the best case for the AVL tree.**

**"How much does balancing buy you on random input?"**

Roughly a factor of 2 in height — 39.8 down to 19.0 at $n = 10^5$ — not the factor of 5,000 that
sorted input showed. The expected height of a random BST is already $\Theta(\log n)$ (Week 1, L06);
balancing improves the constant from about 4.3 to about 1.44, and removes the *variance*.

**The point to make in the room:** if you only ever benchmark on random data, balanced trees look
like a modest optimisation. **The reason to use them is the input you did not test.**

---

## Part C — Time (12 pts)

### C1 (6) — sorted build times, best of 3

| $n$ | BST | ratio | AVL | ratio |
| --- | --- | --- | --- | --- |
| 1,000 | 36.6 ms | — | 6.4 ms | — |
| 2,000 | 126.0 ms | 3.45 | 20.0 ms | 3.13 |
| 4,000 | 470.2 ms | 3.73 | 27.6 ms | 1.38 |
| 8,000 | 1802.4 ms | 3.83 | 61.8 ms | 2.24 |
| 16,000 | 7237.0 ms | 4.02 | 138.7 ms | 2.25 |

**The BST column is the clean result** — 3.45, 3.73, 3.83, 4.02, converging on 4 from below, exactly
$\Theta(n^2)$.

**The AVL column is noisy** — 3.13, 1.38, 2.24, 2.25 — and the 1.38 is a measurement artifact, not a
finding. At these sizes an AVL build takes tens of milliseconds and best-of-3 is not enough
repetition to suppress the variance.

> **Give full marks to any student who reports the noisy AVL column and says so**, and dock a point
> from anyone who reports a suspiciously smooth one without explaining how they got it. Reporting a
> measurement you do not trust, *and saying you do not trust it*, is the behaviour this course wants.
> Suggested follow-up for a student who finishes early: raise the repetition count and watch the
> column settle toward 2.2.

The theoretical $n\log n$ doubling ratio here is 2.19–2.30 (Lab 0, Part C2) — **not 2**.

### C2 (6) — searches, $n = 8{,}000$, sorted-built trees

| structure | height | 2,000 searches |
| --- | --- | --- |
| plain BST | 7,999 | 0.1949 s |
| AVL | 12 | 0.0011 s |

**Speedup ≈ 170×.** Accept 100–400×; it is sensitive to which keys are queried.

---

## Part D — Find the Crossover (8 pts)

### D1 (4)

| $n$ | BST | AVL | AVL/BST |
| --- | --- | --- | --- |
| 10 | 4.6 µs | 20.5 µs | 4.45 |
| 20 | 15.0 µs | 53.3 µs | 3.55 |
| 50 | 73.2 µs | 177.7 µs | 2.43 |
| 100 | 269.4 µs | 402.3 µs | 1.49 |
| 120 | 389.2 µs | 489.0 µs | 1.26 |
| 150 | 600.5 µs | 643.3 µs | **1.07** |
| 200 | 1148.9 µs | 924.4 µs | **0.80** |
| 500 | 6642.3 µs | 2639.1 µs | 0.40 |

**Crossover between $n = 150$ and $n = 200$** on the reference machine. At $n = 10$ the AVL tree is
**4.5× slower**.

Accept anything in the range 100–400. **Do not accept a crossover below 50 or above 1000** without
an explanation — that usually means single-run timing, or an AVL implementation recomputing heights
rather than caching them.

### D2 (4)

**"Property of the algorithms or of the machine?"** (2 pts)

**The machine and the language.** The asymptotics say AVL wins for all sufficiently large $n$; they
say nothing about where "sufficiently large" starts, and that is set entirely by constants — pointer
chasing, interpreter overhead, allocation. The same two algorithms in C would cross somewhere else.

Full marks require the student to distinguish *which* fact is machine-independent (that a crossover
exists, and its direction) from *which* is not (where it is).

**"Does it change what you ship?"** (2 pts)

Accept either side, argued:

- **No.** The plain BST's advantage is bounded by a small constant on tiny inputs; its disadvantage
  is unbounded. A library that cannot see its callers' data must not have a catastrophic case.
- **Yes, as a hybrid.** Real libraries do exactly this — CPython's `list.sort` switches to insertion
  sort below a threshold, for the same reason.

**Deduct for "always use the asymptotically better algorithm" with no engagement with the measured
crossover.** The entire lab was arranged to make that answer uncomfortable.

---

## Common Failures

**`RecursionError` on `height`.** Handled in A1; still catches people.

**Reusing a mutated list between structures.** A student who sorts in place, or reuses a list one
structure has consumed, produces a BST height of 999 at $n = 1000$ and an AVL build time that looks
too good. Symptom: the numbers are *better* than the reference table. **Better than reference is a
bug, not an achievement** — say this out loud early in the session.

**Timing with `time.time()`.** Resolution is too coarse for Part D's microsecond range.
`time.perf_counter()` is required, as in Lab 0.

**Averaging instead of taking a minimum.** For Part D, best-of-$k$ is right: the minimum is the run
least contaminated by scheduling noise. A mean at $n=10$ is dominated by outliers.

---

*CS 102 · Week 2 · Lab 2 Solutions · Instructor Copy · © CSE Department*
