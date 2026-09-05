# CS 211 · Problem Set 8 — Solutions and Mark Scheme
## Instructor Only

**Do not distribute.** All counts verified against the Week 8 lab code on Python 3.14.2.

---

## Part A — Inference Over Real Terms (18)

**A1.** *(4 — 1 the split, 1 the check, 2 the two prior occasions)*

**39 typeable, 16 rejected.** Every rejection is the **occurs check**, which refuses to construct an **infinite type** — one containing itself, `a = a → b`.

Prior occasions: **Week 3**, where `\x -> x x` was rejected by `hm.py`; and **Week 6**, where `cyc_array.cy` could not be written because a self-containing array needs `T = [T]`.

*The Week 6 one is the marked half. A student who finds only the Week 3 case gets 3 of 4.*

**A2.** *(5 — 2 the trace, 2 the evaluation, 1 the reconciliation)*

`and = λp q. p q p` applies `p` to `q` and then to `p`. So `p : α → β → γ` with its second argument being `p` itself, forcing `β = α → β → γ`. Occurs check.

All four cases are correct: `and true true` is true, the other three are false. *(Note the three falses decode as `0 (numeral) or False (boolean)` — the Week 7 collision, still present.)*

**The reconciliation:** typeability and correctness are different properties. HM is **sound and incomplete**; `and` is a correct definition that the type system must nonetheless refuse, because the refusal is a general rule and this term is an instance of the shape it rules out.

*Reject "the type checker has a bug". Accept "the type checker is conservative here" with reasoning.*

**A3.** *(5 — 1 the two types, 2 the explanation, 2 zero/one)*

`two : ∀d. (d → d) → d → d` — 1 quantified variable. `pred` — **14**.

**Why:** HM infers the **principal** type, a function of the term alone. `two` *is* "apply f twice" structurally, so its type says so. `pred` is Kleene's pair-shuffle, so its type describes pair-shuffling. The meaning "predecessor" was in the comments, and inference cannot read comments.

```
zero : ∀a b. a -> b -> b        (f is never applied, so nothing constrains it)
one  : ∀b c. (b -> c) -> b -> c (f applied once, so no domain = codomain constraint)
two  : ∀d. (d -> d) -> d -> d   (f applied to its own result, hence d -> d)
```

`add zero two` typechecks because `zero` and `one` have **more general** types than `two`; unification instantiates them down to `(o → o) → o → o`. **No conflict — the generality goes the helpful way.**

*Students frequently predict this will fail. Credit anyone who predicted failure, tested, and explained why they were wrong.*

**A4.** *(4 — 1 the three, 2 why not, 1 what would)*

All three: `∀a b. a → b → b`.

**Why not:** a principal type is computed **from the term**, and the three are the same term. Adding inference adds no information.

**What would:** a **declaration** — `data Bool = True | False` — which introduces a **nominal** distinction grounded in a chosen name rather than in structure. It adds information the term never carried.

*Full marks require the word nominal or an unambiguous description of it. "You'd annotate them" is half — an annotation that is merely checked structurally does not separate them either.*

---

## Part B — Polymorphism and Rank (20)

**B1.** *(5 — 2 the table, 2 the property, 1 the two prior places)*

| term | normal form | type |
|---|---|---|
| `let i = \x. x in pair (i one) (i true)` | `λf. f (λf x. f x) (λt f. t)` | typeable |
| `(\i. pair (i one) (i true)) (\x. x)` | same | TYPE ERROR |
| `let i = \x. x in i i` | `λx. x` | `∀c. c → c` |
| `(\i. i i) (\x. x)` | `λx. x` | TYPE ERROR |

The property is **soundness with incompleteness** — incomplete *with respect to programs that would have run without error*.

Prior: **Week 5**'s *may*/*must* analyses; **Week 6**'s reference counting, sound and blind to cycles.

**B2.** *(5 — 2 the line, 1 generalise, 2 the construction)*

`generalise(env, tv)` against `Scheme([], tv)`. `generalise` quantifies variables free in the type but **not free in the environment**.

**What the guard prevents.** On

```
\y. let f = \x. y in pair (f one) (f true)
```

`f`'s type is `α → typeof(y)`, and `typeof(y)` is free in the environment.

| | inferred type |
|---|---|
| with the guard | `∀q g. q → (q → q → g) → g` |
| **without** the guard | `∀a m s g. a → (m → s → g) → g` |

**Both typecheck. The unguarded one is wrong.** With the guard, both components of the pair have type `q` — correctly, since both *are* `y`. Without it, they get **independent** types `m` and `s`, so the type promises a pair whose two slots may be used at unrelated types, when at run time both slots hold the same value. A caller could treat one as an `Int` and the other as a `Bool`.

