# PROG 202 · Problem Set 5 · Solutions
## Monads: `Maybe`, `Either`, `State`, and `IO`
### INSTRUCTOR ONLY — NOT FOR STUDENTS

---

**Released:** Week 5 Wednesday · **Due:** Week 6 Friday 17:00 · **100 points** · **15 parts, ~3 hours**

**What this paper is testing.** Q1 and Q2 are the examinable core of Week 5 and are due the day after the
midterm, so most of the cohort will have done them as revision — which is the intent. **Q2(a) is the
midterm question**, marked again here at leisure. Q3 is the measurement. Q4 makes them delete their own
hand-written plumbing from Project 1. Q5 extends Lab 5.

**Timing:** Q1 30 min, Q2 45 min, Q3 30 min, Q4 40 min, Q5 35 min.

**Reference files in this directory:** `MiniSol.hs` (Lab 5), `OwnState.hs` (Q2a).

---

## Q1: `>>=` and `do` (20)

### (a) [7]

```haskell
do { x <- m; y <- n x; pure (x, y) }   ==  m >>= \x -> n x >>= \y -> pure (x, y)
do { m; n; pure () }                    ==  m >> n >> pure ()
do { x <- m; let y = x + 1; pure y }    ==  m >>= \x -> let y = x + 1 in pure y
```
[4]

**The four rules [3]:**

| | |
|---|---|
| `do { x <- m; rest }` | `m >>= \x -> do { rest }` |
| `do { m; rest }` | `m >> do { rest }` |
| `do { let x = e; rest }` | `let x = e in do { rest }` |
| `do { m }` | `m` |

*`resources/newmonad.hs` has both forms of the same computation and they print identically — `(Box 3,Box 3)`.*

### (b) [6]

```haskell
instance Monad Maybe where
  Nothing >>= _ = Nothing
  Just x  >>= f = f x

instance Monad (Either e) where
  Left e  >>= _ = Left e
  Right x >>= f = f x
```
[3]

**Why `Either e` [2]:** a `Monad`'s parameter must be a type constructor of **exactly one remaining
argument** — kind `* -> *`. `Either` takes two, so it must be partially applied, which fixes the *error*
type and leaves the *success* type varying. **That is why `Right` means success**: it is not a convention
you could reverse without also reversing which type the monad threads.

**The trace [1]:** `lookup "a" env` gives `Just 1`, so the first `>>=` takes the `Just x >>= f = f x` branch
and calls the lambda. `lookup "b" env` gives `Nothing`, so the **second** `>>=` takes `Nothing >>= _ =
Nothing` and **`pure (a + b)` is never evaluated.** The computation stops at the second `>>=`.

### (c) [7]

**The error, verbatim [2]:**

```
oldmonad.hs:4:10: error:
    • No instance for (Applicative Box)
        arising from the superclasses of an instance declaration
    • In the instance declaration for ‘Monad Box’
```

**The fix [3]:** `Functor`, then `Applicative`, then `Monad`, as in `resources/newmonad.hs`.

**Which `do` needed [1]:** `do` uses `>>=` (from `Monad`) and `pure` (from `Applicative`). It never uses
`fmap`. **All three instances must exist anyway, because of the superclass chain** — comment out `Functor`
and the `Applicative` instance is rejected. A student who separates "what `do` calls" from "what the
hierarchy requires" has the precise answer.

**`return` [1]** defaults to `pure` and is kept for backward compatibility with code written before 2015.
*(It is now a warning-free synonym; GHC has discussed removing it from the class for a decade.)*

---

## Q2: Writing `State` (22)

### (a) [10]

Full text in `OwnState.hs`, verified to compile `-Wall` clean apart from an unused `modify`, and to agree
with the library.

```haskell
newtype State s a = State { runState :: s -> (a, s) }

instance Monad (State s) where
  State g >>= f = State $ \s -> let (a, s') = g s
                                    State h = f a
                                in  h s'
```
[7 for the newtype, three instances and five functions.]

**The test [2]:** on `Node (Node Leaf 'a' Leaf) 'b' (Node Leaf 'c' Leaf)`,

```
Node (Node Leaf (0,'a') Leaf) (1,'b') (Node Leaf (2,'c') Leaf)
3
```

**The annotation of `>>=` [1]** — three steps and require all three:

1. `g s` — **run the first computation** from the incoming state, getting a result and a new state.
2. `f a` — **feed the result to `f`**, which gives back *the next computation* (not a value).
3. `h s'` — **run that computation from the new state.**

### (b) [6]

```
evalState (pure 1) undefined  ->  1
execState (pure 1) undefined  ->  EXCEPTION
```
[2]

