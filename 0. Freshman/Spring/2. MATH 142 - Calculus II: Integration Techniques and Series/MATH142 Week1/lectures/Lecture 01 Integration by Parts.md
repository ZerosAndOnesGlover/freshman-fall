# MATH 142 · Calculus II
## Week 1 · Lecture 1 (Monday)
### Integration by Parts

**Date:** Monday 18 January 2027 · 11:00–11:50 · Week 1

---

**Reading:** Stewart §7.1 | Apostol Ch. 5 §5.9
**Quiz 01** — this Monday, **covers Week 0** (the FTC, substitution, applications of the integral)

---

## 1. The Derivation

Substitution came from the chain rule. **Parts comes from the product rule**, and the derivation is three lines.

The product rule:

$$\frac{d}{dx}\big[u(x)v(x)\big] = u'(x)v(x) + u(x)v'(x)$$

Integrate both sides. The left side is $uv$ by the FTC:

$$u v = \int u'v\,dx + \int uv'\,dx$$

Rearrange:

$$\boxed{\int u\,v'\,dx = uv - \int v\,u'\,dx}$$

or, in the differential notation everyone actually uses,

$$\boxed{\int u\,dv = uv - \int v\,du}$$

**What it does.** It trades one integral for another. That is all. The technique is worthwhile only when the new integral $\int v\,du$ is easier than the original $\int u\,dv$ — and choosing $u$ badly makes it harder.

---

## 2. Choosing $u$: LIATE

You must split the integrand into $u$ (to be differentiated) and $dv$ (to be integrated). The guiding principle:

> **Choose $u$ to be the part that gets simpler when you differentiate it.**
> **Choose $dv$ to be the part you can actually integrate.**

Both conditions matter. The usual mnemonic orders the candidates for $u$:

| | Type | Example |
|---|---|---|
| **L** | Logarithmic | $\ln x$, $\log_a x$ |
| **I** | Inverse trigonometric | $\arctan x$, $\arcsin x$ |
| **A** | Algebraic | $x^2$, $x+1$ |
| **T** | Trigonometric | $\sin x$, $\cos x$ |
| **E** | Exponential | $e^x$, $2^x$ |

**Whatever appears earlier in LIATE, make it $u$.**

The ordering is not arbitrary. Logarithms and inverse trigonometric functions become *algebraic* when differentiated — an enormous simplification, and the reason they go first. Algebraic terms lose a degree each time. Trigonometric and exponential functions never simplify under differentiation, so they belong in $dv$ where they will be integrated instead.

> **LIATE is a heuristic, not a theorem.** It is right most of the time and you should use it. But in §6 we meet an integral where no choice terminates, and the way out is not a better choice of $u$.

---

## 3. The Four Standard Examples

### Example 1 — the archetype: $\int x e^x\,dx$

LIATE: **A** before **E**, so $u = x$, $dv = e^x dx$.

$$u = x \implies du = dx \qquad dv = e^x dx \implies v = e^x$$

$$\int x e^x dx = xe^x - \int e^x\,dx = \boxed{xe^x - e^x + C} = (x-1)e^x + C$$

*Verified symbolically.*

**Check by differentiating:** $\frac{d}{dx}\big[(x-1)e^x\big] = e^x + (x-1)e^x = xe^x$ ✓

**What would the wrong choice have done?** Taking $u=e^x$, $dv = x\,dx$ gives $v = \tfrac{x^2}{2}$ and

$$\int xe^x dx = \frac{x^2}{2}e^x - \int \frac{x^2}{2}e^x\,dx$$

The new integral has $x^2$ where the old had $x$ — **strictly worse**. This is what "choose the part that simplifies" means, and it is worth doing once so you recognise the symptom.

### Example 2 — the one nobody expects: $\int \ln x\,dx$

There is only one factor. **Take $dv = dx$.**

$$u = \ln x \implies du = \frac{dx}{x} \qquad dv = dx \implies v = x$$

$$\int \ln x\,dx = x\ln x - \int x\cdot\frac{1}{x}\,dx = x\ln x - \int dx = \boxed{x\ln x - x + C}$$

*Verified symbolically.*

**Check:** $\frac{d}{dx}[x\ln x - x] = \ln x + 1 - 1 = \ln x$ ✓

**This is the standard antiderivative of $\ln x$** and you should know it. The trick — supplying an invisible $dv = dx$ — also handles $\int\arctan x\,dx$ and $\int\arcsin x\,dx$.

### Example 3 — trigonometric: $\int x\sin x\,dx$

LIATE: **A** before **T**, so $u = x$, $dv = \sin x\,dx$, $v = -\cos x$.

