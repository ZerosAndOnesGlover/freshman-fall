# MATH 142 · Calculus II
## Week 12 · Lecture 3 (Wednesday)
### The Road Ahead

---

**Reading:** none
**The final exam** is comprehensive — Weeks 0–12, 150 minutes, two-page sheet. **The revision guide is in `resources/`.**

---

## 1. Nothing In This Course Was Terminal

**Every technique you learned this term is the first chapter of something.** This lecture says which, using the actual course codes in the CSE curriculum, so you know where to look.

---

## 2. Integration → Probability

**Week 3 taught you improper integrals.** Here is the one that matters most:

$$\int_0^\infty e^{-x^2}\,dx = \frac{\sqrt\pi}{2}$$

*(Verified.)* **You could not evaluate this by any method in this course** — Week 10 gave you the series, and even that only converges to it, never produces the closed form. The closed form needs a double integral in polar coordinates, which is next year's multivariable calculus.

**Its normalised form is the entire foundation of statistics:**

$$\int_{-\infty}^{\infty}\frac{1}{\sqrt{2\pi}}e^{-x^2/2}\,dx = 1, \qquad \int_{-\infty}^{\infty}\frac{x^2}{\sqrt{2\pi}}e^{-x^2/2}\,dx = 1$$

*(Both verified.)* **The first says the normal distribution is a probability distribution; the second says its variance is 1.** The $\sqrt{2\pi}$ that looks arbitrary in a statistics course is *exactly* the improper integral you learned to handle in Week 3.

> **Continues in: MATH 251 — Probability & Statistics** *(Year 2, Spring)*. Every expectation is an
> integral, most of them improper, and the convergence questions of Weeks 3 and 7 are what decide
> whether a distribution has a mean at all.

**And the Gamma function** generalises the factorial by an improper integral:

$$\Gamma(n+1)=\int_0^\infty t^n e^{-t}\,dt = n!, \qquad \Gamma\!\left(\tfrac12\right)=\sqrt\pi$$

*(Verified: $\int_0^\infty t^4e^{-t}dt=24=4!$.)* **$\Gamma(1/2)^2=\pi$** — the Gaussian integral again, wearing a different hat.

---

## 3. Orthogonality → Signals

**Week 1's least-motivated computation** was this:

$$\int_{-\pi}^{\pi}\sin(mx)\sin(kx)\,dx = \begin{cases}0 & m\ne k\\ \pi & m=k\end{cases}$$

*(Verified.)* **You computed it with a product-to-sum identity and were told it mattered.** Here is why.

**It says the functions $\sin x,\sin2x,\sin3x,\ldots$ are mutually perpendicular**, in exactly the sense that $\mathbf i,\mathbf j,\mathbf k$ are — and therefore any reasonable function can be resolved into components along them, with each coefficient extracted by an integral:

$$f(x)=\sum_{n\ge1}b_n\sin(nx), \qquad b_n=\frac1\pi\int_{-\pi}^{\pi}f(x)\sin(nx)\,dx$$

**This is the Fourier series**, and it is how every audio file, image codec, radio, and MRI machine works.

> **Continues in: ECE 211 — Signals and Systems** *(Year 2, Spring)* — *"Fourier analysis, filtering,
> the mathematical bridge between physics and digital processing."* **You already own the integral it
> is built on.**

**Note also what Week 9 was quietly protecting.** Writing $f$ as an infinite sum and then integrating term by term requires a theorem. **You used one for power series inside the radius of convergence; the Fourier case needs a harder one**, and the fact that it can fail is why analysis exists.

---

## 4. Systems → Linear Algebra

**Monday's system** $x'=y,\ y'=-x$ can be written

$$\frac{d}{dt}\begin{pmatrix}x\\y\end{pmatrix} = \begin{pmatrix}0&1\\-1&0\end{pmatrix}\begin{pmatrix}x\\y\end{pmatrix}$$

**The behaviour is decided by the matrix's eigenvalues, which here are $\pm i$.** *(Verified.)*

