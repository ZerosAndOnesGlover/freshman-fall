# MATH 141 — Calculus I
## Problem Set 10
### Topic: Indefinite Integrals, the Substitution Rule, Integration by Parts
**Released:** Wednesday, Week 10 | **Due:** Wednesday, Week 8 (start of class)

---

## Part A — Basic Substitution (3 pts each)

Evaluate each indefinite integral using substitution.

**A1.** $\displaystyle\int (4x-1)^7\,dx$

**A2.** $\displaystyle\int x\sqrt{5x^2+2}\,dx$

**A3.** $\displaystyle\int \frac{\sec^2x}{(1+\tan x)^3}\,dx$

**A4.** $\displaystyle\int \cos^4x\sin x\,dx$

**A5.** $\displaystyle\int \frac{e^{1/x}}{x^2}\,dx$

**A6.** $\displaystyle\int \frac{3x^2-2}{x^3-2x+5}\,dx$

**A7.** $\displaystyle\int \sec x\,dx$ *(Hint: multiply numerator and denominator by $\sec x+\tan x$, then substitute.)*

**A8.** $\displaystyle\int x^3\sqrt{1-x^2}\,dx$ *(let $u=1-x^2$, then express $x^2$ in terms of $u$ for the leftover factor)*

---

## Part B — Definite Integrals via Substitution (4 pts each)

Evaluate each definite integral. Use the limit-conversion method (Method 2 from Tuesday's lecture).

**B1.** $\displaystyle\int_0^2 x(x^2+1)^2\,dx$

**B2.** $\displaystyle\int_1^4 \frac{1}{\sqrt x(1+\sqrt x)}\,dx$

**B3.** $\displaystyle\int_0^{\pi/2} \sin^5x\cos x\,dx$

**B4.** $\displaystyle\int_0^1 \frac{x}{(x^2+1)^2}\,dx$

**B5.** $\displaystyle\int_1^e \frac{1}{x(1+\ln x)}\,dx$

**B6.** $\displaystyle\int_0^{\ln3} e^x\sqrt{e^x+1}\,dx$

---

## Part C — Symmetry (3 pts each)

**C1.** Use symmetry (justify even/odd first) to evaluate:
- (a) $\displaystyle\int_{-4}^4 (x^5-3x^3+2x)\,dx$
- (b) $\displaystyle\int_{-1}^1 \frac{x^2\cos x}{1+x^4}\,dx$ — you do NOT need to fully evaluate; express as $2\times$ an integral from 0 to 1
- (c) $\displaystyle\int_{-\pi/4}^{\pi/4} \tan^3x\,dx$

**C2.** Evaluate $\displaystyle\int_{-2}^2 (x^6-4x^4+x^2+7)\,dx$ using symmetry to reduce your work.

**C3.** Use the identity $\displaystyle\int_0^a f(x)\,dx=\int_0^a f(a-x)\,dx$ (proved in Tuesday's Exercise 4) to evaluate:
$$\int_0^\pi \frac{x\sin x}{1+\cos^2x}\,dx$$

---

## Part D — Integration by Parts, Single Application (4 pts each)

**D1.** $\displaystyle\int x\cos(3x)\,dx$

**D2.** $\displaystyle\int x e^{-2x}\,dx$

**D3.** $\displaystyle\int \ln(2x)\,dx$

**D4.** $\displaystyle\int \arctan(2x)\,dx$

**D5.** $\displaystyle\int x\sec^2x\,dx$

**D6.** $\displaystyle\int (\ln x)^2\,dx$ *(requires by-parts twice, but the second application does NOT circle back — reduces the power of the log)*

---

## Part E — Integration by Parts, Repeated and Circular (5 pts each)

**E1.** $\displaystyle\int x^2\sin x\,dx$

**E2.** $\displaystyle\int x^2e^{-x}\,dx$

**E3.** $\displaystyle\int e^{-x}\cos x\,dx$ *(solve for $I$ algebraically)*

**E4.** $\displaystyle\int e^{3x}\sin(2x)\,dx$ *(solve for $I$ algebraically)*

**E5.** Evaluate the definite integral $\displaystyle\int_0^{\pi/2} x\sin x\,dx$.

**E6.** Evaluate the definite integral $\displaystyle\int_1^e x^2\ln x\,dx$.

---

## Part F — Mixed Techniques (5 pts each)

Determine which technique (substitution, integration by parts, symmetry, or a combination) is appropriate, then evaluate.

**F1.** $\displaystyle\int x^3e^{x^2}\,dx$ *(Hint: substitute first to reduce to a single-variable-times-exponential form, THEN apply integration by parts.)*

**F2.** $\displaystyle\int \frac{\ln(\ln x)}{x}\,dx$

**F3.** $\displaystyle\int_{-1}^1 x^3\sqrt{1-x^2}\,dx$ *(recognize symmetry FIRST before attempting any computation)*

**F4.** $\displaystyle\int \sin(\ln x)\,dx$ *(requires integration by parts twice, with the "solve for $I$" trick)*

**F5.** $\displaystyle\int x\arctan x\,dx$

---

## Part G — Conceptual and Proof (5 pts each)

**G1.** Explain, using the Product Rule, why the Integration by Parts formula $\int u\,dv=uv-\int v\,du$ is valid. Show the derivation starting from $\frac{d}{dx}[uv]=u'v+uv'$.

**G2.** A student attempts $\displaystyle\int x e^{x^2}\,dx$ using Integration by Parts with $u=x$, $dv=e^{x^2}dx$. Explain why this choice fails (specifically: what goes wrong when trying to find $v$?), and show the correct approach using substitution instead.

**G3.** Explain the LIATE heuristic in your own words: why does it make sense to choose $u$ to be the "hardest to integrate, easiest to differentiate" factor? Illustrate with a specific example where choosing $u$ and $dv$ in the WRONG order makes the problem harder rather than easier (try $\int xe^x\,dx$ with $u=e^x$, $dv=x\,dx$ and show the resulting integral is not simpler).

**G4 (Bonus — 4 pts).** Prove the general reduction formula:
$$\int x^ne^x\,dx = x^ne^x - n\int x^{n-1}e^x\,dx$$
using one application of Integration by Parts. Then use it twice to re-derive $\displaystyle\int x^2e^x\,dx$ from Wednesday's Example 5.

---

## Grading Summary

| Part | Points | Focus |
|------|--------|-------|
| A (8 × 3) | 24 | Basic substitution |
| B (6 × 4) | 24 | Definite integrals via substitution |
| C (3+1 problems) | 15 | Symmetry |
| D (6 × 4) | 24 | Integration by parts (single) |
| E (6 problems) | 30 | Integration by parts (repeated/circular) |
| F (5 × 5) | 25 | Mixed techniques |
| G (3 × 5 + bonus 4) | 15 + 4 | Conceptual/proof |
| **Total** | **157 + 4 bonus** | |
