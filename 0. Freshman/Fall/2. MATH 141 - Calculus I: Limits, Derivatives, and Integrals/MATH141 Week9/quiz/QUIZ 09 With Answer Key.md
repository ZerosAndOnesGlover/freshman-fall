# MATH 141 — Quiz 09
## Administered: start of Week 9, Monday
### Covers: Week 8 — Riemann sums, the definite integral, and its properties

**Duration:** 15 minutes · Closed book · **20 points**

---

## Section A — Short Answer (2 pts each)

**A1.** Write the definition of $\int_a^b f(x)\,dx$ as a limit of Riemann sums, defining every symbol.

**A2.** Compute the right-endpoint Riemann sum for $f(x)=x^2$ on $[0,2]$ with $n=4$.

**A3.** Given $\int_0^3 f = 7$ and $\int_0^5 f = 2$, find $\int_3^5 f$.

**A4.** State what $\int_a^b f$ means when $f$ is negative on part of $[a,b]$.

**A5.** Why is $\int_b^a f = -\int_a^b f$ a *definition* rather than a theorem?

---

## Section B — Longer (5 pts each)

**B1.** Use the comparison property to show $\displaystyle 2 \le \int_0^2 \sqrt{1+x^3}\,dx \le 6$.

**B2.** Evaluate $\displaystyle\int_{-3}^{3}\sqrt{9-x^2}\,dx$ geometrically, and explain why no Riemann
sum computation is needed.

---

**Total: 20 points**

---

## Answer Key (Instructor Copy)

**A1.** $\displaystyle\int_a^b f(x)\,dx=\lim_{n\to\infty}\sum_{i=1}^{n}f(x_i^*)\,\Delta x$, where
$\Delta x=\frac{b-a}{n}$ and $x_i^*$ is any sample point in the $i$-th subinterval.

*1 pt for the sum, 1 for $\Delta x$. Full marks require noting the limit exists **independent of the
sample points** when $f$ is continuous — that independence is what makes the definition well posed.*

**A2.** $\Delta x=0.5$; right endpoints $0.5,1,1.5,2$:

$$0.5\big(0.25+1+2.25+4\big)=0.5(7.5)=\mathbf{3.75}$$

*(True value $\tfrac83\approx2.6667$ — the right sum overestimates because $x^2$ is increasing.
Award 1 bonus-worthy note if the student says so.)*

**A3.** Additivity: $\int_0^5=\int_0^3+\int_3^5$, so $\int_3^5 f = 2-7=\mathbf{-5}$.

**A4.** It is the **signed** (net) area: area above the axis counts positive, area below counts
negative. It is not the geometric area unless $f\ge0$ throughout.

**A5.** Riemann sums are built with $\Delta x=\frac{b-a}{n}$, which presumes $a<b$; the definition
says nothing about reversed limits. We *choose* the orientation convention because it makes
additivity $\int_a^b+\int_b^c=\int_a^c$ hold for **all** orderings of $a,b,c$ instead of only
$a<b<c$. A convention chosen to preserve a theorem is still a convention.

*Students who answer "because it's negative area" have missed the question — that is a consequence,
not a reason. 2 of 2 only with the additivity point.*

**B1.** On $[0,2]$, $x^3$ ranges over $[0,8]$, so $\sqrt{1+x^3}$ ranges over $[1,3]$.

The comparison property $m(b-a)\le\int_a^b f\le M(b-a)$ with $m=1$, $M=3$, $b-a=2$ gives

$$1\cdot2 = 2 \;\le\; \int_0^2\sqrt{1+x^3}\,dx \;\le\; 3\cdot 2 = 6 \quad\checkmark$$

*(Verified numerically: the integral is $3.2413$ — inside the bracket, and closer to the top, since
$\sqrt{1+x^3}$ spends most of $[0,2]$ near its maximum.)*

**Marking:** 2 for finding $m$ and $M$ correctly, 2 for the comparison property, 1 for the arithmetic.

**B2.** $y=\sqrt{9-x^2}$ is the **upper half** of the circle $x^2+y^2=9$ of radius 3. The integral
over $[-3,3]$ is therefore the area of a semicircle:

$$\frac{1}{2}\pi(3)^2=\frac{9\pi}{2}\approx\mathbf{14.1372}$$

No Riemann sum is needed because the integral was *defined* to be the area under the curve for
$f\ge0$, and this area is already known from geometry. The definition is what licenses the shortcut.

*(Verified numerically: $14.13716694$.)*

**Marking:** 2 for identifying the semicircle, 2 for the area, 1 for the explanation. Students who
try to antidifferentiate get 0 for method — that requires trigonometric substitution, which is not
until MATH 151.

---

*MATH 141 · Week 9 · Quiz 09 · © CSE Department*
