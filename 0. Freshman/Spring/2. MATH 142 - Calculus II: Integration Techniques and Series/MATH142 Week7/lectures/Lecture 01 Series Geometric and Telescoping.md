# MATH 142 · Calculus II
## Week 7 · Lecture 1 (Monday)
### Series, Geometric and Telescoping

---

**Reading:** Stewart §11.2 | Apostol Ch. 10 §10.10–10.11
**Quiz 07** — this Monday, **covers Week 6** (sequences, monotone convergence, recursion)

---

## 1. The Definition

Given a sequence $\{a_n\}$, form its **partial sums**:

$$s_1 = a_1,\quad s_2=a_1+a_2,\quad \ldots,\quad s_N = \sum_{n=1}^N a_n$$

Then

$$\boxed{\sum_{n=1}^\infty a_n \;:=\; \lim_{N\to\infty}s_N}$$

If that limit exists and is finite, the series **converges** to it. Otherwise it **diverges**.

> **Note what this does not say.** It does not say "add up infinitely many numbers" — that is not an
> operation anyone can perform. **It says: add finitely many, then take a limit.** The whole subject
> is the study of that limit, and $\{s_N\}$ is an ordinary sequence to which all of Week 6 applies.

### An immediate consequence

$$a_n = s_n - s_{n-1}$$

so the terms are the *increments* of the partial sums. **A series and its sequence of partial sums are two views of the same data**, and it is often the second that is easier to reason about.

---

## 2. Geometric Series — The Most Important Series

$$\sum_{n=0}^\infty ar^n = a+ar+ar^2+ar^3+\cdots$$

**We can find the partial sums exactly**, which is rare. Write

$$s_N = a+ar+\cdots+ar^{N-1},\qquad rs_N = ar+ar^2+\cdots+ar^{N}$$

Subtracting, everything cancels except the ends:

$$s_N(1-r) = a-ar^N \implies s_N = \frac{a(1-r^N)}{1-r}\qquad(r\neq1)$$

Now take $N\to\infty$. **By Week 6's geometric sequence**, $r^N\to0$ exactly when $|r|<1$:

$$\boxed{\sum_{n=0}^\infty ar^n = \frac{a}{1-r} \quad\text{if } |r|<1;\qquad \text{diverges if } |r|\ge1}$$

*(Verified: $\sum_{n\ge0}(\tfrac12)^n=2$, $\sum_{n\ge1}(\tfrac12)^n=1$, $\sum_{n\ge0}3(\tfrac14)^n=4$.)*

### Three warnings

**(a) Where does the sum start?** $\sum_{n\ge0}$ and $\sum_{n\ge1}$ differ by the term $a$. **The formula $\frac{a}{1-r}$ is for a series beginning at $n=0$**, i.e. with first term $a$. Safest rule:

$$\text{sum} = \frac{\text{first term}}{1-r}$$

**(b) $r=1$ must be excluded** before dividing by $1-r$. (Then $s_N = Na\to\infty$.)

**(c) $|r|=1$ diverges.** At $r=-1$ the partial sums oscillate $a,0,a,0,\ldots$ — bounded, but with no limit. **Week 6's point that "diverges" includes oscillation.**

### Why it matters so much

- **Week 9's radius of convergence** is found by comparing a power series with a geometric one.
- **The Ratio Test** (Week 8) is a geometric comparison in disguise.
- $0.\overline{9} = \sum_{n\ge1}9\cdot10^{-n} = \frac{9/10}{1-1/10} = 1$ — **exactly 1**, and this is the proof.

---

## 3. Telescoping Series

The other family we can sum exactly: when consecutive terms cancel.

### Example 1

$$\sum_{n=1}^\infty\frac{1}{n(n+1)}$$

**Partial fractions** (Week 2): $\dfrac{1}{n(n+1)} = \dfrac1n-\dfrac{1}{n+1}$. So

$$s_N = \left(\frac11-\frac12\right)+\left(\frac12-\frac13\right)+\cdots+\left(\frac1N-\frac1{N+1}\right) = 1-\frac{1}{N+1}$$

**Everything cancels except the first and last.** Hence

$$\sum_{n=1}^\infty\frac{1}{n(n+1)} = \lim_{N\to\infty}\left(1-\frac1{N+1}\right) = \boxed{1}$$

*(Verified.)*

### Example 2 — when the cancellation skips

$$\sum_{n=1}^\infty\frac{1}{n(n+2)},\qquad \frac{1}{n(n+2)} = \frac12\left(\frac1n-\frac{1}{n+2}\right)$$

Now terms cancel **two apart**, so **two** survive at each end:

$$s_N = \frac12\left(1+\frac12-\frac{1}{N+1}-\frac{1}{N+2}\right)\longrightarrow \frac12\cdot\frac32 = \boxed{\frac34}$$

