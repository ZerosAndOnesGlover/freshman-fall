# PROG 202 · Problem Set 0 · Solutions
## Purity, Referential Transparency, and Reading a Type
### INSTRUCTOR ONLY — NOT FOR STUDENTS

---

**Released:** Week 0 Wednesday · **Due:** Week 1 Friday 17:00 · **100 points**

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

---

## Q1: Reading a Type (20)

### (a) [5] — one mark each

| Expression | Type |
|---|---|
| `map` | `(a -> b) -> [a] -> [b]` |
| `map reverse` | `[[a]] -> [[a]]` |
| `(.)` | `(b -> c) -> (a -> b) -> a -> c` |
| `(.) (.)` | `(a1 -> b -> c) -> a1 -> (a2 -> b) -> a2 -> c` |
| `zip [1,2,3]` | `Num a => [b] -> [(a, b)]` |

**`map reverse` is the one to look at.** It is `map` with one of two arguments supplied, so it is
still a function; `reverse :: [a] -> [a]` forces both of `map`'s type variables to the same list
type, giving `[[a]] -> [[a]]`. Students who write `[[a]] -> [[b]]` have not seen that `reverse`
constrains them to be equal.

**`(.) (.)` is deliberately horrible and nobody should get it by reasoning.** Full marks for the
`:t` output plus an honest "I could not derive this". A student who *does* derive it should be told
about `Data.Function` and left alone.

**`zip [1,2,3]` keeps a `Num a =>` constraint** because the literals are still overloaded. Students
who write `[b] -> [(Int, b)]` have been bitten by GHCi's defaulting in a different context; give
the mark and note the distinction.

### (b) [4]

`::` **"has type"** · `=>` **"implies" / "such that"** · `->` **"to" / arrow** · `:` **"cons"** ·
`$` **"apply"**.

**`elem :: Eq a => a -> [a] -> Bool` takes two arguments.** Everything left of `=>` is a
*constraint* — a requirement on the caller that `a` be comparable — not a parameter. One mark for
the count, one for a sentence that distinguishes the two arrows.

**Commonest error:** "three arguments, the first being the `Eq a`". That is precisely the
misreading, and it is worth a comment on every script that has it, because Week 4 is unintelligible
with it in place.

### (c) [6]

- `add 3 :: Int -> Int`.
- `add = \x -> \y -> x + y`.
- `map (add 3) [1,2,3]` **has to work** because `add 3` *is* a function of one argument; there is no
  partial-application machinery involved, `add` genuinely returns a function after one argument.
  Full marks require the words "returns a function" or equivalent.
- Anything of type `Int -> Int -> Int` that is neither: `\x _ -> x` (i.e. `const`), `(*)`, `max`,
  `\x y -> x - y`. **`\x y -> y + x` is `flip add` and scores zero for the last bullet** — catching
  that is the point of excluding it.

### (d) [5]

`Num a =>` means the literal works at any numeric type; `Foldable t =>` means `length` works on any
container with a notion of "elements in order", not just lists.

**`length xs / 2` fails** because `length` returns `Int`, `/` requires `Fractional`, and `Int` is not
`Fractional`. The fix is `div` (integer division) or `fromIntegral (length xs) / 2`.

**The argument [2 of the 5]:** no expected answer. Full marks for a position that engages with the
actual trade-off — Haskell makes you say which division you meant; the others pick one silently and
are right most of the time. Reward anyone who notices that **C, Java and Python make three different
silent choices** here (truncating int division, truncating int division, true division), which is
itself the argument.

---

## Q2: Referential Transparency (18)

### (a) [5] — one each

1. `length [1,2,3]` — **yes.** Replaceable by `3` anywhere.
2. `getLine` — **yes**, and this is the one they get wrong. `getLine` is a *value* of type
   `IO String`; it is the same value every time and may be freely substituted. What differs is what
   happens when the runtime *performs* it, and performing is not evaluating. **The recipe is the
   same recipe; the cakes differ.**
3. `putStrLn "hi"` — **yes**, same reason. `putStrLn "hi" :: IO ()` denotes one fixed action.
4. `read "42" :: Int` — **yes**, it is `42`. *(A student who says "no, it can throw" has spotted
   something real: `read "x" :: Int` is bottom. Bottom is still a value and the expression is still
   transparent. Give the mark and the remark.)*
5. `unsafePerformIO getLine` — **no.** That is the entire purpose of the name.

**The mark scheme:** 1 point each, and require a reason for 2 and 5.

