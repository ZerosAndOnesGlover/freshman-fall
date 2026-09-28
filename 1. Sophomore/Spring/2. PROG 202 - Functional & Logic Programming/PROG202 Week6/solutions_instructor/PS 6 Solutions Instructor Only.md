# PROG 202 · Problem Set 6 · Solutions
## Applicatives, Monad Transformers, and Functional Error Handling
### INSTRUCTOR ONLY — NOT FOR STUDENTS

---

**Released:** Week 6 Wednesday · **Due:** Week 7 Friday 17:00 · **100 points** · **15 parts, ~3 hours**

**Due the same day as Project 1**, which is 15% against this paper's ~3%. **Expect this to be the weakest
submission set of the term** and mark it accordingly: the paper says to do Project 1 first, and a student who
took that advice and handed in a thin PS 6 has followed instructions. Q5 is Project 1's report question (c),
so that part should be strong even where the rest is not.

**Timing:** Q1 30 min, Q2 45 min, Q3 30 min, Q4 30 min, Q5 30 min.

**Reference files here:** `StackSol.hs`, `StackWrongOrder.hs`, and Week 6 `resources/` for all three
measurements.

---

## Q1: `<*>` Against `>>=` (20)

### (a) [7]

| | | `<$>`/`<*>` form |
|---|---|---|
| 1. two lookups, add them | **applicative** | `(+) <$> lookup k1 m <*> lookup k2 m` |
| 2. lookup, then use the value as the next key | **monadic** | none — the second needs the first's result |
| 3. five independent fields | **applicative** | `Form <$> f1 <*> f2 <*> f3 <*> f4 <*> f5` |
| 4. read a config, then open the file it names | **monadic** | none |
| 5. two independent `IO` actions, paired | **applicative** | `(,) <$> a <*> b` |

[1 each, 2 for correct forms.]

*The test is mechanical and the paper states it: **is any `<-`-bound name used in a later statement's
arguments?** Students who reason from "does it do I/O" get 2 and 5 wrong.*

### (b) [6]

```haskell
(<*>) :: f (a -> b) -> f a -> f b
(>>=) :: m a -> (a -> m b) -> m b
```

**`>>=`'s second argument is a function of the first's result. `<*>`'s is a value.** [2]

**Hence `Either` reports one error of three [2]:** `>>=` must hand `f` the result of the first step, and a
`Left` has no result, so `f` never runs. **Short-circuiting is the definition of `>>=`**, not a defect — and it
is exactly what `eval` needs.

**Why an applicative can run both [2]:** because the second argument **already exists** — it cannot depend on
the first, so the instance is free to evaluate both and combine whatever comes back. **The independence is what
the weaker type buys.**

### (c) [7]

```
liftA2    :: Applicative f => (a -> b -> c) -> f a -> f b -> f c
sequenceA :: (Traversable t, Applicative f) => t (f a) -> f (t a)
traverse  :: (Traversable t, Applicative f) => (a -> f b) -> t a -> f (t b)
(<*)      :: Applicative f => f a -> f b -> f a     -- run both, keep the LEFT result
(*>)      :: Applicative f => f a -> f b -> f b     -- run both, keep the RIGHT
(<$)      :: Functor f => a -> f b -> f a           -- replace the contents
```
[5]

**Two consequences of `Applicative` rather than `Monad` [2]:**

- **Error reporting:** the same traversal gives first-failure over `Either` and **all failures over
  `Validation`** — the choice of applicative chooses the strategy.
- **Evaluation order:** an applicative traversal is not obliged to be sequential, so it **may be
  parallelised**. A monadic one cannot be, because each step may depend on the last. *(Week 7.)*

---

## Q2: An Applicative That Is Not a Monad (22)

### (a) [8]

The newtype, `Functor` and `Applicative` as in `resources/validate.hs`. [4]

```
Either    : 1 error(s): course code is empty
Validation: 3 error(s): course code is empty; start 60 is outside 08:00-18:00; end 1500 is outside 08:00-18:00
```
and both report `ok Session "PROG 202" 660 735` for a good one. [2]

**Why `Semigroup e` [2]:** the both-failed case **combines the two errors with `<>`**, and `<>` is
`Semigroup`'s method. Without it there is no way to have both errors in one value, so the instance would have
to discard one — which is `Either` again.

### (b) [8]

**It compiles, `-Wall` silent.** [2]

```
(+) <$> l1 <*> l2     = Validation (Left ["e1","e2"])
((+) <$> l1) `ap` l2  = Validation (Left ["e1"])
law (<*>) == ap holds? False
```
[2]