*(Verified.)*

> **Write out the first three and last three terms explicitly.** Guessing which terms survive is the
> main source of error, and it costs nothing to check.

**Telescoping is the discrete version of Week 3's Example 6**, where $\ln(T-1)-\ln(T+1)$ had a finite limit although each piece diverged. **Same structure: a difference survives where the pieces do not.**

---

## 4. Algebra of Series

If $\sum a_n = A$ and $\sum b_n = B$ (both convergent) and $c$ is constant:

$$\sum(a_n\pm b_n) = A\pm B,\qquad \sum ca_n = cA$$

**And two things that are *not* true in general:**

- $\sum a_nb_n \neq AB$. There is no product rule for series.
- **You may not rearrange the terms** of a general convergent series. *(Week 8 shows how badly this fails.)*

**Adding or removing finitely many terms never changes convergence** — it changes the value, but not whether a value exists. **Convergence is a property of the tail.**

---

## 5. The $n$-th Term Test

> **Theorem.** If $\sum a_n$ converges, then $a_n\to0$.
>
> **Contrapositive (the useful form):** if $a_n\not\to0$, then $\sum a_n$ **diverges**.

**Proof.** $a_n = s_n-s_{n-1}$, and if $s_n\to S$ then both $s_n$ and $s_{n-1}$ tend to $S$, so $a_n\to S-S=0$. $\blacksquare$

### ⚠ The converse is false, and this is the central trap of the subject

$$a_n\to0 \quad\textbf{does not imply}\quad \sum a_n \text{ converges}$$

**The harmonic series is the counterexample**, and §6 proves it.

> **The $n$-th Term Test can only ever prove divergence.** If the terms tend to zero, **the test is
> over and has told you nothing** — you must use another. Writing "the terms go to zero, so it
> converges" is the most common error in this course, and it is worth zero marks every time.

### Example 3

$\displaystyle\sum_{n=1}^\infty\frac{n}{2n+1}$ — the terms tend to $\frac12\neq0$, so it **diverges.**

$\displaystyle\sum_{n=1}^\infty\frac{1}{n}$ — the terms tend to $0$, so the test is **inconclusive.** (It diverges, but for a different reason.)

---

## 6. The Harmonic Series Diverges

$$\sum_{n=1}^\infty\frac1n = \infty$$

**Oresme's proof (c. 1350)** groups the terms in blocks of doubling length:

$$1+\underbrace{\frac12}_{\ge\frac12}+\underbrace{\left(\frac13+\frac14\right)}_{>\frac14+\frac14=\frac12}+\underbrace{\left(\frac15+\cdots+\frac18\right)}_{>4\cdot\frac18=\frac12}+\underbrace{\left(\frac19+\cdots+\frac1{16}\right)}_{>8\cdot\frac1{16}=\frac12}+\cdots$$

**Each bracket exceeds $\frac12$**, and there are infinitely many brackets, so the partial sums exceed any bound. $\blacksquare$

*(Verified: the series diverges.)*

### How slowly

$$H_N = \sum_{n=1}^N\frac1n \approx \ln N+\gamma,\qquad \gamma = 0.5772156649\ldots$$

where $\gamma$ is the **Euler–Mascheroni constant**.

*(Verified: $H_N-\ln N-\gamma$ is $0.049$ at $N=10$, $5.0\times10^{-5}$ at $N=10^4$, and $5.0\times10^{-7}$ at $N=10^6$ — the difference is about $\frac{1}{2N}$.)*

**Since the growth is logarithmic, reaching a sum of 100 requires about $1.5\times10^{43}$ terms** *(computed)* — more than any computation will ever perform.

> **Note the block proof needed no calculus at all**, and it settles in five lines a question no
> amount of computing could. **This is why the tests exist.**

**A footnote on the history.** Oresme (c. 1323–1382) had this argument around 1350 — roughly three centuries before calculus. **It was then lost**, and the result had to be proved again by Mengoli in 1647, by Johann Bernoulli in 1687, and by Jakob Bernoulli shortly after. *A five-line argument, mislaid for three hundred years.*

**Nobody knows whether $\gamma$ is rational.** It is one of the most conspicuous open problems in mathematics.

---

## 7. What To Take From This Lecture

1. **A series is the limit of its partial sums.** Not an infinite addition.
2. **Geometric: $\frac{\text{first term}}{1-r}$ for $|r|<1$.** The most-used formula in the rest of the course.
3. **Telescoping: write out both ends** and see what survives.
4. **Convergence depends only on the tail.**
5. **$n$-th Term Test proves divergence only.** $a_n\to0$ is necessary, never sufficient.
6. **The harmonic series is the counterexample to everything you want to believe**, and it diverges too slowly ever to be seen doing so.

---

*Next: Tuesday — The Integral Test, and $p$-Series*
