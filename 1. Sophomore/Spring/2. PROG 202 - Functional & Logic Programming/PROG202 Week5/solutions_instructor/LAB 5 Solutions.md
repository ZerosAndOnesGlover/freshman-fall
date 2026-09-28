# PROG 202 · Lab 5 · Solutions
## An Interpreter That Counts Its Own Steps
### INSTRUCTOR ONLY — NOT FOR STUDENTS

---

**Session:** Wednesday of Week 6, 13:00–14:50, BH 215 · **Unmarked**, checked off in the session.

**The scheduling matters and you should say so at the start.** The **midterm is tomorrow evening**, covering
Weeks 0–5, and **§4 of this lab is the most likely single question on it.** CS 212's midterm is *this*
evening, three hours after the lab ends. The room will be tired; §4 is the part to protect.

**What the session is really for.** §3 — writing one case of the interpreter *without* the monad, and
seeing that a mis-threaded state is not caught by anything. The monad's value is not brevity; it is that
**the threading cannot be got wrong**, because you never write it.

**Timing.** §0 8 · §1 12 · §2 30 · §3 15 · §4 20 · §5 15 · checkoff 8 = **108 minutes.** If behind, cut
**§5** (PS 5 Q3(c) covers it) — never §4.

**Reference solution:** `MiniSol.hs`.

---

## §1 — `tick` and `warn`

```haskell
tick :: Interp ()
tick = modify' (\t -> t { steps = steps t + 1 })

warn :: String -> Interp ()
warn w = modify' (\t -> t { warnings = w : warnings t })
```

**Why `warn` conses rather than appends:** `warnings t ++ [w]` walks the whole log every time, so building
an *n*-entry log costs O(n²) — **L06 §5, measured at 22.57 s against 0.01 s at n = 40,000.** `runProgram`
reverses once, which is one O(n) pass.

**Expect one student to ask why `Trace`'s fields are `!` when `modify'` already forces.** Good question, and
the answer is that they do different things: `modify'` forces the `Trace` to WHNF — the constructor — and
the **`!`s force the fields**. Without them, `steps` would be a chain of `+1` thunks exactly as in Week 3
L07 §6. **This is the same "strict in what?" question a third time and it is worth the two minutes.**

---

## §2 — The Evaluator

Full text in `MiniSol.hs`. The shape:

```haskell
eval env = \case
  Num n -> do { tick; pure n }
  Var x -> do
    tick
    case M.lookup x env of
      Just v  -> pure v
      Nothing -> do { warn ("unbound variable " ++ x); pure 0 }
  Bin op l r -> do
    tick
    a <- eval env l
    b <- eval env r
    case op of
      Div | b == 0 -> do { warn "division by zero"; pure 0 }
      …
  Let x e b -> do
    tick
    v <- eval env e
    eval (M.insert x v env) b
```

**All fourteen cases pass.** Verify before the session.

**The commonest failure is a right answer with a wrong step count** — usually `tick` after the recursive
calls rather than before, which changes nothing for these tests, or `tick` twice in `Bin`. Tell them the
counts are the specification.

**`let-scope`** — `Bin Add (Let "x" (Num 1) (Var "x")) (Var "x")` → `(1, Trace 5 ["unbound variable x"])`:

- **5 steps:** `Bin` 1, `Let` 1, `Num 1` 1, the inner `Var "x"` 1, the outer `Var "x"` 1.
- **The second `Var "x"` is unbound** because `Let` extends the environment **for its body only** — the
  extended `env` is an argument to one recursive call and is never returned. **That asymmetry is the whole
  point of the lab's comment about `Env` not being part of the state**, and it is what makes an environment
  a *reader* rather than a *state*. Week 6 names it.

*The answer is 1 and not 2 because the unbound `Var` gives 0. Students who expected an error have read
Project 1's spec into this one; say that this language has no errors on purpose.*

---

## §3 — What the Monad Is Doing

The explicit `Bin` case:

```haskell
eval :: Env -> Expr -> Trace -> (Int, Trace)
eval env (Bin op l r) t0 =
  let t1       = t0 { steps = steps t0 + 1 }
      (a, t2)  = eval env l t1
      (b, t3)  = eval env r t2
  in  (apply op a b, t3)
```

**Answers.**

1. `Trace` appears **zero** times in the monadic version and **six** times in the explicit one (type,
   `t0`, `t1`, `t2`, `t3`, and the result). Accept any count with the right shape.
2. **Nothing catches it.** Thread `t1` into the second call instead of `t2` and the program compiles, runs,
   and reports a step count that is too small — **the types are identical, because every `Trace` has the
   same type.** This is the answer to press for; it is the session's thesis.

   > **Say this:** the monad does not make the code shorter so much as it removes a variable you could get
   > wrong. There is no `t2` to confuse with `t1` because there is no `t2`.

