# MATH 151 · Week 5
## PS5 Solutions — INSTRUCTOR ONLY

---

> *Revised 2026-09-28: cut from 13 problems (about 27 parts) to 8 problems with 16 parts. New → old: A1 = A1 (a–c), 9 · A2 = A2 (b, d), 12 ·
> B1 = B1 (a, b, e, g), 20 · C1 = C1 (a, b), 10 · C2 = C2, 12 · C3 = C3 (b, c), 12 · C4 = C4, 13 · D1 = D1, 12. D2–D5 are no longer asked.*


## Part A

### A1.

**(a)** Valid function. Every element of $\{1,2,3,4\}$ appears exactly once as first coordinate: 1→a, 2→b, 3→a, 4→c. Totality ✓, well-definedness ✓.

**(b)** NOT a function. Well-definedness fails: element 1 maps to both $a$ and $b$.

**(c)** NOT a function. Totality fails: element 3 has no image.

**(d)** NOT a function from $\mathbb{R}$ to $\mathbb{R}$. Totality fails: $f(0)=1/0$ is undefined — 0 has no image. (It IS a valid function from $\mathbb{R}-\{0\}$ to $\mathbb{R}$.)

---

### A2. $f(x)=x^2-4x+3$

**(a)** Complete the square: $f(x)=(x-2)^2-1$. Since $(x-2)^2\geq0$ for all real $x$, $f(x)\geq-1$, with equality at $x=2$. As $x\to\pm\infty$, $f(x)\to\infty$. Range = $[-1,\infty)$.

**(b)** NOT injective. Disproof: $f(0)=3$ and $f(4)=16-16+3=3$. So $f(0)=f(4)=3$ with $0\neq4$.

**(c)** NOT surjective (onto $\mathbb{R}$). Disproof: take $y=-2$. We'd need $(x-2)^2-1=-2$, i.e., $(x-2)^2=-1$, impossible for real $x$. So $-2$ has no preimage.

**(d)** Restricting to $[2,\infty)$: NOW injective.

**Proof.** Let $a_1,a_2\in[2,\infty)$ with $f(a_1)=f(a_2)$.
$(a_1-2)^2-1=(a_2-2)^2-1 \Rightarrow (a_1-2)^2=(a_2-2)^2$.
Since $a_1,a_2\geq2$, both $a_1-2\geq0$ and $a_2-2\geq0$. Taking (non-negative) square roots: $a_1-2=a_2-2$, so $a_1=a_2$. ∎

---

## Part B

### B1(a): $f(x)=-2x+7$, $\mathbb{Z}\to\mathbb{Z}$

**Injective:** Assume $f(a_1)=f(a_2)$: $-2a_1+7=-2a_2+7 \Rightarrow a_1=a_2$. Injective. ✓

**Surjective:** Take $y=0$. Need $-2x+7=0\Rightarrow x=3.5\notin\mathbb{Z}$. Not surjective.

**Classification: Injective only.**

---

### B1(b): $f(x)=|x|$, $\mathbb{Z}\to\mathbb{N}$

**Injective:** $f(1)=1=f(-1)$, but $1\neq-1$. NOT injective.

**Surjective:** Let $n\in\mathbb{N}$ be arbitrary. Take $x=n\in\mathbb{Z}$. Then $f(n)=|n|=n$ (since $n\geq0$). Surjective. ✓

**Classification: Surjective only.**

---

### B1(c): $f(x)=1/(x^2+1)$, $\mathbb{R}\to\mathbb{R}$

**Injective:** $f(1)=1/2=f(-1)$, but $1\neq-1$. NOT injective.

**Surjective:** Range is $(0,1]$ (since $x^2+1\geq1$, so $0<f(x)\leq1$). Take $y=2\in\mathbb{R}$: no $x$ gives $f(x)=2$ since $f(x)\leq1$ always. NOT surjective.

**Classification: Neither.**

---

### B1(d): $f(m,n)=m-n$, $\mathbb{Z}\times\mathbb{Z}\to\mathbb{Z}$

**Injective:** $f(1,0)=1=f(2,1)$, but $(1,0)\neq(2,1)$. NOT injective.

**Surjective:** Let $k\in\mathbb{Z}$ be arbitrary. Take $(m,n)=(k,0)$. $f(k,0)=k-0=k$. Surjective. ✓

**Classification: Surjective only.**

---

### B1(e): $f(n)=n^2$, $\mathbb{Z}^+\to\mathbb{Z}^+$

