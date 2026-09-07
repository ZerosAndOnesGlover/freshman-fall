# CS 101 · Week 0
## LAB 0 Solutions — INSTRUCTOR ONLY

> **All code below was executed and all stated outputs are real.** Where a benchmark appears,
> the absolute timings are machine-specific — grade the *ratios* and the conclusions, never the
> raw milliseconds.

### ⚠️ Errata — CORRECTED in the handout

One defect, **now fixed**. Recorded here for the change log.

| Location | Was (wrong) | Now |
|---|---|---|
| [[CS101 Week0/lab/LAB 0 Environment Setup\|LAB 0 Environment Setup]], subtitle line | "*Duration: 2 hours · Not graded (completion only)*". This contradicted three other sources: the syllabus bills **Lab 0–11 as twelve graded labs worth 10%**, "graded on completion and correctness"; the gradebook carries a Lab 0 row worth 100 points inside the weighted Labs component; and this file sets out a Method-60 / Result-40 marking scheme, which is meaningless for an ungraded lab. Left as-is, a student would reasonably skip the written work. | "*Duration: 2 hours · Graded — 100 points via in-lab TA checkoff, part of the Labs component (10%)*". [[CS101 Week0/summary\|summary]] updated to match. |

**Note the contrast with PROG 101.** That course's Lab 0 genuinely *is* ungraded — its handout says
"Not graded: completion required before Problem Set 0", and its gradebook explicitly excludes Lab 0
from the Labs table as completion-only with no weight. The two courses made different choices, and
CS 101's handout appears to have inherited PROG 101's wording. Do not "fix" the PROG 101 one to
match; it is correct as it stands.

Students who skipped the written portions on the strength of the old subtitle should not be
penalised for it.

---

## Part 1–2 — Setup and Git

Checkoff only. Confirm `python3 --version` reports 3.10+, `git log --oneline` shows at least one
commit, and the repository has a `.gitignore` containing `__pycache__/`.

**The one thing worth actually checking:** that the student committed *source files only*. A repo
containing `__pycache__/`, `.DS_Store`, or a virtual environment means they ran `git add .` without
a `.gitignore`. Fix it with them now — it is far more painful to fix in Week 8.

---

## Part 3, Exercise 3.2 — REPL Observations Log

The handout pre-fills some rows. The three that students must complete:

| Expression | Result | Required explanation |
|---|---|---|
| `0.1 + 0.2` | `0.30000000000000004` | Neither 0.1 nor 0.2 is exactly representable in binary — both are infinite repeating fractions in base 2, like 1/3 in base 10. The stored values are the nearest `double`s, and their sum is not the nearest `double` to 0.3. |
| `-10 % 3` | `2` | Python's `%` takes the **sign of the divisor**, because `//` floors toward −∞. Since `-10 // 3 == -4`, the identity `(a//b)*b + a%b == a` forces `-12 + 2 = -10`. C truncates toward zero instead and gives `-1`. |
| `bool([])` | `False` | Empty containers are falsey. Note this is about **emptiness**, not contents — `bool([0])` is `True`. |

> A student who writes "they're not the same" for `0.1 + 0.2 == 0.3` has copied the handout's
> pre-filled hint, not answered. The binary-representation reason is the deliverable.

---

## Exercise 3.3 — Temperature Converter (the challenge line)

```python
# Absolute zero
celsius = -273.15
fahrenheit = (celsius * 9/5) + 32
kelvin = celsius + 273.15

print(f"\nAbsolute zero:")
print(f"  {celsius}°C = {fahrenheit:.2f}°F = {kelvin:.2f}K")
```

Output:

```
Absolute zero:
  -273.15°C = -459.67°F = 0.00K
```

**`0.00K` is exact here, not approximate.** `-273.15 + 273.15` evaluates to exactly `0.0` — adding
a float to its own negation is exact in IEEE 754 regardless of whether the value itself was
representable, because both operands have identical magnitude. This is worth a moment at checkoff,
because it is the *opposite* of the `0.1 + 0.2` result from Exercise 3.2 and stops students
concluding that float arithmetic is universally unreliable. It is unreliable in specific,
predictable ways.

