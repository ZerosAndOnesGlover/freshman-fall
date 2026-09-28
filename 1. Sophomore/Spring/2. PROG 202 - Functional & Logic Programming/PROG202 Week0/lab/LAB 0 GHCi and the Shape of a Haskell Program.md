# PROG 202 · Lab 0
## GHCi, and the Shape of a Haskell Program
### Week 0 · sat **Friday of Week 0**, 13:00–14:50, BH 215 · **unmarked, checked off in the session**

---

> **This lab covers Week 0** and is sat on the **Friday that closes the ten-day Week 0**, after both
> of this week's lectures. From Lab 1 onwards this course's labs are on **Wednesdays and cover the
> previous week** — Lab *N* is sat on the Wednesday of Week *N+1*. There is **no lab in Week 1**.
>
> **13:00 is this course's ordinary lab time, on an unusual day.** Every Year 2 course holds its
> Week 0 lab on this Friday; CS 202 has the morning, 10:00–11:50 in BH 210, and BH 215 is free all
> afternoon. It happens once — every other lab in this course is a Wednesday.
>
> **Nothing here is marked.** The TA checks your work off in the session.
> [[Year2 - Sophomore/COURSE POLICIES|COURSE POLICIES]] costs you a letter grade after a second
> unexcused absence, which is the only enforcement there is and the only one needed.

**What you are doing:** learning to *look* at a Haskell program. Not to write one — you will write
about forty lines today and most of them are one line each — but to interrogate it: what type is
this, what has been computed so far, how much did it allocate, and what is the compiler refusing to
believe.

**And you will find a real bug in the university's own timetable.** It is in
[[Year2 - Sophomore/SPRING SCHEDULE|SPRING SCHEDULE]], it has been there all along, and it concerns
this course. Part 4 is where your program prints it.

---

## 0. Before You Start — the Toolchain and Where You Work (10 minutes)

BH 215 runs **Ubuntu 24.04, GHC 9.4.7, SWI-Prolog 9.0.4**, eight cores. On your own machine:

```bash
ghc --version                  # 9.4.x here; 9.2+ is fine for everything before Week 7
ghci --version
swipl --version                # not needed until Week 8.  Check it now anyway
```

**`ghc` and `ghci` must be the same version.** If `ghci` is 8.x and `ghc` is 9.x you have two
installations and you will spend Week 3 debugging the wrong one.

**Where you work.** Not your home directory. Submitted work for this course lives in the semester
submissions repository, at
`5. Academic Registry/4. Submissions/Year2 Sophomore/Spring/2. PROG 202/week0/`. **The repository is
the semester, not the course** — one repo for all six Spring courses — and it is kept out of the
vault's own git repo deliberately.

Name the path once in `~/.bashrc`:

```bash
export ACADEMICS=~/"Documents/1. Academics/0. Computer Science and Engineering (B.Sc)"
export PROG202="$ACADEMICS/5. Academic Registry/4. Submissions/Year2 Sophomore/Spring/2. PROG 202"
```

**Each `weekN/` has a `practice/` folder, and today's work goes there.** `practice/` is git-ignored
in every week of every course: it is for classwork, experiments and things you break on purpose, and
it is never submitted. Anything meant for grading goes in `weekN/` itself.

```bash
mkdir -p "$PROG202/week0/practice"
cd "$PROG202/week0/practice"
cp "$ACADEMICS/1. Sophomore/Spring/2. PROG 202 - Functional & Logic Programming/PROG202 Week0/lab/"{Shape.hs,Sched.hs,Makefile} .
make                           # builds `shape` and `sched`, both warning-clean
./shape                        # prints one course code
```

**Quote every `"$PROG202"`.** The path contains spaces; unquoted it splits into six arguments.

**Check that `practice/` really is ignored** before you rely on it:

```bash
cd "$PROG202"
git check-ignore -v week0/practice/Shape.hs      # should name the .gitignore rule
```

---

## 1. GHCi Is the Laboratory (20 minutes)

Start `ghci` with no arguments and work through this. **Type it, do not read it** — the point of the
session is that your fingers learn `:t`.

### 1a. `:t` everything

```
ghci> :t reverse
ghci> :t (++)
ghci> :t words
ghci> :t (.)
ghci> :t ($)
ghci> :t map
ghci> :t 3
ghci> :t 3.5
ghci> :t length
```

**Write down the answer to three questions before you move on.**

1. `:t 3` prints `3 :: Num a => a`, not `3 :: Int`. What is the `Num a =>` part, and what does it
   mean that the literal has no type of its own? *(Week 4. Guess now.)*
2. `(.)` has the type `(b -> c) -> (a -> b) -> a -> c`. **It returns a function.** Which of the three
   arrows in that type is the one that "returns" it? *(It is a trick question and the answer is the
   most useful fact in Week 2.)*
3. `:t length` here says `length :: Foldable t => t a -> Int`, not `[a] -> Int`. Find one type other
   than a list that you can call `length` on, using `:i Foldable`.

### 1b. `:i` and the fact that nothing is built in

```
ghci> :i Bool
ghci> :i Maybe
ghci> :i []
ghci> :i (&&)
```

