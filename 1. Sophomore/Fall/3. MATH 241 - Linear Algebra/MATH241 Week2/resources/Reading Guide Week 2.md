# MATH 241 · Reading Guide · Week 2
## Strang Chapter 3.1–3.3, and the week Axler starts to be worth reading

---

**Chapter 3 is where the book changes character.** Chapters 1 and 2 were algorithms with pictures attached; Chapter 3 is definitions, and the exercises stop being arithmetic. **The reading load drops and the thinking load rises** — do not mistake the shorter page count for a lighter week.

| Chapter | Read? | Why |
|---|---|---|
| **3.1 Spaces of Vectors** | **All of it** | L07 entire. Strang's list of what is and is not a subspace is longer than ours; do all of it |
| **3.2 The Nullspace of A** | **All of it, twice** | L08 and L09. **The most important section in the first half of the book** |
| **3.3 The Rank and the Row Reduced Form** | **All of it** | L08 §3 and §6, and the setup for Week 3 |
| 3.4 The Complete Solution to Ax = b | **Read §3.4 up to the "complete solution" summary** | L09 §6. The rest is Week 3 |
| 3.5 Independence, Basis and Dimension | Not yet | Week 3 — but skim the first two pages on Friday evening |
| **Axler Ch. 1.C (Subspaces)** | **Read** | Eight pages, and a genuinely better treatment of sums and unions than Strang gives |
| **Goodfellow §2.4** | **Read** | Two pages, "Linear Dependence and Span", in ML notation |

---

## §3.1 — the questions to hold

1. Strang requires eight axioms; L07 §2 lists ten. **Find the discrepancy** — it is a matter of which closure conditions are counted separately — and satisfy yourself that the two definitions agree.
2. He gives $\mathbb{R}^{m\times n}$, polynomials and functions as vector spaces. **Pick the one you find least plausible and check all the axioms.** Twenty minutes, and it is the only way the abstraction becomes real.
3. **His subspace test is two conditions and ours is three.** Reconcile them. *(He folds $0 \in W$ into non-emptiness plus closure under scaling. Both are correct; ours is easier to apply and harder to misapply.)*
4. Find his list of the subspaces of $\mathbb{R}^3$. It should match L07 §4's four. **Why can there be nothing else?** You cannot prove it yet — Week 3 can — but write down what you would need.
5. He introduces $\mathbf{C}(A)$ at the *end* of §3.1, as an example of a subspace. **These notes make it the point of a whole lecture.** Read his half-page first and see whether you would have noticed its importance.

---

## §3.2 — read this twice

6. **The word "nullspace" is one word in Strang and two in most other books.** Both mean $\{x : Ax = 0\}$. Notice now so that a different textbook does not throw you.
7. He computes special solutions before he defines rank. **Do his example by hand before reading his answer**, then compare — including which columns he calls free.
8. **Find where he says the null space is unchanged by elimination.** Does he say the same about the column space? *(He does not, and L08 §4 is why. This is the single most useful thing to have straight this week.)*
9. His "special solutions" are our special solutions. He sets one free variable to 1 and the rest to 0 — **why that choice and not any other?** What would go wrong if you set two of them to 1 at once?
10. He remarks that a wide matrix ($n > m$) always has a nonzero null space. **Reconstruct the argument in one line** before reading his.

---

## §3.3

11. **Rank is defined here, and it is defined as a number of pivots.** Strang will give it three more equivalent definitions by the end of Chapter 3. Write down this one and date it; the point of Week 3 is that they all agree.
12. He introduces $R = \operatorname{rref}(A)$ and the block form $\begin{bmatrix}I & F\\ 0 & 0\end{bmatrix}$ after column permutation. **Work out what $F$ is for this week's $A$**, and check that the special solutions come out as $\begin{bmatrix}-F\\ I\end{bmatrix}$.
13. **The pivot columns of $A$ span $\mathbf{C}(A)$; the pivot columns of $R$ do not.** Find where he says this, and mark it. It is PS 2 Q2(b) and it is the commonest error on that paper.

---

## §3.4, first half only

14. His "complete solution" is $x_p + x_n$ — the same as L09 §6. **He chooses $x_p$ by setting free variables to zero, as we do.** Is that choice forced? *(No. PS 2 Q4(d).)*
15. Find his picture of the solution set as a plane not through the origin. **Draw it yourself for a $2\times3$ example** where the null space is a line.

---

## Where Axler Earns His Place This Week

Strang defines a subspace and moves on. **Axler §1.C spends eight pages on sums of subspaces** and proves things Strang does not:

| Axler | Why bother |
|---|---|
| $U + W$ is the smallest subspace containing both | L07 §6's repair, done properly |
| Direct sums, $U \oplus W$ | The case $U \cap W = \{0\}$. **This is Week 8's orthogonal decomposition**, three weeks early and with no geometry attached |
| Why $U \cup W$ is almost never a subspace | Exercise 14 in his section; it is PS 2 Q1(c) |

**Read it if Strang's §3.1 felt thin.** It is a different temperament — no matrices at all — and Week 4 will be easier for having met it.

---

## The Habit for This Week

**Before you compute anything, say which $\mathbb{R}^k$ the answer lives in.**

$\mathbf{C}(A) \subseteq \mathbb{R}^m$; $\mathbf{N}(A) \subseteq \mathbb{R}^n$. For a $3\times4$ matrix those are $\mathbb{R}^3$ and $\mathbb{R}^4$, and an answer in the wrong one is not slightly wrong — **it is an object of the wrong kind**, and no amount of correct arithmetic afterwards repairs it.

Write the two numbers at the top of the page before you start eliminating. It costs three seconds and it is the difference between the marks on PS 2 Q2 and Q3.

---

## Where to Go Deeper

| Source | Topic |
|---|---|
| **Strang, MIT 18.06, Lectures 5–7** | This week aloud. **Lecture 6 is the null space** and is the one to watch if you watch one |
| **Axler, Ch. 1.C and 2.A** | Subspaces and spans without coordinates. Week 3 and Week 4 both get easier |
| **Strang §3.5, first three pages** | Friday evening. Week 3 opens with independence and it will not be new |
| **PS 0 Q2(c)** | Your own answer, reread. **You computed a column space in Week 0** and can now say so |

---

*MATH 241 · Week 2 · Reading Guide · © CSE Department*
