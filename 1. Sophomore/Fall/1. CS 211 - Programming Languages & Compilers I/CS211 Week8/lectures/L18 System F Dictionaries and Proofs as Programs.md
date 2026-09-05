# CS 211 · Programming Languages & Compilers I
## Week 8 · Lecture 2 of 2
### System F, Dictionaries, and Proofs as Programs

---

**Reading:** Pierce, *TAPL* ch. 23, 9.4 · Wadler & Blott (1989) · Wadler, "Propositions as Types" (2015) · **Next:** L19, concurrency

---

## 1. Writing the Quantifier Down

L17 §7 left inference at rank-1: a `∀` may only sit at the outermost level of a type. `(λi. pair (i one) (i true))` needs

```
(∀a. a → a) → (Nat, Bool)
```

and HM cannot infer it. **System F** — Girard 1972, Reynolds 1974, independently — is the calculus where you write it yourself.

It adds two constructs to the typed lambda calculus, and they are the type-level mirror of the two you already know:

| term level | type level |
|---|---|
| `λx : A. e` — take a value | `Λa. e` — take a **type** |
| `e₁ e₂` — apply to a value | `e [A]` — apply to a **type** |

The polymorphic identity stops being a term with an inferred scheme and becomes a term that literally takes a type:

```
id  =  Λa. λx : a. x            :  ∀a. a → a
id [Nat] three                  :  Nat
id [Bool] true                  :  Bool
```

`∀` is no longer bookkeeping attached to a `let`. It is a **function type whose argument is a type**, and `Λ` is its lambda.

Three things follow, and the third is why System F is not just Haskell's engine.

**Every term carries its own type applications**, so nothing needs to be inferred. Type checking System F is decidable and straightforward.

**Type *inference* for System F is undecidable** — Wells, 1994. You may check what someone wrote; you cannot in general reconstruct it. That is the exact price of the expressiveness L17 §7 measured, and it is why every practical language sits somewhere on the annotation/inference trade-off rather than at one end.

**System F is strongly normalising.** Every well-typed term has a normal form. Which brings back Week 7.

---

## 2. What Typing Costs: Exactly the Thing Week 7 Needed

The simply-typed lambda calculus and System F share a theorem: **every well-typed term terminates.**

That is a remarkable property to get for free, and it is not free. Recall what `infer.py` rejected:

```
  Y  : occurs check: cannot construct the infinite type b = b -> c
  Z  : occurs check
  omega, selfapp, fact, fib, factV, fibV : occurs check
```

**A total language cannot have `Y`, and this is not an accident of Hindley-Milner — it is forced.** If `Y` were typeable you could write a term with no normal form, and then "every well-typed term terminates" would be false. The occurs check is the *mechanism*; strong normalisation is the *reason*.

So a typed language has a choice, and every one of them has made it explicitly:

| language | choice |
|---|---|
| **OCaml, Haskell, ML** | `let rec` is a **primitive**, not a derived combinator. Recursion is built into the definition form, deliberately, and the totality theorem is given up. |
| **Agda, Coq, Lean** | Keep totality. Recursion is allowed only where a **termination checker** can see a decreasing argument. |
| **Rust, Java, C** | Never had the theorem; unbounded recursion is simply allowed. |

> **"Add types and you lose non-termination" is a real trade and the languages you use have all
> bought their way back out of it.** `let rec` looks like a convenience keyword. It is the
> language declining a theorem.

And notice what you lose by *having* `Y`: Week 7 §13's point, from the other side. Once non-termination is expressible, no analysis can decide whether a program halts, so **every optimisation must approximate** — which is why Week 5's liveness was a *may* analysis and dominance a *must*.

---

## 3. Parametricity: What a Type Tells You Before You Read the Code

System F licenses a result with no counterpart in an untyped world.

Consider `∀a. a → a`. The term cannot inspect its argument — it does not know what type it has. There is exactly **one** total function of that type: the identity.

