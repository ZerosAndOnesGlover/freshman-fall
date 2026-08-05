# MATH 142 · Calculus II
## Quiz 04 — With Answer Key
### Week 4 · Monday · **Covers Week 3**

---

**Time:** 15 minutes, start of Monday's lecture
**Closed book, no calculator**
**Total: 20 points** (4 points each)

**Covers Week 3:** improper integrals of both kinds, the $p$-tests, comparison.

---

## Questions

**Q1.** Evaluate $\displaystyle\int_1^\infty\frac{dx}{x^{5/2}}$, or show it diverges.

**Q2.** Evaluate $\displaystyle\int_0^1\frac{dx}{x^{3/4}}$, or show it diverges.

**Q3.** Evaluate $\displaystyle\int_0^\infty e^{-2x}\,dx$, or show it diverges.

**Q4.** Determine whether $\displaystyle\int_1^\infty\frac{dx}{x^2+\sqrt x}$ converges. **Do not evaluate it.**

**Q5.** Evaluate $\displaystyle\int_0^2\frac{dx}{(x-1)^{2/3}}$, or show it diverges. *(Use the real cube root.)*

---
---

# ANSWER KEY

---

**Q1. (4)** $p=\tfrac52>1$, so it **converges**:

$$\lim_{T\to\infty}\left[\frac{x^{-3/2}}{-3/2}\right]_1^T = \lim_{T\to\infty}\frac23\left(1-T^{-3/2}\right) = \boxed{\frac23}$$

*Marking: 1 for the limit notation, 2 for the antiderivative, 1 for the value. Consistent with $\frac{1}{p-1}=\frac{1}{3/2}=\frac23$. Verified symbolically.*

**Q2. (4)** Improper at $x=0$; $p=\tfrac34<1$, so it **converges**:

$$\lim_{t\to0^+}\left[4x^{1/4}\right]_t^1 = \boxed{4}$$

*Marking: **1 of the 4 is for noting the integral is improper at 0.** Deduct it even if the answer is right — the whole of Week 3 is about noticing. Verified symbolically.*

**Q3. (4)**

$$\lim_{T\to\infty}\left[-\frac{e^{-2x}}{2}\right]_0^T = \lim_{T\to\infty}\frac12\left(1-e^{-2T}\right) = \boxed{\frac12}$$

*Marking: 4. **The $\frac12$ from the chain rule** is the only real risk. Verified symbolically.*

**Q4. (4)** **Converges.**

For $x\ge1$: $x^2+\sqrt x > x^2$, so

$$0 < \frac{1}{x^2+\sqrt x} < \frac{1}{x^2}$$

and $\int_1^\infty x^{-2}dx$ converges ($p=2>1$). **By direct comparison, ours converges** — with value less than 1.

*(Limit comparison with $x^{-2}$ also works: $L=\lim\frac{x^2}{x^2+\sqrt x}=1$.)*

*Marking: 1 comparison function, 2 the inequality with its direction, 1 the verdict citing the $p$-test. **Deduct 2 for an inequality pointing the wrong way**, even with the right verdict.*

*Corroborated numerically: partial integrals $0.7371,\ 0.7470,\ 0.7471$ at $T=10^2,10^4,10^6$ — settling below 1, as the bound requires.*

**Q5. (4)** **Interior singularity at $x=1$ — must split.**

$$\int_0^2\frac{dx}{(x-1)^{2/3}} = \int_0^1(1-x)^{-2/3}dx + \int_1^2(x-1)^{-2/3}dx$$

Each is a $p$-test at a singularity with $p=\tfrac23<1$, so **both converge**:

$$= \Big[-3(1-x)^{1/3}\Big]_0^1 + \Big[3(x-1)^{1/3}\Big]_1^2 = 3+3 = \boxed{6}$$

*Marking: **2 of the 4 for splitting at $x=1$.** A student who applied the Fundamental Theorem straight across gets at most 1, even if they land on 6 — here the antiderivative happens to be continuous, so the careless method gives the right number for the wrong reason. **Say so on the script**; this is the luckiest possible version of the $\int_{-1}^1 x^{-2}$ error. Verified symbolically: each half is exactly 3.*

---

## Marking Summary

| Question | Points | Tests |
|---|---|---|
| Q1 | 4 | $p$-test at infinity |
| Q2 | 4 | $p$-test at a singularity; noticing it is improper |
| Q3 | 4 | Exponential decay |
| Q4 | 4 | Direct comparison |
| Q5 | 4 | Interior singularity |
| **Total** | **20** | |

---

## Note for the Instructor

**Q5 is the diagnostic, and it is deliberately a case where carelessness is rewarded** with the right number. Students who did not split should be told explicitly that they got 6 by luck: for $p=\tfrac23$ the antiderivative extends continuously across the singularity, and for $p\ge1$ it does not.

**Midterm 1 is next week.** If Q1/Q2 show the two $p$-tests being confused with each other, that is worth five minutes of board time — it is the single most examinable confusion in Weeks 0–4.

---

*MATH 142 · Week 4 · Quiz 04 · covers Week 3*
