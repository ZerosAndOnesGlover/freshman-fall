# PROG 202 · Functional & Logic Programming
## Week 3 · Lecture 1 of 2
### Thunks, Weak Head Normal Form, and Where the Memory Went

*“Measure. Don't tune for speed until you've measured, and even then don't unless one part of the code overwhelms the rest.”* — Rob Pike, "Notes on Programming in C" (1989), rule 2

---

**Sat:** Tuesday of Week 3, 11:00–12:15, TH 205 · **⚠️ Quiz 3 in the first ten minutes** — covers Week 2 · **Reading:** Hutton §15.1–15.5 · **Next:** L08, infinite lists and laziness as a design tool

**Coursework:** 📊 **Quiz 3** today · 📝 **PS 3** released Wed this week, due Fri of Week 4 17:00 · 🔬 **Lab 2** Wed this week 13:00–14:50 · 📝 **PS 2** due Fri this week 17:00

---

## 1. Everything You Have Measured So Far Is This Lecture

Three weeks of surprising numbers, all one phenomenon:

| Where | What | Explained in |
|---|---|---|
| W0 L02 | `let xs = [1..10⁷]` used twice: **273 MB**; written twice: 44 KB | §5 |
| W0 PS 0 | `sum2` accumulator: **604 MB** at `-O0`, **44 KB** at `-O2` | §4 |
| W2 L06 | `foldl (+) 0`: **619 MB** at `-O0`, 44 KB at `-O2` | §4 |
| W2 L06 | `foldr (+) 0`: **130 MB** at `-O2`, and it does not improve | §3 |
| W2 L06 | `foldr` answers a question about `[1..]`; `foldl` never terminates | **L08** |

**By the end of this lecture you should be able to predict all five** rather than remember them.

---

## 2. A Thunk Is a Value That Has Not Happened Yet

**Haskell evaluates nothing until somebody needs it.** When you write

```haskell
let x = expensive 1000
```

no work is done. `x` is a **thunk**: a small heap object holding a pointer to code and the values that
code needs. It is *about* 16–24 bytes plus its captured environment, and the point is that it is not
the answer.

When something finally needs `x`, the runtime **enters** the thunk, runs the code, and then
**overwrites the thunk with the answer** — so the next request is free. That overwriting is the
"remember it" in *call by need*, and it is the difference from call by name in L02 §2.

> **The blackhole from Week 0 lives here.** Between entering a thunk and overwriting it, the RTS marks
> it. Entering a marked thunk on the same thread means the value depends on itself, which is `<<loop>>`
> — and `and (repeat False)` with `foldl` in Week 2 hit exactly that.

`:sprint` is how you look:

```
ghci> let xs = map (*2) [1..5] :: [Int]
ghci> :sprint xs
xs = _
```

**`_` is a thunk.** Nothing has run: not the `map`, not the `[1..5]`.

---

## 3. Weak Head Normal Form — the Most Important Two Minutes of the Term

"Evaluate `x`" is ambiguous, and Haskell always means the weaker of the two things it could mean.

> **A value is in *weak head normal form* (WHNF) when its outermost constructor is known.**
> It is in *normal form* (NF) when it contains no thunks anywhere.

Forcing goes to **WHNF and stops**. Watch:

```
ghci> let p = (1+1, 2+2) :: (Int, Int)
ghci> :sprint p
p = (_,_)
ghci> p `seq` ()
()
ghci> :sprint p
p = (_,_)
```

**`seq` did nothing visible.** `p` was *already* in WHNF — the pair constructor was known from the
moment `p` was written — so `seq` had no work to do, and **neither component was touched.**

```
ghci> fst p
2
ghci> :sprint p
p = (2,_)
```

Now the first is a number and the second is still a thunk.

And for a list, WHNF is **one cons cell**:

```
ghci> let xs = map (*2) [1..5] :: [Int]
ghci> xs `seq` ()
()
ghci> :sprint xs
xs = _ : _
```

**One cell, and both its head and its tail are thunks.** `seq` on a list tells you only that the list
is not empty.

**Normal form needs `deepseq`**, from the `deepseq` package, which is installed here:

```
ghci> import Control.DeepSeq
ghci> let q = (1+1, 2+2) :: (Int, Int)
ghci> q `deepseq` ()
()
ghci> :sprint q
q = (2,4)
```

**This distinction is the single most common source of confusion in Haskell performance work**, and §6
is a 727 MB example of getting it wrong.

| Operator | Forces to | Reaches inside constructors? |
|---|---|---|
| `seq a b` | WHNF | **No** |
| `f $! x` | WHNF | No — it is `seq` plus application |
| `!x` *(bang pattern)* | WHNF | No |
| `deepseq a b`, `force a` | NF | **Yes** |
| `data T = T !Int` | field to WHNF **on construction** | that field only |

---