`∀a. a → a → a` has exactly **two**: return the first, or return the second. Those are Week 7's `true` and `false`, and now the *type* tells you there are precisely two inhabitants.

`∀a. List a → List a` cannot invent elements or examine them; it can only drop, duplicate and rearrange what it was given. So without reading a line of it you know `reverse`, `tail` and `id` are candidates and `map (+1)` is not — the type forbids it.

This is Reynolds' and Wadler's **parametricity**, and Wadler's slogan for it is "theorems for free": from the type alone you derive laws the function must satisfy.

> **Parametricity is the payoff for polymorphism being *uniform*.** The reason `∀a. a → a` is so
> informative is precisely that the code cannot branch on `a`. Ad-hoc polymorphism — the next
> section — gives that up in exchange for being able to do different things per type, and loses
> the free theorems with it.

---

## 4. Ad-hoc Polymorphism, and the Translation That Removes It

`eq` cannot be parametric. Comparing two `Int`s and two `List Int`s is genuinely different code, so the type `∀a. a → a → Bool` is a lie — there is no such uniform function.

Haskell's answer:

```haskell
class Eq a where
  eq :: a -> a -> Bool

instance Eq Int             where eq = primEqInt
instance Eq a => Eq [a]     where eq = eqList

member :: Eq a => a -> [a] -> Bool
```

This looks like a new language feature. **It is not.**

- **A class declaration is a record type.**
- **An instance is a value of that record.**
- **A constrained function is a function with an extra parameter.**

The record is a **dictionary**, and the translation is dictionary passing — Wadler & Blott, 1989.

```
$ python3 classes.py
; ---- a class is a record type ----
  class Eq a    =>   type DictEq a  = { eq }
  class Ord a   =>   type DictOrd a = { superEq, le }  (superclass: Eq)

; ---- an instance is a value of that record ----
  instance Eq Int
      dEq_Int = { eq = primEqInt }
  instance (Eq a) => Eq List a
      dEq_ListA dEq_a = { eq = eqList dEq_a }
```

Read the second instance. **It has a context, so it compiles to a *function*** — give it a dictionary for `a` and it builds one for `List a`.

That is what makes the system work without an instance for every type:

```
; ---- resolution happens at COMPILE time, and it recurses ----
  Eq List List Int
        Eq List Int  ->  instance Eq List a
          Eq Int  ->  instance Eq Int
      => (dEq_ListListInt (dEq_ListInt dEq_Int))
```

Nobody wrote an instance for lists-of-lists-of-`Int`. **The compiler constructed the dictionary**, by recursion over the type, before the program ran.

And the constrained function:

```
  source:      member : Eq a => a -> List a -> Bool
               member x xs = ...  uses  eq x y

  elaborated:  member : DictEq a -> a -> List a -> Bool
               member dEq_a x xs = ...  uses  (eq dEq_a) x y

  call site `member 3 [1,2,3]` becomes `member dEq_Int 3 [1,2,3]`
```

**The `=>` became a `->`.** Nothing in the elaborated program is a type class; it is records and functions, which the rest of the compiler already knows how to handle.

Finally, note *when* a missing instance is reported:

```
  Show Bool     COMPILE-TIME ERROR -- no instance for Show Bool
```

**At elaboration, before anything ran.** A missing instance is a type error, not a method-not-found at run time. That is the whole difference from duck typing.

---

## 5. The Same Trick, Three Times, With One Difference That Matters

Dictionary passing is not unique to Haskell. It is what every language does for ad-hoc polymorphism — the difference is *where the dictionary comes from*.

| | dictionary | chosen by | cost |
|---|---|---|---|
| **Haskell type class** | passed as a hidden argument | the **static type** at the call site | one indirect call, often inlined away |
| **Rust trait, static dispatch** | none — the code is **monomorphised** | the static type, per instantiation | zero; a direct call, and code bloat |
| **Rust `dyn Trait`** | a vtable pointer beside the data | the **run-time value** | one indirect call |
| **C++ virtual** | a vtable pointer **inside** the object | the run-time value | one indirect call |
| **Java interface** | in the object header | the run-time value | one indirect call plus a lookup |

