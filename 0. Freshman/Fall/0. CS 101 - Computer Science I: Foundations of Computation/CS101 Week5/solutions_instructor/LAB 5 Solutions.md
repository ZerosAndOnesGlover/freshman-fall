# CS 101 — Week 5
## LAB 5 Solutions — INSTRUCTOR ONLY

> **All code below was executed and all stated outputs are real.** Where a benchmark appears,
> the absolute timings are machine-specific — grade the *ratios* and the conclusions, never the
> raw milliseconds.

---

## Part 1 — Implementations

Accept any correct implementation. The one structural requirement is that each sort **returns a new
list and a `SortStats`**, leaving the caller's data untouched — otherwise the second algorithm in
the benchmark loop receives already-sorted input and the numbers are meaningless. Check for
`a = a[:]` (or equivalent) at the top of every in-place sort.

**Verify correctness before timing anything:** `assert out == sorted(data)` after every run. A fast
wrong sort is the most common way this lab goes silently wrong.

---

## Part 2 — Benchmark Results

Measured on random integer data. **Absolute times are machine-specific; the ratios are what
matters.**

| n | selection | insertion | bubble | merge | quicksort | timsort |
|---|---|---|---|---|---|---|
| 10 | 0.013 ms | 0.010 | 0.012 | 0.022 | 0.014 | 0.001 |
| 100 | 0.795 | 0.359 | 0.671 | 0.188 | 0.123 | 0.006 |
| 1,000 | 36.0 | 36.6 | 63.6 | 1.81 | 1.17 | 0.097 |
| 5,000 | 816 | 861 | 1,689 | 12.4 | 7.48 | 0.674 |
| 20,000 | — | — | — | 50.0 | 32.1 | 3.19 |
| 100,000 | — | — | — | 335 | 212 | 20.5 |

Comparison counts:

| n | selection | insertion | bubble | merge | quicksort |
|---|---|---|---|---|---|
| 1,000 | 499,500 | 253,092 | 498,015 | 8,695 | 11,814 |
| 5,000 | 12,497,500 | 6,233,354 | 12,495,355 | 55,269 | 68,496 |
| 100,000 | — | — | — | 1,536,473 | 2,073,014 |

**Note that at n = 10 the O(n²) sorts beat merge sort**, and timsort beats everything by an order
of magnitude at every size. Both facts are worth drawing out — see Part 4 and the discussion below.

### The three required answers

**1. How much slower is `merge_sort` than `timsort` at n = 100,000, and why — both are O(n log n)?**

**335 ms vs 20.5 ms — merge sort is ≈ 16× slower.**

Both are Θ(n log n), so the gap is entirely in the **constant factor**, and there are three sources:

- **Timsort is written in C**, inside the interpreter. The student's merge sort is Python bytecode.
  This alone is worth roughly an order of magnitude and is the dominant term.
- **Timsort is adaptive.** It scans for existing sorted runs and merges them; even random data
  contains short ascending runs by chance, and Timsort exploits every one. Its comparison count on
  random data is well below the naive n log₂ n.
- **Allocation.** The recursive merge sort above builds a new list at every level — Θ(n log n)
  allocations in total. Timsort merges into a single reused buffer sized to the smaller run.

The lesson is the one from L21 §5: **Big-O tells you how the cost grows, not what the cost is.**
Two Θ(n log n) algorithms differing by 16× is normal, and no amount of asymptotic analysis predicts
it. Reject any answer that says "merge sort is slower because it is O(n log n)" — so is timsort.

**2. Selection sort comparison ratio, n = 1000 → 5000.**

12,497,500 / 499,500 = **25.02**, against a predicted (5000/1000)² = **25**. ✓

The agreement is essentially exact — and it *should* be, because selection sort's comparison count
is **deterministic**: exactly n(n−1)/2, independent of the data. Check: 1000·999/2 = 499,500 ✓ and
5000·4999/2 = 12,497,500 ✓. The tiny excess over 25 is the −n term, not noise. A student whose
ratio is 24 or 27 has a bug in their counter, since there is nothing here to vary.

**3. Merge sort comparison ratio, n = 1000 → 100,000.**

1,536,473 / 8,695 = **176.7**, against a predicted n log n ratio of
(100000 · log₂100000)/(1000 · log₂1000) = **166.7**.

