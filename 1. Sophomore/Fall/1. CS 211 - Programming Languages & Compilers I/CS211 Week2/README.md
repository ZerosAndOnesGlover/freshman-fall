# CS 211 · Programming Languages & Compilers I
## Week 2: Parsing — Top-Down and Bottom-Up

**Credits:** 4 (3 lecture + 1 lab) · **Prerequisites:** CS 101, CS 102, MATH 151
**Assessment for this course (overall):** Problem Sets 30%, Projects 25%, Midterms 25%, Final 20%
**This week's deliverables:** Lab 2, PS 2, and **Quiz 2** — Tuesday, covering Week 1.

---

### Why This Week Exists

Because Week 1 produced a flat list of tokens, and Week 0 established that a program is a tree.

**This is the phase that closes that gap** — and it is the last phase concerned only with *form*. From Week 3 onward the compiler starts caring what things mean; this week it still only cares what shape they are.

You build Cyan's parser twice, as you built the lexer twice. **But where Week 1's two lexers agreed on every valid program, this week's two tools disagree about the grammar itself.** bison reports two reduce/reduce conflicts on a grammar that Week 0 proved unambiguous — and understanding why that is not a contradiction is the single most useful thing this week teaches.

---

### Learning Objectives

By the end of Week 2, you should be able to:

1. Write a recursive descent parser directly from a grammar, one function per non-terminal.
2. Explain why left recursion breaks top-down parsing **structurally**, not incidentally.
3. Eliminate left recursion by the textbook rule, and say why practitioners write a loop instead.
4. Compute FIRST and FOLLOW, and state why FOLLOW is needed at all.
5. Apply the LL(1) condition, and **left-factor** a grammar — and recognise when factoring cannot help.
6. Trace a shift-reduce parse, and say at each step why the parser must *not* reduce.
7. Explain what an **item** is and what an LR(0) state records.
8. Place LL(1), SLR(1), LALR(1) and LR(1) in their containment order, and say why bison chose the third.
9. **Read a bison conflict report** — item sets, bracketed actions, and `-Wcounterexamples`.
10. **Distinguish "this grammar is ambiguous" from "this grammar is not LALR(1)"**, and know which evidence settles which.

---

### This Week's Materials

| File | Purpose |
| --- | --- |
| `lectures/L05 Recursive Descent and the Grammars That Fight Back.md` | One function per non-terminal; left recursion; FIRST/FOLLOW; LL(1); why left factoring cannot fix the dangling else |
| `lectures/L06 Bottom-Up Parsing and What Bison Is Telling You.md` | Shift-reduce, items, LALR(1), reading the conflict report, **Cyan's own two conflicts**, precedence declarations |
| `lab/LAB 2 Reading a Conflict Report.md` | The dangling else in four tools, then Cyan's conflict and its fix |
| `lab/first_follow.py` | FIRST/FOLLOW and LL(1) table builder with conflict reporting |
| `lab/dangling.y` · `lab/cyan.y` | bison grammars — the ambiguous one, and Cyan's full grammar |
| `assignments/PS 2 A Recursive Descent Parser for Cyan.md` | FIRST/FOLLOW by hand, conflict reports, and the parser itself |
| `assignments/QUIZ 2 Week 2 Tuesday.md` | **Covers Week 1.** Ten minutes, self-marked against the printed key |
| `resources/Reading Guide Week 2.md` | Dragon §4.4–4.8, with a pragmatic route through §4.6 |
| `solutions_instructor/` | Instructor only |

---

### The One Thing to Take From This Week

**A conflict report is a statement about the tool, not necessarily about your grammar.**

Run bison on Cyan and it reports **two reduce/reduce conflicts** on `[` and `.`. Run Week 0's parse-tree counter on the same grammar and every valid program has **exactly one** tree.

**Both results are correct.** bison answers *"is this grammar LALR(1)?"* — decidable, and the answer is no, because the token that distinguishes `x[i] = ...` from `x[i] < y;` can be arbitrarily far to the right. It cannot answer *"is this grammar ambiguous?"*, because **that question is undecidable** (L02 §8).

**"bison reported a conflict" and "my grammar is ambiguous" are different claims**, and the counterexample output is how you tell which one you have. The dangling else is genuinely ambiguous. Cyan is not. **Same warning, different diagnosis.**

---

### Assessment Reminder

**Labs and quizzes carry no weight**, and both are required. **Quiz 2 is sat Tuesday and covers Week 1** — lexing, not parsing. **Lab 2 is sat Friday of this week**, after both lectures.

Both are tracked in `5. Academic Registry/2. Gradebook/Year2 Sophomore/Fall/_CS 211 Lab and Quiz Record.md`.

---

### Connections

**Back:** **Week 0's grammar is this week's specification** and Week 1's `Token` list is its input. The dangling else appears for the third time — as a gcc warning in L02 §6, an LL(1) table conflict in L05 §5, and a bison state in L06 §4.

**Sideways:** **CS 201 Week 3** covers the stack and calling conventions. The shift-reduce parser's stack is the same data structure making the same trade — unbounded memory buying you power a finite machine cannot have (L04 §7).

**Forward:** **Week 3 annotates the AST this week produces.** The node shapes chosen in PS 2 Q4 are the ones PS 3, PS 4 and both projects walk, so they are worth choosing carefully. **Week 3 is also the first phase that rejects programs the parser accepted** — `x + true` parses perfectly and means nothing.

---

*CS 211 · Week 2 · © CSE Department*
