# PROG 202 · Problem Set 4 · Solutions
## Type Classes, `Functor`, `Foldable`, and Laws
### INSTRUCTOR ONLY — NOT FOR STUDENTS

---

**Released:** Week 4 Wednesday · **Due:** Week 5 Friday 17:00 · **100 points** · **15 parts, ~3 hours**

**What this paper is testing.** Q1 is whether `=>` is finally a working idea. Q2 is instance design, and
Q2(b) reuses Lab 4's contaminated-`mempty` result with marks attached. Q3 is the only measurement.
**Q5 is Project 1 Phase 1**, marked here so the cohort gets feedback three weeks before the deadline —
the same code counts for both and that is deliberate.

**Timing:** Q1 25 min, Q2 40 min, Q3 30 min, Q4 45 min, Q5 40 min.

---

## Q1: Reading Constraints (18)

### (a) [7]

| | arguments | what the constraint buys |
|---|---:|---|
| `elem :: Eq a => a -> [a] -> Bool` | **2** | compare elements with `==` — and **nothing else** |
| `maximum :: (Foldable t, Ord a) => t a -> a` | **1** | walk the container, and order its elements |
| `mconcat :: Monoid a => [a] -> a` | **1** | `<>` and `mempty`, so it works on the empty list |
| `show :: Show a => a -> String` | **1** | render a value it otherwise could not look at |
| `mempty :: Monoid a => a` | **0** | — |

[1 each, 2 for `mempty`.]

**`mempty` [2]:** the class variable appears **only in the result**, so nothing about the arguments can
choose the instance — **the caller's expected type does.** An ambiguous example:

```haskell
print mempty        -- error: Ambiguous type variable
print (mempty :: [Int])
```

**This is the sharpest way to see that a class is not an interface** (L09 §5): no OO dispatch can pick a
method with no receiver.

### (b) [5]

- **`{-# MINIMAL (==) | (/=) #-}` means "define at least one of these two".** [2] It is true because the
  class gives a **default for each in terms of the other** — so either one alone completes the instance,
  and defining neither would loop.
- ```haskell
  instance Eq Day where
    Mon /= Mon = False
    …
  ```
  and `==` then works via the default. [2] *Accept a shorter version using `fromEnum`.*
- **`{-# MINIMAL (==), (/=) #-}` with a comma would mean "define both".** [1] The comma is conjunction and
  the bar is disjunction.

### (c) [6]

- **A function with `Ord a =>` may use `==`, `/=`, `compare`, `<`, `max` and the rest** — the superclass
  is available automatically. [2]
- **`(Eq a, Ord a) =>` is redundant, not an error.** It compiles, `-Wall` says nothing, and reviewers
  should. [2]
- **A type in `Num` and not in `Ord`: `Complex Double`.** [2] Verified: `(1 :+ 2) + (1 :+ 2)` works and
  `(1 :+ 2) < (3 :+ 4)` gives `No instance for (Ord (Complex Double))`. **It is the right design because
  there is no order on the complex numbers compatible with the arithmetic** — any total order you invent
  breaks `a < b ⟹ a + c < b + c`. Accept `Ratio` with a wrong justification for 1.

---

## Q2: Writing Instances (22)

### (a) [8]

```haskell
newtype MaxMinutes = MaxMinutes Int deriving (Eq, Show)
instance Semigroup MaxMinutes where
  MaxMinutes a <> MaxMinutes b = MaxMinutes (max a b)
```

Associativity: `max` is associative, so it holds for all triples, not just three. [2]

**Is it a `Monoid`? Yes, with `mempty = MaxMinutes minBound`** — and it works only because `Int` is
`Bounded`. [3] **Full marks also for "no, not for an unbounded type"** with `Integer` named, which is the
better answer: the instance exists for `Int` and could not for `Integer`.

**`MinMinutes` is the mirror**, with `maxBound`. [1]

**Why the library's `Max`/`Min` require `Bounded` for `Monoid` [2]:** `Data.Semigroup.Max` has a
`Semigroup` instance for any `Ord a` and a **`Monoid` instance only for `Bounded a`** — because the
identity of `max` *is* `minBound` and there is nothing else it could be. **The class hierarchy is carrying
the distinction between "combinable" and "combinable with an identity"**, which is exactly what splitting
`Semigroup` from `Monoid` is for.

### (b) [8]

The instances are in `ClassesSol.hs`. [3]

**The fact `mempty = Stats 0 0 0` relies on [2]:** `longest` is a **maximum**, so its identity must be the
smallest possible duration. `0` is right **only because no duration is ever ≤ 0**, and the guarantee is
**`mkSession` in `Sched.hs`**, which returns `Left` for `start >= end`. **A Week 1 smart constructor is
what makes a Week 4 law hold.** Without it you would need `minBound :: Int`, and you would have to say so
in a comment because nobody would guess.

