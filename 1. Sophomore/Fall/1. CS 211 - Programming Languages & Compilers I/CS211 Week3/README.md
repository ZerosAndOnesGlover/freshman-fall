# CS 211 · Programming Languages & Compilers I
## Week 3: Semantic Analysis — Types and Symbol Tables

**Credits:** 4 (3 lecture + 1 lab) · **Prerequisites:** CS 101, CS 102, MATH 151
**Assessment for this course (overall):** Problem Sets 30%, Projects 25%, Midterms 25%, Final 20%
**This week's deliverables:** Lab 3, PS 3, and **Quiz 3** — Tuesday, covering Week 2.

> **MIDTERM 1 is announced this week and sat in Week 4**, covering **Weeks 0–3**. The revision guide
> ships with Week 4's materials. This is the last new front-end content before it.

---

### Why This Week Exists

Because the parser will accept `return zzz + true;` without complaint.

**Every token is legal, the grammar is satisfied, the tree is well-formed** — and the program is nonsense. **This is the first phase that says no**, and it has to be a separate phase for the reason L02 §8 gave: *declared before use*, *arity matches*, *types agree* are not context-free, and no grammar can express them.

It is also the week the front end finishes. After this, the compiler stops asking what the program *says* and starts deciding what machine will run it.

---

### Learning Objectives

By the end of Week 3, you should be able to:

1. Say why semantic analysis must be separate from parsing, in terms of formal power.
2. Implement a **scope chain**, and explain how shadowing falls out of `lookup` rather than being implemented.
3. Distinguish lexical from dynamic scope, and say why lexical scope won.
4. Explain Cyan's three passes, and why functions may be used before declaration while locals may not.
5. Write type rules for a small language, and defend the absence of implicit conversions.
6. **Explain why a position must be recorded by the phase that has it** and cannot be recovered later.
7. Generate type constraints from an expression and solve them by **unification**.
8. State what the **occurs check** is for, and why inference would not terminate without it.
9. State the **principal type theorem** and say what it buys over a good heuristic.
10. Explain **let-polymorphism** — and recognise the example that appears to demonstrate it and does not.

---

### This Week's Materials

| File | Purpose |
| --- | --- |
| [[L07 Symbol Tables Scope and the First Phase That Says No]] | Scope chains, lexical vs dynamic, three passes, the eighteen refusals, and where positions come from |
| [[L08 Hindley-Milner and the Algorithm That Guesses Right]] | Constraints and unification, the occurs check, principal types, let-polymorphism, and why Cyan annotates anyway |
| [[LAB 3 Scope Types and Inference]] | Break `lookup`, break positions, cross-check inference against GHC, meet the let-polymorphism trap |
| `lab/typecheck.py` | The reference checker — scope chain, three passes, positioned errors |
| `lab/hm.py` | Hindley-Milner in ~120 lines, with traces |
| `lab/scopes.cy` | Three variables named `a` at three depths |
| `lab/parser.py` · `lab/lexer.py` | Weeks 1–2, carried forward — **now with positions on AST nodes** |
| [[PS 3 Scope Analysis and Type Checking]] | Scope by hand, inference by hand, and the checker |
| [[QUIZ 3 Week 3 Tuesday]] | **Covers Week 2.** Ten minutes, self-marked |
| [[CS211 Week3/resources/Reading Guide Week 3\|Reading Guide Week 3]] | Dragon §2.7, §5.1–5.2, §6.5 and **TAPL Ch. 22** |
| `solutions_instructor/` | Instructor only |

---

### The One Thing to Take From This Week

**A position must be recorded by the phase that has it.**

The type checker reports `line 4 col 5: '+' needs int operands, found int and bool`. Column 5 of line 4 is where the `+` is — not where the statement began on line 3.

**To say that, the checker needs a position on the `Binary` node. And by then the tokens are gone.** The lexer had positions and nothing in Week 1 read them. The parser had to copy them onto nodes, and nothing in Week 2 read them either. **This week reads both, and there is no way to recover either if it was skipped.**

**Every phase from here adds a field the next phase needs**: Week 4 wants types on nodes, Week 5 wants liveness on instructions. **Build the field when the phase that produces it runs**, not when the phase that needs it fails.

---

### Assessment Reminder

**Labs and quizzes carry no weight**, and both are required. **Quiz 3 is sat Tuesday and covers Week 2**. **Lab 3 is sat Friday of this week.**

Both are tracked in [[_CS 211 Lab and Quiz Record]].

---

### Connections

**Back:** **L02 §8 predicted this week** — it named three rules a CFG cannot express and said a later phase would handle them. This is that phase. **PS 2's Requirement 7**, which nothing in Week 2 used, is what makes the error messages possible.

**Sideways:** **CS 201 Week 4** is the memory hierarchy. The symbol table is a data structure consulted on nearly every AST node, and in a production compiler its layout is a genuine cache-locality question.

**Forward:** **Week 4 reads `e.ty` on every node** to choose instructions — `+` on `int` and `+` on `string` compile to entirely different code. **Week 8 returns to L08's trade-off**: HM gives up rank-*n* polymorphism to stay decidable, and Week 8 walks up the other side of that hill into System F and type classes. Haskell's `1 + True` error is the seam, and it is a Week 8 problem showing through a Week 3 window.

---

*CS 211 · Week 3 · © CSE Department*
