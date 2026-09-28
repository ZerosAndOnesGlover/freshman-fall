# PROG 202 · Functional & Logic Programming
## Week 2: Higher-Order Functions, Folds, and What They Cost

**Credits:** 3 (2 lecture + 1 lab) · **Prerequisites:** PROG 102, CS 211
**Assessment for this course (overall):** Problem Sets 40%, Projects 30%, Midterm 15%, Final 15%
**This week's deliverables:** PS 2, Quiz 2 (Tuesday, covers Week 1). **Lab 1 is sat this Wednesday**;
Lab 2 is sat on the Wednesday of Week 3.

---

### Why This Week Exists

Because Week 1 left you writing the same two equations over and over, and this is the week they collapse
into one function.

`sum`, `product`, `length`, `reverse`, `eval`, `depth`, `countLits` — all of them are two equations
differing only in a starting value and a combining operation. **When four functions differ only in an
operator, the operator is the argument**, and the function that takes it is `foldr`. That is the whole
idea, and it is the most transferable week in the course: `map`, `filter` and `fold` are in Python, Java,
Rust, C++, TypeScript and Swift now, and they came from here.

**But the week is not really about writing folds. It is about which one, and what the wrong choice
costs.** The received advice — `foldl` overflows the stack, prefer `foldr` — turns out to be **two-thirds
wrong on this machine**, and finding out how is the week's work. At `-O2`, `foldl` uses 44 KB and `foldr`
uses 130 MB. At `-O0` they swap. Nothing overflows unless you cap the stack, and when you do, **both**
overflow.

---

### Learning Objectives

By the end of Week 2, you should be able to:

1. Pass a function as an argument and return one as a result, and say why "higher-order" needs no syntax.
2. **Explain currying** from the associativity of `->` and of application, and say why partial
   application is therefore free.
3. Choose between `map`, `filter`, `takeWhile`, `zipWith` and `concatMap` by naming what each preserves.
4. Write a comprehension and the equivalent combinator pipeline, and say when each reads better.
5. Use `.` and `$`, read `(== LEC) . kind` at a glance, and **say when point-free style stops helping.**
6. **Define `foldr` from memory**, and derive `sum`, `map`, `filter`, `length` and `reverse` from it.
7. State the **universal property of `foldr`** and use it to rewrite `f . map g` as one fold.
8. **Choose the fold from the operator**: strict accumulator → `foldl'`; lazy in its second argument →
   `foldr`, which short-circuits and works on infinite lists.
9. **Reproduce the eight fold numbers** and say which ranking holds at which optimisation level.
10. Explain what `seq` does **and what it does not do**.
11. **Say why `acc ++ [x]` in a loop is quadratic**, from `(++)`'s two-line definition, and give the fix.
12. Say why Hutton's four-line `qsort` beats the library on random input and is unusable on sorted input.

---

### New Syntax and Symbols This Week

Full reference: [[PROG202 Week0/resources/Haskell Syntax and Symbols|Haskell Syntax and Symbols]].

| Symbol | Said out loud | Means |
|---|---|---|
| `.` | **"compose"** | `(f . g) x` = `f (g x)`. Right to left, as in mathematics |
| `$` | **"apply"** | Lowest precedence, right-associative. **It exists to delete a bracket** |
| `\x -> e` | **"lambda"** | An anonymous function |
| `(+ 1)`, `(1 +)` | **"section"** | An operator with one side supplied |
| `(- 1)` | **negative one** | **Not a section.** `-` is the language's one irregular symbol; write `subtract 1` |
| `` `div` `` | **"infix"** | Backticks make a named function infix |
| `(,)` | — | The pair constructor as a function |

**Functions rather than symbols, and all of them are new this week:**
`foldr` · `foldl` · **`foldl'`** *(from `Data.List` — the apostrophe is part of the name, not a quote)* ·
`scanl` · `scanl1` · `zipWith` · `concatMap` · `takeWhile` · `dropWhile` · `uncurry` · `curry` ·
`flip` · `const` · `id` · `maximumBy` *(`Data.List`)* · `comparing` *(`Data.Ord`)* · `sortOn` ·
**`seq`**.

> **`foldl'` is spelled with a prime and it matters.** It lives in `Data.List`, not the Prelude, so it
> needs an import; the Prelude gives you `foldl` without it, which is the one you never want. A
> trailing `'` is an ordinary character in a Haskell name — `x'` is a perfectly good variable — and it
> conventionally means "the strict version of".

---

### This Week's Materials