**The contaminated `mempty` [3].** All ten checks pass with `mempty = Stats 0 0 999` because
`a = foldMap statsOf (take 5 ts)`, `foldMap` seeds with `mempty`, so `longest a` is 999 rather than 50 and
`a <> mempty == a` holds vacuously. **The check that catches it must not build its `Stats` through
`mempty`:**

```haskell
, ("right identity, on a value not built via mempty"
  , let s = statsOf (head ts) in s <> mempty == s)
```

Verified: `True` with the correct `mempty`, `False` with the broken one. **Accept any version using
`statsOf` or a literal `Stats`.**

### (c) [6]

```
mint.hs:2:15: error:
    • No instance for (Monoid Int) arising from a use of ‘mempty’
```
[2]

**Why none [2]:** **addition with 0 and multiplication with 1** are both monoids on `Int`, equally
canonical, and **coherence permits exactly one instance per type per class** — so the library declines to
choose.

**What it provides instead [2]:** `newtype Sum Int` and `newtype Product Int`, each with its own instance.
**`newtype` is right because it is free** — erased at compile time, so `Sum Int` has the identical
representation to `Int` — which is Week 1's claim finally doing real work rather than being asserted.

---

## Q3: What a Dictionary Costs (18)

### (a) [8]

| | runs |
|---|---|
| as written | **3.18 s, 2.97 s, 2.76 s** |
| with `{-# SPECIALISE #-}` | **2.23 s, 2.26 s, 2.18 s** |

**Ratio about 1.3.** [5, allowing ±15%.]

**What the dictionary version does at every `+` [3]:** loads the `Num` dictionary, indexes the `+` field,
and makes an **indirect call** through it — which is not only the call overhead but blocks inlining, so
the arguments stay **boxed** `Int`s on the heap instead of unboxed `Int#`s in registers. The specialised
version has `+` as one machine instruction.

### (b) [6]

**Delete the `NOINLINE` and it is 0.07 s, 0.07 s, 0.08 s.** [2]

**Roughly 40× faster than the dictionary version**, and the marks are for naming what became free: [3]

1. **Inlining** — `sumPoly`'s body is placed in `main`.
2. **Specialisation** — with the call site visible, `a` is known to be `Int`, so the dictionary
   disappears.
3. **Unboxing and fusion** — the accumulator becomes an `Int#` in a register, and `foldl'` over
   `[1..n]` fuses so the list is never built.

**Hence [1]:** the 30% in (a) is the cost of *preventing* GHC from doing its job. **In real code the
dictionary is usually gone**, and the measurement exists to show what it would have cost, not what it
does cost.

**Deduct for "so type classes are free".** They are not — (c) and the cross-module case are real.

### (c) [4]

- **`SPECIALISE` costs code size:** a second copy of the function per specialised type, in the interface
  file and the binary. [2]
- **When you need it: across a module boundary.** GHC can only specialise when it can see the function's
  body at the concrete call site — so a polymorphic function exported from another module is specialised
  only if its unfolding was exported too, which large functions' are not. **`SPECIALISE` in the defining
  module, or `INLINABLE`, is the fix.** [2]

---

## Q4: `Functor`, `Foldable`, and the Laws (22)

### (a) [8]

Instances as in `ClassesSol.hs`. [3]

Hand-checks on a three-node tree. [1]

**The swapped version: GHC accepts it with `-Wall` silent, and both laws fail.** [2] Identity obviously;
**composition because `fmap (f . g)` swaps once and `fmap f . fmap g` swaps twice, and two swaps is none.**

**The tree on which composition passes [2] — and this is narrower than students expect.** Measured:

| tree | `fmap id == id` | composition |
|---|---|---|
| `Leaf`, or `fromList [1]` | True | True |
| `fromList [1,2]`, `fromList [2,1,3]` | False | False |
| `Node (Node Leaf 1 Leaf) 2 (Node Leaf 1 Leaf)` | **True** | **True** |

**Shape symmetry is not enough** — `fromList [2,1,3]` is shape-symmetric and fails, because swapping
exchanges 1 and 3. Only **value**-symmetry hides it.

**Full marks for anyone who notices that `fromList` cannot build such a tree**, because `insert` drops
duplicates — so a generator built from `fromList` will never produce the hiding case. **That is luck, not
design**, and it is the argument for Week 11.

### (b) [8]

```
length (Just 3)        1      length ('x', 5)        1
length Nothing         0      sum ('x', 5)           5
null (Just undefined)  False  maximum ("hello", 3)   3
length (Right 5)       1      concat (Just [1,2])    [1,2]
maximum (Left "x")     *** Exception: maximum: empty structure
```
[4]

