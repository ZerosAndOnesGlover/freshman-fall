# CS 101 · Week 1
## LAB 1 Solutions: INSTRUCTOR ONLY

> **All code below was executed and all stated outputs are real.** Where a benchmark appears,
> the absolute timings are machine-specific — grade the *ratios* and the conclusions, never the
> raw milliseconds.

---

## Part 1 — Python Tutor: Binding, Immutability, Aliasing

The three exercises make one point in three forms: **names are labels on objects; assignment
rebinds a label; mutation changes an object.**

- **1.1 Binding vs. copying.** `b = a` creates a second label on one object. `id(a) == id(b)`.
- **1.2 Immutability.** `s += "x"` on a string *cannot* mutate, so it builds a new object and
  rebinds — `id(s)` changes. Ask students to print `id()` before and after; that is the whole
  demonstration.
- **1.3 The aliasing trap.** `y = x; y.append(4)` changes what `x` sees, because both label the
  same list. `y = x + [4]` does not.

**The sentence to extract at checkoff:** *mutation is visible through every label; rebinding is
visible through one.* A student who can say that has understood Part 1 regardless of what their
diagram looks like.

---

## Exercise 2.1 — Type Conversion Edge Cases

```
int(3.9)        = 3          truncates toward zero, does NOT round
int(-3.9)       = -3         toward zero again — so -3, not -4
int(True)       = 1          bool is a subclass of int
int("  42  ")   = 42         int() strips surrounding whitespace (but not internal)
```

**round / int / floor / ceil:**

| v | `round` | `int` | `floor` | `ceil` |
|---|---|---|---|---|
| 2.5 | **2** | 2 | 2 | 3 |
| 3.5 | **4** | 3 | 3 | 4 |
| 4.5 | **4** | 4 | 4 | 5 |
| −2.5 | **−2** | −2 | −3 | −2 |
| −3.5 | **−4** | −3 | −4 | −3 |

`round` uses **banker's rounding** (half-to-even): 2.5→2 but 3.5→4, and −2.5→−2 but −3.5→−4. This
is IEEE 754 round-half-to-even, chosen because always-round-up biases the sum of many rounded
values upward. It is the single most surprising row of the lab and deserves a minute at checkoff.

Note `int` and `floor` **agree on positives and disagree on negatives** — `int(-3.9) = -3`,
`floor(-3.9) = -4`.

**Falsy values** — all ten print `False`: `False, 0, 0.0, 0j, "", [], (), {}, set(), None`.

**Surprising truthiness** — all five print `True`:

```
bool("False")   = True   non-empty string; the *content* is never examined
bool("0")       = True   likewise — this is why `if input("y/n"): ` is always a bug
bool([False])   = True   a one-element list is non-empty
bool([0])       = True   same
bool(0.0000001) = True   non-zero
```

**bool/int relationship:**

```
isinstance(True, int)   = True    bool IS a subclass of int
isinstance(True, bool)  = True
isinstance(42, bool)    = False   the reverse does not hold
True == 1               = True
```

> **`print(True is 1)` in the handout emits `SyntaxWarning: "is" with 'int' literal. Did you mean "=="?`** in Python 3.8+, and evaluates to `False`. The warning is correct and the line should be
> `True == 1`. Tell students the warning is Python catching a real bug class, not a nuisance — and
> flag the handout line to the course coordinator for rewording.

---

## Exercise 2.2 — Precedence Gauntlet

| Expression | Result | Why |
|---|---|---|
| `2 + 3 * 4` | `14` | `*` before `+` |
| `2 ** 3 ** 2` | **`512`** | `**` is **right**-associative: `2**(3**2)` = 2⁹, not 8² |
| `-2 ** 2` | **`-4`** | `**` binds tighter than unary minus: `-(2**2)` |
| `10 // 3 + 10 % 3` | `4` | `3 + 1` |
| `True + True + True` | `3` | bools are ints |
| `1 < 2 < 3` | `True` | chains to `1<2 and 2<3` |
| `1 < 2 > 3` | **`False`** | chains to `1<2 and 2>3`; the second is false |
| `not True or False` | `False` | `not` binds tighter than `or`: `(not True) or False` |
| `not (True or False)` | `False` | same value here, different parse — a good pair to compare |
| `1 and 2 and 3` | **`3`** | `and` returns an **operand**, not a bool: the last truthy one |
| `0 and 2 and 3` | **`0`** | short-circuits at the first falsey operand and returns it |
| `0 or "" or [] or 42` | **`42`** | first truthy operand |
| `0 or "" or []` | **`[]`** | all falsey → returns the **last** operand |

