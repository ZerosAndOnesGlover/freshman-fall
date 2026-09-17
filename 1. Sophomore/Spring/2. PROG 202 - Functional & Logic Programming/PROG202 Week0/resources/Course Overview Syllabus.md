# PROG 202 · Functional & Logic Programming
## Course Overview & Week-by-Week Road-map
### Year 2 · Spring · 3 credits (2 lecture + 1 lab)

---

## The Course

**PROG 202 is about the two things a program can be when it is not a list of instructions.**

Every language you have written so far — C in PROG 101 and PROG 201, whatever CS 211 had you compile — works the same way underneath: a store of mutable cells, and a sequence of commands that change them. `x = x + 1` is the whole paradigm in three tokens.

This course spends seven weeks on a language where that statement is not merely discouraged but **unwritable**, and five on a language where you do not write commands at all — you state what is true and ask a question.

**Haskell** is pure and lazy: a function is a value, a value never changes, and nothing is computed until someone needs it. **Prolog** is a logic language: you declare facts and rules, and an engine searches for the substitutions that make your query true.

By the end you should be able to answer, mechanically:

- **Why is `f x + f x` allowed to run `f` once**, and what exactly does a C compiler have to prove first?
- **What is in memory** when a Haskell program has computed nothing yet, and how do you look?
- **What is a monad**, in the sense of: what does the word have to mean for `Maybe`, `IO`, `State` and lists to all be one?
- **What does Prolog do** between your query and its first answer, and in what order does it try things?
- And the one the last week is for: **given a problem, which of the three paradigms is it?**

**Prerequisites:** PROG 102 and CS 211. From CS 211 you need grammars, ASTs, and the idea that a type system is a checkable set of rules — this course is where those rules become a *logic*. From PROG 102 you need to be able to write and debug a recursive function without help.

---

## Two Habits This Course Is Built Around

**1. Every number in these notes came off this machine, and the command is printed next to it.**

The same rule the other Year 2 courses follow. Where a measurement contradicts the textbook, or contradicts what the paradigm's enthusiasts say about it, **the measurement is shown and the claim is kept**, because you will meet both.

> Week 0's L02 has the first one, and it is not a contrived example. Every imperative programmer has
> been taught not to compute the same thing twice. In Haskell, computing a list twice uses **44 KB**
> and naming it once uses **272 MB** — same answer, same compiler, 6,100× the memory. The instinct
> is wrong here, and understanding *why* is Week 3.

**2. A paradigm's claim about itself is a hypothesis.**

"Pure functional code is easier to reason about." "Laziness lets you write what you mean." "Logic programming is declarative — you say *what*, not *how*." Each of these is **partly true**, and the interesting part of this course is the boundary.

You will measure a case where purity buys a real optimisation that C cannot have (W0), a case where laziness costs 6,000× the memory for the same answer (W0, W3), a case where the "declarative" Prolog program's answer depends entirely on the order you wrote the clauses (W9), and a case where a test suite that checks *every value correctly* cannot see the bug at all (W11).

**None of that is an argument against the paradigms.** It is what knowing them actually consists of.

---

## Assessment

| Component | Weight | Rule |
|---|---|---|
| **Problem Sets** | **40%** | PS 0–12, released Wednesday, due the following Friday 17:00. Lowest 1 dropped. |
| **Project 1** *(due Week 7)* | **15%** | An interpreter for a small language, in Haskell. |
| **Project 2** *(due completion period)* | **15%** | A logic-programming project with an executable specification. |
| **Midterm** *(Week 6)* | **15%** | 75 minutes, covering **Weeks 0–5**. One handwritten sheet, one side. |
| **Final Exam** | **15%** | 150 minutes, comprehensive. Two handwritten pages. |
| **Total** | **100%** | |

**One midterm, not two.** The curriculum docx says *Midterm 15%*, singular, and
[[Year2 - Sophomore/ASSESSMENT CALENDAR|ASSESSMENT CALENDAR]] puts it in Week 6 over Weeks 0–5. That leaves Weeks 6–12 examined only on
the final, which is why the final is comprehensive and worth as much as the midterm.

