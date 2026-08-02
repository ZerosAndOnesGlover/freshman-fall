# CS 102 · Problem Set 2: Solutions
## Instructor Copy — Not for Distribution

**100 points.** All code below was executed; all output shown is real.

---

## Part A — Rotations (16 pts)

### A1 (4) — the rotations

```python
def rotate_right(y):
    global ROTATIONS; ROTATIONS += 1
    x = y.left
    y.left = x.right
    x.right = y
    update_height(y); update_height(x)     # y BEFORE x
    return x

def rotate_left(x):
    global ROTATIONS; ROTATIONS += 1
    y = x.right
    x.right = y.left
    y.left = x
    update_height(x); update_height(y)     # x BEFORE y
    return y
```

**Marking:** 1 pt each for the correct three pointer assignments; 1 pt each for the height updates
**in the right order**. A submission with the updates reversed loses 1 pt on each function; note it
explicitly in feedback, because it will resurface as a mysterious failure in B2.

### A2 (4) — subtree BST check

```python
def check_bst(t, lo=None, hi=None):
    if t is None: return True
    if lo is not None and t.key <= lo: return False
    if hi is not None and t.key >= hi: return False
    return check_bst(t.left, lo, t.key) and check_bst(t.right, t.key, hi)
```

**Marking:** 0 of 4 for the child-only test (`t.left.key < t.key < t.right.key`). This was Week 1's
headline error and PS 1 E3; it is not a slip by Week 2.

### A3 (8) — the test, and the broken version

```
A3: rotation order-preservation, 500 random trees ... PASS
```

**Marking:** 4 pts for a test that runs 500+ random trees and compares inorder sequences. 4 pts for
the deliberate-breakage report.

Accept any breakage that changes the **order**, e.g. `y.left = x.left`. With that change the test
fails on the first tree with a non-empty left subtree, typically reporting a duplicated key and a
dropped one.

**Award the 4 pts in full, and add a written note, to any student who observes that swapping the two
`update_height` lines does *not* fail this test.** That is the correct and non-obvious answer: the
inorder sequence is untouched by a height bug. The problem statement flags this; students who
engaged with it should be told they were right to.

---

## Part B — AVL Insertion (30 pts)

### B1–B2 (18) — `avl_insert`

See `ps2_ref.py`, reproduced in Lecture 08 §2. Marking for B2:

| | pts |
| --- | --- |
| BST descent correct, duplicates handled | 3 |
| `rebalance` called on the way back up, on **every** path node | 3 |
| LL and RR cases | 4 |
| LR and RL cases, with the inner rotation first | 4 |

**The single most common wrong answer** is testing `bf(t.left) <= 0` rather than `< 0` in the LR
branch. It is wrong, and **it cannot fail on this problem set**: during insertion the child's balance
factor is never $0$ when the parent's is $\pm 2$.

*(Instrumented and verified: over 164,045 rebalance events during random insertions, the child's
balance factor was $0$ on **zero** occasions. Under deletion the same instrumentation sees it
routinely — 22 of 70 events in a single trial.)*

Do not deduct — but flag it in writing, because the identical code applied to deletion is a live bug.
Worth a sentence in the Week 3 lecture.

### B3 (6) — `check_avl`

Must raise on all three of: order violation, **stored** height disagreeing with the recomputed one,
and $|\mathrm{bf}| > 1$. 2 pts each. The stored-height check is the one that earns its keep; a
checker that recomputes heights and never compares them to `t.height` gets 4 of 6.

### B4 (6) — stress test

```
B4: AVL stress, 200 trials, checked after every insertion ... PASS
```

Full marks require: checking after **every** insertion (not once at the end), duplicates and
negatives in the key set, and comparison against `sorted(set(keys))`.

---

## Part C — Measuring (18 pts)

Reference output. **Heights and rotation counts are deterministic and must match exactly.**

### C1 (6) / C2 (6) — sorted input $0 \dots n-1$

| $n$ | BST $h$ | AVL $h$ | perfect | AVL rotations | max rot / insert |
| --- | --- | --- | --- | --- | --- |
| 1,000 | 999 | 9 | 9 | 990 | **1** |
| 10,000 | 9,999 | 13 | 13 | 9,986 | **1** |
| 100,000 | 99,999\* | 16 | 16 | 99,983 | **1** |

