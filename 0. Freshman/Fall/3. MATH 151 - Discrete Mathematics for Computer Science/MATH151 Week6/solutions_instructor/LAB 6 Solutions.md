# MATH 151 · Week 6
## LAB6 Solutions — INSTRUCTOR ONLY

*(Revised 2026-09-28: old Exercises 2.3 (relation from a partition), 3.3 (topological sort) and 4.3 (union-find), and reflection
questions 2–3, are no longer asked; lab 2.3 is old 2.4. Section 4 now uses lists of tuples and loops instead of `all(...)`,
set comprehensions and a dict-based class (CS 101 Week 8). Expected: 1.1(a) is reflexive, antisymmetric and transitive — a
partial order; 1.1(e) is symmetric only; the mod-4 classes are [0,4,8,12], [1,5,9,13], [2,6,10,14], [3,7,11,15], and the
classes of 0–3 suffice because every b in 0..15 is congruent to exactly one of them. `is_transitive` makes m² checks.)*

---

## Section 1 Solutions

### Exercise 1.1

**(a)** $A=\{1,2,3,4\}$, $R=\{(1,1),(2,2),(3,3),(4,4),(1,2),(2,3),(1,3)\}$
Reflexive: all 4 self-loops present. YES.
Symmetric: (1,2) present, (2,1) absent. NO.
Antisymmetric: check pairs with both directions — none found ((1,2) has no (2,1), etc.). YES (vacuously, no violating pair exists).
Transitive: (1,2),(2,3)⟹need(1,3) — present ✓. No other 2-chains. YES.
**Reflexive, antisymmetric, transitive → partial order.**

**(b)** $R=\{(a,b):ab>0\}$ on $\mathbb{Z}$ (nonzero, same sign)
Reflexive: need $a^2>0$, false for $a=0$. NOT reflexive.
Symmetric: $ab=ba$, so $ab>0\iff ba>0$. YES.
Antisymmetric: $(1,2)$: $1\cdot2=2>0$ ✓in R. $(2,1)$: same, in R. $1\neq2$. NOT antisymmetric.
Transitive: if $ab>0$ and $bc>0$, both pairs same-signed with $b$; if $b>0$ then $a>0$ and $c>0$, so $ac>0$. If $b<0$ then $a<0,c<0$, so $ac>0$. YES transitive.
**Symmetric, transitive, not reflexive, not antisymmetric.**

**(c)** Same number of digits, on $\mathbb{Z}^+$
Reflexive: same as self. YES.
Symmetric: same count is symmetric. YES.
Antisymmetric: 5 and 9 both 1-digit, in R both ways, 5≠9. NOT antisymmetric.
Transitive: digit-count equality is transitive. YES.
**Reflexive, symmetric, transitive → equivalence relation.**

**(d)** "at least as tall as" on people
Reflexive: everyone is at least as tall as themselves. YES.
Symmetric: if a≥height b, generally NOT b≥height a unless equal heights. NOT symmetric (generically).
Antisymmetric: if a≥b and b≥a in height, then a,b have EQUAL height — but they might be DIFFERENT people with the same height! So $(a,b)\in R,(b,a)\in R$ doesn't force $a=b$ as PEOPLE (only as heights). NOT antisymmetric (unless we define R on height values themselves, not people).
Transitive: standard transitivity of ≥. YES.
**Reflexive, transitive, generally not symmetric or antisymmetric (subtlety: depends on whether distinct people can share a height — assume yes, so not antisymmetric).**

**(e)** $A=\{1,2,3\}$, $R=\{(1,2),(2,1),(2,3),(3,2)\}$ — no self-loops
Reflexive: no self-loops at all. NOT reflexive.
Symmetric: (1,2)&(2,1) ✓, (2,3)&(3,2) ✓. YES.
Antisymmetric: (1,2),(2,1) both present, 1≠2. NOT antisymmetric.
Transitive: (1,2),(2,1)⟹need(1,1) — absent. NOT transitive.
**Only symmetric.**

