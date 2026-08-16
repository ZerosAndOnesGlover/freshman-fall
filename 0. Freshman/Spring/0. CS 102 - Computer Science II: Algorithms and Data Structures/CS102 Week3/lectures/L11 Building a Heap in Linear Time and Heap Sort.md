# CS 102 · Computer Science II
## Lecture 11: Building a Heap in Linear Time, and Heap Sort

**Date:** Wednesday 3 February 2027 · 09:00–09:50 · Week 3

---

## 1. The Question

You have an unsorted array of $n$ items and you want a heap.

The obvious method is to insert them one at a time. Each `push` costs $O(\log n)$, so the build costs
$O(n\log n)$, and there the matter would seem to rest.

**It does not. A heap can be built in $\Theta(n)$** — genuinely linear, not "linear in practice" —
and the algorithm is shorter than the obvious one. This lecture proves it, and then spends some time
on why the result is easy to disbelieve.

---

## 2. The Algorithm

```python
def build_heap(a):
    n = len(a)
    for i in range(n // 2 - 1, -1, -1):
        sift_down(a, i, n)
```

That is all of it. Sift down every non-leaf node, **starting from the last one and working
backwards**.

Two details, both essential.

**Why start at $n/2 - 1$.** The leaves are indices $\lfloor n/2 \rfloor \dots n-1$ (Lecture 10 §4).
A leaf has no children, so it is already a valid one-element heap. **Half the array needs no work at
all**, and that observation is the beginning of the proof.

**Why backwards.** `sift_down(a, i, n)` assumes both subtrees of $i$ are *already* heaps; its job is
only to place `a[i]` correctly within them. Processing indices in decreasing order guarantees that
assumption, because every child has a larger index than its parent. This is induction, executed as a
loop.

Run it forwards instead and the precondition fails:

*(Verified: the same code with the loop running `for i in range(0, n//2)` produces a structure that
violates the heap property in **1,699 of 2,000** random trials. It is not a subtle bug, but it also
does not fail on every input — which is worse.)*

---

## 3. Why It Is Linear

The temptation is to say "$n/2$ calls to `sift_down`, each $O(\log n)$, therefore $O(n \log n)$."
That reasoning is valid — the bound is true — but it is **not tight**, and the gap is the whole
point.

`sift_down(a, i, n)` does not cost $\log n$. It costs the **height of the subtree rooted at $i$**,
and in a complete tree almost every node has a very short subtree.

| height $h$ | number of nodes at height $h$ | work each | total |
| --- | --- | --- | --- |
| 0 (leaves) | $\le \lceil n/2 \rceil$ | 0 | 0 |
| 1 | $\le \lceil n/4 \rceil$ | 1 | $n/4$ |
| 2 | $\le \lceil n/8 \rceil$ | 2 | $2n/8$ |
| $h$ | $\le \lceil n/2^{h+1} \rceil$ | $h$ | $hn/2^{h+1}$ |

**The nodes that could be expensive are rare, and the nodes that are common are free.** Total work:

$$\sum_{h=0}^{\lfloor \log_2 n\rfloor} \left\lceil \frac{n}{2^{h+1}} \right\rceil \cdot h
\;\le\; \frac{n}{2}\sum_{h=0}^{\infty} \frac{h}{2^{h}} \;=\; \frac{n}{2}\cdot 2 \;=\; n$$

using $\sum_{h\ge0} h x^h = x/(1-x)^2$, which at $x = 1/2$ gives 2. **The series converges**, and that
is the entire trick: the $\log n$ factor never materialises because the terms it would multiply decay
geometrically.

### The exact statement

The sum being bounded is the **sum of the heights of all nodes**, and for a complete tree it has a
closed form:

$$\boxed{\;\sum_{i=0}^{n-1} \mathrm{height}(i) \;=\; n - s_2(n)\;}$$

where $s_2(n)$ is the number of 1-bits in the binary representation of $n$.

