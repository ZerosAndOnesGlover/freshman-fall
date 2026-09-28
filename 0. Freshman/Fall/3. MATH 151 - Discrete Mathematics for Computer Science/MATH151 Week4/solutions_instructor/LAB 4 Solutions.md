# MATH 151 · Week 4
## LAB4 Solutions — INSTRUCTOR ONLY

*(Revised 2026-09-26: lab Exercise 2.2 is old 2.3, lab 2.3 is old 2.5; old 2.2 and 2.4 are no longer asked. Section 3 now uses
lists and membership tests instead of Python sets (CS 101 Week 8). Expected: 3.1 prints no "differs" line for either identity
with the given lists; 3.2 prints 1, 2, 3, 4 — e.g. x = 1 is in A ∪ (B ∩ C) but not in (A ∪ B) ∩ C since 1 ∉ C; 3.3 gives 8 and 32
subsets; 3.4 counts 140 = 100 + 60 − 20, the −|A ∩ B| term removing the 20 multiples of 15.)*

---

## Section 1 Solutions

### Exercise 1.1

**(a)** $A\cap(B\cup C)$ vs $(A\cap B)\cup(A\cap C)$: **Regions MATCH.** (Distributive Law — TRUE identity.)

**(b)** $A-(B\cap C)$ vs $(A-B)\cup(A-C)$: **Regions MATCH.** (This is a valid De Morgan-style identity — proven in Exercise 2.2.)

**(c)** $(A\cup B)\cap C$ vs $A\cup(B\cap C)$: **Regions do NOT match** in general. The left restricts to C after union; the right unions A back in regardless of C. Specifically, the region of A outside of C is in the RHS (via $A\cup\ldots$) but not in the LHS (since LHS requires membership in $C$).

---

### Exercise 1.2 — Venn Diagram Counting

Given: $|U|=100$, $|A|=40$, $|B|=35$, $|C|=30$, $|A\cap B|=15$, $|A\cap C|=10$, $|B\cap C|=8$, $|A\cap B\cap C|=3$.

Working from center outward:

- **All three** ($A\cap B\cap C$): 3
- **A and B only** (not C): $|A\cap B|-|A\cap B\cap C| = 15-3=12$
- **A and C only** (not B): $|A\cap C|-|A\cap B\cap C|=10-3=7$
- **B and C only** (not A): $|B\cap C|-|A\cap B\cap C|=8-3=5$
- **A only:** $|A|-(\text{A∩B only})-(\text{A∩C only})-(\text{all three}) = 40-12-7-3=18$
- **B only:** $35-12-5-3=15$
- **C only:** $30-7-5-3=15$
- **None:** $100 - (18+15+15+12+7+5+3) = 100-75=25$

**Verification:** Sum of all regions: $18+15+15+12+7+5+3+25 = 100$. ✓

**Check total:** $|A\cup B\cup C| = |A|+|B|+|C|-|A\cap B|-|A\cap C|-|B\cap C|+|A\cap B\cap C| = 40+35+30-15-10-8+3=75$. Matches $100-25=75$ (none count). ✓

---

## Section 2 Solutions

### Exercise 2.1: $A\cap(B\cup C)=(A\cap B)\cup(A\cap C)$

**Proof.** [Element-chasing]
$$x\in A\cap(B\cup C) \iff x\in A\land(x\in B\lor x\in C)$$
$$\iff (x\in A\land x\in B)\lor(x\in A\land x\in C) \quad\text{[Distributivity of }\land\text{ over }\lor\text{]}$$
$$\iff x\in(A\cap B)\lor x\in(A\cap C)$$
$$\iff x\in(A\cap B)\cup(A\cap C)$$
Since $x$ arbitrary, the sets are equal. ∎

### Exercise 2.2: $A-(B\cap C)=(A-B)\cup(A-C)$

**Proof.** [Element-chasing]
$$x\in A-(B\cap C) \iff x\in A\land x\notin(B\cap C)$$
$$\iff x\in A\land\neg(x\in B\land x\in C)$$
$$\iff x\in A\land(x\notin B\lor x\notin C) \quad\text{[De Morgan]}$$
$$\iff (x\in A\land x\notin B)\lor(x\in A\land x\notin C) \quad\text{[Distributivity]}$$
$$\iff x\in(A-B)\lor x\in(A-C)$$
$$\iff x\in(A-B)\cup(A-C)$$
Since $x$ arbitrary, the sets are equal. ∎

### Exercise 2.3: Disprove $(A\cup B)\cap C=A\cup(B\cap C)$

**Counterexample:** $A=\{1\}$, $B=\{2\}$, $C=\{1,3\}$.

$A\cup B=\{1,2\}$. $(A\cup B)\cap C=\{1,2\}\cap\{1,3\}=\{1\}$.

$B\cap C=\{2\}\cap\{1,3\}=\emptyset$. $A\cup(B\cap C)=\{1\}\cup\emptyset=\{1\}$.

These happen to **match**, so this choice is *not* a counterexample — a useful reminder that a
single agreeing example proves nothing. The failure is that $A\subseteq C$ here, which makes both
sides collapse to $A$.

