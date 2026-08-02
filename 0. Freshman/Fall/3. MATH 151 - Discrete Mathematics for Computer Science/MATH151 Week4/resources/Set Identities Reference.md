# MATH 151 · Set Identities Reference
## Week 4: Proof Examples and Technique Bank

---

## The Logic ↔ Set Theory Dictionary

Every set identity has a propositional logic counterpart. When stuck on a set proof, translate to logic, prove it there (Week 0 skills), then translate back.

| Set Theory | Logic |
|---|---|
| $A \cup B$ | $P \lor Q$ |
| $A \cap B$ | $P \land Q$ |
| $\overline{A}$ | $\neg P$ |
| $A \subseteq B$ | $P \rightarrow Q$ |
| $A = B$ | $P \leftrightarrow Q$ |
| $U$ (universal set) | $T$ (tautology) |
| $\emptyset$ | $F$ (contradiction) |

**Every set identity is "logic wearing a costume."** De Morgan's for sets IS De Morgan's for logic, applied to the predicate "$x \in \cdot$."

---

## Fully Worked Element-Chasing Proofs (Reference Bank)

### 1. Commutativity of Union

**Theorem.** $A \cup B = B \cup A$.

**Proof.**
$$x \in A\cup B \iff x\in A \lor x\in B \iff x\in B \lor x\in A \iff x\in B\cup A$$
(using commutativity of $\lor$ from Week 0) ∎

### 2. Associativity of Intersection

**Theorem.** $(A\cap B)\cap C = A\cap(B\cap C)$.

**Proof.**
$$x\in(A\cap B)\cap C \iff (x\in A\land x\in B)\land x\in C \iff x\in A\land(x\in B\land x\in C) \iff x\in A\cap(B\cap C)$$
(using associativity of $\land$) ∎

### 3. De Morgan's Law (Union)

**Theorem.** $\overline{A\cup B}=\overline{A}\cap\overline{B}$.