*(Verified: the identity holds for **every** $n$ from 1 to 2,999 — no exceptions.)*

| $n$ | sum of heights | $n - s_2(n)$ | $/n$ |
| --- | --- | --- | --- |
| $1{,}000$ | 994 | 994 | 0.994 |
| $10{,}000$ | 9,995 | 9,995 | 0.9995 |
| $100{,}000$ | 99,994 | 99,994 | 0.9999 |
| $1{,}000{,}000$ | 999,993 | 999,993 | 1.0000 |

**Fewer than $n$ swaps, always.** Not $O(n)$ with a constant to be discovered — fewer than $n$.

And this bound is achieved. *(Verified exhaustively for $n \le 8$: the maximum number of swaps over
**all $n!$ input permutations** equals $n - s_2(n)$ exactly, at every $n$. Over 4,000 random trials
at $n \le 200$, the bound was never exceeded.)*

### The contrast that makes it click

Put the two quantities side by side. The linear build pays the sum of node **heights**; building by
repeated insertion pays, in the worst case, the sum of node **depths**.

| $n$ | $\sum$ heights | $\sum$ depths | ratio |
| --- | --- | --- | --- |
| $1{,}000$ | 994 | 7,987 | 8.0 |
| $10{,}000$ | 9,995 | 113,631 | 11.4 |
| $100{,}000$ | 99,994 | 1,468,946 | 14.7 |
| $1{,}000{,}000$ | 999,993 | 17,951,445 | 18.0 |

Same tree. Same nodes. **Heights sum to $n$; depths sum to $n\log_2 n$.** The asymmetry exists
because a complete tree is bottom-heavy: half the nodes are leaves, and a leaf has height 0 but
depth $\log_2 n$.

> **Sift-down is cheap for the many nodes and expensive for the few. Sift-up is the reverse.** That
> single sentence is the entire result, and it is why the direction of the repair — not its
> asymptotic cost per call — decides the complexity of the build.

This is the reasoning pattern flagged at the end of PS 2: **an aggregate bound can be smaller than
(number of operations) × (worst cost of one)** whenever the expensive cases are rare. You will meet
it again in Week 6, when Union-Find's amortised bound has the same shape.

---

## 4. Measured

### The worst case is not the input you expect

For a min-heap, the natural guess at a worst case is a **decreasing** array — every element as badly
placed as possible.

| $n$ (decreasing input) | build swaps | bound $n - s_2(n)$ | insert-build swaps | $n\log_2 n$ |
| --- | --- | --- | --- | --- |
| 1,023 | 1,013 | 1,013 | 8,194 | 10,229 |
| 10,000 | 9,992 | 9,995 | 113,631 | 132,877 |
| 100,000 | 99,990 | 99,994 | 1,468,946 | 1,660,964 |
| 1,000,000 | 999,988 | 999,993 | 17,951,445 | 19,931,569 |

Look at the first two columns at $n = 10{,}000$: **9,992 against a bound of 9,995.** Decreasing input
does *not* achieve the maximum.

*(Verified: over $n = 1 \dots 399$, decreasing input attains $n - s_2(n)$ for only **129** values of
$n$ and falls short for the other **270** — first at $n = 8$, where it does 6 swaps against a bound of
7.)*

The worst case exists — exhaustive search over all $10!$ permutations at $n = 10$ finds inputs
achieving all 8 swaps — but it is an irregular arrangement, not a recognisable one. **The extremal
input for the linear build is not the reversed array**, and if you had assumed it was, your worst-case
test would have been measuring the wrong thing. Compare Week 2, where the extremal object *was*
recognisable (the Fibonacci tree) and did make a usable test case. It varies, and you have to check.

### Repeated insertion, and an exact identity

The last two columns tell a cleaner story. For **decreasing** input, every inserted key is smaller
than everything already present, so it rises from its leaf all the way to the root — travelling
exactly $\mathrm{depth}(i)$ levels.

