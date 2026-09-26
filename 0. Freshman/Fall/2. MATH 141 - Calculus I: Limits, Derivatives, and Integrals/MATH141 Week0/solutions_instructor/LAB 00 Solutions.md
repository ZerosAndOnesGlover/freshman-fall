# MATH 141 · Week 0
## LAB 00 Solutions — INSTRUCTOR ONLY

> **Every numerical value below was computed, not estimated.** Grade the *reasoning and the observed
> trend*, not agreement to the last decimal place. Desmos shows fewer digits than the REPL.

*(Revised 2026-09-26 to match the Desmos-and-REPL version of the lab: 12 questions, Q1–Q12.)*

---

## Part 1 — Function Families

**Q1.** Even powers are symmetric about the *y*-axis ($(-x)^n = x^n$) and never negative. Odd powers are
symmetric about the origin ($(-x)^n = -x^n$).

**Q2.** $(0,0)$ and $(1,1)$ for all five, since $0^n = 0$ and $1^n = 1$. The even powers also pass through
$(-1, 1)$ and the odd powers through $(-1,-1)$, since $(-1)^n = \pm 1$.

**Q3.** On $(0,1)$ the **lowest** power, $x$, is largest: multiplying by a number less than 1 makes it
smaller, so $x > x^2 > \dots > x^5$. On $(1,\infty)$ the order reverses and $x^5$ is largest. At $x = 1$ all
are equal, which is where the order flips.

**Q4.** The curves cross at $x \approx 1.37$ and $x \approx 9.94$. After $9.94$ the exponential stays above
for good. REPL check: `2**9` is 512 < `9**3` = 729, and `2**10` is 1024 > `10**3` = 1000.

**Q5.** $\ln 100 \approx 4.61$ against $\sqrt{100} = 10$; $\ln 10000 \approx 9.21$ against $\sqrt{10000} = 100$.
$\sqrt{x}$ grows much faster. Multiplying $x$ by 100 only **adds** about $4.6$ to $\ln x$, but multiplies
$\sqrt{x}$ by 10.

---

## Part 2 — Transformations

**Q6.** It moves **right** by 2. The vertex is where the squared term is zero, and $x - 2 = 0$ happens at
$x = 2$. So the graph reaches its old $x = 0$ behaviour two units later. **Inside the parentheses,
everything is backwards.**

**Q7.** Vertex $(4, 1)$. Starting from $y = x^2$: a vertical stretch by 3, a shift right by 4, and a shift up by 1.

**Q8.** Where $x^2 - 4 \ge 0$ (that is, $|x| \ge 2$) the graph is unchanged. Where $x^2 - 4 < 0$ (on
$(-2, 2)$) it is reflected in the $x$-axis, because $|y| = -y$ for negative $y$. The dip to $-4$ becomes a
bump to $+4$.

---

## Part 3 — Secant Lines and the Approach to Calculus

**Q9.**

| $h$ | $f(1+h)$ | slope |
|---|---|---|
| 1 | 4 | 3 |
| 0.5 | 2.25 | 2.5 |
| 0.1 | 1.21 | 2.1 |
| 0.01 | 1.0201 | 2.01 |
| 0.001 | 1.002001 | 2.001 |

The REPL prints `2.100000000000002` and `2.0009999999996975`. Accept these rounded.

**Q10.** The slope approaches **2**.
$$\frac{(1+h)^2 - 1}{h} = \frac{2h + h^2}{h} = 2 + h,$$
which equals $2$ at $h = 0$. That cancellation *is* the derivative computation, done before the students
have the word for it.

**Q11.** It turns into the **tangent line** at $(1, 1)$: the line that touches the parabola there and has
slope 2.

**Q12.** The slopes are $15.25$, $12.61$ and $12.0601$, approaching **12**.
$$(2+h)^3 = 8 + 12h + 6h^2 + h^3, \qquad \frac{(2+h)^3 - 8}{h} = 12 + 6h + h^2,$$
which equals $12$ at $h = 0$.

---

## Marking Scheme

- **Method (≈60%).** A stated reason for each observed behaviour, and the hand algebra in Q7, Q10 and Q12.
- **Execution (≈40%).** Correct values, a correct table, and a conclusion that follows from the data.

**Carry-through.** Penalise a wrong value once. Award the downstream marks if the student reasons
correctly from their own error.

**The failure to watch for:** reporting *what* Desmos or the REPL showed without explaining *why*. "The
slope approaches 2" is an observation; "the slope is $2 + h$, so it approaches 2" is the answer.

---

*MATH 141 · Week 0 · Lab Solutions · Instructor Copy · © CSE Department*
