# MATH 142 · Calculus II
## Problem Set 6 — Solutions
### INSTRUCTOR / TA COPY — not for distribution

---

**Total: 100 points.** Every limit verified symbolically; every recursive limit confirmed numerically.

> **Marking philosophy — this changes from this week.** Through Week 5 the answer carried most of the
> marks. **From here the *justification* does.** A correct limit with no method named is worth about
> half; a correct method with an arithmetic slip keeps most of its marks.
>
> **The single most important thing to enforce is Part C's two-step discipline.** A fixed point
> equation solved without a convergence argument must score zero for method, however tidy the answer —
> because C5 shows exactly what that habit produces.

---

## Part A — Basic Limits (5 pts each)

### A1 (5) $\;\dfrac{3n^2-2n}{n^2+5}$

Divide by $n^2$: $\;\dfrac{3-2/n}{1+5/n^2}\to\boxed{3}$

*Verified. Marking: 2 method, 3 value.*

### A2 (5) $\;\dfrac{\ln n}{n^{1/3}}$

**Pass to the function**, $\frac\infty\infty$, L'Hôpital:

$$\lim_{x\to\infty}\frac{\ln x}{x^{1/3}} = \lim_{x\to\infty}\frac{1/x}{\frac13x^{-2/3}} = \lim_{x\to\infty}\frac{3}{x^{1/3}} = \boxed{0}$$

*Verified. Marking: **2 for passing to the function explicitly** — this is the theorem being applied, and the whole of D2 is about it.*

*(Also acceptable: cite the growth hierarchy $\ln n\ll n^p$.)*

### A3 (5) $\;\left(1+\frac5n\right)^n$

$1^\infty$: take logs, $n\ln\left(1+\frac5n\right)\to5$, so the limit is $\boxed{e^5}$.

*Verified. Marking: 2 for logs, 3 for the value. Accept quoting $\left(1+\frac xn\right)^n\to e^x$.*

### A4 (5) $\;\dfrac{(-1)^n}{n^2+1}$

$\left|\dfrac{(-1)^n}{n^2+1}\right| = \dfrac{1}{n^2+1}\to0$, so by the corollary to the squeeze, the limit is $\boxed{0}$.

*Verified. Marking: 3 for using $|a_n|\to0\implies a_n\to0$, 2 for the value.*

> **The alternating sign is a distractor here and a killer in C5-style problems.** A student who wrote
> "diverges because of $(-1)^n$" has over-applied the Lecture 2 §6 warning — **that warning applies
> when the magnitude tends to a nonzero limit.** Worth an explicit comment.

---

## Part B — Techniques (6 pts each)

### B1 (6) $\;(n^2)^{1/n}$

$\ln a_n = \frac{2\ln n}{n}\to0$, so $a_n\to\boxed{1}$.

*Verified.*

### B2 (6) $\;\sqrt{n^2+3n}-n$

Conjugate:

$$\frac{(n^2+3n)-n^2}{\sqrt{n^2+3n}+n} = \frac{3n}{\sqrt{n^2+3n}+n} = \frac{3}{\sqrt{1+3/n}+1}\to\boxed{\frac32}$$

*Verified. Marking: 3 for the conjugate, 3 for dividing by $n$ correctly. **The common wrong answer is 0**, from asserting that the difference of two things $\approx n$ vanishes.*

### B3 (6) $\;\dfrac{3^n}{n!}$

$a^n\ll n!$, so the limit is $\boxed{0}$.

**The one-line reason:** once $n>6$, every additional factorial factor exceeds $2\cdot3$, so from that point the terms are bounded by a constant times $\left(\frac12\right)^n$ — a geometric sequence tending to 0.

*Verified. Marking: 2 for the value, **4 for the reason** (the question asked). Quoting the hierarchy alone earns 2.*

### B4 (6) $\;n\sin\frac1n$

Substitute $h=\frac1n\to0^+$: $\;\dfrac{\sin h}{h}\to\boxed{1}$.

*Verified. Marking: 6. Accept L'Hôpital on the function.*

### B5 (6) $\;\dfrac{n!\,e^n}{n^n\sqrt n}$

By Stirling, $n!\sim\sqrt{2\pi n}\left(\frac ne\right)^n$, so

$$\frac{n!\,e^n}{n^n\sqrt n} \sim \frac{\sqrt{2\pi n}\cdot n^ne^{-n}\cdot e^n}{n^n\sqrt n} = \frac{\sqrt{2\pi n}}{\sqrt n} = \boxed{\sqrt{2\pi}}\approx2.5066$$

*Verified symbolically: the CAS returns $\sqrt2\sqrt\pi$.*

**Where the constant comes from:** the $\sqrt{2\pi}$ in Stirling's formula, which is derived from **Wallis' product — Lab 1.**

*Marking: 4 for the manipulation, **2 for naming the constant and its origin.** Students who trace it back to Lab 1 have connected two halves of the course and should be told so.*

