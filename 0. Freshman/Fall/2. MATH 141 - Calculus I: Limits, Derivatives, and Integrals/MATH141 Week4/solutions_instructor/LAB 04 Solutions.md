# MATH 141 · Lab 04 Solutions (Instructor)
## Rules, Chains, and Motion

All figures below were produced by running the computation. Students' values should match to the
digits shown.

---

## Part 1: Checking Rules Numerically (6 pts)

### 1A — the central difference converges (2 pts)

$f(x)=(3x^2+1)(x^3-2x)$ at $a=2$; product rule gives exactly $178$.

| $h$ | central difference | absolute error |
|---|---|---|
| $10^{-2}$ | $178.0115000300$ | $1.15\times10^{-2}$ |
| $10^{-4}$ | $178.0000011502$ | $1.15\times10^{-6}$ |
| $10^{-6}$ | $178.0000000124$ | $1.24\times10^{-8}$ |
| $10^{-8}$ | $177.9999980300$ | $1.97\times10^{-6}$ |

Note the error falls by $10^4$ when $h$ falls by $10^2$ — the central difference is **second order**,
$O(h^2)$. Award the 2 marks for observing that, not merely for producing numbers.

### 1B — why it stops improving (2 pts, the marking point)

The full sweep:

| $h$ | error | | $h$ | error |
|---|---|---|---|---|
| $10^{-1}$ | $1.15$ | | $10^{-9}$ | $1.47\times10^{-5}$ |
| $10^{-3}$ | $1.15\times10^{-4}$ | | $10^{-11}$ | $1.92\times10^{-4}$ |
| $10^{-5}$ | $1.32\times10^{-8}$ | | $10^{-13}$ | $1.51\times10^{-1}$ |
| $\mathbf{10^{-6}}$ | $\mathbf{1.24\times10^{-8}}$ ← best | | $10^{-14}$ | $2.12$ |
| $10^{-7}$ | $1.23\times10^{-7}$ | | $\mathbf{10^{-16}}$ | $\mathbf{178}$ — returns **exactly 0** |

**The expected explanation.** Two errors compete:

- **Truncation error** $\sim h^2$, from the approximation itself — shrinks as $h$ shrinks.
- **Rounding error** $\sim \varepsilon/h$, from **subtractive cancellation** — $f(a+h)$ and $f(a-h)$
  agree in more and more leading digits, so their difference loses significance, and dividing by a
  tiny $h$ magnifies what remains.

Total error is minimised where they balance, at $h \approx \varepsilon^{1/3}$. With
$\varepsilon \approx 2.22\times10^{-16}$ that is $6.06\times10^{-6}$ — matching the observed optimum
at $10^{-6}$.

At $h=10^{-16}$, $2+h$ rounds to exactly $2$ in double precision, so the numerator is $0$ and the
whole quotient is $0$.

*This is the same phenomenon as Week 1's $\sqrt{x^2+1}-x$ losing all its digits past $x=10^8$. Full
marks require naming cancellation; "floating point is imprecise" scores 1 of 2.*

### 1C — a second function (2 pts)

$f(x)=\dfrac{x}{\sqrt{x^2+1}}$ at $a=1.2$; exact $\dfrac{1}{(x^2+1)^{3/2}}=0.262370655600$.

| $h$ | numerical | error |
|---|---|---|
| $10^{-2}$ | $0.262381144089$ | $1.05\times10^{-5}$ |
| $10^{-4}$ | $0.262370656649$ | $1.05\times10^{-9}$ |
| $10^{-6}$ | $0.262370655535$ | $6.53\times10^{-11}$ |
| $10^{-8}$ | $0.262370658533$ | $2.93\times10^{-9}$ |

Same shape: best near $10^{-6}$, degrading either side.

---

## Part 2: The Chain Rule, Seen (6 pts)

### 2A (3 pts)

With $f(u)=u^5$ and $u=g(x)=x^2+1$ at $x=1$:

| Quantity | Value |
|---|---|
| $u=g(1)$ | $2$ |
| $\dfrac{df}{du}=5u^4$ at $u=2$ | $80$ |
| $\dfrac{du}{dx}=2x$ at $x=1$ | $2$ |
| Product | $\mathbf{160}$ |

Direct numerical derivative of $(x^2+1)^5$ at $x=1$: $\mathbf{160.000000}$. ✓

