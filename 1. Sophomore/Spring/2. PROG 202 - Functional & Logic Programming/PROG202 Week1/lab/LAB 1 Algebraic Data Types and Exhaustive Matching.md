# PROG 202 · Lab 1
## Algebraic Data Types, and Making the Bug Unwriteable
### Week 1 · sat **Wednesday of Week 2**, 13:00–14:50, BH 215 · **unmarked, checked off in the session**

---

> **This lab covers Week 1** and is sat on the **Wednesday of Week 2**, after both of Week 1's
> lectures and Week 2's Tuesday lecture. **Lab *N* is sat on the Wednesday of Week *N+1*** for the
> rest of the term, because the lab is Wednesday and the lectures are Tuesday and Thursday — a lab
> sat in its own week would have had one of the two.
>
> **There was no lab in Week 1.** Lab 0 was sat on the Friday that closed Week 0.
>
> **Nothing here is marked.** The TA checks your work off in the session.
> [[Year2 - Sophomore/COURSE POLICIES|COURSE POLICIES]] costs you a letter grade after a second
> unexcused absence, which is the only enforcement there is and the only one needed.

**What you are doing:** deleting eleven bugs from `sched` by changing its types, and then discovering
that one of them will not go away and needs a different tool.

L03 §4 measured Week 0's `Session`: of the 120 ways to order its five fields, **twelve type-check and
eleven of them are wrong.** Today you rewrite it so that the number is **one**, find out why it is not
zero, and close the last one with a smart constructor and a module boundary.

**Everything you write today goes in `week1/practice/`**, which is git-ignored. Nothing from this
session is submitted.

---

## 0. Setup (8 minutes)

```bash
mkdir -p "$PROG202/week1/practice"
cd "$PROG202/week1/practice"
cp "$ACADEMICS/1. Sophomore/Spring/2. PROG 202 - Functional & Logic Programming/PROG202 Week1/lab/"{Sched.hs,Main.hs,Break.hs,Makefile} .
make            # will fail: Sched.hs is a skeleton
```

`Sched.hs` has **eight TODOs** and is the only file you edit. `Main.hs` is the driver and `Break.hs`
is §5's deliberate failure; leave both alone.

**The first `make` prints five errors and two of them point at `render`, which is given code.** Nothing
is wrong with `render`: its accessors do not exist until TODO 3 declares the record. **Do TODOs 1, 2
and 3 together**, then build — a missing `Day` cascades into everything and there is no point reading
the errors one at a time until the three types exist.

**Read the export list at the top of `Sched.hs` before you write anything.** It says `Session` and
not `Session (..)`, and §5 is about what that one difference buys.

---

## 1. `Day` and `Kind` as Sum Types (12 minutes) — TODO 1

```haskell
data Day  = Mon | Tue | Wed | Thu | Fri  deriving (Show, Eq, Ord, Enum, Bounded)
data Kind = LEC | LAB | REC | SEM        deriving (Show, Eq, Ord, Enum, Bounded)
```

**Five things are derived and you should be able to say what each buys** (L03 §6). Check three of
them at a prompt before moving on:

```
ghci> :l Sched.hs
ghci> [minBound .. maxBound] :: [Day]
ghci> Mon < Tue
ghci> succ Wed
```

**`Bounded` is the one that matters**, and it is why `Main.hs` writes `[minBound .. maxBound]` where
Week 0 wrote `weekdays = ["Mon","Tue","Wed","Thu","Fri"]`. That list was a thing that could disagree
with the data. Now there is nothing to disagree with.

**Answer before you go on:** `Mon < Tue` is `True`. **Where did that ordering come from?** You did not
write a comparison. And: **give a type for which deriving `Ord` this way would be a bug.**

---

## 2. `Course`, `Minutes`, and `Session` (18 minutes) — TODOs 2 and 3

`newtype`, not `data`, for the two single-field wrappers — it is erased at compile time, so a
`[Minutes]` has the same machine representation as an `[Int]`.