### (b) [6]

`gcc -O2`, GCC 13.3.0, *n* = 10⁹, on the reference machine:

| | once | twice |
|---|---:|---:|
| `pure_sum` | 0.44 s | **0.44 s** |
| `impure_sum` | 0.44 s | **0.88 s** |

**What the compiler lost:** common subexpression elimination. **Why losing it was correct:** with
`calls++` in the body, two calls and one call are distinguishable by a later read of `calls`, so
collapsing them changes the program's meaning. GCC cannot know that nothing reads it — `calls` has
external linkage and another translation unit could.

**[2 of the 6] for any student who *tries* to restore the optimisation and reports what happened.**
The obvious move is to make `calls` `static`, so that no other translation unit can read it. **It does
not work** — measured, GCC 13.3.0, same *n*:

| | once | twice |
|---|---:|---:|
| `impure_sum` with `static long calls` | 0.44 s | **0.89 s** |

Nothing in the program ever reads `calls`; it is `static`; GCC still will not collapse the two calls.
**The analysis is conservative**, and that is the real lesson of the question: purity is not something
a compiler reliably infers, it is something a language either guarantees or does not. Award the marks
for the attempt and the honest negative result, not for a particular conclusion.

### (c) [4]

`-O2`: 0.31 s and 0.32 s. `-O0`: 0.19 s and 0.38 s *(at n = 2×10⁷; at 10⁹ the `-O0` build is too slow
to be worth the wall-clock)*.

**Is `-O0`'s failure to share a bug? No.** Two sentences wanted: sharing here is an *optimisation the
language permits*, not a *guarantee the language makes*; `-O0` exists to compile fast and to keep the
Core close to the source, and doing CSE there would defeat both. **Deduct if a student claims
Haskell guarantees the sharing** — Week 3's `let`-bound sharing is guaranteed, and this is not that,
and the distinction is examinable.

### (d) [3]

No expected answer; mark the argument. The strong replies:

- **Refactoring becomes mechanical.** Extracting an expression into a named function, or inlining
  one, cannot change behaviour. In C both can.
- **Testing becomes total.** A pure function's behaviour is its input/output relation and nothing
  else, which is what makes Week 11 possible at all.
- **Reviewing becomes local.** You can read a pure function and know what it does without knowing
  what else the program contains.
- **Concurrency becomes free of a whole bug class** (Week 7).

**Zero marks for "it's cleaner" with nothing after it.** One mark for a real consequence, three for a
consequence plus a mechanism.

---

## Q3: Evaluation by Substitution (22)

### (a) [6]

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

**Haskell does neither: call by need.** It substitutes unevaluated like call by name, but the two
occurrences of `double 3` are the *same thunk*, so it is forced once — **two `+` operations, with
call-by-name's substitution order.** Full marks require naming call by need and saying it gets
call-by-value's count.

**Deduct 1** for a student who counts the `+` inside `double`'s definition as a separate operation
each time it is *substituted* rather than *performed*; it is a common and forgivable slip.

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

**The middle one is the exam answer.** `!!` walked the spine as far as index 3 and forced **only**
that element. Everything before it exists as a cons cell with an unevaluated head; everything after
it does not exist at all — hence the trailing `_` rather than a bracketed list.

**Note the notation change.** After `length`, the spine is fully known and `:sprint` switches to
`[…]` form; before, it cannot, and prints the cons chain. Award the marks for the *explanation*, not
for reproducing the punctuation.

### (c) [5]

Any nested example. The canonical one:

```
ghci> let zs = [Just (1+1), Just (2+2), Nothing] :: [Maybe Int]
ghci> length zs
3
ghci> :sprint zs
zs = [Just _,Just _,Nothing]
ghci> case head zs of { Just n -> n; Nothing -> 0 }
2
ghci> :sprint zs
zs = [Just 2,Just _,Nothing]
```

**Note what `length` did here and did not do in Lab 0 §1c.** The `Just` constructors are already
visible after forcing only the spine, because the list *literal* built them — `Just (1+1)` is in
weak head normal form the moment it exists; only its *field* is a thunk. Contrast `map (*2) [1..5]`,
where each element is an unapplied thunk and `length` leaves `[_,_,_,_,_]`.

**That contrast is the answer worth drawing out in feedback**, and it is the first appearance of
*weak head normal form*, which Week 3 names.

