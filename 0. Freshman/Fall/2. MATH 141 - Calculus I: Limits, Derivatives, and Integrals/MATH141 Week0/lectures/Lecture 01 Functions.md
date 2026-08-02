# MATH 141 Calculus I
## Week 0 · Lecture 1 of 4
### Functions: The Engine of Mathematics

---

**Course:** MATH 141: Calculus I: Limits, Derivatives, and Integrals  
**Semester:** Fall, Year 1  
**Prerequisites:** Precalculus / High School Algebra & Trigonometry  
**Textbook:** Stewart, *Calculus: Early Transcendentals*, 9th ed. (Primary) | Spivak, *Calculus*, 4th ed. (Enrichment)

---

## Why This Lecture Exists Before Calculus Starts

Calculus is the mathematics of *change*. But before you can study how something changes, you need a precise language for describing *what* is changing and *with respect to what*. That language is the **function**.

Everything in calculus: derivatives, integrals, limits; is defined in terms of functions. If your understanding of functions is fuzzy, calculus will feel like magic tricks rather than a coherent discipline. This week is about making functions completely unambiguous.

---

## 1. What Is a Function? The Precise Definition

Informally, a function is a rule that takes an input and produces an output.

**Formally:**

> A **function** $f$ from a set $A$ to a set $B$, written $f: A \to B$, is a rule that assigns to **each** element $x \in A$ **exactly one** element $f(x) \in B$.

The set $A$ is called the **domain**: the set of all legal inputs.  
The set $B$ is called the **codomain**: the set of all *possible* outputs.  
The **range** (or image) is $\{f(x) : x \in A\}$: the set of outputs that are *actually produced*.

> ⚠️ **Codomain ≠ Range.** The codomain is what the function *could* output; the range is what it *does* output. For $f(x) = x^2$ with $f: \mathbb{R} \to \mathbb{R}$, the codomain is $\mathbb{R}$ but the range is $[0, \infty)$. This distinction matters in higher mathematics.

> **Notation reminder.** $[0,\infty)$ is "all reals from 0 up, **including** 0 and never
> reaching infinity." A square bracket includes its endpoint, a parenthesis excludes it,
> and the two ends are chosen **independently** — so $[2,5)$ means $2 \leq x < 5$ and is
> not a typo. Full treatment: [[Lecture 00 The Language of Mathematics]] §4.


**The Critical Requirement: Uniqueness:**  
Each input must map to **exactly one** output. This is the *vertical line test* in visual form: a graph represents a function if and only if every vertical line intersects it at most once.

### Why Uniqueness Matters
If a "function" could map one input to two outputs, the expression $f(x) + 1$ would be ambiguous: you wouldn't know which value to add 1 to. Mathematics requires unambiguity. Functions provide it.

**Example: Is This a Function?**

| Rule | Domain | Function? | Why |
|------|--------|-----------|-----|
| $f(x) = x^2$ | $\mathbb{R}$ | ✅ Yes | Each $x$ gives one value |
| $f(x) = \pm\sqrt{x}$ | $[0,\infty)$ | ❌ No | $f(4) = +2$ or $-2$? Ambiguous |
| $f(x) = \sqrt{x}$ (principal root) | $[0,\infty)$ | ✅ Yes | Now uniquely defined |

---

## 2. Representing Functions: Four Views

A function can be described in four ways, and fluency in all four is essential.

### 2.1 Algebraic (Formula)
$$f(x) = 3x^2 - 2x + 5$$
Most common in calculus. Enables symbolic manipulation.

### 2.2 Graphical (Visual)
Plot $y = f(x)$ in the $xy$-plane. Visual intuition lives here. The graph tells you where the function is increasing, where it's zero, where it has extrema.

### 2.3 Tabular (Numerical)
| $x$ | $f(x)$ |
|-----|--------|
| 0   | 5      |
| 1   | 6      |
| 2   | 13     |
| 3   | 26     |

Useful for experimentally measured functions, discrete data, and numerical approximation.

### 2.4 Verbal (Description)
"$f(x)$ is the square of the distance from $x$ to 3."  
→ $f(x) = (x-3)^2$

Training yourself to move fluidly among all four representations is one of the core skills developed in calculus.

---

## 3. The Domain: Where a Function Lives

The domain is the set of inputs for which the function is defined. When no domain is specified, we assume the **natural domain**, the largest subset of $\mathbb{R}$ for which the formula makes sense.