**The line worth remembering:** a type class dictionary is selected by the *type*, so it can be resolved and often erased at compile time. A vtable is selected by the *value*, so it cannot. That is why `impl Trait` and generics in Rust cost nothing and `dyn Trait` costs an indirect call, and it is the same distinction CS 201 met as direct against indirect branches — where `L17 Branch Prediction and Out-of-Order Execution` puts a misprediction at 15–20 cycles.

**Existential types** are the other side of it. `dyn Trait` and Java's `List<Shape>` say *there exists* some type with this interface, and hide which — so the dictionary must travel with the value. `∀` is the caller choosing the type; `∃` is the callee having chosen and refusing to say.

---

## 6. Higher-Kinded Types, Briefly

`List` is not a type. `List Int` is a type; `List` is a function from types to types. Its **kind** is `* → *`.

Kinds are types for types, and the same three-line story repeats one level up:

```
  Int, Bool            :: *
  List, Maybe          :: * -> *
  Either, Pair         :: * -> * -> *
  Functor, Monad       ::(* -> *) -> Constraint
```

Being able to abstract over a `* → *` — to write `class Functor f` where `f` is *itself* a type constructor — is **higher-kinded polymorphism**, and it is why Haskell can define `fmap` once for every container. Java and Go cannot: their generics quantify over types (`*`), never over type constructors, so `Functor` is not expressible and each container gets its own `map`.

**Dependent types** invert the layers entirely — types that contain *values*, like `Vec 3 Int`, a vector whose length is part of its type. Then `append : Vec m a → Vec n a → Vec (m+n) a` is checkable, and an out-of-bounds index becomes a type error. Agda, Idris and Lean do this. The cost is that type checking now involves *evaluating* terms, so it inherits everything Week 7 §13 said about decidability.

---

## 7. Proofs Are Programs

Now the result the syllabus calls this week's deep idea, and it is not a metaphor.

Read a type as a proposition:

| type | proposition |
|---|---|
| `A → B` | A implies B |
| `(A, B)` | A **and** B |
| `Either A B` | A **or** B |
| `Void` (no values) | **False** |
| `A → Void` | **not** A |

Under this reading, **a term of type `T` is a proof of the proposition `T`** — the *Curry-Howard correspondence*.

A proof of `A → B` is a function turning any proof of `A` into a proof of `B`. A proof of `A ∧ B` is a pair. A proof of `A ∨ B` is a tagged value saying which side you have. There is no proof of `False` because `Void` has no values.

`curry.py` decides intuitionistic propositional logic — Dyckhoff's LJT, 1992 — and prints the proofs it finds. Look at what they are:

```
$ python3 curry.py
; ---- PROVABLE (12) ----
  ok    A → A                            λp0. p0
  ok    A → B → A                        λp0. λp1. p0
  ok    (A → B → C) → (A → B) → A → C    λp0. λp1. λp2. ((p0 p2) (p1 p2))
  ok    A ∧ B → A                        λp0. fst p0
  ok    A ∧ B → B ∧ A                    λp0. (snd p0, fst p0)
  ok    A → A ∨ B                        λp0. inl p0
  ok    (A → C) → (B → C) → A ∨ B → C    λp0. λp1. λp2. case p2 of ...
  ok    ⊥ → A                            λp0. absurd p0
```

**Read the first three.**

- The proof of `A → A` is `λp. p` — **the identity function**.
- The proof of `A → B → A` is `λp q. p` — **`const`, which Week 7 found is the same term as `true`**.
- The proof of `(A→B→C) → (A→B) → A → C` is `λf g x. (f x) (g x)` — **the S combinator**.

Those two are the axioms **K** and **S** of combinatory logic, and they are exactly the axioms of implicational propositional logic. Nobody arranged that. The correspondence is an isomorphism: **logic and computation are the same structure, discovered twice.**

