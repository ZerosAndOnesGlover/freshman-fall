# ECE 110 · Digital Logic
## Lab 0: Number Systems and the Conversion Bench
### Week 0 Lab Session

**Date:** Friday 22 January 2027 · 14:00–15:50 · Lab section (Week 0) — after both of Week 0's lectures

---

**Duration:** 2 hours (MEC 110)
**Format:** Pairs. **Both partners submit their own report.**
**Graded on:** completion + correctness — **100 points**
**Tools:** Python 3. No breadboard this week — the hardware starts in Lab 2.

---

## Overview

**This lab builds the instrument, not the result.**

You will write a small set of conversion and arithmetic functions and then **use them to test claims** — including two claims that turn out to be false in the obvious formulation. From Lab 1 onward, every circuit you build will be checked against a reference model like this one. **Getting comfortable with exhaustive checking now is the point of the session.**

> **The rule for the whole course, stated once:** a circuit or a claim is not verified because it
> looks right. It is verified because you enumerated the cases.

---

## Part A — The Conversion Bench (25 pts)

**A1 (10 pts).** Write and test:

```
to_base(n, b)        # non-negative integer -> string of digits in base b
from_base(s, b)      # string of digits in base b -> integer
frac_to_binary(f, k) # fraction in [0,1) -> k binary fractional digits + a flag
                     #   flag says whether the expansion terminated within k
```

**Do not use built-in `bin`, `oct`, `hex` or `int(s, b)` in the implementations.** You may use them in your tests, and you should.

**A2 (8 pts).** **Round-trip test.** For every $n$ from $0$ to $4095$ and every base $b \in \{2,3,8,16\}$, check `from_base(to_base(n,b), b) == n`.

**Report the number of cases tested and the number of failures.**

**A3 (7 pts).** Using `frac_to_binary`, determine which of

$$\tfrac12,\quad \tfrac14,\quad \tfrac15,\quad \tfrac58,\quad \tfrac1{10},\quad \tfrac3{16},\quad \tfrac13$$

**terminate in binary.** Then state the rule that predicts it, and **confirm your rule predicts all seven correctly.**

---

## Part B — Two's Complement (30 pts)

**B1 (8 pts).** Write `encode(x, n)` and `decode(bits, n)` for $n$-bit two's complement.

**Round-trip test them over the entire 8-bit range**, $-128$ to $127$. Report cases tested and failures.

**B2 (7 pts).** Find, by search rather than by assertion, **every 8-bit value $x$ for which `decode(encode(-x, 8), 8) != -x`.**

**Report the list.** Then state the general rule for $n$ bits and **confirm it by running the same search at $n = 4$ and $n = 16$.**

**B3 (8 pts).** Implement `add_n(a, b, n)` returning `(sum_bits, carry_out, overflow)`, where overflow is computed from the **carries at the most significant bit** — not by comparing against Python's arithmetic.

**B4 (7 pts).** **Now test it against Python's arithmetic**, over all $65\,536$ ordered pairs of 8-bit signed values.

**Report the number of mismatches.** *(If it is not zero, your rule is wrong — fix it before continuing, and say in the report what was wrong.)*

---

## Part C — Where Carry and Overflow Disagree (20 pts)

**C1 (8 pts).** Using B3, **count** over all $65\,536$ 8-bit pairs how many fall into each cell:

| | $V=0$ | $V=1$ |
|---|---|---|
| $C=0$ | | |
| $C=1$ | | |

**C2 (6 pts).** From your data, **produce one concrete example of each of the four cells**, giving the operands in decimal and the result read both ways.

**C3 (6 pts).** **Are the two flags independent?** Answer from the table in C1, not from intuition, and say what "independent" means for your answer to be meaningful.

---

## Part D — BCD (25 pts)

**D1 (10 pts).** Write `to_bcd(n)` and `bcd_add(a, b)` — the latter operating digit by digit **with the add-six correction**, not by converting to integers and back.

**Test `bcd_add` against ordinary addition for every pair $a, b$ with $0 \le a, b \le 999$.** Report cases and failures.

**D2 (8 pts).** For $d = 1, 2, \ldots, 10$ decimal digits, tabulate **BCD bits**, **binary bits**, and the **percentage overhead**.

**Does the overhead converge, grow, or oscillate as $d$ increases?** Answer from your table.

**D3 (7 pts).** **The claim to test:** *"BCD is exact for money, binary is not."*

Compute $0.10 + 0.20$ three ways — in Python floats, in BCD via your `bcd_add` on cent values, and exactly with `fractions.Fraction`. **Report all three.**

Then state **precisely** what BCD is exact about. *A claim that BCD is "more accurate in general" is false and will be marked as false — say what the actual guarantee is.*

---

## Marking Summary

| Part | Points |
|---|---|
| A — the conversion bench | 25 |
| B — two's complement | 30 |
| C — carry vs overflow | 20 |
| D — BCD | 25 |
| **Total** | **100** |

---

## Submission

**One report per person**, with your code and your measured tables. **Every count you report — cases tested, failures, cell totals — must come from a run, not from expectation.**

> **A report that says "all tests passed" without the number of tests earns half marks.** The number
> is the evidence.

---

*ECE 110 · Week 0 · Lab 0*
