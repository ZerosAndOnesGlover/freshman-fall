# MATH 151 — Discrete Mathematics for Computer Science
## Lecture 4.2 (L13) — Set Identities and Proof Techniques
### Thursday, Week 4

---

> **Core Question:** How do we rigorously prove that two set expressions are always equal, for every possible choice of underlying sets?

---

## 1. The Complete Table of Set Identities

These identities hold for all sets $A$, $B$, $C$ within a universal set $U$. Each mirrors a propositional logic law exactly (Week 0), because set operations are defined via logical connectives on membership.

### Identity Laws
$$A \cup \emptyset = A \qquad A \cap U = A$$

### Domination Laws
$$A \cup U = U \qquad A \cap \emptyset = \emptyset$$

### Idempotent Laws
$$A \cup A = A \qquad A \cap A = A$$

### Complementation Laws
$$A \cup \overline{A} = U \qquad A \cap \overline{A} = \emptyset \qquad \overline{\overline{A}} = A$$

### Commutative Laws
$$A \cup B = B \cup A \qquad A \cap B = B \cap A$$

### Associative Laws
$$(A \cup B) \cup C = A \cup (B \cup C) \qquad (A \cap B) \cap C = A \cap (B \cap C)$$

### Distributive Laws
$$A \cup (B \cap C) = (A \cup B) \cap (A \cup C)$$
$$A \cap (B \cup C) = (A \cap B) \cup (A \cap C)$$

### De Morgan's Laws ⭐
$$\overline{A \cup B} = \overline{A} \cap \overline{B}$$
$$\overline{A \cap B} = \overline{A} \cup \overline{B}$$

### Absorption Laws
$$A \cup (A \cap B) = A \qquad A \cap (A \cup B) = A$$

### Complement of Universal / Empty Set
$$\overline{U} = \emptyset \qquad \overline{\emptyset} = U$$

### Set Difference Identity
$$A - B = A \cap \overline{B}$$

This last identity is crucial — it lets you convert every set-difference expression into intersection and complement, after which all the standard laws apply directly.

---

## 2. Two Proof Techniques for Set Identities

There are two standard techniques for proving $X = Y$ where $X, Y$ are set expressions:

### Technique 1: Element-Chasing (Double Inclusion via Membership)

Prove $x \in X \iff x \in Y$ for an arbitrary element $x$. This directly establishes $X = Y$ by the definition of set equality (extensionality).

**Structure:**
```
Let x be an arbitrary element.
x ∈ X
⟺ [expand definition of X, apply logical laws]
⟺ [expand definition of Y]
⟺ x ∈ Y

Since x was arbitrary, X = Y.
```

### Technique 2: Algebraic Proof via Set Laws

Use the set identities from Section 1 directly, analogous to algebraic manipulation, without unpacking to element-level logic.

**Structure:**
```
X = [expression]
  = [apply law 1]
  = [apply law 2]
  ...
  = Y
```

**Which to use?** Both are equally valid. Algebraic proofs are often shorter once you know the identities well. Element-chasing proofs are more fundamental and better for building intuition, especially when the identity you need isn't in the standard table.

---

## 3. Worked Examples — Element-Chasing

### Example 1: De Morgan's Law for Sets

**Theorem.** $\overline{A \cup B} = \overline{A} \cap \overline{B}$.

**Proof.** Let $x$ be an arbitrary element of the universal set $U$.

