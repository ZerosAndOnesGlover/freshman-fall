# MATH 141 · Calculus I
## Week 1 · Lecture 2 (Tuesday)
### The Formal ε-δ Definition of a Limit

**Date:** Tuesday 25 August 2026 · 11:00–11:50 · Week 1

---

**Reading:** Stewart §2.4 | Spivak Ch. 5 (entire chapter — read it carefully)

---

## Why Formalize?

In Monday's lecture we said: "$\lim_{x \to a} f(x) = L$ means $f(x)$ gets close to $L$ as $x$ gets close to $a$."

This is intuitive but mathematically useless for proofs. Consider:

- How close is "close"?
- Close *enough* for what?
- What if $f(x)$ gets close to $L$ but then moves away again?

The informal definition cannot answer these questions. Mathematicians in the 18th and 19th centuries (particularly Cauchy and Weierstrass) developed the $\varepsilon$-$\delta$ definition to make "close" precise. It is one of the greatest achievements in the history of mathematics — it transformed calculus from a powerful but logically suspect collection of techniques into a rigorous science.

---

## 1. The ε-δ Definition

> **Definition.** $\displaystyle\lim_{x \to a} f(x) = L$ means:
>
> For every $\varepsilon > 0$, there exists $\delta > 0$ such that:
> $$0 < |x - a| < \delta \implies |f(x) - L| < \varepsilon$$

Let's decode every piece of this:

| Symbol/Phrase | Meaning |
|---------------|---------|
| $\varepsilon > 0$ | Any positive "tolerance" for the output |
| $\exists\, \delta > 0$ | We can find a positive "tolerance" for the input |
| $0 < \|x - a\|$ | $x \neq a$ (the limit is about *approaching*, not reaching) |
| $\|x - a\| < \delta$ | $x$ is within distance $\delta$ of $a$ |
| $\implies$ | *then* (if the input condition holds...) |
| $\|f(x) - L\| < \varepsilon$ | ...the output is within distance $\varepsilon$ of $L$ |

### The Game-Theoretic Interpretation

Think of it as a game between two players:
- **Skeptic** names any $\varepsilon > 0$ (how close must $f(x)$ be to $L$?)
- **Prover** must respond with a $\delta > 0$ (how close must $x$ be to $a$?)

If the Prover can always find a winning $\delta$ no matter how small $\varepsilon$ is chosen, the limit is $L$.

The limit does **not** exist if the Skeptic can choose an $\varepsilon$ so small that no $\delta$ works.

---

## 2. Geometric Interpretation

The condition $|x - a| < \delta$ means $x \in (a - \delta, a + \delta)$ — a horizontal band of width $2\delta$ around $a$.

The condition $|f(x) - L| < \varepsilon$ means $f(x) \in (L - \varepsilon, L + \varepsilon)$ — a vertical band of height $2\varepsilon$ around $L$.

The $\varepsilon$-$\delta$ definition says: no matter how narrow the horizontal band we draw around $L$, we can always find a vertical band around $a$ such that all points on the graph inside the vertical band also lie inside the horizontal band.

**Visualize:** Draw the graph. Draw horizontal lines at $L - \varepsilon$ and $L + \varepsilon$. The definition requires finding a $\delta$ such that on the interval $(a-\delta, a+\delta)$ (excluding $a$), the graph stays between those horizontal lines.

---

## 3. Epsilon-Delta Proofs — Method and Examples

**Proof strategy:** Given $\varepsilon > 0$, we must produce an explicit $\delta > 0$.
1. Scratch work: find what $\delta$ needs to be (work backwards from $|f(x) - L| < \varepsilon$)
2. Write the proof: assume $0 < |x - a| < \delta$ and verify $|f(x) - L| < \varepsilon$

### Example 1 (Linear function): Prove $\lim_{x \to 3} (2x - 1) = 5$.

**Scratch work:** We need $|f(x) - L| < \varepsilon$, i.e., $|(2x-1) - 5| < \varepsilon$.
$$|(2x - 1) - 5| = |2x - 6| = 2|x - 3|$$
We need $2|x - 3| < \varepsilon$, i.e., $|x - 3| < \varepsilon/2$.

