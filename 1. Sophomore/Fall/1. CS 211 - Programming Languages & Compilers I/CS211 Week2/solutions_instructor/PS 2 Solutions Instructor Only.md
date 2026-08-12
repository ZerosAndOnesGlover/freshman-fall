# CS 211 · Problem Set 2 · Solutions
## Instructor Only

---

> **All FIRST/FOLLOW sets and conflict counts below were computed** with `lab/first_follow.py` and
> bison 3.8.2. Parser output was checked against the reference `parser.py`.

---

## Q1: FIRST, FOLLOW, and LL(1) (18)

Grammar: `S ::= "let" IDENT "=" E ";" | E ";"`, plus the usual `E`/`T`/`F` ladder.

### (a) [6]

| | FIRST | FOLLOW |
|---|---|---|
| `S` | `let`, `(`, `IDENT`, `NUM` | `$` |
| `E` | `(`, `IDENT`, `NUM` | `)`, `+`, `;` |
| `T` | `(`, `IDENT`, `NUM` | `)`, `*`, `+`, `;` |
| `F` | `(`, `IDENT`, `NUM` | `)`, `*`, `+`, `;` |

*(Measured.)*

**Mark scheme:** 3 for FIRST, 3 for FOLLOW. **−1** per missing element. The most-missed entry is **`;` in FOLLOW(`E`)**, from `S → E ";"`.

### (b) [4] Not LL(1) — six conflicts

```
E on '(':     ('E','+','T')  vs  ('T',)
E on 'IDENT': ('E','+','T')  vs  ('T',)
E on 'NUM':   ('E','+','T')  vs  ('T',)
T on '(':     ('T','*','F')  vs  ('F',)
T on 'IDENT': ('T','*','F')  vs  ('F',)
T on 'NUM':   ('T','*','F')  vs  ('F',)
```

*(Measured.)*

**Six, not four** — this grammar's `F` has three alternatives where L05's had two, so each left-recursive pair conflicts on three lookahead tokens rather than two.

**Mark scheme:** 4 for all six with the competing productions named. **2** for correctly identifying left recursion as the cause but listing fewer.

### (c) [4] After elimination

```bnf
S  ::= "let" IDENT "=" E ";" | E ";"
E  ::= T E'          E' ::= "+" T E' | ε
T  ::= F T'          T' ::= "*" F T' | ε
F  ::= IDENT | NUM | "(" E ")"
```

| | FIRST | FOLLOW |
|---|---|---|
| `E'` | `+`, ε | `)`, `;` |
| `T'` | `*`, ε | `)`, `+`, `;` |

*(Measured. The grammar is now LL(1), with a 20-entry table.)*

**Mark scheme:** 2 grammar, 2 sets.

### (d) [4] Is `S` LL(1)?

**Yes.** FIRST(`"let" IDENT "=" E ";"`) = `{let}`. FIRST(`E ";"`) = `{(, IDENT, NUM}`. **Disjoint**, so one token decides.

**The point of the question:** `let` is a *keyword*, and Week 1's lexer already separated keywords from identifiers by a set lookup (L03 §4). **If it had not — if `let` arrived as `IDENT` — the two productions would both start with `IDENT` and `S` would not be LL(1).**

**Full marks require noticing that the lexer is what makes this work.** An answer of "yes, they're disjoint" with no mention of keyword/identifier separation earns 2 of 4.

---

## Q2: Left Recursion, Three Ways (16)

### (a) [5] Textbook elimination

```bnf
mul_expr  ::= unary mul_expr'
mul_expr' ::= ("*" | "/" | "%") unary mul_expr' | ε
```

**Mark scheme:** 5. **−2** if the operator is left in `mul_expr` rather than moved into the tail.

### (b) [5] The loop

```python
def parse_mul(self):
    node = self.parse_unary()
    while self.peek() and self.peek().kind == 'OP' and self.peek().text in ('*', '/', '%'):
        op = self.eat('OP').text
        node = Node('Binary', op=op, lhs=node, rhs=self.parse_unary())
    return node
```

**The load-bearing line is `lhs=node`** — rebuilding with the accumulated tree on the left is what produces left association.

**Mark scheme:** 5. **−3** for `rhs=node` or for building a right-leaning tree.

