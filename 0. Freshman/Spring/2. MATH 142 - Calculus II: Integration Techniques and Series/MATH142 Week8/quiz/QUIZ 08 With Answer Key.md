# MATH 142 · Calculus II
## Quiz 08 — With Answer Key
### Week 8 · Monday · **Covers Week 7**

---

**Time:** 15 minutes, start of Monday's lecture
**Closed book, no calculator**
**Total: 20 points** (4 points each)

**Covers Week 7:** series, geometric and telescoping, the $n$-th Term Test, the Integral Test, $p$-series, comparison.

---

## Questions

**Q1.** Evaluate $\displaystyle\sum_{n=0}^{\infty}5\left(\frac13\right)^n$.

**Q2.** Evaluate $\displaystyle\sum_{n=1}^{\infty}\frac{1}{n(n+1)}$.

**Q3.** Does $\displaystyle\sum_{n=1}^{\infty}\frac{1}{n^{5/4}}$ converge? Name the test.

**Q4.** Does $\displaystyle\sum_{n=1}^{\infty}\frac{n}{n^2+4}$ converge? Justify by comparison.

**Q5.** Does $\displaystyle\sum_{n=1}^{\infty}\frac{1}{n^2+\sqrt n}$ converge? Justify.

---
---

# ANSWER KEY

---

**Q1. (4)** Geometric, first term 5, $r=\frac13$ with $|r|<1$:

$$\frac{5}{1-\frac13} = \frac{5}{2/3} = \boxed{\frac{15}{2}}$$

*Marking: 1 for checking $|r|<1$, 3 for the value. Verified symbolically.*

**Q2. (4)** Partial fractions: $\frac{1}{n(n+1)} = \frac1n-\frac1{n+1}$, so

$$s_N = 1-\frac{1}{N+1}\longrightarrow\boxed{1}$$

*Marking: 2 decomposition, 2 telescoping with the limit. **The partial sum must appear** — quoting "1" alone earns 2. Verified symbolically.*

**Q3. (4)** **Converges**, by the **$p$-series test** with $p=\frac54>1$.

*Marking: 2 verdict, 2 for naming the test with the value of $p$. Verified: the sum is $\zeta(5/4)\approx4.595$.*

**Q4. (4)** **Diverges.** Limit comparison with $b_n=\frac1n$:

$$L = \lim_{n\to\infty}\frac{n/(n^2+4)}{1/n} = \lim_{n\to\infty}\frac{n^2}{n^2+4} = 1 \in(0,\infty)$$

$\sum\frac1n$ diverges, so ours does.

*(Direct comparison also works: for $n\ge2$, $n^2+4\le2n^2$, so $\frac{n}{n^2+4}\ge\frac{1}{2n}$.)*

*Marking: 2 comparison series, 1 limit, 1 verdict. Verified symbolically; corroborated by partial sums $3.90,\ 8.50,\ 13.10$ — logarithmic growth.*

**Q5. (4)** **Converges.** For $n\ge1$, $n^2+\sqrt n>n^2$, so

$$0<\frac{1}{n^2+\sqrt n}<\frac{1}{n^2}$$

and $\sum\frac1{n^2}$ converges ($p=2>1$). **Direct comparison** gives convergence.

*Marking: 2 inequality with the correct direction, 2 verdict citing the $p$-series. Corroborated: partial sums settle near $1.046$.*

---

## Marking Summary

| Question | Points | Tests |
|---|---|---|
| Q1 | 4 | Geometric |
| Q2 | 4 | Telescoping |
| Q3 | 4 | $p$-series |
| Q4 | 4 | Limit comparison → divergence |
| Q5 | 4 | Direct comparison → convergence |
| **Total** | **20** | |

---

## Note for the Instructor

**Q4 and Q5 are the pair.** They look almost identical — a rational function of $n$ in each case — and the only thing distinguishing them is the **degree gap**: 1 in Q4 (behaves like $\frac1n$, diverges) and 2 in Q5 (behaves like $\frac1{n^2}$, converges).

**That is the single most useful reflex for a rational-function series**, and it is worth stating on the board when returning these: *subtract the degrees; that is your $p$.*

---

*MATH 142 · Week 8 · Quiz 08 · covers Week 7*
