# PROG 202 · Lab 2
## Refactoring an Imperative Loop Into Folds
### Week 2 · sat **Wednesday of Week 3**, 13:00–14:50, BH 215 · **unmarked, checked off in the session**

---

> **This lab covers Week 2** and is sat on the **Wednesday of Week 3**, after both of Week 2's lectures
> and Week 3's Tuesday lecture. **Lab *N* is sat on the Wednesday of Week *N+1*.**
>
> **Nothing here is marked.** The TA checks your work off in the session.
> [[Year2 - Sophomore/COURSE POLICIES|COURSE POLICIES]] costs you a letter grade after a second
> unexcused absence.

**What you are doing:** taking six functions written the way somebody who has just arrived from C would
write them — explicit recursion, hand-threaded accumulators, one of them appending inside a loop — and
replacing each body with `map`, `filter`, `foldr`, `foldl'` or `scanl`.

**Two rules, and they are the whole exercise.** You may not change a type signature, and **the output
must stay byte-identical.** `make check` enforces the second against a reference file, so you find out
immediately rather than at the checkoff.

**One of the six has a performance bug in it**, and it is not the one that looks worst.

---

## 0. Setup (8 minutes)

```bash
mkdir -p "$PROG202/week2/practice"
cd "$PROG202/week2/practice"
cp "$ACADEMICS/1. Sophomore/Spring/2. PROG 202 - Functional & Logic Programming/PROG202 Week2/lab/"{Sched.hs,Report.hs,Main.hs,Makefile,expected.txt} .
make check
```

**`make check` passes before you start**, because the code you have been given is correct. That is the
point: **this lab is a refactor, not a repair.** Everything you do today must keep it passing.

`Sched.hs` is last week's module, complete. `Main.hs` is the driver. **`Report.hs` is the only file you
edit.**

---

## 1. `totalMinutes` and `lectureCourses` (12 minutes) — TODOs 1 and 2

```haskell
totalMinutes :: [Session] -> Int
totalMinutes []     = 0
totalMinutes (t:ts) = duration t + totalMinutes ts
```

**One line, with a fold.** Which fold? Read L06 §3's table: the operator is `(+)`, which is strict in
its accumulator, so the answer is **`foldl'`** — and `sum . map duration` is also acceptable and
arguably better. Try both.

```haskell
lectureCourses :: [Session] -> [Course]
lectureCourses (t:ts) | kind t == LEC = course t : lectureCourses ts
                      | otherwise     =            lectureCourses ts
```

**A guard that keeps or drops is a `filter`. A per-element transformation is a `map`.** This one is
`map course . filter ((== LEC) . kind)` and if you have to look at L05 §4 to read `(== LEC) . kind`,
look at it — it is the idiom of the term.

`make check` after each. **Do not do all six and then build.**

---

## 2. `busiestDay` and `histogram` (25 minutes) — TODOs 3 and 4

These two are the real work, and they are in the wrong order on purpose: **do `histogram` first**, and
then `busiestDay` is one line over it.

### `histogram`

```haskell
histogram :: [Session] -> [(Day, Int)]
```

Minutes per day, **every day present**, Monday first. The given version has two nested hand-written
recursions. You want one comprehension over `[minBound .. maxBound]` with a `sum` inside it.

**`[minBound .. maxBound]` is the reason Week 1 derived `Bounded`.** Add `Sat` to `Day` and this
function picks it up with no edit.

### `busiestDay`

The day with the most minutes, **ties going to the earlier day**. With `histogram` in hand this is
`maximumBy` from `Data.List` and `comparing` from `Data.Ord`:

```haskell
busiestDay ts = fst (maximumBy (comparing snd) (histogram ts))
```

**Run `make check`. It passes.** Now read the next paragraph before you move on, because it does not
mean your code is right.

> **`maximumBy` keeps the *last* maximum on a tie.** The real timetable has no tie, so `make check`
> cannot tell you. Construct one and find out:
>
> ```
> ghci> import Data.List; import Data.Ord
> ghci> fst (maximumBy (comparing snd) [(Mon,100),(Tue,100),(Wed,50)])
> Tue
> ```
>
> **That is the wrong answer** — the spec says the earlier day. The fix is one word: `maximumBy
> (comparing snd) (reverse (histogram ts))`, which gives `Mon`. Check it.

**This is the most important thing in the lab and it is not about folds.** A test suite that only runs
the real data passes a function that is wrong, and it will keep passing until the day two courses tie.
**Week 11 is about generating the input that would have caught it**; today the point is only that
`make check` passing is not the same as being right.

---

## 3. `runningTotals` (10 minutes) — TODO 5

```haskell
runningTotals :: [Session] -> [Int]
```

`[50, 100, 150, …]` — the running total after each session. For `[]` the answer is `[]`.

