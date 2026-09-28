# PROG 202 · Functional & Logic Programming
## Week 2 · Lecture 2 of 2
### `foldr`, `foldl`, `foldl'` — and Measuring Which One Is Wrong

*“Unlike von Neumann languages, the language of ordinary algebra is suitable both for stating its laws and for transforming an equation into its solution, all within the 'language.'”* — John Backus, "Can Programming Be Liberated From the von Neumann Style?" (Turing Award lecture, 1977)

---

**Sat:** Thursday of Week 2, 11:00–12:15, TH 205 · **Reading:** Hutton §7.4–7.6 · **Next:** Week 3 L07, lazy evaluation and where these numbers come from

**Coursework:** 📝 **PS 1** due Fri this week 17:00 · 📊 **Quiz 3** Tue of Week 3 · 📝 **PS 3** released Wed of Week 3, due Fri of Week 4 17:00 · 🔬 **Lab 2** Wed of Week 3 13:00–14:50

---

## 1. The Shape Four Functions Shared

L05 §5 left four functions that differed only in an operator. Here is the same observation on lists,
which is where it is easiest to see:

```haskell
sum     []     = 0            product []     = 1            length []     = 0
sum     (x:xs) = x +  sum xs   product (x:xs) = x * product xs
                                                              length (_:xs) = 1 + length xs
```

**Two equations each, identical in shape, differing in a starting value and a combining function.** So
make those the arguments:

```haskell
foldr :: (a -> b -> b) -> b -> [a] -> b
foldr f z []     = z
foldr f z (x:xs) = f x (foldr f z xs)
```

**That is the whole definition**, and if you `:t` it you will get something wider than the signature
above:

```
ghci> :t foldr
foldr :: Foldable t => (a -> b -> b) -> b -> t a -> b
```

**`t a` rather than `[a]`** — the real `foldr` works on any container that can be folded, not only
lists. That is Week 4's subject; this whole lecture is about the list case and the list signature is
the one to hold in your head for now.

Every one of the three above is now one line:

```haskell
sum     = foldr (+) 0
product = foldr (*) 1
length  = foldr (\_ n -> 1 + n) 0
```

### What `foldr` does, drawn

`foldr` **replaces the list's own constructors**. A list is `1 : (2 : (3 : []))`, and `foldr f z`
rewrites every `:` as `f` and the `[]` as `z`:

```
       1 : (2 : (3 : []))          the list
   f   1 ( f 2 ( f 3   z ))        foldr f z
```

So `foldr (+) 0 [1,2,3]` is `1 + (2 + (3 + 0))`. **Right-associated, and the brackets pile up on the
right** — which is the reason for everything in §3.

`foldl` piles them on the left instead:

```haskell
foldl :: (b -> a -> b) -> b -> [a] -> b
foldl f z []     = z
foldl f z (x:xs) = foldl (f z x) xs      -- (nearly: see §4)
```

```
   ((( z `f` 1) `f` 2) `f` 3)
```

**`foldl (+) 0 [1,2,3]` is `((0 + 1) + 2) + 3`.** For `(+)` the answer is the same, because addition is
associative. **For `(-)` it is not:** `foldr (-) 0 [1,2,3]` is `1 - (2 - (3 - 0)) = 2` and
`foldl (-) 0 [1,2,3]` is `((0-1)-2)-3 = -6`. Check both at a prompt before you go on.

---

## 2. The Universal Property, and Why the Laws Are Worth Knowing

`foldr` is not merely *a* way to write these functions. It is *the* way: **any function defined by
those two equations is a `foldr`**, and that is a theorem, not a style guide.

```
g []     = z
g (x:xs) = f x (g xs)        ⟺        g = foldr f z
```

This is the **universal property of `foldr`**, and Hutton §16 proves it. What it is *for* is the
Backus quote at the top of this lecture: it lets you transform a program the way you transform an
equation. Two consequences you will use:

- **`foldr (:) [] = id`.** Replacing every `:` with `:` and `[]` with `[]` changes nothing.
- **`foldr f z . map g = foldr (f . g) z`** — a `map` followed by a fold is one fold, with no
  intermediate list. That is not a micro-optimisation; it is the identity GHC's list fusion applies,
  and it is why Week 0's `sum [1..n]` allocated 53 KB instead of 1,600 MB.

**You are not asked to prove these.** You are asked to know that a fold obeys laws, because that is
what makes the abstraction worth having over four hand-written recursions.

---

## 3. The Measurement: Which Fold Is Wrong, and When

The received advice is that `foldl` overflows the stack on long lists and `foldr` does not, so prefer
`foldr`, or better `foldl'`. **Two of those three claims are false on this machine**, and the way they
are false is the most useful thing in Week 2.

`resources/folds.hs`, summing `[1..n]` four ways. **`ghc -O2`:**

| *n* = 10,000,000 | maximum residency | time |
|---|---:|---:|
| `foldr (+) 0` | **130 MB** | 0.359 s |
| `foldl (+) 0` | **44 KB** | 0.004 s |
| `foldl' (+) 0` | **44 KB** | 0.004 s |
| `sum` | **44 KB** | 0.007 s |

**Nothing overflowed, and `foldl` is one of the good ones.** GHC's strictness analyser noticed that the
accumulator is always eventually needed, and turned `foldl` into `foldl'`. Meanwhile **`foldr` is the
worst of the four by four orders of magnitude.**

Now `ghc -O0`, the same program:

| *n* = 10,000,000 | maximum residency | time |
|---|---:|---:|
| `foldr (+) 0` | **446 MB** | 1.646 s |
| `foldl (+) 0` | **619 MB** | 3.277 s |
| `foldl' (+) 0` | **44 KB** | 0.106 s |
| `sum` | **44 KB** | 0.112 s |

**The ranking of `foldr` and `foldl` reverses between the two optimisation levels.** And still nothing
crashed.

### Why the textbook says "stack overflow" and you did not get one

Because the default changed. GHC's stack lives on the heap and grows until it hits 80% of the heap
limit, which by default is unlimited. Cap it and the classic behaviour returns immediately:

```
$ ./folds0 foldl 10000000 +RTS -K16m
folds0: Stack space overflow: current size 33624 bytes.
$ ./folds0 foldr 10000000 +RTS -K16m
folds0: Stack space overflow: current size 33624 bytes.
```

**Both of them.** Which tells you the received advice was never really about `foldl` versus `foldr` —
**for a strict operator, neither is safe**, and the thing that saves you is strictness, not direction.

> **This is why the course insists on `+RTS -s` rather than on advice.** *Real World Haskell*'s
> discussion of `foldl` and space is thirteen years older than this compiler and describes a *symptom*
> — a crash — that no longer happens by default. The underlying problem is real and still there; it now
> presents as **619 MB of heap** instead of an exception. A student who learned the rule and not the
> measurement would look at a 619 MB program and conclude `foldl` was fine, because it did not crash.

### So which do you use?

**The operator decides, not the fold.** Here is the case the table above cannot show, because it needs
an infinite list. `resources/short.hs` asks *"is any element greater than 5?"* over `[1..]`:

| | `[1..]`, an infinite list |
|---|---|
| `foldr (\x acc -> x > 5 \|\| acc) False` | **`True`**, immediately |
| `any (> 5)` | **`True`**, immediately |
| `foldl (\acc x -> acc \|\| x > 5) False` | **never terminates** |
| `foldl' (\acc x -> acc \|\| x > 5) False` | **never terminates** |

**`foldr` can stop early and `foldl` cannot, ever.** `foldl` must reach the end of the list before it
can apply anything, because the outermost call is the *last* element. `foldr`'s outermost call is the
*first* element, so if `f` ignores its second argument the rest of the list is never examined.

**The rule, and it is the one to memorise:**

