# MATH 142 · Calculus II
## Problem Set 1
### Topic: Integration by Parts; Trigonometric Integrals
**Released:** Wednesday, Week 1 | **Due:** Wednesday, Week 2 (start of class)

---

> **State your method.** For every integral, say which technique you are using and — for parts — what
> you chose as $u$ and $dv$. An answer with no visible method earns no marks even when correct.
>
> **Differentiate every antiderivative before you write it down.** This is the cheapest error-check
> available and it catches nearly everything in Part A and Part B.

---

## Part A — Integration by Parts, Single Application (5 pts each)

**A1.** $\displaystyle\int x\cos x\,dx$

**A2.** $\displaystyle\int x\ln x\,dx$

**A3.** $\displaystyle\int \arcsin x\,dx$

*There is only one factor. Lecture 1 §3, Example 2 tells you what to do.*

**A4.** $\displaystyle\int_0^{\pi/2} x\cos x\,dx$

*Evaluate the $[uv]$ bracket properly.*

---

## Part B — Repeated, Circular, and Reduction (6 pts each)

**B1.** $\displaystyle\int x^2\cos x\,dx$

**B2.** $\displaystyle\int x^3 e^{-x}\,dx$

*Use tabular integration. Show the table.*

**B3.** $\displaystyle\int e^{2x}\cos 3x\,dx$

*The integral will return. Solve for it. Note the coefficients make the algebra less tidy than the lecture's example — that is the point of the problem.*

**B4.** $\displaystyle\int_0^1 \arctan x\,dx$

**B5.** Use the reduction formula $I_n = \dfrac{n-1}{n}I_{n-2}$ with $I_0 = \dfrac\pi2$ to evaluate

$$I_6 = \int_0^{\pi/2}\sin^6 x\,dx$$

Show every step of the recursion. Then state, without further computation, whether $I_7$ is a rational number or a rational multiple of $\pi$, and why.

---

## Part C — Trigonometric Integrals (6 pts each)

*For each, state which case of the decision table you are in before you begin.*

**C1.** $\displaystyle\int \sin^5 x\cos^2 x\,dx$

**C2.** $\displaystyle\int\cos^4 x\,dx$

**C3.** $\displaystyle\int\tan^5 x\sec^3 x\,dx$

**C4.** $\displaystyle\int\sec^4 x\,dx$

**C5.** $\displaystyle\int\sin 4x\cos 6x\,dx$

---

## Part D — Orthogonality and Concept (10 pts each)

**D1.** *(Orthogonality.)*

- (a) Evaluate $\displaystyle\int_0^{2\pi}\sin 2x\,\sin 3x\,dx$ using a product-to-sum identity. Show the working.
- (b) Evaluate $\displaystyle\int_0^{2\pi}\sin^2 3x\,dx$.
- (c) A signal is known to have the form
$$f(x) = a_2\sin 2x + a_3\sin 3x + a_4\sin 4x$$
for constants $a_2,a_3,a_4$. Using (a) and (b), give a formula for $a_3$ as an integral involving $f$, and explain in one or two sentences why the other two coefficients disappear.

**D2.** *(Why some integrals come back.)*

- (a) $\displaystyle\int x^2 e^x\,dx$ needs two applications of parts and then **terminates**. $\displaystyle\int e^x\sin x\,dx$ needs two applications and **returns to where it started**. Explain what is different about the two integrands that causes this.
- (b) For $\int e^x\sin x\,dx$, explain why applying parts a third time does not help.
- (c) In the circular case you must keep the same *type* of function as $u$ at both applications. Show what goes wrong if, on the second application, you switch and take $u=e^x$.

---

## Marking Summary

| Part | Points | Focus |
|---|---|---|
| A (4 × 5) | 20 | Parts, single application; choosing $u$ |
| B (5 × 6) | 30 | Repeated, tabular, circular, reduction |
| C (5 × 6) | 30 | The trigonometric decision procedure |
| D (2 × 10) | 20 | Orthogonality; why the method loops |
| **Total** | **100** | |

---

## Before You Submit

1. **Differentiate every antiderivative in Parts A–C.** Every one of them can be checked in under a minute.
2. **Check that you named the case** in each of C1–C5.
3. **Check B3's coefficients** by differentiating — the $\tfrac1{13}$ is easy to get wrong and impossible to miss once differentiated.

---

*MATH 142 · Week 1 · Problem Set 1*
