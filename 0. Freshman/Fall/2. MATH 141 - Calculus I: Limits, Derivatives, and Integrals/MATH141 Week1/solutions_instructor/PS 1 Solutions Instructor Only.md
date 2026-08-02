# MATH 141 Calculus I
## Problem Set 1 — Complete Instructor Solutions
### DO NOT DISTRIBUTE TO STUDENTS

---


## Marking Scheme

Point values are printed per problem on the problem set. Within each problem, split the marks:

- **Method (≈60%).** Correct technique named and set up: the right rule or theorem, hypotheses checked where the theorem requires it, and the symbolic work shown before any numerical evaluation.
- **Execution (≈40%).** Correct algebra and simplification, correct final form, and any domain restrictions or constants of integration stated.

A bare answer with no working earns at most the execution marks — and in proof problems ("show that", "prove"), no marks at all, since the reasoning *is* the deliverable.

**Carry-through.** Penalise a given error once. If the student proceeds correctly from their own wrong intermediate value, award the downstream marks in full.

**Equivalent forms.** Accept any algebraically equivalent answer — factored or expanded, and trigonometric identities applied or not — unless the problem explicitly demands a particular form.

### Common errors in this problem set

**1. Evaluating a limit by substitution without justification.** Substitution is valid only where the function is continuous. For 0/0 forms it proves nothing — the algebra (factor, rationalise, conjugate) is the actual work.

**2. Reversing the ε–δ quantifier order.** The definition is: for **every** ε > 0 there **exists** δ > 0. A proof that picks ε in terms of δ has the logic backwards and earns no method marks, however tidy the algebra.

**3. Confusing 'limit exists' with 'function is defined'.** A limit can exist where f(a) is undefined, and f(a) can exist where the limit does not. Continuity requires the limit to exist, f(a) to exist, and the two to agree — all three.

**4. Applying the IVT without checking its hypotheses.** The IVT needs continuity on a **closed** interval [a,b]. It guarantees existence, never uniqueness or a value — a student who claims 'exactly one root' from IVT alone has over-concluded.

---

## Part A — Evaluating Limits

**A1(a)** $\displaystyle\lim_{x \to 3} \frac{x^2 - 9}{x - 3}$

$$= \lim_{x \to 3} \frac{(x-3)(x+3)}{x-3} = \lim_{x \to 3} (x+3) = 6$$

*Cancel factor $(x-3)$, valid since $x \neq 3$ in a limit.*

---

**A1(b)** $\displaystyle\lim_{x \to -2} \frac{x^2 + 5x + 6}{x^2 - x - 6}$

$$= \lim_{x \to -2} \frac{(x+2)(x+3)}{(x+2)(x-3)} = \lim_{x \to -2} \frac{x+3}{x-3} = \frac{-2+3}{-2-3} = \frac{1}{-5} = -\frac{1}{5}$$

---

**A1(c)** $\displaystyle\lim_{x \to 0} \frac{\sqrt{4+x}-2}{x}$

Rationalize: multiply by $\dfrac{\sqrt{4+x}+2}{\sqrt{4+x}+2}$:

$$= \lim_{x \to 0} \frac{(4+x) - 4}{x(\sqrt{4+x}+2)} = \lim_{x \to 0} \frac{x}{x(\sqrt{4+x}+2)} = \lim_{x \to 0} \frac{1}{\sqrt{4+x}+2} = \frac{1}{\sqrt{4}+2} = \frac{1}{4}$$

---

**A1(d)** $\displaystyle\lim_{x \to 1^-} \frac{|x-1|}{x-1}$ and $\displaystyle\lim_{x \to 1^+} \frac{|x-1|}{x-1}$

For $x < 1$: $|x-1| = -(x-1)$, so the expression $= \dfrac{-(x-1)}{x-1} = -1$.

For $x > 1$: $|x-1| = x-1$, so the expression $= \dfrac{x-1}{x-1} = 1$.

$$\lim_{x \to 1^-} = -1, \qquad \lim_{x \to 1^+} = 1$$

Since the one-sided limits differ, the two-sided limit **does not exist**.

---