### Domain Restrictions: Three Sources

**1. Division by Zero**

$$f(x) = \frac{1}{x-3}$$
Domain: $\{x \in \mathbb{R} : x \neq 3\} = (-\infty, 3) \cup (3, \infty)$

> **Notation reminder.** Read this as "the set of all real $x$ **such that** $x$ is not
> equal to 3" — which equals "everything below 3 **union** everything above 3." The
> union appears because "not equal to 3" means "less than 3 **or** greater than 3", and
> "or" is $\cup$. See [[Lecture 00 The Language of Mathematics]] §3 and §5.



**2. Square Roots of Negatives (in $\mathbb{R}$)**

$$g(x) = \sqrt{5 - x}$$
Require $5 - x \geq 0 \Rightarrow x \leq 5$.  
Domain: $(-\infty, 5]$

> **Notation reminder.** $\Rightarrow$ is read "implies", or in a chain of algebra,
> "and therefore". Here: "if $5-x \geq 0$, then $x \leq 5$." See [[Lecture 00 The Language of Mathematics]] §6.


**3. Logarithms of Non-Positives**

$$h(x) = \ln(x^2 - 4)$$
Require $x^2 - 4 > 0 \Rightarrow x^2 > 4 \Rightarrow |x| > 2$.  
Domain: $(-\infty, -2) \cup (2, \infty)$

### Worked Example | Combined Restrictions

Find the domain of $\displaystyle f(x) = \frac{\sqrt{x+1}}{x^2 - x - 6}$

**Step 1:** Numerator requires $x + 1 \geq 0 \Rightarrow x \geq -1$.

**Step 2:** Denominator cannot be zero.  
$x^2 - x - 6 = (x-3)(x+2) = 0 \Rightarrow x = 3$ or $x = -2$.

**Step 3:** Intersect.  
Starting with $x \geq -1$, exclude $x = 3$ (since $-2 < -1$, the other $x$ value of $-2$ exclusion is already handled).

$$\text{Domain} = [-1, 3) \cup (3, \infty)$$

---

## 4. Essential Function Families

### 4.1 Linear Functions
$$f(x) = mx + b$$
- Slope $m$ = rate of change (constant for linear functions)
- $y$-intercept $b$
- Graph: straight line
- **CS Connection:** The simplest "big-O" growth model. An $O(n)$ algorithm has a runtime that is approximately linear.

### 4.2 Power Functions
$$f(x) = x^n \quad (n \in \mathbb{R})$$
- $n = 1$: linear | $n = 2$: parabola | $n = 3$: cubic | $n = 1/2$: square root | $n = -1$: hyperbola
- Key behavior: as $|x| \to \infty$, larger $n$ dominates (for $n > 0$)

### 4.3 Polynomial Functions
$$P(x) = a_n x^n + a_{n-1}x^{n-1} + \cdots + a_1 x + a_0$$
- Domain: all of $\mathbb{R}$
- Degree $n$ polynomial has at most $n$ real roots
- End behavior governed by leading term $a_n x^n$

### 4.4 Rational Functions
$$R(x) = \frac{P(x)}{Q(x)}$$
- Domain excludes zeros of $Q(x)$
- Vertical asymptotes where $Q(x) = 0$ (and $P(x) \neq 0$)
- Horizontal asymptotes determined by degree comparison

### 4.5 Exponential Functions
$$f(x) = a^x \quad (a > 0, a \neq 1)$$
- Domain: $\mathbb{R}$, Range: $(0, \infty)$
- $a > 1$: exponential growth (the basis of Big-O $2^n$ complexity class)
- $0 < a < 1$: exponential decay
- The natural exponential $e^x$ is special: it is its own derivative (revealed in Week 3)

### 4.6 Logarithmic Functions
$$f(x) = \log_a x \quad (a > 0, a \neq 1)$$
- Domain: $(0, \infty)$, Range: $\mathbb{R}$
- Inverse of $a^x$: $y = \log_a x \iff a^y = x$
- **CS Connection:** $\log_2 n$ is the number of times you can halve $n$ before reaching 1. Binary search runs in $O(\log n)$ because each comparison halves the search space.

### 4.7 Trigonometric Functions

