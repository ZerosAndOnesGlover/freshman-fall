# MATH 141 · Calculus I
## Lab 07
### Growth Rates, Curve Sketching Practice, and Optimization

**Date:** Friday 13 November 2026 · 15:00–16:50 · Lab Section (Week 7) — covers Weeks 6–7  
**Duration:** 2 hours | **Tools:** Desmos, and Python using only CS 101 Weeks 0–3 (`def`, `for`, `range`, `math`)
**Expected time:** the session itself (6 questions), plus at most 30 minutes to tidy your answers
**Submission:** Written report due Monday 16 November 2026, 17:00 (Week 8)

> *Revised 2026-09-21.* Part 4 (design your own optimization problem) removed to fit the two hours.
>
> *Revised 2026-09-26.* Cut from about 20 questions, three full curve sketches and a reflection to 6
> questions and one sketch. The $(1+1/x)^x$ table and two of the sketches were removed. The grid-search
> code is now run rather than "run mentally", using `def` and `for` from CS 101 Weeks 2–3.

---

## Lab Objectives

1. See the growth-rate hierarchy that L'Hôpital's Rule proves
2. Sketch one unfamiliar function by hand and check it in Desmos
3. Solve an optimization problem exactly, then by brute-force search, and compare

---

## Part 1 — Growth Rate Hierarchies (20 min)

### Question 1 (20 points)

Graph $\ln x$, $x$, $x^2$ and $e^x$ on $0 \le x \le 20$ in Desmos (restrict the $y$-range to see all four). Rank
them from slowest- to fastest-growing. Then print a table of $\dfrac{\ln x}{x}$ and $\dfrac{x^2}{e^x}$:

```python
import math
for x in [10, 20, 50]:
    print(x, math.log(x) / x, x**2 / math.exp(x))
```

Confirm both limits as $x \to \infty$ with L'Hôpital's Rule. CS 101 Week 6 met the same ranking as Big-O
classes: name an algorithm from CS 101 that runs in $O(\log n)$ time and one that runs in $O(n^2)$.

---

## Part 2 — Curve Sketching with Instant Feedback (35 min)

Let $g(x) = x\ln x$. Do the analysis **by hand first**, predict the graph, **then** check it in Desmos.

### Question 2 (10 points)

What is the domain of $g$? Find $\lim_{x\to0^+} x\ln x$ (a $0\cdot\infty$ form) and $\lim_{x\to\infty} x\ln x$.

### Question 3 (20 points)

Find $g'(x)$ and $g''(x)$, the critical number, the intervals of increase and decrease, and the concavity.
Classify the critical number. Now graph $g$ in Desmos: does it match your prediction? What is the minimum
value?

---

## Part 3 — Optimization: Exact and Brute Force (45 min)

### Question 4 (25 points)

An underwater cable must connect a platform 5 km offshore to a station on the shore. The nearest point on
shore to the platform is $P$, and the station is 10 km along the shore from $P$. Underwater cable costs
\$5000/km and cable on land \$3000/km. The cable runs underwater to a point $x$ km from $P$, then along the
shore to the station.

Write the total cost $C(x)$ for $0 \le x \le 10$. Find the critical number, show it gives the minimum
(compare with the endpoints), and give the minimum cost. Graph $C$ in Desmos to confirm.

### Question 5 (15 points)

A **grid search** tries many points and keeps the best. Run it on Lecture 03's box, $V(x) = x(12-2x)^2$ on
$[0, 6]$, whose exact maximum is at $x = 2$:

```python
def V(x):
    return x * (12 - 2*x)**2

def grid_max(f, a, b, n):
    best_x = a
    best_val = f(a)
    step = (b - a) / n
    for i in range(n + 1):
        x = a + i * step
        if f(x) > best_val:
            best_val = f(x)
            best_x = x
    return best_x, best_val

for n in [10, 100, 10000]:
    print(n, grid_max(V, 0, 6, n))
```

How close does it get to $x = 2$ for each $n$? Why does it never land on exactly $2.0$ for $n = 10000$?

### Question 6 (10 points)

Compare the two approaches. What does calculus give you that grid search does not? When might grid search
still be the practical choice?

---

## Lab Report Requirements

Include your programs and output, your hand analysis for Questions 2–4, Desmos screenshots or links for
Questions 1, 3 and 4, and answers to Questions 1–6.

**Grading:**

| Section | Points |
|---------|--------|
| Part 1 — Growth rate hierarchies | 20 |
| Part 2 — Curve sketching | 30 |
| Part 3 — Optimization, exact and brute force | 50 |
| **Total** | **100** |
