# CS 211 · Problem Set 7 — Solutions and Mark Scheme
## Instructor Only

**Do not distribute.** All beta counts verified against the Week 7 lab code on Python 3.14.2. **Generated variable names are not deterministic** — `fresh` uses a global counter — so mark on alpha-equivalence, never on the numeral in `λy0`.

---

## Part A — Substitution and Capture (20)

**A1.** *(4 — one per term)*

| term | free | bound |
|---|---|---|
| `λx. x y` | `y` | `x` (the λx) |
| `(λx. x) (λy. y x)` | `x` (the one inside `λy`) | `x` in the first, `y` in the second |
| `λx. (λx. x) x` | — | see below |
| `λf. (λx. f (x x)) (λx. f (x x))` | — | `f`, and each `x` to its own λx |

**Term 3 is the marked one.** `λx. (λx. x) x` has two binders named `x`. The `x` inside `(λx. x)` belongs to the **inner** binder; the final `x` belongs to the **outer** one. The rule is that **an occurrence binds to the nearest enclosing binder of that name** — lexical scoping, Week 3's `L07`, and the reason `Scope` chains to a parent.

*Common error: claiming the final `x` is free. It is not — it is under `λx`.*

**A2.** *(6 — 2 the two results, 2 the new term, 2 the "agree by luck" case)*

Correct: `λy0. y`, a **constant** function returning the free `y`. Naive: `λy. y`, the **identity**.

Any second term where the substituted term has a free variable matching an inner binder works, e.g. `(λx y. x y) y` or `(λx. λy. x) (λz. y)`. **Require the student to show both outputs**, not just assert a difference.

The "agree by luck" case: any term where the replacement has **no free variables** — `(λx y. x) (λz. z)` — or where the inner binder's name does not collide. Agreement is luck because `--naive` performs no check at all: it agrees whenever collision happens not to arise, and has no way to know the difference.

**A3.** *(6 — 2 per branch, and the argument matters more than the code)*

Branches: (1) the parameter shadows `x`, so no free `x` remains below — stop; (2) the parameter is free in `s`, so descending would capture — rename first; (3) neither — descend.

**Deleting branch 1: nothing changes, and this is the intended answer.** If `t.param == x` then no free `x` occurs in the body, so substituting there is a no-op — it is a *performance* short-circuit, not a correctness requirement. **Accept a proof by that argument, or a report of running the full `church.py` suite unchanged.** Reject an unsupported "it's needed".

*Careful: it is only a no-op given branch 2 is intact. A student who notices that deleting branch 1 while branch 2 renames could rename a binder unnecessarily — changing names but not meaning — has gone further than required and should be credited.*

**Always renaming (breaking branch 3): results are unchanged up to alpha-equivalence**, and every output gets fresh names. That is the point — **branch 2 is not checking correctness, it is checking necessity.** The renaming is always *safe*; the condition only avoids doing it when it cannot matter.

**A4.** *(4)*

Reduce the same term twice in one process and the fresh names differ (`λy0`, then `λy1`). Results are equal under **alpha-equivalence**; show with `alpha_eq`.

A compiler wants determinism for **reproducible builds** — identical input must give byte-identical output, or caching, distributed builds and debug-info comparison all break. *(Accept: debuggability, diffable dumps, content-addressed build caches.)*

---

## Part B — Reduction Strategies (22)

**B1.** *(5 — 3 the table, 2 the pairing)*

| term | `normal` | `cbn` | `applicative` | `cbv` |
|---|---|---|---|---|
| `(\x y. y) omega one` | `λf x. f x` | `λf x. f x` | diverges | diverges |
| `(\x. x x) (\x. x x)` | diverges | diverges | diverges | diverges |
| `\x. (\y. y) z` | `λx. z` | **`λx. (λy. y) z`** | `λx. z` | **`λx. (λy. y) z`** |

**Row 3 pairs them by whether they reduce under a lambda:** `normal`/`applicative` do and reach a full normal form; `cbn`/`cbv` do not and stop at a **value**. Row 1 pairs them the other way, by whether arguments are evaluated first.

*The two knobs are independent, which is the point of the table: "lazy vs strict" and "full normal form vs value" are different axes, and only the four combinations make the distinction visible.*

**B2.** *(5)*

10384 and 552 (263 + 289).

**Mechanically:** normal order substitutes the *unevaluated* argument `pred n` into `factgen`'s body. That body mentions its parameter more than once along the recursion, so the same `pred` computation — 36 reductions at n=3, 56 at n=5 — is performed again at every level rather than once. Call-by-value reduces it once and substitutes the numeral.

