# MATH 141 · Calculus I
## Week 10 · Lecture 2 (Tuesday)
### The Substitution Rule for Definite Integrals, and Symmetry

*“Symmetry is a vast subject, significant in art and nature. Mathematics lies at its root, and it would be hard to find a better one on which to demonstrate the working of the mathematical intellect.”* — Hermann Weyl, *Symmetry* (1952)

**Date:** Tuesday 1 December 2026 · 11:00–11:50 · Week 10

**Coursework:** 📘 **Midterm 2** Wed 2 Dec 18:00–19:15 · 📝 **PS 10** released Wed 2 Dec 12:00, due Wed 9 Dec 11:00 · 📝 **PS 9** due Wed 2 Dec 11:00 · 🔬 **Lab 10** Fri 4 Dec 15:00–16:50, report due Mon 7 Dec 17:00 · 📊 **Quiz 11** Mon 7 Dec 11:00–11:15

---

**Reading:** Stewart §5.5 (continued) | Spivak Ch. 13 (§13.3, continued)

---

## 1. Two Methods for Definite Integrals with Substitution

When evaluating $\displaystyle\int_a^b f(g(x))g'(x)\,dx$, there are two valid approaches.

### Method 1 — Convert Back to $x$ at the End

1. Find the indefinite integral $\displaystyle\int f(g(x))g'(x)\,dx$ using substitution (as in Monday's lecture)
2. Substitute back to express the antiderivative in terms of $x$
3. Evaluate at the original limits $a$ and $b$

### Method 2 — Change the Limits of Integration (usually faster)

> **Theorem.** If $g'$ is continuous on $[a,b]$ and $f$ is continuous on the range of $u=g(x)$, then:
> $$\int_a^b f(g(x))g'(x)\,dx = \int_{g(a)}^{g(b)} f(u)\,du$$

**Key idea:** when you substitute $u=g(x)$, you must also convert the **limits of integration** from $x$-values to the corresponding $u$-values. Then you never need to substitute back — the final antiderivative evaluation happens entirely in terms of $u$.

### Example 1 — Comparing Both Methods

Evaluate $\displaystyle\int_0^2 x(x^2+1)^3\,dx$.

**Method 1:** Let $u=x^2+1$, $du=2x\,dx$.

$$\int x(x^2+1)^3\,dx = \frac12\int u^3\,du = \frac{u^4}8+C = \frac{(x^2+1)^4}8+C$$

Evaluate at limits: $\dfrac{(5)^4}8 - \dfrac{(1)^4}8 = \dfrac{625-1}8 = \dfrac{624}8 = 78$

**Method 2:** Let $u=x^2+1$, $du=2x\,dx$. Convert limits: when $x=0$, $u=1$; when $x=2$, $u=5$.

$$\int_0^2 x(x^2+1)^3\,dx = \frac12\int_1^5 u^3\,du = \frac12\left[\frac{u^4}4\right]_1^5 = \frac18[625-1] = \frac{624}8 = 78$$

Both methods agree, but **Method 2 is generally faster** since it avoids the back-substitution step. This is the preferred method going forward.

---

## 2. Worked Examples — Definite Integrals via Substitution

### Example 2

$$\int_0^{\pi/2} \cos^3x\sin x\,dx$$

Let $u=\cos x$, $du=-\sin x\,dx$, so $\sin x\,dx = -du$.

Convert limits: $x=0 \Rightarrow u=1$; $x=\pi/2 \Rightarrow u=0$.

$$= \int_1^0 u^3(-du) = \int_0^1 u^3\,du = \left[\frac{u^4}4\right]_0^1 = \frac14$$