**The law [2]: for any type that is both `Applicative` and `Monad`, `(<*>)` must equal `ap`** — `ap` being
`<*>` written with `>>=`. Equivalently `fmap == liftA` and `pure == return`. **So the library provides no
`Monad` instance for validation**: a type can accumulate or it can be a monad, not both.

**The lawful `Monad` instance [2]:** the same one — it *is* lawful **if you also replace `<*>` with the
short-circuiting version**, i.e. give up accumulation. **The cost is the entire point of the type.** *Accept
"there isn't one that keeps accumulation" as the answer; that is the correct conclusion.*

### (c) [6]

Two bad sessions: `Either` gives **one** error, `Validation` gives **all** of theirs. [3]

**What changed [1]:** only the `Applicative` instance. `traverse` is the same function with the same
definition.

**"the choice of applicative chooses …" [2]** → **the error strategy**. Another example: `Maybe` as the
applicative chooses *"tell me only whether it worked"*; `[]` chooses *"give me every combination"*; an
applicative over `IO` chooses *"do them all and report"*. **Accept any that names a different strategy from
the same traversal.**

---

## Q3: The Order of the Stack (20)

### (a) [8]

```
StateT Int (Either String)  -- state outside:     Left "boom at 3"
ExceptT String (State Int)  -- Either outside:    (Left "boom at 3",3)
```
[3]

```haskell
runStateT  :: StateT s m a  -> s -> m (a, s)
runExceptT :: ExceptT e m a -> m (Either e a)
```

**From the types [3]:** `runStateT` over `Either e` gives `Either e (a, s)` — a `Left` replaces the **whole
pair**, so the state is gone. `runExceptT` over `State s` gives `State s (Either e a)` — the state is
**outside** the failure and survives.

**The rule [1]:** the effect that must survive a failure goes **outside `ExceptT`**.

**What warned them [1]: nothing.** Both compile; `step` is byte-identical. That is the answer, and a student
who invents a warning has not read the question.

### (b) [6]

`WriterT [String]` must go **outside `ExceptT`** for the log to survive. [3] Inside, a failure discards it
exactly as it discards the state.

**Generalised to four layers [3]:** **everything you want to read after a failure goes outside the
`ExceptT`; everything you are content to lose goes inside.** Among themselves the survivors' order does not
matter for *survival* (it matters for what `run…` returns, and for nothing else).

### (c) [6]

**The three [3]:**

| | measurement |
|---|---|
| **Week 3:** `Data.Map.Strict` against `.Lazy` for a counter | **44 KB against 107 MB, both at `-O2`** |
| **Week 5:** `State.Strict`+`modify'` against `Lazy`+`modify'` | **44 KB against 398 MB** at `-O0` |
| **Week 6:** `ExceptT e (State s)` against `StateT s (Either e)` | **`(Left …, 3)` against `Left …`** |

**What would have warned them [1]: nothing, in all three.**

**Which is different in kind [2]: the third.** The first two are **performance** — both versions compute the
same answer, one slowly. The third is **semantics**: the two stacks give *different results*. **That is a
sharper and worse failure**, because no amount of profiling finds it and no test that ignores the trace
notices.

*This is the paper's best question. A student who gets the distinction should be told so.*

---

## Q4: `Stack` (20)

### (a) [8]

13/13 and `loadSession` as in `StackSol.hs`. [4]

**`asks dayStart`, no `Config` argument** [1] — and be strict, per the lab solutions.

**No `lift` [2]:** because `asks`, `modify'` and `throwError` come from **`MonadReader`, `MonadState` and
`MonadError`**, which are implemented at every depth, rather than from a particular layer.

**The connection [1]:** those same classes make the code **layer-agnostic**, so it typechecks against any stack
that provides the three effects — **in either order.** The convenience and the hazard are one mechanism.

### (b) [6]

**The shape: right error, `Trace 0 0`, on all seven failures.** [2]

**From the type [2]:** `runStateT` over `ExceptT Err IO` gives `ExceptT Err IO (a, Trace)`, so the pair is
inside the `Either` and a `Left` replaces it — **there is no `Trace` to return**, which is why `runApp` had to
fabricate one.

**The two lines [2]:**

```haskell
type App a = ReaderT Config (ExceptT Err (StateT Trace IO)) a
runApp cfg act = runStateT (runExceptT (runReaderT act cfg)) (Trace 0 0)
```

### (c) [6]

- **`loadAll` could have been applicative** (the rows are independent); **`validateAll` could not have been
  monadic** (a monad short-circuits, which defeats the purpose). [2]
