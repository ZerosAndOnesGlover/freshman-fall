# CS 211 · Programming Languages & Compilers I
## Week 0: Languages, Syntax, and Grammars

**Credits:** 4 (3 lecture + 1 lab) · **Prerequisites:** CS 101, CS 102, MATH 151
**Assessment for this course (overall):** Problem Sets 30%, Projects 25%, Midterms 25%, Final 20%
**This week's deliverables:** Lab 0 and PS 0. **No quiz** — Quiz 1, in Week 1, covers this week.

> **Week 0 is ten days long**, running Aug 27 to Sep 5. It absorbs orientation, add/drop and Labor
> Day, and Week 1 — when graded work begins — opens Sep 8. You get both lectures and the lab.

---

### Why This Week Exists

Because you have used four languages without once asking who decided what they let you say.

**CS 211 is about that decision and the machinery that enforces it.** Over thirteen weeks you will build a complete compiler for a small language called **Cyan** — lexer, parser, type checker, IR, optimiser, code generator — and by Week 11 it will emit LLVM IR that runs.

This week lays the two foundations everything else stands on. It establishes **the difference between syntax and semantics**, which is the distinction the entire course turns on. And it establishes **the grammar** — the finite rulebook that decides which of infinitely many strings are programs, and what tree each one gets.

It also fixes Cyan. The grammar in `resources/The Cyan Language Reference.md` is the specification you will implement, and it does not change until Week 8, when you extend it yourself.

---

### Learning Objectives

By the end of Week 0, you should be able to:

1. State the difference between syntax and semantics, and give two languages that share a syntax and disagree on its meaning.
2. Name the four paradigms and say, for each, how much of the *method* the programmer must supply.
3. Write a context-free grammar as a four-tuple, and explain what "context-free" is a promise not to do.
4. Produce leftmost and rightmost derivations of a string, and explain why both yield one tree.
5. Distinguish a parse tree from an AST, and say what the discarded nodes were for.
6. **Recognise ambiguity, and count it** — including why an ambiguous expression grammar admits Catalan-many trees.
7. Remove ambiguity by stratifying a grammar by precedence, and set associativity by choosing a recursion side.
8. Explain the dangling else, and name two different ways real languages resolve it.
9. State three things a CFG cannot express, and say which compiler phase handles them instead.
10. **Say what a design decision costs**, not merely that it was made.

---

### This Week's Materials

| File | Purpose |
| --- | --- |
| `lectures/L01 What a Language Is and Why There Are So Many.md` | Syntax vs semantics measured on `-7 / 2`; four paradigms; the program as a tree; the eight translations |
| `lectures/L02 Grammars Derivations and Ambiguity.md` | CFGs, BNF/EBNF, derivations; **58,786 parse trees for one expression**; stratification; the dangling else in gcc |
| `lab/LAB 0 Grammars and the Shape of Cyan.md` | The toolchain, derivations by hand, and three grammars you fix yourself |
| `lab/cfg_count.py` | The parse-tree counter — you will use it again in Week 2 |
| `assignments/Problem Set 0.md` | Derivations, the Catalan recurrence, two broken grammars, and one design argument |
| `resources/Course Overview Syllabus.md` | **Read this in full in Week 0** — assessment, the unweighted-lab rule, the lab-week difference from CS 201, deviations |
| `resources/The Cyan Language Reference.md` | **The specification.** Fixed now, changes once in Week 8 |
| `resources/Reading Guide Week 0.md` | Dragon §1.1–1.2, §2.2, §4.2–4.3 and SICP §1.1, with guiding questions |
| `solutions_instructor/` | Instructor only |

---

### The One Thing to Take From This Week

**A grammar does not describe a language. It decides one.**

`E ::= E "+" E | n` looks like a description of addition. It is not — it is a machine that admits 58,786 different meanings for a twelve-operand expression and refuses to say which you meant. Stratify it into `E ::= E "+" T | T` and you have not changed which strings are legal; **you have changed how many trees each one gets, from Catalan-many to exactly one.**

**Both grammars generate the same language.** That is the sentence to hold onto. Ambiguity is a property of the *grammar*, not of the language it generates — and every phase after this one assumes somebody upstream already made the choice.

---

### Assessment Reminder

**Labs and quizzes carry no weight.** The curriculum's assessment line sums to 100% without them, and no percentage has been invented to fill the gap.

They are still required. **The lab is checked off by the TA in the session**, and a second unexcused absence costs a letter grade. **Quiz *N* covers Week *N−1***, runs ten minutes at the start of **Tuesday's** lecture in Weeks 1–11, and prints its own answer key.

> **CS 211's lab does not lag, and CS 201's does.** Lab *N* here covers Week *N* and is sat on the
> **Friday of Week *N***, after both of that week's lectures. The two courses run in the same term
> and disagree deliberately — see the syllabus. Every lab and quiz file states its day *and* its
> week; the file is authoritative.

Both are tracked in `5. Academic Registry/2. Gradebook/Year2 Sophomore/Fall/_CS 211 Lab and Quiz Record.md`.

---

### Connections

**Back:** **MATH 151 is a real prerequisite**, not a formality — Week 1 is finite automata and Week 2 is grammars as formal objects, and both assume induction, sets and relations without re-teaching. **CS 102** supplies the trees and recursion; this course never explains what a tree traversal is.

**Sideways:** **CS 201 runs alongside and the two meet constantly.** CS 201 Week 1's floating-point non-associativity is why L02 §5 cares which side of your grammar recurses. CS 201's `idiv` is why Cyan's division truncates. Later, CS 201's calling convention is what your Week 4 code generator must obey.

**Forward:** L02's grammar is Week 1's token specification and Week 2's parser, function for function. The AST in L01 §4 is what Week 3 annotates with types and Week 4 walks to emit IR. **The eight translations in L01 §5 are the syllabus** — Weeks 1 through 5 are the first six of them, in order.

---

*CS 211 · Week 0 · © CSE Department*
