# CS 201 · Computer Organization & Architecture
## Week 0: From Transistors to Programs

**Credits:** 4 (3 lecture + 1 lab) · **Prerequisites:** PROG 101 (C), ECE 110 (digital logic)
**Assessment for this course (overall):** Problem Sets 35%, Midterms 25%, Final 20%, Projects 20%
**This week's deliverables:** Lab 0 and PS 0. **No quiz** — Quiz 1, in Week 1, covers this week.

> **Week 0 is ten days long**, running Aug 27 to Sep 5. It absorbs orientation, add/drop and Labor
> Day, and Week 1 — when graded work begins — opens Sep 8. You get all three lectures.

---

### Why This Week Exists

Because the rest of the course is an answer, and you need the question first.

You have spent a year writing programs and reasoning about them in the language you wrote them in. **CS 201 is about what is underneath.** Not as trivia — because from Week 4 onward, the questions you will care about (*why is this slow, why is this exploitable, why does this give the wrong answer*) have no answers at the level of C.

This week does three things: it lays out **the layer stack** and what each layer costs, it establishes **the fetch-decode-execute cycle** that every later week refines, and it explains **why performance stopped being free in 2005** — which is the reason Weeks 4, 5, 10 and 11 exist at all.

It also gets the tools into your hands. From Week 1 onward, "look at the disassembly" is an instruction, not a suggestion.

---

### Learning Objectives

By the end of Week 0, you should be able to:

1. Name the layers from transistor to high-level language, and state for each what it hides and what the hiding costs.
2. Explain why the ISA is a contract, and give a consequence that would not hold otherwise.
3. Trace an instruction through fetch, decode, execute, memory and writeback.
4. Compute a relative branch target by hand, and say why the displacement is measured from the *next* instruction.
5. Explain the trade-off in x86-64's variable-length encoding, and why fixed-length ISAs chose differently.
6. Distinguish Moore's Law from Dennard scaling, and say which one ended and what followed.
7. Name the sixteen general-purpose registers and describe the four access widths, including the 32-bit zeroing rule.
8. Compile, disassemble and step through a C program without looking up the commands.
9. **Demonstrate that the compiler does not execute your source** — and say what it is permitted to do instead.

---

### This Week's Materials

| File | Purpose |
| --- | --- |
| [[L01 The Abstraction Hierarchy]] | The layer stack; the ISA as contract; Python vs C measured at 46× |
| [[L02 Von Neumann and the Fetch-Decode-Execute Cycle]] | Stored programs, the five stages, a real function decoded by hand |
| [[L03 Moores Law and the Shape of x86-64]] | Dennard scaling and the power wall; registers, flags, CISC-over-RISC |
| [[LAB 0 From C to Machine Code]] | The toolchain, and the compiler deleting a loop in front of you |
| [[CS201 Week0/assignments/Problem Set 0\|Problem Set 0]] | Layers, hand-decoding, a full cycle trace, cache geometry |
| [[CS201 Week0/resources/Course Overview Syllabus\|Course Overview Syllabus]] | **Read this in full in Week 0** — assessment, the unweighted-lab rule, deviations |
| [[CS201 Week0/resources/Reading Guide Week 0\|Reading Guide Week 0]] | CS:APP Ch. 1 with guiding questions, and two numbers to check against your own machine |
| `solutions_instructor/` | Instructor only |

---

### The One Thing to Take From This Week

**The machine does not run your source code.**

It runs whatever the compiler decided was equivalent, executing on hardware that reorders, caches and speculates. Everything in Lab 0 Part 4 is one demonstration of this: a hundred-million-iteration loop that does not exist in the compiled program, because GCC computed the answer during compilation and emitted it as a constant.

**This is not a trick, and it is not rare.** It is the ordinary condition of running code on a real machine. The skill this course builds is knowing when the gap between your source and the machine matters, and having the tools to see across it when it does.

---

### Assessment Reminder

**Labs and quizzes carry no weight.** The curriculum's assessment line sums to 100% without them, and no percentage has been invented to fill the gap.

They are still required. **The lab is checked off by the TA in the session**, and a second unexcused absence costs a letter grade — because a lab you can skip for a 2% penalty is a lab you will skip in the week you are busiest, which is reliably the week the material is hardest. **Quiz *N* covers Week *N−1***, runs ten minutes at the start of Monday's lecture in Weeks 1–11, and prints its own answer key.

Both are tracked in [[_CS 201 Lab and Quiz Record]].

---

### Connections

**Back:** **ECE 110 is a hard prerequisite.** Gates, adders, multiplexers, flip-flops and the carry/overflow distinction are used from here on without re-teaching — Lecture 3 §5 already leans on your having built an adder and seen CF and OF behave independently. **PROG 101** supplies the C; this course never explains a pointer.

**Sideways:** **PROG 201 runs alongside and assumes this course.** The address space, the process, and the calling convention are CS 201 concepts used there as vocabulary. If the two ever seem to conflict, CS 201 is describing the hardware and PROG 201 the kernel interface to it.

**Forward:** Lecture 2's cycle becomes Week 5's pipeline. Lecture 3's cache geometry becomes Week 4's central experiment and Week 10's coherence problem. Lecture 3's register table becomes Week 3's calling convention — and Week 9's buffer overflow, which works precisely because you know where the return address sits.

---

*CS 201 · Week 0 · © CSE Department*
