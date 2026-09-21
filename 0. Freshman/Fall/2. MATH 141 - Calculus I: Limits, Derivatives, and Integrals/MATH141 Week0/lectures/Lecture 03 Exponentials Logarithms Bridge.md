# MATH 141 · Calculus I
## Week 0 · Lecture 3 of 4
### Exponentials, Logarithms & the Bridge to Calculus

**Date:** Thursday 24 September 2026 · 11:00–11:50 · Week 0  <!-- 4th lecture in a 3-day week; see Calendar Reconciliation -->

---

**Course:** MATH 141: Calculus I  
**Reading:** Stewart §1.4–1.5, §1.6 | Spivak Ch. 15 (reference)

---

## The Purpose of This Lecture

We close Week 0 with the two function families that will reappear more than any others in calculus: exponentials and logarithms. Then we build the conceptual bridge between precalculus and calculus; asking the question that calculus was invented to answer: *what is the instantaneous rate of change?*

---

## 1. Exponential Functions: The Deep Picture

### Definition and Basic Properties

For $a > 0$, $a \neq 1$, the exponential function is:
$$f(x) = a^x$$

**Domain:** $\mathbb{R}$  
**Range:** $(0, \infty)$ — always positive, never zero  
**Key point:** $a^0 = 1$ for any valid base

**Laws of exponents** (these must be automatic):

| Law | Formula |
|-----|---------|
| Product | $a^m \cdot a^n = a^{m+n}$ |
| Quotient | $\dfrac{a^m}{a^n} = a^{m-n}$ |
| Power | $(a^m)^n = a^{mn}$ |
| Root | $a^{m/n} = \sqrt[n]{a^m} = (\sqrt[n]{a})^m$ |
| Negative | $a^{-n} = \dfrac{1}{a^n}$ |
| Different bases | $a^n \cdot b^n = (ab)^n$ |

### Growth vs Decay

- If $a > 1$: **exponential growth**: function increases without bound
- If $0 < a < 1$: **exponential decay**: function decreases toward 0

Note: $a^x$ with $0 < a < 1$ can be rewritten as $(1/a)^{-x} = b^{-x}$ where $b = 1/a > 1$. So decay is just growth reflected over the $y$-axis.

### The Natural Base $e$

The most important base is $e \approx 2.71828...$, defined as:

$$e = \lim_{n \to \infty} \left(1 + \frac{1}{n}\right)^n$$

We will prove why $e$ is the "natural" base when we differentiate exponentials in Week 4. The answer: $\dfrac{d}{dx}[e^x] = e^x$ — the exponential function with base $e$ is its own derivative. No other base has this property exactly (without a multiplicative constant).

**Continuous compounding:** If $P$ dollars is invested at annual rate $r$, compounded continuously:
$$A(t) = Pe^{rt}$$

This arises naturally from the limit definition of $e$ — compound $n$ times per year and let $n \to \infty$.

---

## 2. Logarithmic Functions: The Inverse Story

### Definition

$\log_a x$ is the inverse of $a^x$:
$$y = \log_a x \iff a^y = x$$

This means: $\log_a x$ answers the question *"to what power must I raise $a$ to get $x$?"*

**Domain:** $(0, \infty)$  
**Range:** $\mathbb{R}$  
**Key values:** $\log_a 1 = 0$, $\log_a a = 1$

### Special Cases

- **Common logarithm:** $\log_{10} x = \log x$ (standard in engineering)
- **Natural logarithm:** $\log_e x = \ln x$ (standard in calculus and analysis)

### Logarithm Laws (from exponent laws)

| Law | Formula | Comes from |
|-----|---------|-----------|
| Product | $\ln(xy) = \ln x + \ln y$ | $a^m \cdot a^n = a^{m+n}$ |
| Quotient | $\ln(x/y) = \ln x - \ln y$ | $a^m/a^n = a^{m-n}$ |
| Power | $\ln(x^r) = r\ln x$ | $(a^m)^n = a^{mn}$ |
| Change of base | $\log_a x = \dfrac{\ln x}{\ln a}$ | — |

**Inverse relationships:**
$$e^{\ln x} = x \quad (x > 0) \qquad \ln(e^x) = x \quad (x \in \mathbb{R})$$

$$a^{\log_a x} = x \qquad \log_a(a^x) = x$$

### Graph Relationship

The graph of $y = \ln x$ is the reflection of $y = e^x$ over the line $y = x$.

Key behaviors:
- $\ln x \to -\infty$ as $x \to 0^+$ (approaches negative infinity as $x$ approaches 0 from the right)
- $\ln x \to +\infty$ as $x \to +\infty$ (but slower than any power of $x$)
- $\ln e = 1$, $\ln 1 = 0$

