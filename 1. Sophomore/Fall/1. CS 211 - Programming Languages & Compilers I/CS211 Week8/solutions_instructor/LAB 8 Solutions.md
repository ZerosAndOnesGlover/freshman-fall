# CS 211 · Lab 8 — Solutions
## Instructor Only

**Do not distribute.** All counts verified against the Week 8 lab code on Python 3.14.2.

---

## Running the Lab

**Budget:** A 25, B 20, C 25, D 30 = 100 minutes against 110. **Part D is the one to protect** — it is the week's idea and it is the one students remember for years. If the room is behind at 15:10, cut Q4 and Q10.

**This is the Friday after Midterm 2.** Expect a flat room. Two things help: say at the start that none of this was on the exam, and lead with Q5, which is a genuine surprise and wakes people up.

**Three predictable stalls.**

**Q3 confuses people** because they read "does not typecheck" as "is broken". It is not broken; it computes conjunction correctly on all four inputs. Have them run the four cases before discussing.

**Q7 needs the two prior examples supplied** if nobody finds them. Week 5: liveness is a *may* analysis and dominance a *must*, because exactness is unavailable. Week 6: reference counting is sound and cannot see cycles.

**Q15 is where the lab lands.** Give it room. The intended realisation is that "a proof of `A ∨ ¬A`" is a *program that decides*, and there is nothing to decide with.

---

## Part A — What Inference Says About Week 7

**Q1.** **39 typeable, 16 rejected.** Every rejection is the **occurs check**, which refuses to construct an **infinite type** — one that would have to contain itself, like `a = a → b`.

**Q2.** The two prior appearances:

- **Week 3**, `hm.py`: `\x -> x x` is rejected, in the "errors" section of that file's output.
- **Week 6**, `cyc_array.cy`: `r[0] = r` cannot typecheck because it would need `T = [T]`. L13 §9 called it "an infinite type, which Cyan's grammar has no way to write down".

**What they share:** both are the type system declining to build a type that contains itself, and in both cases the *consequence* was that a term you wanted became unwritable. In Week 6 that unwritability was what made reference counting complete for Cyan.

*A student who connects those two is having the intended experience of the whole course. Say so.*

**Q3.** `and = λp q. p q p` applies `p` to `q` **and to `p` itself**. So `p`'s type must be `α → β → γ` where its second argument is `p`, forcing `β = typeof(p) = α → β → γ`. The occurs check fires.

All four cases evaluate correctly:

```
  and true  true  = True
  and true  false = 0 (numeral) or False (boolean)
  and false true  = false
  and false false = false
```

**Reconciliation:** *typeability and correctness are different properties.* HM is **sound and incomplete** — it rejects some programs that would have run fine, and `and` is one of them. The definition computes conjunction on every input and is also an instance of a construction the type system must refuse in general.

*Push back on "so the type system is wrong". It is not wrong; it is conservative, and Q7 names the property.*

**Q4.** `two : ∀d. (d → d) → d → d` — three tokens and exactly right. `pred`'s type has **fourteen** quantified variables and says nothing about predecessors.

**Why:** HM infers the **principal type**, which is a function of the term and nothing else. `two` *is* structurally "apply f twice", so its principal type says so. `pred` is Kleene's pair-shuffling construction, so its principal type describes **pair-shuffling plumbing** — because that is all the term contains. The meaning "predecessor" lived in `prelude.lam`'s comments and in our heads, and inference cannot read either.

**Q5.**

```
  zero  : forall a b. a -> b -> b
  false : forall a b. a -> b -> b
  nil   : forall a b. a -> b -> b
```

**Types did not separate them**, because a principal type is computed **from the term**, and they are the same term. Nothing was added.

The three theorems are not separated either — `const`/`true` both `∀a b. a → b → a`, `apply`/`one` both `∀b c. (b → c) → b → c`, `compose`/`mult` both `∀d e c. (d → e) → (c → d) → c → e`.

**The word is *declaration*.** `data Bool = True | False` adds information the term never contained: a **nominal** distinction, grounded in a name a programmer chose rather than in structure.

