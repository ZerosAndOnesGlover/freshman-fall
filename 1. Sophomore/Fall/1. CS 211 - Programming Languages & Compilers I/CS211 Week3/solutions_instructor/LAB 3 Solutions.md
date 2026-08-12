# CS 211 · Lab 3 · Solutions and Checkoff Notes
## Instructor Only

---

**Lab 3 is unmarked.** These notes exist so the checkoff is consistent.

> **All outputs below were measured** with Python 3.14.2 and GHC 9.4.7 against the shipped starters.
> **Q14 is the checkoff that matters.**

---

## Part 1 — Scope Chains

### Q1 — Resolutions in `shadow`

```cyan
fn shadow(n: int) -> int {
    let a = n;                 // DECL depth 1
    if a > 0 {                 // use -> depth 1
        let a = a * 2;         // DECL depth 2; the `a` on the right is depth 1
        let b = a;             // DECL depth 2; use -> depth 2
        while b > 10 {         // use -> depth 2
            let a = b - 1;     // DECL depth 3; `b` is depth 2
            b = a;             // target depth 2; value depth 3
        }
        return b;              // use -> depth 2
    }
    return a;                  // use -> DEPTH 1
}
```

**The final `return a;` is the one to press on.** It sits outside the `if`, so depths 2 and 3 are gone. **It resolves to the depth-1 declaration**, whose value is `n` — unaffected by everything the `if` did.

### Q1b — `shadow_bug`, which never terminates

**The one-character fix: delete the `let`.** `a = a - 1;` assigns to the depth-2 variable the `while` is testing; `let a = a - 1;` declares a fresh depth-3 one and leaves the loop condition untouched forever.

**Why the type checker passes it.** Termination is a **semantic property of executions**, not of types — and it is undecidable in general (the halting problem). **Nothing in this course catches it.** Cyan's type system answers "do the operations agree about their operand types", and every operation here does.

**Worth saying explicitly:** a type checker's silence is not a claim of correctness. It is a claim about one specific class of error.

**On the design question**, all three positions are defensible and the marks — this being a checkoff — are for engaging with the trade:

| | |
|---|---|
| **Cyan / Python: permit silently** | Shadowing is genuinely useful in nested scopes; warning on every case is noise |
| **Rust: permit but warn** | Catches this bug; costs a warning on deliberate shadowing, which Rust idiom uses a lot |
| **Java: forbid for locals** | Cannot happen; costs you the ability to reuse an obvious name in an inner scope |

**A student who says "Java is obviously right" should be asked** what they would rename the inner variable to in a five-level-deep loop nest.

### Q2 — Shadowing falls out of `lookup`

```python
def lookup(self, name):
    s = self
    while s is not None:
        if name in s.names: return s.names[name]
        s = s.parent
    return None
```

**It returns on the first hit, walking inward-to-outward.** Nothing anywhere implements shadowing; it is what "stop at the first match" *means* when scopes are nested.

**Accept:** "because it stops at the first match rather than continuing". **Push back on** any answer implying there is shadowing logic elsewhere.

### Q3 — Walking to the last match

```python
def lookup(self, name):
    found, s = None, self
    while s is not None:
        if name in s.names: found = s.names[name]
        s = s.parent
    return found
```

**`scopes.cy` still type-checks** — all three `a`s are `int`, so no type error appears. **That is the interesting part**: the change is invisible to the type checker and completely changes the program's meaning.

**To expose it**, a student needs a value difference. The simplest:

```cyan
fn f() -> int {
    let a = 1;
    if true { let a = 2; return a; }     // innermost: 2   outermost: 1
    return 0;
}
```

**Accept any program that distinguishes them.** A student who says "nothing changes" has not tried hard enough — ask them to make the inner and outer declarations different values.

**Check they reverted `lookup`** before Part 2.

### Q4 — Where scopes come from

```
$ echo 'fn f() { { let a = 2; } }' | python3 parser.py
error: line 1 col 10: unexpected '{'
```

*(Measured.)* **A bare block is a parse error** — `The Cyan Language Reference` §3's `stmt` has no `block` alternative.

**Scopes come from `if` blocks and `while` blocks** (plus function bodies and lambda bodies).

**The connection to L02 §6:** braces were made mandatory to kill the dangling-else ambiguity. **They turn out to also be the scope boundaries**, so one syntactic decision paid twice. **Full marks require naming both payoffs.**

---

## Part 2 — Errors With Positions

### Q5

```
error: line 4 col 5: '+' needs int operands, found int and bool
```

*(Measured.)* **Line 4, column 5 is the `+` itself.** The `return` statement began on line 3.

### Q6 — Which token

**The operator token.** In `parse_add`:

```python
ln, cl = self.pos()          # position of the operator, before eating it
op = self.eat('OP').text
node = Node('Binary', line=ln, col=cl, op=op, lhs=node, rhs=self.parse_mul())
```

**Why it is right:** the error is *about the operator* — it is `+` that demanded two `int`s. Pointing at the left operand would blame `x`, which is fine; pointing at the operator blames the thing that imposed the requirement.

**Accept a student who argues for the left operand** if they justify it — some compilers do point at the expression start. **Do not accept** "it doesn't matter".

### Q7 — Breaking positions

With `line`/`col` forced to 0, `err()` produces `?: '+' needs int operands...`.

**Can the checker recover the position?** **No.** The tokens existed while the parser ran, but `check()` receives only the AST. **The token list is not passed to the checker and, in a real compiler, has been freed.**

**The answer to look for:** the information exists at one moment and one moment only, and if it is not copied then, it is gone.

**Check they reverted `parser.py`.**

### Q8