**That is unsoundness**, and it is the opposite failure from B1's: incompleteness rejects programs that would have worked; unsoundness *accepts* a program and licenses a use that is not safe. Week 5's vocabulary exactly — and it is why `generalise` computes `env_vars` at all.

*The common wrong answer is that the term fails to typecheck without the guard. It does not, and a student who claims it does has not run it. Full marks require both types and a statement of what the second one falsely permits.*

**B3.** *(4 — 2 rank, 1 decidability, 1 the feature)*

**Rank** counts how deep to the *left of an arrow* a `∀` appears. `∀a. a → a` is rank-1 (prenex). `(∀a. a → a) → (Nat, Bool)` is rank-2 — the quantifier is inside the argument position.

Rank 1: inference decidable (HM). Rank 2: inference decidable but not implemented by HM; checking is straightforward given annotations. **Rank ≥ 3: inference undecidable** (Wells, 1999).

Features: GHC's `RankNTypes`, `runST`'s type, or Java/C# generic methods requiring explicit type parameters in some positions. *(Accept any where an annotation is required for this reason.)*

**B4.** *(6 — 2 the counts, 1 the names, 2 the list functions, 1 ad-hoc)*

**`∀a. a → a`: exactly one** total function — the identity. The term receives a value of a type it knows nothing about, so it cannot construct a new one, cannot inspect it, and can only return what it was given.

**`∀a. a → a → a`: exactly two** — return the first or return the second. Those are Week 7's **`true` and `false`** (equally `const` and `flip const`).

`∀a. List a → List a`: `reverse`, `tail`, `id`, `take 3` all have it. **`map (+1)` cannot** — it would have to know `a` is numeric, and the type says the function knows nothing about `a`.

**Ad-hoc polymorphism loses this** because the code *does* branch on the type, so the type no longer constrains what the code can do.

---

## Part C — Implement Type Classes (34)

This is the implementation part and the bulk of the marks. **Mark the behaviour, not the architecture** — several designs work.

**C1.** *(8 — 4 qualified schemes, 4 the reported constraint sets)*

Environment entries carry `(qs, constraints, type)`. On `instantiate`, the constraints are substituted along with the type variables and appended to a collector.

Required: four expressions, including one with two distinct constraints (`(Eq a, Show a) ⇒ …`) and one with a constraint still on a type variable.

*Deduct if constraints are discarded when the head is already concrete — they must still be collected and then discharged in C2, or C4's error timing cannot work.*

**C2.** *(8 — 4 concrete resolution, 4 deferral)*

Concrete: `Eq Int` → `dEq_Int`. Deferred: a constraint on a type variable that the enclosing binding generalises becomes part of the type — `∀a. Eq a ⇒ a → List a → Bool`.

**The deferral half is the one students miss.** A submission that resolves only concrete constraints and errors on variables has implemented half the system, and cannot type `member` at all. Cap at 4 if so.

**C3.** *(8 — 4 elaboration, 2 three functions, 2 the recursive dictionary)*

```
member : DictEq a -> a -> List a -> Bool
member dEq_a x xs = ... (eq dEq_a) x y

call: member 3 [1,2,3]        ->  member dEq_Int 3 [1,2,3]
call: member [1] [[1],[2]]    ->  member (dEq_ListInt dEq_Int) [1] [[1],[2]]
```

**The recursive case is required for full marks.** `(dEq_ListListInt (dEq_ListInt dEq_Int))` demonstrates the compiler *building* a dictionary nobody wrote.

**C4.** *(6 — 2 missing instance, 2 overlap, 2 unsatisfiable context)*

- Missing `Eq Bool`: reported **at elaboration**, before execution. Full marks require naming the stage.
- **Overlap:** `classes.py` as shipped picks whichever instance appears first, which is **not** defensible. Haskell rejects overlap by default; `OverlappingInstances`/per-instance pragmas exist because rejection is sometimes too strict, and the extension is widely regarded as a mistake because instance selection stops being predictable from the type alone. **Accept any argued position**; require that the student says what their implementation does *and* what it should do.
- Unsatisfiable context: reported at elaboration, at the point the recursive resolution fails. The error should name the *inner* constraint (`Eq Tree`), not just the outer one.

**C5.** *(4 — 2 the content, 1 the demonstration, 1 the record point)*

The `Ord` dictionary must contain **the `Eq` dictionary as a field** (`superEq`), because a function with only `Ord a` in scope may still call `eq`, and the only thing it has is the `Ord` dictionary.

Demonstration: elaborate a function with signature `Ord a ⇒ …` that calls `eq`, and show the projection `eq (superEq dOrd_a)`.

**Why a record and not a tuple of methods:** the superclass field is not a method — it is a whole nested dictionary — so the dictionary is a heterogeneous structure with named fields, and superclass access is a projection rather than a lookup.

---

