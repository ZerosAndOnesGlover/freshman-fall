# MATH 141 · Calculus I
## Week 5 · Lecture 2 (Tuesday)
### Derivatives of Logarithms, Logarithmic Differentiation, and Inverse Trig Functions

**Date:** Tuesday 22 September 2026 · 11:00–11:50 · Week 5

---

**Reading:** Stewart §3.6, §3.5 (inverse trig) | Spivak Ch. 15 (logarithm and exponential)

---

## 1. The Derivative of $\ln x$

**Claim:** $\dfrac{d}{dx}[\ln x] = \dfrac{1}{x}$ for $x > 0$.

**Proof via implicit differentiation:**

Let $y = \ln x$. Then $e^y = x$.

Differentiate implicitly: $e^y \cdot \dfrac{dy}{dx} = 1$, so $\dfrac{dy}{dx} = \dfrac{1}{e^y} = \dfrac{1}{x}$. $\square$

This is remarkable: the derivative of the logarithm is a rational function $1/x$. No transcendental functions appear. This is one of the reasons $\ln$ is so central in calculus.

**With the chain rule:**
$$\frac{d}{dx}[\ln(g(x))] = \frac{g'(x)}{g(x)}$$

**Examples:**
$$\frac{d}{dx}[\ln(x^2+1)] = \frac{2x}{x^2+1}$$
$$\frac{d}{dx}[\ln(\sin x)] = \frac{\cos x}{\sin x} = \cot x$$
$$\frac{d}{dx}[\ln|x|] = \frac{1}{x} \quad \text{(for } x \neq 0\text{)}$$

The last result extends the domain: $\ln|x|$ is defined for all $x \neq 0$, and its derivative is $1/x$ everywhere in its domain.

---

## 2. Derivatives of General Logarithms

For $\log_a x = \dfrac{\ln x}{\ln a}$ (change of base):

$$\frac{d}{dx}[\log_a x] = \frac{1}{x \ln a}$$

Note: when $a = e$, $\ln a = 1$, recovering $(d/dx)[\ln x] = 1/x$.

---

## 3. Logarithmic Differentiation

**When to use it:** Functions of the form $[f(x)]^{g(x)}$ — variable base AND variable exponent — which are neither pure power functions nor pure exponentials.

**The method:**
1. Take $\ln$ of both sides: $\ln y = g(x)\ln f(x)$
2. Differentiate implicitly: $\dfrac{y'}{y} = [\text{derivative of right side}]$
3. Multiply both sides by $y$: $y' = y \cdot [\text{derivative of right side}]$
4. Substitute back $y = f(x)^{g(x)}$

### Example 1 — Variable base and exponent: $y = x^x$

$$\ln y = x \ln x$$

$$\frac{y'}{y} = \ln x + x \cdot \frac{1}{x} = \ln x + 1$$

$$y' = x^x(\ln x + 1)$$

Note: neither the power rule (which requires constant exponent) nor the exponential rule (which requires constant base) applies here. Logarithmic differentiation is the only elementary method.

### Example 2 — $y = x^{\sin x}$

$$\ln y = \sin x \cdot \ln x$$

$$\frac{y'}{y} = \cos x \cdot \ln x + \sin x \cdot \frac{1}{x}$$

$$y' = x^{\sin x}\left(\cos x \ln x + \frac{\sin x}{x}\right)$$

### Example 3 — Simplifying products/quotients

Logarithmic differentiation also simplifies messy products and quotients:

$$y = \frac{x^3\sqrt{x^2+1}}{(2x-1)^4}$$

$$\ln y = 3\ln x + \frac{1}{2}\ln(x^2+1) - 4\ln(2x-1)$$

$$\frac{y'}{y} = \frac{3}{x} + \frac{x}{x^2+1} - \frac{8}{2x-1}$$

$$y' = \frac{x^3\sqrt{x^2+1}}{(2x-1)^4}\left(\frac{3}{x} + \frac{x}{x^2+1} - \frac{8}{2x-1}\right)$$

This is far cleaner than applying quotient and product rules repeatedly.

---

## 4. The Number $e$ Defined Precisely

The number $e$ is often defined as $\lim_{n\to\infty}\left(1+\frac{1}{n}\right)^n$. We can now connect this to the derivative.

**Derivation:** We require $\frac{d}{dx}[e^x]\big|_{x=0} = 1$, i.e., $\lim_{h\to0}\frac{e^h-1}{h} = 1$.

This forces $e = \lim_{h\to0}(1+h)^{1/h}$. Setting $h = 1/n$: $e = \lim_{n\to\infty}\left(1+\frac{1}{n}\right)^n \approx 2.71828...$

More general form (set $h = x/n$):
$$e^x = \lim_{n\to\infty}\left(1+\frac{x}{n}\right)^n$$

This limit appears in compound interest: $\$P$ compounded continuously at rate $r$ for $t$ years gives $Pe^{rt}$.

---

## 5. Derivatives of Inverse Trigonometric Functions

Using the implicit differentiation method from Monday's lecture:

### $\arcsin x$ (derived Monday):
$$\frac{d}{dx}[\arcsin x] = \frac{1}{\sqrt{1-x^2}}, \quad x \in (-1,1)$$

### $\arccos x$:

Let $y = \arccos x$, so $\cos y = x$, $y \in [0,\pi]$.

Differentiate: $-\sin y \cdot y' = 1$, so $y' = -\dfrac{1}{\sin y}$.

From $\cos y = x$: $\sin y = \sqrt{1-\cos^2 y} = \sqrt{1-x^2}$ (positive since $y \in [0,\pi]$).

$$\frac{d}{dx}[\arccos x] = \frac{-1}{\sqrt{1-x^2}}$$

Note: $\frac{d}{dx}[\arcsin x] + \frac{d}{dx}[\arccos x] = 0$. This is because $\arcsin x + \arccos x = \pi/2$ (a constant), so their sum differentiates to zero.

### $\arctan x$:

Let $y = \arctan x$, so $\tan y = x$, $y \in (-\pi/2, \pi/2)$.

Differentiate: $\sec^2 y \cdot y' = 1$, so $y' = \cos^2 y$.

From $\tan y = x$: using the identity $\sec^2 y = 1 + \tan^2 y = 1 + x^2$, we get $\cos^2 y = \dfrac{1}{1+x^2}$.

$$\frac{d}{dx}[\arctan x] = \frac{1}{1+x^2}$$

### $\text{arcsec}\, x$:

Let $y = \text{arcsec}\, x$, so $\sec y = x$, $y \in [0,\pi/2)\cup(\pi/2,\pi]$.

Differentiate: $\sec y \tan y \cdot y' = 1$, so $y' = \dfrac{1}{\sec y \tan y}$.

Using $\sec y = x$ and $\tan y = \sqrt{\sec^2 y - 1} = \sqrt{x^2-1}$ (for $|x|>1$):

$$\frac{d}{dx}[\text{arcsec}\, x] = \frac{1}{|x|\sqrt{x^2-1}}$$

---

## 6. Complete Inverse Trig Derivative Table

| Function | Derivative | Domain |
|----------|-----------|--------|
| $\arcsin x$ | $\dfrac{1}{\sqrt{1-x^2}}$ | $(-1,1)$ |
| $\arccos x$ | $\dfrac{-1}{\sqrt{1-x^2}}$ | $(-1,1)$ |
| $\arctan x$ | $\dfrac{1}{1+x^2}$ | $\mathbb{R}$ |
| $\text{arccot}\, x$ | $\dfrac{-1}{1+x^2}$ | $\mathbb{R}$ |
| $\text{arcsec}\, x$ | $\dfrac{1}{|x|\sqrt{x^2-1}}$ | $|x|>1$ |
| $\text{arccsc}\, x$ | $\dfrac{-1}{|x|\sqrt{x^2-1}}$ | $|x|>1$ |

**Pattern:** Each inverse trig derivative pairs with a sign-flipped partner, just as $\arcsin + \arccos = \pi/2$.

**With the chain rule:**
$$\frac{d}{dx}[\arctan(g(x))] = \frac{g'(x)}{1+[g(x)]^2}$$

**Example:** $\dfrac{d}{dx}[\arctan(x^2)] = \dfrac{2x}{1+x^4}$

---

## 7. Combining Everything

**Example:** Differentiate $y = \arcsin(\sqrt{x})$.

Chain rule: outer $\arcsin$, inner $\sqrt{x}$:

$$y' = \frac{1}{\sqrt{1-(\sqrt{x})^2}} \cdot \frac{1}{2\sqrt{x}} = \frac{1}{\sqrt{1-x}} \cdot \frac{1}{2\sqrt{x}} = \frac{1}{2\sqrt{x(1-x)}}$$

**Example:** Differentiate $y = x^2 \arctan(3x)$.

Product rule:
$$y' = 2x\arctan(3x) + x^2 \cdot \frac{3}{1+9x^2} = 2x\arctan(3x) + \frac{3x^2}{1+9x^2}$$

---

## 8. Why Inverse Trig Functions Matter

Inverse trig derivatives appear in **integration** (Weeks 8–10) — they are the antiderivatives of rational and radical expressions:

$$\int \frac{1}{\sqrt{1-x^2}}\,dx = \arcsin x + C \qquad \int \frac{1}{1+x^2}\,dx = \arctan x + C$$

These integrals cannot be expressed in any other elementary form. The inverse trig functions are not peripheral — they are the answer to fundamental integration problems.

---

## 9. When to Reach for Logarithmic Differentiation

Three signatures, and nothing else qualifies:

| Signature | Example | Why logs help |
|---|---|---|
| **Variable base *and* variable exponent** | $x^{\cos x}$, $(\sin x)^x$ | Neither the power rule nor the exponential rule applies — the power rule needs a constant exponent, $a^x$ needs a constant base. Logs are the *only* elementary route. |
| **Long products and quotients** | $\dfrac{\sqrt[3]{x^2+1}(x-2)^5}{(x^2+4)^2}$ | $\ln$ turns products into sums and powers into coefficients, replacing nested product/quotient rules with a single sum of simple terms. |
| **Towers** | $x^{x^x}$ | Apply the method twice. |

> **The most common misuse:** reaching for logs on $x^5$ or $2^x$. Both have standard rules; taking
> logs is legal but slower and introduces an unnecessary division. Logs are for when the *ordinary*
> rules genuinely do not apply.

**A caution about absolute values.** $\ln y$ requires $y > 0$. For a function that can be negative,
the rigorous statement differentiates $\ln|y|$, which gives the same $y'/y$ because
$\frac{d}{dx}\ln|y| = \frac{y'}{y}$ for $y \neq 0$. Working with $|y|$ keeps the method valid on
both sides of a zero — which matters for exercise 2(c), where $(x-2)^5$ changes sign at $x=2$.

---

## 10. Common Errors

**1. Forgetting that $y$ is the whole function.** After $\ln y = \cos x\ln x$ and differentiating to
$\frac{y'}{y} = \ldots$, you must **multiply back by $y$** — and $y$ means the original expression,
not the letter. Leaving the answer as $\frac{y'}{y}$ is an incomplete solution.

**2. $\frac{d}{dx}[\ln(f(x))] = \frac{f'(x)}{f(x)}$, not $\frac{1}{f(x)}$.** The inner derivative is
the whole point of the chain rule and is dropped constantly.

**3. Confusing $\log_a x$ with $\ln x$.** $\frac{d}{dx}\log_a x = \frac{1}{x\ln a}$ — the $\ln a$
lives in the *denominator*. Only for $a=e$ does it disappear.

**4. Losing the domain on inverse trig.** $\frac{d}{dx}\arcsin x = \frac{1}{\sqrt{1-x^2}}$ is defined
only for $|x|<1$; at $x=\pm1$ the tangent is vertical. An answer with no domain statement is
incomplete.

**5. Sign errors in the "arc-co" derivatives.** $\arccos$, $\text{arccot}$, and
$\text{arccsc}$ all carry a **minus sign** — each is the negative of its partner. That is not a
coincidence: $\arcsin x + \arccos x = \pi/2$ is constant, so the derivatives must cancel
(exercise 4).

---

## Lecture 2 Exercises

1. Differentiate:
   - (a) $y = \ln(x^3 + 2x)$
   - (b) $y = \ln|\sec x + \tan x|$
   - (c) $y = \log_3(x^2 - 5)$
   - (d) $y = \arctan\!\left(\dfrac{x}{a}\right)$ where $a$ is a constant

2. Use logarithmic differentiation:
   - (a) $y = x^{\cos x}$
   - (b) $y = (\sin x)^x$
   - (c) $y = \dfrac{\sqrt[3]{x^2+1}\cdot(x-2)^5}{(x^2+4)^2}$

3. Find $y'$:
   - (a) $y = \arcsin(2x-1)$
   - (b) $y = \arctan(\sqrt{x})$
   - (c) $y = \cos(\arcsin x)$ — simplify using a trig identity after differentiating

4. **(Synthesis)** Show that $\dfrac{d}{dx}[\arcsin x] + \dfrac{d}{dx}[\arccos x] = 0$ by direct computation of each derivative. Then explain this result using the identity $\arcsin x + \arccos x = \dfrac{\pi}{2}$.

5. **(Challenge)** Differentiate $y = x^{x^x}$ using logarithmic differentiation twice.

---

### Answers

All results verified numerically by central differences.

**1.**
**(a)** $\boxed{\dfrac{3x^2+2}{x^3+2x}}$ &nbsp;&nbsp;
**(c)** $\boxed{\dfrac{2x}{(x^2-5)\ln 3}}$ &nbsp;&nbsp;
**(d)** $\dfrac{1/a}{1+x^2/a^2} = \boxed{\dfrac{a}{a^2+x^2}}$

**(b)** $y' = \dfrac{\sec x\tan x+\sec^2x}{\sec x+\tan x} = \dfrac{\sec x(\tan x+\sec x)}{\sec x+\tan x} = \boxed{\sec x}$
— a small miracle worth pausing on: this is *the* standard antiderivative of $\sec x$, and it is
where $\int\sec x\,dx = \ln|\sec x+\tan x|+C$ comes from.

**2.** In each case take $\ln$, differentiate, then multiply back by $y$.

**(a)** $\ln y = \cos x\ln x \Rightarrow \boxed{y' = x^{\cos x}\left(\dfrac{\cos x}{x} - \sin x\ln x\right)}$

**(b)** $\ln y = x\ln\sin x \Rightarrow \boxed{y' = (\sin x)^x\left(\ln\sin x + x\cot x\right)}$

**(c)** $\ln|y| = \tfrac13\ln(x^2+1) + 5\ln|x-2| - 2\ln(x^2+4)$, so
$$y' = y\left(\frac{2x}{3(x^2+1)} + \frac{5}{x-2} - \frac{4x}{x^2+4}\right), \qquad
y = \frac{\sqrt[3]{x^2+1}\,(x-2)^5}{(x^2+4)^2}$$
Doing this by product and quotient rules directly is possible and roughly four times the work.

**3.**
**(a)** $\dfrac{2}{\sqrt{1-(2x-1)^2}}$; since $1-(2x-1)^2 = 4x-4x^2$, this simplifies to
$\boxed{\dfrac{1}{\sqrt{x-x^2}}}$ &nbsp;(domain $0<x<1$)

**(b)** $\dfrac{1}{1+x}\cdot\dfrac{1}{2\sqrt x} = \boxed{\dfrac{1}{2\sqrt x\,(1+x)}}$

**(c)** Directly: $-\sin(\arcsin x)\cdot\dfrac{1}{\sqrt{1-x^2}} = \boxed{-\dfrac{x}{\sqrt{1-x^2}}}$.
Alternatively notice $\cos(\arcsin x) = \sqrt{1-x^2}$ *first* — the function was $\sqrt{1-x^2}$ all
along, and differentiating that gives the same answer in one line. **Simplify before
differentiating whenever an inverse-trig composition collapses.**

**4.** $\dfrac{d}{dx}\arcsin x = \dfrac{1}{\sqrt{1-x^2}}$ and $\dfrac{d}{dx}\arccos x = \dfrac{-1}{\sqrt{1-x^2}}$;
the sum is $0$ for every $|x|<1$. ✓

The identity explains it without any computation: $\arcsin x + \arccos x = \pi/2$ is a **constant**,
and the derivative of a constant is zero. Conversely, a function whose derivative vanishes on an
interval is constant there — so the derivative fact and the identity are equivalent, and either
proves the other.

**5.** Let $u=x^x$, so $\ln u = x\ln x$ and $u' = x^x(\ln x+1)$. Then $\ln y = x^x\ln x$, and

$$\frac{y'}{y} = u'\ln x + \frac{u}{x} = x^x(\ln x+1)\ln x + \frac{x^x}{x}$$

$$\boxed{y' = x^{x^x}\cdot x^x\left(\ln^2 x + \ln x + \frac1x\right)}$$

Note $x^{x^x}$ means $x^{(x^x)}$ — exponentiation is **right**-associative. $(x^x)^x = x^{x^2}$ is a
different and much smaller function.

---

*Next: Wednesday — Related Rates*
