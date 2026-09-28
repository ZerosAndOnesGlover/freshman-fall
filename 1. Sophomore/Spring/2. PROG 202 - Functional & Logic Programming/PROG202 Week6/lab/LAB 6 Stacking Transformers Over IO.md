# PROG 202 · Lab 6
## Stacking Transformers Over `IO`, and Finding the Order From the Failures
### Week 6 · sat **Wednesday of Week 7**, 13:00–14:50, BH 215 · **unmarked, checked off in the session**

---

> **This lab covers Week 6** and is sat on the **Wednesday of Week 7**.
>
> **Project 1 is due two days later** — Friday of Week 7, 17:00. This lab does not use Project 1's code
> and will not help you finish it; if Phase 3 is not done, do that first and come to the lab having read the
> sheet.
>
> **Nothing here is marked.** The TA checks your work off in the session.

**What you are doing:** building a three-effect stack over `IO` — a read-only config, a failure with a
reason, and a running trace — and then **finding out from the test failures that the order is wrong.**

**The skeleton ships with the stack in the wrong order on purpose.** Do the other TODOs first; `make test`
will then pass **6 of 13**, and every failure will have the same shape. Reading that shape is the lab.

---

## 0. Setup (8 minutes)

```bash
mkdir -p "$PROG202/week6/practice"
cd "$PROG202/week6/practice"
cp "$ACADEMICS/1. Sophomore/Spring/2. PROG 202 - Functional & Logic Programming/PROG202 Week6/lab/"{Stack.hs,Tests.hs,Main.hs,Makefile} .
make
```

It builds and dies on `TODO 3`. **`Stack.hs` is the only file you edit.**

**Read `Tests.hs` before you write anything.** Thirteen cases. Ten of them check `loadAll`, and each gives
the exact `(Either Err …, Trace)` expected — **including the trace after a failure.** Three check
`validateAll` and give an error *count*. **The messages must match exactly**; they are in `Tests.hs` and
they are the specification.

---

## 1. `loadSession` (25 minutes) — TODO 3

```haskell
loadSession :: Int -> String -> App (String, Int, Int)
```

A row is `"PROG 202,LEC,Tue,660,735"`. `splitOn` is given. Validate in the order `Tests.hs` expects:
empty course code, then start-not-a-number, then end-not-a-number, then starts-at-or-after-it-ends, then
outside-the-permitted-day, then the wrong field count.

**Two requirements that carry the marks:**

- **`bump` every row**, and `bump True` only for a good one. The traces in `Tests.hs` are the specification
  of where `bump` goes.
- **Get the bounds with `asks dayStart` and `asks dayEnd`.** Do **not** add a `Config` argument. The whole
  point of the `ReaderT` layer is that the config is not an argument, and a solution that passes it as one
  has not used the layer.

**Notice what you did not write:** no `lift`. `asks`, `modify'` and `throwError` all work directly, because
they come from the `mtl` classes `MonadReader`, `MonadState` and `MonadError` rather than from a particular
layer (L14 §2). **That is also why the wrong stack order compiles.**

---

## 2. `loadAll` (10 minutes) — TODO 4

One line plus the empty case. It is a `traverse` over the rows, and you need the row numbers — `zip [1..]`.

```bash
make test
```

You should now be passing about **6 of 13**, with seven failures.

---

## 3. `validateAll`, and an Applicative That Is Not a Monad (20 minutes) — TODO 5

```haskell
validateAll :: Config -> [String] -> ([Err], [(String, Int, Int)])
```

**Every bad row reported, not just the first.** The `App` stack cannot do this — its error layer
short-circuits, which is what `>>=` *means* (L13 §1) — so write the `Validation` applicative from L13 §3
here. Eleven lines.

Then `traverse` with it. **The traversal is identical; only the applicative changed.**

**Answer, in a comment in the file:**

1. **Why can `Validation` not be part of the `App` stack?** *(L13 §4. The instance compiles and breaks a
   law; name the law.)*
