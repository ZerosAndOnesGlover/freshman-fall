# ECE 110 · Digital Logic
## Problem Set 1 — Solutions
### INSTRUCTOR / TA COPY — not for distribution

---

**Total: 100 points.** All simplifications verified against truth tables.

---

## Part A — Axioms and Proofs (5 pts each)

### A1 (5)

$$A + AB = A\cdot1 + AB = A(1+B) = A\cdot1 = A$$

*Identity → distributive → null → identity.*

*Marking: 2 answer, **3 for naming all four laws.** An unnamed chain earns 2.*

### A2 (5)

| $A$ | $B$ | $C$ | $BC$ | $A+BC$ | $A{+}B$ | $A{+}C$ | $(A{+}B)(A{+}C)$ |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| 0|0|0|0|**0**|0|0|**0**|
| 0|0|1|0|**0**|0|1|**0**|
| 0|1|0|0|**0**|1|0|**0**|
| 0|1|1|1|**1**|1|1|**1**|
| 1|0|0|0|**1**|1|1|**1**|
| 1|0|1|0|**1**|1|1|**1**|
| 1|1|0|0|**1**|1|1|**1**|
| 1|1|1|1|**1**|1|1|**1**|

**Columns 5 and 8 match on all eight rows.** *(Verified.)*

**Arithmetic counterexample:** $a=1,b=1,c=0$ gives $a+bc = 1$ but $(a+b)(a+c) = 2\cdot1 = 2$.

*Marking: 3 table, 2 counterexample.*

### A3 (5)

**Duality principle:** *the dual of a valid Boolean identity is valid*; form it by swapping $+\leftrightarrow\cdot$ and $0\leftrightarrow1$, leaving variables and complements unchanged.

| identity | dual |
|---|---|
| $A+\overline A = 1$ | $A\overline A = 0$ |
| $A(A+B) = A$ | $A + AB = A$ |
| $A+BC = (A+B)(A+C)$ | $A(B+C) = AB+AC$ |

*Marking: 2 statement, 1 each. **Deduct if a student complements the variables** — that is complementation, not duality, and is the standard confusion.*

### A4 (5)

$$AB+\overline AC+BC = AB+\overline AC+BC(A+\overline A) = AB+\overline AC+ABC+\overline ABC$$
$$= AB(1+C)+\overline AC(1+B) = AB+\overline AC$$

*(Verified: both sides give `[0,1,0,1,0,0,1,1]`.)*

*Marking: 5. **The multiplication by $(A+\overline A)$ is the whole trick**; award 2 for reaching it even if the rest goes wrong.*

---

## Part B — Simplification (6 pts each)

| | expression | minimal SOP | literals |
|---|---|---|---|
| **B1** | $AB+A\overline B$ | $\boxed{A}$ | $4\to1$ |
| **B2** | $A+\overline AB$ | $\boxed{A+B}$ | $3\to2$ |
| **B3** | $ABC+AB\overline C+A\overline BC$ | $\boxed{A(B+C)}$ | $9\to3$ |
| **B4** | $(A+B)(A+\overline B)(\overline A+C)$ | $\boxed{AC}$ | $6\to2$ |
| **B5** | $A\overline B+B\overline C+\overline AC+A\overline BC$ | $\boxed{A\overline B+B\overline C+\overline AC}$ | $9\to6$ |

*(All verified.)*

**B1:** $A(B+\overline B) = A$.
**B2:** absorption's cousin — $A+\overline AB = (A+\overline A)(A+B) = A+B$ by the second distributive law.
**B3:** $AB(C+\overline C)+A\overline BC = AB+A\overline BC = A(B+\overline BC) = A(B+C)$.
**B4:** $(A+B)(A+\overline B) = A+B\overline B = A$, then $A(\overline A+C) = AC$.
**B5:** $A\overline BC$ is **absorbed** by $A\overline B$ — $A\overline B + A\overline BC = A\overline B(1+C) = A\overline B$.

*Marking: 4 answer, 2 working. **For B5 the named theorem (absorption) is required for the last 2**; a student who says "consensus" has the wrong theorem and earns 4.*

> **B5 is deliberately a near-miss for consensus.** The remaining three terms
> $A\overline B + B\overline C + \overline AC$ are the cyclic form that a Karnaugh map in Week 4 will
> show has **no** redundant term, unlike $AB+\overline AC+BC$. Students who "apply consensus" and
> delete one of the three get a wrong answer — worth flagging in the debrief.

---

## Part C — De Morgan and Complementation (5 pts each)

### C1 (5)

$$\overline{AB+\overline C} = \overline{AB}\cdot C = (\overline A+\overline B)C \;=\; \boxed{C(\overline A+\overline B)}$$