\* Not built. Each insertion walks the entire right spine, so $h = n-1$ by construction. A student
who reports a *measured* value here either used a different structure or fabricated it — ask.

Two things to draw out in the returned feedback:

- **The AVL height equals the perfect height at all three sizes.** Not a coincidence: sorted input
  drives every rebalance into the RR case, and the resulting shape is the most even one available.
- **Maximum rotations per insertion is 1, not 2.** Sorted input never produces a double rotation,
  which is exactly why the problem statement warns against testing only with sorted keys. A student
  whose LR and RL branches are dead code will still produce this table perfectly.

### C3 (6) — random input, mean of 5 seeds

| $n$ | BST $h$ | AVL $h$ | AVL rotations |
| --- | --- | --- | --- |
| 1,000 | 20.0 | 11.0 | 698 |
| 10,000 | 29.8 | 15.0 | 6,987 |
| 100,000 | 39.8 | 19.0 | 69,742 |

Seed-dependent, so accept anything within ±1 on BST height. **AVL heights are essentially
seed-independent** — 11.0, 15.0, 19.0 with zero variance across the five seeds at every size — and a
student reporting a fractional AVL height has averaged something else.

The one-sentence answer for C3: the plain BST is feasible at $n = 10^5$ on random input because its
expected height is $\Theta(\log n)$, so the build is $\Theta(n\log n)$, not $\Theta(n^2)$.

---

## Part D — The Height Bound (24 pts)

### D1 (8)

**The recurrence.** A minimal AVL tree of height $h$ has a root and two subtrees. One must have
height exactly $h-1$. The other has height $h-1$ or $h-2$ by the invariant; taking $h-2$ minimises
the node count. Both subtrees must themselves be minimal, since a non-minimal one could be replaced.
Hence $N(h) = N(h-1) + N(h-2) + 1$. Base cases: $N(0)=1$ (single node), $N(1)=2$.

**The identity.** Claim $N(h) = F(h+3) - 1$ with $F(0)=0, F(1)=1$.

*Base:* $N(0) = 1 = F(3) - 1 = 2 - 1$. ✓  $N(1) = 2 = F(4) - 1 = 3 - 1$. ✓

*Step:* assume for all $k < h$, $h \ge 2$. Then
$$N(h) = N(h-1) + N(h-2) + 1 = \big(F(h+2)-1\big) + \big(F(h+1)-1\big) + 1 = F(h+2)+F(h+1)-1 = F(h+3)-1. \;\square$$

**Marking:** 4 for the recurrence *with* the justification that both subtrees must be minimal
(a bare assertion of the recurrence earns 2), 4 for the induction. Strong induction is required —
two base cases and two inductive hypotheses. Deduct 2 for a single base case.

### D2 (6)

$n \ge N(h) = F(h+3) - 1$, so $n + 1 \ge F(h+3)$.

$F(k) = \frac{\varphi^k - \psi^k}{\sqrt5}$ with $\psi = \frac{1-\sqrt5}{2}$, $|\psi| < 1$, so
$|\psi^k|/\sqrt5 < 1/\sqrt5 < \tfrac12$ and hence $F(k) > \varphi^k/\sqrt5 - \tfrac12$. Therefore

$$n + 1 > \frac{\varphi^{h+3}}{\sqrt5} - \frac12
\;\Longrightarrow\; \varphi^{h+3} < \sqrt5\left(n + \tfrac32\right)
\;\Longrightarrow\; h < \log_\varphi\!\left(n + \tfrac32\right) + \log_\varphi\sqrt5 - 3.$$

Since $\log_\varphi x = \log_2 x / \log_2\varphi = 1.4404\log_2 x$ and $\log_\varphi\sqrt5 = 1.6723$:

$$h < 1.4404\log_2\!\left(n + \tfrac32\right) - 1.3277 \;\le\; 1.4404\log_2(n+2) - 1.3277.$$

**Marking:** 2 for the $F(k)$ lower bound, 2 for the algebra, 2 for correct numerical constants.
Accept the $n + \frac32$ form — it is tighter and equally correct.

### D3 (6)

