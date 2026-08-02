# MATH 151 · Discrete Mathematics for Computer Science
## Lab 6 — Relations Workshop: Properties, Equivalence Classes, and Hasse Diagrams
### Wednesday, Week 6 | Duration: 2 hours

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

## Section 2 — Equivalence Relations and Classes (35 min)

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

### Exercise 2.3 — Building a Relation FROM a Partition

Let $A=\{a,b,c,d,e,f\}$ and consider the partition $\{\{a,c\},\{b,d,e\},\{f\}\}$.

**(a)** Write out the full equivalence relation $R$ (all ordered pairs) corresponding to this partition.

**(b)** How many ordered pairs does $R$ contain in total? *(Hint: for a part of size $k$, how many ordered pairs does it contribute?)*

**(c)** Verify: is $R$ reflexive? Symmetric? Transitive? (Spot-check, don't need to check every pair if you can argue generally.)

---

### Exercise 2.4 — A Relation That's NOT an Equivalence Relation

Consider $R = \{(a,b)\in\mathbb{Z}\times\mathbb{Z} : |a-b|\leq 2\}$.

**(a)** Show $R$ is reflexive.

**(b)** Show $R$ is symmetric.

**(c)** Show $R$ is NOT transitive (find a specific counterexample with 3 integers).

**(d)** Since $R$ fails to be an equivalence relation, does it still make sense to talk about "the equivalence class of $a$" under $R$? Explain what breaks down if you try.

---

## Section 3 — Hasse Diagrams and Posets (30 min)

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

### Exercise 3.3 — Topological Sort by Hand

A software project has these module dependencies (must-build-before):

$$\text{core}\preceq\text{network}, \quad \text{core}\preceq\text{ui}, \quad \text{network}\preceq\text{client}, \quad \text{ui}\preceq\text{client}, \quad \text{core}\preceq\text{logging}$$

**(a)** Draw the Hasse diagram.

**(b)** Perform a topological sort by hand: repeatedly select a minimal remaining element.

**(c)** List at least 2 different valid topological orderings.

---

## Section 4 — Python: Relation Property Checker (25 min)

Create `relation_tools.py`.

### Exercise 4.1

```python
def is_reflexive(R, A):
    return all((a,a) in R for a in A)

def is_symmetric(R, A):
    return all((b,a) in R for (a,b) in R)

def is_antisymmetric(R, A):
    return all(a == b for (a,b) in R if (b,a) in R)

def is_transitive(R, A):
    for (a,b) in R:
        for (c,d) in R:
            if b == c and (a,d) not in R:
                return False
    return True

def classify_relation(R, A, name="R"):
    props = []
    if is_reflexive(R, A): props.append("Reflexive")
    if is_symmetric(R, A): props.append("Symmetric")
    if is_antisymmetric(R, A): props.append("Antisymmetric")
    if is_transitive(R, A): props.append("Transitive")
    
    print(f"{name}: {', '.join(props) if props else 'None of the four properties'}")
    
    if is_reflexive(R,A) and is_symmetric(R,A) and is_transitive(R,A):
        print(f"  --> {name} IS an equivalence relation")
    if is_reflexive(R,A) and is_antisymmetric(R,A) and is_transitive(R,A):
        print(f"  --> {name} IS a partial order")
    
    return props
```

**Task:** Add to `relation_tools.py`. Test on all relations from Exercise 1.1 (represent each as a set of tuples over an appropriate finite domain).

```python
A = {1,2,3,4}
R = {(1,1),(2,2),(3,3),(4,4),(1,2),(2,3),(1,3)}
classify_relation(R, A, "Exercise 1.1(a)")
```

---

### Exercise 4.2 — Equivalence Class Computer

```python
def equivalence_classes(R, A):
    """
    Given an equivalence relation R on set A, compute all equivalence classes.
    Returns a list of sets (the classes).
    """
    A = list(A)
    seen = set()
    classes = []
    for a in A:
        if a in seen:
            continue
        cls = {b for b in A if (a,b) in R}
        classes.append(cls)
        seen |= cls
    return classes

# Test with "same remainder mod 4" on {0,...,15}
A = set(range(16))
R = {(a,b) for a in A for b in A if (a-b) % 4 == 0}
classes = equivalence_classes(R, A)
for c in classes:
    print(sorted(c))
```

**Task:** Run this and verify it matches your hand computation from Exercise 2.1 (restricted to the finite set {0,...,15}).

---

### Exercise 4.3 — Union-Find (Disjoint Set) — Computational Equivalence Classes

```python
class UnionFind:
    """Efficiently tracks equivalence classes (connected components)."""
    def __init__(self, elements):
        self.parent = {e: e for e in elements}
    
    def find(self, x):
        """Find canonical representative of x's class."""
        while self.parent[x] != x:
            x = self.parent[x]
        return x
    
    def union(self, x, y):
        """Merge the classes containing x and y."""
        rx, ry = self.find(x), self.find(y)
        if rx != ry:
            self.parent[rx] = ry
    
    def classes(self):
        """Return the current partition as a list of sets."""
        groups = {}
        for e in self.parent:
            r = self.find(e)
            groups.setdefault(r, set()).add(e)
        return list(groups.values())

# Test: build classes matching Exercise 2.3's partition
uf = UnionFind(['a','b','c','d','e','f'])
uf.union('a','c')
uf.union('b','d')
uf.union('d','e')
print(uf.classes())
```

**Task:** Run this and verify the resulting partition matches Exercise 2.3(a). This is exactly how compilers, Kruskal's MST algorithm, and network connectivity checkers implement equivalence classes efficiently — `union` merges classes as new equivalences are discovered, and `find` answers "are these two things equivalent?" in near-constant time.

---

## Section 5 — Reflection (5 min)

1. In Exercise 2.4, the relation $|a-b|\leq2$ fails transitivity. In everyday language, describe a real-world "closeness" relation that has this same flaw (reflexive, symmetric, but not transitive) — why does "close to" not behave like "equal to"?

2. Compare the Union-Find data structure to the Fundamental Theorem of Equivalence Relations from Thursday. What does `find(x)` correspond to, in the language of equivalence classes?

3. Why must a topological sort always succeed on a finite poset, but might fail (be impossible) if the underlying relation has a cycle (e.g., $a\preceq b\preceq c\preceq a$ with $a\neq b\neq c$)?

---

## Checkoff Criteria

Show your TA:

- [ ] Section 1: at least 4 of 5 relations correctly classified
- [ ] Exercise 2.1: complete equivalence relation proof with classes listed
- [ ] Exercise 2.4: correct identification of transitivity failure with explicit counterexample
- [ ] Exercise 3.1: Hasse diagram sketched with max/min/longest chain/antichain identified
- [ ] `relation_tools.py` running: demonstrate `classify_relation` and `equivalence_classes`
- [ ] Exercise 4.3: Union-Find demonstrated matching Exercise 2.3

---

*Bring all Python tools built so far (`logic_tools.py`, `predicate_tools.py`, `set_tools.py`, `function_tools.py`, `relation_tools.py`) to Lab 7 — counting builds on all of these.*
