# CS 101 · Project 2
## Algorithm Visualizer

**Assigned:** Friday 4 December 2026, 10:00 · Week 10
**Due:** Friday 18 December 2026, 17:00 · Week 12 — late penalty from 17:01
**Weight:** Half of the 10% Projects component
**Submission:** `visualize.py`, `report.md` and `benchmark.txt` in `"$CS101/project2"`, committed to the Freshman Fall repo
**Expected time:** about 10 hours over two weeks
**Collaboration:** Individual project — no partners, no code sharing
**Starter:** `project2_starter.py`

---

## Overview

You will build a **terminal-based algorithm visualizer**: a tool that runs sorting and searching
algorithms, records every operation they perform, animates them in the terminal, and reports
measured costs alongside the theoretical predictions from Week 6.

Where Project 1 asked you to *use* algorithms, Project 2 asks you to **instrument** them — to make an
algorithm's behaviour observable, then check that what you observe matches what the theory says.
That shift is the point of the project.

The whole thing runs in the standard library. No `numpy`, no `matplotlib`, no curses libraries, no
external packages of any kind.

---

## Learning Objectives

By completing this project you will:

1. Instrument algorithms so their internal behaviour becomes data
2. Empirically confirm — or refute — Big-O predictions from Week 6
3. Distinguish *best*, *average*, and *worst* case by constructing inputs that trigger each
4. Design a rendering layer cleanly separated from the algorithms it displays
5. Persist and reload traces using the file-handling discipline from Week 10
6. Write honestly about where your measurements disagreed with your predictions

---

## Part 1: The Instrumentation Contract

The starter gives you a `Tracer` class. **Every algorithm you write must go through it.**

```python
t = Tracer([5, 2, 9, 1])
a, b = t.compare(0, 1)      # records a comparison, returns the two values
t.swap(0, 1)                # records and performs a swap
t.write(2, 42)              # records and performs a single write
v = t.compare_value(0, 7)   # compares position 0 against an external value
```

Every call appends a **frame**:

```
(event, snapshot, indices)
```

- `event` — `"compare"`, `"swap"`, or `"write"`
- `snapshot` — a **copy** of the whole array at that moment
- `indices` — a tuple of the positions involved

**Do not change the frame format.** Your renderer, your file format, and the self-test all depend
on it. You may add methods to `Tracer`; you may not bypass it by touching `tracer.data` directly
inside an algorithm. Doing so silently breaks every measurement in your report, and is the most
common way this project goes wrong.

> **Why copies?** A snapshot that aliases the live array would show you the *final* state at every
> frame, because all frames would point at the same list. The starter's self-test checks this
> explicitly. It is the Week 7 aliasing lesson, in a place where it will actually bite you.

---

## Part 2: Required Features

### 2.1 — Algorithms (Required)

Implement, all instrumented through `Tracer`:

| Algorithm | Requirement |
|---|---|
| `bubble_sort` | **Given** as a worked example — study it, do not rewrite it |
| `insertion_sort` | Must be adaptive: O(n) comparisons on sorted input |
| `selection_sort` | Must perform exactly n(n−1)/2 comparisons on **every** input |
| `merge_sort` | Use `t.write()` for the merge; there are no swaps |
| `binary_search` | Must use `compare_value`; O(log n) comparisons |

### 2.2 — The Renderer (Required)

Render a frame as a **proportional bar chart** in the terminal, highlighting the indices involved in
that frame.

```
  [ 12]  ████████████
  [  5]  █████
  [ 19]  ███████████████████   <- compare
  [  3]  ███                   <- compare
  [  8]  ████████
```

Requirements:

- Bars scale to a fixed width (60 characters, as the starter's `render_frame` does) and to the largest value present
- The frame's `indices` are visually distinguished
- `compare`, `swap` and `write` are distinguishable from one another
- Playback prints frames one after another and has a **frame budget** (show at most `k` frames, evenly
  spaced) so that a 40,000-frame bubble sort does not scroll for ten minutes; pressing Enter
  (`input()`) between frames is an acceptable step mode

Your renderer functions take frames only — they never call an algorithm — and your algorithms never
print. **They communicate only through frames.** This separation is graded.

### 2.3 — Verified Measurements (Required)

Your tool must produce a table comparing measured counts with theory. These four claims are
**checkable**, and the starter's self-test checks them:

1. **Selection sort's comparison count is input-independent** — exactly n(n−1)/2, whether the input
   is sorted, reversed, random, or all duplicates.
2. **Bubble and insertion sort each perform exactly `inversions(input)` swaps.** Not approximately —
   exactly, on every input. (`inversions` is provided in the starter.)
3. **Bubble and insertion are O(n) on already-sorted input** — 63 comparisons at n = 64.
4. **Doubling n roughly quadruples** the quadratic sorts' comparisons, while merge sort's grow far
   more slowly.

Claim 2 is the interesting one. Two algorithms that look nothing alike perform *identically* many
swaps, because each swap fixes exactly one inversion and sorting means removing all of them. Your
report must explain why.

### 2.4 — Input Shapes (Required)

Generate at least: `random`, `sorted`, `reversed`, `nearly_sorted`, and `duplicates`.

For each algorithm, identify which shape triggers its **best** and **worst** case, and confirm it by
measurement rather than by assertion.

### 2.5 — Trace Persistence (Required)

Save a recorded trace to disk and reload it for replay without re-running the algorithm.

Apply Week 10 properly:

- Write **atomically** (temp file in the target directory, `fsync`, `os.replace`)
- Specify the encoding explicitly
- On load, **validate the shape** of what you read — a truncated or hand-edited file must produce a
  clear error, not a confusing crash deep in the renderer
- Handle a missing file, an empty file, and a malformed file distinctly

### 2.6 — A Menu (Required)

`main()` offers a menu with `input()` and loops until the user quits:

```
1) animate   — choose algorithm, input shape, size, frame budget
2) save      — run an algorithm and save its trace to a file name you type
3) replay    — load a saved trace and animate it
4) benchmark — print the measured-vs-predicted table (and save it to benchmark.txt)
q) quit
```

Invalid choices and non-numeric sizes produce a helpful message and show the menu again — never a
traceback (the `try`/`except ValueError` idiom).

---

## Part 3: Design Requirements (Non-Negotiable)

1. **One file, clearly separated sections.** `visualize.py` has five headed sections — tracer,
   algorithms, rendering, persistence, menu — in that order. (Splitting a program across modules
   that import each other is not something this course has taught, so it is not required.)
2. **Algorithms know nothing about display.** No `print` inside any algorithm.
3. **No banned libraries.** Standard library only. No `numpy`, `matplotlib`, `pandas`, `curses`,
   `rich`, or any third-party package.
4. **Your own algorithms.** No `list.sort()`, no `sorted()`, no `bisect` inside the implementations.
   You may use `sorted()` in *tests* to check correctness.
5. **Every function has a docstring** stating what it does and its complexity where relevant.
6. **Handle the empty array and the single-element array** everywhere. The self-test checks n = 0
   and n = 1.

---

## Part 4: The Written Report (`report.md`)

1,000–1,500 words, eight sections:

1. **Architecture** — your five sections and why the boundaries fall where they do
2. **The instrumentation decision** — what `Tracer` records, what it does not, and what that costs
3. **Measured vs predicted** — your table, with the four verified claims from §2.3
4. **The inversion result** — why bubble and insertion perform identically many swaps, and why
   selection sort does not share the property
5. **Best and worst cases** — the input shape you constructed for each algorithm, and the measurement
   confirming it
6. **A disagreement** — one place where a measurement surprised you or contradicted your prediction,
   and how you resolved it. *If nothing surprised you, you did not measure enough.*
7. **The rendering trade-off** — storing a full snapshot per frame is Θ(n) memory per frame. State
   the total cost for bubble sort at n = 100, and describe what you would store instead if memory
   mattered
8. **What you would do differently** — with the benefit of having finished

---

## Grading Rubric

| Component | Weight | Criteria |
|-----------|--------|----------|
| Algorithms & instrumentation | 25% | All five correct; every operation routed through `Tracer`; passes the self-test |
| Verified measurements | 20% | All four §2.3 claims demonstrated; table accurate; theory correctly stated |
| Renderer | 15% | Proportional, highlights indices, distinguishes events, frame budget works |
| Architecture & separation | 15% | Clean sections; algorithms independent of display; no `print` in algorithms |
| Persistence & robustness | 10% | Atomic write; validation on load; missing/empty/malformed handled distinctly |
| Written report | 15% | All 8 sections; §4 and §6 substantive rather than perfunctory |
| **Total** | **100%** | |

---

## Submission Checklist

- [ ] `python3 project2_starter.py` (with your implementations) reports **15/15**
- [ ] `visualize.py`, with the five sections of §Part 3
- [ ] `report.md` — 1,000–1,500 words, all 8 sections
- [ ] `benchmark.txt` — saved output of the benchmark menu option
- [ ] One saved trace file, and evidence that the replay option reads it back
- [ ] Test file(s) demonstrating correctness on empty, single-element, and duplicate-heavy inputs
- [ ] Git history showing incremental progress, not one commit the night before

---

## Timeline Suggestion

| By when | What |
|---|---|
| Tue 8 Dec | Read the starter; implement `insertion_sort` and `selection_sort`; get their self-tests green |
| Thu 10 Dec | `merge_sort` and `binary_search` done; all 15 self-tests passing |
| Sat 12 Dec | Renderer working; playback and highlighting |
| Mon 14 Dec | Persistence, menu, benchmark table |
| Wed 16 Dec | Full end-to-end run; begin `report.md` |
| Fri 18 Dec, 17:00 | Final polish, edge cases, submit |

**A warning about pacing.** Weeks 11 and 12 also carry PS 11 and the final exam. The algorithms are
the part with hard correctness requirements and they are front-loaded deliberately — do not leave
them until Week 12.

---

## Academic Integrity Note

The algorithms in this project are in every textbook and all over the internet. You are expected to
have seen them. What is being assessed is your **instrumentation, your measurements, your
architecture, and your report** — none of which can be copied usefully, because they must match the
tool you actually built.

Cite anything you consult. Submitting a visualizer you did not build is both obvious and pointless:
the report asks you to explain results that only your own code produces.

---

*CS 101 · Project 2 · Assigned Friday 4 December, due Friday 18 December 2026, 17:00 · © CSE Department*