**Labs and quizzes carry no weight.** The curriculum's assessment line — *Problem Sets 40%, Projects
30%, Midterm 15%, Final 15%* — sums to 100% without them, and no percentage has been invented to
fill the gap. This is the same rule every Year 2 course follows.

**They are still required.** The lab is checked off by the TA in the session, and
[[Year2 - Sophomore/COURSE POLICIES|COURSE POLICIES]] costs you a letter grade after a second unexcused absence.

**Quizzes** run ten minutes at the start of **Tuesday's** lecture — this course's first lecture of
the week — in **Weeks 1–11**. **Quiz *N* covers Week *N−1*.** The answer key is printed in the paper,
below the questions.

Both are recorded in [[_PROG 202 Lab and Quiz Record]].

---

## Schedule

| | When | Where |
|---|---|---|
| **Lectures** | Tuesday and Thursday 11:00–12:15 | TH 205 |
| **Lab** | Wednesday 13:00–14:50 *(mandatory)* | BH 215 |
| **Office hours** | See below | — |

### Two lectures a week, not three — and they are 75 minutes

This is a **3-credit course with two lecture slots**, where CS 202 and CS 212 are 3-credit courses
with three. The contact time is the same (150 minutes) and the number of lectures is not: **26 across
the term, numbered L01–L26**, two per week, where those courses have 39.

**What that changes for you.** Each lecture carries half again as much material as a CS 212 lecture,
and there is no third session in the week to push the overflow into. Two consequences, both real:

- **A missed lecture is half a week, not a third.** There is no Wednesday to catch it in — Wednesday
  is the lab.
- **The reading is not optional in the way it is elsewhere.** Hutton's chapters are short and this
  course genuinely assumes you have read the one named at the top of each lecture. The
  [[PROG202 Week0/resources/Reading Guide Week 0|Reading Guide]] says which parts, and how long each actually takes.

### The lab runs a week behind the lectures, because Wednesday is in the middle

**Lab *N* covers Week *N* and is sat on the Wednesday of Week *N+1*.**

The lab is Wednesday; the lectures are Tuesday and Thursday. A lab sat on the Wednesday of Week *N*
would have had **one** of that week's two lectures. That is worse than useless for a lab that
practises the week's whole idea, so it lags a full week, and by the time you sit it you have both of
Week *N*'s lectures plus Week *N+1*'s Tuesday.

| Lab | Covers | Sat on |
|---|---|---|
| **Lab 0** | Week 0 | **Friday of Week 0, 13:00–14:50** — the Friday that closes the ten-day week, after both lectures |
| Lab 1 | Week 1 | Wednesday of Week 2 |
| Lab *N* | Week *N* | Wednesday of Week *N+1* |
| Lab 11 | Week 11 | Wednesday of Week 12 |
| **Lab 12** | Week 12 | **Demo day**, Wednesday of the completion period |

**There is no lab session in Week 1.** Lab 0 was sat on the Friday before it, and Lab 1 is waiting
for Week 1's lectures to happen.

**This course loses no lab to the calendar.** Spring Break (Mar 16) falls between Week 7 and Week 8
and takes no teaching Wednesday with it, so thirteen labs fit in thirteen slots with nothing moved.
*(PROG 201 in Fall was not so lucky — Fall Break ate a Monday and Lab 5 had to be made up on a
Friday. Do not carry that expectation across.)*

**Quizzes do not lag.** Quiz *N* is sat at the start of **Tuesday's lecture in Week *N*** and covers
**Week *N−1***.

> **Three Spring courses quiz on three different days.** CS 202 and MATH 251 and ECE 211 quiz
> Monday, CS 212 and this course quiz **Tuesday**, and CS 212's quiz is in the 10:00 slot, forty
> minutes before this one. Read each course's own header rather than carrying a habit between them.

