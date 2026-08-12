# CS 211 · Problem Set 3 · Solutions
## Instructor Only

---

> **All inference results below were produced by `lab/hm.py`** and cross-checked against GHC 9.4.7.
> **All type-checker outputs** are from `lab/typecheck.py`.

---

## Q1: Scope by Hand (16)

### (a) [8] The scope tree

```
depth 0  globals            { f }
 depth 1  f's params        { a : int }
  depth 2  f's body block   { b }
   depth 3  if-block        { a, c }
    depth 4  while-block    { b }
```

**Five scopes.** Note that Cyan's parameters sit in a scope *outside* the body block, so a body-level `let a` would shadow a parameter rather than collide with it.

**Mark scheme:** 5 for the shape, 3 for correct name placement. **−2** for putting parameters in the same scope as the body — it changes whether `let a` at body level is legal.

### (b) [4] The eleven uses

| Line | Use | Resolves to |
|---|---|---|
| `let b = a + 1;` | `a` | depth 1 (parameter) |
| `if b > 0` | `b` | depth 2 |
| `let a = b * 2;` | `b` | depth 2 |
| `let c = a + b;` | `a` | **depth 3** (just declared) |
| | `b` | depth 2 |
| `while c > 0` | `c` | depth 3 |
| `let b = c - 1;` | `c` | depth 3 |
| `c = b;` | `c` | depth 3 |
| | `b` | **depth 4** |
| `return a;` (inside `if`) | `a` | **depth 3** |
| `return b;` (at end) | `b` | **depth 2** |

**Mark scheme:** 4, deducting ~0.5 per error. **The two most-missed are `let c = a + b` — where `a` is the just-declared depth-3 one — and the two returns.**

### (c) [4] The two returns

`return a;` inside the `if` → **depth 3**. `return b;` at the end → **depth 2**.

**If `lookup` returned the outermost match**, `a` would resolve to the parameter (depth 1) and `b` to depth 2 throughout, changing the function's value. **The program would still type-check** — all the names are `int` — which is the point worth making: the change is invisible to the type checker and completely alters the meaning.

**Mark scheme:** 2 for the two depths, 2 for noting it still type-checks.

---

## Q2: Declaration Order (14)

### (a) [5]

**Mutual recursion works** because `check_program` collects **all** function signatures in pass 2 before checking **any** body in pass 3. By the time `odd`'s body is examined, `even` is in the global scope.

**`let a = b; let b = 1;` fails** because statements inside a body are checked in **one pass, in order**. When `let a = b` is checked, `b` has not been declared, and `lookup` returns `None`.

```
line 1 col 25: undefined variable 'b'
```

**Mark scheme:** 3 for the two-pass explanation, 2 for the single-pass one. **A student who says only "functions are global" earns 2** — the question asks about passes.

### (b) [4] Signatures before structs

```cyan
fn area(p: Point) -> int { return p.x * p.y; }
struct Point { x: int; y: int; }
```

**If signatures ran before structs**, resolving `Point` in `area`'s parameter list would fail: `resolve_type` looks in `self.structs`, which is still empty.

```
unknown type 'Point'
```

**Mark scheme:** 2 for a correct program, 2 for naming `resolve_type`'s lookup as the failure.

### (c) [5] What C gains

**Single-pass compilation.** A C compiler that requires declaration before use can emit code as it reads, without holding the whole translation unit in memory — which mattered enormously on 1970s hardware and is why C has header files at all.

**Also accept:** simpler implementation; the ability to compile a file that is larger than memory; deterministic name resolution without a fixpoint.

**Mark scheme:** 5 for single-pass or an equivalent. **2** for "it's simpler" with no reason. **Do not accept** "it catches more errors" — it does not.

---

## Q3: Inference by Hand (22)

### (a) [6] `\x -> \y -> x y`

```
assign x : t0
assign y : t1
unify(t0, t1 -> t2)        -- x is applied to y
```

**Result: `(t1 -> t2) -> t1 -> t2`.** *(Measured.)*

**Mark scheme:** 4 for the equations, 2 for the final type. Accept any consistent variable naming.

### (b) [6] `\f -> \x -> f (f x)`

```
assign f : t0
assign x : t1
unify(t0, t1 -> t2)        -- inner f x
unify(t0, t2 -> t3)        -- outer f applied to the inner result
```

**The forcing step is the second unification.** `f`'s argument type was already fixed to `t1` by the inner application; the outer application demands `f` accept `t2`, the *result* of the inner one. Unifying `t1 -> t2` with `t2 -> t3` forces `t1 = t2` and `t2 = t3`.

**Result: `(t3 -> t3) -> t3 -> t3`.** *(Measured. GHC: `(t -> t) -> t -> t`.)*

**Mark scheme:** 4 equations, 2 for identifying the forcing step. **Full marks require naming *which* unification does it** — the question asks precisely that.

### (c) [4] The occurs check

**Equation: $t_0 = t_0 \to t_1$.**

Applying `x` to itself requires `x : t0` (as the argument) and `x : t0 -> t1` (as the function), so those must unify.

**No finite type satisfies it:** substituting repeatedly gives $t_0 = (t_0 \to t_1) \to t_1 = ((t_0 \to t_1) \to t_1) \to t_1 = \cdots$, growing without bound.

**Mark scheme:** 2 equation, 2 explanation.

### (d) [6] The trap — **the question of the set**

**The lambda version fails:**

```
let f = \x->x in if f true then f 1 else 2     : int
(\f -> if f true then f 1 else 2) (\x->x)      : TYPE ERROR -- cannot unify bool with int
```

*(Measured. GHC agrees: `Couldn't match expected type 'Bool' with actual type 'Int'`.)*

