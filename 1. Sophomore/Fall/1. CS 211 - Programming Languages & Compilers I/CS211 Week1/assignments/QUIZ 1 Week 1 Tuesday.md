# CS 211 · Quiz 1
## Administered: Tuesday, Week 1 (first 10 minutes of lecture)

**Name:** _________________________________ **Section:** ___________ **Date:** ___________

**Covers Week 0** — syntax against semantics, the four paradigms, context-free grammars, derivations, parse trees and ASTs, ambiguity and how to remove it.

**Instructions:** Closed notes. 10 minutes.

> **This quiz is not marked and carries no weight.** The answer key is printed below the questions.
> Sit it closed-book, then turn the page and mark it yourself before you leave the room — the point
> is that you find out what has not landed while there is still a term left to fix it.
>
> Do not look at the key first. It costs you the only thing the exercise is for.

---

**Q1.** In C, `-7 / 2` is `-3`. In Python, `-7 // 2` is `-4`. Both are correct. What is the name of the distinction this illustrates, and which side of it are the two languages differing on?

&nbsp;

&nbsp;

---

**Q2.** Write the four components of a context-free grammar $G$.

&nbsp;

&nbsp;

---

**Q3.** A string has a leftmost derivation and a rightmost derivation under the same grammar. What, if anything, must be the same about them?

&nbsp;

&nbsp;

---

**Q4.** Under `E ::= E "+" E | n`, how many parse trees does `n + n + n` have? How many does `n + n + n + n` have?

&nbsp;

&nbsp;

---

**Q5.** You are given `E ::= E "+" T | T`. Is `+` left-associative or right-associative here, and what in the rule tells you?

&nbsp;

&nbsp;

---

**Q6.** Name one thing a context-free grammar **cannot** express about a programming language, and say which compiler phase handles it instead.

&nbsp;

&nbsp;

---

**Q7.** `ast.parse("(1 + 2) * 3")` produces no node for the parentheses. Where did the information go?

&nbsp;

&nbsp;

---

\pagebreak

---

## Answer Key — mark your own before leaving

**Q1.** **Syntax versus semantics.** The *syntax* is identical — the same operator, the same operands, parsed the same way. The languages differ on **semantics**: the meaning assigned to that syntax. C truncates toward zero (matching the `idiv` instruction); Python floors toward $-\infty$ (so the remainder takes the sign of the divisor).

*Common wrong answer: "one is a bug". Neither is. Both satisfy $q \times b + r = a$.*

---

**Q2.** $G = (N, \Sigma, P, S)$ — **non-terminals**, **terminals**, **productions**, and the **start symbol**.

*Give yourself the mark only if you named all four. "Rules and symbols" is not the answer.*

---

**Q3.** **The parse tree.** Both derivations build the same tree; they differ only in the order in which non-terminals are expanded. A derivation is a linearisation of a tree, and leftmost and rightmost are two walks over one structure.

*If you wrote "nothing" or "the string", re-read L02 §3 — the string being the same is trivially true and not what the question asks.*

---

**Q4.** **`n + n + n` has 2.** **`n + n + n + n` has 5.**

These are the Catalan numbers $C_{k-1}$ for $k$ operands: $1, 1, 2, 5, 14, 42, \dots$

*A very common answer is 3 for the second. Draw them: the five bracketings of four operands are*
`(1+(2+(3+4)))`, `(1+((2+3)+4))`, `((1+2)+(3+4))`, `((1+(2+3))+4)`, `(((1+2)+3)+4)`.

---

**Q5.** **Left-associative.** The rule is **left-recursive** — the recursive reference `E` appears on the *left* of the operator — so `a + b + c` groups as `(a + b) + c`. Writing `E ::= T "+" E` would make it right-associative.

---

**Q6.** Any one of:

- **A variable must be declared before use**
- **A call must supply the number of arguments the declaration takes**
- **Both sides of `=` must have compatible types**

All three are handled in **semantic analysis** (Week 3), by walking the AST with a **symbol table**. Each needs memory of an arbitrarily distant part of the program, which is exactly what "context-free" promises not to require.

*Do not accept "operator precedence" — that one **is** expressible, by stratifying the grammar.*

---

**Q7.** **Into the shape of the tree.** The parentheses instructed the parser to build `Mul` above `Add` rather than the other way round. Having done that, they have no further job: the nesting *is* the record that they were there. This is what the *abstract* in Abstract Syntax Tree means — structure is kept, notation is discarded.

---

### If you got fewer than 5

**Re-read L02 §3–§5 before Thursday**, and redraw the five trees in Q4 by hand. Everything in Week 2 assumes you can look at a grammar rule and immediately say what tree it builds — the parser you write is literally one function per non-terminal, and a function you cannot picture is a function you cannot debug.

---

*CS 211 · Quiz 1 · Covers Week 0 · Unmarked*
