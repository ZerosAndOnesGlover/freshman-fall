# PROG 202 · Functional & Logic Programming
## Week 6: Applicatives, Monad Transformers, and the Midterm

**Credits:** 3 (2 lecture + 1 lab) · **Prerequisites:** PROG 102, CS 211
**Assessment for this course (overall):** Problem Sets 40%, Projects 30%, Midterm 15%, Final 15%
**This week's deliverables:** **the MIDTERM**, PS 6, Quiz 6 (Tuesday, covers Week 5). **Lab 5 is sat this
Wednesday**; Lab 6 is sat on the Wednesday of Week 7.

> **⚠️ MIDTERM: Thursday 5 March, 18:00–19:15, VNC 100. 75 minutes, 100 marks, 15% of the course. Covers
> Weeks 0–5.**
>
> **One A4 sheet of your own handwritten notes is permitted, one side.** Write it — it is the best revision
> exercise there is, and you may keep it. **The paper prints its own figures**, so spend the sheet on
> definitions and code skeletons, not numbers.
>
> This is Week 6's third deadline-bearing item after CS 212's midterm (Wednesday evening) and MATH 251's
> (Monday). **Four evening exams in four evenings**; see [[Year2 - Sophomore/ASSESSMENT CALENDAR|ASSESSMENT CALENDAR]].

---

### Why This Week Exists

Because `>>=` is too strong, and because a stack of effects has an order that nobody warns you about.

**Too strong:** three independent checks on a form, over `Either`, report **one error**. That is not a bug —
`m >>= f` hands `f` the *result* of `m`, so if `m` failed there is nothing to hand over and `f` cannot run.
Short-circuiting is what `>>=` *means*. But the three checks do not depend on each other, and a user deserves
all three messages.

**`<*>`'s second argument is a value, not a function.** So the steps *cannot* depend on each other — and
because they cannot, both can run. Swap the `Applicative` instance and the same three checks report **three
errors**. **The traversal does not change; the strategy does.**

And then the part that is not a convenience but a correctness question. **Two stacks with the same two
effects, one difference in the type:**

| | on failure |
|---|---|
| `StateT s (Either e)` | `Left "boom at 3"` — **the count is gone** |
| `ExceptT e (State s)` | `(Left "boom at 3", 3)` — **the error *and* how far it got** |

**The program is byte-identical in both.** Nothing warns you.

---

### Learning Objectives

By the end of Week 6, you should be able to:

1. Give the types of `<*>` and `>>=` and say which argument is a function of the previous result.
2. **Decide applicative or monadic** from L13 §7's test, and write the `f <$> a <*> b <*> c` form.
3. Write an `Applicative` instance that **accumulates**, and say why it needs `Semigroup e`.
4. **Show that `Validation` must not be a `Monad`**, by naming and breaking `(<*>) == ap`.
5. Explain why `traverse`'s constraint is `Applicative` and not `Monad`, and give two consequences.
6. Say what `traverse id` has been since Week 1.
7. **Say what a monad transformer is**, and that `State s = StateT s Identity`.
8. Recognise a read-only state as a `Reader`.
9. Use `lift`, and say why the `mtl` classes mean you rarely do.
10. **State the stack-order rule** — what must survive a failure goes outside `ExceptT` — and derive it from
    the types of `runStateT` and `runExceptT`.
11. Choose between `Maybe`, `Either`, `Validation` and `ExceptT` for a given failure.
12. **Name the three silent type-level choices of Weeks 3–6**, and say which is different in kind.

---

### New Syntax and Symbols This Week

Full reference: [[PROG202 Week0/resources/Haskell Syntax and Symbols|Haskell Syntax and Symbols]].

| Symbol | Said out loud | Means |
|---|---|---|
| `<*>` | **"ap"** / "apply" | `f (a -> b) -> f a -> f b`. Both arguments already exist |
| `<*`, `*>` | **"then keep left / right"** | Run both, keep one result |
| `<$` | — | Replace the contents, keep the shape |
| `<\|>` | **"alternative"** / "or else" | First success of two. `Alternative`, mentioned only |
| `{-# LANGUAGE FlexibleContexts #-}` | — | Needed for `mtl`-class constraints on a concrete stack |

**Types and functions new this week:** `Applicative` *(now used)* · `liftA2` · `sequenceA` · `traverse` ·
`Traversable` · `ap` · `Validation` *(written by hand)* · `StateT` · `ExceptT` · `ReaderT` · `WriterT` ·
`MaybeT` · `Identity` · `lift` · `liftIO` · `runStateT` / `evalStateT` / `execStateT` · `runExceptT` ·
`runReaderT` · `ask` · `asks` · `local` · `throwError` · `catchError` · `MonadState` · `MonadError` ·
`MonadReader` · `MonadIO`.

> **`<*>` and `>>=` look similar and differ in one place.** `(>>=) :: m a -> (a -> m b) -> m b` — second
> argument a **function**. `(<*>) :: f (a -> b) -> f a -> f b` — second argument a **value**. Everything in
> L13 follows from that one difference, so if you read nothing else, read those two types side by side.

