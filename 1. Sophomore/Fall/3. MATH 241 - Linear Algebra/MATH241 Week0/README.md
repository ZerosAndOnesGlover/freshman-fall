# MATH 241 · Linear Algebra
## Week 0: Linear Systems and Gaussian Elimination

**Credits:** 4 (3 lecture + 1 recitation) · **Prerequisites:** MATH 141
**Assessment for this course (overall):** Problem Sets 35%, Midterms 40%, Final 25%
**This week's deliverable:** PS 0, due **Friday of Week 1**. **No quiz** — Quiz 1, in Week 1, covers this week. **No recitation** — Recitation 0 covers this week and is sat on the **Thursday of Week 1**.

> **Week 0 is ten days long**, running Aug 27 to Sep 5. It absorbs orientation, add/drop and Labor
> Day, and Week 1 — when graded work begins — opens Sep 8.
>
> **The Monday inside it is Labor Day**, and this course lectures on Mondays. So Week 0's three
> lectures are sat on **Friday, Tuesday and Friday**. You get all three; only the days move. From
> Week 1 the pattern is the ordinary Monday / Tuesday / Friday.

---

### Why This Week Exists

Because you have solved simultaneous equations since school, and you have never once been told **what to do when it does not work.**

Two equations in two unknowns is a puzzle. Two hundred equations in two hundred unknowns is a *procedure*, and the procedure has to answer three questions the puzzle never raises: does a solution exist, is it unique, and — the one nobody asks until it bites — **is the number my computer just returned the answer, or is it noise?**

This week is the procedure. **Gaussian elimination is the most-executed numerical algorithm in the world**, it is two nested loops, and by Friday you will know its cost to within a constant, the exact circumstances under which it silently returns a wrong answer, and the one-line fix that every production solver applies unconditionally.

It also installs the habit the whole course runs on: **there are two pictures of every linear system, and the one you were taught at school is the one that stops working first.** L01 replaces it.

---

### Learning Objectives

By the end of Week 0, you should be able to:

1. State what makes an equation linear, and derive additivity and homogeneity from the definition.
2. Draw the **row picture** and the **column picture** of a system, and say what a solution is in each — in two sentences that are not paraphrases.
3. **Read $Ax$ as a linear combination of the columns of $A$**, by default and without translating.
4. Prove that a linear system has no solution, exactly one, or infinitely many, and never any other number.
5. Perform elimination by hand with the multipliers written down, and check the answer by substitution into the original system.
6. Justify each of the three row operations from its reversibility, and say why R3 excludes $c = 0$.
7. **Distinguish a zero pivot that a row exchange fixes from one that proves the matrix singular**, and state the one-line test that separates them.
8. Read off, from an echelon form, whether a given $b$ is reachable and how many free unknowns there are.
9. **Derive the $n^3/3$ operation count**, and use it to say which problems elimination is the wrong tool for.
10. **Say why elimination in floating point can return $0$ for an answer of $1$**, naming the step and the quantity lost.
11. State the partial-pivoting rule, say what bound it guarantees on the multipliers, and say what it does *not* guarantee.
12. **Explain why $\det A$ is the wrong diagnostic for a difficult solve and $\operatorname{cond}(A)$ is the right one**, with an example of each failure.

---

### This Week's Materials

| File | Purpose |
| --- | --- |
| [[L01 Linear Systems the Row Picture and the Column Picture]] | Linearity in two properties; planes against combinations; **$Ax$ as a combination of columns**; three outcomes and the two-line proof; dependent rows and columns arriving together |
| [[L02 Gaussian Elimination Pivots and Echelon Form]] | Back substitution first; three reversible operations; the augmented matrix; the running example worked in full — **pivots $2,3,4$, multipliers $2,-1,3$**; the two kinds of zero pivot; echelon and reduced echelon form |
| [[L03 What Elimination Costs and When It Lies]] | $n^3/3$ derived; **PageRank would take ten million years**; exact arithmetic needing **299-digit pivots**; **`0.0` returned for an answer of `1`**, traced to the bit; partial pivoting; **$\operatorname{cond}(H_{12}) = 4\times10^{16}$ and two correct digits** |
| [[REC 0 Elimination at the Board]] | Board work on the mid-elimination zero and the column picture. **Thursday of Week 1**, the day before PS 0 is due |
| [[MATH241 Week0/assignments/Problem Set 0\|Problem Set 0]] | Five questions, 100 points, due **Friday of Week 1** |
| [[MATH241 Week0/resources/Course Overview Syllabus\|Course Overview Syllabus]] | **Read this in full in Week 0** — assessment, the recitation lag, Labor Day, deviations |
| [[MATH241 Week0/resources/Reading Guide Week 0\|Reading Guide Week 0]] | Strang Ch. 1 and §2.1–2.3, which two sections to skim and why, and fifteen questions |
| `resources/elimination.py` | Every number in L01–L03, reproducible. Pure Python, no dependencies |
| `solutions_instructor/` | Instructor only |

