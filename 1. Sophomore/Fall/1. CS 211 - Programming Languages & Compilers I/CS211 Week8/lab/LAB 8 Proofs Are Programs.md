# CS 211 · Lab 8
## Proofs Are Programs

**Friday of Week 8 · 14:00–15:50 · BH 220 · covers Week 8**
**Unmarked and mandatory.** The TA checks you off in the session. [[Year2 - Sophomore/COURSE POLICIES|COURSE POLICIES]] costs you a letter grade after a second unexcused absence.

**Bring:** a terminal. Everything is in this folder.

> **Midterm 2 was sat on Tuesday evening and covered Weeks 4–7.** Nothing in this lab is on it.
> Part D is the first material of the second half of the course.

---

## Setup

```bash
cd "CS211 Week8/lab"
python3 infer.py | head -5      # should report 55 definitions
python3 curry.py | head -6      # should report 12 provable
```

If either fails, get the TA now rather than at 15:30.

---

## Part A — What Inference Says About Week 7 (25 min)

**Q1.** Run `python3 infer.py` and record the split — how many typeable, how many rejected.

**Every rejection is the same error.** Name it, and say in one sentence what it refuses to construct.

**Q2.** You have met that check twice before, in two very different places. Find both.

- One is Week 3, and it is about a lambda term.
- One is **Week 6**, and it is not about lambda terms at all — it is about why a certain `.cy` file would not compile. *(Look at `cyc_array.cy`.)*

Write down what the two have in common, in one sentence.

**Q3.** Two rejections are surprising:

```
  and : occurs check: cannot construct the infinite type c = (b -> c
  or  : occurs check: cannot construct the infinite type a = a -> c
```

- Look up `and` in `prelude.lam`. Follow the applications and say **why** the check fires.
- Now check whether `and` is *correct*, by evaluating all four cases:
  ```bash
  for p in true false; do for q in true false; do
    python3 lam.py --defs prelude.lam --church "and $p $q"; done; done
  ```
- **It computes conjunction correctly and it does not typecheck.** Write one sentence reconciling those.

**Q4.** Compare two inferred types:

```bash
python3 infer.py 'two'
python3 infer.py 'pred'
```

- `two` gets the type a Church numeral should have. Count the quantified variables in `pred`'s.
- **Why does one come out clean and the other not?** Your answer should be about what HM infers, not about which is more complicated.

**Q5.** The question Week 7 left:

```bash
python3 infer.py 'zero'; python3 infer.py 'false'; python3 infer.py 'nil'
```

- Report all three.
- **Types did not separate them.** Say why not, in terms of what a principal type is computed from.
- Now check the three *theorems* — `const`/`true`, `apply`/`one`, `compose`/`mult`. Are those separated?
- **So what would separate any of them?** Name it. It is one word and it is not "types".

---

## Part B — `let` Is Not Sugar (20 min)

**Q6.** Fill this table by running both tools:

| term | normal form | inferred type |
|---|---|---|
| `let i = \x. x in pair (i one) (i true)` | | |
| `(\i. pair (i one) (i true)) (\x. x)` | | |
| `let i = \x. x in i i` | | |
| `(\i. i i) (\x. x)` | | |

```bash
python3 lam.py  --defs prelude.lam 'TERM'
python3 infer.py 'TERM'
```

**Q7.** Rows 3 and 4 have the **same normal form** and different fates.

- What is that normal form?
- `(\i. i i) (\x. x)` reduces to a completely harmless function and is rejected. **Name the property this demonstrates** — the word is *incomplete*, and you should be able to say what it is incomplete with respect to.
- You have seen the same shape twice before. Find one from **Week 5** and one from **Week 6**. *(Hint: one is about analyses that must approximate; one is about a collector that cannot see something.)*

**Q8.** Open `infer.py` and read the `Abs` case and the `Let` case together.

- Quote the one expression that differs.
- Say what `generalise` does, in one sentence.
- **Why can a lambda-bound name not be generalised?** Answer by saying what would go wrong — think about a function whose argument's type is determined by the *caller*.

---

## Part C — Type Classes (25 min)

**Q9.** Run `python3 classes.py` and read the first two sections.

