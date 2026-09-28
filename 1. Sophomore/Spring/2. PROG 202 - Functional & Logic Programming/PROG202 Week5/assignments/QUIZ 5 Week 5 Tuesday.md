# PROG 202 · Quiz 5
## Administered: Tuesday, Week 5 (first 10 minutes of lecture)

**Name:** _________________________________ **Section:** ___________ **Date:** ___________

**Covers Week 4** — type classes, dictionaries, `Functor`, `Foldable`, and laws.

**Instructions:** Closed notes. 10 minutes.

> **Not marked, no weight.** The answer key is printed below. Sit it closed-book, then mark it yourself
> before you leave. **The midterm is next Thursday and covers Weeks 0–5**, so treat this one as a
> diagnostic.

---

**Q1.** `elem :: Eq a => a -> [a] -> Bool`. How many arguments, and what does the compiler pass that you
did not write?

&nbsp;

&nbsp;

---

**Q2.** Why is `:t 3` reported as `Num a => a` rather than as a type?

&nbsp;

&nbsp;

---

**Q3.** One function, two builds, differing only in a `SPECIALISE` pragma: 2.9 s against 2.2 s. Delete the
`NOINLINE` as well and it is **0.07 s**. What did GHC then become free to do?

&nbsp;

&nbsp;

---

**Q4.** `mempty :: Monoid a => a` takes no arguments. What chooses the instance?

&nbsp;

&nbsp;

---

**Q5.** `length ('x', 5)` is **1** and `maximum ("hello", 3)` is **3**. Why?

&nbsp;

&nbsp;

---

**Q6.** A `Functor` instance that swaps its subtrees compiles with `-Wall` silent. Which laws does it break,
and what does that tell you about the compiler's role?

&nbsp;

&nbsp;

---

**Q7.** Lab 4: `mempty = Stats 0 0 999` is plainly not an identity, and **all ten law checks passed.** Why?

&nbsp;

&nbsp;

---
---

## Answer Key

**Q1.** **Two.** The compiler passes a **dictionary** — a record of `Eq`'s methods for the chosen type — so
the generated code takes three arguments. **Everything left of `=>` is a caller's obligation, not a
parameter.**

---

**Q2.** Because **every integer literal is `fromInteger` applied to an `Integer`**, and
`fromInteger :: Num a => Integer -> a` is a method of `Num`. So `3` works at any numeric type and carries a
**constraint** instead of a type. *(At a GHCi prompt, defaulting then picks `Integer` so it can be printed.)*

---

**Q3.** **Inlining, specialisation, and unboxing/fusion.** With the call site visible, GHC inlines
`sumPoly` into `main`, sees that `a` is `Int` so the dictionary disappears, keeps the accumulator as an
unboxed `Int#` in a register, and fuses `[1..n]` away so no list is built.

**So the 30% is the cost of *preventing* GHC from doing its job**, not the cost of type classes.

---

**Q4.** **The caller's expected type.** There is no argument and no receiver, so nothing but the type the
result is used at can decide. `print mempty` is ambiguous; `print (mempty :: [Int])` is not.

**This is the one thing no OO interface can express**, and the sharpest way to see that a class is not an
interface.

---

**Q5.** **A tuple is `Foldable` in its second component only** — the functor is `(,) a`, so `a` is part of
the *structure* and not an element. So `('x', 5)` is a container of exactly one element, `5`.

`maximum ("hello", 3)` is 3 because `"hello"` is structure. **`length someTuple` is always 1**, and it
compiles silently.

---

**Q6.** **Both** — `fmap id == id` obviously, and composition because `fmap (f . g)` swaps once while
`fmap f . fmap g` swaps twice, and two swaps is none.

**The compiler's role is types, not laws.** An instance's laws are part of its contract and nothing in the
toolchain checks them, which is what Week 11 exists for.

---

**Q7.** Because `a = foldMap statsOf (take 5 ts)`, **`foldMap` seeds with `mempty`**, so `longest a` came
out as 999 rather than 50 — and `a <> mempty == a` then held vacuously. **The broken value contaminated the
data the law was checked against.**

A check that catches it has to build its `Stats` without going through `mempty`, e.g. from `statsOf`.
**A test written in terms of the thing it tests cannot see the thing it tests.**

---

### What to Do With Your Score

| If you missed | Reread |
|---|---|
| **Q1, Q4** | **L09 §2 and §5** — today's lecture is monads, and `>>=`'s type is unreadable if `=>` is not settled |
| Q2 | L09 §3 |
| Q3 | L09 §2 |
| Q5 | L10 §3 |
| **Q6, Q7** | **L10 §2 and Lab 4 §4c** — on the midterm |

**Q1 is the one that matters in the next fifty minutes.** `(>>=) :: Monad m => m a -> (a -> m b) -> m b`
takes **two** arguments.

---

*PROG 202 · Week 5 · Quiz 5 · covers Week 4 · ungraded*