3. **The hidden accumulator is `foldl`'s.** `State`'s `>>=` threads `s` from one computation to the next
   exactly as `foldl` threads its accumulator — **`State` is a fold with the accumulator hidden.**

---

## §4 — Writing `State` Yourself *(the midterm section)*

```haskell
newtype State s a = State { runState :: s -> (a, s) }

instance Functor (State s) where
  fmap f (State g) = State $ \s -> let (a, s') = g s in (f a, s')

instance Applicative (State s) where
  pure a = State $ \s -> (a, s)
  State f <*> State g = State $ \s -> let (h, s')  = f s
                                          (a, s'') = g s'
                                      in  (h a, s'')

instance Monad (State s) where
  State g >>= f = State $ \s -> let (a, s') = g s
                                    State h = f a
                                in  h s'

get          = State $ \s -> (s, s)
put s        = State $ \_ -> ((), s)
modify f     = State $ \s -> ((), f s)
evalState m s = fst (runState m s)
execState m s = snd (runState m s)
```

**Expect the `Monad`-alone error** and make sure they get it:

```
No instance for (Applicative (State s)) arising from the superclasses of an instance declaration
```

**Answers.**

1. Measured, and it is the same in `Lazy` and `Strict`:

   ```
   evalState (pure 1) undefined  ->  ok
   execState (pure 1) undefined  ->  EXCEPTION
   ```

   **From their own `runState`:** `pure 1` is `State $ \s -> (1, s)`, so the pair is `(1, undefined)`.
   `evalState` takes `fst` and never touches the second component; `execState` takes `snd` and forces it.
   **The state is never examined by a computation that does not look at it** — which is laziness being
   useful, and is the same fact as `null (Just undefined)` in Week 4.

2. **`do` needs `Monad`**, which needs `Applicative`, which needs `Functor` — so all three, but only because
   of the superclass chain. Comment out `Functor` and the `Applicative` instance fails to be accepted;
   comment out `Applicative` and `Monad` does. **`do` itself uses only `>>=` and `pure`.** A student who
   notices that `pure` comes from `Applicative` and `>>=` from `Monad`, and that `fmap` is never used by
   `do` at all, has the precise answer.

---

## §5 — Does `modify'` Matter Here?

**Measured on a BH 215 machine, `./bench 200000`:**

| | `-O2` residency | `-O2` time | `-O0` residency |
|---|---:|---:|---:|
| `modify'` | **9,783,360 B** | 0.131 s | **12,183,288 B** |
| `modify` | **17,516,648 B** | 0.183 s | **24,892,488 B** |

**About 2× at both levels.**

**Answers.**

1. Reproduce either level.
2. **The floor is the expression tree itself.** `deepSum 200000` builds a right-nested `Bin` chain of
   200,000 nodes *before* evaluation begins, and that tree is live for the whole run because `runProgram`
   holds its root. So ~9.8 MB is data the interpreter cannot avoid, and the thunk chain `modify` adds is
   roughly the same size again — hence 2× rather than L12's 7,000×.

   **This is the honest version of the lesson** and it is worth saying: the lecture's loop had *nothing*
   live except the accumulator, which is why the ratio was enormous. **In a real program the leak is a term
   added to something, not the whole thing.**

3. Switching to `.Lazy` as well gives the four-number table from L12 §4. **Here `modify'` matters more than
   `Strict`**, which is the reverse of the lecture's loop — because `Bin` binds its two results with `<-`
   and then uses them immediately, so the pairs are consumed promptly and the *state value* is the only
   thing that accumulates. **Accept any answer that notices the ranking differs and offers a reason
   grounded in what their own `eval` does with its results.**

---

## Checkoff

Six items. **Be strict about two:**

- **§3 question 2** must be answered with "nothing catches it". A student who says the compiler would is
  guessing.
- **§4's three instances must be their own**, not the library's, and they must have seen the `Applicative`
  error. This is tomorrow's exam question.

---

## After the Session

**The midterm is tomorrow, 18:00–19:15, Weeks 0–5.** Remind them: §4 of this lab, L07 §3's definition of
WHNF, and L06 §3's fold table are the three highest-value things to have fresh.

**PS 5 is due the Friday of Week 6**, the day after the paper.

**Project 1 is due the Friday of Week 7.** Phase 3 needs nothing they have not now seen, and **Spring Break
is after the deadline.**

**Quiz 6 is the Tuesday of Week 6** and covers this week.

---

*PROG 202 · Week 5 · Lab 5 Solutions · INSTRUCTOR ONLY · © CSE Department*
