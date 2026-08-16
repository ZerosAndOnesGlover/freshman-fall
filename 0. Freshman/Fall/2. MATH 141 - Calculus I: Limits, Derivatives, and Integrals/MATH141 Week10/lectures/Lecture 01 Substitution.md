# MATH 141 · Calculus I
## Week 10 · Lecture 1 (Monday)
### Indefinite Integrals, the Net Change Theorem, and the Substitution Rule

**Date:** Monday 26 October 2026 · 11:00–11:50 · Week 10

---

**Reading:** Stewart §5.4–5.5 | Spivak Ch. 13 (§13.3)
**Quiz 10** — this Monday, covers Week 9 (the Fundamental Theorem of Calculus, accumulation functions)

---

## 1. Indefinite Integral Notation — Formalized

Last week we introduced the **indefinite integral** as a family of antiderivatives:

$$\int f(x)\,dx = F(x) + C \quad \text{where } F'(x) = f(x)$$

Note the crucial distinction:

| Notation | Meaning | Result |
|----------|---------|--------|
| $\displaystyle\int_a^b f(x)\,dx$ | Definite integral | A **number** |
| $\displaystyle\int f(x)\,dx$ | Indefinite integral | A **family of functions** |

The indefinite integral is really asking: "what function, when differentiated, gives me this?" It is the operation of *antidifferentiation*, packaged with the "$+C$" to represent every possible answer at once (justified by Week 4's MVT Corollary 2: antiderivatives differ only by a constant).

### The Complete Elementary Antiderivative Table (consolidated from Weeks 2, 3, 6)

$$\int x^n\,dx = \frac{x^{n+1}}{n+1}+C\ (n\neq-1) \qquad \int\frac1x\,dx=\ln|x|+C \qquad \int e^x\,dx=e^x+C$$

$$\int a^x\,dx = \frac{a^x}{\ln a}+C \qquad \int\sin x\,dx=-\cos x+C \qquad \int\cos x\,dx=\sin x+C$$

$$\int\sec^2x\,dx=\tan x+C \qquad \int\csc^2x\,dx=-\cot x+C \qquad \int\sec x\tan x\,dx=\sec x+C$$

$$\int\csc x\cot x\,dx=-\csc x+C \qquad \int\frac{1}{\sqrt{1-x^2}}dx=\arcsin x+C \qquad \int\frac{1}{1+x^2}dx=\arctan x+C$$

---

## 2. The Net Change Theorem

FTC Part 2 has a physically intuitive restatement:

> **Net Change Theorem.** If $F'(x)$ is continuous on $[a,b]$, then:
> $$\int_a^b F'(x)\,dx = F(b)-F(a)$$

**In words:** the integral of a rate of change equals the total (net) change in the quantity itself.

This single idea unifies many application contexts:

| If $F$ represents... | Then $F'$ represents... | And $\int_a^b F'\,dx$ gives... |
|----------------------|--------------------------|--------------------------------|
| Position $s(t)$ | Velocity $v(t)$ | Net displacement |
| Volume of water in a tank | Rate of flow (in/out) | Net change in volume |
| Population | Growth rate | Net change in population |
| Cost | Marginal cost | Net change in cost |
| Charge | Current | Net charge transferred |

### Example 1 — Displacement vs. Distance (revisited from Week 6)

If $v(t)$ is velocity, $\displaystyle\int_a^b v(t)\,dt$ gives **net displacement** — but if velocity changes sign (the object reverses direction), the total **distance traveled** requires:

$$\text{Distance} = \int_a^b |v(t)|\,dt$$

This requires splitting the integral at each point where $v(t)=0$ and taking absolute values of each piece — exactly what we did in Problem Set 6, Part E1(c).

---

## 3. The Substitution Rule — Motivation

Consider $\displaystyle\int 2x\cos(x^2)\,dx$. None of our elementary antiderivative formulas directly apply — the integrand is a **composition** ($\cos$ applied to $x^2$) multiplied by something resembling the derivative of the inside function.

Recall the Chain Rule: $\dfrac{d}{dx}[\sin(x^2)] = \cos(x^2)\cdot2x$.

This means $2x\cos(x^2)$ is EXACTLY the derivative of $\sin(x^2)$! So:

$$\int 2x\cos(x^2)\,dx = \sin(x^2)+C$$

**The Substitution Rule is the Chain Rule, read backward** — exactly as FTC Part 2 is the Power Rule (and other derivative rules) read backward.

---

## 4. The Substitution Rule — Formal Statement

> **Theorem (Substitution Rule).** If $u=g(x)$ is a differentiable function whose range is an interval $I$, and $f$ is continuous on $I$, then:
> $$\int f(g(x))g'(x)\,dx = \int f(u)\,du$$

**Proof:** By the Chain Rule, if $F'=f$, then $\dfrac{d}{dx}[F(g(x))] = F'(g(x))g'(x) = f(g(x))g'(x)$.

So $F(g(x))$ is an antiderivative of $f(g(x))g'(x)$:

$$\int f(g(x))g'(x)\,dx = F(g(x))+C = F(u)+C = \int f(u)\,du \quad\square$$

---

## 5. The Substitution Rule — Practical Method ("u-substitution")

1. **Choose $u$** — typically the "inside" function of a composition, or an expression whose derivative also appears (up to a constant multiple) elsewhere in the integrand
2. **Compute $du = g'(x)\,dx$**
3. **Rewrite the entire integral in terms of $u$** — every $x$ must disappear
4. **Integrate with respect to $u$** using the elementary table
5. **Substitute back** $u = g(x)$ to express the answer in terms of $x$

### Example 2

$$\int 2x\cos(x^2)\,dx$$

Let $u = x^2$. Then $du = 2x\,dx$.

$$= \int \cos(u)\,du = \sin(u)+C = \sin(x^2)+C$$

**Verify by differentiating:** $\dfrac{d}{dx}[\sin(x^2)] = \cos(x^2)\cdot2x$ ✓

### Example 3

$$\int x^2\sqrt{x^3+1}\,dx$$

Let $u = x^3+1$. Then $du = 3x^2\,dx$, so $x^2\,dx = \dfrac{du}{3}$.

$$= \int \sqrt{u}\cdot\frac{du}{3} = \frac13\int u^{1/2}\,du = \frac13\cdot\frac{u^{3/2}}{3/2}+C = \frac29u^{3/2}+C = \frac29(x^3+1)^{3/2}+C$$

### Example 4 — Adjusting for Missing Constants

$$\int \sin(5x)\,dx$$

Let $u=5x$. Then $du = 5\,dx$, so $dx = \dfrac{du}{5}$.

$$= \int\sin(u)\cdot\frac{du}5 = -\frac15\cos(u)+C = -\frac15\cos(5x)+C$$

### Example 5 — Substitution with Algebraic Manipulation

$$\int \frac{x}{\sqrt{1-4x^2}}\,dx$$

Let $u=1-4x^2$. Then $du=-8x\,dx$, so $x\,dx = -\dfrac{du}8$.

$$= \int\frac{1}{\sqrt u}\cdot\left(-\frac{du}8\right) = -\frac18\int u^{-1/2}\,du = -\frac18\cdot2u^{1/2}+C = -\frac14\sqrt{1-4x^2}+C$$

### Example 6 — Substitution with a Trig Identity Needed First

$$\int \tan x\,dx$$

Rewrite: $\tan x = \dfrac{\sin x}{\cos x}$.

Let $u=\cos x$. Then $du=-\sin x\,dx$, so $\sin x\,dx = -du$.

$$\int\frac{\sin x}{\cos x}\,dx = \int\frac{-du}{u} = -\ln|u|+C = -\ln|\cos x|+C$$

Using the identity $-\ln|\cos x| = \ln|\sec x|$ (since $\sec x = 1/\cos x$):

$$\int\tan x\,dx = \ln|\sec x|+C$$

This is a standard result worth memorizing, and it fills a genuine gap in our antiderivative table.

---

## 6. Choosing the Right Substitution — Pattern Recognition

The skill of substitution is fundamentally about **pattern recognition**. Look for:

| Pattern in integrand | Try $u=$ |
|----------------------|----------|
| $f(g(x))\cdot g'(x)$ | $u=g(x)$ |
| Something raised to a power, times its "almost-derivative" | $u=$ the base |
| $\dfrac{g'(x)}{g(x)}$ | $u=g(x)$ (gives $\ln|u|$) |
| Trig function of a linear expression $ax+b$ | $u=ax+b$ |
| Expression under a root, times something resembling its derivative | $u=$ the expression under the root |

### Example 7 — Recognizing the $g'/g$ Pattern

$$\int \frac{2x+3}{x^2+3x+1}\,dx$$

Notice: the derivative of $x^2+3x+1$ is $2x+3$ — EXACTLY the numerator!

Let $u=x^2+3x+1$. Then $du=(2x+3)\,dx$.

$$= \int\frac{du}{u} = \ln|u|+C = \ln|x^2+3x+1|+C$$

This "$g'/g$" pattern always gives a logarithm and appears constantly.

---

## 7. When Substitution Doesn't Obviously Work — Trying Multiple Substitutions

### Example 8

$$\int x\sqrt{x+1}\,dx$$

Let $u = x+1$, so $x = u-1$ and $du = dx$.

$$= \int (u-1)\sqrt u\,du = \int(u^{3/2}-u^{1/2})\,du = \frac25u^{5/2}-\frac23u^{3/2}+C$$

$$= \frac25(x+1)^{5/2}-\frac23(x+1)^{3/2}+C$$

**Key insight:** here we substituted for the ENTIRE expression under the root, and then solved for the leftover $x$ in terms of $u$ — a technique that extends the basic pattern-matching approach to more complex integrands.

---

## 8. CS Connection — Substitution as Change of Variables

The Substitution Rule is the calculus instance of a much more general and powerful idea: **change of variables**. This concept recurs throughout computer science and applied mathematics:

- **Coordinate transformations in computer graphics:** converting between world space, object space, and screen space is a change-of-variables operation, and Jacobian determinants (the multivariable generalization of $du = g'(x)\,dx$) appear when transforming volumes/areas between coordinate systems.
- **Probability distributions:** when a random variable $Y=g(X)$ is defined in terms of another, the probability density of $Y$ is computed using a substitution-rule-like formula involving $|g'(x)|^{-1}$ (the "change of variables formula" for densities).
- **Normalizing data in machine learning:** feature scaling and normalization are literal substitutions $u = \dfrac{x-\mu}{\sigma}$ designed to simplify the "integrand" (loss landscape) that optimization algorithms must navigate.

The core principle — re-expressing a hard problem in new coordinates where it becomes simple, then translating the answer back — is one of the most powerful and recurring ideas in all of quantitative science, and the Substitution Rule is your first rigorous encounter with it.

---

## Lecture 1 Exercises

1. Evaluate using substitution:
   - (a) $\displaystyle\int (3x+1)^5\,dx$
   - (b) $\displaystyle\int x^2 e^{x^3}\,dx$
   - (c) $\displaystyle\int \frac{\ln x}{x}\,dx$
   - (d) $\displaystyle\int \sin^3x\cos x\,dx$
   - (e) $\displaystyle\int \frac{e^{2x}}{1+e^{2x}}\,dx$

2. Use the $g'/g$ logarithm pattern to evaluate:
   - (a) $\displaystyle\int \frac{x}{x^2+4}\,dx$
   - (b) $\displaystyle\int \cot x\,dx$ *(rewrite as $\cos x/\sin x$ first)*
   - (c) $\displaystyle\int \frac{\sec^2x}{\tan x}\,dx$

3. Use the "solve for leftover $x$" technique (Example 8) to evaluate $\displaystyle\int x^2\sqrt{x-3}\,dx$.

4. A tank's water volume changes at rate $\dfrac{dV}{dt} = 20-3t$ liters/min for $t\in[0,5]$ minutes. Using the Net Change Theorem, find the net change in volume over this time period.

5. **(Conceptual)** Explain, using the Chain Rule, why the Substitution Rule is valid. Specifically, show that if you differentiate the RIGHT-hand side of the Substitution Rule formula (after substituting back $u=g(x)$), you recover the original integrand $f(g(x))g'(x)$.

---


### Answers

**1. (a)** $u=3x+1$: $\boxed{\dfrac{(3x+1)^6}{18}+C}$
**(b)** $u=x^3$: $\boxed{\dfrac{e^{x^3}}{3}+C}$
**(c)** $u=\ln x$: $\boxed{\dfrac{(\ln x)^2}{2}+C}$
**(d)** $u=\sin x$: $\boxed{\dfrac{\sin^4x}{4}+C}$
**(e)** $u=1+e^{2x}$: $\boxed{\tfrac12\ln\!\left(1+e^{2x}\right)+C}$

**2.** All three are the pattern $\displaystyle\int\frac{g'}{g}=\ln|g|+C$.

**(a)** $\boxed{\tfrac12\ln(x^2+4)+C}$ — no absolute value needed, since $x^2+4>0$ always.
**(b)** $\displaystyle\int\frac{\cos x}{\sin x}\,dx=\boxed{\ln|\sin x|+C}$
**(c)** $\displaystyle\int\frac{\sec^2x}{\tan x}\,dx=\boxed{\ln|\tan x|+C}$

**Keep the absolute value** wherever the inner function can be negative — dropping it silently
restricts the domain of your antiderivative.

**3.** $u=x-3$, so $x=u+3$ and $x^2=(u+3)^2=u^2+6u+9$:
$$\int x^2\sqrt{x-3}\,dx=\int\left(u^2+6u+9\right)u^{1/2}\,du=\int\left(u^{5/2}+6u^{3/2}+9u^{1/2}\right)du$$
$$=\boxed{\tfrac27(x-3)^{7/2}+\tfrac{12}{5}(x-3)^{5/2}+6(x-3)^{3/2}+C}$$

The technique — **solve the substitution for $x$ and rewrite the leftover factor** — rescues
integrals where $g'$ is not present as a factor. It works whenever $u=g(x)$ can be inverted.

**4.** Net Change Theorem: the integral of a rate is the net change.
$$\Delta V=\int_0^5(20-3t)\,dt=\left[20t-\tfrac32t^2\right]_0^5=100-37.5=\boxed{+62.5\ \text{litres}}$$
Note the rate turns **negative** after $t=\tfrac{20}{3}\approx6.7$ min — outside this window, so the
tank fills throughout. Had the interval extended past that, the *net* change would still be the
integral, but total water added and removed would require $\int|dV/dt|$.

**5.** Let $F$ be an antiderivative of $f$, so the Substitution Rule claims
$$\int f(g(x))g'(x)\,dx = F(g(x))+C$$
Differentiate the right-hand side by the **chain rule**:
$$\frac{d}{dx}\left[F(g(x))+C\right]=F'(g(x))\cdot g'(x)=f(g(x))\,g'(x)$$
which is precisely the integrand. $\blacksquare$

**Substitution is the chain rule read backwards** — the $g'(x)\,dx$ in the integral is exactly the
factor the chain rule produces going forward. That is why it is the *only* integration technique
that follows directly from a differentiation rule, and why spotting "an inner function whose
derivative is present" is the whole skill.

*Next: Tuesday — Substitution in Definite Integrals; Symmetry*
