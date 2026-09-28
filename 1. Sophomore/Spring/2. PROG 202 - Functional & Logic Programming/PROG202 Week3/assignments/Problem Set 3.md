# PROG 202 · Problem Set 3
## Laziness: Thunks, WHNF, Space Leaks, and Infinite Lists

---

**Released:** Week 3, Wednesday · **Due:** Week 4, Friday 17:00
**Total: 100 points** · Submit one PDF, `PS3_{LastName}_{StudentID}.pdf`, plus your `.hs` files in a
tarball `PS3_{LastName}.tar.gz`

> **About three hours.** Five questions, fifteen parts.
>
> **State your `ghc --version` and `uname -r`.** Every number comes from a binary built with `ghc -O2`
> or `-O0` as the question says. **No timings from `runghc` or `ghci`** — but `:sprint` transcripts from
> `ghci` are exactly what Q1 wants.
>
> **Every `.hs` file compiles clean under `ghc -Wall -O2`.**

---

### Q1: Weak Head Normal Form (20 points)

**(a) [8]** Predict each `:sprint` output, then run it, and report both.

```
ghci> let p = (1+1, 2+2) :: (Int, Int)
ghci> :sprint p
ghci> p `seq` ()
ghci> :sprint p
ghci> fst p
ghci> :sprint p
ghci> let xs = map (*2) [1..5] :: [Int]
ghci> xs `seq` ()
ghci> :sprint xs
ghci> let j = Just (1+1) :: Maybe Int
ghci> j `seq` ()
ghci> :sprint j
```

**One of your predictions is almost certainly wrong**, and it is the second `:sprint p`. Write the
definition of weak head normal form that makes it obvious.

**(b) [6]** For each, say whether it succeeds or throws, and why:

1. `seq undefined ()`
2. `seq (undefined, 2) ()`
3. `seq (1 : undefined) ()`
4. `deepseq (1, undefined) ()`
5. `seq (Acc undefined 3) ()` where `data Acc = Acc !Int !Int`

**Number 5 does not behave like number 2.** Explain the difference in one sentence — it is the whole
reason strict fields exist.

**(c) [6]** `let x = error "boom" in length [x, x, x]` returns `3`.

- Why does the error never happen?
- Give an expression using the same `x` that **does** throw.
- Give one that throws at `-O0` and not at `-O2`, or explain why you believe none exists. *(There is no
  expected answer; the marks are for the reasoning and for having tried it.)*

---

### Q2: The Leak (22 points)

**(a) [10]** Build `resources/mean.hs` at both levels and fill in all sixteen cells for
*n* = 10,000,000:

| | `-O0` allocated | `-O0` residency | `-O2` allocated | `-O2` residency |
|---|---|---|---|---|
| `two` | | | | |
| `lazy` | | | | |
| `bang` | | | | |
| `strict` | | | | |

- The `lazy` row uses **`foldl'`**, the strict fold, and holds about **727 MB** at `-O0`. Explain in one
  sentence using the phrase *weak head normal form*.
- The `two` row leaks at **both** levels and `-O2` makes it worse. **Name that problem** and say why no
  amount of `seq` can fix it.
- The `strict` row allocates **110 KB** at `-O2` where `bang` allocates 160 MB, although both are
  strict. Where did the 160 MB go?

**(b) [6]** At `-O2` the `lazy` row is 44 KB — the same as the fixed versions.

- **Is the bug gone?** Answer in two sentences.
- Name the compiler pass responsible.
- **Give one reason you would still not ship the `lazy` version**, phrased as something you would say
  in a code review.

**(c) [6]** In your Lab 3 `Stats.hs`, you fixed the leak twice: once with bang patterns in the step, and
once with `!` in the data declaration.

- Report the residency and time for `./stats lazy 100000` and `./stats strict 100000` **in both
  fixes**. Four numbers.
- In the second fix, **`step` was not edited and became strict anyway.** Explain what a strict field
  does and *when* it does it.
- **Give a case where the bang-pattern fix is the only one available.** One sentence.

---

### Q3: Folds, Explained (18 points)

You measured these in Week 2 without an explanation. Give the explanations now.

**(a) [7]** `foldl (+) 0 [1..10⁷]` is **619 MB at `-O0`** and **44 KB at `-O2`**.

