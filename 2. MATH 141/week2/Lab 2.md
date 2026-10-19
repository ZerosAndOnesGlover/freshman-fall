---
assessment: Lab 2
course: MATH 141
component: Labs
possible: 20
score: 20
status: graded
started: 2026-10-09
submitted: 2026-10-09
graded: 2026-10-11
source: "LAB 02 Continuity and Bisection.md"
---

# MATH 141 · Lab 2
## Answer Sheet

**Assessment:** `LAB 02 Continuity and Bisection.md`
**Points available:** 20

> Write your answers under each heading. Leave the **Marks** lines alone — they are filled
> in during grading. When you are done, set `status: submitted` in the frontmatter above.

---

### Question 1  (2 points)

**Your answer:**

Continuity at $a$ needs all three: (i) $f(a)$ is defined, (ii) $\lim_{x\to a}f(x)$ exists, (iii) they are equal.

| | Function | Point | Type | Which part fails |
|---|---|---|---|---|
| 1A | $\dfrac{x^2-1}{x-1}$ | $x=1$ | **Removable** | (i): graph is the line $y=x+1$ with a hole at $(1,2)$; the limit is $2$ but $f(1)$ is undefined |
| 1B | $\dfrac1x$ | $x=0$ | **Infinite** | (ii): $f\to+\infty$ from the right and $-\infty$ from the left, so no finite limit exists |
| 1C | $x$ for $x<0$, $x+1$ for $x\ge0$ | $x=0$ | **Jump** | (ii): one-sided limits are $0$ and $1$, so the two-sided limit does not exist |

*Marks: 2 / 2*

---

### Question 2  (3 points)

**Your answer:**

Program:

```python
for k in [1, 3, 5, 7, 9, 11]:
    x = 2 / (k * math.pi)
    print(x, math.sin(1 / x))
```

Output:

| $x$ | $\sin(1/x)$ |
|---|---|
| $0.6366197724$ | $+1$ |
| $0.2122065908$ | $-1$ |
| $0.1273239545$ | $+1$ |
| $0.0909456818$ | $-1$ |
| $0.0707355303$ | $+1$ |
| $0.0578745248$ | $-1$ |

As $k$ increases, $x \to 0$, while $\sin(1/x)$ **alternates exactly between $+1$ and $-1$** and never settles.
The values neither converge nor blow up, so this is an **essential (oscillatory) discontinuity** — part (ii)
fails, but for a different reason than 1B or 1C.

*Marks: 3 / 3*

---

### Question 3  (2 points)

**Your answer:**

Adapted loop:

```python
for x in [1.9, 1.99, 1.999, 2.001, 2.01, 2.1]:
    print(x, (x**3 - 8) / (x - 2))
```

| $x$ | $\dfrac{x^3-8}{x-2}$ |
|---|---|
| $1.9$ | $11.4100$ |
| $1.99$ | $11.9401$ |
| $1.999$ | $11.994001$ |
| $2.001$ | $12.006001$ |
| $2.01$ | $12.0601$ |
| $2.1$ | $12.6100$ |

Values approach $12$ from both sides, so I conjecture $\displaystyle\lim_{x\to2}\frac{x^3-8}{x-2} = 12$.

*Marks: 2 / 2*

---

### Question 4  (3 points)

**Your answer:**

Factor using the difference of cubes, $x^3 - 8 = (x-2)(x^2+2x+4)$:

$$\frac{x^3-8}{x-2} = \frac{(x-2)(x^2+2x+4)}{x-2} = x^2+2x+4,$$

which at $x = 2$ gives $4 + 4 + 4 = 12$. This confirms the conjecture, and the continuous extension is

$$\tilde f(x) = \begin{cases}\dfrac{x^3-8}{x-2}, & x \neq 2\\[6pt] 12, & x = 2.\end{cases}$$

Cancelling $x-2$ **inside the limit** is legitimate because the limit uses only $x$ with
$0 < |x - 2|$: the $\varepsilon$-$\delta$ definition **explicitly excludes** $x = 2$. So within the
limit, $x - 2 \neq 0$ and dividing by it is dividing by a nonzero number. At $x = 2$ itself
(when evaluating $f(2)$) the cancellation would be invalid, because the original expression is
$\frac00$ there — which is exactly why we must *define* $\tilde f(2) = 12$ rather than compute it.

