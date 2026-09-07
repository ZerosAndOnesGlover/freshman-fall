# MATH 141 · Calculus I
## Problem Set 1
### Topic: Limits and Continuity
**Released:** Wednesday, Week 1 · **Due:** Friday, Week 2, 17:00

> **Re-dated 2026-08-16.** This set was previously due Wednesday Week 2 *at the start of class* —
> the same class period that delivers `Lecture 03: The Intermediate Value Theorem`. Part D (12 pts)
> is entirely IVT, so it was collected before the theorem had been taught. The Friday 17:00 deadline
> puts it after Wednesday's lecture and matches the standard problem-set slot in [[Year1 - Freshman/FALL SCHEDULE|FALL SCHEDULE]].
> See [[Year1 - Freshman/PREREQUISITE AUDIT|PREREQUISITE AUDIT]], finding #13.

---

**Instructions:**
- Show all work. Answers without supporting work receive no credit.
- Justify every step with a limit law, theorem, or algebraic identity.
- Box your final answers.
- Collaboration is permitted for discussion of ideas; all written work must be your own.
- Lowest 1 problem set is dropped at end of semester.

---

## Part A — Evaluating Limits (3 pts each)

**A1.** Evaluate each limit, or state that it does not exist (DNE). Justify each answer fully.

(a) $\displaystyle\lim_{x \to 3} \frac{x^2 - 9}{x - 3}$

(b) $\displaystyle\lim_{x \to -2} \frac{x^2 + 5x + 6}{x^2 - x - 6}$

(c) $\displaystyle\lim_{x \to 0} \frac{\sqrt{4 + x} - 2}{x}$
*(Hint: rationalize the numerator)*

(d) $\displaystyle\lim_{x \to 1^-} \frac{|x - 1|}{x - 1}$ and $\displaystyle\lim_{x \to 1^+} \frac{|x - 1|}{x - 1}$. Does the two-sided limit exist?

(e) $\displaystyle\lim_{x \to \infty} \frac{6x^4 - 3x^2 + 7}{2x^4 + x^3 - 5}$

(f) $\displaystyle\lim_{x \to \infty} \left(\sqrt{x^2 + x} - x\right)$
*(Hint: multiply by the conjugate $\dfrac{\sqrt{x^2+x}+x}{\sqrt{x^2+x}+x}$)*

---

**A2.** Use the Squeeze Theorem to evaluate:

(a) $\displaystyle\lim_{x \to 0} \left(x^2 \cos\frac{1}{x^2}\right)$

(b) $\displaystyle\lim_{x \to \infty} \frac{\sin x}{x}$

For each, explicitly state the bounding functions and verify their limits.

---

**A3.** Evaluate using the special trigonometric limits $\displaystyle\lim_{x\to 0}\frac{\sin x}{x} = 1$ and $\displaystyle\lim_{x \to 0} \frac{1 - \cos x}{x} = 0$:

(a) $\displaystyle\lim_{x \to 0} \frac{\sin 7x}{4x}$

(b) $\displaystyle\lim_{x \to 0} \frac{\sin^2 3x}{x^2}$

(c) $\displaystyle\lim_{x \to 0} \frac{1 - \cos 2x}{x}$

(d) $\displaystyle\lim_{x \to 0} \frac{\tan 5x}{\sin 2x}$

---

## Part B — One-Sided Limits and Piecewise Functions (4 pts each)

**B1.** Let
$$f(x) = \begin{cases} x^2 - 1 & x < 0 \\ 2 & x = 0 \\ \sqrt{x} + 1 & 0 < x < 4 \\ 3x - 7 & x \geq 4 \end{cases}$$

Find each of the following, or state DNE:

(a) $\displaystyle\lim_{x \to 0^-} f(x)$, $\quad \displaystyle\lim_{x \to 0^+} f(x)$, $\quad \displaystyle\lim_{x \to 0} f(x)$, $\quad f(0)$

(b) $\displaystyle\lim_{x \to 4^-} f(x)$, $\quad \displaystyle\lim_{x \to 4^+} f(x)$, $\quad \displaystyle\lim_{x \to 4} f(x)$, $\quad f(4)$

(c) Is $f$ continuous at $x = 0$? At $x = 4$? Justify using the three-part definition.

---

**B2.** Find all values of the constants $a$ and $b$ that make the following function continuous everywhere:

$$g(x) = \begin{cases} ax + 3b & x \leq -1 \\ a - 2bx & -1 < x \leq 2 \\ 3a - b + x & x > 2 \end{cases}$$