*(Verified.)*

### C2 (5)

$$\overline{(A+\overline B)(\overline A+C)} = \overline{A+\overline B} + \overline{\overline A+C} = \overline AB + A\overline C \;=\; \boxed{A\overline C+\overline AB}$$

*(Verified.)*

### C3 (5)

$$\overline{A+B\overline C+\overline BD} = \overline A\cdot\overline{B\overline C}\cdot\overline{\overline BD} = \boxed{\overline A(\overline B+C)(B+\overline D)}$$

*(Verified.)*

### C4 (5)

**Counterexample $(A,B)=(1,0)$:** $\overline{AB} = \overline0 = 1$, while $\overline A\,\overline B = 0\cdot1 = 0$.

**Correct law:** $\overline{AB} = \overline A + \overline B$.

*(Also acceptable: $(0,1)$.)*

*Marking: 3 counterexample, 2 law. **The counterexample must be checked, not just named.***

### C5 (5)

| $A$ | $B$ | $A\oplus B$ | $\overline{A\oplus B}$ | $\overline B$ | $A\oplus\overline B$ |
|:-:|:-:|:-:|:-:|:-:|:-:|
| 0|0|0|**1**|1|**1**|
| 0|1|1|**0**|0|**0**|
| 1|0|1|**0**|1|**0**|
| 1|1|0|**1**|0|**1**|

*(Verified.)*

> **Complementing one input inverts XOR; complementing both leaves it unchanged**
> ($\overline A\oplus\overline B = A\oplus B$). **This is the controlled-inverter idea behind Week 6's
> ALU** — one XOR input is the subtract control.

---

## Part D — Canonical Forms (5 pts each)

$$F(A,B,C) = \sum m(0,2,5,7)$$

### D1 (5)

| | $A$ | $B$ | $C$ | $F$ |
|---|:-:|:-:|:-:|:-:|
| $m_0$|0|0|0|**1**|
| $m_1$|0|0|1|0|
| $m_2$|0|1|0|**1**|
| $m_3$|0|1|1|0|
| $m_4$|1|0|0|0|
| $m_5$|1|0|1|**1**|
| $m_6$|1|1|0|0|
| $m_7$|1|1|1|**1**|

$$F = \overline A\,\overline B\,\overline C + \overline AB\overline C + A\overline BC + ABC$$

### D2 (5)

**Maxterms are the zeros: $M_1, M_3, M_4, M_6$.**

$$F = \prod M(1,3,4,6) = (A+B+\overline C)(A+\overline B+\overline C)(\overline A+B+C)(\overline A+\overline B+C)$$

*(Verified.)*

*Marking: 2 maxterm list, 3 the product. **Complementing on 0 instead of 1 is the standard error** and costs the 3.*

### D3 (5)

$$\boxed{F = AC + \overline A\,\overline C} \qquad \textbf{4 literals}$$

*(Verified.)* From $12$ literals canonical to $4$.

### D4 (5)

$$F = (A+\overline C)(\overline A+C) \qquad \textbf{4 literals}$$

*(Verified.)*

**Neither is cheaper — both are 2 terms and 4 literals.** *(Contrast the Week 1 lecture example $\sum m(1,3,5,6,7)$, where SOP won 3 literals to 4. **The point is that you cannot know without computing both.**)*

### D5 (5)

$$F = 1 \iff A = C$$

**$F$ is $\overline{A\oplus C}$ — the XNOR of $A$ and $C$. It does not depend on $B$ at all.**

**How to see it from the table alone:** pair the rows that differ only in $B$ — $(m_0,m_2)$, $(m_1,m_3)$, $(m_4,m_6)$, $(m_5,m_7)$. **Each pair has the same output**, so changing $B$ never changes $F$, so $B$ is not an input of the function in any meaningful sense.

*Marking: 2 for "F is 1 iff A=C" or naming XNOR, **3 for the row-pairing argument.** Simply observing that $B$ vanished from the minimal form earns 2 of the 3 — the question asks how to see it *from the truth table*, which is the skill Week 4's map formalises.*

---

## Marking Summary

| Part | Points |
|---|---|
| A — Axioms and proofs | 20 |
| B — Simplification | 30 |
| C — De Morgan | 25 |
| D — Canonical forms | 25 |
| **Total** | **100** |

---

## The Five Errors To Expect

1. **A3:** complementing variables when forming a dual.
2. **B5:** applying consensus where absorption is what applies.
3. **C1–C3:** breaking the bar without changing the operator.
4. **D2:** complementing maxterm variables on 0 instead of 1.
5. **D5:** noticing $B$ disappeared, but not being able to see it in the table.

---

*ECE 110 · Week 1 · PS 1 Solutions · Instructor Only*
