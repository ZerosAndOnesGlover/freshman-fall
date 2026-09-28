# PROG 202 · Problem Set 0 · Solutions
## Purity, Referential Transparency, and Reading a Type
### INSTRUCTOR ONLY — NOT FOR STUDENTS

---

**Released:** Week 0 Wednesday · **Due:** Week 1 Friday 17:00 · **100 points** · **15 parts, ~3 hours**

**What this paper is testing.** Almost no Haskell is written. Q1 tests whether they can *read* a
type, Q2–Q3 whether they can reason about substitution, Q4 whether they will measure rather than
assume, and Q5 whether they will argue from evidence about something with no right answer. **Q4 is
the one that predicts the rest of the term**: a student who reports numbers from `runghc` after
Q4(a) has told you they will not read instructions, and that is worth an email in Week 1 rather than
Week 6.

**Marking posture for Q1–Q3.** The rubric rewards a *stated prediction* over a correct answer. A
wrong prediction, honestly reported, with an explanation of why it was wrong, is **full marks**. A
bare correct answer with no prediction is **half**. Say this in the first tutorial; they will not
believe it until they see a marked script.

**Timing.** Written to about three hours: Q1 20 min, Q2 45 min (the C build and four timings),
Q3 30 min, Q4 50 min (nine cells plus four), Q5 35 min. If the cohort reports much more, the
candidates to cut next year are Q4(c) and Q5(b).

---

## Q1: Reading a Type (20)

### (a) [8] — two marks each

| Expression | Type |
|---|---|
| `map reverse` | `[[a]] -> [[a]]` |
| `(.)` | `(b -> c) -> (a -> b) -> a -> c` |
| `zip [1,2,3]` | `Num a => [b] -> [(a, b)]` |
| `3` | `Num a => a` |

**`map reverse` is the one to look at.** It is `map` with one of two arguments supplied, so it is
still a function; `reverse :: [a] -> [a]` forces both of `map`'s type variables to the same list
type, giving `[[a]] -> [[a]]`. Students who write `[[a]] -> [[b]]` have not seen that `reverse`
constrains them to be equal.

**`zip [1,2,3]` keeps a `Num a =>` constraint** because the literals are still overloaded. Students
who write `[b] -> [(Int, b)]` have been bitten by GHCi's defaulting in a different context; give the
mark and note the distinction.

**`3 :: Num a => a`** — the literal is *overloaded*, standing for whatever numeric type the context
requires, via `fromInteger`. Accept any answer saying "it has no type of its own yet". Do **not**
accept "it's an `Int` by default": defaulting happens only when nothing else determines it.

### (b) [6]

`::` **"has type"** · `=>` **"implies" / "such that"** · `->` **"to"** · `:` **"cons"** ·
`$` **"apply"**. [1 each for any three; 3 marks total for the naming.]

**`elem` takes two arguments.** [2] Everything left of `=>` is a *constraint* — a requirement on the
caller that `a` be comparable — not a parameter. [1] for a sentence distinguishing the two arrows.

**Commonest error:** "three arguments, the first being the `Eq a`". That is precisely the misreading,
and it is worth a comment on every script that has it, because **Week 4 is unintelligible with it in
place.**

### (c) [6]

- `add 3 :: Int -> Int`. [3]
- `map (add 3) [1,2,3]` **has to work** because `add 3` *is* a function of one argument; there is no
  partial-application machinery involved — `add` genuinely returns a function after one argument. [3]
  **Full marks require the words "returns a function" or equivalent.**

---

## Q2: Referential Transparency (20)

### (a) [6] — two each

1. `length [1,2,3]` — **yes.** Replaceable by `3` anywhere.
2. `getLine` — **yes**, and this is the one they get wrong.
3. `unsafePerformIO getLine` — **no.** That is the entire purpose of the name.

**Why `getLine` is transparent:** it is a *value* of type `IO String`; it is the same value every
time you mention it and may be freely substituted. What differs is what happens when the runtime
*performs* it, and **performing is not evaluating**. The recipe is the same recipe; the cakes differ.

Require a reason for 2 and 3.

### (b) [8]

`gcc -O2`, GCC 13.3.0, *n* = 10⁹, on the reference machine:

| | once | twice |
|---|---:|---:|
| `pure_sum` | 0.44 s | **0.44 s** |
| `impure_sum` | 0.44 s | **0.88 s** |

**What the compiler lost:** common subexpression elimination. **Why losing it was correct:** with
`calls++` in the body, two calls and one call are distinguishable by a later read of `calls`, so
collapsing them changes the program's meaning. GCC cannot know nothing reads it — `calls` has
external linkage and another translation unit could. [4]

**"Try to win it back" [4].** The obvious move is `static long calls`, so no other translation unit
can see it. **It does not work** — measured:

| | once | twice |
|---|---:|---:|
| `impure_sum` with `static long calls` | 0.44 s | **0.89 s** |

Nothing in the program ever reads `calls`; it is `static`; GCC still will not collapse the two calls.
**The analysis is conservative**, and that is the real lesson: purity is not something a compiler
reliably infers, it is something a language either guarantees or does not.

**Award the marks for the attempt and an honest negative result**, not for a particular conclusion. A
student who tries `-flto`, or deleting the line, or `__attribute__((const))`, and reports honestly,
gets full marks. **Two results worth having ready**, both measured: `-flto` does **not** help (0.89 s), and
`__attribute__((noinline,const))` **does** (0.44 s twice). The second is the punchline — it is the
programmer *promising* what GCC could not prove, with no check that the promise is true. **That is
what a type system does for free**, and it is the cleanest one-line answer to Q2(c)'s colleague.

### (c) [6]

`-O2`: 0.31 s and 0.32 s. `-O0`: 0.19 s and 0.38 s *(at n = 2×10⁷; at 10⁹ the `-O0` build is too slow
to be worth the wall-clock).*

**Is `-O0`'s failure to share a bug? No. [3]** Two sentences wanted: sharing here is an *optimisation
the language permits*, not a *guarantee the language makes*; `-O0` exists to compile fast and keep
the Core close to the source. **Deduct if a student claims Haskell guarantees this sharing** —
Week 3's `let`-bound sharing is guaranteed, this is not, and the distinction is examinable.

**The paragraph [3].** No expected answer; mark the argument, and **the question forbids performance
arguments**, so deduct if that is all they have. The strong replies:

- **Refactoring becomes mechanical.** Extracting an expression into a named function, or inlining
  one, cannot change behaviour. In C both can.
- **Testing becomes total.** A pure function's behaviour is its input/output relation and nothing
  else, which is what makes Week 11 possible at all.
- **Reviewing becomes local.** You can read a pure function and know what it does without knowing
  what else the program contains.
- **A whole concurrency bug class disappears** (Week 7).

Zero for "it's cleaner" with nothing after it.

---

## Q3: Evaluation by Substitution (20)

### (a) [8]

**Call by value** (argument first):

```
quad 3 = double (double 3) = double (3 + 3) = double 6 = 6 + 6 = 12
```
**Two `+` operations.**

**Call by name** (substitute unevaluated):

```
quad 3 = double (double 3)
       = double 3 + double 3
       = (3 + 3) + (3 + 3)
       = 6 + 6 = 12
```
**Three `+` operations.**

**Haskell does neither: call by need. [3]** It substitutes unevaluated like call by name, but the two
occurrences of `double 3` are the *same thunk*, so it is forced once — **two `+` operations, with
call-by-name's substitution order.** Full marks require naming call by need and saying it achieves
call-by-value's count.

**Deduct 1** for counting the `+` inside `double`'s definition as a separate operation each time it
is *substituted* rather than *performed*; common and forgivable.

### (b) [6]

```
ghci> let ys = map (+1) [1..6] :: [Int]
ghci> :sprint ys
ys = _
ghci> ys !! 3
5
ghci> :sprint ys
ys = _ : _ : _ : 5 : _
ghci> length ys
6
ghci> :sprint ys
ys = [_,_,_,5,_,_]
```

**The middle one is the answer. [4]** `!!` walked the spine as far as index 3 and forced **only** that
element. Everything before it exists as a cons cell with an unevaluated head; everything after it
does not exist at all — hence the trailing `_` rather than a bracketed list.

