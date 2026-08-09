# ECE 110 · Digital Logic
## Week 0 · Reference Sheet
### Number Systems, Two's Complement, BCD

---

## Positional Notation

$$N = \sum_i d_i\, b^{\,i}, \qquad 0 \le d_i < b$$

| decimal | binary | octal | hex |
|---:|---|---|---|
| 13 | `1101` | `15` | `D` |
| 173 | `10101101` | `255` | `AD` |
| 182 | `10110110` | `266` | `B6` |
| 200 | `11001000` | `310` | `C8` |
| 255 | `11111111` | `377` | `FF` |
| 757 | `1011110101` | `1365` | `2F5` |
| 1000 | `1111101000` | `1750` | `3E8` |
| 4095 | `111111111111` | `7777` | `FFF` |

*(all verified)*

**Integers → base $b$:** repeated division, remainders read **upward**.
**Fractions → base $b$:** repeated multiplication, integer parts read **downward**.

### Binary ↔ hex ↔ octal is regrouping

$$16=2^4 \Rightarrow \text{1 hex digit} = \text{4 bits} \qquad 8=2^3 \Rightarrow \text{1 octal digit} = \text{3 bits}$$

> **Group from the RIGHT. Pad on the LEFT.** Grouping from the left is the most common error on
> this material and it silently scales the answer by a power of two.

### Which fractions are exact?

**A fraction in lowest terms terminates in base $b$ iff every prime factor of its denominator divides $b$.**

**In binary that means a power-of-two denominator, and nothing else.**

| exact | not exact |
|---|---|
| $\tfrac12, \tfrac14, \tfrac58, \tfrac3{16}, 0.6875$ | $\tfrac13, \tfrac15, \tfrac1{10}, 0.3$ |

$$0.1_{10} = 0.0001100110011001100110011\ldots_2 \qquad \texttt{0.1 + 0.2 == 0.30000000000000004}$$

*(verified / measured)*

---

## Unsigned Range

$$n \text{ bits} \Rightarrow 0 \ldots 2^n-1, \quad 2^n \text{ values}$$

| $n$ | 4 | 8 | 10 | 16 | 32 |
|---|---|---|---|---|---|
| max | 15 | 255 | 1023 | 65 535 | 4 294 967 295 |

**One more bit doubles the range.**

---

## Signed Representations

| scheme | $+5$ | $-5$ | zeros | reuses the adder? |
|---|---|---|:-:|:-:|
| Sign–magnitude | `00000101` | `10000101` | 2 | ✗ |
| One's complement | `00000101` | `11111010` | 2 | ✗ |
| **Two's complement** | `00000101` | `11111011` | **1** | **✓** |

**Negate:** invert every bit, then add one.

### Range and its asymmetry

$$-2^{\,n-1} \ \ldots\ 2^{\,n-1}-1 \qquad (n=8:\ -128\ldots127)$$

**One more negative than positive, because there is only one zero.**

$$\boxed{-(-128) = -128} \qquad\text{— unrepresentable, so the input comes back}$$

*(verified; occurs at $-2^{n-1}$ and nowhere else, at every width)*

### Sign extension

**Widen by copying the sign bit**, never by padding zeros.

| | 8-bit | 16-bit |
|---:|---|---|
| $+37$ | `00100101` | `0000000000100101` |
| $-37$ | `11011011` | `1111111111011011` |

**Zero-extending $-37$ gives $219$.** *(verified)*

---

## Carry vs Overflow — **They Are Independent**

| | meaning |
|---|---|
| **$C$ (carry-out)** | the **unsigned** result did not fit |
| **$V$ (overflow)** | the **signed** result did not fit |

$$\boxed{V = C_{\text{in, MSB}} \ \oplus\ C_{\text{out, MSB}}}$$

*(verified against true arithmetic on all **65 536** ordered 8-bit signed pairs — zero mismatches)*

### All four combinations occur

| $C$ | $V$ | example | signed | unsigned | count / 65 536 |
|:-:|:-:|---|---|---|---:|
| 0 | 0 | $30+40$ | $70$ ✓ | $70$ ✓ | 24 768 |
| 0 | 1 | $70+80$ | $-106$ ✗ | $150$ ✓ | 8 128 |
| 1 | 0 | $-30+(-40)$ | $-70$ ✓ | $186$ ✗ | 24 384 |
| 1 | 1 | $-70+(-80)$ | $106$ ✗ | $106$ ✗ | 8 256 |

*(measured)*

> **A carry out of a signed addition means nothing on its own.**
> **Opposite signs can never overflow** — the sum lies between the operands, both of which were
> representable.

---

## BCD

**Each decimal digit in its own four bits.** $1997 \to$ `0001 1001 1001 0111`.

**Codes `1010`–`1111` are illegal — $6/16 = 37.5\%$ of the code space discarded.**

### Addition needs the add-six correction

**If a digit sum exceeds 9, add `0110`; the carry comes from the correction.**

| | plain | valid? | corrected |
|---|---|:-:|---|
| $5+3$ | `01000` $=8$ | ✓ | — |
| $7+8$ | `01111` $=15$ | ✗ | `010101` → **1, 5** |
| $9+9$ | `10010` $=18$ | ✗ | `011000` → **1, 8** |

*(verified)*

**Why six:** binary carries at 16, decimal at 10, and $16-10=6$.

### Cost

| digits | BCD | binary | overhead |
|---:|---:|---:|---:|
| 1 | 4 | 4 | 0.0% |
| 2 | 8 | 7 | 14.3% |
| 3 | 12 | 10 | 20.0% |
| 4 | 16 | 14 | 14.3% |
| 8 | 32 | 27 | 18.5% |

*(measured)*

**The overhead oscillates — it does not converge** — because binary needs $\lceil d\log_2 10\rceil$ bits and the ceiling is a step function. **Bounded above by $4/\log_2 10 - 1 = 20.41\%$.**

### What BCD actually guarantees

> **Exactness for finite decimal fractions — and nothing else.** BCD is *not* more accurate in
> general: $\tfrac13$ is inexact in both, and BCD is larger and slower. **A value you can write down
> in decimal is stored as that value.** That is the whole guarantee, and for a till or a fuel pump it
> is the right one. *(`12.7 * 1.30` in binary floats gives `16.509999999999998`.)*

---

## Common Errors

1. **Grouping bits from the left** when converting to octal or hex.
2. **Zero-extending a negative number.**
3. **Not stating the width** — `1011` is $-5$ in 4 bits and $+11$ in 8.
4. **Treating carry-out as an error flag** for signed arithmetic.
5. **Assuming $V$ and $C$ imply each other.** All four combinations occur.
6. **Claiming BCD is "more accurate".** It is exact about one specific thing.

---

*ECE 110 · Week 0 · Reference Sheet*