**Full marks for any session showing a `_` inside a constructor inside a list.** The trap is typing
`zs` at the prompt, which forces everything; a student whose transcript shows `[Just 2,Just 4,Nothing]`
throughout has fallen into it.

### (d) [5]

- **Blackhole:** the RTS overwrites a thunk with a marker while evaluating it. Entering that marker
  from the same thread means the value depends on itself. **The runtime installs it, not the
  compiler** — 1 mark for that distinction.
- **Uncaught non-termination:** `f n = f (n + 1)`, or `main = print (length [1..])`. Each step
  allocates a *fresh* thunk, so no thunk is ever re-entered. **Blackholing detects self-reference,
  not non-termination**, which is undecidable. [2]
- **The hard bullet [2].** In single-threaded code the check never false-positives: entering a
  blackhole means the current thread is inside that thunk's own evaluation. **With threads it can.**
  Under `-feager-blackholing` GHC blackholes on entry rather than on suspension, so thread A can
  enter a thunk thread B is legitimately evaluating; the RTS normally blocks A on it, but a thread
  that ends up waiting on a value it is itself computing via a different chain can be reported as
  `<<loop>>`. **Full marks for "it cannot happen single-threaded, because …" even without the
  threaded story** — the question says as much.

---

## Q4: Measurement (22)

**Their `ghc --version` must be stated.** Deduct 1 if absent; it is the habit being graded.

### (a) [5]

| How run | Reference machine |
|---|---:|
| `runghc primes.hs` | 8.5 s |
| `ghc -O0` | 1.03 s |
| `ghc -O2` | 0.15 s |

**Ratio ≈ 57×.** All three print `25997`; deduct if a student's three runs disagree on the answer,
which means they edited the file between runs.

**The rule:** *never quote a timing from `ghci` or `runghc`.* Then check they obeyed it in (b)–(d).

### (b) [7]

| | allocated | maximum residency | time |
|---|---:|---:|---:|
| `twice` | 52,944 B | 44,328 B | 0.007 s |
| `named` | 640 MB | 272,645,056 B | 1.11 s |
| `once` | 52,312 B | 44,328 B | 0.004 s |

**The third row is the marked one [3 of the 7].** Most predictions say 273 MB, reasoning that naming
is what costs. It is not: with **one** consumer nothing is retained behind the cursor and fusion
still applies, so it matches `twice` on both figures. **Full marks for a wrong prediction that is
reported and then explained.**

### (c) [5]

At `-O0`: `named` is **244,958,408 B** resident and 880 MB allocated; `twice` is **44,328 B**
resident and **1,600 MB** allocated.

**The answer wanted:**

- **Residency did not move.** The 44 KB / 245 MB gap exists at `-O0` and at `-O2` alike. It is
  *retention* — a name keeps the list alive between two traversals — and no optimisation level
  changes that. (`-O2` makes it marginally worse: 245 → 273 MB.)
- **Allocation is what `-O2` changed**, and only for the unnamed version: 1,600 MB → 53 KB. That is
  **list fusion**, and it is unavailable to the named version precisely because the list is shared.

**[2 of the 5] are for separating those two effects.** A student who says "`-O2` fixed the memory" has
merged them and should be corrected explicitly, because Week 3 builds on the distinction.

### (d) [5]

| | `-O0` | `-O2` |
|---|---:|---:|
| `sum1` *(naive recursion)* | 331 MB | 138 MB |
| `sum2` *(accumulator)* | 604 MB | **44 KB** |

**At `-O0` the accumulator version is worse** — 604 MB against 331 MB — which is the opposite of what
every imperative intuition predicts, and of what most Haskell tutorials assert without measuring.

**At `-O2` it is 14,000× better.**

**The explanation is strictness analysis**, and nobody is expected to have it in Week 0. Full marks
for any hypothesis *consistent with the student's own four numbers*. The good ones say something
like: *"`acc + x` is not evaluated when it is passed, so `sum2` builds a chain of ten million
pending additions; `-O2` must be noticing that `acc` is always eventually needed and adding as it
goes."* **That is exactly right and it is Week 3 L07 §4.**

**Zero marks for a hypothesis contradicted by their own table** — e.g. "the accumulator is always
better" written above numbers showing it is not. That is the single most informative thing this
paper can catch.

---

## Q5: `sched` (18)

### (a) [4]

```
[("CS 202",260),("PROG 202",260),("MATH 251",200),("CS 212",150),("ECE 211",150),("CS 290",50)]
```

