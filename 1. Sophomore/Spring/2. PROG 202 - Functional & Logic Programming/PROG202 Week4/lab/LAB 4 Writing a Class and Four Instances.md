# PROG 202 · Lab 4
## Writing a Class, and Four Instances That Must Obey Laws
### Week 4 · sat **Wednesday of Week 5**, 13:00–14:50, BH 215 · **unmarked, checked off in the session**

---

> **This lab covers Week 4** and is sat on the **Wednesday of Week 5**. **Lab *N* is sat on the
> Wednesday of Week *N+1*.**
>
> **Nothing here is marked.** The TA checks your work off in the session.
> [[Year2 - Sophomore/COURSE POLICIES|COURSE POLICIES]] costs you a letter grade after a second
> unexcused absence.

**What you are doing:** declaring a class of your own, writing four instances, and then discovering that
`make check` and `make laws` catch different things — because an instance can produce exactly the right
output and still be wrong.

**Four TODOs, ten law checks, and every law check must print `ok`.**

---

## 0. Setup (8 minutes)

```bash
mkdir -p "$PROG202/week4/practice"
cd "$PROG202/week4/practice"
cp "$ACADEMICS/1. Sophomore/Spring/2. PROG 202 - Functional & Logic Programming/PROG202 Week4/lab/"{Sched.hs,Classes.hs,Main.hs,Makefile,expected.txt} .
make
```

It builds. It fails at run time on the first `error "TODO 1"`, which is expected.

**`Classes.hs` is the only file you edit.** `Main.hs` and `expected.txt` are the target.

**Read the law comments above each TODO before writing the instance.** Two of the four are easy to write
in a way that compiles, produces plausible output, and breaks a law — and `make check` will not notice.

---

## 1. A Class of Your Own (18 minutes) — TODO 1

```haskell
class Show a => Pretty a where
  pretty     :: a -> String
  prettyList :: [a] -> String
  prettyList = unlines . map pretty
```

**Three things in that declaration to be able to explain at the checkoff:**

- **`Show a =>` is a superclass.** You cannot be `Pretty` without being `Show`. Say what that buys a
  function with `Pretty a =>` in its signature.
- **`prettyList` has a default**, so an instance may define neither, either, or both.
- **`pretty` is for people; `show` is for programmers.** Week 1's Lab §2 made the same distinction and
  broke `Show`'s convention deliberately; this is the class that should have existed instead.

Write four instances: `Day` → `"Monday"`, `Kind` → `"lecture"`, `Minutes` → `"11:00"`, and

```
PROG 202 lecture, Tuesday 11:00-12:15
```

for a `Session`.

**`Kind` has four constructors.** Write all four — and if you write three, note which tool told you, and
that it is the tool from Week 1 L04 §2.

```bash
make check
```

The first three sections should now match.

---

## 2. A `Semigroup` and a `Monoid` (22 minutes) — TODO 2

```haskell
data Stats = Stats { nSessions :: !Int, nMinutes :: !Int, longest :: !Int }
```

**The `!`s are from Week 3 and they are not decoration.** `foldMap statsOf ts` folds this over every
session, and without them you have Lab 3 §3 again.

Write `<>` — combine two summaries of disjoint groups — and then `mempty`.

> **`mempty` is where the thinking is.** Two of the three fields are sums, so their identity is 0. The
> third is a **maximum**, and the identity of `max` is the *smallest possible value*. So:
>
> - Is `0` right? Only if no duration can be negative.
> - **Is that true?** Check `mkSession` in `Sched.hs` before you answer. *(It is — and that is Week 1's
>   smart constructor paying for a Week 4 law, four weeks later, which is worth noticing.)*
> - What would you write if durations could be negative, and what does that cost you?

```bash
make check      # the stats section should now match
make laws       # the first four should be ok
```

**Answer:** you now have `mconcat`, `foldMap`, `stimes` and the rest for free. **Name one function you
did not write that now works on `Stats`**, and check it.

---

## 3. `Functor` and `Foldable` for a Tree (28 minutes) — TODOs 3 and 4

```haskell
data Tree a = Leaf | Node (Tree a) a (Tree a)
```

An ordered binary tree, with `insert` and `fromList` given.

### 3a. `Functor Tree` (TODO 3)

Two equations. **There is exactly one law-abiding implementation and several that compile.**

**Write the wrong one first, on purpose:**

```haskell
fmap f (Node l x r) = Node (fmap f r) (f x) (fmap f l)     -- subtrees swapped
```

```bash
make laws
```

**Both `Functor` laws fail.** Work out why each does — they fail for different reasons, and the
composition one is the interesting case: `fmap (f . g)` swaps **once** and `fmap f . fmap g` swaps
**twice**, which is the same as not swapping at all.

Then write the right one.

**Answer:** **find a tree on which the swapped version passes both laws.** There are two kinds and you
should find both — one is trivial and one is not, and the interesting fact is that **`fromList` cannot
build the second kind.** Say why, and say what that tells you about a test whose inputs come from the same
module as the code.

### 3b. `Foldable Tree` (TODO 4)

**One method is enough.** Write `foldr`, in order — left subtree, then the node, then the right.

