# MATH 142 · Calculus II
## Problem Set 1 — Solutions
### INSTRUCTOR / TA COPY — not for distribution

---

**Total: 100 points.** Every antiderivative below was verified symbolically, and each was independently confirmed to match its standard textbook form.

> **Marking philosophy.** Parts A–C are craft, and craft is marked on method. **A correct answer with
> no stated $u$ and $dv$ earns at most half.** Conversely, a correct method with an arithmetic slip
> should keep most of its marks — the slip is not what the problem is teaching.
>
> **Award full credit for any correct alternative form.** Antiderivatives are unique only up to a
> constant, and several answers below have common variants that differ by one. If a student's answer
> differentiates to the integrand, it is right. Say so on the script.

---

## Part A — Single Application (5 pts each)

### A1 (5) — $\int x\cos x\,dx$

$u=x$, $dv=\cos x\,dx$; $du=dx$, $v=\sin x$:

$$= x\sin x - \int\sin x\,dx = \boxed{x\sin x + \cos x + C}$$

*Verified. **Check:** $\sin x + x\cos x - \sin x = x\cos x$ ✓*

*Marking: 2 for the choice, 2 for execution, 1 for $+C$. **The sign trap**: $-\int \sin x\,dx = +\cos x$.*

### A2 (5) — $\int x\ln x\,dx$

LIATE: **L** before **A**, so $u=\ln x$, $dv = x\,dx$; $du = \tfrac{dx}{x}$, $v=\tfrac{x^2}{2}$:

$$= \frac{x^2\ln x}{2} - \int\frac{x^2}{2}\cdot\frac1x\,dx = \frac{x^2\ln x}{2} - \frac12\int x\,dx = \boxed{\frac{x^2\ln x}{2} - \frac{x^2}{4}+C}$$

*Verified.*

*Marking: **2 of the 5 are for taking $u=\ln x$, not $u=x$.** The reverse choice needs $v=\int\ln x\,dx$, which is a harder problem than the original — students who went that way should be shown why LIATE puts L first.*

### A3 (5) — $\int\arcsin x\,dx$

One factor, so $dv = dx$: $u=\arcsin x$, $du = \frac{dx}{\sqrt{1-x^2}}$, $v=x$:

$$= x\arcsin x - \int\frac{x}{\sqrt{1-x^2}}\,dx$$

The remainder is a substitution, $w = 1-x^2$, $dw=-2x\,dx$:

$$\int\frac{x\,dx}{\sqrt{1-x^2}} = -\frac12\int w^{-1/2}dw = -\sqrt{w} = -\sqrt{1-x^2}$$

$$\boxed{\int\arcsin x\,dx = x\arcsin x + \sqrt{1-x^2} + C}$$

*Verified.*

*Marking: 2 for $dv=dx$, 2 for the substitution, 1 for the sign. **The double negative is the trap**: subtracting $-\sqrt{1-x^2}$ gives $+$.*

### A4 (5) — $\int_0^{\pi/2}x\cos x\,dx$

$$= \Big[x\sin x\Big]_0^{\pi/2} - \int_0^{\pi/2}\sin x\,dx = \frac\pi2 - \Big[-\cos x\Big]_0^{\pi/2} = \frac\pi2 - (0+1) = \boxed{\frac\pi2 - 1}$$

*Verified symbolically: $\pi/2 - 1 \approx 0.5708$.*

*Marking: 2 for the bracket evaluated at both limits, 3 for the rest. **A student who found the indefinite integral and then substituted gets full marks** — that is the legitimate alternative route.*

---

## Part B — Repeated, Circular, Reduction (6 pts each)

### B1 (6) — $\int x^2\cos x\,dx$

Two applications, $u$ the polynomial both times:

$$= x^2\sin x - 2\int x\sin x\,dx = x^2\sin x - 2\big(-x\cos x + \sin x\big)$$

$$= \boxed{x^2\sin x + 2x\cos x - 2\sin x + C}$$

*Verified.*

*Marking: 3 per application. **The $-2$ distributing over both terms** is where marks go; $x^2\sin x + 2x\cos x + 2\sin x$ (sign on the last term) is the common wrong answer and costs 2.*