**Instructor and TA: not yet listed.** The registry's [[Year2 - Sophomore/OFFICE HOURS|OFFICE HOURS]] covers the Fall courses only,
and names nobody for PROG 202. Nothing has been invented to fill the gap; the course portal carries
the staff and their hours once assigned. Until then the **Engineering Help Desk in BH 120** —
Monday–Thursday 10:00–20:00, Friday 10:00–17:00, weekends 12:00–18:00 — is staffed for every
Year 1–2 course.

---

## Tools

Everything runs on Linux — **BH 215, Ubuntu 24.04 LTS, kernel 7.0**, eight cores.

| Tool | Version here | For |
|---|---|---|
| `ghc` | **9.4.7** | The compiler. `-O2` and `-Wall` from Week 0 |
| `ghci` | 9.4.7 | The laboratory. `:t`, `:i`, `:sprint`, `:set +s` — Week 0 is largely this |
| `runghc` | 9.4.7 | Runs a `.hs` file interpreted. **57× slower than `-O2`** (L02 §5); use it for scripts, never for measurement |
| `cabal` | 3.8.1.0 | Present, and **cannot reach Hackage** — see *Deviations* |
| `swipl` | **9.0.4** | SWI-Prolog, from Week 8. Unbounded integers; `library(clpfd)`, `library(chr)`, `library(dcg/basics)` and tabling all present |
| `+RTS -s` | — | The runtime's own report: allocation, maximum residency, GC time. **This is the course's measuring instrument** and Week 0's lab installs the habit |
| `gcc` | 13.3.0 | Used twice, both times as a *contrast*: W0 §3 and W12 |

**Packages available to GHC** are exactly the ones that ship with it: `base`, `containers`, `array`,
`bytestring`, `text`, `mtl`, `transformers`, `parsec`, `stm`, `deepseq`, `time`, `process`, `unix`,
`binary`, `template-haskell`. That list is enough for every week of this course, and the two things
missing from it — `QuickCheck` and `random` — are the subject of a deviation below and of Week 11.

**`+RTS -s` is the single most useful tool in this course**, and it is the one nobody discovers on
their own. A Haskell program that is slow is almost never slow because the arithmetic is slow; it is
slow because it allocated 600 MB it did not need to. `-s` prints that number. Compile with
`-rtsopts`, run with `+RTS -s`, read the second line.

---

## Textbooks

**Hutton, G. — *Programming in Haskell*, 2nd ed. (Cambridge, 2016).**
*Primary text. About 300 pages for the whole language, and it earns every one of them — the
exercises are the good part. Chapters 1–12 are Weeks 0–6; 14–15 are Weeks 2 and 3; 16 is the one
that makes the Curry–Howard remark in Week 12 land.*

**O'Sullivan, B., Stewart, D. & Goerzen, J. — *Real World Haskell* (O'Reilly, 2008).**
*Free at book.realworldhaskell.org. Written against GHC 6, so its library advice is dated and its
`Monad` instances predate the Applicative reform — read it for the engineering chapters (profiling,
performance, error handling) and let Hutton have the language. **Where it and the machine disagree,
this course says so.***

**Clocksin, W. & Mellish, C. — *Programming in Prolog*, 5th ed. (Springer, 2003).**
*Weeks 8–11. The classic, and unusual in being a textbook whose examples still run unmodified.*

**Three papers, read in full, one each:** Hughes, *Why Functional Programming Matters* (1989) in
Week 3; Wadler, *Monads for Functional Programming* (1992) in Week 5; Claessen & Hughes,
*QuickCheck* (ICFP 2000) in Week 11. Each is under twenty pages and each is on the final.

---

## Week by Week

