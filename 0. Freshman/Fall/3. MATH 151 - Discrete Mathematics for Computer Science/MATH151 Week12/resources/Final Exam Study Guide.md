# MATH 151 — Final Exam Study Guide
## Comprehensive: Weeks 0–12

---

## Format

**3 hours · closed book · one double-sided A4 sheet of handwritten notes.**

Coverage is comprehensive, weighted towards Weeks 3, 5, 7, 8, 10, 11 — the material other courses
build on.

---

## The Highest-Yield Revision, In Order

1. **Redo every quiz.** Twelve quizzes, 15 minutes each. They were written to target exactly the
   skills that transfer, and doing all twelve costs three hours.
2. **Do the Part A questions of every problem set** — modelling and setup, not computation.
3. **Read the reference sheets.** Every verified value in the course is collected there.
4. **One full problem set under timed conditions.**

Do not start by re-reading lectures. Recognition is not recall.

---

## Formula Sheet — Know These Cold

### Logic (Weeks 0–1)
$$\neg(\forall x\,P) \equiv \exists x\,\neg P \qquad \neg(p\to q)\equiv p\wedge\neg q \qquad p\to q\equiv\neg q\to\neg p$$
Quantifier **order** matters: $\forall x\exists y \ne \exists y\forall x$.

### Proof (Weeks 2–3)
Direct · contrapositive · contradiction · induction (weak and strong).
Induction: base case, hypothesis, step — and **state where the hypothesis is used**.

### Sets and functions (Weeks 4–5)
$$\lvert\mathcal{P}(A)\rvert=2^{\lvert A\rvert} \qquad \lvert A\times B\rvert=\lvert A\rvert\lvert B\rvert$$
Injective / surjective / bijective. On **finite sets of equal size**, injective ⟺ surjective.
$\mathbb{Z},\mathbb{Q}$ countable; $\mathbb{R}$ not.

### Relations (Week 6)
Reflexive · symmetric · antisymmetric · transitive.
Equivalence relation ⟹ partition into classes.

### Counting (Week 7)
$$P(n,r)=\frac{n!}{(n-r)!} \qquad \binom nr=\frac{n!}{r!(n-r)!} \qquad \binom nk=\binom n{n-k} \qquad \sum_k\binom nk=2^n$$

### Advanced counting (Week 8)
Pigeonhole: $\lceil n/m\rceil$ — **check $n>m$ first**.
Inclusion–exclusion: alternating sum; intersections use **lcm**.
Complement rule for "at least one".
$D_n=n!\sum(-1)^k/k!$; $D_1..D_6 = 0,1,2,9,44,265$; $D_n/n!\to1/e$.

### Recurrences (Week 9)
Distinct roots $Ar_1^n+Br_2^n$ · **double root $(A+Bn)r^n$** · non-homogeneous = homogeneous + particular.
$$F_n=\frac{\varphi^n-\psi^n}{\sqrt5},\quad \varphi=\frac{1+\sqrt5}{2}$$
Generating functions: $\frac{1}{1-x}\to1,1,1,\ldots$; $\frac{1}{1-cx}\to c^n$; multiplication = independent choice.

### Graphs (Week 10)
$$\sum\deg(v)=2\lvert E\rvert$$
$K_n$: $\binom n2$ · $K_{m,n}$: $mn$ · $Q_n$: $2^n$ vertices, $n2^{n-1}$ edges.
Bipartite ⟺ no odd cycle.
Euler circuit ⟺ all degrees even; trail ⟺ exactly two odd.
Hamilton: **no criterion** — NP-complete.

### Trees (Week 11)
$n-1$ edges · degree sum $2(n-1)$ · unique paths · every edge a bridge · $\ge2$ leaves.
Binary tree: height $h$ ⟹ $\le 2^{h+1}-1$ nodes; $n$ nodes ⟹ $h\ge\lceil\log_2(n+1)\rceil-1$.
Cayley: $n^{n-2}$.
Kruskal and Prim always agree on **total weight**.
BFS = shortest paths, **unweighted only**.

### Number theory (Week 12)
Division algorithm: $0\le r<d$, so $-7\bmod3=2$.
$\gcd\cdot\operatorname{lcm}=ab$ · Bézout $ax+by=\gcd$.
$a^{-1}\bmod m$ exists ⟺ $\gcd(a,m)=1$.
$a^{p-1}\equiv1\pmod p$ · $a^{\varphi(n)}\equiv1\pmod n$ · $\varphi(pq)=(p-1)(q-1)$.
RSA: $d=e^{-1}\bmod\varphi(n)$; correctness **is** Euler's theorem.

---

## The Five Errors That Cost the Most Marks

1. **Pigeonhole without checking $n>m$.** PS 8 A1(b) and Quiz 9 Q5(a) were both traps for this.
2. **Forgetting the repeated-root case** in recurrences. $Ar^n+Br^n$ has only one free constant.
3. **Product instead of lcm** for an inclusion–exclusion intersection.
4. **Claiming isomorphism from a matching degree sequence.** $C_6$ versus two triangles.
5. **Not verifying a closed form** against three iterated values.

---

## Named Results You Should Be Able to State

| Result | Week |
|---|---|
| De Morgan's laws | 0 |
| Well-ordering / induction principle | 3 |
| Cantor's diagonal argument | 5 |
| Cantor's theorem $\lvert\mathcal{P}(A)\rvert>\lvert A\rvert$ | 5 |
| Binomial Theorem, Pascal's Rule | 7 |
| Pigeonhole (basic and generalised) | 8 |
| Inclusion–Exclusion | 8 |
| Binet's formula | 9 |
| Handshake Theorem | 10 |
| Euler's circuit criterion | 10 |
| Cayley's formula | 11 |
| The cut property | 11 |
| Fundamental Theorem of Arithmetic | 12 |
| Euclid's infinitude of primes | 12 |
| Bézout's identity | 12 |
| Fermat's Little Theorem, Euler's theorem | 12 |
| Chinese Remainder Theorem | 12 |

---

## Worked Values Worth Memorising

| | |
|---|---|
| $D_1..D_6$ | $0, 1, 2, 9, 44, 265$ |
| $F_0..F_{10}$ | $0,1,1,2,3,5,8,13,21,34,55$ |
| Primes below 50 | 15 of them; below 100, **25** |
| $\varphi(100)$, $\varphi(1000)$ | 40, 400 |
| $\gcd(252,198)$ | 18 |
| Catalan $C_0..C_6$ | $1,1,2,5,14,42,132$ |
| $2^{10}$ | 1024 |
| $\lceil\log_2(10^6+1)\rceil-1$ | 19 |

---

## Timing Strategy

With 3 hours and (typically) 6–8 questions, budget roughly 20 minutes each and keep 20 in reserve.

- **Do the computational questions first.** Counting, gcd, Kruskal traces — they are quick and full marks are available.
- **Proofs last**, and write the structure before the content: "By induction on $n$. Base case… Suppose… Then…". A partial proof with correct structure scores well; a paragraph of prose does not.
- **Show working on every trace.** Kruskal, Euclid, and BFS questions carry method marks that a bare answer forfeits.
- **State theorems by name** when you invoke them. It is faster than re-deriving and it earns the mark.

---

*MATH 151 · Week 12 · Final Exam Study Guide · © CSE Department*

*Good luck.*
