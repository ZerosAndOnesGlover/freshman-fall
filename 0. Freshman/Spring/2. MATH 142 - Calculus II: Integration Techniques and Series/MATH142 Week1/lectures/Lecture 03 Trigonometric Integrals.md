# MATH 142 · Calculus II
## Week 1 · Lecture 3 (Friday)
### Trigonometric Integrals, and the Identity Behind Fourier Analysis

*“Mathematics is the queen of the sciences and number theory is the queen of mathematics.”* — Carl Friedrich Gauss, as quoted in Wolfgang Sartorius von Waltershausen, *Gauss zum Gedächtniss* (1856)

**Date:** Friday 29 January 2027 · 11:00–11:50 · Week 1

**Coursework:** 📝 **PS 1** released today 12:00, due Fri 5 Feb 17:00 · 📊 **Quiz 2** Mon 1 Feb 11:00–11:15 · 🔬 **Lab 1** Wed 3 Feb 15:00–16:50

---

**Reading:** Stewart §7.2 | Apostol Ch. 5 §5.10

---

## 1. Why This Looks Like a List of Cases

Today's material is a **decision procedure**: given $\int\sin^m x\cos^n x\,dx$, the parities of $m$ and $n$ tell you what to do. It is the least conceptual lecture of the course and it earns its place twice over — Week 2's trigonometric substitution produces exactly these integrals, and §5 today contains the identity that makes signal processing possible.

**Everything below reduces to substitution.** The only content is *which* substitution, and the identity that makes it available.

---

## 2. Powers of Sine and Cosine

$$\int \sin^m x\,\cos^n x\,dx$$

### Case 1 — $n$ odd (an odd power of cosine)

Peel off one $\cos x$ to serve as $du$, and convert the rest using $\cos^2 x = 1-\sin^2 x$. Substitute $u = \sin x$.

**Example:** $\displaystyle\int\cos^5 x\,dx$

$$= \int \cos^4 x\cdot\cos x\,dx = \int(1-\sin^2x)^2\cos x\,dx$$

With $u = \sin x$, $du = \cos x\,dx$:

$$= \int(1-u^2)^2du = \int(1 - 2u^2 + u^4)du = u - \frac{2u^3}{3}+\frac{u^5}{5}$$

$$= \boxed{\sin x - \frac{2\sin^3x}{3} + \frac{\sin^5 x}{5} + C}$$

*Verified symbolically.*

### Case 2 — $m$ odd (an odd power of sine)

Symmetric: peel off one $\sin x$, convert the rest with $\sin^2x = 1-\cos^2x$, substitute $u=\cos x$. **Remember $du = -\sin x\,dx$ carries a minus sign.**

**Example:** $\displaystyle\int\sin^3x\cos^2x\,dx$

$$= \int(1-\cos^2x)\cos^2 x\,\sin x\,dx \overset{u=\cos x}{=} -\int(1-u^2)u^2\,du = -\int(u^2-u^4)du$$

$$= -\frac{u^3}{3}+\frac{u^5}{5} = \boxed{-\frac{\cos^3x}{3}+\frac{\cos^5x}{5}+C}$$

*Verified symbolically.*

### Case 3 — **both** even

Neither substitution is available: peeling off one factor leaves an odd power, which cannot be written in terms of the other function. **Use the half-angle identities to lower the powers:**

$$\sin^2 x = \frac{1-\cos 2x}{2} \qquad\qquad \cos^2 x = \frac{1+\cos 2x}{2}$$

**Example:** $\displaystyle\int\sin^2x\cos^2x\,dx$

$$= \int\frac{(1-\cos2x)}{2}\cdot\frac{(1+\cos2x)}{2}dx = \frac14\int(1-\cos^2 2x)\,dx$$

Apply the identity again to $\cos^2 2x = \frac{1+\cos4x}{2}$:

$$= \frac14\int\left(1 - \frac{1+\cos 4x}{2}\right)dx = \frac14\int\left(\frac12 - \frac{\cos4x}{2}\right)dx = \frac{x}{8}-\frac{\sin 4x}{32}+C$$

$$\boxed{\int\sin^2x\cos^2x\,dx = \frac{x}{8}-\frac{\sin4x}{32}+C}$$

