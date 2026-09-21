# MATH 141 · Calculus I
## Week 1 · Lecture 1 (Monday)
### Limits: Intuition, Informal Definition, and the One-Sided Limit

**Date:** Monday 28 September 2026 · 11:00–11:50 · Week 1

---

**Reading:** Stewart §2.1–2.2 | Spivak Ch. 5 (Limits)  
**Quiz 01** is this Monday (covers Week 0 material — see quiz file)

---

## The Central Question of Calculus

Here is the problem that motivated the invention of calculus, independently, by Newton and Leibniz in the 17th century:

> **What is the instantaneous velocity of a moving object?**

Average velocity over a time interval $[t, t+h]$ is easy:
$$v_{\text{avg}} = \frac{\text{distance}}{\text{time}} = \frac{s(t+h) - s(t)}{h}$$

But instantaneous velocity — the reading on a speedometer at a single instant — requires dividing distance by time over an *infinitely short* interval. That means $h \to 0$. But you cannot set $h = 0$ directly (you get $0/0$, which is meaningless).

The **limit** is the mathematical tool invented to resolve this. Every concept in calculus — the derivative, the integral, continuity — is defined using limits.

---

## 1. The Intuitive Idea of a Limit

**Informal definition:**
$$\lim_{x \to a} f(x) = L$$

means: as $x$ gets arbitrarily close to $a$ (but does not equal $a$), the values $f(x)$ get arbitrarily close to $L$.

### The Key Point: The Value at $a$ Doesn't Matter

The limit asks what $f(x)$ *approaches* as $x \to a$ — not what $f(a)$ equals. The function may not even be defined at $a$.

**Example 1:** Let $f(x) = \dfrac{x^2 - 1}{x - 1}$.

At $x = 1$: $f(1) = \dfrac{0}{0}$ — undefined.

But for $x \neq 1$:
$$f(x) = \frac{x^2 - 1}{x - 1} = \frac{(x-1)(x+1)}{x-1} = x + 1$$

So as $x \to 1$, $f(x) \to 2$. We write:
$$\lim_{x \to 1} \frac{x^2 - 1}{x - 1} = 2$$

The function has a *hole* at $x = 1$ but the limit exists and equals $2$.

**Numerical evidence:**

| $x$ | $f(x) = \frac{x^2-1}{x-1}$ |
|-----|----------------------------|
| 0.9 | 1.9 |
| 0.99 | 1.99 |
| 0.999 | 1.999 |
| 1.001 | 2.001 |
| 1.01 | 2.01 |
| 1.1 | 2.1 |

The table suggests — but does not prove — the limit is 2. Algebra confirmed it.

> ⚠️ **Warning:** Numerical tables can be misleading. They suggest limits but don't prove them. The limit of $f(x) = \sin(\pi/x)$ as $x \to 0$ cannot be found from a table — the function oscillates infinitely. Algebra and formal proofs are the only reliable tools.

---

## 2. One-Sided Limits

Sometimes $f(x)$ approaches different values depending on which side of $a$ you approach from.

**Left-hand limit:** $\displaystyle\lim_{x \to a^-} f(x) = L$ means $x$ approaches $a$ from the left ($x < a$).

**Right-hand limit:** $\displaystyle\lim_{x \to a^+} f(x) = L$ means $x$ approaches $a$ from the right ($x > a$).

### The Connection Between One-Sided and Two-Sided Limits

$$\lim_{x \to a} f(x) = L \iff \lim_{x \to a^-} f(x) = L \text{ and } \lim_{x \to a^+} f(x) = L$$

The two-sided limit exists **if and only if** both one-sided limits exist **and are equal**.

**Example 2:** Consider the piecewise function:
$$f(x) = \begin{cases} x + 1 & \text{if } x < 2 \\ 3 & \text{if } x = 2 \\ x^2 - 1 & \text{if } x > 2 \end{cases}$$

- $\displaystyle\lim_{x \to 2^-} f(x) = \lim_{x \to 2^-} (x+1) = 3$
- $\displaystyle\lim_{x \to 2^+} f(x) = \lim_{x \to 2^+} (x^2 - 1) = 3$

