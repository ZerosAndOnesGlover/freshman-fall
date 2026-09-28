# PROG 202 · Functional & Logic Programming
## Week 4: Type Classes, `Functor`, `Foldable`, and Laws

**Credits:** 3 (2 lecture + 1 lab) · **Prerequisites:** PROG 102, CS 211
**Assessment for this course (overall):** Problem Sets 40%, Projects 30%, Midterm 15%, Final 15%
**This week's deliverables:** PS 4, Quiz 4 (Tuesday, covers Week 3), and **Project 1 is assigned
Wednesday** — due Friday of Week 7, 15% of the course. **Lab 3 is sat this Wednesday**; Lab 4 is sat on
the Wednesday of Week 5.

---

### Why This Week Exists

Because `:t 3` has said `Num a => a` since Week 0 and nobody has explained the `=>`.

```
ghci> :t 3
3 :: Num a => a
ghci> :t length
length :: Foldable t => t a -> Int
```

**A type class is a set of types with named operations, and a constraint is a requirement on the caller.**
That is the whole idea, and it comes with three things worth a week: it compiles to a **dictionary** the
compiler passes for you (measured at **30%**, and **40×** if you stop GHC optimising it away); it lets one
function serve every type at once, which is where `Functor` and `Foldable` come from; and it carries
**laws the compiler does not check**.

**That last clause is the week's real subject.** A `Functor` instance that swaps its subtrees compiles with
`-Wall` silent and breaks both functor laws. And in Lab 4 you will break `mempty` to something that is
plainly not an identity, watch **all ten law checks pass anyway**, and find out why.

---

### Learning Objectives

By the end of Week 4, you should be able to:

1. Read a constrained signature: how many arguments it takes, and what the constraint lets the
   implementation do.
2. **Explain `=>` as a dictionary argument**, and say who supplies it.
3. Declare a class with methods, defaults and a superclass, and read `{-# MINIMAL … #-}`.
4. **Say why `:t 3` is `Num a => a`** — that every integer literal is `fromInteger` — and hence why
   `length xs / 2` is a type error.
5. Write instances of `Eq`, `Show`, `Semigroup`, `Monoid`, `Functor` and `Foldable`.
6. **State the laws each class carries**, and say what breaks when one is violated — including that a bad
   `Ord` corrupts `Data.Map` silently rather than throwing.
7. **Say why a type class is not an interface**, in four ways, and why `mempty` is the one no interface can
   express.
8. Explain *coherence*, why there is no `instance Monoid Int`, and what `Sum`/`Product` are for.
9. **Measure what a dictionary costs**, and say why the cost is usually not paid.
10. Write `Foldable` with either `foldr` or `foldMap`, and say what `foldMap` buys that `foldr` cannot.
11. **Name three `Foldable`-on-a-tuple traps** and argue about whether the generalisation was worth it.
12. Say when *not* to generalise.

---

### New Syntax and Symbols This Week

Full reference: [[PROG202 Week0/resources/Haskell Syntax and Symbols|Haskell Syntax and Symbols]].

| Symbol | Said out loud | Means |
|---|---|---|
| `class C a where` | **"class"** | Declare a class. `a` is a type, or a **type constructor** for `Functor` |
| `instance C T where` | **"instance"** | `T` is in `C`, and here is how |
| `class B a => C a` | **"superclass"** | You cannot be `C` without being `B`. On a *class*, not a function |
| `=>` | **"such that"** | Now precisely: a **dictionary argument** the compiler supplies |
| `<$>` | **"fmap"** | Infix `fmap`. `(+1) <$> Just 2` |
| `<>` | **"mappend"** / "combine" | `Semigroup`. Associative **by law**, unchecked |
| `mempty` | **"mempty"** | `Monoid`'s identity. **Dispatches on the return type** |
| `{-# MINIMAL … #-}` | — | Which methods an instance must define. `\|` is or, `,` is and |
| `{-# SPECIALISE f :: T #-}` | **"specialise"** | Emit a dedicated copy for one type. Worth 30% here |
| `{-# LANGUAGE InstanceSigs #-}` | — | Lets you repeat a method's signature inside the instance |

**Functions and types new this week:** `fmap` · `foldMap` · `mconcat` · `mempty` · `stimes` · `toList` ·
`Semigroup` · `Monoid` · `Functor` · `Foldable` · `Traversable` *(named only)* · `Sum` · `Product` ·
`Max` · `Min` · `maximumBy` · `comparing` · `Complex`.

> **`<>` and `<$>` are the two you will read most**, and both are new. `<>` is `Semigroup`'s combine —
> `++` for lists, `max` for `Max`, your own for `Stats`. `<$>` is `fmap`. Neither is special syntax; both
> are ordinary operators defined in a library.

---

### This Week's Materials

