# PROG 202 · Functional & Logic Programming
## Week 5 · Lecture 2 of 2
### The `State` Monad, `IO`, and the Leak That Has Two Names

*“Monads provide a convenient framework for simulating effects found in other languages, such as global state, exception handling, output, or non-determinism.”* — Philip Wadler, *Monads for Functional Programming* (1992), abstract

---

**Sat:** Thursday of Week 5, 11:00–12:15, TH 205 · **Reading:** Wadler §4–§5 · Hutton §12.3 · **Next:** Week 6 L13, applicatives and monad transformers · **⚠️ Midterm Thursday of Week 6, covers Weeks 0–5**

**Coursework:** 📝 **PS 4** due Fri this week 17:00 · 🔬 **Lab 5** Wed of Week 6 13:00–14:50

---

## 1. A Monad That Is a Function

Every monad so far has looked like a container. `State` does not, and that is why it is here.

```haskell
newtype State s a = State { runState :: s -> (a, s) }
```

**A `State s a` is a function** from a starting state to a pair of *a result* and *a new state*. It holds
nothing; it *is* the transformation.

The instances are the whole idea, and they are worth writing out once:

```haskell
instance Functor (State s) where
  fmap f (State g) = State $ \s -> let (a, s') = g s in (f a, s')

instance Applicative (State s) where
  pure a = State $ \s -> (a, s)
  ...

instance Monad (State s) where
  State g >>= f = State $ \s ->
    let (a, s') = g s          -- run the first, getting a result and a new state
        State h = f a          -- feed the result to f, getting the next computation
    in  h s'                   -- run that, from the new state
```

**Read the `>>=` slowly, because it is the only interesting line in the lecture.** It threads `s` from one
computation into the next, and *that threading is the thing you would otherwise write by hand in every
function.*

`State s` is a monad, so `do` works, so:

```haskell
label :: Tree a -> State Int (Tree (Int, a))
label Leaf = pure Leaf
label (Node l x r) = do
  l' <- label l
  n  <- next          -- get the counter and increment it
  r' <- label r
  pure (Node l' (n, x) r')

next :: State Int Int
next = do { n <- get; put (n + 1); pure n }
```

**No counter is passed anywhere and no counter is mutated.** Compare the version you would write without
it: every function takes and returns the counter, and every call site unpacks the pair.

The interface, all of it:

| | type | does |
|---|---|---|
| `get` | `State s s` | the current state as the result |
| `put` | `s -> State s ()` | replace the state |
| `modify` | `(s -> s) -> State s ()` | `get`, apply, `put`. **Lazily — see §4** |
| `modify'` | `(s -> s) -> State s ()` | the same, forcing the new state |
| `gets` | `(s -> a) -> State s a` | `get` then a projection |
| `evalState` | `State s a -> s -> a` | run it, keep the result |
| `execState` | `State s a -> s -> s` | run it, keep the **state** |
| `runState` | `State s a -> s -> (a, s)` | run it, keep both |

---

## 2. Why This Is Not Mutation

`State` looks like mutable state and is not, and the difference is checkable.

**`s` is never modified.** Every `>>=` produces a *new* `s` and passes it forward, exactly as Week 2's
`foldl` passed its accumulator. **`State` is a fold with the accumulator hidden**, which is the single most
useful sentence to hold on to about it.

**Three things follow, and all three are why it is worth having:**

1. **You can run the same computation twice from the same start and get the same answer.** `runState c 0`
   is referentially transparent. Real mutable state has no such property.
2. **You can run it from *any* start.** `execState (label t) 100` labels from 100, with no change to
   `label`.
3. **You can keep the intermediate states**, because they are values. There is no equivalent of "the
   variable's earlier value" in an imperative program.

**And the thing you lose:** nothing about `State` is concurrent-safe or fast in the way a mutable cell is.
`IORef`, `MVar` and `STM` are Week 7, and they are for when you genuinely have one cell that several
threads touch.

---

## 3. `IO` Is the Same Shape, With One Difference

The intuition — and it is an intuition, not the implementation — is

```haskell
newtype IO a = IO (RealWorld -> (a, RealWorld))
```

**`IO` is `State RealWorld`.** That is why `>>=` sequences it: each action receives the world the previous
one produced, so the *order* is forced by data dependency rather than by a rule about statements.

**The one difference is the one that matters:** you cannot write `runState` for `IO`. There is no
`runIO :: IO a -> a`, because there is no value of type `RealWorld` for you to supply. **The only way an
`IO` action runs is by being `main`, or by being reachable from it.**

**So `IO`'s privilege is not that it is magic — it is that its `runState` is missing.** Everything else
about it you now know: `do`, `>>=`, `pure`, `fmap`, `mapM_`, `when`. They are the same functions you used
on `Maybe`.

> **`unsafePerformIO :: IO a -> a` is the missing function, provided anyway.** It exists so that library
> authors can implement things like `Data.ByteString`'s internals, where an effect is genuinely invisible
> from outside. **Using it discards every guarantee in this course** — L01 §2's referential transparency,
> L07 §4's strictness reasoning, Week 7's thread safety. Week 0 §6 said "not for you yet"; it is still not.

