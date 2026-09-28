# PROG 202 · Functional & Logic Programming
## Week 6 · Lecture 2 of 2
### Monad Transformers, and Why the Order of the Stack Changes the Answer

*“This is the story of a pattern that popped up time and again in our daily work, programming in Haskell, until the temptation to abstract it became irresistable.”* — Conor McBride & Ross Paterson, "Applicative programming with effects" (2008), §1

---

**Sat:** Thursday of Week 6, 11:00–12:15, TH 205 · **Reading:** Wadler §4 · **Next:** Week 7 L15, concurrency and STM · **⚠️ MIDTERM TONIGHT 18:00–19:15, VNC 100, Weeks 0–5**

**Coursework:** 📘 **Midterm** today 18:00–19:15 · 📝 **PS 5** due Fri this week 17:00 · 🔬 **Lab 6** Wed of Week 7 13:00–14:50

---

## 1. The Problem

Project 1's `eval` threads an environment and can fail:

```haskell
eval :: Env -> Expr -> Either Err Value
```

Now suppose it must also **count steps**, as Lab 5's `Mini` does. You need `Either` *and* `State`, and
neither monad is the other.

**You cannot compose two monads in general.** `Either Err (State Trace a)` is a type, and it is not a monad
you can `do` in — `>>=` would have to know how to get through both layers, and nothing gives it that. *(The
general fact: monads do not compose. Applicatives do, which is one more reason `Applicative` is a separate
class.)*

**A monad *transformer* is a monad parameterised by another monad.** `StateT s m` adds state to whatever `m`
is:

```haskell
newtype StateT s m a = StateT { runStateT :: s -> m (a, s) }
```

**Compare `State`:** `s -> (a, s)` becomes `s -> m (a, s)`. One `m`, and `State s = StateT s Identity`.

| Transformer | adds | run with |
|---|---|---|
| `StateT s m` | mutable-looking state | `runStateT`, `evalStateT`, `execStateT` |
| `ExceptT e m` | failure with a reason | `runExceptT` |
| `ReaderT r m` | a read-only environment | `runReaderT` |
| `WriterT w m` | an append-only log | `runWriterT` |
| `MaybeT m` | failure without a reason | `runMaybeT` |

**`Env` in Project 1 is a `Reader`.** It goes in and never comes out — L12 §5 flagged that asymmetry and
this is its name. A state you never modify is a reader, and saying so in the type stops anyone modifying it.

---

## 2. `lift`, and the Classes That Save You From It

A stack is layers, and to use an inner layer's operations you must `lift` through the outer ones:

```haskell
lift :: (MonadTrans t, Monad m) => m a -> t m a
```

In `StateT Int (Either String)`, `get` is at the outer layer and works directly, but `Either`'s failure is
inner:

```haskell
step n = do
  modify' (+ 1)
  when (n == 3) (lift (Left "boom at 3"))     -- lift, because Left is in the inner monad
```

**Counting `lift`s in a three-layer stack is miserable**, so `mtl` provides classes that do it for you:

| class | method | works at any depth |
|---|---|---|
| `MonadState s` | `get`, `put`, `modify'` | ✔ |
| `MonadError e` | `throwError`, `catchError` | ✔ |
| `MonadReader r` | `ask`, `local` | ✔ |
| `MonadIO` | `liftIO` | ✔ |

So the same function written against the classes needs no `lift` at all:

```haskell
step n = do
  modify' (+ 1)
  when (n == 3) (throwError "boom at 3")
```

**and it now works in *any* stack that has state and errors**, in either order. That is the point of `mtl`,
and it is also how the next section's trap hides.

---

## 3. The Measurement: the Order Changes the Answer

Two stacks with the same two effects. `resources/order.hs`:

```haskell
type SoverE = StateT Int (Either String)     -- state outside, Either inside
type EoverS = ExceptT String (State Int)     -- Either outside, state inside
```

**The same program in each** — count every step, fail on the third:

```haskell
step n = do { modify' (+ 1); when (n == 3) (throwError "boom at 3") }
```

Run over `[1..5]`:

```
StateT Int (Either String)  -- state outside:
Left "boom at 3"

ExceptT String (State Int)  -- Either outside:
(Left "boom at 3",3)
```

**Read those two lines carefully. They are the lecture.**

| | result | is the state available? |
|---|---|---|
| `StateT s (Either e)` | `Either e (a, s)` | **No.** On failure there is no pair at all, so **the count is gone** |
| `ExceptT e (State s)` | `(Either e a, s)` | **Yes.** The count is 3 — *how far it got* |

**Look at the types and it is obvious in hindsight:** `runStateT` gives `m (a, s)`, and if `m` is `Either e`
then a failure replaces the *whole* `(a, s)`. `runExceptT` over `State` gives `State s (Either e a)`, so the
state is outside the failure and survives it.

**And nothing warns you.** Both stacks compile; both run; the `step` function written against `MonadState`
and `MonadError` is **byte-identical** in the two. **The only difference is one line of type declaration, and
it decides whether your error report can say how far the program got.**