- Draw or write out what the accumulator looks like after three steps at `-O0`.
- Name the pass that removes it at `-O2`, and state precisely what it proves.
- **Why is `foldl'` 44 KB at both levels?** One sentence.

**(b) [6]** `foldr (+) 0 [1..10⁷]` is **130 MB at `-O2` and no optimisation helps.**

- Write out `foldr (+) 0 [1,2,3]` fully bracketed.
- Explain why the whole structure must exist before any addition happens.
- **Is this the same problem as (a)?** Answer explicitly yes or no and justify it. *(The two answers
  differ in what is being held: say what, in each case.)*

**(c) [5]** `foldr (\x acc -> x > 5 || acc) False [1..]` returns `True`. `foldl'` with the equivalent
operator never terminates.

- Say which element is the **outermost** application in each fold.
- Hence explain the difference in one sentence.
- `and (repeat False)` with `foldl` prints `<<loop>>`, not a hang. **Why `<<loop>>`?** *(You met the
  mechanism in Week 0.)*

---

### Q4: Infinite Lists (20 points)

**(a) [7]** `fibs = 0 : 1 : zipWith (+) fibs (tail fibs)`.

- Trace the production of the first **five** cells, showing at each step what `zipWith` had available.
- `bad = zipWith (+) bad (tail bad)` is `<<loop>>`. Explain the difference using the word **productive**.
- `fibs !! 1000` is instant and has 209 digits. **Write the same function as a recursive function
  without a list**, and say why that one is not instant. Give the complexity of each.

**(b) [7]** Hughes's separation.

- Report `within 1e-12 (sqrts 2)`, `relative 1e-12 (sqrts 2)`, and the Prelude's `sqrt 2`, with your own
  `relative`.
- Do the same for `sqrts 1e20`. **An absolute tolerance of 1e-12 on a number near 10¹⁰ succeeds.**
  Print enough of the sequence to explain why. *(The answer is about `Double`.)*
- **Construct a sequence for which the absolute rule does not terminate and the relative rule does**,
  and report the relative rule's answer. State roughly how many steps the absolute rule would need.

**(c) [6]** The famous `primes`.

- Measure `resources/sieve.hs` at *n* = 2,000, 10,000 and 20,000 for both versions. Six timings.
- **What does a real sieve do that the two-liner does not?** One sentence, and name the operation each
  one is dominated by.
- Fit the growth of each from your own numbers, and estimate the *n* at which the two-liner takes a
  minute.

---

### Q5: `sched` Under a Microscope (20 points)

**(a) [7]** Add to your `Stats.hs` a sixth statistic: the **mean** session duration.

- Do it so that the program still runs in constant space at `-O0`. Report `./stats strict 100000 +RTS
  -s` before and after.
- A mean needs a sum and a count, and you already have both. **Say why this is not the `lazyPair` bug
  from Q2** — or, if you wrote it in a way that is, fix it and report both numbers.

**(b) [7]** `histogram` from Lab 2 builds `[(Day, Int)]` with a `sum` per day.

- Rewrite it to accumulate into a `Data.Map.Strict Day Int` in one pass with `insertWith`.
- Now do the same with `Data.Map.Lazy`. **Measure both** on `stream 100000`. Report residency for each.
- **`Data.Map.Strict` is strict in its values and `Data.Map.Lazy` is not.** Say which of the two you
  would use for a counter and why, in terms of §Q1's definition of WHNF.

**(c) [6]** You now have three weeks of measurements on `sched`.

- Give the **one sentence** you would put at the top of `Sched.hs` to warn a future maintainer about the
  space behaviour of the statistics code.
- `+RTS -s` reports both *bytes allocated* and *maximum residency*. **Say which of the two you would
  put in a CI check**, and what threshold, and why the other one is the wrong choice.

---

## Marks

| Q | Topic | Parts | Points |
|---|---|---:|---:|
| 1 | Weak head normal form | 3 | 20 |
| 2 | The leak | 3 | 22 |
| 3 | Folds, explained | 3 | 18 |
| 4 | Infinite lists | 3 | 20 |
| 5 | `sched` under a microscope | 3 | 20 |
| | **Total** | **15** | **100** |

**Late work:** [[Year2 - Sophomore/COURSE POLICIES|COURSE POLICIES]] applies. **The lowest problem
set of the term is dropped.**

---

*PROG 202 · Week 3 · PS 3 · © CSE Department*
