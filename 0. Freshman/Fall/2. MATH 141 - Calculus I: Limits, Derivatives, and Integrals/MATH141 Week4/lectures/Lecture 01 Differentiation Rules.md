# MATH 141 Calculus I
## Week 4 · Lecture 1 (Tuesday)
### Differentiation Rules: Power, Sum, Product, Quotient

---

**Reading:** Stewart §3.1–3.2 | Spivak Ch. 10

---

## Why Rules?

Computing every derivative from the limit definition is correct but slow. The rules we derive today are theorems — each one is proved from the definition — and together they let you differentiate any combination of polynomials, rationals, and algebraic functions mechanically and rapidly.

The rules are not tricks. They are consequences of limit laws applied to the structure of the difference quotient.

---

## 1. The Constant Rule

$$\frac{d}{dx}[c] = 0$$

**Proof:** $\displaystyle\lim_{h\to0}\frac{c - c}{h} = \lim_{h\to0} 0 = 0$. $\square$

A constant doesn't change — its rate of change is zero. Obvious, but must be stated precisely.

---

## 2. The Power Rule

$$\frac{d}{dx}[x^n] = nx^{n-1}$$

**Valid for all real $n$** (integers, fractions, irrationals — we prove the integer case now, extend later).

**Proof (positive integer $n$):** Use the binomial theorem:
$$(x+h)^n = x^n + nx^{n-1}h + \binom{n}{2}x^{n-2}h^2 + \cdots + h^n$$

So:
$$\frac{(x+h)^n - x^n}{h} = nx^{n-1} + \binom{n}{2}x^{n-2}h + \cdots + h^{n-1}$$

As $h\to 0$, every term with a factor of $h$ vanishes, leaving $nx^{n-1}$. $\square$

**Examples — memorize these cold:**

| $f(x)$ | $f'(x)$ |
|--------|---------|
| $x^5$ | $5x^4$ |
| $x^{1/2} = \sqrt{x}$ | $\frac{1}{2}x^{-1/2} = \frac{1}{2\sqrt{x}}$ |
| $x^{-1} = \frac{1}{x}$ | $-x^{-2} = -\frac{1}{x^2}$ |
| $x^{-3}$ | $-3x^{-4}$ |
| $x^{2/3}$ | $\frac{2}{3}x^{-1/3}$ |
| $x^0 = 1$ | $0$ |

---

## 3. The Constant Multiple Rule

$$\frac{d}{dx}[c\cdot f(x)] = c\cdot f'(x)$$

**Proof:** $\displaystyle\lim_{h\to0}\frac{c\cdot f(x+h)-c\cdot f(x)}{h} = c\lim_{h\to0}\frac{f(x+h)-f(x)}{h} = c\cdot f'(x)$. $\square$

Scalar multiplication passes through the derivative, just as it passes through limits.

---

## 4. The Sum and Difference Rules

$$\frac{d}{dx}[f(x)\pm g(x)] = f'(x) \pm g'(x)$$

**Proof:** Follows directly from the limit sum law applied to the difference quotient. $\square$

**Together with the power and constant rules, this lets us differentiate any polynomial:**

$$\frac{d}{dx}[a_nx^n + \cdots + a_1x + a_0] = na_nx^{n-1} + \cdots + a_1$$

**Example:**
$$\frac{d}{dx}[5x^4 - 3x^2 + 7x - 2] = 20x^3 - 6x + 7$$

---

## 5. The Product Rule

$$\frac{d}{dx}[f(x)\cdot g(x)] = f'(x)g(x) + f(x)g'(x)$$

**Critical misconception:** $(fg)' \neq f'g'$. The derivative of a product is NOT the product of the derivatives.

**Proof — the key algebraic trick (add and subtract $f(x+h)g(x)$):**

$$\frac{f(x+h)g(x+h) - f(x)g(x)}{h}$$

$$= \frac{f(x+h)g(x+h) - f(x+h)g(x) + f(x+h)g(x) - f(x)g(x)}{h}$$

$$= f(x+h)\cdot\frac{g(x+h)-g(x)}{h} + g(x)\cdot\frac{f(x+h)-f(x)}{h}$$

As $h\to 0$: $f(x+h)\to f(x)$ (since differentiable $\Rightarrow$ continuous), so:

$$\to f(x)g'(x) + g(x)f'(x) \quad \square$$

**Memory aid:** "First times derivative of second, plus second times derivative of first."

**Examples:**

**(a)** $\dfrac{d}{dx}[x^3 \cdot \sin x] = 3x^2\sin x + x^3\cos x$

**(b)** $\dfrac{d}{dx}[(x^2+1)(x^3-4x)]$

$= 2x(x^3-4x) + (x^2+1)(3x^2-4)$

$= 2x^4 - 8x^2 + 3x^4 - 4x^2 + 3x^2 - 4$

$= 5x^4 - 9x^2 - 4$

*(Check: expand first, then differentiate directly — same answer.)*

---

