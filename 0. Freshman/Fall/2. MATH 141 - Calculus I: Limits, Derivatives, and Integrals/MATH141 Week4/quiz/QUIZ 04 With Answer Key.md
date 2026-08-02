# MATH 141 · Quiz 04
## Administered: start of Week 4, Monday
### Covers: Week 3 — the derivative, its definition, and differentiability

**Duration:** 15 minutes · Closed book · **20 points**

---

## Section A — Short Answer (2 pts each)

**A1.** State the limit definition of $f'(x)$ as a function.

**A2.** Use the definition to find $f'(x)$ for $f(x)=x^2-3x$.

**A3.** Give the domains of $f(x)=\sqrt x$ and of $f'$. Explain why they differ.

**A4.** State the theorem relating differentiability and continuity, and say whether the converse
holds.

**A5.** Give a function continuous at $0$ but not differentiable there, and name the type of failure.

---

## Section B — Longer (5 pts each)

**B1.** For each, state whether $f$ is differentiable at the point and justify:
(a) $f(x)=|x-2|$ at $x=2$ (b) $f(x)=x^{1/3}$ at $x=0$

**B2.** Find $a$ and $b$ making
$$f(x)=\begin{cases}x^2,&x\le1\\ ax+b,&x>1\end{cases}$$
differentiable at $x=1$. State **both** conditions you used.

---

**Total: 20 points**

---

## Answer Key (Instructor Copy)

**A1.** $f'(x)=\displaystyle\lim_{h\to0}\frac{f(x+h)-f(x)}{h}$, defined wherever the limit exists.
*(1 pt for the quotient, 1 for the domain caveat.)*

**A2.**
$$\lim_{h\to0}\frac{(x+h)^2-3(x+h)-(x^2-3x)}{h}=\lim_{h\to0}\frac{2xh+h^2-3h}{h}=\lim_{h\to0}(2x+h-3)=\mathbf{2x-3}$$

**A3.** $\operatorname{dom}(f)=[0,\infty)$; $\operatorname{dom}(f')=(0,\infty)$, since
$f'(x)=\frac{1}{2\sqrt x}$.

They differ at $x=0$: the difference quotient is $\frac{\sqrt h}{h}=\frac{1}{\sqrt h}\to+\infty$, so
the tangent is **vertical** and no finite derivative exists — even though $f$ is perfectly continuous
there.

**A4.** **Differentiable at $a$ $\Rightarrow$ continuous at $a$.** The **converse is false**.
*(1 pt each. Deduct the second if a student asserts equivalence.)*

**A5.** $f(x)=|x|$ — a **corner**. The one-sided derivatives are $+1$ and $-1$: finite but unequal.

*Also acceptable:* $x^{2/3}$ (cusp) or $x^{1/3}$ (vertical tangent), provided the type is named.

**B1.**

**(a) Not differentiable.** Verified one-sided quotients: $\frac{|2+h-2|}{h}=+1$ for $h>0$ and $-1$
for $h<0$, at every scale tested down to $h=10^{-9}$. Finite but unequal ⟹ no two-sided limit. This
is a **corner**. *(3 pts for the computation, 2 for naming the failure.)*

**(b) Not differentiable.** The quotient is $\frac{h^{1/3}}{h}=h^{-2/3}$, verified as
$100,\ 10^4,\ 10^6$ at $h=10^{-3},10^{-6},10^{-9}$. It diverges to $+\infty$ from **both** sides —
a **vertical tangent**. The function is continuous at $0$; it simply has no finite slope.

*Do not accept "the derivative is infinity" as a claim that it exists. $+\infty$ is not a number.*

**B2.** Two conditions:

**Continuity** (necessary, since differentiability implies it): $1^2=a(1)+b \Rightarrow a+b=1$.

**Matching slopes:** left piece $2x$ gives $2$ at $x=1$; right piece gives $a$. So $a=2$.

Therefore $\mathbf{a=2,\ b=-1}$.

*Verified: both pieces give $1$ at $x=1$, and both slopes are $2$. The line $2x-1$ is exactly the
tangent to $x^2$ at that point.*

**Marking:** 2 pts for the continuity condition, 2 for the slope condition, 1 for the correct pair.
**A student who matches only slopes gets 2 of 5** — that leaves $b$ free and produces a jump, at
which the function is not even continuous.

---

*MATH 141 · Week 4 · Quiz 04 · © CSE Department*
