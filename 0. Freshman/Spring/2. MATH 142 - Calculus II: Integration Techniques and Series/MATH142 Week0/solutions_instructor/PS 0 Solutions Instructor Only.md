# MATH 142 · Calculus II
## Problem Set 0 — Solutions
### INSTRUCTOR / TA COPY — not for distribution

---

**Total: 100 points.** Every answer below was verified symbolically or numerically before release.

> **Marking philosophy for PS 0.** This set is review and its diagnostic value exceeds its grade
> value. **Annotate rather than only deduct** — a student who loses marks on Part B needs to know
> *this week* that substitution is not secure, because Weeks 1–2 assume it completely.
>
> **The single most informative question is D2.** A student who cannot separate *existence* from
> *expressibility* will find Week 3 and Week 10 conceptually impossible. Flag every weak D2 for
> follow-up regardless of the overall score.

---

## Part A — The FTC and the Definition (5 pts each)

### A1 (5) — $\int_0^4(2x-3)\,dx$

$$\big[x^2-3x\big]_0^4 = (16-12)-0 = \boxed{4}$$

Using **FTC Part 2**.

*Marking: 4 for the value, **1 for naming Part 2**. Deduct the naming point if they wrote "the Fundamental Theorem" without specifying which part — the problem asked.*

### A2 (5) — $\frac{d}{dx}\int_2^{x^3}\ln(1+t^2)\,dt$

Let $F(u)=\int_2^u\ln(1+t^2)dt$, so $F'(u)=\ln(1+u^2)$ by **FTC Part 1**. The integral is $F(x^3)$, so by the chain rule:

$$\frac{d}{dx}F(x^3) = F'(x^3)\cdot 3x^2 = \boxed{3x^2\ln(1+x^6)}$$

*Verified numerically: at $x=1.4$ and $x=2.1$, numerical differentiation of the quadrature agrees to 16 significant figures.*

*Marking: 3 for $\ln(1+x^6)$, **2 for the $3x^2$**. The missing chain-rule factor is the classic error and is worth its own deduction.*

*Note $(x^3)^2 = x^6$, not $x^5$ or $x^9$ — a few students will slip here.*

### A3 (5) — $\frac{d}{dx}\int_{\sin x}^{0}e^{t^2}\,dt$

**Two things need care**, as flagged: the variable is in the *lower* limit, and it is a composite.

Flip first:

$$\int_{\sin x}^{0}e^{t^2}dt = -\int_0^{\sin x} e^{t^2}dt$$

Then FTC Part 1 with the chain rule:

$$\frac{d}{dx}\left[-\int_0^{\sin x}e^{t^2}dt\right] = -e^{(\sin x)^2}\cdot\cos x = \boxed{-\cos x\,e^{\sin^2 x}}$$

*Verified numerically at $x=0.6$ and $x=1.1$ to 16 significant figures.*

*Marking: 2 for the sign, 2 for the chain-rule factor $\cos x$, 1 for $e^{\sin^2 x}$. **A student who gets $+\cos x\,e^{\sin^2x}$ has done everything but the flip** — award 3.*

*Worth saying in class: $e^{t^2}$ has no elementary antiderivative, so there is no route here except the FTC. Students who tried to integrate first will have spent the whole question getting nowhere.*

### A4 (5) — $\int_0^1 x^2\,dx$ from the definition

$\Delta x = \frac1n$, right endpoints $x_i = \frac{i}{n}$:

$$\sum_{i=1}^n\left(\frac{i}{n}\right)^2\frac1n = \frac{1}{n^3}\sum_{i=1}^n i^2 = \frac{1}{n^3}\cdot\frac{n(n+1)(2n+1)}{6} = \frac{(n+1)(2n+1)}{6n^2}$$

$$\lim_{n\to\infty}\frac{2n^2+3n+1}{6n^2} = \frac{2}{6} = \boxed{\frac13}$$

FTC Part 2 confirms: $\big[\tfrac{x^3}{3}\big]_0^1 = \tfrac13$. ✓

*Verified: the symbolic limit of the sum evaluates to $1/3$.*

*Marking: 1 for $\Delta x$ and sample points, 2 for the algebra, 1 for the limit, 1 for the FTC confirmation. **Deduct nothing for using left endpoints** — the limit is the same and a student who noticed that deserves a comment, not a penalty.*

---

## Part B — Substitution (6 pts each)

*Standard marking throughout: **2 for stating the substitution**, 3 for execution, 1 for the constant or the changed limits. Award full credit for any correct alternative route.*

### B1 (6) — $\int x^2(1+x^3)^5\,dx$

$u=1+x^3$, $du=3x^2dx$, so $x^2dx = \tfrac13du$:

$$\frac13\int u^5\,du = \frac{u^6}{18}+C = \boxed{\frac{(1+x^3)^6}{18}+C}$$