**A1(e)** $\displaystyle\lim_{x \to \infty} \frac{6x^4 - 3x^2 + 7}{2x^4 + x^3 - 5}$

Divide numerator and denominator by $x^4$:

$$= \lim_{x \to \infty} \frac{6 - 3/x^2 + 7/x^4}{2 + 1/x - 5/x^4} = \frac{6 - 0 + 0}{2 + 0 - 0} = 3$$

---

**A1(f)** $\displaystyle\lim_{x \to \infty} \left(\sqrt{x^2+x} - x\right)$

Multiply by $\dfrac{\sqrt{x^2+x}+x}{\sqrt{x^2+x}+x}$:

$$= \lim_{x \to \infty} \frac{(x^2+x) - x^2}{\sqrt{x^2+x}+x} = \lim_{x \to \infty} \frac{x}{\sqrt{x^2+x}+x}$$

Divide numerator and denominator by $x$ (positive for large $x$):

$$= \lim_{x \to \infty} \frac{1}{\sqrt{1 + 1/x} + 1} = \frac{1}{\sqrt{1+0}+1} = \frac{1}{2}$$

---

**A2(a)** $\displaystyle\lim_{x \to 0} x^2 \cos\!\left(\frac{1}{x^2}\right)$

Since $-1 \leq \cos(1/x^2) \leq 1$ for all $x \neq 0$:
$$-x^2 \leq x^2 \cos\!\left(\frac{1}{x^2}\right) \leq x^2$$

Since $\lim_{x\to 0}(-x^2) = 0 = \lim_{x \to 0} x^2$, by the Squeeze Theorem the limit is $\boxed{0}$.

---

**A2(b)** $\displaystyle\lim_{x \to \infty} \frac{\sin x}{x}$

Since $-1 \leq \sin x \leq 1$ for all $x$:
$$\frac{-1}{x} \leq \frac{\sin x}{x} \leq \frac{1}{x}$$

Since $\lim_{x \to \infty} \dfrac{1}{x} = 0 = \lim_{x \to \infty} \dfrac{-1}{x}$, by Squeeze Theorem the limit is $\boxed{0}$.

---

**A3(a)** $\displaystyle\lim_{x \to 0} \frac{\sin 7x}{4x} = \frac{7}{4}\lim_{x \to 0}\frac{\sin 7x}{7x} = \frac{7}{4}(1) = \boxed{\frac{7}{4}}$

**A3(b)** $\displaystyle\lim_{x \to 0} \frac{\sin^2 3x}{x^2} = \lim_{x \to 0}\left(\frac{\sin 3x}{x}\right)^2 = \lim_{x \to 0}\left(3 \cdot \frac{\sin 3x}{3x}\right)^2 = (3 \cdot 1)^2 = \boxed{9}$

**A3(c)** $\displaystyle\lim_{x \to 0}\frac{1-\cos 2x}{x} = \lim_{x \to 0}\frac{1-\cos 2x}{x} \cdot \frac{2}{2} = 2\lim_{x \to 0}\frac{1-\cos 2x}{2x} = 2(0) = \boxed{0}$

**A3(d)** $\displaystyle\lim_{x \to 0}\frac{\tan 5x}{\sin 2x} = \lim_{x\to 0}\frac{\sin 5x}{\cos 5x \cdot \sin 2x} = \lim_{x\to 0}\frac{\sin 5x}{5x} \cdot \frac{2x}{\sin 2x} \cdot \frac{5x}{2x\cos 5x}$

$= 1 \cdot 1 \cdot \dfrac{5}{2 \cdot 1} = \boxed{\dfrac{5}{2}}$

---

## Part B

**B1(a):**
- $\lim_{x\to 0^-} f(x) = \lim_{x\to 0^-}(x^2-1) = -1$
- $\lim_{x\to 0^+} f(x) = \lim_{x\to 0^+}(\sqrt{x}+1) = 1$
- $\lim_{x\to 0} f(x)$: DNE (one-sided limits $-1 \neq 1$)
- $f(0) = 2$

