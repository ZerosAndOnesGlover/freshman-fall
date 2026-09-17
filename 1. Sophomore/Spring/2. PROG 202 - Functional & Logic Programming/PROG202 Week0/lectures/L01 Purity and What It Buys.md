# PROG 202 · Functional & Logic Programming
## Week 0 · Lecture 1 of 2
### Purity, Referential Transparency, and What Forbidding Assignment Buys

---

**Reading:** Hutton §1.1–1.5, §2.1–2.4 · **Next:** L02, GHCi and how evaluation actually proceeds

---

## 1. The Paradigm, in One Sentence

**A program is an expression to be evaluated, not a sequence of commands to be obeyed.**

Everything else follows from taking that literally. Here is the same computation in both paradigms:

```c
/* C: a sequence of commands that change a store */
int total = 0;
for (int i = 0; i < n; i++) total += price[i] * qty[i];
```

```haskell
-- Haskell: one expression, no variable that changes
total = sum (zipWith (*) prices quantities)
```

The C version has a variable `total` that holds four different values over its lifetime, and an `i`
that holds `n+1`. The Haskell version has **no variable that ever holds two different values**. That
is not a stylistic preference; the language has no construct that would let you write one.

**`x = x + 1` is not discouraged in Haskell. It is a definition, and it is a lie.** It says *x is
one more than itself*, which is true of no number; asked for the value, the machine tries to compute
`x` in order to compute `x` and never gets anywhere. Compiled, the runtime notices:

```
$ ghc -O0 -o loopx loopx.hs && ./loopx
loopx: <<loop>>
```

**`<<loop>>` is the RTS catching the program entering a thunk that is already being evaluated** — a
*blackhole*. It is not a general non-termination detector (nothing can be), it is one cheap check
that happens to catch this. In `ghci` the same definition simply hangs, because the bytecode
interpreter does not blackhole the same way. Lab 0 §3 has you do both.

---

## 2. Referential Transparency, Stated Precisely

> **An expression is referentially transparent when it can be replaced by its value without changing
> the meaning of the program.**

That is the whole definition and it is worth reading twice, because two useful consequences fall out
of it immediately.

**Consequence one: equals can be substituted for equals.** If `area r = pi * r * r`, then anywhere
`area 3` appears you may write `pi * 3 * 3`, and anywhere *that* appears you may write `28.274334`.
This is exactly what you do in algebra, and it is exactly what you cannot do in C, where
`area(3)` might print something, or increment a counter, or return a different answer the second time.

**Consequence two: the order of evaluation cannot change the answer.** If no expression can affect
another except by being its input, then `f x + g y` means the same thing whichever of `f x` and
`g y` is computed first, or if they are computed on different cores, or if one of them is never
computed at all.

**This is the property the whole course is about.** Weeks 2 and 4 use it to build abstractions that
would be unsound otherwise; Week 3 uses it to postpone computation indefinitely; Week 7 uses it to
run things in parallel with no locks; Week 11 uses it to generate ten thousand test inputs and know
that the function under test cannot have been corrupted by the previous nine thousand.

### The word "pure"

A **pure** function's result depends on its arguments and nothing else, and evaluating it changes
nothing outside itself. `sin`, `length`, `sort` are pure. `time()`, `rand()`, `getchar()`,
`malloc()` and any function that writes to a global are not.

**Haskell's rule is not "be pure".** It is: **a function whose type does not mention an effect cannot
have one.** The type is the enforcement, and §6 is where that becomes concrete.

---

## 3. What Purity Buys: One Measurement

Here is an optimisation every compiler wants to make. You have written

```
expensive(n) + expensive(n)
```

and the compiler would like to run `expensive` **once**. This is *common subexpression elimination*,
and whether it is legal depends entirely on whether `expensive` is pure.

`resources/cse.c` defines two functions with byte-identical arithmetic. The second has one extra
line — `calls++`, incrementing a global that nothing ever reads:

```c
__attribute__((noinline))
long pure_sum(long n)   { long s = 0; for (long i = 1; i <= n; i++) s += i; return s; }

__attribute__((noinline))
long impure_sum(long n) { long s = 0; for (long i = 1; i <= n; i++) s += i; calls++; return s; }
```

`gcc -O2`, GCC 13.3.0, *n* = 1,000,000,000:

| C function | called once | called twice | did GCC share it? |
|---|---:|---:|---|
| `pure_sum` | 0.44 s | **0.44 s** | **Yes** — it proved the body was pure and ran the loop once |
| `impure_sum` | 0.44 s | **0.88 s** | **No** — one write to a counter nobody reads, and the optimisation is gone |

**The line that cost 0.44 seconds was `calls++`.** GCC did the right thing: the two calls are no
longer interchangeable, because a caller could in principle observe how many happened. It cannot
know that nothing does.