**The notation change [2].** After `length` the spine is fully known and `:sprint` switches to `[…]`
form; before, it cannot. Award for the *explanation*, not for reproducing the punctuation.

### (c) [6]

- **Blackhole [3]:** the RTS overwrites a thunk with a marker while evaluating it; entering that
  marker from the same thread means the value depends on itself. **The runtime installs it, not the
  compiler** — 1 of the 3 marks is for that distinction. GHCi's bytecode interpreter does not install
  them the same way, which is why it hangs instead.
- **Uncaught non-termination [3]:** `f n = f (n + 1)`, or `main = print (length [1..])`. Each step
  allocates a *fresh* thunk, so no thunk is ever re-entered. **Blackholing detects self-reference,
  not non-termination**, which is undecidable.

---

## Q4: Measurement (22)

**Their `ghc --version` must be stated.** Deduct 1 if absent; the habit is what is being graded.

### (a) [5]

| How run | Reference machine |
|---|---:|
| `runghc primes.hs` | 8.5 s |
| `ghc -O0` | 1.03 s |
| `ghc -O2` | 0.15 s |

**Ratio ≈ 57×.** All three print `25997`; deduct if a student's three runs disagree on the answer,
which means they edited the file between runs.

**The rule:** *never quote a timing from `ghci` or `runghc`.* Then check they obeyed it in (b) and (c).

### (b) [10]

| | `-O0` allocated | `-O0` residency | `-O2` allocated | `-O2` residency |
|---|---:|---:|---:|---:|
| `twice` | 1,600 MB | **44,328 B** | **52,944 B** | **44,328 B** |
| `named` | 880 MB | **244,958,408 B** | 640 MB | **272,645,056 B** |
| `once` | 880 MB | 44,328 B | 52,312 B | 44,328 B |

Allow ±5% on the megabyte figures; the 44,328 B should be exact.

**The `once` prediction [3].** Most predictions say 273 MB, reasoning that naming is what costs. It is
not: with **one** consumer nothing is retained behind the cursor and fusion still applies, so `once`
matches `twice` on both figures. **Full marks for a wrong prediction reported and then explained.**

**The two mechanisms [4], and this is the part to get right.**

- **The residency gap is not the optimiser's doing.** 44 KB against 245 MB is already there at
  `-O0`. It is **retention**: laziness plus GC stream a list nobody holds, and a name holds it.
  `-O2` neither causes nor fixes it — it makes it slightly *worse* (245 → 273 MB).
- **What `-O2` adds is fusion**, visible only in the allocation column: 1,600 MB → 53 KB for `twice`.
  For `named` fusion is impossible, because the list is shared, so allocation only falls 880 → 640 MB.

**A student who says "`-O2` fixed the memory" has merged the two and should be corrected
explicitly**, because Week 3 builds on the distinction. **If you say one thing when handing this
back, say:** *fusion is an optimisation you can lose by giving something a name.*

### (c) [7]

| | `-O0` | `-O2` |
|---|---:|---:|
| `sum1` *(naive recursion)* | 331 MB | 138 MB |
| `sum2` *(accumulator)* | 604 MB | **44 KB** |

**At `-O0` the accumulator version is worse** — 604 MB against 331 MB — the opposite of what every
imperative intuition predicts, and of what most Haskell tutorials assert without measuring. **At
`-O2` it is roughly 14,000× better.** [4 for the four numbers.]

**The explanation is strictness analysis**, and nobody is expected to have it in Week 0. [3] for any
hypothesis *consistent with the student's own four numbers*. The good ones say something like:
*"`acc + x` is not evaluated when it is passed, so `sum2` builds a chain of ten million pending
additions; `-O2` must be noticing that `acc` is always eventually needed and adding as it goes."*
**That is exactly right and it is Week 3 L07 §4.**

**Zero for a hypothesis contradicted by their own table** — e.g. "the accumulator is always better"
written above numbers showing it is not. That is the single most informative thing this paper can
catch.

---

## Q5: `sched` (18)

### (a) [6]

```
[("CS 202",260),("PROG 202",260),("MATH 251",200),("CS 212",150),("ECE 211",150),("CS 290",50)]
```

Sum = **1,070** ✓ [4]