- **`validateAll` needs the `Config` explicitly** because it is **not in the stack at all** — there is no
  `ReaderT` to `asks` from, because `Validation` is not a monad and cannot be a transformer layer. [2]
- **"Every bad row, but stop after ten" [2]:** start from **`validateAll`**, because you need accumulation
  and the short-circuiting version cannot produce more than one. Add a `take 10` on the error list — or, if
  you must stop *doing work* after ten rather than just reporting ten, you need a fold that can halt, which is
  neither: `foldr` with an early exit, or a monadic fold over a state holding the errors so far. **Full marks
  for noticing that "stop reporting" and "stop working" are different requirements.**

---

## Q5: Where Project 1 Would Go (18)

### (a) [6]

```haskell
eval :: Expr -> ReaderT Env (ExceptT Err (State Trace)) Value
```
[3]

**The order, one sentence each [2]:**

- **`ReaderT Env` outermost** — it never fails and never changes, so nothing below it can be affected by it;
  putting it outside keeps `ask` available everywhere at no cost.
- **`ExceptT Err` in the middle** — failures must propagate out through the reader, and must *not* discard the
  trace below.
- **`State Trace` innermost** — so that it is **outside the failure in the `run` order** and the trace survives
  an error, which is L14 §3's rule.

**`Env` is the `Reader` [1]**, not a `State`, because **it goes in and never comes out**: `Let` extends it for
one recursive call and never returns it. Making it a `State` would permit a modification the language does not
have.

### (b) [6]

Timings before and after with `Data.Map`. [2]

**No measurable difference [2]**, because the environments in all 27 tests are **at most three or four
deep** — a list lookup at that size beats a tree, and the constant factors dominate. **An input that would
change it:** a program with hundreds of nested `let`s, or a top-level environment of hundreds of bindings
looked up in a loop.

**Why immutable is right anyway [2]:** Week 3 measured a persistent insert into a map 1,000× larger at
**1.86×**, not 1,000× — the path to the root is copied and everything else is shared. So the "copy" an
immutable environment implies is `O(log n)` at worst and `O(1)` for a cons, **and it buys closures that
cannot be corrupted by a later binding** — which is Project 1's `closure-is-not-dynamic` test.

### (c) [6]

**Why no recursion [2]:** `Let x e b` evaluates `e` in the **outer** environment, before `x` is bound, so the
closure `f` captures an `Env` that does not contain `f`. When the body calls `f`, the lookup of `f` inside
`f`'s own body fails with `Unbound`.

**The minimal change [2]:** make `Let` bind `x` in the environment that `e` itself is evaluated in — a
**recursive `let`**:

```haskell
Let x e b -> do
  let env' = extend x v env
      v    = …evaluate e in env'…      -- v refers to env', which refers to v
  eval env' b
```

**The cost:** `v` is now defined in terms of an environment containing `v`, so a *non*-function right-hand side
that examines itself is an infinite loop rather than an error — `let x = x + 1` becomes `<<loop>>` instead of
`Unbound x`. **Accept "add a `LetRec` constructor" as an alternative**, with the cost being one more case
everywhere.

**The Week 3 concept [2]: laziness**, specifically that a `let`-bound value may refer to itself if it is
**productive** (L08 §2). In a strict language `env'` could not be built, because `v` would have to be evaluated
first; in Haskell the knot ties. **This is `fibs` in a different costume** and a student who says so has the
best possible answer.

---

## Marks

| Q | Topic | Parts | Points |
|---|---|---:|---:|
| 1 | `<*>` against `>>=` | 3 | 20 |
| 2 | An applicative that is not a monad | 3 | 22 |
| 3 | The order of the stack | 3 | 20 |
| 4 | `Stack` | 3 | 20 |
| 5 | Where Project 1 would go | 3 | 18 |
| | **Total** | **15** | **100** |

---

## What to Watch For Across the Cohort

1. **A thin paper overall.** Expected — Project 1 is due the same day and is worth five times as much. Do not
   read it as disengagement; check Q5, which overlaps the project report.
2. **Q1(a) items 2 and 4 marked applicative.** They are reasoning from "does it do I/O" rather than from the
   dependency test. Five minutes in the Week 8 tutorial, before the language changes.
3. **Q3(c) not distinguishing performance from semantics.** This is the paper's sharpest question and it is
   on the final. Worth raising with the whole group.
4. **Q5(c) not reaching laziness.** The recursive-`let` knot is `fibs` again and it is the clearest
   demonstration in the course that Weeks 3 and 6 are one subject. Point it out to anyone who missed it.

---

*PROG 202 · Week 6 · PS 6 Solutions · INSTRUCTOR ONLY · © CSE Department*
