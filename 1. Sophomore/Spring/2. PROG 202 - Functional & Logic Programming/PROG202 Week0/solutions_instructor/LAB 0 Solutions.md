# PROG 202 · Lab 0 · Solutions
## GHCi, and the Shape of a Haskell Program
### INSTRUCTOR ONLY — NOT FOR STUDENTS

---

**Session:** Friday of Week 0, 13:00–14:50, BH 215 · **Unmarked**, checked off in the session.

**What the session is really for.** Not Haskell — there is almost no Haskell written today. It is for
installing three habits that the next twelve weeks assume: **`:t` before you guess**, **`:sprint`
when you are confused about evaluation**, and **`+RTS -s` before you believe a performance claim.**
Students who leave without those spend Week 3 lost.

**Timing that works.** §0 ten minutes, §1 twenty, §2 twelve, §3 ten, §4 forty, §5 twelve, checkoff
five — **109 of the session's 110 minutes**, and the sheet is written to finish inside it with no
write-up to take away. §4 is the one that overruns; §5 is the one to cut if you are behind, because
PS 0 Q4(b) does its full table with marks attached.

---

## §0 — Toolchain

**Where they work.** `week0/practice/` in the semester submissions repo, which is git-ignored in
every week of every course. **Nothing from today is submitted** — PS 0 is Week 0's submitted work.
Check one student's `git check-ignore -v week0/practice/Shape.hs` out loud so the whole room sees the
rule named.

**The two failures you will actually see:**

1. **Mismatched `ghc` and `ghci`.** A student with a distribution GHC and a `ghcup` GHC on `PATH` in
   different orders. `ghc --version` and `ghci --version` disagreeing is the tell. Fix by putting
   `~/.ghcup/bin` first, or by uninstalling one.
2. **The path with spaces.** `cd $PROG202` without quotes. This bites at least two students per
   session and the error message (`cd: too many arguments`) does not say why.

BH 215 machines are correct out of the box: **GHC 9.4.7, SWI-Prolog 9.0.4, eight cores.**

---

## §1 — GHCi

### 1a

```
map      :: (a -> b) -> [a] -> [b]
(++)     :: [a] -> [a] -> [a]
words    :: String -> [String]
(.)      :: (b -> c) -> (a -> b) -> a -> c
($)      :: (a -> b) -> a -> b
3        :: Num a => a
3.5      :: Fractional a => a
length   :: Foldable t => t a -> Int
```

**Question 1 — `Num a => a`.** The literal `3` is *overloaded*: it stands for whatever numeric type
the surrounding expression requires, via `fromInteger`. Accept any answer that says "it has no type
of its own yet". Do **not** accept "it's an Int by default" — defaulting happens only when nothing
else determines it, and at the prompt.

**Question 2 — the trick.** *Which arrow returns the function?* **None of them, and all of them.**
`(b -> c) -> (a -> b) -> a -> c` is right-associative: it reads
`(b -> c) -> ((a -> b) -> (a -> c))`. There is no distinguished "return" arrow because **every
Haskell function of more than one argument already returns a function.** Students who say "the last
one" have not met currying yet; this is the moment to say the word, and L02 §5's `f x y = (f x) y`
is the follow-up.

**Question 3 — `Foldable`.** `:i Foldable` lists `Maybe`, `[]`, `Either a`, `(,) a`, and more.
`length (Just 3)` is `1`; `length ('x', 5)` is `1`. Both are surprising and both are correct, and
Week 4 §7 is where the argument about whether they should be goes.

### 1b

`Bool` has **six** instances here: `Bounded`, `Enum`, `Show`, `Read`, `Eq`, `Ord`. The point to make
aloud: *nothing in that output is compiler magic. Week 1 defines `Bool` in one line and Week 4
writes three of those six instances.*

### 1c — the one that matters

```
ghci> let xs = map (*2) [1..5] :: [Int]
ghci> :sprint xs
xs = _
ghci> length xs
5
ghci> :sprint xs
xs = [_,_,_,_,_]
ghci> sum xs
30
ghci> :sprint xs
xs = [2,4,6,8,10]
```

**The one-sentence answer you are listening for:** *`length` needs the spine and not the elements,
so only the cons cells were built.*

**Forcing only the last element:** `last xs` gives **`xs = [_,_,_,_,10]`** — the spine is fully
forced (it had to walk to the end, which is why `:sprint` can print it in `[…]` form at all) but
four of the five elements are still `_`. **`:sprint` uses the `[…]` notation only when the spine is
completely known**, and the `_ : _ : …` form otherwise; contrast `ys !! 3` in PS 0 Q3b, which gives
`ys = _ : _ : _ : 5 : _` because the spine beyond index 3 has not been forced.

**Common wrong answer:** "`length` evaluated the list". Push back: it evaluated the *structure*. If
`xs` were `map expensive [1..5]`, `length` would still be instant.

### 1d

`(0.02 secs, 88,074,288 bytes)`. Numbers vary; the allocation figure should be within a few percent
of 88 MB on any machine, because it is deterministic — it is **not** a timing.

---

## §2 — `Shape.hs`

### (a)