| If the combining function is… | use | because |
|---|---|---|
| **strict** in the accumulator (`+`, `*`, `max`) | **`foldl'`** | constant space, and it is right at every `-O` level |
| **lazy** in its second argument (`&&`, `\|\|`, `:`, `++`) | **`foldr`** | it short-circuits, and it works on infinite lists |
| building a list | **`foldr`** | it fuses, and the result streams |

**`foldl` without the prime is never the answer.** At `-O2` it is silently repaired; at `-O0` it is the
worst of the four; with a capped stack it crashes. There is no case where you want it and not
`foldl'`.

---

## 4. `foldl` Is Not Quite What §1 Said

The definition in §1 was a simplification. The real one accumulates *unevaluated*:

```haskell
foldl f z (x:xs) = foldl f (f z x) xs
```

`f z x` is **not computed** — it is a thunk, passed forward. So after ten million steps the accumulator
is a chain of ten million pending additions, and *then* `print` asks for it and the whole chain
collapses at once. **That chain is the 619 MB.**

`foldl'` differs by one character of intent:

```haskell
foldl' f z (x:xs) = let z' = f z x in z' `seq` foldl' f z' xs
```

**`seq` forces its first argument before returning its second.** That is the entire difference, and it
is worth 619 MB.

> **`seq` is Week 3's subject** and this is its first appearance. For now: `seq a b` evaluates `a` far
> enough to know it is not an error or an infinite loop — **to *weak head normal form*, one
> constructor deep** — and then returns `b`. It does not evaluate `a` completely, which is a
> distinction Week 3 L08 spends a section on and which trips up everybody who meets `seq` first and
> `deepseq` second.

---

## 5. `++` Is O(n) in Its Left Argument, and Here Is What That Costs

```haskell
(++) :: [a] -> [a] -> [a]
[]     ++ ys = ys
(x:xs) ++ ys = x : (xs ++ ys)
```

**It walks its left argument and never looks at its right.** So `xs ++ ys` costs `length xs`, and
appending one element to the end of a list you are building costs the length of what you have built so
far.

`resources/append.hs` builds a list of *n* elements, one at a time, the two ways round:

```haskell
leftward  n = foldl' (\acc x -> acc ++ [x]) [] [1..n]   -- append at the end
rightward n = foldr  (\x acc -> x : acc)    [] [1..n]   -- cons at the front
```

| *n* | `leftward` | `rightward` |
|---:|---:|---:|
| 10,000 | 1.17 s | 0.01 s |
| 20,000 | 4.93 s | 0.01 s |
| 40,000 | **22.57 s** | **0.01 s** |

**Quadratic against constant.** The time quadruples as *n* doubles, and at 40,000 elements the wrong
version is **2,257×** slower. Both produce the identical list.

**This is the single most common performance bug in beginner Haskell**, and it does not look like a
bug: `acc ++ [x]` is the obvious way to say "add to the end". The fixes, in order of preference:

1. **Build it backwards with `:` and `reverse` once** at the end. `reverse` is O(n), done once.
2. **Use `foldr` and cons**, which produces the list in order with no reversal.
3. If you genuinely need to append at both ends, use a different structure — `Data.Sequence`, or the
   difference-list trick that PS 2 asks about.

---

## 6. The Four-Line `qsort`, Measured

Hutton §1.4's quicksort is the most-quoted Haskell program in existence, and the Week 0 reading guide
asked you to estimate what it costs. Here is the answer.

```haskell
qsort []     = []
qsort (x:xs) = qsort smaller ++ [x] ++ qsort larger
  where smaller = [ a | a <- xs, a <= x ]
        larger  = [ b | b <- xs, b >  x ]
```

`resources/qsort.hs`, 1,000,000 pseudo-random `Int`s from a seeded LCG, `-O2`:

| | allocated | maximum residency | time |
|---|---:|---:|---:|
| Hutton's `qsort` | 2,236 MB | 55.9 MB | **1.75 s** |
| `Data.List.sort` | 1,562 MB | 47.8 MB | **3.24 s** |

