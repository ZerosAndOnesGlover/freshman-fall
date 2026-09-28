# PROG 202 · Reading Guide · Week 5
## Wadler's monad paper — and the two sections of it that are this week

---

**This week's required reading is Wadler, *Monads for Functional Programming* (1992).** Twenty-four pages,
**on the final**, and — unlike the Hughes paper in Week 3 — you should read **§1–§3 before Tuesday** and
**§4–§5 before Thursday**, because the lectures follow it directly.

**Budget two hours for the paper and one for Hutton.** The midterm is next Thursday, so this is the last
light-reading week until Week 8.

---

## Wadler, §1–§3 — Tuesday's lecture

**§1 opens with "Shall I be pure or impure?"** and that is the question the whole paper answers. Read the
introduction properly; it is two pages and it frames everything.

**§2 is the one to read twice.** Wadler takes a small evaluator and modifies it four times — adding error
handling, then state, then output, then non-determinism — **and each time the whole interpreter has to be
rewritten.** Then he does it again with monads and each change is local.

> **You have written §2's first version.** Project 1's `eval` is Wadler's evaluator with an `Either` for
> errors, and the `case … of Left e -> Left e` lines you wrote by hand are exactly the rewriting he is
> complaining about. **Read §2 with your own `Eval.hs` open.** It is the single best-timed piece of reading
> in this course.

**§3 gives the laws.** Three of them, and Wadler explains what each *buys* rather than just stating it.

**Questions to hold:**

1. §2's evaluator is modified four times. **For each of the four, say what Project 1 would need to change**
   — and note that one of the four is already there.
2. §3's laws are stated as equations between programs. **Which of the three is the one you rely on when you
   extract a couple of `do` statements into a helper function?** *(Exam question.)*
3. Wadler's notation is not Haskell's: he writes `unit` for `pure`/`return` and `*` for `>>=`, and his
   monad is a triple `(M, unit, *)`. **Do the translation once, in the margin**, and the rest reads
   normally.

---

## Wadler, §4–§5 — Thursday's lecture

**§4 is the state monad** — L12 §1 in the original. His `State` is the same `s -> (a, s)`, and his
derivation of it from the evaluator-with-a-counter is clearer than any lecture can be in fifty minutes.

**§5 is arrays with in-place update**, and it is where monads stop being a convenience and start being the
only way. Read it for the *idea* — that a monad can make a genuinely destructive operation safe, because
the type prevents the old version from being observed — and do not worry about the array API.

**Questions:**

1. **§4's counter is Lab 5's `steps`.** After the lab, come back and compare his version with yours.
2. §5's claim is that in-place update can be *safe* if the monad is the only way in. **That is Week 1's
   smart-constructor-plus-export-list argument** applied to mutation. Say why it is the same argument.
3. Wadler wrote this in 1992 and `IO` as we have it arrived in Haskell 1.3 in 1996. **Which parts of §5 did
   the language adopt, and which did it not?** *(`ST` and `IORef` are the answer; Week 7 meets them.)*

---

## Hutton §12.2–12.5

Now read the chapter you were told to stop in the middle of last week.

| | |
|---|---|
| **§12.2** | `Applicative`. **Read it, and expect it not to land yet** — Week 6 gives the reason to want it |
| **§12.3** | `Monad`. This is L11, with `Maybe`, `[]` and `State` as the examples |
| §12.4 | The monad laws, again. Compare with Wadler §3 |
| §12.5 | The `do` desugaring rules, precisely stated. **Worth copying out** |

**Question:** Hutton's §12.3 uses the **list** monad as a main example and this course barely mentions it.
`sequence [[1,2],[3,4]]` is `[[1,3],[1,4],[2,3],[2,4]]` — **the Cartesian product.** Work out from
`instance Monad []` why, and then note that **Week 9 is this monad with a different syntax**: Prolog's
backtracking is the list monad's non-determinism made the language's only control structure.

---

## Real World Haskell

**Chapter 14, "Monads"** — and this is the chapter with the incompatibility. Its instances are written with
`return` and `>>=` alone and **will not compile on GHC 9.4.7**:

```
oldmonad.hs:4:10: error:
    • No instance for (Applicative Box)
        arising from the superclasses of an instance declaration
```

**Read it anyway**, because its `Logger` and `Parse` monads are worked out more carefully than anywhere
else, and **mentally add the two missing instances.** `resources/oldmonad.hs` and `resources/newmonad.hs`
are the before and after; compile both once.

**This is the third and last of the three disagreements** the Week 0 syllabus promised. The other two were
the `foldl` symptom in Week 2 and the profiling flags in Week 3.

---

## What to Actually Do

**Read Wadler §2 with `Eval.hs` open**, and then write your own `State` from scratch before the lab.

§4 of Lab 5 asks for it, PS 5 Q2 marks it, and **the midterm is the Thursday after.** Three good reasons,
and the real one is that a monad you have implemented is a different object from a monad you have read
about.

---

*PROG 202 · Week 5 · Reading Guide · © CSE Department*
