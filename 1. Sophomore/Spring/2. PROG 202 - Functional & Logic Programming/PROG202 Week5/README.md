# PROG 202 · Functional & Logic Programming
## Week 5: Monads — `Maybe`, `Either`, `State`, and `IO`

**Credits:** 3 (2 lecture + 1 lab) · **Prerequisites:** PROG 102, CS 211
**Assessment for this course (overall):** Problem Sets 40%, Projects 30%, Midterm 15%, Final 15%
**This week's deliverables:** PS 5, Quiz 5 (Tuesday, covers Week 4). **Lab 4 is sat this Wednesday**; Lab 5
is sat on the Wednesday of Week 6.

> **⚠️ This is the last week the midterm covers.** The paper is **Thursday of Week 6, 18:00–19:15, Weeks
> 0–5.** Lab 5 — this week's lab — is sat the day before it, on purpose.
>
> **Required reading: Wadler, *Monads for Functional Programming* (1992).** §1–§3 before Tuesday, §4–§5
> before Thursday. On the final.

---

### Why This Week Exists

Because you have written the same plumbing three times and it is time somebody named it.

**Project 1, TODO 3.** Every arithmetic case unwraps an `Either` and rewraps it, four `case` arms deep.
**Project 1, TODO 4.** You could not use `filter`, because the predicate could fail, so you wrote the
recursion by hand. **Week 1, Lab 1.** `traverse id` over seventeen `Either`s, and you were told it was
Week 6 and asked to guess what it did.

**Three problems, one shape: do the next thing only if the previous thing worked, and pass the result
along.** The `Left e -> Left e` lines carry no information and there are more of them than there is
program.

**A monad is the name for that plumbing, and naming it deletes it.** Project 1's `Bin` case goes from nine
lines to four. Your `filterM'` turns out to be `filterM`. Lab 1's `traverse id` turns out to be `sequence` —
**measured: substituting it changes nothing about the output.**

And then `State`, which is the one that breaks the picture people arrive with: **a monad that is a function,
not a container.**

---

### Learning Objectives

By the end of Week 5, you should be able to:

1. Recognise the plumbing pattern in code you have already written.
2. **Read `(>>=) :: Monad m => m a -> (a -> m b) -> m b`** and say what each part is.
3. Write `instance Monad Maybe` and `instance Monad (Either e)` from memory, and **say why it is `Either e`**.
4. **Desugar `do` by hand**, all four rules, and say what `<-` actually is.
5. Explain the `Functor` → `Applicative` → `Monad` chain, and **write all three instances** — plus recognise
   the error you get if you write only `Monad`.
6. State the three monad laws and say which one licenses extracting a `do` block into a helper.
7. **Replace hand-written plumbing with `mapM`, `filterM`, `sequence`, `foldM`, `when`.**
8. **Write `State` from scratch**: the `newtype`, three instances, `get`, `put`, `modify`, `evalState`,
   `execState`.
9. Say why `State` is not mutation, with three things you can do that mutation cannot.
10. **Explain `IO` as `State RealWorld` with `runState` missing.**
11. **Say what `State.Strict` forces and what `modify'` forces** — they are different — and why you need both.
12. Say what `sequence` does for `[]`, and why Week 9 will need that answer.

---

### New Syntax and Symbols This Week

Full reference: [[PROG202 Week0/resources/Haskell Syntax and Symbols|Haskell Syntax and Symbols]].

| Symbol | Said out loud | Means |
|---|---|---|
| `>>=` | **"bind"** | `m a -> (a -> m b) -> m b`. The whole week |
| `>>` | **"then"** | Sequence, discarding the first result |
| `=<<` | **"reverse bind"** | `>>=` with the arguments swapped |
| `<-` (in `do`) | **"bind"** | Now precisely: **the parameter of a lambda `>>=` is about to be given** |
| `pure` / `return` | — | `a -> m a`. `return` defaults to `pure` and is kept for history |
| `$` in `State $ \s -> …` | **"apply"** | Week 2's bracket-deleter, used constantly this week |
| `{-# LANGUAGE LambdaCase #-}` | — | `\case` for a function that is one `case` on its last argument |

**Functions and types new this week:** `Monad` · `Applicative` *(named; Week 6 uses it)* · `mapM` ·
`mapM_` · `filterM` · `foldM` · `sequence` · `sequence_` · `when` · `unless` · `replicateM` · `void` ·
`State` · `get` · `put` · `modify` · **`modify'`** · `gets` · `evalState` · `execState` · `runState` ·
`Control.Monad.State.Strict`.

> **`modify'` has a prime for the same reason `foldl'` does**, and it is the same trap: the unprimed one is
> in scope, looks right, and is never what you want. **Import `Control.Monad.State.Strict` and use
> `modify'`.**

---

### This Week's Materials

