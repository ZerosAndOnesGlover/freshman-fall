# CS 211 · Programming Languages & Compilers I
## Week 3 · Lecture 1 of 2
### Symbol Tables, Scope, and the First Phase That Says No

---

**Reading:** Dragon §2.7, §6.5, §5.1–5.2 · **Next:** L08, type inference and unification

---

## 1. The Tree Is Built and Means Nothing

Week 2 delivered an AST. Here is a program it accepts happily:

```cyan
fn f() -> int {
    return zzz + true;
}
```

**Every token is legal. The grammar is satisfied. The tree is well-formed.** And the program is nonsense: `zzz` was never declared, and you cannot add a boolean to anything.

**This is the phase that notices.** Semantic analysis is the first one that can reject a program the parser was perfectly happy with — and L02 §8 already told you why it has to be a separate phase. *Declared before use*, *arity matches*, *types agree*: none of those are context-free, and a grammar cannot express them.

**Two jobs, and they interleave:**

| | |
|---|---|
| **Name resolution** | For every use of a name, find its declaration — or report that there is none |
| **Type checking** | For every expression, compute a type — or report that it has none |

They interleave because you cannot type `x + 1` without knowing what `x` *is*, and you cannot know that without resolving the name.

---

## 2. The Symbol Table

**A symbol table maps names to what the compiler knows about them.** For Cyan that is a type; for a real compiler it is also storage class, mutability, source position, and eventually a machine location.

The Dragon Book draws it as a column running the full height of the phase diagram, beside every phase rather than inside one. **That is accurate.** The parser can create entries, the type checker fills them in, Week 4's IR generator reads them to allocate slots, and Week 5's register allocator rewrites them. **It is the one structure the whole compiler shares.**

---

## 3. Scope Is a Chain, Not a Table

The naive symbol table is one dictionary. **It is wrong immediately**, because the same name can mean different things in different places:

```cyan
fn shadow(n: int) -> int {
    let a = n;                 // depth 1
    if a > 0 {
        let a = a * 2;         // depth 2 -- shadows the outer a
        while a > 10 {
            let a = a - 1;     // depth 3 -- shadows again
            n = n + a;
        }
    }
    return a;                  // the depth-1 one
}
```

**Three different variables, all called `a`.** The implementation is a chain of scopes:

```python
class Scope:
    def __init__(self, parent=None):
        self.names = {}
        self.parent = parent

    def lookup(self, name):
        s = self
        while s is not None:
            if name in s.names:
                return s.names[name]
            s = s.parent
        return None
```

**`lookup` walks outward and stops at the first hit.** That single loop *is* lexical scoping. Shadowing is not a feature anyone implemented — it is what falls out of stopping at the first match rather than the last.

**And note where the scopes come from:** `check_block` creates one per block, so the braces you were forced to write in Week 0 (L02 §6, the dangling else) turn out to be the scope boundaries too. **One syntactic decision, two payoffs.**

### Lexical versus dynamic scope

**Lexical** (or *static*) scope: a name refers to the declaration that lexically encloses its use. **You can resolve every name by reading the source**, with no idea what runs when. Cyan, C, Java, Python, Haskell, Rust.

**Dynamic** scope: a name refers to the most recent declaration on the *call stack*. Emacs Lisp, early Lisps, shell variables, and — as a deliberate opt-in — Perl's `local`.

```
fn f() { return x; }        // which x?
fn g() { let x = 1; return f(); }
fn h() { let x = 2; return f(); }
```

**Under lexical scope this program does not compile** — `x` in `f` resolves to nothing, and that is the answer at compile time. **Under dynamic scope `g()` returns 1 and `h()` returns 2**, and you cannot know which without running it.

> **Lexical scope won, and the reason is this phase.** A compiler that can resolve every name
> statically can also type-check every expression statically, allocate every local to a known slot,
> and inline with confidence. **Dynamic scope makes all three impossible**, which is a very high
> price for the flexibility it buys.

---

## 4. Declaration Order, and Why Functions Are Different

```cyan
fn odd(n: int) -> bool  { return even(n - 1); }
fn even(n: int) -> bool { return odd(n - 1); }
```

**`odd` calls `even` before `even` is declared, and this type-checks.** *(Verified.)* But:

```cyan
fn f() -> int { let a = b; let b = 1; return a; }
```

```
line 1 col 25: undefined variable 'b'
```

**Same file, opposite answers.** The rule is that **locals must be declared before use and functions need not be** — and the implementation is why:

```python
# Pass 2: function signatures, so calls may precede declarations.
for d in prog.decls:
    if d.kind == 'Fn':
        self.globals.declare(d.name, sig, 0)

# Pass 3: bodies.
for d in prog.decls:
    if d.kind == 'Fn':
        self.check_fn(d)
```

**Two passes over the top level.** All signatures are collected before any body is checked, so by the time `odd`'s body is examined, `even` is in the table. **Locals get one pass**, in statement order, so `b` is genuinely not there yet.

**This is a language design decision, not a technical necessity.** C originally required declaration before use for functions too, which is why C has *forward declarations* and header files. **Cyan's two-pass approach removes the need for either** — at the cost of the compiler having to make two passes, which nobody minds.

**Structs get an even earlier pass**, because a function signature may mention a struct type:

```python
# Pass 1: struct names, so types can refer to them.
```

**Three passes, in dependency order.** Add generics in Week 8 and you will need a fourth.

---

## 5. What "Type Checking" Actually Does

For each expression node, compute a type from its children's types, or fail.

