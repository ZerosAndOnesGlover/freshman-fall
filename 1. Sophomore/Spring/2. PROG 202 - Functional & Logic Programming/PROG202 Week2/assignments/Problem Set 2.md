# PROG 202 · Problem Set 2
## Higher-Order Functions, Folds, and What They Cost

---

**Released:** Week 2, Wednesday · **Due:** Week 3, Friday 17:00
**Total: 100 points** · Submit one PDF, `PS2_{LastName}_{StudentID}.pdf`, plus your `.hs` files in a
tarball `PS2_{LastName}.tar.gz`

> **About three hours.** Five questions, fifteen parts.
>
> **State your `ghc --version` and `uname -r`.** Q3 and Q4 are measurements and every number must come
> from a binary built with `ghc -O2` — or `-O0` where the question says so. **No timing from `runghc`
> or `ghci`**, which is the rule PS 0 Q4(a) existed to establish.
>
> **Every `.hs` file compiles clean under `ghc -Wall -O2`.**

---

### Q1: Reading Higher-Order Types (18 points)

**(a) [7]** Predict the type, then check with `:t`, and report both.

| Expression | Your prediction | `:t` says |
|---|---|---|
| `map map` | | |
| `zipWith const` | | |
| `uncurry (+)` | | |
| `filter . (==)` | | |
| `(.) . (.)` | | |

Two of the five are genuinely useful. Say which, and what for.

**(b) [5]** `add :: Int -> Int -> Int`.

- Write out `add`'s type with every bracket made explicit.
- What is the type of `add 3`, and what is the type of `add 3 4`?
- **`map (add 3) [1,2,3]` needs no lambda and no helper.** Explain why, in terms of what `add`'s type
  says it takes.
- Give an expression of type `[Int] -> [Int]` that adds 3 to every element, **without** using `add`,
  a lambda, or a named helper.

**(c) [6]** `(- 1)` is not the "subtract one" section.

- What is `(- 1)`? Check with `:t` and report it.
- What does `map (- 1) [1,2,3]` do, and why?
- Give **two** correct ways to write "subtract one" as a section or partial application.
- This is the only place in the language where an operator is irregular. Say what the irregularity is.

---

### Q2: Writing Folds (22 points)

**(a) [8]** Define each of these **as a single `foldr`**, with no explicit recursion and no other list
function:

```haskell
myMap    :: (a -> b) -> [a] -> [b]
myFilter :: (a -> Bool) -> [a] -> [a]
myLength :: [a] -> Int
myReverse :: [a] -> [a]
```

Then define `myReverse` **again** as a `foldl'`. **One of your two `myReverse`s is O(n) and the other
is O(n²).** Say which before you measure, then measure both at *n* = 20,000 and 40,000 and report four
timings.

**(b) [8]** Evaluate by hand, showing every step, then check:

1. `foldr (-) 0 [1,2,3]`
2. `foldl (-) 0 [1,2,3]`
3. `foldr (:) [] [1,2,3]`
4. `foldl (flip (:)) [] [1,2,3]`

Then: **the universal property of `foldr`** says any function defined by

```haskell
g []     = z
g (x:xs) = f x (g xs)
```

is `foldr f z`. Use it to show that `foldr (:) [] = id`, and to rewrite `sum . map (* 2)` as a single
`foldr` with no `map` in it.

**(c) [6]** `and = foldr (&&) True`.

- Why is `foldr` the right fold here? Answer in terms of which element is the **outermost** call.
- What does `and (repeat False)` do with `foldr`, with `foldl`, and with `foldl'`? **Run all three
  with a timeout and report exactly what you see.** Two of the three do the same thing and it is not a
  hang — you have seen it before, in Week 0.
- Give a different operator for which `foldl'` is correct and `foldr` is a mistake, and say why.

---

### Q3: Measuring the Folds (22 points)

**(a) [10]** Build `resources/folds.hs` at **both** `-O2` and `-O0`, and fill in all eight cells for
*n* = 10,000,000 using `+RTS -s`:

| | `-O2` residency | `-O2` time | `-O0` residency | `-O0` time |
|---|---|---|---|---|
| `foldr (+) 0` | | | | |
| `foldl (+) 0` | | | | |
| `foldl' (+) 0` | | | | |
| `sum` | | | | |

