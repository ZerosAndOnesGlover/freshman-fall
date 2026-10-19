---
assessment: Lab 2
course: CS 101
component: Labs
possible: 100
score: 100
status: graded
started: 2026-10-13
submitted: 2026-10-13
graded: 2026-10-16
source: "LAB 2 Debugging and Loops.md"
---

# CS 101 · Lab 2
## Answer Sheet

**Assessment:** `LAB 2 Debugging and Loops.md`
**Points available:** 100

Work in this folder: `debug_exercise.py` (Part 2, fixed), `loops.py` (Parts 3–4), and the detailed
debugging write-up in `lab2_notes.md`.

---

## Part 1 — Tracing by Hand (20)

### Exercise 1.1 (10)

`result` starts at `0`, so `result *= i` stays `0` forever and the program prints `0`, not `120`.
Trace of the first three iterations: `(i=1) 0*1=0`, `(i=2) 0*2=0`, `(i=3) 0*3=0`. The invariant
`result == (i - 1)!` at `i = 1` requires `result == 0! == 1`. **Fix:** `result = 1` → prints `120`.

### Exercise 1.2 (10)

| `i` | inner steps (`total`) |
|-----|-----------------------|
| 1 | 0→1 |
| 2 | 1→2, 2→4 |
| 3 | 4→5, 5→7, 7→10 |
| 4 | 10→11, 11→13, 13→16, 16→20 |

**Printed:** `20`. For each `i` the inner loop adds `1 + … + i` (the `i`-th triangular number), so
`total` is the sum of the first four triangular numbers: `1 + 3 + 6 + 10 = 20`.

_Marks: 20 / 20_

---

## Part 2 — Print-Debugging (30)

A `print` was added inside each loop, the run read, the wrong line named, the fix applied, and the
debug print removed. Full write-up in `lab2_notes.md`.

| Bug | Wrong line | What was meant | Fix | Fixed output |
|-----|-----------|----------------|-----|--------------|
| 1 | `total = i` | add each odd number | `total += i` | `2500` |
| 2 | `is_prime = True` (inside the divisor test) | a divisor means *not* prime | `is_prime = False` | `9 False` |
| 3 | `count + 1` | increment `count` | `count += 1` | `3` |
| 4 | `largest = 0` | start from a real value | `largest = values[0]` | `-1` |
| 5 | `i = len(word)` | last index is `len - 1` | `i = len(word) - 1` | `olleh` |

Final output of `debug_exercise.py`:

```
bug 1: 2500
bug 2: 9 False
bug 3: 3
bug 4: -1
bug 5: olleh
```

_Marks: 30 / 30_

---

## Part 3 — Loops to Write (35) — `loops.py`

**3.1(a) Collatz length:** `1` → `0`, `6` → `8`, `27` → `111`.

**3.1(b) Longest run for starts 1..20:** `18 20`.

**3.2 Sieve of Eratosthenes**, for `n = 30`:

```
[2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
10
[1, 2, 2, 4, 2, 4, 2, 4, 6]
```

For `n = 100` the prime count is `25`.

_Marks: 35 / 35_

---

## Part 4 — Invariant Comments (15)

Complete invariant comments (initialisation / preservation / termination) are written above the
Collatz loop (3.1a) and the sieve loop (3.2) in `loops.py`, e.g.:

```python
# Invariant: at the start of each iteration, n is the value reached from the start by `steps` moves.
# Initialisation: true before the first iteration because 0 moves leaves n == start.
# Preservation: each iteration applies one move and adds one to `steps`.
# Termination: the sequence reaches 1 and each iteration shrinks the remaining distance by one.
```

```python
# Invariant: every composite number with a prime factor less than p has been crossed out.
# Initialisation: p == 2, and no smaller prime factor exists yet.
# Preservation: crossing out multiples of p removes every composite whose smallest factor is p.
# Termination: p grows by one each iteration and stops once p * p > n.
```

_Marks: 15 / 15_

---

## Part 5 — Reflection

**Q1. Classify the five bugs.**

| Bug | Class |
|-----|-------|
| 1 | wrong **accumulation** (`=` instead of `+=`) |
| 2 | wrong **update** (flag set the wrong way) |
| 3 | wrong **update** (`count + 1` discards the result) |
| 4 | wrong **initialisation** (`largest = 0`) |
| 5 | wrong **condition/bound** (`i` starts past the last index) |

**Q2.** Bug 4 broke the invariant *"`largest` is the largest value seen so far"*: before the loop
`0` had never been seen, yet it was treated as the running maximum. For an all-negative list
(`[-1, -5, -3]`) `0` is larger than every real value, so nothing updated and `0` was printed.
Starting from `values[0]` makes the invariant true before the first iteration and restores `-1`.

---

## Grading Summary

| | |
|---|---|
| **Score** | 100 / 100 |
| **Percent** | 100% |
| **Graded** | 2026-10-16 |

**Feedback:**
Full marks. Part 1 traces are correct (1.1 prints `0`, fixed by `result = 1`; 1.2 prints `20` as the
sum of the first four triangular numbers). All five bugs are found, named by line, fixed, and
classified correctly, with the debug prints removed. `loops.py` reproduces every check value —
Collatz `0/8/111`, `18 20`, and the sieve output and gaps for `30` and count `25` for `100` — and the
Part 4 invariant comments argue initialisation, preservation and termination rather than restating the
invariant. Q2 correctly pins the broken invariant to the `largest = 0` initialisation.
