# CS 101: Project 2 Instructor Guide
## Algorithm Visualizer

**Reference core:** `project2_reference.py` — verified **15/15** self-tests passing.
**Starter baseline:** `project2_starter.py` ships at **3/15** (bubble sort is worked; two frame-contract
tests pass for free).

---

## What This Project Is Actually Testing

Not the algorithms — they are in every textbook and students have seen them since Week 5. The
assessable content is:

1. **Discipline in routing every operation through `Tracer`.** This is the single most common failure
   and it is silent: a student who mutates `tracer.data` directly gets correct *sorting* and wrong
   *measurements*, then writes a report full of numbers that do not mean what they claim.
2. **Empirical confirmation of theory.** Four checkable claims (spec §2.3), all verified below.
3. **Architectural separation.** Algorithms must not know the renderer exists.
4. **Honest reporting**, especially report §6 — the disagreement between prediction and measurement.

---

## The Four Verified Claims

All figures below were confirmed by execution against the reference core.

### Claim 1 — Selection sort's comparison count is input-independent

Exactly **n(n−1)/2**, regardless of input shape. Verified at n = 32 (496 comparisons) across random,
sorted, and reversed inputs — identical in all three.

**Why:** the inner loop runs over the entire unsorted remainder on every pass, unconditionally. It
never breaks early, because finding the minimum requires examining every candidate. No input can
shorten it.

*Students often expect sorted input to be faster. It is not, and the reason is worth drawing out.*

### Claim 2 — Bubble and insertion swaps both equal the inversion count

**Exactly**, on every input. Verified:

| n | inversions | bubble swaps | insertion swaps |
|---|---|---|---|
| 5 | 5 | 5 | 5 |
| 10 | 26 | 26 | 26 |
| 20 | 64 | 64 | 64 |
| 40 | 405 | 405 | 405 |
| 64 | 1026 | 1026 | 1026 |
| 100 | 2504 | 2504 | 2504 |
| sorted (n=30) | 0 | 0 | 0 |
| reversed (n=30) | 435 | 435 | 435 |

**Why:** both algorithms only ever swap **adjacent** elements, and swapping an adjacent out-of-order
pair removes **exactly one** inversion — it cannot affect the relative order of any other pair.
Sorting means reaching zero inversions. So the swap count is forced, and it is the same number for
any adjacent-swap sort.

**Why selection sort does not share it:** its swaps are between *distant* positions, and one such
swap can fix many inversions at once (or create some). It performs at most n−1 swaps — 60 at n = 64,
against 948 for the other two on the same input.

This is the most interesting result in the project. A strong report explains it; a weak one reports
the coincidence without accounting for it. **Weight report §4 accordingly.**

### Claim 3 — Bubble and insertion are Θ(n) on sorted input

Both perform **63** comparisons at n = 64 — that is n−1, one pass with no swaps. Bubble needs the
`swapped` flag for this; insertion gets it from the `break` in the inner loop.

*A bubble sort without the early-exit flag does n(n−1)/2 comparisons on sorted input and fails this
test.* That is the intended lesson: "bubble sort is Θ(n²)" is a statement about the worst case, and
the best case depends on an implementation detail.

### Claim 4 — Growth rates

Measured comparisons, random input:

| n | bubble | ratio | merge | ratio |
|---|---|---|---|---|
| 16 | 117 | — | 45 | — |
| 32 | 418 | 3.57 | 121 | 2.69 |
| 64 | 1938 | 4.64 | 308 | 2.55 |
| 128 | 8073 | 4.17 | 734 | 2.38 |
| 256 | 32175 | 3.99 | 1738 | 2.37 |

Bubble's ratio converges on **4.0** — doubling n quadruples the work, the signature of Θ(n²). Merge's
settles around **2.3**, consistent with Θ(n log n): the ratio is 2·(log 2n / log n), which approaches
2 slowly from above.

*Marking note:* students who report a bubble ratio of exactly 4.00 at small n have probably not
measured — the convergence is visibly noisy below n = 64, as the table shows.

---

## Reference Figures for Report §7

Bubble sort at n = 100 (random input), from the reference core:

- **7,474 frames**, 4,830 comparisons, 2,644 swaps
- Each frame stores a **100-element snapshot**
- Total: **747,400 integer references ≈ 5.7 MB** for sorting one hundred numbers

The expected answer to "what would you store instead": **the delta only** — the event and its
indices — reconstructing state during replay by re-applying operations from the initial array. That
is ~3 small integers per frame, about **33× smaller**, at the cost of losing random access to an
arbitrary frame (you must replay from the start, or checkpoint periodically).

*Accept any answer that identifies the space/replay-time trade-off.* Reject answers that just say
"use less memory" without saying what is given up.

---

## Common Failure Modes

| Symptom | Cause | Marking |
|---|---|---|
| All frames show the sorted array | `snapshot` aliases the live list instead of copying | Fails the frame-contract test; costs the instrumentation mark. This is the Week 7 aliasing lesson |
| Correct sorting, wrong counts | Algorithm touches `tracer.data` directly | Serious — every number in the report is then meaningless. Cap the measurements mark |
| Selection sort count varies by input | Early exit added "to optimise" | The optimisation is wrong for this algorithm; discuss rather than heavily penalise |
| Bubble is Θ(n²) on sorted input | Missing the `swapped` early-exit flag | Fails Claim 3; a genuine correctness gap against the spec |
| `print` inside an algorithm | Architecture violation | Costs the separation mark; flag it explicitly, it recurs in later courses |
| Renderer imports algorithms module | Coupling in the wrong direction | Half the separation mark |
| Report §6 says "nothing surprised me" | Did not measure enough | The spec warns about this. Award minimal credit for §6 |

---

## Marking the Report

The report is 15%, and the two sections that separate strong from adequate work are:

**§4 (the inversion result)** — does the student explain *why*, in terms of adjacent swaps each
removing exactly one inversion? Or do they merely observe that the numbers matched?

**§6 (a disagreement)** — is there a real one, investigated? Good examples students actually find:
merge sort using *fewer* comparisons than n log₂ n suggests (because merges terminate early when one
run exhausts); bubble's growth ratio being erratic below n = 64; frame counts exceeding comparison
counts by more than expected.

A report where every prediction matched perfectly indicates measurement that was not attempted, or
was quietly adjusted to fit.

---

## Bonus (5%)

Quicksort with selectable pivots. The expected demonstration: **already-sorted input** with
first-element pivoting produces Θ(n²) — every partition splits into 0 and n−1. Median-of-three fixes
this specific input but does not eliminate the worst case in general; a determined adversary can
still construct one.

*Award full bonus only if the student states that last point.* "Median-of-three solves it" is the
misconception the exercise exists to correct.

---

*CS 101 · Week 12 · Project 2 Instructor Guide · Do not distribute*