So choose $\delta = \varepsilon/2$.

**Formal proof:**

*Given $\varepsilon > 0$, let $\delta = \varepsilon/2$. Suppose $0 < |x - 3| < \delta$. Then:*
$$|(2x - 1) - 5| = |2x - 6| = 2|x - 3| < 2\delta = 2 \cdot \frac{\varepsilon}{2} = \varepsilon$$

*Therefore $\lim_{x \to 3}(2x - 1) = 5$. $\square$*

---

### Example 2 (Quadratic): Prove $\lim_{x \to 2} x^2 = 4$.

**Scratch work:** Need $|x^2 - 4| < \varepsilon$.
$$|x^2 - 4| = |x - 2||x + 2|$$

We need to bound $|x + 2|$. **Strategy:** Assume $\delta \leq 1$ (a restriction we'll impose). Then $|x - 2| < 1$, so $1 < x < 3$, which gives $3 < x + 2 < 5$, so $|x + 2| < 5$.

Therefore: $|x^2 - 4| = |x - 2| \cdot |x + 2| < |x - 2| \cdot 5$.

For this to be $< \varepsilon$: need $|x - 2| < \varepsilon/5$.

**Choose $\delta = \min(1, \varepsilon/5)$.**

**Formal proof:**

*Given $\varepsilon > 0$, let $\delta = \min(1, \varepsilon/5)$. Suppose $0 < |x - 2| < \delta$.*

*Since $\delta \leq 1$, we have $|x - 2| < 1$, so $-1 < x - 2 < 1$, i.e., $1 < x < 3$. Thus $3 < x + 2 < 5$, giving $|x + 2| < 5$.*

*Therefore:*
$$|x^2 - 4| = |x - 2||x + 2| < \delta \cdot 5 \leq \frac{\varepsilon}{5} \cdot 5 = \varepsilon$$

*So $\lim_{x \to 2} x^2 = 4$. $\square$*

---

### Example 3: Prove the limit does NOT exist.

Prove $\lim_{x \to 0} \dfrac{|x|}{x}$ does not exist.

**Strategy:** Show that no single $L$ can satisfy the definition by finding an $\varepsilon$ that breaks any candidate.

For $x > 0$: $|x|/x = 1$. For $x < 0$: $|x|/x = -1$.

For any proposed limit $L$, let $\varepsilon = 1/2$. In any interval $(-\delta, \delta)$, there are points where $f(x) = 1$ and points where $f(x) = -1$. These are distance 2 apart; they cannot both be within $1/2$ of the same $L$. So no $\delta$ works. $\square$

---

## 4. Proving the Two Special Trigonometric Limits

### $\lim_{x \to 0} \dfrac{\sin x}{x} = 1$

**Proof using the Squeeze Theorem:**

For $0 < x < \pi/2$, compare areas:
- Area of triangle $\triangle OAP$ (where $P = (\cos x, \sin x)$, $A = (1,0)$, $O$ = origin): $\frac{1}{2}\cos x \sin x$
- Area of circular sector $OAP$: $\frac{1}{2}x$ (sector of unit circle with angle $x$)
- Area of triangle $\triangle OAT$ (where $T = (1, \tan x)$): $\frac{1}{2}\tan x$

From the containment of regions:
$$\frac{1}{2}\cos x \sin x \leq \frac{x}{2} \leq \frac{1}{2}\tan x$$

Multiply through by $\dfrac{2}{\sin x}$ (positive for $0 < x < \pi/2$):
$$\cos x \leq \frac{x}{\sin x} \leq \frac{1}{\cos x}$$

All three quantities are positive on $(0, \pi/2)$, so taking reciprocals reverses the chain — the
outer terms swap places and the middle becomes $\dfrac{\sin x}{x}$:
$$\cos x \leq \frac{\sin x}{x} \leq \frac{1}{\cos x}$$

As $x \to 0^+$: $\cos x \to 1$ and $\dfrac{1}{\cos x} \to 1$.

By Squeeze: $\displaystyle\lim_{x \to 0^+} \dfrac{\sin x}{x} = 1$.

Since $\dfrac{\sin x}{x}$ is even, the left limit also equals 1. Therefore:
$$\lim_{x \to 0} \frac{\sin x}{x} = 1$$

### $\lim_{x \to 0} \dfrac{1 - \cos x}{x} = 0$

**Proof:** Multiply by $\dfrac{1 + \cos x}{1 + \cos x}$:

$$\frac{1 - \cos x}{x} = \frac{1 - \cos^2 x}{x(1 + \cos x)} = \frac{\sin^2 x}{x(1 + \cos x)} = \frac{\sin x}{x} \cdot \frac{\sin x}{1 + \cos x}$$

As $x \to 0$:
$$\frac{\sin x}{x} \to 1 \quad \text{and} \quad \frac{\sin x}{1 + \cos x} \to \frac{0}{1 + 1} = 0$$

Therefore $\displaystyle\lim_{x \to 0} \frac{1 - \cos x}{x} = 1 \cdot 0 = 0$. $\square$

---

## 5. The ε-δ Definition and Computer Science

The $\varepsilon$-$\delta$ definition is the mathematical ancestor of **numerical tolerances** and **convergence criteria** in computing:

- **Iterative algorithms** (Newton's method, gradient descent): "stop when the change is less than $\varepsilon$"
- **Floating-point comparison**: never test `a == b` for floats; test `|a - b| < ε`
- **Convergence tests**: a sequence converges if for every $\varepsilon > 0$, there exists $N$ such that for all $n > N$, $|a_n - L| < \varepsilon$

This is not coincidence — the designers of numerical algorithms are implementing the mathematical definition of convergence in code.

---

## 6. Formal Definitions of One-Sided and Infinite Limits

**Left-hand limit:** $\displaystyle\lim_{x \to a^-} f(x) = L$ means:
$$\forall\,\varepsilon > 0,\; \exists\,\delta > 0: a - \delta < x < a \implies |f(x) - L| < \varepsilon$$

**Right-hand limit:** $\displaystyle\lim_{x \to a^+} f(x) = L$ means:
$$\forall\,\varepsilon > 0,\; \exists\,\delta > 0: a < x < a + \delta \implies |f(x) - L| < \varepsilon$$

**Infinite limit:** $\displaystyle\lim_{x \to a} f(x) = +\infty$ means:
$$\forall\,M > 0,\; \exists\,\delta > 0: 0 < |x - a| < \delta \implies f(x) > M$$

**Limit at infinity:** $\displaystyle\lim_{x \to \infty} f(x) = L$ means:
$$\forall\,\varepsilon > 0,\; \exists\,N > 0: x > N \implies |f(x) - L| < \varepsilon$$

---

## Summary

The $\varepsilon$-$\delta$ definition transforms the intuitive phrase "getting close" into a precise, quantified statement. The key insight:

> **The order of quantifiers matters critically.** "For all $\varepsilon$, there exists $\delta$" is completely different from "there exists $\delta$, for all $\varepsilon$." The former is the limit; the latter would be trivially false for most functions.

This sensitivity to quantifier order is shared with computer science: `∀x, ∃y: P(x,y)` (for every input there is some output) vs `∃y, ∀x: P(x,y)` (one output works for all inputs) are entirely different logical claims.

---

## Lecture 2 Exercises

1. **(ε-δ proof)** Prove that $\displaystyle\lim_{x \to 4} \sqrt{x} = 2$ using the $\varepsilon$-$\delta$ definition.  
   *Hint: Use the identity $|\sqrt{x} - 2| = \dfrac{|x-4|}{|\sqrt{x}+2|}$ and note $\sqrt{x} + 2 \geq 2$ for $x \geq 0$.*

2. **(ε-δ proof)** Prove $\displaystyle\lim_{x \to -1} (3x^2 + x) = 2$.

3. Use the two special trig limits to find:
   - (a) $\displaystyle\lim_{x \to 0} \dfrac{\sin 5x}{3x}$
   - (b) $\displaystyle\lim_{x \to 0} \dfrac{\tan x}{x}$
   - (c) $\displaystyle\lim_{x \to 0} \dfrac{\sin^2 x}{x}$

4. **(Reading the definition)** Consider the statement: "There exists $\delta > 0$ such that for all $\varepsilon > 0$, $0 < |x-a| < \delta \implies |f(x) - L| < \varepsilon$." Explain why this is *not* the definition of a limit and what it would mean if it were true.

5. **(Challenge)** The $\varepsilon$-$\delta$ definition says the limit is $L$ if the Prover can always respond to any $\varepsilon$. Write a formal proof (or disproof) that $\displaystyle\lim_{x \to 0} \dfrac{x \sin(1/x)}{1} = 0$. Note: $|\sin(1/x)| \leq 1$ for all $x \neq 0$.

---


### Answers

**1.** Given $\varepsilon>0$. Using the hint, for $x\geq0$:
$$\left|\sqrt x-2\right|=\frac{|x-4|}{\sqrt x+2}\leq\frac{|x-4|}{2}$$
since $\sqrt x+2\geq2$. So choosing $\boxed{\delta=2\varepsilon}$ (and $\delta\leq4$ to keep
$x\geq0$) gives $|x-4|<\delta \Rightarrow |\sqrt x-2|<\varepsilon$. $\blacksquare$

The trick is the **conjugate**: it converts a difference of roots into a difference of the
arguments, which is what $\delta$ controls.

**2.** First check the value: $3(-1)^2+(-1)=2$ ✓. Then
$$\left|3x^2+x-2\right|=\left|(x+1)(3x-2)\right|=|x+1|\,|3x-2|$$
Restrict to $\delta\leq1$, so $|x+1|<1$ gives $-2<x<0$ and hence $|3x-2|<8$. Then
$$|3x^2+x-2|<8|x+1|<\varepsilon \quad\text{whenever}\quad |x+1|<\frac{\varepsilon}{8}$$
Take $\boxed{\delta=\min\left(1,\ \varepsilon/8\right)}$. $\blacksquare$

The two-stage choice — bound the *other* factor first, then solve — is the standard technique for
any non-linear $\varepsilon$-$\delta$ proof.

**3. (a)** $\dfrac{\sin5x}{3x}=\dfrac53\cdot\dfrac{\sin5x}{5x}\to\boxed{\dfrac53}$

**(b)** $\dfrac{\tan x}{x}=\dfrac{\sin x}{x}\cdot\dfrac{1}{\cos x}\to1\cdot1=\boxed{1}$

**(c)** $\dfrac{\sin^2x}{x}=\sin x\cdot\dfrac{\sin x}{x}\to0\cdot1=\boxed{0}$

*(All three confirmed numerically at $x=10^{-3}$ and $10^{-5}$.)*

**4.** The quantifiers are **reversed**. The real definition is
$$\forall\varepsilon>0\ \ \exists\delta>0 \ \ \ldots$$
so $\delta$ is allowed to depend on $\varepsilon$ — a smaller tolerance may demand a smaller
neighbourhood. The stated version asserts **one single $\delta$ works for every $\varepsilon$**,
which would force $|f(x)-L|$ to be smaller than *every* positive number on a fixed punctured
neighbourhood — i.e. $f(x)=L$ **identically** near $a$.

So the statement is not a weaker or stronger form of the limit definition; it describes a function
that is **constantly equal to $L$** near $a$. Quantifier order is not a formality — reversing it
changes the meaning entirely.

**5.** $\left|x\sin(1/x)-0\right|=|x|\left|\sin(1/x)\right|\leq|x|$ for all $x\neq0$.

Given $\varepsilon>0$, take $\boxed{\delta=\varepsilon}$. Then $0<|x-0|<\delta$ implies
$|x\sin(1/x)|\leq|x|<\varepsilon$. $\blacksquare$

Note the proof never needs to know *what* $\sin(1/x)$ does — only that it is **bounded**. That is
the entire content of the squeeze argument, made formal.

*Next: Wednesday — Continuity: The Geometric Meaning and the Three-Part Definition*