| File | Purpose |
| --- | --- |
| [[L11 Monads The Pattern You Have Already Written]] | The plumbing in your own Project 1; `>>=` for `Maybe` and `Either e`; **`do` desugared**; the three-class chain and the error you get without it; the laws; **`filterM` is your `filterM'`**; what a monad is *not* |
| [[L12 The State Monad and What IO Really Is]] | **`State` as a function, not a container**; `>>=` as threading; why it is not mutation; **`IO` as `State RealWorld` with `runState` missing**; **the four-way strictness measurement** |
| [[LAB 5 An Interpreter in the State Monad]] | An interpreter carrying a step counter and a warning log with neither as an argument, then **the same thing written by hand to see what the monad prevents**. **Wednesday of Week 6** |
| `lab/Mini.hs`, `Tests.hs`, `Main.hs`, `Bench.hs`, `Makefile` | Five TODOs, fourteen cases whose **step counts are the specification**, and a benchmark |
| [[PROG202 Week5/assignments/Problem Set 5\|Problem Set 5]] | Fifteen parts, 100 points, due **Friday of Week 6** — the day after the midterm |
| [[PROG202 Week5/assignments/QUIZ 5 Week 5 Tuesday\|QUIZ 5]] | Ten minutes, Tuesday, covers **Week 4** |
| [[PROG202 Week5/resources/Reading Guide Week 5\|Reading Guide Week 5]] | **Wadler, and which sections are which lecture** — read §2 with `Eval.hs` open |
| `resources/state.hs` | The four-way measurement |
| `resources/oldmonad.hs`, `newmonad.hs` | The *Real World Haskell* instance that does not compile, and the one that does |
| `solutions_instructor/` | Instructor only — includes `OwnState.hs`, the hand-written `State` |

---

### The One Thing to Take From This Week

**`State` is a fold with the accumulator hidden.**

That sentence does two jobs. It tells you what `State` *is* — `s -> (a, s)`, a function threading a value
forward exactly as `foldl` threads its accumulator, with `>>=` doing the threading you would otherwise write
by hand. And it tells you why it is **not** mutation: the same computation run twice from the same start
gives the same answer, it can be run from any start, and every intermediate state is a value you could have
kept.

**The reason it matters is not brevity.** Lab 5 has you write one case of the interpreter *without* the
monad, and the finding is this: if you thread the wrong state into the second recursive call — `t1` where
`t2` was meant — **nothing catches it.** The types are identical, because every state has the same type. The
monad's value is that **there is no `t2` to confuse with `t1`, because there is no `t2`.**

And then the week's measurement, which is Week 3's question for the third time. Counting to three million:

| | residency |
|---|---:|
| `State.Lazy` + `modify` | 308 MB |
| `State.Lazy` + `modify'` | **398 MB** — *worse, by being more strict* |
| `State.Strict` + `modify` | 167 MB |
| **`State.Strict` + `modify'`** | **44 KB** |

**`State.Strict` forces the pair; `modify'` forces the value. They are orthogonal and you need both.**
Week 3 said `foldl'` is strict in the constructor and not the fields (727 MB); Week 3 said
`Data.Map.Strict` is strict in the values and `Lazy` is not (107 MB); **now this. When a name says
"strict", ask *strict in what*.**

---

### Assessment Reminder

**Labs and quizzes carry no weight.** A second unexcused lab absence costs a letter grade. **Quiz *N*
covers Week *N−1***, Tuesday, ten minutes.

> **Lab 4 is sat this Wednesday.** Lab 5 — this week's — is sat the **Wednesday of Week 6**, and **the
> midterm is the Thursday of Week 6.** That is one day apart and it is deliberate: Lab 5 §4 is the paper's
> most likely question.
>
> **Project 1 is due Friday of Week 7.** Phase 2 is this week's material. **Spring Break is after the
> deadline.**

Both are tracked in [[_PROG 202 Lab and Quiz Record]].

---

### Connections

**Back:** **this week is Weeks 1–4 collected.** Project 1's `Either` plumbing is L11 §1; Lab 1's
`traverse id` is `sequence`; Week 4's class hierarchy is why `pure` is available on every monad; and Week
3's "strict in what?" is L12 §4 for the third time. **`State` is Week 2's `foldl` with the accumulator
hidden**, and saying so out loud is the cheapest way to make it one idea instead of two.

**Sideways:** **CS 202's process state** is the thing `State RealWorld` is a model of, and its
`fork`-and-thread-a-context is the same shape by hand.

**Forward:** **Week 6 is `Applicative` and monad transformers** — how to have `State` *and* `Either` at
once, which is the type Project 1's `eval` would need if it counted steps. It also finally explains
`traverse`, which you have been asked to guess at twice. **Week 7's STM is the monad for state several
threads share**, which is the case `State` explicitly does not handle. And **Week 9's Prolog is the list
monad promoted to being the only control structure** — `sequence [[1,2],[3,4]]` being the Cartesian product
is that week's mechanism, seen early.

---

*PROG 202 · Week 5 · © CSE Department*