## 6. The Quotient Rule

$$\frac{d}{dx}\left[\frac{f(x)}{g(x)}\right] = \frac{f'(x)g(x) - f(x)g'(x)}{[g(x)]^2}$$

**Proof:** Apply the product rule to $f(x) = \left[\dfrac{f}{g}\right]\cdot g(x)$ and solve, or derive directly from the difference quotient (Stewart §3.2 has the full proof).

**Memory aid:** "Lo d-Hi minus Hi d-Lo, over Lo-Lo."
(where Hi = numerator, Lo = denominator)

**Examples:**

**(a)** $\dfrac{d}{dx}\left[\dfrac{x^2+1}{x^3-1}\right] = \dfrac{2x(x^3-1) - (x^2+1)(3x^2)}{(x^3-1)^2}$

$= \dfrac{2x^4 - 2x - 3x^4 - 3x^2}{(x^3-1)^2} = \dfrac{-x^4 - 3x^2 - 2x}{(x^3-1)^2}$

**(b)** $\dfrac{d}{dx}[\tan x] = \dfrac{d}{dx}\left[\dfrac{\sin x}{\cos x}\right] = \dfrac{\cos x\cdot\cos x - \sin x\cdot(-\sin x)}{\cos^2 x} = \dfrac{\cos^2 x + \sin^2 x}{\cos^2 x} = \dfrac{1}{\cos^2 x} = \sec^2 x$

---

## 7. Derivatives of All Six Trig Functions

From the quotient rule and the two special limits $\lim_{x\to0}\frac{\sin x}{x}=1$ and $\lim_{x\to0}\frac{1-\cos x}{x}=0$:

| Function | Derivative | Proof basis |
|----------|-----------|-------------|
| $\sin x$ | $\cos x$ | Special trig limits + definition |
| $\cos x$ | $-\sin x$ | Special trig limits + definition |
| $\tan x$ | $\sec^2 x$ | Quotient rule on $\sin/\cos$ |
| $\sec x$ | $\sec x\tan x$ | Quotient rule on $1/\cos$ |
| $\csc x$ | $-\csc x\cot x$ | Quotient rule on $1/\sin$ |
| $\cot x$ | $-\csc^2 x$ | Quotient rule on $\cos/\sin$ |

**Deriving $(\sin x)' = \cos x$ from the definition:**

$$\frac{d}{dx}[\sin x] = \lim_{h\to0}\frac{\sin(x+h)-\sin x}{h}$$

Use the addition formula $\sin(x+h) = \sin x\cos h + \cos x\sin h$:

$$= \lim_{h\to0}\frac{\sin x\cos h + \cos x\sin h - \sin x}{h}$$

$$= \lim_{h\to0}\left[\sin x\cdot\frac{\cos h - 1}{h} + \cos x\cdot\frac{\sin h}{h}\right]$$

$$= \sin x\cdot(0) + \cos x\cdot(1) = \cos x \quad\square$$

*(This is exactly why we needed $\lim_{h\to0}\frac{\sin h}{h}=1$ and $\lim_{h\to0}\frac{\cos h-1}{h}=0$.)*

---

## 8. Higher-Order Derivatives

The derivative of the derivative is the **second derivative**:

$$f''(x) = \frac{d^2y}{dx^2} = \frac{d}{dx}\left[\frac{dy}{dx}\right]$$

And so on for higher orders:

| Notation | Leibniz | Meaning |
|----------|---------|---------|
| $f'(x)$ | $dy/dx$ | Instantaneous rate of change |
| $f''(x)$ | $d^2y/dx^2$ | Rate of change of the rate (acceleration) |
| $f'''(x)$ | $d^3y/dx^3$ | Jerk (rate of change of acceleration) |
| $f^{(n)}(x)$ | $d^ny/dx^n$ | $n$-th derivative |

**Example:** $f(x) = x^4 - 3x^2 + 5$

$f'(x) = 4x^3 - 6x$

$f''(x) = 12x^2 - 6$

$f'''(x) = 24x$

$f^{(4)}(x) = 24$

$f^{(5)}(x) = 0$

All derivatives of order $\geq 5$ are zero for any degree-4 polynomial.

---

## 9. Summary Table — Rules So Far

| Rule | Formula |
|------|---------|
| Constant | $(c)' = 0$ |
| Power | $(x^n)' = nx^{n-1}$ |
| Constant multiple | $(cf)' = cf'$ |
| Sum/Difference | $(f\pm g)' = f'\pm g'$ |
| Product | $(fg)' = f'g + fg'$ |
| Quotient | $(f/g)' = (f'g - fg')/g^2$ |

**Coming Wednesday:** The Chain Rule — the most important rule of all.

---

## 10. Common Errors

**1. $(fg)' \neq f'g'$ and $(f/g)' \neq f'/g'$.** These are definition-level errors; award no method
marks where they appear. Quick disproof: with $f=g=x$, $(x^2)'=2x$ but $f'g'=1$.

