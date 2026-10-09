# CS 211 · Programming Languages & Compilers I
## Week 10 · Lecture 2 of 2
### Little Languages, and What They Cost

*“The utility of a language as a tool of thought increases with the range of topics it can treat, but decreases with the amount of vocabulary and the complexity of grammatical rules which the user must keep in mind. Economy of notation is therefore important.”* — Kenneth E. Iverson, "Notation as a Tool of Thought", Turing Award Lecture (1979), §1.4

---

**Reading:** Fowler, *Domain-Specific Languages* ch. 1–4 · Hudak (1996), "Building DSLs" · Bentley (1986), "Little Languages" · **Next:** L23, the complete mini-compiler

**Coursework:** 📝 **PS 9** due Fri this week 17:00 · 🔬 **Lab 10** Fri this week 14:00–15:50 · 📊 **Quiz 11** Tue of Week 11 · 📝 **PS 11** released Wed of Week 11, due Fri of Week 12 17:00

---

## 1. Two Ways to Build a Language

L21 moved the line between *language feature* and *library code*. Push that further and you get a **domain-specific language**: a notation designed for one problem, rather than for computation in general.

There are exactly two places to put one.

**An internal DSL** lives inside a host language, using whatever the host's syntax already allows — operator overloading, method chaining, blocks, macros. **An external DSL** has its own syntax, its own parser, and its own file format.

`circuit.py` builds the same circuit language both ways, so the comparison is concrete rather than rhetorical.

---

## 2. The Internal DSL: Five Methods

```python
class Node:
    # The internal DSL is these five lines.
    def __and__(self, o):    return Node('and', self, o)
    def __or__(self, o):     return Node('or', self, o)
    def __xor__(self, o):    return Node('xor', self, o)
    def __invert__(self):    return Node('not', self)
```

That is the whole implementation. And it works:

```python
a, b, cin = inputs("a b cin")
s1    = a ^ b
total = s1 ^ cin
carry = (a & b) | (s1 & cin)
```

```
  sum   = (xor (xor a b) cin)
  carry = (or (and a b) (and (xor a b) cin))
  gates, shared wires counted once: 5   (2 xor + 2 and + 1 or)
```

A full adder, with the correct truth table, and **five gates** — the textbook figure.

Note *why* it is five and not six. `sum` and `carry` both use `(xor a b)`, and in Python that is **one object with two references**. A shared subexpression is a shared wire. The counter has to know that:

```python
def gate_count(*nodes, seen=None):
    """The `seen` set must be shared between outputs, not reset per output.
    A full adder's `sum` and `cout` both use `xor(a, b)` -- that is ONE
    gate with two consumers, and counting it twice reports 6 where the
    textbook says 5."""
```

