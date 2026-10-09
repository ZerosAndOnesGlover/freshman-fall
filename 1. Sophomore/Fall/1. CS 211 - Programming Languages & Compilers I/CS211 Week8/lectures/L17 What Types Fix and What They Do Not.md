# CS 211 · Programming Languages & Compilers I
## Week 8 · Lecture 1 of 2
### What Types Fix, and What They Do Not

*“The connection between the language in which we think/program and the problems and solutions we can imagine is very close. For this reason restricting language features with the intent of eliminating programmer errors is at best dangerous.”* — Bjarne Stroustrup, *The C++ Programming Language*, Special Edition (2000), Notes to the Reader

---

**Reading:** Pierce, *TAPL* ch. 8–9, 22 · Cardelli & Wegner (1985) · **Next:** L18, System F, classes, and Curry-Howard

**Coursework:** 📊 **Quiz 8** today · 📘 **Midterm 2** today 20:00–21:15 · 📝 **PS 8** released Wed this week, due Fri of Week 9 17:00 · 📝 **PS 7** due Fri this week 17:00 · 🔬 **Lab 8** Fri this week 14:00–15:50

---

## 1. The Question Week 7 Left

Week 7 ended with a term that meant three things:

```
zero = λf x. x       false = λt f. f       nil = λc n. n
alpha-equivalent: True
```

The obvious diagnosis is that the language has no types, and the obvious remedy is to add some. So add some. Week 3 already wrote the algorithm — `hm.py`, unification with an occurs check, `instantiate`, `generalise` — over a toy AST with integers and `if`.

`infer.py` is that engine with **one thing changed: the input**. Same unification, same occurs check, same `Scheme`. Point it at `prelude.lam`:

```
$ python3 infer.py
; ---- Hindley-Milner over prelude.lam (55 definitions) ----
; the engine is Week 3's, unchanged; only the input is new
```

Two results come back. One is the one everybody expects. The other is not.

---

## 2. Thirty-Nine Survive, Sixteen Do Not

```
; ---- 39 typeable ----
  id         : forall a. a -> a
  const      : forall a b. a -> b -> a
  compose    : forall d e c. (d -> e) -> (c -> d) -> c -> e
  two        : forall d. (d -> d) -> d -> d
  succ       : forall e f c. ((e -> f) -> c -> e) -> (e -> f) -> c -> f
  pair       : forall a b e. a -> b -> (a -> b -> e) -> e
  ...

; ---- 16 REJECTED ----
  selfapp    : occurs check: cannot construct the infinite type a = a -> b
  omega      : occurs check: cannot construct the infinite type a = a -> b
  and        : occurs check: cannot construct the infinite type c = (b -> c
  or         : occurs check: cannot construct the infinite type a = a -> c
  eq         : occurs check: cannot construct the infinite type e = (d -> e
  lt         : occurs check: cannot construct the infinite type e = (d -> e
  Y          : occurs check: cannot construct the infinite type b = b -> c
  Z          : occurs check: cannot construct the infinite type b = b -> d
  fact       : occurs check: cannot construct the infinite type b = b -> c
  fib        : ...
  factV      : ...
```

**All sixteen rejections are the same check.** Not sixteen different type errors — one error, sixteen times.

Recall what the occurs check is. Unifying `a` with `a → b` would require a type that contains itself, and there is no finite type that does. `lam.py`'s `subst` never had to think about it; `unify` does, in four lines:

```python
if occurs(a, b):
    raise TypeError_(f"occurs check: cannot construct the "
                     f"infinite type {a!r} = {b!r}")
```

You have met it twice before. **Week 3** rejected `λx. x x` with it. **Week 6** could not write `cyc_array.cy` because a self-containing array needs `T = [T]`, and that lecture called the obstacle "an infinite type, which Cyan's grammar has no way to write down". Same check, three appearances, and each time it was the thing standing between you and a term you wanted.

### Two rejections that are not obvious

`Y`, `Z`, `omega` and `selfapp` are unsurprising — they are self-application, which is what the occurs check exists to refuse.

**`and` and `or` are not obviously self-application at all:**

```
and = λp q. p q p
or  = λp q. p p q
```

`and` applies `p` to `q` and to **`p`**. So `p` must accept something of its own type, and the occurs check fires. **Boolean conjunction, in the Church encoding, is self-application in disguise** — and nobody writing that four-character definition in Week 7 noticed, because there was nothing to notice it with.

> **A type checker is not primarily a device for catching your mistakes.** It is a device for
> telling you what you actually wrote. `and = λp q. p q p` is a correct definition of conjunction
> that computes the right answer on every input, and it is *also* an instance of a construction
> the type system has to refuse. Both of those were true in Week 7 and neither was visible.

---

## 3. What the Types Look Like When They Do Work

Typeable is not the same as usefully typed.

