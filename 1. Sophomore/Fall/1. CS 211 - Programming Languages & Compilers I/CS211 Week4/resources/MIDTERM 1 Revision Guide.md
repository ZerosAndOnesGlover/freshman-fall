# CS 211 · Midterm 1 · Revision Guide
## Weeks 0–3 · Sat Week 4, Wednesday 20:00–21:15

---

**75 minutes, 75 marks.** One handwritten A4 sheet, **one side only**. No devices.
**Covers Weeks 0–3.** Week 4's IR material is **not** examined.

---

## What the Paper Looks Like

Five questions, fifteen marks each, in course order:

| | Topic | Weeks |
|---|---|---|
| **Q1** | Grammars and ambiguity | 0 |
| **Q2** | Lexical analysis | 1 |
| **Q3** | Parsing | 2 |
| **Q4** | Semantic analysis | 3 |
| **Q5** | **Synthesis** — a design question spanning several weeks | 0–3 |

**Q5 is open-ended and worth as much as the others.** It asks you to change the language and reason about consequences. **Attempt it even if you are short of time**; a partial argument scores, and a blank scores nothing.

---

## What Your One Sheet Should Have On It

**Do not copy the lecture notes onto it.** You have one side; spend it on things that are *hard to reconstruct under time pressure* and cheap to write down.

**Worth the space:**

- The **Catalan numbers** $1, 1, 2, 5, 14, 42, 132$ — Q1 may ask for a count.
- The **FIRST/FOLLOW rules**, especially the ε case.
- The **LL(1) condition**, both clauses.
- **Leader rules** for basic blocks *(not examined, but cheap)*.
- **The precedence ladder** of `The Cyan Language Reference` §3.
- The **eighteen type errors**' categories — not the wordings.
- **HM's inference rules** for lambda, application, and `let`.

**Not worth the space** — you either know these or the sheet will not save you:

- Definitions of "token", "lexeme", "grammar". If you cannot state these from memory, revise rather than transcribe.
- Anything from Week 4.

---

## Week by Week

### Week 0 — Grammars

**Must be able to do cold:**

- State a CFG as a four-tuple.
- Produce **leftmost and rightmost derivations** of a short string, and say why both give one tree.
- **Draw all parse trees** for an ambiguous string, and evaluate each.
- **Stratify a grammar by precedence**, and set associativity by choosing the recursion side.
- Explain the **dangling else**, and name two resolutions.
- State three things a CFG **cannot** express, and which phase handles them.

**The distinction most likely to be tested:** *ambiguity is a property of a grammar, not of a language.* Two grammars can generate identical languages and disagree entirely on tree counts.

**Numbers worth knowing:** the ambiguous `E ::= E + E | n` gives **58,786** trees for twelve operands; the stratified grammar gives **1**, and both accept exactly the same strings.

### Week 1 — Lexing

- **Maximal munch, including the tie-break.** `x-->y` is four tokens.
- **Thompson's construction** and the **subset construction** — be able to run both on a small regex.
- **Minimisation** by partition refinement.
- **The exponential blowup**: an NFA of 58 states gives a minimal DFA of exactly $2^{n+1} = 512$, and **minimisation removes only one state.**
- **Why parsing needs a stack** — the pigeonhole proof for balanced parentheses.

**The question that is missed every year:** *is the language of parentheses nested at most $k$ deep regular?* **Yes**, with about $k+2$ states. The impossibility proof needs *unbounded* nesting, and "finite automata cannot count" is a slogan missing its qualifier.

### Week 2 — Parsing

- Why **left recursion** breaks recursive descent, structurally.
- **Left-recursion elimination**, and why practitioners write a loop instead.
- **FIRST and FOLLOW**, and why FOLLOW exists at all (ε-productions).
- **Left factoring**, and the fact that it **cannot** fix the dangling else.
- **Shift-reduce**: given a stack and a lookahead, decide and justify. Know the word **handle**.
- **LL(1) ⊂ SLR(1) ⊂ LALR(1) ⊂ LR(1)**, and why bison chose LALR(1).
- **Reading a conflict report**: bracketed actions are the *disabled* ones.

**The distinction most likely to be tested:** *a bison conflict means "not provably LALR(1)", not "ambiguous".* Cyan's own grammar has two reduce/reduce conflicts and is verifiably unambiguous. **bison decides a question that is decidable; ambiguity is not.**

### Week 3 — Semantic Analysis

- **Scope as a chain**, and shadowing as a consequence of `lookup`.
- **Lexical vs dynamic scope**, and why lexical won.
- **The three passes**, and why functions may be used before declaration and locals may not.
- **Type rules**, and the cost of having no implicit conversions.
- **Where positions come from**, and why they cannot be recovered later.
- **Unification**, the **occurs check**, and why it makes inference terminate.
- **The principal type theorem.**
- **Let-polymorphism** — generalise at `let`, not at lambda.

**The trap most likely to be tested:** `let id = \x->x in id (id 1)` **type-checks in both `let` and lambda form**, because both uses are at `int -> int`. Demonstrating let-polymorphism needs a variable used at **two different types** — the `if f true then f 1 else 2` shape.

---

## Twelve Questions to Test Yourself With

Do these closed-book, in about forty minutes. **If you can do all twelve, you are ready.**

1. `E ::= E "-" E | n`. Draw all trees for `9-5-2` and evaluate each.
2. Rewrite it left-associative. What in your rewrite produces the associativity?
3. Tokenise `a<<=b` and `x-->y`. Justify each with maximal munch.
4. Build the NFA for `(a|b)*b` by Thompson, then subset-construct the DFA.
5. Is `{ (ⁿ )ⁿ : n ≤ 20 }` regular? Justify, and give a state count if yes.
6. Compute FIRST and FOLLOW for `S ::= "let" IDENT "=" E ";" | E ";"` with the usual `E`/`T`/`F`.
7. Why is that grammar's `S` choice LL(1)? *(The answer involves the lexer.)*
8. Stack holds `E + T`, lookahead `*`. Shift or reduce, and what is the term for the thing you must not reduce?
9. bison reports one shift/reduce conflict. Name the two things that could mean.
10. Give three programs the parser accepts and the type checker rejects, one per rule category.
11. Infer the type of `\f -> \g -> \x -> f (g x)`, showing every equation.
12. Why does `\x -> x x` fail? Write the equation, and say what happens without the occurs check.

**Answers are distributed throughout Weeks 0–3's lectures and solutions.** Working out *where* to look is itself revision.

---

## Practicalities

**Timing.** One mark per minute, and Q5 is worth 15. **Do not spend forty minutes on Q1–Q2** — they are the parts you know best and the easiest place to lose the paper.

**Show reasoning.** Every "explain" and "justify" carries roughly half its marks for the argument. A correct one-word answer to Q3(d) earns about two of four.

**Drawing.** Parse trees, CFGs and automata should be drawn, not described. **Label your states and non-terminals** — an unlabelled diagram is hard to award marks to.

**If you are stuck on Q5**, write down the trade-off first: *what does this change buy, and what does it cost?* That framing alone earns marks, and the specifics usually follow once it is on paper.

---

*CS 211 · Midterm 1 Revision Guide · Covers Weeks 0–3*
