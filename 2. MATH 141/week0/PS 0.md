---
assessment: PS 0
course: MATH 141
component: Problem Sets
possible: 100
score:
status: submitted
started: 2026-09-28
submitted: 2026-10-09
source: Problem Set 0.md
---

# MATH 141 · PS 0

## Answer Sheet

**Assessment:** `Problem Set 0.md`
**Points available:** 100

> Write your answers under each heading. Leave the **Marks** lines alone — they are filled
> in during grading. When you are done, set `status: submitted` in the frontmatter above.

---

### Problem 1 — Domains (12 points)

**Your answer:**

The domain is the set of x-values for which the expression is defined.

- For polynomials, the domain is all real numbers.
- For fractions, the denominator cannot be zero.
- For square roots, the radicand must be greater than or equal to zero.
- For logarithms, the argument must be positive.

Examples:

- $f(x)=\sqrt{x-4}$ has domain $[4,\infty)$.
- $f(x)=\frac{1}{x-3}$ has domain $\mathbb{R}\setminus\{3\}$.
- $f(x)=\ln(x+2)$ has domain $(-2,\infty)$.
- $f(x)=\frac{\sqrt{x^2-9}}{x-5}$ requires $x^2-9\ge 0$ and $x\ne 5$, so the domain is $(-\infty,-3]\cup[3,\infty)$ with $x\ne 5$.

_Marks: \_\_\_ / 12_

---

### Problem 2 — A Function That Undoes Itself (12 points)

**Your answer:**

A function that undoes itself satisfies $f(f(x))=x$. This is called an involution.

Examples:

- $f(x)=x$ works because $f(f(x))=x$.
- $f(x)=c-x$ works because $f(f(x))=c-(c-x)=x$.
- $f(x)=\frac{1}{x}$ works for $x\ne 0$ because $f(f(x))=\frac{1}{1/x}=x$.

So a function can undo itself when applying it twice returns the original input.

_Marks: \_\_\_ / 12_

---

### Problem 3 — Equations (12 points)

**Your answer:**

To solve an equation, isolate the variable or factor if needed, then check the solution in the original equation.

Examples:

- $2x+7=15 \Rightarrow 2x=8 \Rightarrow x=4$
- $x^2-5x+6=0 \Rightarrow (x-2)(x-3)=0 \Rightarrow x=2,3$
- $3^{x+1}=81=3^4 \Rightarrow x+1=4 \Rightarrow x=3$

The key is to use inverse operations and verify the result.

_Marks: \_\_\_ / 12_

---

### Problem 4 — Inequalities (12 points)

**Your answer:**

Inequalities are solved by finding the critical values where the expression is zero or undefined, then checking intervals.

Examples:

- $x^2-4>0 \Rightarrow (x-2)(x+2)>0 \Rightarrow x<-2$ or $x>2$
- $3x-5\le 7 \Rightarrow 3x\le 12 \Rightarrow x\le 4$
- $\frac{1}{x-2}>0 \Rightarrow x>2$

The solution set must be checked against sign changes on the number line.

_Marks: \_\_\_ / 12_

---

### Problem 5 — Rationalizing (10 points)

**Your answer:**

Rationalizing removes radicals from the denominator by multiplying numerator and denominator by a conjugate or equivalent factor.

Examples:

- $\frac{1}{\sqrt{5}-2} = \frac{\sqrt{5}+2}{(\sqrt{5}-2)(\sqrt{5}+2)} = \sqrt{5}+2$
- $\frac{2}{\sqrt{x}+1} = \frac{2(\sqrt{x}-1)}{x-1}$
- $(\sqrt{a}-\sqrt{b})(\sqrt{a}+\sqrt{b}) = a-b$

This keeps the expression equivalent while making it easier to simplify or evaluate.

_Marks: \_\_\_ / 10_

---

### Problem 6 — Exponential and Logarithmic Equations (12 points)

**Your answer:**

Use exponential and logarithmic inverses to solve these.

Examples:

- $2^{x+1}=16=2^4 \Rightarrow x+1=4 \Rightarrow x=3$
- $\log_2(x-1)=3 \Rightarrow x-1=2^3=8 \Rightarrow x=9$
- $\ln x=5 \Rightarrow x=e^5$
- $\log(2x+1)=\log 7 \Rightarrow 2x+1=7 \Rightarrow x=3$

The key idea is that exponentials and logs are inverse operations.

_Marks: \_\_\_ / 12_

---

### Problem 7 — Half-Life (12 points)

**Your answer:**

The half-life model is:

$$A(t)=A_0\left(\frac{1}{2}\right)^{t/h}$$

where $A_0$ is the initial amount, $h$ is the half-life, and $t$ is elapsed time.

Example:

- If $A_0=100$ grams and the half-life is 5 years, then after 15 years,
  $$A(15)=100\left(\frac{1}{2}\right)^{15/5}=100\left(\frac{1}{2}\right)^3=12.5\text{ g.}$$

In general, solving for time gives:

$$t=h\log_2\left(\frac{A_0}{A}\right).$$

_Marks: \_\_\_ / 12_

---

### Problem 8 — Trigonometry (18 points)

**Your answer:**

Key identities:

- $\sin^2\theta+\cos^2\theta=1$
- $1+\tan^2\theta=\sec^2\theta$
- $\sin(\theta+2\pi k)=\sin\theta$
- $\cos(\theta+2\pi k)=\cos\theta$
- $\tan(\theta+\pi k)=\tan\theta$

Examples:

- $\sin\theta=\frac{1}{2}$ gives $\theta=30^\circ+360^\circ k$ or $150^\circ+360^\circ k$
- $\cos\theta=\frac{\sqrt{3}}{2}$ gives $\theta=30^\circ+360^\circ k$ or $330^\circ+360^\circ k$
- $\tan\theta=\sqrt{3}$ gives $\theta=60^\circ+180^\circ k$
- On $[0,2\pi)$, $\sin\theta=\frac{1}{2}$ occurs at $\theta=\frac{\pi}{6}$ and $\frac{5\pi}{6}$.

Trigonometric equations are solved using the unit circle and periodicity.

_Marks: \_\_\_ / 18_

---

## Grading Summary

_Filled in by the grader._

|             |              |
| ----------- | ------------ |
| **Score**   | \_\_\_ / 100 |
| **Percent** | \_\_\_       |
| **Graded**  | \_\_\_       |

**Feedback:**
