# CS 201 · Computer Organization & Architecture
## Week 1: Data Representation — Integers and Floating Point

**Credits:** 4 (3 lecture + 1 lab) · **Prerequisites:** PROG 101 (C), ECE 110 (digital logic)
**Assessment for this course (overall):** Problem Sets 35%, Midterms 25%, Final 20%, Projects 20%
**This week's deliverables:** PS 1 (due Week 2 Friday), Lab 1, and **Quiz 1 on Monday, covering Week 0**.

---

### Why This Week Exists

Because everything above this layer assumes the numbers are numbers, and they are not.

ECE 110 gave you two's complement as a *circuit* — you built the adder and watched the overflow flag. This week is about what that means one layer up, where C's type system and the compiler's optimiser both have opinions about arithmetic, and those opinions do not agree with the hardware's.

Two ideas, and they are the same idea:

**Finite representations lose information, and they lose it silently.** Signed overflow, absorption in a sum, cancellation in a subtraction — none of these announce themselves. The value is simply wrong, and the program continues.

**The compiler is a party to this.** Signed overflow being *undefined* is not a statement about the hardware; it is a licence the compiler uses, and it will delete your overflow check. `-ffast-math` will delete your compensated summation. Week 0 ended with the compiler removing a loop and the answer staying right. This week it removes a correction and the answer goes wrong.

---

### Learning Objectives

By the end of Week 1, you should be able to:

1. State the range and anomalies of *n*-bit two's complement, including why $-(-2^{n-1})$ is itself.
2. Explain why signed overflow is undefined in C and unsigned is not, and predict the code each generates.
3. Identify signed/unsigned conversion bugs, including the `strlen(s) - 1` family.
4. Decompose a `float` into sign, biased exponent and mantissa **by hand**, and reconstruct its value.
5. Explain what each reserved exponent encodes, and why denormals exist at all.
6. Say why 0.1 is not representable, and why `0.1 + 0.2 != 0.3` is arithmetic working correctly.
7. Explain absorption, and compute the index at which a summation stops accumulating.
8. Demonstrate non-associativity, and explain why it blocks vectorisation and makes parallel reductions non-reproducible.
9. Recognise catastrophic cancellation and reformulate to avoid it.
10. **Distrust a benchmark that shows no effect.**

---

### This Week's Materials

| File | Purpose |
| --- | --- |
| [[L04 Integers Overflow and Undefined Behaviour]] | Two's complement one layer up; UB as a licence, with the disassembly |
| [[L05 IEEE 754 Anatomy of a Float]] | The three fields, the two reserved exponents, real bit patterns, denormals at 34× |
| [[L06 Why Floating Point Addition Is Not Associative]] | Absorption, summation order, Kahan, cancellation, and why not to use floats for money |
| [[PS 1 Bit Level Manipulation and IEEE 754]] | Hand dissection, branch-free bit tricks, total-order keys, the summation experiment |
| [[CS201 Week1/assignments/QUIZ 1 Week 1 Monday\|QUIZ 1 Week 1 Monday]] | Ten minutes on Week 0. **Unmarked — the key is in the paper** |
| [[LAB 1 Demonstrating Floating Point Non-Associativity]] | Measure all of it yourself, including the benchmark that lies |
| [[CS201 Week1/resources/Reading Guide Week 1\|Reading Guide Week 1]] | CS:APP Ch. 2 with guiding questions and three claims to check |
| `solutions_instructor/` | Instructor only |

---

### The One Thing to Take From This Week

**Every result is an approximation, and the approximation is invisible.**

The forward `float` sum of $\sum 1/i$ over ten million terms is **7.7% wrong** — not in the last digit, in the second. **79% of the terms contribute exactly nothing**, starting precisely at $i = 2^{21}$, and nothing in the program indicates this. No warning, no flag, no exception. It returns a plausible number.

Reversing the loop makes it 139× better. Compensating makes it 1.7 million times better. **A compiler flag makes the compensation vanish.** *(All measured — Lab 1.)*

The skill is not memorising IEEE 754. It is knowing that a floating-point result is a claim, and knowing how to check it.

---

### Assessment Reminder

**Labs and quizzes carry no weight**; the four weighted components already sum to 100%. Both are still required — the lab is checked off in the session, and a second unexcused absence costs a letter grade.

**Quiz 1 is Monday** and covers **Week 0**. It prints its own answer key: sit it closed-book, then mark it yourself before leaving. Looking at the key first costs you the only thing the exercise is for.

Both tracked in [[_CS 201 Lab and Quiz Record]].

---

### Connections

**Back:** **ECE 110** built the two's complement adder and showed that carry-out and signed overflow are independent flags — L04 §1 starts from that and does not re-derive it. **ECE 110's BCD week** reached the same conclusion this week reaches about money, from the hardware side.

**Forward:** Week 2 reads the assembly these types compile to, and the `movss`/`addss` family is a separate instruction set from the integer one. Week 5's SIMD is where non-associativity becomes a *performance* problem rather than an accuracy one, because it is what blocks vectorisation. **Week 9's integer-overflow attacks are L04 §4 with a stack under them.** MATH 341 in Year 3 is this week for a whole semester.

**Sideways:** PROG 201 is using `size_t` everywhere this term. L04 §6 is why that matters.

---

*CS 201 · Week 1 · © CSE Department*