*Verified symbolically.*

**Note the shape of the answer**: a term linear in $x$ plus oscillation. Every all-even case produces this, and the linear term is why such integrals grow without bound over long intervals — the physical statement that **average power is nonzero**.

**Alternative:** the reduction formula from Lecture 2 handles even powers too, and for high exponents it is faster.

### The decision table

| $m$ (sine) | $n$ (cosine) | Do this |
|---|---|---|
| any | **odd** | peel one $\cos x$; $u=\sin x$ |
| **odd** | any | peel one $\sin x$; $u=\cos x$ |
| **even** | **even** | half-angle identities, or reduction formula |

*(If both are odd, either route works. Choose the one leaving less algebra.)*

---

## 3. Powers of Tangent and Secant

$$\int\tan^m x\,\sec^n x\,dx$$

The two facts that drive everything:

$$\frac{d}{dx}\tan x = \sec^2 x \qquad \frac{d}{dx}\sec x = \sec x\tan x \qquad \sec^2x = 1+\tan^2x$$

### Case A — $n$ even (an even power of secant)

Peel off $\sec^2x$ for $du$, convert the rest with $\sec^2x = 1+\tan^2x$, substitute $u=\tan x$.

**Example:** $\displaystyle\int\tan^4x\sec^4x\,dx$

$$= \int\tan^4x\,(1+\tan^2x)\,\sec^2x\,dx \overset{u=\tan x}{=} \int u^4(1+u^2)du = \frac{u^5}{5}+\frac{u^7}{7}$$

$$= \boxed{\frac{\tan^5x}{5}+\frac{\tan^7x}{7}+C}$$

*Verified symbolically.*

### Case B — $m$ odd (an odd power of tangent)

Peel off $\sec x\tan x$ for $du$, convert the remaining even power of tangent with $\tan^2x = \sec^2x-1$, substitute $u=\sec x$.

**Example:** $\displaystyle\int\tan^3x\sec^3x\,dx$

$$= \int\tan^2x\,\sec^2x\,\cdot\,\sec x\tan x\,dx = \int(\sec^2x-1)\sec^2x\cdot\sec x\tan x\,dx$$

With $u=\sec x$:

$$= \int(u^2-1)u^2\,du = \frac{u^5}{5}-\frac{u^3}{3} = \boxed{\frac{\sec^5x}{5}-\frac{\sec^3x}{3}+C}$$

*Verified symbolically.*

### The awkward cases

$m$ even **and** $n$ odd fits neither pattern. These need the reduction formula, or the standard results

$$\int\sec x\,dx = \ln|\sec x + \tan x| + C \qquad \int\sec^3x\,dx = \frac{\sec x\tan x + \ln|\sec x+\tan x|}{2}+C$$

*Both verified by differentiation — the second differentiates to exactly $\sec^3 x$.*

> **A note repeating Week 0's lesson.** Asked for $\int\sec^3x\,dx$, a computer algebra system returns
> a combination of $\ln(1+\sin x)$ and $\ln(1-\sin x)$ that looks nothing like the boxed formula.
> Both are correct — they differ by a constant. **Differentiating the boxed form gives $\sec^3 x$ in
> one line**, which settles it. Do not assume you are wrong because the machine printed something else.

---

## 4. Products of Different Frequencies

$$\int\sin(mx)\cos(nx)\,dx, \qquad \int \sin(mx)\sin(nx)\,dx, \qquad \int\cos(mx)\cos(nx)\,dx$$

None of the above strategies applies — the arguments differ. Use the **product-to-sum identities**:

$$\sin A\sin B = \tfrac12\big[\cos(A-B) - \cos(A+B)\big]$$
$$\cos A\cos B = \tfrac12\big[\cos(A-B) + \cos(A+B)\big]$$
$$\sin A\cos B = \tfrac12\big[\sin(A-B) + \sin(A+B)\big]$$

*All three verified symbolically.*

**These turn a product into a sum, and sums integrate term by term.**

### Example

$$\int\sin 3x\cos 5x\,dx = \frac12\int\big[\sin(-2x) + \sin 8x\big]dx = \frac12\int\big[\sin 8x - \sin 2x\big]dx$$

