# PROG 202 · Problem Set 4
## Type Classes, `Functor`, `Foldable`, and Laws

---

**Released:** Week 4, Wednesday · **Due:** Week 5, Friday 17:00
**Total: 100 points** · Submit one PDF, `PS4_{LastName}_{StudentID}.pdf`, plus your `.hs` files in a
tarball `PS4_{LastName}.tar.gz`

> **About three hours.** Five questions, fifteen parts.
>
> **Project 1 was also assigned this Wednesday**, and it is due in Week 7 with the midterm in between.
> This problem set is the shorter of the two things on your desk; do it first and Project 1 Phase 1 will
> be easier.
>
> **State your `ghc --version`.** Q3 is a measurement. **Every `.hs` file compiles clean under
> `ghc -Wall -O2`.**

---

### Q1: Reading Constraints (18 points)

**(a) [7]** For each signature, say **how many arguments the function takes** and **what the constraint
lets the implementation do that it otherwise could not**:

```haskell
elem     :: Eq a => a -> [a] -> Bool
maximum  :: (Foldable t, Ord a) => t a -> a
mconcat  :: Monoid a => [a] -> a
mempty   :: Monoid a => a
show     :: Show a => a -> String
```

**`mempty` is the one to think about.** It has no arguments at all and its class variable appears only in
the result. Say what chooses the instance, and write an expression where GHC cannot tell.

**(b) [5]** `:i Eq` reports `{-# MINIMAL (==) | (/=) #-}`.

- What does that pragma mean, and what in the class declaration makes it true?
- Write `instance Eq Day` defining **only** `/=`, and confirm `==` works.
- What would `{-# MINIMAL (==), (/=) #-}` mean instead? *(Note the comma.)*

**(c) [6]** `class Eq a => Ord a` — the `Eq a =>` here is a **superclass**, not a constraint on a
function.

- What does it let a function with `Ord a =>` do for free?
- Is `(Eq a, Ord a) => a -> Bool` wrong, redundant, or an error? Compile something with it and report.
- **`Num` has no `Ord` superclass.** Name a type in `Num` that cannot sensibly be ordered, and say why
  that is the right design. *(There is one in the standard library.)*

---

### Q2: Writing Instances (22 points)

**(a) [8]** `newtype MaxMinutes = MaxMinutes Int`, where `<>` keeps the larger.

- Write `instance Semigroup MaxMinutes` and check associativity by hand on three values.
- **Is it a `Monoid`?** If so give `mempty` and prove it is an identity; if not, say what is missing and
  what one change to the type would fix it.
- Do the same for `newtype MinMinutes`, and say why the standard library provides `Max`/`Min` over a
  `Bounded` type rather than over `Int` directly.

**(b) [8]** From your Lab 4 `Classes.hs`:

- Report your `Semigroup Stats` and `Monoid Stats`.
- **`mempty = Stats 0 0 0` relies on a fact about durations.** State the fact and name the function in
  `Sched.hs` that guarantees it. What would you write if that guarantee did not exist?
- You broke `mempty` to `Stats 0 0 999` in Lab 4 §4c. **All ten law checks still passed.** Explain why,
  and give the law check that does catch it.

**(c) [6]** There is no `instance Monoid Int`.

- Compile `print (mempty :: Int)` and report the error.
- **Why is there no instance?** Name the two obvious candidates.
- What does the standard library provide instead, and why is `newtype` the right tool? *(Week 1 said
  `newtype` was free. This is what it is free *for*.)*

---

### Q3: What a Dictionary Costs (18 points)

**(a) [8]** `resources/spec.hs` is one function, compiled twice, differing only in a `SPECIALISE`
pragma. Build both and report three runs of each at *n* = 200,000,000:

| | runs |
|---|---|
| as written | |
| with `{-# SPECIALISE #-}` | |

- Give the ratio.
- **Explain what the dictionary version does at every `+`** that the specialised version does not.

