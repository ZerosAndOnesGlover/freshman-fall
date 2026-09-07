# CS 211 · Quiz 9

**Sat:** Tuesday of **Week 9**, first 10 minutes of lecture · TH 205
**Covers:** **Week 8** — type systems, polymorphism, type classes, Curry-Howard
**Unmarked.** Recorded in [[_CS 211 Lab and Quiz Record]].

**The answer key is printed below the questions.** Do not look at it until you have written something for all six.

---

## Questions

**1.** *(2 min)* Week 3's inference engine, run unchanged over Week 7's `prelude.lam`, rejects 16 of the 55 definitions.

**Every rejection is the same check.** Name it, and say in one sentence what it refuses to construct.

---

**2.** *(2 min)* `and = λp q. p q p` computes conjunction correctly on all four inputs, and does not typecheck.

Explain why it fails, and say what this shows about the relationship between *computes the right answer* and *is well-typed*.

---

**3.** *(2 min)* `zero`, `false` and `nil` are the same term. Inference gives all three the type `∀a b. a → b → b`.

**So types did not separate them.** Say why not — and name the thing that would.

---

**4.** *(1 min)* These two terms have the same normal form, `λx. x`:

```
let i = \x. x in i i          (\i. i i) (\x. x)
```

One typechecks and one does not. **Name the property of type systems this demonstrates**, and say what it is incomplete *with respect to*.

---

**5.** *(2 min)* In Haskell, `member :: Eq a => a -> [a] -> Bool` elaborates to `member :: DictEq a -> a -> [a] -> Bool`.

Say what happened to the `=>`, what a *class* and an *instance* become, and **when** a missing instance is reported.

---

**6.** *(1 min)* Under Curry-Howard, the proof of `A → B → A` is `λp q. p`.

`A ∨ ¬A` has **no** proof. Say why, in terms of what a proof of a disjunction has to *be*.

---
---

## Answer Key

**1.** The **occurs check**. It refuses to construct an **infinite type** — one that would have to contain itself, like `a = a → b`.

*You have met it twice before: Week 3 rejecting `λx. x x`, and Week 6, where `cyc_array.cy` could not be written because a self-containing array needs `T = [T]`.*

---

**2.** `and = λp q. p q p` applies `p` to `q` **and to `p` itself**, so `p`'s type would have to contain its own type as an argument. Occurs check.

**Typeability and correctness are different properties.** Hindley-Milner is **sound and incomplete**: it rejects some programs that would have run perfectly. `and` is one of them — a correct definition of conjunction that is also an instance of a shape the type system must refuse in general.

*Church conjunction is self-application in disguise, and nothing in Week 7 could have revealed that.*

---

**3.** A **principal type is computed from the term**, and the three *are* the same term. Inference adds no information the term did not already contain — so it cannot distinguish meanings the term never recorded.

**What separates them is a declaration** — `data Bool = True | False`. That introduces a **nominal** distinction, grounded in a name a programmer chose rather than in structure.

*The useful axis is not typed against untyped. It is **inferred** against **declared**.*

*(Note the same holds for the three "theorems": `const`/`true`, `apply`/`one` and `compose`/`mult` all share their types too.)*

---

**4.** **Soundness with incompleteness** — the type system is incomplete **with respect to the set of programs that would have run without error.** It rejects some of them, always erring in the safe direction.

`(λi. i i) (λx. x)` reduces to the identity function and is perfectly harmless. HM rejects it because `i` is lambda-bound and therefore monomorphic, while the body needs it at two types.

*Third appearance of this shape: Week 5's may/must analyses, Week 6's reference counting, and now typing.*

---

**5.** The **`=>` became a `->`**: a constraint became an ordinary parameter.

- A **class** is a **record type** — `DictEq a = { eq }`.
- An **instance** is a **value** of that record. An instance with a context compiles to a *function*: `dEq_ListA dEq_a = { eq = eqList dEq_a }`.

A missing instance is reported **at compile time, during elaboration, before anything runs.** It is a type error, not a method-not-found.

*And the compiler builds dictionaries nobody wrote: `Eq [[Int]]` resolves to `(dEq_ListListInt (dEq_ListInt dEq_Int))`.*

---

**6.** A proof of `A ∨ B` must be a **tagged value** — it must say *which side* it has, and carry a proof of it.

So a proof of `A ∨ ¬A` would be a program that decides, for an arbitrary unknown `A`, whether to produce `inl` with a proof of `A` or `inr` with a function from `A` to `Void`. **It has nothing to inspect and no way to choose.**

Classical logic asserts "A or not A" without saying which; constructive logic demands the witness. Assume excluded middle as an axiom and every classical tautology returns — with `lem` appearing as a **free variable**, an assumption rather than a construction.

---

## How You Did

**6 correct** — you are ready for Week 9.
**4–5** — reread the section you missed before Thursday.
**0–3** — L17 and L18, properly, this week.

**Question 3 is the one that matters**, and it is the week's actual result. If you answered "types separate them", you have the Week 7 prediction rather than the Week 8 measurement — and the Week 7 files were corrected for exactly that reason.

---

*CS 211 · Week 9 · Quiz 9 · © CSE Department*
