# CS 211 · Programming Languages & Compilers I
## Week 3 · Lecture 2 of 2
### Hindley-Milner, and the Algorithm That Guesses Right

*“Well-typed programs cannot "go wrong".”* — Robin Milner, "A Theory of Type Polymorphism in Programming" (1978)

---

**Reading:** TAPL Ch. 22 · Dragon §6.5 · **Next:** Week 4, L09 — the IR, and what a compiler thinks a program *is*

**Coursework:** 📝 **PS 2** due Fri this week 17:00 · 🔬 **Lab 3** Fri this week 14:00–15:50 · 📊 **Quiz 4** Tue of Week 4 · 📘 **Midterm 1** Wed of Week 4 20:00–21:15 · 📝 **PS 4** released Wed of Week 4, due Fri of Week 5 17:00

---

## 1. The Annotations Are Doing Work You Could Skip

Cyan makes you write this:

```cyan
fn inc(x: int) -> int { return x + 1; }
```

Haskell makes you write this:

```haskell
inc = \x -> x + 1
```

```
$ ghci
> :t inc
inc :: Int -> Int
```

*(Measured, GHC 9.4.7.)*

**Nothing was declared and the compiler knows the type.** Not guessed — *derived*, and it will reject `inc True` with the same confidence as if you had written the signature yourself.

**This is Hindley-Milner type inference**, and it is one of the genuinely beautiful results in the field: **a statically typed language that needs no type annotations at all**, with a guarantee that the type it finds is the most general one possible.

---

## 2. The Idea: Unknowns and Equations

**Treat every unknown type as a variable, walk the expression generating equations, then solve.** It is simultaneous equations, over types instead of numbers.

For `\x -> x + 1`:

```
assign x : t0            -- x's type is unknown; call it t0
unify(t0, int)           -- '+' demands an int on the left
unify(int, int)          -- and on the right; 1 is already int
```

*(Measured — this is the actual trace.)*

**Three steps.** `t0` was unknown; `+` forced it to `int`; the result is `int -> int`.

**Two operations do all the work:**

| | |
|---|---|
| **Generate** | Walk the tree. Each construct contributes equations — a call demands its function's argument type match the argument's type; an `if` demands both branches agree |
| **Solve** | *Unification.* Given two types, make them equal by binding type variables, or fail |

---

## 3. Unification

```python
def unify(a, b):
    a, b = prune(a), prune(b)
    if isinstance(a, TVar):
        if a is not b:
            if occurs(a, b):
                raise TypeError_(f"occurs check: cannot construct infinite type")
            a.ref = b                      # bind the variable
        return
    if isinstance(b, TVar):
        return unify(b, a)
    if a.name != b.name or len(a.args) != len(b.args):
        raise TypeError_(f"cannot unify {a!r} with {b!r}")
    for x, y in zip(a.args, b.args):
        unify(x, y)                        # structural, recursive
```

**Four cases.** A variable binds to whatever it meets. Two constructors must have the same name and arity, and then their arguments must unify pairwise.

**`prune` follows the chain of bindings** to the current representative — the same idea as union-find, and the reason unification is near-linear rather than quadratic.

### The occurs check

The one case that looks like bureaucracy and is not:

```
\x -> x x    ->    TYPE ERROR -- occurs check: cannot construct infinite type t0 = t0 -> t1
```

*(Measured.)*

**Applying `x` to itself demands that `x`'s type be a function taking `x`'s own type**: $t_0 = t_0 \to t_1$. There is no finite type satisfying that. **Without the occurs check the algorithm builds a cyclic structure and loops forever**, so this three-line guard is what makes inference terminate.

GHC agrees, in its own words:

```
Couldn't match expected type ‘t1’ with actual type ‘t1 -> t2’
```

---

## 4. Inference, Measured

**No annotations anywhere in the input.** *(All verified, and cross-checked against GHC 9.4.7.)*

| Expression | Inferred type | GHC says |
|---|---|---|
| `\x -> x` | `t0 -> t0` | `p -> p` |
| `\x -> x + 1` | `int -> int` | `Int -> Int` |
| `\f -> \x -> f (f x)` | `(t3 -> t3) -> t3 -> t3` | `(t -> t) -> t -> t` |
| `\x -> \y -> x` | `t0 -> t1 -> t0` | `p1 -> p2 -> p1` |
| `\f -> \g -> \x -> f (g x)` | `(t3 -> t4) -> (t2 -> t3) -> t2 -> t4` | `(t1 -> t2) -> (t3 -> t1) -> t3 -> t2` |
| `\x -> if x <= 0 then 1 else x` | `int -> int` | `Int -> Int` |

**Read the third row.** Nothing said `f` takes and returns the same type. **The algorithm derived it** from `f (f x)`: the result of `f x` is passed to `f`, so `f`'s argument and result types must unify.

**Read the fifth row — function composition.** Three type variables and a specific threading among them, all derived from `f (g x)` alone.

> **The two implementations agree on every one**, differing only in what they name the variables.
> That is not a coincidence — GHC implements the same algorithm, and the **principal type theorem**
> says there is exactly one most-general answer to find.

---

## 5. The Principal Type Theorem

> **If an expression is typeable at all, Hindley-Milner finds a type from which every other valid
> type for that expression can be obtained by substitution.**

**"Most general" is precise here.** `\x -> x` has type `int -> int`, and `bool -> bool`, and `[int] -> [int]`. **All of them are instances of `t0 -> t0`**, and HM returns that one — not a plausible guess, but *the* answer, with nothing more general possible and nothing less general missed.