Contrast `-273.15 + 273.15 + 0.1` with `-273.15 + (273.15 + 0.1)` if you want to show that
float addition is **not associative** — the two differ in the last bits.

---

## Exercise 3.4 — Calculator, the four required test cases

| Input | Observed behaviour |
|---|---|
| `a=17, b=5` | `Floor div: 3.0`, `Remainder: 2.0` — both **floats**, because `a` and `b` came from `float(input(...))`. `17.0 // 5.0` is `3.0`, not `3`. |
| `a=0, b=5` | Everything works. `0/5 = 0.000000`, `0 // 5 = 0.0`, `0 % 5 = 0.0`, `0 ** 5 = 0.0`. No special case needed. |
| `a=5, b=0` | The guard fires and prints "Division by zero is undefined." **But `5.0 ** 0.0` still evaluates, to `1.0`** — the power line sits outside the `if`, so it runs regardless. That is correct mathematically and worth pointing out: the guard protects three operations, not four. |
| `a=-7, b=3` | `Floor div: -3.0` and `Remainder: 2.0`. Students who expected `-2` and `-1` (the C answer) have met Python's flooring modulo. |

**The `a=-7, b=3` case is the one to discuss at checkoff.** `-7 // 3` is `-3` because floor division
rounds toward **negative infinity**, so `-2.333...` floors to `-3`, not `-2`.

---

## Part 5 — Reflection Questions

**1. Unlimited vs. fixed-size integers.**

*Python's arbitrary precision is necessary for:* cryptography. RSA operates on integers of 2048+
bits and needs them exact — a wraparound does not give a slightly wrong answer, it gives a broken
cipher. Also acceptable: combinatorics (100! has 158 digits), exact rational arithmetic, hash
computations that must not truncate.

*C's fixed size is preferable for:* anything where predictable memory layout or speed matters —
arrays, structs, embedded systems, or code where an `int` must fit in a register and arithmetic
must be one instruction. A Python `int` is a heap object of ~28 bytes with function-call
arithmetic; a C `int` is 4 bytes and one opcode.

Reject the common non-answer "Python is better because it never overflows" — the question asks for
a case where fixed width **wins**.

**2. Float imprecision and money.**

Binary floating point can represent only fractions whose denominator is a power of two. `0.1` is
1/10, and 10 is not a power of 2, so it stores as the nearest `double` — slightly off. Errors
accumulate over repeated arithmetic.

*Consequence for financial software:* systematic drift. Summing a million transactions accumulates
rounding error, ledgers fail to balance to the cent, and `if balance == 0` can be false on an
account that is genuinely empty. The industry fix is to store **integer cents**, or to use
`decimal.Decimal`, which is base-10 and exact for the values money actually takes.

**3. Why flooring modulo is useful for day-of-week arithmetic.**

Because it **always returns a non-negative result for a positive divisor**, so it can be used
directly as an index. `days[(today + n) % 7]` works for negative `n` — three days *before* Monday
gives `(0 - 3) % 7 == 4`, which correctly indexes Friday. With C's truncating modulo the same
expression gives `-3`, which either raises or (in Python) silently indexes from the end. Any
wrap-around indexing — circular buffers, clock arithmetic, hash buckets — is cleaner under flooring
semantics.

**4. Small commits.**

Each commit is an independently revertable unit and a labelled point in history. Small commits let
you use `git bisect` to find which change broke something, revert one mistake without losing four
good changes, and read a meaningful `git log`. One giant "Complete lab 0" commit is
all-or-nothing: the history records that work happened but not what any part of it was for.

Accept any answer that reaches *revertability* or *bisectability*; "it's tidier" alone is a partial
answer.

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

*CS 101 · Week 0 · Lab Solutions · Instructor Copy · © CSE Department*
