# MATH 151 · Discrete Mathematics for Computer Science
## Lab 4 — Set Workshop: Proofs, Venn Diagrams, and Computation
### Wednesday 28 October 2026, 15:00–16:50 · Week 5 | Duration: 2 hours | Covers Week 4 (all three lectures)

---

**Lab Objectives:**
1. Practice element-chasing and algebraic proofs of set identities
2. Use Venn diagrams as an intuition-building (not proof-providing) tool
3. Verify set identities computationally before proving them
4. Compute power sets recursively and check identities element by element
5. Apply Inclusion-Exclusion to real counting problems

**Materials:** Pencil, paper, laptop with Python 3.

---

## Section 1 — Venn Diagrams as Intuition (Not Proof) (20 min)

Venn diagrams are excellent for building intuition but are **not** a valid proof technique in this course — they don't scale beyond 3 sets and don't handle general/arbitrary sets. Use them to guess identities, then prove with element-chasing or algebra.

### Exercise 1.1

For each pair of expressions, sketch a 3-set Venn diagram (sets $A$, $B$, $C$) and shade the region corresponding to each expression. Determine if the two expressions represent the same region.

**(a)** $A \cap (B \cup C)$ vs. $(A \cap B) \cup (A \cap C)$

**(b)** $A - (B \cap C)$ vs. $(A - B) \cup (A - C)$

**(c)** $(A \cup B) \cap C$ vs. $A \cup (B \cap C)$

For each pair, state whether the shaded regions match. If they match, this suggests (but doesn't prove) an identity — you'll prove the true ones in Section 2.

---

### Exercise 1.2 — Venn Diagram Counting

Draw a 3-circle Venn diagram for sets $A$, $B$, $C$ within universe $U$. Label the 8 regions (including "in none").

Given: $|U|=100$, $|A|=40$, $|B|=35$, $|C|=30$, $|A\cap B|=15$, $|A\cap C|=10$, $|B\cap C|=8$, $|A\cap B\cap C|=3$.

Fill in the count for each of the 8 regions of the Venn diagram (the 7 "inside" regions plus "outside all three").

*(Work from the center outward: fill in $|A\cap B\cap C|$ first, then the pairwise-only regions, then the single-set-only regions, then the outside region.)*

---

## Section 2 — Proof Writing (45 min)

Write complete proofs. For each, state whether you use element-chasing or algebraic proof.

---

### Exercise 2.1

Prove: $A \cap (B \cup C) = (A \cap B) \cup (A \cap C)$

(This confirms your Venn diagram observation from Exercise 1.1(a).)

&nbsp;

&nbsp;

&nbsp;

&nbsp;

&nbsp;

---

### Exercise 2.2

**Disprove** (find a counterexample): $(A \cup B) \cap C = A \cup (B \cap C)$

(This should NOT match in your Venn diagram from 1.1(c) in general — find specific sets that break it.)

&nbsp;

&nbsp;

&nbsp;

&nbsp;

---

### Exercise 2.3

Prove: $A \subseteq B \iff A \cup B = B$

*(This is a biconditional — prove both directions.)*

&nbsp;

&nbsp;

&nbsp;

&nbsp;

&nbsp;

&nbsp;

---

## Section 3 — Python: Membership Tables (35 min)

A set identity holds exactly when, for **every** element x, "x is in the left side" and "x is in the right side"
have the same truth value. So a set identity is a propositional equivalence checked element by element —
Lab 0 again. Here the sets are Python **lists**, and `x in A` tests membership (CS 101 Lecture 05 §6). A loop
over the universe (CS 101 Week 2) does the checking.

Create `set_check.py`.

### Exercise 3.1 — Checking an Identity Element by Element

```python
U = list(range(1, 11))
A = [1, 2, 3, 4, 5]
B = [3, 4, 5, 6, 7]
C = [5, 6, 7, 8, 9]

# A ∩ (B ∪ C)  versus  (A ∩ B) ∪ (A ∩ C)
for x in U:
    lhs = (x in A) and ((x in B) or (x in C))
    rhs = ((x in A) and (x in B)) or ((x in A) and (x in C))
    if lhs != rhs:
        print("differs at", x)
print("checked", len(U), "elements")
```

Run it. Then change the two lines to check Exercise 1.1(b)'s identity, A − (B ∩ C) = (A − B) ∪ (A − C). (x ∈ A − B
is `(x in A) and not (x in B)`.) Try a second choice of A, B, C for each. Why does "no line printed" support your
Section 2 proof (and the Venn diagram) without proving the identity?

### Exercise 3.2 — The False Claim

Now check Exercise 2.2's claim, (A ∪ B) ∩ C = A ∪ (B ∩ C), with the same lists. Which x does the program print?
Use it to state a counterexample, and compare it with the one you found by hand.

### Exercise 3.3 — Power Set, Recursively

CS 101 Lecture 15 §5 builds the subsets of a list recursively: the subsets of the rest, plus each of those with the
first element added. Write

```python
def power_set(lst):
    """All subsets of lst, as a list of lists."""
```

and check that `len(power_set([1, 2, 3]))` is `8` and `len(power_set([1, 2, 3, 4, 5]))` is `32`. Print the eight
subsets of `[1, 2, 3]` and compare with your hand computation.

### Exercise 3.4 — Inclusion–Exclusion, Counted

How many integers from 1 to 300 are divisible by 3 or 5? First compute it by hand with |A ∪ B| = |A| + |B| − |A ∩ B|.
Then count it with a loop:

```python
count = 0
for x in range(1, 301):
    if x % 3 == 0 or x % 5 == 0:
        count += 1
print(count)
```

Do they agree? Which term of the formula corrects for the numbers counted twice?

---

## Section 4 — Reflection (10 min)

1. Why can't a Venn diagram serve as a rigorous proof for an identity involving 4 or more sets?

2. Why does a *single* explicit counterexample suffice to disprove a universal claim, even though *no* number of successful checks like Exercise 3.1 proves one?

3. Your `power_set` follows $\mathcal{P}(\{a\}\cup S) = \mathcal{P}(S) \cup \{s\cup\{a\} : s\in\mathcal{P}(S)\}$. How does it mirror the inductive proof that $|\mathcal{P}(A)| = 2^{|A|}$ from Friday's lecture?

---

## Checkoff Criteria

Show your TA:

- [ ] Exercise 1.2: Venn diagram fully labeled with correct region counts (sum should equal 100)
- [ ] Exercise 2.1: complete element-chasing proof
- [ ] Exercise 2.2: correct counterexample with computation shown
- [ ] Exercise 2.3: both directions of the biconditional proven
- [ ] `set_check.py` running: Exercise 3.1 on both identities, and `power_set([1, 2, 3])`
- [ ] Exercise 3.2: the program's counterexample matches the hand-found one

---

