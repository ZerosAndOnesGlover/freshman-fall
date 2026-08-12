# CS 211 · Problem Set 2
## A Recursive Descent Parser for Cyan

---

**Released:** Week 2, Wednesday · **Due:** Week 3, Friday 17:00
**Total: 100 points** · Submit one PDF (`PS2_{LastName}_{StudentID}.pdf`) **and** `parser.py`

> **This is the second vertebra of the compiler.** It consumes the `Token` list your PS 1 lexer
> produces and emits an AST that Week 3's type checker will annotate. **The AST node shapes you
> choose here you will live with for the rest of the term** — PS 3, PS 4 and both projects all walk
> this tree.
>
> If your PS 1 lexer is not working, use `lab/lexer.py` from Week 1 and say so. **You will not lose
> marks here for a Week 1 defect**, and carrying a broken lexer forward costs you far more.

---

### Q1: FIRST, FOLLOW, and LL(1) (18 points)

Use this grammar:

```bnf
S  ::= "let" IDENT "=" E ";" | E ";"
E  ::= E "+" T | T
T  ::= T "*" F | F
F  ::= IDENT | NUM | "(" E ")"
```

**(a) [6]** Compute FIRST and FOLLOW for `S`, `E`, `T` and `F`. Show them as a table.

**(b) [4]** **Is this grammar LL(1)?** If not, list every conflict as *(non-terminal, lookahead token, the two competing productions)*.

**(c) [4]** Eliminate the left recursion. Give the transformed grammar, and recompute FIRST and FOLLOW for the new non-terminals only.

**(d) [4]** The `S` rule has two productions. **After the transformation, is `S`'s choice LL(1)?** Answer with reference to FIRST sets — and note that `let` is a keyword while `E` can begin with `IDENT`.

---

### Q2: Left Recursion, Three Ways (16 points)

**(a) [5]** Apply the textbook elimination rule to

```bnf
mul_expr ::= mul_expr ("*" | "/" | "%") unary | unary
```

Write out the transformed pair of rules.

**(b) [5]** Now write the **loop** version, as a parser function in the style of `parse_add` from L05 §3.

**(c) [6]** The transformed grammar of (a) builds a **right-leaning** tree; the loop of (b) builds a **left-leaning** one. **The language requires left-leaning.**

Explain what a parser using (a)'s grammar must do to recover left associativity, and say why L05 claims the loop is "the same transformation folded into iteration".

---

### Q3: Reading a Conflict Report (22 points)

**(a) [8]** Run bison on the ambiguous dangling-else grammar (`lab/dangling.y`).

Report the number and kind of conflicts. Then run with `--report=all` and quote **state 6**. **Explain what the square brackets around one action mean.**

**(b) [6]** Run with `-Wcounterexamples`. It prints a shift derivation and a reduce derivation. **For each, state which `if` the `else` binds to.** Which did bison choose, and which mainstream language does that match?

**(c) [8]** Run bison on `lab/cyan.y` — the full Cyan grammar.

It reports conflicts. **Week 0 verified this grammar unambiguous** (23 valid programs, one tree each; 9 malformed, zero trees).

**Reconcile the two results.** Your answer must say precisely what bison is asserting, what it is *not* asserting, and why both results are correct. **This is the question the whole week is built around** — a vague answer earns few marks even if it gestures at the right idea.

---

### Q4: The Parser (36 points)

**Write `parser.py`** — a recursive descent parser for the whole of `The Cyan Language Reference` §3.

#### Required interface

```python
parse(src: str) -> Node          # returns the Program node
```

Node kinds, at minimum: `Program`, `Fn`, `Struct`, `Block`, `Let`, `Assign`, `If`, `While`, `Return`, `ExprStmt`, `Binary`, `Unary`, `Call`, `Index`, `Field`, `Var`, `Int`, `Str`, `Bool`, `Array`, `New`, `Lambda`, and the type nodes `TyPrim`, `TyArray`, `TyFn`, `TyName`.

Plus a dump mode:

```bash
$ python3 parser.py program.cy       # prints the AST
```

#### Requirements

1. **All seven precedence levels**, with the associativity `The Cyan Language Reference` §3 specifies.
2. **Comparison is non-associative.** `a < b < c` must be rejected with a message that suggests `a < b && b < c`.
3. **No `Paren` node.** `(1+2)*3` and `1+2*3` must differ only in tree shape — L01 §4.
4. **`else if` chains** parse without nesting a redundant `Block`.
5. **Assignment targets are checked.** `3 = 4;` must be rejected. You may do this in the grammar or as a shape check on the parsed expression — **state which you chose in your PDF and why.**
6. **Errors carry a line and column**, taken from the token. `expected ';', found '}'` with no position earns no marks for error quality.

#### Verification

Your parser must produce these exact shapes. *(Written as s-expressions for brevity; your dump format may differ.)*

| Input | Tree |
|---|---|
| `1+2*3` | `(+ 1 (* 2 3))` |
| `1*2+3` | `(+ (* 1 2) 3)` |
| `1-2-3` | `(- (- 1 2) 3)` |
| `-2*3` | `(* (- 2) 3)` |
| `a\|\|b&&c` | `(\|\| a (&& b c))` |
| `a&&b\|\|c` | `(\|\| (&& a b) c)` |
| `a.b.c` | `(fld (fld a b) c)` |
| `f(1)(2)` | `(call (call f 1) 2)` |
| `a[1][2]` | `(idx (idx a 1) 2)` |
| `-a.b` | `(- (fld a b))` |
| `(1+2)*3` | `(* (+ 1 2) 3)` |

**And must reject:** `1<2<3`, `1+`, `(1`, `1 2`, `3 = 4;`, `if x return 1;`, `let x = 1` *(no semicolon)*.

**It must parse `lab/sample.cy`** from Week 1 without error.

#### Marks

| | |
|---|---:|
| All eleven precedence/associativity shapes correct | 12 |
| All seven rejections, with useful messages | 8 |
| Declarations, statements and types — full grammar coverage | 8 |
| `sample.cy` parses; `else if` chains flat; no `Paren` node | 5 |
| Errors carry line and column | 3 |

---

### Q5: A Design Decision (8 points)

Requirement 5 let you check assignment targets either in the grammar or as a shape check.

**(a) [4]** State which you chose. Give the **error message** your parser produces for `3 = 4;`, verbatim.

**(b) [4]** L06 §5 showed that the grammatical version costs two reduce/reduce conflicts in bison, while the shape check costs none. **`The Cyan Language Reference` specifies the grammatical version anyway.**

**Is the reference wrong?** Two or three sentences, distinguishing what a language specification is for from what a parser implementation is for.

---

## Marks

| Question | Topic | Points |
|---|---|---|
| Q1 | FIRST, FOLLOW, LL(1) | 18 |
| Q2 | Left recursion, three ways | 16 |
| Q3 | Reading a conflict report | 22 |
| Q4 | The parser | 36 |
| Q5 | A design decision | 8 |
| **Total** | | **100** |

---

*Quiz 3, at the start of Tuesday's lecture in Week 3, covers this week — recursive descent, left recursion, FIRST/FOLLOW, LL(1), shift-reduce, and conflict reports.*
