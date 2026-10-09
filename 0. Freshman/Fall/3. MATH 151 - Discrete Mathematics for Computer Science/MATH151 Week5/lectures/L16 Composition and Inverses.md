# MATH 151 · Discrete Mathematics for Computer Science
## Lecture 16 (L16) — Composition of Functions and Inverse Functions
### Thursday, Week 5

*“It is by logic that we prove, but by intuition that we discover. To know how to criticize is good, to know how to create is better.”* — Henri Poincaré, *Science and Method* (1908)

**Date:** Thursday 29 October 2026 · 13:00–13:50 · Week 5

**Reading:** Rosen, 8e §2.3 · Epp, 5e §7.2–7.3 · Levin, 3e §0.4 *(details at the end of the lecture)*

**Coursework:** 📝 **PS 4** due Fri 30 Oct 17:00 · 📝 **PS 5** released Fri 30 Oct 14:00, due Fri 6 Nov 17:00 · 📊 **Quiz 6** Mon 2 Nov 13:00–13:15 · 🔬 **Lab 5** Wed 4 Nov 15:00–16:50 · 📘 **Midterm 1** Fri 6 Nov 18:00–19:15

---

> **Core Question:** How do we combine functions to build new ones, and when can a function be "undone"?

---

## 1. Function Composition

**Definition.** Given functions $f: A \to B$ and $g: B \to C$, the **composition** $g \circ f: A \to C$ is defined by:

$$(g \circ f)(a) = g(f(a))$$

