# MATH 142 · Calculus II
## Problem Set 3 — Solutions
### INSTRUCTOR / TA COPY — not for distribution

---

**Total: 100 points.** Every value below was verified symbolically; every comparison verdict was corroborated by numerical partial integrals.

> **Marking philosophy.** This set is about **hypotheses**, not computation. The arithmetic is the
> easiest of the course so far; the marks are in noticing that an integral is improper, writing the
> limit, and pointing an inequality the right way.
>
> **Deduct for a missing $\lim$ even when the number is right.** That is not pedantry: a student who
> writes $\big[-\tfrac1x\big]_1^\infty$ has not distinguished this week's material from Week 0's, and
> will produce $-2$ on D2 without noticing.

---

## Part A — Type I (5 pts each)

### A1 (5) — $\int_1^\infty\frac{dx}{x^3}$

$$= \lim_{T\to\infty}\left[-\frac{1}{2x^2}\right]_1^T = \lim_{T\to\infty}\left(\frac12 - \frac{1}{2T^2}\right) = \boxed{\frac12}$$

*Verified symbolically. Consistent with the $p$-test: $p=3>1$, value $\frac{1}{p-1}=\frac12$.*

*Marking: 1 for the limit notation, 3 for the antiderivative and evaluation, 1 for the value.*

### A2 (5) — $\int_0^\infty e^{-3x}\,dx$

$$= \lim_{T\to\infty}\left[-\frac{e^{-3x}}{3}\right]_0^T = \lim_{T\to\infty}\left(\frac13 - \frac{e^{-3T}}{3}\right) = \boxed{\frac13}$$

*Verified symbolically.*

*Marking: 5. **The $\frac13$ from the chain rule** is the only real risk.*

### A3 (5) — $\int_0^\infty xe^{-x^2}\,dx$

**Substitution, not parts.** $u=x^2$, $du=2x\,dx$:

$$= \lim_{T\to\infty}\left[-\frac{e^{-x^2}}{2}\right]_0^T = \frac12 \implies \boxed{\frac12}$$

*Verified symbolically.*

*Marking: 2 for choosing substitution over parts, 3 for the rest. **Students who reach for integration by parts (because of the $x$) will not finish** — $\int e^{-x^2}dx$ is not elementary, as Week 0 established. Worth a comment on any script that tried it: the presence of the $x$ is what makes the substitution work, and its absence is what makes the Gaussian impossible.*

### A4 (5) — $\int_2^\infty\frac{dx}{x^2-1}$

Partial fractions: $\dfrac{1}{(x-1)(x+1)} = \dfrac{1}{2(x-1)}-\dfrac{1}{2(x+1)}$.

$$\int_2^T = \frac12\Big[\ln|x-1|-\ln|x+1|\Big]_2^T = \frac12\left[\ln\frac{x-1}{x+1}\right]_2^T = \frac12\left(\ln\frac{T-1}{T+1} - \ln\frac13\right)$$

As $T\to\infty$, $\frac{T-1}{T+1}\to1$ so $\ln\frac{T-1}{T+1}\to0$:

$$= \frac12\ln 3 \approx \boxed{0.5493}$$

*Verified symbolically: $\frac{\ln 3}{2}$.*

**The requested explanation:** $\ln(T-1)$ and $\ln(T+1)$ each diverge, but their **difference** is $\ln\frac{T-1}{T+1}$, and the ratio tends to 1, so the difference tends to $\ln 1 = 0$. **Combining the logarithms before taking the limit is essential** — writing $\lim\ln(T-1) - \lim\ln(T+1)$ is $\infty-\infty$, which is meaningless.

*Marking: 3 for the computation, **2 for the explanation.** A student who combined the logs without comment gets the 3 but not the 2 — the problem asked why it works.*

*Worth flagging in class: this is the integral analogue of a **telescoping series**, which they meet in Week 7. Same structure, same resolution.*

---

## Part B — Type II (6 pts each)

### B1 (6) — $\int_0^1 x^{-1/3}dx$

$p=\tfrac13<1$, so it converges.

$$= \lim_{t\to0^+}\left[\frac{3x^{2/3}}{2}\right]_t^1 = \frac32 - 0 = \boxed{\frac32}$$

*Verified symbolically.*

*Marking: 2 for identifying that it is improper at 0, 1 for the limit, 3 for the value.*

> **Deduct the 2 if the student did not notice it was improper**, even with the right answer. The
> whole week is about noticing.

### B2 (6) — $\int_0^4\frac{dx}{\sqrt{4-x}}$

Singularity at the **right** endpoint.

