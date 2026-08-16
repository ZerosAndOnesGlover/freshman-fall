# MATH 141 · Calculus I
## Week 6 · Lecture 3 (Wednesday)
### L'Hôpital's Rule: Resolving Indeterminate Forms

**Date:** Wednesday 30 September 2026 · 11:00–11:50 · Week 6

---

**Reading:** Stewart §4.4 | Spivak Ch. 11 (§11.4, via MVT extensions)

---

## 1. The Problem: Indeterminate Forms Revisited

Back in Week 1, we encountered limits like $\displaystyle\lim_{x\to0}\frac{\sin x}{x}$ that produce the meaningless expression $\dfrac{0}{0}$ upon direct substitution. We resolved that particular limit using geometry and the Squeeze Theorem. But many $\dfrac{0}{0}$ (and $\dfrac{\infty}{\infty}$) limits resist elementary algebraic tricks entirely. Consider:

$$\lim_{x\to0}\frac{e^x-1-x}{x^2} \qquad \lim_{x\to\infty}\frac{\ln x}{x} \qquad \lim_{x\to0}\frac{\tan x - x}{x^3}$$

None of these simplify by factoring or rationalizing. We need a fundamentally new tool — and it comes directly from the Mean Value Theorem machinery built last week.

---

## 2. L'Hôpital's Rule — Statement

> **Theorem (L'Hôpital's Rule).** Suppose $f$ and $g$ are differentiable near $a$ (except possibly at $a$), and $g'(x) \neq 0$ near $a$ (except possibly at $a$). Suppose that:
>
> $$\lim_{x\to a}f(x) = 0 \text{ and } \lim_{x\to a}g(x) = 0 \qquad \text{(the } 0/0 \text{ case)}$$
>
> OR
>
> $$\lim_{x\to a}f(x) = \pm\infty \text{ and } \lim_{x\to a}g(x) = \pm\infty \qquad \text{(the } \infty/\infty \text{ case)}$$
>
> Then:
> $$\lim_{x\to a}\frac{f(x)}{g(x)} = \lim_{x\to a}\frac{f'(x)}{g'(x)}$$
>
> **provided the limit on the right exists (or is $\pm\infty$).**

The rule also holds for one-sided limits and for $a = \pm\infty$.

> ⚠️ **Critical misunderstanding to avoid:** L'Hôpital's Rule does NOT say "take the derivative of the quotient." It says: take the derivative of the numerator and denominator **separately**, then form a new quotient. This is completely different from the quotient rule.

---

## 3. Why This Works — Proof Sketch (Cauchy's MVT)

The proof relies on a generalization of the MVT called the **Generalized (Cauchy) Mean Value Theorem**:

> If $f, g$ are continuous on $[a,b]$ and differentiable on $(a,b)$, with $g'(x)\neq0$ on $(a,b)$, then there exists $c\in(a,b)$ such that:
> $$\frac{f(b)-f(a)}{g(b)-g(a)} = \frac{f'(c)}{g'(c)}$$

**Proof of Cauchy's MVT:** Define $h(x) = f(x) - f(a) - \dfrac{f(b)-f(a)}{g(b)-g(a)}[g(x)-g(a)]$.

Then $h(a) = 0$ and $h(b) = 0$. By Rolle's Theorem, $\exists\,c\in(a,b)$ with $h'(c)=0$:

$$f'(c) - \frac{f(b)-f(a)}{g(b)-g(a)}g'(c) = 0 \implies \frac{f(b)-f(a)}{g(b)-g(a)} = \frac{f'(c)}{g'(c)} \quad\square$$

**Sketch of L'Hôpital's Rule proof (for the $0/0$ case, assuming $f(a)=g(a)=0$):**

$$\frac{f(x)}{g(x)} = \frac{f(x)-f(a)}{g(x)-g(a)} = \frac{f'(c)}{g'(c)} \quad\text{for some } c \text{ between } a \text{ and } x$$

As $x\to a$, we have $c\to a$ as well (squeezed between $a$ and $x$), so:

$$\lim_{x\to a}\frac{f(x)}{g(x)} = \lim_{c\to a}\frac{f'(c)}{g'(c)} = \lim_{x\to a}\frac{f'(x)}{g'(x)} \quad\square$$

This is a beautiful illustration of how last week's MVT machinery — seemingly abstract at the time — pays off immediately as a computational tool.

---

## 4. Basic Examples — the $0/0$ Case

### Example 1

$$\lim_{x\to0}\frac{e^x-1}{x}$$

Direct substitution: $\dfrac{1-1}{0} = \dfrac{0}{0}$. Apply L'Hôpital:

$$= \lim_{x\to0}\frac{e^x}{1} = e^0 = 1$$

