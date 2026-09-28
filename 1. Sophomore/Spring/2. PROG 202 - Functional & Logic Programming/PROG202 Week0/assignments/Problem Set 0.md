# PROG 202 · Problem Set 0
## Purity, Referential Transparency, and Reading a Type

---

**Released:** Week 0, Wednesday · **Due:** Week 1, Friday 17:00
**Total: 100 points** · Submit one PDF, `PS0_{LastName}_{StudentID}.pdf`, plus your `.hs` files in a
tarball `PS0_{LastName}.tar.gz`

> **About three hours.** Five questions, fifteen parts. If it is taking much longer than that, stop
> and bring the rest to office hours — that is information the course wants, not a failure.
>
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
> course from PS 0 onwards.

---

### Q1: Reading a Type (20 points)

**(a) [8]** For each expression, **write the type by hand**, then check with `:t`. Report both.

| Expression | Your prediction | `:t` says |
|---|---|---|
| `map reverse` | | |
| `(.)` | | |
| `zip [1,2,3]` | | |
| `3` | | |

**(b) [6]** Name each symbol out loud, the way
[[PROG202 Week0/resources/Haskell Syntax and Symbols|Haskell Syntax and Symbols]] names it, and say
what it does: `::`  `=>`  `->`  `:`  `$`

Then, using `elem :: Eq a => a -> [a] -> Bool`: **how many arguments does `elem` take?** Explain the
difference between `->` and `=>` in one sentence.

**(c) [6]** Given `add :: Int -> Int -> Int`, `add x y = x + y`:

- What is the type of `add 3`?
- `map (add 3) [1,2,3]` works. Explain, in terms of currying, **why it has to**.

---

### Q2: Referential Transparency (20 points)

**(a) [6]** For each, say whether it is referentially transparent — whether the expression may be
replaced by its value without changing the program's meaning — and why:

1. `length [1,2,3]`
2. `getLine`
3. `unsafePerformIO getLine`

**`getLine` is referentially transparent.** Say why, and say what *is* different about it.

**(b) [8]** Compile `resources/cse.c` with `gcc -O2` and time all four cases at *n* = 10⁹:

| | once | twice |
|---|---|---|
| `pure_sum` | | |
| `impure_sum` | | |

**One line of C — `calls++`, incrementing a global nothing reads — is the difference.** Explain what
the compiler lost and why losing it was correct. Then **try to win it back** (one obvious change
suggests itself), report what happened, and say what that tells you.

**(c) [6]** Run `resources/cse.hs` at `-O2` and at `-O0`; report the four numbers. **At `-O0` the
sharing does not happen** — is that a bug in GHC? Two sentences.

Then answer a colleague who says *"purity just means the compiler optimises better; I care about
correctness."* One paragraph, and **do not argue from performance.**

---

### Q3: Evaluation by Substitution (20 points)

**(a) [8]** Given `double x = x + x` and `quad x = double (double x)`:

Reduce `quad 3` to a number **twice** — once evaluating the argument first (call by value), once
substituting it unevaluated (call by name). Show every step and **count the `+` operations each
way**. Then say which count Haskell actually performs, and why it is neither of those two strategies.

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
and what it did not, and why the notation changes between the second and third.

**(c) [6]** `x = x + 1` compiled gives `<<loop>>`; in `ghci` it hangs.

- What is a *blackhole*, and **which component installs it** — compiler or runtime?
- Write a non-terminating Haskell program that `<<loop>>` does **not** catch, and explain in one
  sentence why it cannot.

---

### Q4: Measurement (22 points)

State your `ghc --version` and `uname -r` at the top of this answer.

**(a) [5]** Reproduce L02 §5's table with `resources/primes.hs`:

| How run | Your time |
|---|---|
| `runghc primes.hs` | |
| `ghc -O0` | |
| `ghc -O2` | |

Report the ratio between the first and the last, then **state the rule this table exists to
establish** in one sentence — and obey it for the rest of this problem set.

**(b) [10]** Fill in all nine cells for `resources/share2.hs`, using `+RTS -s`:

| | `-O0` allocated | `-O0` residency | `-O2` allocated | `-O2` residency |
|---|---|---|---|---|
| `twice` | | | | |
| `named` | | | | |
| `once` | | | | |

**`once` is the row to predict before you run it** — the list is *named*, like `named`, but used
once. Report your prediction and the result.

Then: **one of the two gaps in this table is present at both optimisation levels and the other only
at `-O2`.** Say which is which, and name the mechanism behind each.

**(c) [7]** Take L01 §4's two definitions:

```haskell
sum1 []     = 0
sum1 (x:xs) = x + sum1 xs

sum2 = go 0 where go acc []     = acc
                  go acc (x:xs) = go (acc + x) xs
```

Measure maximum residency for each on `[1..10000000::Int]`, at `-O0` and at `-O2`. **Four numbers.**

`sum2` is the one that looks like a loop and the one everyone is told to prefer. **At one of the two
optimisation levels it is worse.** Report which, and give your best hypothesis why.

*(You are not expected to be right. The marks are for a hypothesis consistent with your own four
numbers — Week 3 will tell you whether it was.)*

---

### Q5: `sched` (18 points)

Start from your Lab 0 `Sched.hs`.

**(a) [6]** Add `contactPerCourse :: [(String, Int)]` — each course with its weekly contact minutes,
sorted by minutes descending. Report the output, and **check the total is still 1,070.**

Two courses tie at the top by different routes. Say which, and what that says about this course's
two-lecture week.

**(b) [6]** Your `overlaps` uses `s1 < e2 && s2 < e1`.

- Write out the four interval cases — disjoint before, disjoint after, touching, containing — and
  show the condition is right for each.
- Change both `<` to `<=`, re-run, and report **how many extra lines appear and where**. One of the
  two checks is unaffected; explain why.

**(c) [6]** Lab 0 found that **PROG 202's Tuesday and Thursday lectures each run fifteen minutes into
the protected 12:00–13:00 lunch hour.**

- **Defect in the timetable, or in the claim that the hour is protected?** One paragraph each way.
- [[Year2 - Sophomore/SPRING SCHEDULE|SPRING SCHEDULE]] says the hour is protected;
  [[Year2 - Sophomore/MASTER TIMETABLE|MASTER TIMETABLE]] gives this course Tue/Thu 11:00. Both are
  registry files. **Which should be believed, and what principle did you use to decide?**
- Propose a fix that changes exactly one number in one file, and say what it breaks. *(Check
  [[Year2 - Sophomore/ROOM ASSIGNMENTS|ROOM ASSIGNMENTS]] before you claim TH 205 is free at 10:00.)*

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

**Late work:** [[Year2 - Sophomore/COURSE POLICIES|COURSE POLICIES]] applies. **The lowest problem
set of the term is dropped**, which is there for the week you are ill, not for the week you forgot.

---

*PROG 202 · Week 0 · PS 0 · © CSE Department*