Both equal 3, so $\displaystyle\lim_{x \to 2} f(x) = 3$.

Note: $f(2) = 3$ here also, but the limit would still be 3 even if $f(2)$ were defined differently — because limits don't care about the value at the point.

**Example 3 — Limit Does Not Exist:**
$$g(x) = \begin{cases} x + 1 & \text{if } x < 0 \\ x^2 + 1 & \text{if } x > 0 \end{cases}$$

- $\displaystyle\lim_{x \to 0^-} g(x) = 0 + 1 = 1$
- $\displaystyle\lim_{x \to 0^+} g(x) = 0 + 1 = 1$

Actually both are 1 — limit exists! But consider:
$$h(x) = \begin{cases} x + 1 & \text{if } x < 0 \\ x^2 + 2 & \text{if } x > 0 \end{cases}$$

- $\displaystyle\lim_{x \to 0^-} h(x) = 1$
- $\displaystyle\lim_{x \to 0^+} h(x) = 2$

Since $1 \neq 2$, $\displaystyle\lim_{x \to 0} h(x)$ **does not exist (DNE)**.

---

## 3. Infinite Limits and Vertical Asymptotes

When $f(x)$ grows without bound as $x \to a$, we write:
$$\lim_{x \to a} f(x) = +\infty \quad \text{or} \quad \lim_{x \to a} f(x) = -\infty$$

These are **not** real limits (infinity is not a number) — they are a precise way of saying the function grows without bound.

**Example 4:** $f(x) = \dfrac{1}{(x-2)^2}$

As $x \to 2$ from either side, $(x-2)^2 \to 0^+$, so $\dfrac{1}{(x-2)^2} \to +\infty$.

$$\lim_{x \to 2} \frac{1}{(x-2)^2} = +\infty$$

The line $x = 2$ is a **vertical asymptote**.

**Example 5 — Different signs on each side:**
$$\lim_{x \to 0^+} \frac{1}{x} = +\infty \qquad \lim_{x \to 0^-} \frac{1}{x} = -\infty$$

So $\displaystyle\lim_{x \to 0} \frac{1}{x}$ DNE (one-sided limits are $+\infty$ and $-\infty$, which differ).

**Vertical asymptote rule:** If $f(x) = P(x)/Q(x)$ and $Q(a) = 0$ but $P(a) \neq 0$, then $x = a$ is a vertical asymptote.

---

## 4. Limits at Infinity and Horizontal Asymptotes

$$\lim_{x \to \infty} f(x) = L \quad \text{means } f(x) \to L \text{ as } x \to \infty$$

**Example 6:**
$$\lim_{x \to \infty} \frac{3x^2 - 2x + 1}{5x^2 + 4} = \lim_{x \to \infty} \frac{3 - 2/x + 1/x^2}{5 + 4/x^2} = \frac{3 - 0 + 0}{5 + 0} = \frac{3}{5}$$

The technique: **divide numerator and denominator by the highest power of $x$**.

**General rational function rules** ($P$, $Q$ polynomials of degrees $m$, $n$):

| Condition | $\lim_{x\to\infty} P(x)/Q(x)$ |
|-----------|-------------------------------|
| $m < n$ | $0$ |
| $m = n$ | ratio of leading coefficients |
| $m > n$ | $\pm\infty$ |

The line $y = L$ is a **horizontal asymptote** if $\displaystyle\lim_{x \to \pm\infty} f(x) = L$.

---

## 5. When Limits Fail to Exist — A Taxonomy

A limit $\displaystyle\lim_{x \to a} f(x)$ fails to exist in three ways:

| Type | Description | Example |
|------|-------------|---------|
| **Jump discontinuity** | Left and right limits exist but differ | $\lfloor x \rfloor$ at integers |
| **Infinite limit** | Function grows without bound | $1/x$ at $x=0$ |
| **Oscillation** | Function oscillates with no settling value | $\sin(1/x)$ at $x=0$ |

The last case — $\sin(1/x)$ — is subtle. As $x \to 0$, the function oscillates between $-1$ and $+1$ infinitely often. No matter how close to 0 you get, the function takes all values between $-1$ and $1$. No limit exists.

---

## 6. Computing Limits: Direct Substitution

