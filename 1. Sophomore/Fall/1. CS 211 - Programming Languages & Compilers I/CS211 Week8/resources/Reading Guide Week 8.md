# CS 211 · Reading Guide · Week 8
## Type Systems in Depth: Polymorphism and Generics

**This week has a scheduling problem before it has a reading problem.** Midterm 2 is on Tuesday evening and covers Weeks 4–7. **Do not read ahead for Week 8 before the exam.** The revision guide in this folder is what Monday and Tuesday are for; come back here on Wednesday.

What follows assumes you start reading on Wednesday and have until the following week.

---

## Before Tuesday (L17 — inference, and what it does not fix)

**Twenty minutes, and only if the exam revision is done.**

| Source | Section | Why | Pages |
|---|---|---|---|
| **Pierce, TAPL** | **ch. 8** | Typed arithmetic: safety = progress + preservation. The two theorems named. | 6 |
| **Pierce, TAPL** | **ch. 9.1–9.3** | The simply-typed lambda calculus. **§9.3's typing rules are `infer.py`'s three cases.** | 8 |

**Skip entirely until after the exam:** ch. 22 on reconstruction. It is Thursday's material and it is long.

---

## Before Thursday (L18 — System F, classes, Curry-Howard)

| Source | Section | Why | Pages |
|---|---|---|---|
| **Pierce, TAPL** | **ch. 22** | Type reconstruction and let-polymorphism. **§22.7 is exactly the `let`/`λ` distinction L17 §6 measures.** | 14 |
| **Pierce, TAPL** | **ch. 23.1–23.4** | System F. Read §23.3 for the encodings — Church numerals return, now typed. | 12 |
| **Wadler & Blott (1989)** | **all** | "How to make ad-hoc polymorphism less ad hoc." The paper that invented type classes, twelve pages, and `classes.py` is its §2. | 12 |
| **Wadler (2015)** | **all** | "Propositions as Types." *CACM.* **If you read one thing this week, this.** No prerequisites, and it is the best account of L18 §7 in print. | 9 |

---

## Papers, If You Want Them

- **Hindley (1969)** and **Milner (1978)** — the two independent discoveries of the algorithm you ran in Week 3. Milner's is the readable one.
- **Girard (1972)** and **Reynolds (1974)** — System F, twice, independently, in different fields. Reynolds' presentation is the one to try.
- **Wells (1994)** — type inference for System F is undecidable. Read the statement of the theorem and stop.
- **Wadler (1989), "Theorems for Free!"** — parametricity, with worked examples. Short and delightful.
- **Griffin (1990)** — classical logic corresponds to `call/cc`. Read it after L18 §8 lands, not before.
- **Dyckhoff (1992)** — the contraction-free calculus `curry.py` implements. Read it if you want to know why the prover terminates.

---

## Documentation

- **GHC User's Guide, `RankNTypes`** — the annotation requirement, and why it exists. Two pages, and L17 §7 is the reason.
- **The Rust Book, ch. 10 and 17.2** — `impl Trait` against `dyn Trait`. Read them side by side with L18 §5.
- **`agda.readthedocs.io`, "Termination Checking"** — what a total language requires instead of `let rec`.

---

## The One Thing Worth Reading Twice

**TAPL §22.7, on `let`-polymorphism** — specifically the sentence explaining why generalisation happens at `let` and not at `λ`.

Then run:

```bash
python3 lam.py  --defs prelude.lam '(\i. i i) (\x. x)'
python3 infer.py '(\i. i i) (\x. x)'
```

The first prints `λx. x`. The second prints a type error.

The book explains the *rule*. It does not dwell on the consequence, which is that **a type system rejects working programs and this is not a defect** — it is the price of deciding, before the program runs, a question that is undecidable in general. Noticing that the rejected term is the identity function is the difference between having read §22.7 and having understood it.

---

## A Note on What This Week Is Really About

The syllabus calls this week "Type Systems in Depth", which suggests it is about mechanism — generics, variance, kinds, the machinery of `<T>`.

It is not. **It is about what declarations buy that inference cannot.**

Week 7 ended with three terms that were the same term and asked for a type system to separate them. Week 8 runs the type system and finds that it separates nothing — the collision survives, and so do the three "theorems". The thing that fixes it is `data Bool = True | False`: a **name**, chosen by a person, carried by the compiler as a nominal fact.

That reframing is worth more than any of the mechanism. Every argument you will have about static and dynamic typing is really an argument about how much you are willing to *declare* in exchange for how much the compiler will check — and inference, which looks like it should make declarations unnecessary, turns out to be the thing that cannot supply them.

**And then §7 of L18 goes somewhere else entirely.** A type is a proposition and a program is a proof, and the proof of `A → B → A` is a function you have known since Week 7 under a different name. That is not a metaphor and it is not decoration. It is why proof assistants are type checkers, and why a verified compiler is a typed program.

---

*CS 211 · Week 8 · Reading Guide · © CSE Department*