**The tie [2]:** CS 202 and PROG 202 both reach 260 by different routes — CS 202 is 3×50 lecture +
110 lab, PROG 202 is 2×75 lecture + 110 lab. **Two lectures a week is not less teaching**, and this
is the clearest evidence of it in the course.

### (b) [6]

**The four cases [3]** — see Lab 0 Solutions §4a for the table; reproduce it or equivalent.

| Case | `s1 < e2` | `s2 < e1` | Overlap? |
|---|---|---|---|
| A entirely before B | ✓ | ✗ | no |
| A entirely after B | ✗ | ✓ | no |
| A ends exactly when B starts | ✓ | ✗ *(e1 = s2)* | no — correct |
| A contains B | ✓ | ✓ | **yes** |

**With `<=` [3]:** clashes stay at **0**; lunch collisions go **2 → 5**, adding ECE 211 Mon 13:00,
PROG 202 Lab Wed 13:00, ECE 211 Fri 13:00 — all three of which *start* exactly when lunch ends.

**Why `clashes` is unaffected:** the timetable contains **no two real sessions that touch exactly** —
the closest gap is ten minutes, a three-way tie. The bug is invisible until the data contains a
touching pair, and the lunch pseudo-session is the only thing that supplies one. **That is what a
boundary bug looks like in the wild**, and it is why Week 11 generates inputs rather than choosing
them.

### (c) [6] — the argument

**No expected answer.** Two marks per bullet.

**"The claim is wrong" side:** the grid is a rendering; MASTER TIMETABLE's 11:00–12:15 is the
authoritative booking. "Protected" is aspirational prose in a study-advice document.

**"The timetable is wrong" side:** sixteen of seventeen sessions respect the hour. One exception out
of seventeen is an oversight, not a policy, and the *shape* of the error — a 75-minute session
starting on the hour before a 60-minute break — is what you get when someone changes a course from
50 to 75 minutes and does not re-check the row below.

**Which file wins:** the good answer names a **principle**, not a file. The best is *specificity*:
MASTER TIMETABLE and ROOM ASSIGNMENTS both independently record Tue/Thu 11:00 for TH 205, and SPRING
SCHEDULE's lunch row is a single un-sourced claim repeated five times. Two independent records beat
one. **Accept the opposite conclusion if the principle is stated and applied honestly.**

**The one-number fix.** Candidates:

- **Move the lectures to 10:45–12:00.** TH 205 has no Spring booking before 11:00, but 10:45 is
  *before* CS 212 ends at 10:50 in TH 200 — so it breaks, by five minutes.
- **Move them to 11:00–12:00** (60 minutes). Costs 30 minutes a week and takes the course below its
  150-minute line.
- **Move the lunch hour to 12:15–13:15 on Tue and Thu.** Nothing else is scheduled in that window on
  either day, so it breaks nothing. **This is the best answer** and few will find it, because it
  changes the *claim* rather than the *course*.

**Deduct for any fix asserted without checking ROOM ASSIGNMENTS.** The question says to check.

---

## Marks

| Q | Topic | Parts | Points |
|---|---|---:|---:|
| 1 | Reading a type | 3 | 20 |
| 2 | Referential transparency | 3 | 20 |
| 3 | Evaluation by substitution | 3 | 20 |
| 4 | Measurement | 3 | 22 |
| 5 | `sched` | 3 | 18 |
| | **Total** | **15** | **100** |

---

## What to Watch For Across the Cohort

**Three signals in this paper predict trouble later, and all three are cheap to act on in Week 1:**

1. **Q4 answered from `runghc`.** They did not read the instruction the question exists to
   establish. Email them.
2. **Q3(a) with no distinction between substituting and performing.** This is the misconception that
   makes Week 5 impossible. Fix it in the Week 1 tutorial, not in Week 5.
3. **Q1(b) counting `Eq a` as an argument.** Same, for Week 4.

**One signal predicts the opposite:** a student who answered Q5(c) by actually opening ROOM
ASSIGNMENTS and finding the 12:15 fix has the disposition this course is trying to produce. There are
usually two or three. Tell them so.

---

*PROG 202 · Week 0 · PS 0 Solutions · INSTRUCTOR ONLY · © CSE Department*
