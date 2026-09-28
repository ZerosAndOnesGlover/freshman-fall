# PROG 202 · Functional & Logic Programming
## Week 5 · Lecture 1 of 2
### Monads: The Pattern You Have Already Written Three Times

*“Shall I be pure or impure?”* — Philip Wadler, *Monads for Functional Programming* (1992), §1

---

**Sat:** Tuesday of Week 5, 11:00–12:15, TH 205 · **⚠️ Quiz 5 in the first ten minutes** — covers Week 4 · **Reading:** Wadler, *Monads for Functional Programming* (1992), §1–§3 · Hutton §12.2–12.3 · **Next:** L12, the `State` monad

**Coursework:** 📊 **Quiz 5** today · 📝 **PS 5** released Wed this week, due Fri of Week 6 17:00 · 🔬 **Lab 4** Wed this week 13:00–14:50 · 📝 **PS 4** due Fri this week 17:00 · 📘 **Midterm** Thu of Week 6 18:00–19:15

---

## 1. You Have Written This Three Times

**Project 1, TODO 3.** Every step unwraps an `Either` and rewraps it:

```haskell
Bin op l r -> case eval env l of
  Left e   -> Left e
  Right lv -> case eval env r of
    Left e   -> Left e
    Right rv -> binop op lv rv
```

**Project 1, TODO 4.** You could not use `filter`, because the predicate could fail, so you wrote:

```haskell
filterM' _ []       = Right []
filterM' p (x : xs) = case p x of
  Left e     -> Left e
  Right keep -> case filterM' p xs of
    Left e     -> Left e
    Right rest -> Right (if keep then x : rest else rest)
```

**And in Week 1, Lab 1's `timetable`** used `traverse id` over a list of `Either`s because seventeen
`mkSession` calls each might fail.

**Three problems, one shape: *do the next thing only if the previous thing worked, and pass the result
along.*** The `case … of Left e -> Left e` lines are pure plumbing — they carry no information and there
are more of them than there is program.

**A monad is the name for that plumbing**, and this lecture is the claim that naming it deletes it.

---

## 2. `>>=`, and What It Is For

```haskell
(>>=) :: Monad m => m a -> (a -> m b) -> m b
```

**Said "bind".** Read the type as *"given a computation producing an `a`, and a function that takes an `a`
and produces a computation of `b`, give me a computation of `b`."*

For `Maybe` the definition is two lines and it is the two lines you have been writing by hand:

```haskell
instance Monad Maybe where
  Nothing >>= _ = Nothing
  Just x  >>= f = f x
```

For `Either e` it is the same shape:

```haskell
instance Monad (Either e) where
  Left e  >>= _ = Left e
  Right x >>= f = f x
```

**Note `Either e` and not `Either`.** A monad's parameter is a type constructor of **one** argument, so the
error type is fixed and the *success* type is the one that varies — which is why `Either` is a monad in its
right-hand side and why the convention that `Right` means success is load-bearing rather than aesthetic.

Now Project 1's `Bin` case:

```haskell
Bin op l r -> eval env l >>= \lv -> eval env r >>= \rv -> binop op lv rv
```

**Four `case` arms became two `>>=`s**, and no line mentions `Left` at all.

---

## 3. `do` Is `>>=` With Better Punctuation

```haskell
Bin op l r -> do
  lv <- eval env l
  rv <- eval env r
  binop op lv rv
```

**That is the same program.** `do` desugars mechanically:

| `do` block | desugars to |
|---|---|
| `do { x <- m; rest }` | `m >>= \x -> do { rest }` |
| `do { m; rest }` | `m >> do { rest }` |
| `do { let x = e; rest }` | `let x = e in do { rest }` |
| `do { m }` | `m` |

**There is no magic and no special case.** `resources/newmonad.hs` has the same computation written both
ways and they are the same value:

```
ghci> (withDo, withBind)
(Box 3,Box 3)
```

> **This is where Week 0's `<-` finally makes sense.** In Week 0 you were told `name <- getLine` is "the
> only way to get the `String` out of an `IO String`", and that `<-` is not assignment. Now you can say
> what it *is*: **`<-` is the left-hand side of a lambda that `>>=` is about to be given.** `name` cannot
> be reassigned because it is a function's parameter.

**And the same three lines work over a different monad with no change:**

```haskell
lookupBoth env = do
  a <- lookup "a" env
  b <- lookup "b" env
  pure (a + b)
```

`lookup` returns `Maybe`, so this is the `Maybe` monad: `Just 3` when both are present, **`Nothing` when
either is missing**, and nowhere in the code is the missing case mentioned.

---

## 4. The Hierarchy, and the One Thing That Will Bite You

```haskell
class Functor f                     where fmap :: (a -> b) -> f a -> f b
class Functor f     => Applicative f where pure :: a -> f a
                                           (<*>) :: f (a -> b) -> f a -> f b
class Applicative m => Monad m       where (>>=) :: m a -> (a -> m b) -> m b
```

**Three classes, each a superclass of the next.** So **every monad is an applicative and a functor**, and
`fmap`, `<$>`, `pure` and `<*>` are all available on any monad for free.

| You want | Use | Because |
|---|---|---|
| apply a plain function to a wrapped value | `fmap` / `<$>` | Week 4 |
| put a plain value in the wrapper | `pure` | *(`return` is a synonym, kept for history)* |
| chain, where the next step **depends on** the previous result | **`>>=`** or `do` | this lecture |
| combine several **independent** wrapped values | `<*>` | **Week 6** |

**The distinction in the last two rows is the whole of Week 6** and it is worth planting now: `>>=` lets
step two *look at* step one's result; `<*>` does not. If your steps are independent you do not need a
monad, and that will matter.

