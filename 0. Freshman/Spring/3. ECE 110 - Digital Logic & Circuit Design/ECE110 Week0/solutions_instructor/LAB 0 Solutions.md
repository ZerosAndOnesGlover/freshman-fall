# ECE 110 · Digital Logic
## Lab 0 — Solutions and Checkoff Notes
### INSTRUCTOR / TA COPY — not for distribution

---

**Total: 100 points.** Every figure below was produced by running the lab.

---

## Part A — The Conversion Bench (25 pts)

### A1 (10)

Standard repeated-division and repeated-multiplication implementations. **`to_base` must handle $n=0$** — returning the empty string is the most common defect and the round-trip test in A2 catches it immediately.

*Marking: 6 for three working functions, 4 for `frac_to_binary` returning a termination flag rather than just digits.*

### A2 (8)

$$\textbf{16\,384 cases tested, 0 failures.}$$

*(4096 values × 4 bases.)*

*Marking: 4 implementation, **4 for reporting the case count.** "It works" without the number earns 0 of the 4.*

### A3 (7)

| fraction | terminates? |
|---|---|
| $\tfrac12$ | ✓ |
| $\tfrac14$ | ✓ |
| $\tfrac15$ | ✗ |
| $\tfrac58$ | ✓ |
| $\tfrac1{10}$ | ✗ |
| $\tfrac3{16}$ | ✓ |
| $\tfrac13$ | ✗ |

*(Verified.)*

**The rule:** a fraction in lowest terms terminates in base $b$ **iff every prime factor of its denominator divides $b$.** In binary that means **the denominator is a power of two**, and the four that terminate are exactly $2, 4, 8, 16$.

*Marking: 3 table, 4 rule. **The rule must be stated in terms of the denominator's prime factors**, not "denominators that are even" — $\tfrac1{10}$ is even and fails.*

---

## Part B — Two's Complement (30 pts)

### B1 (8)

$$\textbf{256 cases tested, 0 failures.}$$

### B2 (7)

| $n$ | values where negation fails |
|---:|---|
| 4 | $\{-8\}$ |
| 8 | $\{-128\}$ |
| 16 | $\{-32768\}$ |

*(Found by search, verified.)*

**The rule:** it fails at $x = -2^{\,n-1}$ **and nowhere else** — the one value whose negation is not representable.

*Marking: 4 for the three searches, 3 for the general rule. **A student who asserts $-2^{n-1}$ without searching earns 3 of 7** — the exercise is the search.*

### B3 (8)

Overflow **must** be computed as $C_{\text{in,MSB}} \oplus C_{\text{out,MSB}}$. **A submission that computes it by comparing against Python's `+` has not done the exercise** and cannot earn B4's marks either, since B4 would then be circular.

### B4 (7)

$$\textbf{65\,536 pairs tested, 0 mismatches.}$$

*(Verified.)*

*Marking: 3 for running it, **4 for the mismatch count being reported and being zero.** If a student reports a non-zero count and then explains what they fixed, award full marks — that is the correct behaviour.*

---

## Part C — Where Carry and Overflow Disagree (20 pts)

### C1 (8)

| | $V=0$ | $V=1$ |
|---|---:|---:|
| **$C=0$** | 24 768 | 8 128 |
| **$C=1$** | 24 384 | 8 256 |

**Total 65 536.** *(Measured.)*

*Marking: 8 for the correct four counts summing to 65 536.*

### C2 (6)

| $C$ | $V$ | example | signed result | unsigned result |
|---|---|---|---|---|
| 0 | 0 | $30+40$ | $70$ ✓ | $70$ ✓ |
| 0 | 1 | $70+80$ | $-106$ ✗ | $150$ ✓ |
| 1 | 0 | $-30+(-40)$ | $-70$ ✓ | $186$ ✗ |
| 1 | 1 | $-70+(-80)$ | $106$ ✗ | $106$ ✗ |

*(All verified.)*

*Marking: 1.5 per cell. **Accept any correct example**; there are tens of thousands of each.*

### C3 (6)

**The flags are independent**, and C1 is the evidence: **all four cells are non-empty**, so knowing one flag tells you nothing certain about the other.

**What "independent" has to mean for the answer to be meaningful:** that no value of $C$ forces a value of $V$, i.e. all four combinations are reachable. **This is a statement about reachability, not about the counts being equal** — they are not equal (roughly 75% of pairs have $V=0$), and a student who argues from the counts being unequal that the flags are *dependent* has confused reachability with statistical independence.

