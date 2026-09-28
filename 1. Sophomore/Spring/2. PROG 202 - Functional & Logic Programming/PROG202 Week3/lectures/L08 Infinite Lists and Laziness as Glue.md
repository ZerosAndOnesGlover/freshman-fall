# PROG 202 · Functional & Logic Programming
## Week 3 · Lecture 2 of 2
### Infinite Lists, and Laziness as the Other Kind of Glue

*“The other new kind of glue that functional languages provide enables whole programs to be glued together.”* — John Hughes, "Why Functional Programming Matters" (1989), §5

---

**Sat:** Thursday of Week 3, 11:00–12:15, TH 205 · **Reading:** Hughes, *Why Functional Programming Matters* (1989) — **all 23 pages, this week** · Hutton §15.6–15.8 · **Next:** Week 4 L09, type classes

**Coursework:** 📝 **PS 2** due Fri this week 17:00 · 🔬 **Lab 3** Wed of Week 4 13:00–14:50

---

## 1. `[1..]` Is a Perfectly Ordinary Value

```
ghci> take 10 [1..]
[1,2,3,4,5,6,7,8,9,10]
ghci> take 5 (map (*2) [1..])
[2,4,6,8,10]
ghci> takeWhile (< 20) (filter even [1..])
[2,4,6,8,10,12,14,16,18]
```

**None of those built an infinite list.** `[1..]` is a thunk which, when forced to WHNF, produces one
cons cell whose tail is another thunk. `take 10` forces it ten times and stops. **There was never a
moment at which more than a handful of cells existed** — which is L07 §5's retention argument used for
good: nobody holds the front, so the collector reclaims behind the cursor.

The four ways to make one, and they cover almost everything:

```haskell
[1..]                     -- enumFrom
repeat 7                  -- 7, 7, 7, …
cycle [1,2,3]             -- 1,2,3,1,2,3,…
iterate (*2) 1            -- 1,2,4,8,16,…   <- the important one
```

**`iterate f x` is `[x, f x, f (f x), …]`** and it is how you turn any step function into a stream of
states. Almost every infinite list in real code is an `iterate`.

---

## 2. A Definition May Refer to Itself

```haskell
fibs :: [Integer]
fibs = 0 : 1 : zipWith (+) fibs (tail fibs)
```

```
ghci> take 10 fibs
[0,1,1,2,3,5,8,13,21,34]
```

**`fibs` is defined in terms of `fibs` and it is not a loop.** Trace the first step by hand, which is
the whole trick:

```
fibs            = 0 : 1 : zipWith (+) fibs (tail fibs)
                            zipWith needs one cell of each argument
fibs            = 0 : 1 : …          we already have two cells
tail fibs       =     1 : …
zipWith (+) …   = (0+1) : …          = 1 : …
fibs            = 0 : 1 : 1 : …
```

Each cell is computed from cells **already produced**, so the recursion always has what it needs. This
is called **knot-tying**, and it works because forcing `fibs` to WHNF needs only the `0 :` — which is
available without consulting the recursive part at all.

**`fibs !! 1000` has 209 digits** and is instant, because `Integer` is arbitrary-precision and each
cell is computed once and remembered. Try it: this is sharing paying for itself, and writing the same
thing as a recursive *function* recomputes exponentially.

> **The condition for knot-tying to work is that the definition be *productive*:** forcing the first
> cell must not require the first cell. `xs = zipWith (+) xs (tail xs)` — the same thing without the
> two seed cells — is `<<loop>>`, because the outermost cons is not available until `zipWith` has
> something to work with. **Try both**; the difference is two characters and it is the whole idea.

---

## 3. Hughes's Argument, Which Is This Week's Reading

Hughes's claim is that **laziness is a kind of glue**, and the example is this. Newton's method for a
square root:

```haskell
sqrts :: Double -> [Double]
sqrts n = iterate (\x -> (x + n / x) / 2) 1
```

**That function does not terminate and does not decide when it is done.** It produces approximations
for ever. The stopping rule is a *separate* function:

```haskell
within :: Double -> [Double] -> Double
within eps (a:b:rest) | abs (a - b) <= eps = b
                      | otherwise          = within eps (b:rest)
```

```
ghci> take 8 (sqrts 2)
[1.0, 1.5, 1.4166666666666665, 1.4142156862745097, 1.4142135623746899,
 1.414213562373095, 1.414213562373095, 1.414213562373095]
ghci> within 1e-12 (sqrts 2)
1.414213562373095
```

**Six steps were computed. The seventh was not.**

**This is the modularity claim and it is worth stating precisely.** In an imperative language the
convergence test lives *inside* the iteration loop, because the loop has to know when to stop. So
"Newton's method" and "the stopping rule" are one lump of code, and changing the rule — to *relative*
error, or to "two consecutive equal results", or to "at most twenty steps" — means editing the
algorithm.

Here they are **two functions that do not know about each other**, glued by a list that is never built.
`within 1e-12`, `relative 1e-6`, `take 20` — three stopping rules, no change to `sqrts`.

**Lab 3 §4 asks you to write a second stopping rule** and notice that you did not touch the generator.

### Generate and test

The same shape, more generally: **produce all the candidates, filter to the good ones, take what you
need.**

```haskell
firstPythagorean :: (Int, Int, Int)
firstPythagorean = head [ (a,b,c) | c <- [1..], b <- [1..c], a <- [1..b]
                                 , a*a + b*b == c*c ]
```

**That searches an infinite space and terminates.** The generator is unbounded; `head` decides how much
of it happens. Week 9 is this idea with a different engine — **Prolog's whole execution model is
generate-and-test**, and the reason Weeks 8–10 follow Weeks 0–7 is that laziness makes the idea
familiar before the syntax changes.

---

## 4. The Sieve That Is Not the Sieve

The most-quoted infinite list in Haskell:

```haskell
primes :: [Int]
primes = sieve [2..]
  where sieve (p:xs) = p : sieve [ x | x <- xs, x `mod` p /= 0 ]
```

It is six words of code and it is beautiful and **it is not the Sieve of Eratosthenes.** The real sieve
crosses off multiples by *addition*; this one **divides every survivor by every prime found so far.**

`resources/sieve.hs` measures it against a real incremental sieve that keeps a priority queue of
next-composites and never divides:

| *n*th prime | quoted "sieve" | real sieve |
|---:|---:|---:|
| 2,000 → 17,393 | 0.07 s | 0.02 s |
| 10,000 → 104,743 | **1.51 s** | **0.08 s** |

**19× at the ten-thousandth prime**, and the gap widens: the quoted version does Θ(n²/log n) divisions
where the sieve does Θ(n log log n) additions.

**Why this is in the lecture and not a footnote.** It is the clearest case in the course of a program
that is *elegant, correct, famous, and the wrong algorithm* — and of the fact that laziness makes it
possible to write an algorithm whose cost is not visible in its shape. Nothing in those two lines
suggests a quadratic. **You find out by measuring**, which is L07's Pike quote again.

> **If you want the reference:** Melissa O'Neill, "The Genuine Sieve of Eratosthenes" (*JFP* 19(1),
> 2009) is nine pages on exactly this program and is the source of the priority-queue version in
> `resources/sieve.hs`. Not required reading; excellent.

---

## 5. What Laziness Costs

Three costs, and the first two are the ones that will bite you.

**One: you cannot read the space behaviour off the source.** That is L07 in its entirety. In C, an
array of ten million `int` is forty megabytes and the declaration says so. Here, `sum xs` is 44 KB or
273 MB depending on whether anything else mentions `xs`, and the source looks the same either way.

**Two: errors and non-termination move.** A thunk that throws does so wherever it is *forced*, not where
it was *written*:

```haskell
let x = error "boom" in (length [x, x, x], "fine")
```

**`length` never forces the elements, so this returns `(3, "fine")`.** The error is in the value and
never happens. That is exactly right and it means a stack trace points at the consumer, which is why
GHC's exceptions are less useful than you would like.