---

### This Week's Materials

| File | Purpose |
| --- | --- |
| [[PROG202 Week6/assignments/MIDTERM\|MIDTERM]] | **Thursday, 75 min, 100 marks.** Sections A 30 / B 40 / C 30, any two of three in C. Prints its own figures |
| [[L13 Applicative Functors and Errors That Accumulate]] | Why `Either` reports one error of three; `<*>` against `>>=`; **an applicative that accumulates — 1 error against 3**; **why `Validation` must not be a monad**, with the law broken; `traverse` at last |
| [[L14 Monad Transformers and Why the Order Matters]] | Transformers; `Reader` for a read-only state; `lift` and the `mtl` classes; **the order measurement**; four failure types and a decision procedure; where Project 1 would go; the honest case against |
| [[LAB 6 Stacking Transformers Over IO]] | A three-effect stack over `IO` — **shipped in the wrong order**, so the order is diagnosed from seven identically-shaped failures. **Wednesday of Week 7** |
| `lab/Stack.hs`, `Tests.hs`, `Main.hs`, `Makefile` | Five TODOs, thirteen cases, and a trace that must survive a failure |
| [[PROG202 Week6/assignments/Problem Set 6\|Problem Set 6]] | Fifteen parts, 100 points, due **Friday of Week 7** — **the same day as Project 1** |
| [[PROG202 Week6/assignments/QUIZ 6 Week 6 Tuesday\|QUIZ 6]] | Ten minutes, Tuesday, covers **Week 5**. The last diagnostic before the paper |
| [[PROG202 Week6/resources/Reading Guide Week 6\|Reading Guide Week 6]] | **The lightest reading week of the term, on purpose** — and what to put on the A4 sheet |
| `resources/order.hs`, `validate.hs`, `vlaw.hs` | The order measurement, the 1-against-3, and the law violation |
| `solutions_instructor/` | Instructor only — the mark scheme, both lab references, and `StackWrongOrder.hs` |

---

### The One Thing to Take From This Week

**The weaker interface admits more instances, and the stronger one destroys what you wanted.**

`Validation` accumulates errors because `<*>` guarantees its two arguments are independent. Give it a `Monad`
instance — which **compiles, `-Wall` silent** — and `>>=` must hand the second step the first's result, so on
failure the second step cannot run, so the accumulation is gone. Measured:

```
(+) <$> l1 <*> l2     = Validation (Left ["e1","e2"])
((+) <$> l1) `ap` l2  = Validation (Left ["e1"])
law (<*>) == ap holds? False
```

**So `Validation` can accumulate or it can be a monad, and not both** — which is why `Applicative` is a
separate class and not a stepping-stone to `Monad`, and why the standard library ships validation as a
different type rather than a flag on `Either`.

**And the week's other half is the same lesson about *order* rather than strength.** `StateT s (Either e)`
loses the state on failure; `ExceptT e (State s)` keeps it. **Same program, same `mtl` classes, byte-identical
code** — and the reason the code is identical is the reason the mistake is silent: `MonadState` and
`MonadError` are implemented at every depth, which is the convenience *and* the hazard.

**That is the third silent type-level choice this course has shown you, and it is the worst of the three.**
Week 3's `Data.Map.Lazy` and Week 5's `State.Lazy` cost **performance** — both versions compute the same
answer. This one costs **semantics**: the two stacks give different results, and no profiler will find it.

---

### Assessment Reminder

**Labs and quizzes carry no weight.** **Quiz *N* covers Week *N−1***, Tuesday, ten minutes.

> **Lab 5 is sat this Wednesday**, the day before the paper, on the `State` monad. Lab 6 — this week's — is
> sat the **Wednesday of Week 7**.
>
> **Project 1 is due Friday of Week 7, 17:00, with PS 6.** Both are that day and neither moves. Project 1 is
> 15% and PS 6 is about 3%; **do Project 1 first.** **Spring Break follows the deadline, not precedes it.**

Both are tracked in [[_PROG 202 Lab and Quiz Record]].

---

### Connections

**Back:** **this week finishes three things that have been open since Week 1.** Lab 1's `traverse id` is
`sequenceA`; Project 1's `filterM'` was `filterM`; and L12 §5's remark that `Env` "goes in and never comes
out" is now a `Reader`. Week 4's `Semigroup` is what `Validation` combines errors with — **the class that
looked like ceremony is what makes accumulation possible.**

**Sideways:** **CS 212's error-handling and API-versioning weeks** ask the same question about failure that
L14 §4 does, in a language without the types to express it.

**Forward:** **Week 7 is the last Haskell week** — STM, lightweight threads, `par`/`pseq` on eight cores — and
it opens with a measurement this week prepares: **`par` on a thunk nobody forces gives a speed-up of exactly
1.0×**, which is Week 3's WHNF once more. L13 §5's second consequence of `traverse`'s `Applicative`
constraint is what makes a parallel traversal legal at all.

**Then Week 8 changes language**, and the syntax reference starts again from nothing.

---

*PROG 202 · Week 6 · © CSE Department*
