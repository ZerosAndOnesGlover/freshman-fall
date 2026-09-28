# PROG 202 · Quiz 6
## Administered: Tuesday, Week 6 (first 10 minutes of lecture)

**Name:** _________________________________ **Section:** ___________ **Date:** ___________

**Covers Week 5** — monads, `>>=`, `do`, `State`, `IO`.

**Instructions:** Closed book. 10 minutes.

> **Not marked, no weight.** The key is printed below. **The midterm is this Thursday and covers Weeks
> 0–5** — this is your last diagnostic before it, so mark it honestly.

---

**Q1.** Give the type of `>>=`. How many arguments does it take?

&nbsp;

&nbsp;

---

**Q2.** Desugar `do { x <- m; y <- n x; pure (x, y) }`. Then say what `<-` actually is.

&nbsp;

&nbsp;

---

**Q3.** Why is it `instance Monad (Either e)` and not `instance Monad Either`?

&nbsp;

&nbsp;

---

**Q4.** `newtype State s a = State { runState :: s -> (a, s) }`. Write `>>=` for it.

&nbsp;

&nbsp;

&nbsp;

---

**Q5.** In one sentence: what is `IO`, and what single thing distinguishes it from `State RealWorld`?

&nbsp;

&nbsp;

---

**Q6.** Counting to 3×10⁶ at `-O0`: `Lazy`+`modify` 308 MB, **`Lazy`+`modify'` 398 MB**, `Strict`+`modify`
167 MB, `Strict`+`modify'` 44 KB. Why is the second row worse than the first?

&nbsp;

&nbsp;

---

**Q7.** `sequence [[1,2],[3,4]]`. What is it?

&nbsp;

&nbsp;

---
---

## Answer Key

**Q1.** `(>>=) :: Monad m => m a -> (a -> m b) -> m b`. **Two arguments** — the `Monad m =>` is a
constraint, and the compiler passes the dictionary.

---

**Q2.** `m >>= \x -> n x >>= \y -> pure (x, y)`.

**`<-` is the parameter of a lambda that `>>=` is about to be given.** Which is why it cannot be reassigned,
and why it is not assignment.

---

**Q3.** Because a `Monad`'s parameter must be a type constructor of **exactly one remaining argument** —
kind `* -> *`. `Either` takes two, so it must be partially applied. **That fixes the error type and leaves
the success type varying**, which is why `Right` means success as a matter of kinds rather than taste.

---

**Q4.**

```haskell
State g >>= f = State $ \s -> let (a, s') = g s
                                  State h = f a
                              in  h s'
```

Three steps: **run the first from the incoming state; feed its result to `f`, which gives back the *next
computation*; run that from the new state.**

---

**Q5.** **`IO` is `State RealWorld`** — each action receives the world the previous one produced, which is
why `>>=` sequences it. **The distinguishing thing is that `runState` is missing:** there is no
`runIO :: IO a -> a`, because you have no `RealWorld` to supply, so the only way an action runs is by being
reachable from `main`.

*`unsafePerformIO` is that missing function, provided anyway, and it discards every guarantee in this course.*

---

**Q6.** **`modify'` forces the state value; `State.Lazy` still builds a chain of unevaluated `(a, s)`
pairs.** So the lazy-plus-`modify'` version does **all the forcing work and keeps all the structure** — it
pays the cost of strictness and gets none of the benefit.

**They are two independent decisions:** `Strict` vs `Lazy` is about the *pair*, `modify` vs `modify'` about
the *value*. **You need both.**

---

**Q7.** **`[[1,3],[1,4],[2,3],[2,4]]` — the Cartesian product.** The list monad's `>>=` is "for each element,
do the rest", so `sequence` over a list of lists gives every way of choosing one element from each.

*Not "flatten". And **Week 9 is this monad with a different syntax** — Prolog's backtracking is the list
monad's non-determinism promoted to being the only control structure.*

---

### What to Do With Your Score

| If you missed | Reread |
|---|---|
| **Q1, Q2** | **L11 §2–§3** — today is `<*>`, whose type is unreadable if `>>=`'s is not settled |
| Q3 | L11 §2 |
| **Q4** | **L12 §1 — this is the most likely single question on Thursday's paper** |
| Q5 | L12 §3 |
| **Q6** | **L12 §4** |
| Q7 | PS 5 Q4(c) |

**Q4 is the one to fix today.** Section C of the midterm offers it as a fifteen-mark question and it is the
one most students choose.

---

*PROG 202 · Week 6 · Quiz 6 · covers Week 5 · ungraded*