$$\text{insert-build cost on a decreasing sequence} \;=\; \sum_{i=0}^{n-1}\mathrm{depth}(i) \;=\; \Theta(n\log n)$$

*(Verified: exact equality for every $n$ from 1 to 499, and spot-checked at $n = 10^4$ and $10^5$.)*

That is the $\Theta(n \log n)$, made concrete: **18 times more work than the linear build at
$n = 10^6$, and the factor grows with $\log n$.**

### On random input, both are linear

| $n$, random | build swaps | insert-build swaps | ratio |
| --- | --- | --- | --- |
| $1{,}000$ | 738 | 1,246 | 1.69 |
| $10{,}000$ | 7,484 | 12,834 | 1.71 |
| $100{,}000$ | 74,369 | 128,102 | 1.72 |
| $1{,}000{,}000$ | 744,081 | 1,280,868 | 1.72 |

*(Means of 5 seeds.)*

**The ratio is constant.** On random input the insert-build is *also* $\Theta(n)$, because a random
key rises only $O(1)$ levels on average — the early exit of Lecture 10 §5 fires almost immediately.
The $\Theta(n\log n)$ is a genuine worst case, not a typical one.

So the honest summary is: the linear build wins by a constant factor of about 1.7 on typical input,
and by a factor of $\log n$ on adversarial input. **Both facts matter, and quoting only the second is
the kind of benchmarking Lecture 09 warned about.**

### Wall clock

Using CPython's `heapq` (C-accelerated) on this machine, best of 5:

| $n$ | `heapify` | `heappush` loop | ratio |
| --- | --- | --- | --- |
| $10{,}000$ | 0.3 ms | 2.1 ms | 7.8 |
| $100{,}000$ | 3.0 ms | 26.5 ms | 8.9 |
| $1{,}000{,}000$ | 50.4 ms | 357.2 ms | 7.1 |
| $4{,}000{,}000$ | 210.4 ms | 1590.0 ms | 7.6 |

*(Decreasing input — the worst case for the push loop.)*

**The wall-clock ratio does not grow the way the swap counts do**, and you should be suspicious of
that rather than ignore it. The reason is that `heapify` runs entirely in C, while the push loop is a
Python-level `for` statement executing $n$ interpreted iterations. That interpreter overhead is
$\Theta(n)$ with a large constant, and at these sizes it, not the $\log n$, dominates. **The
measurement is real; the thing it measures is partly the interpreter.** Lab 3 has you separate the
two by counting operations as well as timing them.

---

## 5. Heap Sort

Build a max-heap; repeatedly swap the root to the end and shrink.

```python
def heapsort(a):
    n = len(a)
    for i in range(n // 2 - 1, -1, -1):     # Theta(n): build a MAX-heap
        sift_down_max(a, i, n)
    for end in range(n - 1, 0, -1):         # Theta(n log n): extract
        a[0], a[end] = a[end], a[0]         # largest goes to its final position
        sift_down_max(a, 0, end)            # heap shrinks by one
```

The loop invariant: `a[end+1:]` holds the largest elements in sorted order, and `a[:end+1]` is a
max-heap. Both hold initially, and the body preserves them.

**A max-heap sorts ascending.** This inverts most people's first guess and is worth a moment: the
largest element is at the root, and the root is swapped to the *back*, so the array fills from the
right with descending values — leaving ascending order.

Heap sort's properties:

- **$\Theta(n\log n)$ worst case.** Not "average" — the height is $\lfloor\log_2 n\rfloor$ no matter
  the input. Quicksort's $O(n^2)$ worst case has no analogue here.
- **$O(1)$ auxiliary space**, truly in place. Merge sort needs $\Theta(n)$.
- **Not stable.**
- **Not adaptive.** Nearly-sorted input does not help; see the measurements below.

---

## 6. Heap Sort Against Merge Sort

Both are $\Theta(n\log n)$. They are not otherwise similar.