*This is the lab's first surprise and it contradicts what Week 7's README predicted — deliberately. If a student points out the contradiction, tell them they are right and that the Week 7 files were corrected.*

---

## Part B — `let` Is Not Sugar

**Q6.**

| term | normal form | type |
|---|---|---|
| `let i = \x. x in pair (i one) (i true)` | `λf. f (λf x. f x) (λt f. t)` | typeable |
| `(\i. pair (i one) (i true)) (\x. x)` | **the same** | **TYPE ERROR** (occurs) |
| `let i = \x. x in i i` | `λx. x` | `∀c. c → c` |
| `(\i. i i) (\x. x)` | **`λx. x`** | **TYPE ERROR** (occurs) |

**Q7.** The shared normal form of rows 3 and 4 is **`λx. x`**, the identity.

The property is that a type system is **sound and incomplete**: incomplete *with respect to the set of programs that would have run without error*. It rejects some of them, always erring in the safe direction.

Prior appearances:

- **Week 5:** liveness is a *may* analysis, dominance a *must*. Neither is exact, because exactness is undecidable — so each approximates in the direction that cannot cause a wrong answer.
- **Week 6:** reference counting is sound and incomplete — a count of zero proves unreachability, a positive count proves nothing, and cycles are the gap.

*Accept Week 4's constant folder only if the student argues it well; the folder's bug was unsoundness, not conservatism, so it is the opposite case and worth saying so.*

**Q8.** The differing expression is **`generalise(env, tv)`** against **`Scheme([], tv)`**.

`generalise` quantifies every type variable free in the inferred type but **not** free in the environment, producing `∀…. τ` so that each use may instantiate it freshly.

**Why a lambda-bound name cannot be generalised:** its type is not yet known — it is determined by the **caller**, at the application site, and inference has not reached that site. Generalising it would amount to promising that the function works for *every* instantiation of the parameter, which is a rank-2 claim the caller has not made. `(λi. i i) (λx. x)` is exactly that: the body needs `i` at two types, but `i`'s type is fixed by whatever gets applied.

---

## Part C — Type Classes

**Q9.** A class is a **record type**. An instance is a **value** of that record. A constraint is a **parameter**.

The `=>` became a `->`: `member : Eq a => a -> List a -> Bool` elaborates to `member : DictEq a -> a -> List a -> Bool`.

**Q10.** The dictionary came from the **compiler**, which built it by recursion over the type structure.

The instance that compiled to a function is `instance (Eq a) => Eq (List a)` — it has a **context**, so it needs a dictionary for `a` before it can produce one for `List a`:

```
dEq_ListA dEq_a = { eq = eqList dEq_a }
```

This happened **at compile time**, before the program ran. There is no run-time search.

**Q11.** All three fail at **elaboration** — while resolving constraints, before any code executes.

In a dynamically typed language the equivalent program starts, runs, and fails at the moment the method is called, possibly on a rare path, possibly in production. **A missing instance is a type error here, not a method-not-found later.**

**Q12.** *(Discussion.)* Points to draw out:

- **The dictionary can be erased** because it is selected by the *static type*, which the compiler knows. A vtable cannot, because the choice depends on a value only available at run time.
- `impl Trait` is static (monomorphised, direct call, zero cost, code bloat); `dyn Trait` is dynamic (vtable beside the data, one indirect call).
- CS 201 **Week 5** (`L17 Branch Prediction and Out-of-Order Execution`) is the reference: a mispredicted branch costs **15–20 cycles**, and an indirect call the predictor cannot resolve is the hard case. That is why this is a performance decision, and why Rust makes you type `dyn` to opt into it.

---

## Part D — Proofs Are Programs

**Q13.**

| proposition | proof term | the function |
|---|---|---|
| `A → A` | `λp0. p0` | **the identity** |
| `A → B → A` | `λp0. λp1. p0` | **`const`** — which Week 7 found is the same term as `true` |
| `(A → B → C) → (A → B) → A → C` | `λp0. λp1. λp2. ((p0 p2) (p1 p2))` | **the S combinator** |

