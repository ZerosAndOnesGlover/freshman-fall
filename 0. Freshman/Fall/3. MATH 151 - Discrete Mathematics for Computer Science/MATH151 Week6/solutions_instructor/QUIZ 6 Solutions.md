# MATH 151 · Week 6
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

**(a)** **No.** Lecture 15 §7: if $f:A\to B$ is injective then $|A|\le|B|$. Here $|A|=4>3=|B|$, so no function
$A\to B$ is injective (some two inputs must share an output).

*Grading: 1 pt for "no", 1 pt for citing $|A|\le|B|$ (or the equivalent "4 distinct outputs need 4 elements").*

**(b)** For example $f(1)=a,\ f(2)=b,\ f(3)=c,\ f(4)=a$. Every element of $B$ is hit, so $f$ is **surjective**; it is
**not injective** since $f(1)=f(4)$ — as (a) says it must be.

*Grading: 1 pt for a valid surjection, 1 pt for "not injective" with the witness pair. Do not require or reward
the phrase "Pigeonhole Principle" — that name is taught in Week 8.*

---

### Grade Distribution

| Score | Interpretation |
|---|---|
| 18–20 | Mastered functions |
| 14–17 | Solid; review composition order and inverse algebra |
| 10–13 | Re-read Lectures 5.1–5.3; redo PS5 |
| < 10 | Schedule office hours before Week 6 |
