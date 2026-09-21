# CS 101 · Lab 2
## Tracing, Print-Debugging, and Loop Invariants

**Date:** Tuesday 13 October 2026 · 15:00–16:50 · Lab Section (Week 3) — covers Week 2 (L07–L09)
*Duration: 2 hours · 100 points via TA checkoff, part of the Labs component (10%)*

---

## Objectives

By the end of this lab, you will:
- [ ] Trace loops by hand with full state tables (L08 §2)
- [ ] Find bugs by printing the right state at the right place
- [ ] Write the Collatz length, the Sieve of Eratosthenes (L09 §8) and FizzBuzz (L07 §7) as loops
- [ ] Document a loop with its invariant (L08 §3)

**Tools used:** Weeks 0–2 only — `if`/`elif`/`else`, `while`, `for`, `range`, `break`/`continue`,
nested loops, lists. Every program is a plain script: no `def` (that is Week 3).

---

## Setup

```bash
mkdir -p "$CS101/week2"
cd "$CS101/week2"
```

Copy `debug_exercise.py` from this week's `lab/` folder into `"$CS101/week2"`.

---

## Part 1: Tracing by Hand (35 minutes) — 30 points

Work on paper. Do not run anything in this part.

### Exercise 1.1 (12 points)

```python
x = 100
result = 0
count = 0
while x > 1:
    if x % 2 == 0:
        x = x // 2
    else:
        x = 3 * x + 1
    result += x
    count += 1
```

Build the state table for the first 8 iterations — columns: iteration, `x` at the start, even?,
`x` at the end, `result`, `count`. Then:
1. What does `result` accumulate?
2. State the loop invariant: what is true about `result` and `count` at the start of each iteration?

### Exercise 1.2 (8 points)

This is meant to print `5! = 120`. Trace three iterations, find the bug, and use the invariant
`result == (i - 1)!` to say what the starting value must be.

```python
n = 5
result = 0
i = 1
while i <= n:
    result *= i
    i += 1
print(result)
```

### Exercise 1.3 (10 points)

```python
total = 0
i = 1
while i <= 4:
    j = 1
    while j <= i:
        total += j
        j += 1
    i += 1
print(total)
```

Trace it with one row per inner-loop step. What is printed? What is being added up for each `i`?

---

## Part 2: Print-Debugging (30 minutes) — 25 points

`debug_exercise.py` holds five short programs, each with one bug:

| Bug | Should print |
|---|---|
| 1 | the sum of the odd numbers 1..99 — `2500` |
| 2 | whether `n` is prime — `9 False` |
| 3 | the number of `a`s in `"banana"` — `3` |
| 4 | the largest of `[-1, -5, -3]` — `-1` |
| 5 | `"hello"` reversed without `[::-1]` — `olleh` |

**A useful print shows the loop position and every variable that matters:**

```python
print(f"[i={i}] total={total}")        # useful
print("here")                          # tells you almost nothing
```

For each bug: (1) add a print inside the loop, (2) run and read the output, (3) name the wrong line
and say what the programmer meant, (4) fix it, (5) remove the debug print. Record all five in
`lab2_notes.md`.

---

## Part 3: Loops to Write (40 minutes) — 35 points

Create `loops.py`. Each exercise is a short script section.

### Exercise 3.1: Collatz (10 points)

**(a)** Read `n` and print how many steps the Collatz rule (even → `n // 2`, odd → `3n + 1`) takes to
reach 1. Check: `1` → 0, `6` → 8, `27` → 111.

**(b)** With a `for` loop over 1..20 around a `while` loop, print the starting number that takes the
most steps, and how many. Check: `18 20`.

### Exercise 3.2: Sieve of Eratosthenes (15 points)

Following L09 §8: read `n`, make `is_prime = [True] * (n + 1)`, mark 0 and 1 as not prime, and for
each `p` with `p * p <= n` that is still marked prime, cross out `p*p, p*p + p, …`. Then:

- print the primes up to `n` — for 30: `[2, 3, 5, 7, 11, 13, 17, 19, 23, 29]`
- print how many there are — for 100: `25`
- print the gaps between consecutive primes — for 30: `[1, 2, 2, 4, 2, 4, 2, 4, 6]`

### Exercise 3.3: FizzBuzz (10 points)

For 1..30, print `Fizz` for multiples of 3, `Buzz` for multiples of 5, `FizzBuzz` for multiples of
both, and the number otherwise. Then change your program so multiples of 7 also add `Bazz`
(21 → `FizzBazz`, 35 would be `BuzzBazz`) — build the word up with `+=`, don't list every combination.

---

## Part 4: Invariant Comments (15 minutes) — 10 points

Above two of your loops (3.1(a) and 3.2 are good choices), write:

```python
# Invariant: at the start of each iteration, ...
# Initialisation: true before the first iteration because ...
# Preservation: the body keeps it true because ...
# Termination: the loop stops because ...
```

---

## Part 5: Commit and Reflection

```bash
cd "$CS101/week2"
git add .
git commit -m "CS 101 Lab 2: tracing, debugging, loop invariants"
git push
```

In `lab2_notes.md`:

**Q1.** Classify each of the five bugs: wrong initialisation, wrong condition/bound, wrong update, or
wrong accumulation.

**Q2.** Bug 4 started `largest` at `0`. Which invariant did that break, and what start value restores it?

---

## TA Checkoff Criteria

| Part | Points | Show your TA |
|---|---|---|
| 1 | 30 | Three traced tables on paper, with the answers |
| 2 | 25 | Five bugs fixed and explained (5 each) |
| 3 | 35 | `loops.py` gives every check value above |
| 4 | 10 | Two complete invariant comments |
| **Total** | **100** | Reflection answered and work committed (required) |

---

*CS 101 · Week 2 · Lab 2 · Tuesday 13 October 2026 · © CSE Department*