### (c) [6] Recovering associativity

**What (a)'s parser must do:** `mul_expr'` is right-recursive, so a naive parser building a node per recursive call produces `a * (b * c)`. To get `(a * b) * c` it must **thread the left-hand tree down as an inherited attribute** — `mul_expr'` takes the tree built so far as a parameter, combines it with the operand it just read, and passes the *result* into its own recursive call.

**Why the loop is the same transformation:** `mul_expr' ::= op unary mul_expr' | ε` is **tail recursive**, and the accumulator being threaded through it is exactly the loop variable `node`. **Converting tail recursion with an accumulator into a loop is mechanical**, and the loop version does it without the reader having to see the intermediate grammar at all.

**Mark scheme:** 3 for the accumulator/inherited-attribute answer, 3 for the tail-recursion connection. **A student who says only "the loop is simpler" earns 2** — the question asks *why they are the same thing*.

---

## Q3: Reading a Conflict Report (22)

### (a) [8] The dangling else

**1 shift/reduce conflict.** State 6:

```
    1 stmt: IF E stmt •  [$end, ELSE]
    2     | IF E stmt • ELSE stmt

    ELSE  shift, and go to state 7

    ELSE      [reduce using rule 1 (stmt)]
    $default  reduce using rule 1 (stmt)
```

**The square brackets mark the action bison disabled.** It kept the shift; the bracketed reduce is shown so you can see what the resolution discarded.

**Mark scheme:** 3 count/kind, 3 quoting state 6, 2 for the brackets. **A student who reads the brackets as an additional action earns 0 of the 2** — it is the single most common misreading, and worth calling out in review.

### (b) [6] The counterexample

- **Shift derivation** — the `ELSE` sits inside the inner `stmt`: **binds to the inner (nearest) `if`.**
- **Reduce derivation** — the inner `if` reduces first: **binds to the outer `if`.**

