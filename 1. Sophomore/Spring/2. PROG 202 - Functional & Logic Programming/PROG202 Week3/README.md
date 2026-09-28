# PROG 202 · Functional & Logic Programming
## Week 3: Lazy Evaluation — Thunks, WHNF, and Where the Memory Went

**Credits:** 3 (2 lecture + 1 lab) · **Prerequisites:** PROG 102, CS 211
**Assessment for this course (overall):** Problem Sets 40%, Projects 30%, Midterm 15%, Final 15%
**This week's deliverables:** PS 3, Quiz 3 (Tuesday, covers Week 2). **Lab 2 is sat this Wednesday**;
Lab 3 is sat on the Wednesday of Week 4.

**Required reading: Hughes, *Why Functional Programming Matters* (1989), all 23 pages, this week.**
It is on the final.

---

### Why This Week Exists

Because three weeks of surprising numbers have accumulated and they are all one thing.

| Where | What |
|---|---|
| W0 L02 | `let xs = [1..10⁷]` used twice: **273 MB**. Written twice: **44 KB** |
| W0 PS 0 | the accumulator version of `sum`: **604 MB** at `-O0`, **44 KB** at `-O2` |
| W2 L06 | `foldl (+) 0`: **619 MB** at `-O0`, **44 KB** at `-O2` |
| W2 L06 | `foldr (+) 0`: **130 MB** at `-O2`, and no optimisation helps |
| W2 L06 | `foldr` answers a question about `[1..]`; `foldl` never terminates |

**This is the week you stop remembering those and start predicting them.** One definition does most of
the work — *weak head normal form* — and one command shows you everything — `:sprint`.

And then the week's own measurement, which is the one that will cost you money in a job: **a program
using `foldl'`, the strict fold, holding 727 MB.** It is strict and it leaks, because `foldl'` forces its
accumulator to WHNF, and the WHNF of a pair is the pair.

---

### Learning Objectives

By the end of Week 3, you should be able to:

1. Say what a thunk is, what entering one does, and why the second request is free.
2. **Define weak head normal form**, and use it to predict what `seq` does to a pair, a list and a `Just`.
3. Distinguish `seq`/`$!`/`!` from `deepseq`/`force`, and say which reaches inside a constructor.
4. Read a `:sprint` transcript, and use `:sprint` to find out what has been evaluated.
5. **Explain strictness analysis**, why it repaired `foldl` at `-O2`, and why it is not a guarantee.
6. **Say why `foldr` with a strict operator cannot be repaired**, and what is held in each case — heap
   chain against evaluation stack.
7. Distinguish **retention** from **fusion**, and say which one `-O2` can affect.
8. **Find a space leak**: `+RTS -s` first, then residency against allocation, then look for a name.
9. Fix one three ways — bang patterns, explicit `seq`, strict fields — and say why the third is best.
10. **Say why `Data.Map.Strict` is the right map for a counter**, in terms of WHNF.
11. Write and reason about infinite lists: `iterate`, knot-tying, and what *productive* means.
12. **State Hughes's modularity argument** and give the `sqrts`/`within` example.
13. Say what laziness costs: unreadable space behaviour, displaced errors, boxing.

---

### New Syntax and Symbols This Week

Full reference: [[PROG202 Week0/resources/Haskell Syntax and Symbols|Haskell Syntax and Symbols]].

| Symbol | Said out loud | Means |
|---|---|---|
| `seq a b` | **"seq"** | Force `a` to **WHNF**, then return `b`. Does **not** reach inside constructors |
| `f $! x` | **"strict apply"** | `seq x (f x)`. The strict cousin of `$` |
| `!x` *(pattern)* | **"bang pattern"** | Force on binding. Needs `{-# LANGUAGE BangPatterns #-}` |
| `data T = T !Int` | **"strict field"** | Force **when the constructor is applied**. Needs no extension |
| `~p` | **"lazy pattern"** | Match without forcing. Rare |
| `deepseq`, `force` | **"deepseq"** | Force to **normal form** — no thunks anywhere. From `Control.DeepSeq` |
| `{-# LANGUAGE … #-}` | **"language pragma"** | First appearance: `BangPatterns` |
| `_` in `:sprint` output | **"a thunk"** | Not evaluated yet |

**Functions and tools:** `iterate` · `repeat` · `cycle` · `takeWhile` · `dropWhile` ·
`Data.Map.Strict` against `Data.Map.Lazy` · `insertWith` · `+RTS -s` · `+RTS -K16m` ·
`:sprint` · `-prof -fprof-auto` and `+RTS -hc`.

> **`!` means three different things now** and this is the week to keep them straight: `!x` in a
> *pattern* forces on binding; `!Int` in a *data declaration* forces on construction; and `!!` is list
> indexing and has nothing to do with either.

---

### This Week's Materials

