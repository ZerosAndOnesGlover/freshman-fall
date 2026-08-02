# MATH 151 · Week 5
## LAB5 Solutions — INSTRUCTOR ONLY

---

## Section 1 Solutions

### Exercise 1.1

**(a)** $f(n)=n^3$, $\mathbb{Z}\to\mathbb{Z}$.
**Injective:** Assume $a_1^3=a_2^3$. Since cube is strictly increasing over $\mathbb{R}$ (hence over $\mathbb{Z}$), $a_1=a_2$. Injective.
**Surjective:** Take $y=2$. Need $x^3=2$; no integer solution. NOT surjective.
**Classification: Injective only.**

**(b)** $f(x)=e^x$, $\mathbb{R}\to\mathbb{R}$.
**Injective:** $e^x$ strictly increasing ⟹ injective. ✓
**Surjective:** Range of $e^x$ is $(0,\infty)$, not all of $\mathbb{R}$. Take $y=-1$: no $x$ with $e^x=-1$. NOT surjective.
**Classification: Injective only.**

**(c)** $f(n)=n\bmod 3$, $\mathbb{Z}\to\mathbb{Z}$ (codomain declared as all of ℤ, though outputs only ever land in {0,1,2}).
**Injective:** $f(0)=0=f(3)$, but $0\neq3$. NOT injective.
**Surjective:** Take $y=5$. No integer has $n\bmod3=5$ (remainders are only 0,1,2). NOT surjective.
**Classification: Neither.**

**(d)** $f:\{1,2,3,4,5\}\to\{1,2,3,4,5\}$, given as a table: this is a permutation (bijection) — each of 1-5 appears exactly once as output (3,1,4,2,5 — check: yes, all distinct and covering {1,...,5}).
**Classification: Bijective.**