**bison chose shift**, which matches **C** (and C++, Java, C#, JavaScript — any of these earns the mark).

**Mark scheme:** 2 per derivation, 2 for the choice and the language.

### (c) [8] Reconciling bison with Week 0 — **the question of the week**

**Full marks require all three claims:**

**1. The grammar is not ambiguous.** Week 0's parse-tree counter gave **exactly one tree** to each of 23 valid programs and zero to 9 malformed ones. Ambiguity would mean some program has two trees; none does.

**2. bison asserts only that the grammar is not LALR(1).** It could not construct a deterministic parse table with one token of lookahead in a merged LR(1) automaton. **That is a property of a parsing method**, and it is decidable.

**3. bison cannot assert ambiguity, because ambiguity is undecidable** (L02 §8). No tool answers it in general. bison checks a *sufficient* condition for determinism; failing it means **"not proved"**, not **"disproved"**.

**Why this grammar fails it concretely:** at `IDENT` beginning a statement, the parser must reduce toward `lvalue` (heading for `x[i] = ...`) or toward `prim` (heading for `x[i] < y;`). **The distinguishing token — the `=` — can be arbitrarily far to the right**, past a whole `expr`. No fixed lookahead $k$ helps.

**Mark scheme:** 3 for (1) with the Week 0 evidence, 3 for (2), 2 for (3). **An answer asserting the grammar is ambiguous earns 0**, however well argued — it contradicts a mechanical verification the student was given.

**Partial credit worth giving:** a student who says "bison is more restrictive than the class of unambiguous grammars" has (2) and (3) in substance and should get 5–6 even if phrased loosely.

---

## Q4: The Parser (36)

### Reference implementation

The shipped `lab/` files do **not** include a parser — unlike Week 1, where the lexer was given. **Students write this one cold**, which is why it carries 36 points rather than 26.

### The eleven shapes

| Input | Required tree |
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

*(All eleven verified against the reference parser.)*

**The three that separate a correct parser from a nearly-correct one:**

- **`-2*3` → `(* (- 2) 3)`.** Unary binds tighter than `*`. A parser that calls `parse_unary` at the wrong level gives `(- (* 2 3))`.
- **`-a.b` → `(- (fld a b))`.** Postfix binds tighter than unary — the *opposite* nesting from the previous case. **Both must be right**, and getting one usually breaks the other if the levels are misordered.
- **`a&&b||c` → `(|| (&& a b) c)`.** `&&` tighter than `||`. Students who copy C's precedence table from memory usually get this; students who guess sometimes invert it.

### The seven rejections

| Input | Expected |
|---|---|
| `1<2<3` | non-associative comparison, message suggesting `a < b && b < c` |
| `1+` | unexpected end of input |
| `(1` | expected `)` |
| `1 2` | trailing tokens after a complete expression |
| `3 = 4;` | left-hand side not assignable |
| `if x return 1;` | expected `{` |
| `let x = 1` | expected `;` |

**Reference messages**, for calibration:

```
line 1: comparison is non-associative; write 'a < b && b < c'
line 1 col 14: expected PUNCT '{', found KEYWORD 'return'
line 1 col 19: expected PUNCT ';', found PUNCT '}'
line 1: left-hand side of '=' is not assignable
```

### Mark breakdown

| | | Notes |
|---|---:|---|
| Eleven shapes | 12 | ~1 each; award proportionally |
| Seven rejections with useful messages | 8 | 1 each, plus 1 for message quality overall |
| Full grammar coverage | 8 | declarations, structs, types, lambdas, arrays, `new` |
| `sample.cy`; flat `else if`; no `Paren` node | 5 | |
| Line and column on errors | 3 | |

**Four failure modes worth naming:**

1. **A `Paren` node in the AST.** Costs 2 of the 5. It is not merely redundant — Week 4's code generator would have to skip it at every use, and Week 5's optimiser again.
2. **`else if` nested inside a spurious `Block`.** Costs 1. Check with `fn f(){ if a { } else if b { } else { } }` and count nodes: **4 `Block`s** — the function body plus one per branch — and **2 `If`s**. *(Measured.)* A parser that wraps the `else if` in its own block reports 5 and 2.
3. **Comparison implemented as a loop** (like `+`), making it left-associative rather than rejecting. **Costs the rejection mark and one shape mark** — and is worth a comment, because it silently accepts a construct the reference grammar forbids.
4. **Positions dropped.** Students who did not carry `line`/`col` in PS 1 cannot produce them here. **Do not double-penalise** — if PS 1 already lost the 4 position marks, take only the 3 here.

---

## Q5: A Design Decision (8)

### (a) [4]

**Either choice is correct.** Award for a verbatim message with a position, and for correctly stating which mechanism produced it.

- **Grammatical (`lvalue` non-terminal):** the message will be a parse failure — `expected ';', found '='` or similar.
- **Shape check:** the message can be specific — `left-hand side of '=' is not assignable`.

**A student with no position in the message loses 2.**

### (b) [4] Is the reference wrong?

**No.** Expected argument:

- **A specification says what the language is.** `lvalue` states the rule in the same formalism as the rest of the document, so a reader needs no extra prose and no knowledge of any parsing technology.
- **An implementation is constrained by its tooling.** LALR(1) cannot express this rule deterministically, so bison-based implementations encode it as a check instead. **The language is the same either way.**

**Mark scheme:** 4 for the specification/implementation distinction. **2** for "no, because the shape check enforces the same rule" — true but missing why the reference is *entitled* to state it differently. **0** for "yes, the reference should match bison."

---

## Mark Distribution

| Question | Points | Common failure |
|---|---:|---|
| Q1 | 18 | Missing `;` in FOLLOW(`E`); not seeing the lexer's role in (d) |
| Q2 | 16 | Right-leaning tree in the loop version |
| Q3 | 22 | **Misreading the brackets; claiming Cyan is ambiguous** |
| Q4 | 36 | `-a.b` versus `-2*3`; a `Paren` node |
| Q5 | 8 | "The reference should change" |
| **Total** | **100** | |

**Q3(c) is the one to review in class**, and it is worth ten minutes rather than two. The distinction between *undecidable* and *not proved by this tool* recurs in Week 5 (does this optimisation preserve semantics?) and Week 11 (why the student's own compiler reports a conflict). **If the cohort average on Q3(c) is below 60%, do not move on to Week 4 without revisiting it.**

---

*CS 211 · PS 2 Solutions · Instructor Only*