- **`maximum (Left "x")` throws [1]** — `Left` is an *empty* `Foldable` (the functor is `Either a`, so only
  the `Right` component is an element), and `maximum` of nothing is an error. **`length (Left "boom")` is
  0 for the same reason and does not throw**, which is the pair worth contrasting.
- **`null (Just undefined)` is `False` [1]** because `null` asks about **structure** and never forces the
  element — Week 3's WHNF being useful rather than expensive.
- **The paragraph [2].** No expected answer. Mark whether they engage with the actual trade. The strong
  answers name a concrete cost (`length someTuple == 1` compiles silently) *and* a concrete benefit (one
  `sum`, `traverse_`, `foldMap` for `Map`, `Set`, `Seq`, `Maybe`, your own `Tree`), and then say what
  decides it: **how often the codebase has tuples flowing into positions that expect containers.** Give
  full marks for either conclusion; give 1 for an unargued preference.

### (c) [6]

```haskell
instance Foldable Tree where
  foldMap _ Leaf         = mempty
  foldMap f (Node l x r) = foldMap f l <> f x <> foldMap f r
```
[3]

**`[1,2,3]` gives 6 for both because 1+2+3 = 1×2×3.** `[1,2,4]` gives **7 and 8**. [1]

**What associativity makes legal [2]: reordering the combining, hence evaluating the two subtrees in
parallel.** `foldr` cannot offer it — it fixes the order by construction. **That is Week 7**, and it is why
`foldMap` is a class method rather than a derived function.

---

## Q5: `sq`, Phase 1 (20)

### (a) [8]

Twelve cases, `make test-phase1`. [8, pro rata.] The reference is
`PROJECT 1 EvalRef.hs` in this directory. **Do not circulate it** — Project 1 is not due until Week 7.

### (b) [6]

```haskell
filterM' :: (a -> Either Err Bool) -> [a] -> Either Err [a]
filterM' _ []       = Right []
filterM' p (x : xs) = do
  keep <- p x
  rest <- filterM' p xs
  Right (if keep then x : rest else rest)
```
[3]

**Why `filter` does not fit [2]:** `filter` wants `a -> Bool` and the predicate is `a -> Either Err Bool`.
The types do not line up, and no amount of composing fixes it — **the predicate can fail, and `filter` has
nowhere to put a failure.**

**The name [1]:** **`filterM`**, from `Control.Monad`. Accept any description of "a `filter` whose
predicate returns a wrapped `Bool`, threading the wrapper through". **Keep their answer**; Week 6 L20 asks
for it back, as Lab 1's `traverse id` guess did.

*Students who found and imported `filterM` rather than writing it: full marks, and a note that writing it
once is what makes Week 5 easy.*

### (c) [6]

Their `Eq`/`Ne` and the `mixed-equality` case passing. [2]

**The argument for returning `false` [2]:** it is total — no comparison ever fails — so a query never dies
in production because of a comparison, and `x == y` for values of different kinds is *meaningfully* false.
**Python 3 makes this choice for `==`** (and the opposite for `<`, which raises). JavaScript's `==` is the
cautionary version.

**Which would you ship [2]:** no expected answer. Mark whether they name evidence. The good ones say
something like *"refuse, because `day t == LEC` is a mistake a user will make and silently getting `false`
gives them an empty result with no explanation"* — and then name the evidence that would change their
mind: **how often real queries legitimately compare across kinds** (rarely) versus **how often a query
crashing in production is worse than a wrong empty answer** (often, for a reporting tool).

---

## Marks

| Q | Topic | Parts | Points |
|---|---|---:|---:|
| 1 | Reading constraints | 3 | 18 |
| 2 | Writing instances | 3 | 22 |
| 3 | What a dictionary costs | 3 | 18 |
| 4 | `Functor`, `Foldable`, laws | 3 | 22 |
| 5 | `sq`, Phase 1 | 3 | 20 |
| | **Total** | **15** | **100** |

---

## What to Watch For Across the Cohort

1. **Q1(a) giving `mempty` one argument.** They are still reading `=>` as a parameter, four weeks in and
   one week before the midterm. Fix it individually, not in the tutorial.
2. **Q3(b) concluding "type classes are free".** They have over-corrected from (a). The honest position —
   usually free, and here is when not — is the examinable one.
3. **Q5(a) below 12/12.** Project 1 is due Week 7 with the midterm in between; a student stuck on Phase 1
   in Week 5 needs to be told now that Phase 3 is the long one.
4. **Q2(b) not naming `mkSession`.** The cross-week connection is the best thing on this paper and about
   half the cohort will miss it. Worth a line in the tutorial: **the laws you can satisfy depend on the
   invariants you established three weeks earlier.**

---

*PROG 202 · Week 4 · PS 4 Solutions · INSTRUCTOR ONLY · © CSE Department*
