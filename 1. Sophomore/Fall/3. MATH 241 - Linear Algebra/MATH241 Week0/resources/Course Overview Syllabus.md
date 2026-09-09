# MATH 241 · Linear Algebra
## Course Overview & Week-by-Week Road-map
### Year 2 · Fall · 4 credits (3 lecture + 1 recitation)

---

## The Course

**Linear algebra is what you get when you insist that a function be boring.**

A linear map is one that respects addition and scaling and does nothing else — no squaring, no thresholds, no special cases. That is a severe restriction, and the payoff for accepting it is the whole subject: **every linear map on a finite-dimensional space is a matrix, every matrix is a linear map, and the map can be understood completely.** Nothing else in mathematics is understood completely.

The reason a computer science degree spends a term on it is that the restriction is not as severe as it sounds. A neural network is linear maps with a scalar nonlinearity wedged between them. A rotation is a matrix. A JPEG is a change of basis followed by throwing away the small coordinates. PageRank is an eigenvector. Least squares is a projection. Every one of those is a sentence you will be able to *cash out* by Week 12.

By the end you will be able to answer, with a construction rather than a definition: **when does $Ax = b$ have a solution, and how many; what does $A$ do to space; which directions does it leave alone; and what is the best you can do when no exact answer exists.**

**Prerequisites:** MATH 141 (Calculus I). The calculus is used lightly — you need to be comfortable with functions, with proof by contradiction, and with the idea that a definition is a contract. **MATH 151's proof habits are more use here than MATH 141's integrals.**

---

## Two Habits This Course Is Built Around

**1. Every theorem is an algorithm, and the algorithm is the proof.**

"$A$ is invertible if and only if elimination produces $n$ pivots" is not a fact to memorise. It is a *procedure* — run elimination, count the pivots — and the procedure is where the proof lives. Where a result in these notes can be turned into something you could implement, it is stated that way, because a definition you can run is a definition you cannot half-remember.

> **The corollary, which costs people marks:** if you cannot say what the algorithm would *do* to a
> particular matrix, you have not understood the theorem, however fluently you can recite it. Every
> problem set has at least one question that is the theorem with the numbers filled in.

**2. Exact arithmetic and floating-point arithmetic are two different subjects, and this course does both.**

By hand, elimination on a matrix of integers is exact and the answer is a fraction. On a machine, the same algorithm on the same matrix can return **zero where the answer is one**, with no error, no warning and no exception — and Week 0's L03 shows exactly that, in four lines of Python. Strang's theory is the first subject. Which of its steps survive contact with a `double` is the second.

> **Every number in these notes was computed, and the program that computed it ships with the
> notes.** `resources/elimination.py` in Week 0 and `resources/matrices.py` in Week 1 reproduce
> every figure quoted in the lectures. Where a result is exact it was computed in `Fraction`; where
> it is floating point it was computed in `float` and the machine is named. **Timings are from the
> department reference machine** — Intel i5-8250U, Ubuntu 24.04.4, CPython 3.14 — and yours will
> differ in magnitude and must not differ in shape.

---

## Assessment

| Component | Weight | Rule |
|---|---|---|
| **Problem Sets** | **35%** | PS 0–12, released Wednesday, due the following Friday 17:00. **Lowest 1 dropped.** |
| **Midterm 1** *(Week 6)* | **20%** | 75 minutes, covering **Weeks 0–5**. One handwritten sheet, one side. |
| **Midterm 2** *(Week 10)* | **20%** | 75 minutes, covering **Weeks 6–9**. Same format. |
| **Final Exam** | **25%** | 150 minutes, comprehensive. Two handwritten pages. |
| **Total** | **100%** | |

> **The curriculum docx states no weights for MATH 241.** It gives the course's credits,
> prerequisites, textbooks and thirteen weekly topics, and stops. The split above is
> [[Year2 - Sophomore/MASTER TIMETABLE|MASTER TIMETABLE]]'s — *Problem Sets 35%, Midterms 40%,
> Final 25%* — which is the only other complete statement of 100% for this course, and it is adopted
> for the same reason ECE 110 adopted it in Year 1. Recorded as a deviation below and in
> [[MATH 241]].

**Quizzes and recitation carry no weight.** The three weighted components already reach 100%, and no percentage has been invented to fill a gap that does not exist. This is the Year 2 rule in every course.

**They are still required.** Recitation attendance is enforced by the rule in [[Year2 - Sophomore/COURSE POLICIES|COURSE POLICIES]], not by a mark.

**Quizzes** run ten minutes at the start of **Monday's** lecture — this course's first lecture of the week — in **Weeks 1–11**. **Quiz *N* covers Week *N−1*.** The answer key is printed in the paper, below the questions; you mark it yourself before leaving.

