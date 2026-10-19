---
assessment: Lab 1
course: MATH 141
component: Labs
possible: 100
score: 96
status: graded
started: 2026-10-02
submitted: 2026-10-05
graded: 2026-10-09
source: "LAB 01 Limits Numerical Graphical.md"
---

# MATH 141 · Lab 1
## Answer Sheet

**Assessment:** `LAB 01 Limits Numerical Graphical.md`
**Points available:** 100

> Write your answers under each heading. Leave the **Marks** lines alone — they are filled
> in during grading. When you are done, set `status: submitted` in the frontmatter above.

---

### Question 1  (9 points)

**Your answer:**

Using `math.sin(math.pi / x)` at the four values:

| $x$ | $f(x) = \sin(\pi/x)$ |
|-----|----------------------|
| 1 | `1.2246467991473532e-16` |
| 0.1 | `-1.2246467991473533e-15` |
| 0.01 | `1.964386723728472e-15` |
| 0.001 | `-3.2141664592756335e-13` |

Every entry is zero apart from round-off ($\pi/x$ is a whole multiple of $\pi$, so $\sin$ should be $0$).
Based only on this table I would guess $\lim_{x\to 0}\sin(\pi/x) = 0$.

*Marks: 9 / 9*

---

### Question 2  (9 points)

**Your answer:**

`math.sin(math.pi / x)` at the two new points:

- $f(2/401) = \sin(200.5\pi) =$ `1.0`
- $f(2/403) = \sin(201.5\pi) =$ `-1.0`

Both $x$-values are within $0.005$ of $0$, yet $f$ equals $1$ at one and $-1$ at the other.
Points arbitrarily close to $0$ take both values, so the function cannot settle on the single value $0$.
My guess from Question 1 was **wrong**: the table only sampled a few lucky points.
*(Note: $2/401$ and $2/403$ are not representable as exact floats, so trailing round-off shifts the argument slightly; I read the $1.0$ / $-1.0$ above directly.)*

*Marks: 9 / 9*

---

### Question 3  (9 points)

**Your answer:**

Desmos: graph `y = sin(pi/x)` for $-0.5 \le x \le 0.5$ (screenshot attached).

Near $x = 0$ the curve oscillates faster and faster between $-1$ and $1$ and fills a solid band
rather than approaching any level. The limit would have to be one number $L$ that $f(x)$ stays close to
for **all** $x$ near $0$. But **every** interval around $0$, no matter how narrow, contains points where
$f = 1$ (at $x = 2/(4k+1)$) and points where $f = -1$ (at $x = 2/(4k+3)$). No single $L$ can be within,
say, $0.5$ of both $1$ and $-1$, so the limit does not exist.

*Marks: 7 / 9*

---

### Question 4  (9 points)

**Your answer:**

Hand rationalization first. For $x \neq 0$,

$$g(x) = \frac{\sqrt{1+x}-1}{x}\cdot\frac{\sqrt{1+x}+1}{\sqrt{1+x}+1}
= \frac{(1+x)-1}{x\,(\sqrt{1+x}+1)}
= \frac{x}{x\,(\sqrt{1+x}+1)}
= \frac{1}{\sqrt{1+x}+1}.$$

| $x$ | original form | rationalized form |
|-----|---------------|-------------------|
| `1e-4` | `0.49998750062396624` | `0.49998750062496095` |
| `1e-8` | `0.4999999969612645` | `0.49999999875` |
| `1e-12` | `0.5000444502911705` | `0.499999999999875` |
| `1e-15` | `0.44408920985006256` | `0.4999999999999999` |

The original form is good to about 8 digits at `1e-8`, then gets **worse**: `0.50004` at `1e-12`
and `0.444` at `1e-15`. This is **catastrophic cancellation** (CS 101 Lecture 04 §4). A float carries
about 16 significant digits. For tiny $x$, $\sqrt{1+x}$ and $1$ agree in almost all of them, so
subtracting two nearly equal numbers leaves mostly round-off noise. Dividing by the tiny $x$ then
magnifies that noise.

*Marks: 9 / 9*

---

### Question 5  (9 points)

**Your answer:**

The **rationalized** form is more trustworthy as $x \to 0$, because it never subtracts nearly equal
numbers — it stays accurate right down to `1e-15` (`0.500000000000000`). This tells us that the algebra
we do to find a limit by hand (here, multiplying by the conjugate to cancel the removable factor) also
makes the computation numerically stable. The computer was not unreliable; the **original expression**
was badly conditioned.

*Marks: 9 / 9*

---

### Question 6  (8 points)

**Your answer:**

Using `math.sin(x) / x`:

| $x$ | $\sin x / x$ |
|-----|--------------|
| $0.5$ | `0.958851077208406` |
| $0.1$ | `0.9983341664682815` |
| $0.01$ | `0.9999833334166665` |
| $-0.1$ | `0.9983341664682815` |