| File | Purpose |
| --- | --- |
| [[L09 Type Classes and What a Constrained Type Promises]] | Classes, instances, defaults, superclasses; **`=>` as a dictionary, measured at 30% and 40×**; `Num` and `:t 3`; laws the compiler ignores; **why a class is not an interface**, and coherence |
| [[L10 Functor Foldable and the Laws]] | `fmap` and `<$>`; **the two laws, and the swapping `Pair` that compiles and breaks both**; `Foldable` from one method; **`length ('x', 5) == 1`** and the rest; `foldMap`; `traverse` named; when not to generalise |
| [[LAB 4 Writing a Class and Four Instances]] | A class of your own, four instances, ten law checks — **and a broken `mempty` that all ten miss**. **Wednesday of Week 5** |
| `lab/Classes.hs`, `Sched.hs`, `Main.hs`, `Makefile`, `expected.txt` | Four TODOs, a law harness, and `make check` / `make laws` |
| [[PROG202 Week4/assignments/PROJECT 1 An Interpreter for sq\|PROJECT 1]] | **Assigned Wednesday, due Friday of Week 7, 15%.** One file, 27 tests, three phases, a four-page report |
| `assignments/project1/` | The complete handout: `Syntax.hs`, `Value.hs`, `Tests.hs`, `Main.hs`, `Makefile`, and the `Eval.hs` skeleton |
| [[PROG202 Week4/assignments/Problem Set 4\|Problem Set 4]] | Fifteen parts, 100 points, due **Friday of Week 5**. **Q5 is Project 1 Phase 1** |
| [[PROG202 Week4/assignments/QUIZ 4 Week 4 Tuesday\|QUIZ 4]] | Ten minutes, Tuesday, covers **Week 3** |
| [[PROG202 Week4/resources/Reading Guide Week 4\|Reading Guide Week 4]] | Hutton 3.7–3.9, 8.5, 12.1, 14 — **and why to stop at the end of §12.1** |
| `resources/spec.hs`, `dict.hs`, `foldable.hs` | The 30%/40× measurement, and every `Foldable` trap in one file |
| `solutions_instructor/` | Instructor only — includes Project 1's reference `Eval.hs`, **which is not to be circulated** |

---

### The One Thing to Take From This Week

**An instance's contract is a set of laws, and nothing in the toolchain checks them.**

`-Wall` catches a missing case. The type checker catches a wrong type. **Neither catches a `Functor`
instance that swaps its subtrees** — that compiles silently and quietly breaks every piece of generic code
that assumed `fmap id == id`.

And the way you find out is worse than you expect. In Lab 4 you will set

```haskell
mempty = Stats 0 0 999          -- plainly not an identity for max
```

and **all ten law checks still print `ok`**, because the value they check against is built with `foldMap`,
`foldMap` seeds with `mempty`, and **the broken `mempty` contaminated its own test data.** The failure is
visible only because the driver happens to print `mempty` on its own line.

**A test written in terms of the thing it is testing cannot see the thing it is testing.** That sentence is
this week's real content, it is why `Semigroup` is split from `Monoid` in the first place, and it is the
entire premise of **Week 11**.

---

### Assessment Reminder

**Labs and quizzes carry no weight.** They are still required; a second unexcused lab absence costs a
letter grade. **Quiz *N* covers Week *N−1***, ten minutes at the start of **Tuesday's** lecture.

> **Lab 3 is sat this Wednesday** and covers Week 3. Lab 4 — this week's — is sat on the **Wednesday of
> Week 5**.
>
> **Project 1 is assigned this Wednesday and is 15% of the course.** Phases 1 and 2 use only material the
> **midterm** also covers, so doing them before the Week 6 paper is revision rather than a competing
> demand. **Spring Break is after the deadline, not before it.**
>
> **The midterm is Thursday of Week 6, 18:00–19:15, and covers Weeks 0–5.** Next week is the last week it
> covers.

Both are tracked in [[_PROG 202 Lab and Quiz Record]].

---

### Connections

**Back:** **this week explains `=>`, which has been in every `:t` output since Week 0.** Week 1's
`deriving` is now something you can write by hand; Week 1's `newtype` is what `Sum` and `Product` are made
of; Week 2's `foldr` turns out to be a class method, which is why its real type says `Foldable t =>`; and
**Week 1's `mkSession` is what makes Lab 4's `mempty = Stats 0 0 0` lawful** — an invariant established
three weeks earlier paying for a law today.

**Sideways:** **CS 212's "programming to an interface"** is L09 §5 from the other side, and the four
differences are worth taking to that course. **CS 211 last term** wrote the type checker that makes
constraints resolvable at all.

**Forward:** **Week 5 is monads**, and you have already written one — `Either Err Value` in Project 1, and
the `filterM` you had to write by hand for `Filter`. **Week 6's `Applicative` is what `traverse` needs**,
which is Lab 1's `traverse id` finally explained. **Week 7 needs `foldMap`'s associativity** to reduce a
tree in parallel. And **Week 11 is this week's last paragraph**, with a generator attached.

---

*PROG 202 · Week 4 · © CSE Department*