Show your system of equations and solve it completely.

---

## Part C — Epsilon-Delta Proofs (5 pts each)

**C1.** Using the formal $\varepsilon$-$\delta$ definition, prove:
$$\lim_{x \to 5} (3x - 7) = 8$$

Your proof must: (i) begin with "Given $\varepsilon > 0$," (ii) explicitly state your choice of $\delta$, and (iii) verify the implication.

---

**C2.** Using the formal $\varepsilon$-$\delta$ definition, prove:
$$\lim_{x \to 3} x^2 = 9$$

*(Hint: Restrict $\delta \leq 1$ first to bound the factor $|x + 3|$. Then choose $\delta = \min(1, \varepsilon/7)$.)*

---

**C3.** Use the $\varepsilon$-$\delta$ definition to prove that $\displaystyle\lim_{x \to 2} \frac{1}{x} = \frac{1}{2}$.

*(Hint: Restrict $\delta \leq 1$ so that $x \in (1, 3)$. Then $\left|\frac{1}{x} - \frac{1}{2}\right| = \frac{|x-2|}{2|x|}$. Bound $\frac{1}{|x|}$ using the restriction.)*

---

## Part D — Intermediate Value Theorem (4 pts each)

**D1.** Prove that the equation $x^4 + x - 3 = 0$ has at least two real solutions. Identify intervals containing each solution.

---

**D2.** A continuous function $f$ satisfies $f(0) = -1$ and $f(3) = 5$.

(a) Prove there exists $c \in (0, 3)$ such that $f(c) = 0$.

(b) Prove there exists $c \in (0, 3)$ such that $f(c) = c$.
*(Hint: Define $g(x) = f(x) - x$ and apply IVT.)*

(c) Can you conclude there is a $c$ with $f(c) = 7$? Explain carefully.

---

**D3.** Two hikers start at the bottom of a mountain trail at 8:00 AM on the same day, traveling the same path. Hiker A reaches the summit at 2:00 PM. Hiker B starts at the summit at 8:00 AM and reaches the bottom at 2:00 PM. Prove that at some time between 8:00 AM and 2:00 PM, both hikers were at exactly the same point on the trail.

*(This is a classic IVT application. Define position functions carefully.)*

---

## Part E — Conceptual and Synthesis (6 pts each)

**E1.** A student writes: *"Since $\lim_{x \to 2} f(x) = 5$ and $f(2) = 5$, the function $f$ is continuous at $x = 2$."*

Is this reasoning correct? What is missing? State the complete three-part definition and explain which parts the student verified and which were assumed.

---

**E2.** Consider the function $f(x) = \dfrac{x^2 - x - 6}{x - 3}$.

(a) What is the natural domain of $f$?

(b) Evaluate $\displaystyle\lim_{x \to 3} f(x)$.

(c) Define $g(x)$ to be the continuous extension of $f$ to all of $\mathbb{R}$. Write a formula for $g(x)$.

(d) What type of discontinuity does $f$ have at $x = 3$?

(e) Graph $f$ and $g$ on the same axes, clearly indicating the difference.

---

**E3 (Challenge — 3 bonus pts).** The following function is defined for all $x \in [-1, 1]$:
$$f(x) = \begin{cases} x \sin\!\left(\dfrac{1}{x}\right) & x \neq 0 \\ 0 & x = 0 \end{cases}$$

(a) Prove $f$ is continuous at $x = 0$. *(Use the Squeeze Theorem.)*

(b) Is $f$ differentiable at $x = 0$? To investigate, compute $\displaystyle\lim_{h \to 0} \frac{f(h) - f(0)}{h}$ and determine if it exists.

(c) What does part (b) suggest about the relationship between continuity and differentiability? (This will be made precise in Week 3, where differentiability is shown to imply continuity but not conversely.)

---

## Grading Rubric (Summary)

| Part | Points | Focus |
|------|--------|-------|
| A (6 problems × 3) | 18 | Limit computation techniques |
| B (2 problems × 4) | 8 | Piecewise functions and continuity |
| C (3 problems × 5) | 15 | Epsilon-delta proofs |
| D (3 problems × 4) | 12 | Intermediate Value Theorem |
| E (2 problems × 6) | 12 | Conceptual understanding |
| E3 bonus | 3 | Challenge |
| **Total** | **65 + 3 bonus** | |

---

*Submit to the course portal by 11:59 PM the night before class, or bring a physical copy to class Wednesday.*