*Marks: 3 / 3*

---

### Question 5  (4 points)

**Your answer:**

Filled-in condition: `fa * fm < 0`.

```python
a = 2.0
b = 3.0
step = 0
while step < 8:
    m = (a + b) / 2
    fa = a**3 - 2*a - 5
    fm = m**3 - 2*m - 5
    print(step + 1, a, b, m, fm)
    if fa * fm < 0:            # the root is in [a, m] when f(a) and f(m) have opposite signs
        b = m
    else:
        a = m
    step = step + 1
```

**Why.** $f(x) = x^3 - 2x - 5$ is a polynomial, hence continuous on $[a, m]$. If $f(a)$ and $f(m)$ have
**opposite signs**, then $f(a)f(m) < 0$, and by the **Intermediate Value Theorem** $f$ takes the value $0$
somewhere between them — so the root lies in $[a, m]$ and we may set $b = m$. Otherwise $f(a)$ and $f(m)$
share a sign and the sign change is in the other half, so we set $a = m$.

Output (8 steps):

| Step | $a$ | $b$ | $m$ | $f(m)$ |
|---|---|---|---|---|
| 1 | 2.0 | 3.0 | 2.5 | 5.625 |
| 2 | 2.0 | 2.5 | 2.25 | 1.890625 |
| 3 | 2.0 | 2.25 | 2.125 | 0.345703125 |
| 4 | 2.0 | 2.125 | 2.0625 | −0.351318359375 |
| 5 | 2.0625 | 2.125 | 2.09375 | −0.008941650390625 |
| 6 | 2.09375 | 2.125 | 2.109375 | 0.166835784912 |
| 7 | 2.09375 | 2.109375 | 2.1015625 | 0.078562259674 |
| 8 | 2.09375 | 2.1015625 | 2.09765625 | 0.034714281559 |

*Marks: 4 / 4*

---

### Question 6  (3 points)

**Your answer:**

```python
a = 2.0
b = 3.0
step = 0
while b - a > 1e-6:
    m = (a + b) / 2
    fa = a**3 - 2*a - 5
    fm = m**3 - 2*m - 5
    if fa * fm < 0:
        b = m
    else:
        a = m
    step = step + 1
print(step, m)
```

The loop runs **20 steps**, and the final midpoint is $m = 2.094552$ to six decimal places. (The true root
is $2.0945514815\ldots$, so the bracket has narrowed to within $10^{-6}$ as required.)

*Marks: 3 / 3*

---

### Question 7  (3 points)

**Your answer:**

Running the Question 6 program with each tolerance:

| $\varepsilon$ | steps | $\lceil\log_2(1/\varepsilon)\rceil$ |
|---|---|---|
| $10^{-4}$ | 14 | 14 |
| $10^{-6}$ | 20 | 20 |
| $10^{-10}$ | 34 | 34 |

The step counts **match the formula exactly**. This is because each bisection step halves the width of the
interval (width $1 \to 1/2 \to 1/4 \to \dots$), so after $n$ steps the width is $2^{-n}$; requiring
$2^{-n} \le \varepsilon$ gives $n \ge \log_2(1/\varepsilon)$.

*Marks: 3 / 3*

---

## Grading Summary

*Filled in by the grader.*

| | |
|---|---|
| **Score** | 20 / 20 |
| **Percent** | 100% |
| **Graded** | 2026-10-11 |

**Feedback:**
All seven questions correct and complete.

- **Q1:** All three types classified correctly, each with the specific part of the definition that fails.
- **Q2:** Table computed at the required points; the exact $\pm1$ alternation identified and classified as
  essential/oscillatory.
- **Q3–Q4:** Values converge to $12$ from both sides; difference-of-cubes factorisation correct; continuous
  extension stated. The cancellation is justified by linking it to the $0<|x-a|$ in the limit definition —
  exactly the marking point.
- **Q5:** Condition `fa*fm < 0` correct, with the IVT reason; all eight output lines match.
- **Q6:** Runs under `while b - a > 1e-6`, 20 steps, root reported correctly.
- **Q7:** Step counts match $\lceil\log_2(1/\varepsilon)\rceil$ for all three tolerances, with the halving
  argument given.

No errors. Full marks.
