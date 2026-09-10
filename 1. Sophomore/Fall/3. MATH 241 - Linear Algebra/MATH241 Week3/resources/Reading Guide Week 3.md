# MATH 241 · Reading Guide · Week 3
## Strang §3.5–§3.6, and the diagram to redraw from memory

---

**Two sections, and the second is four pages long and is the most important four pages in the book.** §3.6 assembles everything since Week 0 into one picture, and Strang draws that picture roughly forty more times before the end. **Learn to redraw it now** — this week's habit, below.

| Chapter | Read? | Why |
|---|---|---|
| **3.5 Independence, Basis and Dimension** | **All of it** | L10 and L11 entire |
| **3.6 Dimensions of the Four Subspaces** | **All of it, twice** | L12. Short, and it is the summary of the whole first half |
| 3.4 (rest of it) | **Finish it** | You read the first half last week; the rank discussion at the end is L12 §4 |
| 4.1 Orthogonality of the Four Subspaces | **Skim** | Week 8, and reading two pages now makes L12 §7 land properly |
| **Axler 2.A–2.C** | **Read 2.A and 2.C** | Span, independence, basis and dimension without a matrix anywhere. **The better treatment of §4's theorem** |
| **Goodfellow §2.4–2.5** | Read | Span and rank in ML notation, three pages |

---

## §3.5 — the questions to hold

1. Strang defines independence for the **columns of a matrix** and then for an abstract list. **Check that the two agree** — and notice that his matrix version is L10 §2's, $\mathbf{N}(A) = \{0\}$.
2. He proves that $n$ vectors in $\mathbb{R}^m$ with $n > m$ are dependent. **Reconstruct the argument yourself before reading it.** It is three lines and it is a pivot count.
3. **Find his statement that every basis has the same size.** Compare his proof with L11 §4's. *(His is an exchange argument; ours routes through $W = V\!m\,C$ and L10 §4. Same content, and one of them will suit you better — know which.)*
4. "Dimension" is defined only *after* that theorem. **Why can it not be defined before?** Answer in one sentence; it is the entire reason the theorem is stated.
5. He gives bases for $\mathbf{C}(A)$ and $\mathbf{N}(A)$. **You computed both last week.** What did Week 2 not know that Week 3 does? *(That they are the right size, and that the size does not depend on how you eliminated.)*
6. Find his remark that a space has many bases but one dimension. **List three different bases for $\mathbb{R}^2$** and confirm.
7. **§3.5 near the end: the "$k$ vectors in a $k$-dimensional space" shortcut** — L11 §8. Find it, and find the sentence that says the count alone is not enough.

---

## §3.6 — read this twice, and draw the picture

8. **The four subspaces and their dimensions.** Write out $r$, $n-r$, $r$, $m-r$ and, for each, which of $\mathbb{R}^m$ and $\mathbb{R}^n$ it sits in. **Get this cold; PS 3 Q3 is exactly it.**
9. Strang's basis for the row space is **the nonzero rows of $R$**; his basis for the column space is **the pivot columns of $A$**. **Find where he explains the asymmetry.** If you cannot state the reason in one sentence, reread L12 §3 — it is the most examinable idea of the week.
10. **Row rank $=$ column rank.** He proves it much as L12 §4 does. **Does his proof explain *why*, or only establish *that*?** Say which, and hold the question until Week 11.
11. Find his big figure — two boxes on the left, two on the right, arrows across. **Copy it onto one page by hand, with the dimensions labelled.** Then close the book and draw it again.
12. He says the left null space is "the least important" of the four. **These notes disagree** — L12 §5 makes it the list of solvability conditions on $b$. Read both claims and decide. *(He revises his own view in Chapter 4; the disagreement is really about when it becomes useful.)*
13. What does $\mathbf{N}(A^\mathsf{T}) = \{0\}$ mean about $A$, in plain words? *(Every $b$ is reachable. Full row rank.)*

---

## §4.1, two pages only

14. Strang states that $\mathbf{N}(A) \perp \mathbf{C}(A^\mathsf{T})$ and that they are **orthogonal complements** — a stronger claim than perpendicularity. **What does the extra word buy?** *(That together they fill $\mathbb{R}^n$, which perpendicularity alone does not give — REC 3 §2(d) is exactly this trap.)*
15. Stop when he introduces projections. That is Week 8 and it needs the machinery.

---

## Where Axler Earns His Place This Week

**This is the week to actually read him.** Strang proves the dimension theorem with matrices; Axler proves it with no matrices at all, and Chapter 2 is the best-written thing in either book.

| Axler | Why bother |
|---|---|
| **2.A** span and independence | The *Linear Dependence Lemma*, which is L10 §3 sharpened, and it is the engine of everything after |
| **2.B** bases | Every spanning list contains a basis; every independent list extends to one. **Neither is in Strang** and both are used silently all term |
| **2.C** dimension | $\dim(U+W) = \dim U + \dim W - \dim(U\cap W)$ — PS 3 Q2(b) is an instance, and Week 8 needs it |

**Read 2.A and 2.C even if you skip 2.B.** Twenty-five pages, no matrices, and Week 4 will be substantially easier.

---

## The Habit for This Week

**Draw the four-subspace diagram from memory, once a day, until Friday.**

Two boxes in $\mathbb{R}^n$ — row space $(r)$ above null space $(n-r)$. Two boxes in $\mathbb{R}^m$ — column space $(r)$ above left null space $(m-r)$. An arrow carrying the row space onto the column space; an arrow crushing the null space to $0$.

It takes ninety seconds. **By Friday you should be able to produce it without hesitating over which dimension goes where**, because from Week 8 onwards it is the frame every remaining topic is hung on: projections are onto the top-right box, least squares deals with the bottom-right one, and the SVD gives all four an orthonormal basis at once.

**If you can draw it, you have Week 3. If you cannot, no amount of computed bases will substitute.**

---

## Where to Go Deeper

| Source | Topic |
|---|---|
| **Strang, MIT 18.06, Lectures 9–10** | Independence/basis/dimension, then the four subspaces. **Lecture 10 is the diagram** |
| **Strang, *The Fundamental Theorem of Linear Algebra*, Amer. Math. Monthly 100 (1993)** | Six pages, freely available, on this one picture. Readable now |
| **Axler Ch. 2** | The whole thing without coordinates |
| **Week 11** | Where row rank $=$ column rank finally gets an explanation rather than a proof |

---

*MATH 241 · Week 3 · Reading Guide · © CSE Department*
