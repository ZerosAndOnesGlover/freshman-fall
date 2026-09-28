# MATH 151 · Week 4
## PS4 Solutions — INSTRUCTOR ONLY

---

> *Revised 2026-09-28: cut from 13 problems (about 30 parts) to 8 problems with 17 parts. New → old: A1 = A1 (a, c, e, g), 12 ·
> A2 = A2 (a, c, d), 12 · B1 = B1 (b, c), 16 · C1 = C1 (c, d), 12 · D1 = D1, 12 · D2 = D2, 12 · E1 = E1, 12 · E2 = E3, 12. D3, D4, E2
> (multiples of 3 or 5 — Lab 4 counts it) and E4 are no longer asked. A1's handout also lost a drafting slip in its set definitions.*


## Part A

### A1. $U=\{1,\ldots,15\}$, $A=\{1,3,5,7,9,11,13,15\}$, $B=\{2,3,5,7,11,13\}$, $C=\{1,2,3,4,5,6,7\}$

**(a)** $A\cap B = \{3,5,7,11,13\}$

**(b)** $B\cup C = \{1,2,3,4,5,6,7,11,13\}$

**(c)** $A-C = \{9,11,13,15\}$

**(d)** $\overline{B} = \{1,4,6,8,9,10,12,14,15\}$

**(e)** $A\oplus C$: $A-C=\{9,11,13,15\}$, $C-A=\{2,4,6\}$. $A\oplus C=\{2,4,6,9,11,13,15\}$

**(f)** $(A\cap B)\cup(B\cap C)$: $A\cap B=\{3,5,7,11,13\}$, $B\cap C=\{2,3,5,7\}$. Union: $\{2,3,5,7,11,13\}$

**(g)** $\overline{A\cup B}$: $A\cup B=\{1,2,3,5,7,9,11,13,15\}$. Complement: $\{4,6,8,10,12,14\}$

