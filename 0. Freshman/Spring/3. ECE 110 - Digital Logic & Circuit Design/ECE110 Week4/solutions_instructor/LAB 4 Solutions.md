# ECE 110 · Digital Logic
## Lab 4 — Solutions and Checkoff Notes
### INSTRUCTOR / TA COPY — not for distribution

---

**Total: 100 points.** All minimal forms verified with `sympy`; all gate counts under the stated convention.

---

## Parts A & B — Hand Minimisation vs the Machine (55 pts)

| | function | minimal SOP | lits | canonical lits |
|---|---|---|---:|---:|
| **A1** | $\sum m(0,1,2,5,6,7)$ | $AC + B\overline C + \overline A\,\overline B$ | **6** | 18 |
| **A2** | $\sum m(0,2,5,7,8,10,13,15)$ | $BD + \overline B\,\overline D$ | **4** | 32 |
| **A3** | $\sum m(0,2,8,10)$ | $\overline B\,\overline D$ | **2** | 16 |
| **A4** | $\sum m(0,1,4,5,8,9,12,13)$ | $\overline C$ | **1** | 32 |
| **A5** | $\sum m(0,1,2,3,4,5,10,11,14,15)$ | $AC + \overline A\,\overline B + \overline A\,\overline C$ | **6** | 40 |
| **A6** | $\sum m(1,3,7,11,15) + \sum d(0,2,5)$ | $CD + \overline A\,\overline B$ | **4** | 20 |

*(All verified.)*

### What each one is testing

- **A2** is $\overline{B\oplus D}$ — **$A$ and $C$ are irrelevant.** Students who produce a 4-term answer have not spotted that half the variables drop out.
- **A3** is the **four corners**. It needs both edge wraps at once and is the single most-failed item.
- **A4** is one group of **eight** — the entire $C=0$ half. Students who circle two groups of four get a correct 2-term answer and lose the point.
- **A5** is the lecture's example; **the pairs-only cover is 20 literals** and correct.
- **A6** rewards using the don't-cares.

### B3 — where POS wins

$$\textbf{A5: } (C+\overline A)(A+\overline B+\overline C) = \mathbf{5} \text{ literals against SOP's } 6$$
$$\textbf{A6: } D(C+\overline A) = \mathbf{3} \text{ literals against SOP's } 4$$

*(Both verified.)* **A1, A2, A3, A4 tie.**

*Marking A (30): 5 each, **awarded for a drawn map and a sealed answer, not for being minimal.***
*Marking B1 (10): the comparison table. **B2 (8): the diagnosis** — this is where the marks are. **B3 (7): must find both A5 and A6.***

> **The expected distribution is 2–4 losses out of 6.** A student reporting zero losses either did
> Part B first or is not counting literals; check their A3 and A4 specifically.

---

## Part C — Prime Implicants By Program (20 pts)

$$F = \sum m(0,1,2,5,6,7,8,9,10,14)$$

### C1 (8) — six prime implicants

$$\overline B\,\overline C,\quad \overline B\,\overline D,\quad C\overline D,\quad \overline ABC,\quad \overline ABD,\quad \overline A\,\overline CD$$

*(Verified by exhaustive cube merging.)*

### C2 (6) — two essential

| essential | forced by |
|---|---|
| $\overline B\,\overline C$ | $m_0$, $m_9$ |
| $C\overline D$ | $m_{14}$ |

*(Verified: each of those minterms is covered by exactly one prime implicant.)*

### C3 (6)

**Essentials cover $m_0,m_1,m_2,m_6,m_8,m_9,m_{10},m_{14}$; $m_5$ and $m_7$ remain.**

**$\overline ABD$ covers both**, so:

$$F = \overline B\,\overline C + C\overline D + \overline ABD \qquad \textbf{7 literals}$$

**Agrees with `SOPform`.** *(Verified.)*

---

## Part D — Does Smaller Actually Work? (25 pts)

### D1 (12)

**Canonical and minimal forms of A5 agree on all 16 inputs: 0 failures.** *(Verified.)*

*A behavioural `assign` for both is acceptable here — the point is equivalence, not structure.*

### D2 (8)

**Convention: 2-input gates; an $n$-literal product needs $n-1$ ANDs; one inverter per distinct complemented variable, shared.**

| form | inverters | ANDs | ORs | **total** |
|---|---:|---:|---:|---:|
| canonical (10 terms × 4 literals) | 4 | 30 | 9 | **43** |
| minimal $AC+\overline A\,\overline B+\overline A\,\overline C$ | 2 | 3 | 2 | **7** |

$$\boxed{43 \to 7 \text{ gates, a } 6.1\times \text{ reduction}}$$

### D3 (5)

$$\sum m(0,2,8,10) = \overline B\,\overline D \quad\Rightarrow\quad \textbf{2 inverters + 1 AND} = \mathbf{3}\text{ gates}$$

**The canonical form would take $4 + 12 + 3 = \mathbf{19}$ gates.** *(Verified.)*

**On the bench: one 74HC04 and one 74HC08, and the four 1-rows verify.**

*Marking: 3 for the build, 2 for both counts.*

---

## Marking Summary

| Part | Points |
|---|---|
| A — hand minimisation | 30 |
| B — machine check | 25 |
| C — prime implicants | 20 |
| D — smaller in hardware | 25 |
| **Total** | **100** |

---

## Checkoff Checklist

1. **Part A answers sealed before Part B was run**
2. B1's table has all three columns
3. **B2 diagnoses each loss against the rule list**
4. **B3 finds POS cheaper on A5 *and* A6**
5. C1 finds **six** prime implicants
6. C2 names the forcing minterm for each essential
7. D2 states its counting convention
8. D3 gives both 3 and 19

---

## Note for the Debrief

**Ask for a show of hands: who lost A3? Most of the room.**

> **A3 is four ones in the corners of the map, and it minimises to two literals.** Almost everyone
> circles two pairs and writes a four-literal answer that is **completely correct**. **Nothing in a
> correct answer tells you it is not minimal** — that is why the machine check exists, and why the
> discipline is to go back and ask whether any group could have been larger.

Then the payoff:

> **A5 went from 43 gates to 7.** Same function, same truth table, **six times less silicon** — and
> the only thing that changed was noticing three groups instead of six.

Then set the boundary, because it matters next week and in Week 6:

> **Minimisation bought you area. It bought you almost no speed** — both forms are two levels deep.
> **Remember Week 3: the ripple-carry adder's problem was delay, and no minimisation would have
> touched it.** Different problem, different tool.

---

*ECE 110 · Week 4 · Lab 4 Solutions · Instructor Only*
