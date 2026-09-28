# PROG 202 · Functional & Logic Programming
## Week 6 · Lecture 1 of 2
### Applicative Functors, and Errors That Accumulate

*“In this paper, we introduce Applicative functors—an abstract characterisation of an applicative style of effectful programming, weaker than Monads and hence more widespread.”* — Conor McBride & Ross Paterson, "Applicative programming with effects" (2008), abstract

---

**Sat:** Tuesday of Week 6, 11:00–12:15, TH 205 · **⚠️ Quiz 6 in the first ten minutes** — covers Week 5 · **Reading:** Hutton §12.2 · **Next:** L14, monad transformers · **⚠️ MIDTERM Thursday 18:00–19:15, Weeks 0–5**

**Coursework:** 📊 **Quiz 6** today · 📝 **PS 6** released Wed this week, due Fri of Week 7 17:00 · 🔬 **Lab 5** Wed this week 13:00–14:50 · 📘 **Midterm** Thu this week 18:00–19:15 · 📝 **PS 5** due Fri this week 17:00

---

## 1. The Problem `>>=` Cannot Solve

Here is a validator. Three independent checks on a session:

```haskell
mkE :: String -> Int -> Int -> Either [String] Session
mkE c s e = Session <$> nonEmpty c <*> inDay "start" s <*> inDay "end" e
```

Given a course code that is empty, a start of 60 and an end of 1500 — **three things wrong** —
`resources/validate.hs` reports:

```
Either    : 1 error(s): course code is empty
```

**One error.** The other two checks never ran.

**That is not a bug in `Either`; it is what `>>=` means.** `m >>= f` gives `f` the *result* of `m`, so if
`m` failed there is no result, so `f` cannot run. **Short-circuiting is the definition**, and it is exactly
what you want for `eval` — a type error in the left operand means there is nothing to add.

**But these three checks do not depend on each other**, and a user filling in a form deserves all three
messages at once.

---

## 2. `<*>`: Combining Independent Effects

```haskell
class Functor f => Applicative f where
  pure  :: a -> f a
  (<*>) :: f (a -> b) -> f a -> f b
```

**`<*>` is said "ap" or "apply".** Read the type: *a wrapped function, a wrapped argument, a wrapped
result.*

**The crucial difference from `>>=`, and the whole lecture is in it:**

| | type | can the second step see the first's result? |
|---|---|---|
| `<*>` | `f (a -> b) -> f a -> f b` | **No.** Both arguments already exist |
| `>>=` | `m a -> (a -> m b) -> m b` | **Yes.** The second is a *function of* the first's result |

**`<*>`'s second argument is a value, not a function.** So it cannot depend on the first — and *because* it
cannot, the instance is free to run both and combine whatever happens.

The idiom, which you have been reading since Week 4 without a name:

```haskell
Session <$> nonEmpty c <*> inDay "start" s <*> inDay "end" e
--      ^^^ fmap the constructor over the first, then <*> the rest
```

**`f <$> a <*> b <*> c` is "apply the *n*-argument function `f` to *n* wrapped arguments".** It is the
applicative style, and once you see it you will see it everywhere.

`liftA2 f a b` is `f <$> a <*> b` with a name, and `sequenceA` and `traverse` are next.

---

## 3. An Applicative That Accumulates

`Data.Validation` is not installed here, so `resources/validate.hs` writes it — **eleven lines**, and the
interesting one is the first:

```haskell
newtype Validation e a = Validation (Either e a)

instance Semigroup e => Applicative (Validation e) where
  pure = Validation . Right
  Validation (Left e1) <*> Validation (Left e2) = Validation (Left (e1 <> e2))   -- BOTH failed
  Validation (Left e1) <*> _                    = Validation (Left e1)
  _ <*> Validation (Left e2)                    = Validation (Left e2)
  Validation (Right f) <*> Validation (Right a) = Validation (Right (f a))
```

**One line does the work:** when both sides are errors, **combine them with `<>`** — which is why the
instance needs `Semigroup e`, and why Week 4's `Semigroup` was worth a lecture.

Same three checks, same `<$>`/`<*>` syntax, different instance:

```
Either    : 1 error(s): course code is empty
Validation: 3 error(s): course code is empty; start 60 is outside 08:00-18:00; end 1500 is outside 08:00-18:00
```

**Three errors instead of one, and the only change is the `Applicative` instance.**

---

## 4. And `Validation` Must Not Be a Monad

The obvious next question is whether we can give `Validation` a `Monad` instance too and have both. **Try
it** — `resources/vmonad.hs`:

```haskell
instance Semigroup e => Monad (Validation e) where
  Validation (Left e)  >>= _ = Validation (Left e)
  Validation (Right a) >>= f = f a
```

**It compiles, `-Wall` silent.** It is also the *only* instance you could write, because `>>=` must hand the
first step's result to `f`, and a `Left` has no result.

**And it breaks a law.** Every `Monad`'s `<*>` must agree with `ap` — `Control.Monad.ap`, which is `<*>`
defined via `>>=`. Measured:

```
(+) <$> l1 <*> l2     = Validation (Left ["e1","e2"])     -- accumulates
((+) <$> l1) `ap` l2  = Validation (Left ["e1"])           -- short-circuits
law (<*>) == ap holds? False
```

**So `Validation` can be a monad or it can accumulate, and not both.** The library's answer is to provide no
`Monad` instance at all, which is why `Data.Validation` exists as a separate type rather than as a flag on
`Either`.