*(This recovers a fact we could have derived directly: this limit is exactly the definition of $\frac{d}{dx}[e^x]$ at $x=0$, which equals $e^0=1$.)*

### Example 2

$$\lim_{x\to0}\frac{\tan x - x}{x^3}$$

Direct substitution: $0/0$. Apply L'Hôpital:

$$= \lim_{x\to0}\frac{\sec^2x - 1}{3x^2}$$

Still $0/0$ (since $\sec^2 0 = 1$). **Apply L'Hôpital again:**

$$= \lim_{x\to0}\frac{2\sec^2x\tan x}{6x} = \lim_{x\to0}\frac{\sec^2x\tan x}{3x}$$

Still $0/0$. **Apply once more:** (using product rule on numerator)

$$\frac{d}{dx}[\sec^2x\tan x] = 2\sec^2x\tan x\cdot\tan x + \sec^2x\cdot\sec^2x = 2\sec^2x\tan^2x+\sec^4x$$

$$= \lim_{x\to0}\frac{2\sec^2x\tan^2x+\sec^4x}{3} = \frac{0+1}{3} = \frac{1}{3}$$

**Lesson:** L'Hôpital's Rule can be applied repeatedly as long as each successive limit is still indeterminate.

---

## 5. Basic Examples — the $\infty/\infty$ Case

### Example 3

$$\lim_{x\to\infty}\frac{\ln x}{x}$$

Both numerator and denominator $\to\infty$. Apply L'Hôpital:

$$= \lim_{x\to\infty}\frac{1/x}{1} = \lim_{x\to\infty}\frac{1}{x} = 0$$

**Interpretation:** logarithmic growth is dominated by linear growth — $\ln x$ grows far slower than $x$.

### Example 4

$$\lim_{x\to\infty}\frac{x^2}{e^x}$$

Both $\to\infty$. Apply L'Hôpital:

$$= \lim_{x\to\infty}\frac{2x}{e^x}$$

Still $\infty/\infty$. **Apply again:**

$$= \lim_{x\to\infty}\frac{2}{e^x} = 0$$

**Interpretation:** exponential growth dominates polynomial growth, no matter how high the polynomial degree. This is a fundamentally important fact for algorithm complexity analysis.

---

## 6. Other Indeterminate Forms — Converting to $0/0$ or $\infty/\infty$

L'Hôpital's Rule directly handles only $0/0$ and $\infty/\infty$. Other indeterminate forms — $0\cdot\infty$, $\infty-\infty$, $0^0$, $1^\infty$, $\infty^0$ — must first be algebraically converted.

### Form $0 \cdot \infty$

**Strategy:** Rewrite as a quotient: $fg = \dfrac{f}{1/g}$ or $\dfrac{g}{1/f}$.

**Example 5:** $\displaystyle\lim_{x\to0^+}x\ln x$

Rewrite: $x\ln x = \dfrac{\ln x}{1/x}$, now $\dfrac{-\infty}{\infty}$ form. Apply L'Hôpital:

$$= \lim_{x\to0^+}\frac{1/x}{-1/x^2} = \lim_{x\to0^+}(-x) = 0$$

### Form $\infty - \infty$

**Strategy:** Combine into a single fraction (common denominator), which typically produces $0/0$.

**Example 6:** $\displaystyle\lim_{x\to0}\left(\frac{1}{\sin x} - \frac{1}{x}\right)$

Combine: $\dfrac{x - \sin x}{x\sin x}$, now $0/0$. Apply L'Hôpital:

$$= \lim_{x\to0}\frac{1-\cos x}{\sin x + x\cos x}$$

Still $0/0$. **Apply again:**

$$= \lim_{x\to0}\frac{\sin x}{\cos x + \cos x - x\sin x} = \lim_{x\to0}\frac{\sin x}{2\cos x - x\sin x} = \frac{0}{2} = 0$$

### Forms $0^0$, $1^\infty$, $\infty^0$

**Strategy:** Take the natural log to convert the exponent into a product (usually $0\cdot\infty$ form), solve that limit, then exponentiate back with $e$.

**Example 7:** $\displaystyle\lim_{x\to0^+}x^x$ (form $0^0$)

Let $y = x^x$. Then $\ln y = x\ln x$.

From Example 5: $\displaystyle\lim_{x\to0^+}x\ln x = 0$.

So $\displaystyle\lim_{x\to0^+}\ln y = 0$, which means $\displaystyle\lim_{x\to0^+}y = e^0 = 1$.

$$\lim_{x\to0^+}x^x = 1$$

**Example 8:** $\displaystyle\lim_{x\to\infty}\left(1+\frac{1}{x}\right)^x$ (form $1^\infty$ — this is literally the definition of $e$!)

