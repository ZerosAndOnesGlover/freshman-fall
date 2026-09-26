# MATH 141 · Week 1
## LAB 01 Solutions — INSTRUCTOR ONLY

> **Every numerical value below was computed in Python, not estimated.** Grade the *reasoning and the
> observed trend*, not agreement to the last decimal place.

*(Revised 2026-09-26 to match the 11-question version of the lab, which uses only Week 0–1 Python.)*

---

## Part 1 — When Numerical Tables Lie

| x | `math.sin(math.pi / x)` |
|---|---|
| 1 | 1.2246467991473532e-16 |
| 0.1 | -1.2246467991473533e-15 |
| 0.01 | 1.964386723728472e-15 |
| 0.001 | -3.2141664592756335e-13 |

**Q1.** Every entry is zero apart from round-off, since $\pi/x$ is a whole multiple of $\pi$. The natural
guess is $0$.

**Q2.** $f(2/401) = \sin(200.5\pi) = 1$ and $f(2/403) = \sin(201.5\pi) = -1$. Python prints `1.0` and `-1.0`.
Points arbitrarily close to $0$ give $1$ and $-1$, so the guess of $0$ is wrong.

**Q3.** Near $0$ the graph oscillates faster and faster between $-1$ and $1$ and fills a band. The limit
would have to be one number $L$ that $f(x)$ stays close to for **all** $x$ near $0$. But every interval
around $0$ contains points where $f = 1$ and points where $f = -1$, so no $L$ works. **A table samples a
few points; a limit is a statement about all of them.**

**Exercise 1.2 table.**

| x | original | rationalized |
|---|---|---|
| 1e-4 | 0.49998750062396624 | 0.49998750062496095 |
| 1e-8 | 0.4999999969612645 | 0.49999999875 |
| 1e-12 | 0.5000444502911705 | 0.499999999999875 |
| 1e-15 | 0.44408920985006256 | 0.4999999999999999 |

**Q4.** The original form is good to about 8 digits at `1e-8` and then gets **worse**: 0.50004 at `1e-12`
and 0.444 at `1e-15`. This is **catastrophic cancellation**. A float carries about 16 significant digits.
For tiny $x$, $\sqrt{1+x}$ and $1$ agree in almost all of them, so subtracting leaves mostly round-off
noise. Dividing by the tiny $x$ then magnifies that noise.

**Q5.** The rationalized form, because it has no subtraction of nearly equal numbers. The algebra that
finds the limit by hand also makes the computation stable. The computer is not unreliable; the
*expression* was badly conditioned.

---

## Part 2 — The Limit of sin x / x

| x | sin(x)/x |
|---|---|
| 0.5 | 0.958851077208406 |
| 0.1 | 0.9983341664682815 |
| 0.01 | 0.9999833334166665 |
| −0.1 | 0.9983341664682815 |

**Q6.** It approaches **1**. $\frac{\sin x}{x}$ is even: $\frac{\sin(-x)}{-x} = \frac{-\sin x}{-x} = \frac{\sin x}{x}$.

> **The degrees trap.** A student whose table reads about 0.01745 has a calculator in degree mode. Python's
> `math.sin` is always in radians.

**Q7.** Desmos reports `undefined`. The function has no value at $0$. The curve looks unbroken because the
hole is a single point, which a plot cannot show. The limit exists, but $f(0)$ does not.

**Q8.** At $x = 0.1$: $\cos 0.1 = 0.99500$, $\frac{\sin 0.1}{0.1} = 0.99833$, $\frac{1}{\cos 0.1} = 1.00502$.
The chain holds. As $x \to 0^+$ both outer bounds tend to $\cos 0 = 1$, so the Squeeze Theorem forces the
middle to $1$ as well.

---

## Part 3 — ε-δ Intuition

**Q9.** $\delta = 0.25$. Algebraically, $|(2x+1) - 5| = 2|x - 2| < 0.5$ exactly when $|x-2| < 0.25$. The
graph and the algebra agree.

**Q10.** $\delta = 0.05$ and $\delta = 0.005$. The rule is $\delta = \varepsilon/2$, because the line has
slope 2: moving $x$ by $\delta$ moves $f(x)$ by $2\delta$.

**Q11.** $x^2 < 4.5$ needs $x < 2.1213$; $x^2 > 3.5$ needs $x > 1.8708$. The right side is the tighter one,
so the largest $\delta \approx 0.1213$. The lecture's $\delta = \min(1, 0.5/5) = 0.1$ is **smaller**. That is
fine: a proof needs *a* $\delta$ that works, and any smaller $\delta$ also works. It does not need the largest.

The quantifier order is the thing to check: for **every** ε there **exists** a δ. A student who picks ε in
terms of δ has the logic backwards.

---

## Marking Scheme

- **Method (≈60%).** A stated reason for each observed behaviour, and the hand rationalization before the
  Exercise 1.2 table.
- **Execution (≈40%).** Correct values, sensible precision, and a conclusion that follows from the data.

**Carry-through.** Penalise a wrong value once; award downstream marks if the student reasons
correctly from their own error.

**The failure to watch for:** reporting *what* the computer printed without explaining *why*. "The
table approaches 0.5" is an observation; "the table approaches 0.5 because the conjugate cancels the
removable factor" is the answer. A report that is a transcript earns the execution marks only.

---

*MATH 141 · Week 1 · Lab Solutions · Instructor Copy · © CSE Department*
