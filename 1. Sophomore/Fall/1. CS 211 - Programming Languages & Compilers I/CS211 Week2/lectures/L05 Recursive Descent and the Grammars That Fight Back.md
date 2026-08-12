# CS 211 · Programming Languages & Compilers I
## Week 2 · Lecture 1 of 2
### Recursive Descent, and the Grammars That Fight Back

---

**Reading:** Dragon §4.4 · **Next:** L06, bottom-up parsing and what bison is telling you

---

## 1. One Function Per Non-Terminal

Here is the whole idea of top-down parsing, and it is genuinely this simple:

> **Write one function for each non-terminal. Each function's body is its production.**

The Cyan grammar says:

```ebnf
if_stmt ::= "if" expr block [ "else" ( if_stmt | block ) ]
```

The parser says:

```python
def parse_if(self):
    self.eat('KEYWORD', 'if')
    cond = self.parse_expr()
    then = self.parse_block()
    els = None
    if self.accept('KEYWORD', 'else'):
        els = self.parse_if() if self.at('KEYWORD', 'if') else self.parse_block()
    return Node('If', cond=cond, then=then, els=els)
```

**Read the two side by side.** `"if"` became `eat('KEYWORD','if')`. `expr` became a call to `parse_expr`. The optional `[ ... ]` became an `if`. **The code is the grammar, transliterated**, and that correspondence is the entire appeal of the technique — when the grammar changes, you know exactly which function to edit.

**This is called *recursive descent***: recursive because the functions call each other as the grammar nests, descent because it builds the tree from the root down.

> **It builds a leftmost derivation.** At each step it expands the leftmost unexpanded non-terminal —
> which is exactly what "call `parse_expr` first, then handle what follows" does. L02 §3 said
> leftmost and rightmost derivations give the same tree; **this is the algorithm that produces the
> leftmost one**, and L06 gives you the one that produces the rightmost.

---

## 2. The Grammar Fights Back Immediately

Try the same transliteration on the expression grammar:

```ebnf
add_expr ::= add_expr ("+" | "-") mul_expr | mul_expr
```

```python
def parse_add(self):
    lhs = self.parse_add()      # <-- infinite recursion
    ...
```

**`parse_add` calls `parse_add` as its first action, having consumed nothing.** It never terminates, and it never even looks at a token.

**This is not a bug in the code. It is a structural incompatibility**: recursive descent must consume input before recursing, and a **left-recursive** rule recurses before consuming. Any grammar rule of the form $A \to A\alpha$ breaks it.

**And left recursion is not an accident of how the grammar was written** — L02 §5 established that it is precisely what makes `+` left-associative. **The grammar is left-recursive because the language requires it.** So the fix cannot be "write the grammar differently and accept different trees".

---

## 3. Eliminating Left Recursion

The standard transformation. Given

$$A \to A\alpha \mid \beta$$

*(that is: $A$ is a $\beta$ followed by any number of $\alpha$s)*, rewrite as

$$A \to \beta A' \qquad A' \to \alpha A' \mid \varepsilon$$

**Applied to the expression grammar:**

```ebnf
E  ::= T E'          E' ::= "+" T E' | ε
T  ::= F T'          T' ::= "*" F T' | ε
F  ::= n | "(" E ")"
```

**And this works.** Verified with an LL(1) checker:

```
=== Left-recursive E ::= E + T | T ===
  --> NOT LL(1): 4 conflict(s)
      E on 'n': ('E', '+', 'T')  vs  ('T',)
      E on '(': ('E', '+', 'T')  vs  ('T',)
      T on 'n': ('T', '*', 'F')  vs  ('F',)
      T on '(': ('T', '*', 'F')  vs  ('F',)

=== After left-recursion elimination ===
  --> LL(1). Table has 13 entries.
```

**But look at what it cost.** The tree `E'` builds is right-leaning — `E' → + T E'` recurses on the right — so the parser must *reassemble* left-associativity afterwards, usually by threading an accumulator through `E'`. **The grammar is now LL(1) and no longer says what it means.**

### What the parser actually does instead

`parser.py` does not use the transformed grammar. It uses a **loop**:

```python
def parse_add(self):
    node = self.parse_mul()
    while self.peek().text in ('+', '-'):
        op = self.eat('OP').text
        node = Node('Binary', op=op, lhs=node, rhs=self.parse_mul())
    return node
```

