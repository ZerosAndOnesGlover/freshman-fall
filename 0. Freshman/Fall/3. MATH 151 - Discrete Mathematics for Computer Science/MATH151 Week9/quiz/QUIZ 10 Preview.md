# MATH 151 · Discrete Mathematics for Computer Science
## Quiz 10 — Scope Preview
### Quiz administered: Monday 30 November 2026, 13:00–13:15 (first 15 minutes of lecture) · Week 10

---

**Coverage:** Week 9 material — recurrence relations and generating functions.

---

## What You Must Know Cold

### 1. Writing a recurrence

Given a word problem, produce the relation **and** the initial conditions. This is the most heavily
tested skill in the material, because it is the one that transfers.

The standard move: **ask what happens at the last step**, and express the whole in terms of smaller
instances.

### 2. Classification

Order · linear or not · constant coefficients or not · homogeneous or not. You must be able to say
why $a_n = n\,a_{n-1}$ is linear but not constant-coefficient, and why $a_n = a_{n-1}^2$ is neither.

### 3. The characteristic equation

$$a_n = c_1a_{n-1}+c_2a_{n-2} \;\longrightarrow\; r^2-c_1r-c_2=0$$

| Roots | Solution |
|---|---|
| Distinct | $Ar_1^n+Br_2^n$ |
| Double | $(A+Bn)r^n$ |

**Know the repeated-root case.** It is the most commonly missed, because $Ar^n+Br^n$ looks
plausible until you notice it has only one free constant.

### 4. Non-homogeneous

Homogeneous solution **plus** particular solution. Fit the particular first, apply initial conditions
to the total. Guess the particular by the shape of $f(n)$; if $f(n)=d^n$ and $d$ is already a root,
multiply by $n$.

### 5. Binet's formula

$$F_n=\frac{\varphi^n-\psi^n}{\sqrt5},\qquad \varphi=\frac{1+\sqrt5}{2},\ \psi=\frac{1-\sqrt5}{2}$$

Know that $|\psi|<1$, so $F_n$ is the nearest integer to $\varphi^n/\sqrt5$.

### 6. Generating functions

$G(x)=\sum a_nx^n$. Know these three cold:

$$\frac{1}{1-x}\to 1,1,1,\ldots \qquad \frac{1}{1-cx}\to c^n \qquad \frac{1}{(1-x)^2}\to 1,2,3,\ldots$$

And know that **multiplying** generating functions models independent choices — one factor per coin
type, one factor per restriction.

---

## Sample Quiz 10 Problems (Week 9 portion)

**Problem 1.** (4 pts) Write a recurrence with initial conditions for the number of ways to climb $n$
stairs taking 1 or 2 steps at a time. Compute the first five values.

**Problem 2.** (4 pts) Solve $a_n = 5a_{n-1}-6a_{n-2}$ with $a_0=1$, $a_1=4$.

**Problem 3.** (4 pts) Solve $a_n = 6a_{n-1}-9a_{n-2}$ with $a_0=1$, $a_1=9$. State which case
applies.

**Problem 4.** (4 pts) Write the generating function for the sequence $a_n = 4^n$, and the first four
coefficients of $\dfrac{1}{(1-x)^2}$.

**Problem 5.** (4 pts) Write the generating function for making $n$ cents from 2¢ and 7¢ coins. You
do not need to expand it.

---

## Study Recommendations

1. **Do every Part A problem on PS 9 without solving anything.** Write only the recurrence and the initial conditions. Ten minutes, and it drills the skill that carries the most marks.
2. **Memorise the two-case table** for the characteristic equation. Under time pressure, the repeated-root case is what gets forgotten.
3. **Verify one closed form by iteration before the quiz.** It takes two minutes and builds the habit that catches sign errors.
4. **Know the three standard generating functions.** Everything else is built from them.

---

*MATH 151 · Week 9 · © CSE Department*