$$= \lim_{t\to4^-}\Big[-2\sqrt{4-x}\Big]_0^t = \lim_{t\to4^-}\big(4 - 2\sqrt{4-t}\big) = \boxed{4}$$

*Verified symbolically.*

*Marking: 2 for locating the singularity at $x=4$, 4 for the evaluation.*

### B3 (6) — $\int_0^1 x\ln x\,dx$

Parts (Week 1): $u=\ln x$, $dv = x\,dx$ gives $\frac{x^2\ln x}{2}-\frac{x^2}{4}$.

$$= \lim_{t\to0^+}\left[\frac{x^2\ln x}{2}-\frac{x^2}{4}\right]_t^1 = \left(0-\frac14\right) - \lim_{t\to0^+}\left(\frac{t^2\ln t}{2}-\frac{t^2}{4}\right) = \boxed{-\frac14}$$

*Verified symbolically.*

**The justification requested:** $\lim_{t\to0^+}t^2\ln t = 0$. Write it as $\frac{\ln t}{t^{-2}}$, an $\frac{-\infty}{\infty}$ form; L'Hôpital gives $\frac{1/t}{-2t^{-3}} = -\frac{t^2}{2}\to0$.

*Marking: 3 for the integration, **3 for the limit justified.** Asserting "$t^2\ln t\to0$ because $t^2$ goes to zero faster" earns 1 — that is the right idea without the argument, and L'Hôpital was covered in MATH 141.*

### B4 (6) — $\int_{-1}^{1}x^{-2/3}dx$

**Interior singularity at $x=0$ — must split.** With the real cube root, $x^{2/3}=(\sqrt[3]x)^2\ge0$, so the integrand is positive on both sides.

$$= \int_{-1}^{0}x^{-2/3}dx + \int_0^1 x^{-2/3}dx$$

Each is a $p$-test at a singularity with $p=\tfrac23<1$ — **both converge**:

$$= \lim_{t\to0^-}\Big[3x^{1/3}\Big]_{-1}^{t} + \lim_{s\to0^+}\Big[3x^{1/3}\Big]_s^1 = \big(0-(-3)\big) + \big(3-0\big) = \boxed{6}$$

*Verified symbolically: each half is exactly 3, total 6.*

*Marking: **3 for splitting at 0**, 3 for the evaluation. A student who did not split but got 6 anyway (by luck, since the antiderivative happens to be continuous here) earns 3.*

### B5 (6) — $\int_0^2\frac{dx}{(x-1)^2}$

**Interior singularity at $x=1$.** Split:

$$\int_0^1\frac{dx}{(x-1)^2} + \int_1^2\frac{dx}{(x-1)^2}$$

Each is $p=2\ge1$ at a singularity — **each diverges**. For instance

$$\int_t^{1^-}\ \text{gives}\ \lim_{t\to1^-}\left(\frac{1}{1-t}-1\right) = \infty$$

**The integral diverges.**

*Verified symbolically: the CAS returns $\infty$.*

**The careless answer** would be $\big[-\frac{1}{x-1}\big]_0^2 = -1-1 = -2$ — negative, for a positive integrand. **Same trap as D2, same wrong number.**

*Marking: 3 for splitting, 3 for the correct verdict. **A student answering $-2$ scores 0** and should be sent straight to D2, which is the same problem with the diagnosis attached.*

---

## Part C — Comparison (6 pts each)

*Standard marking: 2 for the comparison function, 2 for verifying the inequality or the limit, 2 for the correct verdict with the $p$-test cited.*

### C1 (6) — $\int_1^\infty\frac{dx}{x^3+5}$ — **converges**

For $x\ge1$: $x^3+5>x^3$, so $0<\frac{1}{x^3+5}<\frac{1}{x^3}$. Since $\int_1^\infty x^{-3}dx$ converges ($p=3>1$), **so does ours**, with value $<\frac12$.

*Corroborated: partial integrals $0.222486,\ 0.2225364,\ 0.2225364,\ 0.2225364$ at $T=10^2,10^4,10^6,10^8$ — settled, and indeed below $0.5$.*

### C2 (6) — $\int_1^\infty\frac{2+\cos x}{\sqrt x}\,dx$ — **diverges**

$\cos x\ge-1$, so $2+\cos x\ge1$, giving $\frac{2+\cos x}{\sqrt x}\ge\frac{1}{\sqrt x}>0$. Since $\int_1^\infty x^{-1/2}dx$ diverges ($p=\tfrac12\le1$), **so does ours**.

*Corroborated: $35.4,\ 395.7,\ 4052,\ 40399$ — growing like $4\sqrt T$, exactly as an average numerator of 2 predicts.*