*(Note how reversing the limits — from $[1,0]$ to $[0,1]$ — automatically cancels the leftover minus sign, per Week 6's convention $\int_b^a = -\int_a^b$.)*

### Example 3

$$\int_1^e \frac{(\ln x)^2}{x}\,dx$$

Let $u=\ln x$, $du=\dfrac1x dx$.

Convert limits: $x=1\Rightarrow u=\ln1=0$; $x=e\Rightarrow u=\ln e=1$.

$$= \int_0^1 u^2\,du = \left[\frac{u^3}3\right]_0^1 = \frac13$$

### Example 4

$$\int_0^1 \frac{x}{\sqrt{x^2+3}}\,dx$$

Let $u=x^2+3$, $du=2x\,dx$.

Convert limits: $x=0\Rightarrow u=3$; $x=1\Rightarrow u=4$.

$$= \frac12\int_3^4 u^{-1/2}\,du = \frac12\left[2u^{1/2}\right]_3^4 = \left[\sqrt u\right]_3^4 = \sqrt4-\sqrt3 = 2-\sqrt3$$

---

## 3. Symmetry — A Powerful Shortcut

Recall Week 8 (Problem Set 8, D4): even and odd functions have special integral properties. We can now PROVE these results rigorously using substitution.

> **Theorem (Symmetry in Integration).**
>
> If $f$ is **even** ($f(-x)=f(x)$): $\displaystyle\int_{-a}^a f(x)\,dx = 2\int_0^a f(x)\,dx$
>
> If $f$ is **odd** ($f(-x)=-f(x)$): $\displaystyle\int_{-a}^a f(x)\,dx = 0$

### Proof

Split the integral: $\displaystyle\int_{-a}^a f(x)\,dx = \int_{-a}^0 f(x)\,dx + \int_0^a f(x)\,dx$

In the first integral, substitute $u=-x$, so $du=-dx$, and when $x=-a$, $u=a$; when $x=0$, $u=0$.

$$\int_{-a}^0 f(x)\,dx = \int_a^0 f(-u)(-du) = \int_0^a f(-u)\,du$$

**If $f$ is even:** $f(-u)=f(u)$, so this equals $\displaystyle\int_0^a f(u)\,du = \int_0^a f(x)\,dx$ (renaming the dummy variable).

$$\int_{-a}^a f(x)\,dx = \int_0^af(x)\,dx+\int_0^af(x)\,dx = 2\int_0^af(x)\,dx \quad\square$$

**If $f$ is odd:** $f(-u)=-f(u)$, so this equals $\displaystyle-\int_0^a f(u)\,du$.

$$\int_{-a}^a f(x)\,dx = -\int_0^af(x)\,dx+\int_0^af(x)\,dx = 0 \quad\square$$

**This makes Problem Set 8 D4's area argument rigorous** — the Substitution Rule was the missing tool.

### Example 5

Evaluate $\displaystyle\int_{-2}^2 (x^4-3x^2+1)\,dx$ using symmetry.

$f(x)=x^4-3x^2+1$ is even (only even powers of $x$).

$$= 2\int_0^2(x^4-3x^2+1)\,dx = 2\left[\frac{x^5}5-x^3+x\right]_0^2 = 2\left[\frac{32}5-8+2\right] = 2\left[\frac{32}5-6\right] = 2\left[\frac{32-30}5\right] = \frac45$$

### Example 6

Evaluate $\displaystyle\int_{-\pi}^{\pi}x^2\sin(x)\,dx$ using symmetry — **without any computation**.

$f(x)=x^2\sin x$: $f(-x)=(-x)^2\sin(-x)=x^2(-\sin x)=-x^2\sin x=-f(x)$. **Odd function.**

$$\int_{-\pi}^\pi x^2\sin x\,dx = 0$$

This shortcut saves an integration-by-parts computation entirely (a technique we learn Wednesday) — recognizing symmetry can eliminate substantial work.

---

## 4. More Substitution Patterns — Building Fluency

### Example 7 — Substitution Involving $\sec$ and $\tan$

$$\int \sec^2x\tan x\,dx$$

Let $u=\tan x$, $du=\sec^2x\,dx$.

$$= \int u\,du = \frac{u^2}2+C = \frac{\tan^2x}2+C$$

*(Alternatively, letting $u=\sec x$ gives $\dfrac{\sec^2x}2+C$ — both are valid antiderivatives, differing by the constant $\frac12$ via the identity $\sec^2x=1+\tan^2x$. This is a good moment to note: antiderivatives are only unique up to a constant, and different valid substitution choices can produce different-looking — but equally correct — answers.)*

### Example 8 — Combining Techniques

$$\int_0^{\ln2} \frac{e^x}{\sqrt{e^x+1}}\,dx$$

Let $u=e^x+1$, $du=e^x\,dx$.

Convert limits: $x=0\Rightarrow u=2$; $x=\ln2\Rightarrow u=e^{\ln2}+1=2+1=3$.

$$= \int_2^3 u^{-1/2}\,du = \left[2u^{1/2}\right]_2^3 = 2\sqrt3-2\sqrt2$$

### Example 9 — A "Disguised" Substitution

$$\int \frac{1}{x\ln x}\,dx$$

Let $u=\ln x$, $du=\dfrac1x dx$.

$$= \int\frac{du}{u} = \ln|u|+C = \ln|\ln x|+C$$

---

## 5. CS Connection — Symmetry as an Optimization Principle

The symmetry shortcuts in this lecture are a specific instance of a general and extremely important principle in computation: **exploit structure to avoid unnecessary work.**

- **Even/odd decomposition** appears throughout signal processing: any function (or discrete signal) can be decomposed into even and odd parts, and the Fast Fourier Transform exploits symmetries in exactly this spirit to reduce computational complexity from $O(n^2)$ to $O(n\log n)$.
- **Recognizing invariants** (like "this function is even, so I only need half the domain") is the same skill used in algorithm design when recognizing that a problem has redundant sub-structure (dynamic programming) or symmetric cases that can be collapsed (many combinatorics and graph algorithms).
- **Checking symmetry before brute-force computation** is a cheap, fast test that can save enormous computational effort — precisely analogous to checking easy special cases before attempting a general-purpose algorithm.

The mathematical habit of asking "does this problem have a symmetry I can exploit?" *before* diving into computation is a transferable skill with direct payoff in software engineering and algorithm design.

---

## Lecture 2 Exercises

1. Evaluate using substitution with limit conversion (Method 2):
   - (a) $\displaystyle\int_0^1 x^2(1+x^3)^4\,dx$
   - (b) $\displaystyle\int_0^{\pi/4}\sec^2x\tan^3x\,dx$
   - (c) $\displaystyle\int_1^4 \frac{1}{\sqrt x(1+\sqrt x)^2}\,dx$ *(let $u=1+\sqrt x$)*
   - (d) $\displaystyle\int_0^1 xe^{-x^2}\,dx$

2. Use symmetry to evaluate immediately (no computation, just justification):
   - (a) $\displaystyle\int_{-3}^3 x^5\,dx$
   - (b) $\displaystyle\int_{-1}^1 \frac{x^2}{1+x^4}\,dx$ *(reduce to $2\times$ the integral from 0 to 1 — you don't need to fully evaluate)*
   - (c) $\displaystyle\int_{-\pi/2}^{\pi/2} \sin(x^3)\cos x\,dx$

3. Evaluate $\displaystyle\int_{-2}^{2}(3x^4-2x^2+5)\,dx$ using symmetry to simplify the computation.

4. **(Proof)** Use the substitution $u=a-x$ to prove: $\displaystyle\int_0^a f(x)\,dx = \int_0^a f(a-x)\,dx$. This is a useful general identity — apply it to verify $\displaystyle\int_0^{\pi/2}\sin x\,dx = \int_0^{\pi/2}\cos x\,dx$ (using $f(x)=\sin x$ and $a=\pi/2$, noting $\sin(\pi/2-x)=\cos x$).

5. **(Challenge)** Evaluate $\displaystyle\int_0^\pi \frac{x\sin x}{1+\cos^2x}\,dx$ using the identity from Exercise 4 (substitute $x\to\pi-x$, add the original and new integral together, and solve for the value).

---


### Answers

**1.** Convert the limits along with the variable — never mix $x$-limits with a $u$-expression.

**(a)** $u=1+x^3$, $du=3x^2dx$; limits $1\to2$:
$\tfrac13\displaystyle\int_1^2u^4du=\tfrac{1}{15}\left[u^5\right]_1^2=\boxed{\tfrac{31}{15}}$
**(b)** $u=\tan x$, limits $0\to1$: $\displaystyle\int_0^1u^3du=\boxed{\tfrac14}$
**(c)** $u=1+\sqrt x$, $du=\tfrac{dx}{2\sqrt x}$, limits $2\to3$:
$2\displaystyle\int_2^3u^{-2}du=2\left[-\tfrac1u\right]_2^3=\boxed{\tfrac13}$
**(d)** $u=-x^2$: $-\tfrac12\left[e^{-x^2}\right]_0^1=\boxed{\tfrac{1-e^{-1}}{2}\approx0.3161}$

**2. (a)** $x^5$ is **odd** on the symmetric interval $[-3,3]$ → $\boxed{0}$
**(b)** $\dfrac{x^2}{1+x^4}$ is **even** →
$\boxed{2\displaystyle\int_0^1\frac{x^2}{1+x^4}\,dx}$
**(c)** $\sin(x^3)$ is odd and $\cos x$ is even, so the product is **odd** → $\boxed{0}$

Parity algebra: odd × even = odd, odd × odd = even, even × even = even. (c) is the one students
miss, because neither factor is obviously the deciding one.

**3.** $3x^4$ and $-2x^2$ and $5$ are all **even**, so
$$\int_{-2}^{2}=2\int_0^2\left(3x^4-2x^2+5\right)dx
=2\left[\tfrac{3x^5}{5}-\tfrac{2x^3}{3}+5x\right]_0^2
=2\left(\tfrac{96}{5}-\tfrac{16}{3}+10\right)=\boxed{\tfrac{716}{15}\approx47.73}$$
*(Numerically confirmed.)* Symmetry halves the arithmetic and removes the chance of a sign error at
the lower limit.

**4.** Substitute $u=a-x$, so $x=a-u$ and $dx=-du$. The limits reverse: $x=0\to u=a$ and
$x=a\to u=0$. Hence
$$\int_0^af(x)\,dx=\int_a^0f(a-u)(-du)=\int_0^af(a-u)\,du=\int_0^af(a-x)\,dx$$
since the name of the dummy variable is immaterial. $\blacksquare$

**Application:** with $f=\sin$ and $a=\tfrac\pi2$, and $\sin\!\left(\tfrac\pi2-x\right)=\cos x$:
$$\int_0^{\pi/2}\sin x\,dx=\int_0^{\pi/2}\cos x\,dx$$
Both equal 1 ✓ — the sine and cosine humps are reflections of one another.

**5.** Let $I=\displaystyle\int_0^\pi\frac{x\sin x}{1+\cos^2x}\,dx$ and apply Exercise 4 with
$a=\pi$. Since $\sin(\pi-x)=\sin x$ and $\cos^2(\pi-x)=\cos^2x$:
$$I=\int_0^\pi\frac{(\pi-x)\sin x}{1+\cos^2x}\,dx=\pi\int_0^\pi\frac{\sin x}{1+\cos^2x}\,dx-I$$
So $2I=\pi\displaystyle\int_0^\pi\frac{\sin x}{1+\cos^2x}\,dx$. Substituting $u=\cos x$ turns that
into $\pi\displaystyle\int_{-1}^{1}\frac{du}{1+u^2}=\pi\left[\arctan u\right]_{-1}^{1}=\pi\cdot\tfrac\pi2$.
$$\boxed{I=\frac{\pi^2}{4}\approx2.4674}$$
*(Numerically confirmed to 10 decimal places.)*

The move is worth naming: **the awkward factor $x$ is eliminated by adding the integral to its own
reflection**, leaving something elementary. The same trick handles many integrals where a
polynomial multiplies a symmetric function.

*Next: Wednesday — Integration by Parts*
