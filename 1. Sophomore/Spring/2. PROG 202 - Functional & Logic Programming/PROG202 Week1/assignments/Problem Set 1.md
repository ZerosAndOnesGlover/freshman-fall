# PROG 202 · Problem Set 1
## Algebraic Data Types, Pattern Matching, and Type Inference

---

**Released:** Week 1, Wednesday · **Due:** Week 2, Friday 17:00
**Total: 100 points** · Submit one PDF, `PS1_{LastName}_{StudentID}.pdf`, plus your `.hs` files in a
tarball `PS1_{LastName}.tar.gz`

> **About three hours.** Five questions, fifteen parts.
>
> **Every `.hs` file compiles clean under `ghc -Wall -O2`.** This week that is most of the point:
> `-Wall` is what tells you about the case you forgot, and a submission with an
> `-Wincomplete-patterns` warning has the bug the warning names.
>
> Q1 is by hand first — write the prediction, then check, then report both.

---

### Q1: Counting Types (18 points)

**(a) [8]** How many values does each type have? Show the arithmetic, not just the number.

| Type | Count | Working |
|---|---|---|
| `Maybe (Bool, Bool)` | | |
| `Either Bool (Maybe Bool)` | | |
| `Bool -> Maybe Bool` | | |
| `(Bool, ()) ` | | |
| `Maybe Bool -> Bool` | | |
| `() -> ()` | | |

Then state the three rules in one line each: how many values `(a, b)`, `Either a b` and `a -> b` have
in terms of `|a|` and `|b|`.

**(b) [5]** Write out **all four** values of `Bool -> Bool` as Haskell expressions, using only library
functions and lambdas. Then say how many values `Bool -> Bool -> Bool` has, and give three of them by
name.

**(c) [5]** A colleague proposes this type for a room booking:

```haskell
data Slot = Slot { taken :: Bool, takenBy :: Maybe String, freeFrom :: Maybe Int }
```

- **How many states does `Slot` have**, treating `String` as having *s* values and `Int` as *n*?
- **How many of them are meaningful?** State the invariant the type does not enforce.
- Give a replacement type with exactly the meaningful states and no `Bool`.

---

### Q2: Designing the Type (22 points)

**(a) [8]** An assessment in this course is one of: a problem set with a number and a due week; a lab
with a number and the week it covers; the midterm, which has a week and a coverage range; the final,
which has neither. Some are marked out of 100 and some carry no marks at all.

Write a single Haskell type `Assessment` for this, with **no `Maybe` and no `Bool` anywhere**, such
that no value of the type is meaningless. Then write

```haskell
weight :: Assessment -> Double
```

returning the fraction of the course grade each carries, using the figures in
[[PROG202 Week0/resources/Course Overview Syllabus|the syllabus]]. `-Wall` must be silent.

**(b) [8]** Add to your `Expr` from L04 §4:

```haskell
data Expr = Lit Int | Add Expr Expr | Mul Expr Expr | Neg Expr
```

- Write `eval :: Expr -> Int` and `render :: Expr -> String`. `render` must produce
  `"2 + 3 * 4"` for `Add (Lit 2) (Mul (Lit 3) (Lit 4))` — **with no redundant brackets**, which means
  `render` has to know about precedence.
- Add a `Sub Expr Expr` constructor and recompile **without touching `eval` or `render`**. Report the
  exact warning text for each, and then handle the case.
- `render (Sub (Lit 1) (Sub (Lit 2) (Lit 3)))` must not print `1 - 2 - 3`. Say why, and what your
  code does about it.

**(c) [6]** `deriving Ord` on `data Day = Mon | Tue | Wed | Thu | Fri` gives `Mon < Tue`.

- Where does that ordering come from?
- Give a type where deriving `Ord` this way is a **bug**, and say what the symptom would be.
- `data Priority = Low | Medium | High | Critical` — is deriving `Ord` right here? Justify in one
  sentence either way.

---

### Q3: Pattern Matching (20 points)

**(a) [7]** For each, say whether it compiles, and if so what it matches. If not, say why.