*The `const`/`true` recognition is the one to fish for. It closes a loop opened two weeks earlier.*

**Q14.** Curry-Howard claims that **a proposition is a type and a proof of it is a term of that type** — and it is an **identity**, not an analogy. The two systems are the same structure, arrived at independently by logicians and by computer scientists.

**Q15.** A proof of `A ∨ ¬A` must be a **value of type `Either A (A → Void)`** — a tagged value carrying either a proof of `A` or a function turning any proof of `A` into a contradiction.

To produce it, the program must **decide which tag to use**, for an arbitrary unknown `A`, with nothing to inspect. It cannot. Classical logic asserts "A is true or it is not" without saying which; constructive logic demands the witness.

**Why the decision procedure matters:** "not provable" here is a *result*, not a timeout. Week 7's `Diverged` was scrupulous about the opposite case — it said explicitly that stopping proved nothing, because normalisation is undecidable. Intuitionistic **propositional** logic *is* decidable, so LJT can make the stronger claim, and the difference between the two situations is exactly what students should take away.

**Q16.** `lem` appears as a **free variable** of every proof that uses it — an **assumption**, not a construction. The proof term is no longer closed, so it is not a program you can run; it is a program with a hole where a value should be.

That is what classical logic adds, and it is why a classical proof need not be a program.

*The advanced follow-up, if someone asks: the computational content of LEM is `call/cc` (Griffin 1990), so classical proofs correspond to programs with first-class continuations.*

**Q17.** All three are provable:

```
(A → B) → (B → C) → (A → C)   λp0. λp1. λp2. (p1 (p0 p2))
(A ∧ B → C) → (A → B → C)     λp0. λp1. λp2. (p0 (p1, p2))
¬¬(A ∨ ¬A)                    λp0. (λp2. (p0 inr p2) λp1. (p0 inl p1))
```

**The third is the point of the question.** Excluded middle is **not** provable and its **double negation is** — a genuinely surprising result that most students predict wrongly.

The intuition: you cannot produce `A ∨ ¬A`, but you *can* refute anyone who claims to refute it. Given `k : (A ∨ ¬A) → ⊥`, hand it `inr (λa. k (inl a))` — if someone later supplies an `a`, use `k` again on the other branch. The proof term beta-reduces to the standard `λk. k (inr (λa. k (inl a)))`.

**This is Glivenko's theorem in miniature**: every classical propositional tautology is intuitionistically provable *under a double negation*. Worth stating if the room is engaged.

---

## If You Finish Early

**Q18.** Reverting `app(t, sub)` to `app(t, lam(y, sub))` changes the **proof terms** and does **not** change the provable/not-provable split. With the checker wired in, the affected rows print `ILL-TYPED`; without it, everything still reported `ok`.

**That is the lesson:** testing *provability* passes while the proofs are wrong. It is the same failure as Week 5's printer, Week 6's peak-RSS benchmark and Week 7's `0 == False` — **the instrument agreed with the bug.** This defect was in the shipped file and was found by reading one proof term and noticing its arity.

**Q19.** `¬¬(A ∨ ¬A)`'s proof is a beta-redex; reducing gives `λk. k (inr (λa. k (inl a)))`.

**Proof simplification is beta-reduction** — *cut elimination*, on the logic side. Normalising a proof removes the detours (lemmas proved and immediately used), and under Curry-Howard that is exactly evaluating the program. Week 7 spent a fortnight on the same operation without calling it that.

**Q20.** Adding `Show Bool` resolves. Adding a second `Eq [Int]` alongside `Eq a => Eq [a]` makes resolution **ambiguous**, and `classes.py` picks whichever appears first in the list — which is *not* defensible behaviour.

Haskell rejects overlapping instances by default; `OverlappingInstances` (now per-instance pragmas) exists because rejection is sometimes too strict, and is widely regarded as a design mistake, because instance selection stops being predictable from the type alone.

**Accept any view, argued.** The question is whether "most specific wins" is a rule you can reason about locally, and the honest answer is that it usually is not.

---

*CS 211 · Week 8 · Lab 8 Solutions · © CSE Department*
