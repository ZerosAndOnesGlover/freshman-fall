# PROG 202 · Problem Set 0
## Purity, Referential Transparency, and Reading a Type

---

**Released:** Week 0, Wednesday · **Due:** Week 1, Friday 17:00
**Total: 100 points** · Submit one PDF, `PS0_{LastName}_{StudentID}.pdf`, plus your `.hs` files in a
tarball `PS0_{LastName}.tar.gz`

> Collaboration: discussing approaches is fine and encouraged. The write-up and the code must be
> yours. State at the top: *"I worked on this problem set independently"* or name who you discussed
> which question with.
>
> **Q1 and Q3 are to be answered by hand first.** Write your prediction down, then check it in
> `ghci`, then report both — a wrong prediction honestly reported and explained is worth full marks;
> a right answer with no prediction is worth half.
>
> **Q4 requires output from your own machine.** State your `ghc --version` and `uname -r`.
>
> **Every `.hs` file you submit compiles clean under `ghc -Wall -O2`.** Warnings cost marks in this
> course from PS 0 onwards. The one that will catch you is `Pattern match(es) are non-exhaustive`,
> and it is catching a real bug.

---

### Q1: Reading a Type (20 points)

**(a) [5]** For each expression, **write the type by hand**, then check with `:t`. Report both.

| Expression | Your prediction | `:t` says |
|---|---|---|
| `map` | | |
| `map reverse` | | |
| `(.)` | | |
| `(.) (.)` | | |
| `zip [1,2,3]` | | |

**(b) [4]** Name each of these symbols out loud, in the way
[[PROG202 Week0/resources/Haskell Syntax and Symbols|Haskell Syntax and Symbols]] names them, and say
what it does: `::`  `=>`  `->`  `:`  `$`

Then explain the difference between `->` and `=>` in one sentence, using
`elem :: Eq a => a -> [a] -> Bool` as the example. **How many arguments does `elem` take?**

**(c) [6]** `f x y` is not `f(x, y)`. Given

```haskell
add :: Int -> Int -> Int
add x y = x + y
```

- What is the type of `add 3`?
- Write `add` as an explicit lambda, with two `\`s.
- `map (add 3) [1,2,3]` works. Explain, in terms of currying, **why it has to**.
- Write something of type `Int -> Int -> Int` that is *not* `add` and not `flip add`.

**(d) [5]** `:t 3` reports `3 :: Num a => a`, not `3 :: Int`. `:t length` reports
`Foldable t => t a -> Int`, not `[a] -> Int`.

State what each constraint is doing. Then say why `length xs / 2` is a type error in Haskell and
compiles in Python, Java and C — and which of the two behaviours you would defend to a colleague.
*(There is no expected answer to the last part; the marks are for the argument.)*

---

### Q2: Referential Transparency (18 points)

**(a) [5]** For each of these, say whether it is referentially transparent — whether the expression
may be replaced by its value without changing the program's meaning — and why:

1. `length [1,2,3]`
2. `getLine`
3. `putStrLn "hi"`
4. `read "42" :: Int`
5. `unsafePerformIO getLine`

Two of these are subtler than they look. **`getLine` is referentially transparent**; say why, and say
what *is* different about it.

**(b) [6]** Reproduce L01 §3's C measurement on your own machine. Compile `resources/cse.c` with
`gcc -O2` and time all four cases at *n* = 10⁹:

| | once | twice |
|---|---|---|
| `pure_sum` | | |
| `impure_sum` | | |

**One line of C — `calls++`, incrementing a global nothing reads — is the difference.** Explain what
the compiler lost and why losing it was correct.

**(c) [4]** Now do the Haskell half — `resources/cse.hs` at `-O2` and at `-O0`. Report the four
numbers. **At `-O0` the sharing does not happen.** Is that a bug in GHC? Answer in two sentences.

**(d) [3]** A colleague says: *"So purity just means the compiler can optimise better. That's a
micro-optimisation; I care about correctness."* Give the strongest one-paragraph reply you can, using
something other than performance.

---

### Q3: Evaluation by Substitution (22 points)

**(a) [6]** Given

```haskell
double x = x + x
quad   x = double (double x)
```

Reduce `quad 3` to a number **twice**: once evaluating the argument first (call by value) and once
substituting it unevaluated (call by name). Show every step. **Count the `+` operations each way**
and say which count Haskell actually performs, and why it is neither.

**(b) [6]** Predict the three `:sprint` outputs, then run them:

```
ghci> let ys = map (+1) [1..6] :: [Int]
ghci> :sprint ys
ghci> ys !! 3
ghci> :sprint ys
ghci> length ys
ghci> :sprint ys
```

**One of your three predictions is probably wrong**, and it is the second. Explain what `!!` forced
and what it did not.

**(c) [5]** Write an expression `e` such that `:sprint e` shows a partially-evaluated *nested*
structure — something with a `_` inside a constructor that is inside a list. Show the session.

**(d) [5]** `x = x + 1` compiled gives `<<loop>>`; in `ghci` it hangs.

- What is a *blackhole*, and which component installs it?
- Write a non-terminating program that `<<loop>>` does **not** catch, and explain why it cannot.
- `<<loop>>` is described as a "cheap check that happens to catch this". Give a program where the
  check fires but the program was **not** actually going to loop forever. *(Hint: it cannot be done
  in single-threaded code. Say why, and you have full marks for this bullet.)*

---

### Q4: Measurement (22 points)

State your `ghc --version` and `uname -r` at the top of this answer.

**(a) [5]** Reproduce L02 §5's table with `resources/primes.hs`:

| How run | Your time |
|---|---|
| `runghc primes.hs` | |
| `ghc -O0` | |
| `ghc -O2` | |

Report the ratio between the first and the last. **State the rule this table exists to establish**,
in one sentence, and then obey it for the rest of the problem set.

**(b) [7]** Reproduce L02 §6 with `resources/share2.hs` and `+RTS -s`:

| | maximum residency | total memory | time |
|---|---|---|---|
| `./share2 twice` | | | |
| `./share2 named` | | | |
| `./share2 once` | | | |

The third row is the one to think about: the list is **named**, like the second, but used **once**.
Predict it before you run it and report both.

**(c) [5]** Repeat row two (`named`) at `-O0`. Report it. **Which optimisation level changed which
number, and which number did not move?**

**(d) [5]** Take L01 §4's two definitions:

```haskell
sum1 []     = 0
sum1 (x:xs) = x + sum1 xs