---

## Part C — Monotone Convergence and Recursion (6 pts each)

### C1 (6) $\;a_1=\sqrt6$, $a_{n+1}=\sqrt{6+a_n}$

**(a) Bounded above by 3.** $a_1=\sqrt6\approx2.449<3$ ✓. If $a_n<3$ then $a_{n+1}=\sqrt{6+a_n}<\sqrt9=3$ ✓.

**(b) Increasing.** $a_{n+1}>a_n\iff 6+a_n>a_n^2 \iff a_n^2-a_n-6<0\iff(a_n-3)(a_n+2)<0$, true for $0<a_n<3$ ✓ by (a).

**(c)** Increasing and bounded above $\implies$ converges. Then $L=\sqrt{6+L}$, so $L^2-L-6=(L-3)(L+2)=0$; terms are positive so

$$\boxed{L=3}$$

*Verified: sympy gives roots $\{3\}$ under positivity, and 30 iterations converge to $3.0$.*

*Marking: 2 + 2 + 2. **The induction in (a) must be a genuine induction**, and (b) must use (a). Discarding $L=-2$ requires a stated reason.*

### C2 (6) — Babylonian for $\sqrt5$

**(a)** $L = \frac12\left(L+\frac5L\right)\implies 2L^2 = L^2+5\implies L^2=5$, so $L=\pm\sqrt5$; the positive one is relevant.

**(b)** $g(x)=\frac12\left(x+\frac5x\right)$, so $g'(x)=\frac12\left(1-\frac{5}{x^2}\right)$, and at $x=\sqrt5$:

$$g'(\sqrt5) = \frac12\left(1-\frac55\right) = \boxed{0}$$

**$g'(L)=0\implies$ quadratic convergence — digits should double each step.**

**(c)** From $a_1=2$:

| $n$ | $a_n$ |
|---|---|
| 1 | $2$ |
| 2 | $2.25$ |
| 3 | $2.2361111\ldots$ |
| 4 | $2.2360679779\ldots$ |
| 5 | $2.2360679774997896964091\ldots$ |

$\sqrt5 = 2.2360679774997896964091\ldots$ — the two agree through $2.2360679774997896964$, i.e. **20 correct digits after 5 steps.** *(Verified.)*

*The digit counts run roughly $1,\ 3,\ 6,\ 12,\ 20$ — doubling, as $g'(L)=0$ predicts.*

*Marking: 2 + 2 + 2. **(b)'s zero derivative is the point of the problem.***

### C3 (6) $\;a_1=1$, $a_{n+1}=1+\dfrac{1}{1+a_n}$

**Convergence:** the map $g(x)=1+\frac{1}{1+x}$ has $g'(x) = -\frac{1}{(1+x)^2}$, and on $x\ge1$ we have $|g'|\le\frac14<1$ — **a contraction**, so the iteration converges. *(Accept a monotone-subsequence argument instead; the sequence alternates about the limit, so it is not itself monotone.)*

**Limit:** $L = 1+\frac{1}{1+L}\implies L(1+L) = 1+L+1 \implies L^2 = 2$, so

$$\boxed{L=\sqrt2}$$

*Verified: sympy gives $\sqrt2$; 40 iterations give $1.4142135623731$.*

**This is the continued fraction for $\sqrt2$**, which is worth pointing out.

*Marking: 3 for a convergence argument, 3 for the limit. **Accept the contraction argument** — it is Lecture 3 §5's criterion, and students who reach for it are ahead.*

### C4 (6) $\;a_n = \dfrac{n!}{n^n}$

**Decreasing:**

$$\frac{a_{n+1}}{a_n} = \frac{(n+1)!}{(n+1)^{n+1}}\cdot\frac{n^n}{n!} = \frac{(n+1)n^n}{(n+1)^{n+1}} = \left(\frac{n}{n+1}\right)^n<1$$

so $a_{n+1}<a_n$ ✓

**Bounded below:** every term is positive, so $a_n>0$ ✓

**Decreasing and bounded below $\implies$ converges.** By the growth hierarchy $n!\ll n^n$, the limit is $\boxed{0}$.

*Verified.*

*Marking: 3 for the ratio argument, 1 for boundedness, 2 for the limit. **The ratio simplifying to $\left(\frac{n}{n+1}\right)^n$ is the elegant step**; note in passing that this ratio tends to $1/e$, not 0 — the terms shrink geometrically, which is more than enough.*

### C5 (6) — the trap

**(a)** $a_1=2,\ a_2=4,\ a_3=10,\ a_4=28,\ a_5=82$. **Increasing without bound — divergent.** *(Verified.)*

**(b)** $L=3L-2\implies 2L=2\implies L=1$.

