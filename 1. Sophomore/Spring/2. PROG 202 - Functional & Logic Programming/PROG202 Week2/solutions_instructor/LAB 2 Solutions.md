# PROG 202 · Lab 2 · Solutions
## Refactoring an Imperative Loop Into Folds
### INSTRUCTOR ONLY — NOT FOR STUDENTS

---

**Session:** Wednesday of Week 3, 13:00–14:50, BH 215 · **Unmarked**, checked off in the session.

**What the session is really for.** Two things, and the second is not about folds.

The first is mechanical: six loops become six combinators, and the students should leave able to see
`map`, `filter` or a fold in a hand-written recursion without thinking about it.

**The second is §2's tie.** `busiestDay` written the obvious way passes `make check` and is wrong.
Nothing in the lab's own test data can reveal it. **A student who leaves understanding that a passing
test suite is evidence about the inputs you chose, not about the function, has had the more valuable
half of the session** — and it is the on-ramp to Week 11.

**Timing.** §0 8 · §1 12 · §2 25 · §3 10 · §4 20 · §5 20 · checkoff 10 = **105 minutes.** §5 is the
one to cut if behind, because PS 2 Q3 does it with marks.

**Reference solution:** `ReportSol.hs` in this directory.

---

## §0 — Setup

**`make check` passes before they start.** Say this out loud; some students will assume the given code
is broken and start debugging it. It is correct, and correctness is the constraint, not the goal.

---

## §1 — `totalMinutes`, `lectureCourses`

```haskell
totalMinutes :: [Session] -> Int
totalMinutes = foldl' (\acc t -> acc + duration t) 0
-- or:      = sum . map duration

lectureCourses :: [Session] -> [Course]
lectureCourses = map course . filter ((== LEC) . kind)
```

**Accept `sum . map duration` and prefer it.** If asked which is better: `sum . map duration` says what
it means and fuses to the same loop; the explicit `foldl'` is what you write when the combining step is
not already a named function.

**The mistake to expect:** `foldr (+) 0 . map duration`. It is correct and, on seventeen sessions,
indistinguishable. Do not let it pass without naming it — L06 §3's table says `foldr` with a strict
operator is the 130 MB row, and this is the moment the table becomes personal.

**`(== LEC) . kind`** will need explaining to about a third of the room. Draw it: `kind` takes the field
out, `(== LEC)` compares, `.` glues. The Python they are translating from is `lambda t: t.kind == LEC`.

---

## §2 — `histogram` and `busiestDay`, and the tie

```haskell
histogram :: [Session] -> [(Day, Int)]
histogram ts = [ (d, minutesOn d) | d <- [minBound .. maxBound] ]
  where minutesOn d = sum [ duration t | t <- ts, day t == d ]
```

**Expected:** `[(Mon,175),(Tue,285),(Wed,260),(Thu,175),(Fri,175)]`, summing to 1,070.

Point at `[minBound .. maxBound]`: Week 1 derived `Bounded` for this line, and adding `Sat` to `Day`
needs no edit here.

**It is O(days × sessions)** — five passes over seventeen. Nobody cares, and a student who builds a
`Data.Map` instead has done something better and should be told so, and told that Week 4 gives them the
vocabulary for why.

### The tie — this is the section that matters

```haskell
-- what they will write, and it passes make check:
busiestDay ts = fst (maximumBy (comparing snd) (histogram ts))
```

**Measured, on a constructed tie:**

```
ghci> fst (maximumBy (comparing snd) [(Mon,100),(Tue,100),(Wed,50)])
Tue
```

**`maximumBy` keeps the *last* maximum.** `Data.List.maximumBy` folds with "if the comparison is `GT`
keep the old, otherwise take the new", so equal elements take the new one. The spec says the earlier
day, so this is wrong.

**The fix:**

```haskell
busiestDay ts = fst (maximumBy (comparing snd) (reverse (histogram ts)))
```

```
ghci> fst (maximumBy (comparing snd) (reverse [(Mon,100),(Tue,100),(Wed,50)]))
Mon
```

**Run both in front of the room.** The `reverse` is load-bearing and looks like noise, which is exactly
why it gets deleted by the next person to touch the file.

> **The speech to give, and keep it to four sentences.** `make check` passes for both versions, because
> the real timetable has no tie — the closest two days are 175 and 175, which *is* a tie, so check that
> too. *(It is: Mon, Thu and Fri all have 175. The tie is only invisible at the **maximum**, where Tue
> is alone on 285.)* So the function is wrong and the suite is green, and it will stay green until the
> day two courses move. **Week 11 generates the input that would have caught this on the first run.**

**Accept any correct alternative:** `minimumBy (comparing (negate . snd))`, a `foldl'` that keeps the
first maximum explicitly, or `head (sortOn (negate . snd) (histogram ts))` — `sortOn` is stable, so this
one is correct without a `reverse` and is the nicest answer. A student who finds it has understood
stability and should be told that is what they found.

---

## §3 — `runningTotals`