The four in bold are the ones students reliably miss. The last four together make the essential
point: **`and`/`or` are selection operators, not boolean operators.** That is what makes
`name = user_input or "anonymous"` work — and what makes it a bug when `0` is a legal input.

---

## Exercise 2.3 — Bitwise

`a = 0b10110100 = 180`, `b = 0b01101011 = 107`.

```
   a & b =    32 = 00100000
   a | b =   255 = 11111111
   a ^ b =   223 = 11011111
      ~a =  -181  (negative)
  a << 2 =   720 = 1011010000
  a >> 2 =    45 = 00101101
```

**Answers to the four questions:**

1. **`a & b`** yields 1 in a position only when *both* inputs have 1 there. Here only bit 5 is set
   in both, giving 32. It is the standard tool for *masking* — testing or clearing selected bits.
2. **`a << 2` = multiplication by 4.** 180 × 4 = 720. In general `x << k` is `x * 2**k`.
3. **`a >> 2` = floor division by 4.** 180 // 4 = 45. In general `x >> k` is `x // 2**k` — note
   **floor**, so `-7 >> 1` is `-4`, not `-3`.
4. **`~a` is negative** because Python's integers behave like infinite-width two's complement.
   `~x == -x - 1` exactly, so `~180 = -181`. There is no fixed width for the sign bit to live in,
   which is also why `bin(-181)` prints `-0b10110101` rather than a bit pattern.

Note `a << 2` prints as ten bits under `{result:08b}` — the width is a *minimum*, not a truncation.
Students who expected it to wrap have imported a C intuition; Python integers never overflow.

---

## Part 3 — String Challenges

```python
reversed_text = text[::-1]                                    # '!dlroW ,olleH'
is_palindrome = word == word[::-1]                            # True for 'racecar'
vowel_count   = sum(sentence.lower().count(v) for v in "aeiou")   # 11
title_case    = " ".join(w.capitalize() for w in s.split())   # 'The Quick Brown Fox'

for n in range(1, 11):
    print(f"{n:>5} {n**2:>8} {n**3:>12}")
```

Table output:

```
    n       n²           n³
--------------------------
    1        1            1
    2        4            8
   ...
   10      100         1000
```

> **Challenge 3 traps.** `sentence.count("a")` without `.lower()` misses the capital `T`… which is
> not a vowel, so the count is still 11 here — the bug is *invisible on this input*. Test with
> `"AEIOU"` to expose it. This is a good moment to make the point that passing the given example is
> not evidence of correctness.
>
> **Challenge 4:** `.capitalize()` lowercases the rest of the word, so `"mcDonald"` → `"Mcdonald"`.
> `.title()` has the same flaw plus apostrophe handling (`"o'brien"` → `"O'Brien"` vs `"O'brien"`).
> Both are acceptable; a student who notices the limitation is ahead.

---

## Exercise 3.3 — f-String Formatting

```python
for p in (2, 4, 6, 8):
    print(f"π ≈ {pi:.{p}f}")          # nested format spec
print(f"{large:,.2f}")                 # 1,234,567.89
print(f"{small:.3e}")                  # 1.234e-05
print(f"{score:.1f}%")                 # 87.7%
print(f"255 in decimal: {255:d}")      # 255
print(f"255 in hex:     {255:x}")      # ff
print(f"255 in octal:   {255:o}")      # 377
print(f"255 in binary:  {255:b}")      # 11111111
```

Verified output:

```
π ≈ 3.14
π ≈ 3.1416
π ≈ 3.141593
π ≈ 3.14159265
1,234,567.89
1.234e-05
87.7%
```

The **nested replacement field** `{pi:.{p}f}` is the part worth showing explicitly — most students
write four separate lines, which is correct but misses that the precision can itself be computed.

Add `#` for a prefix: `{255:#x}` → `0xff`.

---

## Part 4 — Unit Converter

Accept any working implementation. The three things to check:

1. **Conversions go through a base unit.** A converter with a lookup table of factors relative to
   one canonical unit (metres, grams, …) needs *n* entries; one with pairwise conversions needs
   *n²* and will be inconsistent. Reward the first design explicitly.
2. **Input validated with `try`/`except ValueError`**, converting before checking range.
3. **Output formatted with an explicit precision** rather than dumping raw float repr.

Temperature is the one conversion that **cannot** use a pure scale factor, because it has an offset.
A student whose table-driven design handles length and mass but breaks on temperature has found a
real modelling issue — that is a good outcome, not a failure.

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

*CS 101 · Week 1 · Lab Solutions · Instructor Copy · © CSE Department*
