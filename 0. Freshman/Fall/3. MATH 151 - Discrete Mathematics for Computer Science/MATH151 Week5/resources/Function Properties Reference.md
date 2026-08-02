# MATH 151 — Function Properties Reference
## Week 5: Functions, Composition, Inverses, Bijections and Cardinality

---

## Core Definitions

| Term | Definition |
|---|---|
| Function $f:A\to B$ | Relation $f\subseteq A\times B$ with $\forall a\in A,\exists!b\in B,(a,b)\in f$ |
| Domain | $A$ (the set all inputs must come from) |
| Codomain | $B$ (the declared set outputs land in) |
| Range/Image | $\{f(a):a\in A\}\subseteq B$ (the actual set of achieved outputs) |
| Injective (1-1) | $\forall a_1,a_2\in A,\ f(a_1)=f(a_2)\to a_1=a_2$ |
| Surjective (onto) | $\forall b\in B,\exists a\in A,\ f(a)=b$ |
| Bijective | Injective AND surjective |

---

## Proof Template — Injectivity

```
Claim: f: A → B is injective.

Proof.
Let a₁, a₂ ∈ A be arbitrary.
Assume f(a₁) = f(a₂).
[algebraic steps]
Therefore a₁ = a₂.
Since a₁, a₂ were arbitrary, f is injective. ∎
```

**Disproof template:**
```
Claim: f is NOT injective.
Disproof. Take a₁ = [value], a₂ = [value]. 
Then a₁ ≠ a₂, but f(a₁) = [compute] = [compute] = f(a₂).
So f is not injective. ∎
```

---

## Proof Template — Surjectivity

```
Claim: f: A → B is surjective.

Proof.
Let b ∈ B be arbitrary.
Let a = [construct explicit expression in terms of b].
[Verify a ∈ A — check domain constraints!]
Verify: f(a) = f([expression]) = [algebra] = b. ✓
Since b was arbitrary, f is surjective. ∎
```

**Disproof template:**
```
Claim: f is NOT surjective.
Disproof. Take b = [specific value in codomain].
Suppose f(a) = b for some a ∈ A. Then [derive equation for a].
[Show no valid a ∈ A satisfies this — e.g., a is not an integer, or no real solution, etc.]
So no preimage exists. f is not surjective. ∎
```

---

## Counting Facts (Finite Sets)

| Condition | Implication |
|---|---|
| $f:A\to B$ injective | $|A|\leq|B|$ |
| $f:A\to B$ surjective | $|A|\geq|B|$ |
| $f:A\to B$ bijective | $|A|=|B|$ |
| $|A|=|B|$ (finite) AND $f$ injective | $f$ is automatically bijective |
| $|A|=|B|$ (finite) AND $f$ surjective | $f$ is automatically bijective |

**These shortcuts FAIL for infinite sets.** Example: $f:\mathbb{Z}^+\to\mathbb{Z}^+$, $f(n)=n+1$ is injective but not surjective (1 has no preimage).

---

## Composition

| Fact | Statement |
|---|---|
| Definition | $(g\circ f)(a) = g(f(a))$ — apply f first, then g |
| Associativity | $h\circ(g\circ f) = (h\circ g)\circ f$ |
| Commutativity | Does NOT hold in general |
| Identity | $f\circ\text{id}_A = f$, $\text{id}_B\circ f = f$ |

### Composition Preservation Table

| If... | Then... |
|---|---|
| $f,g$ both injective | $g\circ f$ injective |
| $f,g$ both surjective | $g\circ f$ surjective |
| $f,g$ both bijective | $g\circ f$ bijective |
| $g\circ f$ injective | $f$ injective (NOT necessarily $g$) |
| $g\circ f$ surjective | $g$ surjective (NOT necessarily $f$) |

**Memory aid:** "Injectivity flows backward through composition (constrains $f$); surjectivity flows forward (constrains $g$)."

---

## Inverses

| Fact | Statement |
|---|---|
| Fundamental Theorem | $f$ invertible $\iff$ $f$ bijective |
| Two-sided condition | $f^{-1}\circ f = \text{id}_A$ AND $f\circ f^{-1}=\text{id}_B$ |
| Inverse of composition | $(g\circ f)^{-1} = f^{-1}\circ g^{-1}$ (order reverses!) |
| Left inverse exists | $\iff f$ injective |
| Right inverse exists | $\iff f$ surjective |

### Computing an Inverse — Algorithm

1. Write $y=f(x)$.
2. Solve for $x$ in terms of $y$.
3. The result is $f^{-1}(y)$.
4. Verify BOTH $f^{-1}(f(x))=x$ AND $f(f^{-1}(y))=y$.

---


## Common Errors to Avoid

| Error | Correction |
|---|---|
| Confusing codomain and range | Codomain is declared; range is what's actually achieved — always check surjectivity against the CODOMAIN |
| Assuming injective ⟹ surjective (infinite sets) | Only true for same-size FINITE sets |
| Writing $g\circ f$ but computing $f(g(x))$ | $(g\circ f)(x) = g(f(x))$ — rightmost function applies first |
| Assuming composition is commutative | Almost always false — check both orders |
| Forgetting to verify constructed preimage is IN the domain | Especially critical when domain is $\mathbb{Z}$ but algebra gives a non-integer |