- A class is a ______. An instance is a ______. A constraint is a ______.
- Fill those in from the output, then say what happened to the `=>` in `member : Eq a => a -> List a -> Bool`.

**Q10.** Look at the resolution trace:

```
  Eq List List Int
        Eq List Int  ->  instance Eq List a
          Eq Int  ->  instance Eq Int
      => (dEq_ListListInt (dEq_ListInt dEq_Int))
```

- **Nobody wrote an instance for lists of lists of Int.** Where did that dictionary come from?
- Which instance in `classes.py` compiled to a *function* rather than a constant, and why?
- At what point in the pipeline did this happen — before or after the program ran?

**Q11.** Break it:

```bash
python3 classes.py | tail -6
```

- Three lookups fail. **At what stage?**
- Explain in one sentence how this differs from a dynamically typed language, where the same program would fail when the method was called.

**Q12.** *(Discussion — do this one out loud with your neighbour.)*

A type class dictionary is chosen by the **static type**. A C++ vtable is chosen by the **run-time value**.

- Which one can the compiler erase, and why?
- Rust has `impl Trait` (static) and `dyn Trait` (dynamic). Which is which?
- CS 201 measured what an unpredicted indirect branch costs. Roughly what, and why does that make this a performance question rather than a style one?

---

## Part D — Proofs Are Programs (30 min)

**Q13.** Run `python3 curry.py` and read the first table.

Write down the proof terms for the first three propositions, and **name each function**. You have seen all three before this term — one in Week 7 twice over.

**Q14.** The first two proofs are the axioms **K** and **S** of combinatory logic, and they are also the axioms of implicational logic.

**Nobody arranged that.** Say, in one sentence, what the Curry-Howard correspondence claims — and say whether it is an analogy or an identity.

**Q15.** Now the second table. Five classical tautologies come back **not provable**.

- Take `A ∨ ¬A`. A proof of it would have to be a value of type `Either A (A → Void)`. **Say what such a program would have to do**, and why it cannot.
- `curry.py` uses a *decision procedure*, not a bounded search. **Why does that distinction matter** for the claim being made? *(Compare: Week 7's `Diverged` explicitly said it did not prove anything.)*

**Q16.** Assume the missing axiom:

```bash
python3 curry.py | tail -8
```

All five become provable. **Look at what `lem` is in those proof terms** — the last three lines of the output say it. Explain why a classical proof "need not be a program".

**Q17.** Prove these by hand first, then check with the tool. **Predict before you run.**

- `(A → B) → (B → C) → (A → C)`
- `(A ∧ B → C) → (A → B → C)`
- `¬¬(A ∨ ¬A)`

To check one:

```bash
python3 -c "
from curry import *
print(provable(imp(imp(A,B), imp(imp(B,C), imp(A,C)))))
"
```

**The third one is the interesting one.** Excluded middle is not provable; predict whether its *double negation* is, before you run it. Then explain the result either way.

---

## If You Finish Early

**Q18.** `curry.py` type-checks its own proofs — `check` is called on every term in the self-test. **Break the hard `→L` rule** (change `app(t, sub)` back to `app(t, lam(y, sub))`) and re-run. Which line of output changes, and which does *not*? Say what that tells you about testing provability against testing proofs.

**Q19.** Find a proposition that `curry.py` proves with a term containing a **beta-redex** — a proof that could be simplified. `¬¬(A ∨ ¬A)` is one. Reduce it by hand and compare with the standard proof `λk. k (inr (λa. k (inl a)))`. What does *proof simplification* correspond to, on the programs side?

**Q20.** Add `Show Bool` to `classes.py`'s instance table and re-run. Then add a *second* `Eq [Int]` instance alongside `Eq a => Eq [a]` and see what your resolver does. **Is picking one of them the right behaviour?** Form a view before looking up what Haskell does.

---

## Before You Leave

Show the TA:

1. Your Q1 split and the name of the single check behind every rejection.
2. Your Q5 answer — and the one word that separates `zero` from `false`.
3. Your Q7 answer: the shared normal form, and the property it demonstrates.
4. Your Q13 three proof terms, with the functions named.

---

*CS 211 · Week 8 · Lab 8 · © CSE Department*