## 4. Strictness Analysis: Why `-O2` Repaired `foldl`

`foldl (+) 0 [1..10⁷]` cost **619 MB** at `-O0` and **44 KB** at `-O2` (W2 L06 §3). Nothing about the
source changed.

**At `-O0`, the accumulator is a thunk chain.** `foldl` passes `f z x` forward unevaluated, so after ten
million steps the accumulator is

```
((((0 + 1) + 2) + 3) + … + 10000000)
```

— ten million pending additions, each a heap object, **none of them collectable because the next one
points at it.** Then `print` asks for the answer and the whole chain collapses at once. That chain is
the 619 MB.

**At `-O2`, GHC proves it will be needed.** The *strictness analyser* asks, of each argument: *if this
function's result is demanded, is this argument certainly demanded too?* For `foldl (+)` the answer is
yes — the final `print` forces the accumulator, which forces the last `+`, which forces its left
argument, and so on — so GHC compiles the loop to evaluate as it goes, on an unboxed `Int#` in a
register. Constant space, no thunks.

**Two consequences, and the second is the one to carry:**

1. **`foldl'` does not need the analysis.** It says `seq` explicitly, so it is 44 KB at every
   optimisation level. That is why it is the rule.
2. **The analysis is a *best effort*, not a guarantee.** It succeeded here. Change the program so the
   accumulator is only *sometimes* demanded — put it in a `Maybe`, or behind a branch that might not
   run — and the analysis correctly refuses, at any `-O` level, because forcing it would change the
   program's meaning. **You cannot look at source code and know whether the analysis will fire.** You
   can look at `+RTS -s`.

> **This is why the course insists on measurement rather than rules.** "`foldl` is fine at `-O2`" is
> true of the program in `folds.hs` and is not a fact about `foldl`.

### And `foldr` is not repaired, because it cannot be

`foldr (+) 0 [1..10⁷]` is 130 MB at `-O2` and there is no analysis that fixes it. `foldr`'s outermost
application is

```
1 + (foldr (+) 0 [2..10000000])
```

To add, you need the right-hand side, which needs the next one, and so on **to the end of the list** —
so the whole pending structure exists before a single addition happens, and this time it is the
*evaluation stack* rather than a thunk chain. **Strictness is not the problem; direction is.** For a
strict operator, `foldr` is asking to build the entire computation before doing any of it.

---

## 5. Sharing, and Week 0's 273 MB

```haskell
print (sum [1..10000000], length [1..10000000])   --  44 KB
let xs = [1..10000000] in print (sum xs, length xs) -- 273 MB
```

**A name must denote one value.** That is not an implementation detail; it is what `=` means. So in the
second line `xs` is *one* list, `sum` walks it from the front, and `length` also needs it from the
front — so **every cell between `sum`'s cursor and the front must be kept alive** until `length` gets
there. Ten million cons cells, 273 MB.

In the first line the two `[1..10000000]`s are **different expressions**. Each is produced lazily,
consumed immediately by its one consumer, and collected as it goes — nothing is ever retained.

**And naming it costs a second time**, in allocation rather than residency: the unnamed version
allocates **53 KB** at `-O2` because GHC *fuses* `sum [1..n]` into a counting loop with no list at all,
and fusion is impossible when the list is shared. The named version allocates 640 MB.

| | what it is | can `-O2` help? |
|---|---|---|
| **Retention** — 44 KB vs 273 MB | a live reference keeps data reachable | **No.** Present at `-O0` too |
| **Fusion** — 53 KB vs 640 MB allocated | the intermediate list is never built | **Yes, and naming it switches fusion off** |

**Two different phenomena, and merging them is the commonest mistake.** A "space leak" of the first
kind is a *reachability* problem — something is still pointing at data you are finished with — and the
only fix is to stop pointing at it. Of the second kind it is an *allocation* problem, and the fix is to
let the optimiser see the pipeline.

---

## 6. The Space Leak You Will Actually Write

Here is the mean of a list, in one pass, because two passes retain the list. `resources/mean.hs`:

```haskell
lazyPair xs = let (s, c) = foldl' step (0, 0) xs in fromIntegral s / fromIntegral c
  where step (s, c) x = (s + x, c + 1)
```

**`foldl'` is the strict fold. This still leaks, and by more than anything else in the course.**

*n* = 10,000,000:

| | `-O0` allocated | `-O0` residency | `-O2` allocated | `-O2` residency |
|---|---:|---:|---:|---:|
| two passes, `sum`/`length` | 880 MB | **245 MB** | 720 MB | **289 MB** |
| one pass, lazy pair | 2,505 MB | **727 MB** | 160 MB | **44 KB** |
| one pass, `(!s, !c)` | 1,840 MB | 60 KB | 160 MB | 44 KB |
| one pass, `data Acc = Acc !Int !Int` | 1,280 MB | 60 KB | **110 KB** | **44 KB** |

