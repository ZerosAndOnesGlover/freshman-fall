# ECE 110 · Digital Logic
## Problem Set 0
### Topic: Number Systems, Two's Complement, and BCD
**Released:** Thursday, Week 0 · **Due:** Thursday, Week 1 at the start of class

---

> **Show the working, not just the answer.** A conversion with no method shown earns half marks even
> when it is right, because the method is what Week 3 will need.
>
> **Every answer here can be checked by converting back.** Do that before you submit — it costs
> thirty seconds and catches nearly everything.
>
> **State the width.** "Two's complement" is meaningless without a bit width; `1011` is $-5$ in four
> bits and $+11$ in eight.

---

## Part A — Conversions (5 pts each)

**A1.** Convert $173_{10}$ to binary, octal and hexadecimal.

*Note: one of your three answers will look startlingly like a decimal number you recognise. It is a coincidence of this particular value, not an error.*

**A2.** Convert $10110110_2$ to decimal, octal and hexadecimal. **Do the octal and hex by regrouping, not by going through decimal**, and show the groupings.

**A3.** Convert $\texttt{0x2F5}$ to decimal and to binary.

**A4.** Convert $0.6875_{10}$ and $0.3_{10}$ to binary, to at most ten fractional bits.
For each, **say whether the representation is exact**, and justify the answer from the denominator rather than from the pattern you observe.

---

## Part B — Two's Complement (5 pts each)

**B1.** Give the **8-bit two's complement** encoding of $-37$, $-100$, $-1$ and $-128$.

**B2.** State the range of an $n$-bit two's complement number, then give it for $n=8$.
**Explain in one sentence why the range is asymmetric**, referring to the number of zeros.

**B3.** Sign-extend $-37$ and $+37$ from 8 bits to 16 bits.
**What decimal value would $-37$ take if you zero-extended it instead?**

**B4.** Compute $-(-128)$ in 8-bit two's complement, showing the invert-and-add-one steps.
**Explain what has happened**, and state the general rule for which value this occurs at in $n$ bits.

**B5.** Write pseudocode for a function `safe_negate(x, n)` that returns $-x$ in $n$-bit two's complement, or signals an error rather than returning a wrong answer. **The whole mark is in the guard.**

---

## Part C — Carry and Overflow (6 pts each)

**C1.** For each of the following 8-bit additions, give the binary sum, the **carry-out $C$**, the **overflow flag $V$**, the result read as **signed**, and the true mathematical value:

**(a)** $70 + 80$  **(b)** $-70 + (-80)$  **(c)** $90 + (-100)$  **(d)** $127 + 1$  **(e)** $-1 + (-1)$

*Lay this out as a table.*

**C2.** From your C1 table, find **one row where $C=1$ but the signed answer is correct**, and **one row where $C=0$ but the signed answer is wrong**.
**What do these two rows together establish?**

**C3.** State the overflow detection rule in terms of the carries at the most significant bit, and **verify it by hand on rows (a) and (c)** of C1 — showing the two carry bits explicitly.

**C4.** **Prove** that adding two numbers of *opposite* sign can never overflow.
*A one-paragraph argument bounding the magnitude of the result is what is wanted; no algebra with bits is required.*

**C5.** A processor computes $200 + 100$ in 8 bits and raises $C=1$, $V=0$.
**A program reads the result as unsigned and gets 44. A second program reads the same bits as signed and gets 44.** Explain, in two sentences, why exactly one of those programs has a bug.

---

## Part D — BCD (5 pts each)

**D1.** Encode $1997$ and $405$ in BCD. For each, state **how many bits BCD uses** and **how many plain binary would need**.

**D2.** Add $47 + 38$ in BCD, digit by digit, showing the correction step and where the carry comes from.

**D3.** **Why is the correction constant six?** Answer in terms of where binary carries and where decimal carries.

**D4.** BCD discards codes `1010` through `1111`. **What fraction of the 4-bit code space is that?**
Then: for an 8-digit value, how many bits does BCD use against plain binary?

**D5.** A fuel pump computes the price of $12.7$ litres at $1.30$ per litre.
**Explain why its designer chose BCD over binary**, and state precisely what the 37.5% waste bought. *One paragraph. "It is more accurate" earns nothing — say what is exact and what is not.*

---

## Marking Summary

| Part | Problems | Points |
|---|---|---|
| A — Conversions | 4 × 5 | 20 |
| B — Two's complement | 5 × 5 | 25 |
| C — Carry and overflow | 5 × 6 | 30 |
| D — BCD | 5 × 5 | 25 |
| **Total** | | **100** |

---

> **Before you submit:** convert every Part A answer back to decimal, and check every Part C row by
> adding the true values. **Both checks are mechanical and both are worth more than they cost.**

---

*ECE 110 · Problem Set 0 · due Thursday of Week 1*
