# PROG 202 · Lab 5
## An Interpreter That Counts Its Own Steps
### Week 5 · sat **Wednesday of Week 6**, 13:00–14:50, BH 215 · **unmarked, checked off in the session**

---

> **This lab covers Week 5** and is sat on the **Wednesday of Week 6**.
>
> **The midterm is the next evening** — Thursday of Week 6, 18:00–19:15, covering **Weeks 0–5**. This lab
> is the last piece of material it examines, and sitting a two-hour practical on the `State` monad
> twenty-nine hours before the paper is deliberate. **CS 212's midterm is this evening**, three hours after
> this lab ends; plan your Wednesday.
>
> **Nothing here is marked.** The TA checks your work off in the session.

**What you are doing:** writing an interpreter that carries a step counter and a warning log through every
recursive call **without either being an argument**.

**The language is deliberately smaller than Project 1's** — integers, variables, `let`, four operators, and
no errors at all. That is so the only thing under test is the monad.

**Five TODOs, fourteen test cases, and one measurement.**

---

## 0. Setup (8 minutes)

```bash
mkdir -p "$PROG202/week5/practice"
cd "$PROG202/week5/practice"
cp "$ACADEMICS/1. Sophomore/Spring/2. PROG 202 - Functional & Logic Programming/PROG202 Week5/lab/"{Mini.hs,Tests.hs,Main.hs,Bench.hs,Makefile} .
make test
```

It builds and dies on `TODO 1`. **`Mini.hs` is the only file you edit.**

**Read `Tests.hs` first.** Fourteen cases, each giving an expression and the exact `(answer, Trace)` it must
produce — **including the step count**. The step counts are the specification of where `tick` goes, and you
cannot guess them: `Num 42` is **1** step, `Bin Add (Num 1) (Num 2)` is **3**.

---

## 1. `tick` and `warn` (12 minutes) — TODOs 4 and 5

Do these **first**, even though they are numbered last, because nothing else compiles without them.

```haskell
tick :: Interp ()
tick = modify' (\t -> t { steps = steps t + 1 })
```

**`modify'`, not `modify`.** §5 measures what the other one costs, in this program.

```haskell
warn :: String -> Interp ()
warn w = modify' (\t -> t { warnings = w : warnings t })
```

**Note that `warn` conses at the front, so the log comes out backwards** — and `runProgram` reverses it
once at the end. **Do not be tempted to append.** Say why, in one sentence, before you move on; the answer
is L06 §5 and it is worth 22.57 seconds.

---

## 2. The Evaluator (30 minutes) — TODOs 1–3

```haskell
eval :: Env -> Expr -> Interp Int
```

**`Interp Int` is `State Trace Int`.** So `eval` returns a *computation*, and `do` sequences them.

**Every case ticks exactly once, before anything else.** That is what makes the test counts predictable,
and getting it wrong is the commonest way to fail a test whose answer is right.

- **`Num`** — tick, return.
- **`Var`** — tick, look up; if missing, `warn` and return 0. **This language has no errors on purpose**, so
  that the `State` monad is the only mechanism under test. Project 1 is where errors live.
- **`Bin`** — tick, evaluate both sides, combine. Division by zero warns and gives 0.
- **`Let`** — tick, evaluate the bound expression, then evaluate the body **in an extended environment**.

```bash
make test
```

**All fourteen must pass.**

**Answer before moving on:** `let-scope` is

```haskell
Bin Add (Let "x" (Num 1) (Var "x")) (Var "x")
```

and it expects `(1, Trace 5 ["unbound variable x"])`. **Explain both numbers** — why 5 steps, and why the
second `Var "x"` is unbound when the first was not.

---

## 3. What the Monad Is Doing (15 minutes)

**No line of your `eval` mentions `steps`, `warnings`, or a `Trace`.** The counter and the log are threaded
by `>>=` and you never wrote the threading.

**Prove it to yourself by writing the version without the monad.** Change the type to

```haskell
eval :: Env -> Expr -> Trace -> (Int, Trace)
```