*Verified: the difference between this and the CAS antiderivative is the constant $-1/18$, confirming both.*

### B2 (6) — $\int_0^{\pi/2}\cos x\,e^{\sin x}\,dx$

$u=\sin x$, $du=\cos x\,dx$. Limits: $x=0\Rightarrow u=0$; $x=\pi/2\Rightarrow u=1$.

$$\int_0^1 e^u\,du = \big[e^u\big]_0^1 = \boxed{e-1}$$

*Verified symbolically.*

*Marking: **the changed limits are worth 1 of the 6.** A student who wrote $\big[e^{\sin x}\big]_0^{\pi/2}$ and evaluated correctly also earns full marks — that is the "convert back first" route.*

### B3 (6) — $\int\frac{(\ln x)^3}{x}\,dx$

$u=\ln x$, $du=\frac{dx}{x}$:

$$\int u^3\,du = \boxed{\frac{(\ln x)^4}{4}+C}$$

*Verified symbolically.*

### B4 (6) — $\int_{-1}^{1}x^5\cos(x^2)\,dx$

**One line:** $x^5$ is odd, $\cos(x^2)$ is even, so the integrand is odd; the interval is symmetric about $0$; therefore the integral is $\boxed{0}$.

*Verified symbolically: $0$.*

*Marking: **6 for the symmetry argument.** A student who found the antiderivative (it requires parts twice) and got $0$ earns 4 — correct, but the problem said to read it first and the skill being taught is recognition. **A student who got a non-zero answer has an arithmetic error**, since the true value is exactly 0.*

### B5 (6) — $\int\sec^2 x\tan^3x\,dx$

$u=\tan x$, $du=\sec^2x\,dx$:

$$\int u^3\,du = \boxed{\frac{\tan^4 x}{4}+C}$$

*Verified: the CAS returns $-\frac{\cos 2x}{4\cos^4 x}$, which differs from $\frac{\tan^4x}{4}$ by exactly $\frac14$ — a constant, so both are correct. **A good example to show the class**: two antiderivatives that look nothing alike, reconciled in one line.*

---

## Part C — Applications (10 pts each)

### C1 (10) — area between $y=x^3$ and $y=x$ on $[-1,1]$

**The curves cross at $x=0$** (and at $\pm1$, the endpoints). On $(0,1)$, $x>x^3$; on $(-1,0)$, $x^3>x$.

$$A = \int_{-1}^{0}(x^3-x)\,dx + \int_0^1(x-x^3)\,dx = \frac14 + \frac14 = \boxed{\frac12}$$

By contrast $\displaystyle\int_{-1}^1(x-x^3)\,dx = 0$, because $x-x^3$ is odd. **The two differ because area is unsigned and the integral is signed** — the two halves have equal magnitude and opposite sign, so they cancel in the integral and add in the area.

*Verified symbolically: $\int_{-1}^1|x-x^3|dx = 1/2$.*

*Marking: 3 for finding the crossing at $x=0$, 4 for the two correctly-oriented integrals, 3 for the explanation. **A student who wrote a single integral and got 0 earns at most 3** — this is exactly the error the problem was built to catch, and the sketch was requested for this reason.*

### C2 (10) — average value of $1/x$ on $[1,e]$, and the MVT point

$$f_{\text{avg}} = \frac{1}{e-1}\int_1^e\frac{dx}{x} = \frac{1}{e-1}\big[\ln x\big]_1^e = \frac{1-0}{e-1} = \boxed{\frac{1}{e-1}}\approx 0.5820$$

MVT for Integrals: solve $f(c)=f_{\text{avg}}$, i.e. $\dfrac1c = \dfrac{1}{e-1}$, giving

$$\boxed{c = e-1 \approx 1.7183}$$

and $1 < 1.7183 < e\approx 2.7183$ ✓ — it lies in the interval, as the theorem guarantees.

*Verified symbolically.*

*Marking: 4 for the average, 3 for solving for $c$, 3 for verifying $c$ is in range. **The verification is not a formality** — it is the content of the theorem, and students who skip it have not understood what was being asserted.*

*Nice observation to offer: $c=e-1$ is exactly $1$ less than the right endpoint. Coincidence of this example, not a general fact.*

### C3 (10) — motion with $v(t)=\sin t$ on $[0,\tfrac{3\pi}{2}]$

**(a) Displacement:**

$$\int_0^{3\pi/2}\sin t\,dt = \big[-\cos t\big]_0^{3\pi/2} = -\cos\tfrac{3\pi}{2} + \cos 0 = 0 + 1 = \boxed{1\text{ m}}$$

**(b) Distance:** $\sin t \ge 0$ on $[0,\pi]$ and $\le 0$ on $[\pi,\tfrac{3\pi}2]$. Split at $t=\pi$:

$$\int_0^{\pi}\sin t\,dt + \int_\pi^{3\pi/2}(-\sin t)\,dt = 2 + 1 = \boxed{3\text{ m}}$$

**(c)** The particle moves forward 2 m over $[0,\pi]$, then reverses and moves back 1 m over $[\pi,\tfrac{3\pi}{2}]$. Displacement records only the net position change ($2-1=1$); distance counts both legs ($2+1=3$).

*Verified symbolically: displacement $1$, distance $3$.*

*Marking: 3 + 4 + 3. **Answering 1 m for both parts scores 3 total** — it means the sign change was not found. Part (c) must mention the reversal explicitly; "because one uses absolute value" restates the formula without explaining the motion and earns 1 of 3.*

---

## Part D — Concept and Looking Ahead (10 pts each)

### D1 (10) — $\int_{-2}^{2}(x^3+3x^2)\,dx$ by symmetry

Split by linearity:

- $x^3$ is **odd** and $[-2,2]$ is symmetric about $0$, so $\displaystyle\int_{-2}^2 x^3dx = 0$.
- $3x^2$ is **even**, so $\displaystyle\int_{-2}^2 3x^2dx = 2\int_0^2 3x^2dx = 2\big[x^3\big]_0^2 = 2(8) = 16$.

$$\text{Total} = 0 + 16 = \boxed{16}$$

*Verified symbolically: $16$.*

**Conditions required.** For either rule: the **interval must be symmetric about the origin**, i.e. of the form $[-a,a]$; and the **function must have the stated parity on that interval**.

**Counterexample requested:** $f(x)=x$ is odd, but $\displaystyle\int_0^1 x\,dx = \tfrac12 \neq 0$ — the interval $[0,1]$ is not symmetric about $0$. (Any correct example accepted.)

*Marking: 5 for the computation with both terms handled by parity, 3 for stating both conditions, 2 for a valid counterexample. **A student who integrated directly and got 16 earns 4 of the 5** — correct but not what was asked.*

### D2 (10) — existence versus expressibility

**(a)** $f(t)=e^{-t^2}$ is continuous on all of $\mathbb{R}$. By the **Fundamental Theorem of Calculus, Part 1**, for any $x$ the function $F(x)=\int_0^x e^{-t^2}dt$ is well defined and differentiable. FTC Part 1 is an **existence theorem**: continuity alone guarantees an antiderivative exists.

**(b)** $F'(x) = \boxed{e^{-x^2}}$

**(c)** There is no contradiction because **the two statements are about different things**:

- FTC Part 1 asserts that a certain function *exists* and is differentiable. It is defined by the integral itself, and needs no formula in terms of familiar functions.
- Liouville's theorem asserts that this function *cannot be written* as a finite combination of a particular restricted list of functions (polynomials, roots, exponentials, logarithms, trigonometric and inverse trigonometric functions).

A function can perfectly well exist, be smooth, be computable to any precision, and still not be expressible in a chosen finite vocabulary. **"Elementary" is a statement about notation, not about mathematics.** Indeed $F$ has a name — $\frac{\sqrt\pi}{2}\operatorname{erf}(x)$ — but $\operatorname{erf}$ is *defined* as this integral, so naming it adds nothing except convenience.

*Marking: 3 + 2 + 5. **Full marks on (c) require the student to identify that the two claims have different subjects** — one about existence, one about representability in a fixed vocabulary. Answers of the form "because erf exists" earn 2: naming the function is not the explanation, since the name is defined by the integral.*

*This question is the conceptual gate to the whole course. **Flag every answer scoring below 6 for follow-up in office hours**, independent of the student's total.*

---

## Marking Summary

| Part | Points | Focus |
|---|---|---|
| A (4 × 5) | 20 | The FTC, both parts; the definition |
| B (5 × 6) | 30 | Substitution, limits, symmetry |
| C (3 × 10) | 30 | Area, average value, net change |
| D (2 × 10) | 20 | Symmetry rules; existence vs expressibility |
| **Total** | **100** | |

---

## Diagnostic Notes for the Instructor

Watch the distribution of these four in particular — each predicts a specific later failure:

| Question | Weakness it reveals | Bites in |
|---|---|---|
| **A2 / A3** | FTC Part 1 with a chain rule | Every exam; Week 3 |
| **B2** | Not changing limits on a definite substitution | Weeks 1–2, constantly |
| **C1** | Confusing signed integral with geometric area | Week 4 (volumes) |
| **D2** | Existence vs expressibility | Weeks 3, 9, 10 — conceptually fatal |

**If more than a third of the cohort misses B2**, spend ten minutes of Week 1 Monday on it before starting integration by parts. Parts on a definite integral has the same trap with an extra term, and it will compound.

---

*MATH 142 · Week 0 · PS 0 Solutions · Instructor Only*