**Reading order:** $g \circ f$ means "first apply $f$, then apply $g$." This is the opposite of left-to-right reading — an extremely common source of errors. Always double-check by considering what $(g\circ f)(a)$ computes: $f$ acts on $a$ first (it's closest to $a$), producing $f(a) \in B$; then $g$ acts on that result.

**Requirement:** For $g \circ f$ to be well-defined, the codomain of $f$ must match the domain of $g$ (or at least, the range of $f$ must be a subset of the domain of $g$).

### Worked Example 1

Let $f: \mathbb{Z} \to \mathbb{Z}$, $f(x) = x+1$, and $g: \mathbb{Z} \to \mathbb{Z}$, $g(x) = x^2$.

$$(g\circ f)(x) = g(f(x)) = g(x+1) = (x+1)^2$$

$$(f\circ g)(x) = f(g(x)) = f(x^2) = x^2+1$$

**Note:** $(g\circ f)(x) = (x+1)^2 = x^2+2x+1 \neq x^2+1 = (f\circ g)(x)$ in general.

**Function composition is NOT commutative.** $g\circ f \neq f\circ g$ in general — this must always be checked, never assumed.

---

## 2. Composition Preserves Injectivity and Surjectivity

**Theorem.** If $f: A \to B$ and $g: B \to C$ are both injective, then $g\circ f: A \to C$ is injective.

**Proof.** Let $a_1, a_2 \in A$ be arbitrary. Assume $(g\circ f)(a_1) = (g\circ f)(a_2)$.

By definition of composition: $g(f(a_1)) = g(f(a_2))$.

Since $g$ is injective: $f(a_1) = f(a_2)$.

Since $f$ is injective: $a_1 = a_2$.

Since $a_1, a_2$ were arbitrary, $g\circ f$ is injective. ∎

**Theorem.** If $f: A \to B$ and $g: B \to C$ are both surjective, then $g\circ f: A \to C$ is surjective.

**Proof.** Let $c \in C$ be arbitrary. Since $g$ is surjective, there exists $b \in B$ with $g(b) = c$.

Since $f$ is surjective, there exists $a \in A$ with $f(a) = b$.

Then $(g\circ f)(a) = g(f(a)) = g(b) = c$.

Since $c$ was arbitrary, $g\circ f$ is surjective. ∎

**Corollary.** If $f$ and $g$ are both bijective, then $g\circ f$ is bijective. (Direct consequence of the two theorems.)

### The Converse Is Partially True — Handle With Care

**Theorem.** If $g\circ f$ is injective, then $f$ is injective.

**Proof.** [Contrapositive] Assume $f$ is not injective. Then there exist $a_1 \neq a_2$ with $f(a_1) = f(a_2)$.

Then $g(f(a_1)) = g(f(a_2))$, i.e., $(g\circ f)(a_1) = (g\circ f)(a_2)$ with $a_1\neq a_2$.

So $g\circ f$ is not injective. By contrapositive, if $g\circ f$ is injective, $f$ is injective. ∎

**Important:** This does NOT tell you $g$ is injective! $g$ could fail to be injective on elements outside the range of $f$, and $g\circ f$ could still be injective.

**Theorem.** If $g\circ f$ is surjective, then $g$ is surjective.

**Proof.** Let $c\in C$ be arbitrary. Since $g\circ f$ is surjective, there exists $a\in A$ with $(g\circ f)(a) = c$, i.e., $g(f(a)) = c$.

Let $b = f(a) \in B$. Then $g(b) = c$.

Since $c$ was arbitrary, $g$ is surjective. ∎

**Again:** this does NOT tell you $f$ is surjective.

---

### Worked Counterexample — Illustrating the Asymmetry

Let $A = \{1\}$, $B = \{1,2\}$, $C=\{1\}$.

$f: A\to B$, $f(1)=1$. (Injective, not surjective onto B.)

$g: B\to C$, $g(1)=1, g(2)=1$. (Surjective onto C, not injective.)

$(g\circ f)(1) = g(f(1)) = g(1) = 1$.

$g\circ f: A\to C$ is trivially bijective (single element domain and codomain, both singletons) — injective AND surjective, despite $g$ not being injective and $f$ not being surjective!

This confirms: $g\circ f$ injective only forces $f$ injective (not $g$); $g\circ f$ surjective only forces $g$ surjective (not $f$).

---

## 3. Associativity of Composition

**Theorem.** For functions $f: A\to B$, $g: B\to C$, $h: C\to D$:
$$h \circ (g \circ f) = (h \circ g) \circ f$$

**Proof.** For arbitrary $a \in A$:

$$[h\circ(g\circ f)](a) = h((g\circ f)(a)) = h(g(f(a)))$$
$$[(h\circ g)\circ f](a) = (h\circ g)(f(a)) = h(g(f(a)))$$

Both sides equal $h(g(f(a)))$ for every $a$. Since the functions agree on every input, they are equal. ∎

**Consequence:** We can write $h\circ g\circ f$ unambiguously, without parentheses — the grouping doesn't matter (though the ORDER absolutely does, since composition is not commutative).

---

## 4. The Identity Function

**Definition.** For a set $A$, the **identity function** $\text{id}_A: A \to A$ is defined by $\text{id}_A(a) = a$ for all $a \in A$.

**Key property:** For any $f: A \to B$:
$$f \circ \text{id}_A = f \qquad \text{and} \qquad \text{id}_B \circ f = f$$

The identity function acts as a "do-nothing" — analogous to the number 1 for multiplication or the empty string for concatenation.

---

## 5. Inverse Functions

**Definition.** Let $f: A \to B$. A function $g: B \to A$ is the **inverse** of $f$ if:
$$g \circ f = \text{id}_A \qquad \text{and} \qquad f \circ g = \text{id}_B$$

If such a $g$ exists, we write $g = f^{-1}$, and say $f$ is **invertible**.

### The Fundamental Theorem of Invertibility

**Theorem.** A function $f: A \to B$ is invertible if and only if $f$ is bijective.

**Proof.**

**($\rightarrow$) If $f$ is invertible, then $f$ is bijective.**

Assume $f^{-1}$ exists with $f^{-1}\circ f = \text{id}_A$ and $f\circ f^{-1} = \text{id}_B$.

*Injective:* Let $f(a_1) = f(a_2)$. Apply $f^{-1}$ to both sides: $f^{-1}(f(a_1)) = f^{-1}(f(a_2))$, i.e., $a_1 = a_2$ (using $f^{-1}\circ f = \text{id}_A$). So $f$ is injective.

*Surjective:* Let $b \in B$ be arbitrary. Let $a = f^{-1}(b) \in A$. Then $f(a) = f(f^{-1}(b)) = (f\circ f^{-1})(b) = \text{id}_B(b) = b$ (using $f\circ f^{-1} = \text{id}_B$). So $f$ is surjective.

Therefore $f$ is bijective.

**($\leftarrow$) If $f$ is bijective, then $f$ is invertible.**

Assume $f$ is bijective. Define $g: B \to A$ as follows: for each $b\in B$, since $f$ is surjective, there exists $a\in A$ with $f(a)=b$; since $f$ is injective, this $a$ is unique. Define $g(b) := $ this unique $a$.

(This defines $g$ as a genuine function: totality holds because $f$ is surjective — every $b$ has some preimage; well-definedness holds because $f$ is injective — the preimage is unique.)

Verify $g\circ f = \text{id}_A$: for $a\in A$, let $b=f(a)$. By construction, $g(b)$ is the unique element mapping to $b$ under $f$ — and $a$ is such an element, so $g(b)=a$, i.e., $g(f(a))=a$.

Verify $f\circ g = \text{id}_B$: for $b\in B$, let $a=g(b)$, so $f(a)=b$ by construction. Then $f(g(b))=f(a)=b$.

Therefore $g=f^{-1}$ exists, and $f$ is invertible. ∎

**This theorem is why "invertible" and "bijective" are used almost interchangeably** — they are logically equivalent for functions.

---

## 6. Computing Inverse Functions — Worked Examples

### Example 2

$f: \mathbb{R} \to \mathbb{R}$, $f(x) = 2x+3$. We showed this is bijective (Monday's lecture). Find $f^{-1}$.

**Method:** Solve $y = 2x+3$ for $x$ in terms of $y$: $x = \frac{y-3}{2}$.

So $f^{-1}(y) = \frac{y-3}{2}$.

**Verify:** $f^{-1}(f(x)) = f^{-1}(2x+3) = \frac{(2x+3)-3}{2} = \frac{2x}{2} = x$. ✓

$f(f^{-1}(y)) = f\left(\frac{y-3}{2}\right) = 2\cdot\frac{y-3}{2}+3 = (y-3)+3 = y$. ✓

### Example 3

$f: \mathbb{Z} \to \mathbb{Z} \times \{0,1\}$ where $f(n) = (\lfloor n/2\rfloor, n \bmod 2)$ — this decomposes an integer into "half" and "parity."

This turns out to be a bijection (each integer corresponds uniquely to a quotient-remainder pair under division by 2). The inverse:

$$f^{-1}(q, r) = 2q + r$$

**Verify:** if $n$ is even, $n=2k$: $f(n) = (k, 0)$. $f^{-1}(k,0) = 2k+0=2k=n$. ✓
If $n$ is odd, $n=2k+1$: $f(n)=(k,1)$. $f^{-1}(k,1)=2k+1=n$. ✓

---

## 7. Non-Invertible Functions and Partial Workarounds

If $f: A\to B$ is not bijective, there is no true inverse function. But two useful partial notions exist:

**Left inverse:** $g: B\to A$ such that $g\circ f = \text{id}_A$. Exists iff $f$ is injective.

**Right inverse:** $g: B\to A$ such that $f\circ g = \text{id}_B$. Exists iff $f$ is surjective.

**Example:** $f: \mathbb{Z} \to \mathbb{Z}$, $f(n) = 2n$ (injective, not surjective — range is even integers only).

A left inverse exists: $g(n) = \lfloor n/2\rfloor$ satisfies $g(f(n))=g(2n)=\lfloor 2n/2\rfloor=n$ for all $n$. But $f(g(n)) = f(\lfloor n/2\rfloor) = 2\lfloor n/2\rfloor \neq n$ when $n$ is odd — so $g$ is NOT a right inverse; it's only a left inverse. This confirms $f$ has no full two-sided inverse (consistent with $f$ not being surjective).

---

## 8. Composition and Inverses in Computer Science

**Unix pipes and function composition:** `cat file | grep pattern | sort` is literally $sort \circ grep \circ cat$ — data flows through a composition of functions (programs), each transforming the output of the previous.

**Cryptography:** Decryption is the inverse function of encryption: $D_k = E_k^{-1}$. This is why encryption functions (for a fixed key) must be bijective — a non-bijective "encryption" cannot be reliably decrypted.

**Compiler pipelines:** `lexer → parser → typechecker → codegen` is a composition of functions, each transforming one intermediate representation into the next. (CS 211/CS 311.)

**Reversible computing:** In quantum computing and some low-power computing models, all logic gates must be bijective (invertible) — this connects directly to the theorem above: a computational step can be "run backward" if and only if it's a bijection.

**Serialization/Deserialization:** A serializer $\text{serialize}: \text{Object} \to \text{Bytes}$ and deserializer $\text{deserialize}: \text{Bytes}\to\text{Object}$ should ideally be mutual inverses: $\text{deserialize}(\text{serialize}(x)) = x$.

---

## 9. Summary

```
Composition:
  (g∘f)(a) = g(f(a))
  Requires: range(f) ⊆ domain(g)
  Associative: h∘(g∘f) = (h∘g)∘f
  NOT commutative: g∘f ≠ f∘g in general
  
  f,g injective ⟹ g∘f injective
  f,g surjective ⟹ g∘f surjective
  g∘f injective ⟹ f injective (NOT g)
  g∘f surjective ⟹ g surjective (NOT f)

Inverse:
  f invertible ⟺ f bijective
  f∘f⁻¹ = id_B,  f⁻¹∘f = id_A
  
  Left inverse exists ⟺ f injective
  Right inverse exists ⟺ f surjective
```

---

## 10. End-of-Lecture Exercises

1. Let $f(x)=x+2$, $g(x)=3x$, both $\mathbb{Z}\to\mathbb{Z}$. Compute $(g\circ f)(x)$ and $(f\circ g)(x)$. Are they equal?

2. Prove: if $f:A\to B$ and $g:B\to C$ are both bijective, then $(g\circ f)^{-1} = f^{-1}\circ g^{-1}$.
   *(Note the order reversal — this is important and often tested.)*

3. Determine whether each function is invertible. If yes, find the inverse. If no, explain why (injective failure, surjective failure, or both):
   - (a) $f:\mathbb{R}\to\mathbb{R}$, $f(x) = 5x-7$
   - (b) $f:\mathbb{R}\to\mathbb{R}$, $f(x) = x^3$
   - (c) $f:\mathbb{Z}\to\mathbb{Z}$, $f(x) = x+1$
   - (d) $f:\mathbb{R}\to[0,\infty)$, $f(x)=x^2$

4. Give an example of functions $f, g$ where $g\circ f$ is injective, but $g$ is not injective. (You may reuse the pattern from Section 2's worked counterexample, or construct your own.)

5. Prove: $\text{id}_A \circ f = f$ for any $f: B \to A$.

---

## Reading

- **Rosen, 8e §2.3** — Composition and inverse functions
- **Epp, 5e §7.2–7.3** — Inverse functions; composition of functions
- **Levin, 3e §0.4** — Functions

*Next: Lecture 17 — Bijections and Cardinality*
