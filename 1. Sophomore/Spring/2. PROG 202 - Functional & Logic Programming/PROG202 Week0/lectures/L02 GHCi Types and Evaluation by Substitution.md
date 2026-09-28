# PROG 202 · Functional & Logic Programming
## Week 0 · Lecture 2 of 2
### GHCi as a Laboratory: Types, Substitution, and Looking at What Has Not Happened Yet

*“To apply a compound procedure to arguments, evaluate the body of the procedure with each formal parameter replaced by the corresponding argument.”* — Harold Abelson & Gerald Jay Sussman, *Structure and Interpretation of Computer Programs* (1985), §1.1.5, "The Substitution Model"

---

**Reading:** Hutton §2.5–2.7, §3, §4.1–4.4 · **Next:** Week 1 L03, algebraic data types and inference

**Coursework:** 📝 **PS 0** released Wed this week, due Fri of Week 1 17:00 · 🔬 **Lab 0** Fri this week 13:00–14:50

---

## 1. The Shape of a Haskell Program

Here is a whole one. It is `lab/Shape.hs`, and every part of it is load-bearing.

```haskell
module Main where                       -- 1. the module header

import Data.List (sort)                 -- 2. explicit import list

-- | Minutes of contact time in one session.
minutes :: Int -> Int -> Int            -- 3. a type signature
minutes start end = end - start         -- 4. an equation, not an assignment

busiest :: [(String, Int)] -> String    -- 5. a signature with structure in it
busiest = snd . last . sort . map swap  -- 6. a definition with no arguments
  where swap (c, m) = (m, c)            -- 7. a local definition

main :: IO ()                           -- 8. the one action the runtime performs
main = putStrLn (busiest table)
  where table = [("CS 202", 150), ("PROG 202", 260), ("CS 290", 50)]
```

**Four things that are not like C, and each is the subject of a later week.**

- **A type signature is optional and you write it anyway.** GHC can infer `minutes`' type (Week 1);
  you write it because it is the clearest documentation there is and because the error message when
  you are wrong points at the right line instead of a line four functions away.
- **`minutes start end = end - start` is an equation.** It does not *do* anything. It says that
  wherever `minutes a b` appears you may write `b - a`, and that is the only thing it says.
- **`busiest` is defined with no arguments at all.** It is a *composition* of four functions, and
  composition is a value like any other. Week 2 is this line.
- **`where` binds names local to one equation.** Not a block, not a scope you can assign into — a
  set of further equations.

**Run it three ways.** `runghc Shape.hs` interprets it. `ghci Shape.hs` loads it and gives you a
prompt. `ghc -Wall -O2 -o shape Shape.hs && ./shape` compiles it. §5 measures what that choice costs.

---

## 2. Evaluation Is Substitution, and You Can Do It by Hand

Because every definition is an equation, **evaluating a Haskell expression is replacing the left-hand
side by the right-hand side until nothing is left to replace.** There is no machine state to track.

```haskell
double x = x + x
quad   x = double (double x)
```

```
   quad 3
=  double (double 3)          -- by the definition of quad
=  double 3 + double 3        -- by the definition of double
=  (3 + 3) + (3 + 3)          -- twice more
=  6 + 6
=  12
```

**Every line is an ordinary equation and you may apply them in any order.** Try the other order:

```
   quad 3
=  double (double 3)
=  double (3 + 3)
=  double 6
=  6 + 6
=  12
```

**Same answer, four steps instead of five.** That it is the same answer is §2 of L01 — referential
transparency — and it is what makes the choice of order a *performance* question rather than a
*correctness* one. The second order is *call by value*: evaluate the argument first. The first is
*call by name*: substitute the argument unevaluated.

**Haskell does neither.** It does *call by need*: substitute unevaluated, but **remember the result
the first time anyone asks**, so `double 3` is computed once even though it appears twice. That is
the sharing L01 §3 measured, and unlike the `-O2` optimisation there, it is guaranteed. Week 3 is
about what it costs.

> **Doing this by hand is not a party trick.** Weeks 3, 5 and 9 all have questions on the exam that
> are "reduce this expression and show your steps", and Week 9 is the same exercise for Prolog, where
> the rewriting rule is unification rather than substitution.

---

## 3. GHCi Is the Laboratory

Six commands, and you will use all six every day of this course.

| Command | What it tells you |
|---|---|
| `:t expr` | The **type** of an expression, inferred. Your first move, always |
| `:i name` | **Information**: where it is defined, its fixity, and every instance it has |
| `:sprint x` | What `x` **has actually been evaluated to so far**. Nothing else shows you this |
| `:set +s` | Print **time and allocation** after every expression |
| `:l File` / `:r` | Load a file; reload it after editing |
| `:{ … :}` | A multi-line definition at the prompt |

Real session, GHC 9.4.7:

```
ghci> :t (++)
(++) :: [a] -> [a] -> [a]
ghci> :t ($)
($) :: (a -> b) -> a -> b
ghci> :t (.)
(.) :: (b -> c) -> (a -> b) -> a -> c
ghci> :t fmap
fmap :: Functor f => (a -> b) -> f a -> f b
ghci> :t 3
3 :: Num a => a
ghci> :t 3.5
3.5 :: Fractional a => a
```

**Two of those deserve a pause now and a week later.**

`:t 3` says `Num a => a` — **the literal `3` does not have a type; it has a constraint.** It is
whatever numeric type the context needs. This is why `length xs / 2` is a type error in Haskell and
compiles in every other language you know, and it is Week 4's whole subject.

`:t (.)` — `(b -> c) -> (a -> b) -> a -> c` — is function composition, and reading that signature
until it is obvious is fifteen minutes well spent. **It takes two functions and returns a function.**
Nothing is applied to anything; the result is a new function waiting for its `a`.

```
ghci> :i Bool
type Bool :: *
data Bool = False | True
  	-- Defined in ‘GHC.Types’
instance Bounded Bool  -- Defined in ‘GHC.Enum’
instance Enum Bool     -- Defined in ‘GHC.Enum’
instance Show Bool     -- Defined in ‘GHC.Show’
instance Read Bool     -- Defined in ‘GHC.Read’
instance Eq Bool       -- Defined in ‘GHC.Classes’
instance Ord Bool      -- Defined in ‘GHC.Classes’
```

**`Bool` is not built in.** It is an ordinary two-constructor data type defined in a library, with
six instances, and you could write it yourself in one line. Week 1 does.

---

## 4. `:sprint` — Looking at What Has Not Happened

This is the command nobody finds on their own, and it is the reason GHCi is a laboratory rather than
a calculator. **`:sprint` prints a value without forcing any part of it**, showing unevaluated pieces
as `_`.

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

**Read those three `:sprint`s slowly, because they are the whole of Week 3 in six lines.**

1. After `let`, **nothing has been computed.** `xs` is a *thunk*: a pointer to code and its captured
   environment. The `map` has not run. `[1..5]` has not been built.
2. `length xs` needed to know **how many cells there are** and nothing about what is in them. So the
   list structure — the *spine* — was built, and each element is still an unevaluated `_`. `length`
   never looked at a single number.
3. `sum xs` needed the numbers, so now they exist.

**This is why `length` on a list of expensive computations is cheap, and it is also why a program
can hold five million unevaluated additions and then fall over.** Both halves are Week 3.

`:set +s` adds the second instrument:

```
ghci> :set +s
ghci> sum [1..1000000::Int]
500000500000
(0.02 secs, 88,074,288 bytes)
```

**88 MB allocated to add up a million numbers.** Not leaked — allocated and immediately collected;
GHC's nursery is a bump allocator and this is normal and fast. But the number is the honest one, and
**the habit of looking at allocation rather than at time** is what this course wants you to leave
with. Time is noisy and machine-specific; allocation is deterministic and is usually the cause.

---

## 5. `runghc`, `-O0`, `-O2`: Measure Before You Believe

`resources/primes.hs` counts the primes below 300,000 by trial division — deliberately naive, so that
the time is dominated by ordinary arithmetic.

| How it was run | Time | Relative |
|---|---:|---:|
| `runghc primes.hs` *(interpreted)* | **8.5 s** | 57× |
| `ghc -O0 -o p0 primes.hs; ./p0` | **1.03 s** | 6.9× |
| `ghc -O2 -o p2 primes.hs; ./p2` | **0.15 s** | 1× |

All three print `25997`.

**Three rules come out of this table and they hold for the whole term:**

1. **Never quote a timing from `ghci` or `runghc`.** It is measuring the interpreter. Every
   measurement in this course, and every measurement in your problem sets, comes from a binary built
   with `ghc -O2`.
2. **`-O0` is not "unoptimised Haskell", it is a different language performance-wise.** The 6.9×
   between `-O0` and `-O2` is mostly strictness analysis and inlining, and L01 §3's exercise 4 shows
   a case where it is the difference between 44 KB and 604 MB of live memory.
3. **`ghci` is still where you work.** Its job is `:t`, `:sprint` and trying things, and it is
   excellent at that. It is not a benchmark harness.

---

## 6. The Measurement That Inverts the Instinct

You have been taught, correctly, in every other course, not to compute the same thing twice. Here is
that advice applied to Haskell, and measured. `resources/share2.hs`, both lines compiled `-O2`:

```haskell
-- (a) the list is written out twice
print (sum [1..10000000], length [1..10000000])

-- (b) the list is named once and used twice
let xs = [1..10000000] in print (sum xs, length xs)
```

| `-O2` | allocated | maximum residency | time |
|---|---:|---:|---:|
| **(a) written twice** | **53 KB** | **44 KB** | 0.007 s |
| **(b) named once** | 640 MB | **273 MB** | 1.11 s |

**Same answer. The version that mentions the list twice holds 6,100× less memory and runs 160×
faster.**