*Marking note: **this divergence is numerically obvious**, unlike $1/x$'s. Worth contrasting with Lab 3 Part C4.*

### C3 (6) — $\int_1^\infty\frac{x}{x^3+1}\,dx$ — **converges**

Limit comparison with $g=\frac{1}{x^2}$:

$$L = \lim_{x\to\infty}\frac{x/(x^3+1)}{1/x^2} = \lim_{x\to\infty}\frac{x^3}{x^3+1}=1$$

$0<L<\infty$ and $\int x^{-2}$ converges, **so ours converges**.

*Corroborated: $0.825649,\ 0.835549,\ 0.8356479,\ 0.8356488$ — settled.*

*Direct comparison also works here ($x^3+1>x^3$ gives $\frac{x}{x^3+1}<\frac{1}{x^2}$); accept either.*

### C4 (6) — $\int_2^\infty\frac{dx}{\sqrt{x^3-1}}$ — **converges**

**Direct comparison points the wrong way**: $x^3-1<x^3$ gives $\frac{1}{\sqrt{x^3-1}}>\frac{1}{x^{3/2}}$, which bounds *below* by a convergent integral — useless.

**Two valid fixes:**

- **Limit comparison** with $x^{-3/2}$: $L=\lim\sqrt{\frac{x^3}{x^3-1}}=1$, so same fate — converges.
- **Repair the direct comparison:** for $x\ge2$, $x^3-1\ge\frac{7}{8}x^3$, so $\frac{1}{\sqrt{x^3-1}}\le\sqrt{\frac87}\,x^{-3/2}$ — a convergent bound.

*Corroborated: $1.22753,\ 1.40753,\ 1.42553,\ 1.42733$ — settling near $1.4275$.*

*Marking: **the problem asked which route was used and why**, so 2 of the 6 are for stating that the naive direct comparison fails and why. A student who used limit comparison without noticing the issue earns 4.*

### C5 (6) — $\int_0^1\frac{\sin x}{x^{3/2}}\,dx$ — **converges**

**Type II**, singular at $x=0$. The standard fact is $\lim_{x\to0}\frac{\sin x}{x}=1$, so near 0 the integrand behaves like $\frac{x}{x^{3/2}} = x^{-1/2}$.

Limit comparison with $g(x)=x^{-1/2}$:

$$L=\lim_{x\to0^+}\frac{\sin x/x^{3/2}}{x^{-1/2}} = \lim_{x\to0^+}\frac{\sin x}{x} = 1$$

$\int_0^1x^{-1/2}dx=2$ converges ($p=\tfrac12<1$), **so ours converges.**

*Corroborated numerically: the value is $1.93515$.*

*Marking: 2 for recognising it as Type II, 2 for $\frac{\sin x}{x}\to1$, 2 for the verdict. **A student who compared at $\infty$ instead of at 0 has missed that the interval is $[0,1]$** — award 1.*

---

## Part D — Concept (10 pts each)

### D1 (10) — the two $p$-tests

**(a)** $\int_1^\infty x^{-p}$ converges $\iff p>1$. $\int_0^1x^{-p}$ converges $\iff p<1$.

**(b)** The two integrals ask opposite things of the function:

- **At infinity** the interval is unbounded, so the *only* way to accumulate finite area is for the integrand to shrink quickly enough that the tail contributes almost nothing. **A large $p$ helps.**
- **At a singularity** the interval is short but the function is unbounded, so finiteness requires the blow-up to be gentle enough that the spike is thin. **A large $p$ hurts.**

$p=2$ illustrates both: $\frac1{x^2}$ decays fast (good at $\infty$) and explodes violently (bad at 0).

**(c)** At $p=1$:

$$\int_1^T\frac{dx}{x} = \ln T \xrightarrow{T\to\infty}\infty \qquad\qquad \int_t^1\frac{dx}{x} = -\ln t \xrightarrow{t\to0^+}\infty$$

The failing functions are **$\ln T$** and **$-\ln t$** respectively. *(Verified: both diverge.)*

**(d)** $\int_0^\infty x^{-p}dx = \int_0^1 + \int_1^\infty$, and both pieces must converge. The first needs $p<1$; the second needs $p>1$. **No $p$ satisfies both, so it diverges for every $p$.**

*Marking: 2 + 4 + 2 + 2. **(b) is the discriminating part.** Restating the inequalities in words earns 1 of the 4; full marks require the shrink-fast/blow-up-slowly reasoning tied to why each is needed.*

### D2 (10) — the $-2$

**(a)** $\frac{1}{x^2}>0$ wherever it is defined, so its integral over any interval **cannot be negative.** No computation required.

