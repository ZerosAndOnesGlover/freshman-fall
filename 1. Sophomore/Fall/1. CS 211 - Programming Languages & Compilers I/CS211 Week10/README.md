# CS 211 · Programming Languages & Compilers I
## Week 10: Domain-Specific Languages and Metaprogramming

**Credits:** 4 (3 lecture + 1 lab) · **Prerequisites:** CS 101, CS 102, MATH 151
**Assessment for this course (overall):** Problem Sets 30%, Projects 25%, Midterms 25%, Final 20%
**This week's deliverables:** Lab 10, PS 10, and Quiz 10 (Tuesday, covers Week 9).

> ## ⚠ Project 1 and PS 10 are both due Friday of Week 11.
>
> Project 1 is **12.5% of the course**; PS 10 is roughly **2.3%**, and the Problem Sets component
> **drops your lowest mark**. If you have to choose, the arithmetic is not close. Plan for it this
> week rather than next Friday afternoon.

---

### Why This Week Exists

Because Week 7 proved that **`if` cannot be an ordinary function** in a strict language, and Week 7's fix put the cost on the caller — every branch wrapped in a thunk.

There is a second way out, and it does not touch the caller at all. **Make the thing that is not a function.** A macro runs at expansion time and receives its arguments as *unevaluated syntax*, so a macro can be `if`. It can also be `while`, `unless`, `cond`, and anything else you care to invent — as library code, in a file, with no change to the evaluator.

Push that further and you are not adding a control structure, you are building a **language**: a notation for one problem, which is what the rest of the week is about — and what it costs, which is more than the tutorials say.

---

### Learning Objectives

By the end of Week 10, you should be able to:

1. State the two differences between a **macro** and a function, and say what follows from each.
2. Demonstrate something a macro can do that a function cannot, and connect it to Week 7.
3. Explain **homoiconicity**, and why it makes Lisp macros ordinary list manipulation.
4. Write a macro using **quasiquote**, **unquote** and **unquote-splicing**.
5. Recognise **variable capture** in a macro, and fix it with `gensym`.
6. Say what **hygiene** means, and which real macro systems have it.
7. Distinguish **internal** from **external** DSLs, and name the deciding question.
8. Build a parser from **combinators**, and explain how the grammar becomes a value.
9. Explain why **left recursion** still fails, and why the error messages get worse.
10. Recognise a **shared subexpression as a shared wire** — a DAG, not a tree.
11. Compare macro systems across languages, and say what they are all working around.
12. Judge when a DSL is **not** worth building.

---

### This Week's Materials

| File | Purpose |
| --- | --- |
| `lectures/L21 Code as Data and the Macro That Is If.md` | Macros against functions **measured**, homoiconicity, `while` as library code, expansion, **capture and `gensym`** |
| `lectures/L22 Little Languages and What They Cost.md` | Internal against external DSLs, parser combinators, **left recursion inherited**, **the error-message trade**, macro systems compared, code generation |
| `assignments/PS 10 A Circuit DSL and Its Simulator.md` | Macros, the circuit DSL both ways, **sequential logic**, circuit optimisation, better combinator errors |
| `assignments/QUIZ 10 Week 10 Tuesday.md` | **Covers Week 9.** Six questions, key printed below them |
| `lab/LAB 10 A Parser Combinator Library.md` | Macros in a REPL, then combinators, then the DSL |
| `lab/lisp.py` | A Lisp, in order to have macros. **The whole front end is thirty lines** |
| `lab/demo.py` | The five demonstrations, including the capture bug and its fix |
| `lab/combinators.py` | The grammar as a value — **4 lines** — and the two things it does not fix |
| `lab/circuit.py` | The same circuit language internal and external, with a simulator |
| `resources/Reading Guide Week 10.md` | SICP §4.1 · *On Lisp* ch. 7–8 · Fowler ch. 1–4 · Bentley 1986 |
| `solutions_instructor/` | Instructor only |

---

### The One Thing to Take From This Week

**The grammar went from 357 lines to 4, and the error messages became unusable.**

| input | Week 2's hand-written parser | this week's combinators |
|---|---|---|
| `(1 + 2` | `line 1 col 30: expected PUNCT ')', found PUNCT ';'` | `expected number or ')' at '(1 + 2'` |

The combinator version reports at the **start of the input**, because alternation backtracks and throws away everything both branches learned.

That is the shape of nearly every abstraction in this week. **Macros**: the core stays small and the thing the programmer wrote is gone by the time anything fails. **Internal DSLs**: free to build, permanently limited to the host's grammar. **External DSLs**: say exactly what you mean, and you now own the diagnostics, the editor support and every "why doesn't this work". **Code generation**: one description, many consumers, and a debugger that steps into code nobody wrote.

> **This is why clang, rustc and GHC all hand-write their parsers**, despite every one of those
> teams knowing precisely what a parser combinator is. They are optimising for the error message,
> because that is the part users actually interact with.

---

### Assessment Reminder

**Labs and quizzes carry no weight**, and both are required. **Quiz 10 is sat Tuesday and covers Week 9. Lab 10 is Friday and covers this week.**

Both are tracked in `5. Academic Registry/2. Gradebook/Year2 Sophomore/Fall/_CS 211 Lab and Quiz Record.md`. **PS 10 is a weighted component** and goes in `CS 211.md` — **and so does Project 1, due the same day.**

---

### Connections

**Back:** **Week 7 §10 said `if` cannot be a function; a macro can.** **Week 7 §5's capture is `swap-bad`**, and `gensym` is Week 7's `fresh`. **Week 2's left recursion is inherited unchanged** by combinators, because combinators *are* recursive descent with the call graph reified. **Week 8's dictionary passing is the same expansion shape** — the `=>` became a `->` and nothing survived. **Week 7's thunk is `lazy`**, delaying a recursive grammar in a strict host. **Week 4's tree-versus-DAG mistake** reappears as counting a full adder's shared XOR twice.

**Sideways:** **CS 201's Week 0–1 gate-level material** is what `circuit.py` simulates; the full adder there is this one.

**Forward:** **Week 11 assembles the compiler end to end**, and Project 1 is due. **Week 12** asks what all of this was for — and "which notation should this be written in" is the question the whole course has been circling.

---

*CS 211 · Week 10 · © CSE Department*