> **The rule, and it is the only one you need to remember:** **the effect you want to survive a failure goes
> *outside* `ExceptT`.** Logs, counters, metrics, partial results — outside. Anything you are content to lose
> — inside.
>
> **This is the third time this course has shown you that a type-level choice nobody warns you about decides
> a runtime property.** Week 3: `Data.Map.Strict` against `Lazy`. Week 5: `State.Strict` against `Lazy`.
> Now: the order of a transformer stack. **In every case both versions compile and one is wrong for your
> purpose.**

---

## 4. Functional Error Handling: Four Choices

You now have four ways for a computation to fail, and they are not interchangeable.

| | when | cost |
|---|---|---|
| **`Maybe`** | one failure mode, no explanation needed | the caller cannot report *why* |
| **`Either e`** | failure with a reason, **first one only** | no accumulation |
| **`Validation e`** | independent checks, **all reasons** | **not a monad** — no dependent steps |
| **`ExceptT e m`** | failure *plus* another effect | a transformer stack to reason about |

**And a fifth that this course does not use:** `throwIO`/`Control.Exception`, for genuinely exceptional
conditions in `IO` — a missing file, a dropped socket. **The rule Haskell practice has settled on:** expected
failures belong in the type; unexpected ones may be exceptions. *`error` and `undefined` are for neither;
they are for "this cannot happen", and L04 §2 measured what happens when it does.*

**The decision procedure, in order:**

1. Can it fail for exactly one uninteresting reason? **`Maybe`.**
2. Are the failures independent and worth reporting together? **`Validation`.**
3. Is the next step a function of the previous result? **`Either e`.**
4. Do you also need state, a log or `IO`? **`ExceptT e` over it**, and put what must survive on the outside.

---

## 5. Where Project 1 Would Go

```haskell
eval :: Expr -> ReaderT Env (ExceptT Err (State Trace)) Value
```

**Read it outside-in:** a reader for the environment (goes in, never out), an `ExceptT` for errors, and a
`State` for the trace — **and the `State` is innermost, so the trace survives an error.** Which is what you
want: an interpreter that fails should still be able to say how many steps it took.

**You are not asked to do this to Project 1.** Phase 3 is due next Friday and this would be a rewrite. **You
are asked to be able to write that type and justify the order**, which is PS 6 Q5 and a likely final-exam
question.

**Lab 6 builds it** — a three-layer stack over `IO`, small enough to fit in a session, and it measures what
happens when you get the order wrong.

---

## 6. The Honest Case Against

Transformer stacks are the standard answer and they have a real cost. Four objections, all fair:

1. **Error messages.** A type error inside a three-layer stack mentions all three layers and the `mtl`
   classes, and is genuinely hard to read. This is the most common reason people give up on them.
2. **`lift` counting**, if you are not using the `mtl` classes — and the classes have their own cost: `n`
   transformers need `n²` instances, which is why `mtl` is the size it is.
3. **Performance.** Each layer is a wrapper, and `-O2` usually but not always sees through them; a
   `StateT` over `IO` in a hot loop is measurably slower than an `IORef`.
4. **The order trap in §3**, which is not a cost so much as a hazard.

**The alternatives people actually use:** one hand-written monad for the whole application (a `newtype` over
the stack, with the instances written once); the `ReaderT` pattern (one `ReaderT Env IO` and `IORef`s inside
it); or effect systems. **All of them are re-litigating §3's question**, and knowing that question is what
transfers.

---

## 7. What to Take Away

1. **Monads do not compose in general.** A transformer is a monad parameterised by another monad:
   `StateT s m a = s -> m (a, s)`, and `State s = StateT s Identity`.
2. **A state you never modify is a `Reader`.** Project 1's `Env` is one.
3. **`lift` moves an operation up a layer**, and the `mtl` classes — `MonadState`, `MonadError`,
   `MonadReader`, `MonadIO` — mean you rarely write it.
4. **Measured: `StateT s (Either e)` loses the state on failure; `ExceptT e (State s)` keeps it.** Same
   program, `Left "boom at 3"` against `(Left "boom at 3", 3)`.
5. **The effect that must survive a failure goes outside `ExceptT`.**
6. **Nothing warns you**, and the `step` function is identical in both — the third time this course has shown
   a silent type-level choice deciding a runtime property.
7. **Four failure types, and a decision procedure**: `Maybe`, `Validation`, `Either`, `ExceptT` over
   something.
8. **The case against is real**: error messages, `n²` instances, wrapper cost. The alternatives all answer
   §3's question differently rather than avoiding it.

---

## Exercises

*(Not assessed. PS 6 is the assessed work. **The midterm is tonight** — do these after it.)*

1. Write out `runStateT`'s and `runExceptT`'s types for the two stacks in §3, and derive from the types alone
   which one keeps the state.
2. Add a `WriterT [String]` log to each of §3's stacks. **Where must it go for the log to survive a
   failure?** Predict, then check.
3. `State s = StateT s Identity`. Write `Identity` yourself — it is three lines — and check that
   `runIdentity . runStateT` behaves like `runState`.
4. Take Lab 5's `Mini` and give it an error case (division by zero becomes a failure rather than a warning).
   Do it twice, once with each stack order, and report what each gives for a program that fails halfway.
5. Write the type of Project 1's `eval` with a reader, errors and a step counter, and **justify the order of
   all three layers** in one sentence each.

---

*PROG 202 · Week 6 · L14 · © CSE Department*
