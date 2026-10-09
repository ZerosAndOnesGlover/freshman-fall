# MATH 151 · Discrete Mathematics for Computer Science
## Lecture 29 (L29) — Generating Functions
### Friday, Week 9

*“A generating function is a device somewhat similar to a bag. Instead of carrying many little objects detachedly, which could be embarrassing, we put them all in a bag, and then we have only one object to carry, the bag.”* — George Pólya, *Mathematics and Plausible Reasoning*, Vol. 1 (1954)

**Date:** Friday 27 November 2026 · 13:00–13:50 · Week 9

**Reading:** Rosen, 8e §8.4 · Levin, 3e §5.1 · Graham, Knuth & Patashnik, *Concrete Mathematics* ch. 7 *(details at the end of the lecture)*

**Coursework:** 📝 **PS 8** due today 17:00 · 📝 **PS 9** released today 14:00, due Fri 4 Dec 17:00 · 📊 **Quiz 10** Mon 30 Nov 13:00–13:15 · 🔬 **Lab 9** Wed 2 Dec 15:00–16:50

---

## 1. A Sequence as a Single Object

Thursday's characteristic-equation method is powerful but narrow: it handles linear,
constant-coefficient recurrences and little else. **Generating functions** are a wider technique, and
they rest on one strange idea.

> **Definition.** The (ordinary) **generating function** of a sequence $a_0, a_1, a_2, \ldots$ is the
> formal power series
> $$G(x) = \sum_{n=0}^{\infty} a_n x^n = a_0 + a_1x + a_2x^2 + \cdots$$

The sequence becomes the **coefficients** of a single function. Manipulating the function
manipulates the whole sequence at once.

**"Formal" matters.** We never substitute a number for $x$ and we never ask whether the series
converges. $x$ is a bookkeeping device — a hook to hang coefficients on. All operations are defined
by what they do to coefficients, and questions of convergence are irrelevant to every use below.

---

## 2. The Two Series You Must Know

$$\frac{1}{1-x} = 1 + x + x^2 + x^3 + \cdots \qquad(a_n = 1)$$

**Why:** multiply both sides by $(1-x)$; on the right everything cancels except the leading 1.

From it, by substituting $cx$ for $x$:

$$\frac{1}{1-cx} = 1 + cx + c^2x^2 + \cdots \qquad(a_n = c^n)$$

**Verified by formal division:**

| Function | Coefficients |
|---|---|
| $\dfrac{1}{1-x}$ | $1, 1, 1, 1, 1, 1, 1, 1$ |
| $\dfrac{1}{1-2x}$ | $1, 2, 4, 8, 16, 32, 64, 128$ |
| $\dfrac{1}{(1-x)^2}$ | $1, 2, 3, 4, 5, 6, 7, 8$ |

That last one is worth noticing: squaring the denominator turns the constant sequence into the
counting sequence.

---

## 3. Solving a Recurrence With Generating Functions

The method, in four steps:

1. Let $G(x) = \sum a_n x^n$.
2. Multiply the recurrence by $x^n$ and sum over all $n$ where it holds.
3. Recognise the shifted sums as $G(x)$ with adjustments, then solve algebraically for $G(x)$.
4. Expand $G(x)$ back into a power series; the coefficients are your sequence.

### Worked example — Fibonacci

$F_n = F_{n-1}+F_{n-2}$ for $n \geq 2$, with $F_0 = 0$, $F_1 = 1$.

Multiply by $x^n$ and sum from $n=2$:

$$\sum_{n\ge2}F_nx^n = \sum_{n\ge2}F_{n-1}x^n + \sum_{n\ge2}F_{n-2}x^n$$

The left side is $G(x) - F_0 - F_1x = G(x) - x$. The first sum on the right is $x\,G(x)$ (reindex),
and the second is $x^2G(x)$. So

$$G(x) - x = xG(x) + x^2G(x)$$

$$G(x)\left(1 - x - x^2\right) = x \qquad\Longrightarrow\qquad \boxed{G(x) = \frac{x}{1-x-x^2}}$$

**Verified:** expanding $\dfrac{x}{1-x-x^2}$ as a power series gives coefficients

$$0,\ 1,\ 1,\ 2,\ 3,\ 5,\ 8,\ 13,\ 21,\ 34,\ 55,\ 89$$

— exactly the Fibonacci numbers.

**Note where the characteristic equation went.** The denominator $1-x-x^2$ is the *reversed*
characteristic polynomial $r^2-r-1$. The two methods are the same mathematics wearing different
clothes: partial-fraction decomposition of $x/(1-x-x^2)$ reproduces Binet's formula exactly.

### A second example

$a_n = 5a_{n-1}-6a_{n-2}$, $a_0=1$, $a_1=4$ has generating function

