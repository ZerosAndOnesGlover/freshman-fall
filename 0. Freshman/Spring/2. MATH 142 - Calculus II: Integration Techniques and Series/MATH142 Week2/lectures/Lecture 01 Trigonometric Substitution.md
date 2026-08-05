# MATH 142 · Calculus II
## Week 2 · Lecture 1 (Monday)
### Trigonometric Substitution

---

**Reading:** Stewart §7.3 | Apostol Ch. 6 §6.13
**Quiz 02** — this Monday, **covers Week 1** (integration by parts, reduction formulas, trigonometric integrals)

---

## 1. The Idea: Substitution, Run Backwards

Ordinary substitution replaces a complicated expression with a single letter, making things simpler. **Today we do the reverse** — replace the simple letter $x$ with a complicated trigonometric expression, deliberately.

Why would that help? Because of the Pythagorean identities. Consider

$$\int\sqrt{1-x^2}\,dx$$

The square root blocks every technique so far. But if $x = \sin\theta$, then

$$1 - x^2 = 1-\sin^2\theta = \cos^2\theta \implies \sqrt{1-x^2} = |\cos\theta|$$

**The square root disappears.** That is the whole idea: the identity converts a sum or difference of squares into a perfect square, and a perfect square has no radical.

---

## 2. The Three Patterns

| Expression | Substitute | Because | Range of $\theta$ |
|---|---|---|---|
| $\sqrt{a^2-x^2}$ | $x = a\sin\theta$ | $a^2 - a^2\sin^2\theta = a^2\cos^2\theta$ | $[-\tfrac\pi2,\tfrac\pi2]$ |
| $\sqrt{a^2+x^2}$ | $x = a\tan\theta$ | $a^2+a^2\tan^2\theta = a^2\sec^2\theta$ | $(-\tfrac\pi2,\tfrac\pi2)$ |
| $\sqrt{x^2-a^2}$ | $x = a\sec\theta$ | $a^2\sec^2\theta - a^2 = a^2\tan^2\theta$ | $[0,\tfrac\pi2)\cup[\pi,\tfrac{3\pi}2)$ |

**Memorise the *reason*, not the table.** Each row is one Pythagorean identity: $\sin^2+\cos^2=1$, $1+\tan^2=\sec^2$, $\sec^2-1=\tan^2$. Given the identity, the substitution is forced.

### Why the ranges matter

Restricting $\theta$ makes the substitution **invertible** and fixes the sign of the radical. On $[-\tfrac\pi2,\tfrac\pi2]$ we have $\cos\theta\ge0$, so

$$\sqrt{a^2-x^2} = a|\cos\theta| = a\cos\theta$$

**without an absolute value.** Skip this step and you will eventually produce an answer that is right in magnitude and wrong in sign on half its domain. It is the most common silent error in the technique.

---

## 3. The Procedure

1. **Identify** which of the three patterns is present.
2. **Substitute** $x$ and compute $dx$.
3. **Simplify** the radical using the identity — drop the absolute value, justified by the range.
4. **Integrate** — the result is a trigonometric integral from Week 1.
5. **Convert back to $x$** using a reference triangle. *(Or, for a definite integral, change the limits at step 2 and skip this.)*

**Step 5 is where the marks go.**

---

## 4. Worked Examples

### Example 1 — $\int\sqrt{1-x^2}\,dx$

Pattern $\sqrt{a^2-x^2}$ with $a=1$: put $x=\sin\theta$, $dx = \cos\theta\,d\theta$, $\theta\in[-\tfrac\pi2,\tfrac\pi2]$.

$$\int\sqrt{1-\sin^2\theta}\,\cos\theta\,d\theta = \int\cos^2\theta\,d\theta$$

**This is a Week 1 integral** — both powers even, so use the half-angle identity:

$$= \int\frac{1+\cos2\theta}{2}d\theta = \frac\theta2 + \frac{\sin2\theta}{4} = \frac\theta2+\frac{\sin\theta\cos\theta}{2}$$

*(using $\sin2\theta = 2\sin\theta\cos\theta$)*

**Converting back.** From $x=\sin\theta$: $\theta = \arcsin x$, and $\cos\theta = \sqrt{1-x^2}$ (positive on our range).

$$\boxed{\int\sqrt{1-x^2}\,dx = \frac{\arcsin x}{2}+\frac{x\sqrt{1-x^2}}{2}+C}$$

*Verified symbolically.*

**Sanity check:** $\int_0^1\sqrt{1-x^2}\,dx$ is a quarter of the unit disc, so it should be $\tfrac\pi4$. Our formula gives $\tfrac{\arcsin 1}{2}+0 = \tfrac\pi4$ ✓. *Verified symbolically.*

### Example 2 — $\int\frac{x^2}{\sqrt{9-x^2}}\,dx$

Pattern $\sqrt{a^2-x^2}$ with $a = 3$: $x = 3\sin\theta$, $dx = 3\cos\theta\,d\theta$, $\sqrt{9-x^2}=3\cos\theta$.

$$\int\frac{9\sin^2\theta}{3\cos\theta}\cdot3\cos\theta\,d\theta = 9\int\sin^2\theta\,d\theta = 9\left(\frac\theta2 - \frac{\sin\theta\cos\theta}{2}\right)$$

**Back to $x$:** $\sin\theta = \tfrac x3$, $\theta = \arcsin\tfrac x3$, $\cos\theta = \tfrac{\sqrt{9-x^2}}{3}$.

