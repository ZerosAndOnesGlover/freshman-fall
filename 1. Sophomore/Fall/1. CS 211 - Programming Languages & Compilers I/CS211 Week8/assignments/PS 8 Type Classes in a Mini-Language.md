# CS 211 · Problem Set 8
## Type Classes in a Mini-Language

---

**Released:** Week 8, Wednesday · **Due:** Week 9, Friday 17:00
**100 points · counts toward the Problem Sets component (30% of the final grade)**

**Submit:** `infer.py`, `classes.py` and any new modules (runnable end to end), plus `ps8.md` (written answers, tables, traces). Written answers inside code comments will not be marked.

> **Midterm 2 was sat on the Tuesday of this week and does not cover Week 8.** Nothing in this
> problem set is on it.

Start from the Week 8 lab folder. `lam.py`, `infer.py`, `classes.py` and `curry.py` are given to you complete.

---

## Part A — Inference Over Real Terms (18 points)

**A1.** *(4)* Run `python3 infer.py` and record the split: how many of the 55 definitions are typeable, and how many are rejected?

- **Every rejection is the same check.** Name it, and state in one sentence what it refuses to build.
- You have met that check twice before this week. Name both occasions. *(One is Week 3. The other is not about lambda terms at all.)*

**A2.** *(5)* Two of the rejections are surprising: `and` and `or`.

- Write out `and = λp q. p q p` and explain, by following the application, why the occurs check fires.
- **Is `and` a correct definition of conjunction?** Verify by evaluating it on all four inputs with `lam.py`, and reconcile your answer with the fact that it does not typecheck.
- State, in one sentence, what this shows about the relationship between "computes the right answer" and "is well-typed".

**A3.** *(5)* Compare the inferred type of `two` with the inferred type of `pred`.

- Give both. How many quantified variables does each have?
- `two` gets exactly the type a Church numeral should have and `pred` does not get anything recognisable. **Explain why**, in terms of what HM infers and what the term actually contains.
- `zero` and `one` do **not** get `(a → a) → a → a` either. Give their types and explain the difference. Then explain why `add zero two` nevertheless typechecks.

**A4.** *(4)* Run:

```
$ python3 infer.py 'zero'
$ python3 infer.py 'false'
$ python3 infer.py 'nil'
```

- Report all three.
- Week 7 predicted that a type system would separate them. **It does not.** Explain why not, in terms of what a principal type is a function of.
- Name what *would* separate them, and say what information it adds that the term does not contain.

---

## Part B — Polymorphism and Rank (20 points)

**B1.** *(5)* `let` is new in Week 8's `lam.py`. Show that it is sugar for evaluation and not for typing:

| term | normal form | inferred type |
|---|---|---|
| `let i = \x. x in pair (i one) (i true)` | | |
| `(\i. pair (i one) (i true)) (\x. x)` | | |
| `let i = \x. x in i i` | | |
| `(\i. i i) (\x. x)` | | |

- Fill the table by running both tools.
- **`(\i. i i) (\x. x)` reduces to the identity function and is rejected.** State the property of type systems this demonstrates, using the word *incomplete* correctly.
- Name two other places this term you have seen the same shape — one from Week 5, one from Week 6.

**B2.** *(5)* Read `infer`'s `Let` case and its `Abs` case side by side.

