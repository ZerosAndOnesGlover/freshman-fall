# ECE 110 · Digital Logic
## Week 0 · Lecture 2 (Thursday)
### Signed Numbers and BCD

---

**Reading:** Harris & Harris §1.4.6 | Mano & Ciletti §1.5–1.7
**PS 0** released today, due Thursday of Week 1.

---

## 1. There Is No Minus Sign

**A register holds bits. It does not hold a symbol for "negative".** So a negative number must be *encoded* in those bits, and how you encode it is a design decision with consequences.

**Three schemes have been used. Two of them lost.**

| scheme | rule | $+5$ | $-5$ |
|---|---|---|---|
| **Sign–magnitude** | MSB is the sign, rest is magnitude | `00000101` | `10000101` |
| **One's complement** | negate by inverting every bit | `00000101` | `11111010` |
| **Two's complement** | negate by inverting, then adding 1 | `00000101` | `11111011` |

*(All verified.)*

---

## 2. Why Two's Complement Won

**Two reasons, and the second is the one that matters.**

### It has one zero

Sign–magnitude has `00000000` and `10000000` — **positive zero and negative zero.** So does one's complement. **Every comparison against zero then needs two tests**, and a whole class of bugs lives in the gap.

**Two's complement has exactly one zero.**

### It makes subtraction into addition

$$A - B = A + (-B)$$

**In two's complement the ordinary binary adder computes this correctly with no modification.** In the other two schemes it does not — they need end-around carry, or a separate subtractor, or both.

> **This is the whole argument.** Week 3 builds one adder. In two's complement, that one circuit does
> addition *and* subtraction. **A representation that halves your hardware wins**, and it is why every
> processor you will ever use has made this choice.

---

## 3. The Range Is Not Symmetric

**In $n$ bits, two's complement spans:**

$$-2^{\,n-1} \ \ldots \ 2^{\,n-1}-1$$

**For 8 bits: $-128$ to $+127$.** There is **one more negative value than positive**, precisely because there is only one zero to spend.

### The bug this creates

$$-(-128) = -128 \qquad \textbf{(verified)}$$

**Negating the most negative number returns it unchanged.** Invert `10000000` to get `01111111`, add 1, and you are back at `10000000`.

> **There is no representable answer**, so the hardware returns the input. **This is a live bug class,
> not a curiosity** — `abs()` of the most negative integer is wrong in C, in Java, and in most
> assembly. You will write the detector in PS 0.

---

## 4. Sign Extension

**Widening a two's complement number means copying the sign bit**, not padding with zeros.

| value | 8-bit | 16-bit |
|---:|---|---|
| $+5$ | `00000101` | `0000000000000101` |
| $-5$ | `11111011` | `1111111111111011` |
| $-128$ | `10000000` | `1111111110000000` |
| $+127$ | `01111111` | `0000000001111111` |

*(All verified.)*

**Zero-padding $-5$ would give $251$.** The distinction between sign extension and zero extension is a real instruction-set decision you will meet again in CS 201.

---

## 5. Carry And Overflow Are Different Flags

**This is the most-missed idea in Week 0, so it gets its own section.**

- **Carry-out** is the bit that falls off the top. It means the **unsigned** result did not fit.
- **Overflow** means the **signed** result did not fit.

**They are independent.** Watch:

| sum | carry-out | overflow | as unsigned | as signed |
|---|---|---|---|---|
| $200+100$ | **1** | **0** | $44$ *(wrong, wrapped)* | $44$ *(right)* |
| $60+70$ | **0** | **1** | $130$ *(right)* | $-126$ *(wrong)* |

*(Both measured.)*

**The same adder produced both.** Whether a result is wrong depends entirely on how you agreed to *read* the bits — and the hardware raises both flags and lets the program decide which one it cares about.

### The detection rule

$$V \;=\; C_{\text{in, MSB}} \ \oplus\ C_{\text{out, MSB}}$$

**Overflow occurred exactly when the carry into the sign bit differs from the carry out of it.**

*(Verified exhaustively: this rule agrees with the true arithmetic on **all 65 536** ordered pairs of 8-bit signed values — zero mismatches.)*

**Worked cases:**

| | binary | result | $C_{out}$ | $V$ | true |
|---|---|---|---|---|---|
| $60+70$ | `00111100`+`01000110`=`10000010` | $-126$ | 0 | **1** | $130$ |
| $-60+-70$ | `11000100`+`10111010`=`01111110` | $+126$ | 1 | **1** | $-130$ |
| $100+(-40)$ | `01100100`+`11011000`=`00111100` | $+60$ | 1 | 0 | $60$ ✓ |
| $-128+(-1)$ | `10000000`+`11111111`=`01111111` | $+127$ | 1 | **1** | $-129$ |

*(All verified.)* **Note row three: carry-out is 1 and the answer is perfectly correct.** A carry out of a signed addition means nothing on its own.

> **Adding two numbers of opposite sign can never overflow.** The magnitude of the result is bounded
> by the larger operand, which was representable. **Overflow requires like signs** — and the result
> then has the wrong sign, which is the other way to detect it.

---

## 6. BCD — Buying Decimal, And Paying For It

**Binary-coded decimal gives each decimal digit its own four bits.** $1997$ becomes `0001 1001 1001 0111`.

### It is deliberately wasteful

**Four bits hold sixteen codes; BCD uses ten.** Codes `1010`–`1111` are illegal — **37.5% of the space discarded.**

| digits | max value | BCD bits | binary bits | wasted |
|---:|---:|---:|---:|---:|
| 2 | 99 | 8 | 7 | 1 |
| 3 | 999 | 12 | 10 | 2 |
| 4 | 9999 | 16 | 14 | 2 |
| 8 | 99 999 999 | 32 | 27 | **5** |

*(Verified.)*

### Its arithmetic needs a correction

**Adding BCD digits in a plain binary adder can land in the illegal range. The fix is to add six.**

| | plain binary | valid BCD? | corrected |
|---|---|---|---|
| $5+3$ | `01000` $=8$ | ✓ | — |
| $7+8$ | `01111` $=15$ | ✗ | $+\,0110\Rightarrow$ `010101` = digits **1, 5** |
| $9+9$ | `10010` $=18$ | ✗ | $+\,0110\Rightarrow$ `011000` = digits **1, 8** |

*(All verified.)*

**Why six?** Because binary carries at 16 and decimal carries at 10; adding $16-10=6$ pushes an out-of-range sum past the binary carry and re-aligns the digits.

### So why use it at all?

**Because $0.1$ is exact in BCD and never exact in binary.**

> A till, a fuel pump, a payroll system and a financial ledger must round the way a human expects.
> **BCD spends 37% of its code space to buy exact decimal fractions**, and for those applications
> that is the correct trade. **This is the first design decision in the course with a real cost on
> both sides** — and there will be one nearly every week from here.

---

## 7. What To Take From This Lecture

1. **Registers hold bits, not signs.** Negativity is an encoding.
2. **Two's complement won because subtraction becomes addition** — one adder does both.
3. **The range is asymmetric**, and $-(-128)=-128$ is a real bug, not a trick question.
4. **Widen by copying the sign bit.**
5. **Carry and overflow are independent flags**; $V = C_{in} \oplus C_{out}$, verified over all 65 536 cases.
6. **Opposite signs cannot overflow.**
7. **BCD wastes 37.5% of its codes to make decimal fractions exact.** That is a trade, not a mistake.

---

*Next: Friday — Lab 0, the conversion bench*