**Injective:** Assume $f(a_1)=f(a_2)$: $a_1^2=a_2^2$. Since $a_1,a_2\in\mathbb{Z}^+$ (both positive), taking positive square roots: $a_1=a_2$. Injective. ✓

**Surjective:** Take $y=2$. Need $x^2=2$, $x=\sqrt2\notin\mathbb{Z}^+$. NOT surjective.

**Classification: Injective only.**

---

### B1(f): $f(S)=\overline{S}$ on $\mathcal{P}(\{1,2,3\})$

**Injective:** Assume $f(S_1)=f(S_2)$: $\overline{S_1}=\overline{S_2}$. Taking complements of both sides: $S_1=S_2$. Injective. ✓

**Surjective:** Let $T\in\mathcal{P}(\{1,2,3\})$ be arbitrary. Take $S=\overline{T}$. Then $f(S)=\overline{\overline{T}}=T$. Surjective. ✓

**Classification: Bijective.** (Makes sense: complementation is its own inverse.)

---

### B1(g): Piecewise $f(n)=n+1$ if even, $n-1$ if odd, $\mathbb{Z}\to\mathbb{Z}$

**Injective:** Suppose $f(a_1)=f(a_2)$.

If $a_1,a_2$ both even: $a_1+1=a_2+1\Rightarrow a_1=a_2$.
If $a_1,a_2$ both odd: $a_1-1=a_2-1\Rightarrow a_1=a_2$.
If $a_1$ even, $a_2$ odd: $a_1+1$ is odd, $a_2-1$ is even. These can't be equal (different parities) — contradiction, so this case can't occur if $f(a_1)=f(a_2)$.

So in all valid cases $a_1=a_2$. Injective. ✓

**Surjective:** Let $y\in\mathbb{Z}$ be arbitrary.
If $y$ is odd: take $x=y-1$ (even). $f(x)=x+1=y-1+1=y$. ✓
If $y$ is even: take $x=y+1$ (odd). $f(x)=x-1=y+1-1=y$. ✓

Surjective. ✓

**Classification: Bijective.** (This function swaps each even number with the next odd number and vice versa — e.g., $0\leftrightarrow1$, $2\leftrightarrow3$, etc. — a classic bijection.)

---

## Part C

### C1. $f(x)=2x-1$, $g(x)=x^2$

**(a)** $(g\circ f)(x) = g(f(x)) = g(2x-1) = (2x-1)^2 = 4x^2-4x+1$

**(b)** $(f\circ g)(x) = f(g(x)) = f(x^2) = 2x^2-1$

**(c)** $(g\circ f)(3)$:
(i) Directly: $4(9)-4(3)+1=36-12+1=25$
(ii) Step-by-step: $f(3)=2(3)-1=5$. $g(5)=25$.
Match: 25=25. ✓

---

### C2. Is $g\circ f$ necessarily non-injective if $f$ injective but $g$ not?

**Answer: NOT necessarily. $g\circ f$ CAN still be injective.**

**Counterexample:** Let $A=\{1,2\}$, $B=\{1,2,3\}$, $C=\{1,2\}$.

$f:A\to B$, $f(1)=1,f(2)=2$ (injective).
$g:B\to C$, $g(1)=1,g(2)=2,g(3)=1$ (NOT injective — $g(1)=g(3)=1$).

$(g\circ f)(1)=g(1)=1$. $(g\circ f)(2)=g(2)=2$.

Since $1\neq2$ maps to distinct values, $g\circ f$ IS injective — despite $g$ not being injective (the non-injective behavior of $g$ only matters for element $3$, which is never in the range of $f$).

**Conclusion:** $f$ injective alone does not force $g\circ f$ to be non-injective; $g$'s failure of injectivity outside the range of $f$ is invisible to the composition. ∎

---

### C3. Invertibility

**(a)** $f(x)=7x+2$: Bijective (linear, nonzero slope, over $\mathbb{R}$). $y=7x+2\Rightarrow x=(y-2)/7$.
$f^{-1}(y)=(y-2)/7$. Verify: $f^{-1}(f(x))=(7x+2-2)/7=x$ ✓. $f(f^{-1}(y))=7\cdot\frac{y-2}{7}+2=(y-2)+2=y$ ✓.

**(b)** $f(x)=1/x$ over $\mathbb{R}-\{0\}\to\mathbb{R}-\{0\}$: Bijective (its own inverse). $y=1/x\Rightarrow x=1/y$.
$f^{-1}(y)=1/y$. Verify: $f^{-1}(f(x))=1/(1/x)=x$ ✓.