---

## 3. Worked Problems: Exponential and Logarithmic Equations

### Exponential Equations

**Example 1:** Solve $4^x = 8$  
Write in same base: $2^{2x} = 2^3 \Rightarrow 2x = 3 \Rightarrow x = 3/2$

**Example 2:** Solve $e^{2x} - 3e^x + 2 = 0$  
Substitute $u = e^x$: $u^2 - 3u + 2 = 0 \Rightarrow (u-1)(u-2) = 0$  
$u = 1 \Rightarrow e^x = 1 \Rightarrow x = 0$  
$u = 2 \Rightarrow e^x = 2 \Rightarrow x = \ln 2$

**Example 3:** Solve $5^{x-2} = 3^x$  
Take $\ln$: $(x-2)\ln 5 = x\ln 3$  
$x\ln 5 - 2\ln 5 = x\ln 3$  
$x(\ln 5 - \ln 3) = 2\ln 5$  
$x = \dfrac{2\ln 5}{\ln 5 - \ln 3} = \dfrac{2\ln 5}{\ln(5/3)}$

### Logarithmic Equations

**Example 4:** Solve $\ln(x+1) + \ln(x-1) = \ln 3$  
$\ln[(x+1)(x-1)] = \ln 3$  
$(x+1)(x-1) = 3$  
$x^2 - 1 = 3 \Rightarrow x^2 = 4 \Rightarrow x = \pm 2$

Check: $x = -2$ gives $\ln(-1)$ — undefined. ❌  
$x = 2$: $\ln(3) + \ln(1) = \ln 3 + 0 = \ln 3$ ✅

**Example 5:** Solve $\log_2(x) + \log_2(x-2) = 3$  
$\log_2[x(x-2)] = 3 \Rightarrow x(x-2) = 8$  
$x^2 - 2x - 8 = 0 \Rightarrow (x-4)(x+2) = 0$  
$x = 4$ (valid: $4 > 2$) or $x = -2$ (invalid: $\log_2(-2)$ undefined) ❌  
**Solution:** $x = 4$

---

## 4. Exponential Growth and Decay Models

These appear throughout calculus, physics, and engineering.

### General Model

$$\frac{dy}{dt} = ky$$

