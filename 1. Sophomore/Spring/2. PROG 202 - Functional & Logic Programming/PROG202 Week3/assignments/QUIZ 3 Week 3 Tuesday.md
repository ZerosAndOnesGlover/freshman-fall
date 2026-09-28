# PROG 202 · Quiz 3
## Administered: Tuesday, Week 3 (first 10 minutes of lecture)

**Name:** _________________________________ **Section:** ___________ **Date:** ___________

**Covers Week 2** — higher-order functions, currying, composition, and the two folds.

**Instructions:** Closed notes. 10 minutes.

> **This quiz is not marked and carries no weight.** The answer key is printed below the questions.
> Sit it closed-book, then turn the page and mark it yourself before you leave the room.

---

**Q1.** Why is `map (add 3) [1,2,3]` legal with no lambda, given `add :: Int -> Int -> Int`?

&nbsp;

&nbsp;

---

**Q2.** Evaluate `foldr (-) 0 [1,2,3]` and `foldl (-) 0 [1,2,3]`.

&nbsp;

&nbsp;

---

**Q3.** State the rule for choosing between `foldl'` and `foldr`. Your answer should mention the
operator, not the list.

&nbsp;

&nbsp;

---

**Q4.** `foldl (+) 0 [1..10⁷]` used **44 KB** at `-O2` and **619 MB** at `-O0`. Why is `foldl'` the rule
anyway?

&nbsp;

&nbsp;

---

**Q5.** `foldr` answers `True` for "is any element greater than 5?" over `[1..]`. `foldl` never
terminates. Which element is the outermost application in each?

&nbsp;

&nbsp;

---

**Q6.** Building a list with `acc ++ [x]` inside a fold took 22.57 s at *n* = 40,000 where consing took
0.01 s. Why, from `(++)`'s definition?

&nbsp;

&nbsp;

---

**Q7.** Hutton's four-line `qsort` beat `Data.List.sort` on a million random `Int`s. Give the one
measurement that makes it the wrong choice anyway.

&nbsp;

&nbsp;

---
---

## Answer Key

**Q1.** Because **`add` never took two arguments.** `Int -> Int -> Int` is `Int -> (Int -> Int)`, so
`add 3` *is already* a function of one argument. Partial application is not a feature; it is what
currying makes automatic.

---

**Q2.** `foldr (-) 0 [1,2,3]` = `1 - (2 - (3 - 0))` = **2**.
`foldl (-) 0 [1,2,3]` = `((0 - 1) - 2) - 3` = **−6**.

*`foldr` brackets right, `foldl` brackets left, and for a non-associative operator they differ.*

---

**Q3.** **The operator decides.** If it is **strict in the accumulator** (`+`, `*`, `max`) use
**`foldl'`**. If it is **lazy in its second argument** (`&&`, `||`, `:`, `++`) use **`foldr`**, which
then short-circuits and works on infinite lists.

---

**Q4.** Because the 44 KB was **strictness analysis**, which is an optimisation and not a guarantee —
their own `-O0` column is the proof. `foldl'` says `seq` out loud, so it is 44 KB at **every**
optimisation level and does not depend on the analyser succeeding.

*And `foldl` without the prime has no case where you want it over `foldl'`.*

---

**Q5.** `foldr`'s outermost application involves the **first** element: `f x₁ (foldr f z rest)`. So an
operator that ignores its second argument never examines the rest.

`foldl`'s outermost application involves the **last** element, so it cannot produce anything until it
reaches the end of the list — and `[1..]` has no end.

---

**Q6.** `(x:xs) ++ ys = x : (xs ++ ys)` — the recursion is on the **left** argument only, so `xs ++ ys`
costs `length xs` and never inspects `ys`. Appending at the end therefore **re-walks everything built so
far**, and the total is the sum of all the lengths it passed through.

---

**Q7.** **On already-sorted input it takes 19.0 s at *n* = 40,000**, where `Data.List.sort` does a
million in 0.194 s. Its average case is better and its worst case is the input you actually get — logs,
timestamps, anything sorted by an earlier stage.

*Accept also: it is not in place, and it does not choose a pivot.*

---

### What to Do With Your Score

There is no score. Instead:

| If you missed | Reread |
|---|---|
| Q1 | L05 §2 — **and fix it today**; every type this week has arrows in it |
| Q2, Q5 | L06 §1 and §3 |
| **Q3, Q4** | **L06 §3** — these two are on the midterm |
| Q6 | L06 §5 |
| Q7 | L06 §6 |

**Q4 is this week's question.** Today's lecture explains *why* `-O2` could repair `foldl` and could not
repair `foldr`, and if the difference between an optimisation and a guarantee is not yet sharp, the
whole lecture will slide past.

---

*PROG 202 · Week 3 · Quiz 3 · covers Week 2 · ungraded*
