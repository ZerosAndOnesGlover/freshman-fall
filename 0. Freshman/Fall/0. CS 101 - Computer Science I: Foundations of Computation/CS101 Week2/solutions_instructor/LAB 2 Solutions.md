# CS 101 Week 2
## LAB 2 Solutions: INSTRUCTOR ONLY

> **All code below was executed and all stated outputs are real.** Where a benchmark appears,
> the absolute timings are machine-specific — grade the *ratios* and the conclusions, never the
> raw milliseconds.

---

## Part 1, Exercise 1.1 — Tracing the `Collatz` Accumulator

| Iteration | `x` (start) | `x % 2 == 0?` | `x` (end) | `result` | `count` |
| --------- | ----------- | ------------- | --------- | -------- | ------- |
| 0 (init)  | 100         | —             | —         | 0        | 0       |
| 1         | 100         | True          | 50        | 50       | 1       |
| 2         | 50          | True          | 25        | 75       | 2       |
| 3         | 25          | False         | 76        | 151      | 3       |
| 4         | 76          | True          | 38        | 189      | 4       |
| 5         | 38          | True          | 19        | 208      | 5       |
| 6         | 19          | False         | 58        | 266      | 6       |
| 7         | 58          | True          | 29        | 295      | 7       |
| 8         | 29          | False         | 88        | 383      | 8       |

**1. What does it compute?** `count` is the number of `Collatz` steps from 100 down to 1, and
`result` is the **sum of every value the sequence takes after the starting value** (100 itself is
never added, because `result += x` runs *after* `x` is updated).

**2. Loop invariant.** At the start of each iteration:

> `count` = number of `Collatz` steps taken so far, and
> `result` = the sum of all values the sequence has visited since the start, **excluding** the
> initial 100 and **including** the current `x`.

**3. Final values: `count = 25`, `result = 708`.** (Verified by execution.)

The exclusion of the starting value is the subtle part, and the most common wrong answer is 808
(= 708 + 100) from students who assume the initial value is included. Ask them which line adds to
`result` and whether it runs before or after the update.

---

## Exercise 1.2 — The Factorial Bug

Trace of the first three iterations as written:

| i | `result` before | `result *= i` | `result` after |
|---|---|---|---|
| 1 | 0 | 0 × 1 | 0 |
| 2 | 0 | 0 × 2 | 0 |
| 3 | 0 | 0 × 3 | 0 |

**The bug:** `result = 0`. Zero is the **absorbing element** for multiplication, so the product is
pinned at 0 forever. It prints `0`, not 120.

**What the invariant tells you.** The intended invariant is *`result == (i-1)!` at the start of each
iteration*. At entry `i = 1`, so the invariant demands `result == 0! == 1`. **The correct
initialisation is forced by the invariant** — it is not a guess. This is the pedagogical point of
the exercise: initialise to the **identity element** of whatever operation the loop applies
(0 for sums, 1 for products, `-inf` for maxima, `[]` for accumulating lists).

**Fixed:** `result = 1` → prints `120`. ✓

---

## Exercise 1.3 — Nested Loops

| Outer `i` | Inner `j` values | Added this pass | Running `total` |
|---|---|---|---|
| 1 | 1 | 1 | 1 |
| 2 | 1, 2 | 3 | 4 |
| 3 | 1, 2, 3 | 6 | 10 |
| 4 | 1, 2, 3, 4 | 10 | **20** |

**Output: `20`.**

**The pattern:** each outer pass adds the *i*-th **triangular number** T_i = i(i+1)/2, so the total
is the sum of triangular numbers 1 + 3 + 6 + 10 = 20 — the fourth **tetrahedral** number,
n(n+1)(n+2)/6 = 4·5·6/6 = 20.

The complexity point matters more than the formula: the inner loop's bound depends on the outer
index, so the body runs 1+2+…+n = n(n+1)/2 times — **Θ(n²)** with half the constant of a full
nested loop. Students should recognise this shape on sight; it recurs in L17's insertion sort.

---

## Part 3: Reference Implementations

All verified against the `docstring` examples.