| Function | Domain | Range | Period |
|----------|--------|-------|--------|
| $\sin x$ | $\mathbb{R}$ | $[-1,1]$ | $2\pi$ |
| $\cos x$ | $\mathbb{R}$ | $[-1,1]$ | $2\pi$ |
| $\tan x$ | $\mathbb{R} \setminus \{(2k+1)\pi/2\}$ | $\mathbb{R}$ | $\pi$ |
| $\sec x$ | $\mathbb{R} \setminus \{(2k+1)\pi/2\}$ | $(-\infty,-1]\cup[1,\infty)$ | $2\pi$ |
| $\csc x$ | $\mathbb{R} \setminus \{k\pi\}$ | $(-\infty,-1]\cup[1,\infty)$ | $2\pi$ |
| $\cot x$ | $\mathbb{R} \setminus \{k\pi\}$ | $\mathbb{R}$ | $\pi$ |

Key identities (you must know these cold):
$$\sin^2 x + \cos^2 x = 1$$
$$\sin(A \pm B) = \sin A \cos B \pm \cos A \sin B$$
$$\cos(A \pm B) = \cos A \cos B \mp \sin A \sin B$$
$$\sin(2x) = 2\sin x \cos x$$
$$\cos(2x) = \cos^2 x - \sin^2 x = 1 - 2\sin^2 x = 2\cos^2 x - 1$$

---

## 5. Transformations of Functions

Given a base function $f(x)$, we can construct families of related functions:

| Transformation | Formula | Effect |
|---------------|---------|--------|
| Vertical shift up $c$ | $f(x) + c$ | Graph shifts up by $c$ |
| Vertical shift down $c$ | $f(x) - c$ | Graph shifts down by $c$ |
| Horizontal shift right $c$ | $f(x - c)$ | Graph shifts right by $c$ |
| Horizontal shift left $c$ | $f(x + c)$ | Graph shifts left by $c$ |
| Vertical stretch by $c$ | $c \cdot f(x)$, $c > 1$ | Graph stretches vertically |
| Vertical compression | $c \cdot f(x)$, $0 < c < 1$ | Graph compresses vertically |
| Reflection over $x$-axis | $-f(x)$ | Graph flips over $x$-axis |
| Reflection over $y$-axis | $f(-x)$ | Graph flips over $y$-axis |
| Horizontal compression | $f(cx)$, $c > 1$ | Graph compresses horizontally |

> ⚠️ **Common error:** Students confuse the direction of horizontal shifts. $f(x - 3)$ shifts the graph **right** by 3 (not left). Think of it this way: you need $x = 3$ to make $x - 3 = 0$, so the "action" of the function moves to the right.

---

## 6. Composition and Inverse Functions

### 6.1 Composition
$(f \circ g)(x) = f(g(x))$ — apply $g$ first, then $f$.

**Domain of $f \circ g$:** $\{x \in \text{dom}(g) : g(x) \in \text{dom}(f)\}$

**Example:** Let $f(x) = \sqrt{x}$ and $g(x) = 1 - x^2$.  
$(f \circ g)(x) = \sqrt{1 - x^2}$  
Domain requires $1 - x^2 \geq 0 \Rightarrow x^2 \leq 1 \Rightarrow x \in [-1, 1]$.

Note that $f \circ g \neq g \circ f$ in general. Composition is not commutative.

### 6.2 Inverse Functions
$f^{-1}$ is the inverse of $f$ if:
$$f^{-1}(f(x)) = x \quad \text{for all } x \in \text{dom}(f)$$
$$f(f^{-1}(y)) = y \quad \text{for all } y \in \text{range}(f)$$

An inverse exists iff $f$ is **one-to-one** (injective): different inputs give different outputs. Graphically: the **horizontal line test**.

**To find $f^{-1}$:**
1. Write $y = f(x)$
2. Solve for $x$ in terms of $y$
3. Swap $x$ and $y$

**Example:** $f(x) = 2x + 7$  
$y = 2x + 7 \Rightarrow x = \frac{y-7}{2} \Rightarrow f^{-1}(x) = \frac{x-7}{2}$

**Graph relationship:** The graph of $f^{-1}$ is the reflection of the graph of $f$ over the line $y = x$.

---

## 7. Connecting to Computer Science

### Functions in CS vs Functions in Math

In mathematics, a function must be:
- **Total:** defined for every input in its domain
- **Deterministic:** same input always gives same output
- **Pure:** no side effects