```haskell
runningTotals :: [Session] -> [Int]
runningTotals = tail . scanl (+) 0 . map duration
```

**Expected:** `[50,100,150,200,250,300,350,400,450,525,600,675,750,860,970,1020,1070]` — seventeen
entries ending at 1,070.

**The extra element.** `scanl (+) 0 [1,2,3]` is `[0,1,3,6]` — **four entries for three inputs**, because
the first is the *starting value* before anything has been added. That is not an off-by-one error;
`scanl` is reporting the accumulator at every step including step zero.

**Two fixes, and one of them is a trap:**

| | `[]` | correct? |
|---|---|---|
| `tail . scanl (+) 0` | `tail [0]` = `[]` ✓ | **yes** |
| `scanl1 (+)` | `[]` ✓ | **yes** |
| `tail . scanl1 (+)` | `tail []` → **exception** | **no** |

**The third is what a student gets by combining both hints**, and it passes `make check` because the
timetable is never empty. Ask the room to try `runningTotals []` in GHCi. It is the same lesson as §2,
twenty minutes later, and the repetition is deliberate.

---

## §4 — The One With the Bug

```haskell
report :: [Session] -> [String]
report = map render
```

**That is the whole fix**, and the anticlimax is the point: the `go`/`acc` apparatus existed only to do
what `map` does.

**The measurement they must reproduce:**

```
./append left 40000      22.57 s
./append right 40000      0.01 s
```

with 1.17 s and 4.93 s at 10,000 and 20,000 — ratios 4.2 and 4.6, quadratic.

**The sentence, without the word "quadratic" [the graded part]:** *`++` walks its whole left argument
every time, so adding the tenth element re-walks nine, the hundredth re-walks ninety-nine, and building
the list costs the sum of all the lengths it passed through.*

**Accept anything with "re-walks what it has already built".** Reject "because `++` is slow" — `++` is
not slow; it is O(1) in its right argument, and `x : acc` is the same operation done the other way
round.

**If time allows**, the third fix is worth thirty seconds: build backwards with `:` and `reverse` once.
Ask why `reverse` at the end is fine when `++` in the loop is not. *(One O(n) pass against n of them.)*

---

## §5 — The Folds

All eight numbers are in L06 §3. Have them on the board.

**(a)** `-O2`: `foldl` 44 KB beats `foldr` 130 MB. `-O0`: `foldr` 446 MB beats `foldl` 619 MB.
**The optimiser changed `foldl`**, by 4 orders of magnitude, and left `foldr` merely 3.5× better.

Any hypothesis of the shape *"`-O2` noticed the accumulator is always needed and evaluated it as it
went"* is correct and is **strictness analysis**. Do not give them the name unless they get there; Week 3
L07 §4 does.

**(b)**

```
$ ./folds0 foldl 10000000              -- 619 MB resident, 3.28 s, no crash
$ ./folds0 foldl 10000000 +RTS -K16m
folds0: Stack space overflow: current size 33624 bytes.
$ ./folds0 foldr 10000000 +RTS -K16m
folds0: Stack space overflow: current size 33624 bytes.
```

**The two-sentence answer:** the advice was about **strictness, not direction** — for an operator that
is strict in its accumulator, neither fold is safe, and what saves you is forcing as you go
(`foldl'`), not choosing a side. The "stack overflow" in the books describes a default that has
changed: GHC's stack now lives on the heap and grows to 80% of it, so the same bug presents as 619 MB
rather than an exception.

**Make the point about what that costs a learner.** A student who knew the rule and not the measurement
would see a 619 MB program that did not crash and conclude `foldl` was fine.

**(c)** `foldr` answers `True`; both left folds never terminate.

**The answer wanted:** `foldr`'s **outermost** application is the *first* element — `f x1 (foldr f z
rest)` — so if `f` ignores its second argument, the rest is never examined. `foldl`'s outermost
application involves the *last* element, so it cannot produce anything at all until it has reached the
end of the list, and `[1..]` has no end.

---

## Checkoff

Five items. **Be strict about two:**

- §2's tie must be *demonstrated*, not described, and their fixed `busiestDay` must give `Mon`.
- §4's sentence must avoid the word "quadratic". It is a small constraint and it forces the mechanism.

---

## After the Session

**PS 2 is due the Friday of Week 3** and repeats §4 and §5 with marks. Q2(a) asks for `myReverse` as
both a `foldr` and a `foldl'` and measures both — **the `foldr` version is 25.3 s at n = 40,000 against
0.01 s**, which is §4's lesson landing on Hutton's own `reverse` from §7.3.

**Quiz 3 is the Tuesday of Week 3** and covers this week.

**Week 3 explains every number in this lab.** Tell them so, and tell them to read Hughes before Tuesday
— the `foldr`-on-`[1..]` result in §5(c) is that paper's central example, and it reads completely
differently once you have measured it yourself.

---

*PROG 202 · Week 2 · Lab 2 Solutions · INSTRUCTOR ONLY · © CSE Department*