Close, and **the excess is expected**, not error. Merge sort's comparison count is bounded above by
n⌈log₂n⌉ but the actual count depends on how the merges interleave; the "predicted" figure also
uses exact logs where the recursion depth is a ceiling. Agreement to within 6% over a 100× range in
n is a strong confirmation of n log n. Students should compare this against the **alternative
hypotheses**: pure Θ(n) predicts a ratio of 100, Θ(n²) predicts 10,000. The data excludes both
decisively.

---

## Part 4 — Best-Case Behaviour (n = 2,000)

| Input | Algorithm | Comparisons | Swaps |
|---|---|---|---|
| **sorted** | selection | **1,999,000** | 0 |
| sorted | insertion | **1,999** | 0 |
| sorted | bubble | **1,999** | 0 |
| **reversed** | selection | 1,999,000 | 1,000 |
| reversed | insertion | 1,999,000 | 1,999,000 |
| reversed | bubble | 1,999,000 | 1,999,000 |

This table is the heart of the lab.

- **Selection sort makes 1,999,000 comparisons in every case** — sorted, reversed, random. It must
  scan the whole unsorted remainder to find the minimum, so its cost depends only on n. Best case
  = worst case = Θ(n²). Note it does only **1,000 swaps** on reversed input, because each swap
  places two elements correctly; selection sort is the *swap*-optimal O(n²) sort, at Θ(n).
- **Insertion and bubble sort both make just 1,999 = n−1 comparisons on sorted input** — one per
  element, each finding itself already in place. That is **Θ(n)**, making both **adaptive**.
  Bubble sort achieves this only with the early-exit `swapped` flag; without it, it is Θ(n²) on
  sorted input too. **Check for that flag** — a student whose sorted-input bubble count is 1,999,000
  has omitted it.
- On **reversed** input all three converge to the same 1,999,000 comparisons, but insertion and
  bubble also perform 1,999,000 **swaps/shifts** against selection's 1,000. This is why bubble
  sort is the slowest in wall-clock time (1,689 ms vs 816 ms at n = 5,000) despite an identical
  comparison count — it moves data far more.

**The takeaway:** insertion sort's adaptivity is why Timsort uses it on short and nearly-sorted
runs, and why "all three are Θ(n²)" conceals a real engineering difference.

---

## Part 5 — Stability

```python
recs = [("b",1), ("a",2), ("b",0), ("a",1)]
sorted(recs, key=lambda p: p[0])
# -> [('a', 2), ('a', 1), ('b', 1), ('b', 0)]
```

The two `'a'` records emerge as `('a',2)` then `('a',1)` — their **original relative order**, not
sorted by the second field. That is stability, and Python guarantees it for `sorted` and
`list.sort`.

Expected findings for the students' own sorts:

| Algorithm | Stable? | Why |
|---|---|---|
| Insertion | **Yes** | Only shifts past strictly-greater elements (`a[j] > key`) |
| Bubble | **Yes** | Only swaps strictly-out-of-order adjacent pairs (`a[j] > a[j+1]`) |
| Merge | **Yes** | Provided the merge takes from the left run on ties (`L[i] <= R[j]`) |
| Selection | **No** | Its long-range swap can jump one equal element past another |
| Quicksort | **No** | Partitioning moves elements across the array arbitrarily |

> **The one-character stability bugs.** In merge sort, changing `L[i] <= R[j]` to `L[i] < R[j]`
> takes from the *right* run on ties and destroys stability while leaving the output sorted — so a
> correctness test passes and stability silently breaks. Likewise `a[j] >= key` in insertion sort.
> Test stability explicitly with duplicate keys and distinguishable payloads; sortedness alone
> cannot detect it.

Stability matters because it enables **multi-key sorting by successive passes**: sort by secondary
key, then by primary, and the secondary order survives within each group.

---

## Marking Scheme

The lab is checkoff-graded against the criteria on the handout. Within each part:

- **Method (≈60%).** Correct approach, required loop/structure type actually used, edge cases
  considered, invariants stated where the handout asks for them.
- **Result (≈40%).** Code runs, produces the specified output, and the written answers are correct.

**Carry-through.** A wrong helper that is then used correctly downstream costs marks once.

**Watch for the two failure modes that matter:**
1. Code that produces the right answer for the sample input and is wrong in general — always run
   the edge cases listed under each exercise.
2. Written answers that restate the observation instead of explaining it. "0.1 + 0.2 isn't 0.3
   because floats are imprecise" earns nothing; the answer must reach binary representation.

---

*CS 101 · Week 5 · Lab Solutions · Instructor Copy · © CSE Department*
