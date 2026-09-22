# CS 102 · Problem Set 3 — Solutions
## Heaps and Priority Queues

**INSTRUCTOR / TA COPY — not for distribution**

Every number here was produced by running code. Where a student's figure should match exactly, it is
marked **deterministic**; where it will not, it is marked **machine-dependent**.

---

> **Revised 2026-09-22.** The old Part D (measuring build swaps) was removed: Lecture 11 §4 already
> reports those numbers. The old Part E is now Part D, and items were re-weighted to keep 100 points.
> Where a breakdown inside an item still quotes the old points, scale it in proportion.

## Part A — The Array Representation (18)

### A1 (4)

```python
def left(i):   return 2*i + 1
def right(i):  return 2*i + 2
def parent(i): return (i - 1) // 2
```

**(a) depth** of index $i$ is $\lfloor \log_2(i+1) \rfloor$, i.e. `(i+1).bit_length() - 1`.
Deterministic check, $i = 0 \dots 14$: `0,1,1,2,2,2,2,3,3,3,3,3,3,3,3`.

**(b) leaves** are the indices $\lfloor n/2 \rfloor \dots n-1$ — that is $\lceil n/2 \rceil$ of them.
Index $i$ is a leaf iff $2i+1 \ge n$.

**(c) height** of the heap is $\lfloor \log_2 n \rfloor$ (edges). Check, $n = 1\dots 17$:
`0,1,1,2,2,2,2,3,3,3,3,3,3,3,3,4,4`.

*Award 1 each for the three functions collectively, then 1 per correct formula.* A common error in
(b) is giving $n/2$ rather than $\lceil n/2\rceil$ — accept $\lfloor n/2\rfloor \dots n-1$ as the
index range, which is what matters.

---

### A2 (10)

**(a) (2)** $i//2 = (i-1)//2$ iff $i$ is odd.

Write $i = 2k$: then $i//2 = k$ and $(i-1)//2 = (2k-1)//2 = k-1$. They differ.
Write $i = 2k+1$: then $i//2 = k$ and $(i-1)//2 = (2k)//2 = k$. They agree.

Since $\mathrm{left}(i) = 2i+1$ is always odd and $\mathrm{right}(i) = 2i+2$ always even, **the buggy
formula is correct for every left child and wrong for every right child.**

*Full marks require both the parity argument and the left/right consequence. The consequence alone,
asserted, scores 1.*

**(b) (4)** **Deterministic. $n = 7$.**

One witness: inserting $0, 1, 4, 2, 5, 6, 3$ yields `[0, 1, 4, 2, 5, 6, 3]`, in which index 6 holds
3 under parent index 2 holding 4 — so $4 > 3$ violates the heap property.

Minimality: exhaustive search over all permutations of $n \le 6$ finds **no** failing ordering; at
$n = 7$, **432 of the 5,040** orderings fail.

*Accept any of the 432 witnesses. Award 2 for a correct $n$ with a valid witness, 2 more for the
exhaustive check at all smaller sizes. A student who reports $n = 7$ without checking $n \le 6$ has
not answered the question — cap at 2.*

**(c) (2)** **Deterministic.** Increasing input produces a **valid heap at every size tested**
(checked at $n = 10, 100, 1000$).

The reason: in an increasing sequence, each new element is larger than everything present, so
`sift_up` exits on its first comparison and the parent function's return value is never used to move
anything. **The test exercises the buggy line without ever depending on its answer.**

*This is the graded idea of Part A.* Award both marks only for an answer that identifies **why** the
test is blind, not merely that it passes. "Because the array is already sorted" is not sufficient — a
decreasing array is also sorted and does catch it at $n \ge 100$.

For reference, the full failure profile:

| input | $n=10$ | $n=100$ | $n=1000$ |
| --- | --- | --- | --- |
| increasing | passes | passes | passes |
| decreasing | passes | fails | fails |
| random | fails 4.3% | fails 98.5% | fails 100% |

---

### A3 (4)

A valid min-heap that is not sorted: `[1, 2, 3, 5, 4, 7, 6]` — check index 4 (value 4) against its
parent index 1 (value 2): fine, but $5 > 4$ appears earlier in the array, so it is unsorted.

A sorted array of 7: `[1, 2, 3, 4, 5, 6, 7]`.

**Yes — every sorted array is a valid min-heap.** If `a` is ascending then $a[j] \le a[i]$ whenever
$j \le i$, and a parent index is always strictly smaller than its child index, so
$a[\mathrm{parent}(i)] \le a[i]$ holds for every $i$. The converse fails, which is the point.

