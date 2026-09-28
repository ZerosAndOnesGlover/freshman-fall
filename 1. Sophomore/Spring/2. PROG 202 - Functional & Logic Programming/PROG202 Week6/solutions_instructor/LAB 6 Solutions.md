# PROG 202 · Lab 6 · Solutions
## Stacking Transformers Over `IO`, and Finding the Order From the Failures
### INSTRUCTOR ONLY — NOT FOR STUDENTS

---

**Session:** Wednesday of Week 7, 13:00–14:50, BH 215 · **Unmarked**, checked off in the session.

**Project 1 is due two days later** and the room will be thinking about it. Say at the start that this lab
does not touch Project 1's code and will not help them finish it — **and that Phase 3 needs nothing they have
not seen.**

**What the session is really for.** §4. **The skeleton ships with the stack in the wrong order**, so the
students meet the transformer-order problem as a *diagnosis* rather than a definition: seven tests fail, every
failure has the same shape, and the shape is the answer.

**Timing.** §0 8 · §1 25 · §2 10 · §3 20 · §4 25 · §5 12 · checkoff 8 = **108 minutes.** Cut **§5** if
behind — PS 6 Q2 and Q3 cover all of it with marks. **Do not cut §4.**

**Reference solutions:** `StackSol.hs` (13/13) and `StackWrongOrder.hs` (6/13, for demonstrating).

---

## §1 — `loadSession`

Full text in `StackSol.hs`. The two things carrying the marks:

**`bump` on every row, `bump True` only for a good one.** The traces in `Tests.hs` are the specification; a
student whose answers are right and whose traces are wrong has put `bump` in the wrong place, usually inside
the `otherwise` branch only.

**`asks dayStart` / `asks dayEnd`, and no `Config` argument.** Be strict about this at the checkoff. A
solution that threads a `Config` works, passes every test, and **has not used the `ReaderT` layer at all** —
which is the one thing §1 exists to teach.

**The point to draw out, because it sets up §4:** they wrote **no `lift`**. `asks`, `modify'` and `throwError`
all work directly because they come from `MonadReader`, `MonadState` and `MonadError` rather than from a
particular layer (L14 §2).

> **Say this now, not in §4:** the `mtl` classes are what make the code layer-agnostic — **and that is exactly
> why the wrong stack order compiles.** The convenience and the hazard are the same mechanism.

---

## §2 — `loadAll`

```haskell
loadAll [] = throwError Empty
loadAll rs = traverse (uncurry loadSession) (zip [1 ..] rs)
```

**6 of 13 passing at this point.** Check that before moving on; if a student is passing more or fewer, their
`bump` placement differs from the spec and §4's diagnosis will not be clean.

---

## §3 — `validateAll`

The `Validation` newtype plus `Functor` and `Applicative`, then `traverse` with it. Full text in
`StackSol.hs`. **Expected: 3, 1 and 0 errors** for the three `orderCases`.

**Answers.**

1. **`Validation` cannot be part of the stack because it must not be a `Monad`.** The instance compiles and
   **breaks the law `(<*>) == ap`** — measured in `resources/vlaw.hs`: `Left ["e1","e2"]` against
   `Left ["e1"]`. A transformer stack is built from monads, so there is no `ValidationT`.
2. **`loadAll` could have been applicative** — the rows are independent, and only `App`'s error layer forces
   the short-circuit. **`validateAll` could not have been monadic**, because a monadic version would
   short-circuit and the whole point is that it does not. **The asymmetry is the answer**: applicative is the
   weaker interface, so more things can implement it, and the accumulation is available only there.

*Listen for "because `Validation` is not a monad" with no law named. Half credit; the law is the content.*

---

## §4 — The Order *(the session)*

**The failure shape, and put it on the board:**

```
FAIL empty course code
       want: (Left (BadRow 2 "empty course code"),Trace {rowsSeen = 2, rowsOk = 1})
       got : (Left (BadRow 2 "empty course code"),Trace {rowsSeen = 0, rowsOk = 0})
```

**Every failing case: right error, `Trace 0 0`.** Seven of them. Every passing case either succeeds or has a
genuinely zero trace.

**(a) The answer must come from the type**, and that is the marked part:

```haskell
runStateT  :: StateT s m a -> s -> m (a, s)
runExceptT :: ExceptT e m a -> m (Either e a)
```

With `App = ReaderT Config (StateT Trace (ExceptT Err IO))`, running the state layer gives
`ExceptT Err IO (a, Trace)` — so the **whole pair** sits inside the `Either`, and a `Left` replaces it. **There
is no `Trace` to return**, which is why `runApp` had to invent one.

**(b) The fix, two lines:**

```haskell
type App a = ReaderT Config (ExceptT Err (StateT Trace IO)) a

runApp cfg act = runStateT (runExceptT (runReaderT act cfg)) (Trace 0 0)
```

`runStateT` is now outermost, so its result is `IO (Either Err a, Trace)` — **the state is outside the
failure.** 13/13.

**(c) Answers.**

1. **The rule:** *the effect you want to survive a failure goes **outside** `ExceptT`.*
2. **Nothing warned them**, and the other two cases are:
   - **Week 3:** `Data.Map.Lazy` as a counter, **107 MB against `Strict`'s 44 KB, both at `-O2`.**
   - **Week 5:** `State.Lazy` + `modify'`, **398 MB against `Strict` + `modify'`'s 44 KB** at `-O0`.

   *And the third-different-in-kind question, which is PS 6 Q3(c): the first two are **performance** — both
   versions compute the same answer — and this one is **semantics**: the two stacks give different results.
   That is a sharper distinction and the good students find it.*
3. **A compiler wants the state outside** — it should report the syntax error *and* how many tokens it got
   through, so `ExceptT` innermost of the two. **A bank transfer wants it inside**: on failure you want no
   partial state at all, and losing it is the feature. **Accept either assignment if defended**; the marks are
   for noticing that the right answer depends on whether the partial state is *evidence* or *damage*.

---

## §5 — The Standalone Demonstrations *(cut if over time)*

```
StateT Int (Either String)  -- state outside:      Left "boom at 3"
ExceptT String (State Int)  -- Either outside:     (Left "boom at 3",3)
```

**(a)** `WriterT [String]` must go **outside `ExceptT`** to survive, exactly as the state must. In a four-layer
stack the rule generalises: **everything you want after a failure goes outside the `ExceptT`, in any order
among themselves.**

**(b)** `Either` 1 error, `Validation` 3. **(c)** The three lines of `vlaw`, and the law is **`(<*>) == ap`**.

---

## Checkoff

Six items. **Be strict about two:**

- **No `Config` argument** in `loadSession`. It is the only way to tell whether they used the `Reader` layer.
- **§4(a) answered from the type.** A student who says "because the state gets lost" has described the symptom
  they were shown. The question is why, and `runStateT :: … -> m (a, s)` is the whole answer.

---

## After the Session

**Project 1 is due Friday 17:00.** Then Spring Break.

**PS 6 is due the same Friday**, and Q4 is this lab with marks. Tell them Q5 is Project 1's report question
(c), so it is not extra work.

**Week 7 is the last Haskell week.** Its opening measurement is one this lab has prepared them for: **`par` on
a thunk nobody forces gives a speed-up of exactly 1.0×** — Week 3's WHNF, one more time.

**Lab 7 is the Wednesday of Week 8**, by which point the course is in Prolog.

---

*PROG 202 · Week 6 · Lab 6 Solutions · INSTRUCTOR ONLY · © CSE Department*