$$G(x) = \frac{1-x}{1-5x+6x^2}$$

**Verified:** its coefficients are $1, 4, 14, 46, 146, 454, 1394, 4246$ — matching Thursday's closed
form $2\cdot3^n-2^n$.

---

## 4. Generating Functions as Counting Machines

The real power is combinatorial, and it comes from one observation: **multiplying generating
functions convolves their coefficients.**

$$\left(\sum a_nx^n\right)\left(\sum b_nx^n\right) = \sum_n\left(\sum_{k=0}^{n}a_kb_{n-k}\right)x^n$$

That inner sum is exactly "choose some from the first pile and the rest from the second". So
**multiplication of generating functions models independent choices.**

### Making change

In how many ways can you make $n$ cents from 1¢, 5¢, and 10¢ coins?

Each coin type contributes a factor recording how many of that coin you use:

$$G(x) = \underbrace{\frac{1}{1-x}}_{\text{pennies}}\cdot\underbrace{\frac{1}{1-x^5}}_{\text{nickels}}\cdot\underbrace{\frac{1}{1-x^{10}}}_{\text{dimes}}$$

The coefficient of $x^n$ counts the ways. **Verified:** the coefficient of $x^{25}$ is $12$, and
listing the combinations by hand gives the same 12.

### Choosing with restrictions

"Select $n$ objects from three types, using at most 2 of type A, an even number of type B, and at
least 3 of type C":

$$(1+x+x^2)\cdot\frac{1}{1-x^2}\cdot\frac{x^3}{1-x}$$

Each restriction becomes a factor, mechanically. No case analysis, no inclusion–exclusion — the
algebra does the bookkeeping.

**This is the pitch for generating functions:** problems whose direct solution needs delicate case
work become routine polynomial manipulation.

---

## 5. In Computer Science

**Analysis of algorithms.** Generating functions are the standard tool for average-case analysis —
the expected number of comparisons in quicksort, the expected depth of a random binary search tree.

**The Catalan numbers.** $C_n = \frac{1}{n+1}\binom{2n}{n}$ counts binary trees with $n$ nodes,
balanced bracket strings of length $2n$, and triangulations of a polygon. Its generating function
$C(x) = \frac{1-\sqrt{1-4x}}{2x}$ falls out of the recurrence
$C_n = \sum_{k} C_k C_{n-1-k}$ — a convolution, hence a product. **Verified:**
$C_0..C_8 = 1, 1, 2, 5, 14, 42, 132, 429, 1430$.

**Polynomial multiplication.** Multiplying generating functions *is* polynomial multiplication, which
the Fast Fourier Transform performs in $\Theta(n\log n)$ rather than $\Theta(n^2)$. Every convolution
in signal processing is this operation.

---

## 6. Summary

| Idea | Statement |
|---|---|
| Generating function | $G(x)=\sum a_nx^n$ — the sequence *is* the coefficients |
| "Formal" | Never evaluate, never worry about convergence |
| $\frac{1}{1-x}$ | $1,1,1,\ldots$ |
| $\frac{1}{1-cx}$ | $c^n$ |
| $\frac{1}{(1-x)^2}$ | $1,2,3,4,\ldots$ |
| Fibonacci | $G(x)=\dfrac{x}{1-x-x^2}$ |
| Denominator | the reversed characteristic polynomial |
| **Multiplication** | convolves coefficients ⟹ models independent choices |
| Making change | one factor per coin type |
| Restrictions | one factor per restriction |

---

## 7. End-of-Lecture Exercises

1. Write the first six coefficients of $\dfrac{1}{1-3x}$.

2. Find the generating function for $a_n = 2a_{n-1}$, $a_0 = 1$, and identify the sequence.

3. Find the generating function for $a_n = a_{n-1}+2a_{n-2}$, $a_0 = 2$, $a_1 = 7$. *(You solved this recurrence in Lecture 28 Exercise 3 — check the coefficients match.)*

4. Write the generating function for making $n$ cents from 1¢, 2¢, and 5¢ coins. Find the coefficient of $x^{10}$ and verify by listing.

5. Write the generating function for choosing $n$ objects from four types with **at most 3 of each**, and state the coefficient of $x^5$.

6. **(Stretch.)** Use partial fractions on $\dfrac{x}{1-x-x^2}$ to derive Binet's formula. *(Factor the denominator as $(1-\varphi x)(1-\psi x)$.)*

---

## Reading

- **Rosen, 8e §8.4** — Generating functions
- **Levin, 3e §5.1** — Generating functions
- **Graham, Knuth & Patashnik, *Concrete Mathematics* ch. 7** — the definitive treatment, if you want depth

*Next: Week 10 — Graphs: Terminology, Representations, Paths, Connectivity*
