# CS 211 · Programming Languages & Compilers I
## Week 8: Type Systems in Depth — Polymorphism and Generics

**Credits:** 4 (3 lecture + 1 lab) · **Prerequisites:** CS 101, CS 102, MATH 151
**Assessment for this course (overall):** Problem Sets 30%, Projects 25%, Midterms 25%, Final 20%
**This week's deliverables:** **MIDTERM 2** (Tuesday evening), Lab 8, PS 8, and Quiz 8 (Tuesday, covers Week 7).

> **MIDTERM 2 · Tuesday 28 October, 20:00–21:15 · 75 marks · 12.5% of the course grade · covers
> Weeks 4–7.** Nothing from this week is on it. [[CS211 Week8/resources/MIDTERM 2 Revision Guide|MIDTERM 2 Revision Guide]] is the
> place to start.

---

### Why This Week Exists

Because Week 7 ended with three terms that were the same term, and the obvious remedy is a type system.

So apply one. Week 3 already wrote the algorithm — unification, the occurs check, `generalise`. `infer.py` is that engine with **one thing changed: it runs on `prelude.lam` instead of six hand-written expressions.**

Sixteen of the fifty-five definitions are rejected, and every single rejection is the occurs check. Two of them are `and` and `or`, which nobody expected, because Church conjunction turns out to be self-application in disguise.

And then the result the week is built on: **the collision survives.** `zero`, `false` and `nil` all infer to `∀a b. a → b → b`, because a principal type is computed from the term and they *are* the same term. Inference separates nothing.

**What separates them is a declaration.** That is the week.

---

### Learning Objectives

By the end of Week 8, you should be able to:

1. Run inference over real terms and explain why the **occurs check** is behind every rejection.
2. Connect that check to **Week 3's `x x`** and to **Week 6's uninstantiable array type**.
3. Explain why a term can compute the right answer on every input and still fail to typecheck.
4. Distinguish **inferred** from **declared**, and say what a nominal declaration adds that a term does not contain.
5. Distinguish **parametric**, **ad-hoc** and **subtype** polymorphism, and give each one's compilation strategy.
6. Explain why **`let` is not sugar**: identical normal forms, different typeability.
7. Use *sound*, *complete*, *conservative* and *unsound* correctly about a type system.
8. Define **rank**, and state what is decidable at rank 1, 2 and 3.
9. Explain why a **total language cannot have `Y`**, and what each language family does instead.
10. Derive **theorems for free** from a polymorphic type.
11. Elaborate **type classes** to dictionary passing, and say why a dictionary can be erased and a vtable cannot.
12. Read a type as a proposition and a term as a **proof**, and explain why excluded middle has none.

---

### This Week's Materials

| File | Purpose |
| --- | --- |
| [[CS211 Week8/assignments/MIDTERM 2\|MIDTERM 2]] | **The paper.** 75 marks, Weeks 4–7 |
| [[CS211 Week8/resources/MIDTERM 2 Revision Guide\|MIDTERM 2 Revision Guide]] | What to revise, in priority order, and what is not on it |
| [[L17 What Types Fix and What They Do Not]] | Inference over the prelude, the occurs check, **the collision that survives**, three polymorphisms, `let`, rank |
| [[L18 System F Dictionaries and Proofs as Programs]] | System F, strong normalisation, parametricity, **dictionary passing**, higher kinds, **Curry-Howard** |
| [[PS 8 Type Classes in a Mini-Language]] | Constraint collection, resolution, elaboration — and a guard whose removal is *unsound* |
| [[QUIZ 8 Week 8 Tuesday]] | **Covers Week 7.** Sat the morning of the midterm, deliberately |
| [[LAB 8 Proofs Are Programs]] | What inference says about Week 7, then `let`, then proofs |
| `lab/infer.py` | **Week 3's engine, new input.** Types all 55 definitions |
| `lab/classes.py` | A class is a record; an instance is a value; a constraint is a parameter |
| `lab/curry.py` | Dyckhoff's LJT — a **decision** procedure — printing the proofs it finds, **and type-checking them** |
| `lab/lam.py` | Week 7's interpreter. **Changed this week:** `let` is new — sugar for evaluation, not for typing |
| `lab/prelude.lam` · `church.py` | Carried forward from Week 7, unchanged |
| [[CS211 Week8/resources/Reading Guide Week 8\|Reading Guide Week 8]] | TAPL ch. 9, 22, 23 · Wadler & Blott 1989 · Wadler 2015 |
| `solutions_instructor/` | Instructor only |

---

### The One Thing to Take From This Week

**Types did not fix Week 7's collision.**

```
$ python3 infer.py
  zero  : forall a b. a -> b -> b
  false : forall a b. a -> b -> b
  nil   : forall a b. a -> b -> b
  still the same term: True
```

Week 7 predicted a type system would separate them. **It does not**, and neither does it separate the three "theorems" — `const`/`true`, `apply`/`one`, `compose`/`mult` all share their types too. A principal type is computed *from the term*, and inference adds no information the term did not already carry.

What separates them is `data Bool = True | False` — a **nominal** distinction, grounded in a name a person chose.

> **The useful axis is not typed against untyped. It is inferred against declared.** Inference
> reports what a term already means; a declaration adds what it does not. That is why every
> practical language makes you write `data`, `struct`, `enum` or `class` — and why Church
> encodings are a proof of expressiveness rather than a way to write programs.

*Week 6 met the same idea from the other end: `Ref` was a distinct class, so the collector never had to guess whether a word was a pointer. That was a nominal decision too, and it bought precise collection.*

---

### Assessment Reminder

**Labs and quizzes carry no weight**, and both are required. **Quiz 8 is sat Tuesday morning and covers Week 7 — the same material as a quarter of the midterm that evening.** That placement is deliberate: mark it against the key and you have a revision list with eight hours left.

**Midterm 2 is Tuesday 28 October, 20:00–21:15**, and is a **weighted component** recorded in [[CS 211]]. Lab 8 is Friday and covers this week.

**PS 8 is released Wednesday and due Friday of Week 9.** **Project 1 is due Week 11** — by now you should be through the Week 8 milestone: lexer and parser done, AST dumps correct, grammar argument written.

---

### Connections

**Back:** **Week 3's inference engine, unchanged.** **The occurs check for the third time** — `x x` in Week 3, `T = [T]` in Week 6, sixteen definitions here. **Week 7's collision**, taken as the opening question and not resolved by the obvious remedy. **Week 5's `may`/`must` and Week 6's reference counting** are the same sound-and-incomplete shape that HM has.

**Sideways:** **CS 201 Week 5's `L17 Branch Prediction and Out-of-Order Execution`** puts a misprediction at 15–20 cycles, which is why a dictionary that can be erased and a vtable that cannot are a performance distinction rather than a stylistic one.

**Forward:** **Week 9 asks a question none of Weeks 4–8 has had to** — what a program *means* when two of them run at once — and the answer needs a memory model rather than a type system. **Week 11's mini-compiler** needs the elaboration idea from L18 §4 if your Project 1 feature has constraints. **Project 1's `null`/option-type option** is L17 §4's nominal-declaration argument, in your own compiler.

---

*CS 211 · Week 8 · © CSE Department*