---

## Section 2 Solutions

### Exercise 2.1

**Proof that same-remainder-mod-4 is an equivalence relation:**

Reflexive: $a\equiv a\pmod4$ since $4\mid0$. ✓
Symmetric: if $4\mid(a-b)$ then $4\mid(b-a)=-(a-b)$. ✓
Transitive: if $4\mid(a-b)$ and $4\mid(b-c)$, then $4\mid[(a-b)+(b-c)]=(a-c)$. ✓

Equivalence relation. ∎

Classes:
$[0]=\{\ldots,-4,0,4,8,\ldots\}$, reps: 0,4,8
$[1]=\{\ldots,-3,1,5,9,\ldots\}$, reps: 1,5,9
$[2]=\{\ldots,-2,2,6,10,\ldots\}$, reps: 2,6,10
$[3]=\{\ldots,-1,3,7,11,\ldots\}$, reps: 3,7,11

---

### Exercise 2.2

**(a)** Reflexive: same birthday as self ✓. Symmetric: if a,b share birthday, b,a share it too ✓. Transitive: if a,b share birthday and b,c share it, a,c share it ✓ (transitivity of equality on (month,day) pairs). Equivalence relation.

**(b)** At most 366 equivalence classes (accounting for Feb 29). Each class represents "everyone born on this specific calendar date" — a group of possibly many people, possibly empty if no one in the population was born that day.

---

### Exercise 2.3

**(a)** Partition $\{\{a,c\},\{b,d,e\},\{f\}\}$:

From $\{a,c\}$: $(a,a),(a,c),(c,a),(c,c)$
From $\{b,d,e\}$: $(b,b),(b,d),(b,e),(d,b),(d,d),(d,e),(e,b),(e,d),(e,e)$
From $\{f\}$: $(f,f)$

$R$ = union of all above.

**(b)** Total pairs: $2^2 + 3^2 + 1^2 = 4+9+1=14$ pairs. (For a part of size $k$, contributes $k^2$ ordered pairs — every combination including self-pairs.)

**(c)** Reflexive: every element's self-pair is included (each part contributes its own diagonal). ✓
Symmetric: each part's pairs are constructed symmetrically (if $(x,y)$ from a part, so is $(y,x)$, since both x,y are in the same part). ✓
Transitive: within a part, all pairs present means any 2-step chain lands back in the same part, whose pair is already included. ✓

---

### Exercise 2.4

$R=\{(a,b):|a-b|\leq2\}$ on $\mathbb{Z}$

**(a)** Reflexive: $|a-a|=0\leq2$. ✓

**(b)** Symmetric: $|a-b|=|b-a|$. ✓

**(c)** NOT transitive. Counterexample: $a=0,b=2,c=4$. $|0-2|=2\leq2$ ✓. $|2-4|=2\leq2$ ✓. But $|0-4|=4\not\leq2$. Fails.

**(d)** Since $R$ is not an equivalence relation, "the equivalence class of $a$" is not well-defined in the sense of the Fundamental Theorem — the set $\{x:xRa\}$ can still be COMPUTED (e.g., $\{a-2,a-1,a,a+1,a+2\}$), but these sets do NOT form a partition: they overlap in complicated ways without being identical or disjoint (e.g., the "class" of 0 is $\{-2,-1,0,1,2\}$ and the "class" of 1 is $\{-1,0,1,2,3\}$ — these overlap but are not equal), violating the disjoint-or-identical property that makes equivalence classes meaningful.

---

## Section 3 Solutions

### Exercise 3.1

$A=\{1,2,3,4,5,6,8,9,12,24\}$, divisibility order.