**(b) [6]** Now **delete the `NOINLINE`** from `sumPoly` and measure again.

- Report three runs. The number is not a small improvement.
- **Explain what GHC did**, naming three separate transformations it became free to apply.
- **Hence say why the 30% in (a) is not a reason to avoid type classes.**

**(c) [4]** `{-# SPECIALISE #-}` is not free either.

- What does it cost, in the compiled artefact?
- Give the situation in which you would need it — the one where GHC cannot specialise on its own. *(It is
  about module boundaries.)*

---

### Q4: `Functor`, `Foldable`, and the Laws (22 points)

**(a) [8]** `data Tree a = Leaf | Node (Tree a) a (Tree a)`.

- Write `instance Functor Tree` and `instance Foldable Tree` (in order).
- Check `fmap id == id` and `fmap (f . g) == fmap f . fmap g` by hand on a three-node tree, showing the
  trees.
- Now write the **swapping** version, `fmap f (Node l x r) = Node (fmap f r) (f x) (fmap f l)`, compile it
  with `-Wall`, and report: **which laws fail, and does GHC object?**
- **Construct a tree on which the composition law passes for the swapping version.** Say what that tells
  you about checking a law with one example.

**(b) [8]** Predict each, then run it, and report both:

```haskell
length (Just 3)          length ('x', 5)          maximum ("hello", 3)
length Nothing           sum ('x', 5)             length (Right 5)
null (Just undefined)    concat (Just [1,2])      maximum (Left "x" :: Either String Int)
```

- **One throws.** Which, and why?
- **`null (Just undefined)` is `False` and does not throw.** Explain using Week 3's vocabulary.
- `length someTuple` is always 1. **Generalising `length` from `[a] -> Int` to `Foldable t => t a -> Int`
  turned a family of type errors into silently-wrong programs.** Argue for or against the change, in one
  paragraph, and say what you would need to know about a codebase to decide. *(No expected answer.)*

**(c) [6]** `foldMap :: Monoid m => (a -> m) -> t a -> m`.

- Write `instance Foldable Tree` again with `foldMap` instead of `foldr`, and confirm `sum`, `length` and
  `toList` still work.
- `foldMap Sum [1,2,3]` and `foldMap Product [1,2,3]` are both 6. **Pick numbers that distinguish them**
  and report both.
- **`<>` is associative by law.** Name what becomes legal because of that, which no `foldr` can offer, and
  say which week of this course needs it.

---

### Q5: `sq`, Phase 1 (20 points)

This is Project 1's first phase, marked here as a problem set so that you get feedback three weeks before
the deadline. **The same code counts for both** — this is deliberate and is not double submission.

**(a) [8]** Implement TODOs 1–4 of `Eval.hs` and report `make test-phase1`. **All twelve must pass.**

**(b) [6]** `Filter` takes a predicate that can fail, so `Data.List.filter` is no use.

- Give your implementation.
- **Say exactly why `filter` does not fit**, in terms of the two types involved.
- You have written a recursion that threads a possible failure through a list. **Week 5 has a name for
  it.** Guess the name, or describe what a library function doing this would have to look like. *(Keep
  your answer; Week 6 L20 asks for it back, as Lab 1's `traverse id` guess did.)*

**(c) [6]** `Eq` in `sq` refuses to compare two different kinds of value: `day t == LEC` is a type error
and not `false`.

- Report your implementation of `Eq`/`Ne` and the `mixed-equality` test passing.
- **Give the argument for the other choice** — returning `false` for a mixed comparison — and name a
  mainstream language that makes it.
- Which would you put in a language people had to use, and what evidence would change your mind?

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

**Late work:** [[Year2 - Sophomore/COURSE POLICIES|COURSE POLICIES]] applies. **The lowest problem set of
the term is dropped** — and note that **Project 1 is not a problem set** and cannot be the one you drop.

---

*PROG 202 · Week 4 · PS 4 · © CSE Department*
