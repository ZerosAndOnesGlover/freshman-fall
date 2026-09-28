# PROG 202 · Lab 3
## Watching Laziness: Thunks, Space Leaks, and `seq`
### Week 3 · sat **Wednesday of Week 4**, 13:00–14:50, BH 215 · **unmarked, checked off in the session**

---

> **This lab covers Week 3** and is sat on the **Wednesday of Week 4**. **Lab *N* is sat on the
> Wednesday of Week *N+1*.**
>
> **Nothing here is marked.** The TA checks your work off in the session.
> [[Year2 - Sophomore/COURSE POLICIES|COURSE POLICIES]] costs you a letter grade after a second
> unexcused absence.

**What you are doing:** looking at memory that is not there yet, and then finding a 234 MB leak in a
program that already uses the strict fold.

By the end you will have seen `seq` do nothing, made a program 5,280× smaller by adding five
characters, and — the part that matters — **fixed a function you did not edit**, by moving the
strictness into a type.

---

## 0. Setup (8 minutes)

```bash
mkdir -p "$PROG202/week3/practice"
cd "$PROG202/week3/practice"
cp "$ACADEMICS/1. Sophomore/Spring/2. PROG 202 - Functional & Logic Programming/PROG202 Week3/lab/"{Sched.hs,Stats.hs,Makefile} .
make
./stats lazy 1000
```

```
sessions=17000 minutes=1070000 lectures=13000 labs=2000 longest=110
```

**Check that arithmetic**: 1,000 copies of a 17-session week is 17,000 sessions and 1,000 × 1,070
minutes. `Stats.hs` is the only file you edit.

---

## 1. `:sprint` — Watching Nothing Happen (18 minutes)

Open `ghci` with no arguments and type all of this. **The point is your fingers, not your eyes.**

### 1a. A pair

```
ghci> let p = (1+1, 2+2) :: (Int, Int)
ghci> :sprint p
ghci> p `seq` ()
ghci> :sprint p
ghci> fst p
ghci> :sprint p
```

You should see `p = (_,_)`, then `()`, then **`p = (_,_)` again**, then `2`, then `p = (2,_)`.

**Stop and explain the third line to the person next to you.** `seq` is the strictness primitive and it
did nothing at all. If you can say why in one sentence you have understood weak head normal form, which
is most of this week.

### 1b. A list

```
ghci> let xs = map (*2) [1..5] :: [Int]
ghci> xs `seq` ()
ghci> :sprint xs
```

`xs = _ : _` — **one cons cell, and its head and tail are both thunks.** `seq` on a list tells you only
that the list is not empty.

### 1c. Normal form

```
ghci> import Control.DeepSeq
ghci> let q = (1+1, 2+2) :: (Int, Int)
ghci> q `deepseq` ()
ghci> :sprint q
```

`q = (2,4)`. **That is the difference between WHNF and NF**, and it is the difference between `seq` and
`deepseq`.

**Answer these three before you move on:**

1. `seq (undefined, 2) ()` succeeds. `seq undefined ()` throws. Why is that consistent?
2. `let x = error "boom" in length [x, x, x]` returns **3**. Why does the error never happen?
3. `data Acc = Acc !Int !Int`. What is `seq (Acc undefined 3) ()`? **Predict, then check.** It is not
   what 1 would suggest, and the reason is worth knowing.

---

## 2. Reproducing the 727 MB (18 minutes)

```bash
cd "$ACADEMICS/1. Sophomore/Spring/2. PROG 202 - Functional & Logic Programming/PROG202 Week3/resources"
ghc -Wall -O2 -rtsopts -o mean  mean.hs
ghc -Wall -O0 -rtsopts -o mean0 mean.hs
for k in two lazy bang strict; do ./mean0 $k 10000000 +RTS -s 2>&1 | grep residency; done
for k in two lazy bang strict; do ./mean  $k 10000000 +RTS -s 2>&1 | grep residency; done
```

**Fill in the eight residency figures.** One of them is about 727 MB and it is the one written with
`foldl'`.

**Answer:**

**(a)** The `lazy` row uses `foldl'`, the strict fold. **Why does it leak?** One sentence, using the
phrase *weak head normal form*.

**(b)** The `two` row leaks **at both optimisation levels** — 245 MB and 289 MB — and `-O2` makes it
slightly worse. **It is a different problem from (a).** Name it, and say why no `seq` anywhere can fix
it.

**(c)** At `-O2` the `lazy` row is 44 KB. **So is the bug gone?** Answer carefully; L07 §4's last
paragraph is the thing being tested.

---

## 3. The Leak in `Stats.hs` (25 minutes)

Now the same bug, in a program that looks nothing like a toy.

```bash
cd "$PROG202/week3/practice"
./stats lazy   100000 +RTS -s 2>&1 | grep -E "residency|Total   time"
./stats strict 100000 +RTS -s 2>&1 | grep -E "residency|Total   time"
```

Both are identical right now, because `stepStrict = step`. You should see about **234 MB** and 1.5 s.

100,000 copies is 1.7 million sessions — not a realistic timetable, and **a realistic amount of data**
for anything that processes a stream.

### 3a. Find it before you fix it

`step` builds a five-field `Stats` from the previous one. `foldl'` forces the result to WHNF each time.

**Write down, before touching anything: how many thunk chains are being built, and how long is each?**

### 3b. Fix it with bang patterns

