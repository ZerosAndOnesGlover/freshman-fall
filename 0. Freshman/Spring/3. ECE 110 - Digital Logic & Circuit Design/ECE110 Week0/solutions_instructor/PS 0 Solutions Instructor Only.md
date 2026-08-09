# ECE 110 · Digital Logic
## Problem Set 0 — Solutions
### INSTRUCTOR / TA COPY — not for distribution

---

**Total: 100 points.** All values verified by computation.

---

## Part A — Conversions (5 pts each)

### A1 (5)

$$173_{10} = \boxed{10101101_2} = \boxed{255_8} = \boxed{\texttt{AD}_{16}}$$

*(Verified.)*

> **The coincidence flagged in the problem:** $173_{10} = 255_8$. **This is not the byte-sized 255**
> — that one is $377_8$. Students who "recognise" 255 and write $11111111_2$ have made exactly the
> mistake the note warned about, and the round-trip check catches it.

*Marking: 2 + 1.5 + 1.5. **Deduct 1 for no working shown** even when all three are right.*

### A2 (5)

$$10110110_2 = \boxed{182_{10}}$$

**By regrouping** — this is what the marks are for:

$$\underbrace{10}_{2}\ \underbrace{110}_{6}\ \underbrace{110}_{6} = \boxed{266_8} \qquad \underbrace{1011}_{\texttt{B}}\ \underbrace{0110}_{6} = \boxed{\texttt{B6}_{16}}$$

*(Verified.)*

*Marking: 1 decimal, 2 octal, 2 hex. **Groupings must be shown.** A student who converts through decimal earns 1 of the 4 for octal+hex — the exercise is the regrouping.*

**Note the left-padding:** $10110110$ has eight bits, so the octal grouping is $\underline{010}\,110\,110$ — the leading group is padded to three. Grouping from the left instead gives $101\,101\,10 \to 5,5,2$ and a wrong answer.

### A3 (5)

$$\texttt{0x2F5} = 2\cdot256 + 15\cdot16 + 5 = \boxed{757_{10}} = \boxed{1011110101_2}$$

*(Verified.)* **Binary directly from the hex digits:** `0010 1111 0101`, leading zeros dropped.

### A4 (5)

**$0.6875$:**

$$0.6875 \times 2 = \mathbf{1}.375 \to \mathbf{0}.75 \to \mathbf{1}.5 \to \mathbf{1}.0 \implies \boxed{0.1011_2} \quad \textbf{exact}$$

*(Verified: $0.1011_2 = \tfrac{11}{16} = 0.6875$.)*

**$0.3$:**

$$0.3_{10} = 0.0100110011001100\ldots_2 \quad \textbf{not exact}$$

*(Verified — `1100` repeats.)*

**The justification must come from the denominator:** $0.6875 = \tfrac{11}{16}$ and $16=2^4$, so it terminates. $0.3 = \tfrac3{10}$ and $10 = 2\cdot5$; the factor 5 does not divide 2, so it cannot.

*Marking: 2 + 2, plus **1 for justifying from the denominator rather than from the observed pattern.** "It repeats, so it isn't exact" is circular and loses that mark.*

---

## Part B — Two's Complement (5 pts each)

### B1 (5)

| value | 8-bit two's complement |
|---:|---|
| $-37$ | `11011011` |
| $-100$ | `10011100` |
| $-1$ | `11111111` |
| $-128$ | `10000000` |

*(All verified.)*

*Marking: 1.25 each. **$-1$ being all ones and $-128$ being the lone MSB are the two worth checking** — they are the values students most often get by pattern rather than by method.*

### B2 (5)

$$-2^{\,n-1} \ \ldots\ 2^{\,n-1}-1 \qquad\Longrightarrow\qquad n=8:\ \boxed{-128 \ \ldots\ 127}$$

**Why asymmetric:** the $2^n$ codes are split into one zero and $2^n-1$ non-zero values. **Sign–magnitude and one's complement spend two codes on zero and get a symmetric range; two's complement spends one, so the extra code goes to the negatives.**

*Marking: 3 range, 2 explanation. **The explanation must mention the single zero.***