**2. Quotient-rule order.** $\left(\dfrac{f}{g}\right)' = \dfrac{f'g-fg'}{g^2}$ — the **numerator's**
derivative comes first, and the whole numerator is a *difference*, so order matters. Reversing it
flips the sign of every answer. The mnemonic "low d-high minus high d-low, over low squared" fixes
the order.

**3. The power rule needs a constant exponent.** $\frac{d}{dx}x^n = nx^{n-1}$ requires $n$ constant.
It does **not** apply to $x^x$ or $2^x$ — the first needs logarithmic differentiation (Week 5), the
second is $2^x\ln 2$.

**4. Negative and fractional exponents.** $\frac{d}{dx}x^{-1/2} = -\tfrac12x^{-3/2}$: subtracting 1
from $-\tfrac12$ gives $-\tfrac32$, not $-\tfrac12\cdot\tfrac12$. Convert roots and reciprocals to
exponent form *before* differentiating.

**5. Stopping at $f'$ when $f''$ was asked.** And note $f''$ means differentiate twice, not square
the derivative.

---

## Lecture 2 Exercises

1. Differentiate without simplifying first:
   - (a) $f(x) = 3x^5 - 7x^3 + 2x - 11$
   - (b) $g(x) = x^{2/3} + 4x^{-1/2} - 6$
   - (c) $h(x) = (x^2+3)(2x-1)$ — use the product rule, then verify by expanding first

2. Find $\dfrac{d}{dx}\left[\dfrac{x^2 - 2x + 1}{x+3}\right]$.

3. Find equations of all tangent lines to $y = x^3 - 3x$ that are parallel to $y = 9x + 1$.

4. Derive $(\sec x)' = \sec x\tan x$ using the quotient rule on $1/\cos x$.

5. Find $f''(x)$ for $f(x) = x^5 - 10x^3 + 15x$.

6. **(Synthesis)** A function satisfies $f(2) = 3$, $f'(2) = -1$, $g(2) = 4$, $g'(2) = 5$. Find:
   - (a) $(fg)'(2)$
   - (b) $(f/g)'(2)$
   - (c) $(3f - 2g)'(2)$

---

### Answers

**1.**
**(a)** $\boxed{15x^4-21x^2+2}$

**(b)** $\boxed{\tfrac23x^{-1/3}-2x^{-3/2}}$

**(c)** Product rule: $2x(2x-1)+(x^2+3)(2) = 4x^2-2x+2x^2+6 = \boxed{6x^2-2x+6}$.
Expanding first gives $2x^3-x^2+6x-3$, whose derivative is $6x^2-2x+6$ ✓ — the agreement is the
check, and it is worth doing once to see that the product rule is not an approximation.

**2.** $\boxed{\dfrac{(2x-2)(x+3)-(x^2-2x+1)}{(x+3)^2} = \dfrac{x^2+6x-7}{(x+3)^2}}$

Worth noticing: $x^2-2x+1=(x-1)^2$ and the numerator factors as $(x+7)(x-1)$, so the derivative
vanishes at $x=1$ — where the original numerator has a double root and the curve touches zero.

**3.** $y'=3x^2-3$. Parallel to $y=9x+1$ means slope $9$: $3x^2-3=9 \Rightarrow x^2=4
\Rightarrow x=\pm2$.

- $x=2$: $y=8-6=2$, tangent $y-2=9(x-2)$, i.e. $\boxed{y=9x-16}$
- $x=-2$: $y=-8+6=-2$, tangent $y+2=9(x+2)$, i.e. $\boxed{y=9x+16}$

**Two** tangent lines, both verified to pass through their points of tangency. A common slip is
finding $x=\pm2$ and then reporting only one line.

**4.** $\sec x=(\cos x)^{-1}$, so by the quotient rule on $\dfrac{1}{\cos x}$:
$$\frac{d}{dx}\sec x=\frac{0\cdot\cos x-1\cdot(-\sin x)}{\cos^2x}=\frac{\sin x}{\cos^2 x}
=\frac{1}{\cos x}\cdot\frac{\sin x}{\cos x}=\boxed{\sec x\tan x}$$

**5.** $f'(x)=5x^4-30x^2+15$, so $\boxed{f''(x)=20x^3-60x}$.

**6.** With $f(2)=3,\ f'(2)=-1,\ g(2)=4,\ g'(2)=5$:

- **(a)** $(fg)'(2)=f'g+fg' = (-1)(4)+(3)(5)=\boxed{11}$
- **(b)** $(f/g)'(2)=\dfrac{f'g-fg'}{g^2}=\dfrac{(-1)(4)-(3)(5)}{16}=\boxed{-\dfrac{19}{16}}$
- **(c)** $(3f-2g)'(2)=3(-1)-2(5)=\boxed{-13}$

This exercise is the best test in the set: it can only be done by knowing the *rules*, since no
formula for $f$ or $g$ is ever given.

---

*Next: Wednesday — The Chain Rule*
