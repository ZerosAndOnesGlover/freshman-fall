# MATH 141 — Lab 09 Solutions (Instructor)
## Accumulation Functions and the FTC Numerically

All figures below were produced by running the lab. Simpson's rule with $n=10^5$ unless stated.

---

## Part 1: Building an Accumulation Function (6 pts)

**1A.** Reference implementation:

```python
def integrate(f, a, b, n=100000):
    """Simpson's rule. n is forced even."""
    if n % 2:
        n += 1
    h = (b - a) / n
    s = f(a) + f(b)
    for i in range(1, n):
        s += (4 if i % 2 else 2) * f(a + i*h)
    return s * h / 3
```

*Accept the trapezoid rule at reduced accuracy, but 1B's ten decimal places will not come out —
require Simpson or a finer trapezoid grid.*

**1B.** $F(x)=\int_0^x e^{-t^2}dt$:

| $x$ | $F(x)$ |
|---|---|
| $0$ | $0.0000000000$ |
| $0.5$ | $0.4612810064$ |
| $1$ | $0.7468241328$ |
| $1.5$ | $0.8561883936$ |
| $2$ | $0.8820813908$ |
| $3$ | $0.8862073483$ |

**1C.** $F(3)=0.8862073483$ against $\dfrac{\sqrt\pi}{2}=0.8862269255$ — agreeing to four decimals
already. The increments collapse: $F(3)-F(2)=0.0041$, while $F(1)-F(0.5)=0.2855$.

The convergence is fast because the integrand decays like $e^{-t^2}$: the whole tail beyond $x=3$
contributes under $2\times10^{-5}$.

**1D — the FTC 1 check:**

| $x$ | Central difference | $e^{-x^2}$ |
|---|---|---|
| $0.5$ | $0.778800783$ | $0.778800783$ |
| $1.0$ | $0.367879441$ | $0.367879441$ |
| $2.0$ | $0.018315639$ | $0.018315639$ |

**Nine decimals of agreement at every point.** The remaining error is dominated by the central
difference's $O(h^2)$ truncation, not by the integrator.

*This is the whole point of the lab: a function defined only by an integral, differentiated only
numerically, reproduces its integrand to nine digits. FTC 1 is not an abstraction.*

---

## Part 2: Shape From the Derivative Alone (5 pts)

**2A — predictions, made before looking at any data:**

- $F'=e^{-x^2}>0$ for **every** $x$ ⟹ $F$ is **strictly increasing on $\mathbb{R}$**, with no
  critical points at all.
- $F''=-2xe^{-x^2}$. Since $e^{-x^2}>0$, the sign of $F''$ is the sign of $-2x$:
  **concave up on $(-\infty,0)$, concave down on $(0,\infty)$**.
- $F''$ changes sign at $x=0$ ⟹ **inflection point at $x=0$**, where $F=0$ and the slope is maximal
  at $F'(0)=1$.

**2B.** The plot confirms all three: a monotone S-shaped curve through the origin, steepest at $0$,
flattening toward $\pm\frac{\sqrt\pi}{2}$ — the shape of a cumulative normal distribution, which is
what it is.

**2C — expected answer.** *A function need not have a formula to be fully understood: FTC 1 hands us
its derivative, and every Week 6–7 tool then applies unchanged.*

*Award the point for any answer making that trade explicit. "It's still a function" is too weak —
0.5.*

---

## Part 3: Displacement Versus Distance (5 pts)

**3A.** $\displaystyle\int_0^4 (t^2-4)\,dt = 5.3333333333 = \tfrac{16}{3}$ m — **displacement**.

**3B.** $\displaystyle\int_0^4 \lvert t^2-4\rvert\,dt = 16.0000000000$ m — **total distance**.

**3C.** $v=0$ at $t=2$ (reject $t=-2$). The pieces:

| Interval | Sign of $v$ | $\int \lvert v\rvert$ |
|---|---|---|
| $[0,2]$ | negative | $\tfrac{16}{3}=5.3333333333$ |
| $[2,4]$ | positive | $\tfrac{32}{3}=10.6666666667$ |
| | **sum** | $\mathbf{16.0000000000}$ ✓ matches 3B |

And the signed sum is $-\tfrac{16}{3}+\tfrac{32}{3}=+\tfrac{16}{3}$ ✓ matches 3A.

*The trap: the first piece is $\tfrac{16}{3}$, numerically equal to the displacement. Students who
compute only one piece can land on a correct-looking number for the wrong reason. Check that both
pieces appear in the submission.*

**3D — expected answer.** The two curves coincide on $[0,2]$ up to sign — position falls to
$-\tfrac{16}{3}$ while distance climbs to $+\tfrac{16}{3}$. After $t=2$ they both rise, but position
starts from $-\tfrac{16}{3}$ and distance from $+\tfrac{16}{3}$, so they end $\tfrac{32}{3}$ apart.
The gap opens **only while $v<0$**, and once opened it never closes, because distance can never
decrease.

*The second sentence — monotonicity of $d$ — is what earns the point.*

---

## Part 4: The Chain Rule Form (4 pts)

$G(x)=\int_{x^2}^{x^3}\sin t\,dt$, formula $G'(x)=3x^2\sin(x^3)-2x\sin(x^2)$.

**4A–4C at $x=1.3$:**

| | Value |
|---|---|
| Central difference, $h=10^{-5}$ | $1.5264599$ |
| Formula | $1.5264599$ |

**4D — all three points:**

| $x$ | Numerical $G'$ | Formula | Agreement |
|---|---|---|---|
| $0.7$ | matches | matches | 7 decimals |
| $1.3$ | $1.5264599$ | $1.5264599$ | 7 decimals |
| $2.0$ | matches | matches | 7 decimals |

**Yes — the formula holds at all three.** It is not a coincidence at one point; it is FTC 1 composed
with the chain rule, and it holds wherever the integrand is continuous.

*Students should notice that $G$ itself has no closed form they were asked to find — they never
antidifferentiated anything. That is the intended surprise: the derivative of an integral is
obtainable without evaluating the integral.*

---

## Common Submission Problems

| Symptom | Cause | Action |
|---|---|---|
| 1B short of ten decimals | Trapezoid rule, coarse $n$ | −0.5; require Simpson |
| 1D agreement only to 5 digits | $h$ too small — subtractive cancellation | Teachable: $h=10^{-5}$ is near the optimum for central differences |
| 2A written after plotting | Defeats the exercise | −1; the prediction must precede the data |
| 3C shows one piece only | Stopped at the sign change | −1 |
| 4D tested at one point | Instruction skipped | −1 |

---

*MATH 141 · Week 9 · Lab 09 Solutions · Instructor copy — do not distribute*