**Write the two `Show` instances by hand.** Derived `Show` gives you `Minutes 660`, which is correct
and unreadable. You want `11:00`:

```haskell
instance Show Minutes where
  show (Minutes t) = pad (t `div` 60) ++ ":" ++ pad (t `mod` 60)
    where pad n = if n < 10 then '0' : show n else show n
```

and a `Course` should print as `PROG 202`, not `Course "PROG 202"`.

> **A `Show` instance is for programmers, not users.** The convention is that `show` produces
> something you could paste back into the source. These two break that convention deliberately,
> because `sched`'s output is read by people; when you write a library, derive it instead.

Then `Session` as a record with five named fields (TODO 3). Derive `(Eq, Show)`. **Do not derive
`Ord`** — think about what order two sessions would come in, and you will find there is no obvious
answer, which is the signal not to.

Now check the whole point of the exercise:

```
ghci> :r
ghci> :t course
ghci> :t start
```

**Five accessor functions appeared and you did not write them.** That is what a record declaration
gives you.

---

## 3. The Body of the Module (25 minutes) — TODOs 4–8

### 3a. `mkSession` (TODO 4)

The smart constructor. Reject `s >= e` with a `Left` that names the session and both times; otherwise
`Right`. **Its type is the point:** a caller cannot get a `Session` out of an `Either String Session`
without saying what happens on failure.

### 3b. `duration`, `overlaps`, `inWindow` (TODOs 5–7)

`duration` pattern-matches the `Minutes` out. `overlaps` means what it meant in Week 0 — same day,
intervals intersect, **touching is not overlapping** — but should read better now the fields have
names. Compare your line with your Week 0 one and keep the comparison for §6.

`Window` exists because `Kind` has four constructors and **none of them is lunch**. Week 0 faked a
lunch "session" with a `("LUNCH", "---", …)` tuple; that fake is now unwriteable, which is the types
doing their job and forcing a better design.

### 3c. `timetable` (TODO 8)

Seventeen sessions, the same data as Week 0, every one through `mkSession`. Each call gives an
`Either String Session` and you need an `Either String [Session]`.

**`traverse id` does it.** You are not expected to know why — it is Week 6 — but use it and **write
down, in one sentence, what you think it is doing.** Keep the sentence; Week 6 L20 asks you to compare
it with the answer.

Now:

```bash
make && ./sched
```

```
sessions         : 17
contact minutes  : 1070
clashes          :
lunch collisions :
  PROG 202 LEC Tue 11:00-12:15
  PROG 202 LEC Thu 11:00-12:15
minutes per day  : [(Mon,175),(Tue,285),(Wed,260),(Thu,175),(Fri,175)]
```

**Same seventeen sessions, same 1,070 minutes, same two lunch collisions as Week 0.** A rewrite that
changes the answers is a rewrite with a bug in it.

**Answer:** the per-day figures are new. **Tuesday is 285 minutes and Monday is 175.** Check that the
five add to 1,070, and say which day you would rather have a 09:00 exam on.

---

## 4. The Hole the Types Left (12 minutes)

Run the experiment from L03 §4 yourself:

```bash
cd "$ACADEMICS/1. Sophomore/Spring/2. PROG 202 - Functional & Logic Programming/PROG202 Week1/resources"
python3 orderings.py tuple middle
```

It compiles 120 files per design and takes about a minute each.

| design | accepted of 120 | wrong but accepted |
|---|---:|---:|
| `tuple` — Week 0 | 12 | **11** |
| `middle` — what you just wrote | 2 | **1** |

**The one that is left is `(0, 1, 2, 4, 3)`: `start` and `end` swapped**, because both are `Minutes`.

**Now prove to yourself that `mkSession` catches it.** Add an eighteenth session to `timetable` with
its times the wrong way round:

```haskell
, mkSession (Course "PROG 202") LEC Thu (hm 12 15) (hm 11 0)
```