**`node` is rebuilt on each iteration with the old node as its left child.** Left-to-right iteration produces a left-leaning tree — which is left associativity, directly, with no transformation and no accumulator.

> **This is the same transformation, folded back into iteration.** $A' \to \alpha A' \mid \varepsilon$
> is tail recursion, and tail recursion is a loop. **Every practical recursive descent parser does
> this**, which is why the elimination rule is worth knowing as theory and almost never worth
> applying as written.

Verified — the loop gives exactly the associativity the grammar specified:

```
1-2-3     -> (- (- 1 2) 3)
1+2+3+4   -> (+ (+ (+ 1 2) 3) 4)
1+2*3     -> (+ 1 (* 2 3))
-2*3      -> (* (- 2) 3)
a||b&&c   -> (|| a (&& b c))
```

---

## 4. FIRST and FOLLOW

To write `parse_stmt`, the parser must decide which production to use **by looking at one token**. That decision needs two pieces of information about every non-terminal.

**FIRST($\alpha$)** — the set of terminals that can begin a string derived from $\alpha$. If $\alpha$ can derive $\varepsilon$, then $\varepsilon \in$ FIRST($\alpha$).

**FOLLOW($A$)** — the set of terminals that can appear immediately after $A$ in some derivation. `$` (end of input) is in FOLLOW(start).

**Computed for the transformed expression grammar:**

| | FIRST | FOLLOW |
|---|---|---|
| `E` | `(`, `n` | `$`, `)` |
| `E'` | `+`, ε | `$`, `)` |
| `T` | `(`, `n` | `$`, `)`, `+` |
| `T'` | `*`, ε | `$`, `)`, `+` |
| `F` | `(`, `n` | `$`, `)`, `*`, `+` |

*(Measured.)*

**Why FOLLOW is needed at all:** because of $\varepsilon$. When the parser is at `E'` and sees `)`, no production of `E'` *starts* with `)` — but `E' → ε` is legal precisely when the next token can follow `E'`. **FOLLOW is the set that licenses taking the empty production.**

### The LL(1) condition

> A grammar is **LL(1)** if, for every non-terminal, the one-token lookahead always determines the
> production uniquely.

Concretely, for each $A \to \alpha \mid \beta$:

1. FIRST($\alpha$) and FIRST($\beta$) must be **disjoint**, and
2. if one derives $\varepsilon$, the other's FIRST must be disjoint from FOLLOW($A$).

**LL(1)** means: scan **L**eft to right, produce a **L**eftmost derivation, with **1** token of lookahead.

**The left-recursive grammar fails condition 1** — FIRST(`E + T`) and FIRST(`T`) are both `{(, n}`, because `E + T` starts with an `E` which starts with a `T`. **That is the same defect as §2's infinite loop**, stated in terms of sets rather than stack frames.

---

## 5. Left Factoring

A second, milder defect. Two productions sharing a prefix:

$$A \to \alpha\beta \mid \alpha\gamma$$

One token of lookahead sees $\alpha$ and cannot choose. **Factor out the common prefix:**

$$A \to \alpha A' \qquad A' \to \beta \mid \gamma$$

**Now the parser commits to $\alpha$ first and decides afterwards**, by which time it has more information.

### Applied to the dangling else — and it does not work

```ebnf
S ::= "if" e S | "if" e S "else" S | s
```

Both `if` productions share the prefix `if e S`. Left-factor:

```ebnf
S  ::= "if" e S S' | s
S' ::= "else" S | ε
```

**Run the checker on both:**

```
=== Dangling else (unfactored) ===
  --> NOT LL(1): 1 conflict(s)
      S on 'if': ('if', 'e', 'S')  vs  ('if', 'e', 'S', 'else', 'S')

=== Dangling else (left-factored) ===
  FIRST(S' ) = { else, ε }        FOLLOW(S' ) = { $, else }
  --> NOT LL(1): 1 conflict(s)
      S' on 'else': ('else', 'S')  vs  ('ε',)
```

**Still not LL(1). The conflict moved; it did not go away.**