### B3 (5)

$$-37: \texttt{11011011} \to \boxed{\texttt{1111111111011011}} \qquad +37: \texttt{00100101} \to \boxed{\texttt{0000000000100101}}$$

*(Verified.)*

**Zero-extending $-37$ gives $\boxed{219}$** — the 8-bit pattern read as an unsigned 16-bit number.

*Marking: 2 + 1 + 2. **The 219 is the mark that matters**; it is what makes the rule more than a ritual.*

### B4 (5)

$$-128 = \texttt{10000000} \ \xrightarrow{\text{invert}}\ \texttt{01111111} \ \xrightarrow{+1}\ \texttt{10000000} = -128$$

$$\boxed{-(-128) = -128}$$

*(Verified.)*

**What has happened:** $+128$ is outside the representable range, so there is no correct answer to return. **The operation is not defined and the hardware returns the input.**

**General rule:** this occurs at $x = -2^{\,n-1}$, **and only there**, for every width $n$.

*Marking: 2 working, 2 explanation, 1 general rule. **"The computer makes a mistake" earns 0 of the explanation marks** — the value is unrepresentable, which is a different and more useful statement.*

### B5 (5)

```
function safe_negate(x, n):
    min_val = -(2 ** (n - 1))
    if x == min_val:
        raise OverflowError          # -x is not representable in n bits
    return -x
```

*Marking: **all 5 are in the guard.** A correct negation with no check earns 0. Accept any signalling mechanism — exception, error return, status flag — provided it is not a wrong value.*

---

## Part C — Carry and Overflow (6 pts each)

### C1 (6)

| | binary | sum | signed | $C$ | $V$ | true |
|---|---|---|---:|:-:|:-:|---:|
| **(a)** $70+80$ | `01000110`+`01010000` | `10010110` | $-106$ | 0 | **1** | $150$ |
| **(b)** $-70+(-80)$ | `10111010`+`10110000` | `01101010` | $+106$ | **1** | **1** | $-150$ |
| **(c)** $90+(-100)$ | `01011010`+`10011100` | `11110110` | $-10$ | 0 | 0 | $-10$ ✓ |
| **(d)** $127+1$ | `01111111`+`00000001` | `10000000` | $-128$ | 0 | **1** | $128$ |
| **(e)** $-1+(-1)$ | `11111111`+`11111111` | `11111110` | $-2$ | **1** | 0 | $-2$ ✓ |

*(All verified.)*

*Marking: 1.2 per row, all five columns required.*

### C2 (6)

- **$C=1$, signed answer correct:** row **(e)**, $-1+(-1)=-2$.
- **$C=0$, signed answer wrong:** row **(a)**, $70+80$ giving $-106$, or row **(d)**.

**What the pair establishes:** **carry-out and overflow are independent** — neither implies the other, in either direction. **A carry out of a signed addition carries no information about whether the signed result is correct.**

*Marking: 2 + 2 + 2. **The conclusion must be about independence**, not merely "they are different".*

### C3 (6)

$$V = C_{\text{in, MSB}} \oplus C_{\text{out, MSB}}$$

**Row (a), $70+80$:** bit 6 gives $1+1+0$, so the carry **into** bit 7 is $1$; bit 7 gives $0+0+1 = 1$ with no carry out, so $C_{out}=0$. $V = 1\oplus0 = \mathbf{1}$ ✓

**Row (c), $90+(-100)$:** the carry into bit 7 is $0$; bit 7 gives $0+1+0=1$, carry out $0$. $V = 0\oplus0 = \mathbf{0}$ ✓

*(Verified — and the rule agrees with true arithmetic on **all 65 536** 8-bit signed pairs.)*

*Marking: 2 rule, 2 per hand-check. **Both carry bits must appear explicitly.***

### C4 (6)

**Proof.** Let $a \ge 0 > b$. Then $a + b \le a$ and $a + b > b$, so the sum lies in $[\,b,\,a\,]$ — **between the two operands.** Both operands are representable by assumption, and the representable range is an interval, so the sum is representable. **Therefore no overflow.**