**(a) Covering relations:**
$1\lessdot2,1\lessdot3,1\lessdot5$
$2\lessdot4,2\lessdot6$
$3\lessdot6,3\lessdot9$
$4\lessdot8,4\lessdot12$
$5\lessdot$ (nothing else in set is a multiple of 5 except 5 itself, and 5 doesn't divide any other listed number except itself — 5 is isolated above 1)
$6\lessdot12$
$8\lessdot24$
$9\lessdot$ (nothing — 9 doesn't divide 12 or 24; 9∤24 since 24/9 not integer)
$12\lessdot24$

**(c) Maximum/minimum:** **No maximum.** The candidate would be 24, but $9\nmid24$, so 9 and 24 are incomparable and 24 dominates neither 9 nor 5. Maximal elements: 5, 9, 24 (nothing in the set is divisible by 5 other than 5; nothing by 9 other than 9; nothing by 24 other than 24). Minimum: 1 (divides everything). 

**(d) Longest chain:** $1,2,4,8,24$ — length 5.

**(e) Antichain of size 3:** $\{5,9,24\}$ — pairwise: 5∤9,9∤5,5∤24,24∤5,9∤24,24∤9. All incomparable. ✓ (Also could use other combinations.)

---

### Exercise 3.2

**(b)** Level sizes: 1,3,3,1 (subsets of size 0,1,2,3 of a 3-element set) — matches row 3 of Pascal's Triangle: $\binom30,\binom31,\binom32,\binom33 = 1,3,3,1$.

**(c)** Maximal chains from ∅ to {1,2,3}: each corresponds to an order of adding the 3 elements — there are $3!=6$ such chains (e.g., ∅,{1},{1,2},{1,2,3} corresponds to adding 1,then 2,then 3).

---

### Exercise 3.3

**(a)/(b)** Minimal element: core. Remove core: network, ui, logging all become minimal. 

Valid topological sorts (partial list, several exist since network/ui/logging are mutually incomparable and both network,ui must precede client):
- core, network, ui, logging, client
- core, ui, network, logging, client
- core, logging, network, ui, client
- core, network, logging, ui, client
- (and more permutations of {network, ui, logging} before client, with logging having no further constraint)

$3! = 6$ total valid orderings (any permutation of network, ui, logging after core, as long as client comes after both network and ui — since logging has no downstream dependency, it can go anywhere after core).

---

## Section 4 — Python Expected Outputs

### Exercise 4.1

```
Exercise 1.1(a): Reflexive, Antisymmetric, Transitive
  --> Exercise 1.1(a) IS a partial order
```

(Matches hand analysis.)

### Exercise 4.2

Running on {0,...,15} with mod-4 equivalence should produce 4 classes:
```
[0, 4, 8, 12]
[1, 5, 9, 13]
[2, 6, 10, 14]
[3, 7, 11, 15]
```

### Exercise 4.3

```python
uf.classes()
# [{'a','c'}, {'b','d','e'}, {'f'}]
```
Matches Exercise 2.3(a) partition exactly.

---

## Section 5 — Reflection Model Answers

1. Real-world example: "is within walking distance of" — you might be within walking distance of a coffee shop, which is within walking distance of a park, but the coffee shop-to-park distance stacked with your distance might exceed a reasonable "walking distance" threshold from you to the park directly. Closeness relations based on a threshold typically fail transitivity because small gaps can accumulate.

2. `find(x)` in Union-Find directly corresponds to identifying which equivalence class $x$ belongs to (returning a canonical representative) — it answers "what is $[x]$?" in constant amortized time via path compression, rather than the naive $O(n)$ scan of computing $\{y : y\sim x\}$ directly from the relation definition.

3. Topological sort succeeds on any finite poset because a finite poset always has a minimal element (no infinite descending chains possible in a finite set — Well-Ordering-style argument). If the underlying relation has a cycle, it's no longer a valid partial order (a cycle $a\prec b\prec c\prec a$ would force $a\prec a$ via transitivity, violating antisymmetry unless $a=b=c$) — such a "relation" isn't a genuine poset, and no consistent linear extension can exist, since you'd need $a$ before $b$ before $c$ before $a$ simultaneously — impossible.