---

### The One Thing to Take From This Week

**Elimination does not solve systems. It *classifies* them, and solving is what it does on the way.**

Hand it any $[\,A \mid b\,]$ and it comes back with three facts you did not have to know in advance: how many pivots $A$ has, whether *this* $b$ is reachable, and how many dimensions of solutions there are if it is. **You never have to check whether a system is solvable before solving it**, and that is not a convenience — it is the reason the algorithm scales past the size at which you could have inspected the matrix yourself.

**The corollary runs the other way and is L03's whole subject.** An algorithm that always returns something will return something when it should not. On $\;\varepsilon x_1 + x_2 = 1,\; x_1 + x_2 = 2\;$ with $\varepsilon = 10^{-17}$, L02's algorithm returns $x_1 = 0.0$ for an answer of $1$ — no exception, no warning, a plain number, $100\%$ wrong. **The classification is exact and the arithmetic is not**, and everything numerical in the rest of this course lives in that gap.

---

### Assessment Reminder

**Quizzes and the recitation carry no weight.** Problem Sets 35 + Midterms 40 + Final 25 already reach 100%, and no percentage has been invented to fill a gap that does not exist.

They are still required. **Recitation attendance is enforced** by [[Year2 - Sophomore/COURSE POLICIES|COURSE POLICIES]], and a second unexcused absence costs a letter grade. **Quiz *N* covers Week *N−1***, runs ten minutes at the start of **Monday's** lecture in Weeks 1–11, and prints its own answer key.

> **There is no recitation this week and there is no quiz.** Recitation 0 covers Week 0 and is sat
> on the **Thursday of Week 1** — the day before PS 0 is due — because this course's Thursday
> session comes before its Friday lecture. **CS 201's and PROG 201's labs lag the same way and
> CS 211's does not**; read each course's own header rather than carrying a habit between them.

Quizzes are tracked in [[_MATH 241 Quiz Record]].

---

### Connections

**Back:** **MATH 141 is barely used and MATH 151 is used constantly.** Nothing this week needs a derivative. What it needs is MATH 151's habits — reading a definition as a contract, proving an "if and only if", and being comfortable that "there are exactly three cases" is a claim requiring proof rather than a list. L01 §5 and L02 §2 are both MATH 151 exercises wearing new clothes.

**Sideways:** **CS 201 Week 1 is L03 §4 from the other side.** This week you meet a `double` losing the digits that mattered; next week CS 201 dissects the `double` and shows you why floating-point addition is not associative. The two courses are describing one object from opposite ends, and the Week 1 pairing is the closest they come all term. **PROG 201's `fork` has nothing to do with any of this**, which is worth saying so that you stop looking for a connection.

**Forward:** **Week 1 is this week's discarded arithmetic, recovered.** The three multipliers $2, -1, 3$ that L02 computed and threw away are a matrix, $A = LU$ is the statement that they always were, and keeping them turns every subsequent solve with the same $A$ from $n^3/3$ into $n^2$. **Week 2 names the objects L01 §5 stumbled over** — the set of reachable $b$ is the column space, the plane of failure is a constraint from the left null space. **Week 5's determinant is the product of these pivots**, which is why $\det$ is cheap once you have eliminated and catastrophic if you compute it from the definition. And **L03 §7's condition number is the thread through the second half of the course**: Week 8's orthogonal matrices are the ones for which it equals $1$, which is why Week 9 prefers QR and Week 11 trusts the SVD.

---

*MATH 241 · Week 0 · © CSE Department*
