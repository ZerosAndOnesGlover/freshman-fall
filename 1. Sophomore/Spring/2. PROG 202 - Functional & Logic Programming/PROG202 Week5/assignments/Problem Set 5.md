# PROG 202 · Problem Set 5
## Monads: `Maybe`, `Either`, `State`, and `IO`

---

**Released:** Week 5, Wednesday · **Due:** Week 6, Friday 17:00
**Total: 100 points** · Submit one PDF, `PS5_{LastName}_{StudentID}.pdf`, plus your `.hs` files in a
tarball `PS5_{LastName}.tar.gz`

> **About three hours.** Five questions, fifteen parts.
>
> **The midterm is the Thursday of Week 6 and covers Weeks 0–5** — so this problem set is due the day
> after it. **Q1 and Q2 are the most examinable things in Week 5**; do them before the paper and the
> problem set becomes revision rather than a second demand.
>
> **State your `ghc --version`.** Q3 is a measurement. **Every `.hs` file compiles clean under
> `ghc -Wall -O2`.**

---

### Q1: `>>=` and `do` (20 points)

**(a) [7]** Desugar each by hand into `>>=`, `>>` and lambdas. Then compile both forms and confirm they are
the same value.

```haskell
do { x <- m; y <- n x; pure (x, y) }
do { m; n; pure () }
do { x <- m; let y = x + 1; pure y }
```

Then state the four desugaring rules in one line each.

**(b) [6]** `instance Monad Maybe` is two lines and `instance Monad (Either e)` is two lines.

- Write both from memory, then check.
- **Why `Either e` and not `Either`?** Say what kind of thing a `Monad`'s parameter must be.
- `lookup "a" env >>= \a -> lookup "b" env >>= \b -> pure (a + b)` where `"b"` is missing. **Trace it
  through your two-line instance**, and say at which `>>=` the computation stops.

**(c) [7]** Take `newtype Box a = Box a`.

- Write `instance Monad Box` with **only** `return` and `>>=`, compile it, and **report the error
  verbatim**.
- Fix it. Report all three instances, in order.
- **Which of the three did `do` notation actually need?** Comment each out in turn and report what breaks.
- `return` is no longer needed at all. Say what it defaults to, and why the standard library keeps it.

---

### Q2: Writing `State` (22 points)

**(a) [10]** With **no import of `Control.Monad.State`**, write:

```haskell
newtype State s a = State { runState :: s -> (a, s) }
```

and then `instance Functor (State s)`, `instance Applicative (State s)`, `instance Monad (State s)`, and
`get`, `put`, `modify`, `evalState`, `execState`.

- Report all of it.
- **Test it** on `label` from L12 §1 — the in-order tree numbering — and report the labelled tree and the
  final counter for a three-node tree.
- **`>>=` is the only interesting line.** Annotate yours: say what each of its three steps does.

**(b) [6]** `evalState (pure 1) undefined` succeeds; `execState (pure 1) undefined` throws.

- Predict, run, report.
- **Explain from your own `runState`**, not from the library's.
- Does it differ between `Control.Monad.State.Lazy` and `.Strict`? Check, and report.

**(c) [6]** *"`State` is just mutation with extra steps."*

Answer in one paragraph, and your answer must contain **three things you can do with `State` that you
cannot do with a mutable variable.** L12 §2 lists them; give an example of each in `sq` or `Mini` terms.

---

### Q3: The Two Strictness Decisions (18 points)

**(a) [8]** Build `resources/state.hs` at `-O0` and report all four:

| | maximum residency | time |
|---|---|---|
| `Lazy` + `modify` | | |
| `Lazy` + `modify'` | | |
| `Strict` + `modify` | | |
| `Strict` + `modify'` | | |

- **One row is worse than the row above it although it is "more strict".** Identify it and explain.
- Say precisely what `State.Strict` forces and what `modify'` forces. They are different things.

**(b) [6]** Now the same question at `-O2`.

- Report the four numbers.
- **They are all the same.** Give the two-sentence reason a student should nevertheless still write
  `Strict` and `modify'`.
- Name the *other* two places in Weeks 3–5 where the same "strict in what?" question arose, with their
  measurements.

**(c) [4]** In your Lab 5 `Mini.hs`, change `tick` from `modify'` to `modify` and measure `./bench 200000`.

- Report both residencies.
- **The ratio is about 2×, not 7,000×.** Say what is occupying the rest of the memory and why it puts a
  floor under the improvement.

---

### Q4: Refactoring With Monads (20 points)

**(a) [7]** In Project 1's `Eval.hs`, rewrite the `Bin`, `If` and `Field` cases using `do` notation.

- Report the before and after for `Bin`, with line counts.
- Confirm `make test` still gives the same number.
- **Which of the monad laws are you relying on** when you extract the two `eval` calls into a `do` block?
  Name it.

**(b) [7]** Replace your hand-written `filterM'` with `filterM` from `Control.Monad`, and your hand-written
`mapM` equivalent with `mapM`.

- Report the diff.
- **You wrote `filterM'` in Week 4 and were asked to guess its name.** Report your guess and whether it was
  right.
- `mapM`, `filterM`, `foldM`, `sequence`, `replicateM`, `when`. **For each, say which of your own code it
  replaces, or "none yet".**

**(c) [6]** `sequence :: Monad m => [m a] -> m [a]`.

- What does `sequence` do for `m = Maybe`? For `m = Either String`? For `m = []`?
- **The third one is not what you expect.** Run `sequence [[1,2],[3,4]]` and explain the answer.
- Lab 1's `traverse id` is `sequence`. **Report the one-line change** to Lab 1's `timetable` that uses it,
  and confirm the output is unchanged.

---

### Q5: `Mini` (20 points)

From your Lab 5 `Mini.hs`.

**(a) [8]** Report `make test` at 14/14, and your `eval`.

Then: `let-scope` is `Bin Add (Let "x" (Num 1) (Var "x")) (Var "x")` and expects
`(1, Trace 5 ["unbound variable x"])`. **Explain both numbers.**

**(b) [6]** Add a third field to `Trace`: `maxDepth :: !Int`, the deepest nesting reached.

- Report your change. **You will need to know the current depth**, which is not in `Trace`.
- **There are two ways to do it** — an extra argument to `eval`, or a fourth field that you increment and
  decrement. Implement one, describe the other, and say which you prefer and why.
- Report the `maxDepth` for the `deep` test case, and check it by hand.

**(c) [6]** `warn` conses at the front and `runProgram` reverses once at the end.

- **Why not append in `warn`?** Give the measurement from Week 2 that answers this.
- Suppose the log had to be readable *while the program was still running*. What would you change, and what
  would it cost?
- `Trace`'s fields are both `!`. **Say what would go wrong without them**, and name the week.

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

**Late work:** [[Year2 - Sophomore/COURSE POLICIES|COURSE POLICIES]] applies. **The lowest problem set of
the term is dropped.**

---

*PROG 202 · Week 5 · PS 5 · © CSE Department*