```
$ ./sched
rejected: PROG 202 LEC Thu: starts at 12:15 and ends at 11:00
```

**The whole timetable is rejected, not just that session** — which is what `traverse` did, and is the
right behaviour for a file of static data. Take the bad session out again.

**Answer:** you could have got the count to **zero** with a `newtype Start` and a `newtype End`
(`orderings.py strict` proves it). **Give one reason not to**, and say what you would have to write
every time you compared a start to an end.

---

## 5. The Module Boundary (15 minutes)

`mkSession` is only a guarantee if it is the **only** way in. It is not, yet — inside `Sched.hs` the
`Session` constructor is right there.

```bash
make break
```

`Break.hs` imports `Sched` and calls the `Session` constructor directly, with the times swapped. It
**must fail**:

```
Break.hs:14:7: error:
    • Illegal term-level use of the type constructor or class ‘Session’
    • imported from ‘Sched’ at Break.hs:11:1-12
    • Perhaps use variable ‘mkSession’ (imported from Sched)
```

**Read that message properly, because it is not the message you expected.** GHC does not say *"Session
is not exported"*. It says you have used a **type** name where a **value** was wanted — and
suggests `mkSession`.

**Answer these three:**

1. Why is that the error? *(L03 §2. Types and values live in separate namespaces, and the export list
   let one of the two `Session`s through.)*
2. Change the export list to `Session (..)` and run `make break` again. What happens, and what have
   you just given away?
3. Put it back. Then explain why **`mkSession` is worthless without the export list** — in one
   sentence, as if to a colleague who thinks the check in `mkSession` is the safety.

---

## 6. Exhaustiveness (12 minutes)

```bash
cd "$ACADEMICS/1. Sophomore/Spring/2. PROG 202 - Functional & Logic Programming/PROG202 Week1/resources"
ghc -Wall -fno-code exhaustive.hs
```

Two warnings. **One names the missing case; the other gives up with an ellipsis.** Read both.

Then, back in your own `Sched.hs`, find two bugs `-Wall` will **not** find for you:

**(a)** Write `roomFor :: Kind -> String` with only three of the four cases, compile with `-Wall`, and
confirm GHC names the fourth.

**(b)** Now write this and compile it with `-Wall`:

```haskell
firstSession :: [Session] -> Session
firstSession ts = head ts
```

**Zero warnings.** Run it on `[]`:

```
Prelude.head: empty list
```

**`-Wall` catches the incomplete `case` and misses `head`.** Say why the compiler *can* check one and
*cannot* check the other — then fix `firstSession` so the bug is not there to be caught. **The fix is
in the type, not in the body:** return a `Maybe Session` and use `listToMaybe` from `Data.Maybe`. Once
the type admits the empty case, every caller is made to handle it, which is L03 §3.

---

## 7. Checkoff

Show the TA:

- [ ] `./sched` printing **17 sessions, 1,070 minutes, no clashes, the two lunch collisions, and the
      five per-day figures** (§3c)
- [ ] Your two hand-written `Show` instances, and `./sched`'s output as evidence they work (§2)
- [ ] `rejected: PROG 202 LEC Thu: starts at 12:15 and ends at 11:00` (§4)
- [ ] `make break` failing, and your one-sentence answer to §5 question 3
- [ ] `firstSession` fixed so the `head` bug cannot occur, and your answer to §6 (§6b)
- [ ] Your one sentence on what `traverse id` is doing (§3c) — **keep this; Week 6 asks for it**

---

## What Comes Next

**Week 2 takes the recursion out.** `sum (map duration ts)`, the list comprehensions, `pairs` — all of
them are the same three or four shapes of loop written out longhand, and Week 2 names them: `map`,
`filter`, `foldr`, `foldl`. It also measures which of the last two you should use, and the answer is
not the one *Real World Haskell* gives.

**Lab 2 is on the Wednesday of Week 3.**

---

*PROG 202 · Week 1 · Lab 1 · © CSE Department*