Now the same shape in Haskell — `resources/cse.hs`, `ghc -O2` 9.4.7, same *n*:

| Haskell | once | twice |
|---|---:|---:|
| `expensive n` at `-O2` | 0.31 s | **0.32 s** |
| `expensive n` at `-O0` | 0.19 s *(n = 2×10⁷)* | **0.38 s** |

At `-O2`, `expensive n + expensive n` costs what one call costs — and the times scale linearly with
*n* (0.04 s / 0.13 s / 0.31 s for 10⁸ / 4×10⁸ / 10⁹), so this is a real loop that ran once, not a
closed form the compiler spotted.

**At `-O0` it runs twice, exactly 2×.** That matters: sharing is an *optimisation GHC is permitted
to make*, not a semantic guarantee. Week 3 is about the one form of sharing that *is* guaranteed.

> **Read the table correctly.** The claim is **not** "Haskell is faster than C" — the two loops are
> different machine code and the comparison of 0.31 s to 0.44 s means very little. The claim is about
> **which transformation was legal without proof.** GCC had to prove purity and could only do it for
> one of two functions that differ by one line. GHC never has to prove it, because there is no way to
> write the line.

---

## 4. What Purity Costs: There Is No Assignment

You now cannot write a loop with an accumulator. The replacement is **recursion**, and then — from
Week 2 — a **fold**, which is the pattern all such recursions share.

```haskell
-- Sum a list.  Three ways, all pure, all in this week's lab.
sum1 :: [Int] -> Int                      -- explicit recursion
sum1 []     = 0
sum1 (x:xs) = x + sum1 xs

sum2 :: [Int] -> Int                      -- the accumulator becomes an argument
sum2 = go 0
  where go acc []     = acc
        go acc (x:xs) = go (acc + x) xs

sum3 :: [Int] -> Int                      -- the pattern, named (Week 2)
sum3 = foldr (+) 0
```

**`sum2` is the loop.** `acc` is the mutable variable, except that instead of being overwritten it is
*passed forward* — each call gets its own, and none of them ever changes. The machine code GHC emits
for `sum2` is a loop with a register that is overwritten, which is the point: **immutability is a
property of the language you write, not of the hardware it runs on.**

### "Immutable means copying, and copying is slow"

This is the first objection, and it is a good one. If a value never changes, then `insert` into a
1,000,000-entry map must build a new 1,000,000-entry map, which is absurd.

It does not. `resources/persist.hs` builds a `Data.Map.Strict` of *n* entries and then performs
100,000 single inserts **into that same map**, never into the result of the previous insert:

| Map size *n* | allocated by 100,000 inserts | **per insert** |
|---:|---:|---:|
| 1,000 | 56.0 MB | **560 bytes** |
| 1,000,000 | 104.0 MB | **1,040 bytes** |

**A thousand times as many entries, and the insert costs 1.86× as much.** `log₂ 1000 = 10` and
`log₂ 10⁶ = 20`, so the prediction was exactly 2×. A persistent balanced tree copies **the path from
the changed leaf to the root** and shares every other subtree with the original — about twenty nodes
here, not a million.

**This is only safe because nothing can change.** A mutable tree cannot share subtrees with its own
previous version, because someone might write through the sharing. Immutability is what *pays for*
the structure that makes immutability affordable. Week 4 comes back to this with `Foldable`.

---

## 5. The Bug Class That Disappears

`resources/alias.py` is three lines of ordinary Python:

```python
def normalise(names):
    names.sort()              # in place.  The caller's list is now sorted too.
    return names

roster = ["Zainab", "Adebayo", "Chen"]
first  = roster[0]
sorted_roster = normalise(roster)
print("roster[0] was", first, "and is now", roster[0])
```

```
roster[0] was Zainab and is now Adebayo
```

**`roster` was changed by a function that was handed it.** The caller never asked for that and the
signature `normalise(names)` does not say it happens. The defence, in every imperative language, is
to copy before you pass — which costs what a copy costs, and which you will forget.

There is no Haskell translation of this program, because `sort` has the type

```haskell
sort :: Ord a => [a] -> [a]
```

It **takes a list and returns a list.** There is no version of `sort` that takes a list and returns
`()` having rearranged it, and the reason is not that the library authors chose well — it is that the
type `[a] -> ()` has exactly one inhabitant, the function that ignores its argument and returns `()`,
and it could not possibly have done anything useful on the way.

> **This is the first appearance of the idea Week 12 closes on.** A type in Haskell is a claim about
> what a function *can* do, not a claim about what shape its bits are. `[a] -> ()` cannot do
> anything; `[a] -> [a]` cannot look at the elements *(it is polymorphic in `a`, so what would it
> look at them with?)*; `Ord a => [a] -> [a]` can compare them and nothing else. Week 4 makes that
> precise and Week 12 gives it its name.