**(e)** $f(m,n)=(n,m)$, $\mathbb{Z}\times\mathbb{Z}\to\mathbb{Z}\times\mathbb{Z}$.
**Injective:** Assume $f(m_1,n_1)=f(m_2,n_2)$: $(n_1,m_1)=(n_2,m_2)$, so $n_1=n_2$ and $m_1=m_2$, i.e., $(m_1,n_1)=(m_2,n_2)$. Injective.
**Surjective:** Given $(a,b)$, take $(m,n)=(b,a)$: $f(b,a)=(a,b)$. Surjective.
**Classification: Bijective** (it's its own inverse — a "swap" function).

**(f)** Piecewise $f(x)=x+1$ if $x\geq0$, $x-1$ if $x<0$, $\mathbb{R}\to\mathbb{R}$.
**Injective:** If both $\geq0$: $a_1+1=a_2+1\Rightarrow a_1=a_2$. If both $<0$: similarly. If mixed signs: $a_1+1\geq1$ (positive branch) while $a_2-1<-1$ (negative branch) — ranges don't overlap, so equality is impossible across branches. Injective.
**Surjective:** For $y\geq1$: take $x=y-1\geq0$, $f(x)=y$. For $y<-1$: take $x=y+1<0$, $f(x)=y$. But what about $y\in[-1,1)$? E.g. $y=0$: need $x\geq0$ with $x+1=0\Rightarrow x=-1$, not $\geq0$. Or $x<0$ with $x-1=0\Rightarrow x=1$, not $<0$. No valid $x$. NOT surjective — the interval $[-1,1)$ is unreachable (a "gap").
**Classification: Injective only.**

---

## Section 2 Solutions

### Exercise 2.1

**(a)** $(f\circ g)(x) = f(g(x)) = f(2x) = 2x+3$.
$(g\circ f)(x) = g(f(x)) = g(x+3) = 2(x+3) = 2x+6$.

**(b)** $(f\circ g)(5) = 2(5)+3=13$. Step-by-step: $g(5)=10$, $f(10)=13$. Match ✓.
$(g\circ f)(5) = 2(5)+6=16$. Step-by-step: $f(5)=8$, $g(8)=16$. Match ✓.

**(c)** NOT equal: $2x+3 \neq 2x+6$ (differ by constant 3 for all $x$).

---

### Exercise 2.2

**(a)** $f(x)=-3x+5$: bijective (linear, nonzero slope). $y=-3x+5\Rightarrow x=(5-y)/3$.
$f^{-1}(y)=(5-y)/3$. Verify: $f^{-1}(f(x))=(5-(-3x+5))/3=(3x)/3=x$ ✓.

**(b)** $f(x)=x^3+1$: bijective over ℝ (cube is bijective on ℝ, shifted by 1 preserves bijectivity). $y=x^3+1\Rightarrow x=\sqrt[3]{y-1}$.
$f^{-1}(y)=\sqrt[3]{y-1}$. Verify: $f^{-1}(f(x))=\sqrt[3]{(x^3+1)-1}=\sqrt[3]{x^3}=x$ ✓.

**(c)** $f(x)=\ln(x)$, $(0,\infty)\to\mathbb{R}$: bijective (standard fact). $f^{-1}(y)=e^y$.
Verify: $f^{-1}(f(x))=e^{\ln x}=x$ ✓ (for $x>0$).

**(d)** $f(x)=2x+1$, $\mathbb{Z}\to\mathbb{Z}$: injective (linear, nonzero slope) but NOT surjective — take $y=0$: $2x+1=0\Rightarrow x=-1/2\notin\mathbb{Z}$. NOT invertible as a function $\mathbb{Z}\to\mathbb{Z}$ (though it would be invertible as $\mathbb{R}\to\mathbb{R}$).

---

### Exercise 2.3

$f(x)=2x$, $g(x)=x+1$, $h(x)=x^2$.

**(a)** $(h\circ g\circ f)(x) = h(g(f(x))) = h(g(2x)) = h(2x+1) = (2x+1)^2 = 4x^2+4x+1$

**(b)** $(f\circ g\circ h)(x) = f(g(h(x))) = f(g(x^2)) = f(x^2+1) = 2(x^2+1) = 2x^2+2$

**(c)** NOT equal: $4x^2+4x+1 \neq 2x^2+2$ in general (e.g., at $x=1$: $4+4+1=9$ vs $2+2=4$). Confirms order matters severely in composition chains.

**(d)** $h\circ(g\circ f)$: $(g\circ f)(x)=g(2x)=2x+1$. $h(2x+1)=(2x+1)^2=4x^2+4x+1$.
$(h\circ g)\circ f$: $(h\circ g)(x)=h(x+1)=(x+1)^2$. Applied to $f(x)=2x$: $(2x+1)^2=4x^2+4x+1$.
Both give $4x^2+4x+1$ — confirms associativity. ✓

---


## Section 4 — Python Expected Outputs

### Exercise 4.1

```
x^2: NEITHER (over domain/codomain [-10,10])
x+5 (correct codomain): BIJECTIVE
|x|: SURJECTIVE ONLY (not injective)
x^3 (correct codomain): BIJECTIVE
```

**Discrepancy discussion:** Over the truncated finite domain $\{-10,\ldots,10\}$:
- $x^2$: still not injective (pairs like $\pm1,\pm2,$ etc. collide) — matches infinite-domain analysis.
- $|x|$: still surjective onto $\{0,\ldots,10\}$ but not injective — matches.
- $x+5$ and $x^3$: bijective on the finite truncation when codomain is defined as the actual image — this matches infinite-domain behavior since these are injective functions with codomain set to match their range exactly.

Discrepancies would arise if the codomain were declared differently — e.g., $x^3$ over domain $\{-10,\ldots,10\}$ with codomain $\mathbb{Z}$ (infinite) would fail surjectivity even though it's injective, since most integers aren't perfect cubes.

### Exercise 4.2

For $f(x)=6-x$ on $\{1,\ldots,5\}$: `inv = {5:1, 4:2, 3:3, 2:4, 1:5}` (dictionary mapping output back to input).

For the Exercise 1.1(d) permutation (1→3,2→1,3→4,4→2,5→5): inverse should map 3→1, 1→2, 4→3, 2→4, 5→5.


## Section 5 — Reflection Model Answers

1. Functions like $x^3$ and $x+5$ don't change classification between infinite and finite-truncated domains IF the codomain is correspondingly restricted to match the actual range. Discrepancies arise specifically when the codomain is declared as a larger infinite set (like all of $\mathbb{Z}$) while the domain is finite — surjectivity necessarily fails in that mismatch since a finite domain can only produce finitely many outputs, never covering an infinite codomain.

2. `len(set(outputs)) == len(outputs)` tests injectivity because converting a list to a `set` automatically removes duplicates. If the list of outputs has no duplicates, converting to a set doesn't shrink it — lengths match, confirming every input produced a DISTINCT output, which is exactly the definition of injective.