2. `loadAll` is monadic and `validateAll` is applicative, and **they do the same validations**. Which of the
   two could have been written the other way, and which could not?

```bash
make test
```

The three `validateAll` cases should now pass: **3, 1 and 0 errors.**

---

## 4. The Order (25 minutes) — TODO 1 and TODO 2

You are now passing **6 of 13**. Look at the seven failures.

```
FAIL empty course code
       want: (Left (BadRow 2 "empty course code"),Trace {rowsSeen = 2, rowsOk = 1})
       got : (Left (BadRow 2 "empty course code"),Trace {rowsSeen = 0, rowsOk = 0})
```

**Every failing case has the right error and `Trace 0 0`.** And every *passing* case either succeeds, or
fails with a trace that is genuinely zero.

**Work out what that means before you read on.** Then:

**(a)** Look at `runApp` as it stands. **It has to invent a `Trace` out of nothing** in the failure branch:

```haskell
pure (case r of Left e -> (Left e, Trace 0 0); Right (a, t) -> (Right a, t))
```

**Why did it have to?** Answer from the *type* of `runExceptT (runStateT …)`, not from the behaviour.

**(b)** Fix it. **One line in TODO 1 and one in TODO 2.** L14 §3's rule is one sentence; apply it.

```bash
make test
```

**13 of 13.**

**(c)** Answer these, and they are the checkoff:

1. **State the rule** you applied, in one sentence.
2. The `loadSession` function is **byte-identical** in the working and broken versions. **Nothing warned
   you.** Name the other two places in Weeks 3–6 where a silent type-level choice decided a runtime
   property, with their measurements.
3. Which of the two orders would you want for a **compiler** reporting a syntax error, and which for a
   **bank transfer** that fails halfway? Justify each in one sentence.

---

## 5. The Standalone Demonstration (12 minutes)

The same result, stripped to twenty lines:

```bash
cd "$ACADEMICS/1. Sophomore/Spring/2. PROG 202 - Functional & Logic Programming/PROG202 Week6/resources"
ghc -Wall -O2 -o order order.hs && ./order
```

```
StateT Int (Either String)  -- state outside:
Left "boom at 3"
ExceptT String (State Int)  -- Either outside:
(Left "boom at 3",3)
```

**Reproduce it.** Then:

**(a)** Add a `WriterT [String]` log to each stack. **Where must it go for the log to survive the failure?**
Predict, then check.

**(b)** `ghc -Wall -O2 -o validate validate.hs && ./validate` — the `Either`-against-`Validation`
comparison, **1 error against 3**. Reproduce it.

**(c)** `ghc -Wall -O2 -o vlaw vlaw.hs && ./vlaw` — the law violation. **Report all three lines.** Say which
law it is and why the library therefore ships no `Monad` instance for `Validation`.

---

## 6. Checkoff

Show the TA:

- [ ] `make test` printing **13/13** (§4b)
- [ ] `asks dayStart` used, and **no `Config` argument** anywhere in `loadSession` (§1)
- [ ] Your comment answering §3 question 1 — **which law `Validation`'s `Monad` instance breaks**
- [ ] The **failure shape** from §4 and your answer to §4(a) — *from the type*
- [ ] Your one-sentence rule from §4(c)1, and the two other cases from §4(c)2 with their numbers
- [ ] `./vlaw`'s three lines (§5c)

---

## What Comes Next

**Project 1 is due Friday, 17:00.** Then **Spring Break.**

**Week 7 is concurrency** — STM, lightweight threads, and `par`/`pseq` on eight cores. It is the last
Haskell week: **Week 8 changes language** and the punctuation reference starts again from nothing.

And Week 7 opens with a measurement this lab has prepared you for: **`par` applied to a thunk that nobody
forces gives a speed-up of exactly 1.0×.** Week 3 explains why; Week 7 measures it.

**Lab 7 is on the Wednesday of Week 8** — the first week of Prolog.

---

*PROG 202 · Week 6 · Lab 6 · © CSE Department*
