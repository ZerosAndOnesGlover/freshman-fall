# MATH 141 — Calculus I
## Week 10 Reference Sheet
### Substitution Rule · Symmetry · Integration by Parts

---

## The Substitution Rule

$$\int f(g(x))g'(x)\,dx = \int f(u)\,du \quad\text{where } u=g(x),\ du=g'(x)\,dx$$

**Procedure:** choose $u$ → compute $du$ → rewrite entirely in $u$ → integrate → substitute back.

**For definite integrals (preferred method):** convert the limits too —
$$\int_a^b f(g(x))g'(x)\,dx = \int_{g(a)}^{g(b)}f(u)\,du$$
(then no need to substitute back)

### Pattern Recognition Guide

| Pattern | Try |
|---------|-----|
| $f(g(x))\cdot g'(x)$ | $u=g(x)$ |
| Power of an expression × its derivative | $u=$ the base expression |
| $\dfrac{g'(x)}{g(x)}$ | $u=g(x)$ → gives $\ln|u|$ |
| Trig of linear expression $ax+b$ | $u=ax+b$ |

---

## Symmetry Shortcuts

$$f \text{ even } (f(-x)=f(x)): \quad \int_{-a}^a f(x)\,dx = 2\int_0^a f(x)\,dx$$

$$f \text{ odd } (f(-x)=-f(x)): \quad \int_{-a}^a f(x)\,dx = 0$$

**Useful general identity:** $\displaystyle\int_0^a f(x)\,dx = \int_0^a f(a-x)\,dx$ (substitute $u=a-x$)

---

## Integration by Parts

$$\int u\,dv = uv - \int v\,du$$

**Derivation:** integrate the Product Rule $\dfrac{d}{dx}[uv]=u'v+uv'$.

### LIATE — Choosing $u$ (in priority order)

$$\textbf{L}\text{ogarithmic} > \textbf{I}\text{nverse trig} > \textbf{A}\text{lgebraic} > \textbf{T}\text{rigonometric} > \textbf{E}\text{xponential}$$

Choose $u$ = whichever type appears **earliest** in this list; the rest (with $dx$) is $dv$.

**Single-factor trick:** for $\int\ln x\,dx$, $\int\arctan x\,dx$, etc., write as $u\cdot1$, with $dv=dx$.

### Repeated Integration by Parts — the Tabular Method

For $\int P(x)f(x)\,dx$ with polynomial $P(x)$:

1. Left column: $P(x)$ and successive derivatives (down to 0)
2. Right column: $f(x)$ and successive antiderivatives
3. Alternate signs $+,-,+,-,\ldots$
4. Multiply diagonally (row's left × NEXT row's right), sum with signs

### The "Solve for $I$" Technique

When repeated by-parts returns a multiple of the original integral $I$ (common with $e^{ax}\sin(bx)$ or $e^{ax}\cos(bx)$):
1. Apply by-parts twice
2. Recognize $I$ reappearing on the right side
3. Solve the resulting linear equation for $I$

---

## Definite Integral via Parts

$$\int_a^b u\,dv = \Big[uv\Big]_a^b - \int_a^b v\,du$$

---

## Complete Antiderivative Table (through Week 10)

| $f(x)$ | $\int f(x)\,dx$ |
|--------|-------------------|
| $x^n$ ($n\neq-1$) | $\dfrac{x^{n+1}}{n+1}+C$ |
| $1/x$ | $\ln\|x\|+C$ |
| $e^x$ | $e^x+C$ |
| $a^x$ | $a^x/\ln a+C$ |
| $\sin x$ | $-\cos x+C$ |
| $\cos x$ | $\sin x+C$ |
| $\sec^2x$ | $\tan x+C$ |
| $\csc^2x$ | $-\cot x+C$ |
| $\sec x\tan x$ | $\sec x+C$ |
| $\csc x\cot x$ | $-\csc x+C$ |
| $\tan x$ | $\ln\|\sec x\|+C$ |
| $\sec x$ | $\ln\|\sec x+\tan x\|+C$ |
| $1/\sqrt{1-x^2}$ | $\arcsin x+C$ |
| $1/(1+x^2)$ | $\arctan x+C$ |
| $\ln x$ | $x\ln x-x+C$ |
| $\arctan x$ | $x\arctan x-\frac12\ln(1+x^2)+C$ |

---

## Common Errors

| ❌ Wrong | ✅ Right |
|---------|---------|
| Forgetting to convert limits when substituting in a definite integral (if not converting back to $x$) | Either convert limits AND stay in $u$, OR substitute back to $x$ before evaluating — never mix |
| Choosing $u$ and $dv$ against LIATE without reason | Follow LIATE; if the resulting integral is HARDER, swap the choice |
| Forgetting "+C" is only added once, at the very end | Don't add constants at intermediate by-parts or substitution steps |
| Giving up on "circular" integrals | Recognize the reappearance of $I$ and solve algebraically |
| Missing symmetry shortcuts | Always check even/odd before grinding through a computation, especially on $[-a,a]$ |

---

## Week 10 Schedule

| Day | Event | Topic |
|-----|-------|-------|
| Monday | **Quiz 10** + Lecture 1 | Indefinite integrals, Net Change Theorem, Substitution Rule |
| Tuesday | Lecture 2 | Substitution in definite integrals, symmetry theorems |
| Friday | **Lab 10** | Pattern recognition drills, symmetry visualization, tabular method |
| Wednesday | Lecture 3 + **PS7 Released** | Integration by Parts, repeated & circular cases |

**Next week:** Trigonometric integrals and trigonometric substitution.