### B2 (6) — $\int x^3e^{-x}\,dx$ by tabular integration

| sign | $u$ | $dv$ |
|:---:|---|---|
| $+$ | $x^3$ | $e^{-x}$ |
| $-$ | $3x^2$ | $-e^{-x}$ |
| $+$ | $6x$ | $e^{-x}$ |
| $-$ | $6$ | $-e^{-x}$ |
| | $0$ | $e^{-x}$ |

$$= -x^3e^{-x} - 3x^2e^{-x} - 6xe^{-x} - 6e^{-x} + C = \boxed{-(x^3+3x^2+6x+6)e^{-x}+C}$$

*Verified.*

*Marking: 2 for a correctly-built table, 4 for the result. **Every term is negative** — the alternating signs of the table and the alternating signs of $\int e^{-x}$ combine to give a uniform sign, which surprises students and is worth pointing out. **The table must be shown** (the problem asked); deduct 2 if only the answer appears.*

### B3 (6) — $\int e^{2x}\cos 3x\,dx$

Call it $I$. Take $u$ trigonometric both times.

$$I = \frac{e^{2x}\cos3x}{?}\ \ldots$$

Working it through (either order of $u$ works provided it is consistent):

$$I = \frac{e^{2x}\cos 3x}{2} + \frac32\int e^{2x}\sin 3x\,dx$$
$$\int e^{2x}\sin3x\,dx = \frac{e^{2x}\sin3x}{2} - \frac32 I$$

Substituting:

$$I = \frac{e^{2x}\cos3x}{2} + \frac{3e^{2x}\sin3x}{4} - \frac94 I \implies \frac{13}{4}I = \frac{e^{2x}(2\cos3x + 3\sin3x)}{4}$$

$$\boxed{I = \frac{e^{2x}\big(2\cos 3x + 3\sin 3x\big)}{13}+C}$$

*Verified symbolically — the CAS returns exactly $\frac{(3\sin 3x + 2\cos 3x)e^{2x}}{13}$.*

*Marking: 2 for reaching a circular equation, 2 for solving it, 2 for the coefficients. **The $13 = 2^2+3^2$ is not a coincidence** and is worth remarking on in class — for $\int e^{ax}\cos bx\,dx$ the denominator is always $a^2+b^2$. A student who noticed that deserves a comment.*

*This problem separates students who understood §3 of Lecture 2 from those who memorised the specific answer for $a=b=1$.*

### B4 (6) — $\int_0^1\arctan x\,dx$

From Lecture 1, $\int\arctan x\,dx = x\arctan x - \tfrac12\ln(1+x^2)$:

$$\Big[x\arctan x - \tfrac12\ln(1+x^2)\Big]_0^1 = \left(\frac\pi4 - \frac{\ln 2}{2}\right) - 0 = \boxed{\frac\pi4 - \frac{\ln2}{2}}\approx 0.4388$$

*Verified symbolically.*

*Marking: 3 for the antiderivative, 3 for the evaluation. $\arctan 1 = \pi/4$ must be right.*

### B5 (6) — $I_6$ by the reduction formula

$$I_6 = \frac56 I_4 = \frac56\cdot\frac34 I_2 = \frac56\cdot\frac34\cdot\frac12 I_0 = \frac{15}{48}\cdot\frac\pi2 = \frac{5}{16}\cdot\frac{\pi}{2} = \boxed{\frac{5\pi}{32}}$$

*Verified symbolically: $5\pi/32 \approx 0.4909$.*

**Second part:** $I_7$ is a **rational number**, not a multiple of $\pi$. Odd $n$ recurses down to the base case $I_1 = 1$, which is rational; $\pi$ enters only via $I_0 = \pi/2$, which only even $n$ reaches.

*(For reference: $I_7 = \tfrac{16}{35}$.)*

*Marking: 4 for the recursion shown step by step, 2 for the parity argument. **"Because the pattern alternates" earns 1** — the question asked why, and the answer is about which base case the recursion terminates on.*

---

## Part C — Trigonometric Integrals (6 pts each)

*Marking throughout: **1 point of the 6 is for naming the case** before computing. This is deliberate — the decision procedure is the content of the lecture.*