**(b)** **FTC Part 2 requires $f$ to be continuous on the closed interval $[a,b]$.** Here $f(x)=x^{-2}$ is not merely discontinuous at $0$ — it is **undefined** there, and unbounded near it. The hypothesis fails, so the conclusion carries no force.

*(Worth stating explicitly: the theorem was not "wrong". It was not applicable.)*

**(c)** Split at the singularity:

$$\int_{-1}^{1}\frac{dx}{x^2} = \int_{-1}^{0}\frac{dx}{x^2}+\int_0^1\frac{dx}{x^2}$$

$$\int_s^1\frac{dx}{x^2} = \left[-\frac1x\right]_s^1 = \frac1s - 1\xrightarrow{s\to0^+}\infty$$

so the right half diverges (as does the left, by symmetry). **The integral diverges.**

*Verified: the CAS returns $\infty$.*

**(d)** The correct construction requires a **sign-changing** integrand. The cleanest example:

$$\int_{-1}^{2}\frac{dx}{x^3}\ \overset{\text{carelessly}}{=}\ \left[-\frac{1}{2x^2}\right]_{-1}^{2} = -\frac18 - \left(-\frac12\right) = \boxed{+\frac38} = 0.375$$

**This is positive, and nothing about it looks wrong.** The integrand is negative on $[-1,0)$ and positive on $(0,2]$, and the interval is longer on the positive side — so a modest positive answer is exactly what a student would expect. **The sign check gives no warning at all.**

The true integral **diverges**: $\int_{-1}^{0}x^{-3}dx = -\infty$ and $\int_0^2 x^{-3}dx = +\infty$.

*Verified: the careless value is exactly $\frac38$; each half diverges, and a CAS asked for the whole thing returns `nan` — correctly refusing to evaluate $\infty-\infty$.*

### Why the original trap was detectable, and this one is not

This is worth making explicit, because it sharpens the moral:

**For a positive integrand, the careless method essentially always returns a negative number.** $F$ is increasing on each side of the singularity, and across it $F$ drops from $+\infty$ to $-\infty$, so $F(b)-F(a)$ picks up that drop. Checked on four cases:

| careless evaluation | result |
|---|---|
| $\int_{-1}^{1}x^{-2}dx$ | $-2$ |
| $\int_{-1}^{3}x^{-2}dx$ | $-\tfrac43$ |
| $\int_0^3(x-1)^{-2}dx$ | $-\tfrac32$ |
| $\int_{-2}^{1}x^{-4}dx$ | $-\tfrac38$ |

**All negative — so the sign check always fires.** It is precisely when the integrand changes sign that the check is unavailable, and that is exactly the case constructed above.

> **The moral:** the $-2$ was detectable only because the integrand was positive, which made an
> impossible sign available as a warning. **That warning is a lucky accident of the example, not a
> method.** The defence is not "check whether the answer looks odd" — it is **check the hypotheses
> before applying the theorem**, every time.

*Marking: 2 + 3 + 3 + 2. **(d) is marked on the moral, not on the example.** Accept any construction that yields a plausible wrong answer — a student who produces $0$ from $\int_{-1}^{1}x^{-3}dx$ (where the two boundary terms cancel and symmetry makes $0$ look *very* convincing) has found an even better example and should be told so. A valid example with no conclusion drawn earns 1 of the 2.*

---

## Marking Summary

| Part | Points | Focus |
|---|---|---|
| A (4 × 5) | 20 | Type I; setting up the limit |
| B (5 × 6) | 30 | Type II; endpoint and interior singularities |
| C (5 × 6) | 30 | Direct and limit comparison |
| D (2 × 10) | 20 | The $p$-tests; a diagnostic error |
| **Total** | **100** | |

---

## Diagnostic Notes

| Question | Weakness it reveals | Bites in |
|---|---|---|
| **B4 / B5 / D2** | Not checking for singularities | Midterm 1; and permanently |
| **C4** | Using a comparison that points the wrong way | Weeks 7–8, constantly |
| **D1(b)** | Memorised two inequalities instead of one reason | Week 7 ($p$-series) |
| **A4** | Taking limits of pieces instead of the combination | Week 7 (telescoping series) |

**Midterm 1 is Wednesday 3 March (Week 6).** This set plus Week 4 completes its syllabus. The single most valuable revision instruction to give the class: **for every integral on the exam, look at it before computing** — is it improper, is the fraction proper, is there symmetry. Three of the four failure modes above are failures to look.

---

*MATH 142 · Week 3 · PS 3 Solutions · Instructor Only*
