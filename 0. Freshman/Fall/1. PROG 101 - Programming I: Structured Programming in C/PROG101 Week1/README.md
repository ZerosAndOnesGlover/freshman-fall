# PROG 101 · Week 1: Types, Variables, and the Memory Model
## Data Representation · Integers · Floating Point

---

## Week Overview

Week 1 goes deep into C's type system and memory model — the foundation everything else rests on. You will understand *why* integers overflow, *why* floating-point arithmetic is approximate, and *how* the compiler stores your variables in memory. By Monday's lab you will be reading your variables' bytes in GDB and thinking at the machine level.

---

## Schedule

| Day | Event | Topic | Duration |
|-----|-------|-------|----------|
| Tue 29 Sep | **Quiz 0** + Lecture 1 | Types, Variables, and the Memory Model | 50 min |
| Wed 30 Sep | Lecture 2 | Integer Representation | 50 min |
| Thu 1 Oct | Lecture 3 | Floating-Point and Type Conversions | 50 min |
| Mon 5 Oct, 15:00 (Week 2) | **Lab 1** | Memory and representation, seen through GDB | 2 hours |

**Problem Set 1** released Thursday 1 October, 11:00, due Friday 9 October, 17:00. Quiz 0 covers Week 0 material; **Quiz 1 is administered in Week 2** and covers this week.

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
│   ├── LAB 1 Memory and Representation.md          ← Lab instructions (20 pts, 2 hrs)
│   └── starter/
│       └── explore.c                               ← Variables to inspect in GDB
│
├── assignments/
│   └── Problem Set 1.md                            ← PS1: 5 problems, 100 pts
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
- [ ] Read two's-complement and IEEE 754 bit patterns straight out of memory

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

**1. Mixing signed and unsigned in comparisons**
```c
int len = strlen(s);            // WRONG: strlen returns size_t (unsigned)
if (len - 1 >= 0) ...          // Always true! (unsigned can't be < 0)
size_t len = strlen(s);        // CORRECT type for sizes
```

**2. Forgetting & in scanf**
```c
scanf("%d", x);    // WRONG: passes value, not address
scanf("%d", &x);   // CORRECT
```

**3. Integer division when you want float division**
```c
double avg = total / count;         // Integer division!
double avg = (double)total / count; // Correct
```

**4. Using wrong format specifier**
```c
double x = 3.14;
printf("%d", x);   // WRONG: %d reads 4 bytes as int; double is 8 bytes → garbage
printf("%f", x);   // CORRECT
```

---

---

*PROG 101 · Week 1*
