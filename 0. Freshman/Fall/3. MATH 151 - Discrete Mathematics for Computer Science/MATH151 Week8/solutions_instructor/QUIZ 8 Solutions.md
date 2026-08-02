# MATH 151 — Quiz 8 Solutions
## INSTRUCTOR ONLY — DO NOT DISTRIBUTE

**Total: 20 points.** All values verified computationally.

---

**Q1. (4 pts)** $10 \times 9 \times 8 \times 7 = \mathbf{5040}$, which is $P(10,4)$.

Each digit position draws from the digits not yet used, so the count falls by one each time.

*Marking: 2 for the product, 1 for the value, 1 for the permutation notation. A student answering
$10^4 = 10000$ has ignored "no repeated digit" — 0 marks.*

---

**Q2. (4 pts)** $\binom{10}{3} = \mathbf{120}$ and $P(10,3) = \mathbf{720}$.

$P(10,3)$ counts **ordered** selections; $\binom{10}{3}$ counts **unordered** ones. They differ by
the factor $3! = 6$, the number of orderings of each chosen set — and indeed $720 / 120 = 6$.

*Marking: 1 each for the values, 2 for an explanation that names order as the distinguishing feature.*

---

**Q3. (4 pts)** By the Binomial Theorem, the coefficient of $x^{3}y^{5}$ in $(x+y)^8$ is
$\binom{8}{3} = \mathbf{56}$.

The identity is **symmetry**: $\binom{n}{k} = \binom{n}{n-k}$, so $\binom{8}{3} = \binom{8}{5} = 56$
— verified. Choosing which 3 factors contribute an $x$ is the same as choosing which 5 contribute a
$y$.

*Marking: 2 for the value, 2 for naming the symmetry identity. Students who compute $\binom{8}{5}$
directly and get 56 also earn full marks if they explain the correspondence.*

---

**Q4. (4 pts)** $\binom{10}{3} = \mathbf{120}$.

It is a combination because the three 1s are **indistinguishable** — a bit string is determined
entirely by *which* positions hold the 1s, not by any order among them. Choosing positions
$\{1,4,7\}$ gives one string, not $3!$ different strings.

*Marking: 2 for the value, 2 for the indistinguishability argument. "Because order doesn't matter"
alone earns 1 — the question asks why it doesn't.*

---

**Q5. (4 pts)** Total committees of 4 from 12 people: $\binom{12}{4} = 495$.
Committees with **no** woman (all 4 from the 7 men): $\binom{7}{4} = 35$.

$$495 - 35 = \mathbf{460}$$

*(Verified against the direct case sum $\sum_{w=1}^{4}\binom{5}{w}\binom{7}{4-w} = 460$.)*

*Marking: 1 for the total, 1 for the complement count, 2 for the subtraction and answer. The direct
four-case sum is equally correct and worth full marks, but note in feedback that it is four times the
work — this question is the setup for Week 8's complement habit.*

---

## Grade Distribution Notes

Q5 is the discriminator. Students who reach for the complement have absorbed the most transferable
idea in Week 7; those who enumerate cases will find Week 8's inclusion–exclusion much harder, since
it is the same move generalised.