**Why the guarantee did not help:** the standardisation theorem says normal order *finds a normal form if one exists*. `fact four` has one, and both strategies find it. The theorem is about **termination**, and says nothing whatever about cost — so on a term where both terminate it offers no advantage at all.

**B3.** *(12 — 6 working implementation, 3 the table, 3 the two follow-ups)*

Reference numbers:

| n | normal | cbv | **need** | forces |
|---|---|---|---|---|
| 1 | 45 | 53 | 45 | 32 |
| 2 | 248 | 119 | **94** | 68 |
| 3 | 1525 | 239 | **177** | 131 |
| 4 | 10384 | 552 | **384** | 292 |
| 5 | >60000 | 1864 | **1237** | — |
| 6 | >60000 | 9539 | **6210** | — |

Ratio at n = 4: **27×** against normal order.

**Student counts need not match.** They depend on where thunks are introduced. **What must hold:** correct results; counts far below normal order's; the ratio growing with n; and `(\x y. y) omega one` still terminating.

**The termination check is the one to actually run.** A student who has built call-by-value by accident gets excellent numbers and fails this test, and the numbers alone will not reveal it.

**Semantic change or implementation technique?** — **implementation technique.** Call-by-need and call-by-name produce the *same results* on the same terms and terminate on exactly the same terms; only the number of reductions differs. *(Accept the sophisticated objection that it becomes observable in the presence of side effects or timing, and that this is exactly why Haskell is pure. That answer is better than the expected one.)*

---

## Part C — Encodings (22)

**C1.** *(4)* `double = λn. mult two n` (or `add n n`). `mult two n` costs less than `add n n` for larger `n` — and the marked part is that the student measured rather than guessed.

`iseven = λn. n not true`. `max = λm n. (leq m n) n m`.

**C2.** *(6)*

`pred n` for n = 1…6: 16, 26, 36, 46, 56, 66 — **linear, +10 per step.**

Predicted `sub six two` = `two pred six` ≈ `pred six` + `pred five` = 66 + 56 = 122. **Actual: 126.** The 4-reduction difference is the `sub` wrapper itself applying the numeral `two`. **Full marks require the prediction stated before the measurement and the gap accounted for**, not a post-hoc match.

**C3.** *(6 — 2 the list, 3 the classification, 1 the type-system question)*

Seven pairs; see the Lab 7 solutions for the table. **Three theorems** (`const`/`true`, `apply`/`one`, `compose`/`mult`), **four collisions** (`id`/`unit`, and the `false`/`nil`/`zero` triangle).

The classification is the marked part. A theorem is reproduced by any correct encoding because the two operations genuinely coincide; a collision is an artefact of *this* encoding and a different one (Scott numerals, say) separates them.

**Why a type system need not separate the theorems:** they are the same operation, so confusing them is harmless — you cannot compute a wrong answer by using `mult` where `compose` was meant. The collisions are different meanings, and there confusion is exactly the hazard.

*A student who finds only three pairs has compared by printed form rather than with `alpha_eq`. Send them back.*

**C4.** *(6)*

```
leaf     = λv. λl n. l v
node     = λa b. λl n. n (a l n) (b l n)
foldtree = λt l n. t l n
treesum  = λt. foldtree t (λv. v) add
depth    = λt. foldtree t (λv. one) (λa b. succ (max a b))
```

Verified on `t5 = node (node (leaf 1) (leaf 2)) (node (leaf 3) (node (leaf 4) (leaf 5)))`:

| term | result | betas |
|---|---|---|
| `treesum (leaf three)` | 3 | 8 |
| `depth (leaf three)` | 1 | 8 |
| `treesum t5` | **15** | 64 |
| `depth t5` | **4** | 429 |

Note `depth` costs 6.7× `treesum` on the same tree — it calls `max`, which calls `leq`, which calls `sub`, which is `pred` repeated. **C2's asymmetry, arriving inside a student's own code.**

**The distinguishability question is the marked one.** A `leaf` and a `node` must not be alpha-equivalent, and with the encoding above they are not — a leaf ignores `n`, a node uses it. **Students who define `leaf = λv. v` will collide with `id` and with everything else**, and discovering that is the intended experience of C3 arriving in their own code.

---

## Part D — Recursion and Evaluation Order (24)

**D1.** *(6)* 44 steps, 3911 steps, and `6` in 175 + 64.

**44 vs 3911:** Y's self-application `x x` is an *argument*, so call-by-value reduces it immediately and never enters `factgen` at all. Z wraps it as `λv. x x v`, an abstraction, which call-by-value treats as a **value** and does not enter — so control reaches `factgen` and real progress happens. **3911 is still a failure** because `if` is an ordinary function whose three arguments are all evaluated, so the recursive branch is computed on every call including the base case.