```python
def collatz_length(n):
    # Invariant: `steps` = number of Collatz steps applied to the original n so far.
    steps = 0
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        steps += 1
    return steps
# collatz_length(6)  -> 8   ✓ matches the docstring
# collatz_length(27) -> 111 (peaks at 9232 on the way — good demo that "it gets smaller" is false)


def max_collatz_length(limit):
    # Invariant: (best_n, best) is the argmax over all starts examined so far.
    best_n, best = 1, 0
    for k in range(1, limit + 1):
        length = collatz_length(k)
        if length > best:
            best, best_n = length, k
    return (best_n, best)
# max_collatz_length(20)   -> (18, 20)     ✓ matches the docstring
# max_collatz_length(1000) -> (871, 178)


def sieve_of_eratosthenes(n):
    if n < 2:
        return []
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    p = 2
    while p * p <= n:
        if is_prime[p]:
            for multiple in range(p * p, n + 1, p):
                is_prime[multiple] = False
        p += 1
    return [i for i, prime in enumerate(is_prime) if prime]
# sieve_of_eratosthenes(10) -> [2, 3, 5, 7]                              ✓
# sieve_of_eratosthenes(30) -> [2,3,5,7,11,13,17,19,23,29]               ✓
# sieve_of_eratosthenes(1)  -> []   sieve(0) -> []   sieve(2) -> [2]     ✓


def prime_gaps(n):
    ps = sieve_of_eratosthenes(n)
    return [ps[i + 1] - ps[i] for i in range(len(ps) - 1)]
# prime_gaps(30) -> [1, 2, 2, 4, 2, 4, 2, 4, 6]   ✓ matches the docstring


def fizzbuzz_range(start, end, rules=None):
    if rules is None:
        rules = [(3, "Fizz"), (5, "Buzz")]
    out = []
    for n in range(start, end + 1):
        word = "".join(w for d, w in rules if n % d == 0)
        out.append(word if word else str(n))
    return out
# Both docstring examples reproduce exactly, including "FizzBazz" at 21.


def digital_root(n):
    # Invariant: digital_root(n) is unchanged by each iteration (digit-sum preserves n mod 9).
    while n > 9:
        n = sum(int(c) for c in str(n))
    return n
# digital_root(493) -> 7   ✓
```

**Notes for checkoff:**

- **`sieve` must start the inner loop at `p*p`, not `2*p`.** Every composite multiple of `p` below
  `p²` has a smaller prime factor and was already crossed off. Starting at `2*p` is correct but
  does redundant work; starting at `p` is a bug that eliminates every prime.
- **`sieve(1)` and `sieve(0)` must return `[]`, not crash.** `[True] * 2` with `is_prime[0] =
  is_prime[1] = False` would work, but `n < 2` guard is cleaner. Test it.
- **`prime_gaps` returns one fewer element than there are primes.** A student returning a list of
  the same length has an off-by-one at one end.
- **`fizzbuzz_range` must join in rule order**, not sorted order — `[(5,"Buzz"),(3,"Fizz")]` should
  produce `"BuzzFizz"` at 15. Test with reordered rules.
- **`digital_root`** has a closed form: `0 if n == 0 else 1 + (n - 1) % 9`. Verified identical to
  the loop for all n in 0..5000. Mention it after they implement the loop, not before — the loop is
  the exercise, the identity is the reward.

---

## Part 4 — Loop Invariant Documentation

Model answer for `sieve_of_eratosthenes`:

```
# === Loop Invariant ===
# At the start of each outer iteration with candidate p:
#   is_prime[k] is False for every k <= n that has a proper prime factor < p,
#   and True for every other k in 2..n.
#
# Initialization: before the first pass p = 2, no k has a prime factor < 2,
#   so all of 2..n are still marked True. Invariant holds.
#
# Body preserves it: if is_prime[p] is True then p has no prime factor below
#   itself, so p is prime. Marking p*p, p*p+p, ... False adds exactly the
#   multiples of p not already handled by a smaller prime, extending the
#   invariant from "< p" to "<= p".
#
# Termination: p increases by 1 each pass and the loop exits when p*p > n,
#   which happens after at most sqrt(n) passes.
#
# Correctness: at exit every composite k <= n has a prime factor <= sqrt(n),
#   which has therefore already had its turn, so k is marked False. Every
#   remaining True entry is prime.
# =====================
```

**Grade the *maintenance* clause hardest.** Initialisation and termination are usually stated
correctly; the maintenance step is where students hand-wave, and it is the only part that actually
does any work. An invariant that is not preserved by the body is not an invariant, and a proof that
does not show preservation is not a proof.

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

*CS 101 · Week 2 · Lab Solutions · Instructor Copy · © CSE Department*