**This is what separates inference from heuristics.** TypeScript and C++'s `auto` also fill in types you did not write, but neither has this guarantee; they have rules that usually do what you meant. **HM has a theorem.**

---

## 6. Let-Polymorphism, and Where the Power Actually Lives

```
let f = \x -> x in if f true then f 1 else 2     ->    int
```

*(Measured.)*

**`f` is used at `bool -> bool` in the condition and at `int -> int` in the branch.** Two different types for one variable, in one expression.

**Now move the binding into a lambda instead**, changing nothing else:

```
(\f -> if f true then f 1 else 2) (\x -> x)
        ->    TYPE ERROR -- cannot unify bool with int
```

*(Measured. GHC agrees on both: the `let` version compiles, and the lambda version gives
`Couldn't match expected type 'Bool' with actual type 'Int'`.)*

**Same expression, same argument, opposite answers.** The difference is entirely in *how the variable was bound*.

> **Be careful which example you use to see this.** `let id = \x->x in id (id 1)` type-checks under
> **both** forms — because both occurrences of `id` are used at `int -> int` there, so no
> polymorphism is required. **You need two genuinely different types to see the effect**, which is
> why the condition above is a `bool` and the branch an `int`.

**When HM binds a `let` variable it generalises**: any type variable not constrained by the surrounding environment becomes universally quantified.

```python
def generalise(env, t):
    env_free = set()
    for s in env.values():
        env_free |= free_vars(s.t) - set(s.qs)
    return Scheme(list(free_vars(t) - env_free), t)
```

`id` gets the *scheme* $\forall t.\, t \to t$, and every use **instantiates** it with fresh variables.

**Lambda-bound variables are not generalised.** In `\f -> (f 1, f True)`, `f` has one monomorphic type and cannot be both. **That restriction is exactly what keeps inference decidable** — the unrestricted version is System F, whose inference is undecidable, and which is Week 8.

> **So HM is a carefully chosen point on a trade-off**, not the most powerful system available. It
> gives up rank-*n* polymorphism and gets, in exchange, complete inference with no annotations and
> a principal-type guarantee. **Week 8 walks up the other side of that hill.**

---

## 7. Why Cyan Does Not Do This

Cyan requires annotations on parameters and return types. `let` infers, and nothing else does:

```cyan
fn inc(x: int) -> int { return x + 1; }    // annotated
let y = inc(1);                            // y : int, inferred
```

**Three reasons, and none of them is that HM is hard.**

**1. Error messages.** HM reports the failure where unification finally breaks, which is often far from the mistake. Change `f`'s body in a hundred-line Haskell program and the error appears at the call site. **With annotations, the error is at the boundary you declared**, and the boundary is where you were thinking.

**2. Signatures are documentation.** `fn dist2(p: Point, q: Point) -> int` tells a reader everything. In practice Haskell programmers write top-level signatures **anyway**, by convention — which is an admission that the inference is more valuable for locals than for interfaces.

**3. It does not survive contact with the features you want.** Add subtyping, or overloading, or mutable references, and complete inference stops working. **Haskell's own `1 + True` shows the seam:**

```
No instance for (Num Bool) arising from the literal ‘1’
```

**That is not a unification failure** — it is a *type class* failure, because Haskell's `1` has type `Num a => a` rather than `Int`. **Haskell is not HM; it is HM plus a constraint system bolted alongside**, and Week 8 is about what that bolt costs.

**The modern consensus is local inference:** annotate at boundaries, infer inside them. **Rust, Swift, Scala, C# and Go all do this**, and so does Cyan.

---

## 8. What to Take Away

1. **Inference is simultaneous equations over types.** Generate constraints by walking the tree; solve them by unification.
2. **Unification is four cases**, and `prune` makes it near-linear.
3. **The occurs check is what makes it terminate** — `\x -> x x` demands an infinite type.
4. **The algorithm derives structure nobody stated**: `\f -> \x -> f (f x)` gets `(t -> t) -> t -> t` from the shape of the application alone.
5. **The principal type theorem** is the difference between inference and a good guess.
6. **Let-polymorphism is where the power lives**, and generalising only at `let` is what keeps inference decidable.
7. **Cyan annotates deliberately** — for error locality and for documentation, not because inference is difficult.
8. **Haskell's `1 + True` error is a type-class error, not a unification error.** That seam is Week 8.

---

## Exercises

1. Trace the inference of `\f -> \x -> f (f x)` by hand. Write every equation, in order, and say which step forces `f`'s argument and result to be the same.
2. `\x -> x x` fails the occurs check. **Give a different expression that fails it**, and one that looks like it should but does not.
3. The composed type is `(t3 -> t4) -> (t2 -> t3) -> t2 -> t4`. **Rename the variables so the type reads naturally** as "compose", then say why the algorithm did not produce your names.
4. `let id = \x->x in id (id 1)` type-checks, **and so does `(\id -> id (id 1)) (\x -> x)`** — even though the second is lambda-bound. Explain why this pair does *not* demonstrate let-polymorphism, and what would have to change about the body for it to.
5. §5 says every valid type of `\x -> x` is an instance of `t0 -> t0`. **Give the substitution** that produces `[int] -> [int]`.
6. §7 argues annotations give better error locality. **Construct a Cyan program and a Haskell program with the same bug**, and compare where each compiler points.
7. Cyan infers `let` and nothing else. **What would break if Cyan also inferred parameter types?** Consider mutual recursion between two functions, and what order the three passes in L07 §4 would have to run in.

---

*Next week: the front end is finished. Week 4 turns the typed tree into an intermediate representation — the form a compiler actually optimises — and Midterm 1 covers everything to here.*
