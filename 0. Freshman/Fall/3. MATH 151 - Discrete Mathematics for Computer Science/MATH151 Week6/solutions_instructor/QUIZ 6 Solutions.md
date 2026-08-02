# MATH 151 — Week 6
## Quiz 6 Solutions — INSTRUCTOR ONLY

---

### Problem 1 (6 points) — $f(x)=4x-5$, $\mathbb{Z}\to\mathbb{Z}$

**(a)** (3 pts) **Injective — PROVE.**

**Proof.** Let $a_1,a_2\in\mathbb{Z}$ be arbitrary. Assume $f(a_1)=f(a_2)$.
$4a_1-5=4a_2-5 \Rightarrow 4a_1=4a_2 \Rightarrow a_1=a_2$.
Since arbitrary, $f$ is injective. ∎

**(b)** (3 pts) **NOT surjective — DISPROVE.**

**Disproof.** Take $y=0$. Need $4x-5=0\Rightarrow x=5/4\notin\mathbb{Z}$. No integer preimage. $f$ is not surjective. ∎

*Grading: 3 pts each — 1 for correct claim (injective/not surjective), 2 for correct proof/disproof mechanics.*

---

### Problem 2 (5 points)

**(a)** (2 pts) $(g\circ f)(x)=g(f(x))=g(x+2)=3(x+2)=3x+6$

**(b)** (2 pts) $(f\circ g)(x)=f(g(x))=f(3x)=3x+2$

**(c)** (1 pt) NOT equal: $3x+6\neq3x+2$ for any $x$ (differ by constant 4). Composition is not commutative here (or in general).

---

### Problem 3 (5 points) — $f(x)=4x-5$, $\mathbb{R}\to\mathbb{R}$

**Invertible.** (Linear function, nonzero slope, domain/codomain both $\mathbb{R}$ — bijective.)

$y=4x-5\Rightarrow x=(y+5)/4$

$f^{-1}(y)=(y+5)/4$

**Verify:** $f^{-1}(f(x))=f^{-1}(4x-5)=\dfrac{(4x-5)+5}{4}=\dfrac{4x}{4}=x$ ✓

*Grading: 1 pt for correctly identifying invertibility. 3 pts for correct algebra deriving $f^{-1}$. 1 pt for verification.*

---

### Problem 4 (4 points)

**Pigeons:** the 13 chosen integers. **Pigeonholes:** the 12 pairs summing to 25 from $\{1,\ldots,24\}$: $\{1,24\},\{2,23\},\ldots,\{12,13\}$.

**Proof.** Partition $\{1,\ldots,24\}$ into 12 pairs each summing to 25. With 13 integers chosen (pigeons) and 12 pairs (pigeonholes), $13>12$ ⟹ two chosen integers fall into the same pair ⟹ their sum is 25. ∎

*Grading: 1 pt for correctly identifying pigeons. 1 pt for correctly constructing the 12 pigeonhole pairs. 2 pts for correctly stated conclusion with valid counting ($13>12$).*

---

### Grade Distribution

| Score | Interpretation |
|---|---|
| 18–20 | Mastered functions and Pigeonhole |
| 14–17 | Solid; review composition order and inverse algebra |
| 10–13 | Re-read Lectures 5.1–5.3; redo PS5 |
| < 10 | Schedule office hours before Week 6 |