**This is a fold that keeps every intermediate result, and it has a name.** Look up `scanl` and
`scanl1` in GHCi with `:t` and work out which you want, and what to do about the extra element `scanl`
produces.

```
ghci> scanl (+) 0 [1,2,3]
ghci> scanl1 (+) [1,2,3]
```

**One of those two has four elements where you want three.** Say which, and why it is there — it is not
an off-by-one error, it is the fold's starting value, and `scanl` is telling you the truth.

---

## 4. The One With the Bug (20 minutes) — TODO 6

```haskell
report :: [Session] -> [String]
report ts = go [] ts
  where
    go acc []     = acc
    go acc (x:xs) = go (acc ++ [render x]) xs
```

**It is correct. `make check` passes. And it is quadratic.**

`acc ++ [render x]` walks the whole accumulator on every step, so building an *n*-element list costs
O(n²) (L06 §5). With seventeen sessions that is 153 steps and you will never notice.

**Make yourself notice.** `Sched.hs` exports `timetable`; build a big list and time the two versions:

```haskell
-- in ghci, with your Report loaded
ghci> let big n = concat (replicate n ts)     -- ts from `Right ts <- pure timetable`
ghci> length (report (big 500))               -- 8500 sessions
```

Then measure it properly with the course's own program, which strips the problem to its bones:

```bash
cd "$ACADEMICS/1. Sophomore/Spring/2. PROG 202 - Functional & Logic Programming/PROG202 Week2/resources"
ghc -O2 -rtsopts -o append append.hs
./append left 40000      # 22.57 s here
./append right 40000     #  0.01 s here
```

**Reproduce both numbers**, then fix `report`. The fix is short enough to be an anticlimax, and that is
also the lesson: the whole `go`/`acc` apparatus existed only to do something `map` already does.

**Answer before the checkoff:** the accumulator version and `map` produce the same list. **Give the
sentence that explains why one is O(n) and the other O(n²)** without using the word "quadratic".

---

## 5. The Folds Themselves (20 minutes)

Now measure the thing the lectures claimed.

```bash
cd "$ACADEMICS/1. Sophomore/Spring/2. PROG 202 - Functional & Logic Programming/PROG202 Week2/resources"
ghc -O2 -rtsopts -o folds  folds.hs
ghc -O0 -rtsopts -o folds0 folds.hs
for k in foldr foldl "foldl'" sum; do ./folds  "$k" 10000000 +RTS -s 2>&1 | grep residency; done
for k in foldr foldl "foldl'" sum; do ./folds0 "$k" 10000000 +RTS -s 2>&1 | grep residency; done
```

**Fill in the eight numbers**, then answer:

**(a)** At `-O2`, `foldl` uses 44 KB and `foldr` uses 130 MB. At `-O0`, `foldl` uses 619 MB and `foldr`
uses 446 MB. **The ranking reverses.** Which one did the optimiser change, and what would you guess it
did? *(Week 3 confirms or corrects you.)*

**(b)** The textbook says `foldl` overflows the stack. **Nothing overflowed.** Now:

```bash
./folds0 foldl 10000000 +RTS -K16m
./folds0 foldr 10000000 +RTS -K16m
```

**Both overflow.** In one sentence: what was the received advice actually about?

**(c)** Finally, the case a finite list cannot show:

```bash
ghc -O2 -o short short.hs
for k in foldr foldl "foldl'"; do echo -n "$k: "; timeout 4 ./short "$k" || echo "(no answer)"; done
```

**`foldr` answers `True` on an infinite list and neither left fold ever will.** Say why, in terms of
which element is the *outermost* call.

---

## 6. Checkoff

Show the TA:

- [ ] `make check` passing with **all six bodies replaced** and no type signature changed
- [ ] Your `busiestDay` giving **`Mon`** for the constructed tie, and your explanation of why
      `make check` could not have told you (§2)
- [ ] `./append left 40000` and `./append right 40000`, your two timings, and your one-sentence
      explanation without the word "quadratic" (§4)
- [ ] The eight fold numbers from §5, and your answers to (a), (b) and (c)
- [ ] `./short foldr` printing `True`, and `./short foldl` printing nothing

---

## What Comes Next

**Week 3 explains every surprising number in this lab.** Why `foldl` is 619 MB at `-O0` and 44 KB at
`-O2`; why `foldr` can answer a question about an infinite list; what `seq` in `foldl'` actually does;
and what Week 0's 273 MB was. It is called *Lazy Evaluation* and it is the week this course turns on.

**Read Hughes's "Why Functional Programming Matters" before Tuesday.** Twenty-three pages, it is on the
final, and its argument is exactly the `foldr`-on-an-infinite-list result you just measured.

**Lab 3 is on the Wednesday of Week 4.**

---

*PROG 202 · Week 2 · Lab 2 · © CSE Department*