The moment it compiles you get `sum`, `length`, `maximum`, `minimum`, `elem`, `null`, `toList`, `any`,
`all` and about a dozen more. **Check that you do**, in GHCi:

```
ghci> :l Classes.hs Sched.hs
ghci> let t = fromList [3,1,4,1,5,9,2,6 :: Int]
ghci> (sum t, length t, maximum t, 4 `elem` t, toList t)
```

**Answer:** `fromList [3,1,4,1,5,9,2,6]` has **eight** inputs. What does `length t` say, and why?
*(Look at `insert`. This matters in §4.)*

---

## 4. The Law Checks, and What They Cannot Do (20 minutes)

```bash
make laws
```

Ten checks. **All ten must print `ok`.**

Now read `lawChecks` in `Classes.hs` — the code, not the output. **Three things about it are the point of
this lab:**

**(a) Every check is one example.** `("Semigroup Stats: associative (one case)", (a <> b) <> c == a <> (b
<> c))` tests associativity on **one** triple of values. Associativity is a claim about *all* triples.
**A passing check is not a proof and the name says so.**

**(b) One of the checks was wrong before it was right, and the comment in the file says which.** The
first version compared `length tree` against `length starts` — seventeen sessions in, and it failed,
because `insert` ignores duplicates so **the tree is a set**: seventeen durations become three distinct
values. **The instance was correct and the check was wrong.**

**Write down what would have happened if the check had been the only evidence**, and the instance had
*also* been wrong.

**(c) Deliberately break one law and watch which checks notice.** Change `mempty` to `Stats 0 0 999`
— which is plainly not an identity for `max`.

**Predict first: how many of the ten checks fail, and does `make check` fail?** Write both predictions
down. Then:

```bash
make laws
make check
```

**Ten `ok`s, and `make check` fails.**

**That is the wrong way round and it is the most important result in the lab.** Work out why the identity
check passed. Print the values if you need to:

```haskell
let a = foldMap statsOf (take 5 ts)
(a, mempty :: Stats, a <> mempty, a <> mempty == a)
```

```
a           = Stats {nSessions = 5, nMinutes = 250, longest = 999}
mempty      = Stats {nSessions = 0, nMinutes = 0, longest = 999}
a <> mempty = Stats {nSessions = 5, nMinutes = 250, longest = 999}
True
```

**The five sessions are all 50 minutes long, so `longest a` should be 50.** It is 999 — because `a` was
built with `foldMap`, `foldMap` seeds with `mempty`, and **the broken `mempty` contaminated the very
value the law was checked against.** The test could not see the break because the test data was produced
by the thing under test.

**And `make check` caught it only by accident**, because `Main.hs` happens to print `mempty` on its own
line.

**Answer, and this is the checkoff item:**

1. Write the one-line code-review comment you would leave on `mempty = Stats 0 0 999`.
2. **Write a law check that would have caught it.** *(It has to build its `Stats` values without going
   through `mempty`. There is exactly one way.)*
3. In one sentence: what general class of bug does a test written in terms of the thing it is testing
   fail to find? **Week 11 has a name for the answer.**

Put it back.

---

## 5. `foldMap`, and Why It Is the Other Method (12 minutes — *do this only if §1–§4 are done*)

`Foldable` can be defined by `foldMap` instead of `foldr`:

```haskell
foldMap :: Monoid m => (a -> m) -> t a -> m
```

**Write `instance Foldable Tree` again, with `foldMap` this time** (comment out your `foldr`), and check
that `sum`, `length` and `toList` still work.

**Answer:**

1. Which of the two was easier to write, and which would you put in a library?
2. `foldMap` needs `<>` to be **associative by law**. Say what becomes legal because of that, and which
   week needs it. *(L10 §3's last paragraph.)*
3. `foldMap Sum [1,2,3]` is 6 and `foldMap Product [1,2,3]` is also 6. **Pick better numbers**, and then
   say why `Sum` and `Product` are `newtype`s rather than two `Monoid Int` instances.

---

## 6. Checkoff

Show the TA:

- [ ] `make check` passing, with all four TODOs done (§1–§3)
- [ ] `make laws` printing **ten `ok`s** (§4)
- [ ] The **swapped** `Functor Tree`, both laws failing, and your symmetric tree that hides the
      composition failure (§3a)
- [ ] `mempty = Stats 0 0 999` — **ten `ok`s and a failing `make check`** — and your law check
      from §4c question 2 that does catch it
- [ ] Your answer to §3b — what `length (fromList [3,1,4,1,5,9,2,6])` is and why
- [ ] *(if you reached §5)* Your `foldMap` version working, and your answer to §5 question 2

---

## What Comes Next

**Project 1 was assigned this Wednesday** — an interpreter, due **Friday of Week 7**. `Expr` and `eval`
from Week 1 L04 §4 are its first commit, and today's `Pretty` class is its printer. **Start it this
weekend**; Week 6 has the midterm in it.

**Week 5 is monads**, and it is the week `Maybe`, `IO` and `State` turn out to be one idea. It also
finishes Project 1's evaluator: the environment you will need is a `State`, and the errors are an
`Either`.

**Lab 5 is on the Wednesday of Week 6** — the day after the midterm's coverage ends and the day before
the paper. That is deliberate.

---

*PROG 202 · Week 4 · Lab 4 · © CSE Department*
