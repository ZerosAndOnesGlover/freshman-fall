# MATH 241 · Recitation 9
## Fitting, the Day After the Midterm
### Covers Week 9 · sat **Thursday of Week 10**, 15:00–15:50, SSB 108 · **unmarked, attendance required**

---

> **This session sits where Recitation 5 did, and the sheet is built for it again.**
>
> **Midterm 2 was yesterday** (Wednesday, 18:00–19:15, SSB 110, Weeks 6–9). **PS 9 is due at 17:00
> tomorrow.** Short drill, long clinic, problem set before post-mortem.

**What to bring:** your PS 9 attempt, **and** one question from yesterday's paper you cannot call.

---

## 0. Before You Come (10 minutes, at home)

Fit $y = c + dx$ to $(1,2)$, $(2,3)$, $(3,5)$.

**Bring $A$, $A^\mathsf{T}A$, $A^\mathsf{T}b$, $\hat x$, the residual $e$, and the check $A^\mathsf{T}e = 0$.**

---

## 1. The Drill (10 min)

**(a)** Compare answers. Expect $y = \tfrac13 + \tfrac32x$ with $e = \left(\tfrac16, -\tfrac13, \tfrac16\right)$ — **but check against part (c) before believing either of you.**

**(b)** **Two free checks you should always run.** Confirm $\sum e_i = 0$ and $\sum x_ie_i = 0$, and say which equation of $A^\mathsf{T}e = 0$ each one is.

**(c)** Verify the line passes through the centroid $(\bar x, \bar y) = (2, \tfrac{10}{3})$.

**(d)** **Without refitting:** if every $y_i$ increased by 7, what would happen to $c$ and to $d$? Predict, then check.

---

## 2. Why Not the Normal Equations (15 min)

**This is the session.**

$$A = \begin{bmatrix}1&1\\ \varepsilon&0\\ 0&\varepsilon\end{bmatrix}$$

**(a)** Compute $A^\mathsf{T}A$ by hand. **Its columns are obviously independent — say why in five seconds.**

**(b)** Give $\det(A^\mathsf{T}A)$ exactly. Now: **at what $\varepsilon$ does a `double` compute that determinant as zero?** Derive it from $\varepsilon_{\text{mach}} = 2^{-52}$ rather than guessing.

**(c)** **The point of the section.** At $\varepsilon = 10^{-8}$, $A^\mathsf{T}A$ is exactly singular in floating point while $A$ has two visibly independent columns.

**Where was the information lost?** Answer precisely — name the operation.

**(d)** $\operatorname{cond}(A^\mathsf{T}A) = \operatorname{cond}(A)^2$. Using Week 0's rule of thumb, **how many digits does each method have at $\operatorname{cond}(A) = 10^6$?**

**(e)** **The argument to have as a pair.** Here is the three-method table from the script:

| $\varepsilon$ | normal equations | Gram–Schmidt QR | Householder QR |
|---|---|---|---|
| $10^{-7}$ | $0.500000000$ | $0.511501869$ | $0.500000000$ |
| $10^{-8}$ | FAILED | $1.000000000$ | $0.500000000$ |

**At $10^{-7}$ the method you were told to avoid is exact and the method you were told to use is wrong.** Explain both. **Is the normal equations' answer there something you could rely on?**

> *(No. $\operatorname{cond}(A^\mathsf{T}A) \approx 2\times10^{14}$ at that $\varepsilon$ — the posed
> problem has two reliable digits and nine came out right by the luck of a symmetric $2\times2$.
> **And the Gram–Schmidt failure is Week 8's L26 §5 measured**: nearly parallel columns, catastrophic
> cancellation in the subtraction. **"Use QR" was never the whole advice.**)*

---

## 3. What It Assumes (10 min)

**(a)** Five points on $y = x$: $(1,1)$ … $(5,5)$. **Predict** what happens to the fitted line if $(5,5)$ becomes $(5,15)$. Then compute.

**(b)** Now **predict** what happens if $(3,3)$ becomes $(3,13)$ instead — same size of change, middle of the data. **Commit to a prediction before computing.**

**(c)** **You were probably wrong.** The slope does not move at all; only the intercept does, and the residual is *twice* as large as in (a). **Explain both facts**, using Q1(c)'s centroid result.

**(d)** **So $\lVert e\rVert$ does not measure how badly an outlier distorted the model.** What would?

---

## 4. Clinic — PS 9, and Yesterday's Paper (15+ min)

### PS 9 first, due tomorrow at 17:00

- **Q2(c), the zero residual.** If §3 landed, this is written. A degree-3 polynomial through 4 points **always** fits exactly; that is arithmetic, not evidence.
- **Q4(d).** Three separate explanations required. **If you have only explained why the normal equations eventually fail, you have answered a third of it.**
- **Q5(b).** §3(b)–(c) of this sheet.
- **Q5(d).** One integral, then two sentences connecting it to Week 0. The integral is the easy half.

### Then yesterday's paper

**Bring the question you could not call.** Not for a mark — for the final, which is comprehensive.

> **What the TA will and will not do.** Will: work the *method* of a hard question with different
> numbers. Will not: confirm your answer, or discuss the mark scheme. **Papers are returned in
> Week 11, at Recitation 10.**
>
> **If the whole paper was hard**, that is an office-hours conversation, not a clinic one. Prof.
> Abara is 10:00–11:00 Thursdays in SSB 310 — **this morning** — and the Help Desk is BH 120.
> **Weeks 10 and 11 are the hardest of the course** and they assume Weeks 6–9 throughout.

---

*MATH 241 · Week 9 · Recitation 9 · sat Thursday of Week 10 · unmarked*