**B1(b):**
- $\lim_{x\to 4^-} f(x) = \lim_{x\to 4^-}(\sqrt{x}+1) = \sqrt{4}+1 = 3$
- $\lim_{x\to 4^+} f(x) = \lim_{x\to 4^+}(3x-7) = 12-7 = 5$
- $\lim_{x\to 4} f(x)$: DNE (one-sided limits $3 \neq 5$)
- $f(4) = 3(4)-7 = 5$

**B1(c):**
- At $x=0$: Not continuous. Two-sided limit DNE.
- At $x=4$: Not continuous. Two-sided limit DNE. (Also $f(4) = 5$ but limit from left is 3.)

---

**B2.** Continuity at $x = -1$:

$\lim_{x\to -1^-}g(x) = a(-1) + 3b = -a + 3b$

$\lim_{x\to -1^+}g(x) = a - 2b(-1) = a + 2b$

Set equal: $-a + 3b = a + 2b \Rightarrow b = 2a \quad \cdots (1)$

Continuity at $x = 2$:

$\lim_{x\to 2^-}g(x) = a - 2b(2) = a - 4b$

$\lim_{x\to 2^+}g(x) = 3a - b + 2$

Set equal: $a - 4b = 3a - b + 2 \Rightarrow -2a - 3b = 2 \quad \cdots (2)$

Substitute $(1)$ into $(2)$: $-2a - 3(2a) = 2 \Rightarrow -8a = 2 \Rightarrow a = -\dfrac{1}{4}$

Then $b = 2(-\frac{1}{4}) = -\dfrac{1}{2}$.

**Answer:** $a = -\dfrac{1}{4}$, $b = -\dfrac{1}{2}$

---

## Part C — Epsilon-Delta Proofs

**C1.** Prove $\lim_{x\to 5}(3x-7) = 8$.

*Scratch work:* $|(3x-7)-8| = |3x-15| = 3|x-5|$. Need $3|x-5| < \varepsilon$, so $|x-5| < \varepsilon/3$. Choose $\delta = \varepsilon/3$.

*Proof:* Given $\varepsilon > 0$, let $\delta = \varepsilon/3$. Suppose $0 < |x-5| < \delta$. Then:
$$|(3x-7)-8| = |3x-15| = 3|x-5| < 3\delta = 3\cdot\frac{\varepsilon}{3} = \varepsilon \quad \square$$

---

**C2.** Prove $\lim_{x\to 3} x^2 = 9$.

*Scratch work:* $|x^2 - 9| = |x-3||x+3|$. Restrict $\delta \leq 1$: then $|x-3|<1 \Rightarrow 2<x<4 \Rightarrow 5<x+3<7$, so $|x+3|<7$. Need $|x-3| \cdot 7 < \varepsilon$, so $|x-3| < \varepsilon/7$. Choose $\delta = \min(1, \varepsilon/7)$.

*Proof:* Given $\varepsilon > 0$, let $\delta = \min(1, \varepsilon/7)$. Suppose $0 < |x-3| < \delta$. Since $\delta \leq 1$: $|x-3|<1$, so $2<x<4$, giving $5<x+3<7$, hence $|x+3|<7$. Then:
$$|x^2-9| = |x-3||x+3| < \delta \cdot 7 \leq \frac{\varepsilon}{7} \cdot 7 = \varepsilon \quad \square$$

---

**C3.** Prove $\lim_{x\to 2}\dfrac{1}{x} = \dfrac{1}{2}$.

*Scratch work:* $\left|\dfrac{1}{x}-\dfrac{1}{2}\right| = \dfrac{|x-2|}{2|x|}$. Restrict $\delta \leq 1$: $|x-2|<1 \Rightarrow 1<x<3 \Rightarrow |x|>1 \Rightarrow \dfrac{1}{|x|}<1 \Rightarrow \dfrac{1}{2|x|}<\dfrac{1}{2}$. So $\dfrac{|x-2|}{2|x|} < \dfrac{|x-2|}{2}$. Need $\dfrac{|x-2|}{2}<\varepsilon$, so $|x-2|<2\varepsilon$. Choose $\delta = \min(1, 2\varepsilon)$.