$$\boxed{= \frac92\arcsin\frac x3 - \frac{x\sqrt{9-x^2}}{2}+C}$$

*Verified symbolically.*

### Example 3 — $\int\frac{dx}{(x^2+4)^{3/2}}$

Pattern $\sqrt{a^2+x^2}$ with $a=2$: $x = 2\tan\theta$, $dx = 2\sec^2\theta\,d\theta$.

$$(x^2+4)^{3/2} = \big(4\sec^2\theta\big)^{3/2} = 8\sec^3\theta$$

$$\int\frac{2\sec^2\theta}{8\sec^3\theta}d\theta = \frac14\int\frac{d\theta}{\sec\theta} = \frac14\int\cos\theta\,d\theta = \frac{\sin\theta}{4}$$

**Back to $x$.** Reference triangle for $\tan\theta = \tfrac x2$: opposite $x$, adjacent $2$, hypotenuse $\sqrt{x^2+4}$. So $\sin\theta = \tfrac{x}{\sqrt{x^2+4}}$.

$$\boxed{\int\frac{dx}{(x^2+4)^{3/2}} = \frac{x}{4\sqrt{x^2+4}}+C}$$

*Verified symbolically.*

**Notice how clean that answer is** — no arctangent, no logarithm. A substitution that looked like it would produce a mess produced an algebraic function. This is typical of the $(\ )^{3/2}$ family.

### Example 4 — $\int\frac{dx}{\sqrt{x^2-9}}$

Pattern $\sqrt{x^2-a^2}$ with $a=3$: $x = 3\sec\theta$, $dx = 3\sec\theta\tan\theta\,d\theta$, and $\sqrt{x^2-9}=3\tan\theta$ on the chosen range.

$$\int\frac{3\sec\theta\tan\theta}{3\tan\theta}d\theta = \int\sec\theta\,d\theta = \ln|\sec\theta+\tan\theta|$$

**Back to $x$:** $\sec\theta = \tfrac x3$, $\tan\theta = \tfrac{\sqrt{x^2-9}}{3}$:

$$= \ln\left|\frac{x+\sqrt{x^2-9}}{3}\right| = \boxed{\ln\big|x+\sqrt{x^2-9}\big| + C}$$

absorbing $-\ln3$ into the constant. *Verified symbolically.*

> **The $\int\sec\theta\,d\theta$ from Week 1 does real work here.** That is why it was in the
> catalogue — the secant substitution produces it constantly.

---

## 5. Reference Triangles

Converting back is easier drawn than remembered. The substitution states one trigonometric ratio; **draw the right triangle with those two sides, get the third from Pythagoras, and read off whatever you need.**

| Substitution | Opposite | Adjacent | Hypotenuse |
|---|---|---|---|
| $x = a\sin\theta$ | $x$ | $\sqrt{a^2-x^2}$ | $a$ |
| $x = a\tan\theta$ | $x$ | $a$ | $\sqrt{a^2+x^2}$ | 
| $x = a\sec\theta$ | $\sqrt{x^2-a^2}$ | $a$ | $x$ |

**In each case the radical is one of the three sides**, which is exactly why the substitution removes it.

---

## 6. Definite Integrals: Change the Limits Instead

For a definite integral you may convert the limits at the start and never return to $x$ — no triangle needed.

$$\int_0^2\sqrt{4-x^2}\,dx$$

With $x=2\sin\theta$: $x=0\Rightarrow\theta=0$; $x=2\Rightarrow\sin\theta=1\Rightarrow\theta=\tfrac\pi2$.

$$= \int_0^{\pi/2}2\cos\theta\cdot2\cos\theta\,d\theta = 4\int_0^{\pi/2}\cos^2\theta\,d\theta = 4\cdot\frac\pi4 = \boxed{\pi}$$

*(using $I_2 = \pi/4$ from Week 1's table)*

*Verified symbolically: exactly $\pi$.*

**Check:** this is a quarter disc of radius 2, area $\tfrac14\pi(2)^2 = \pi$ ✓.

> **On a definite integral, changing the limits is almost always less work and less risk.** Use it.

---

## 7. A Warning About the Machine

$$\int\frac{\sqrt{x^2-9}}{x}\,dx = \sqrt{x^2-9} - 3\arccos\frac3x + C \qquad (x>3)$$

Asked for this without being told $x>3$, a computer algebra system returns a `Piecewise` expression several lines long, involving imaginary units and inverse hyperbolic functions — because it is trying to be correct on the complex plane and on both branches $x>3$ and $x<-3$.

**Told that $x$ is positive, it produces the boxed answer immediately.** Differentiating the boxed form confirms it on $x>3$, and numerical differentiation at $x = 3.5, 5, 9$ agrees to 16 significant figures.

> **The lesson, for the third week running:** state your domain. The machine will not assume one, and
> its refusal to assume looks like a wrong answer. **Differentiating your own answer settles it.**

---

## 8. What To Take From This Lecture

1. **Three patterns, three identities.** $\sqrt{a^2-x^2}\to a\sin\theta$; $\sqrt{a^2+x^2}\to a\tan\theta$; $\sqrt{x^2-a^2}\to a\sec\theta$.
2. **The range of $\theta$ is what lets you drop the absolute value.** State it.
3. **What comes out is a Week 1 trigonometric integral.** Last week was the preparation for this one.
4. **Draw the reference triangle** to convert back.
5. **On definite integrals, change the limits** and skip the conversion entirely.

---

*Next: Tuesday — Completing the Square, and Making an Integral Fit a Pattern*