*(The first version of that function did reset `seen` per output and reported 6. The bug is instructive: the DSL was building a **DAG** and the tool was reading it as a **tree**, which is the single most common mistake in circuit and IR tooling — and Week 4's CFG had exactly the same shape.)*

**What the internal DSL cost:** nothing. No grammar, no parser, no file format. And it inherits Python's tooling entire — line numbers, the debugger, the profiler, the editor, the package manager.

**What it cannot do:** be spelled the way engineers speak. `nand(a, b)` has to be written `~(a & b)`, because Python has no `nand` operator and you may not add one. **An internal DSL is limited to what the host's grammar already permits**, permanently.

---

## 3. The External DSL: Its Own Syntax

```
in a b cin
s1   = xor(a, b)
sum  = xor(s1, cin)
c1   = and(a, b)
c2   = and(s1, cin)
cout = or(c1, c2)
```

That says what it means. `xor(a, b)` is how the operation is spoken and written in every other context an engineer meets it.

And the two agree:

```
  internal and external produce identical truth tables: True
```

**What the external DSL cost:** a grammar, a parser, and from now on you own the error messages, the editor support, the syntax highlighting, and every question of the form "why does this not work". §5 measures the last of those, and it is worse than people expect.

| | internal | external |
|---|---|---|
| implementation | 5 operator methods | a grammar and a parser |
| notation | limited to the host's grammar | anything you can parse |
| `nand(a,b)` | `~(a & b)` | `nand(a, b)` |
| errors, debugger, tooling | **the host's, free** | **yours, from scratch** |
| a non-programmer can read it | rarely | often, and that is usually the point |

> **The question is not which is better. It is who reads it.** A DSL that hardware engineers,
> accountants or biologists will read and write is worth an external syntax and the tooling bill
> that comes with it. A DSL that only your own team will touch is almost always better internal,
> because the bill is large and it never stops arriving.

---

## 4. Parser Combinators: The Grammar as a Value

If you do build an external DSL, you need a parser. Week 2 wrote one by hand — one function per non-terminal, `parse_expr` calling `parse_add` calling `parse_mul`.

**A parser combinator is a parser that is a value.**

```python
NUMBER = regex(r'\d+(?:\.\d+)?') >> (lambda t: int(t))
atom   = lazy(lambda: NUMBER | (seq(lit('('), expr, lit(')')) >> (lambda v: v[1])))
term   = seq(atom, many(seq(lit('*') | lit('/'), atom))) >> _fold
expr   = seq(term, many(seq(lit('+') | lit('-'), term))) >> _fold
```

**Four lines**, and they are the grammar:

```
expr := term (('+'|'-') term)*
term := atom (('*'|'/') atom)*
atom := NUMBER | '(' expr ')'
```

Three operators carry it: `|` is alternation, `+` is sequencing, `>>` maps a function over a result. Everything else — `many`, `sep_by`, `lazy` — is built from those.

```
  1 + 2                    => 3        ok
  2 + 3 * 4                => 14       ok
  (2 + 3) * 4              => 20       ok
  1 + 2 * (3 - 1) / 2      => 3.0      ok
```

*(Each checked against Python's own `eval` of the same string.)*

**Two things that are only visible when the grammar is a value.**

**`expr` is an object.** You can print it, store it in a dictionary, pass it to a function, or *generate* it. Week 2's parser existed only as the shape of a call graph, and a call graph is not something a program can inspect.

**Associativity lives in the fold, not the grammar.**

```
  10 - 2 - 3  parses as  ('-', ('-', 10, 2), 3)
```

`_fold` walks the operator list left to right, so `-` comes out left-associative. **Change `_fold` and you change associativity without touching a single production** — where a hand-written recursive-descent parser would need the recursion restructured.

**And `lazy` is Week 7's thunk.** A grammar is recursive, and Python is strict: at the moment you write `expr` inside `atom`, `expr` does not exist. `lazy(lambda: ...)` delays it. Same mechanism, same reason, entirely different setting.

---

## 5. What Combinators Do Not Fix

Two costs, and the second is the one nobody puts in the tutorial.

**Left recursion still kills you.**

```python
bad_expr = lazy(lambda: (seq(bad_expr, lit('+'), NUMBER) >> _fold) | NUMBER)
```

```
  => RecursionError: infinite recursion before reading a token
```

**This is Week 2's problem, unchanged.** A left-recursive rule calls itself before consuming input, so a top-down parser never terminates — and combinators *are* recursive descent with the call graph reified, so they inherit every limitation of it. Week 2's fix (rewrite the grammar, put the recursion on the right, recover associativity in a fold) is still the fix. **Nothing was solved; the same solution is just written differently.**

**And the error messages get worse.** Same two inputs, two parsers:

| input | Week 2's hand-written parser | the combinators |
|---|---|---|
| `(1 + 2` | `line 1 col 30: expected PUNCT ')', found PUNCT ';'` | `expected number or ')' at '(1 + 2'` |
| `1 +` | `line 1 col 28: unexpected ';'` | `trailing input at '+'` |

**The hand-written parser names the line, the column, what it wanted and what it found. The combinator points at the beginning of the input.**

The cause is structural rather than sloppy. Alternation **backtracks**: when `a | b` fails, it has thrown away everything both branches learned and can only report at the position where the whole alternation started. Getting good errors out of combinators requires committing to a branch once you are sure — `try`/`cut` in the parser-combinator literature — and every serious combinator library has some version of it, precisely because the naive behaviour is unusable.

> **The grammar went from 357 lines to 4, and the diagnostics went from excellent to unusable.**
> That is the trade, it is real, and it is why production compilers — clang, rustc, GHC — use
> hand-written recursive-descent parsers despite every one of those teams knowing exactly what a
> combinator is. **They are optimising for the error message, because that is what users
> actually interact with.**

---

## 6. Macros in Languages That Are Not Lisp

L21's macros were easy because Lisp code is already a data structure. Everyone else has to work for it.

**C preprocessor macros** operate on the **token stream**, before parsing. They know nothing about syntax, types or scope — which is why `#define SQ(x) x*x` breaks on `SQ(1+2)`, why every macro is wrapped in defensive parentheses, and why `SWAP(x,t)` captures (L21 §7). **Not hygienic, not syntax-aware, and still in every C codebase on earth.**

**Rust procedural macros** take a `TokenStream` and return a `TokenStream`. Syntax-aware, hygienic, and they run inside the compiler — which is how `#[derive(Debug)]` generates an implementation from a struct definition, and how `#[tokio::main]` rewrites a function.

**C++ templates** are a macro system nobody designed as one. They are Turing-complete *by accident* — discovered in 1994, not intended — which is why template metaprogramming produces famously unreadable errors: you are running a program at compile time in a language never meant to be programmed in. `constexpr` and `consteval` are the retrofit.

**Java annotation processors and Go's `go:generate`** are the same idea with the reflection turned all the way down: read the source, write a new file, compile that.

| | operates on | hygienic? | when |
|---|---|---|---|
| Lisp `defmacro` | **lists — the AST itself** | no (use `gensym`) | expansion |
| Scheme `syntax-rules` | patterns over syntax | **yes** | expansion |
| C preprocessor | **tokens** | **no** | before parsing |
| Rust `macro_rules!` | token trees | **yes** | after parsing |
| Rust proc-macro | `TokenStream` | yes | inside the compiler |
| C++ template | types | n/a | instantiation |

**The pattern is that everyone reinvents homoiconicity badly.** Lisp's macros are simple because the representation was already there. Every other language bolts on a second representation — a token stream, a `TokenStream`, an annotation model — and pays for it in complexity and error quality.

---

## 7. Code Generation, and When Not to Have a Language

Not every little language needs to be executed. Many are read once and turned into code:

- **Protocol Buffers, Thrift, Cap'n Proto** — a schema, and generated serialisers for ten languages.
- **ANTLR, bison, flex** — a grammar, and a generated parser. Week 2 used `cyan.y` and this is what it was.
- **OpenAPI, GraphQL schemas** — an interface, and generated clients and servers.

The shared property: **one description, many consumers.** A `.proto` file is the reason a Go service and a Python client agree about a message, and neither one is the source of truth.

And the shared cost: **a build step**. Generated code is checked in or it is not; either way something can be stale, the debugger steps into code nobody wrote, and the error messages point at generated line numbers. **That is the same bill as §5, arriving in a different envelope.**

> **The honest test for whether a DSL is worth it** is not "would a notation be nicer here". It is:
> *is this description read by more than one consumer, or by people who are not programmers?* If
> neither, a library of ordinary functions will serve better and cost far less — and the ordinary
> functions come with a debugger.

---

## 8. What to Take From This

1. **Internal DSLs cost almost nothing and are limited to the host's grammar** — five operator methods gave a working circuit language; `nand(a,b)` still has to be `~(a & b)`.
2. **External DSLs say what you mean and hand you the whole tooling bill** — errors, editors, highlighting, and every "why doesn't this work".
3. **The deciding question is who reads it**, not which is more elegant.
4. **A shared subexpression is a shared wire.** Counting the full adder as a tree gives 6 gates; as a DAG, 5 — the same tree-versus-DAG mistake as Week 4's CFG.
5. **Parser combinators make the grammar a value** — four lines instead of a call graph, inspectable and generable.
6. **Associativity lives in the fold**, so it can be changed without touching a production.
7. **`lazy` is Week 7's thunk**, delaying a recursive definition in a strict host.
8. **Left recursion is not fixed** — combinators are recursive descent with the call graph reified, and they inherit its limits exactly.
9. **The grammar shrank from 357 lines to 4 and the error messages became unusable.** That is why clang, rustc and GHC all hand-write their parsers.
10. **Everyone reinvents homoiconicity badly.** Lisp's macros are simple because the representation was already there; every other system bolts on a second one.
11. **Generated code is worth it when one description has many consumers** — and it always costs a build step and a debugger that steps into code nobody wrote.

**Next week the compiler is assembled end to end** — every phase from Week 0 to Week 6, running one program — and Project 1 is due.

---

*CS 211 · Week 10 · Lecture 22 · © CSE Department*