**(c)** $f(x)=x^2$ over $[0,\infty)\to[0,\infty)$: Bijective on this restricted domain (injective since both non-negative; surjective since every non-negative $y$ has $\sqrt y\geq0$ as preimage).
$f^{-1}(y)=\sqrt y$. Verify: $f^{-1}(f(x))=\sqrt{x^2}=|x|=x$ (since $x\geq0$) ✓.

**(d)** $f(x)=3x$, $\mathbb{Z}\to\mathbb{Z}$: NOT invertible over these sets.
Injective: yes ($3a_1=3a_2\Rightarrow a_1=a_2$). Surjective: NO — take $y=1$, need $3x=1\Rightarrow x=1/3\notin\mathbb{Z}$. Since not surjective, not bijective, hence NOT invertible (as a function $\mathbb{Z}\to\mathbb{Z}$).

---

### C4. $(g\circ f)^{-1}=f^{-1}\circ g^{-1}$

**Proof.** Since $f,g$ bijective, $g\circ f$ is bijective (shown in Thursday's lecture), so $(g\circ f)^{-1}$ exists. We verify $f^{-1}\circ g^{-1}$ satisfies the defining property of the inverse.

Check $(f^{-1}\circ g^{-1})\circ(g\circ f) = \text{id}_A$:

$(f^{-1}\circ g^{-1})\circ(g\circ f) = f^{-1}\circ(g^{-1}\circ g)\circ f$ [associativity]
$= f^{-1}\circ\text{id}_B\circ f$ [since $g^{-1}\circ g=\text{id}_B$]
$= f^{-1}\circ f$ [identity property]
$= \text{id}_A$ ✓

Check $(g\circ f)\circ(f^{-1}\circ g^{-1}) = \text{id}_C$:

$(g\circ f)\circ(f^{-1}\circ g^{-1}) = g\circ(f\circ f^{-1})\circ g^{-1}$
$= g\circ\text{id}_B\circ g^{-1} = g\circ g^{-1} = \text{id}_C$ ✓

Since $f^{-1}\circ g^{-1}$ satisfies both defining equations, $(g\circ f)^{-1}=f^{-1}\circ g^{-1}$. ∎

---


---

## Part D — Bijections and Cardinality

### D1. Bijection $\mathbb{N} \to$ perfect squares *(6 pts)*

$f(n) = (n+1)^2$, giving $0\mapsto1,\; 1\mapsto4,\; 2\mapsto9,\; 3\mapsto16,\; 4\mapsto25,\; 5\mapsto36$.

**Injective.** If $(m+1)^2 = (n+1)^2$ with $m,n \geq 0$ then $m+1, n+1 > 0$, so taking positive
square roots gives $m+1 = n+1$, hence $m = n$.

**Surjective.** Every perfect square of a positive integer is $k^2$ for some $k \geq 1$, and
$f(k-1) = k^2$.

**On sparsity:** the gap between consecutive squares is $(n+1)^2 - n^2 = 2n+1$, which grows without
bound — the squares have density zero in $\mathbb{N}$. Countability is unaffected, because it asks
only whether the elements can be *listed*, not how densely they sit. **Density and cardinality are
different questions**, and this is the cleanest example of the difference.

*Marking: 2 injective, 2 surjective, 2 for the sparsity comment. Students who answer $f(n)=n^2$ on
$\mathbb{N}$ including 0 are also correct if their codomain includes 0.*

---

### D2. Union of two countable sets *(6 pts)*

Let $A = \{a_0, a_1, \ldots\}$ and $B = \{b_0, b_1, \ldots\}$ be countable. Interleave:

$$a_0,\, b_0,\, a_1,\, b_1,\, a_2,\, b_2,\, \ldots$$

Every element of $A \cup B$ appears: $a_n$ at position $2n$, $b_n$ at position $2n+1$. So the
listing is surjective onto $A\cup B$, and every element has a **finite** position.

**Duplicates.** If $A$ and $B$ overlap, the list repeats elements. Delete each repeat on its second
appearance; a listing with items deleted is still a listing. (Formally: a surjection
$\mathbb{N} \to S$ with $S$ infinite yields a bijection by discarding repeats.)

**If either set is finite,** exhaust it and continue with the tail of the other.

*Marking: 3 for the interleaving, 2 for handling duplicates, 1 for the finite case. Answers that
concatenate — all of $A$, then all of $B$ — earn 1: nothing in $B$ would ever be reached.*

---

### D3. The Cantor pairing function *(6 pts)*

**(a)** $\pi(3,4) = \dfrac{7 \cdot 8}{2} + 4 = 28 + 4 = \mathbf{32}$;
$\pi(4,3) = \dfrac{7 \cdot 8}{2} + 3 = 28 + 3 = \mathbf{31}$.

Both pairs lie on the **same anti-diagonal** $x + y = 7$, so both get the same base offset
$\frac{7\cdot8}{2} = 28$. Position *within* the diagonal is given by $y$, and $(4,3)$ has the
smaller $y$, so it comes first. The function is not symmetric, and it should not be — $(3,4)$ and
$(4,3)$ are different pairs and must receive different indices.

**(b)** Find the diagonal first: we need $d$ with $\frac{d(d+1)}{2} \le 14 < \frac{(d+1)(d+2)}{2}$.
Since $\frac{4\cdot5}{2} = 10 \le 14 < 15 = \frac{5\cdot6}{2}$, we have $d = 4$.
Then $y = 14 - 10 = 4$ and $x = d - y = 0$, giving $(x,y) = \mathbf{(0,4)}$.

Check: $\pi(0,4) = \frac{4\cdot5}{2} + 4 = 10 + 4 = 14$ ✓

*(All values verified computationally.)*

*Marking: 2 for (a)'s values, 2 for the same-diagonal explanation, 2 for (b). The diagonal-first
method is what makes (b) tractable; trial and error also earns full marks if the answer is right.*

---

### D4. A bijection $(0,1) \to \mathbb{R}$ *(5 pts)*

$$f(x) = \tan\!\left(\pi\left(x - \tfrac12\right)\right)$$

As $x$ runs over $(0,1)$, the argument $\pi(x - \frac12)$ runs over $(-\frac{\pi}{2}, \frac{\pi}{2})$,
on which $\tan$ is continuous and strictly increasing from $-\infty$ to $+\infty$. Strictly
increasing ⟹ injective; the range is all of $\mathbb{R}$ ⟹ surjective.

The inverse is $f^{-1}(y) = \dfrac{\arctan y}{\pi} + \dfrac12$. Verified: the round trip
$f^{-1}(f(x))$ returns $x$ exactly for $x = 0.1, 0.25, 0.5, 0.75, 0.9$, and
$f(0.25) = -1$, $f(0.5) = 0$, $f(0.75) = 1$.

*A rational alternative also works:* $g(x) = \dfrac{2x-1}{x(1-x)}$, giving
$g(0.25) = -2.667$, $g(0.5) = 0$, $g(0.75) = 2.667$.

**On "length":** the interval $(0,1)$ has length 1 and $\mathbb{R}$ has infinite length, yet they
have the **same cardinality**. Length (measure) and cardinality are independent notions of size —
a bijection preserves neither distance nor length, only the pairing.

*Marking: 3 for a correct bijection with justification, 2 for the length observation.*

---

### D5. Finite subsets vs the full power set *(5 pts)*

**Finite subsets of $\mathbb{N}$ are countable.** Group them by their maximum element (with
$\emptyset$ first). For each $n$, the subsets with maximum $n$ are subsets of $\{0,\ldots,n\}$
containing $n$ — there are exactly $2^{n}$ of them, a **finite** block. Listing block $0$, then
block $1$, then block $2$, … reaches every finite subset at a finite position.

**$\mathcal{P}(\mathbb{N})$ is not countable.** The same grouping fails: an **infinite** subset has
no maximum element, so it belongs to no block and is never listed. And no other listing works either
— by diagonalisation, given any list $S_0, S_1, S_2, \ldots$ of subsets, the set
$D = \{n : n \notin S_n\}$ differs from every $S_n$ (at the element $n$), so it is missing.

**Where the argument turns:** the listing method needs the elements to be sorted into **finitely
many finitely-sized blocks**. Finite subsets admit such a decomposition; arbitrary subsets do not,
because "infinite subset" is not reachable by any finite-block scheme.

*Marking: 2 for the finite-subset listing, 2 for why it fails on $\mathcal{P}(\mathbb{N})$, 1 for
naming diagonalisation. Students who only assert "Cantor's theorem" without engaging with the
listing get 2 of 5 — the question asks *where* the argument breaks.*
