# PROG 202 · Lab and Quiz Record
## Not part of the course grade

> **This file is deliberately outside the gradebook's weighted components.** PROG 202's
> labs and quizzes carry **no weight** — Problem Sets 40, Projects 30, Midterm 15 and Final 15 already sum to 100% without them,
> and `PROG 202.md` says so.
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


## Labs

**Thirteen labs, Weeks 0–12, in the scheduled session.** Mandatory. The TA checks the work off during or just after the session; nothing is marked out of anything.

> **Attendance is the enforcement.** `COURSE POLICIES.md` reduces the final course grade > by one letter after a second unexcused lab absence. That rule, not a mark, is why the > lab is not optional.

| Lab | Week | Topic | Out of | Done |
|---|---|---|---|---|
| Lab 0 | Week 0 | GHCi, the REPL, and the shape of a Haskell program | — | |
| Lab 1 | Week 1 | Algebraic data types and exhaustive pattern matching | — | |
| Lab 2 | Week 2 | Refactor an imperative loop into folds | — | |
| Lab 3 | Week 3 | Watch laziness: thunks, space leaks, and seq | — | |
| Lab 4 | Week 4 | Implement a type class and its instances | — | |
| Lab 5 | Week 5 | Build a small interpreter in the State monad | — | |
| Lab 6 | Week 6 | Stack monad transformers over IO | — | |
| Lab 7 | Week 7 | STM: a concurrent bank account with no locks | — | |
| Lab 8 | Week 8 | SWI-Prolog: a family-tree knowledge base | — | |
| Lab 9 | Week 9 | Trace unification and backtracking by hand, then in the tracer | — | |
| Lab 10 | Week 10 | A constraint solver for a scheduling problem | — | |
| Lab 11 | Week 11 | QuickCheck: find a bug in a provided library | — | |
| Lab 12 | Week 12 | Final project demo | — | |

---

## Quizzes

**Ten minutes at the start of the course's first lecture of the week, Weeks 1–11.** Closed book. Not marked — the answer key is printed in the paper, below the questions.

**Quiz *N* is sat in Week *N* and covers Week *N−1*.** Year 2 numbers its quizzes after the week they are sat in. *(Year 1 was not consistent about this: CS 102 and MATH 142 used the same rule, but ECE 110 numbered its quizzes after the material instead. Check the course before assuming.)*

| Quiz | Sat in | Covers | Topic | Out of | Done |
|---|---|---|---|---|---|
| Quiz 1 | Week 1 | Week 0 | Haskell and GHCi; purity and referential transparency | — | |
| Quiz 2 | Week 2 | Week 1 | Algebraic data types, pattern matching, type inference | — | |
| Quiz 3 | Week 3 | Week 2 | Higher-order functions: map, filter, foldr, foldl | — | |
| Quiz 4 | Week 4 | Week 3 | Lazy evaluation; infinite lists; thunks | — | |
| Quiz 5 | Week 5 | Week 4 | Type classes: Eq, Ord, Show, Num, Functor, Foldable | — | |
| Quiz 6 | Week 6 | Week 5 | Monads: Maybe, IO, State | — | |
| Quiz 7 | Week 7 | Week 6 | Applicative functors; monad transformers | — | |
| Quiz 8 | Week 8 | Week 7 | Concurrency in Haskell: STM, lightweight threads, par and seq | — | |
| Quiz 9 | Week 9 | Week 8 | Prolog: facts, rules, queries | — | |
| Quiz 10 | Week 10 | Week 9 | Unification, resolution, and the execution model | — | |
| Quiz 11 | Week 11 | Week 10 | Constraint solving and natural-language parsing in Prolog | — | |

*There is no quiz covering Week 11 or Week 12 — those are examined only on the final.*

---

## Why Unmarked Work Is Worth Doing

The feedback loop that matters here is the one that closes in the next five minutes, not the one that closes when a grade comes back three weeks later. A quiz you mark yourself against the key in the same sitting tells you what has not landed while there is still a term left to fix it. Marking it would add a number and subtract nothing from the misunderstanding.

---

*PROG 202 · Lab and Quiz Record · Year 2 Spring*