> **This is the third of the three places this course contradicts *Real World Haskell*.** Its Chapter 14
> defines a monad with `return` and `>>=` alone:
>
> ```haskell
> instance Monad Box where
>   return x = Box x
>   Box x >>= f = f x
> ```
>
> **On GHC 9.4.7 that does not compile:**
>
> ```
> oldmonad.hs:4:10: error:
>     • No instance for (Applicative Box)
>         arising from the superclasses of an instance declaration
> ```
>
> The book predates the 2015 **Applicative–Monad Proposal**, which made `Applicative` a superclass of
> `Monad`. **You must write all three instances, in order** — `Functor`, then `Applicative`, then
> `Monad` — and `return` is no longer needed at all, because it defaults to `pure`. `resources/` has both
> versions; compile each once so that you recognise the error when a 2009 tutorial gives it to you.

---

## 5. The Laws

```
pure x >>= f      ==  f x                       -- left identity
m >>= pure        ==  m                          -- right identity
(m >>= f) >>= g   ==  m >>= (\x -> f x >>= g)    -- associativity
```

**Read them as the claim that `do` blocks may be refactored the way you would refactor straight-line
code.** Left identity says a pointless binding can be removed. Right identity says a pointless `pure` can
be removed. **Associativity says you may extract a block of statements into a helper** and call it, which
is the one you rely on every day without noticing.

**As in Week 4, GHC checks none of them.** And as in Week 4, the reason to care is not purity: it is that
every library function over monads — `mapM`, `sequence`, `when`, `forever`, `foldM` — is written assuming
they hold.

**`Maybe` and `Either e` satisfy all three; check left identity for `Maybe` by hand now, it is two lines.**

---

## 6. What You Get Once It Is Named

This is the pay-off, and it is concrete. Every one of these is in `Control.Monad`, works for **any** monad,
and you have hand-written two of them:

| Function | Type | You wrote it as |
|---|---|---|
| `mapM` / `traverse` | `(a -> m b) -> [a] -> m [b]` | Lab 1's `traverse id` |
| `filterM` | `(a -> m Bool) -> [a] -> m [a]` | **Project 1's `filterM'`** |
| `foldM` | `(b -> a -> m b) -> b -> [a] -> m b` | — |
| `sequence` | `[m a] -> m [a]` | Lab 1's `traverse id`, again |
| `when` / `unless` | `Bool -> m () -> m ()` | — |
| `replicateM` | `Int -> m a -> m [a]` | — |
| `void` | `m a -> m ()` | — |

**So Project 1's `filterM'` is `filterM`, and Lab 1's `traverse id` is `sequence`.** Both were the right
thing to write by hand the first time — you cannot recognise a pattern you have never instantiated, which
is Perlis's epigram from L10 — and both should be an import from now on.

**The Filter case of `eval` becomes one line:**

```haskell
Filter f e -> do
  fv <- eval env f
  vs <- eval env e >>= asList
  VList <$> filterM (\v -> apply fv v >>= asBool) vs
```

---

## 7. What a Monad Is Not

Three corrections, because all three are in circulation and all three cause trouble.

**It is not "programmable semicolons" in any useful sense.** That slogan tells you what `do` looks like and
nothing about why `Maybe`, `Either`, `[]`, `State` and `IO` are the same thing.

**It is not about side effects.** `Maybe` has no effects. `[]` has no effects. **`IO` is the only monad in
this course that does anything to the world**, and it is a monad for the same reason the others are: it has
a sensible `>>=`.

**It is not a container.** `State s` is a function, not a box; `(->) r` is a monad and holds nothing at all.
*If you have been picturing a box with a value in it, `State` next lecture will break the picture, which is
why it is next lecture.*

**What it is:** a type constructor with a lawful `>>=` and `pure`. That is the entire definition, and its
usefulness is that **a surprising number of unrelated-looking plumbing problems have the same shape.**

---

## 8. What to Take Away

1. **You have written the plumbing three times**: Project 1's `Bin`, Project 1's `filterM'`, Lab 1's
   `traverse id`.
2. **`>>=` chains a computation with a function that produces the next computation.** For `Maybe` and
   `Either e` the definition is two lines.
3. **`Either e`, not `Either`** — the error type is fixed, the success type varies.
4. **`do` desugars to `>>=` mechanically**, and `<-` is a lambda's parameter, which is why it is not
   assignment.
5. **`Functor` → `Applicative` → `Monad`**, each a superclass, so `fmap`, `<$>`, `pure` and `<*>` are free
   on any monad.
6. **`return` and `>>=` alone will not compile.** Write all three instances; `return` defaults to `pure`.
7. **Three laws, unchecked**, and they are what let you refactor a `do` block.
8. **`filterM` is your `filterM'` and `sequence` is your `traverse id`.** Import them now.
9. **A monad is not effects, not a container, and not semicolons.** It is a lawful `>>=`.

---

## Exercises

*(Not assessed. PS 5 is the assessed work.)*

1. Desugar this by hand into `>>=` and lambdas, then check by compiling both:
   `do { x <- m; y <- n x; pure (x, y) }`
2. Write `instance Monad Box` for `newtype Box a = Box a`, getting the error first, then fixing it with all
   three instances. **Keep the error message.**
3. Rewrite Project 1's `Bin` case with `do`. Count the lines before and after.
4. Replace your `filterM'` with `filterM` from `Control.Monad` and re-run `make test`. Then do the same for
   `mapM`.
5. `lookup "a" env >>= \a -> lookup "b" env >>= \b -> pure (a + b)`. What does it give when `"b"` is
   missing, and **at what point does the computation stop**? Trace it through `Maybe`'s two-line instance.

---

*PROG 202 · Week 5 · L11 · © CSE Department*