## Part D — Curry-Howard (16)

**D1.** *(5 — 3 the terms, 2 the naming)*

| proposition | term | function |
|---|---|---|
| `A → A` | `λp0. p0` | identity |
| `A → B → A` | `λp0. λp1. p0` | `const` — Week 7's `true` |
| `(A→B→C)→(A→B)→A→C` | `λp0. λp1. λp2. ((p0 p2) (p1 p2))` | the **S** combinator |

The system is **combinatory logic** — these are its axioms **K** and **S**, and they are also the axioms of implicational propositional logic.

**D2.** *(5 — 2 why not, 2 the decision procedure, 1 lem)*

A proof of `A ∨ ¬A` must be a **value of type `Either A (A → Void)`** — it must *decide*, for arbitrary unknown `A`, which tag to produce, with nothing to inspect. It cannot.

**Decision procedure vs search:** "not provable" is a **result**, not a timeout. Contrast Week 7's `Diverged`, which stated explicitly that stopping proved nothing because normalisation is undecidable. Intuitionistic *propositional* logic is decidable, so the stronger claim is available here and only here.

With LEM assumed, `lem` is a **free variable** of the resulting proof term: an assumption, not a construction. The term is no longer closed, so it is not a runnable program.

**D3.** *(6 — 1 each, 1 for the reconciliation)*

**All five are provable.**

```
(A → B) → (B → C) → (A → C)   λp0. λp1. λp2. (p1 (p0 p2))
(A ∧ B → C) → (A → B → C)     λp0. λp1. λp2. (p0 (p1, p2))
(A → B → C) → (A ∧ B → C)     λp0. λp1. ((p0 fst p1) snd p1)
¬¬(A ∨ ¬A)                    λp0. (λp2. (p0 inr p2) λp1. (p0 inl p1))
(A ∨ B) ∧ ¬A → B              λp0. case fst p0 of inl p1 → absurd (snd p0 p1); inr p2 → p2
```

**`¬¬(A ∨ ¬A)` is the one worth thinking about**, and most students predict it is unprovable because LEM is. It is provable: you cannot produce `A ∨ ¬A`, but you can refute anyone claiming to refute it. Given `k`, hand it `inr (λa. k (inl a))`. The tool's term beta-reduces to the standard `λk. k (inr (λa. k (inl a)))`.

**This is Glivenko's theorem in miniature:** every classical propositional tautology is intuitionistically provable under a double negation.

*The final mark is for a student who predicted wrongly, said so, and explained the resolution. That is the intended experience.*

---

## Part E — Written (12)

**E1.** *(6 — 2 mechanism/reason, 1 OCaml, 2 Agda, 1 what is lost)*

The **occurs check is the mechanism**; **strong normalisation is the reason**. If `Y` were typeable, a well-typed term would have no normal form and the theorem "every well-typed term terminates" would be false. The check is how the type system enforces what the theorem requires.

**OCaml, Haskell and ML: `let rec` is a primitive.** Recursion is built into the definition form rather than derived, and the totality theorem is deliberately given up.

**Agda and Coq require a termination check** — recursion is permitted only where an argument provably decreases. The cost is that some correct programs are rejected because the checker cannot see why they terminate, and the programmer must restructure or supply a well-foundedness proof.

**What is lost:** you can no longer decide whether an arbitrary program halts, so **every analysis must approximate**. Week 5 did this constantly — *may* and *must*.

**E2.** *(6 — 2 the difference, 2 the erasure, 1 Rust, 1 CS 201)*

- **A dictionary is selected by the static type; a vtable by the run-time value.**
- The compiler *knows* the static type at the call site, so it can resolve the dictionary, inline the method, and delete the argument. It cannot know the run-time value, so the indirection has to survive to run time.
- `impl Trait`/generics: monomorphised, direct calls, no dictionary at run time, code bloat. `dyn Trait`: vtable beside the pointer, one indirect call, one copy of the code.
- CS 201 Week 5 (`L17`): a mispredicted branch costs **15–20 cycles**, and an indirect call whose target the predictor cannot resolve is the case that misses. A direct call is predicted essentially for free.

---

## Overall

**Expected distribution:** A and D should be high — they are mostly running tools and reading carefully. **Part C is the whole assessment**, and C2's deferral and C3's recursive dictionary are the two places submissions stop short.

**Two failure modes:**

1. **A Part C that only handles concrete types.** It will look complete, resolve `Eq Int` beautifully, and be unable to type `member`. Test every submission on a function with a constraint on a type variable.
2. **D3 transcribed from the tool.** The question says predict first, and the tell is a student who reports `¬¬(A ∨ ¬A)` as provable with no comment. Genuine engagement always mentions the surprise.

---

*CS 211 · Week 8 · PS 8 Solutions · © CSE Department*