**$n = 2, 7, 20$.** *(Verified by exhaustive check over $n = 1 \dots 500{,}000$: the $n+1$ form is
violated exactly 13 times, at $n = 2, 7, 20, 54, 143, 376, 986, 2583, 6764, 17710, 46367, 121392,
317810$.)*

What is special: **each is $N(h)$ for an odd $h$** — 2 = N(1), 7 = N(3), 20 = N(5). These are the
sizes at which the worst-case height is actually attained, so they are precisely where a bound that
is off by a hair must fail. Accept any answer identifying them as minimal-AVL-tree sizes; award the
full 6 for noticing the odd-$h$ pattern, 4 for identifying them as $N(h)$ values without it.

### D4 (4)

- **Minimum:** $N(10) = 232$.
- **Maximum:** a perfect tree of height 10, $2^{11} - 1 = 2047$.

2 pts each, both requiring justification. A common error is $2^{10}$ or $2^{10}-1$ for the maximum —
a height-10 tree has 11 levels under the edge convention.

---

## Part E — Reasoning (12 pts)

### E1 (3)

An insertion raises a subtree's height by 1. The rotation at the lowest violating node **gives that
level back** — the rebalanced subtree has exactly its pre-insertion height — so every ancestor sees
an unchanged child and needs no repair. The recursion continues only to update heights.

A deletion *lowers* a subtree's height. The rotation that repairs the resulting imbalance can lower
it again, which is a fresh violation for the parent. The repair therefore propagates, and can reach
the root. *(Measured: on a Fibonacci tree of height 18 with 10,945 nodes, one deletion required 9
rotations — exactly $h/2$, and $h/2$ is $\Theta(\log n)$.)*

**Marking:** the phrase to look for is *the rotation restores the original subtree height*. Without
it, 1 pt.

### E2 (3)

**AVL for read-heavy workloads.** A lookup table built once and queried constantly: the AVL tree is
16 tall on 100,000 sorted keys against the red-black tree's 30, and every single query pays that
difference. Nearly twice the comparisons per lookup, forever.

**Red-black for update-heavy workloads, especially with deletions.** Bounded rotations on both
operations — at most 2 per insert and 3 per delete, measured — against AVL's $\Theta(\log n)$
deletion, plus one bit of metadata per node instead of an integer.

**Marking:** 3 pts requires citing measured numbers from Lecture 09 §3, as the question demands. An
answer that says only "AVL is more balanced, red-black rebalances less" earns 1 — and note in
feedback that the second half of that sentence is false for insertion on sorted input.

### E3 (3)

The size-balanced invariant leaves almost no freedom of shape. At $n = 7$ there is **exactly one**
legal tree, against 17 AVL-legal shapes and 429 BSTs. With no slack, an insertion cannot be absorbed
locally: inserting a new minimum into a size-balanced tree of 255 nodes changes the left-subtree size
of **253 of them**.

The cost is $\Theta(n)$ per insertion — worse than the sorted array the whole exercise was meant to
improve on. The invariant is not wrong; it is **too strong to maintain**, which is the general lesson
of Lecture 07 §2.

Accept any concrete sequence forcing global restructuring. Full marks require naming the cost.

### E4 (3)

`SortedList` is a list of ~1,000-element sublists. Its inner loop is a `list` slice assignment,
which is a `memmove` over contiguous memory in C. The AVL tree executes interpreted function calls
and dereferences pointers into scattered heap objects. **Moving 1,000 contiguous machine words costs
less than 17 interpreted comparisons**, so the structure with the worse asymptotic complexity wins by
16× at $n = 10^5$.

The AVL tree wins when the constant gap closes or the asymptotic gap opens: implemented in C rather
than Python, or at $n$ large enough that $\sqrt n$-style sublist movement dominates $\log n$ — or on a
workload `SortedList` does not support cheaply. **Any one of these, argued, earns the third point.**

---

## Grade Distribution Note

Parts A–B are mechanical and should be near-full for most of the cohort. **The separation happens in
D1 (strong induction, done properly) and E1 (the insert/delete asymmetry).** If E1 is widely missed,
recover it at the start of Week 3 — the same reasoning pattern returns when we argue that heap
`sift_down` costs $O(n)$ in aggregate.

---

*CS 102 · Week 2 · PS 2 Solutions · Instructor Copy · © CSE Department*
