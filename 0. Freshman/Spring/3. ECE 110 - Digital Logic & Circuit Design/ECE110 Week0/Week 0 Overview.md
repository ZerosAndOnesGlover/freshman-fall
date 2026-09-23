# ECE 110 · Digital Logic
## Week 0 · Overview
### Number Systems — Binary, Octal, Hex, Conversions, BCD

---

**Topic:** how a machine holds a number
**Reading:** Harris & Harris §1.4 | Mano & Ciletti Ch. 1
**Assessment this week:** PS 0 (released Thu 21 Jan 14:30, due Thu 28 Jan 13:00), Lab 0 (**Fri 22 Jan**, 14:00). **No quiz** — quizzes begin in Week 2.

---

## Why This Is Week 0 And Not Week 1

**Everything after this week is about circuits.** This week is about the thing the circuits carry.

You already know that computers work in binary. **What you probably do not know is what that costs** — which numbers cannot be represented at all, which arithmetic silently gives the wrong answer, and why a design would ever choose a representation that wastes 37% of its codes on purpose.

---

## The Two Lectures

| | Day | Topic | The point |
|---|---|---|---|
| **Lecture 1** | Wednesday | Number Systems and Conversions | Base is notation; the value is the value |
| **Lecture 2** | Thursday | Signed Numbers and BCD | Representation is a design decision with costs |

---

## Positional Notation Is One Idea

$$N = \sum_{i} d_i \cdot b^{\,i}$$

**That is the whole of base conversion.** Base 2, 8, 10 and 16 differ only in how many symbols $d_i$ may take.

| decimal | binary | octal | hex |
|---:|---|---|---|
| 13 | `1101` | `15` | `D` |
| 200 | `11001000` | `310` | `C8` |
| 255 | `11111111` | `377` | `FF` |
| 1000 | `1111101000` | `1750` | `3E8` |
| 4095 | `111111111111` | `7777` | `FFF` |

*(All verified.)*

**Hex and octal exist only because 16 and 8 are powers of two.** One hex digit is exactly four bits and one octal digit exactly three, so conversion is regrouping rather than arithmetic. **Ten is not a power of two, and that single fact is the source of most of this week's difficulty.**

---

## The Thing Base Ten Hides

**$0.1$ has no finite binary representation.**

$$0.1_{10} = 0.0001100110011001100110011\ldots_2$$

*(Verified — the pattern `0011` repeats forever.)*

**This is not a rounding bug and it is not fixable.** It is the same fact as $\tfrac13$ having no finite decimal expansion, and it is why

```
>>> 0.1 + 0.2
0.30000000000000004
```

*(Measured.)*

> **You will meet this again in CS 201 and in every language you ever use.** The place to understand
> it is here, where you can see the bits.

---

## Signed Numbers: Why Two's Complement Won

**Three schemes can represent negatives; only one lets you reuse the adder.**

| scheme | $-5$ in 8 bits | two zeros? | needs a separate subtractor? |
|---|---|---|---|
| Sign–magnitude | `10000101` | **yes** | yes |
| One's complement | `11111010` | **yes** | yes |
| **Two's complement** | `11111011` | **no** | **no** |

**Two's complement wins because subtraction becomes addition** — and that means Week 3's adder is the only arithmetic circuit you have to build.

### The asymmetry, and the bug it causes

**8-bit two's complement spans $-128$ to $+127$.** There is one more negative value than positive, because there is only one zero.

$$-(-128) = -128 \qquad \textbf{(verified)}$$

**Negating the most negative number returns it unchanged.** No flag is raised by the negation itself. **This is a real bug class**, not a curiosity, and you will write the check for it in PS 0.

---

## BCD: Paying For Decimal On Purpose

**Binary-coded decimal stores each decimal digit in its own four bits.** It is deliberately wasteful:

| digits | max value | BCD bits | binary bits | waste |
|---:|---:|---:|---:|---|
| 2 | 99 | 8 | 7 | 1 |
| 3 | 999 | 12 | 10 | 2 |
| 4 | 9999 | 16 | 14 | 2 |
| 8 | 99 999 999 | 32 | 27 | **5** |

*(Verified.)* **Six of every sixteen codes — `1010` through `1111` — are illegal, so 37.5% of the code space is thrown away.**

**And its arithmetic needs a correction step.** Adding two BCD digits in plain binary can land in the illegal range, and the fix is to add six:

| sum | plain binary | valid? | corrected |
|---|---|---|---|
| $5+3$ | `01000` = 8 | ✓ | — |
| $7+8$ | `01111` = 15 | ✗ | $+\,0110 \to$ `010101` = **1 5** |
| $9+9$ | `10010` = 18 | ✗ | $+\,0110 \to$ `011000` = **1 8** |

*(Verified.)*

> **So why would anyone use it?** Because a till, a fuel pump and a financial ledger must round the
> way a human expects, and $0.1$ is exact in BCD. **The 37% waste buys exact decimal fractions**, and
> for those applications that is the right trade. **This is the course's first design decision with a
> measurable cost on both sides.**

---

## This Week's Work

1. **Lab 0** — the conversion bench. Build the tools you will use for the rest of the term.
2. **PS 0** — conversions, two's complement, overflow detection, BCD.
3. **No quiz.** Quizzes begin Week 2 and are ungraded throughout.

---

*Next: Wednesday — Number Systems and Conversions*