---

## 6. So Where Does the I/O Go?

A program that cannot have effects cannot print. Haskell's answer is not an exception to purity — it
is a type.

```
ghci> :t putStrLn
putStrLn :: String -> IO ()
ghci> :t getLine
getLine :: IO String
```

**`IO String` is not `String`.** It is a *description of an action* which, when the runtime performs
it, will yield a `String`. `getLine` is a pure value: it is the same value every time you mention it,
in the way that a recipe is the same recipe however many cakes you bake from it.

```haskell
main :: IO ()
main = do
  name <- getLine              -- perform the action, bind its result
  putStrLn ("hello, " ++ name)
```

Two things to notice, and both are Week 5's subject in embryo:

- **`<-` is not assignment.** It is the *only* way to get the `String` out of an `IO String`, it
  works only inside a `do` block that is itself building an `IO` action, and `name` — once bound —
  never changes.
- **The type of `main` is the honest declaration.** `main :: IO ()` says *this program performs
  effects and produces nothing*. A function whose type is `Int -> Int` performs none, and the
  compiler enforces that, which is why §3's optimisation is always available.

**There is no way to write `unsafeRead :: () -> String`** that reads a line — not because of a
convention, but because the only way to run an `IO` action is to be part of `main`, and the only way
to be part of `main` is to have `IO` in your type. *(There is one deliberate hole,
`unsafePerformIO`, which exists so that people who are writing the libraries this rule is enforced
by can break it. Week 5 §8 shows what it is for and what it costs. It is not for you yet.)*

---

## 7. What This Buys That You Can Use Tomorrow

Even if you never write Haskell again — and the curriculum's own note says that is not the point —
three of this week's ideas transfer without modification:

1. **Separate the computation from the effect.** A function that computes and a function that prints
   are two functions. The computing one is testable, cacheable, parallelisable and reviewable; the
   printing one is none of those. *(This is CS 212's "unit testable" and CS 212's `confirm_booking`,
   487 lines with 11 tests, from the other side.)*
2. **Never mutate an argument.** If a caller has to read your implementation to know whether its
   data survived the call, your signature is lying. Week 11 has the version of this argument that
   comes with evidence.
3. **Make the type say it.** `Optional<User>` in Java, `Option<T>` in Rust, `T | None` in Python's
   type hints — all three are Week 1's `Maybe`, and the reason they exist is Week 5's.

---

## 8. What to Take Away

1. **A program is an expression.** No statement sequence, no store, no variable that changes.
2. **Referential transparency:** an expression can be replaced by its value. Everything in this
   course is downstream of that sentence.
3. **Purity is what makes the optimisation legal.** GCC lost common subexpression elimination to a
   single `calls++`; GHC cannot lose it, because the line is unwritable. **0.44 s versus 0.88 s.**
4. **Immutability is affordable because sharing is safe.** A persistent insert into a map 1,000×
   larger costs **1.86×**, not 1,000×.
5. **Aliasing bugs do not have a Haskell translation.** `sort :: Ord a => [a] -> [a]`, and there is
   no other kind.
6. **Effects live in types.** `IO String` is a description of an action, not a string; `<-` is the
   only way through, and it is not assignment.
7. **Sharing at `-O2` is an optimisation, not a promise.** At `-O0` the same program runs the
   computation twice. Week 3 is about the sharing that *is* promised, and about what it costs.

---

## Exercises

*(Not assessed. PS 0 is the assessed work; these are five minutes each in `ghci`.)*

1. Put `let x = x + 1 :: Int` and `print x` in a file, compile it, and run it; then type the same
   two lines into `ghci`. **You get `<<loop>>` from one and a hang from the other.** Say which is
   which and why neither is a type error. Then try `let x = 1 + 1` and `:sprint x` before and after
   asking for `x`.
2. `:t` each of these and say which could possibly perform an effect: `length`, `putStr`, `readFile`,
   `lines`, `interact`. One of them will surprise you.
3. Add a third function to `cse.c` that is pure but whose body GCC cannot see (`long ext_sum(long);`
   defined in another translation unit, compiled separately). Predict which column it lands in,
   then check. What flag changes the answer?
4. Compile `sum1` and `sum2` from §4 with `-rtsopts`, run each on `[1..10000000]`, and report
   **maximum residency** from `+RTS -s`. Do it at `-O0` and at `-O2`. **One of the four numbers is
   44 KB and one is 604 MB**, and which version wins is not the same at both optimisation levels.
   Write down your explanation now; Week 3 will tell you whether it was right.
5. Rewrite `alias.py` so that the bug cannot happen, without changing `normalise`'s callers. Count
   the characters you had to add, and say what you would have to remember in order to add them.

---

*PROG 202 · Week 0 · L01 · © CSE Department*