| File | Purpose |
| --- | --- |
| [[L07 Thunks Weak Head Normal Form and Space Leaks]] | Thunks; **WHNF, with `seq` on a pair doing nothing**; `deepseq`; **strictness analysis, and why `foldr` is beyond it**; retention against fusion; **the 727 MB `foldl'`**; how to find a leak |
| [[L08 Infinite Lists and Laziness as Glue]] | `[1..]` as an ordinary value; `iterate`; **knot-tying and *productive***; **Hughes's `sqrts`/`within`**; generate-and-test; **the "sieve" that is 19× slower than one**; what laziness costs |
| [[LAB 3 Watching Laziness Thunks and Space Leaks]] | `:sprint`, the 727 MB, and a **234 MB leak in `Stats.hs` fixed by editing a type rather than a function**. **Wednesday of Week 4** |
| `lab/Stats.hs`, `Sched.hs`, `Makefile` | Five statistics in one pass over 1.7 million sessions, and one TODO |
| [[PROG202 Week3/assignments/Problem Set 3\|Problem Set 3]] | Five questions, fifteen parts, 100 points, due **Friday of Week 4** |
| [[PROG202 Week3/assignments/QUIZ 3 Week 3 Tuesday\|QUIZ 3]] | Ten minutes, Tuesday, covers **Week 2**. Prints its own key |
| [[PROG202 Week3/resources/Reading Guide Week 3\|Reading Guide Week 3]] | **Hughes, and how to read it** — plus why Week 3 and not Week 0 |
| `resources/mean.hs`, `infinite.hs`, `sieve.hs` | The sixteen-cell leak table, knot-tying and Newton, and the sieve that is not one |
| `solutions_instructor/` | Instructor only |

---

### The One Thing to Take From This Week

**`foldl'` is the strict fold, and it forces the outermost constructor only.**

That sentence is worth 727 MB. Here is the mean of a list in one pass, written by somebody who knows to
use the strict fold:

```haskell
lazyPair xs = let (s, c) = foldl' step (0, 0) xs in fromIntegral s / fromIntegral c
  where step (s, c) x = (s + x, c + 1)
```

**At `-O0` this holds 727 MB** — worse than the two-pass version it was written to replace. `foldl'`
forces `(s + x, c + 1)` to weak head normal form; the WHNF of a pair is *the pair constructor*; and the
two components stay thunks and build two chains ten million links long.

**The general shape, and it recurs everywhere:** *a strict operation on a container is strict in the
container, not in its contents.* `Data.Map.Strict` exists because `Data.Map.Lazy`'s `insertWith (+)`
stores the unapplied addition — measured, **107 MB against 44 KB** — and `-O2` repairs the pair and
**cannot** repair the map, because the analyser cannot see inside a balanced tree.

**And the fix that generalises is not `seq`.** It is `data Stats = Stats !Int !Int !Int !Int !Int` — put
the strictness in the **type**, and every construction anywhere becomes strict, including in the function
you did not edit. Lab 3 §3c makes that happen in front of you, and it is the same argument as Week 1's
export list: **make the invariant a property of the data, not a rule every caller has to remember.**

---

### Assessment Reminder

**Labs and quizzes carry no weight.** They are still required; the lab is checked off in the session and
a second unexcused absence costs a letter grade. **Quiz *N* covers Week *N−1***, ten minutes at the start
of **Tuesday's** lecture, Weeks 1–11.

> **Lab 2 is sat this Wednesday and covers Week 2.** Lab 3 — this week's — is sat on the **Wednesday of
> Week 4.**
>
> **The midterm is in Week 6 and covers Weeks 0–5.** This week is the middle of it, and the definition
> of weak head normal form is the one thing from Weeks 0–5 that the rest of the course keeps needing.

Both are tracked in [[_PROG 202 Lab and Quiz Record]].

---

### Connections

**Back:** **this week is the answer key to Weeks 0–2.** Every number in the table at the top is explained
by §3 or §4 of L07. Week 2's `foldl'` is L07 §4's `seq` made explicit; Week 0's `:sprint` is L07 §3's
instrument; Week 0's `<<loop>>` is the blackhole in L07 §2.

**Sideways:** **CS 202's page-cache and allocator weeks** are the same question one layer down — what
does a program's memory cost when nobody is looking, and what instrument tells you. **CS 212's technical-
debt week** has the version of L07 §7 that is about process rather than tools.

**Forward:** **Week 4 explains the `Foldable t =>` you have been reading in every `:t` output** and gives
you `Functor`, the first of the three abstractions Weeks 4–6 stand on. **Week 5's `State` monad is a fold
with the accumulator hidden**, and every leak in this week's lab is available there with the leak harder
to see. **Week 7's parallelism cannot work at all without this week**: `par` on a thunk that nobody forces
does nothing, and the first thing that lecture measures is a speed-up of exactly 1.0×.

---

*PROG 202 · Week 3 · © CSE Department*