**Proof.**
$$x\in\overline{A\cup B} \iff x\notin(A\cup B) \iff \neg(x\in A\lor x\in B) \iff \neg(x\in A)\land\neg(x\in B) \iff x\in\overline{A}\land x\in\overline{B} \iff x\in\overline{A}\cap\overline{B}$$
(central step: De Morgan's Law for propositions) ∎

### 4. De Morgan's Law (Intersection)

**Theorem.** $\overline{A\cap B}=\overline{A}\cup\overline{B}$.

**Proof.** Analogous, using $\neg(P\land Q)\equiv\neg P\lor\neg Q$. ∎

### 5. Distributivity (∩ over ∪)

**Theorem.** $A\cap(B\cup C)=(A\cap B)\cup(A\cap C)$.

**Proof.**
$$x\in A\cap(B\cup C) \iff x\in A\land(x\in B\lor x\in C) \iff (x\in A\land x\in B)\lor(x\in A\land x\in C)$$
(propositional distributivity: $P\land(Q\lor R)\equiv(P\land Q)\lor(P\land R)$)
$$\iff x\in(A\cap B)\lor x\in(A\cap C) \iff x\in(A\cap B)\cup(A\cap C)$$ ∎

### 6. Distributivity (∪ over ∩)

**Theorem.** $A\cup(B\cap C)=(A\cup B)\cap(A\cup C)$.

**Proof.** Analogous, using $P\lor(Q\land R)\equiv(P\lor Q)\land(P\lor R)$. ∎

### 7. Difference Identity

**Theorem.** $A-B=A\cap\overline{B}$.

**Proof.**
$$x\in A-B \iff x\in A\land x\notin B \iff x\in A\land x\in\overline{B} \iff x\in A\cap\overline{B}$$ ∎

### 8. Absorption

**Theorem.** $A\cup(A\cap B)=A$.

**Proof.**
$$x\in A\cup(A\cap B) \iff x\in A \lor (x\in A\land x\in B)$$

By the propositional absorption law $P\lor(P\land Q)\equiv P$:
$$\iff x\in A$$ ∎

---

## Fully Worked Algebraic Proofs (Reference Bank)

### 1. Proving $A - (B\cup C) = (A-B)\cap(A-C)$ algebraically

$$A-(B\cup C) = A\cap\overline{B\cup C} \qquad [\text{Difference Identity}]$$
$$= A\cap(\overline{B}\cap\overline{C}) \qquad [\text{De Morgan}]$$
$$= (A\cap\overline{B})\cap(A\cap\overline{C}) \qquad [\text{using } A\cap A = A \text{ and rearranging}]$$
$$= (A-B)\cap(A-C) \qquad [\text{Difference Identity, twice}]$$ ∎

### 2. Proving $A\cup(A\cap B) = A$ algebraically

$$A\cup(A\cap B) = (A\cap U)\cup(A\cap B) \qquad [\text{Identity Law: } A=A\cap U]$$
$$= A\cap(U\cup B) \qquad [\text{Distributivity}]$$
$$= A\cap U \qquad [\text{Domination: } U\cup B=U]$$
$$= A \qquad [\text{Identity Law}]$$ ∎

### 3. Proving $\overline{A-B} = \overline{A}\cup B$ algebraically

$$\overline{A-B} = \overline{A\cap\overline{B}} \qquad [\text{Difference Identity}]$$
$$= \overline{A}\cup\overline{\overline{B}} \qquad [\text{De Morgan}]$$
$$= \overline{A}\cup B \qquad [\text{Double Complement}]$$ ∎

---

## Subset Proof Bank

### 1. $A\cap B \subseteq A$

**Proof.** Let $x\in A\cap B$ be arbitrary. Then $x\in A \land x\in B$. In particular $x\in A$. Since $x$ was arbitrary, $A\cap B\subseteq A$. ∎

### 2. $A \subseteq A\cup B$

**Proof.** Let $x\in A$ be arbitrary. Then $x\in A \lor x\in B$ (trivially, since $x\in A$), so $x\in A\cup B$. Since $x$ was arbitrary, $A\subseteq A\cup B$. ∎

### 3. Monotonicity of Intersection

**Theorem.** If $A\subseteq B$ and $C\subseteq D$, then $A\cap C\subseteq B\cap D$.

**Proof.** Let $x\in A\cap C$ be arbitrary. Then $x\in A$ and $x\in C$. Since $A\subseteq B$, $x\in B$. Since $C\subseteq D$, $x\in D$. So $x\in B\cap D$. Since $x$ was arbitrary, $A\cap C\subseteq B\cap D$. ∎

### 4. Contrapositive for Sets

**Theorem.** $A\subseteq B \iff \overline{B}\subseteq\overline{A}$.

**Proof.**
$(\rightarrow)$ Assume $A\subseteq B$. Let $x\in\overline{B}$, so $x\notin B$. If $x\in A$, then since $A\subseteq B$, $x\in B$ — contradiction. So $x\notin A$, i.e., $x\in\overline{A}$. Thus $\overline{B}\subseteq\overline{A}$.

$(\leftarrow)$ Assume $\overline{B}\subseteq\overline{A}$. By the forward direction applied to $\overline{B}, \overline{A}$ (roles reversed) and double complementation, $\overline{\overline{A}}\subseteq\overline{\overline{B}}$, i.e., $A\subseteq B$. ∎

---

## Standard Disproof Counterexamples (Memorize These Patterns)

| Claim (False) | Counterexample | Computation |
|---|---|---|
| $A-(B-C)=(A-B)-C$ | $A=\{1,2,3\}, B=\{2\}, C=\{3\}$ | LHS=$\{1,3\}$, RHS=$\{1\}$ |
| $\mathcal{P}(A)\cup\mathcal{P}(B)=\mathcal{P}(A\cup B)$ | $A=\{1\}, B=\{2\}$ | $\{1,2\}\in$ RHS but not LHS |
| $(A\cup B)\cap C=A\cup(B\cap C)$ | $A=\{1\}, B=\{2\}, C=\{1,3\}$ | LHS=$\{1\}$, RHS=$\{1,2\}$ |
| $A\oplus B=A\cup B$ | $A=B=\{1\}$ | LHS=$\emptyset$, RHS=$\{1\}$ |

---

## Golden Rules for Set Proofs

1. **Every "let x be arbitrary" must genuinely assume nothing extra.**
2. **Element-chasing proofs should read as a chain of $\iff$ (or $\Rightarrow$ for subsets), each justified by a definition or a logic law.**
3. **Algebraic proofs should cite the specific named law at each step.**
4. **To disprove, one explicit counterexample with computed sets is sufficient and required.**
5. **When stuck, convert to logic** — every set-level puzzle has a logic-level twin from Week 0.
