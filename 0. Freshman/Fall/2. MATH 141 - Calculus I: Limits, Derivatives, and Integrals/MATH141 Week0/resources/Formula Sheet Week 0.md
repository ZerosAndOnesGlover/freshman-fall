# MATH 141 · Calculus I
## Week 0 Formula Sheet & Study Reference
### Everything You Must Know Before Calculus Begins

---

*Print this. Put it next to your desk. These formulas should become automatic.*

---

## 1. Algebra: Core Identities

### Factoring
$$a^2 - b^2 = (a+b)(a-b)$$
$$a^3 - b^3 = (a-b)(a^2+ab+b^2)$$
$$a^3 + b^3 = (a+b)(a^2-ab+b^2)$$
$$(a+b)^2 = a^2 + 2ab + b^2$$
$$(a-b)^2 = a^2 - 2ab + b^2$$
$$(a+b)^3 = a^3 + 3a^2b + 3ab^2 + b^3$$
$$(a-b)^3 = a^3 - 3a^2b + 3ab^2 - b^3$$

### Quadratic Formula
$$ax^2 + bx + c = 0 \implies x = \frac{-b \pm \sqrt{b^2-4ac}}{2a}$$

Discriminant: $\Delta = b^2 - 4ac$
- $\Delta > 0$: two real roots
- $\Delta = 0$: one repeated root
- $\Delta < 0$: no real roots

### Absolute Value
$$|x| = \begin{cases} x & x \geq 0 \\ -x & x < 0 \end{cases}$$
$$|ab| = |a||b| \qquad |a+b| \leq |a|+|b|$$
$$|x| < c \iff -c < x < c \quad (c>0)$$
$$|x| > c \iff x > c \text{ or } x < -c$$

---

## 2. Exponents and Logarithms

### Exponent Laws
$$a^m \cdot a^n = a^{m+n} \qquad \frac{a^m}{a^n} = a^{m-n}$$
$$(a^m)^n = a^{mn} \qquad (ab)^n = a^n b^n$$
$$a^0 = 1 \qquad a^{-n} = \frac{1}{a^n} \qquad a^{m/n} = \sqrt[n]{a^m}$$

### Logarithm Laws
$$\log_a(xy) = \log_a x + \log_a y$$
$$\log_a\!\left(\frac{x}{y}\right) = \log_a x - \log_a y$$
$$\log_a(x^r) = r\log_a x$$
$$\log_a x = \frac{\ln x}{\ln a} \quad \text{(change of base)}$$

### Inverse Relationships
$$e^{\ln x} = x \quad (x>0) \qquad \ln(e^x) = x \quad (x \in \mathbb{R})$$

### Key Values
$$\ln 1 = 0 \qquad \ln e = 1 \qquad e \approx 2.71828$$
$$\log_{10} 1 = 0 \qquad \log_{10} 10 = 1$$

---

## 3. Trigonometry

### Unit Circle: Exact Values

| Degrees | Radians | $\sin$ | $\cos$ | $\tan$ |
|---------|---------|--------|--------|--------|
| $0°$ | $0$ | $0$ | $1$ | $0$ |
| $30°$ | $\pi/6$ | $1/2$ | $\sqrt{3}/2$ | $1/\sqrt{3}$ |
| $45°$ | $\pi/4$ | $\sqrt{2}/2$ | $\sqrt{2}/2$ | $1$ |
| $60°$ | $\pi/3$ | $\sqrt{3}/2$ | $1/2$ | $\sqrt{3}$ |
| $90°$ | $\pi/2$ | $1$ | $0$ | undef |
| $120°$ | $2\pi/3$ | $\sqrt{3}/2$ | $-1/2$ | $-\sqrt{3}$ |
| $135°$ | $3\pi/4$ | $\sqrt{2}/2$ | $-\sqrt{2}/2$ | $-1$ |
| $150°$ | $5\pi/6$ | $1/2$ | $-\sqrt{3}/2$ | $-1/\sqrt{3}$ |
| $180°$ | $\pi$ | $0$ | $-1$ | $0$ |
| $270°$ | $3\pi/2$ | $-1$ | $0$ | undef |
| $360°$ | $2\pi$ | $0$ | $1$ | $0$ |

**Signs by quadrant (All Students Take Calculus):**
- Q1: All positive
- Q2: Sin positive
- Q3: Tan positive
- Q4: Cos positive

### Pythagorean Identities
$$\sin^2\theta + \cos^2\theta = 1$$
$$1 + \tan^2\theta = \sec^2\theta$$
$$1 + \cot^2\theta = \csc^2\theta$$

### Angle Addition
$$\sin(A \pm B) = \sin A\cos B \pm \cos A\sin B$$
$$\cos(A \pm B) = \cos A\cos B \mp \sin A\sin B$$
$$\tan(A \pm B) = \frac{\tan A \pm \tan B}{1 \mp \tan A\tan B}$$

### Double Angle
$$\sin(2\theta) = 2\sin\theta\cos\theta$$
$$\cos(2\theta) = \cos^2\theta - \sin^2\theta = 1-2\sin^2\theta = 2\cos^2\theta - 1$$
$$\tan(2\theta) = \frac{2\tan\theta}{1-\tan^2\theta}$$

### Half Angle (Power Reduction) — Essential for Integration
$$\sin^2\theta = \frac{1-\cos(2\theta)}{2} \qquad \cos^2\theta = \frac{1+\cos(2\theta)}{2}$$