| File | Purpose |
| --- | --- |
| [[L05 Higher-Order Functions and Composition]] | Functions as values; **currying from the two associativities**; `map`/`filter`/`zipWith`; comprehensions against combinators; `.` and `$`; **where point-free stops helping**; four functions with one function's content |
| [[L06 foldr foldl and Which One to Use]] | `foldr` as constructor replacement; the universal property; **the eight fold numbers, and the ranking that reverses**; the stack overflow that needs `+RTS -K16m`; **`foldr` on an infinite list**; `seq`; **`++` at 22.57 s against 0.01 s**; **`qsort` faster than the library, and unusable on sorted input** |
| [[LAB 2 Refactoring Loops Into Folds]] | Six loops into six combinators, byte-identical output enforced. **Wednesday of Week 3, 13:00–14:50** |
| `lab/Report.hs`, `Sched.hs`, `Main.hs`, `Makefile`, `expected.txt` | Six TODOs, last week's module, a driver, and the reference output `make check` diffs against |
| [[PROG202 Week2/assignments/Problem Set 2\|Problem Set 2]] | Five questions, fifteen parts, 100 points, about three hours, due **Friday of Week 3** |
| [[PROG202 Week2/assignments/QUIZ 2 Week 2 Tuesday\|QUIZ 2]] | Ten minutes, Tuesday, covers **Week 1**. Prints its own key |
| [[PROG202 Week2/resources/Reading Guide Week 2\|Reading Guide Week 2]] | Hutton 6 and 7 — **and why the Hughes paper is next week's, not this week's** |
| `resources/folds.hs`, `short.hs`, `append.hs`, `qsort.hs` | Every measurement above, each with its numbers in its header comment |
| `solutions_instructor/` | Instructor only |

---

### The One Thing to Take From This Week

**The operator decides the fold. The fold does not decide anything.**

Almost everybody arrives with a rule of the form *"use `foldr`"* or *"use `foldl'`"* and leaves applying
it uniformly. The measurements say that is not a choice you can make once:

| operator | right fold | why |
|---|---|---|
| strict in the accumulator — `+`, `*`, `max` | **`foldl'`** | 44 KB at every optimisation level. `foldr` is 130 MB |
| lazy in its second argument — `&&`, `\|\|`, `:`, `++` | **`foldr`** | it stops early, and **answers questions about infinite lists that no left fold can** |

And **`foldl` without the prime is never the answer.** At `-O2` the optimiser silently repairs it; at
`-O0` it is the worst of the four at 619 MB; with a capped stack it crashes. There is no input for which
you want it over `foldl'`.

**The deeper habit is the one the numbers install.** The advice in the textbooks was not wrong when it
was written — it described a crash that GHC no longer produces by default, so the same bug now shows up
as 619 MB of quietly-consumed heap. **A student who had learned the rule and not the measurement would
look at that program, see it complete without an exception, and conclude `foldl` was fine.**

That is what `+RTS -s` is for, and it is why this course asks for numbers rather than rules.

---

### Assessment Reminder

**Labs and quizzes carry no weight.** They are still required; the lab is checked off in the session and
a second unexcused absence costs a letter grade.

**Quiz *N* covers Week *N−1***, ten minutes at the start of **Tuesday's** lecture, Weeks 1–11.

> **Lab 1 is sat this Wednesday and covers Week 1.** Lab 2 — this week's — is sat on the **Wednesday of
> Week 3**. The lab is always a week behind the lectures.

Both are tracked in [[_PROG 202 Lab and Quiz Record]].

---

### Connections

**Back:** **Week 1's `Sched.hs` is the input to this week's lab**, unchanged. L05 §5 is the observation
L04's exercises asked you to notice and remember. And Week 0's 44 KB / 273 MB is the same phenomenon as
`foldr`'s 130 MB, which Week 3 finally names.

**Sideways:** **CS 202 is measuring the same kind of thing from the other side** — its page-cache and
allocator weeks are about what a program's memory costs when nobody is looking. **CS 212's refactoring
week** is Lab 2 with a different vocabulary: its "extract method" and "replace loop with pipeline" are
exactly the six TODOs, and its rule that a refactor must not change behaviour is `make check`.

**Forward:** **Week 3 explains every number in this week.** Why `foldl` is 619 MB and then 44 KB; why
`foldr` can answer a question about `[1..]`; what `seq` forces; and what Week 0's 273 MB was. **Week 4
generalises `foldr` off lists** — that `Foldable t =>` in every `:t` output — and **Week 5's `State`
monad is a fold with the accumulator hidden**, which is worth knowing now so that it is one idea and not
two.

---

*PROG 202 · Week 2 · © CSE Department*