```haskell
total :: [(String, Int)] -> Int
total = sum . map snd
```

Accept `total t = sum (map snd t)`. If a student writes explicit recursion, accept it and say that
Week 2 is about why the point-free version is preferred — do not mark it wrong.

### (b)

```
Shape.hs:17:1: warning: [-Wmissing-signatures]
    Top-level binding with no type signature: busiest :: [(String, Int)] -> String
```

**The inferred type is the same one they deleted.** Worth saying: GHC inferred it *and told them what
it was*, so `-Wall` doubles as a way to ask "what type did I just write?".

### (c) — the exercise

**With the signature**, changing `snd` to `fst`:

```
Shape.hs:18:12: error:
    • Couldn't match type ‘Int’ with ‘[Char]’
      Expected: (Int, String) -> String
        Actual: (Int, String) -> Int
```

— blamed on line 18, the composition, which is where the mistake is.

**Without the signature**, the error moves to `main`, several lines away, and complains that
`putStrLn` was given an `Int`. **That is the whole lesson.** Type inference is global: with no
signature to stop it, the wrong type propagates until it meets something that disagrees, and the
line it is reported on is the *victim*, not the *culprit*.

> **Say this out loud, it is the reason for the course's style rule:** a type signature is not
> documentation that the compiler happens to check. It is a **firewall** that stops an error
> travelling. Write one on every top-level binding.

---

## §3 — `x = x + 1`

```
$ ghc -O0 -o loopx loopx.hs && ./loopx
loopx: <<loop>>
```

In `ghci` it hangs. Both behaviours are correct.

**Answers:**

1. **Not a type error** because `x :: Int` and `x + 1 :: Int` agree perfectly. The definition is
   well-typed and false. Haskell's `=` is a *recursive* definition, so `x` is defined in terms of
   itself, which is legal and useful (`ones = 1 : ones` in Week 3) and here has no solution.
2. **`<<loop>>` is printed by the runtime**, not the compiler. The RTS marks a thunk as a
   *blackhole* while it is being evaluated; entering a blackhole from the same thread means the
   value depends on itself.
3. **GHCi's bytecode interpreter does not blackhole the same way**, so nothing notices and it spins.
4. **A loop `<<loop>>` cannot catch:** `main = print (length [1..])`, or `f n = f (n+1)`. Neither
   re-enters a thunk under evaluation — each step creates a *new* thunk. Blackhole detection catches
   *self-reference*, not *non-termination*, and non-termination is undecidable.

**The hard bullet (PS 0 Q3d third point) if a student asks:** a blackhole can be entered by a
*different* thread legitimately — that is how GHC's `par` (Week 7) blocks a thread on a value another
thread is computing. In single-threaded code, entering a blackhole is always the loop; with threads,
`-feager-blackholing` can produce a false positive under contention. Nobody should reach this today.

---

## §4 — `sched`

### 4a — the boundary

```haskell
minutes :: Session -> Int
minutes (_, _, _, s, e) = e - s

overlaps :: Session -> Session -> Bool
overlaps (_, _, d1, s1, e1) (_, _, d2, s2, e2) = d1 == d2 && s1 < e2 && s2 < e1
```

**The four cases, which you should draw on the board:**

| Case | `s1 < e2` | `s2 < e1` | Overlap? |
|---|---|---|---|
| A entirely before B | ✓ | ✗ | no |
| A entirely after B | ✗ | ✓ | no |
| A ends exactly when B starts | ✓ | ✗ *(e1 = s2)* | no — correct |
| A contains B | ✓ | ✓ | **yes** |

**`<=` in either position breaks case 3 only.** That is why §4c still reports zero clashes with `<=`
— the timetable has no two real sessions that touch exactly — and why §4d's lunch check jumps from
two to five. **The bug is invisible until the data contains a touching pair.** Make that point: this
is what a boundary bug looks like in the wild, and it is why Week 11 generates inputs rather than
choosing them.

### 4b — `pairs`

```haskell
pairs :: [a] -> [(a, a)]
pairs xs = [ (x, y) | (i, x) <- zip [0 :: Int ..] xs
                    , (j, y) <- zip [0 ..] xs
                    , i < j ]
```

`length (pairs [1..10]) == 45`. The `:: Int` annotation on the first `zip` is needed or GHC defaults
`i` and `j` to `Integer` and `-Wall` says nothing — harmless, but the annotation is good practice.

**The O(n²) remark**, if anyone asks: yes, and 17 sessions is 136 pairs. Week 2 has the version that
sorts first and is O(n log n), as an exercise.

### 4c — `clashes`

```haskell
clashes :: [(Session, Session)]
clashes = [ (a, b) | (a, b) <- pairs timetable, overlaps a b ]
```

**Empty.** Seventeen sessions, 136 pairs, no collision. Say explicitly that this is the *expected*
result and that a checker which finds nothing is still doing its job — students distrust a program
that prints nothing.

### 4d — the finding

```haskell
lunchCollisions :: [Session]
lunchCollisions = [ t | d <- weekdays, t <- timetable, overlaps (lunch d) t ]
```