**`Bool` is an ordinary data type with two constructors, defined in a library.** So is `Maybe`. So,
almost, is the list. Note down how many instances `Bool` has; Week 4 is about that list.

### 1c. `:sprint` — seeing what has *not* happened

This is the command that makes GHCi worth having, and it is the one you will still be using in
Week 11.

```
ghci> let xs = map (*2) [1..5] :: [Int]
ghci> :sprint xs
ghci> length xs
ghci> :sprint xs
ghci> sum xs
ghci> :sprint xs
```

You should see, in order: `xs = _`, then `xs = [_,_,_,_,_]`, then `xs = [2,4,6,8,10]`.

**Explain the middle one to the person next to you before you go on.** `length` returned 5 without
evaluating a single element. It knew how many cells there were and nothing about what was in them.
If you can say *why* in one sentence, you have understood Week 3 four weeks early.

Now find an expression that forces **only the last element**, and check with `:sprint`.

### 1d. `:set +s` — the second instrument

```
ghci> :set +s
ghci> sum [1..1000000::Int]
500000500000
(0.02 secs, 88,074,288 bytes)
```

**88 megabytes to add up a million numbers.** Not a leak — allocated and immediately reclaimed. Get
used to the number being large; get used to reading it.

---

## 2. The Shape of a Program (12 minutes)

Open `Shape.hs`. It is fifteen lines and L02 §1 walks through every one of them.

```bash
runghc Shape.hs                        # interpreted
ghc -Wall -O2 -o shape Shape.hs        # compiled.  Must be silent
./shape
```

**Tasks:**

**(a)** Add a function `total :: [(String, Int)] -> Int` that sums the minutes column, and print it
from `main`. Do it **without** writing a recursive function — `map` and `sum` are enough.

**(b)** Delete the type signature of `busiest` and recompile with `-Wall`. Two things happen: it
still compiles, and you get a warning. Write down both, and then ask `ghci` for the inferred type
with `:t busiest`. Is it the type you removed?

**(c)** Now break it: change `snd` to `fst` in `busiest` and recompile. **Read the error message
carefully** and write down which line number it blames. Then put `snd` back, remove the signature
*as well*, break it again, and compare. **This is the exercise.** A missing signature moves the
error from the line with the mistake to some line that merely disagrees with it, possibly in another
function entirely.

**(d)** In `ghci`, `:l Shape.hs` and then `:t busiest`, `:t minutes`, `:t main`. Then edit the file
in another window and type `:r`.

---

## 3. `x = x + 1` (10 minutes)

Put these two lines in `loopx.hs`:

```haskell
main :: IO ()
main = do
  let x = x + 1 :: Int
  print x
```

```bash
ghc -O0 -o loopx loopx.hs && ./loopx
```

You get:

```
loopx: <<loop>>
```

**Now type the same two lines into `ghci`.** It hangs; kill it with Ctrl-C.

**Write down the answers:**

