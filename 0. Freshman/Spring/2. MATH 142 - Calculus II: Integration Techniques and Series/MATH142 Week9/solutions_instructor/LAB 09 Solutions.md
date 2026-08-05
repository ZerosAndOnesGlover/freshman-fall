# MATH 142 · Calculus II
## Lab 09 — Solutions and Checkoff Notes
### INSTRUCTOR / TA COPY — not for distribution

---

**Total: 100 points.** All figures produced by running the lab.

---

## Part A — Radii (20 pts)

### A1 (12)

| | Series | $\lim\left\lvert\frac{c_{n+1}}{c_n}\right\rvert$ | $R$ |
|---|---|---|---|
| (i) | $\sum\frac{x^n}{n}$ | $1$ | $1$ |
| (ii) | $\sum\frac{x^n}{n!}$ | $0$ | $\infty$ |
| (iii) | $\sum n!\,x^n$ | $\infty$ | $0$ |
| (iv) | $\sum\frac{n^n}{n!}x^n$ | $e$ | $\frac1e$ |
| (v) | $\sum\frac{(3n)!}{(n!)^3}x^n$ | $27$ | $\frac1{27}$ |

*(All verified.)*

*Marking: 12, i.e. roughly 2.4 per series. **Both a hand computation and the CAS confirmation are required.***

### A2 (8)

The two unusual radii are **(iv) $R=\frac1e$** and **(v) $R=\frac1{27}$**.

- **(iv)** comes from $\left(1+\frac1n\right)^n\to e$ — **Week 6, Lecture 2, Example 2.**
- **(v)** comes from $\frac{(3n+1)(3n+2)(3n+3)}{(n+1)^3}\to 27$, i.e. three factors each tending to 3. *(Not a named Week 6 limit, but the same dominant-term reasoning.)*

*Marking: 4 for identifying the two, 4 for the sources. **Full credit for (v) if the student explains the $3^3$ rather than naming a theorem.***

---

## Part B — Can You See the Boundary? (30 pts)

### B1 (12)

Partial sums $s_{200}$ of $\sum\frac{x^n}{n}$, $R=1$:

| $x$ | $s_{200}$ | inside/outside |
|---|---|---|
| $0.9$ | $2.30258509296$ | **inside** |
| $0.99$ | $4.55727989114$ | **inside** |
| $1.0$ | $5.87803094812$ | boundary — **diverges** |
| $1.01$ | $9.54109970914$ | **outside** |
| $1.1$ | $1.1033037521\times10^{7}$ | outside |

*(Verified.)*

*Marking: 8 table, 4 for correct inside/outside labelling.*

### B2 (10)

**(a)** $4.557$, $5.878$, $9.541$.

**(b)** **Only $x=0.99$ converges.** At $x=1$ the series is the harmonic series and at $x=1.01$ the terms grow — both diverge.

**(c)** **No.** The three numbers are $4.56$, $5.88$, $9.54$ — all modest, all of the same order, all still increasing as $N$ grows. **Nothing distinguishes a partial sum climbing towards $4.605$ from one climbing towards infinity.**

*Marking: 2 + 3 + 5. **(c) is the point of the lab.** An answer of "no, they look similar" earns 3; full marks require noting that all three are still increasing and that a convergent partial sum and a slowly divergent one are indistinguishable at finite $N$.*

### B3 (8)

At $x=1.01$:

| $N$ | $s_N$ |
|---|---|
| $200$ | $9.541$ |
| $1000$ | $2400.3$ |
| $5000$ | $8.34\times10^{19}$ |

*(Verified.)*

**Divergence becomes unmistakable somewhere between $N=200$ and $N=1000$**, and is beyond any doubt by $N=5000$.

**Compare $x=1.1$**, where $s_{200}$ is already $1.1\times10^7$ — **obvious immediately.** The closer $x$ is to $R$, the longer the divergence stays hidden; **at $x=1$ exactly it is hidden forever** (the harmonic series grows like $\ln N$).

*Marking: 4 table, 4 for the comparison. **Full marks require the observation that proximity to $R$ controls how long the divergence hides.***

---

## Part C — The Cost Near the Boundary (25 pts)

### C1 (12)

Terms needed for $\left|-\ln(1-x) - s_N\right|<10^{-10}$:

| $x$ | $-\ln(1-x)$ | $N$ |
|---|---|---|
| $0.5$ | $0.69314718056$ | $29$ |
| $0.9$ | $2.30258509299$ | $190$ |
| $0.99$ | $4.60517018599$ | $1{,}988$ |
| $0.999$ | $6.90775527898$ | $19{,}974$ |

*(Verified.)*

### C2 (8)

| $x$ | $N$ | $N(1-x)$ |
|---|---|---|
| $0.5$ | $29$ | $14.5$ |
| $0.9$ | $190$ | $19.0$ |
| $0.99$ | $1988$ | $19.88$ |
| $0.999$ | $19974$ | $19.97$ |

**$N(1-x)$ settles at about $\boxed{20}$**, so $N\approx\dfrac{20}{1-x}$.