**(h)** $\overline{A}\cap\overline{B}$: $\overline{A}=\{2,4,6,8,10,12,14\}$, $\overline{B}=\{1,4,6,8,9,10,12,14,15\}$. Intersection: $\{4,6,8,10,12,14\}$. **Matches (g).** ✓ (De Morgan's Law confirmed)

---

### A2.

**(a)** $A-(B-C)=(A-B)-C$: **FALSE.**
Counterexample: $A=\{1,2,3\}, B=\{2\}, C=\{3\}$.
$B-C=\{2\}$. $A-(B-C)=\{1,3\}$.
$A-B=\{1,3\}$. $(A-B)-C=\{1\}$.
$\{1,3\}\neq\{1\}$.

**(b)** $A\times(B\cup C)=(A\times B)\cup(A\times C)$: **TRUE.**
This is a valid identity (proven via distributivity — see D-series proofs). No counterexample exists.

**(c)** If $A\cup B=A\cup C$, then $B=C$: **FALSE.**
Counterexample: $A=\{1,2\}, B=\{1\}, C=\{2\}$.
$A\cup B=\{1,2\}$, $A\cup C=\{1,2\}$. Equal. But $B=\{1\}\neq\{2\}=C$.

**(d)** If $A\cap B=A\cap C$ AND $A\cup B=A\cup C$, then $B=C$: **TRUE.**

*Proof sketch:* Let $x\in B$. If $x\in A$: then $x\in A\cap B=A\cap C$, so $x\in C$. If $x\notin A$: since $x\in B\subseteq A\cup B=A\cup C$ and $x\notin A$, we must have $x\in C$. Either way $x\in C$. So $B\subseteq C$. By symmetry, $C\subseteq B$. Hence $B=C$.

*(Grading: full credit for correct TRUE/FALSE plus valid justification; for (d) full proof credit requires the symmetric argument.)*

---

## Part B — Set Identity Proofs

### B1(a): $A\cup(A\cap B)=A$ (Absorption)

**[Algebraic proof]**
$$A\cup(A\cap B) = (A\cap U)\cup(A\cap B) \quad[\text{Identity}]$$
$$= A\cap(U\cup B) \quad[\text{Distributivity}]$$
$$= A\cap U \quad[\text{Domination: }U\cup B=U]$$
$$= A \quad[\text{Identity}]$$ ∎

---

### B1(b): $(A\cup B)-C=(A-C)\cup(B-C)$

**[Element-chasing proof]**
$$x\in(A\cup B)-C \iff x\in(A\cup B)\land x\notin C$$
$$\iff (x\in A\lor x\in B)\land x\notin C$$
$$\iff (x\in A\land x\notin C)\lor(x\in B\land x\notin C) \quad[\text{Distributivity of }\land\text{ over }\lor]$$
$$\iff x\in(A-C)\lor x\in(B-C)$$
$$\iff x\in(A-C)\cup(B-C)$$

Since $x$ arbitrary, the sets are equal. ∎

---

### B1(c): $A\cap(B\oplus C)=(A\cap B)\oplus(A\cap C)$

**[Element-chasing proof]**

Recall $x\in B\oplus C \iff$ exactly one of $x\in B, x\in C$ holds $\iff (x\in B\land x\notin C)\lor(x\notin B\land x\in C)$.

$$x\in A\cap(B\oplus C) \iff x\in A \land [(x\in B\land x\notin C)\lor(x\notin B\land x\in C)]$$
$$\iff (x\in A\land x\in B\land x\notin C)\lor(x\in A\land x\notin B\land x\in C) \quad[\text{distribute }x\in A]$$

Now consider $(A\cap B)\oplus(A\cap C)$:
$$x\in(A\cap B)\oplus(A\cap C) \iff [x\in(A\cap B)\land x\notin(A\cap C)]\lor[x\notin(A\cap B)\land x\in(A\cap C)]$$
$$\iff [(x\in A\land x\in B)\land\neg(x\in A\land x\in C)]\lor[\neg(x\in A\land x\in B)\land(x\in A\land x\in C)]$$

First bracket: $(x\in A\land x\in B)\land(x\notin A\lor x\notin C)$
$= (x\in A\land x\in B\land x\notin A)\lor(x\in A\land x\in B\land x\notin C)$
$= F \lor (x\in A\land x\in B\land x\notin C)$ [since $x\in A\land x\notin A$ is always false]
$= x\in A\land x\in B\land x\notin C$

By symmetric reasoning, second bracket $= x\in A\land x\notin B\land x\in C$.

So $x\in(A\cap B)\oplus(A\cap C) \iff (x\in A\land x\in B\land x\notin C)\lor(x\in A\land x\notin B\land x\in C)$

This matches exactly the expression derived for $x\in A\cap(B\oplus C)$ above. ∎

*(This is a more intricate proof — award partial credit generously for correct case-by-case reasoning even if the write-up differs in structure.)*

---

### B1(d): $\overline{A-B}=\overline{A}\cup B$

**[Algebraic proof]**
$$\overline{A-B} = \overline{A\cap\overline{B}} \quad[\text{Difference Identity}]$$
$$= \overline{A}\cup\overline{\overline{B}} \quad[\text{De Morgan}]$$
$$= \overline{A}\cup B \quad[\text{Double Complement}]$$ ∎

---

## Part C — Subset Proofs

### C1(a): $A\cap B\subseteq A$

**Proof.** Let $x\in A\cap B$ be arbitrary. Then $x\in A\land x\in B$, so in particular $x\in A$. Since $x$ arbitrary, $A\cap B\subseteq A$. ∎

### C1(b): $A\subseteq A\cup B$

**Proof.** Let $x\in A$ be arbitrary. Then $x\in A\lor x\in B$ holds (since $x\in A$), so $x\in A\cup B$. Since $x$ arbitrary, $A\subseteq A\cup B$. ∎

### C1(c): If $A\subseteq B$ and $C\subseteq D$, then $A\cap C\subseteq B\cap D$.

**Proof.** Assume $A\subseteq B$ and $C\subseteq D$. Let $x\in A\cap C$ be arbitrary. Then $x\in A$ and $x\in C$. Since $A\subseteq B$, $x\in B$. Since $C\subseteq D$, $x\in D$. So $x\in B\cap D$. Since $x$ arbitrary, $A\cap C\subseteq B\cap D$. ∎

### C1(d): $A\times B\subseteq(A\cup C)\times(B\cup D)$

**Proof.** Let $(a,b)\in A\times B$ be arbitrary. Then $a\in A$ and $b\in B$. Since $A\subseteq A\cup C$ (Exercise C1(b) applied to $A, C$), $a\in A\cup C$. Similarly, $b\in B\cup D$. So $(a,b)\in(A\cup C)\times(B\cup D)$. Since $(a,b)$ arbitrary, $A\times B\subseteq(A\cup C)\times(B\cup D)$. ∎

---

## Part D — Power Sets and Cartesian Products

### D1. $A=\{a,b,c\}$

**(a)** $\mathcal{P}(A) = \{\emptyset,\{a\},\{b\},\{c\},\{a,b\},\{a,c\},\{b,c\},\{a,b,c\}\}$

**(b)** Elements with exactly 2 elements: $\{a,b\},\{a,c\},\{b,c\}$ — **3 subsets**.

**(c)** $|\mathcal{P}(A)|=8=2^3=2^{|A|}$. ✓

---

### D2. $A\subseteq B \iff \mathcal{P}(A)\subseteq\mathcal{P}(B)$

**Proof.**

$(\rightarrow)$ Assume $A\subseteq B$. Let $S\in\mathcal{P}(A)$ be arbitrary, i.e., $S\subseteq A$. Since $A\subseteq B$ (transitivity of subset), $S\subseteq B$, i.e., $S\in\mathcal{P}(B)$. Since $S$ arbitrary, $\mathcal{P}(A)\subseteq\mathcal{P}(B)$.

$(\leftarrow)$ Assume $\mathcal{P}(A)\subseteq\mathcal{P}(B)$. Since $A\in\mathcal{P}(A)$ (every set is a subset of itself), we have $A\in\mathcal{P}(B)$, meaning $A\subseteq B$. ∎

---

### D3. $A=\{1,2\}$, $B=\{3,4\}$

**(a)** $A\times B=\{(1,3),(1,4),(2,3),(2,4)\}$
$B\times A=\{(3,1),(3,2),(4,1),(4,2)\}$
**Not equal** — no ordered pair is shared (since $A\cap B=\emptyset$, in fact $(A\times B)\cap(B\times A)=\emptyset$ in this case).

**(b)** $(A\times B)\cap(B\times A) = \emptyset$ (as noted; no pair (x,y) can have $x\in A\cap B$ and $y\in A\cap B$ simultaneously satisfying both orderings here since $A\cap B=\emptyset$).

**(c)** $A\times(B\times A)$ consists of pairs $(a,(b,a'))$ where $a\in A$, $(b,a')\in B\times A$ — e.g., $(1,(3,1))$. This has elements that are pairs whose second component is itself a pair.

$(A\times B)\times A$ consists of pairs $((a,b),a')$ — e.g., $((1,3),1)$.

These are **different structures**: $A\times(B\times A)$ has elements of the form $(a,(b,a'))$ (nested pair as second component), while $(A\times B)\times A$ has elements of the form $((a,b),a')$ (nested pair as first component). Though there's a natural bijection between them (both correspond to ordered triples $(a,b,a')$), they are not literally the same set under the standard set-theoretic definition of ordered pairs. This illustrates why Cartesian product is not strictly associative as sets, even though it is "associative up to natural bijection" — a subtlety resolved formally by treating $n$-tuples as a primitive notion (Section 5, Friday's lecture) or via canonical identification.

---

### D4. $\mathcal{P}(A)\cap\mathcal{P}(B)=\mathcal{P}(A\cap B)$

**Proof.** [Element-chasing]

$$S\in\mathcal{P}(A)\cap\mathcal{P}(B) \iff S\in\mathcal{P}(A)\land S\in\mathcal{P}(B)$$
$$\iff S\subseteq A \land S\subseteq B$$
$$\iff \forall x(x\in S\rightarrow x\in A) \land \forall x(x\in S\rightarrow x\in B)$$
$$\iff \forall x[(x\in S\rightarrow x\in A)\land(x\in S\rightarrow x\in B)]$$
$$\iff \forall x[x\in S\rightarrow(x\in A\land x\in B)] \quad[\text{distributing implication over conjunction of consequents}]$$
$$\iff \forall x(x\in S\rightarrow x\in A\cap B)$$
$$\iff S\subseteq A\cap B$$
$$\iff S\in\mathcal{P}(A\cap B)$$

Since $S$ arbitrary, $\mathcal{P}(A)\cap\mathcal{P}(B)=\mathcal{P}(A\cap B)$. ∎

*(Simpler alternative: $S\subseteq A$ and $S\subseteq B$ together mean every element of S is in both A and B, i.e., in $A\cap B$ — and conversely. Accept either level of formality.)*

---

## Part E — Inclusion-Exclusion

### E1. 200 students, 120 French, 100 Spanish, 40 both.

$$|F\cup S| = 120+100-40 = 180$$

Students in neither: $200-180=\mathbf{20}$.

---

### E2. Divisible by 3 or 5, from 1 to 300.

$|A|$ (mult. of 3) $=\lfloor300/3\rfloor=100$
$|B|$ (mult. of 5) $=\lfloor300/5\rfloor=60$
$|A\cap B|$ (mult. of 15) $=\lfloor300/15\rfloor=20$

$$|A\cup B|=100+60-20=\mathbf{140}$$

---

### E3. Divisible by 2, 3, or 5, from 1 to 500.

$|A|$(÷2)$=250$, $|B|$(÷3)$=166$, $|C|$(÷5)$=100$
$|A\cap B|$(÷6)$=83$, $|A\cap C|$(÷10)$=50$, $|B\cap C|$(÷15)$=33$
$|A\cap B\cap C|$(÷30)$=16$

$$|A\cup B\cup C| = 250+166+100-83-50-33+16$$

Grouping the terms: singles $250+166+100 = 516$; pairs $83+50+33 = 166$; so
$516 - 166 + 16 = \mathbf{366}$.

---

### E4. 150 people, three products.

$|A|=80,|B|=70,|C|=60$
$|A\cap B|=30,|A\cap C|=25,|B\cap C|=20$
$|A\cap B\cap C|=10$

First, $|A\cup B\cup C| = 80+70+60-30-25-20+10 = 210-75+10=145$.

To find "exactly one":

Number in exactly two or more $=$ (pairwise sums) accounting properly. Standard technique:

Exactly one $= |A\cup B\cup C| - (\text{at least two})$

Number in **at least two** $= |A\cap B|+|A\cap C|+|B\cap C| - 2|A\cap B\cap C|$
$= 30+25+20-2(10) = 75-20=55$

*(This formula counts each "exactly two" person once and each "exactly three" person... let's verify: standard identity — sum of pairwise intersections counts triple-overlap elements 3 times (once per pair), so subtracting $2\times$ triple gives exactly the count of elements in ≥2 sets, counted once each. This is a standard combinatorial identity.)*

Number in **exactly one** $= |A\cup B\cup C| - (\text{at least two}) = 145 - 55 = \mathbf{90}$

*Alternative direct computation:*
- Exactly A only: $|A|-|A\cap B|-|A\cap C|+|A\cap B\cap C| = 80-30-25+10=35$
- Exactly B only: $70-30-20+10=30$
- Exactly C only: $60-25-20+10=25$
- Sum: $35+30+25=90$ ✓ (Matches.)

**Answer: 90 people use exactly one product.**