1. Why is this not a type error? `x` and `x + 1` are both `Int`.
2. What is `<<loop>>`, and which component printed it — the compiler or the runtime?
3. Why does the compiled program detect it and `ghci` not? *(The word you want is **blackhole**.
   `ghci`'s bytecode interpreter does not install them the same way.)*
4. `<<loop>>` is not a general non-termination detector — nothing can be one. Write a
   non-terminating Haskell program that it does **not** catch. *(One line.)*

---

## 4. `sched` — the Course's Running Example (40 minutes)

Open `Sched.hs`. It holds the **real Year 2 Spring timetable**: seventeen sessions, taken from
[[Year2 - Sophomore/SPRING SCHEDULE|SPRING SCHEDULE]], as a list of five-tuples. There are five
`TODO`s and each is one to four lines.

> **The tuples are the wrong tool and you are using them on purpose.** `Session` is
> `(String, String, String, Int, Int)` — three strings in a row, and nothing stops you passing the
> day where the course goes. Week 1 L03 opens by replacing this type, and the replacement makes
> today's most likely bug impossible to write. Make the bug first.

### 4a. `minutes` and `overlaps` (TODOs 1 and 2)

`minutes` is a pattern match on a tuple. `overlaps` is the interesting one:

**Two sessions overlap when they are on the same day and their intervals intersect.** The subtlety is
the boundary. PROG 202's lab ends at 14:50 and MATH 251's recitation starts at 15:00 — those do not
overlap. But if the lab ended at 15:00 they still would not: **a session that ends exactly when
another starts is not a clash.**

The condition is `s1 < e2 && s2 < e1`. Convince yourself it is right by testing the four cases —
before, after, touching, containing — and note that **`<=` in either place gives the wrong answer**
for touching sessions.

### 4b. `pairs` (TODO 3)

Every unordered pair, each once. `pairs [1,2,3]` is `[(1,2),(1,3),(2,3)]` — three, not six, and no
`(1,1)`.

The idiom is a list comprehension with two generators and a guard, and the trick is getting an index
to compare. `zip [0..] xs` pairs each element with its position.

**Check it in `ghci` before you use it**: `length (pairs [1..10])` should be 45.

### 4c. `clashes` (TODO 4)

One line, given `pairs` and `overlaps`. Run it.

**You should get nothing.** The timetable has no clashes: seventeen sessions and not one collision.
That is a real fact about the registry's schedule and it is good news.

### 4d. `lunchCollisions` (TODO 5) — the bug

[[Year2 - Sophomore/SPRING SCHEDULE|SPRING SCHEDULE]]'s grid marks **12:00–13:00 every weekday** as
`🍽️ Lunch Break (protected — no classes scheduled)`, and the Monday breakdown says in as many words:
*"Lunch Break (protected — schedule this, do not skip it)"*.

`lunch d` is a pseudo-session for that hour. Find every real session that overlaps one.

Run it. You get:

```
sessions         : 17
contact minutes  : 1070
clashes          :
lunch collisions :
  PROG 202 LEC Tue 11:00-12:15
  PROG 202 LEC Thu 11:00-12:15
```

**Both collisions are this course's own lectures.** PROG 202 meets Tuesday and Thursday 11:00–12:15,
and the protected hour starts at 12:00, so twice a week this course runs fifteen minutes into a slot
the timetable says is protected. **Thirty minutes a week, for thirteen weeks.**

Nobody noticed because nobody ran the check. Reading the grid, the 11:00 row and the 12:00 row look
adjacent; only the end time gives it away, and the end time is in a different file.

**Answer these before the checkoff:**

1. **Which other session comes closest to a collision without being one?** Find it with your own
   code, not by eye.
2. The `contact minutes` figure is **1,070 — seventeen hours fifty minutes a week.** Check it by
   hand against the grid. Does your arithmetic agree, and if not, which of you is wrong?
3. **Is this a bug in the timetable or a bug in the claim?** Both readings are defensible. Write one
   sentence for each, and say which you would send to the registrar.
4. Your `overlaps` decided this. If you had written `<=` instead of `<`, how many *more* lines would
   have printed? Change it, run it, and put it back.

---

## 5. `+RTS -s`, and the Number That Should Bother You (12 minutes)

`make stats` runs `./sched +RTS -s`. Read the report; find `bytes allocated in the heap`, `maximum
residency`, and `%GC time`.

Now the measurement from L02 §6, in your own hands. Put both of these in one file and run each:

```haskell
main = print (sum [1..10000000::Int], length [1..10000000::Int])   -- written twice
main = let xs = [1..10000000::Int] in print (sum xs, length xs)    -- named once
```

```bash
ghc -O2 -rtsopts -o a A.hs && ./a +RTS -s
```

| `-O2` | allocated | maximum residency |
|---|---:|---:|
| written twice | **53 KB** | **44 KB** |
| named once | 640 MB | **273 MB** |

**Reproduce both rows.** Then:

**(a)** Try a third version: `let xs = [1..10000000] in print (sum xs)` — named, but used **once**.
Predict the residency before you run it, then run it. **Most people predict wrong.**

**(b)** Rebuild the *written-twice* version at `-O0` and report its **allocated** figure. It is not
53 KB. That one extra number is the whole of §5.

*(PS 0 Q4(b) fills in the full nine-cell table for marks. Do not do it now — do it there.)*

**(c)** In one sentence each, and without looking anything up:

- **why does giving the list a name cost 273 MB?**
- **why does `-O2` take the written-twice version's allocation from 1,600 MB to 53 KB**, and why can
  it not do the same for the named one?

Your two sentences are the hypotheses Week 3 will test. Write them down; you will be asked to compare
them with what you believe then.

---

## 6. Checkoff

Show the TA:

- [ ] `ghci` open, with a `:sprint` showing `[_,_,_,_,_]` and an explanation of it (§1c)
- [ ] `Shape.hs` compiling `-Wall`-clean with your `total` function, and your written note on where
      the error moved to when the signature was missing (§2c)
- [ ] `./loopx` printing `<<loop>>`, and your one-line program that loops without being caught (§3)
- [ ] `./sched` printing **1070 contact minutes, no clashes, and the two PROG 202 lunch
      collisions** (§4d)
- [ ] Your answer to §4d question 3 — timetable bug or claim bug — in one sentence each way
- [ ] Both residency figures from §5 and the `-O0` allocation figure from §5b, measured on your
      own machine, and your two hypotheses from §5c

**Nothing to commit today.** Everything you wrote is in `week0/practice/`, which is git-ignored on
purpose. **PS 0 is the submitted work for Week 0**, and its answer sheet and code go in `week0/`
itself — see the course README in the submissions repo.

---

## What Comes Next

**Week 1 replaces `Session`.** Three `String`s in a row is a type that lets you write
`("Tue", "PROG 202", "LEC", ...)` and get no complaint until the output is wrong. Algebraic data
types make that arrangement unrepresentable, and pattern matching makes the compiler tell you when
you have forgotten a case. `Sched.hs` is the first thing Week 1 rewrites.

**Lab 1 is on the Wednesday of Week 2**, not next week. There is no lab in Week 1.

---

*PROG 202 · Week 0 · Lab 0 · © CSE Department*
