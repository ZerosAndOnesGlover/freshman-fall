# MATH 141 · Calculus I
## Week 1 Resource Sheet
### Limits and Continuity — Quick Reference

---

## Limit Laws (All at once)

Assume $\lim_{x\to a}f(x)=L$ and $\lim_{x\to a}g(x)=M$ both exist. Then:

$$\lim_{x\to a}[f(x)\pm g(x)] = L \pm M$$
$$\lim_{x\to a}[f(x)\cdot g(x)] = L\cdot M$$
$$\lim_{x\to a}\frac{f(x)}{g(x)} = \frac{L}{M} \quad (M\neq 0)$$
$$\lim_{x\to a}[f(x)]^n = L^n$$
$$\lim_{x\to a}\sqrt[n]{f(x)} = \sqrt[n]{L} \quad (L>0 \text{ if } n \text{ even})$$
$$\lim_{x\to a}c = c \qquad \lim_{x\to a}x = a$$

---

## The Two Special Trig Limits

$$\lim_{x\to 0}\frac{\sin x}{x} = 1 \qquad \lim_{x\to 0}\frac{1-\cos x}{x} = 0$$

**Derived forms** (used constantly):

$$\lim_{x\to 0}\frac{\sin kx}{x} = k \qquad \lim_{x\to 0}\frac{\sin kx}{kx} = 1$$
$$\lim_{x\to 0}\frac{\tan x}{x} = 1 \qquad \lim_{x\to 0}\frac{\sin ax}{\sin bx} = \frac{a}{b}$$

---

## Indeterminate Forms (Require extra work)

| Form | Examples | Technique |
|------|----------|-----------|
| $0/0$ | $\frac{x^2-1}{x-1}$ at $x=1$ | Factor, cancel, rationalize |
| $\infty/\infty$ | $\frac{x^2+1}{3x^2-1}$ as $x\to\infty$ | Divide by highest power |
| $\infty - \infty$ | $\sqrt{x^2+x}-x$ as $x\to\infty$ | Conjugate multiply |
| $0\cdot\infty$ | $x\ln x$ as $x\to 0^+$ | Rewrite as $0/0$ or $\infty/\infty$ |
| $0^0$, $1^\infty$, $\infty^0$ | Various | Logarithm technique (Week 6) |

---

## Continuity — Three-Part Checklist

$f$ is continuous at $a$ $\iff$ ALL THREE:
1. $f(a)$ is defined
2. $\lim_{x\to a}f(x)$ exists
3. $\lim_{x\to a}f(x) = f(a)$

**Discontinuity types:**

| Type | One-sided limits | Removable? |
|------|-----------------|------------|
| Removable | Both exist, equal each other | ✅ Yes |
| Jump | Both exist, unequal | ❌ No |
| Infinite | At least one is $\pm\infty$ | ❌ No |
| Oscillatory | At least one DNE | ❌ No |

---

## The ε-δ Definition

$$\lim_{x\to a}f(x)=L \iff \forall\,\varepsilon>0,\;\exists\,\delta>0: 0<|x-a|<\delta \implies |f(x)-L|<\varepsilon$$

**Proof template:**
1. *Given $\varepsilon > 0$.*
2. *Let $\delta = $ [expression in $\varepsilon$, possibly with $\min$].*
3. *Suppose $0 < |x-a| < \delta$.*
4. *Then $|f(x)-L| = \cdots < \varepsilon$.*

**Standard $\delta$ choices:**
- For $\lim_{x\to a}(mx+b) = ma+b$: use $\delta = \varepsilon/|m|$
- For quadratics: use $\delta = \min(1, \varepsilon/C)$ where $C$ bounds the extra factor

---

## Intermediate Value Theorem

**Hypotheses:** $f$ continuous on $[a,b]$, $N$ strictly between $f(a)$ and $f(b)$

**Conclusion:** $\exists\, c\in(a,b)$ with $f(c)=N$

**Typical use:** Prove a root exists by finding $a,b$ with $f(a)<0<f(b)$ (or vice versa).

---

## Common Mistakes to Avoid

| ❌ Wrong | ✅ Right |
|---------|---------|
| Evaluate $\lim_{x\to a}f(x)$ by computing $f(a)$ when $a$ not in domain | Factor/cancel first, then substitute |
| Conclude limit DNE just because $f(a)$ is undefined | Limits don't require $f(a)$ defined |
| Use numerical table as proof of limit value | Algebra + limit laws = proof |
| Write $\lim_{x\to a}f(x) = \pm\infty$ and call it "the limit" | Say "the limit is infinite" or "DNE ($\to\infty$)" |
| Apply L'Hôpital's rule now (Week 6 only!) | Use algebra for $0/0$ forms this week |

---

## Reading Guide — Week 1

### Stewart (Primary)
- §2.1: Tangent and velocity problems — motivation for limits
- §2.2: The limit of a function — intuition and examples (**read carefully**)
- §2.3: Calculating limits using limit laws (**work all examples**)
- §2.4: The precise definition ε-δ (**study proofs, not just examples**)
- §2.5: Continuity — definition, IVT (**know IVT statement cold**)

### Spivak (Rigorous Supplement)
- Ch. 5: Limits — the formal definition developed from scratch. More rigorous than Stewart. If you want to understand *why* the definition takes the form it does, read this.
- Ch. 6: Continuous functions — the IVT proved properly.

### Online Resources
- **3Blue1Brown** "Essence of Calculus" Episode 7: Limits — excellent visual intuition
- **Paul's Online Math Notes** (tutorial.math.lamar.edu) — limit computation examples
- **MIT OCW 18.01** Lecture 2 — limits and continuity from Prof. Jerison

---

## Week 1 Schedule Summary

| Day | Event | Content |
|-----|-------|---------|
| Monday | **Quiz 01** (15 min) + Lecture 1 | Quiz covers Week 0; Lecture: limits intuition, one-sided limits, Squeeze Theorem |
| Tuesday | Lecture 2 | ε-δ definition, proofs, two special trig limits |
| Wednesday | Lecture 3 + **PS 1 released** (12:00) | Infinite limits and limits at infinity; Problem Set 1 due next Wednesday |
| Friday | **Lab 01** (2 hours) | Numerical/graphical investigation; bisection |

---

## Looking Ahead — Week 2

Week 2 introduces the **derivative** — the central object of differential calculus. It is defined as a limit:

$$f'(a) = \lim_{h \to 0} \frac{f(a+h) - f(a)}{h}$$

Every technique from Week 1 (evaluating $0/0$ indeterminate forms, one-sided limits, the special trig limits) will be used immediately in Week 2. The investment in limits pays off starting Monday of Week 2.