**Read the second row.** At `-O0` the "strict" fold holds **727 MB** — worse than the two-pass version
it was written to improve on.

**Why: `foldl'` forces its accumulator to WHNF, and the accumulator is a pair.** WHNF of a pair is
`(_, _)` — the constructor. §3 showed `seq` on a pair doing nothing, and this is that fact costing
727 MB: every step builds `(s + x, c + 1)` with both components as thunks, `seq` confirms it is a pair,
and the two chains grow to ten million links each.

**Three fixes, in increasing order of how much you should like them:**

1. **`step (!s, !c) x = …`** — bang patterns force the components as they are bound. 727 MB → 60 KB.
   Needs `{-# LANGUAGE BangPatterns #-}`.
2. **`foldl' step (0, 0)` with `step (s, c) x = s `seq` c `seq` (s + x, c + 1)`** — the same thing
   written by hand.
3. **A strict data type**: `data Acc = Acc !Int !Int`. The `!`s make strictness a property of the
   *type*, so every construction anywhere forces the fields and no caller has to remember.

**The third is the right answer** and it is the one that also wins at `-O2`: 110 KB allocated against
160 MB, because there is no pair to allocate at all.

> **The row nobody expects is the first.** The two-pass version leaks **at both optimisation levels**,
> 245 MB and 289 MB, and `-O2` makes it slightly *worse*. It is §5's retention: `xs` is named and two
> traversals need it. **No strictness annotation can fix a retention problem**, which is why the
> one-pass version was worth writing in the first place — it just has to be written strictly.

---

## 7. How to Find One

When a program uses more memory than you expected, in this order:

1. **`+RTS -s`.** Look at **maximum residency** (how much was live at once — retention) and **bytes
   allocated** (total churn — fusion and boxing). They answer different questions and beginners read
   the wrong one.
2. **Ask which it is.** High residency and modest allocation is *retention*: something is still
   pointing at old data. High allocation and low residency is usually fine — GHC's nursery is a bump
   allocator — unless the GC time in `-s` is large.
3. **For retention, look for a name.** A `let`-bound structure used twice, a lazy accumulator, a
   `Data.Map` with lazy values, a `foldl` without a prime.
4. **`:sprint` in GHCi** on a small input, to see what is and is not evaluated.
5. **`-prof -fprof-auto` and `+RTS -hc`** for a heap profile, when the first four have not found it.
   *(This is the flag `Real World Haskell` Chapter 25 calls `-auto-all`; it was renamed. The book's
   third disagreement with this machine.)*

**Step 1 finds it most of the time**, and the habit of running it before guessing is what Pike's rule
at the top of this lecture is asking for.

---

## 8. What to Take Away

1. **A thunk is a heap object holding unrun code.** Entering it runs the code and overwrites it, which
   is why the second request is free.
2. **Forcing goes to weak head normal form: the outermost constructor, and no further.** `seq` on a
   pair does nothing; `seq` on a list gives you one cons cell.
3. **`seq`/`$!`/`!` reach WHNF; `deepseq`/`force` reach normal form.** Confusing the two is the standard
   Haskell performance mistake.
4. **Strictness analysis is why `-O2` repaired `foldl`** — and it is best-effort, so `foldl'` (which
   says `seq` out loud) is the rule.
5. **`foldr` with a strict operator cannot be repaired.** The problem is direction, not strictness.
6. **Retention and fusion are different things.** 273 MB is a live reference and `-O2` cannot help;
   53 KB against 640 MB allocated is fusion and naming the list switches it off.
7. **`foldl'` over a pair leaks 727 MB**, because WHNF of a pair is the constructor. Use
   `data Acc = Acc !Int !Int` and make strictness a property of the type.
8. **`+RTS -s` first, then ask whether it is residency or allocation.** Not the other way round.

---

## Exercises

*(Not assessed. PS 3 is the assessed work.)*

1. Reproduce §3's three `:sprint` sequences exactly. Then predict and check `:sprint` for
   `Just (1+1)` after `seq`, and for `[1+1, 2+2]` after `length`.
2. `seq (1, undefined) ()` succeeds and `seq undefined ()` throws. Explain both from §3's definition,
   then predict `seq (undefined, 2) ()`.
3. Run `resources/mean.hs` at both optimisation levels and reproduce all sixteen numbers. Which row
   would you ship, and what does it cost you in source-code ugliness?
4. Write `mySum :: [Int] -> Int` that leaks at `-O2` — not at `-O0`, at `-O2`. *(You will need the
   accumulator to be only conditionally demanded. This is harder than it sounds and the point is to
   find out why.)*
5. `data Acc = Acc !Int !Int` makes the fields strict. What is the WHNF of `Acc undefined 3`? Predict,
   then check with `seq`.

---

*PROG 202 · Week 3 · L07 · © CSE Department*
