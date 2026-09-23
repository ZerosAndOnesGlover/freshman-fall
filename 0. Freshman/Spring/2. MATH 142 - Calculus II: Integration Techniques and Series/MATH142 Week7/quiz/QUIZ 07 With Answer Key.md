# MATH 142 · Calculus II
## Quiz 07 — With Answer Key
### Week 7 · Monday · **Covers Week 6**

---

**Date:** Monday 8 March 2027 · 11:00–11:15 (start of Lecture 1) · Week 7
**Time:** 15 minutes, start of Monday's lecture
**Closed book, no calculator**
**Total: 20 points** (4 points each)

**Covers Week 6:** sequences, limit techniques, the growth hierarchy, monotone convergence.

---

## Questions

**Q1.** $\displaystyle\lim_{n\to\infty}\frac{4n^2-n}{3n^2+2}$

**Q2.** $\displaystyle\lim_{n\to\infty}\frac{\ln n}{\sqrt n}$ — name the method you use.

**Q3.** $\displaystyle\lim_{n\to\infty}\left(1+\frac2n\right)^n$

**Q4.** Does $\displaystyle\left\{\frac{n!}{2^n}\right\}$ converge? Justify.

**Q5.** Let $a_1=\sqrt{12}$ and $a_{n+1}=\sqrt{12+a_n}$. Given that this sequence converges, find its limit.

---
---

# ANSWER KEY

---

**Q1. (4)** Divide by $n^2$: $\;\dfrac{4-1/n}{3+2/n^2}\to\boxed{\dfrac43}$

*Marking: 1 method, 3 value. Verified symbolically.*

**Q2. (4)** **Pass to the function** and apply **L'Hôpital**:

$$\lim_{x\to\infty}\frac{\ln x}{\sqrt x} = \lim_{x\to\infty}\frac{1/x}{\frac12x^{-1/2}} = \lim_{x\to\infty}\frac{2}{\sqrt x} = \boxed{0}$$

*(Equally acceptable: cite the growth hierarchy $\ln n\ll n^p$.)*

*Marking: **2 for naming the method** — the question asked — and 2 for the value. A student who applied L'Hôpital directly to the sequence should be told there are no derivatives there; the theorem is about the function. Verified symbolically.*

**Q3. (4)** $1^\infty$: taking logs, $n\ln\left(1+\frac2n\right)\to2$, so the limit is $\boxed{e^2}$.

*(Or quote $\left(1+\frac xn\right)^n\to e^x$.)*

*Marking: 4. Verified symbolically.*

**Q4. (4)** **No — it diverges to $\infty$.**

By the growth hierarchy, $a^n \ll n!$, so $\dfrac{n!}{2^n}\to\infty$.

*Marking: 2 for the verdict, 2 for citing the hierarchy in the correct direction. **The common error is to invert it** and answer 0 — worth flagging, since $\frac{2^n}{n!}\to0$ is the fact students half-remember. Verified symbolically.*

**Q5. (4)** Given convergence, let $L=\lim a_n$. Continuity gives $L=\sqrt{12+L}$, so

$$L^2 = 12+L \implies L^2-L-12 = (L-4)(L+3) = 0$$

All terms are positive, so $L\ne-3$:

$$\boxed{L=4}$$

*Verified: sympy returns the positive root 4, and 40 iterations converge to $4.0$.*

*Marking: 2 for setting up $L=g(L)$, 1 for solving, **1 for discarding $-3$ with a stated reason.***

> **Note the question said "given that this sequence converges".** That phrasing is deliberate — it
> supplies the hypothesis that Week 6's two-step method requires. **A student who noticed and remarked
> on it deserves a comment**; a student who habitually solves $L=g(L)$ without one is heading for the
> PS 6 C5 error.

---

## Marking Summary

| Question | Points | Tests |
|---|---|---|
| Q1 | 4 | Dominant power |
| Q2 | 4 | The function connection + L'Hôpital |
| Q3 | 4 | $1^\infty$ via logs |
| Q4 | 4 | Growth hierarchy, correct direction |
| Q5 | 4 | Fixed point, with the hypothesis supplied |
| **Total** | **20** | |

---

## Note for the Instructor

**Q4 is the diagnostic.** Students who answer 0 have memorised $\frac{a^n}{n!}\to0$ without the ordering it comes from — and the growth hierarchy is used constantly from here to Week 10, especially in the Ratio Test.

**Q5's phrasing is the other thing to watch.** Today's lecture introduces series, where *every* test has hypotheses, and the habit of checking them is the single most important thing to establish this week.

---

*MATH 142 · Week 7 · Quiz 07 · covers Week 6*
