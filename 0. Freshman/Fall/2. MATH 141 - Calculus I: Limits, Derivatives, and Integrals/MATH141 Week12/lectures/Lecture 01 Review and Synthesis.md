# MATH 141 — Calculus I
## Week 12 · Lecture 1 (Monday)
### Review and Synthesis

---

## The Course in One Diagram

Twelve weeks, and underneath them **one structure**:

$$\text{limits} \;\longrightarrow\; \text{derivatives} \;\longleftrightarrow\; \text{integrals}$$

The arrow to the right is definition — both derivative and integral are limits. The double arrow is
the **Fundamental Theorem**: they are inverse operations.

Everything else is technique or application.

---

## 1. The Three Pillars

### Limits (Weeks 1–2)

The ε-δ definition made "approaches" precise, and everything after depends on it.

| Concept | Statement |
|---|---|
| $\lim_{x\to a}f(x)=L$ | For every $\varepsilon>0$ there is $\delta>0$ with $0<\lvert x-a\rvert<\delta \Rightarrow \lvert f(x)-L\rvert<\varepsilon$ |
| Continuity | $\lim_{x\to a}f(x)=f(a)$ — all three parts |
| Discontinuity types | Removable, jump, infinite, essential |
| IVT | Continuous $f$ on $[a,b]$ hits every value between $f(a)$ and $f(b)$ |

**Why it needed to be rigorous:** the IVT is *false over $\mathbb{Q}$* — $x^2-2$ on $[1,2]$ has no
rational root. Completeness of $\mathbb{R}$, not geometry, is what makes calculus work.

### Derivatives (Weeks 3–7)

| Concept | Statement |
|---|---|
| Definition | $f'(x)=\lim_{h\to0}\dfrac{f(x+h)-f(x)}{h}$ |
| Differentiable ⟹ continuous | **Converse false** — $\lvert x\rvert$, $x^{2/3}$, $x^{1/3}$ |
| Rules | Power, product, quotient, chain |
| Implicit differentiation | Differentiate both sides, solve for $dy/dx$ |
| MVT | Some $c$ with $f'(c)=\dfrac{f(b)-f(a)}{b-a}$ |
| $f'$ sign | Increasing / decreasing |
| $f''$ sign | Concave up / down |

### Integrals (Weeks 8–11)

| Concept | Statement |
|---|---|
| Definition | $\int_a^b f=\lim_{n\to\infty}\sum f(x_i^*)\Delta x$ |
| **FTC Part 1** | $\dfrac{d}{dx}\displaystyle\int_a^x f = f(x)$ |
| **FTC Part 2** | $\displaystyle\int_a^b f = F(b)-F(a)$ |
| Techniques | Substitution, by parts |
| Applications | Area, volume, work, average value |

---

## 2. Six Threads That Ran Through Everything

**1. Signed versus absolute.** The same distinction, four times:

| Signed | Absolute |
|---|---|
| $\int_a^b f$ | area |
| $\int v\,dt$ = displacement | $\int\lvert v\rvert dt$ = distance |
| $\int(f-g)$ | $\int\lvert f-g\rvert$ = area between curves |

Each time, the fix is the same: **split where the sign changes**. Verified consequence: not
splitting gave $0$ instead of $0.8284$ for the area between $\sin$ and $\cos$.

**2. The MVT is everywhere.** It proves that $f'=0$ implies constant (Week 6), which proves FTC
Part 2 (Week 9), which is why the $+C$ cancels.

**3. Existence versus computation.** The IVT guarantees a root without locating it; FTC Part 1
guarantees an antiderivative exists for $e^{-x^2}$ even though no elementary formula does. **Knowing
something exists is a separate question from finding it.**

**4. Local versus global.** $f'(c)=0$ is local information; the MVT and the Extreme Value Theorem
convert it into global conclusions.

**5. Slice, approximate, sum, limit.** Every application in Weeks 8–11 is this one construction.

**6. Symmetry first.** Checking whether an integrand is odd on a symmetric interval takes a second
and can end the problem.

---

## 3. The Errors That Cost Most Marks

| Error | Correction |
|---|---|
| $\lim=\infty$ means the limit exists | It **does not exist**; it fails in a describable way |
| Continuous ⟹ differentiable | **False** — the converse holds, not this |
| Forgetting the chain rule's inner factor | $\frac{d}{dx}f(g) = f'(g)\cdot g'$ |
| $(fg)'=f'g'$ | Two terms: $f'g+fg'$ |
| "Speeding up because $a>0$" | Compare the **signs** of $v$ and $a$ |
| Applying the FTC across a discontinuity | $\int_{-1}^1 x^{-2}$ "$=-2$" is nonsense |
| One integral across a crossing | Split — verified to give $0$ otherwise |
| $\int(R_o-R_i)^2$ for a washer | Square **first**: $\int(R_o^2-R_i^2)$ — off by 5× |
| Forgetting to change limits after substituting | Or substitute back before evaluating |
| Distance = displacement | Only when $v$ never changes sign |