**(c)** **No contradiction: (b) computes what the limit *would* be if one existed.** The derivation $L=\lim a_{n+1}=g(\lim a_n)=g(L)$ **assumes the limit exists** — and here it does not. **The missing hypothesis is convergence itself**, which Step 1 of the two-step method exists to establish.

**(d)** $g(x)=3x-2$, so $g'(x)=3$ everywhere, and $|g'(1)|=3>1$. **The fixed point is repelling:** any start other than exactly $L=1$ moves away from it, at a factor of 3 per step.

*Indeed $a_1=2$ is a distance 1 from the fixed point, and the distances go $1,3,9,27,81$ — exactly $3^{n-1}$.*

*Marking: 1 + 1 + 3 + 1. **(c) is the question.** It must identify that the fixed point derivation presupposes convergence. "Because it diverges" earns 1 — that is the observation, not the diagnosis.*

> **This is structurally identical to Week 3's $\int_{-1}^1x^{-2}=-2$:** a theorem applied without
> checking its hypotheses, producing a confident wrong number. Make that link explicit when returning
> the set.

---

## Part D — Concept (10 pts each)

### D1 (10) — completeness

**(a)** An increasing sequence bounded above converges; a decreasing sequence bounded below converges.

**(b)** Within $\mathbb Q$ the sequence is increasing and bounded above by 2, so the theorem *would* assert a limit in $\mathbb Q$. **But its limit is $\sqrt2$, which is irrational.** So the theorem is **false in $\mathbb Q$** — the least upper bound of the set of terms simply does not exist within $\mathbb Q$.

**(c)** The proof of the theorem consists of taking the **least upper bound** of the terms and showing the sequence converges to it. **That supremum is guaranteed to exist only by the completeness axiom of $\mathbb R$.** So the theorem is really a statement about the *number system*: it says $\mathbb R$ has no gaps. Nothing about the sequence changes when we move from $\mathbb Q$ to $\mathbb R$ — only the availability of the limit.

**(d)** In Week 3, the increasing bounded quantity was

$$F(T) = \int_a^T f(x)\,dx$$

which increases in $T$ because $f\ge0$, and is bounded above by $\int_a^\infty g$ for the comparison function $g$. **Monotone convergence then gives the existence of $\lim_{T\to\infty}F(T)$** — i.e. convergence of the improper integral.

*Marking: 2 + 3 + 3 + 2. **(c) must identify the supremum as the point of contact with completeness.** (d) is a genuine retrospective connection and students who see it have understood both weeks.*

### D2 (10) — one-way streets

**(a)** If $a_n=f(n)$ and $\lim_{x\to\infty}f(x)=L$ **then** $\lim_{n\to\infty}a_n=L$. **The implication runs from function to sequence only.**

**(b)** $f(x)=\sin(\pi x)$, $a_n=\sin(\pi n)$. Every $a_n=0$ since $\pi n$ is an integer multiple of $\pi$, so $a_n\to0$; but $f$ oscillates between $-1$ and $1$ forever and has no limit.

**The sequence samples the function only at integers**, and here the integers are precisely the zeros — so the sequence sees none of the oscillation.

**(c)** The student has used the **converse**, which is false. The correct value is

$$\lim_{n\to\infty}\sin(\pi n) = \boxed{0}$$

since every term is exactly 0.

**(d)** **You may:** compute $\lim_{x\to\infty}f(x)$ with L'Hôpital and transfer the answer to the sequence. This is how essentially every limit in Part A and B was done.

**You may not:** conclude anything when the function limit fails to exist. **A non-existent function limit is simply no information about the sequence** — you must then argue directly (squeeze, monotone convergence, or the definition).

*Marking: 2 + 3 + 2 + 3. **(d) must state both halves.** A student who only says "use L'Hôpital carefully" earns 1 of the 3.*

---

## Marking Summary

| Part | Points | Focus |
|---|---|---|
| A (4 × 5) | 20 | Standard limits |
| B (5 × 6) | 30 | Logs, conjugates, hierarchy, Stirling |
| C (5 × 6) | 30 | Monotone convergence; recursion; the fixed point trap |
| D (2 × 10) | 20 | Completeness; the one-way implication |
| **Total** | **100** | |

---

## Diagnostic Notes

| Question | Weakness | Bites in |
|---|---|---|
| **C5** | Solving $L=g(L)$ without proving convergence | Week 7 onward, constantly |
| **A4** | Treating any $(-1)^n$ as automatic divergence | Week 8 (alternating series) |
| **D1** | Not seeing monotone convergence behind the tests | Weeks 7–8 (every positive-term test) |
| **D2(d)** | Concluding from a failed L'Hôpital | Week 8 (the $n$-th term test) |

**Week 7 begins series.** The one habit to carry forward is **C5's**: *a test tells you something only when its hypotheses hold.* Every convergence test in the next three weeks has hypotheses, and the characteristic error of the whole second half is applying one without them.

---

*MATH 142 · Week 6 · PS 6 Solutions · Instructor Only*