**And now Week 10 pays off.** The scalar equation $y'=\lambda y$ has solution $e^{\lambda t}$; with $\lambda=\pm i$ that is $e^{\pm it}$, and Euler's formula — which you obtained in Week 10 by adding the Maclaurin series of $\cos$ and $\sin$ —

$$e^{it}=\cos t+i\sin t$$

**turns the exponential back into the circular motion you drew in the phase plane.** Purely imaginary eigenvalues mean rotation; that is a theorem, and the sines and cosines are its shadow.

> **Continues in: MATH 241 — Linear Algebra** *(Year 2, Fall)*. Every linear system of differential
> equations is an eigenvalue problem. **The phase-plane pictures of Monday are classified completely
> by the eigenvalues of a $2\times2$ matrix.**

---

## 5. Convergence → Analysis

**This course proved a great deal and assumed a little.** The assumptions were flagged as they went by:

| Assumed | Where | The real theorem |
|---|---|---|
| A bounded monotone sequence converges | Week 6 | **completeness of $\mathbb R$** |
| Term-by-term differentiation of a power series | Week 9 | **uniform convergence** |
| Rearranging a conditionally convergent series changes the sum | Week 8 | **Riemann's rearrangement theorem** |
| $f$ smooth $\Rightarrow$ Taylor series converges to $f$ | Week 10 | **false** — $e^{-1/x^2}$ |

**The last row is the one to remember.** *(Verified in Week 10: every derivative of $e^{-1/x^2}$ vanishes at $0$, so its Maclaurin series is identically zero and represents the function nowhere but the origin.)* **A function can be infinitely differentiable and still not equal its own Taylor series.** That single counterexample is why "smooth" and "analytic" are different words.

> **Continues in: real analysis.** The subject exists to supply proofs for the four rows above, and
> it will feel like a second pass over this course with the gaps filled in.

---

## 6. Numerical Methods → Computing

**Yesterday's lecture showed a quadratic formula returning a 25% error in double precision.** That is not a mathematics problem; it is an arithmetic problem, and arithmetic is hardware.

> **Continues in: CS 201 — Computer Organization & Architecture** *(Year 2, Fall)*. Floating-point
> representation, rounding modes, and why $0.1+0.2\ne0.3$ are facts about the machine, not about
> $\mathbb R$.

**And the algorithms themselves** — quadrature, root-finding, ODE integrators, the order-of-convergence analysis you performed eleven times — **are the content of MATH 341 — Numerical Methods & Analysis** *(Year 3, Fall)*. **You have already done the measurements; what you have not seen is the proofs of the orders you measured, or the stability theory that decides whether the measurement means anything.**

---

## 7. The Map

| This course | Continues in |
|---|---|
| Improper integrals, the Gaussian | **MATH 251** — Probability & Statistics |
| Orthogonality, Fourier *(Week 1)* | **ECE 211** — Signals and Systems |
| Systems, phase plane, eigenvalues | **MATH 241** — Linear Algebra |
| Floating point, error propagation | **CS 201** — Computer Organization |
| Sequences, series, convergence proofs | real analysis |
| Quadrature, RK4, order of convergence | **MATH 341** — Numerical Methods & Analysis |
| Volumes, arc length, the $\sqrt\pi$ | multivariable calculus |

---

## 8. What To Take From This Course

**Three things, and they are not techniques.**

1. **Convergence is not a formality.** A series can converge and be useless *(harmonic-adjacent, $10^{43}$ terms)*; a rearrangement can change a sum to anything you like; a bound can be tight or hopeless, and knowing which is the whole skill.

2. **The order of convergence decides every practical question.** Eleven labs, one number. Not elegance, not age, not cleverness — the exponent $p$.

3. **The CAS is a check, not an oracle.** You caught a numerical library four digits wrong, a `dsolve` that could not, a $\pi$ approximation whose sign you had backwards, and a quadratic formula off by 25% — **every one of them by an independent check you could do by hand.**

> **The habit those three build is the point of the course.** The integrals will fade. **The reflex
> to ask "how would I know if this were wrong?" is the thing you keep.**

---

*Next: the FINAL EXAM. See the revision guide in `resources/`, and read the Course Retrospective afterwards.*