| Week | Topic | The question it answers |
|---|---|---|
| **0** | FP philosophy · Haskell · GHCi | What does a language *gain* by forbidding assignment? |
| **1** | Types: inference, ADTs, pattern matching | Why can the compiler know the type you did not write? |
| **2** | Higher-order functions; `foldr`/`foldl`; composition | What is left of a loop when you take the variable away? |
| **3** | Lazy evaluation; infinite lists; thunks | When does a Haskell program actually compute anything? |
| **4** | Type classes: `Eq`, `Ord`, `Show`, `Num`, `Functor`, `Foldable` | How is one function written once for every type at once? |
| **5** | Monads: `Maybe`, `IO`, `State` · **MIDTERM** | What single idea are these three the same shape of? |
| **6** | Applicatives; monad transformers; functional error handling · **Project 1 due W7** | How do you stack two effects without writing a third monad? |
| **7** | Concurrency: STM, lightweight threads, `par`/`pseq` | What does immutability buy a program with eight cores? |
| **8** | Prolog: facts, rules, queries | What is a program with no functions and no order? |
| **9** | Unification and resolution; the execution model | What does Prolog *do*, step by step? |
| **10** | Constraint solving; natural-language parsing | Where does logic programming beat everything else? |
| **11** | Property-based testing; formal specification | How do you test a property instead of an example? |
| **12** | Comparative study; choosing a paradigm · **Project 2 due** | Given a problem, which of the three is it? |

### The thing that runs through all thirteen weeks

**One problem, solved twice, measured both times.**

`sched` is a timetable checker. Its data is **this vault's own Year 2 Spring timetable** — the
seventeen sessions in [[Year2 - Sophomore/SPRING SCHEDULE|SPRING SCHEDULE]], 1,070 contact minutes a week — and its job is to answer
questions about it: does any two sessions clash, how much contact time is there, and can thirteen
labs be assigned to thirteen slots without breaking a constraint.

You build it in Haskell in Weeks 0–7, as tuples and then as algebraic data types and then as folds
and then in the `State` monad. You build it **again in Prolog** in Weeks 8–10, where the clash check
is one rule and the lab assignment is a constraint problem. Week 11 tests both against the same
properties. Week 12 puts the two implementations side by side with their measurements and asks which
was the right language — and the answer is not the same for both questions.

**Lab 0 finds the first real bug in the data on its first run.** It is in the registry, not in your
code, and it is still there.

---

## What This Course Feeds

**Immediately:** CS 211 last term gave you parsing and type rules; this course is where a type system
becomes a logic you can compute in. CS 212 this term wants you to test behaviour rather than
examples, which is Week 11 from the other side.

**Next year:** **CS 331 (AI)** is Weeks 8–10 continued — search, unification, and constraint
propagation are its first month. **CS 321 (Databases)** is Prolog's semantics with a different
syntax; Datalog *is* Prolog without function symbols, and the query optimiser is Week 9's execution
model made deliberate. **CS 311 (Compilers II)** will have you write type inference, which is
Week 1's algorithm.

**Whatever you actually write for a living:** the transferable half is Weeks 2–4. `map`, `filter`,
`fold`, and "make the type say it" are now in Python, Java, Rust, C++, TypeScript and Swift, and they
arrived there from here.

---

## Deviations From the Curriculum

Recorded here so a reader meets them without needing `5. Build Records/`. The reasoning behind each
is in [[PROG 202 Scheduling Notes]].

