# MATH 141 — Quiz 11
## Administered: start of Week 11, Monday
### Covers: Week 10 — integration techniques

**Duration:** 15 minutes · Closed book · **20 points**

---

## Section A — Short Answer (2 pts each)

**A1.** Evaluate $\displaystyle\int 2x(x^2+1)^4\,dx$ by substitution. State your $u$.

**A2.** Evaluate $\displaystyle\int_0^{1} 2x e^{x^2}\,dx$, changing the limits with the substitution.

**A3.** Evaluate $\displaystyle\int x\cos x\,dx$ by parts. State your $u$ and $dv$.

**A4.** State the integration-by-parts formula, and the guideline for choosing $u$.

**A5.** Explain why $\displaystyle\int_{-2}^{2}x^3\sqrt{1+x^2}\,dx=0$ without computing it.

---

## Section B — Longer (5 pts each)

**B1.** Evaluate $\displaystyle\int_0^{\pi/2}\sin^3x\cos x\,dx$. Show the substitution and the
changed limits.

**B2.** Evaluate $\displaystyle\int \ln x\,dx$. *(Hint: parts, with an unobvious choice of $dv$.)*

---

**Total: 20 points**

---

## Answer Key (Instructor Copy)

**A1.** $u=x^2+1$, $du=2x\,dx$:

$$\int u^4du=\frac{u^5}{5}+C=\mathbf{\frac{(x^2+1)^5}{5}+C}$$

**A2.** $u=x^2$, $du=2x\,dx$. Limits: $x=0\Rightarrow u=0$; $x=1\Rightarrow u=1$.

$$\int_0^1 e^u\,du=\big[e^u\big]_0^1=\mathbf{e-1}\approx1.71828$$

*Award full marks only if the **limits are changed**. Substituting back to $x$ and using the original
limits is also correct but slower; changing limits is the habit being built.*

**A3.** $u=x$, $dv=\cos x\,dx$; then $du=dx$, $v=\sin x$:

$$\int x\cos x\,dx=x\sin x-\int\sin x\,dx=\mathbf{x\sin x+\cos x+C}$$

**A4.** $\displaystyle\int u\,dv=uv-\int v\,du$.

**Choose $u$ to be the factor that gets simpler when differentiated** (commonly a polynomial or a
logarithm), and $dv$ the factor you can integrate. *(LIATE is an acceptable answer.)*

**A5.** $x^3$ is **odd** and $\sqrt{1+x^2}$ is **even**, so the product is **odd**. The interval
$[-2,2]$ is symmetric about the origin, so the integral vanishes by Week 8's symmetry property.

*Do not accept "the areas cancel" without identifying the parity.*

**B1.** $u=\sin x$, $du=\cos x\,dx$. Limits: $x=0\Rightarrow u=0$; $x=\pi/2\Rightarrow u=1$.

$$\int_0^1u^3du=\left[\frac{u^4}{4}\right]_0^1=\mathbf{\frac14}$$

*(Verified numerically: $0.2500000000$.)*

**Marking:** 2 for the substitution, 2 for the changed limits, 1 for the value.

**B2.** The trick is $dv=dx$:

Let $u=\ln x$, $dv=dx$. Then $du=\dfrac{dx}{x}$, $v=x$:

$$\int\ln x\,dx=x\ln x-\int x\cdot\frac1x\,dx=x\ln x-\int dx=\mathbf{x\ln x-x+C}$$

*The unobvious step is treating the **whole integrand** as $u$ and $dx$ as $dv$. Students who cannot
see a "product" here are stuck; naming that move is worth 2 of the 5.*

*Check by differentiating: $\frac{d}{dx}(x\ln x-x)=\ln x+1-1=\ln x$ ✓ — and requiring that check is
good practice.*

---

*MATH 141 · Week 11 · Quiz 11 · © CSE Department*
