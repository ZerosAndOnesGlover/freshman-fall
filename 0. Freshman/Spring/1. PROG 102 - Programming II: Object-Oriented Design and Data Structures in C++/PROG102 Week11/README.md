# PROG 102 · Programming II — Object-Oriented Design and Data Structures in C++
## Week 11: Functional Programming in C++ and Modern Features

**Credits:** 4 (3 lecture + 1 lab) · **Prerequisites:** PROG 101 (C), CS 101
**Assessment for this course (overall):** Labs 20%, Problem Sets 30%, Midterms 25%, Final 15%, Projects 10%
**This week's deliverables:** PS 11, Lab 11, Quiz 11 (Monday, covers Week 10) · **Project 2 assigned**

---

### Why This Week Exists

You have been using lambdas since **Week 3**. You passed one to `std::count_if`, to `std::sort`, to
`std::thread`, to `remove_if`. Nobody ever told you what one *is*.

**This week closes three loops the course deliberately left open:**

- **Week 2** said a template is a class the compiler writes for you. **A lambda is also a class the
  compiler writes for you**, and Lecture 34 shows it is *the same size* as the one you would write.
- **Week 8** measured `std::function` as the slowest of four ways to pass a comparison and attributed
  it to type erasure. **Lecture 35 shows the mechanism** — and finds a second cost nobody mentions.
- **Week 10** had you passing lambdas to threads. **Lecture 34 §5** shows the capture bug that makes
  that dangerous, and it is one your compiler does not warn about.

### Learning Objectives

By the end of Week 11, you should be able to:

1. Explain what a lambda **is** — the class, the captured members, the call operator.
2. Predict `sizeof` a lambda from its capture list.
3. Choose between `[=]`, `[&]`, `[x]`, `[&x]` and `[x = expr]`, and say what each costs.
4. **Demonstrate the dangling-capture bug**, and explain why the compiler is silent about it.
5. Explain type erasure, and say when `std::function` is the right tool despite its cost.
6. **Find the capture size at which `std::function` starts heap-allocating.**
7. Use `constexpr` for compile-time computation, and prove the computation happened at compile time.
8. Use `if constexpr` and structured bindings.
9. Rewrite an imperative loop in functional style — **and say when not to.**

### This Week's Materials

| File | Purpose |
| --- | --- |
| `lectures/L34 Lambdas and Closures.md` | What a lambda is, captures, and the dangling bug |
| `lectures/L35 std function and Type Erasure.md` | The mechanism, the hidden allocation, and when to use it |
| `lectures/L36 constexpr and Modern Features.md` | `constexpr`, `if constexpr`, structured bindings, ranges preview |
| `assignments/PS 11 Imperative to Functional.md` | Due Friday of Week 12 |
| `assignments/QUIZ 11 Week 11 Monday.md` | 15 minutes, covers Week 10 |
| `assignments/PROJECT 2 A Data Structure Library.md` | **Assigned this week, due Week 12** |
| `lab/LAB 11 Profiling Lambda Overhead.md` | Measure the three ways to hold a callable |
| `resources/Reading Guide Week 11.md` | Meyers Items 31–34, and every command |
| `solutions_instructor/PS 11 Solutions.md` | Instructor only |
| `solutions_instructor/LAB 11 Solutions.md` | Instructor only |

### The One Thing to Take From This Week

**A lambda is a class. `std::function` is a box you put it in, and the box costs more than the thing.**

Measured, per call:

| | ns |
| --- | --- |
| lambda called directly | **0.61–0.67** |
| function pointer | **1.50–1.54** |
| `std::function` | **2.15–2.21** |

**Three and a half times**, for the same lambda, differing only in how it is stored. Week 8 saw the
consequence inside `std::sort`; this week is the cause.

### The Measurement Nobody Expects

`std::function` has a **small-buffer optimization**: small callables live inside it, large ones go on
the heap. The threshold on the reference machine:

| capture size | allocations |
| --- | --- |
| 1, 8, **16** bytes | **0** |
| **17** bytes | **1 — heap** |

**Sixteen bytes.** Capture two pointers and you are fine; capture a third, or a `std::string`, and
every `std::function` construction silently allocates.

**That is a number worth carrying**, because nothing in the type system or the compiler will tell you
which side of it you are on.

### Project 2 Is Assigned This Week

**Due Week 12** — the capstone: a data structure library with a full test suite. It is worth 5%
directly and its demo is Lab 12, and **the final exam draws its questions from it.** Read the
specification this week.

### Connections

**Back:** **Week 2**'s templates are what make a lambda usable as a parameter. **Week 3**'s algorithms
take them. **Week 8**'s benchmark is explained here. **Week 10**'s threads take them, dangerously.

**Forward:** **Week 12** is testing, profiling and cache behaviour — and Lab 11's numbers feed directly
into it.

---

*PROG 102 · Week 11 · © CSE Department*
