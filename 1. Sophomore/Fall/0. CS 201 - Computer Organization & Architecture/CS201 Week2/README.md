# CS 201 · Computer Organization & Architecture
## Week 2: x86-64 Assembly Language

**Credits:** 4 (3 lecture + 1 lab) · **Prerequisites:** PROG 101 (C), ECE 110 (digital logic)
**Assessment for this course (overall):** Problem Sets 35%, Midterms 25%, Final 20%, Projects 20%
**This week's deliverables:** PS 2 (due Week 3 Friday), Lab 2, and **Quiz 2 on Monday, covering Week 1**.

---

### Why This Week Exists

Because from here to Week 12, "read the disassembly" is the answer to most questions, and you cannot read what you cannot decode.

Week 0 showed you a listing and told you not to worry about it yet. **This is the week you stop needing that concession.** By Friday you should be able to open any function you can write, at any optimisation level, and say what it does.

There is a second thing, less obvious and more important. **Reading compiler output is how you find out what your source code actually means.** `x / 8` and `x >> 3` look interchangeable and compile to four instructions and one. A `switch` compiles four different ways depending on the values in it. A division by a constant contains no division. **None of this is visible in C**, and all of it matters by Week 11.

---

### Learning Objectives

By the end of Week 2, you should be able to:

1. Name the sixteen general-purpose registers and their conventional roles, and apply the 32-bit zeroing rule.
2. Read and write both Intel and AT&T syntax, and convert between them.
3. Decompose any memory operand into base, index, scale and displacement.
4. Explain why `lea` computes without accessing memory, and use it as a multiplier.
5. Distinguish `shr` from `sar`, and say which C chooses and why.
6. Explain what `cdq` is for and what happens without it.
7. Recognise a fixed-point reciprocal, and derive the magic constant for a given divisor.
8. State the four flags, which instructions set them, and which jumps read which.
9. Use the unsigned range-check idiom, and explain why one comparison bounds both sides.
10. Identify which of four `switch` strategies a listing uses.
11. **Write, assemble, link and call x86-64 assembly from C.**

---

### This Week's Materials

| File | Purpose |
| --- | --- |
| `lectures/L07 Registers Operands and the Two Syntaxes.md` | The register file, the two syntaxes, every addressing mode, `lea` |
| `lectures/L08 Arithmetic and What the Compiler Does Instead of Dividing.md` | `imul`/`idiv`/`cdq`, magic numbers, `x/8` vs `x>>3`, `setcc` and `cmov` |
| `lectures/L09 Flags Conditionals and Control Flow.md` | The flags, signed vs unsigned jumps, range checks, four ways to compile a `switch` |
| `assignments/PS 2 Writing x86-64 Assembly.md` | Five functions in NASM, a magic-number derivation, a `switch` investigation |
| `assignments/QUIZ 2 Week 2 Monday.md` | Ten minutes on Week 1. **Unmarked — key in the paper** |
| `lab/LAB 2 Reading Compiler Output.md` | Addressing modes, division, four switches, and your first hand-written assembly |
| `resources/Reading Guide Week 2.md` | CS:APP Ch. 3 §3.1–3.6, and how to look things up in the Intel SDM |
| `solutions_instructor/` | Instructor only |

---

### The One Thing to Take From This Week

**The instruction set is smaller and stranger than you expect, and the compiler is fluent in it.**

Smaller: there is essentially one memory-operand form, four scale values, four flags, and a dozen instructions you will see constantly.

Stranger: `lea` is the general adder. `cmp` computes nothing. Division by a constant is a multiplication. A range check is a single unsigned comparison. **A `switch` over seven values might compile to $10x + 10$, or a table in `.rodata`, or an indirect jump, or a chain of comparisons — and the compiler chooses by looking at your case values.**

You are not going to out-write the compiler. **The point of reading its output is to find out what it understood you to mean**, which is not reliably what you meant.

---

### Assessment Reminder

**Labs and quizzes carry no weight**; the four weighted components already sum to 100%. Both are required — the lab is checked off in the session, and a second unexcused absence costs a letter grade.

**Quiz 2 is Monday** and covers **Week 1**. Key is in the paper; sit it closed-book first.

**PS 2 is the first assignment where you submit code that must run.** Include the `.note.GNU-stack` directive in every `.asm` file — Q3(f) is about what happens when you do not, and the answer is that your program's stack becomes executable.

---

### Connections

**Back:** **Week 1's signed/unsigned rule** is the mechanism behind L09 §4's range-check idiom — the same reinterpretation that made `strlen(s)-1` enormous makes one comparison bound both sides. **Week 1's `INT_MIN` anomaly** reappears in PS 2 Q3(b), this time in assembly you wrote. **Week 0's `lea rdx,[rdx+rax*2+0x1]`** finally makes sense.

**Forward:** **Week 3 is the other half of this week** — `call`, `ret`, the stack frame, and where those six argument registers came from. Week 5's branch prediction needs L09's jumps. Week 9's exploits need to know that `ret` reads an address off the stack, which is Week 3's first slide.

**Sideways:** PROG 201 is writing system calls this term; `syscall` follows the same register-passing discipline with a different register set.

---

*CS 201 · Week 2 · © CSE Department*