The simplest technique: if $f$ is a "nice" function (polynomial, rational, trigonometric) and $a$ is in its domain, then:
$$\lim_{x \to a} f(x) = f(a)$$

**Example 7:**
$$\lim_{x \to 3} (x^2 + 2x - 1) = 9 + 6 - 1 = 14 \checkmark$$

When does direct substitution fail? When $f(a)$ is undefined — particularly $\dfrac{0}{0}$, $\dfrac{\infty}{\infty}$, or $0 \cdot \infty$. These are called **indeterminate forms** and require additional techniques (algebra, L'Hôpital's rule in Week 6).

---

## 7. The Limit Laws

If $\displaystyle\lim_{x \to a} f(x) = L$ and $\displaystyle\lim_{x \to a} g(x) = M$, then:

| Law | Statement |
|-----|-----------|
| Sum | $\lim[f(x) + g(x)] = L + M$ |
| Difference | $\lim[f(x) - g(x)] = L - M$ |
| Constant multiple | $\lim[c \cdot f(x)] = cL$ |
| Product | $\lim[f(x) \cdot g(x)] = LM$ |
| Quotient | $\lim\dfrac{f(x)}{g(x)} = \dfrac{L}{M}$, provided $M \neq 0$ |
| Power | $\lim[f(x)]^n = L^n$ |
| Root | $\lim\sqrt[n]{f(x)} = \sqrt[n]{L}$ (for appropriate conditions) |

These laws mean: **limits respect the arithmetic operations.** This is what makes computing limits with algebra valid.

---

## 8. The Squeeze Theorem

If $g(x) \leq f(x) \leq h(x)$ near $a$ (but not necessarily at $a$), and
$$\lim_{x \to a} g(x) = \lim_{x \to a} h(x) = L,$$
then $\displaystyle\lim_{x \to a} f(x) = L$.

**Classic application:**
$$\lim_{x \to 0} x^2 \sin\!\left(\frac{1}{x}\right)$$

Since $-1 \leq \sin(1/x) \leq 1$ for all $x \neq 0$:
$$-x^2 \leq x^2 \sin\!\left(\frac{1}{x}\right) \leq x^2$$

And $\displaystyle\lim_{x \to 0} (-x^2) = 0$ and $\displaystyle\lim_{x \to 0} x^2 = 0$.

By the Squeeze Theorem: $\displaystyle\lim_{x \to 0} x^2 \sin\!\left(\frac{1}{x}\right) = 0$.

Note: $\lim_{x \to 0} \sin(1/x)$ does not exist, but $x^2$ "squeezes" the oscillation to zero.

---

## Two Special Trigonometric Limits

These arise constantly in the rest of the course:

$$\boxed{\lim_{x \to 0} \frac{\sin x}{x} = 1} \qquad \boxed{\lim_{x \to 0} \frac{1 - \cos x}{x} = 0}$$

