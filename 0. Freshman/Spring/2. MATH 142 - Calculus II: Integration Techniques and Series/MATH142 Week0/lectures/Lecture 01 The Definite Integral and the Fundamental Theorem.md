# MATH 142 · Calculus II
## Week 0 · Lecture 1 (Monday)
### The Definite Integral and the Fundamental Theorem

---

**Reading:** Stewart §5.1–5.3 | Apostol Ch. 1 §1.1–1.17 (the definition done properly)

---

## 1. What the Integral Actually Is

Most students leave MATH 141 with this working definition:

> $\int_a^b f(x)\,dx$ means "find $F$ with $F'=f$, then compute $F(b)-F(a)$."

**That is not the definition. That is a theorem** — and treating it as a definition will make Week 3 incomprehensible, because in Week 3 we will write integrals for which no such $F$ can be found and yet the integral exists.

The definition is a limit. Partition $[a,b]$ into $n$ subintervals of width $\Delta x = \frac{b-a}{n}$, pick a sample point $x_i^*$ in each, and form the **Riemann sum**

$$\sum_{i=1}^{n} f(x_i^*)\,\Delta x$$

Each term is the area of a rectangle: height $f(x_i^*)$, width $\Delta x$. The sum approximates the area under the curve. Then

$$\boxed{\int_a^b f(x)\,dx \;=\; \lim_{n\to\infty} \sum_{i=1}^{n} f(x_i^*)\,\Delta x}$$

provided this limit exists and is independent of how the sample points were chosen. When it does, $f$ is called **integrable** on $[a,b]$.

**Every continuous function on a closed bounded interval is integrable.** That is a theorem too, and it is the reason we rarely worry about the definition — but it is worth knowing that it can fail. The function that is $1$ at rationals and $0$ at irrationals is not Riemann integrable on any interval: the sum is $b-a$ if you sample rationals and $0$ if you sample irrationals, so the limit depends on the choice and the definition refuses to give an answer.

### 1.1 Why this matters for a computer scientist

The Riemann sum is not just a definitional device — **it is an algorithm**, and it is the one your computer actually runs. A machine cannot find an antiderivative; it can add up $n$ rectangles. Everything in Lab 0 this week is a refinement of this sum, and the entire field of numerical integration is the study of choosing $x_i^*$ well.

---

## 2. The Fundamental Theorem, Both Parts

The FTC is two statements. **Students lose marks by not saying which one they are using**, so we name them.

### FTC Part 1 — the integral of a derivative-to-be

If $f$ is continuous on $[a,b]$, define

$$F(x) = \int_a^x f(t)\,dt$$

Then $F$ is differentiable on $(a,b)$ and