---

## 4. The Measurement: `State` Has Two Strictness Decisions and You Need Both

Counting to three million in `State`, four ways. `resources/state.hs`:

```haskell
lazyModify    n = Lazy.execState   (mapM_ (\_ -> Lazy.modify   (+1)) [1..n]) 0
lazyModify'   n = Lazy.execState   (mapM_ (\_ -> Lazy.modify'  (+1)) [1..n]) 0
strictModify  n = Strict.execState (mapM_ (\_ -> Strict.modify (+1)) [1..n]) 0
strictModify' n = Strict.execState (mapM_ (\_ -> Strict.modify'(+1)) [1..n]) 0
```

**`ghc -O0`, *n* = 3,000,000:**

| | maximum residency | time |
|---|---:|---:|
| `Control.Monad.State.Lazy` + `modify` | 308 MB | 2.98 s |
| `Control.Monad.State.Lazy` + `modify'` | **398 MB** | 3.73 s |
| `Control.Monad.State.Strict` + `modify` | 167 MB | 1.70 s |
| **`Control.Monad.State.Strict` + `modify'`** | **44 KB** | **0.50 s** |

**At `-O2` all four are 44 KB**, which by now you should distrust rather than be reassured by.

**The row to stare at is the second one: `modify'` made it worse.** 308 MB became 398 MB by adding
strictness. That is not a paradox once you know what each word means:

| | what is strict |
|---|---|
| `State.Strict` vs `State.Lazy` | whether **the `(a, s)` pair** produced by each `>>=` is forced |
| `modify` vs `modify'` | whether **the new state value** is forced |

**They are orthogonal, and neither alone is enough.** `Lazy` + `modify'` forces each state value *and*
builds a chain of unevaluated pairs — so it does all the work of forcing and keeps all the structure,
which is why it is the worst of the four.

> **This is Week 3 one level up, and it is the same trap in a third costume.** Week 3: `foldl'` is strict
> in the accumulator's *constructor*, not its fields — 727 MB. Week 3: `Data.Map.Strict` is strict in its
> *values*, and `Data.Map.Lazy` is not — 107 MB. Now: `State.Strict` is strict in the *pair*, and
> `modify'` in the *value*, and you need both — 398 MB if you pick one.
>
> **The general rule, and it is the most transferable thing in Weeks 3–5: when a name says "strict", ask
> *strict in what*.** There is always more than one answer, and the module that says `Strict` in its name
> has picked one of them for you.

**The rule for this course:** `import Control.Monad.State.Strict`, and `modify'`. Always. Lab 5 measures
what the other three cost.

---

## 5. `State` in Project 1

Project 1's `eval` threads an environment:

```haskell
eval :: Env -> Expr -> Either Err Value
```

**The `Env` goes in and never comes out**, which is the clue that it is a *reader*, not a *state* — and
`Reader` is Week 6. But if the interpreter had a mutable feature — a counter of evaluation steps, a cache,
a list of warnings — the environment would have to come back out, and the type would become

```haskell
eval :: Expr -> StateT Env (Either Err) Value
```

**which is Week 6's monad transformers**, and it is the reason Week 6 exists rather than the course ending
here.

**Lab 5 builds the version you can build today:** the same interpreter with a step counter, in
`State`, over a language small enough to fit in a session. **It is the last thing the midterm covers.**

---

## 6. What to Take Away

1. **`State s a` is a function `s -> (a, s)`**, not a container. It holds nothing.
2. **`>>=` threads the state**, and that threading is the boilerplate it deletes.
3. **`State` is a fold with the accumulator hidden.** Hold on to that sentence.
4. **It is not mutation:** the same computation run twice from the same start gives the same answer, it can
   be run from any start, and the intermediate states are values.
5. **`IO` is `State RealWorld` with `runState` missing**, and that missing function is the whole of its
   privilege. `unsafePerformIO` is it, provided anyway, and it discards everything.
6. **`State` has two independent strictness decisions.** Measured at `-O0`: `Lazy`+`modify` 308 MB,
   **`Lazy`+`modify'` 398 MB — worse**, `Strict`+`modify` 167 MB, **`Strict`+`modify'` 44 KB.**
7. **When a name says "strict", ask *strict in what*.** Three weeks, three instances of the same question.
8. **Use `Control.Monad.State.Strict` and `modify'`.**

---

## Exercises

*(Not assessed. PS 5 is the assessed work.)*

1. Write `State` yourself — the `newtype`, and all three instances — without looking at the library. Then
   write `get`, `put` and `modify` in terms of it. **This is on the midterm.**
2. `label` from §1, but numbering right-to-left. Change one thing.
3. `evalState (pure 1) undefined` succeeds. `execState (pure 1) undefined` does not. Predict, check,
   explain.
4. Reproduce §4's four numbers at `-O0` and at `-O2`. Then explain the second row to somebody who has read
   only Week 3.
5. Write `runState` for `IO`. Say exactly where you get stuck, and what you would need.

---

*PROG 202 · Week 5 · L12 · © CSE Department*
