# MATH 241 · Linear Algebra
## Week 5: Determinants

**Credits:** 4 (3 lecture + 1 recitation) · **Prerequisites:** MATH 141
**Assessment for this course (overall):** Problem Sets 35%, Midterms 40%, Final 25%
**This week's deliverables:** PS 5 (released Wednesday, due **Friday of Week 6**) and **Quiz 5** (Monday, covers Week 4). **PS 4 is due at 17:00 this Friday.**
**Recitation 4 is sat this Thursday** — it covers **Week 4**. Recitation 5, covering this week, is sat on the **Thursday of Week 6**.

> **This is the last teaching week before Midterm 1.** The paper is **Wednesday of Week 6,
> 18:00–19:15, SSB 110**, and covers **Weeks 0–5** — so this week's material is on it. One
> handwritten sheet, one side.
>
> **CS 201's Midterm 1 is this Monday evening**, 18:00–19:15, VNC 100.
>
> **Week 6 is compressed.** Its Monday is **Fall Break** (no classes), so **Quiz 6 moves to the
> Tuesday**; the midterm is Wednesday, Recitation 5 is Thursday, and PS 5 is due Friday.

---

### Why This Week Exists

Because Week 4 ended with three quantities that survive a change of basis — rank, trace and determinant — and **only rank had been explained.**

The determinant is one number extracted from $n^2$, so nearly everything is discarded. **What survives is worth a week**: it decides invertibility, it measures how much a transformation scales volume, and it is the same in every basis. The third of those is the theorem Week 4's L15 §6 used and could not prove.

**And there is a fourth reason, which is the real one.** Week 6 finds eigenvalues by solving

$$\det(A - \lambda I) = 0,$$

a determinant with a symbol in it. **Elimination cannot do that** — it would divide by expressions that might be zero, forcing a case split at every pivot. **Cofactor expansion can**, because it only ever multiplies and adds. So L17 spends a lecture on a method it then shows to be $9\times10^{14}$ times too slow for numbers, and the justification arrives next week.

**Week 5 also renews a warning it is now equipped to state properly.** $\det A = 0$ characterises singularity **exactly** — no approximation anywhere — and it is still a bad numerical test, because $\det(cA) = c^n\det A$ makes it depend on your choice of units. **An exact criterion and a useless one, simultaneously**, and understanding how both can be true is worth more than the theorem.

---

### Learning Objectives

By the end of Week 5, you should be able to:

1. State the three defining properties, and **derive** the working rules from them.
2. **Read P3 correctly** — linear in each row *separately* — and hence get $\det(cA) = c^n\det A$ right.
3. Compute a determinant **by elimination**, as $\pm$ the product of the pivots, with the sign rule.
4. **State $\det A = 0 \iff$ singular**, and place it as the seventh of Week 1's characterisations.
5. Compute by **cofactor expansion**, choosing the row or column with the most zeros.
6. **Cost the $n!$ formula against $n^3/3$**, and say what that means at $n = 20$.
7. State the adjugate formula and Cramer's rule, **and say why neither is a method.**
8. **Say when cofactors *are* the right tool** — small $n$, sparse rows, and symbolic entries.
9. **Explain $\lvert\det A\rvert$ as the volume-scaling factor**, and the sign as orientation.
10. Use $\det(AB) = \det A\det B$ to get $\det(A^{-1})$, $\det(A^k)$ and **similarity invariance**.
11. **Connect $\lvert\det J\rvert$ to MATH 142's change of variables**, and derive polar coordinates' $r$.
12. **Explain why an exact criterion can be a bad numerical test**, using scale-invariance.

---

### This Week's Materials