```
sessions         : 17
contact minutes  : 1070
clashes          :
lunch collisions :
  PROG 202 LEC Tue 11:00-12:15
  PROG 202 LEC Thu 11:00-12:15
```

**Both are this course's own lectures**, overrunning the protected hour by fifteen minutes, twice a
week, for thirteen weeks — **6.5 hours across the term.**

**Question 1 — the closest near-miss.** A three-way tie at **ten minutes**: MATH 251 → CS 202 on
Monday, CS 202 → CS 212 on Wednesday, CS 212 → PROG 202 on Tuesday. **No two real sessions touch
exactly**, which is the fact that hides the `<=` bug in 4c.

**Question 2 — 1,070 minutes.** By hand: five components at 150 (MATH 251 3×50, CS 202 3×50, CS 212
3×50, PROG 202 2×75, ECE 211 2×75), two at 110 (the two labs), two at 50 (MATH 251 recitation,
CS 290 seminar) = 750 + 220 + 100 = **1,070 = 17 h 50 min**. Students who get 1,020 have counted the
PROG 202 lectures at 50 minutes from habit.

**Question 3 — bug in the timetable or in the claim?** Both readings are defensible and **you should
not steer them to one.** The two good answers:

- *The claim is wrong.* "Protected" plainly means "no classes scheduled here", and one is. The grid
  is a summary; the authoritative row is the MASTER TIMETABLE's 11:00–12:15. Fix the prose.
- *The timetable is wrong.* Every other Spring session ends by 12:00 or starts at 13:00. PROG 202 is
  the single exception in seventeen, which is the signature of an oversight rather than a policy.

**The best answers notice that the grid itself displays PROG 202 in the 11:00 row and shows no
12:00 entry**, so the collision is invisible to a reader and visible only to a program. That is the
real lesson of the exercise and it is worth naming.

**Question 4 — `<=`.** Clashes stay at **0**; lunch collisions go from **2 to 5**, adding ECE 211
Monday 13:00, PROG 202 Lab Wednesday 13:00, and ECE 211 Friday 13:00 — all three of which *start* at
the moment lunch ends.

---

## §5 — `+RTS -s`

**The full matrix, measured on a BH 215 machine (GHC 9.4.7).** Have it on the board before they
start; they will get all eight and not know what to make of them.

| | `-O0` allocated | `-O0` residency | `-O2` allocated | `-O2` residency |
|---|---:|---:|---:|---:|
| `twice` | 1,600 MB | **44,328 B** | **52,944 B** | **44,328 B** |
| `named` | 880 MB | **244,958,408 B** | 640 MB | **272,645,056 B** |
| `once` | 880 MB | 44,328 B | 52,312 B | 44,328 B |

**(a) named but used once:** **44,328 bytes**, and at `-O2` only **52,312 bytes allocated** — the
list is not built at all. Most students predict 273 MB. **Naming is not what costs; naming *plus two
consumers that walk at different speeds* is.** With one consumer nothing is retained behind `sum`'s
cursor, and fusion still applies.

**(b) the two columns are two different phenomena, and this is the part to get right.**

- **The residency gap is not the optimiser's doing.** 44 KB against 245 MB is already there at
  `-O0`. It is **retention**: laziness plus GC stream a list nobody holds, and a name holds it.
  `-O2` neither creates nor fixes this — it makes it slightly *worse* (245 MB → 273 MB).
- **What `-O2` adds is fusion**, visible in the allocation column: 1,600 MB → 53 KB for `twice`.
  For `named`, fusion is impossible because the list is shared, so allocation only falls 880 →
  640 MB.

**If you say only one thing here, say this:** *fusion is an optimisation you can lose by giving
something a name.*

> **This paragraph replaces an earlier version of these notes that said the `-O2` gap was created by
> fusion.** It is not; the residency gap is present at `-O0` and fusion is a separate, allocation-side
> effect. The eight numbers above were re-measured. Mentioning that the notes were wrong is worth
> doing out loud — it is the course's own habit applied to itself.

**(c) the hypotheses.** For the first, anything of the shape *"both traversals need the list, so it
has to stay in memory"* is full credit. For the second, *"if nobody keeps the list, the compiler
needn't build it"* is full credit. Nobody has the vocabulary for *fusion* yet and they should not be
pushed toward it. Write the good ones on the board and leave them up — Week 3 L07 opens by returning
to them.

---

## Checkoff

Six items. **Be strict about two of them:**

- the `:sprint` explanation in §1c must be *spoken*, not shown — a student can produce
  `[_,_,_,_,_]` by typing and still not know what it means;
- the §5c hypothesis must be *written down*, because Week 3 asks them to compare it with what they
  believed then.

The rest is presence and a working build.

---

## After the Session

**There is no lab in Week 1.** Lab 1 is on the **Wednesday of Week 2** and covers Week 1.

**PS 0 is due the Friday of Week 1** and repeats §4 and §5 with marks attached. Students who
completed §5 today have already done Q4(b).

**Quiz 1 is Tuesday of Week 1**, ten minutes, covering Week 0.

---

*PROG 202 · Week 0 · Lab 0 Solutions · INSTRUCTOR ONLY · © CSE Department*