*Marking: 6. **The argument must bound the result by the operands and invoke that the range is an interval.** A bit-level argument about carries is acceptable if correct, but is longer.*

### C5 (6)

$200+100$ in 8 bits gives `00101100` $= 44$, with $C=1$, $V=0$.

**The unsigned reader has the bug.** It intended $300$, which does not fit in 8 bits; the carry flag is precisely the hardware telling it so, and it ignored the flag.

**The signed reader does not.** Read as signed, the operands are $-56$ and $+100$, whose sum is $+44$ — **which is exactly what it got**, and $V=0$ confirms it. Its answer is correct *for the numbers it thinks it has*.

*Marking: 3 + 3. **Full marks require noticing that the signed reader's operands are $-56$ and $+100$**, not 200 and 100 — that is what makes its answer genuinely correct rather than accidentally so.*

---

## Part D — BCD (5 pts each)

### D1 (5)

$$1997 \to \texttt{0001 1001 1001 0111} \qquad 405 \to \texttt{0100 0000 0101}$$

| | BCD bits | binary bits |
|---|---:|---:|
| 1997 | 16 | 11 |
| 405 | 12 | 9 |

*(Verified.)*

### D2 (5)

**Units:** $7+8 = 15 = \texttt{01111}$ — **invalid**, so add six: $\texttt{01111}+\texttt{0110} = \texttt{010101}$ → digit **5**, carry **1**.
**Tens:** $4+3+1 = 8 = \texttt{1000}$ — valid, digit **8**.

$$\boxed{47+38 = 85}$$

*(Verified.)*

**The carry comes from the correction**, not from the raw binary addition — $\texttt{01111}$ has no carry out of bit 3 until the six is added.

*Marking: 3 digits, 2 for locating the carry. **The carry's origin is the mark students miss.***

### D3 (5)

**Binary carries at 16; decimal carries at 10.** Adding $16-10 = 6$ pushes an out-of-range sum past the binary carry boundary, which both produces the decimal carry and leaves the correct residue behind.

*Marking: 5. **Both numbers must appear.** "Because six is the number of unused codes" is the same arithmetic seen from a different angle and is also accepted.*

### D4 (5)

**Codes `1010`–`1111` are 6 of 16:**

$$\frac{6}{16} = \boxed{37.5\%}$$

**Eight digits:** BCD **32 bits**, binary **27 bits**. *(Verified.)*

### D5 (5)

**The pump must charge $12.7 \times 1.30 = 16.51$ and print exactly that.**

**In binary, neither $12.7$ nor $1.30$ is representable**, and the product is not either:

```
>>> 12.7 * 1.30
16.509999999999998
>>> 12.7 * 1.30 == 16.51
False
```

*(Measured. Exactly: $\tfrac{127}{10}\cdot\tfrac{13}{10} = \tfrac{1651}{100}$.)*

**The product is off by a fraction of a cent**, and rounding it for display can disagree with the arithmetic a customer does by hand. Across millions of transactions the discrepancies are systematic rather than random, and they are auditable.

**In BCD each decimal digit is stored as itself**, so a value that can be written down in decimal is held as that value and no conversion error exists. **The 37.5% waste bought exactness for finite decimal fractions — and nothing else.**

*Marking: 5. **Deduct 3 for any answer resting on BCD being "more accurate".** It is not: $\tfrac13$ is inexact in both, and BCD is larger and slower. The guarantee is specifically about finite decimal fractions.*

---

## Marking Summary

| Part | Points |
|---|---|
| A — Conversions | 20 |
| B — Two's complement | 25 |
| C — Carry and overflow | 30 |
| D — BCD | 25 |
| **Total** | **100** |

---

## The Six Errors To Expect

1. **A1:** writing $11111111_2$ for $255_8$ — the flagged coincidence, caught by converting back.
2. **A2:** grouping bits from the left instead of the right.
3. **A4:** justifying exactness from the observed pattern instead of the denominator.
4. **B3:** zero-extending a negative value.
5. **C2:** concluding the flags are "different" rather than **independent**.
6. **D5:** claiming BCD is more accurate in general.

---

*ECE 110 · Week 0 · PS 0 Solutions · Instructor Only*
