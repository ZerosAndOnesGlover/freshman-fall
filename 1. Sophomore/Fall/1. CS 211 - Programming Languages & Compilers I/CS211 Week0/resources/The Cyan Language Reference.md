# The Cyan Language · Reference
## CS 211 · The language you will spend thirteen weeks compiling

---

> **This file is the specification.** When your compiler and this document disagree, this document is
> right. It is fixed as of Week 0 and changes exactly once, in **Week 8**, when you extend it with
> generics yourself as Problem Set 8.
>
> **The grammar below is verified unambiguous** — 23 valid programs each parse to exactly one tree
> and 9 malformed ones to zero, plus 33 expressions and 11 malformed expressions, checked
> mechanically. The checker is `lab/cfg_count.py`, and Lab 0 has you run it.

---

## 1. A Complete Program

```cyan
struct Point {
    x: int;
    y: int;
}

fn dist2(p: Point, q: Point) -> int {
    let dx = p.x - q.x;
    let dy = p.y - q.y;
    return dx * dx + dy * dy;
}

fn fib(n: int) -> int {
    if n < 2 { return n; }
    return fib(n - 1) + fib(n - 2);
}

fn main() -> int {
    let a = new Point { x: 0, y: 0 };
    let b = new Point { x: 3, y: 4 };
    let adder = fn(k: int) -> int { return k + fib(10); };
    return dist2(a, b) + adder(1);
}
```

Every construct in Cyan appears above except `while`, arrays, and `else`.

---

## 2. Lexical Structure

*(Implemented in Week 1.)*

| Token class | Definition |
|---|---|
| `IDENT` | `[A-Za-z_][A-Za-z0-9_]*`, not a keyword |
| `INT` | `[0-9]+` — decimal only; no hex, no underscores, no negative literals |
| `STRING` | `"` … `"` with escapes `\n`, `\t`, `\\`, `\"` |
| Keywords | `fn` `let` `if` `else` `while` `return` `struct` `new` `true` `false` `int` `bool` `string` |
| Operators | `+` `-` `*` `/` `%` `==` `!=` `<` `<=` `>` `>=` `&&` `\|\|` `!` `=` `->` |
| Punctuation | `(` `)` `{` `}` `[` `]` `,` `;` `:` `.` |
| Comments | `//` to end of line; `/*` … `*/`, **not nested** |
| Whitespace | space, tab, newline, CR — separates tokens, otherwise ignored |

**There is no negative integer literal.** `-5` is unary minus applied to `5`. This matters in Week 1: the lexer never produces a token for `-5`, only `-` then `5`.

**Maximal munch.** The lexer always takes the longest match. `<=` is one token, never `<` then `=`; `identifier` is one token, never `ident` then `ifier`.

---

## 3. The Grammar

EBNF. `{ X }` is zero or more, `[ X ]` is optional, `|` is alternation. Quoted items are terminals; `IDENT`, `INT` and `STRING` are the token classes above.

### Declarations

```ebnf
program     ::= { decl }
decl        ::= fn_decl | struct_decl | let_stmt

fn_decl     ::= "fn" IDENT "(" [ params ] ")" [ "->" type ] block
struct_decl ::= "struct" IDENT "{" { field } "}"
field       ::= IDENT ":" type ";"
params      ::= param { "," param }
param       ::= IDENT ":" type
```

A function with no `-> type` returns nothing, and `return;` is the only legal return in it.

### Types

```ebnf
type        ::= "int" | "bool" | "string"
              | "[" type "]"
              | "fn" "(" [ type { "," type } ] ")" "->" type
              | IDENT
```

`IDENT` as a type is a struct name. `[int]` is an array of `int`. `fn(int, int) -> bool` is a function type, and function types are first class — they can be parameters, locals and return types.

### Statements

```ebnf
block       ::= "{" { stmt } "}"
stmt        ::= let_stmt | assign_stmt | if_stmt
              | while_stmt | return_stmt | expr_stmt

let_stmt    ::= "let" IDENT [ ":" type ] "=" expr ";"
assign_stmt ::= lvalue "=" expr ";"
lvalue      ::= IDENT | lvalue "[" expr "]" | lvalue "." IDENT
if_stmt     ::= "if" expr block [ "else" ( if_stmt | block ) ]
while_stmt  ::= "while" expr block
return_stmt ::= "return" [ expr ] ";"
expr_stmt   ::= expr ";"
```

**Branch and loop bodies are `block`s, so braces are mandatory.** This is what makes the grammar free of the dangling-else ambiguity — see L02 §6.

**`lvalue` is a separate non-terminal on purpose.** `3 = 4;` is a *syntax* error in Cyan, not a type error, because no derivation of `lvalue` produces an integer literal.

### Expressions