**The rule:** in a strict language a conditional cannot be an ordinary function, because a function cannot decline to evaluate its arguments.

**D2.** *(6)* The three terms, and `alpha_eq(eta_reduce(Z), Y)` is `True`.

**"The same function"** is extensional: for every argument both yield the same result. It is a claim about *results*, not about *when* or *whether the computation gets there under a particular strategy*.

Python: `lambda: expr` passed where `expr` would have been. JavaScript: `() => expr`, or `setTimeout(() => f(), 0)` versus `setTimeout(f(), 0)`. **Both are eta-expansions performed to delay evaluation**, and the second JS pair is a bug students have written.

**D3.** *(12 — 6 working, 3 the CBV version, 3 the closing question)*

Reference (pair-based):

```
mutgen = λp. pair (λn. if (iszero n) true  (snd p (pred n)))
                  (λn. if (iszero n) false (fst p (pred n)))
evens  = fst (Y mutgen)
odds   = snd (Y mutgen)
```

`evens 0…6` = T, F, T, F, T, F, T at **18, 52, 114, 214, 362, 568, 842** betas.

Call-by-value version needs **two** changes, and students typically find only the first:

1. thunk the branches (`lazyif`, as in `factgenV`);
2. **eta-expand the projections** — `evensV = λn. fst (Z mutgenV) n`, not `evensV = fst (Z mutgenV)`. Without it, `fst (Z mutgenV)` is a redex at the top level and call-by-value drives the fixed point before any argument arrives.

`evensV 0…6` = **20, 61, 119, 194, 286, 395, 521** betas.

**The closing question:** OCaml's `and` makes the compiler build a **single recursive definition over a tuple (or a mutually-referential closure environment) and project out of it** — exactly the pair construction, done by the compiler instead of by hand. *(Accept: the compiler allocates the closures first and back-patches their environment pointers, which is the imperative form of the same fixed point. That answer is better.)*

---

## Part E — Written (12)

**E1.** *(6 — 2 the two benefits, 2 shift, 2 the real speed source)*

De Bruijn buys: **alpha-equivalence becomes structural equality**, and **capture becomes impossible** — not handled, absent.

`shift` adds a constant to every *free* index in a term, tracking a cutoff so that indices bound inside the term do not move. Every beta needs **two**: one on the argument as it goes under the binder (its free indices are now one further from home) and one on the result as the binder is removed.

**The real speed source is environments and closures.** Instead of substituting the argument into the body, carry a list of values and let index `k` mean "the k-th entry". A beta-step becomes *push onto the environment* — constant time — rather than *rewrite the whole body*. The body is never copied, so the 5–74× disappears along with the traversals. **This is what a student implementing first-class functions in Project 1 will need**, and it is worth saying so on the feedback.

**E2.** *(6 — 3 omega, 2 OCaml, 1 the cost)*

For `λx. x x`, suppose `x : T`. The application `x x` requires `x` to be a function `A → B` with its argument of type `A`, so `T = T → B`. **No finite type satisfies `T = T → B`** — it is an infinite type, and this is the *occurs check*, which Week 3's Hindley-Milner already rejects for exactly this reason. So `λx. x x` is untypeable and `omega` cannot be written.

**OCaml has recursion because `let rec` is a primitive**, not a derived combinator — the language builds the fixed point into the definition form rather than expressing it as a term. *(Same for Haskell, ML, Scheme.)*

**What you lose once `Y` is available:** you can no longer decide, in general, whether a program terminates — so you cannot evaluate arbitrary expressions at compile time, and **any analysis must approximate**. Week 5 did this constantly: liveness is a *may* analysis and dominance a *must* analysis precisely because exactness is unavailable. *(Accept: total functional languages like Agda and Coq give up `Y` to keep decidability, and pay for it in expressiveness.)*

---

## Overall

**Expected distribution:** A and C are recall-plus-a-step and should be high. **B3 and D3 separate the class**, and both are implementation tasks with a stated correctness check — mark the check, not the prose. **E2 is the bridge into Week 8** and identifies who is reading the course as an argument.

**Two failure modes to watch:**

1. **B3 that is secretly call-by-value.** Good numbers, correct results, fails `(\x y. y) omega one`. **Run that one test on every submission**; it takes five seconds and it is the whole question.
2. **C3 answered by inspection.** Three pairs reported instead of seven means they compared printed forms. The question says brute force for a reason.

---

*CS 211 · Week 7 · PS 7 Solutions · © CSE Department*
