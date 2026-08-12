# CS 211 · Midterm Examination 1
## Programming Languages & Compilers I

---

**Week 4 · Wednesday 20:00–21:15 · 75 minutes**
**Covers Weeks 0–3** — grammars, lexing, parsing, and semantic analysis.
**Weight: 12.5% of the course grade**

**Permitted:** one handwritten sheet of A4, **one side**. No devices.
**Total: 75 marks** — one mark per minute; budget accordingly.

**Name:** _________________________________ **Student ID:** ___________________

---

> **Answer all five questions.** Marks are shown per part. Where a question asks you to *explain*,
> a correct answer with no reasoning earns roughly half.
>
> **Q5 is the synthesis question** and is deliberately open. Attempt it even if you are short of
> time — a partial argument scores.

---

## Q1 · Grammars and Ambiguity (15 marks)

**(a) [3]** State the four components of a context-free grammar.

**(b) [4]** The grammar `E ::= E "-" E | n` is ambiguous.

Draw **all** parse trees for `9 - 5 - 2`, and give the value each one evaluates to.

**(c) [4]** Rewrite the grammar so that `-` is **left-associative**. Then state, in one sentence, what feature of your rewrite produces the associativity.

**(d) [4]** A grammar admits 58,786 parse trees for a twelve-operand expression.

**Is the *language* ambiguous?** Answer yes or no and justify. Your justification must distinguish a property of a grammar from a property of a language.

---

## Q2 · Lexical Analysis (15 marks)

**(a) [3]** State the maximal munch rule **including its tie-break**.

**(b) [4]** Cyan's operators include `-`, `->`, `<` and `<=`, and `--` is not an operator.

Give the token sequence for `x-->y`, and explain in one sentence why the first `-` does not become part of a `->`.

**(c) [4]** An NFA has $n$ states.

- What is the maximum number of states its DFA can have?
- **Does minimisation avoid that maximum?** Justify with reference to what the states must distinguish.

**(d) [4]** True or false: *no finite automaton can recognise the language of parentheses balanced and nested at most 50 deep.*

Answer, and justify. **If you answer false, state how many states a DFA needs.**

---

## Q3 · Parsing (15 marks)

**(a) [3]** Why does a left-recursive production break a recursive descent parser? One sentence, referring to what the parser does before it examines a token.

**(b) [4]** Given `E ::= T E'` and `E' ::= "+" T E' | ε`:

- Why is **FOLLOW** needed to build the parse table, when **FIRST** alone is not enough?
- Give the situation, concretely.

**(c) [4]** In a shift-reduce parse of `n + n * n`, the stack holds `E + T` and the lookahead is `*`.

**Shift or reduce?** Justify — and name the term for a right-hand side on the stack that must *not* be reduced.

**(d) [4]** `bison` reports a conflict on a grammar you wrote.

**Name the two distinct things this could mean**, and say which of the two questions bison is actually able to decide.

---

## Q4 · Semantic Analysis (15 marks)

**(a) [4]** For each, name the compiler phase that rejects it, and say why an earlier phase cannot:

| Program fragment | Phase | Why not earlier |
|---|---|---|
| `let x = 1 @ 2;` | | |
| `let x = (1 + 2;` | | |
| `let x = 1 + true;` | | |

*(Three rows, roughly one mark each, plus one for the overall reasoning.)*

**(b) [4]** This Cyan program type-checks:

```cyan
fn odd(n: int) -> bool  { return even(n - 1); }
fn even(n: int) -> bool { return odd(n - 1); }
```

This one does not:

```cyan
fn f() -> int { let a = b; let b = 1; return a; }
```

**Explain both**, in terms of the passes the checker makes over the program.

**(c) [3]** Hindley-Milner infers `(t -> t) -> t -> t` for `\f -> \x -> f (f x)`.

**Say precisely which step of the inference forces `f`'s argument and result types to be the same.**

**(d) [4]** `\x -> x x` fails the occurs check.

Write the equation that cannot be solved, and explain why no finite type satisfies it. **Then say what the algorithm does if the occurs check is removed.**

---

## Q5 · Synthesis (15 marks)

**A language designer proposes adding chained comparison to Cyan**, so that `a < b < c` means `a < b && b < c`, as in Python. Cyan currently makes comparison non-associative, and `a < b < c` is a syntax error.

**(a) [5]** State the change required to `The Cyan Language Reference` §3's grammar. Write the new `cmp_expr` production.

**(b) [4]** **Name one thing that becomes harder** in a phase *other* than parsing. Be specific about the phase and the difficulty.

*(Hint: consider what `a < b < c` must evaluate, and how many times.)*

**(c) [6]** C accepts `a < b < c` and evaluates it as `(a < b) < c`, giving `1` for `a=1, b=5, c=3`.

**Three languages, three positions**: C reinterprets, Python special-cases, Cyan refuses.

**Argue for one**, and — this is where the marks are — **name a concrete situation in which a user of your chosen language is worse off** than a user of one of the other two.

---

## Mark Distribution

| Question | Topic | Marks |
|---|---|---:|
| Q1 | Grammars and ambiguity | 15 |
| Q2 | Lexical analysis | 15 |
| Q3 | Parsing | 15 |
| Q4 | Semantic analysis | 15 |
| Q5 | Synthesis | 15 |
| **Total** | | **75** |

---

*CS 211 · Midterm 1 · Week 4 · Covers Weeks 0–3*
