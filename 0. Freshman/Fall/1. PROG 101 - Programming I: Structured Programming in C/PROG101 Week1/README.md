# PROG 101 — Week 1: Types, Variables, and the Memory Model
## Data Representation · Operators · Control Flow

---

## Week Overview

Week 1 goes deep into C's type system and memory model — the foundation everything else rests on. You will understand *why* integers overflow, *why* floating-point arithmetic is approximate, and *how* the compiler stores your variables in memory. By Thursday you will be manipulating bits, tracing loops by hand, and thinking at the machine level.

---

## Schedule

| Day | Event | Topic | Duration |
|-----|-------|-------|----------|
| Tuesday | Lecture 1 | Types, Variables, and the Memory Model | 50 min |
| Wednesday | Lecture 2 | Operators, Expressions, and Bit Manipulation | 50 min |
| Thursday | Lecture 3 | Control Flow: if, switch, while, for | 50 min |
| Monday | **Lab 1** | Memory Layout, Bitlib, Loop Tracing | 2 hours |

---

## Files in This Package

```
PROG101_Week1/
├── README.md
│
├── lectures/
│   ├── Lecture 01 Types Variables Memory.md   ← Types, sizeof, two's complement
│   ├── Lecture 02 Operators Expressions Bits.md ← Operators, precedence, bitwise ops
│   └── Lecture 03 Control Flow.md              ← if/switch/while/for, loop invariants
│
├── lab/
│   ├── LAB 1 Memory Bits Loops.md              ← Lab instructions
│   └── starter/
│       ├── bitlib.h                            ← Header (complete)
│       └── bitlib.c                            ← Implementation skeleton (fill in)
│
├── assignments/
│   └── Problem Set 1.md                       ← PS1: 6 problems, 100 pts
│
├── quizzes/
│   └── QUIZ 1.md                              ← Quiz (Week 2 Tuesday) + answer key
│
└── resources/
    └── Week 1 Reference and Worksheet.md       ← Two's complement worksheet + bit ref
```

---

## Learning Objectives

After Week 1, you will be able to:

- [ ] State the size (bytes) and range of every fundamental C type
- [ ] Explain two's complement representation from first principles
- [ ] Predict the result of integer overflow for signed and unsigned types
- [ ] Explain why `0.1 + 0.2 != 0.3` in floating-point
- [ ] Use `sizeof` correctly, including on arrays and pointers
- [ ] Apply all C operators with correct precedence
- [ ] Rely on short-circuit evaluation to write safe pointer/index guards
- [ ] Set, clear, toggle, and test individual bits using masks and shifts
- [ ] Write correct `if/else if/else`, `switch`, `while`, `do-while`, and `for` loops
- [ ] Trace any loop by hand using a variable table
- [ ] State and apply the loop invariant of a simple loop

---

## Textbook Reading

| Lecture | K&R | King |
|---------|-----|------|
| Lecture 1 | Ch. 2 (Types, Operators, Expressions) §2.1–2.4 | Ch. 7 (Basic Types) |
| Lecture 2 | Ch. 2 §2.5–2.10 | Ch. 4 (Expressions) |
| Lecture 3 | Ch. 3 (Control Flow) — full chapter | Ch. 5 (Selection), Ch. 6 (Loops) |

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