Let $y = \left(1+\dfrac1x\right)^x$. Then $\ln y = x\ln\left(1+\dfrac1x\right)$.

Rewrite as quotient: $\dfrac{\ln(1+1/x)}{1/x}$, form $0/0$ as $x\to\infty$. Apply L'Hôpital (differentiating with respect to $x$, treating $1/x$ carefully):

Let $t = 1/x \to 0^+$. Then we need $\displaystyle\lim_{t\to0^+}\frac{\ln(1+t)}{t}$.

Apply L'Hôpital: $\displaystyle\lim_{t\to0^+}\frac{1/(1+t)}{1} = 1$.

So $\displaystyle\lim_{x\to\infty}\ln y = 1$, giving $\displaystyle\lim_{x\to\infty}y = e^1 = e$.

$$\lim_{x\to\infty}\left(1+\frac{1}{x}\right)^x = e$$

This confirms the limit definition of $e$ from Week 3, now derived rigorously via L'Hôpital's Rule.

---

## 7. When L'Hôpital's Rule Does NOT Apply

**Common misuse 1 — Not an indeterminate form:**

$$\lim_{x\to0}\frac{\sin x}{x+1}$$

This is $\dfrac{0}{1} = 0$ directly — NOT indeterminate. Applying L'Hôpital here (getting $\lim\cos x/1 = 1$) gives the **wrong answer**. Always verify the form is truly $0/0$ or $\infty/\infty$ before applying the rule.

**Common misuse 2 — Rule doesn't terminate:**

$$\lim_{x\to\infty}\frac{x}{\sqrt{x^2+1}}$$

Apply L'Hôpital: $\displaystyle\lim_{x\to\infty}\frac{1}{x/\sqrt{x^2+1}}$ — this just recreates a similar expression, looping forever. Here, algebraic manipulation (divide by $x$) is faster and correct:

$$\lim_{x\to\infty}\frac{x}{\sqrt{x^2+1}} = \lim_{x\to\infty}\frac{1}{\sqrt{1+1/x^2}} = 1$$

**Lesson:** L'Hôpital's Rule is powerful but not always the most efficient tool. Always consider algebraic simplification first.

---

## 8. CS Connection — Growth Rate Hierarchies

L'Hôpital's Rule gives rigorous proof of the **growth rate hierarchy** fundamental to algorithm complexity analysis:

$$\ln x \ll x^\epsilon \ll x \ll x\ln x \ll x^2 \ll \cdots \ll 2^x \ll x! \ll x^x$$

(for any small $\epsilon > 0$, as $x\to\infty$, using $\ll$ to mean "grows asymptotically slower than")

Each relation $\displaystyle\lim_{x\to\infty}\frac{f(x)}{g(x)} = 0$ can be proven with L'Hôpital's Rule. This is precisely why:
- $O(\log n)$ algorithms (binary search) outperform $O(n)$ algorithms (linear search) for large $n$
- $O(n\log n)$ sorting algorithms (mergesort) outperform $O(n^2)$ algorithms (bubble sort)
- Exponential-time algorithms ($O(2^n)$) become computationally infeasible far faster than any polynomial-time algorithm, no matter the polynomial's degree

The formal justification for "Big-O dominance" in every algorithms course you'll take is, at its root, a L'Hôpital's Rule computation.

---

## Lecture 1 Exercises

1. Evaluate using L'Hôpital's Rule:
   - (a) $\displaystyle\lim_{x\to0}\frac{e^{2x}-1}{\sin x}$
   - (b) $\displaystyle\lim_{x\to1}\frac{x^3-1}{x^2-1}$ (verify by also factoring — do both methods agree?)
   - (c) $\displaystyle\lim_{x\to\infty}\frac{x^3}{e^x}$
   - (d) $\displaystyle\lim_{x\to0^+}\frac{\ln(\sin x)}{\ln x}$

2. Convert to $0/0$ or $\infty/\infty$ form, then apply L'Hôpital:
   - (a) $\displaystyle\lim_{x\to\infty}x\sin\!\left(\frac{1}{x}\right)$
   - (b) $\displaystyle\lim_{x\to0^+}\left(\frac{1}{x}-\frac{1}{\sin x}\right)$
   - (c) $\displaystyle\lim_{x\to0^+}(\cos x)^{1/x^2}$ *(form $1^\infty$)*
   - (d) $\displaystyle\lim_{x\to\infty}x^{1/x}$ *(form $\infty^0$)*

3. Explain why L'Hôpital's Rule gives the WRONG approach (or fails to terminate) for $\displaystyle\lim_{x\to\infty}\frac{x+\sin x}{x}$. Evaluate this limit correctly using an alternative method.

