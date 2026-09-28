# PROG 202 · Reading Guide · Week 4
## Hutton 3.7–3.9, 8.5 and 14 — and the chapter you should *not* read yet

---

Week 4 is the last week before the midterm's coverage ends, and it is the week the `=>` you have been
reading since Week 0 gets explained. **Budget two hours**, and spend the rest on Project 1 Phase 1.

| Chapter | Now? | Why |
|---|---|---|
| **3.7–3.9** | **Read** | Class-constrained types, the standard classes, and the table of which basic types are in which. Six pages and they are L09 §1–§3 |
| **8.5–8.6** | **Read** | Declaring your own class and instances. §8.6's tautology checker is also **Project 1 in miniature** |
| **12.1** | **Read §12.1 only** | `Functor`. **Stop at the end of §12.1** — §12.2 is `Applicative` and §12.3 is monads, and both are next week or the one after |
| **14.1–14.4** | **Read** | `Monoid`, `Foldable`, `foldMap`. This is L10 §3 |
| 14.5 (`Traversable`) | skim | Lab 1's `traverse id` lives here. You will not understand it until Week 6; look at the *type* and move on |
| **12.2–12.5** | **not yet** | `Applicative` and monads. Week 5 and Week 6 |
| 15 | done in Week 3 | |

**If you have two hours:** §3.7–3.9, then §14.1–14.4, then §8.5, then §12.1.

---

## Chapter 3.7–3.9 — the six pages that answer Week 0

**Questions to hold:**

1. §3.7 introduces `Num a => a -> a`. Hutton calls these types *overloaded*. **What is the difference
   between `length :: [a] -> Int` and `sum :: Num a => [a] -> a`** — what can `sum` do that `length`
   cannot, and what can `length` be *sure* of that `sum` cannot? *(This is Wadler's quote at the top of
   L09, and it is a final-exam question.)*
2. §3.9's table lists which basic types belong to which class. **Find a type in `Num` that is not in
   `Ord`.** There is one in the standard library and it is the right design; say why. *(PS 4 Q1(c).)*
3. Hutton says `Integral` and `Fractional` are separate classes. **Work out what breaks if they are
   merged**, and then explain why `length xs / 2` is a type error in one sentence.

---

## Chapter 14 — `Monoid` before `Foldable`, and that order matters

§14.1 does `Monoid`, §14.2 `Foldable`, and it is worth noticing that **`foldMap` needs the first to
define the second.** Read them in that order even if you are tempted to skip to the folds.

**Questions:**

1. §14.1 gives `instance Monoid [a]` with `mempty = []` and `<>` as `++`. **Check both laws.** Then find
   the sentence where Hutton says the laws are not checked by the compiler — and if he does not say it,
   note that he does not.
2. §14.2's `Foldable` has a huge class declaration with defaults everywhere. **Which single method is the
   minimum?** There are two answers; give both and say which you would rather write.
3. §14.3 discusses `length`, `sum` and friends generalised to `Foldable`. **Hutton does not mention
   `length ('x', 5) == 1`.** Try it, then decide whether the omission is a fault in the book. *(There is
   a real argument that it is not: he is teaching the abstraction, not the standard library's choices.)*

---

## Chapter 12.1 — and stopping there

§12.1 is four pages on `Functor` and it is all you need this week.

**Question:** Hutton states the two functor laws and says instances "should" satisfy them. **Write an
instance that compiles and satisfies neither**, and then say what stops you shipping it. *(The answer is
not the compiler. It is Week 11, and L10 §2 is the argument.)*

**Do not read §12.2 onward.** `Applicative` without a reason to want it is a list of operators, and Week 6
supplies the reason. Every year some students read ahead here and arrive at Week 5 believing monads are
harder than they are.

---

## Real World Haskell

**Chapter 6, "Using Typeclasses"** — and this is the chapter where the book is at its best. It is written
for someone who wants to know *when* to declare a class rather than what the syntax is, and its
JSON-rendering example is the clearest motivation in print.

**One caution, and it is the third of this course's three disagreements with the book** *(the Week 0
syllabus lists all three)*: its Chapter 14 defines `Monad` instances with only `return` and `>>=`, which
**will not compile on GHC 9.4.7** — since GHC 7.10 every `Monad` must also be an `Applicative` and a
`Functor`. That bites next week, not this one, and Week 5 L11 §6 says exactly what to write instead.

---

## Not Reading: Project 1

**Project 1 was assigned on Wednesday and Phase 1 uses only this week's material and earlier.** PS 4 Q5
*is* Phase 1, so doing the problem set does the phase.

**The reading that actually helps Project 1** is Hutton **§8.6**, the tautology checker: a data type, a
recursive evaluator over it, an environment for variables, and a search. It is forty minutes and it is the
same shape as `Eval.hs`.

---

*PROG 202 · Week 4 · Reading Guide · © CSE Department*