These properties are exactly what *pure functions* in functional programming satisfy (Haskell, etc.). Python/C functions may violate all three (they can throw exceptions, use random numbers, or modify global state). Understanding the mathematical ideal makes you appreciate why pure functions are easier to reason about.

### Logarithms and Algorithm Analysis

When analyzing binary search:
- $n$ items → at most $\lceil \log_2 n \rceil$ comparisons
- $n = 10^6$: $\log_2(10^6) \approx 20$ comparisons
- $n = 10^9$: $\log_2(10^9) \approx 30$ comparisons

This logarithmic scaling, the reason $O(\log n)$ algorithms are so powerful, comes from the inverse relationship between exponential and logarithmic functions.

### Exponential Growth and Complexity

The difference between polynomial and exponential functions:
- $n^{100}$ (polynomial): for $n = 100$, value is $100^{100} = 10^{200}$ — enormous, but computable in principle
- $2^n$ (exponential): for $n = 1000$, value is $2^{1000}$ — no computer in the universe can handle this

This is why NP-complete problems (which appear to require exponential time) are practically unsolvable for large inputs.

---

## 8. Summary

| Concept | Core Idea |
|---------|-----------|
| Function | A rule mapping each input to exactly one output |
| Domain | The set of valid inputs |
| Range | The set of actual outputs |
| One-to-one | Different inputs → different outputs (invertible) |
| Composition | Chaining functions: apply one, feed result to next |
| Inverse | Undoes the original function |

**The deeper point:** Functions are not just computational tools. They are the formal language in which calculus, analysis, and all of modern mathematics are written. Every theorem in this course is a statement about functions.

---

## Lecture 1 Exercises (Self-Check)

1. Find the domain of $f(x) = \dfrac{\ln(x-1)}{\sqrt{4-x^2}}$.

2. Let $f(x) = x^2 + 1$ and $g(x) = \sqrt{x-1}$. Find $(f \circ g)(x)$ and $(g \circ f)(x)$ and their domains.

3. Show that $f(x) = \dfrac{2x+3}{x-1}$ has an inverse and find it.

4. Graph $f(x) = |x|$ and then describe how to obtain the graph of $g(x) = |x+2| - 3$ using transformations.

5. **(Thinking question)** A function $f$ satisfies $f(f(x)) = x$ for all $x$ in its domain. What does this tell you about the relationship between $f$ and $f^{-1}$? Give an example.

### Answers

**1.** Need $x-1>0$ **and** $4-x^2>0$ (strict — it sits under a root *in a denominator*), i.e.
$x>1$ and $-2<x<2$. Domain $=\boxed{(1,\,2)}$.

**2.** $(f\circ g)(x)=\left(\sqrt{x-1}\right)^2+1=\boxed{x}$, with domain $\boxed{[1,\infty)}$ —
**not** all of $\mathbb{R}$. The formula simplifies to $x$, but the domain is inherited from the
inner function and survives the simplification. This is the most common error on composition
problems.

$(g\circ f)(x)=\sqrt{(x^2+1)-1}=\sqrt{x^2}=\boxed{|x|}$, domain all of $\mathbb{R}$. Note
$\sqrt{x^2}=|x|$, not $x$.

**3.** Solving $y=\dfrac{2x+3}{x-1}$ gives $x(y-2)=y+3$, so
$$\boxed{f^{-1}(x)=\frac{x+3}{x-2}}$$
An inverse exists because $f$ is one-to-one: for $\frac{ax+b}{cx+d}$ this holds exactly when
$ad-bc\neq0$, and here $ad-bc=2(-1)-3(1)=-5\neq0$. Verified numerically: $f^{-1}(f(x))=x$ at
$x=2,3,5$.

**4.** Shift **left 2** (inside the function, so opposite to the sign) and **down 3**. The vertex
moves from $(0,0)$ to $\boxed{(-2,-3)}$.

**5.** $f(f(x))=x$ says $f$ is **its own inverse**, $f=f^{-1}$ — such a function is an
**involution**, and its graph is symmetric about the line $y=x$.

Examples: $f(x)=\frac1x$, $f(x)=-x$, $f(x)=c-x$ for any constant $c$. Note the function in
Exercise 3 is *not* one, since $f^{-1}=\frac{x+3}{x-2}\neq f$.


---

*Next lecture: [[Lecture 02 Algebra Review]]*
*Reading: Stewart §1.1–1.2; Spivak Ch. 1 (Prologue)*