- **The ranking of `foldr` and `foldl` reverses between the two levels.** State the two rankings.
- Which row is unchanged across all four cells, and why does that make it the right default?

**(b) [6]** The textbook says `foldl` overflows the stack on a long list. **It does not here.**

- Report what `./folds0 foldl 10000000` actually does, with its residency.
- Now run it with `+RTS -K16m`, and run **`foldr`** the same way. Report both.
- **In two sentences: what was the received advice actually about?** Your answer should explain why
  `foldr` overflows too.

**(c) [6]** `foldl'` differs from `foldl` by a `seq`.

- Write out both definitions.
- Explain what `seq a b` does, and what it does **not** do. *(One sentence each. The second sentence
  is the one people get wrong.)*
- The `-O2` `foldl` figure is 44 KB, which is what `foldl'` gives. **Name the compiler pass that most
  likely did that**, and say why it cannot be relied on. *(Week 3 confirms this; a hypothesis
  consistent with your table is full marks.)*

---

### Q4: `++`, and the Four-Line `qsort` (20 points)

**(a) [7]** Reproduce `resources/append.hs`:

| *n* | `left` | `right` |
|---:|---|---|
| 10,000 | | |
| 20,000 | | |
| 40,000 | | |

- Confirm the growth is quadratic from your own three numbers, showing the ratios.
- `(++)`'s definition is two lines. **Quote it, and point at the character that makes it O(n) in its
  left argument and O(1) in its right.**
- Give the fix, and say what the fix costs.

**(b) [7]** Reproduce `resources/qsort.hs` on 1,000,000 pseudo-random `Int`s at `-O2`:

| | allocated | maximum residency | time |
|---|---|---|---|
| `qsort` | | | |
| `Data.List.sort` | | | |

**The four-liner is faster.** Say why that is not a reason to use it, using (c)'s measurement as the
evidence.

**(c) [6]** Now give both the *already-sorted* input `[1..n]`:

| *n* | `qsort` | `Data.List.sort` |
|---|---|---|
| 10,000 | | |
| 20,000 | | |
| 40,000 | | |

- Your three `qsort` numbers grow **faster than quadratic**. Give the two ratios and one sentence on
  where the extra comes from.
- `Data.List.sort` does 1,000,000 ascending elements in under a quarter of a second. **Why?** One
  sentence about the algorithm.
- Hutton's function is called `qsort` and is not quicksort. **Name two properties of real quicksort it
  does not have.**

---

### Q5: `sched`, Folded (18 points)

Start from your Lab 2 `Report.hs`.

**(a) [6]** Report your six replaced bodies, and for each name the function you used (`map`, `filter`,
`foldl'`, `scanl`, …).

For `runningTotals`: `scanl (+) 0` gives one element too many and `scanl1 (+)` does not. **Explain
where the extra element comes from**, and say what each does on the empty list — one of the two obvious
fixes crashes there and the other does not.

**(b) [6]** `busiestDay` must break ties toward the earlier day.

- `maximumBy (comparing snd) (histogram ts)` passes `make check`. **Show that it is nevertheless
  wrong**, by constructing a tie and reporting the answer.
- Give the one-word fix and show it gives `Mon`.
- **`make check` passed a wrong function.** In two sentences, say what kind of test would have caught
  it, and why the real timetable never could.

**(c) [6]** Add to `Report.hs`:

```haskell
gaps :: Day -> [Session] -> [(Minutes, Minutes)]
```

the free intervals on one day between 08:00 and 18:00, built with `sortOn`, `zip` and a fold or
comprehension — **no explicit recursion.** Report Wednesday's.

Then say which of `foldr` and `foldl'` you used and why, and what your function does for a day with no
sessions at all.

---

## Marks

| Q | Topic | Parts | Points |
|---|---|---:|---:|
| 1 | Reading higher-order types | 3 | 18 |
| 2 | Writing folds | 3 | 22 |
| 3 | Measuring the folds | 3 | 22 |
| 4 | `++` and `qsort` | 3 | 20 |
| 5 | `sched`, folded | 3 | 18 |
| | **Total** | **15** | **100** |

**Late work:** [[Year2 - Sophomore/COURSE POLICIES|COURSE POLICIES]] applies. **The lowest problem
set of the term is dropped.**

---

*PROG 202 · Week 2 · PS 2 · © CSE Department*