**Three: every value is boxed until something proves it need not be.** `[Int]` is a chain of cons cells
each pointing at an `Int` object; `Data.Vector.Unboxed` or an unboxed `Int#` in a strict field is what
you reach for when that matters. L07 §6's `data Acc = Acc !Int !Int` is the small version of this, and
it is why the strict-accumulator row allocated **110 KB** where the pair version allocated 160 MB.

**And the honest summary**, which the lectures have now measured four times:

| Laziness gives you | Laziness costs you |
|---|---|
| infinite structures, and control separated from generation | space behaviour that is not visible in the source |
| short-circuiting for free (`&&`, `foldr`, `take`) | errors that surface at the consumer |
| sharing of expensive results, automatically | boxing, and a thunk per delayed value |
| the ability to define a value in terms of itself | a 727 MB "strict" fold if you do not know what WHNF is |

**None of that is an argument against it.** It is what knowing the language consists of, and it is why
this course spends a week of thirteen here.

---

## 6. What to Take Away

1. **`[1..]` is an ordinary value.** Forcing it to WHNF gives one cell; nothing more ever exists unless
   something holds the front.
2. **`iterate f x` is the general infinite list** and almost every real one is one.
3. **A definition may refer to itself if it is *productive*** — `fibs = 0 : 1 : zipWith (+) fibs (tail
   fibs)` works and `xs = zipWith (+) xs (tail xs)` is `<<loop>>`.
4. **Hughes's point: laziness separates the generator from the stopping rule.** `sqrts` never decides
   when it is done; `within 1e-12` does, and computes six approximations out of infinitely many.
5. **Generate and test searches an infinite space and terminates.** Week 9 is this with a different
   engine.
6. **The famous `primes` is not the Sieve of Eratosthenes** and is **19× slower** than one at the
   ten-thousandth prime. Elegant, correct, famous, wrong algorithm.
7. **Laziness costs you the readability of space behaviour, the locality of errors, and boxing.** The
   first is L07's whole subject.

---

## Exercises

*(Not assessed. PS 3 is the assessed work.)*

1. Write `fibs` and then write `xs = zipWith (+) xs (tail xs)`. Run both. Explain the difference in one
   sentence using the word *productive*.
2. `take 5 (cycle [1,2,3])`, `take 5 (repeat 7)`, `takeWhile (< 100) (iterate (*3) 1)`. Then write
   `cycle` yourself, in one line, using something that refers to itself.
3. Write `relative :: Double -> [Double] -> Double`, a stopping rule on *relative* rather than absolute
   error, and use it with `sqrts`. **Confirm you did not edit `sqrts`.**
4. `let x = error "boom" in length [x, x, x]` returns 3. Now find an expression using the same `x` that
   *does* throw, and one that throws only at `-O0`. *(The second is harder and is worth the time.)*
5. Measure `resources/sieve.hs` at *n* = 20,000 and 50,000. Fit the growth of each version. Then work
   out how large *n* must be before the quoted sieve takes a minute.

---

## Reading

**Hughes, J. — *Why Functional Programming Matters* (1989).** 23 pages, this week, and **on the final.**

Read §1–§2 for the modularity argument, §3 for higher-order functions as glue (which was Week 2), and
**§4–§5 closely** — that is this lecture. §6's game-tree example is the pay-off and is worth the effort.

**Two questions to hold while reading:**

1. §5's `within` is this lecture's example, and Hughes uses it to argue that laziness is *necessary* for
   the modularity he wants. **Is it?** Could you get the same separation with an iterator, a generator,
   or a callback — and what would you have given up? *(This is a final-exam question, and Python's
   generators are a fair answer to bring to it.)*
2. Hughes wrote this in 1989 to argue that functional programming deserved attention. **Which of his
   claims are now simply true of every mainstream language, and which are still only true here?** Week
   12 asks this again with three years more evidence.

---

*PROG 202 · Week 3 · L08 · © CSE Department*
