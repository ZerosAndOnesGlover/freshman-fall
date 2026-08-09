# CS 201 · Week 1 · Reading Guide
## CS:APP Chapter 2 — Representing and Manipulating Information

---

**Set reading:** Bryant & O'Hallaron, **§2.1–2.4**. This is the longest chapter in the book and the one with the most exercises; it repays every hour.
**Optional:** Goldberg, *What Every Computer Scientist Should Know About Floating-Point Arithmetic* (1991) — §1–2.

---

## How to Read Chapter 2

**Do the practice problems as you go.** CS:APP puts them inline with worked answers at the end of the chapter, and Chapter 2 is the one place in the book where reading without doing them genuinely does not work. Bit manipulation is a motor skill.

**Budget more time for §2.3 than you expect.** Integer arithmetic looks like the easy section and contains the subtlest material in the chapter — the sections on overflow and on signed/unsigned conversion are where the exam questions come from.

---

## Section by Section

| § | Topic | What to take from it |
|---|---|---|
| **2.1.1–2.1.3** | Hex, words, byte ordering | Get fluent at hex ↔ binary. **Little-endian** matters from Week 2 onward |
| **2.1.4–2.1.6** | Bit operations, C's operators | The distinction between `&`/`|` and `&&`/`||` — masking versus logic |
| **2.1.7–2.1.9** | Shifts | Arithmetic vs logical right shift. C's rule for signed types, and what is left unspecified |
| **2.2** | Integer representations | Two's complement formally. Mostly ECE 110 revision; read for the notation |
| **2.2.5–2.2.6** | **Signed/unsigned conversion** | **Read twice.** L04 §6's `strlen(s) - 1` bug lives here |
| **2.3.1–2.3.3** | Addition and overflow | The formal statement of what your ECE 110 adder does |
| **2.3.4–2.3.6** | Multiplication, division by shifts | Why `x / 8` is not just `x >> 3` for negative `x` |
| **2.4.1–2.4.2** | Fractional binary, IEEE 754 | This is L05. The book's Figure 2.35 is worth copying by hand |
| **2.4.3** | **Special values** | Denormals, infinity, NaN — and *why* denormals exist |
| **2.4.4–2.4.5** | Rounding, FP operations | This is L06. **Read §2.4.5 slowly** — it states non-associativity formally |
| **2.4.6** | Floating point in C | Conversion rules. `int` → `float` loses precision; `int` → `double` does not |

---

## Questions to Read Against

**On §2.1 — bits and bytes**

1. Why is hexadecimal the conventional notation for bit patterns rather than octal or decimal?
2. On a little-endian machine, the `int` `0x01234567` at address `0x100` stores which byte at `0x100`? Predict, then check with a program.
3. What does `x & (x-1)` do? Try three values before you look it up. *(This is PS 1 Q3(e)'s ancestor.)*

**On §2.2–2.3 — integers**

4. The book gives $T2U$ and $U2T$ conversion functions. Apply them to $-1$ in 32 bits, both directions.
5. Why is `-x` equal to `~x + 1`? Give the one-line algebraic argument, not the procedure.
6. For `int x`, is `x >> 3` the same as `x / 8`? Try $x = -17$. Where does the difference come from, and which one does C's `/` require?
7. CS:APP says signed overflow in C is undefined. **L04 showed GCC compiling `x + 1 > x` to a constant `1`.** Connect the two: which sentence in §2.3 licenses that?

**On §2.4 — floating point**

8. Reproduce Figure 2.35's tiny format by hand for at least three values, including one denormal.
9. Why is the exponent biased rather than two's complement? *(L05 §1 gives one reason. The book gives it too — find it.)*
10. The book states that FP addition is commutative but not associative. Give an example of each property, one showing commutativity holding and one showing associativity failing.
11. Rounding is round-to-nearest-even by default. Why *even*, rather than always rounding halves up? What bias does that avoid?

> **Question 11 is the one worth thinking hardest about.** It is the reason a long sum of values ending
> in exactly `.5` does not drift upward, and it is examinable.

---

## Reading Against the Machine

Check three of the book's claims yourself. Twenty minutes, and worth more than re-reading a section.

```bash
# 1. Byte ordering — is this machine little-endian?
python3 -c "import sys; print(sys.byteorder)"

# 2. Your own float dissector — write it, do not copy it
#    memcpy a float into an unsigned, then print sign, exponent, mantissa.
#    Test on 1.0f, -2.0f, 0.1f, FLT_MIN, FLT_MIN/2, INFINITY, NAN.

# 3. Where does float stop counting?
#    Increment a float by 1 in a loop and find where it stops changing.
#    Predict the answer from 24 bits of precision before you run it.
```

For (3): the prediction is $2^{24} = 16\,777\,216$, and **it is exact** — `2^24 + 1` rounds back to `2^24` while `2^24 + 2` is representable. *(Verified in L05 §5.)* The `double` equivalent is $2^{53} = 9\,007\,199\,254\,740\,992$, also exact: at $2^{53}-1$ adding 1 still works; at $2^{53}$ it does not. *(Verified.)*

---

## Terminology You Should Own by Week 2

| | | |
|---|---|---|
| two's complement | sign extension | arithmetic vs logical shift |
| little-endian | word size | usual arithmetic conversions |
| undefined behaviour | unspecified behaviour | implementation-defined |
| mantissa / significand | biased exponent | implicit leading 1 |
| denormal | gradual underflow | flush-to-zero |
| NaN | signed zero | ULP |
| round-to-nearest-even | absorption | catastrophic cancellation |
| Kahan summation | associativity | correctly rounded |

**The three at the bottom of the middle column** — ULP, absorption, cancellation — are the vocabulary for the rest of this topic and for MATH 341 in Year 3.

---

## If You Want More

**Goldberg (1991)**, *What Every Computer Scientist Should Know About Floating-Point Arithmetic*. Long, and the canonical reference. **Read §1 and §2**; the rest is there when you need it.

**Kahan's own writing** on the design of IEEE 754 is opinionated and excellent. He argued for denormals against significant resistance, and his account of why is the best explanation of gradual underflow available.

**`float.exposed`** and similar interactive bit-flippers let you drag bits and watch the value change. Ten minutes with one of these is worth an hour of reading Figure 2.35 — but do the hand computations in PS 1 Q2 first, or you will learn the tool instead of the format.

---

*CS 201 · Week 1 · Reading Guide*
