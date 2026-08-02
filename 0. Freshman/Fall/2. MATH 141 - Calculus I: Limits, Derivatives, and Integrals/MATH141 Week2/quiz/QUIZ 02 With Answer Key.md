# MATH 141 — Quiz 02
## Administered: start of Week 2, Monday
### Covers: Week 1 — limits, ε-δ, infinite limits and limits at infinity

**Duration:** 15 minutes · Closed book · **20 points**

---

## Section A — Short Answer (2 pts each)

**A1.** State the ε-δ definition of $\lim_{x\to a}f(x)=L$.

**A2.** Evaluate $\displaystyle\lim_{x\to\infty}\frac{3x^2+2x}{x^2-5}$ and justify the method.

**A3.** Evaluate $\displaystyle\lim_{x\to0^+}\frac1x$ and $\displaystyle\lim_{x\to0^-}\frac1x$. Does
$\lim_{x\to0}\frac1x$ exist?

**A4.** Why is $\lim_{x\to0}\frac{1}{x^2}=+\infty$ a legitimate statement while
$\lim_{x\to0}\frac1x=\infty$ is not?

**A5.** List three indeterminate forms and explain what "indeterminate" means.

---

## Section B — Longer (5 pts each)

**B1.** Evaluate $\displaystyle\lim_{x\to\infty}\big(\sqrt{x^2+1}-x\big)$, showing the algebra.

**B2.** Find all horizontal and vertical asymptotes of $f(x)=\dfrac{3x^2+2x}{x^2-5}$.

---

**Total: 20 points**

---

## Answer Key (Instructor Copy)

**A1.** For every $\varepsilon>0$ there exists $\delta>0$ such that
$0<\lvert x-a\rvert<\delta \implies \lvert f(x)-L\rvert<\varepsilon$.

*1 pt for the quantifier order (∀ε ∃δ), 1 for the strict inequality $0<\lvert x-a\rvert$. Reversing
the quantifiers is a whole-mark error.*

**A2.** $\mathbf 3$. Divide numerator and denominator by $x^2$, the highest power in the denominator:
$\dfrac{3+2/x}{1-5/x^2}\to\dfrac{3}{1}$. Equal degrees ⟹ ratio of leading coefficients.

*(Verified: $f(10^7)=3.000000$.)*

**A3.** $+\infty$ and $-\infty$ respectively. **No**, $\lim_{x\to0}\frac1x$ does **not** exist —
the one-sided limits disagree.

*(Verified: $\pm10^8$ at $x=\pm10^{-8}$.)*

**A4.** For $\frac{1}{x^2}$ the two one-sided limits **agree** (both $+\infty$), so a single
two-sided statement is meaningful. For $\frac1x$ they differ in sign, so no single statement covers
both sides.

*Neither says the limit "exists" — both describe how it fails. Award full marks only if the student
notes that $\infty$ is not a number.*

**A5.** Any three of $\frac00$, $\frac\infty\infty$, $\infty-\infty$, $0\cdot\infty$, $1^\infty$,
$0^0$, $\infty^0$.

**Indeterminate** means the **form alone does not determine the limit** — different functions of the
same form can give different answers. It does **not** mean the limit fails to exist.

*Example worth crediting: $\frac{x}{x^2},\frac xx,\frac{x^2}{x}$ are all $\frac\infty\infty$ with
limits $0,1,\infty$.*

**B1.** Rationalise:

$$\sqrt{x^2+1}-x=\frac{(\sqrt{x^2+1}-x)(\sqrt{x^2+1}+x)}{\sqrt{x^2+1}+x}=\frac{1}{\sqrt{x^2+1}+x}\to\mathbf 0$$

*(Verified: $0.000500$ at $x=1000$, decaying like $1/(2x)$.)*

**Marking:** 2 for recognising $\infty-\infty$ as indeterminate, 2 for the rationalisation, 1 for the
value. Answering $0$ by asserting "the $+1$ doesn't matter" earns 2 — right answer, no method.

**B2. Horizontal:** $y=3$, from A2. The same value holds as $x\to-\infty$.

**Vertical:** $x^2-5=0$ at $x=\pm\sqrt5\approx\pm2.236$. The numerator $3x^2+2x$ is nonzero at both
($\approx19.47$ at $+\sqrt5$), so both are genuine vertical asymptotes.

*(Verified: $f$ reaches $\pm43\,500$ within $10^{-4}$ of $\sqrt5$.)*

**Marking:** 2 for the horizontal, 2 for locating both vertical asymptotes, 1 for **checking the
numerator is nonzero** — without that check a removable discontinuity would be misclassified.

---

*MATH 141 · Week 2 · Quiz 02 · © CSE Department*