### Reciprocal Identities
$$\csc\theta = \frac{1}{\sin\theta} \qquad \sec\theta = \frac{1}{\cos\theta} \qquad \cot\theta = \frac{1}{\tan\theta} = \frac{\cos\theta}{\sin\theta}$$

### Inverse Trig Domains and Ranges
| Function | Domain | Range |
|----------|--------|-------|
| $\arcsin x$ | $[-1,1]$ | $[-\pi/2, \pi/2]$ |
| $\arccos x$ | $[-1,1]$ | $[0, \pi]$ |
| $\arctan x$ | $(-\infty,\infty)$ | $(-\pi/2, \pi/2)$ |

Key limits: $\displaystyle\lim_{x\to\infty}\arctan x = \frac{\pi}{2}$, $\displaystyle\lim_{x\to-\infty}\arctan x = -\frac{\pi}{2}$

---

## 4. Functions: Key Concepts

### Domain Restrictions
| Source | Restriction | Example |
|--------|-------------|---------|
| Even root | radicand $\geq 0$ | $\sqrt{x}$: need $x \geq 0$ |
| Denominator | denom $\neq 0$ | $\frac{1}{x}$: need $x \neq 0$ |
| Logarithm | argument $> 0$ | $\ln x$: need $x > 0$ |
| $\arcsin$, $\arccos$ | argument in $[-1,1]$ | $\arcsin x$: need $|x| \leq 1$ |

### Transformation Rules (starting from $y = f(x)$)
| Transformation | New function | Effect |
|---------------|-------------|--------|
| Vertical shift up $c$ | $f(x)+c$ | Up $c$ |
| Vertical shift down $c$ | $f(x)-c$ | Down $c$ |
| Horizontal shift right $c$ | $f(x-c)$ | Right $c$ |
| Horizontal shift left $c$ | $f(x+c)$ | Left $c$ |
| Vertical stretch ($c>1$) | $cf(x)$ | Stretch vertically |
| Vertical compress ($0<c<1$) | $cf(x)$ | Compress vertically |
| Horizontal compress ($c>1$) | $f(cx)$ | Compress horizontally |
| Reflect over $x$-axis | $-f(x)$ | Flip vertically |
| Reflect over $y$-axis | $f(-x)$ | Flip horizontally |

### Even and Odd Functions
- **Even:** $f(-x) = f(x)$ — symmetric about $y$-axis — examples: $x^2$, $\cos x$, $|x|$
- **Odd:** $f(-x) = -f(x)$ — symmetric about origin — examples: $x^3$, $\sin x$, $x$

### Inverse Function Facts
- $f^{-1}$ exists iff $f$ is one-to-one (passes horizontal line test)
- $(f^{-1})^{-1} = f$
- Domain of $f^{-1}$ = Range of $f$; Range of $f^{-1}$ = Domain of $f$
- Graph of $f^{-1}$ = reflection of graph of $f$ over $y = x$

---

## 5. The Bridge to Calculus

### Average Rate of Change
$$\text{AROC}_{[a,b]} = \frac{f(b) - f(a)}{b - a} = \text{slope of secant line}$$

### Approaching the Derivative
$$f'(a) = \lim_{h \to 0} \frac{f(a+h) - f(a)}{h} \quad \leftarrow \text{(formal definition, Week 3)}$$

### Rationalizing the Numerator — Template
$$\frac{\sqrt{x+h} - \sqrt{x}}{h} \cdot \frac{\sqrt{x+h}+\sqrt{x}}{\sqrt{x+h}+\sqrt{x}} = \frac{1}{\sqrt{x+h}+\sqrt{x}}$$

### Complex Fraction — Template
$$\frac{\frac{1}{x+h} - \frac{1}{x}}{h} = \frac{\frac{x-(x+h)}{x(x+h)}}{h} = \frac{-h}{h \cdot x(x+h)} = \frac{-1}{x(x+h)}$$

---

## 6. Key Number Approximations

$$e \approx 2.71828 \qquad \ln 2 \approx 0.6931 \qquad \ln 10 \approx 2.3026$$
$$\pi \approx 3.14159 \qquad \sqrt{2} \approx 1.4142 \qquad \sqrt{3} \approx 1.7321$$

---

## 7. Things That Are WRONG | Common Errors

❌ $\sqrt{a^2+b^2} = a+b$  
❌ $(a+b)^2 = a^2+b^2$ (missing $2ab$)  
❌ $\frac{a+b}{a} = b$ (can't cancel additive terms)  
❌ $\ln(a+b) = \ln a + \ln b$ (log of sum is NOT sum of logs)  
❌ $\ln(a-b) = \ln a - \ln b$ (log of difference is NOT difference of logs)  
❌ $e^{a+b} = e^a + e^b$ (exponential of sum is NOT sum of exponentials — it's $e^a \cdot e^b$)  
❌ $\sin(A+B) = \sin A + \sin B$  
❌ $\sqrt[n]{a+b} = \sqrt[n]{a} + \sqrt[n]{b}$  
❌ $\log_a(x^n) = (\log_a x)^n$ (the exponent comes outside as a multiplier, not a power)

---

*Keep this sheet. Refer to it when stuck. Internalize it over the first two weeks. By Week 3, you should no longer need it.*