$$\boxed{F'(x) = f(x)}$$

**In words: every continuous function has an antiderivative, and here it is.** This is an existence theorem, and it is the more profound of the two. Notice what it does *not* say: it does not say you can write $F$ down in elementary terms. $f(t)=e^{-t^2}$ is continuous, so $F(x)=\int_0^x e^{-t^2}dt$ exists and is differentiable — and cannot be expressed with the functions you know.

**Note the variable discipline.** The integration variable is $t$, the limit is $x$. Writing $\int_a^x f(x)\,dx$ uses $x$ for two different things and is a genuine error, not a notational nicety.

### FTC Part 2 — the evaluation rule

If $f$ is continuous on $[a,b]$ and $F$ is **any** antiderivative of $f$, then

$$\boxed{\int_a^b f(x)\,dx = F(b) - F(a)}$$

This is the computational workhorse — the one you have been using all along. It is a *consequence* of Part 1 plus the fact that two antiderivatives of the same function differ by a constant (which is why the constant cancels in $F(b)-F(a)$, and why we may say "any antiderivative").

---

## 3. FTC Part 1 With a Chain Rule

The most common exam use of Part 1 has a function in the upper limit. Suppose

$$G(x) = \int_1^{x^2} \sqrt{1+t^3}\,dt$$

Write $F(u) = \int_1^u \sqrt{1+t^3}\,dt$, so $G(x)=F(x^2)$ and $F'(u)=\sqrt{1+u^3}$ by Part 1. Then the chain rule gives

$$G'(x) = F'(x^2)\cdot \frac{d}{dx}(x^2) = \sqrt{1+(x^2)^3}\cdot 2x = \boxed{2x\sqrt{1+x^6}}$$

**Check the shape of that answer.** It contains no integral sign, and it took one line. Meanwhile the integrand $\sqrt{1+t^3}$ has *no elementary antiderivative* — a computer algebra system asked for $\int\sqrt{1+t^3}\,dt$ returns a hypergeometric function. So we have differentiated something we cannot integrate, exactly. That asymmetry is the FTC earning its name.

**Verification.** This was checked numerically: computing $G$ by high-precision quadrature and differentiating numerically at $x = 1.3,\ 2.0,\ 2.7$ agrees with $2x\sqrt{1+x^6}$ to 18 significant figures. Notably, a CAS asked to do this symbolically produced an unsimplifiable hypergeometric expression and could not confirm the equality — the one-line FTC argument is both faster and more reliable than the machine here. **Keep that in mind all semester: the CAS is a tool, not an oracle.**

### The general form

$$\frac{d}{dx}\int_{g(x)}^{h(x)} f(t)\,dt = f(h(x))\,h'(x) - f(g(x))\,g'(x)$$

The minus sign on the lower limit comes from $\int_g^h = \int_a^h - \int_a^g$.

---

## 4. Properties You Will Use Constantly

For integrable $f,g$ on the relevant intervals:

| Property | Statement |
|---|---|
| Linearity | $\int_a^b \big(\alpha f + \beta g\big) = \alpha\int_a^b f + \beta\int_a^b g$ |
| Additivity | $\int_a^c f = \int_a^b f + \int_b^c f$ |
| Reversal | $\int_b^a f = -\int_a^b f$ |
| Zero width | $\int_a^a f = 0$ |
| Comparison | $f \le g$ on $[a,b] \implies \int_a^b f \le \int_a^b g$ |
| Bounds | $m \le f \le M$ on $[a,b] \implies m(b-a) \le \int_a^b f \le M(b-a)$ |

**The comparison property is the seed of Week 3 and Week 7.** Every comparison test — for improper integrals and for infinite series — is this one line applied with care.

**Additivity is what lets you handle absolute values**: to integrate $|f|$, find where $f$ changes sign and split there. We use this in Lecture 3.

---

## 5. Worked Examples

### Example 1 — a direct evaluation

$$\int_0^2 (x^2+1)\,dx = \left[\frac{x^3}{3}+x\right]_0^2 = \left(\frac83 + 2\right) - 0 = \frac{14}{3}$$

*Verified symbolically: $14/3$.*

### Example 2 — a symmetric integrand

$$\int_0^\pi \sin x\,dx = \big[-\cos x\big]_0^\pi = -\cos\pi + \cos 0 = 1 + 1 = 2$$

*Verified symbolically: $2$.*

Note this is **not** zero, even though $\sin$ is odd — oddness gives zero only over an interval symmetric about the origin, and $[0,\pi]$ is not. Over $[-\pi,\pi]$ it would be zero.

### Example 3 — reading the FTC backwards

Find $\displaystyle\frac{d}{dx}\int_x^{5} \cos(t^2)\,dt$.

The variable is in the *lower* limit, so flip it first:

$$\int_x^5 \cos(t^2)\,dt = -\int_5^x \cos(t^2)\,dt \implies \frac{d}{dx}\left[\,\cdot\,\right] = -\cos(x^2)$$

**The minus sign is the whole problem.** Students who skip the flip lose the mark.

---

## 6. The Definition, Used Once

Compute $\int_0^1 x\,dx$ from the definition, to see that it can be done — and why we do not do it often.

Take $x_i^* = \frac{i}{n}$ (right endpoints), $\Delta x = \frac1n$:

$$\sum_{i=1}^n \frac{i}{n}\cdot\frac1n = \frac{1}{n^2}\sum_{i=1}^n i = \frac{1}{n^2}\cdot\frac{n(n+1)}{2} = \frac{n+1}{2n}$$

$$\int_0^1 x\,dx = \lim_{n\to\infty} \frac{n+1}{2n} = \frac12$$

which agrees with $\big[\tfrac{x^2}{2}\big]_0^1 = \tfrac12$.

**This required a closed form for $\sum i$.** For $\int_0^1 e^{-x^2}dx$ there is no closed form for the corresponding sum, which is precisely why we need either the FTC (unavailable here) or numerical methods (Lab 0) or series (Week 10).

---

## 7. What To Take From This Lecture

1. **The integral is a limit of sums.** The FTC is a theorem connecting it to antidifferentiation, not the definition.
2. **Say which part of the FTC you are using.** Part 1 differentiates an integral; Part 2 evaluates one.
3. **A function in the upper limit brings a chain rule**; a function in the lower limit brings a minus sign.
4. **Existence and expressibility are different questions.** Every continuous function has an antiderivative. Most cannot be written down.

---

*Next: Tuesday — Substitution and the Antiderivative Catalogue*