**From their own `runState` [2]:** `pure 1` is `State $ \s -> (1, s)`, so `runState (pure 1) undefined` is
the pair `(1, undefined)`. `evalState` is `fst` and never forces the second component; `execState` is `snd`
and does. **A computation that does not look at the state does not force it** — the same fact as
`null (Just undefined)` in Week 4.

**Lazy vs Strict [2]:** **no difference** — measured, both behave identically here, because `pure` does not
`>>=` anything, and `State.Strict`'s extra forcing lives in `>>=`. **Full marks for checking and reporting
"no difference"**; this is a question where the expected answer is that the obvious hypothesis is wrong.

### (c) [6]

One paragraph, and it must contain three things. [2 each]

1. **Run it twice from the same start and get the same answer** — `runState c 0` is referentially
   transparent. In `Mini`: `runProgram e` twice gives the same `Trace`, every time.
2. **Run it from *any* start** — `execState (label t) 100` labels from 100 with no change to `label`. In
   `Mini`: run the same program with a pre-seeded step count to measure a fragment.
3. **Keep the intermediate states, because they are values** — there is no equivalent of "the variable's
   earlier value". In `Mini`: you could return every `Trace` along the way, not just the last.

**Deduct for "it's pure" without a consequence.**

---

## Q3: The Two Strictness Decisions (18)

### (a) [8]

`-O0`, *n* = 3,000,000:

| | maximum residency | time |
|---|---:|---:|
| `Lazy` + `modify` | 308,161,000 B | 2.976 s |
| `Lazy` + `modify'` | **397,931,816 B** | 3.729 s |
| `Strict` + `modify` | 167,178,928 B | 1.697 s |
| `Strict` + `modify'` | **44,328 B** | 0.500 s |

[5]

**The worse-when-stricter row [2]:** `Lazy` + `modify'`. It **forces every state value** *and* **still
builds a chain of unevaluated `(a, s)` pairs** — so it does all the forcing work and keeps all the
structure. Strictness in the wrong place costs and buys nothing.

**What each forces [1]:**

| | |
|---|---|
| `State.Strict` vs `.Lazy` | whether the **`(a, s)` pair** produced by each `>>=` is forced |
| `modify` vs `modify'` | whether the **new state value** is forced |

**They are orthogonal.**

### (b) [6]

**At `-O2` all four are 44,328 B.** [2]

**Why write `Strict` + `modify'` anyway [2]:** because the 44 KB is an optimisation and not part of the
program's meaning — the `-O0` column proves it — and because a small change to the program (a state the
optimiser cannot prove is always demanded) restores the 398 MB at any level. **Same argument as `foldl'`
in Week 2.**

**The other two places [2]:**

- **Week 3 L07 §6:** `foldl'` is strict in the accumulator's *constructor*, not its fields — **727 MB** for
  a lazy pair.
- **Week 3 PS 3 Q5(b):** `Data.Map.Strict` is strict in its *values*, `Data.Map.Lazy` is not — **107 MB
  against 44 KB, at `-O2`**, the case the optimiser does not repair.

### (c) [4]

| `tick` uses | `-O2` residency |
|---|---:|
| `modify'` | 9,783,360 B |
| `modify` | 17,516,648 B |
[2]

**The floor [2]:** `deepSum 200000` builds a **200,000-node expression tree before evaluation starts**, and
`runProgram` holds its root for the whole run — so ~9.8 MB is data the interpreter cannot avoid. The thunk
chain `modify` adds is about the same size again, hence 2× rather than L12's 7,000×.

**This is the honest version of the lesson and worth a remark on every script:** the lecture's loop had
nothing live but the accumulator. **In a real program a leak is a term added to something, not the whole
thing**, and a 2× residency regression is exactly the kind that ships.

---

## Q4: Refactoring With Monads (20)

### (a) [7]

```haskell
Bin op l r -> do
  lv <- eval env l
  rv <- eval env r
  binop op lv rv
```

**Four lines against the eight or nine of nested `case`s.** [4] `make test` must still give 27/27. [1]

**The law [2]: associativity.**
`(m >>= f) >>= g == m >>= (\x -> f x >>= g)` is exactly the claim that a block of `do` statements may be
extracted into a helper and called, which is what grouping the two `eval`s into a `do` block does.
**Accept "the third law" with the equation.**

### (b) [7]

The diff replaces `filterM'` with `filterM` and their recursion with `mapM`. [3]

**Their Week 4 guess [1]** — from PS 4 Q5(b), which asked them to name it. Give the mark for reporting the
guess honestly whether or not it was right.

**The table [3]:**

| | replaces |
|---|---|
| `mapM` / `traverse` | their `MapE` recursion, and Lab 1's `traverse id` |
| `filterM` | **their `filterM'`** |
| `sequence` | **Lab 1's `traverse id`** |
| `foldM` | none yet — Lab 5's `eval` over a list would be one |
| `replicateM`, `when` | none yet |