---

## 4. Verified Numbers Worth Carrying

| | |
|---|---|
| Root of $x^3-x-2$ on $[1,2]$ | $1.521379706805$ |
| Bisection to $10^{-6}$ on $[1,2]$ | **20** iterations |
| $\lvert x\rvert$ at $0$ | One-sided slopes $\pm1$ — corner |
| $x^{2/3}$ at $0$ | $\pm\infty$, opposite signs — cusp |
| $x^{1/3}$ at $0$ | $+\infty$ both sides — vertical tangent |
| $\int_0^{2\pi}\sin$ vs $\int_0^{2\pi}\lvert\sin\rvert$ | $0$ vs $4$ |
| $\int_0^1 e^{-x^2}$ | $0.7468241328$ — no elementary antiderivative |
| Sphere by disks | $\tfrac43\pi R^3$ |
| $y=x^2$ on $[0,2]$ about $y$-axis | $8\pi$, by shells **and** washers |

---

## Summary

| Thread | |
|---|---|
| The structure | limits → derivatives ↔ integrals, joined by the FTC |
| Signed vs absolute | Split where the sign changes — four instances |
| The MVT | Underwrites Week 6 *and* FTC Part 2 |
| Existence vs computation | IVT and FTC Part 1 both promise without providing |
| Slice → approximate → sum → limit | Every application, one construction |
| Symmetry | Check it first; it can end the problem |

---

## Lecture 1 Exercises

**1.** State both parts of the FTC and explain in one sentence how each is used.

**2.** Give a function that is (a) continuous but not differentiable at a point, (b) differentiable
everywhere but with a discontinuous derivative.

**3.** Explain why $\int_a^b v\,dt$ and $\int_a^b\lvert v\rvert dt$ differ, and give a $v$ on $[0,3]$
for which they do.

**4.** Name three theorems from this course that guarantee something *exists* without saying where
it is.

### Answers

**1. Part 1:** $\dfrac{d}{dx}\int_a^x f(t)dt=f(x)$ — used to **differentiate accumulation
functions** and to guarantee an antiderivative exists.

**Part 2:** $\int_a^b f=F(b)-F(a)$ — used to **evaluate** definite integrals without limits of sums.

*Part 1 is the theoretical half (integration undoes differentiation); Part 2 is the computational
half.*

**2. (a)** $\lvert x\rvert$ at $0$ — continuous, but the one-sided derivatives are $+1$ and $-1$.
*(Also $x^{2/3}$, $x^{1/3}$.)*

**(b)** $f(x)=x^2\sin(1/x)$ with $f(0)=0$ — differentiable everywhere with $f'(0)=0$, but
$f'(x)=2x\sin(1/x)-\cos(1/x)$ has no limit at $0$. Verified: $f'$ equals $-1$ at $x=1/(k\pi)$ for
arbitrarily large $k$.

**3.** $\int v\,dt$ is **signed** — intervals where $v<0$ subtract — so it gives net **displacement**.
$\int\lvert v\rvert dt$ counts every interval positively, giving **total distance**. They agree only
when $v$ never changes sign.

**Example:** $v(t)=t-2$ on $[0,3]$.

$$\int_0^3(t-2)dt=\left[\tfrac{t^2}{2}-2t\right]_0^3=\tfrac92-6=-\tfrac32$$

$$\int_0^3\lvert t-2\rvert dt=\int_0^2(2-t)dt+\int_2^3(t-2)dt=2+\tfrac12=\tfrac52$$

Displacement $-\tfrac32$, distance $\tfrac52$.

**4.** Any three of:

- **IVT** (Week 2) — a root exists in $(a,b)$; says nothing about where.
- **MVT** (Week 6) — some $c$ has $f'(c)$ equal to the secant slope; does not locate $c$.
- **Extreme Value Theorem** (Week 6) — a continuous function on $[a,b]$ attains a max and min.
- **MVT for integrals** (Week 8) — $f$ attains its average value somewhere.
- **FTC Part 1** (Week 9) — an antiderivative exists, even when no elementary formula does.

*The pattern is worth naming: existence theorems are usually proved by completeness or continuity
arguments that are inherently non-constructive. Bisection (Week 2) is the exception — its proof
**is** an algorithm.*

---

*Next: Tuesday — Taylor Polynomials: A Preview*