*Proof:* Given $\varepsilon > 0$, let $\delta = \min(1, 2\varepsilon)$. Suppose $0 < |x-2| < \delta$. Since $\delta \leq 1$: $|x-2|<1$, so $1<x<3$, giving $|x|>1$, so $\dfrac{1}{2|x|}<\dfrac{1}{2}$. Then:
$$\left|\frac{1}{x}-\frac{1}{2}\right| = \frac{|x-2|}{2|x|} < \frac{|x-2|}{2} < \frac{\delta}{2} \leq \frac{2\varepsilon}{2} = \varepsilon \quad \square$$

---

## Part D — IVT

**D1.** $f(x) = x^4 + x - 3$.

$f(0) = -3 < 0$, $f(2) = 16+2-3 = 15 > 0 \Rightarrow$ root in $(0,2)$.

$f(-2) = 16-2-3 = 11 > 0$, $f(-1) = 1-1-3 = -3 < 0 \Rightarrow$ root in $(-2,-1)$.

Since $f$ is a polynomial (continuous), IVT gives at least one root in each interval. Two roots confirmed.

---

**D2(a).** $g(x) = f(x)$. $g(0) = -1 < 0 < 5 = g(3)$. Since $0$ is between $f(0)$ and $f(3)$, by IVT $\exists\, c\in(0,3)$ with $f(c)=0$. $\square$

**D2(b).** Let $h(x) = f(x)-x$. $h(0) = f(0)-0 = -1 < 0$ and $h(3) = f(3)-3 = 5-3 = 2 > 0$. By IVT $\exists\, c\in(0,3)$ with $h(c)=0$, i.e., $f(c)=c$. $\square$

**D2(c).** No. IVT guarantees values between $f(a)=-1$ and $f(b)=5$. Since $7 > 5$, the IVT gives no conclusion. Without more information about $f$, we cannot determine whether $f(c)=7$ for some $c$.

---

**D3.** Let position $0$ = bottom, position $1$ = summit. Let $A(t)$ = Hiker A's position at time $t\in[0,6]$ (hours after 8 AM). Let $B(t)$ = Hiker B's position. $A(0)=0, A(6)=1$; $B(0)=1, B(6)=0$. Both are continuous. Let $g(t) = A(t)-B(t)$. Then $g(0) = -1 < 0$ and $g(6) = 1 > 0$. By IVT, $\exists\, c\in(0,6)$ with $g(c)=0$, i.e., $A(c)=B(c)$. At time $c$ hours after 8 AM, both hikers are at the same position. $\square$

---

## Part E

**E1.** The reasoning is incomplete. The student verified (2) $\lim_{x\to2}f(x)=5$ and (3) the limit equals $f(2)=5$ simultaneously. But the three requirements are: (1) $f(2)$ is defined, (2) $\lim_{x\to2}f(x)$ exists, (3) they are equal. The student assumed all three without stating them. A complete argument must verify each separately.

**E2.**
(a) Domain: $\mathbb{R}\setminus\{3\}$ (denominator zero at $x=3$)
(b) $\lim_{x\to3}\dfrac{(x-3)(x+2)}{x-3} = \lim_{x\to3}(x+2) = 5$
(c) $g(x) = x+2$ for all $x\in\mathbb{R}$
(d) Removable discontinuity (limit exists, $f(3)$ undefined)
(e) $f$ is the line $y=x+2$ with a hole at $(3,5)$; $g$ is the complete line.

---

**E3 (Bonus).**

(a) $\left|x\sin\!\left(\frac{1}{x}\right) - 0\right| = |x|\left|\sin\!\left(\frac{1}{x}\right)\right| \leq |x| \to 0$. By Squeeze, $\lim_{x\to0}f(x)=0=f(0)$. Continuous. $\square$

(b) $\lim_{h\to0}\dfrac{f(h)-f(0)}{h} = \lim_{h\to0}\dfrac{h\sin(1/h)}{h} = \lim_{h\to0}\sin(1/h)$.

This limit does not exist (oscillates between $-1$ and $1$). So $f$ is not differentiable at 0.

(c) Continuity does not imply differentiability. A function can be continuous at a point but fail to have a derivative there. This example is pathological but illuminating — the "corner" or "kink" intuition for non-differentiability is insufficient; here there is no geometric corner, just infinite oscillation in the slope.