**The four-liner is faster than the library.** That is not the expected answer and it is the measured
one. It allocates 43% more and finishes in 54% of the time, because `Data.List.sort` is a *stable*
bottom-up mergesort and stability is not free.

**Now give it sorted input**, which is what real data usually is:

| *n*, already ascending | `qsort` | `Data.List.sort` |
|---:|---:|---:|
| 10,000 | 0.571 s | — |
| 20,000 | 2.714 s | 0.003 s |
| 40,000 | **19.0 s** | — |
| 1,000,000 | *hours* | **0.194 s** |

**19 seconds for 40,000 elements, and it is getting worse than quadratic** (×4.75 then ×7.0 as *n*
doubles, the extra coming from the collector). `Data.List.sort` does a million already-sorted elements
in **0.194 s**, because a bottom-up mergesort detects runs and an already-sorted list is one run.

**Three conclusions, and the third is the one that matters:**

1. **It is not a bad program.** On random data it beats the library.
2. **It is not quicksort.** Real quicksort is in-place and picks its pivot; this copies and takes the
   head. The name is borrowed.
3. **Its worst case is the input you actually get.** Already-sorted and nearly-sorted data is the
   common case in practice — logs, timestamps, database results, anything you sorted once already —
   and on that input the four-liner is unusable and the library is instant. **Knowing the asymptotics
   is not enough; you have to know which input you have.**

---

## 7. What to Take Away

1. **`foldr` replaces a list's constructors:** every `:` becomes `f` and `[]` becomes `z`.
2. **`foldr` brackets to the right, `foldl` to the left.** For `(-)` on `[1,2,3]` that is **2** against
   **−6**.
3. **The universal property:** any function with those two equations *is* a `foldr`. That is what lets
   you reason about folds algebraically, and it is the identity behind fusion.
4. **Measured at `-O2`: `foldr` 130 MB, `foldl` 44 KB.** At `-O0`: `foldr` 446 MB, `foldl` **619 MB**.
   **The ranking reverses**, nothing crashes, and the textbook's "stack overflow" needs `+RTS -K16m`
   to reproduce — at which point **both** folds overflow.
5. **`foldl'` is 44 KB at every optimisation level.** `foldl` without the prime is never the answer.
6. **The operator decides the fold**, not the fold the operator: strict accumulator → `foldl'`; lazy in
   the second argument → `foldr`, which **short-circuits on an infinite list where `foldl` never
   terminates**.
7. **`seq` forces to weak head normal form** and is the whole difference between the two left folds.
8. **`acc ++ [x]` in a loop is quadratic**: 22.57 s against 0.01 s at 40,000 elements. Cons and
   reverse.
9. **Hutton's `qsort` beats `Data.List.sort` on random input and takes hours on sorted input.** Know
   which input you have.

---

## Exercises

*(Not assessed. PS 2 is the assessed work.)*

1. Evaluate by hand, then check: `foldr (-) 0 [1,2,3]`, `foldl (-) 0 [1,2,3]`,
   `foldr (:) [] [1,2,3]`, `foldl (flip (:)) [] [1,2,3]`. The last one has a name.
2. Write `reverse` as a `foldl` and as a `foldr`. One of them is O(n) and the other O(n²) — work out
   which before you measure, then measure.
3. `foldr (\x acc -> x : acc) [] = id`. Write `map f` as a `foldr`, then `filter p`, then `length`.
4. Run `resources/folds.hs` yourself at both optimisation levels and reproduce the eight numbers.
   Then add `foldr` with `(:)` building a list rather than `(+)` summing, and explain why its residency
   is different from the `(+)` case.
5. `and :: [Bool] -> Bool` is `foldr (&&) True`. Why is that the right fold, and what happens to
   `and (repeat False)` with each of the three folds? **One answers. The other two do not hang** —
   they do something you have seen before, in Week 0. Predict which, then check.

---

*PROG 202 · Week 2 · L06 · © CSE Department*