*Award 1 + 1 for the examples, 2 for the proof. The proof must invoke `parent(i) < i`; an answer that
merely says "it works for my example" scores 0 of those 2.*

---

## Part B — The Priority Queue (32)

Reference implementation:

```python
class MinHeap:
    def __init__(self, xs=None):
        self.a = []
        self.swaps = 0
        if xs is not None:
            self.build(xs)

    def __len__(self):  return len(self.a)

    def peek(self):
        if not self.a: raise IndexError("peek from an empty heap")
        return self.a[0]

    def _swap(self, i, j):
        self.a[i], self.a[j] = self.a[j], self.a[i]
        self.swaps += 1

    def sift_up(self, i):
        while i > 0:
            p = (i - 1) // 2
            if self.a[i] < self.a[p]:
                self._swap(i, p); i = p
            else:
                break                                  # REQUIRED, not an optimisation

    def sift_down(self, i, n=None):
        a = self.a
        if n is None: n = len(a)
        while True:
            l, r, m = 2*i + 1, 2*i + 2, i
            if l < n and a[l] < a[m]: m = l
            if r < n and a[r] < a[m]: m = r            # smaller of the two children
            if m == i: return
            self._swap(i, m); i = m

    def push(self, x):
        self.a.append(x)
        self.sift_up(len(self.a) - 1)

    def pop_min(self):
        if not self.a: raise IndexError("pop from an empty heap")
        top = self.a[0]
        last = self.a.pop()
        if self.a:
            self.a[0] = last
            self.sift_down(0)
        return top

    def build(self, xs):
        self.a = list(xs)
        for i in range(len(self.a)//2 - 1, -1, -1):
            self.sift_down(i)

    def check_heap(self):
        return all(self.a[(i-1)//2] <= self.a[i] for i in range(1, len(self.a)))
```