1. `f (Just x : rest) = x`
2. `g all@(x:_) = (all, x)`
3. `h (Session {day = d}) = d`
4. `k [a, b] = a + b`
5. `m (x:x:rest) = x`

One of these is a mistake people make constantly and the error message is not obvious. Say which, and
quote GHC's message.

**(b) [7]** `resources/exhaustive.hs` has the same function over `Kind` and over `String`, each
missing a case. Compile with `-Wall` and report **both** warnings in full.

Then answer: **why can GHC name the missing case for `Kind` and not for `String`?** Two sentences, and
the answer is about the types, not the compiler.

**(c) [6]** Each of these compiles with **no warning at all** under `-Wall` on GHC 9.4.7 and can still
crash. For each, give the input that crashes it and the exact runtime message:

```haskell
data B = Ok { sess :: Int } | Bad { sess :: Int, why :: String }

p :: B -> String
p = why

q :: [Int] -> Int
q = head
```

Then say, for each, **what to write instead** so the crash is not possible. One of the two fixes is a
type change and the other is a data-design change.

---

### Q4: Inference (20 points)

**(a) [7]** Give the type GHC infers for each. Predict by hand, then check with `:t`, and report both.

```haskell
f1 x y  = (y, x)
f2 x    = [x, x]
f3 f x  = f (f x)
f4 g h  = g . h
f5 x    = if x then 1 else 0
```

`f5` is the interesting one and its type is not `Bool -> Int`. Explain what it is and why.

**(b) [7]** Take this module, which has one mistake, on the line marked:

```haskell
minutesOf :: (String, Int, Int) -> Int
minutesOf (_, s, e) = e - s

total :: [(String, Int, Int)] -> Int
total = sum . map minutesOf

average :: [(String, Int, Int)] -> Int
average xs = total xs / length xs          -- MISTAKE HERE

summarise :: [(String, Int, Int)] -> String
summarise xs = "average " ++ show (average xs)
```

- Compile it as written and report the line and message.
- Now **delete every type signature** and compile again. Report the line and message.
- Do the same for Week 0's `Shape.hs` with `snd` changed to `fst`, with and without the signature on
  `busiest`. **One of these two experiments moves the error and one does not.**
- **Explain the difference.** What is true of the second mistake that is not true of the first?

**(c) [6]** *"Inference is good enough that signatures are redundant."* Answer this in one paragraph,
using your own output from (b) as the evidence, and give the one case where a signature changes what
the program **means** rather than only where the error is reported.

---

### Q5: `sched`, Retyped (20 points)

Start from your Lab 1 `Sched.hs`.

**(a) [7]** Run `resources/orderings.py tuple middle strict` and report the table. Then:

- The `middle` design leaves **one** wrong ordering acceptable. Which, and why that one?
- `strict` leaves none. **Give two concrete costs** of the `strict` design, with a line of code each.
- Say which you would ship, and what closes the gap in the one you chose.

**(b) [7]** `mkSession` rejects `start >= end`. Add two more checks it should arguably make, as extra
`Left` cases, and for each say whether a **type** could have done the job instead:

- a session outside 08:00–18:00;
- a `LEC` on a day no lecture is timetabled.

Report `./sched`'s output with a deliberately bad session added for each.

**(c) [6]** `Sched.hs` exports `Session` without its constructor.

- Compile `Break.hs` and report GHC's message verbatim. **It does not say "not exported"** — explain
  what it says instead, in terms of Haskell's two namespaces.
- Change the export to `Session (..)`, compile `Break.hs` again, and report what now happens at **run**
  time.
- In one sentence: why is `mkSession` worthless without the export list?

---

## Marks

| Q | Topic | Parts | Points |
|---|---|---:|---:|
| 1 | Counting types | 3 | 18 |
| 2 | Designing the type | 3 | 22 |
| 3 | Pattern matching | 3 | 20 |
| 4 | Inference | 3 | 20 |
| 5 | `sched`, retyped | 3 | 20 |
| | **Total** | **15** | **100** |

**Late work:** [[Year2 - Sophomore/COURSE POLICIES|COURSE POLICIES]] applies. **The lowest problem
set of the term is dropped.**

---

*PROG 202 · Week 1 · PS 1 · © CSE Department*