4. **(Proof)** Use L'Hôpital's Rule to prove that for any positive integer $n$, $\displaystyle\lim_{x\to\infty}\frac{x^n}{e^x}=0$. *(Hint: apply the rule $n$ times, or use induction.)*

5. **(Synthesis)** Show, using L'Hôpital's Rule, that $\displaystyle\lim_{x\to\infty}\left(1+\frac{k}{x}\right)^x = e^k$ for any constant $k$. This generalizes Example 8 and is the basis of the continuous compounding formula in finance.

---


### Answers

**Always verify the form is $\tfrac00$ or $\tfrac\infty\infty$ before applying the rule.**

**1. (a)** $\tfrac00$; differentiate top and bottom: $\dfrac{2e^{2x}}{\cos x}\to\boxed{2}$
**(b)** $\tfrac00$: $\dfrac{3x^2}{2x}\to\boxed{\tfrac32}$. Factoring agrees:
$\dfrac{(x-1)(x^2+x+1)}{(x-1)(x+1)}\to\dfrac{3}{2}$ ✓ — two methods, same answer.
**(c)** $\tfrac\infty\infty$ three times: $\dfrac{3x^2}{e^x}\to\dfrac{6x}{e^x}\to\dfrac{6}{e^x}\to\boxed{0}$
**(d)** $\tfrac{-\infty}{-\infty}$: $\dfrac{\cot x}{1/x}=\dfrac{x\cos x}{\sin x}\to\boxed{1}$

**2. (a)** Form $\infty\cdot0$. Substitute $t=1/x$: $\dfrac{\sin t}{t}\to\boxed{1}$.
**(b)** Form $\infty-\infty$. Combine: $\dfrac{\sin x-x}{x\sin x}$, now $\tfrac00$; two applications
give $\boxed{0}$.
**(c)** Form $1^\infty$. Take logs: $\dfrac{\ln\cos x}{x^2}\to-\tfrac12$, so the limit is
$\boxed{e^{-1/2}\approx0.6065}$.
**(d)** Form $\infty^0$. Take logs: $\dfrac{\ln x}{x}\to0$, so the limit is $\boxed{1}$.

*(All four confirmed numerically.)* For **(c)** and **(d)** the logarithm is not optional — the rule
applies to quotients, so every exponential indeterminate form must first be converted.

**3.** L'Hôpital gives $\dfrac{1+\cos x}{1}=1+\cos x$, which **oscillates between 0 and 2 and has
no limit**. The rule has not failed — it simply yields no conclusion, because L'Hôpital requires
that the limit of $f'/g'$ *exist*. When it does not, the theorem says nothing either way.

Correct method — divide through:
$$\frac{x+\sin x}{x}=1+\frac{\sin x}{x}\longrightarrow 1+0=\boxed{1}$$
since $|\sin x|\leq1$ and $x\to\infty$.

**The general lesson: an inconclusive L'Hôpital attempt is not evidence the limit fails to exist.**
Always have an algebraic fallback.

**4.** Induction on $n$. *Base:* $\displaystyle\lim_{x\to\infty}\frac{x}{e^x}=\lim\frac{1}{e^x}=0$
by one application. *Step:* assume $\lim x^{n-1}/e^x=0$; then $x^n/e^x$ is $\tfrac\infty\infty$, and
one application gives $\dfrac{nx^{n-1}}{e^x}=n\cdot\dfrac{x^{n-1}}{e^x}\to n\cdot0=0$.
Hence $\boxed{\lim_{x\to\infty}x^n/e^x=0}$ for every positive integer $n$. $\blacksquare$

Each application lowers the polynomial degree by one while leaving $e^x$ untouched — which is
exactly why **exponentials beat every polynomial**.

**5.** Let $y=\left(1+\tfrac kx\right)^x$. Then
$$\ln y = x\ln\!\left(1+\frac kx\right) = \frac{\ln\left(1+k/x\right)}{1/x}$$
which is $\tfrac00$ as $x\to\infty$. Applying L'Hôpital (differentiating with respect to $x$):
$$\frac{\dfrac{-k/x^2}{1+k/x}}{-1/x^2} = \frac{k}{1+k/x}\longrightarrow k$$
So $\ln y\to k$ and therefore $\boxed{y\to e^k}$. $\blacksquare$
*(Check: $k=3$, $x=10^7$ gives $20.0855$ against $e^3=20.0855$ ✓.)*

This is the continuous-compounding formula: interest at annual rate $k$ compounded $x$ times per
year approaches $e^k$ as $x\to\infty$.

*Next: Tuesday — Curve Sketching: Full Synthesis*