### C1 (6) — $\int\sin^5x\cos^2x\,dx$ — **$m$ odd**

$$= \int(\sin^2x)^2\cos^2x\cdot\sin x\,dx = \int(1-\cos^2x)^2\cos^2x\,\sin x\,dx$$

With $u = \cos x$, $du = -\sin x\,dx$:

$$= -\int(1-u^2)^2u^2\,du = -\int\big(u^2 - 2u^4 + u^6\big)du = -\frac{u^3}{3}+\frac{2u^5}{5}-\frac{u^7}{7}$$

$$\boxed{= -\frac{\cos^3x}{3}+\frac{2\cos^5x}{5}-\frac{\cos^7x}{7}+C}$$

*Verified: matches the CAS form exactly.*

### C2 (6) — $\int\cos^4x\,dx$ — **both even**

$$\cos^4 x = \left(\frac{1+\cos2x}{2}\right)^2 = \frac{1+2\cos2x+\cos^22x}{4}$$

Apply the identity again to $\cos^2 2x = \frac{1+\cos4x}{2}$:

$$= \frac14\left(1 + 2\cos 2x + \frac{1+\cos 4x}{2}\right) = \frac38 + \frac{\cos2x}{2}+\frac{\cos4x}{8}$$

$$\int\cos^4x\,dx = \boxed{\frac{3x}{8}+\frac{\sin2x}{4}+\frac{\sin4x}{32}+C}$$

*Verified.*

*Marking: **the double application of the half-angle identity is the difficulty** — students who apply it once and stop, leaving $\cos^2 2x$, should get 3. Accept the reduction-formula route for full marks.*

### C3 (6) — $\int\tan^5x\sec^3x\,dx$ — **$m$ odd**

$$= \int\tan^4x\,\sec^2x\cdot\sec x\tan x\,dx = \int(\sec^2x-1)^2\sec^2x\cdot\sec x\tan x\,dx$$

With $u=\sec x$:

$$= \int(u^2-1)^2u^2\,du = \int\big(u^6 - 2u^4 + u^2\big)du$$

$$\boxed{= \frac{\sec^7x}{7}-\frac{2\sec^5x}{5}+\frac{\sec^3x}{3}+C}$$

*Verified.*

*Marking: **note that $n=3$ is odd here, so Case A ($n$ even) is unavailable** — the student must spot that $m$ odd is the applicable case. Award the case-naming point only if they said which.*

### C4 (6) — $\int\sec^4x\,dx$ — **$n$ even**

$$= \int\sec^2x\cdot\sec^2x\,dx = \int(1+\tan^2x)\sec^2x\,dx \overset{u=\tan x}{=} \int(1+u^2)du$$

$$\boxed{= \tan x + \frac{\tan^3x}{3}+C}$$

*Verified.*

*Marking: straightforward; 6 for a clean solution. A student who reached for the $\int\sec^3$ formula has misread the exponent.*

### C5 (6) — $\int\sin4x\cos6x\,dx$ — **product-to-sum**

$$\sin4x\cos6x = \tfrac12\big[\sin(4x-6x)+\sin(4x+6x)\big] = \tfrac12\big[\sin10x - \sin2x\big]$$

*(using $\sin(-2x) = -\sin 2x$)*

$$\int = \frac12\left(-\frac{\cos10x}{10}+\frac{\cos2x}{2}\right) = \boxed{\frac{\cos2x}{4}-\frac{\cos10x}{20}+C}$$

*Verified: matches the CAS form exactly.*

*Marking: 2 for the identity, 2 for handling $\sin(-2x)$, 2 for the integration. **The odd-function step is the trap** — students who write $+\sin 2x$ get the sign of the first term wrong.*

---

## Part D — Orthogonality and Concept (10 pts each)

### D1 (10) — orthogonality

**(a)** $\sin2x\sin3x = \tfrac12[\cos(-x) - \cos5x] = \tfrac12[\cos x - \cos 5x]$.

$$\int_0^{2\pi}\tfrac12\big[\cos x - \cos5x\big]dx = \frac12\left[\sin x - \frac{\sin5x}{5}\right]_0^{2\pi} = \boxed{0}$$