Look at why: `else` is in **both** FIRST(`else S`) **and** FOLLOW(`S'`). Seeing `else`, the parser can either take it — attaching to the *inner* `if` — or take $\varepsilon$ and let an enclosing `S'` have it, attaching to the *outer* `if`.

> **That is L02 §6's ambiguity, arriving through a completely different door.** No grammar
> transformation removes it, because **the language is ambiguous, not merely the grammar's
> presentation of it.** Left factoring fixes presentation problems. This is not one.

**The resolutions are the ones you already know:** take the `else` whenever you see it (bind to the nearest `if` — C's rule), or require braces so the situation cannot arise (Cyan's rule). **`parse_if` in §1 does the first**, and Cyan's mandatory blocks mean it never has to.

---

## 6. Error Messages Are the Payoff

Recursive descent's real advantage over the generated parsers in L06 is not speed. **It is that the parser knows what it was doing.**

```
line 1 col 14: expected PUNCT '{', found KEYWORD 'return'
line 1 col 19: expected PUNCT ';', found PUNCT '}'
line 1: left-hand side of '=' is not assignable
line 1: comparison is non-associative; write 'a < b && b == c'
```

*(All measured, from `parser.py` on malformed input.)*

**Each of those was written by a human at the point in the code where the failure is meaningful.** `parse_block` knows it wanted a `{`. `parse_cmp` knows the user chained comparisons and can suggest the fix. **A generated parser reports "syntax error, unexpected ELSE, expecting '{'"** — mechanically correct and much less useful.

**This is why hand-written recursive descent has won in production.** GCC, Clang, Rust's `rustc`, Go's compiler and TypeScript all abandoned generated parsers for hand-written recursive descent, and error quality is the reason cited every time.

> **Note the third message.** *"Left-hand side of `=` is not assignable"* is produced by a check in
> `parse_stmt`, not by the grammar — the parser parses an expression, then tests its *shape* before
> accepting `=`. **`The Cyan Language Reference` expresses the same rule grammatically, via
> `lvalue`.** Both work. The grammar version gives a parse failure; the shape-check version gives a
> better message. **Choosing between them is exactly the L02 §8 question**, and reasonable compilers
> differ.

---

## 7. What to Take Away

1. **One function per non-terminal**, and the code reads as the grammar transliterated.
2. **Left recursion breaks it structurally** — recursion before consumption never terminates.
3. **The textbook elimination works but distorts the tree**; in practice you write a loop, which is the same transformation folded into iteration and keeps left associativity for free.
4. **FIRST and FOLLOW are what one-token lookahead needs**, and FOLLOW exists because of $\varepsilon$.
5. **LL(1) = Left-to-right, Leftmost derivation, 1 lookahead**, and the condition is disjointness.
6. **Left factoring fixes shared prefixes. It does not fix ambiguity** — the dangling else stays non-LL(1) after factoring, because the problem was never presentational.
7. **Hand-written parsers win on error messages**, which is why every major production compiler uses one.

---

## Exercises

1. Transliterate `while_stmt ::= "while" expr block` into a parser function. It should take you one minute; the point is to notice that it does.
2. Apply the left-recursion elimination rule to `mul_expr ::= mul_expr ("*"|"/"|"%") unary | unary`. Then write the loop version. Which would you rather maintain?
3. Compute FIRST and FOLLOW for `stmt` in the Cyan grammar. Is `parse_stmt`'s dispatch LL(1)? *(Careful: `assign_stmt` and `expr_stmt` both begin with an expression.)*
4. §6 notes `parse_stmt` parses an expression and then checks whether `=` follows. **That is more than one token of lookahead.** Is Cyan's statement grammar LL(1)? If not, what is the smallest $k$ for which it is LL($k$) — or is there no such $k$?
5. FOLLOW(`E'`) is `{$, )}` but FOLLOW(`T'`) is `{$, ), +}`. Account for the extra `+`.
6. Give a grammar that is **not** LL(1) but becomes LL(1) after left factoring alone, with no other change.
7. The dangling else stays non-LL(1) after factoring. **Construct a grammar for `if`/`else` that *is* LL(1)** and generates a language with optional else-branches. What did you have to change about the language?

---

*Next: L06 — the other direction. Bottom-up parsing builds the tree from the leaves, handles left recursion without complaint, and tells you about conflicts in a report you have to learn to read.*