Both are recorded in [[_MATH 241 Quiz Record]].

---

## Schedule

| | When | Where |
|---|---|---|
| **Lectures** | Monday, Tuesday, Friday 11:00–11:50 | SSB 110 |
| **Recitation** | Thursday 15:00–15:50 *(mandatory)* | SSB 108 |
| **Office hours** | Monday 13:00–15:00, Thursday 10:00–11:00 | SSB 310 |

**Instructor:** Prof. Ruth Abara · r.abara@ist.edu · SSB 310

> **This course has a recitation, not a laboratory**, and the difference is not cosmetic. There is
> no machine to sit at and nothing to hand in. It is fifty minutes of board work on the problem set
> you are in the middle of, and **it is worth nothing at all unless you arrive with a specific
> question**. Turning up to watch someone else's question answered is the least efficient hour in
> the timetable.

### The recitation runs a week behind the lectures, because Thursday comes before Friday

**Recitation *N* covers Week *N* and is sat on the Thursday of Week *N+1*.**

This is forced, not chosen. The lectures are Monday, Tuesday and **Friday**; the recitation is Thursday, which falls *before* the third of them. A recitation sat on the Thursday of Week *N* would be missing that week's last lecture.

The lag also puts it where it is most useful: **PS *N* is released on the Wednesday of Week *N* and due at 17:00 on the Friday of Week *N+1*, so Recitation *N* lands on the afternoon before its deadline**, with all of the material behind it and the problem set in your hand.

| Recitation | Covers | Sat on |
|---|---|---|
| **Rec 0** | Week 0 | **Thursday of Week 1** — the day before PS 0 is due |
| Rec 1 | Week 1 | Thursday of Week 2 |
| Rec *N* | Week *N* | Thursday of Week *N+1* |
| Rec 11 | Week 11 | Thursday of Week 12 |
| **Rec 12** | Week 12 | Thursday of the completion period — **final review** |

**There is no recitation session in Week 0.** Its two Thursdays both fall before the week's teaching is done, and there is no problem set to work through yet.

> **CS 201's and PROG 201's labs lag too; CS 211's does not.** Three of your four courses this term
> put session *N* in week *N+1* and the fourth does not, because CS 211's lab is a Friday and has
> all of its week's teaching behind it. **Read each course's own header rather than carrying a habit
> between them.** Every recitation file in this course states its own sitting week.

**Quizzes do not lag.** Quiz *N* is sat at the start of **Monday's lecture in Week *N*** and covers **Week *N−1***.

---

## Textbooks

**Strang, G. — *Introduction to Linear Algebra*, 5th ed. (Wellesley-Cambridge, 2016).**
*Primary text. Strang's instinct is always to show you the picture before the proof, which is the right order for this material, and his MIT lectures (18.06 on OCW, free) are the same course delivered aloud. **Read the book and watch the lecture for the same section** — they are not redundant; he says different things.*

**Axler, S. — *Linear Algebra Done Right*, 3rd ed. (Springer, 2015).**
*Secondary, and a genuinely different book — it develops the whole theory without determinants until the final chapter, on the grounds that determinants obscure what eigenvalues are. Read it when a Strang result feels like a computation you cannot see the reason for. Weeks 5–7 are where the two books diverge most usefully.*

**Goodfellow, I., Bengio, Y. & Courville, A. — *Deep Learning* (MIT Press, 2016), Chapter 2.**
*Free at deeplearningbook.org. Twenty pages that state exactly the linear algebra a machine learning course will assume you have, in machine learning's notation rather than a mathematician's. Worth reading in Week 0 to see where this is all going, and again in Week 12 to see that you got there.*

**A note on notation.** Strang writes vectors as columns and means it; Axler works with abstract vector spaces and gets to matrices late. This course follows Strang. **When the two books disagree about what a symbol means, these notes say so** rather than picking one silently.

---

## Week by Week

| Week | Topic | The question it answers |
|---|---|---|
| **0** | Linear Systems; Gaussian Elimination | What does it mean to solve $Ax = b$, and what does the algorithm actually do? |
| **1** | Matrices: Operations, Transpose, Inverse | Why is matrix multiplication defined *that* way? |
| **2** | Vector Spaces and Subspaces; Null Space, Column Space | Which $b$ are reachable, and how many $x$ reach them? |
| **3** | Linear Independence, Basis, Dimension | How many vectors do you need, and how do you know? |
| **4** | Linear Transformations and Their Matrices | The matrix depends on the basis. The map does not. |
| **5** | Determinants: Properties, Cofactor Expansion, Cramer's Rule | What one number can tell you about a matrix, and what it cannot |
| **6** | Eigenvalues and Eigenvectors · **MIDTERM 1** | Which directions does $A$ leave alone? |
| **7** | Diagonalization; Complex Eigenvalues | When is a matrix just a scaling in disguise? |
| **8** | Orthogonality; Projections; Gram–Schmidt | What is the closest point in a subspace? |
| **9** | Least Squares; QR Decomposition | What do you do when $Ax = b$ has no solution? |
| **10** | Symmetric Matrices; Spectral Theorem; Quadratic Forms · **MIDTERM 2** | Why is $A^\mathsf{T}A$ the matrix everything reduces to? |
| **11** | Singular Value Decomposition | Every matrix, factored — rotation, stretch, rotation |
| **12** | Applications: PCA, PageRank, Regression, Fourier · **Final review** | All four are the same theorem |