Both terms are cosines of a nonzero integer multiple of $x$, each completing whole periods over $[0,2\pi]$.

*Verified symbolically: exactly 0.*

**(b)** $\sin^2 3x = \frac{1-\cos6x}{2}$:

$$\int_0^{2\pi}\frac{1-\cos6x}{2}dx = \frac12\left[x - \frac{\sin6x}{6}\right]_0^{2\pi} = \frac{2\pi}{2} = \boxed{\pi}$$

*Verified symbolically: exactly $\pi$.*

**(c)** Multiply $f$ by $\sin3x$ and integrate over $[0,2\pi]$:

$$\int_0^{2\pi}f(x)\sin3x\,dx = a_2\underbrace{\int\sin2x\sin3x}_{0} + a_3\underbrace{\int\sin^23x}_{\pi} + a_4\underbrace{\int\sin4x\sin3x}_{0} = a_3\pi$$

$$\boxed{a_3 = \frac1\pi\int_0^{2\pi}f(x)\sin(3x)\,dx}$$

The other coefficients vanish **because $\sin 2x$ and $\sin 4x$ are orthogonal to $\sin 3x$** — by (a), the integral of a product of sines of *different* integer frequencies over a full period is zero.

*Marking: 3 + 3 + 4. **Full marks on (c) require the word "orthogonal" or an explicit statement that the cross terms integrate to zero.** A student who wrote the formula without saying why the other terms die gets 2 of the 4.*

*This is the Fourier coefficient formula. Say so when returning the set — students should know they have just derived something they will use for the rest of their degree.*

### D2 (10) — why some integrals come back

**(a)** In $\int x^2e^x dx$ the factor $u=x^2$ is a **polynomial**: each differentiation lowers its degree, so after finitely many steps it becomes zero and the process terminates.

In $\int e^x\sin x\,dx$ **neither factor simplifies under differentiation.** $\sin x \to \cos x\to-\sin x$ cycles with period 4, and $e^x$ is unchanged. There is no descending quantity, so nothing forces termination — and after two steps the pair $(e^x, \sin x)$ has returned to its starting form.

**(b)** A third application simply repeats the second step's structure: it returns $\int e^x\cos x\,dx$ to $\int e^x \sin x\,dx$ again. The cycle has period 2 in the integrals, so odd numbers of applications land on the companion integral and even numbers on the original. **No number of applications terminates.**

**(c)** Take $I = \int e^x\sin x\,dx = e^x\sin x - \int e^x\cos x\,dx$ as before, then on the second application choose $u = e^x$, $dv = \cos x\,dx$:

$$\int e^x\cos x\,dx = e^x\sin x - \int e^x \sin x\,dx = e^x \sin x - I$$

Substituting back:

$$I = e^x\sin x - \big(e^x\sin x - I\big) = I$$

**The identity $I=I$** — true, useless. The second application exactly undid the first.

*Marking: 4 + 2 + 4. **(c) must show the algebra through to $I=I$**; asserting "it cancels" earns 1. This is the part that distinguishes understanding from recall.*

---

## Marking Summary

| Part | Points | Focus |
|---|---|---|
| A (4 × 5) | 20 | Parts, single application; choosing $u$ |
| B (5 × 6) | 30 | Repeated, tabular, circular, reduction |
| C (5 × 6) | 30 | The trigonometric decision procedure |
| D (2 × 10) | 20 | Orthogonality; why the method loops |
| **Total** | **100** | |

---

## Diagnostic Notes

| Question | Weakness it reveals | Bites in |
|---|---|---|
| **A2** | Choosing $u$ against LIATE | All of Weeks 1–2 |
| **B3** | Memorised the $a=b=1$ case rather than the method | Midterm 1 |
| **C3 / C4** | Cannot identify which parity case applies | Week 2 — trig substitution lands here |
| **D2(c)** | Followed the steps without understanding why they work | Week 2, and conceptually onward |

**If Part C scores are weak, act before Week 2 starts.** Trigonometric substitution converts algebraic integrals into exactly these, and a student who cannot finish a trigonometric integral will find next week's technique produces nothing but a harder problem.

---

*MATH 142 · Week 1 · PS 1 Solutions · Instructor Only*
