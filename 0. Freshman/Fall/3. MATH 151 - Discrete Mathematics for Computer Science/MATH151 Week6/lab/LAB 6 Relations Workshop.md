# MATH 151 · Discrete Mathematics for Computer Science
## Lab 6 — Relations Workshop: Properties, Equivalence Classes, and Hasse Diagrams
### Wednesday 11 November 2026, 15:00–16:50 · Week 7 | Duration: 2 hours | Covers Week 6 (all three lectures)

---

**Lab Objectives:**
1. Practice classifying relations by their fundamental properties
2. Compute equivalence classes and verify the partition correspondence
3. Draw and interpret Hasse diagrams
4. Build a Python relation-property checker for finite sets
5. Implement and use a Union-Find structure to connect equivalence classes to CS

**Materials:** Pencil, paper, laptop with Python 3.

---

## Section 1 — Property Classification Drills (25 min)

For each relation, determine reflexive/symmetric/antisymmetric/transitive. Work quickly — build pattern recognition.

### Exercise 1.1

**(a)** $A=\{1,2,3,4\}$, $R=\{(1,1),(2,2),(3,3),(4,4),(1,2),(2,3),(1,3)\}$

**(b)** On $\mathbb{Z}$: $R = \{(a,b) : a\cdot b > 0\}$ (same sign, both nonzero)

**(c)** On $\mathbb{Z}^+$: $R = \{(a,b) : a\text{ and }b\text{ have the same number of digits}\}$

**(d)** On people: $R = \{(a,b) : a\text{ is at least as tall as }b\}$

**(e)** $A=\{1,2,3\}$, $R = \{(1,2),(2,1),(2,3),(3,2)\}$ (no self-loops at all)

---

## Section 2 — Equivalence Relations and Classes (30 min)

### Exercise 2.1

Prove that "same remainder mod 4" is an equivalence relation on $\mathbb{Z}$ (full three-property proof), then list all 4 equivalence classes with 3 sample elements each.

&nbsp;

&nbsp;

&nbsp;

&nbsp;

&nbsp;

---

### Exercise 2.2

On the set of all people, define $a\sim b \iff a$ and $b$ have the same birthday (month and day, ignoring year).

**(a)** Prove this is an equivalence relation.

**(b)** How many equivalence classes are (at most) possible? What does an equivalence class represent, in everyday terms?

&nbsp;

&nbsp;

---

### Exercise 2.3 — A Relation That's NOT an Equivalence Relation

Consider $R = \{(a,b)\in\mathbb{Z}\times\mathbb{Z} : |a-b|\leq 2\}$.

**(a)** Show $R$ is reflexive.

**(b)** Show $R$ is symmetric.

**(c)** Show $R$ is NOT transitive (find a specific counterexample with 3 integers).

**(d)** Since $R$ fails to be an equivalence relation, does it still make sense to talk about "the equivalence class of $a$" under $R$? Explain what breaks down if you try.

---

## Section 3 — Hasse Diagrams and Posets (25 min)

### Exercise 3.1

For the divisibility poset on $A=\{1,2,3,4,5,6,8,9,12,24\}$:

**(a)** List all covering relations (pairs $a\lessdot b$).

**(b)** Sketch the Hasse diagram (draw on paper — nodes with lines, no arrows, higher = "bigger" in divisibility).

**(c)** Identify the maximum and minimum elements (if they exist).

**(d)** Find the longest chain. State its elements and length.

**(e)** Find an antichain of size 3.

---

### Exercise 3.2

Consider the poset $(\mathcal{P}(\{1,2,3\}), \subseteq)$.

**(a)** Draw the Hasse diagram (this is the classic "cube" poset — 8 nodes).

**(b)** How many elements are at each "level" (by subset size 0,1,2,3)? What pattern do you notice? *(Connect to Pascal's Triangle / binomial coefficients — preview of Week 7!)*

**(c)** Identify all maximal chains (from $\emptyset$ to $\{1,2,3\}$) — how many are there? *(Hint: each corresponds to an ordering of adding elements 1, 2, 3 one at a time.)*

---

## Section 4 — Python: Relation Property Checker (25 min)

Create `relation_tools.py`. A relation is a **list of pairs**, written as tuples like `(1, 2)`, and
`(a, b) in R` tests membership (CS 101 Lecture 05 §6). Loops and `def` do the rest.

### Exercise 4.1

```python
def is_reflexive(R, A):
    for a in A:
        if (a, a) not in R:
            return False
    return True

def is_symmetric(R):
    for (a, b) in R:
        if (b, a) not in R:
            return False
    return True

def is_antisymmetric(R):
    for (a, b) in R:
        if a != b and (b, a) in R:
            return False
    return True

def is_transitive(R):
    for (a, b) in R:
        for (c, d) in R:
            if b == c and (a, d) not in R:
                return False
    return True
```

**Task:** Write `classify_relation(R, A, name)` that prints which of the four properties hold, and whether R is
an equivalence relation or a partial order. Test it on Exercise 1.1(a) and 1.1(e):

```python
A = [1, 2, 3, 4]
R = [(1, 1), (2, 2), (3, 3), (4, 4), (1, 2), (2, 3), (1, 3)]
classify_relation(R, A, "Exercise 1.1(a)")
```

### Exercise 4.2 — Equivalence Classes

Build "same remainder mod 4" on {0, …, 15} with two loops, then list the classes:

```python
A = list(range(16))
R = []
for a in A:
    for b in A:
        if (a - b) % 4 == 0:
            R.append((a, b))

def equivalence_class(R, A, a):
    """[a] = all b related to a."""
    cls = []
    for b in A:
        if (a, b) in R:
            cls.append(b)
    return cls

for a in [0, 1, 2, 3]:
    print(a, equivalence_class(R, A, a))
```

**Task:** Check the four classes against Exercise 2.1 (restricted to {0, …, 15}). Why is it enough to print the
classes of 0, 1, 2 and 3?

---

## Section 5 — Reflection (5 min)

1. In Exercise 2.3, the relation $|a-b|\leq2$ fails transitivity. In everyday language, describe a real-world
"closeness" relation that has the same flaw (reflexive, symmetric, but not transitive). Why does "close to" not
behave like "equal to"?

2. `is_transitive` checks every pair of pairs. For a relation with m pairs, how many checks is that?

---

## Checkoff Criteria

Show your TA:

- [ ] Section 1: at least 4 of 5 relations correctly classified
- [ ] Exercise 2.1: complete equivalence relation proof with classes listed
- [ ] Exercise 2.3: correct identification of transitivity failure with explicit counterexample
- [ ] Exercise 3.1: Hasse diagram sketched with max/min/longest chain/antichain identified
- [ ] `relation_tools.py` running: demonstrate `classify_relation` and the four equivalence classes

---