The values appear to approach **1**. The $x = 0.1$ and $x = -0.1$ rows agree because $\frac{\sin x}{x}$
is **even**: $\frac{\sin(-x)}{-x} = \frac{-\sin x}{-x} = \frac{\sin x}{x}$.

*(Values are in radians — a calculator left in degree mode would give about $0.01745$.)*

*Marks: 8 / 8*

---

### Question 7  (8 points)

**Your answer:**

Desmos draws an unbroken curve through $x = 0$, but typing `sin(0)/0` returns **`undefined`**
(division by zero). The picture is misleading because the "hole" is a **single point**
$(0,1)$, and a plot of finite resolution cannot show one missing point. So the limit
$\lim_{x\to 0}\frac{\sin x}{x} = 1$ exists even though $f(0)$ is undefined.

*Marks: 8 / 8*

---

### Question 8  (9 points)

**Your answer:**

`math.cos(0.1) = 0.9950041652780258` and `1 / math.cos(0.1) = 1.0050209184004553`, so at $x = 0.1$:

$$\cos 0.1 = 0.99500 \;\le\; \frac{\sin 0.1}{0.1} = 0.99833 \;\le\; \frac{1}{\cos 0.1} = 1.00502.$$

The chain holds. As $x \to 0^+$ both outer bounds tend to $\cos 0 = 1$; and since
$\frac{\sin x}{x}$ is squeezed between two quantities that both approach $1$, the Squeeze Theorem forces
$\lim_{x\to 0^+}\frac{\sin x}{x} = 1$ as well.

*Marks: 9 / 9*

---

### Question 9  (10 points)

**Your answer:**

With $e = 0.5$ I graph $y = 4.5$ and $y = 5.5$ and widen the band $2-d < x < 2+d$ until $f(x)=2x+1$
first leaves it; the largest $d$ for which the whole band stays inside is $d = 0.25$.

Algebraically, $|(2x+1)-5| = 2\,|x-2| < 0.5$ exactly when $|x-2| < 0.25$, so $\delta = 0.25$.
The graph and the algebra **agree**.

*Marks: 8 / 10*

---

### Question 10  (10 points)

**Your answer:**

- $e = 0.1$: $\;2|x-2| < 0.1 \Rightarrow \delta = 0.05$.
- $e = 0.01$: $\;2|x-2| < 0.01 \Rightarrow \delta = 0.005$.

The rule is $\delta = \varepsilon/2$. It works because the line has **slope 2**: moving $x$ by $\delta$
moves $f(x)$ by $2\delta$, so to keep $|f(x)-5| < \varepsilon$ we must take $\delta = \varepsilon/2$
(the exact largest value; any smaller $\delta$ would also work).

*Marks: 10 / 10*

---

### Question 11  (10 points)

**Your answer:**

For $f(x) = x^2$ and the lines $y = 4 \pm e$ with $e = 0.5$, I need $x^2 < 4.5$ and $x^2 > 3.5$.
From the graph the band around $x = 2$ is cut off on the right where the parabola first crosses
$y = 4.5$, at $x < \sqrt{4.5} = 2.1213$; the left crossing is at $x > \sqrt{3.5} = 1.8708$.
The right side is tighter, so the largest $\delta \approx 2.1213 - 2 = 0.1213$.

The lecture's $\delta = \min(1,\varepsilon/5) = \min(1, 0.1) = 0.1$ is **smaller** than the largest
possible $\delta \approx 0.1213$. That does not matter: an $\varepsilon$-$\delta$ proof only needs *some*
$\delta$ that works, and any smaller $\delta$ automatically works too. It does not have to find the
largest one.

*Marks: 10 / 10*

---

## Grading Summary

*Filled in by the grader.*

| | |
|---|---|
| **Score** | 96 / 100 |
| **Percent** | 96% |
| **Graded** | 2026-10-09 |

**Feedback:**
All numerical values match the answer key, and every behaviour is explained, not merely reported.
The hand rationalization in Q4 is correct and the catastrophic-cancellation argument (from CS 101
Lecture 04 §4) is exactly the point. Q6 identifies the even symmetry; Q7 correctly separates "limit
exists" from "$f(0)$ undefined"; Q8 uses the Squeeze chain correctly. Part 3 is strong: $\delta=\varepsilon/2$
for the slope-2 line, $\delta\approx 0.1213$ for $x^2$, and the observation that a smaller $\delta$
(such as the lecture's $0.1$) is still a valid proof.

Deducted 4 points (2 on Q3, 2 on Q9): the Lab Report Requirements ask for one Desmos screenshot or
link for Q3 and one for Part 3, and neither is attached — the graphs are described but not shown.
Everything else is full marks.
