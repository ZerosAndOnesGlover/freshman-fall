# ECE 110 · Digital Logic
## Week 0 · Lecture 1 (Wednesday)
### Number Systems and Conversions

---

**Reading:** Harris & Harris §1.4 | Mano & Ciletti §1.1–1.3
**No quiz this week.** Quizzes begin Week 2, and they are ungraded throughout.

---

## 1. One Idea, Four Bases

**A positional numeral is a polynomial evaluated at the base:**

$$N = \sum_{i} d_i \cdot b^{\,i}, \qquad 0 \le d_i < b$$

**That is the entire content of base conversion.** $427_{10}$ means $4\cdot10^2+2\cdot10^1+7\cdot10^0$; $1011_2$ means $1\cdot2^3+0\cdot2^2+1\cdot2^1+1\cdot2^0=11$. **Nothing else is going on.**

| decimal | binary | octal | hex |
|---:|---|---|---|
| 13 | `1101` | `15` | `D` |
| 200 | `11001000` | `310` | `C8` |
| 255 | `11111111` | `377` | `FF` |
| 1000 | `1111101000` | `1750` | `3E8` |
| 4095 | `111111111111` | `7777` | `FFF` |

*(All verified.)*

> **The value never changes.** $255$, `11111111` and `FF` are three spellings of one number. **Base is
> notation.** Students who lose marks in this course lose them by forgetting that.

---

## 2. Converting *To* Another Base

### Integers — repeated division

**Divide by the target base; the remainders are the digits, LSB first.**

$$1000 \div 2 \to \text{remainders } 0,0,0,1,0,1,1,1,1,1$$

**Read them upward:** `1111101000`. *(Verified: $1111101000_2 = 1000$.)*

### Fractions — repeated multiplication

**Multiply by the base; the integer parts are the digits, MSB first.**

$$0.625 \times 2 = \mathbf{1}.25 \quad 0.25\times2=\mathbf{0}.5 \quad 0.5\times2=\mathbf{1}.0 \;\Rightarrow\; 0.101_2$$

*(Verified exact.)*

**But this does not always terminate:**

$$\tfrac13 = 0.010101010101\ldots_2 \qquad\textbf{(verified, recurring)}$$

---

## 3. Why Hex and Octal Exist

**Because 16 and 8 are powers of two, and 10 is not.**

$$16 = 2^4 \implies \text{one hex digit} \equiv \text{exactly four bits}$$
$$8 = 2^3 \implies \text{one octal digit} \equiv \text{exactly three bits}$$

**So binary ↔ hex is regrouping, not arithmetic:**

$$\underbrace{0011}_{3}\ \underbrace{1110}_{E}\ \underbrace{1000}_{8} \;=\; \texttt{3E8}_{16} \;=\; 1000_{10}$$

**Group from the right, pad the left with zeros.** *(Padding on the wrong side is the single most common error on this material, and it silently multiplies your answer by a power of two.)*

> **Hex is not a different number system. It is binary written four bits at a time**, for people who
> cannot read thirty-two ones and zeros without losing their place. **Nobody computes in hex; they
> read in hex.**

---

## 4. The Consequence Of Ten Not Being A Power Of Two

**$0.1$ cannot be written exactly in binary.** Apply repeated multiplication:

$$0.1_{10} = 0.0001100110011001100110011\ldots_2$$

*(Verified — `0011` repeats forever.)*

**A finite machine must therefore truncate**, and

```
>>> 0.1 + 0.2
0.30000000000000004
```

*(Measured, IEEE-754 double precision.)*

**This is not a defect in the hardware and it is not fixable by using more bits.** It is the same fact as $\tfrac13$ having no finite decimal expansion. A base-$b$ fraction terminates exactly when its denominator's prime factors all divide $b$; **$10 = 2\cdot5$ and $5 \nmid 2$**, so a tenth cannot terminate in binary.

> **Which fractions *are* exact in binary?** Those with a power-of-two denominator, and only those.
> $\tfrac12,\tfrac14,\tfrac58,\tfrac{3}{16}$ — exact. $\tfrac1{10},\tfrac13,\tfrac15$ — never.

**Week 11 will show you the memory cell that stores these bits. Week 0 is where you learn what they can and cannot mean.**

---

## 5. How Many Bits Do I Need?

**To represent $N$ distinct values you need $\lceil \log_2 N\rceil$ bits.** For unsigned integers in $n$ bits:

$$\text{range } 0 \ldots 2^n-1, \qquad \text{count } 2^n$$

| $n$ | max unsigned | familiar as |
|---:|---:|---|
| 4 | 15 | one hex digit, one BCD digit |
| 8 | 255 | a byte |
| 10 | 1023 | ~1K |
| 16 | 65 535 | a 16-bit port |
| 32 | 4 294 967 295 | an IPv4 address space |

**Adding one bit doubles the range.** It does not add a fixed amount — a fact that will decide several design arguments later in the course.

---

## 6. What To Take From This Lecture

1. **A numeral is a polynomial in its base.** One idea, four bases.
2. **Integers convert by repeated division; fractions by repeated multiplication.**
3. **Hex and octal are regroupings of binary**, which is the only reason they are used.
4. **Group from the right and pad on the left.**
5. **$0.1$ is not representable in binary**, and no amount of precision fixes it.
6. **$n$ bits give $2^n$ values.** One more bit doubles the range.

---

*Next: Thursday — Signed Numbers and BCD*