```
  two        : forall d. (d -> d) -> d -> d
  pair       : forall a b e. a -> b -> (a -> b -> e) -> e
  pred       : forall m n v w t k k1 l1 n1 o1 j1 c d r1. ((((m -> n -> n) ->
               (v -> w) -> t -> v) -> (((v -> w) -> t -> v) -> ((v -> w) ->
               t -> w) -> k) -> k) -> ...
```

`two` gets exactly the type a Church numeral should have. `pred` gets a type with **fourteen quantified variables** that no human will read, and which says nothing recognisable about predecessors.

The reason is that HM infers the *principal* type — the most general one consistent with the term — and the term is a lambda-calculus encoding rather than an implementation of a declared idea. **The type describes the plumbing, because the plumbing is all there is.** Nothing in `pred` says "this is about numbers"; that meaning lived entirely in our heads and in `prelude.lam`'s comments.

---

## 4. The Result That Inverts the Story

Now the question the whole week is supposed to answer.

```
; ---- the Week 7 collision, retyped ----
  zero       : forall a b. a -> b -> b
  false      : forall a b. a -> b -> b
  nil        : forall a b. a -> b -> b
  still the same term: True
```

**Types do not fix it.**

All three get the same principal type, because they *are* the same term and a principal type is a function of the term. Adding Hindley-Milner separated nothing. And the same holds for Week 7's three "theorems":

| | | shared type |
|---|---|---|
| `const` | `true` | `∀a b. a → b → a` |
| `apply` | `one` | `∀b c. (b → c) → b → c` |
| `compose` | `mult` | `∀d e c. (d → e) → (c → d) → c → e` |

Week 7 §5 claimed that "telling the theorems from the collisions is exactly the service a type system provides". **That claim, as stated, is wrong, and this is the measurement that shows it.** Inferring types over the same terms distinguishes neither group.

### So what would fix it?

Not types. **Declarations.**

```haskell
data Bool = True | False
data Nat  = Zero | Succ Nat
```

`True` and `Zero` are now different because a programmer *said* they were different, and the compiler carries that decision as a **nominal** distinction — one grounded in the name of the declared type, not in its structure. Structurally `Bool` and `Nat`'s zero case are both "the nullary first constructor". Nominally they are unrelated, permanently, because `data` says so.

> **The useful axis is not typed against untyped. It is inferred against declared.** Inference
> reports what a term already means. A declaration adds information the term did not contain —
> which is why every practical language makes you write `data`, `struct`, `enum` or `class`, and
> why Church encodings are a proof of expressiveness rather than a way to program.
>
> Week 6 met the same distinction from the other side: `Ref` was a *distinct class*, so the
> collector could tell a pointer from an integer without guessing. That was a nominal decision
> too, and it bought precise collection.

**Structural typing** — where two types are the same if they have the same shape — is a real design choice, and TypeScript, Go's interfaces and OCaml's objects all make it. It buys convenience and it costs exactly this: `{x: number}` and `{x: number}` are the same type whether or not you meant them to be.

---

## 5. Three Kinds of Polymorphism

"Polymorphic" is used for three unrelated mechanisms, and confusing them makes the rest of this week impossible.

| | what varies | resolved | example |
|---|---|---|---|
| **Parametric** | the *type*, uniformly | at compile time, by instantiation | `id : ∀a. a → a` |
| **Ad-hoc** | the *code*, per type | at compile time, by the type | `eq : Eq a ⇒ a → a → Bool` |
| **Subtype** | the *code*, per value | usually at run time, by the value | `Shape.area()` |

**Parametric polymorphism does the same thing to every type.** `id` cannot inspect its argument — it does not know what it has, so there is exactly one thing it can do. That constraint is the feature: *parametricity* means a function's type tells you a great deal about what it must do. There is only one total function of type `∀a. a → a`, and only two of type `∀a. a → a → a`.

**Ad-hoc polymorphism runs different code per type.** `eq` on `Int` and `eq` on `List Int` share a name and nothing else. L18 §7 shows what the compiler turns this into.

**Subtype polymorphism** picks the code from the run-time value, not the static type. It is the one that needs a run-time representation of the choice — a vtable pointer in the object.

The distinction that matters for a compiler: **parametric polymorphism can be compiled away entirely** (one copy of the code, or one copy per instantiation), **ad-hoc polymorphism becomes an extra argument**, and **subtype polymorphism becomes an indirect call**. Three mechanisms, three different costs, one overloaded English word.

---

## 6. `let` Is Not Sugar

Here is HM's central mechanism, and a measurement that pins it exactly.

Week 8's `lam.py` adds one construct:

```
let x = e in b
```

For **evaluation** it is nothing. `desugar` turns it into `(λx. b) e`, which reduces identically — Week 7 did not need it and did not have it.

