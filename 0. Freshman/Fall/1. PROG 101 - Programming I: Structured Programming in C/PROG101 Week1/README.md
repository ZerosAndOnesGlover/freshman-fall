# PROG 101 · Week 1: Types, Variables, and the Memory Model
## Data Representation · Integers · Floating Point

---

## Week Overview

Week 1 goes deep into C's type system and memory model — the foundation everything else rests on. You will understand *why* integers overflow, *why* floating-point arithmetic is approximate, and *how* the compiler stores your variables in memory. By Monday's lab you will be manipulating bits, tracing loops by hand, and thinking at the machine level.

---

## Schedule

| Day | Event | Topic | Duration |
|-----|-------|-------|----------|
| Tuesday | **Quiz 0** + Lecture 1 | Types, Variables, and the Memory Model | 50 min |
| Wednesday | Lecture 2 | Integer Representation | 50 min |
| Thursday | Lecture 3 | Floating-Point and Type Conversions | 50 min |
| Monday (Week 2) | **Lab 1** | Memory Layout, Bitlib, Loop Tracing | 2 hours |

**Problem Set 1** released after Thursday's lecture, due before Week 2 Lecture 1 (Tuesday). Quiz 0 covers Week 0 material; **Quiz 1 is administered in Week 2** and covers this week.

---

## Files in This Package

```
PROG101 Week1/
├── README.md
│
├── lectures/
│   ├── Lecture 01 Types Variables Memory.md        ← Types, sizeof, stack vs static
│   ├── Lecture 02 Integer Representation.md        ← Two's complement, overflow, signed/unsigned
│   └── Lecture 03 Floating Point and Conversions.md ← IEEE 754, NaN, conversion rules
│
├── lab/
│   ├── LAB 1 Memory Bits Loops.md                  ← Lab instructions (20 pts, 2 hrs)
│   └── starter/
│       ├── bitlib.h                                ← Header (complete)
│       └── bitlib.c                                ← Implementation skeleton (fill in)
│
├── assignments/
│   └── Problem Set 1.md                            ← PS1: 6 problems, 100 pts
│
├── resources/
│   └── Week 1 Reference and Worksheet.md           ← Two's complement worksheet + bit ref
│
└── solutions_instructor/
    └── LAB 1 Solutions.md                          ← Instructor only
```

There is no quiz packaged with this week. Quiz 0 (in `PROG101 Week0/quizzes/`) is sat on Tuesday of this week; Quiz 1 (in `PROG101 Week2/quizzes/`) covers Week 1 and is sat in Week 2.

---

## Learning Objectives

After Week 1, you will be able to:

From the lectures:

- [ ] State the size (bytes) and range of every fundamental C type
- [ ] Explain two's complement representation from first principles
- [ ] Predict the result of integer overflow — and say why signed and unsigned differ *fundamentally*
- [ ] Recognise the signed/unsigned comparison trap before it costs you a day
- [ ] Explain why `0.1 + 0.2 != 0.3` in floating-point, and predict which values *are* exact
- [ ] Handle infinity, NaN, and negative zero without being surprised
- [ ] Apply C's implicit conversion and promotion rules deliberately
- [ ] Use `sizeof` correctly, including on arrays and pointers
- [ ] Describe where a variable lives — stack or static — and for how long

From the lab and reference card:

- [ ] Inspect a variable's bytes in memory with GDB and read them back as a value
- [ ] Set, clear, toggle, and test individual bits using masks and shifts
- [ ] Trace any loop by hand using a variable table
- [ ] State and apply the loop invariant of a simple loop

---

## Textbook Reading

| Lecture | K&R | King |
|---------|-----|------|
| Lecture 1 | Ch. 2 (Types, Operators, Expressions) §2.1–2.4 | Ch. 7 (Basic Types) |
| Lecture 2 | §2.2, §2.9 (data types, bitwise operators) | Ch. 7 §7.1–7.2 |
| Lecture 3 | §2.7 (type conversions) | Ch. 7 §7.3–7.4 |

Each lecture closes with its own reading list — `<limits.h>` and `<float.h>` on your own system, the relevant C11 clauses, Goldberg on floating-point. Those are the ones that matter.

Also read: **CS:APP §2.1–2.3** (Information Storage, Integer Representations, Integer Arithmetic) — this covers two's complement and overflow at a depth that no other source matches. These 50 pages will transform how you think about data.

---

## The Key Idea of This Week

C is a thin layer over the machine. When you write:

```c
int x = -42;
```

The compiler:
1. Allocates 4 bytes on the stack
2. Stores the two's complement representation of -42 in those bytes: `0xFFFFFFD6`
3. Associates the name `x` with the address of those bytes (name only exists at compile time)

At runtime: there is no `x`. There are 4 bytes at some address, containing `D6 FF FF FF` (on a little-endian system). The type `int` tells the CPU to interpret those bytes as a two's complement signed integer.

This is the mental model you are building this week. Once you have it, low-level bugs become *understandable* — because you know exactly what the machine is doing.

---

## The Most Common Week 1 Mistakes

**1. Off-by-one in loops**
```c
for (int i = 0; i <= n; i++)    // Accesses arr[n] — out of bounds!
for (int i = 0; i < n;  i++)    // Correct: accesses arr[0..n-1]
```

**2. Mixing signed and unsigned in comparisons**
```c
int len = strlen(s);            // WRONG: strlen returns size_t (unsigned)
if (len - 1 >= 0) ...          // Always true! (unsigned can't be < 0)
size_t len = strlen(s);        // CORRECT type for sizes
```

**3. Forgetting & in scanf**
```c
scanf("%d", x);    // WRONG: passes value, not address
scanf("%d", &x);   // CORRECT
```

**4. Integer division when you want float division**
```c
double avg = total / count;         // Integer division!
double avg = (double)total / count; // Correct
```

**5. Using wrong format specifier**
```c
double x = 3.14;
printf("%d", x);   // WRONG: %d reads 4 bytes as int; double is 8 bytes → garbage
printf("%f", x);   // CORRECT
```

---

## Challenge Problems (Optional, No Credit)

These are for students who want to go deeper:

1. **The Gray Code:** Write a function `int to_gray(int n)` that converts a binary integer to its Gray code (each consecutive pair of values differs by exactly one bit). Then write `int from_gray(int g)` that converts back. Use only bit operations.

2. **Integer Square Root:** Write `int isqrt(unsigned int n)` that returns the integer square root of n (floor of √n) using only integer arithmetic — no `<math.h>`, no floating point. Hint: binary search, or Newton's method with integers.

3. **Rotate Bits:** Write `uint32_t rotate_left(uint32_t x, int n)` that rotates the bits of x left by n positions (bits shifted off the left end wrap around to the right). Do this without any branching. Warning: a naive shift-based approach has undefined behavior — think carefully.

4. **Collatz Conjecture:** For any positive integer n: if n is even, divide by 2; if odd, multiply by 3 and add 1. Repeat. The conjecture is that this always eventually reaches 1. Write a program that: (a) computes the Collatz sequence for a given n, (b) finds the number under 1,000,000 with the longest Collatz sequence, (c) uses only `int` arithmetic and detects if overflow would occur.
