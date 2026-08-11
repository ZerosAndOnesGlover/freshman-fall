# CS 211 · Programming Languages & Compilers I
## Week 1: Lexical Analysis and Regular Languages

**Credits:** 4 (3 lecture + 1 lab) · **Prerequisites:** CS 101, CS 102, MATH 151
**Assessment for this course (overall):** Problem Sets 30%, Projects 25%, Midterms 25%, Final 20%
**This week's deliverables:** Lab 1, PS 1, and **Quiz 1** — Tuesday, covering Week 0.

> **Week 1 opens Sep 8**, when graded work begins. Week 0 was ten days; every week from here is five.

---

### Why This Week Exists

Because the parser you write next week must be handed tokens, and something has to make them.

**This is phase one of the eight from L01 §5**, and it is the only phase this course finishes completely in one week. By Friday you will have built Cyan's lexer twice — once by hand and once with `flex` — and diffed the two token streams.

The week also settles a question Week 0 left open: **why is lexing a separate phase at all?** The practical answers are speed and simplicity. **The real answer is a theorem.** Tokens are a regular language, program structure is not, and those two classes need different machines — a table for one, a stack for the other. The phase boundary sits exactly on that line, which is why it is a clean split rather than a matter of taste.

---

### Learning Objectives

By the end of Week 1, you should be able to:

1. State what a token carries and why the source position is not optional.
2. Write regular expressions using only the four formal operators, and say which familiar features are abbreviations and which are not regular at all.
3. Apply **maximal munch**, including the tie-break on rule order, and explain why `x-->y` is four tokens.
4. Build an NFA from a regular expression by Thompson's construction.
5. **Run the subset construction** and explain why a DFA state is a set of NFA states.
6. Minimise a DFA by partition refinement, and use the uniqueness of the minimal DFA to decide regular-expression equivalence.
7. State the exponential blowup, and say why minimisation does not avoid it.
8. **Prove that no finite automaton recognises balanced parentheses**, and say what that implies for Week 2.
9. Write a working lexer without a regex library.
10. Argue about error recovery as a design choice rather than a correctness question.

---

### This Week's Materials

| File | Purpose |
| --- | --- |
| `lectures/L03 Tokens Regular Expressions and Maximal Munch.md` | Tokens, the formal four operators, maximal munch measured on six inputs, what the lexer discards |
| `lectures/L04 Finite Automata and the Subset Construction.md` | NFA/DFA, Thompson, the subset construction, **58 NFA states → 512 minimal DFA states**, minimisation, and why parsing needs a stack |
| `lab/LAB 1 Two Lexers and Where They Disagree.md` | Build the `flex` lexer, diff it against the hand-written one, then find the three inputs where they part |
| `lab/lexer.py` | The reference hand-written lexer — read it in Part 1, replace it in PS 1 |
| `lab/sample.cy` · `lab/expected_tokens.txt` | The 109-token test input and its expected output |
| `lab/compare.sh` | Builds the flex lexer and diffs both token streams |
| `assignments/PS 1 A Lexer From a Hand-Built DFA.md` | Regular expressions formally, the constructions by hand, and your own lexer |
| `assignments/QUIZ 1 Week 1 Tuesday.md` | **Covers Week 0.** Ten minutes, self-marked against the printed key |
| `resources/Reading Guide Week 1.md` | Dragon Ch. 3 in full — the longest single reading of the term |
| `solutions_instructor/` | Instructor only |

---

### The One Thing to Take From This Week

**The exponential is real, and you cannot minimise your way out of it.**

$(a\mid b)^*a(a\mid b)^n$ has an NFA that grows by six states per increment and a minimal DFA that hits $2^{n+1}$ **exactly, at every $n$** — 58 NFA states against 512 minimal DFA states, measured. Minimisation removes precisely one state and stops, because the rest are not redundant: to know what the character $n+1$ from the end was, the machine genuinely must remember $2^{n+1}$ distinct histories.

**And yet Cyan's entire token set compiles to 70 DFA states from a 176-state NFA** — *smaller* than the NFA it came from. **Both facts are true, and the gap between them is the whole practical story of lexer generators.** The worst case is attained; it just is not attained by anything a language designer would write.

---

### Assessment Reminder

**Labs and quizzes carry no weight**, and both are required. **Quiz 1 is sat Tuesday and covers Week 0** — grammars, not lexing. **Lab 1 is sat Friday of this week**, after both lectures.

> **Lab *N* covers Week *N* and is sat on the Friday of Week *N*.** CS 201's lab lags by a week and
> CS 211's does not — see the Week 0 syllabus. Every lab and quiz file states its day *and* its week.

Both are tracked in `5. Academic Registry/2. Gradebook/Year2 Sophomore/Fall/_CS 211 Lab and Quiz Record.md`.

---

### Connections

**Back:** Week 0's grammar is what the tokens feed. **MATH 151's induction and pigeonhole** are used directly — §7 of L04 is a pigeonhole argument, and PS 1 Q4 asks you to reproduce it.

**Sideways:** **CS 201 Week 2** is reading x86-64 assembly, which is the output end of the pipeline whose input end you are building here. `objdump` disassembling bytes into mnemonics is a lexer, and it faces the same maximal-munch problem on variable-length instruction encodings.

**Forward:** **Week 2's parser consumes `Token` objects from this week's lexer** — the interface is fixed in PS 1 Q5 and does not change. The `line` and `col` fields go unused until **Week 3**, when the type checker needs somewhere to point; PS 1 requires them now because retrofitting positions across a finished compiler is miserable.

---

*CS 211 · Week 1 · © CSE Department*