```python
if op in self.ARITH:
    if op == '+' and lt == STR and rt == STR:
        return STR
    if lt != INT or rt != INT:
        err(e, f"'{op}' needs int operands, found {lt!r} and {rt!r}")
    return INT
```

**That is the whole shape of the phase**, repeated per node kind. The interesting content is in what the rules *refuse*.

**Cyan has no implicit conversions at all.** Not `int` to `bool`, not `int` to `string`:

```
line 2 col 6: if condition must be bool, found int
```

**C would have accepted `if 1`.** C says any scalar is a truth value, zero being false. **That buys brevity and costs you `if (x = 1)`** — the assignment-instead-of-comparison bug, which is a `bool` in C and a type error in Cyan.

**The trade, once more:** Cyan's rule means `while 1 { }` does not compile and you must write `while true { }`. **That is a real cost paid by every programmer, every day, to remove a class of bug.** Whether it is worth it is a genuine question — Go agrees with Cyan, C and Python do not.

### The eighteen refusals

**Every one of these parses.** *(All verified.)*

| Program | Type error |
|---|---|
| `1 + true` | `'+' needs int operands, found int and bool` |
| `return zzz;` | `undefined variable 'zzz'` |
| `if 1 { }` | `if condition must be bool, found int` |
| `g(1,2)` where `g` takes one | `expected 1 argument(s), found 2` |
| `g(true)` where `g` takes `int` | `argument 1 should be int, found bool` |
| `fn f() -> int { return true; }` | `function returns int but this returns bool` |
| `let a = b; let b = 1;` | `undefined variable 'b'` |
| `let a = 1; let a = 2;` | `'a' is already declared in this scope` |
| `a[0]` where `a: int` | `cannot index a value of type int` |
| `a[true]` | `array index must be int, found bool` |
| `p.zz` | `struct 'P' has no field 'zz'` |
| `new P { x: 1 }` missing `y` | `struct 'P' is missing field(s): y` |
| `[1, true]` | `array elements have differing types: int and bool` |
| `1 == true` | `cannot compare int with bool` |
| `a = true` where `a: int` | `cannot assign bool to a target of type int` |
| `a()` where `a: int` | `cannot call a value of type int` |
| `1 && 2` | `'&&' needs bool operands, found int and int` |
| `let a = [];` | `cannot infer the type of an empty array literal` |

**The last one is the interesting one**, and §6 is about it.

---

## 6. Where the Positions Come From

Look at those messages again:

```
line 4 col 5: '+' needs int operands, found int and bool
```

**Line 4, column 5 is where the `+` is** — not where the statement started, not where the function started. To say that, the type checker needs a position **on the `Binary` node**.

**And that is a problem, because by now the tokens are gone.** The lexer had positions (Week 1). The parser consumed the tokens and built a tree. **If the parser did not copy the position onto each node, the information no longer exists anywhere.**

```python
class Node:
    def __init__(self, kind, line=0, col=0, **kw):
```

> **This is the retrofit Week 1 warned about, arriving one level up.** PS 1 required positions on
> tokens and nothing in Week 1 read them. PS 2 required positions on nodes and nothing in Week 2
> read them. **This week reads both**, and a student who skipped either requirement now gets to add
> a field to every one of thirty AST constructors while their type checker sits half-written.
>
> **Every phase from here adds a field that the next phase needs.** Week 4 attaches types to nodes
> for the IR generator; Week 5 attaches liveness to IR instructions. **Build the field when the
> phase that produces it runs, not when the phase that needs it fails.**

---

## 7. What to Take Away

1. **This is the first phase that says no** to a program the parser accepted — and it must be separate, because the rules it enforces are not context-free.
2. **A symbol table maps names to knowledge**, and it is shared by every phase rather than owned by one.
3. **Scope is a chain, and `lookup` walking outward *is* lexical scoping.** Shadowing is a consequence, not a feature.
4. **Blocks open scopes**, so Week 0's mandatory braces pay a second dividend.
5. **Lexical scope won because it makes this phase possible**; dynamic scope defers every question to runtime.
6. **Declaration order is a design decision.** Cyan takes three passes so that functions and structs may be used before declaration, and locals may not.
7. **No implicit conversions** costs keystrokes and removes a bug class. C chose the other way.
8. **A position must be recorded by the phase that has it**, because no later phase can recover it.

---

## Exercises

1. `lookup` stops at the first match walking outward. **What would change if it walked to the *last* match instead?** Would any program change meaning, or would some stop compiling?
2. Cyan allows shadowing. Rust warns about it; Java forbids it for locals. **Give one concrete bug shadowing causes, and one concrete case where forbidding it is annoying.**
3. §4 shows mutual recursion working between functions but not between locals. **Write a Cyan program where two *locals* would need to refer to each other**, and say what the compiler would have to do to support it.
4. `let a = [];` fails because an empty array literal has no inferrable element type. **Give three ways a language could fix this**, and name a language that uses each.
5. C accepts `if (x = 1)`. **Write the Cyan equivalent** and say exactly which rule from §5 rejects it. Is it the same rule that rejects `if 1`?
6. The three passes in §4 run structs, then signatures, then bodies. **Construct a Cyan program that would break if signatures ran before structs.**
7. Suppose the parser recorded positions on statements but not expressions. **Which of §5's eighteen messages would get worse, and how much worse?** Pick the three that suffer most.

---

*Next: L08 — what happens when the annotations are not there at all. Hindley-Milner infers the most general type of an expression with no help, and it does it by generating equations and solving them.*