$$x \in \overline{A \cup B}$$
$$\iff x \notin (A \cup B) \qquad \text{[definition of complement]}$$
$$\iff \neg(x \in A \cup B) \qquad \text{[definition of } \notin \text{]}$$
$$\iff \neg(x \in A \lor x \in B) \qquad \text{[definition of union]}$$
$$\iff \neg(x \in A) \land \neg(x \in B) \qquad \text{[De Morgan's Law, propositional logic]}$$
$$\iff x \notin A \land x \notin B$$
$$\iff x \in \overline{A} \land x \in \overline{B} \qquad \text{[definition of complement]}$$
$$\iff x \in \overline{A} \cap \overline{B} \qquad \text{[definition of intersection]}$$

Since $x$ was arbitrary, $\overline{A \cup B} = \overline{A} \cap \overline{B}$. ∎

**Observe:** The entire proof is a direct translation of the propositional De Morgan's Law $\neg(P \lor Q) \equiv \neg P \land \neg Q$, applied at the level of set membership. This is exactly why the set-theoretic and propositional versions share the same name.

---

### Example 2: Distributive Law

**Theorem.** $A \cap (B \cup C) = (A \cap B) \cup (A \cap C)$.

**Proof.** Let $x$ be arbitrary.

$$x \in A \cap (B \cup C)$$
$$\iff x \in A \land x \in (B \cup C) \qquad \text{[intersection]}$$
$$\iff x \in A \land (x \in B \lor x \in C) \qquad \text{[union]}$$
$$\iff (x \in A \land x \in B) \lor (x \in A \land x \in C) \qquad \text{[Distributivity, propositional logic]}$$
$$\iff x \in (A \cap B) \lor x \in (A \cap C) \qquad \text{[intersection]}$$
$$\iff x \in (A \cap B) \cup (A \cap C) \qquad \text{[union]}$$

Since $x$ was arbitrary, the two sets are equal. ∎

---

### Example 3: A Set Difference Identity

**Theorem.** $A - (B \cup C) = (A - B) \cap (A - C)$.

**Proof.** Let $x$ be arbitrary.

$$x \in A - (B \cup C)$$
$$\iff x \in A \land x \notin (B \cup C) \qquad \text{[difference]}$$
$$\iff x \in A \land \neg(x \in B \lor x \in C) \qquad \text{[union]}$$
$$\iff x \in A \land (x \notin B \land x \notin C) \qquad \text{[De Morgan]}$$
$$\iff (x \in A \land x \notin B) \land (x \in A \land x \notin C) \qquad \text{[distribute } x \in A \text{ — see note below]}$$
$$\iff x \in (A - B) \land x \in (A - C) \qquad \text{[difference]}$$
$$\iff x \in (A-B) \cap (A-C) \qquad \text{[intersection]}$$

Since $x$ was arbitrary, $A - (B \cup C) = (A-B) \cap (A-C)$. ∎

**Note on the distribute step:** $P \land (Q \land R) \equiv (P \land Q) \land (P \land R)$ is valid propositionally (verify via idempotence: $(P\land Q)\land(P\land R) \equiv P\land P\land Q\land R \equiv P\land Q\land R$).

---

## 4. Worked Example — Algebraic (Law-Based) Proof

### Example 4: The Same Theorem, Proved Algebraically

**Theorem.** $A - (B \cup C) = (A - B) \cap (A - C)$.

**Proof.**
$$A - (B \cup C) = A \cap \overline{B \cup C} \qquad \text{[Difference Identity]}$$
$$= A \cap (\overline{B} \cap \overline{C}) \qquad \text{[De Morgan's Law]}$$
$$= (A \cap \overline{B}) \cap (A \cap \overline{C}) \qquad \text{[using } A = A \cap A \text{, Associativity, Commutativity — see below]}$$
$$= (A - B) \cap (A - C) \qquad \text{[Difference Identity, applied twice]}$$

∎

*Detail on the middle step:* $A \cap (\overline{B} \cap \overline{C}) = (A \cap A) \cap (\overline{B} \cap \overline{C})$ [Idempotence: $A = A \cap A$] $= (A \cap \overline{B}) \cap (A \cap \overline{C})$ [rearranging via Associativity/Commutativity].

**Comparing the two proofs:** The algebraic proof is shorter once you're fluent in the identities. The element-chasing proof is more transparent about *why* the identity holds, since it's grounded directly in logic. Both are equally rigorous.

---

## 5. Disproving Set Identities — Counterexamples

Not every plausible-looking set identity is true. To disprove a claimed identity, exhibit specific sets where it fails.

### Example 5

**Claim (FALSE):** $A - (B - C) = (A - B) - C$ for all sets $A, B, C$.

**Disproof.** Let $A = \{1,2,3\}$, $B = \{2\}$, $C = \{3\}$.

$$B - C = \{2\} - \{3\} = \{2\}$$
$$A - (B-C) = \{1,2,3\} - \{2\} = \{1,3\}$$

$$A - B = \{1,2,3\} - \{2\} = \{1,3\}$$
$$(A-B) - C = \{1,3\} - \{3\} = \{1\}$$

$\{1,3\} \neq \{1\}$, so the claim is FALSE. ∎

**The correct identity** (which you'll prove in the problem set) is: $A - (B-C) = (A-B) \cup (A \cap C)$.

---

### Example 6

**Claim (FALSE):** $\mathcal{P}(A) \cup \mathcal{P}(B) = \mathcal{P}(A \cup B)$.

**Disproof.** Let $A = \{1\}$, $B = \{2\}$.

$\mathcal{P}(A) = \{\emptyset, \{1\}\}$, $\mathcal{P}(B) = \{\emptyset, \{2\}\}$.
$\mathcal{P}(A) \cup \mathcal{P}(B) = \{\emptyset, \{1\}, \{2\}\}$.

$A \cup B = \{1,2\}$. $\mathcal{P}(A \cup B) = \{\emptyset, \{1\}, \{2\}, \{1,2\}\}$.

$\{1,2\} \in \mathcal{P}(A\cup B)$ but $\{1,2\} \notin \mathcal{P}(A)\cup\mathcal{P}(B)$ (since $\{1,2\}$ is not a subset of $\{1\}$ alone or $\{2\}$ alone).

So the sets are not equal. ∎

*(The correct relationship is $\mathcal{P}(A) \cup \mathcal{P}(B) \subseteq \mathcal{P}(A \cup B)$, and equality holds only in special cases — see Friday's lecture.)*

---

## 6. Proving Subset Relationships

Sometimes you need $A \subseteq B$ rather than $A = B$. The technique is nearly identical — element-chasing but with $\rightarrow$ instead of $\leftrightarrow$.

### Example 7

**Theorem.** $A \cap B \subseteq A \cup B$ for all sets $A, B$.

**Proof.** Let $x \in A \cap B$ be arbitrary.

By definition of intersection, $x \in A$ and $x \in B$.

In particular, $x \in A$. By the definition of union (since $x\in A$, certainly $x\in A \lor x\in B$), $x \in A \cup B$.

Since $x$ was an arbitrary element of $A \cap B$, we conclude $A \cap B \subseteq A \cup B$. ∎

### Example 8

**Theorem.** If $A \subseteq B$, then $\overline{B} \subseteq \overline{A}$.

**Proof.** Assume $A \subseteq B$. Let $x \in \overline{B}$ be arbitrary.

Then $x \notin B$.

We claim $x \notin A$. Suppose for contradiction $x \in A$. Since $A \subseteq B$, this would give $x \in B$ — contradicting $x \notin B$. Therefore $x \notin A$.

So $x \in \overline{A}$.

Since $x$ was arbitrary, $\overline{B} \subseteq \overline{A}$. ∎

**Note:** This proof embeds a contrapositive argument (from Week 2) inside an element-chasing proof — a common and natural combination.

---

## 7. Common Errors in Set Proofs

### Error 1: Proving Only One Direction

To prove $A = B$, you generally need BOTH $A \subseteq B$ and $B \subseteq A$ (unless using a chain of $\iff$ throughout, which establishes both directions simultaneously).

### Error 2: Assuming the Element Has Extra Properties

When you write "let $x \in A$ be arbitrary," you may assume NOTHING about $x$ beyond $x \in A$ (and whatever else is explicitly given). Do not assume $x$ is, say, a specific type of number unless the problem states so.

### Error 3: Confusing $\in$ and $\subseteq$

$x \in A$ means $x$ is an element of $A$. $X \subseteq A$ means every element of $X$ is in $A$. These are different relations with different types — do not write $\{1\} \in \{1,2,3\}$ (false — $\{1\}$ is a set, not an element of this set) when you mean $\{1\} \subseteq \{1,2,3\}$ (true) or $1 \in \{1,2,3\}$ (true).

---

## 8. Summary — Proof Strategy Guide

| To prove | Strategy |
|---|---|
| $A = B$ | Element-chasing with $\iff$ throughout, OR algebraic law chain, OR double inclusion ($A\subseteq B$ and $B\subseteq A$ separately) |
| $A \subseteq B$ | Let $x \in A$ be arbitrary; derive $x \in B$ |
| $A \neq B$ | Exhibit a specific element in one but not the other, or specific sets making the general claim false |
| $A \cap B = \emptyset$ | Assume $x \in A \cap B$ for contradiction; derive a contradiction |

---

## 9. End-of-Lecture Exercises

1. Prove by element-chasing:
   - (a) $A \cup (B \cap C) = (A \cup B) \cap (A \cup C)$
   - (b) $\overline{A \cap B} = \overline{A} \cup \overline{B}$
   - (c) $A \cap (B - C) = (A \cap B) - (A \cap C)$

2. Prove the same identity from 1(a) using only the algebraic laws (no element-chasing).

3. Disprove each claim with a specific counterexample:
   - (a) $A - B = \overline{B} - \overline{A}$ for all sets $A, B$.
   - (b) $(A \cup B) - C = A \cup (B - C)$ for all sets $A, B, C$.

4. Prove: $A \subseteq B$ if and only if $\overline{B} \subseteq \overline{A}$ (the contrapositive relationship for sets).

5. Prove: $A - (B - C) = (A - B) \cup (A \cap C)$.

---

*Next: Lecture 4.3 — Power Sets, Cartesian Products, and Inclusion-Exclusion*