| What | Why |
|---|---|
| **QuickCheck is not installed, cannot be installed, and Week 11 builds one instead** | The curriculum's Week 11 is "Property-Based Testing with QuickCheck". GHC 9.4.7's package database here has 37 packages and `QuickCheck` is not among them; neither is `random`, which it needs. `cabal update` fails — `<repo>/root.json does not have enough signatures signed with the appropriate keys` — so there is no Hackage to install from and a student account cannot fix that. **Week 11 therefore builds a property tester from nothing**: a splitmix-style PRNG, an `Arbitrary` class with a size parameter, `forAll`, counterexample reporting, and — the part everybody skips — **shrinking**. It is about 150 lines, it finds the same bugs, and building it is a better week than importing it would have been. The Claessen–Hughes paper is read either way. **PS 11 and Lab 11 use the course's own `Check.hs`**, which ships in Week 11's `resources/`. |
| **Week 7's `par`/`pseq` come from `base`, not from the `parallel` package** | Every tutorial writes `import Control.Parallel`. That package is not installed and cannot be. `par` and `pseq` are in **`GHC.Conc`** in `base` with identical semantics, and `-threaded -rtsopts` plus `+RTS -N8` is the whole story on this machine's eight cores. The lecture measures real speed-up; it also measures the case where `par` produces none, which is the half the tutorials omit. |
| **`stack` and `hlint` are absent** | Neither is needed. Every program in this course is one or two files built with `ghc -Wall -O2`, which is deliberate — build tooling is CS 212's subject, not this one's. `hlint`'s advice is instead given where it belongs, inline in the lectures, as the reason a fold is preferred to a recursion. |
| **Two lectures a week, 26 in total, not three and 39** | [[Year2 - Sophomore/MASTER TIMETABLE|MASTER TIMETABLE]] gives this course Tue/Thu 11:00–12:15. Same contact minutes as a three-slot 3-credit course, fewer and longer sessions. The week's material is split in two rather than three, and each lecture is correspondingly denser. Not a deviation from the curriculum so much as one from its siblings, and it is the first thing a student notices. |
| **One midterm** | The docx says *Midterm 15%*, singular, where CS 202's says two. Weeks 6–12 are therefore examined for the first time on the final. The final is comprehensive and the Week 12 lecture is a revision lecture with teeth rather than a valediction. |
| **The Week 0 lab is on the Friday of Week 0 at 13:00, not a Wednesday** | [[Year2 - Sophomore/ASSESSMENT CALENDAR|ASSESSMENT CALENDAR]] puts every Year 2 course's Week 0 lab on the Friday that closes the ten-day Week 0. CS 202 holds that morning (10:00–11:50, BH 210); **13:00–14:50 is this course's ordinary lab time on a different day of the week**, and BH 215 is free. It applies to Lab 0 only. |
| **Lab 5 is sat the day before this course's own midterm** | Lab 5 covers Week 5 and so is sat on the Wednesday of Week 6 — 13:00–14:50 — and the midterm is **Thursday of Week 6 at 18:00**, covering Weeks 0–5. Nothing is moved: a two-hour practical on the `State` monad twenty-nine hours before a paper that examines it is good timing, not bad. Both the lab sheet and the Week 5 README say so. The collision worth knowing about is the other one — **CS 212's midterm is the Wednesday evening of the same week**, 18:00, three hours after this lab ends. |
| **`Real World Haskell` is a recommended text that this course contradicts in three places** | It is thirteen years older than the compiler on these machines. Its `Monad` instances predate the Applicative reform of GHC 7.10 and will not compile as written (W5), its profiling chapter uses flags `ghc` no longer spells that way (W3), and its advice to prefer `foldl` over `foldr` for "efficiency" is wrong in the direction that matters (W2). The book stays on the list because its engineering chapters have no replacement. Each contradiction is named in the week it arises. |
| **No `random`, so every "random" thing in this course is a named, seeded generator you wrote** | `System.Random` is not in the package database. Week 11's tester carries a 60-bit-multiplier splitmix variant with the seed printed on every failure, which is what a property tester should do anyway: **a failing case you cannot reproduce is not a bug report.** Where earlier weeks want arbitrary data they build it with `iterate` from a stated seed. |
| **The Prolog half runs on SWI-Prolog 9.0.4, and Clocksin & Mellish is not written against it** | The textbook is standard-Prolog; SWI has `format/2`, `between/3`, `succ_or_zero`, tabling as a directive, and a different module system. Where the book's program needs a change to run, the change is shown in the lecture rather than silently applied. **`library(clpfd)` is SWI-specific and Week 10 depends on it entirely** — it is present, it reports `bounded=false`, and the alternative (writing a propagation engine by hand) is Week 10's last section as reading. |

---

*PROG 202 · Year 2 Spring · © CSE Department*