and implement **just the `Bin` case**. Do not do the whole thing; three minutes on one case is enough.

**Then answer:**

1. **How many times does `Trace` appear** in your monadic `Bin` case, and in your explicit one?
2. In the explicit version, **what happens if you thread the wrong `Trace`** into the second recursive
   call — say the original instead of the one the first call returned? Does anything catch it?
3. **`State` is a fold with the accumulator hidden.** Say which part of Week 2 the hidden accumulator
   corresponds to.

**Put the monadic version back.**

---

## 4. `get`, `put`, and Writing `State` Yourself (20 minutes)

**This is on the midterm tomorrow**, so do it here rather than reading it.

In a scratch file, with **no import of `Control.Monad.State`**, write:

```haskell
newtype State s a = State { runState :: s -> (a, s) }
```

and then, in order: `instance Functor (State s)`, `instance Applicative (State s)`,
`instance Monad (State s)`, and then `get`, `put`, `modify`, `evalState`, `execState`.

**You will get the error from L11 §4 if you try `Monad` alone.** Get it on purpose; it is the one a 2009
tutorial will hand you.

Then check your own `State` against the library's on `label` from L12 §1:

```haskell
next = do { n <- get; put (n + 1); pure n }
```

**Answer:**

1. `evalState (pure 1) undefined` **succeeds** and `execState (pure 1) undefined` **throws**. Predict, run,
   explain — from your own `runState`, not from the library's.
2. Which of your three instances did `do` actually need? *(Try commenting each out.)*

---

## 5. Does `modify'` Matter Here? (15 minutes)

L12 §4 measured four State variants on a counting loop. **Now measure it in the interpreter you just
wrote.**

```bash
make bench
./bench 200000 +RTS -s 2>&1 | grep -E 'maximum residency|Total   time'
```

Then change `tick` to use **`modify`** instead of `modify'`, rebuild, and measure again.

**Reference numbers on a BH 215 machine, `-O2`, *n* = 200,000:**

| `tick` uses | maximum residency | time |
|---|---:|---:|
| `modify'` | **9.78 MB** | 0.131 s |
| `modify` | **17.5 MB** | 0.183 s |

and at `-O0`, **12.2 MB against 24.9 MB.** Roughly **2× at both optimisation levels.**

**Answer:**

1. Reproduce both rows at one optimisation level.
2. **2× is much less dramatic than L12's 308 MB against 44 KB.** Say why — what is taking up the other
   9.78 MB, and why does it put a floor under the improvement? *(Look at what `deepSum 200000` builds
   before evaluation starts.)*
3. `Mini.hs` imports `Control.Monad.State.Strict`. **Change it to `.Lazy` and measure again.** You now have
   four numbers; put them in L12 §4's table shape and say which of the two decisions mattered more **here**,
   and why that differs from the lecture's loop.

**Put `modify'` and `.Strict` back.**

---

## 6. Checkoff

Show the TA:

- [ ] `make test` printing **14/14** (§2)
- [ ] Your explanation of `let-scope`'s **5 steps** and its warning (§2)
- [ ] Your explicit `Bin` case, and your answer to §3 question 2 — **what catches a mis-threaded `Trace`**
- [ ] **Your own `State`**, with all three instances, running `next` correctly (§4)
- [ ] The `Applicative` error from trying `Monad` alone (§4)
- [ ] Both `bench` rows, and your answer to §5 question 2 (§5)

---

## What Comes Next

**The midterm is tomorrow evening**, 18:00–19:15, covering **Weeks 0–5**. §4 of this lab is the most likely
single question on it.

**Week 6 is applicatives and monad transformers** — how to have `State` *and* `Either` at the same time,
which is the type Project 1's `eval` would need if it had a step counter. It also explains Lab 1's
`traverse id` and Project 1's `filterM`, which you have now been asked to guess at twice.

**Project 1 is due Friday of Week 7.** Phase 3 needs nothing you have not seen.

**Lab 6 is on the Wednesday of Week 7.**

---

*PROG 202 · Week 5 · Lab 5 · © CSE Department*