The reason is exactly L01 §2's sharing, turned against you. In **(b)**, `xs` is a name, and a name
must denote one value; `sum` walks it from the front while `length` still needs the front, so **every
cell must be kept alive between the two traversals** — ten million cons cells, 273 MB of them. In
**(a)** the two lists are separate expressions and neither is ever retained, so each cell is
collected the moment it has been added up.

**Now run the same two at `-O0`, because the four numbers together say something neither pair says
alone:**

| | `-O0` allocated | `-O0` residency | `-O2` allocated | `-O2` residency |
|---|---:|---:|---:|---:|
| written twice | 1,600 MB | **44 KB** | **53 KB** | **44 KB** |
| named once | 880 MB | **245 MB** | 640 MB | **273 MB** |

**Two different effects, and students routinely merge them:**

- **The residency gap is not the optimiser's doing.** 44 KB against 245 MB is already there at
  `-O0`. It is *retention*: laziness plus garbage collection stream a list that nobody is holding
  on to, and a name is holding on to it. **`-O2` cannot fix this and does not.**
- **What `-O2` does is delete the list.** Allocation for the written-twice version falls from
  1,600 MB to **53 KB** — GHC's *list fusion* rewrites `sum [1..n]` into a counting loop with no
  cons cells at all. For the named version fusion is impossible, because the list is shared, so its
  allocation stays at 640 MB.

**Fusion is an optimisation you can lose by naming something.** That is the sentence to carry into
Week 3.

> **This is the single most important fact in Week 0 and it is not a Haskell wart.** It is what
> happens when *how much memory a program uses* stops being visible in the source text. C tells you:
> an array of ten million `int` is forty megabytes, there it is in the declaration. Haskell does not,
> and the instrument that tells you instead is `+RTS -s`. **Week 3 is called "Lazy Evaluation" and it
> is really called "this table".**

---

## 7. `-Wall` From Today

```
ghc -Wall -O2 -o prog Prog.hs
```

`-Wall` is not optional in this course and warnings cost marks from PS 0, the same rule PROG 201
used for `gcc -Wall -Wextra`. The three you will actually hit:

| Warning | What it usually means |
|---|---|
| `Top-level binding with no type signature` | Write the signature. It is the documentation and it improves the error messages |
| `Pattern match(es) are non-exhaustive` | **A case you did not handle, which is a crash waiting.** Week 1 is about making this impossible |
| `Defined but not used` | Usually a typo in a `where` clause: you defined `helper` and called `helpr` |

The middle one is the one that matters. In C an unhandled case falls through; in Haskell it is a
runtime `Non-exhaustive patterns` error — and **the compiler already knew**, and told you, and you
did not have `-Wall` on.

---

## 8. What to Take Away

1. **A Haskell program is equations plus one `main :: IO ()`.** A signature is optional; write it.
2. **Evaluation is substitution**, and you can do it on paper. Haskell substitutes unevaluated and
   remembers the result: **call by need**.
3. **`:t` is your first move**, `:i` your second. `:t 3` is `Num a => a` and that will matter in
   Week 4.
4. **`:sprint` shows what has not been computed yet.** `xs = _` → `[_,_,_,_,_]` → `[2,4,6,8,10]`, as
   `length` and then `sum` forced more of it. Nothing else in the toolchain shows you this.
5. **`runghc` is 57× slower than `-O2` here.** Never quote a timing from it.
6. **`+RTS -s` is the instrument.** Watch allocation and maximum residency, not the clock.
7. **Naming a list you traverse twice cost 273 MB where writing it twice cost 44 KB**, at both
   optimisation levels — that gap is *retention*, not the optimiser. What `-O2` adds is **fusion**,
   which deletes the list entirely (1,600 MB of allocation down to 53 KB) and which **naming the
   list switches off**. Hold on to both until Week 3.
8. **`-Wall`, always.** Especially for non-exhaustive patterns.

---

## Exercises

*(Not assessed. Five minutes each at a `ghci` prompt.)*

1. Reduce `quad (quad 2)` by hand in both orders from §2, counting the `+` operations each way.
   Then define `double x = x + x` in GHCi with `:set +s` on and check which count the allocation
   figure is nearer to.
2. `:t` these and explain each: `map`, `map map`, `(.) (.)`, `flip`, `zipWith3`. The third is
   deliberately horrible; the exercise is to read it anyway.
3. Reproduce §4's three `:sprint` outputs, then find an expression that forces the *last* element of
   `xs` and nothing else. What does `:sprint` show?
4. Run §6's two versions yourself with `+RTS -s`, at `-O0` and `-O2`, and reproduce all eight
   numbers. Then try a third version: `let xs = [1..10000000] in print (sum xs)` — **named, but used
   once**. Predict its residency *and* its allocation at each level before you run it. One of the
   four is 52 KB and one is 880 MB.
5. Compile a program with a deliberately non-exhaustive pattern match, with and without `-Wall`, and
   run each. Which of the two error messages tells you the line number of the pattern?

---

*PROG 202 · Week 0 · L02 · © CSE Department*