Sum = **1,070** ✓. CS 202 and PROG 202 tie at 260 by different routes: CS 202 is 3×50 lecture +
110 lab, PROG 202 is 2×75 lecture + 110 lab. Worth a remark in feedback — it is the clearest
illustration of why this course's two-lecture week is not less teaching.

### (b) [4]

Wednesday, between 08:00 and 17:00, as (start, end) in minutes past midnight:

```
[(480,540),(590,600),(650,780),(890,900),(950,1020)]
```

i.e. **08:00–09:00, 09:50–10:00, 10:50–13:00, 14:50–15:00, 15:50–17:00.**

Accept any equivalent rendering. The two ten-minute gaps are changeover time and a student who filters
them out has made a defensible choice — say so rather than deducting, but require the choice be
stated.

### (c) [4]

**The four cases** — see Lab 0 Solutions §4a for the table; reproduce it or equivalent. [2]

**With `<=` in both positions:** clashes stay at **0**; lunch collisions go **2 → 5**, adding
ECE 211 Mon 13:00, PROG 202 Lab Wed 13:00, ECE 211 Fri 13:00 — all three of which *start* exactly
when lunch ends. [1]

**The fact not in the data [1]:** whether you can get from one room to another in zero minutes.
`overlaps` with `<` says a session ending at 14:50 in BH 215 and one starting at 14:50 in SSB 108 is
fine; the registrar cares that BH and SSB are different buildings. **The data has no room-to-room
travel time and no rooms in `Session` at all**, so neither definition can be the right one. Reward
anyone who says the schema is what needs fixing.

### (d) [6] — the argument

**No expected answer.** Two paragraphs, 2 marks each, and 2 for the fix.

**"The claim is wrong" side:** the grid is a rendering; MASTER TIMETABLE's 11:00–12:15 is the
authoritative booking. "Protected" is aspirational prose in a study-advice document.

**"The timetable is wrong" side:** sixteen of seventeen sessions respect the hour. One exception out
of seventeen is an oversight, not a policy, and the *shape* of the error — a 75-minute session
starting on the hour before a 60-minute break — is what you get when someone changes a course from
50 to 75 minutes and does not re-check the row below.

**Which file wins [2]:** the good answer names a principle, not a file. The best is *specificity*:
MASTER TIMETABLE and ROOM ASSIGNMENTS both independently record Tue/Thu 11:00 for TH 205, and
SPRING SCHEDULE's lunch row is a single un-sourced claim repeated five times. Two independent records
beat one. **Accept the opposite conclusion if the principle is stated and applied honestly.**

**The one-number fix [2].** Candidates:

- **Move the lectures to 10:45–12:00.** Breaks nothing in ROOM ASSIGNMENTS (TH 205 has no Spring
  booking before 11:00) but collides with **CS 212 at 10:00–10:50 in TH 200** only if travel time is
  zero — 10:50 to 10:45 is negative, so it *does* break, by five minutes.
- **Move them to 11:00–12:00** (a 60-minute lecture). Costs 30 minutes a week of contact time and
  takes the course below its 150-minute line.
- **Move the lunch hour to 12:15–13:15 on Tue and Thu.** Breaks nothing — nothing else is scheduled
  in that window either day — and is the cheapest fix. **This is the best answer** and few will find
  it, because it changes the *claim* rather than the *course*.

**Deduct for any fix asserted without checking ROOM ASSIGNMENTS.** The question says to check.

---

## Marks

| Q | Topic | Points |
|---|---|---:|
| 1 | Reading a type | 20 |
| 2 | Referential transparency | 18 |
| 3 | Evaluation by substitution | 22 |
| 4 | Measurement | 22 |
| 5 | `sched` | 18 |
| | **Total** | **100** |

---

## What to Watch For Across the Cohort

**Three signals in this paper predict trouble later, and all three are cheap to act on in Week 1:**

1. **Q4 answered from `runghc`.** They did not read the instruction that the question exists to
   establish. Email them.
2. **Q3(a) with no distinction between substituting and performing.** This is the misconception that
   makes Week 5 impossible. Fix it in the Week 1 tutorial, not in Week 5.
3. **Q1(b) counting `Eq a` as an argument.** Same, for Week 4.

**One signal predicts the opposite:** a student who answered Q5(d) by actually opening ROOM
ASSIGNMENTS and finding the 12:15 fix has the disposition this course is trying to produce. There
are usually two or three. Tell them so.

---

*PROG 202 · Week 0 · PS 0 Solutions · INSTRUCTOR ONLY · © CSE Department*
