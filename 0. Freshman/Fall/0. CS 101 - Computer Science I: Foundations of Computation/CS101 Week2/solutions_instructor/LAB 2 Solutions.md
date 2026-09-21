# CS 101 · Week 2
## LAB 2 Solutions: INSTRUCTOR ONLY

> Lab sat Tuesday 13 October 2026. **All code below was executed; outputs are real.**

---

## Part 1 — Tracing (30)

### 1.1 (12)

| Iter | `x` start | even? | `x` end | `result` | `count` |
|---|---|---|---|---|---|
| 1 | 100 | T | 50 | 50 | 1 |
| 2 | 50 | T | 25 | 75 | 2 |
| 3 | 25 | F | 76 | 151 | 3 |
| 4 | 76 | T | 38 | 189 | 4 |
| 5 | 38 | T | 19 | 208 | 5 |
| 6 | 19 | F | 58 | 266 | 6 |
| 7 | 58 | T | 29 | 295 | 7 |
| 8 | 29 | F | 88 | 383 | 8 |

`result` is the sum of every value in the Collatz trajectory of 100 after the seed (the full run is
25 steps; `result` ends at **708**). Invariant: *`count` is the number of Collatz steps taken so far,
and `result` is the sum of the `count` values reached after 100.* *(8 table, 4 answers.)*

### 1.2 (8)

`result` starts at `0`, so every product is `0` and it prints `0`. The invariant `result == (i - 1)!`
at `i = 1` needs `result == 0! == 1`. Fix: `result = 1` → prints `120`.

### 1.3 (10)

For `i = 1..4` the inner loop adds `1 + … + i`: 1, 3, 6, 10. Printed: **20** — the sum of the
first four triangular numbers.

---

## Part 2 — Print-Debugging (25, 5 each)

| Bug | Buggy output | Wrong line | Fix | Class |
|---|---|---|---|---|
| 1 | `99` | `total = i` | `total += i` → `2500` | accumulation |
| 2 | `9 True` | `is_prime = True` inside the `if` | `is_prime = False` → `9 False` | update |
| 3 | `0` | `count + 1` computes and discards | `count += 1` → `3` | update |
| 4 | `0` | `largest = 0` | `largest = values[0]` → `-1` | initialisation |
| 5 | `IndexError` | `i = len(word)` | `i = len(word) - 1` → `olleh` | condition/bound |

Q2: the invariant *"`largest` is the largest value seen so far"* is false before the loop when
`largest = 0` and every value is negative — `0` was never seen. Starting from `values[0]` makes it
true from the start.

---

## Part 3 — Loops (35)

```python
# 3.1(a)
n = int(input("n: "))
steps = 0
# Invariant: after `steps` iterations, n is the value reached from the start by `steps` Collatz moves.
while n != 1:
    if n % 2 == 0:
        n = n // 2
    else:
        n = 3 * n + 1
    steps += 1
print(steps)

# 3.1(b)
best_start = 1
best_steps = 0
for start in range(1, 21):
    n = start
    steps = 0
    while n != 1:
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
        steps += 1
    if steps > best_steps:
        best_start = start
        best_steps = steps
print(best_start, best_steps)

# 3.2
n = int(input("n: "))
is_prime = [True] * (n + 1)
is_prime[0] = False
is_prime[1] = False
p = 2
# Invariant: every composite number with a prime factor < p is crossed out.
while p * p <= n:
    if is_prime[p]:
        for multiple in range(p * p, n + 1, p):
            is_prime[multiple] = False
    p += 1
primes = []
for k in range(n + 1):
    if is_prime[k]:
        primes.append(k)
print(primes)
print(len(primes))
gaps = []
for i in range(len(primes) - 1):
    gaps.append(primes[i + 1] - primes[i])
print(gaps)

# 3.3
for k in range(1, 31):
    word = ""
    if k % 3 == 0:
        word += "Fizz"
    if k % 5 == 0:
        word += "Buzz"
    if k % 7 == 0:
        word += "Bazz"
    print(word if word else k)
```

Verified: 3.1(a) `27` → `111` (and `1` → `0`, `6` → `8`); 3.1(b) → `18 20` (19 also takes 20 steps;
the strict `>` keeps the first). 3.2 `30` → `[2, 3, 5, 7, 11, 13, 17, 19, 23, 29]`, 10 primes, gaps
`[1, 2, 2, 4, 2, 4, 2, 4, 6]`; `100` → 25 primes. 3.3 prints `… Fizz Bazz 8 … Bazz FizzBuzz … FizzBazz …`
with 21 → `FizzBazz` and 15, 30 → `FizzBuzz`.

*10 / 15 / 10. In 3.3, a solution that lists `FizzBuzzBazz` etc. as separate cases works but loses 3.*

## Part 4 — Invariants (10)

5 each: all four lines present and true. The comments in the reference code above are acceptable
invariants; initialisation/preservation/termination must be argued, not restated.

---

*CS 101 · Week 2 · Lab 2 Solutions · Instructor only*