> **This is the sharpest available statement of why `Applicative` is a separate class.** It is not a
> stepping-stone on the way to `Monad`, and it is not "a monad with less syntax". **There are useful things
> that are applicatives and must not be monads**, and the reason is precisely that they exploit the
> independence `<*>` guarantees and `>>=` destroys.
>
> **"Weaker than Monads and hence more widespread"** — the quote at the top of this lecture — is a claim
> about exactly this: the weaker interface admits more instances.

---

## 5. `traverse`, at Last

You were told in Week 1 that `traverse id` was Week 6, and asked to write down a guess. **Get the guess
out.**

```haskell
class (Functor t, Foldable t) => Traversable t where
  traverse  :: Applicative f => (a -> f b) -> t a -> f (t b)
  sequenceA :: Applicative f => t (f a) -> t' (f a)   -- roughly; see below
```

**With `t = []` and `f = Either String`:**

```haskell
traverse :: (a -> Either String b) -> [a] -> Either String [b]
```

*"Apply a possibly-failing function to every element; give me all the results, or the first failure."*

And `sequenceA` — `sequence`'s applicative sibling — is `traverse id`: **a list of `Either`s becoming an
`Either` of a list.** That is Lab 1's line, and `sequence` is the monadic special case you replaced it with
in Week 5.

**Note the constraint: `Applicative f`, not `Monad f`.** So `traverse` works over `Validation`, and *that*
is the pay-off:

```haskell
traverse validateSession sessions :: Validation [String] [Session]
```

**Every bad session's errors, all at once**, from the same function that gives you the first failure if you
run it over `Either`. **The choice of applicative chooses the error strategy**, and the traversal does not
change.

**This is why `Traversable`'s constraint is `Applicative` and not `Monad`.** A monadic traversal would have
to be sequential; an applicative one need not be, which is also why it can be parallel — Week 7.

---

## 6. The Laws, and the One That Matters

```
pure id <*> v              == v                          -- identity
pure f <*> pure x          == pure (f x)                  -- homomorphism
u <*> pure y               == pure ($ y) <*> u            -- interchange
pure (.) <*> u <*> v <*> w == u <*> (v <*> w)             -- composition
```

**You will not use those four directly.** The one you will use is the relationship law:

```
(<*>) == ap          -- for any type that is both Applicative and Monad
fmap  == liftA       -- and Functor must agree too
```

**That is the law §4 broke**, and it is the one that makes a stack of three instances coherent. When you
write all three instances for your own type — as Week 5 made you do — **`ap` and `<*>` agreeing is the thing
to check**, and it is the first property Week 11's tester is pointed at.

---

## 7. When You Do Not Need a Monad

A practical rule, and it is the transferable half of this lecture.

**If your steps do not depend on each other, say so by using `<*>`**, and you get three things for free:

1. **Error accumulation is available** — you can swap the applicative and change the strategy without
   touching the logic.
2. **The order is not fixed**, so the implementation may reorder or parallelise.
3. **The type documents the independence**, so a reader knows step two cannot have looked at step one.

**If a later step needs an earlier result, you need `>>=` and there is no way round it.** `eval` needs it:
you cannot add two values before you have them.

> **How to tell, mechanically:** write the `do` block. **If no `<-`-bound name is used in a later
> statement's *arguments*, it is applicative** and `f <$> a <*> b` will express it. If one is, it is
> monadic. `-Wall` will not tell you; nothing will; it is a thing you notice.

---

## 8. What to Take Away

1. **`>>=` short-circuits by definition**, because the second step is a *function of* the first's result.
   `Either` reporting one error out of three is not a bug.
2. **`<*>`'s second argument is a value, not a function**, so the steps cannot depend on each other — and
   *because* they cannot, both can run.
3. **`f <$> a <*> b <*> c`** is the applicative style. Learn to read it; it is everywhere.
4. **Measured: the same three checks give 1 error over `Either` and 3 over `Validation`**, differing only in
   the `Applicative` instance — and `Validation`'s needs `Semigroup e`, which is what `<>` combines the
   errors with.
5. **`Validation` must not be a `Monad`.** The instance compiles and breaks `(<*>) == ap` — measured,
   `Left ["e1","e2"]` against `Left ["e1"]`. **Some things are applicatives and must not be monads.**
6. **`traverse`'s constraint is `Applicative`, not `Monad`** — which is why the same traversal gives you
   first-failure over `Either` and all-failures over `Validation`.
7. **`traverse id` is `sequenceA`**, and Lab 1's line was this all along.
8. **If no `<-`-bound name is used in a later statement's arguments, you do not need a monad.**

---

## Exercises

*(Not assessed. PS 6 is the assessed work.)*

1. `:t` these and say what each does: `liftA2`, `sequenceA`, `traverse`, `<*`, `*>`, `<$`. The last three are
   punctuation you will meet in other people's code.
2. Write `Session <$> nonEmpty c <*> inDay "start" s <*> inDay "end" e` as a `do` block over `Either`. Then
   say why it cannot be written as a `do` block over `Validation`.
3. Reproduce §4's law violation. Then write the `Monad` instance for `Validation` that **does** satisfy
   `(<*>) == ap`, and say what it costs.
4. `traverse validateSession sessions` over `Validation [String]`. Run it on a list with two bad sessions and
   report how many errors you get.
5. For each, say whether it is applicative or monadic, using §7's test: *"look up two keys and add them"*;
   *"look up a key, then use the result as the next key"*; *"validate five fields"*; *"read a config file,
   then open the file it names"*.

---

*PROG 202 · Week 6 · L13 · © CSE Department*