sum2 = go 0 where go acc []     = acc
                  go acc (x:xs) = go (acc + x) xs
```

Measure maximum residency for each on `[1..10000000::Int]`, at `-O0` and at `-O2`. **Four numbers.**
One of them is about 44 KB and one is about 600 MB.

`sum2` is the one that looks like a loop and is the one everyone is told to prefer. **At one of the
two optimisation levels it is worse.** Report which, and write your best guess at why. *(You are not
expected to be right. Week 3 grades this question again, in effect, and the marks here are for a
hypothesis that is consistent with your own numbers.)*

---

### Q5: `sched` (18 points)

Start from your Lab 0 `Sched.hs`.

**(a) [4]** Add `contactPerCourse :: [(String, Int)]` — each course paired with its weekly contact
minutes, sorted by minutes descending. Report the output. **Check that the total is still 1,070.**

**(b) [4]** Add `freeSlots :: String -> [(Int, Int)]`: given a day, the gaps between the end of one
session and the start of the next, between 08:00 and 17:00. Report Wednesday's.

**(c) [4]** Your `overlaps` uses `s1 < e2 && s2 < e1`.

- Write out the four interval cases — disjoint before, disjoint after, touching, containing — and
  show that the condition is right for each.
- Change both `<` to `<=`, re-run, and report **how many extra lines** appear and which they are.
- Say which of the two definitions the registrar would want, and why the answer depends on a fact
  about buildings that is not in the data.

**(d) [6]** Lab 0 found that **PROG 202's Tuesday and Thursday lectures each run fifteen minutes into
the protected 12:00–13:00 lunch hour** — thirty minutes a week, thirteen weeks.

- **Is this a defect in the timetable or in the claim that the hour is protected?** One paragraph
  each way.
- [[Year2 - Sophomore/SPRING SCHEDULE|SPRING SCHEDULE]] says the hour is protected; the
  [[Year2 - Sophomore/MASTER TIMETABLE|MASTER TIMETABLE]] gives this course Tue/Thu 11:00. **Both are
  registry files.** Which one should be believed, and what principle did you use to decide?
- Propose a fix that changes exactly one number in one file, and say what it breaks. *(Check
  [[Year2 - Sophomore/ROOM ASSIGNMENTS|ROOM ASSIGNMENTS]] before you claim TH 205 is free at 10:00.)*

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

**Late work:** [[Year2 - Sophomore/COURSE POLICIES|COURSE POLICIES]] applies. **The lowest problem
set of the term is dropped**, which is there for the week you are ill, not for the week you forgot.

---

*PROG 202 · Week 0 · PS 0 · © CSE Department*