**A genuine counterexample:** $A=\{4\}$, $B=\{2\}$, $C=\{1,3\}$ — chosen so that $A\not\subseteq C$.

$A\cup B=\{4,2\}$. $(A\cup B)\cap C=\{2,4\}\cap\{1,3\}=\emptyset$.

$B\cap C=\{2\}\cap\{1,3\}=\emptyset$. $A\cup(B\cap C)=\{4\}\cup\emptyset=\{4\}$.

$\emptyset\neq\{4\}$. ✓ Counterexample confirmed.

**Simpler standard counterexample:** $A=\{1\}, B=\emptyset, C=\{2\}$.

$(A\cup B)\cap C = \{1\}\cap\{2\}=\emptyset$.
$A\cup(B\cap C) = \{1\}\cup\emptyset=\{1\}$.

$\emptyset\neq\{1\}$. ✓ This is cleaner.

*(Grading: accept any valid counterexample where the sets genuinely differ — many students will find different valid examples.)*

### Exercise 2.4: $\overline{A}-\overline{B}=B-A$

**Proof.** [Element-chasing]
$$x\in\overline{A}-\overline{B} \iff x\in\overline{A}\land x\notin\overline{B}$$
$$\iff x\notin A \land x\in B \quad\text{[complement, double negation]}$$
$$\iff x\in B\land x\notin A$$
$$\iff x\in B-A$$
Since $x$ arbitrary, the sets are equal. ∎

### Exercise 2.5: $A\subseteq B\iff A\cup B=B$

**Proof.**

$(\rightarrow)$ Assume $A\subseteq B$. We show $A\cup B=B$.
$\subseteq$: Let $x\in A\cup B$. If $x\in A$, then since $A\subseteq B$, $x\in B$. If $x\in B$, trivially $x\in B$. Either way $x\in B$. So $A\cup B\subseteq B$.
$\supseteq$: $B\subseteq A\cup B$ always (Exercise C1(b) pattern).
Therefore $A\cup B=B$.

$(\leftarrow)$ Assume $A\cup B=B$. Let $x\in A$ be arbitrary. Then $x\in A\cup B$ (trivially). Since $A\cup B=B$, $x\in B$. Since $x$ arbitrary, $A\subseteq B$. ∎

---

## Section 3 — Python Expected Outputs

### Exercise 3.1

All three test cases should show `HOLDS` for the identity $A\cap(B\cup C)=(A\cap B)\cup(A\cap C)$, and similarly for Exercises 2.2 and 2.4's identities when translated to Python.

### Exercise 3.2 — Counterexample search

Expected: the program will quickly find a counterexample (within the universe {1,...,10}) similar to `A={1}, B={}, C={2}` or similar sets where $(A\cup B)\cap C \neq A\cup(B\cap C)$.

### Exercise 3.3 — Power Set

For $A=\{1,2,3\}$: 8 elements — $\emptyset$, $\{1\}$, $\{2\}$, $\{3\}$, $\{1,2\}$, $\{1,3\}$, $\{2,3\}$, $\{1,2,3\}$ (order may vary).

For $A=\{1,2,3,4,5\}$: 32 elements.

### Exercise 3.4

$A\times B$ for $A=\{1,2\}$, $B=\{'x','y','z'\}$: 6 pairs, matches $|A|\cdot|B|=2\times3=6$.

Inclusion-exclusion verifications: all should return `True` for the equality check across all tested triples (since these are true mathematical identities, not conjectures).

Multiples of 3 or 5 up to 300: **140** (matches PS4 E2 hand calculation).

---

## Section 4 — Reflection Model Answers

1. **Why Venn diagrams don't scale to 4+ sets:** A Venn diagram with $n$ sets needs $2^n$ distinguishable regions, each pairwise intersection pattern uniquely represented as a connected region. Beyond 3 circles, standard circular Venn diagrams cannot represent all $2^n$ regions as simple connected shapes — you need more exotic curves (ellipses for 4 sets), and even then, visual clarity collapses. More fundamentally, a diagram is a picture of *specific* sets, not a proof about *arbitrary* sets — it cannot establish a universal claim.

2. **Why one counterexample suffices but no number of confirmations proves:** A universal claim $\forall A,B,C\, [\text{identity}]$ is false if there exists even one triple where it fails — this is the direct application of the quantifier negation rule from Week 1 ($\neg\forall x P(x)\equiv\exists x\neg P(x)$). One witness to the negation suffices. Conversely, confirming the identity on finitely many (even many) specific sets does not establish it for ALL sets — this is the same reasoning as "proof by example is not proof" from Week 2.

3. **Recursive vs bitmask power set:** The recursive definition $\mathcal{P}(\{a\}\cup S)=\mathcal{P}(S)\cup\{s\cup\{a\}:s\in\mathcal{P}(S)\}$ directly mirrors the inductive step of Friday's proof — it partitions subsets into "those without $a$" (= $\mathcal{P}(S)$) and "those with $a$" (= $\mathcal{P}(S)$ each unioned with $\{a\}$), exactly matching the two cases used in the induction proof of $|\mathcal{P}(A)|=2^{|A|}$. The bitmask approach is a different (non-recursive) implementation strategy that computes the same result, but doesn't expose the inductive structure as directly.