This equation says: *the rate of change of $y$ is proportional to $y$ itself.* Its solution (which we'll derive in Week 11 using integration):

$$y(t) = y_0 e^{kt}$$

where $y_0 = y(0)$ is the initial value.

- $k > 0$: exponential growth
- $k < 0$: exponential decay

### Half-Life

For radioactive decay, the **half-life** $T_{1/2}$ is the time for half the substance to decay:
$$\frac{1}{2}y_0 = y_0 e^{kT_{1/2}} \Rightarrow e^{kT_{1/2}} = \frac{1}{2} \Rightarrow T_{1/2} = \frac{\ln(1/2)}{k} = -\frac{\ln 2}{k}$$

### Doubling Time

For growth, the **doubling time** $T_2$ is when $y = 2y_0$:
$$T_2 = \frac{\ln 2}{k}$$

**Rule of 70:** For a growth rate of $r\%$ per year, doubling time $\approx 70/r$ years. This is the continuous-compounding version, using $\ln 2 \approx 0.693 \approx 70/100$.

---

## 5. The Bridge to Calculus: The Average Rate of Change

We are now ready to ask the question that calculus was invented to answer.

### Average Rate of Change

The **average rate of change** of $f$ on $[a, b]$ is:
$$\frac{f(b) - f(a)}{b - a} = \frac{\Delta y}{\Delta x}$$

This is the slope of the **secant line** connecting $(a, f(a))$ and $(b, f(b))$.

**Example:** For $f(x) = x^2$, the average rate of change from $x = 1$ to $x = 3$:
$$\frac{f(3) - f(1)}{3 - 1} = \frac{9 - 1}{2} = 4$$

The secant line from $(1, 1)$ to $(3, 9)$ has slope 4.

### The Instantaneous Rate of Change (Preview)

What if we want the rate of change *at a single point* $x = 1$? A single point gives:
$$\frac{f(1) - f(1)}{1 - 1} = \frac{0}{0}$$

This is undefined — the **$0/0$ indeterminate form**. This is exactly why Newton and Leibniz invented calculus: to give meaning to this expression.

The key idea: let $b$ approach $a$:
$$\text{Instantaneous rate} = \lim_{b \to a} \frac{f(b) - f(a)}{b - a}$$

For $f(x) = x^2$ at $x = 1$, compute the average rate over $[1, 1+h]$:
$$\frac{(1+h)^2 - 1}{h} = \frac{1 + 2h + h^2 - 1}{h} = \frac{2h + h^2}{h} = 2 + h$$

As $h \to 0$, this approaches $2$. The instantaneous rate of change of $x^2$ at $x = 1$ is $2$. This is the **derivative** — what the entire next three months are about.

---

## 6. Rates of Change in Computer Science

### Algorithm Growth Rates

The "rate of change" of an algorithm's runtime as input size grows is exactly the derivative-like concept behind Big-O analysis.

For $T(n) = n^2$:
- Average rate of change from $n$ to $n+1$: $(n+1)^2 - n^2 = 2n + 1 \approx 2n$ for large $n$
- This is why we say the "growth rate" of $n^2$ is $O(n)$ — the *derivative* of $n^2$ is $2n$

For $T(n) = e^n$:
- Average rate: $e^{n+1} - e^n = e^n(e - 1) \approx 1.718 \cdot e^n$
- The growth rate of an exponential is proportional to itself — *it gets worse as fast as it is*

This is why exponential-time algorithms are intractable: their difficulty grows as fast as their current size.

### Signal Decay and Transmission

Network signals decay exponentially with distance:
$$P(d) = P_0 e^{-\alpha d}$$

where $\alpha$ is the attenuation coefficient. Understanding logarithms lets you work with **decibels** (logarithmic scale for power ratios):
$$\text{dB} = 10 \log_{10}\left(\frac{P_2}{P_1}\right)$$

---

## 7. The Conceptual Framework of Calculus

We close this week with the big picture.

### Three Central Problems

Calculus was developed to solve three interconnected problems:

**1. The Tangent Problem (Differential Calculus)**  
Given a curve $y = f(x)$, find the slope of the line tangent to the curve at a point.  
*Solution:* The derivative $f'(a) = \displaystyle\lim_{h\to 0}\frac{f(a+h)-f(a)}{h}$

**2. The Area Problem (Integral Calculus)**  
Given a curve $y = f(x)$, find the area between the curve and the $x$-axis on $[a,b]$.  
*Solution:* The definite integral $\displaystyle\int_a^b f(x)\,dx$

**3. The Accumulation Problem**  
Given a rate of change, find the total accumulated change.  
*Example:* Given velocity $v(t)$, find total displacement $\displaystyle\int_a^b v(t)\,dt$

**The Fundamental Theorem of Calculus** connects problems 1 and 2 — differentiation and integration are inverse operations. This is the deepest theorem in the course, and everything builds toward it (Week 9).

### What the Course Looks Like

```
Week 0:  Precalculus Review       ← You are here
Week 1:  Limits (formal)
Week 2:  Continuity
Week 3:  The Derivative (definition)
Week 4:  Differentiation Rules
Week 5:  Implicit Diff, Related Rates
Week 6:  Applications: Extrema, MVT
Week 7:  Curve Sketching, Optimization
Week 8:  The Integral (Riemann Sums)
Week 9:  Fundamental Theorem of Calculus  ← The climax
Week 10: Integration Techniques
Week 11: Applications of Integration
Week 12: Review, Taylor Polynomials Preview
```

Each week depends on the ones before. There is no skipping.

---

## 8. Week 0 Synthesis

You now have (or have refreshed) the complete precalculus toolkit:

- **Functions:** definition, domain, range, transformations, composition, inverses
- **Algebra:** equations and inequalities of all types, sign charts, rationalization
- **Geometry:** coordinate plane, distance, lines, circles
- **Exponentials and Logarithms:** laws, equations, growth/decay models
- **Trigonometry:** unit circle, identities, inverse functions

And you have a preview of what's coming:
- The limit as the mathematical tool for capturing "approaching without reaching"
- The derivative as the instantaneous rate of change
- The integral as the accumulated change

**Coming up in Week 1:** We will rigorously define what $\displaystyle\lim_{x \to a} f(x) = L$ means using the $\varepsilon$-$\delta$ definition, and compute limits using limit laws.

---

## Lecture 3 Exercises

1. Solve: $2e^x - 5 = 3e^{-x}$ *(Hint: multiply both sides by $e^x$)*

2. The population of a colony doubles every 6 hours. If there are 100 bacteria initially:
   - (a) Write the population as $P(t) = P_0 e^{kt}$. Find $k$.
   - (b) Find the population after 24 hours.
   - (c) When will the population reach one million?

3. Carbon-14 has a half-life of 5730 years. A sample contains 30% of its original C-14. How old is the sample?

4. For $f(x) = x^3$:
   - (a) Compute the average rate of change from $x = 2$ to $x = 2 + h$
   - (b) Simplify the expression
   - (c) What value does it approach as $h \to 0$?

5. Prove: $\log_a b \cdot \log_b a = 1$ for any valid bases $a, b$.

6. **(Exponential dominance)** Show that $e^x > x^{100}$ for all sufficiently large $x$.  

*(Hint: consider $\ln(e^x) = x$ vs $\ln(x^{100}) = 100\ln x$. Which grows faster?)*

7. Without a calculator, order from smallest to largest:
$$e^\pi, \quad \pi^e, \quad e^e, \quad \pi^\pi$$
*(Hint: use $\ln$ to compare. You may use $e \approx 2.718$, $\pi \approx 3.14159$)*

---

## Week 0 Wrap-Up: What You Must Have Memorized

Before Week 1 begins, the following must be instantly available without thinking:

**Algebra:**
- Factoring formulas (difference of squares, sum/difference of cubes)
- Quadratic formula with discriminant
- Laws of exponents and logarithms

**Trigonometry:**
- Unit circle values at $0, \pi/6, \pi/4, \pi/3, \pi/2$ and their reflections
- Pythagorean identities: $\sin^2\theta + \cos^2\theta = 1$ and variants
- Double angle and half angle formulas

**Functions:**
- Graphs of $x^n$, $e^x$, $\ln x$, $\sin x$, $\cos x$, $\tan x$, $|x|$, $\sqrt{x}$
- Transformation rules
- Domain restriction sources: division by zero, even roots, logarithms

---


### Answers

**1.** Multiplying by $e^x$ gives $2e^{2x}-5e^x-3=0$; with $u=e^x$, $(2u+1)(u-3)=0$. Since $e^x>0$
always, **reject** $u=-\tfrac12$:
$$\boxed{x=\ln3\approx1.0986}$$

**2. (a)** $200=100e^{6k}\Rightarrow\boxed{k=\tfrac{\ln2}{6}\approx0.1155\ \text{h}^{-1}}$
&nbsp;&nbsp;**(b)** $P(24)=100\cdot2^4=\boxed{1600}$ — four doublings.
&nbsp;&nbsp;**(c)** $2^{t/6}=10^4\Rightarrow t=6\log_2(10^4)\approx\boxed{79.7\ \text{hours}}$

**3.** $0.30=\left(\tfrac12\right)^{t/5730}\Rightarrow t=5730\log_2\!\left(\tfrac1{0.30}\right)
\approx\boxed{9950\ \text{years}}$

*(Check: $0.5^{9952.8/5730}=0.3000$ ✓.)* Report 2–3 significant figures — "30%" carries no more
precision, so quoting "9952.8 years" overstates what is known.

**4. (a)** $\dfrac{(2+h)^3-8}{h}$ &nbsp;**(b)** $=\boxed{12+6h+h^2}$ &nbsp;**(c)** $\to\boxed{12}$,
which is $f'(2)=3(2)^2$.

**5.** $\log_ab\cdot\log_ba=\dfrac{\ln b}{\ln a}\cdot\dfrac{\ln a}{\ln b}=\boxed{1}$ — the two
change-of-base factors are reciprocals. Requires $a,b>0$ and $a,b\neq1$.

**6.** Compare logarithms (legitimate because $\ln$ is strictly increasing): $\ln(e^x)=x$ against
$\ln(x^{100})=100\ln x$. Since $\dfrac{x}{100\ln x}\to\infty$, eventually $x>100\ln x$ and hence
$e^x>x^{100}$. $\blacksquare$

The crossover is near $x\approx994$ — worth stating, because "eventually" can be very late and no
amount of testing at small $x$ would reveal the true behaviour.

**7.** Take $\ln$ of each: $e\approx2.718$, $e\ln\pi\approx3.114$, $\pi\approx3.142$,
$\pi\ln\pi\approx3.596$. Since $\ln$ preserves order:
$$\boxed{e^e < \pi^e < e^\pi < \pi^\pi}$$
Numerically $15.15<22.46<23.14<36.46$ ✓. The near-tie between $\pi^e$ and $e^\pi$ differs by under
3% — deciding it *without* logarithms is genuinely hard, which is the point of the exercise.

*End of Week 0: Three Lectures Complete*  
*Assignment 0 released: see `assignments/` folder*  
*Lab 00: Saturday session: see `lab/` folder*  
*Quiz 00: Diagnostic (not graded): see `quiz/` folder*