### Comparisons, random input (mean of 5)

| $n$ | heap sort | merge sort | ratio | $n\log_2 n$ | heap$/n\log n$ | merge$/n\log n$ |
| --- | --- | --- | --- | --- | --- | --- |
| $1{,}000$ | 16,833 | 8,705 | 1.93 | 9,966 | 1.69 | 0.87 |
| $10{,}000$ | 235,359 | 120,417 | 1.95 | 132,877 | 1.77 | 0.91 |
| $100{,}000$ | 3,019,554 | 1,536,292 | 1.97 | 1,660,964 | 1.82 | 0.92 |

**Heap sort does about twice the comparisons.** The reason is structural: each `sift_down` step needs
**two** comparisons — one to pick the smaller child, one to test it against the parent — where merge
sort's inner loop needs one. The $2n\log_2 n$ against $n\log_2 n$ is visible in the last two columns.

### Comparisons, already-sorted and reverse-sorted input

| $n$ | | heap sort | merge sort | ratio |
| --- | --- | --- | --- | --- |
| $100{,}000$ | sorted | 3,112,517 | 815,024 | **3.82** |
| $100{,}000$ | reversed | 2,926,640 | 853,904 | **3.43** |

**Heap sort does slightly *more* work on sorted input than on random input** (3,112,517 against
3,019,554), while merge sort does roughly half as much. Heap sort is not adaptive; merge sort
partially is, and Python's Timsort aggressively is — a point that returns in section 7.

### Wall clock, random input, best of 3

| $n$ | heap sort | merge sort | ratio | heap sort µs/elem | merge sort µs/elem |
| --- | --- | --- | --- | --- | --- |
| $1{,}000$ | 2.1 ms | 2.0 ms | 1.07 | 2.111 | 1.979 |
| $10{,}000$ | 30.0 ms | 25.0 ms | 1.20 | 3.004 | 2.495 |
| $100{,}000$ | 444.8 ms | 318.4 ms | 1.40 | 4.448 | 3.184 |
| $1{,}000{,}000$ | 6922.2 ms | 4287.1 ms | **1.61** | 6.922 | 4.287 |

Both are pure Python, so the comparison between them is fair.

**The gap widens steadily — 1.07 to 1.61 — and comparisons alone do not explain it**, since the
comparison ratio is flat at about 1.95. The last two columns are where the answer is. Taking
$n = 1{,}000$ as the baseline and asking how much the *per-element* cost grows:

| $n$ | heap sort | merge sort | $n\log n$ predicts |
| --- | --- | --- | --- |
| $10{,}000$ | 1.42× | 1.26× | 1.33× |
| $100{,}000$ | 2.11× | 1.61× | 1.67× |
| $1{,}000{,}000$ | **3.28×** | 2.17× | **2.00×** |

**Merge sort tracks the prediction and heap sort runs away from it.** By $n = 10^6$ heap sort costs
64% more per element than its own asymptotics account for, while merge sort is within 9%.

That excess is **memory locality**, exactly as Lecture 10 §4 warned. `sift_down` walks
$i \to 2i+1 \to 4i+3$, doubling its stride at every step, so the deep levels of a large heap are
effectively random access and every step is a probable cache miss. Merge sort's inner loop is three
sequential scans, which is the pattern hardware prefetchers are built for. **Heap sort's beautiful
array representation is also the reason it is slow** — and the effect is invisible until the heap
outgrows the cache, which is why the $n = 1{,}000$ row shows almost no gap at all.

### Where heap sort's time actually goes

| $n$, random | build comparisons | extract comparisons | build share |
| --- | --- | --- | --- |
| $1{,}000$ | 1,848 | 14,973 | 11.0% |
| $10{,}000$ | 18,795 | 216,569 | 8.0% |
| $100{,}000$ | 188,010 | 2,831,128 | **6.2%** |