| File | Purpose |
| --- | --- |
| [[L16 The Determinant by Its Properties]] | Three properties, everything else derived; **adding a multiple of a row changes nothing, which is what lets elimination compute it**; $\det = \pm$ product of the pivots; **Week 1's matrix had pivots 2, 3, 4, so its determinant was 24 all along**; $\det = 0 \iff$ singular, completing Week 1's list of seven |
| [[L17 Cofactor Expansion and What It Costs]] | The $n!$ formula and the checkerboard; **why the $3\times3$ diagonal trick fails at $4\times4$**; **$9\times10^{14}$ at $n=20$, and 751× measured at $n=8$**; the adjugate and Cramer's rule, exact and unusable; **the four cases where cofactors win — including the symbolic one Week 6 needs** |
| [[L18 Determinant as Volume and the Product Rule]] | **The three properties are the properties of area**; the shear's determinant is 1 by base-times-height; **the sign is orientation**; $\det(AB) = \det A\det B$ and its consequences; **similarity invariance — Week 4's debt paid**; **polar coordinates' $r$ is a Jacobian determinant** |
| [[REC 5 Determinants, the Day After the Midterm]] | Drill, the two traps, and a long clinic — **PS 5 first, then the paper.** Thursday of Week 6 |
| [[PS 5 Determinants]] | Five questions, 100 points, due **Friday of Week 6** |
| [[MATH241 Week5/assignments/QUIZ 5 Week 5 Monday\|QUIZ 5 Week 5 Monday]] | Ten minutes, covers **Week 4**, answer key printed |
| [[MATH241 Week5/resources/Reading Guide Week 5\|Reading Guide Week 5]] | Strang Ch. 5, fifteen questions, **and what belongs on the midterm cheat sheet** |
| `resources/determinants.py` | Every number in L16–L18, reproducible. Three routes to one determinant, and the timing |
| `solutions_instructor/` | Instructor only |

---

### The One Thing to Take From This Week

**An exact criterion can be a useless test, and knowing why is the point.**

$$\det A = 0 \iff A \text{ is singular}$$

is a theorem. It is proved in L16 §5, it has no error term, and it holds for every square matrix over any field. **And you must never write `if det(A) != 0:`.**

**The reason is scale.** $\det(cA) = c^n\det A$, so the determinant of a $1000\times1000$ matrix with entries around $0.1$ is about $10^{-1000}$ — **which underflows a `double` to exactly zero**, while the matrix may be perfectly well conditioned. Conversely $\operatorname{diag}(10^6, 10^{-6})$ has determinant exactly 1 and condition number $10^{12}$.

**A quantity that changes when you switch from metres to millimetres cannot be measuring how hard a problem is.** $\operatorname{cond}(A) = \lVert A\rVert\lVert A^{-1}\rVert$ does not change, and it is the number to compute. *(Week 0's L03 §7 said this before the determinant was defined; PS 0 Q5(b) built both counterexamples.)*

> **The same shape recurs all term.** Cramer's rule is exact and unusable. The adjugate formula is
> exact and unusable. The $n!$ definition is exact and unusable. **Week 5 is where you learn to ask
> a second question after "is it correct?"** — and the second question is what the rest of numerical
> mathematics is about.

---

### Assessment Reminder

**Quizzes and the recitation carry no weight** and are still required. **Quiz 5 is at the start of Monday's lecture and covers Week 4.**

> **Recitation 5 sits the day after Midterm 1 and the day before PS 5 is due.** It is built for that
> — a short drill and a long clinic. **Bring your PS 5 attempt and one question from the paper you
> could not call.**

Quizzes are tracked in [[_MATH 241 Quiz Record]].

---

### Connections

**Back:** **Week 1's matrix returns for a fourth time**, and its determinant is the product of pivots $2, 3, 4$ that L02 §4 computed and never multiplied. **Week 1's L05 §3 quoted the adjugate formula and deferred it**; L17 §4 delivers. **Week 4's L15 §6 assumed similarity invariance**; L18 §4 proves it in one line. And **Week 0's L03 §6 warned that $\det$ is the wrong diagnostic** before $\det$ existed — L18 §6 is that warning, now with the definition to back it.

**Sideways:** **CS 201's Midterm 1 is this Monday**, covering its Weeks 0–4. Nothing in this week's material bears on it. **PROG 201's Week 5 is sockets and the C10K problem** — no connection, and looking for one is wasted effort in a week with two exams in it.

**Forward:** **Week 6 is the reason this week exists.** Eigenvalues come from $\det(A - \lambda I) = 0$, a determinant with a symbol in it, and **L17's cofactors are the only tool that computes it** — elimination would divide by expressions that may vanish. **Week 6 also completes Week 4's invariants**: the trace turns out to be the sum of the eigenvalues and the determinant their product, so the two quantities L15 §6 could only *verify* acquire meanings. **Week 7's diagonalisation is L15 §7's first row**, and $\det = 0$ is how you find the eigenvalues that make it possible. **Week 8's orthogonal matrices are PS 5 Q5(d)'s** — $\det Q = \pm 1$, rigid motions, the ones with condition number 1.

---

*MATH 241 · Week 5 · © CSE Department*
