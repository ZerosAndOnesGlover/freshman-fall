# ECE 110 · Digital Logic
## Week 4 · Reference Sheet
### Karnaugh Maps and Minimization

---

## Gray Code Order

$$00,\ 01,\ 11,\ 10 \qquad\text{not}\qquad 00,\ 01,\ 10,\ 11$$

**Adjacent codes differ in exactly one bit — including the wrap from last to first.** *(verified)*

$$\text{gray}(0..7) = 000,\ 001,\ 011,\ 010,\ 110,\ 111,\ 101,\ 100$$

> **The map is a torus.** Left edge joins right, top joins bottom, and **the four corners are
> mutually adjacent.**

---

## The 4-Variable Map

| $AB\backslash CD$ | 00 | 01 | 11 | 10 |
|:-:|:-:|:-:|:-:|:-:|
| **00** | $m_0$ | $m_1$ | $m_3$ | $m_2$ |
| **01** | $m_4$ | $m_5$ | $m_7$ | $m_6$ |
| **11** | $m_{12}$ | $m_{13}$ | $m_{15}$ | $m_{14}$ |
| **10** | $m_8$ | $m_9$ | $m_{11}$ | $m_{10}$ |

**$m_0$ is adjacent to $m_1, m_2, m_4, m_8$** — the last two by wrapping.

---

## Grouping Rules

1. **Rectangular**, size $1,2,4,8,16$ — **never 3, 6, 12.**
2. **May wrap** edges and corners.
3. **May overlap** — $X+X=X$, so it is free.
4. **Largest groups first**, then fewest groups.
5. **Every 1 covered; no 0 covered.**

$$\text{a group of } 2^k \text{ cells eliminates } k \text{ variables}$$

**Because the differing variables cancel:** $AB\overline C+ABC = AB(\overline C+C)=AB$.

> ⚠ **A correct cover need not be minimal, and nothing in the answer tells you.**
> **After covering every 1, go back and ask whether any group could have been larger.**
> *(Example: $\sum m(0,1,2,3,4,5,10,11,14,15)$ — a pairs-only cover is 6 terms / 20 literals and
> completely correct; the minimum is 3 terms / 6 literals.)*

---

## Implicants

| term | meaning |
|---|---|
| **implicant** | any legal group |
| **prime implicant** | a group that **cannot be enlarged** |
| **essential prime implicant** | the **only** implicant covering some minterm |

**Procedure:** all primes → take every essential → cover the rest with as few primes as possible.

**Being prime is necessary, not sufficient.** Step 4 is a genuine covering problem.

### Worked: $F=\sum m(0,1,2,5,6,7,8,9,10,14)$

**Primes:** $\overline B\,\overline C,\ \overline B\,\overline D,\ C\overline D,\ \overline ABC,\ \overline ABD,\ \overline A\,\overline CD$
**Essential:** $\overline B\,\overline C$ *(forced by $m_0$)*, $C\overline D$ *(forced by $m_{14}$)*
**Remaining $m_5,m_7$** → add $\overline ABD$

$$F = \overline B\,\overline C + C\overline D + \overline ABD \qquad \textbf{7 literals}$$

*(verified)*

---

## POS From The Zeros

**Group the 0s to get $\overline F$, then De Morgan.** **Always do both maps** — neither form always wins:

| function | SOP | POS |
|---|---:|---:|
| $\sum m(0,1,2,3,4,5,10,11,14,15)$ | 6 | **5** |
| $\sum m(1,3,7,11,15)+\sum d(0,2,5)$ | 4 | **3** |
| $\sum m(0,2,5,7,8,10,13,15)$ | 4 | 4 |
| $\sum m(0,2,8,10)$ | 2 | 2 |

*(all verified)*

---

## Don't-Cares

**Impossible inputs are marked $\times$ and may be read as 1 or 0 — whichever enlarges the groups.**

**"Is this BCD digit $\ge5$?"**

| | expression | literals |
|---|---|---:|
| using don't-cares | $A+BC+BD$ | **5** |
| treating them as 0 | $\overline ABC+\overline ABD+A\overline B\,\overline C$ | 9 |

*(verified)*

> **A don't-care is a claim about the world, not about the algebra.** It is the one input to
> minimisation that cannot be checked against the truth table. **Write down why each combination
> cannot occur** — if the claim is wrong, the circuit is wrong in a way the map will never show.

---

## Beyond Four Variables

**Maps: fine to 4, awkward at 5–6, unusable beyond.**

**Quine–McCluskey** — same two steps as a table:
1. merge cubes differing in one bit until nothing merges → **prime implicants**
2. **solve the covering problem**

**Mechanical, hence automatable** — it is what synthesis tools run *(Week 12)*. **But step 2 is NP-hard, so real tools use heuristics and do not guarantee a true minimum.** A correctly done 4-variable map does.

---

## What Minimisation Buys

$$\sum m(0,1,2,3,4,5,10,11,14,15): \quad \textbf{43 gates} \to \textbf{7 gates} \ (6.1\times)$$

$$\sum m(0,2,8,10): \quad \textbf{19 gates} \to \textbf{3 gates}$$

*(measured, 2-input gates, shared inverters)*

> **Minimisation buys AREA. It buys almost no SPEED** — both forms are two levels deep.
> **Week 3's ripple-carry adder was a delay problem and no minimisation would have touched it.**
> Different problem, different tool — **Week 6.**

---

## Common Errors

1. **Missing the four-corner group.** *(Most common by far.)*
2. **Two groups of four where one of eight exists.**
3. **Avoiding overlap**, which is free.
4. **Grouping in ordinary binary order** instead of Gray.
5. **Treating a don't-care as 0** and losing half the saving.
6. **Stopping at a correct cover** without checking every group is maximal.
7. **Expecting minimisation to fix a delay problem.**

---

*ECE 110 · Week 4 · Reference Sheet*