*(Verified: this `push` produces byte-identical array layouts to `heapq.heappush` on 500 random
operation sequences. Students may legitimately differ from `heapq` if they break ties differently,
so **do not** mark against `heapq`'s array — mark against `check_heap` and drain order.)*

### B1 (7)

The required counterexample: **`a = [5, 3, 4]`**. Both children are smaller than the root, so a
careless implementation may swap with either.

- Swap with the **larger** child (4): `[4, 3, 5]`. Now $a[0] = 4 > a[1] = 3$ — **still violated**.
- Swap with the **smaller** child (3): `[3, 5, 4]`. Correct.

The general reason: the new parent must be $\le$ **both** children, so it must be the minimum of the
three values.

*3 for the two sift routines, 3 for a correct counterexample with the resulting array shown. Accept
any array of the form $[x, y, z]$ with $x > y$, $x > z$, $y < z$.*

### B2 (8)

2 each for `push`, `pop_min`, `peek`/`__len__`, and the `IndexError`.

**The most common error is in `pop_min` on a one-element heap.** After `a.pop()` the list is empty and
`a[0] = last` raises `IndexError` — the `if self.a:` guard is required. Watch for students who
special-case `len(self.a) == 1` earlier and thereby return the wrong element; test it.

### B3 (7)

Must be `for i in range(n//2 - 1, -1, -1)` with `sift_down`. Award 0 of 6 for a build implemented as
repeated `push`, however correct — the question asks for the linear algorithm and Part C proves it.

Accept `range(n//2, -1, -1)`: starting one index too high is harmless, since index $\lfloor n/2\rfloor$
is a leaf and `sift_down` returns immediately.

### B4 (5)

```python
def check_heap(self):
    return all(self.a[(i-1)//2] <= self.a[i] for i in range(1, len(self.a)))
```

3 for correctness, 3 for it actually being **called after every operation** in Part B5's tests. A
`check_heap` that exists but is invoked only once at the end scores 3 of 6.

### B5 (5)

Expected report: 300+ trials, **0 failures**. Reference run: 400 trials of interleaved push/pop with
`check_heap()` after every operation, plus a full drain compared against `sorted()` — 0 failures. The
same for `build`: 400 trials, 0 failures.

*A student reporting failures they did not fix should lose the marks here and in B1–B3, not just
here.*

---

## Part C — Why the Build Is Linear (26)

### C1 (5)

A complete binary tree of $n$ nodes has at most $\lceil n/2^{h+1}\rceil$ nodes of height $h$.

At $h = 0$ the nodes of height 0 are the leaves, of which there are exactly
$\lceil n/2 \rceil = \lceil n/2^{0+1}\rceil$. For the inductive step, every node of height $h$ has at
least one child of height $h-1$, and distinct nodes of height $h$ have disjoint children, so the count
at height $h$ is at most half the count at height $h-1$; the bound follows.

*Accept the induction, or a direct argument from the level structure. 2 for the leaf base case, 2 for
the halving step.*

### C2 (10)

Total work is bounded by

$$\sum_{h=0}^{\lfloor\log_2 n\rfloor} \left\lceil\frac{n}{2^{h+1}}\right\rceil \cdot O(h)
\;=\; O\!\left(n \sum_{h=0}^{\infty} \frac{h}{2^{h+1}}\right)
\;=\; O\!\left(\frac{n}{2}\sum_{h=0}^{\infty} \frac{h}{2^{h}}\right)$$

**Evaluating the series** (the marked step — students must show this, not assert it):

Starting from $\sum_{h\ge0} x^h = \dfrac{1}{1-x}$ for $|x| < 1$, differentiate both sides:

$$\sum_{h\ge1} h\,x^{h-1} = \frac{1}{(1-x)^2}
\quad\Longrightarrow\quad
\sum_{h\ge0} h\,x^{h} = \frac{x}{(1-x)^2}$$

At $x = 1/2$: $\dfrac{1/2}{(1/2)^2} = \dfrac{1/2}{1/4} = 2$. Hence the total is
$O\!\left(\tfrac{n}{2}\cdot 2\right) = O(n)$.

**Where the $\log n$ went:** it is still there as the upper limit of the sum, but the terms it
multiplies decay geometrically, so the sum converges to a constant instead of growing. The naive
bound multiplies the *maximum* cost by the *number* of calls; the correct bound sums the *actual*
cost of each call, and almost every node has height 0 or 1.

*4 for the summation setup, 3 for a genuine derivation of the series (a bare "= 2" scores 0 of these
3; an integral test or ratio argument is fine), 1 for the explanation of the missing $\log n$.*

### C3 (5)

**Precondition:** `sift_down(i)` requires that the subtrees rooted at $2i+1$ and $2i+2$ are **already
valid heaps**. It only moves `a[i]` down; it never repairs anything below.

Descending order establishes this because every child index exceeds its parent index, so by the time
$i$ is processed, everything with a larger index has been. Running forwards processes a parent before
its children, so the precondition fails at the very first non-leaf with an unheapified subtree.

**Demonstration.** Reference run: a forward-loop build violated the heap property in **1,699 of
2,000** random trials.

*2 for the precondition, 2 for the demonstration with a number. Note the failure rate is not 100% —
a student reporting ~85% is right, and one reporting 100% has a bug in their checker.*

### C4 (6)

Both perform $n$ repairs, each $O(\log n)$ in the worst case, but **the repairs run in opposite
directions and the tree is bottom-heavy.**

`sift_down` from node $i$ costs the **height** of $i$'s subtree; half the nodes are leaves with height
0, and the sum of all heights is at most $n$. `sift_up` from node $i$ costs the **depth** of $i$;
half the nodes are leaves at the maximum depth, and the sum of all depths is $\Theta(n\log n)$.

**The expensive nodes are the rare ones for sift-down and the common ones for sift-up.**

*Full marks require locating the nodes. "Because most nodes are near the bottom" is worth 2; it is
only half the argument until the student says that being near the bottom is cheap for one direction
and expensive for the other.*

Reference figures:

| $n$ | $\sum$ heights | $\sum$ depths |
| --- | --- | --- |
| $10^3$ | 994 | 7,987 |
| $10^4$ | 9,995 | 113,631 |
| $10^5$ | 99,994 | 1,468,946 |
| $10^6$ | 999,993 | 17,951,445 |

---

## Part D — `decrease_key` (24)

### D1 (9) — `IndexedPQ`

```python
class IndexedPQ:
    def __init__(self):
        self.a = []          # list of (priority, key)
        self.pos = {}        # key -> index in self.a

    def _swap(self, i, j):
        self.a[i], self.a[j] = self.a[j], self.a[i]
        self.pos[self.a[i][1]] = i
        self.pos[self.a[j][1]] = j

    def _up(self, i):
        while i > 0:
            p = (i - 1) // 2
            if self.a[i][0] < self.a[p][0]: self._swap(i, p); i = p
            else: break

    def _down(self, i):
        n = len(self.a)
        while True:
            l, r, m = 2*i+1, 2*i+2, i
            if l < n and self.a[l][0] < self.a[m][0]: m = l
            if r < n and self.a[r][0] < self.a[m][0]: m = r
            if m == i: return
            self._swap(i, m); i = m

    def push(self, key, pri):
        if key in self.pos:                       # decrease_key
            i = self.pos[key]
            if pri < self.a[i][0]:
                self.a[i] = (pri, key); self._up(i)
            return
        self.a.append((pri, key)); self.pos[key] = len(self.a) - 1
        self._up(len(self.a) - 1)

    def pop(self):
        top = self.a[0]; last = self.a.pop(); del self.pos[top[1]]
        if self.a:
            self.a[0] = last; self.pos[last[1]] = 0; self._down(0)
        return top[1], top[0]
```

*4 for a correct heap with the position map, 2 for the map being maintained in **`_swap`** rather than
scattered through `_up`/`_down`, 1 for ignoring non-improving priorities.*

**The bug to look for:** forgetting `self.pos[last[1]] = 0` in `pop`, or deleting the popped key's
entry after overwriting it. Both leave a stale map that only shows up several operations later. E3's
cross-check catches it; a student who reports E3 passing with this bug present has not run it.

### D2 (9) — `LazyPQ`

As in Lecture 12 §3. *4 for correct staleness detection in `pop`, 2 for suppressing non-improving
pushes, 1 for handling exhaustion (a heap that is non-empty but contains only stale entries).*

**The bug to look for:** testing staleness with `self.best.get(key) is not None` rather than
`== pri`. This admits the first-popped entry for a key regardless of priority and is wrong only when
a `decrease_key` occurred — so it passes any test without repeated keys. **E3's requirement of
repeated keys exists to catch exactly this**; if a student's test generator draws keys from a large
range, their cross-check proves nothing. Check the generator, not just the reported result.

### D3 (6)

Expected: 200+ trials, 0 failures. *(Reference: 300 trials against a brute-force reference, checking
identical output sets, correct final priorities, and non-decreasing pop order. 0 failures.)*

Expected judgement:

- **Ship `LazyPQ`.** Fewer invariants, all staleness logic confined to `pop`, and it composes with the
  standard library instead of replacing it. `IndexedPQ`'s map must be maintained by every swap in the
  structure, which is a correctness obligation on code that has nothing to do with `decrease_key`.
- **Bound:** the heap holds at most one entry per `push` plus one per `decrease_key`, so its size is
  $O(V + D)$ where $D$ is the number of `decrease_key` calls. In Dijkstra $D \le E$, so the heap is
  $O(V + E) = O(E)$ and each operation costs $O(\log E)$. Since $E \le V^2$, $\log E \le 2\log V$, so
  $O(\log E) = O(\log V)$ and **the $O((V+E)\log V)$ bound is unchanged.**

*2 for a defended choice — accept `IndexedPQ` if the student argues from memory or from a workload
with very many `decrease_key` calls per key. 2 for the bound, which must include the
$\log E = O(\log V)$ step; stopping at "the heap is bigger but it still works" scores 1.*

---

## Marking Summary

| Part | Points |
| --- | --- |
| A | 18 |
| B | 32 |
| C | 26 |
| D | 24 |
| **Total** | **100** |

---

## Notes for the Grading Meeting

**1. A2(c) and C4 are the two questions that carry the week.** A2(c) is a test that passes and proves
nothing; C4 is an aggregate bound that is smaller than (operations) × (worst cost of one). If the
cohort does well on the code and poorly on these two, the problem set has not done its job, and it is worth ten minutes at the start of Week 4 rather than a
remark on the scripts.

**2. Do not deduct twice for the `sift_down` wrong-child bug.** It will fail B5, and B1 asks for the
counterexample explicitly. Deduct in B1 if the counterexample is wrong and in B5 if the tests were not
run; do not also deduct in B2.

**3. Expect `pop_min` on a one-element heap to be the single most common runtime failure.** Test it
first when a submission crashes.

**4. Carried forward from PS 2.** The Week 2 solutions flagged that the `bf(t.left) <= 0` versus
`< 0` bug in AVL insertion is undetectable on PS 2's inputs and asked for it to be raised in Week 3.
It is: **Lecture 11 §3's aggregate argument is the same reasoning pattern** — a cost that looks like
(number of operations) × (worst case each) but is not, because the expensive case is rare. Students
who lost marks on PS 2 D1 should be pointed at C4 here, which asks the same question in a setting
where the answer is easier to see.

**5. Forward.** C2's convergent-series argument returns in **Week 6** for Union-Find's amortised
bound.

---

*CS 102 · Week 3 · PS 3 Solutions · © CSE Department*
