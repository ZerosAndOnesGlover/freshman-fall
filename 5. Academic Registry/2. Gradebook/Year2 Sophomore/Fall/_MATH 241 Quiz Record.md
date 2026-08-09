# MATH 241 · Quiz Record
## Not part of the course grade

> **This file is deliberately outside the gradebook's weighted components.** MATH 241's
> quizzes carry **no weight** — Problem Sets 35, Midterms 40 and Final 25 already sum to 100% without them,
> and `MATH 241.md` says so.
>
> The leading underscore in the filename keeps this file out of `tools/gpa.py`'s course scan. Do not
> rename it without checking `collect()` in that script.

---

## Why This Is a Separate File

The gradebook parser reads a component's items from its heading until the **next `##` heading
containing a percentage**. An unweighted subheading has none, so its rows are silently absorbed into
the component above it. The failure was found in CS 102 in Year 1, where eleven quiz rows quietly
attached themselves to Project 2. Year 2 avoids it the same way Year 1 settled on: the unweighted
work lives here, and the gradebook has no table for it at all.

**The `Out of` column reads `—`, not a number.** That is load-bearing. `tools/make_answer_sheets.py`
reads it, and a non-numeric entry is what makes a sheet say `Marks: ___ / —` rather than inventing a
total the paper never claimed. Writing `0` would mean the same thing to a reader and the wrong thing
to the tool.

Use the **Done** column as a tick. The point of the record is that you can see, in one place, which
weeks you actually did the work.

---


*MATH 241 holds a Thursday recitation rather than a laboratory.*

---

## Quizzes

**Ten minutes at the start of the course's first lecture of the week, Weeks 1–11.** Closed book. Not marked — the answer key is printed in the paper, below the questions.

**Quiz *N* is sat in Week *N* and covers Week *N−1*.** Year 2 numbers its quizzes after the week they are sat in. *(Year 1 was not consistent about this: CS 102 and MATH 142 used the same rule, but ECE 110 numbered its quizzes after the material instead. Check the course before assuming.)*

| Quiz | Sat in | Covers | Topic | Out of | Done |
|---|---|---|---|---|---|
| Quiz 1 | Week 1 | Week 0 | Linear systems; Gaussian elimination | — | |
| Quiz 2 | Week 2 | Week 1 | Matrix operations, transpose, inverse | — | |
| Quiz 3 | Week 3 | Week 2 | Vector spaces and subspaces; null space, column space | — | |
| Quiz 4 | Week 4 | Week 3 | Linear independence, basis, dimension | — | |
| Quiz 5 | Week 5 | Week 4 | Linear transformations and their matrices | — | |
| Quiz 6 | Week 6 | Week 5 | Determinants; cofactor expansion; Cramer's rule | — | |
| Quiz 7 | Week 7 | Week 6 | Eigenvalues, eigenvectors, the characteristic polynomial | — | |
| Quiz 8 | Week 8 | Week 7 | Diagonalization; complex eigenvalues | — | |
| Quiz 9 | Week 9 | Week 8 | Orthogonality; projections; Gram-Schmidt | — | |
| Quiz 10 | Week 10 | Week 9 | Least squares; QR decomposition | — | |
| Quiz 11 | Week 11 | Week 10 | Symmetric matrices; the spectral theorem; quadratic forms | — | |

*There is no quiz covering Week 11 or Week 12 — those are examined only on the final.*

---

## Why Unmarked Work Is Worth Doing

The feedback loop that matters here is the one that closes in the next five minutes, not the one that closes when a grade comes back three weeks later. A quiz you mark yourself against the key in the same sitting tells you what has not landed while there is still a term left to fix it. Marking it would add a number and subtract nothing from the misunderstanding.

---

*MATH 241 · Quiz Record · Year 2 Fall*