*Marking: 3 for the verdict from the table, **3 for defining the sense of "independent".** This distinction is the point of the part.*

---

## Part D — BCD (25 pts)

### D1 (10)

$$\textbf{1\,000\,000 cases tested, 0 failures.}$$

*(All pairs $0 \le a,b \le 999$.)*

**The correction must be applied per digit, with the carry propagating.** A submission that converts to `int`, adds, and converts back will pass the test and earns **4 of 10** — it has tested Python's addition, not BCD's.

### D2 (8)

| digits | BCD bits | binary bits | overhead |
|---:|---:|---:|---:|
| 1 | 4 | 4 | **0.0%** |
| 2 | 8 | 7 | 14.3% |
| 3 | 12 | 10 | 20.0% |
| 4 | 16 | 14 | 14.3% |
| 5 | 20 | 17 | 17.6% |
| 6 | 24 | 20 | 20.0% |
| 7 | 28 | 24 | 16.7% |
| 8 | 32 | 27 | 18.5% |
| 9 | 36 | 30 | 20.0% |
| 10 | 40 | 34 | 17.6% |

*(Measured.)*

**The answer is "oscillates".** It does not converge and it does not grow.

> **Why:** binary needs $\lceil d\log_2 10\rceil$ bits, and the ceiling is a step function, so the
> overhead saws up and down against the smooth $4d$. **It is bounded above by**
> $$\frac{4}{\log_2 10}-1 = 20.41\%$$
> *(verified: the maximum over $d \le 40$ is 20.39%)*, **and it is 0% only at $d=1$**, where four bits
> is the honest requirement either way.

*Marking: 5 table, **3 for "oscillates" with the step-function reason.** "Converges to about 20%" earns 1 — the values visibly go down as well as up, and a student who reports convergence has not read their own table.*

### D3 (7)

| method | result |
|---|---|
| Python floats | $0.30000000000000004$ |
| BCD on cent values | $30$ *(cents)* |
| `Fraction(1,10)+Fraction(2,10)` | $3/10$ |

*(All measured.)*

**What BCD is actually exact about:** **decimal fractions with a fixed, finite number of decimal places** — because each decimal digit is stored as itself, so no base conversion happens and nothing is rounded.

**What it is *not*:** more accurate in general. **BCD is no better than binary at $\tfrac13$**, which is inexact in both. It is not more precise, it does not have more bits of significand, and it is slower and larger. **Its only guarantee is that a value you can write down in decimal is stored as that value.**

*Marking: 3 for the three results, **4 for the precise statement.** "BCD is more accurate" is marked wrong even when accompanied by correct numbers — the whole part exists to kill that sentence.*

---

## Marking Summary

| Part | Points |
|---|---|
| A | 25 |
| B | 30 |
| C | 20 |
| D | 25 |
| **Total** | **100** |

---

## Checkoff Checklist

1. A2 reports **16 384 cases, 0 failures**
2. A3's rule is about the denominator's **prime factors**
3. **B2 found $-2^{n-1}$ by search**, at all three widths
4. **B3 computes $V$ from the MSB carries**, not from Python's arithmetic
5. B4 reports **65 536 pairs, 0 mismatches**
6. **C1's four cells are all non-empty** and sum to 65 536
7. C3 defines the sense of "independent" it is using
8. D1's `bcd_add` works **digit by digit**
9. **D2 says "oscillates"**, with the ceiling-function reason
10. **D3 does not claim BCD is generally more accurate**

---

## Note for the Debrief

**Open the course's two habits here, because this lab is where both are cheapest to demonstrate.**

> **Nobody in this room checked 65 536 cases by hand, and nobody had to.** You wrote the rule
> $V = C_{in}\oplus C_{out}$ from the lecture, and then you found out whether it was true. **It was —
> zero mismatches.** Next week you will write a Boolean identity and find out the same way.

Then the second habit:

> **Part D asked you to test a sentence you have heard before: "BCD is exact for money, binary is
> not."** Half of it is true and the half that is false is the interesting half. **BCD is not more
> accurate. It is exact about one specific thing**, and it pays 20% in bits for that.
>
> **Every week of this course has a trade like that in it**, and the trade is always measurable.

Then close:

> Next week the numbers stop being the subject and the *algebra* starts. **Everything you build for
> the rest of the term is made of AND, OR and NOT** — and the surprise is how little that costs you.

---

*ECE 110 · Week 0 · Lab 0 Solutions · Instructor Only*