*The point is that the chain rule is a genuine factorisation — each factor is computed at its own
input, and $\frac{df}{du}$ is evaluated at $u=g(1)=2$, not at $x=1$. Students who evaluate
$\frac{df}{du}$ at $1$ get $5$ instead of $80$; that is the classic error and it is worth naming.*

### 2B (3 pts)

$F(x)=\sqrt{1+\sin(x^2)}$ decomposes into **three** layers:

| Layer | Function |
|---|---|
| Outer | $\sqrt{\ \cdot\ }$ |
| Middle | $1+\sin(\ \cdot\ )$ |
| Inner | $x^2$ |

$$F'(x)=\frac{1}{2\sqrt{1+\sin(x^2)}}\cdot\cos(x^2)\cdot 2x$$

At $x=1$: exact $\mathbf{0.3981570233}$, numerical $0.3981570232$, error $4.6\times10^{-11}$. ✓

*Require the layers to be **written down before differentiating**. The common failure is dropping the
innermost $2x$, which is what the explicit decomposition prevents.*

---

## Part 3: A Complete Motion Analysis (8 pts)

$s(t)=t^4-8t^3+18t^2$ on $[0,4]$.

### 3A — the table (2 pts)

| $t$ | $s(t)$ | $v(t)$ | $a(t)$ |
|---|---|---|---|
| $0$ | $0.00$ | $0.00$ | $36.00$ |
| $1$ | $11.00$ | $16.00$ | $0.00$ |
| $2$ | $24.00$ | $8.00$ | $-12.00$ |
| $3$ | $27.00$ | $0.00$ | $0.00$ |
| $4$ | $32.00$ | $16.00$ | $36.00$ |

### 3B — zeros (2 pts)

$$v(t)=4t^3-24t^2+36t=4t(t^2-6t+9)=\mathbf{4t(t-3)^2}$$
$$a(t)=12t^2-48t+36=\mathbf{12(t-1)(t-3)}$$

$v=0$ at $t=0$ and $t=3$ (**double root**). $a=0$ at $t=1$ and $t=3$.

*The factoring is required; grinding the cubic numerically loses the structure that 3D depends on.*

### 3C — the sketches (2 pts)

Look for three stacked graphs sharing a time axis, with:

- $v=0$ marked at $t=0,3$ on the $s$ graph — **horizontal tangents** on $s$.
- $a=0$ marked at $t=1,3$ on the $v$ graph — **turning points of $v$**, i.e. inflection points of $s$.
- $v$ touching zero at $t=3$ **without crossing** — the graph is tangent to the axis there.

That last feature is the one that carries the mark; a sketch showing $v$ crossing at $t=3$ has missed
the double root.

### 3D — displacement and distance (2 pts, the marking point)

**Displacement** $=s(4)-s(0)=32-0=\mathbf{32}$ m.

**Total distance** $=\mathbf{32}$ m — **they are equal**.

**The required justification, from the factored form:** $v(t)=4t(t-3)^2$. For $t \in (0,4]$ both $4t>0$
and $(t-3)^2 \ge 0$, so $v \ge 0$ throughout — verified across the interval. The zero at $t=3$ is a
**double root**, so $v$ *touches* the axis without changing sign.

The particle therefore never reverses, never retraces ground, and distance equals displacement.

*Contrast Wednesday's lecture example, $v=3(t-1)(t-3)$: **simple** roots, sign genuinely changes, and
distance ($12$ m) exceeded displacement ($4$ m).*

**Marking:** award both marks only for reasoning from the factored form. A student who computes
$|s(3)-s(0)|+|s(4)-s(3)|=27+5=32$ arrives at the right number by splitting unnecessarily — award 1
and point out that the double root made the split redundant.

---

## Common Submission Problems

| Symptom | Cause | Action |
|---|---|---|
| 1B answered "rounding error" with no mechanism | Missed cancellation | −1 |
| 2A evaluates $df/du$ at $x$ rather than $u=g(x)$ | The classic chain-rule error | −2, name it |
| 2B drops the inner $2x$ | Did not decompose first | −2 |
| 3D asserts equality without justification | The question asks for the reasoning | −1 |
| 3C shows $v$ crossing at $t=3$ | Missed the double root | −1 |

---

*MATH 141 · Week 4 · Lab 04 Solutions · Instructor copy — do not distribute*