### (c) [6]

| `m` | `sequence` |
|---|---|
| `Maybe` | all the `Just`s, or `Nothing` if any is `Nothing`. `sequence [Just 1, Just 2]` = `Just [1,2]`; with a `Nothing`, `Nothing` |
| `Either String` | all the `Right`s, or the **first** `Left`. `sequence [Right 1, Left "e", Left "f"]` = `Left "e"` |
| `[]` | **the Cartesian product** |
[3]

**`sequence [[1,2],[3,4]]` is `[[1,3],[1,4],[2,3],[2,4]]`.** [2] The list monad's `>>=` is "for each
element, do the rest", so `sequence` over a list of lists produces every way of choosing one element from
each — which is not "flatten" and surprises everybody.

> **Worth a remark: Week 9 is this monad with a different syntax.** Prolog's backtracking is the list
> monad's non-determinism promoted to being the language's only control structure.

**Lab 1's one-line change [1]:** `timetable = sequence [ mkSession … ]`, and the output is unchanged.

---

## Q5: `Mini` (20)

### (a) [8]

14/14, and `eval` as in `MiniSol.hs`. [5]

**`let-scope` [3]:** **5 steps** — `Bin`, `Let`, `Num 1`, the inner `Var`, the outer `Var`. **The second
`Var "x"` is unbound** because `Let` extends the environment for its **body only**: the extended `env` is an
argument to one recursive call and is never returned. **That asymmetry is why the environment is not part of
the state**, and Week 6 names what it is instead.

### (b) [6]

**Two designs, and both are acceptable:** [4]

```haskell
-- (i) depth as an argument
eval :: Int -> Env -> Expr -> Interp Int     -- and `modify'` maxDepth = max d
-- (ii) a fourth field, incremented and decremented
depth :: !Int    -- enter: depth+1, update maxDepth; leave: depth-1
```

**(i) is the better answer and the marks are for saying why:** the depth goes *in* and never *out*, like
`Env`, so making it state means maintaining an invariant (every increment paired with a decrement) that the
type does not enforce — and an early `pure` or an exception would leave it wrong. **(ii) is what you would
write in an imperative language and it is the one with a bug waiting.** [1]

**`deep` is `foldr (\i acc -> Bin Add (Num i) acc) (Num 0) [1..10]`** — right-nested, so the depth is
**11**: ten `Bin` nodes plus the `Num 0` at the bottom. Accept 10 or 11 with the counting shown. [1]

### (c) [6]

- **Why not append [2]:** `warnings t ++ [w]` re-walks the whole log every time, so an *n*-entry log costs
  O(n²) — **L06 §5, measured at 22.57 s against 0.01 s at n = 40,000.** One `reverse` at the end is one
  O(n) pass.
- **Readable while running [2]:** you would have to emit as you go rather than accumulate — print in `IO`,
  or use a `Writer`-style structure with an O(1) append such as a difference list or `Data.Sequence`. **The
  cost is that the interpreter is no longer a pure function of its input**, or that you have taken on a
  structure with worse constants for the common case.
- **Without the `!`s [2]:** `steps` would be a chain of `+1` thunks — **Week 3 L07 §6**, and `modify'`
  would not save it, because `modify'` forces the `Trace` to WHNF (the constructor) and not its fields.
  **The same "strict in what?" question a fourth time.**

---

## Marks

| Q | Topic | Parts | Points |
|---|---|---:|---:|
| 1 | `>>=` and `do` | 3 | 20 |
| 2 | Writing `State` | 3 | 22 |
| 3 | The two strictness decisions | 3 | 18 |
| 4 | Refactoring with monads | 3 | 20 |
| 5 | `Mini` | 3 | 20 |
| | **Total** | **15** | **100** |

---

## What to Watch For Across the Cohort

1. **Q2(a) with `>>=` written but not understood.** The three-step annotation is the discriminator: a
   student who cannot say what `f a` returns has copied it. This was on the midterm the day before, so
   compare.
2. **Q3(a) not identifying the worse-when-stricter row.** They reported four numbers without reading them.
3. **Q4(c) answering "flatten" for the list monad.** Very common. `[[1,3],[1,4],[2,3],[2,4]]` is the
   answer, and it is worth ten seconds in the tutorial because **Week 9 depends on it.**
4. **Q5(b) choosing design (ii) without noticing the invariant.** The good students see that an
   increment/decrement pair is exactly the sort of thing a type should enforce and does not — which is Week
   1's argument arriving in Week 5.

---

*PROG 202 · Week 5 · PS 5 Solutions · INSTRUCTOR ONLY · © CSE Department*
