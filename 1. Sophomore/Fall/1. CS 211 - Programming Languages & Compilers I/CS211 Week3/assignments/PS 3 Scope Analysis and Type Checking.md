# CS 211 · Problem Set 3
## Scope Analysis and Type Checking

---

**Released:** Week 3, Wednesday · **Due:** Week 4, Friday 17:00
**Total: 100 points** · Submit one PDF (`PS3_{LastName}_{StudentID}.pdf`) **and** `typecheck.py`

> **Third vertebra.** It consumes the AST from PS 2 and annotates every expression node with a type.
> Week 4's IR generator reads those annotations, so `e.ty` must actually be *set*, not merely
> computed and discarded.
>
> **Midterm 1 is in Week 4 and covers Weeks 0–3.** This problem set is the best revision available
> for the semantic-analysis third of it.

---

### Q1: Scope by Hand (16 points)

```cyan
fn f(a: int) -> int {
    let b = a + 1;
    if b > 0 {
        let a = b * 2;
        let c = a + b;
        while c > 0 {
            let b = c - 1;
            c = b;
        }
        return a;
    }
    return b;
}
```

**(a) [8]** **Draw the scope tree.** One node per scope, showing which names each declares and its depth. Cyan's parameters live in the function scope; each `block` opens a child.

**(b) [4]** For **every** use of `a`, `b` and `c` in the body, state which declaration it resolves to, by depth. There are eleven uses.

**(c) [4]** `return a;` inside the `if` and `return b;` at the end resolve to declarations at different depths. **Give both**, and say what would change if `lookup` returned the *outermost* match rather than the innermost.

---

### Q2: Declaration Order (14 points)

**(a) [5]** This type-checks:

```cyan
fn odd(n: int) -> bool  { return even(n - 1); }
fn even(n: int) -> bool { return odd(n - 1); }
```

This does not:

```cyan
fn f() -> int { let a = b; let b = 1; return a; }
```

**Explain both**, in terms of the passes `check_program` makes.

**(b) [4]** L07 §4 says the checker makes **three** passes over the top level: structs, then signatures, then bodies. **Construct a program that breaks if signatures run before structs**, and say exactly which lookup fails.

**(c) [5]** C requires functions to be declared before use, which is why it has forward declarations and header files. **Cyan does not. Name one thing C gains** from its stricter rule — think about what a C compiler can do in a single pass that Cyan's cannot.

---

### Q3: Inference by Hand (22 points)

Use the HM rules from L08. **Show every equation.**

**(a) [6]** Infer the type of `\x -> \y -> x y`. Give the final type and the unifications that produced it.

**(b) [6]** Infer the type of `\f -> \x -> f (f x)`. **Say precisely which step forces `f`'s argument and result types to unify.**

**(c) [4]** `\x -> x x` fails the occurs check. **Write the equation that cannot be solved**, and explain in one sentence why no finite type satisfies it.

**(d) [6]** Both of these are HM-typeable:

```
let f = \x -> x in if f true then f 1 else 2
(\f -> if f true then f 1 else 2) (\x -> x)
```

…except that **one is not.** Say which, give the error, and explain the rule that separates them. **Then explain why `let id = \x->x in id (id 1)` and its lambda form are *both* fine** — this pair is a trap, and saying why is most of the marks.

---

### Q4: The Type Checker (40 points)

**Extend your PS 2 parser with `typecheck.py`**, implementing `The Cyan Language Reference` §4 in full.

#### Required interface

```python
check(src: str) -> (ast, checker)      # raises TypeError_ on failure
```

Every expression node must carry `e.ty` after a successful check.

#### Requirements

1. **A scope chain**, not a flat dictionary. Blocks open scopes; `lookup` walks outward.
2. **Three passes** at the top level — structs, signatures, bodies — so functions and structs may be used before declaration.
3. **Redeclaration in the same scope is an error**; shadowing in a nested scope is not.
4. **No implicit conversions.** `if 1` is a type error, as is `1 == true`.
5. **Every error message carries a line and column**, taken from the offending node. This is what PS 2 Requirement 7 was for.
6. **`e.ty` is set on every expression node**, including ones whose type you did not need.

#### It must reject all eighteen

Each of these **parses cleanly** and must be rejected. *(All verified against the reference.)*

| | |
|---|---|
| `1 + true` | `1 == true` |
| `zzz` undefined | `a = true` where `a: int` |
| `if 1 { }` | `a()` where `a: int` |
| wrong argument count | `1 && 2` |
| wrong argument type | `let a = [];` |
| wrong return type | `a[0]` where `a: int` |
| `let a = b; let b = 1;` | `a[true]` |
| `let a = 1; let a = 2;` | `p.zz` — no such field |
| `[1, true]` | `new P { x: 1 }` missing `y` |

#### It must accept all of these

```cyan
fn odd(n: int) -> bool { return even(n - 1); }   // mutual recursion
fn even(n: int) -> bool { return odd(n - 1); }
fn f() { let a = 1; if true { let a = 2; } }     // shadowing
fn g(h: fn(int) -> int) -> int { return h(1); }  // function-typed parameter
fn s() -> string { return "a" + "b"; }           // string concatenation
fn l() { let k = fn(x: int) -> int { return x + 1; }; k(1); }
```

Plus `lab/scopes.cy` and Week 1's `lab/sample.cy`.

#### Marks

| | |
|---|---:|
| All eighteen rejections, with correct messages | 14 |
| All six acceptances, plus both sample files | 8 |
| Scope chain with correct shadowing and redeclaration rules | 6 |
| Three-pass structure | 4 |
| Every message carries an accurate line **and column** | 5 |
| `e.ty` set on every expression node | 3 |

---

### Q5: A Rule You Choose (8 points)

`The Cyan Language Reference` §4 gives `+` on two `string`s. It says nothing about `*`.

**(a) [4]** **Add `string * int`** — `"ab" * 3` is `"ababab"` — to your checker. Give the rule as you would write it in the reference, in the style of §4's table.

**(b) [4]** **Is `3 * "ab"` legal in your version?** State your choice and defend it. Python allows both; C has neither. **Name what your choice costs**, and be specific — "it's less flexible" is not an answer.

---

## Marks

| Question | Topic | Points |
|---|---|---|
| Q1 | Scope by hand | 16 |
| Q2 | Declaration order | 14 |
| Q3 | Inference by hand | 22 |
| Q4 | The type checker | 40 |
| Q5 | A rule you choose | 8 |
| **Total** | | **100** |

---

*Quiz 4, at the start of Tuesday's lecture in Week 4, covers this week. **Midterm 1 is also in Week 4**, covering Weeks 0–3 — see the revision guide in Week 4's resources.*