*(The leading-order estimate in the hint gives $\ln(10^{10}) = 23.0$; the measured constant is smaller because the error carries an extra factor $\frac{1}{N(1-x)}$ beyond the dominant $x^N$, which helps. **Accept anything in the range 18–23**, and credit a student who notices the discrepancy and explains it.)*

*Marking: 5 for the scaled column, 3 for the constant.*

### C3 (5)

**At $x=1$ exactly the series is $\sum\frac1n$ — the harmonic series, which diverges.** No finite $N$ achieves any accuracy, because there is no value to approach.

This is consistent with the interval of convergence $[-1,1)$: **$x=1$ is excluded**, and the blow-up of $N$ as $x\to1^-$ is the analytic shadow of that exclusion.

*Marking: 5. **The link to the interval $[-1,1)$ is required.***

---

## Part D — Getting $\pi$ From a Series (25 pts)

### D1 (8)

$$\arctan x = x-\frac{x^3}{3}+\frac{x^5}{5}-\frac{x^7}{7}+\frac{x^9}{9}-\cdots$$

*(Verified against the CAS expansion to $O(x^{10})$.)*

### D2 (9)

Errors of $s_N$ against $\frac\pi4 = 0.785398163397$:

| $N$ | error | bound $\frac{1}{2N+1}$ | holds |
|---|---|---|---|
| $10$ | $2.49383\times10^{-2}$ | $4.76190\times10^{-2}$ | ✓ |
| $100$ | $2.49994\times10^{-3}$ | $4.97512\times10^{-3}$ | ✓ |
| $1000$ | $2.50000\times10^{-4}$ | $4.99750\times10^{-4}$ | ✓ |

*(Verified — and note the error is consistently about **half** the bound, exactly as Week 8 predicted.)*

**For 10 digits:** need $\frac{1}{2N+1}<10^{-10}$, i.e.

$$\boxed{N > 5\times10^{9}\ \text{terms}}$$

*Marking: 5 table, 4 for the term count. **The "half the bound" observation should be credited** — it is Week 8's result reappearing.*

### D3 (8)

At $x=\frac{1}{\sqrt3}$, where $\arctan\frac{1}{\sqrt3}=\frac\pi6$:

$$\boxed{\textbf{17 terms}}$$ for $10^{-10}$ accuracy. *(Verified.)*

**Against $5\times10^9$ at $x=1$ — a factor of roughly $3\times10^{8}$.**

**Why:** the terms are $\frac{x^{2n+1}}{2n+1}$, and at $x=\frac{1}{\sqrt3}$ we have $x^2=\frac13$, so **the terms decay geometrically like $3^{-n}$.** At $x=1$ there is no geometric decay at all — the terms fall off only like $\frac1n$, because **$x=1$ sits exactly on the boundary of the interval of convergence.**

**This is Part C's finding stated the other way round:** the cost blows up as $x\to R$, so **evaluate as far inside the radius as you can arrange.**

*Marking: 3 for the term count, 5 for the explanation. **The explanation must identify geometric decay inside the radius versus none at the boundary.***

### Part E (within D3)

**The common reason across Labs 3, 7 and 9:**

> **Convergence is a property of the infinite tail, and no finite computation inspects the tail.**

*Marking: credited within D3. Award nothing for "the numbers look similar" — that is the symptom.*

---

## Marking Summary

| Part | Points |
|---|---|
| A | 20 |
| B | 30 |
| C | 25 |
| D | 25 |
| **Total** | **100** |

---

## Checkoff Checklist

1. A2 traces $R=\frac1e$ to $\left(1+\frac1n\right)^n\to e$
2. **B2(c) says the three numbers cannot be told apart**
3. B3 notes proximity to $R$ controls how long divergence hides
4. **C2's scaled column settles near 20**
5. C3 links to the interval $[-1,1)$
6. D2 confirms the error is ~half the alternating bound
7. **D3 gives 17 terms and explains via geometric decay**

---

## Note for the Debrief

> **Five numbers: $4.56$, $5.88$, $9.54$ at two hundred terms.** One of those series converges and two
> diverge, and nothing in the numbers says which. **The Ratio Test says which, exactly, in one line.**
>
> **This is the third time.** Lab 3: no computation distinguishes $\int x^{-1}$ from $\int x^{-1.01}$.
> Lab 7: the harmonic series needs $10^{43}$ terms to reach 100. Lab 9: the boundary of convergence is
> a single exact number that two hundred terms cannot locate.
>
> **The reason is always the same. Convergence is about the tail, and you never see the tail.**

Then the constructive half, which sets up Week 10:

> And yet Part D computed $\pi$ to ten digits **in seventeen terms** — by choosing to evaluate at
> $\frac{1}{\sqrt3}$ instead of at 1. **Same series, same function, a factor of three hundred million
> in work**, decided entirely by where you sit relative to the radius.
>
> **Next week that becomes a design principle.** Taylor series can be centred anywhere, and choosing
> the centre well is how a numerical library evaluates $\sin$, $\exp$ and $\log$ fast enough to be
> called billions of times a second.

---

*MATH 142 · Week 9 · Lab 09 Solutions · Instructor Only*
