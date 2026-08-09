# ECE 110 · Digital Logic
## Problem Set 4 — Solutions
### INSTRUCTOR / TA COPY — not for distribution

---

**Total: 100 points.** All minimal forms verified with `sympy`; prime implicants found by exhaustive cube merging.

---

## Part A (5 pts each)

**A1 (5).** Gray-code order guarantees that **physically adjacent cells differ in exactly one variable**, so a pair of adjacent 1s always cancels that variable: $AB\overline C+ABC = AB$. **Ordinary binary order breaks this** — $01\to10$ changes both bits.

**A2 (5).** The standard template. *(Marks are for correct minterm numbering, especially rows `11` then `10`.)*

**A3 (5).** $m_0$ is adjacent to $\boxed{m_1,\ m_2,\ m_4,\ m_8}$.

**The two non-obvious ones are $m_2$ and $m_8$**, reached by wrapping off the left edge and the top edge respectively. **The map is a torus** — left joins right, top joins bottom.

*Marking: 2 for the list, **3 for explaining both wraps.***

**A4 (5).** Rectangular; size a power of two; may wrap; may overlap. **Also: maximal groups first, every 1 covered, no 0 covered.**

**A group of 6 is illegal** because 6 is not a power of two — a group of $2^k$ cells eliminates $k$ variables precisely because the differing variables cancel in pairs, and **6 cells cannot be expressed as a single product term.**

---

## Part B (6 pts each)

| | minimal SOP | literals |
|---|---|---:|
| **B1** $\sum m(0,1,2,5,6,7)$ | $AC+B\overline C+\overline A\,\overline B$ | **6** |
| **B2** $\sum m(0,2,5,7,8,10,13,15)$ | $BD+\overline B\,\overline D$ | **4** |
| **B3** $\sum m(0,2,8,10)$ | $\overline B\,\overline D$ | **2** |
| **B4** $\sum m(0,1,4,5,8,9,12,13)$ | $\overline C$ | **1** |
| **B5** $\sum m(0,1,2,3,4,5,10,11,14,15)$ | $AC+\overline A\,\overline B+\overline A\,\overline C$ | **6** |

*(All verified.)*

**B2 — what is notable:** the answer is $\overline{B\oplus D}$. **$F$ does not depend on $A$ or $C$ at all** — both drop out. Visible on the map as a checkerboard in $B,D$ repeated identically across every $A,C$ block.

**B3** requires **both edge wraps simultaneously** — the four corners. This is the most-missed problem on the set.

**B4** is a single group of **eight** (the whole $C=0$ half). Two groups of four is correct and not minimal.

**B5 POS:** $(C+\overline A)(A+\overline B+\overline C)$ — **5 literals, cheaper than the SOP's 6.** *(Verified.)*

*Marking: 4 answer, 2 map. **B5 needs both forms and a verdict.***

---

## Part C (5 pts each)

$$F = \sum m(0,1,2,5,6,7,8,9,10,14)$$

**C1 (5).** Six prime implicants:

$$\overline B\,\overline C,\quad \overline B\,\overline D,\quad C\overline D,\quad \overline ABC,\quad \overline ABD,\quad \overline A\,\overline CD$$

**C2 (5).**

| essential | sole cover of |
|---|---|
| $\overline B\,\overline C$ | $m_0$ *(also $m_9$)* |
| $C\overline D$ | $m_{14}$ |

**C3 (5).** Essentials cover $m_0,m_1,m_2,m_6,m_8,m_9,m_{10},m_{14}$. **Remaining: $m_5$ and $m_7$**, both covered by $\overline ABD$.

**C4 (5).**

$$\boxed{F = \overline B\,\overline C + C\overline D + \overline ABD} \qquad \textbf{7 literals}$$

**C5 (5).** Unused primes: $\overline B\,\overline D$, $\overline ABC$, $\overline A\,\overline CD$.

**Being prime means the group cannot be *enlarged*. It does not mean the group is *needed*.** Once the essentials are taken, what remains is a **covering problem** — choose the fewest implicants that cover the leftovers — and these three lose that competition because $\overline ABD$ covers both remaining minterms by itself.

*Marking: 2 list, **3 for the covering-problem explanation.** "They were not essential" earns 1 — that restates the question.*

---

## Part D (5 pts each)

**D1 (5).** $\sum m(1,3,7,11,15)+\sum d(0,2,5)$:

$$\text{SOP} = CD+\overline A\,\overline B \ \ (\mathbf{4}) \qquad \text{POS} = D(C+\overline A) \ \ (\mathbf{3})$$

$$\textbf{POS wins.}$$ *(Verified.)*

**D2 (5).**

| | expression | literals |
|---|---|---:|
| using don't-cares | $A+BC+BD$ | **5** |
| treating them as 0 | $\overline ABC+\overline ABD+A\overline B\,\overline C$ | 9 |

*(Verified.)*

**D3 (5).** **Not a bug.**

$1111$ is not a valid BCD digit, so **the specification does not define an output there.** Any circuit is correct on inputs the specification does not constrain, and the don't-care version is correct on **every input that can actually occur** — verified on all ten valid codes.

> **But it is only correct if the assumption holds.** If $1111$ can reach this circuit — a fault, an
> uninitialised register, a mis-decoded bus — **the output is now 1 where the designer never
> intended anything.** The map will never reveal that.

*Marking: 2 for "not a bug", **3 for the conditional.** An unqualified "not a bug" earns 2.*

**D4 (5).** **Write down why each don't-care combination cannot occur.**

**Because a don't-care is a claim about the world, not about the algebra.** It is the one input to minimisation that cannot be checked from the truth table, and if the claim is wrong the circuit is wrong in a way no verification against the map will catch.

**D5 (5).** **Quine–McCluskey.**

1. **Merge terms differing in one bit, repeatedly; what never merges is the set of prime implicants.**
2. **Solve the covering problem** — choose the fewest primes covering every minterm.

**Real tools do not always return a true minimum because step 2 is NP-hard**, so past a certain size they use heuristics. **A four-variable K-map, done properly, does guarantee minimality.**

---

## Marking Summary

| Part | Points |
|---|---|
| A | 20 |
| B | 30 |
| C | 25 |
| D | 25 |
| **Total** | **100** |

---

## The Five Errors To Expect

1. **B3:** missing the four-corner group — by far the most common.
2. **B4:** two groups of four instead of one of eight; correct, not minimal.
3. **B2:** not noticing that $A$ and $C$ drop out entirely.
4. **C5:** answering "they were not essential" instead of naming the covering problem.
5. **D3:** an unqualified "not a bug", with no statement of what the answer depends on.

---

*ECE 110 · Week 4 · PS 4 Solutions · Instructor Only*