---

## 8. What Is *Not* Provable, and Why That Is the Point

```
; ---- NOT PROVABLE (5) ----
  none  A ∨ ¬A               (excluded middle)
  none  ¬¬A → A              (double negation)
  none  ((A → B) → A) → A    (Peirce's law)
  none  ¬(A ∧ B) → ¬A ∨ ¬B   (a de Morgan)
  none  (A → B) ∨ (B → A)    (linearity)
```

Every one of those is a **classical tautology** — true under any assignment of true and false. And LJT is a *decision procedure*, so "none" is a proof of unprovability, not a search that gave up.

The reason is visible in the types. A proof of `A ∨ ¬A` must be a program that **produces a tagged value**: either an `inl` carrying a proof of `A`, or an `inr` carrying a function from `A` to `Void`. To write it you would have to *decide*, for an arbitrary unknown `A`, which one you have. **You cannot, because `A` is arbitrary and you have nothing to inspect.**

Classical logic says "A is true or it is not" without saying which. Constructive logic — the one types give you — demands the witness.

Add the axiom and everything returns:

```
; ---- but each becomes provable given the missing axiom ----
  A ∨ ¬A                 PROVED from LEM
  ¬¬A → A                PROVED from LEM
  ((A → B) → A) → A      PROVED from LEM
  ...
  `lem` is a free variable of every proof above: an ASSUMPTION,
  not a construction.
```

> **A free variable in a proof term is an assumption, and that is precisely what classical logic
> adds.** Constructively, excluded middle is not false — it is *unproved*, and taking it as an
> axiom is taking a value you cannot build. The computational content of that axiom turns out to
> be `call/cc`: Griffin (1990) showed that classical reasoning corresponds to first-class
> continuations, which is why a proof by contradiction reads like a program that jumps out of its
> own evaluation.

**This is what proof assistants are.** Coq, Agda, Lean and Idris are type checkers whose types are propositions, and their proofs are programs you can run. CompCert is a C compiler *proved* to preserve semantics, and seL4 is an OS kernel with a machine-checked functional-correctness proof — both of them typed programs whose types are the theorem.

Which turns the week's opening question inside out. Week 7 asked what a function is. Week 8's answer: **a function is an implication, and a type checker is a proof checker** — the one you have been running on Cyan since Week 3.

---

## 9. What to Take From This

1. **System F writes the quantifier down**: `Λa. e` and `e [A]` are the type-level mirror of `λ` and application.
2. **Checking System F is decidable; inferring it is not** (Wells 1994). That is the price of what L17 §7 measured.
3. **A total language cannot have `Y`** — the occurs check is the mechanism, strong normalisation the reason. `let rec` is a language declining a theorem.
4. **Parametricity gives theorems for free**: `∀a. a → a` has exactly one inhabitant, `∀a. a → a → a` exactly two — Week 7's `true` and `false`.
5. **A class is a record, an instance is a value, a constraint is a parameter.** The `=>` becomes a `->` and nothing type-class-shaped survives.
6. **The compiler builds dictionaries by recursion over the type**, at compile time — `(dEq_ListListInt (dEq_ListInt dEq_Int))`, which nobody wrote.
7. **A dictionary is chosen by the type and a vtable by the value**, which is why one can be erased and the other cannot.
8. **Higher kinds** are types for type constructors; Java and Go stop at `*` and so cannot express `Functor`.
9. **A term of type `T` is a proof of `T`.** The proofs of the first two theorems are `id` and `const`; the third is the S combinator.
10. **Excluded middle is unprovable because a proof would have to be a program that decides**, and adding it as an axiom leaves a free variable in every proof that uses it.

**Next week the type system stops being the hard part.** Concurrency introduces a question none of Weeks 4–8 has had to ask — *what does this program even mean when two of them run at once* — and the answer requires a memory model.

---

*CS 211 · Week 8 · Lecture 18 · © CSE Department*