$$\int x\sin x\,dx = -x\cos x - \int(-\cos x)\,dx = \boxed{-x\cos x + \sin x + C}$$

*Verified symbolically.*

**The sign is where marks are lost.** $v = -\cos x$, and then $-\int v\,du = -\int(-\cos x)dx = +\int\cos x\,dx$. Two minus signs, both easy to drop. **Differentiate to check.**

### Example 4 — inverse trigonometric: $\int\arctan x\,dx$

$u = \arctan x$, $dv = dx$:

$$du = \frac{dx}{1+x^2} \qquad v = x$$

$$\int\arctan x\,dx = x\arctan x - \int\frac{x}{1+x^2}\,dx$$

The remaining integral is a **substitution** ($w = 1+x^2$), from Week 0:

$$\int\frac{x}{1+x^2}dx = \frac12\ln(1+x^2)$$

$$\boxed{\int\arctan x\,dx = x\arctan x - \frac12\ln(1+x^2) + C}$$

*Verified symbolically.*

**Note the structure**: parts reduced it to a substitution. **Most real integrals need more than one technique**, and recognising the second one is part of the skill.

---

## 4. Definite Integrals by Parts

The formula carries the evaluation bars on the $uv$ term:

$$\boxed{\int_a^b u\,dv = \Big[uv\Big]_a^b - \int_a^b v\,du}$$

**The bracket must be evaluated at both limits, and the remaining integral keeps its limits.** Forgetting to evaluate $[uv]$ is the most common error.

### Example 5

$$\int_0^1 x e^x\,dx = \Big[xe^x\Big]_0^1 - \int_0^1 e^x dx = (1\cdot e - 0) - \Big[e^x\Big]_0^1 = e - (e-1) = \boxed{1}$$

*Verified symbolically: exactly $1$.*

A pleasing answer, and a good check that the arithmetic is right — $e$ cancels completely.

### Example 6

$$\int_1^e \ln x\,dx = \Big[x\ln x - x\Big]_1^e = (e - e) - (0 - 1) = \boxed{1}$$

*Verified symbolically: exactly $1$.*

**Geometrically:** the area under $\ln x$ from 1 to $e$ is exactly 1. Worth remembering as a sanity anchor.

---

## 5. When Parts Is the Wrong Tool

Parts can be applied to anything. It usually should not be.

$$\int\frac{dx}{1+x^2}$$

Try $u = \frac{1}{1+x^2}$, $dv = dx$:

$$= \frac{x}{1+x^2} + \int\frac{2x^2}{(1+x^2)^2}\,dx$$

which is worse. **The answer is $\arctan x + C$ from the Week 0 catalogue** — no technique required.

> **Before reaching for parts, ask: is this a catalogue entry? Is it a substitution?**
> Parts is for a **product of two unlike things**, where one simplifies on differentiation. If the
> integrand is not a product in that sense, parts is unlikely to be the answer.

### The recognition table

| Integrand looks like | Try |
|---|---|
| $f(g(x))g'(x)$ — inner function and its derivative | **Substitution** |
| (polynomial) × (exponential or trig) | **Parts**, $u$ = polynomial |
| lone $\ln x$, $\arctan x$, $\arcsin x$ | **Parts** with $dv = dx$ |
| (polynomial) × $\ln x$ | **Parts**, $u = \ln x$ |
| a catalogue entry | **Just write it down** |

---

## 6. A Warning About Tomorrow

Everything above terminated: one application of parts, and the remaining integral was elementary. Two things go wrong, and both are Lecture 2:

1. **$\int x^2 e^x\,dx$** — one application leaves $\int 2x e^x dx$, still a product. You must apply parts *again*. Polynomials of degree $n$ need $n$ applications.

2. **$\int e^x\sin x\,dx$** — apply parts twice and you return to **exactly the integral you started with**. No choice of $u$ terminates. The way out is not a better choice; it is to treat the equation as an algebraic equation and solve for the unknown integral.

---

## 7. What To Take From This Lecture

1. **$\int u\,dv = uv - \int v\,du$** — the product rule, integrated.
2. **Choose $u$ to simplify on differentiation, $dv$ to be integrable.** LIATE orders the candidates.
3. **$\int\ln x\,dx = x\ln x - x + C$** — take $dv = dx$ when there is only one factor.
4. **Definite parts:** evaluate the $[uv]$ bracket at both limits.
5. **Parts is not universal.** Check the catalogue and substitution first.
6. **Differentiate every answer.** The sign errors in Examples 3 and 4 are caught in ten seconds.

---

*Next: Tuesday — Repeated Parts, Reduction Formulas, and the Integral That Comes Back*