- Quote the one line that differs in what goes into the environment, and explain what `generalise` does.
- `generalise` refuses to quantify any variable that is **free in the environment**. **Delete that guard** — quantify everything — and infer the type of

  ```
  \y. let f = \x. y in pair (f one) (f true)
  ```

  **The term typechecks either way. The two types are not the same.** Give both, and say precisely what the unguarded type claims that is false. *(Look at how many distinct variables appear where the pair's two components go, and ask what value actually sits in each.)*
- This is **unsoundness**, not incompleteness. Explain the difference in one sentence, using Week 5's vocabulary.

**B3.** *(4)* HM cannot infer the type `(∀a. a → a) → (Nat, Bool)`.

- Explain what *rank* means, and why that type is rank-2 while `∀a. a → a` is rank-1.
- State what is decidable at rank 1, at rank 2, and at rank 3 and above.
- Name a language feature you have used that requires an annotation for exactly this reason.

**B4.** *(6)* Parametricity.

- How many **total** functions have the type `∀a. a → a`? How many have `∀a. a → a → a`? Justify both counts by arguing about what such a function can possibly do.
- Week 7 gave the second pair names. What are they?
- A function has type `∀a. List a → List a`. Give two functions with that type and one plausible-sounding function that **cannot** have it, and say why the type forbids it.
- **Ad-hoc polymorphism loses this property.** Explain why in one sentence.

---

## Part C — Implement Type Classes (34 points)

`classes.py` demonstrates the target: a class is a record type, an instance is a value of it, a constrained function takes it as an argument. **It resolves instances but it does not infer anything.** Your job is to connect it to `infer.py` so that constraints come from inference rather than from a hand-written list.

**C1.** *(8)* **Collect constraints during inference.**

- Extend the type environment so a name may carry a *qualified* scheme: `forall a. Eq a => a -> a -> Bool`.
- When such a name is instantiated, record a constraint `(Eq, τ)` in a list rather than discarding it.
- Report the constraint set for at least four expressions, including one with two distinct constraints and one with a constraint on a type variable.

**C2.** *(8)* **Resolve them.**

- After inference, discharge each constraint against the instance table using `classes.resolve`.
- A constraint on a *concrete* type resolves to a dictionary expression. A constraint still on a *type variable* must instead be **deferred**: it becomes part of the inferred type. Show both cases.
- Report the qualified type your implementation infers for a function that uses `eq` on its argument. It should be `∀a. Eq a ⇒ a → List a → Bool` or equivalent.

**C3.** *(8)* **Elaborate.**

- Emit the dictionary-passing translation: constraints become leading parameters, and method uses become projections from the parameter.
- Show the elaborated form of at least three functions, one of which has two constraints.
- **Show a call site being given its dictionary**, including one where the dictionary is *built* by recursion — `(dEq_ListInt dEq_Int)` or deeper.

**C4.** *(6)* **Break it, deliberately, and report what happens and when.**

- Remove `instance Eq Bool` and use `eq` at `Bool`. What is reported, and **at what stage**?
- Add a **second, overlapping** instance — say `Eq [Int]` alongside `Eq a => Eq [a]`. What should happen? Say what your implementation does, whether that is right, and what Haskell does. *(Look up `OverlappingInstances` only after you have formed your own view.)*
- Make an instance context unsatisfiable — `instance Eq a => Eq (Tree a)` with no `Eq` for the element type in use — and report the error and the stage.

**C5.** *(4)* Superclasses. `Ord` declares `Eq` as a superclass.

- What must the `Ord` dictionary contain, and why?
- Show that a function with only an `Ord a` constraint can nevertheless call `eq`.
- Explain in one sentence why this makes the dictionary a **record with a field**, not merely a tuple of methods.

---

## Part D — Curry-Howard (16 points)

**D1.** *(5)* Run `python3 curry.py` and record both tables.

- For the first three provable propositions, give the proof term and **name the function it is** — you have seen all three before.
- Two of those are the axioms of a well-known system. Name it.

**D2.** *(5)* `A ∨ ¬A` is not provable.

- Explain why, in terms of what a proof of a disjunction has to *be*.
- `curry.py` uses a **decision procedure**, not a bounded search. Explain why that distinction matters for the claim being made.
- Show that it becomes provable when LEM is assumed, and say what `lem` is in the resulting proof term.

**D3.** *(6)* Give a proof term for each of these, or show it is not provable:

- `(A → B) → (B → C) → (A → C)`
- `(A ∧ B → C) → (A → B → C)`
- `(A → B → C) → (A ∧ B → C)`
- `¬¬(A ∨ ¬A)`
- `(A ∨ B) ∧ ¬A → B`

Check each against `curry.py` afterwards. **Where your hand answer and the tool disagree, say which is right and why** — the tool is not automatically correct, and one of these is worth thinking about before you run it.

---

## Part E — Written (12 points)

**E1.** *(6)* A total language cannot have `Y`.

- Explain why, connecting the occurs check to strong normalisation. Which is the mechanism and which is the reason?
- OCaml, Haskell and ML all have recursion. **How?** Answer in one sentence.
- Agda and Coq keep totality. What do they require instead, and what does it cost the programmer?
- Name one thing you can no longer do to programs once non-termination is expressible. *(Week 5 did it constantly.)*

**E2.** *(6)* A type class dictionary and a C++ vtable do the same job.

- State the one difference that matters, in terms of what selects the implementation.
- Explain why that difference lets one of them be erased at compile time and not the other.
- Rust has both `impl Trait` and `dyn Trait`. Map each onto your answer, and say what each costs.
- Connect this to CS 201: what does an indirect call cost that a direct call does not, and why?

---

## Reference Numbers

From the machine these notes were prepared on (Python 3.14.2). **Counts are deterministic.**

| Measurement | Value |
| --- | --- |
| `infer.py` over `prelude.lam` | **39 typeable, 16 rejected** |
| cause of every rejection | the **occurs check** |
| rejected, surprisingly | `and`, `or`, `eq`, `lt` |
| `zero` / `false` / `nil` | all `∀a b. a → b → b` |
| `const` / `true` | both `∀a b. a → b → a` |
| `compose` / `mult` | both `∀d e c. (d → e) → (c → d) → c → e` |
| `two` | `∀d. (d → d) → d → d` |
| `pred` | 14 quantified variables |
| `let i = \x. x in i i` | `∀c. c → c` |
| `(\i. i i) (\x. x)` | **TYPE ERROR**, reduces to `λx. x` |
| `curry.py` provable / not | **12 / 5** |
| proof of `A → A` | `λp0. p0` |
| proof of `A → B → A` | `λp0. λp1. p0` |
| `Eq [[Int]]` resolves to | `(dEq_ListListInt (dEq_ListInt dEq_Int))` |

---

## A Note on Part C4 and Part D3

Both ask you to reach a judgement rather than compute an answer.

C4's overlapping-instances question has no single right answer — Haskell's default is to reject, the extension exists because rejecting is sometimes too strict, and the extension is widely regarded as a mistake. **Say what your implementation does, what you think it should do, and why.** All three are needed.

D3 contains one proposition where a careful hand answer is likely to disagree with a first guess. **Work them out before running the tool.** A student who predicts, checks, finds a disagreement and explains it has done the question; a student who runs the tool first and transcribes has not, and it will be visible.

---

*CS 211 · Week 8 · Problem Set 8 · © CSE Department*
