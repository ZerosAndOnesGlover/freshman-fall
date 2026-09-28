# PROG 202 · Lab 4 · Solutions
## Writing a Class, and Four Instances That Must Obey Laws
### INSTRUCTOR ONLY — NOT FOR STUDENTS

---

**Session:** Wednesday of Week 5, 13:00–14:50, BH 215 · **Unmarked**, checked off in the session.

**What the session is really for.** The instances take forty minutes and are not the point. **§4 is the
point**, and it has one result that will change how the room thinks about tests:

**Break `mempty` to `Stats 0 0 999` — plainly not an identity — and all ten law checks still print
`ok`.** They pass because `a` is built with `foldMap`, `foldMap` seeds with `mempty`, and **the broken
`mempty` contaminated the value the law was checked against.** `make check` catches it only because
`Main.hs` happens to print `mempty` on its own line.

**A student who leaves understanding that a test written in terms of the thing it tests cannot see the
thing it tests has had the session.** Everything about Week 11 follows from it.

**Timing.** §0 8 · §1 18 · §2 22 · §3 28 · §4 20 · checkoff 8 = **104 minutes**, with §5 (12 min) as
overflow for anyone who finishes early — the sheet marks it optional and PS 4 Q4(c) covers it with marks.
**Do not cut §4.**

**Reference solution:** `ClassesSol.hs`.

---

## §1 — `Pretty`

```haskell
instance Pretty Day where
  pretty Mon = "Monday"
  pretty Tue = "Tuesday"
  pretty Wed = "Wednesday"
  pretty Thu = "Thursday"
  pretty Fri = "Friday"

instance Pretty Kind where
  pretty LEC = "lecture"
  pretty LAB = "lab"
  pretty REC = "recitation"
  pretty SEM = "seminar"

instance Pretty Minutes where
  pretty = show

instance Pretty Session where
  pretty t = show (course t) ++ " " ++ pretty (kind t) ++ ", "
             ++ pretty (day t) ++ " " ++ pretty (start t) ++ "-" ++ pretty (end t)
```

**Expected first four lines:**

```
  MATH 251 lecture, Monday 08:00-08:50
  MATH 251 lecture, Tuesday 08:00-08:50
  MATH 251 lecture, Thursday 08:00-08:50
  CS 202 lecture, Monday 09:00-09:50
```

**Answers.**

- **`Show a =>` as a superclass** means any function with `Pretty a =>` may also call `show`. Point out
  that this is a *design* choice here and a slightly questionable one — `Pretty` does not need `Show` —
  and that it is in the skeleton so that the superclass mechanism appears somewhere. A student who says
  the superclass is unnecessary is **right**, and should be told so.
- **`prettyList`'s default** means an instance may define neither. Ask what you would override it *for*;
  the good answer is a comma-separated list rather than one per line.
- **Three of four `Kind` constructors** gets `-Wincomplete-patterns`, which is Week 1 L04 §2. Expect at
  least two students to hit it.

**The `pretty` / `show` distinction** is worth thirty seconds: this is the class that should have existed
in Week 1, when `Show Minutes` was written to produce `11:00` and broke `Show`'s convention to do it.

---

## §2 — `Semigroup` and `Monoid`

```haskell
instance Semigroup Stats where
  a <> b = Stats (nSessions a + nSessions b)
                 (nMinutes  a + nMinutes  b)
                 (max (longest a) (longest b))

instance Monoid Stats where
  mempty = Stats 0 0 0
```

**Expected:** `Stats {nSessions = 17, nMinutes = 1070, longest = 110}`, and `mempty` as `Stats 0 0 0`.

**The `mempty` discussion is the teaching, not the answer.**

- Two fields are sums, identity 0.
- The third is a **maximum**, whose identity is the smallest possible value — so `0` is right **only if no
  duration is ever negative.**
- **It is not**, and the guarantee comes from `mkSession` in `Sched.hs`, which rejects `start >= end`.
  **A Week 1 smart constructor is what makes a Week 4 law hold.** Say that sentence; it is the best
  cross-week connection in the course so far.
- If durations could be negative you would need `minBound :: Int` — which works because `Int` is
  `Bounded` — and the standard library's answer is exactly that: `Data.Semigroup.Max` requires `Bounded`
  for its `Monoid` instance. PS 4 Q2(a) is this.

**A function they did not write that now works:** `mconcat`, `foldMap`, `stimes`, `sconcat`. `mconcat (map
statsOf ts)` is checked against `foldMap statsOf ts` in the law list and they agree.

---

## §3 — `Functor` and `Foldable`

```haskell
instance Functor Tree where
  fmap _ Leaf         = Leaf
  fmap f (Node l x r) = Node (fmap f l) (f x) (fmap f r)

instance Foldable Tree where
  foldr _ z Leaf         = z
  foldr f z (Node l x r) = foldr f (f x (foldr f z r)) l
```

### 3a — the swapped version

**Measured: both laws fail.**

```
  FAIL Functor Tree: fmap id == id (one case)
  FAIL Functor Tree: composition (one case)
```

**Identity fails** for the obvious reason. **Composition fails for a better one:** `fmap (f . g)` swaps
**once** and `fmap f . fmap g` swaps **twice**, and two swaps is no swap — so the two sides differ by
exactly one reflection.

**The follow-up is the graded part, and it is narrower than it first looks.** Measured, with the swapped
`fmap`:

| tree | `fmap id == id` | composition |
|---|---|---|
| `Leaf` | **True** | **True** |
| `fromList [1]` | **True** | **True** |
| `fromList [1,2]` | False | False |
| `fromList [2,1,3]` — *shape*-symmetric | False | False |
| `Node (Node Leaf 1 Leaf) 2 (Node Leaf 1 Leaf)` — **value**-symmetric | **True** | **True** |

**Shape symmetry is not enough** — `fromList [2,1,3]` is its own mirror image as a *shape* and still
fails, because swapping exchanges the values 1 and 3. **Only a tree that is its own mirror image
*including its values* hides the bug**, plus the two degenerate cases.

**And here is the part to say out loud:** `fromList` **cannot build** a value-symmetric tree with more
than one node, because `insert` drops duplicates. So a generator built from `fromList` will never produce
the case that hides the bug — which is luck, not design, and **next time the luck runs the other way.**
That is the argument for Week 11 in one paragraph.

### 3b

**`length (fromList [3,1,4,1,5,9,2,6])` is 7, not 8.** `insert` returns the tree unchanged on an equal
element, so **the tree is a set**. The duplicate `1` is dropped.

**This matters in §4** and the skeleton's comment says so: the first version of the `Foldable` law checks
compared `length tree` against `length starts` — seventeen durations in, three distinct out — and
**failed. The instance was right and the check was wrong.**

---

## §4 — The Law Checks

All ten print `ok` for a correct solution. Verify that before the session; a green baseline is the whole
premise.

**(a)** Every check is **one example**, and the names say `(one case)` deliberately. Associativity is a
claim about all triples.

**(b)** The check that was wrong before it was right, above. **The question to press:** *what would have
happened if the check had been the only evidence and the instance had also been wrong?* — the two errors
could have cancelled, and nobody would have looked again.

**(c) — the section that matters.** Change `mempty` to `Stats 0 0 999`.

**Collect predictions first, out loud.** Most of the room will say several checks fail. Then:

```
make laws   ->  ten ok
make check  ->  FAILS
```

**Why the identity check passed**, and put this on the board:

```
a           = Stats {nSessions = 5, nMinutes = 250, longest = 999}
mempty      = Stats {nSessions = 0, nMinutes = 0, longest = 999}
a <> mempty = Stats {nSessions = 5, nMinutes = 250, longest = 999}
a <> mempty == a  ->  True
```

**The first five sessions are all fifty minutes long, so `longest a` should be 50.** It is 999, because
`a = foldMap statsOf (take 5 ts)` and `foldMap` seeds with `mempty`. **The broken value propagated into
the test data.**

**Answers.**

1. The code-review comment. Mark the mechanism, not the tone. Good: *"`longest` is a max, so `mempty`'s
   third field must be the identity of `max` — the smallest possible duration, which is 0 here because
   `mkSession` rejects non-positive ones. 999 is a maximum, not an identity."*
2. **The law check that catches it** must build its `Stats` **without** `mempty`:
   ```haskell
   , ("Monoid Stats: right identity, on a value not built via mempty"
     , let s = statsOf (head ts) in s <> mempty == s)
   ```
   `statsOf` is the only constructor of a `Stats` that does not go through `foldMap`/`mconcat`. **Accept
   anything that uses `statsOf` or a literal `Stats`.** This is the one bullet worth insisting on.
3. **The general class of bug:** one that the test is *blind to* because the test's inputs were produced
   by the code under test. **Week 11's name for the fix is a *generator*** — inputs built independently
   of the implementation. Accept "the test and the code share an assumption".

---

## §5 — `foldMap` *(cut this if you are over time)*

```haskell
instance Foldable Tree where
  foldMap _ Leaf         = mempty
  foldMap f (Node l x r) = foldMap f l <> f x <> foldMap f r
```

1. **`foldMap` is easier** — three terms and an operator, no accumulator to thread — and it is what a
   library writes. `foldr` is easier to *reason* about the order of.
2. **`<>` being associative by law means the combining may happen in any order**, so the two recursive
   calls are independent and may run **in parallel**. That is **Week 7**, and it is the reason `foldMap`
   exists rather than being a derived operation.
3. `foldMap Sum [1,2,3]` and `foldMap Product [1,2,3]` are **both 6** — 1+2+3 = 1×2×3. Any other numbers
   distinguish them: `[1,2,4]` gives 7 and 8. **`Sum` and `Product` are `newtype`s because coherence
   allows exactly one `Monoid Int` instance and there are two equally good candidates** (L09 §5) — and
   `newtype` is free, which is Week 1's claim finally doing real work.

---

## Checkoff

Six items. **Be strict about one:** §4c's second answer — the law check that catches the broken `mempty`.
A student who cannot produce it has watched the demonstration without taking the lesson, and the lesson is
the session.

---

## After the Session

**PS 4 is due the Friday of Week 5** and Q5 **is Project 1 Phase 1**, which is deliberate — the code
counts for both.

**Quiz 5 is the Tuesday of Week 5** and covers this week.

**The midterm is the Thursday of Week 6 and covers Weeks 0–5.** Lab 5 is the Wednesday before it, on the
`State` monad, and that ordering is intentional. Say so now; students who plan around it do better.

**Week 5 is monads**, and the honest preview is: they have already written one. `Either Err Value` in
Project 1, and the hand-rolled `filterM'` they needed for `Filter`, are the shape L11 names.

---

*PROG 202 · Week 4 · Lab 4 Solutions · INSTRUCTOR ONLY · © CSE Department*