**The rule:** HM **generalises at `let`** — a `let`-bound variable's unconstrained type variables become universally quantified, and each use instantiates them freshly. **Lambda-bound variables are not generalised**, so `f` has one monomorphic type and cannot be both `bool -> bool` and `int -> int`.

**Why `id (id 1)` is fine in both forms:** **both uses of `id` are at `int -> int`.** The inner call takes an `int` and returns an `int`; the outer takes that `int` and returns an `int`. **No polymorphism is needed**, so nothing distinguishes the two binding forms.

**Mark scheme:** 2 for identifying the failing one with its error, 2 for the generalisation rule, **2 for the `id` explanation**. **A student who states the rule correctly but claims `id (id 1)` also fails in lambda form earns 4 of 6** — they have memorised the rule without checking whether it applies, which is exactly what the question tests.

---

## Q4: The Type Checker (40)

`lab/typecheck.py` is the model answer and students have had it since Friday of Week 3. **Mark for a working implementation, not originality**; a verbatim copy is a plagiarism matter, not a marking one.

### The eighteen rejections

**All verified.** Each program **parses cleanly**.

| Program | Reference message |
|---|---|
| `1 + true` | `'+' needs int operands, found int and bool` |
| `return zzz;` | `undefined variable 'zzz'` |
| `if 1 { }` | `if condition must be bool, found int` |
| `g(1,2)`, `g` takes 1 | `expected 1 argument(s), found 2` |
| `g(true)`, `g` takes int | `argument 1 should be int, found bool` |
| `fn f() -> int { return true; }` | `function returns int but this returns bool` |
| `let a = b; let b = 1;` | `undefined variable 'b'` |
| `let a = 1; let a = 2;` | `'a' is already declared in this scope` |
| `a[0]`, `a: int` | `cannot index a value of type int` |
| `a[true]` | `array index must be int, found bool` |
| `p.zz` | `struct 'P' has no field 'zz'` |
| `new P { x: 1 }` missing `y` | `struct 'P' is missing field(s): y` |
| `[1, true]` | `array elements have differing types: int and bool` |
| `1 == true` | `cannot compare int with bool` |
| `a = true`, `a: int` | `cannot assign bool to a target of type int` |
| `a()`, `a: int` | `cannot call a value of type int` |
| `1 && 2` | `'&&' needs bool operands, found int and int` |
| `let a = [];` | `cannot infer the type of an empty array literal` |

**Wording need not match**; the *category* must.

### Mark breakdown

| | | Notes |
|---|---:|---|
| Eighteen rejections | 14 | ~0.8 each |
| Six acceptances + both sample files | 8 | Mutual recursion and the function-typed parameter are the two that catch people |
| Scope chain, shadowing, redeclaration | 6 | Test with `scopes.cy` |
| Three-pass structure | 4 | Verify by putting a `struct` *after* the function using it |
| Line **and column** on every message | 5 | |
| `e.ty` set on every expression node | 3 | Walk the tree post-check and assert |

**Four failure modes:**

1. **A flat symbol table with save/restore** instead of a chain. Often works, but breaks on `scopes.cy`'s three-deep nesting. **Costs the 6 scope marks** if it gives wrong resolutions.
2. **Types compared by identity rather than structure.** `Ty('array', (INT,)) == Ty('array', (INT,))` must be true. Students who forget `__eq__` get baffling failures on arrays.
3. **Column missing, line present.** Costs 2 of 5. Usually means the node took its position from the statement rather than the operator.
4. **`e.ty` computed but not assigned.** Costs the 3 marks, and **breaks Week 4 silently** — worth a comment on the script rather than just a deduction.

---

## Q5: A Rule You Choose (8)

### (a) [4]

In `The Cyan Language Reference` §4's table style:

| Operator | Operand types | Result |
|---|---|---|
| `*` | `string`, `int` | `string` (repetition) |

Implementation, in `check_binary`:

```python
if op == '*' and lt == STR and rt == INT:
    return STR
```

**placed before the int-int check**, exactly as the existing `+`/string case is.

**Mark scheme:** 2 for the rule as a reference-style entry, 2 for correct placement.

### (b) [4] Is `3 * "ab"` legal?

**Both answers earn full marks with a real cost named.**

| Choice | Argument | Cost |
|---|---|---|
| **Symmetric** (Python's) | `*` is commutative for numbers, so users expect it to be here | Two rules instead of one; and it is a *lie* — string repetition is not commutative in any meaningful sense, since `"ab" * 3` and `3 * "ab"` only coincide because one is defined as the other |
| **Left-only** | One rule; the asymmetry is honest, since the string is the thing being repeated | `3 * "ab"` is a type error that reads like it should work, and users coming from Python will hit it |

**Mark scheme:** 2 for a stated choice, 2 for a specific cost. **"It's less flexible" earns 0 of the 2** — the question says so explicitly.

---

## Mark Distribution

| Question | Points | Common failure |
|---|---:|---|
| Q1 | 16 | Parameters placed in the body scope; `let c = a + b`'s `a` |
| Q2 | 14 | "It catches more errors" for (c) |
| Q3 | 22 | **Reciting the generalisation rule without checking it applies** |
| Q4 | 40 | `__eq__` on types; `e.ty` computed but unassigned |
| Q5 | 8 | Naming no concrete cost |
| **Total** | **100** | |

**Q3(d) is the one to review**, and it is worth doing right before Midterm 1 rather than after — the midterm covers Weeks 0–3, and a student who thinks `id (id 1)` demonstrates let-polymorphism will answer a midterm question on generalisation the same wrong way.

---

*CS 211 · PS 3 Solutions · Instructor Only*