**The spine of the course is one question asked five times.** *When can I replace $A$ by something simpler?* Week 1 answers $A = LU$; Week 7 answers $A = S\Lambda S^{-1}$; Week 9 answers $A = QR$; Week 10 answers $A = Q\Lambda Q^\mathsf{T}$; Week 11 answers $A = U\Sigma V^\mathsf{T}$ and needs no hypotheses at all. If you can say what each factorisation costs, when it exists, and what it is *for*, you have the course.

---

## What This Course Feeds

**Immediately:** **CS 201 is running alongside, and Week 0's L03 is CS 201's Week 1.** The reason elimination without pivoting returns zero instead of one is that floating-point subtraction of nearby numbers is catastrophic, which is exactly the non-associativity CS 201 measures next week. The two courses meet at the `double`, from opposite sides.

**Next term:** **MATH 251 (Probability & Statistics)** is built on this: a covariance matrix is symmetric positive semidefinite, and Week 10 is what that phrase means. **ECE 211 (Signals and Systems)** is Week 12's Fourier item taken seriously — a transform is a change of basis.

**Later:** CS 331 (Machine Learning) assumes every week of this course and re-derives none of it. CS 321 (Graphics) is Weeks 4 and 8 in three dimensions. CS 351 (Numerical Methods) is Week 0's L03 for a whole term. **The single most-used result in all three is the SVD**, which is Week 11.

---

## Deviations From the Curriculum

Recorded here so a reader meets them without needing `5. Build Records/`:

| What | Why |
|---|---|
| **The curriculum states no assessment weights for this course** | Its MATH 241 entry gives credits, prerequisites, textbooks, relevance and thirteen weekly topics, and stops — unlike CS 201, PROG 201 and CS 211, whose weights it states in full. [[Year2 - Sophomore/MASTER TIMETABLE\|MASTER TIMETABLE]]'s *PS 35 / Midterms 40 / Final 25* is the only other complete statement and is adopted, following the ECE 110 precedent from Year 1. Nothing about the topics or their order is affected. |
| **Week 0 has no Monday lecture** | Week 0 runs Aug 27 – Sep 5, and the Monday inside it is **Labor Day**, on which [[ACADEMIC CALENDAR]] holds no classes. This course's slots are Mon/Tue/Fri, so Week 0's three lectures are sat on **Friday, Tuesday and Friday** instead. All three happen; only their days move, and each lecture file states its own. |
| **The recitation lags a full week** | Thursday falls before this course's Friday lecture, so a recitation cannot cover the week it is sat in. Recitation *N* covers Week *N* and is sat on the Thursday of Week *N+1* — which is also the day before PS *N* is due. There is no recitation in Week 0. |
| **Quiz 6 is sat on a Tuesday, not a Monday** | The Monday of Week 6 is Fall Break. Quiz 6 moves to the start of that week's first lecture, which is the Tuesday. It is the only quiz in the term that is not a Monday, and the Week 6 paper says so in its header. |
| **The registry lists no TA for this course** | [[Year2 - Sophomore/OFFICE HOURS\|OFFICE HOURS]] gives a TA for CS 201, CS 211 and PROG 201 and none for MATH 241, while [[Year2 - Sophomore/FALL SCHEDULE\|FALL SCHEDULE]] describes the recitation as TA-led. Until one is assigned the recitation is run by Prof. Abara, and the Engineering Help Desk in BH 120 covers drop-in help. Recorded in [[MATH 241 Scheduling Notes]] §4 as an omission rather than a decision. |
| **Lectures quote a floating-point result before CS 201 has taught floating point** | L03 §4 shows elimination returning `0.0` for an answer of `1`, which is a consequence of IEEE 754 cancellation — CS 201's Week 1, one week after this. The lecture states the mechanism in full rather than deferring, and marks the forward reference. Nothing in it depends on CS 201 having happened. |

---

*MATH 241 · Year 2 Fall · © CSE Department*