Lecture 11 spent three sections on a $\Theta(n)$ build that accounts for **6% of heap sort's work**,
and the share shrinks as $n$ grows. Optimising it further would be pointless. The linear build matters
because it is used *on its own* — `heapify`, top-$k$, Dijkstra's initialisation — not because it
speeds up heap sort.

### Space

*(Verified with `tracemalloc`, $n = 100{,}000$: peak traced allocation **781 KiB** for heap sort
against **1,687 KiB** for merge sort, a factor of 2.2 — and heap sort's figure is entirely the
defensive copy it makes of the input list. A genuinely in-place version allocates nothing at all,
while merge sort's $\Theta(n)$ is unavoidable.)*

### Stability

Merge sort is stable; heap sort is not, and the smallest possible counterexample makes the point:

```
Two records with equal keys:   [(0,'a'), (0,'b')]
heap sort gives:               [(0,'b'), (0,'a')]      ← swapped
```

*(Verified by exhaustive search over all 0/1 key patterns for $n \le 8$, comparing against a stable
reference. Heap sort's smallest instability is at $n = 2$; merge sort produced **no** instability
anywhere in that search. On 100 records drawn from 10 distinct keys, heap sort was unstable in
**2,000 of 2,000** trials, merge sort in **0 of 2,000**.)*

$n = 2$ is as small as a counterexample can be. The very first swap of the build — `a[0], a[end]` —
moves an element past its equal without cause, and nothing afterwards can undo it.

### The summary

| | heap sort | merge sort |
| --- | --- | --- |
| worst case | $\Theta(n\log n)$ | $\Theta(n\log n)$ |
| comparisons | $\approx 2n\log_2 n$ | $\approx n\log_2 n$ |
| auxiliary space | $O(1)$ | $\Theta(n)$ |
| stable | no | yes |
| adaptive | no | somewhat |
| locality | poor | excellent |
| measured, $n=10^5$ | 444.8 ms | 318.4 ms |
| measured, $n=10^6$ | 6,922 ms | 4,287 ms |

**Heap sort wins exactly one column, and it is the one it is chosen for.** Guaranteed
$\Theta(n\log n)$ in $O(1)$ space is the combination nothing else offers — quicksort is fast and in
place but has a quadratic worst case; merge sort is fast and safe but needs linear space. When memory
is genuinely constrained and the worst case genuinely matters, heap sort is the answer.

That is a narrow niche, and real libraries occupy it deliberately. On the machine these notes were
prepared on, `/usr/include/c++/13/bits/stl_algo.h` defines `std::sort` as:

```cpp
std::__introsort_loop(__first, __last, std::__lg(__last - __first) * 2, __comp);
std::__final_insertion_sort(__first, __last, __comp);
```

and inside `__introsort_loop`:

```cpp
if (__depth_limit == 0)
  {
    std::__partial_sort(__first, __last, __last, __comp);   // == __make_heap + __sort_heap
    return;
  }
--__depth_limit;
```

**`std::sort` is quicksort with a heap sort parachute.** It starts a recursion budget at
$2\lfloor\log_2 n\rfloor$; if quicksort's partitioning goes badly enough to exhaust it, the remaining
range is heap sorted, capping the worst case at $\Theta(n\log n)$. Heap sort is not the fast path —
it is the guarantee that lets the fast path stay fast, and it is chosen for the one column it wins.

---

## 7. What to Do

- Read CLRS §6.3–6.4 — `BUILD-MAX-HEAP` and `HEAPSORT`. §6.3's Figure 6.3 is the proof of section 3
  in a picture.
- **PS 3** part C proves the $\sum h/2^h$ bound; part D reproduces the $n - s_2(n)$ measurement.
- **Lab 3** builds both sorts and finds the locality effect on your own machine.
- Next lecture: what a heap is actually *for* — the priority queue, and the algorithms that need one.

---

*CS 102 · Week 3 · Lecture 11 · © CSE Department*