Replace `stepStrict` so that each field is forced as it is computed:

```haskell
stepStrict s t =
  let !a = nSessions s + 1
      !b = nMinutes s + duration t
      … 
  in Stats a b c d e
```

`{-# LANGUAGE BangPatterns #-}` is already at the top of the file.

```
lazy     234,075,256 bytes maximum residency   1.510 s
strict          44,328 bytes maximum residency   0.028 s
```

**5,280× less memory and 54× faster, for five `!` characters.** Reproduce both rows.

### 3c. Now fix it the other way, and watch what happens to `step`

Put the bangs in the **data declaration** instead, and **change nothing else** — leave `stepStrict` as
your version from 3b, and leave `step` exactly as it was given to you:

```haskell
data Stats = Stats
  { nSessions :: !Int
  , nMinutes  :: !Int
  …
```

Rebuild and run **both**:

```
lazy     44,328 bytes maximum residency   0.027 s
strict   44,328 bytes maximum residency   0.027 s
```

**The `lazy` version is fixed and you did not edit it.**

**This is the most important five minutes of the lab.** Answer:

1. **Why** did `step` become strict without being changed? *(Say what a strict field does and when.)*
2. Which of the two fixes would you rather inherit from a colleague, and why?
3. Give a case where the bang-pattern fix is the **only** option — that is, where you cannot put the
   `!` in the type. *(Think about who owns the type.)*

---

## 4. Infinite Lists, and a Stopping Rule You Write (20 minutes)

```bash
cd "$ACADEMICS/1. Sophomore/Spring/2. PROG 202 - Functional & Logic Programming/PROG202 Week3/resources"
ghc -Wall -O2 -o infinite infinite.hs
./infinite take
./infinite fib 1000
./infinite sqrt 2
```

### 4a. Knot-tying

In `ghci`, define `fibs` and then define it **without the two seed cells**:

```haskell
fibs = 0 : 1 : zipWith (+) fibs (tail fibs)
bad  = zipWith (+) bad (tail bad)
```

`take 3 fibs` works. `take 3 bad` gives **`<<loop>>`**. Explain the difference in one sentence using the
word **productive**.

### 4b. The separation Hughes is arguing for

`sqrts n` produces approximations for ever and **never decides when to stop**. `within eps` decides and
**never knows how they were produced.**

**Write a second stopping rule**, on *relative* rather than absolute error:

```haskell
relative :: Double -> [Double] -> Double
```

Run both rules on `sqrts 2`, `sqrts 1e-8` and `sqrts 1e20`, and report the six answers against
`sqrt` from the Prelude.

**You will find that both rules work on all three inputs**, including `1e20`, where an absolute
tolerance of `1e-12` on a number near ten billion has no business succeeding. **Work out why it does.**
*(Hint: print the first twelve approximations for `sqrts 1e20` and look at the last three. The answer is
about `Double`, not about Newton.)*

**Then find an input or a generator for which the absolute rule genuinely does not terminate and the
relative one does.** It exists; `sqrts` is not it, and finding that out is the exercise.

**Finally, confirm the thing that is the point: you did not edit `sqrts`.** Say what you would have had
to edit in a language where the loop owned the convergence test.

### 4c. Generate and test

```haskell
head [ (a,b,c) | c <- [1..], b <- [1..c], a <- [1..b], a*a + b*b == c*c ]
```

**That searches an infinite space and returns `(3,4,5)`.** Say what would happen if `head` were `last`,
and what that tells you about who controls termination.

---

## 5. The Sieve (12 minutes)

```bash
ghc -Wall -O2 -o sieve sieve.hs
for n in 2000 10000; do
  echo -n "naive $n: "; /usr/bin/time -f "%es" ./sieve naive $n
  echo -n "real  $n: "; /usr/bin/time -f "%es" ./sieve real  $n
done
```

Both print `17393` and `104743`. **The times differ by about 19× at *n* = 10,000.**

**Answer:**

1. The famous two-liner is called a sieve and **is not one.** In one sentence, what does a real sieve do
   that it does not?
2. **Nothing in those two lines suggests a quadratic.** Say what that tells you about reading
   performance off Haskell source. *(This is the same answer as §2(b) and §3, in a third costume.)*

---

## 6. Checkoff

Show the TA:

- [ ] `:sprint p` showing **`(_,_)` after `seq`**, and your one-sentence explanation (§1a)
- [ ] Your answer to §1 question 3 — `seq (Acc undefined 3) ()` — with the result you measured
- [ ] The eight residency figures from §2, and your answers to (a), (b) and (c)
- [ ] **`./stats lazy` at 44 KB with `step` unedited** (§3c), and your answer to question 1
- [ ] Your `relative` stopping rule working on `sqrts`, and `sqrts` unedited (§4b)
- [ ] `take 3 bad` giving `<<loop>>`, and your sentence with the word *productive* (§4a)

---

## What Comes Next

**Week 4 is type classes**, and it answers a question that has been open since Week 0: why `:t 3` says
`Num a => a`, why `length` says `Foldable t =>`, and how one `foldr` works on things that are not lists.
It also brings `Functor`, which is the first of the three abstractions Weeks 4–6 are built on.

**PS 3 is due the Friday of Week 4** and repeats §2, §3 and §5 with marks.

**Lab 4 is on the Wednesday of Week 5.**

---

*PROG 202 · Week 3 · Lab 3 · © CSE Department*