```ebnf
expr        ::= or_expr
or_expr     ::= and_expr { "||" and_expr }
and_expr    ::= cmp_expr { "&&" cmp_expr }
cmp_expr    ::= add_expr [ ( "==" | "!=" | "<" | "<=" | ">" | ">=" ) add_expr ]
add_expr    ::= mul_expr { ( "+" | "-" ) mul_expr }
mul_expr    ::= unary { ( "*" | "/" | "%" ) unary }
unary       ::= [ "-" | "!" ] postfix
postfix     ::= primary { "(" [ args ] ")" | "[" expr "]" | "." IDENT }
primary     ::= INT | STRING | "true" | "false" | IDENT
              | "(" expr ")" | array_lit | struct_lit | fn_lit
args        ::= expr { "," expr }
array_lit   ::= "[" [ args ] "]"
struct_lit  ::= "new" IDENT "{" [ inits ] "}"
inits       ::= init { "," init }
init        ::= IDENT ":" expr
fn_lit      ::= "fn" "(" [ params ] ")" [ "->" type ] block
```

### Precedence and associativity, as a table

Highest binding first. This table is *derived from* the grammar above, not additional to it.

| Level | Operators | Associativity |
|---|---|---|
| 1 | `f(…)` `a[i]` `x.f` | left |
| 2 | unary `-` `!` | right (prefix) |
| 3 | `*` `/` `%` | left |
| 4 | `+` `-` | left |
| 5 | `==` `!=` `<` `<=` `>` `>=` | **non-associative** |
| 6 | `&&` | left |
| 7 | `\|\|` | left |

**Comparison is non-associative**, so `a < b < c` is a syntax error rather than the silent nonsense C produces. Write `a < b && b < c`. See L02 §7 for why three languages answer this three different ways.

**`new Point { … }` needs its keyword.** Without `new`, `if p { }` could not be distinguished from an `if` whose condition is a struct literal `p { }`. Rust hits exactly this problem and solves it by banning struct literals in condition position; Cyan spends a keyword instead and keeps the grammar context-free with no special case.

---

## 4. Semantics — the parts the grammar cannot state

*(Enforced in Week 3.)*

**Typing.** Static and mostly inferred. `let` without an annotation takes the type of its initialiser; parameters and return types must always be annotated. There is **no implicit conversion of any kind** — not `int` to `bool`, not `int` to `string`. `if 1 { }` is a type error.

| Operator | Operand types | Result |
|---|---|---|
| `+` `-` `*` `/` `%` | `int`, `int` | `int` |
| `+` | `string`, `string` | `string` (concatenation) |
| `<` `<=` `>` `>=` | `int`, `int` | `bool` |
| `==` `!=` | two of the same type | `bool` |
| `&&` `\|\|` | `bool`, `bool` | `bool` |
| unary `-` | `int` | `int` |
| unary `!` | `bool` | `bool` |

**Division.** `/` truncates toward zero and `%` takes the sign of the left operand — **C's rule, not Python's**, because Cyan compiles to one `idiv` and refuses to pay for a correction step. `n / 0` and `n % 0` are runtime errors that abort.

**Scoping is lexical.** A `block` opens a scope; a name is visible from its declaration to the end of its enclosing block. Shadowing an outer name is legal. Functions may be called before their declaration at top level; locals may not be used before theirs.

**Closures capture by reference**, and a captured local outlives the frame it was declared in. This is the single feature that forces a heap and therefore Week 6's collector.

**Evaluation order is left to right**, and every operator including `&&` and `||` is fully specified — `&&` and `||` short-circuit. **Cyan has no undefined behaviour.** Every program either produces a value, aborts with a named runtime error, or fails to compile.

**Integers are 64-bit signed and wrap on overflow.** Wrapping is *defined*, unlike C's signed overflow, which is undefined — CS 201 Week 1 covers why that distinction matters to an optimiser.

---

## 5. Runtime Errors

These abort the program with a message and a non-zero exit status:

| Error | When |
|---|---|
| `division by zero` | `/` or `%` with a zero right operand |
| `index out of bounds` | `a[i]` with `i < 0` or `i >= len(a)` |
| `null field access` | reading a field of an uninitialised struct reference |

**Bounds are checked on every array access.** That is a deliberate refusal of C's design, and Week 5 asks you to measure what it costs and then optimise most of the checks away.

---

## 6. What Cyan Does Not Have

Named here so you do not go looking:

**No `for` loop** — `while` is enough, and desugaring `for` is an exercise in Week 10.
**No modules or imports** — one file is the whole program.
**No generics until Week 8** — you add them, as PS 8.
**No mutable global state** — top-level `let` is a constant.
**No exceptions** — runtime errors abort; there is no handler.
**No floating point.** Deliberate: it would double the type rules and add nothing this course teaches that CS 201 Week 1 did not already cover better.

---

## 7. Files and the Compiler

| | |
|---|---|
| Source extension | `.cy` |
| Compiler | `cyanc`, written in Python 3 |
| Invocation | `python3 cyanc.py program.cy` |
| Dump flags | `--dump-tokens`, `--dump-ast`, `--dump-types`, `--dump-tac`, `--dump-ssa`, `--dump-llvm` |

**The dump flags are the debugging method of this course**, not a convenience. They appear in Week 1 with `--dump-tokens` and each later phase adds one. When output is wrong, dump each representation in order and find the first that surprises you.

---

*CS 211 · The Cyan Language Reference · Week 0 · © CSE Department*