Any three of L07 §5's eighteen. **The marking point is that they predicted line and column before running** — the habit, not the answers.

---

## Part 3 — Inference

### Q9 — The six types

| Expression | Type |
|---|---|
| `\x -> x` | `t0 -> t0` |
| `\x -> x + 1` | `int -> int` |
| `\f -> \x -> f (f x)` | `(t3 -> t3) -> t3 -> t3` |
| `\x -> \y -> x` | `t0 -> t1 -> t0` |
| `\f -> \g -> \x -> f (g x)` | `(t3 -> t4) -> (t2 -> t3) -> t2 -> t4` |
| `\x -> if x <= 0 then 1 else x` | `int -> int` |

*(Measured.)*

**Why `f`'s argument and result unify in `f (f x)`:** the *result* of the inner `f x` is passed as the *argument* to the outer `f`, so `f`'s result type must unify with `f`'s argument type.

### Q10 — The trace for `\x -> if x <= 0 then 1 else x`

```
assign x : t0
unify(t0, int)         -- <= demands int on the left
unify(int, int)        -- and on the right
unify(bool, bool)      -- the condition must be bool
unify(int, int)        -- both branches must agree
```

*(Measured — five steps.)*

**Accept four to six steps** depending on whether the student writes the condition check separately.

### Q11 — GHC cross-check

```
i     :: p -> p
twice :: (t -> t) -> t -> t
comp  :: (t1 -> t2) -> (t3 -> t1) -> t3 -> t2
```

*(Measured, GHC 9.4.7.)*

**The structures match exactly; only the variable names differ.** That is not a disagreement because **type variables are bound** — a type is defined up to renaming of its quantified variables, exactly as $\lambda x.x$ and $\lambda y.y$ are the same function.

**The principal type theorem is why this is expected**: there is exactly one most-general type, so two correct implementations must find it.

### Q12 — The occurs check

```
\x -> x x  ->  TYPE ERROR -- occurs check: cannot construct infinite type t0 = t0 -> t1
```

**The equation:** applying `x` to itself requires `x : t0` and `x : t0 -> t1`, hence $t_0 = t_0 \to t_1$.

**No finite type satisfies it** — substituting repeatedly gives $t_0 = (t_0 \to t_1) \to t_1 = ((t_0 \to t_1) \to t_1) \to t_1$, growing without bound.

### Q13 — Removing the guard

**The algorithm builds a cyclic type structure**, and the first thing that walks it — `prune`, `repr`, or `free_vars` — recurses forever. **Expect a `RecursionError` or a hang**, depending on where it is hit first.

**Warn students before they run it** and be ready with Ctrl-C.

### Q14 — **Let-polymorphism, and the trap**

```
let f = \x->x in if f true then f 1 else 2        : int
(\f -> if f true then f 1 else 2) (\x->x)         : TYPE ERROR -- cannot unify bool with int
let id = \x->x in id (id 1)   [both OK]           : int
(\id -> id (id 1)) (\x->x)     [both OK]          : int
```

*(All measured. GHC agrees on the first pair — the `let` compiles, the lambda gives
`Couldn't match expected type 'Bool' with actual type 'Int'`.)*

**The demonstrating pair is the first.** `f` is used at `bool -> bool` in the condition and `int -> int` in the branch — **two genuinely different types**, which only a generalised (`let`-bound) variable can supply.

**Why `id (id 1)` does not demonstrate it:** **both occurrences of `id` are used at `int -> int`.** The inner call takes an `int` and returns one; the outer call takes that `int` and returns one. **No polymorphism is required, so the lambda form works too.**

**Checkoff standard.** The student must say that the `id` pair needs `id` at only **one** type. **A student who says "the lambda version fails because lambda-bound variables aren't generalised" has the rule right but has not noticed it does not apply here** — press them, because it is precisely the case where reciting the rule gives the wrong answer.

### Q15 — Limitation or choice?

**A deliberate choice.** Generalising lambda-bound variables gives **System F**, whose type inference is **undecidable**. HM restricts generalisation to `let` in order to keep complete inference with no annotations.

**Accept:** "it's the price of decidable inference". **Week 8** is where the restriction is lifted, with annotations supplied by hand.

---

## Part 4 — Where Haskell Is Not HM

### Q16

```
No instance for (Num Bool) arising from the literal ‘1’
```

*(Measured.)*

**What it implies:** in Haskell the literal `1` does **not** have type `Int`. It has type `Num a => a` — *any* type that is an instance of `Num`. So GHC unifies `a` with `Bool` successfully, and then fails on the **constraint** `Num Bool`, for which there is no instance.

**`hm.py` has no constraints**, so its `1` is simply `int` and the failure is a plain unification error.

**Full marks require noticing that GHC's unification succeeded** and the failure came afterwards.

### Q17

**Type classes** are bolted onto HM. **Week 8.**

---

## Checkoff Summary

| Part | Minimum to pass |
|---|---|
| **1** | Q1's four resolutions with `return a` at depth 1; Q3 demonstrated **and reverted**; Q4 naming both payoffs of mandatory braces |
| **2** | Q5's line 4 col 5; Q7 run, reverted, and the recoverability answered "no" |
| **3** | Six types; Q11's renaming argument; **Q14's trap explained** |
| **4** | Q16 distinguishing a class failure from a unification failure |

**If a student is short on time, cut Part 2's Q8 and Part 3's Q13.** Do not cut Q14.

**Two reverts to verify before they leave:** `Scope.lookup` (Q3) and `Node.__init__` (Q7). A student who leaves with either still broken will start PS 3 against a sabotaged toolchain.

---

*CS 211 · Lab 3 Solutions · Instructor Only*