These cannot be derived by direct substitution (both give $0/0$). The first is proved geometrically using the Squeeze Theorem (see Tuesday's lecture). They are the foundation of every trigonometric derivative.

---

## Looking Ahead: Why Formalize?

The informal definition — "$f(x)$ gets close to $L$ as $x$ gets close to $a$" — is intuitive but imprecise. What does "close" mean? How close? Close enough for what purpose?

In Tuesday's lecture, we develop the formal $\varepsilon$-$\delta$ definition that answers these questions with mathematical precision. It is the most important definition in calculus — and the most challenging — but it is what transforms calculus from a collection of techniques into a rigorous mathematical theory.

---

## Lecture 1 Exercises

1. Use a table of values to estimate $\displaystyle\lim_{x \to 0} \dfrac{\sin 3x}{x}$. Then confirm algebraically by writing $\dfrac{\sin 3x}{x} = 3 \cdot \dfrac{\sin 3x}{3x}$.

2. Evaluate, if they exist:
   - (a) $\displaystyle\lim_{x \to 2} \dfrac{x^2 - 4}{x - 2}$
   - (b) $\displaystyle\lim_{x \to 0^+} \dfrac{|x|}{x}$ and $\displaystyle\lim_{x \to 0^-} \dfrac{|x|}{x}$
   - (c) $\displaystyle\lim_{x \to \infty} \dfrac{4x^3 - 2x}{7x^3 + x^2}$

3. Use the Squeeze Theorem to find $\displaystyle\lim_{x \to 0} x^4 \cos(2/x)$.

4. A function $f$ satisfies $3x - 1 \leq f(x) \leq x^2 + 2$ for all $x$ near $1$. Find $\displaystyle\lim_{x \to 1} f(x)$.

5. **(Thinking)** Explain in your own words why $\displaystyle\lim_{x \to 0} \sin\!\left(\dfrac{1}{x}\right)$ does not exist, but $\displaystyle\lim_{x \to 0} x \sin\!\left(\dfrac{1}{x}\right) = 0$. What is the key difference?

---


### Answers

**1.** The table approaches **3**. Algebraically, $\dfrac{\sin3x}{x}=3\cdot\dfrac{\sin3x}{3x}$, and
as $x\to0$ the substitution $u=3x$ also sends $u\to0$, so the second factor $\to1$ and the limit is
$\boxed{3}$. *(Numerically: $2.9552,\ 2.99955,\ 2.9999955$ at $x=0.1,0.01,0.001$.)*

The general rule: $\displaystyle\lim_{x\to0}\frac{\sin(kx)}{x}=k$.

**2. (a)** $\dfrac{x^2-4}{x-2}=x+2$ for $x\neq2$, so the limit is $\boxed{4}$. The function is
undefined *at* 2, which is irrelevant — a limit never consults the value at the point.

**(b)** $\displaystyle\lim_{x\to0^+}\frac{|x|}{x}=\boxed{1}$ and
$\displaystyle\lim_{x\to0^-}\frac{|x|}{x}=\boxed{-1}$. They differ, so the two-sided limit
**does not exist**.

**(c)** Divide through by $x^3$: $\dfrac{4-2/x^2}{7+1/x}\to\boxed{\dfrac47}$. For a ratio of
polynomials of equal degree, the limit at infinity is the ratio of leading coefficients.

**3.** $-x^4\leq x^4\cos(2/x)\leq x^4$, and both bounds $\to0$, so by the Squeeze Theorem the limit
is $\boxed{0}$. The cosine factor is bounded but wildly oscillatory; the $x^4$ crushes it.

**4.** **This exercise cannot be done as stated — the bounds do not pinch.**

$\displaystyle\lim_{x\to1}(3x-1)=2$ but $\displaystyle\lim_{x\to1}(x^2+2)=3$. The Squeeze Theorem
requires the two bounds to share a limit; here they differ by 1. Worse, $x^2+2=3x-1$ would need
$x^2-3x+3=0$, whose discriminant is $-3$ — the two curves **never meet at all**.

All that can be concluded is $2\leq\displaystyle\lim_{x\to1}f(x)\leq3$, *if* the limit exists.

> **Corrected version.** Use bounds that touch at $x=1$:
> $$2x-1\ \leq\ f(x)\ \leq\ x^2 \qquad\text{near } x=1$$
> Both tend to $\boxed{1}$, and the gap $x^2-(2x-1)=(x-1)^2\geq0$ is non-negative for *every* $x$,
> so the ordering is valid everywhere and the bounds pinch exactly at $x=1$. Hence
> $\displaystyle\lim_{x\to1}f(x)=1$.

The lesson is worth keeping: **always check that the two bounds converge to the same value** before
invoking the Squeeze Theorem. Bounds that merely sandwich a function prove nothing on their own.

**5.** $\sin(1/x)$ oscillates between $-1$ and $+1$ infinitely often as $x\to0$, never settling —
so no single value $L$ can be approached, and the limit **does not exist**.

Multiplying by $x$ changes everything: $|x\sin(1/x)|\leq|x|\to0$, so the Squeeze Theorem forces the
limit to $\boxed{0}$. **The key difference is the amplitude.** Oscillation alone does not prevent a
limit — *unbounded-amplitude* oscillation does. Here the envelope $\pm|x|$ shrinks to zero and drags
the whole oscillation with it.

*Next: Tuesday — The Formal $\varepsilon$-$\delta$ Definition and Two Special Trigonometric Limits*