$$= \frac12\left(-\frac{\cos 8x}{8} + \frac{\cos 2x}{2}\right) = \boxed{\frac{\cos 2x}{4} - \frac{\cos 8x}{16}+C}$$

*Verified symbolically — the CAS returns exactly this.*

---

## 5. Orthogonality — The Payoff

Now evaluate those products over a **full period**, $[0,2\pi]$, for positive integers $m,n$:

$$\int_0^{2\pi}\sin(mx)\sin(nx)\,dx = \begin{cases} 0 & m\neq n\\[4pt] \pi & m = n\end{cases}$$

$$\int_0^{2\pi}\cos(mx)\cos(nx)\,dx = \begin{cases} 0 & m\neq n\\[4pt] \pi & m = n\end{cases}$$

$$\int_0^{2\pi}\sin(mx)\cos(nx)\,dx = 0 \quad\text{for all } m,n$$

*Verified symbolically for $(m,n) = (1,2), (2,3), (1,3), (2,2), (3,3)$ — every case matches.*

### Why it is true

For $m\neq n$, product-to-sum gives $\tfrac12[\cos((m-n)x) - \cos((m+n)x)]$, and **each cosine has an integer number of full periods on $[0,2\pi]$**, so each integrates to zero. When $m=n$, the first term becomes $\cos 0 = 1$, whose integral over $[0,2\pi]$ is $2\pi$ — and the $\tfrac12$ gives $\pi$.

**The entire phenomenon is that $\int_0^{2\pi}\cos(kx)\,dx = 0$ for every nonzero integer $k$, and $2\pi$ for $k=0$.**

### Why it matters

Think of $\int_0^{2\pi} f\,g\,dx$ as a **dot product** of functions. Then these formulas say the functions

$$\sin x,\ \cos x,\ \sin 2x,\ \cos 2x,\ \sin 3x,\ \cos 3x,\ \ldots$$

are **mutually perpendicular** — an orthogonal basis, exactly like $\hat\imath,\hat\jmath,\hat k$ in three dimensions but infinite-dimensional.

Suppose a signal is a combination of frequencies:

$$f(x) = a_1\sin x + a_2\sin 2x + a_3\sin 3x + \cdots$$

**How do you extract $a_7$?** Multiply by $\sin 7x$ and integrate. Every term dies except one:

$$\int_0^{2\pi} f(x)\sin(7x)\,dx = a_7\int_0^{2\pi}\sin^2(7x)\,dx = a_7\pi \implies a_7 = \frac1\pi\int_0^{2\pi}f(x)\sin(7x)\,dx$$

> **That is the Fourier coefficient formula, and this is its entire derivation.** Orthogonality is
> what makes it work: the integral acts as a filter that annihilates every frequency but the one you
> multiplied by.

**Where you will meet this:** MP3 and AAC encode audio by discarding Fourier coefficients the ear cannot hear. JPEG does the same for images with a cosine variant (the DCT). Every spectrum analyser, every noise filter, every convolution-based algorithm rests on the three formulas above.

We return to this in **Week 10**, when infinite series make the "combination of frequencies" precise.

---

## 6. What To Take From This Lecture

1. **Odd power → peel one factor off and substitute.** The odd one tells you which substitution.
2. **All even → half-angle identities**, or the reduction formula.
3. **Tangent/secant:** even power of $\sec$ → $u = \tan x$; odd power of $\tan$ → $u = \sec x$.
4. **Different frequencies → product-to-sum.**
5. **Orthogonality is the reason Fourier analysis exists**, and it is three lines of this week's material.

---

## Looking Ahead

Every integral this week had an elementary answer reachable by parts or a trigonometric identity. Next week we attack integrals that are *algebraic* — $\int\sqrt{1-x^2}\,dx$, $\int\frac{dx}{x^2-1}$ — with no obvious trigonometry in sight.

**The strategy will be to put the trigonometry there ourselves**, by substituting $x = \sin\theta$ and turning an algebraic integral into one from today's lecture. Today's material is the destination of next week's technique.

---

*Next: Week 2, Monday — Trigonometric Substitution*