For **typing** it is everything:

```python
if isinstance(e, Let):
    tv = infer(e.val, env)
    return infer(e.body, {**env, e.name: generalise(env, tv)})
```

A lambda-bound name goes into the environment as `Scheme([], tv)` — **no quantifier, one type, every use forced to agree**. A let-bound name is **generalised**, so each use instantiates it freshly.

Measure the difference:

```
$ python3 infer.py 'let i = \x. x in pair (i one) (i true)'
  type : forall i j n o f. (((i -> j) -> i -> j) -> (n -> o -> n) -> f) -> f

$ python3 infer.py '(\i. pair (i one) (i true)) (\x. x)'
  type : TYPE ERROR -- occurs check: cannot construct the infinite type i = m -> i
```

```
$ python3 lam.py --defs prelude.lam 'let i = \x. x in pair (i one) (i true)'
  λf. f (λf x. f x) (λt f. t)

$ python3 lam.py --defs prelude.lam '(\i. pair (i one) (i true)) (\x. x)'
  λf. f (λf x. f x) (λt f. t)
```

**Identical normal forms. One typechecks and one does not.**

Starker still:

```
$ python3 infer.py 'let i = \x. x in i i'          → forall c. c -> c
$ python3 infer.py '(\i. i i) (\x. x)'             → TYPE ERROR
$ python3 lam.py   '(\i. i i) (\x. x)'             → λx. x
```

**`(λi. i i) (λx. x)` reduces to the identity function.** It is a completely harmless program. HM rejects it.

> **A type system is sound and incomplete, and this is what incompleteness looks like from the
> inside: a program that would have run fine, refused.** That is the third time this term the same
> shape has appeared — reference counting is sound and cannot see cycles (W6), liveness is a *may*
> analysis and dominance a *must* (W5), and now typing rejects working programs. **Every static
> analysis you have written approximates in one direction, and the direction is always the safe
> one.** Week 7 §13 said why: exactness is undecidable.

The practical consequence is the one that surprises people: **`let x = e in b` and `(λx. b) e` are the same program and different declarations.** That is why ML and Haskell make `let` primitive rather than sugar, and why "just inline it" is not always a meaning-preserving refactor in a typed language.

---

## 7. Where Inference Stops

HM's incompleteness is not arbitrary. It has a precise boundary, and it is worth naming because L18 crosses it.

In HM, a quantifier can only appear at the **outermost** level of a type: `∀a. a → a` is allowed, `(∀a. a → a) → Int` is not. That is called **rank-1** or **prenex** polymorphism, and it is exactly what makes inference decidable without annotations.

`(λi. pair (i one) (i true))` needs its parameter `i` to be *polymorphic* — used at two types inside the body. Writing that type down requires a quantifier to the left of an arrow:

```
(∀a. a → a) → (Nat, Bool)
```

That is **rank-2**, and HM cannot infer it. It can *check* it, if you write it down — which is precisely what GHC's `RankNTypes` extension offers, and why it requires an annotation.

> **Complete type inference and higher-rank polymorphism cannot both be had.** Type inference for
> rank-2 is decidable; for **rank 3 and above it is undecidable**, a result of Wells (1999).
> Every language in this space has picked a point on that trade-off: ML and early Haskell take
> rank-1 and full inference, modern Haskell takes higher rank with annotations, and Java and C#
> take rank-1 generics with annotations everywhere.

---

## 8. What to Take From This

1. **Week 3's inference engine runs unchanged on Week 7's terms.** Only the input is new.
2. **Sixteen of fifty-five definitions are rejected, and every rejection is the occurs check** — the same check that stopped `λx. x x` in Week 3 and `T = [T]` in Week 6.
3. **`and` and `or` fail.** Church conjunction is self-application in disguise, and nothing in Week 7 could have shown you that.
4. **Typeable is not usefully typed.** `pred` gets fourteen quantified variables and says nothing about predecessors.
5. **Types do not fix Week 7's collision.** `zero`, `false` and `nil` all get `∀a b. a → b → b`. The claim that a type system separates them was wrong as stated.
6. **What separates them is a *declaration*, not a type.** The useful axis is inferred against declared, and that is why every practical language makes you write `data`.
7. **Three kinds of polymorphism**, three different compilation strategies: instantiate, pass a dictionary, indirect call.
8. **`let` is not sugar.** Identical normal forms, different typeability — and `(λi. i i) (λx. x)` reduces to the identity and is rejected.
9. **Sound and incomplete, for the third time this term**, and always erring in the safe direction.
10. **Rank-1 is the boundary of inference.** Rank-2 is checkable, rank-3 undecidable.

**Next:** what you get by writing the quantifier down yourself — System F, type classes, and the discovery that a proof and a program are the same object.

---

*CS 211 · Week 8 · Lecture 17 · © CSE Department*
