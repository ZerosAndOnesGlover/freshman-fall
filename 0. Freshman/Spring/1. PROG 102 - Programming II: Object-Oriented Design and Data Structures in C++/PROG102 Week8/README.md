# PROG 102 · Programming II — Object-Oriented Design and Data Structures in C++
## Week 8: Design Patterns II — Behavioural

**Credits:** 4 (3 lecture + 1 lab) · **Prerequisites:** PROG 101 (C), CS 101
**Assessment for this course (overall):** Labs 20%, Problem Sets 30%, Midterms 25%, Final 15%, Projects 10%
**This week's deliverables:** PS 8 (released Fri 19 Mar 10:00, due **Fri 26 Mar 17:00**), Lab 8 (**Mon 22 Mar**, 15:00), Quiz 8 (**Tue 16 Mar**, 10:00, covers Week 7) · Project 1 due next Friday, 26 Mar

---

### Why This Week Exists

Week 7's patterns were about **structure** — how objects are arranged. This week's are about
**behaviour**: who talks to whom, who decides what, and how responsibility moves at run time.

They are the patterns you will meet most often, because they are what event-driven and configurable
software is made of. **Observer** is every GUI, every spreadsheet, every reactive framework.
**Strategy** is every pluggable algorithm. **Command** is every undo stack.

And this week ends somewhere the previous one did not: **two of these patterns are largely obsolete in
modern C++**, not because they were wrong but because C++11 added the language feature they were
working around. Lecture 27 §4 makes that case with line counts and a benchmark.

### Learning Objectives

By the end of Week 8, you should be able to:

1. Implement **Observer**, and demonstrate the dangling-observer bug that the naive version has.
2. Fix it with `weak_ptr`, and explain why that also solves the deregistration problem.
3. Implement **Strategy**, **Command** (with undo), **Template Method** and **State**.
4. **Measure** four ways of expressing a strategy and explain why the ranking is not what you expect.
5. Explain the Open/Closed Principle and say which patterns embody it.
6. Describe **MVC** and say what it is and is not.
7. Argue which patterns C++11 made unnecessary — **and which it did not**.

### This Week's Materials

| File | Purpose |
| --- | --- |
| [[L25 Observer]] | Publish-subscribe, the dangling observer, and `weak_ptr` |
| [[L26 Strategy Command and Template Method]] | Three ways of parameterising behaviour |
| [[L27 State MVC and What C++11 Obsoleted]] | State machines, MVC, and the week's argument |
| [[PS 8 Observer and Strategy]] | Due Fri 26 Mar 17:00 |
| [[PROG102 Week8/assignments/QUIZ 8 Week 8 Monday\|QUIZ 8 Week 8 Monday]] | 15 minutes, covers Week 7 |
| [[LAB 8 Building an Event System]] | An event system that survives its subscribers dying |
| [[PROG102 Week8/resources/Reading Guide Week 8\|Reading Guide Week 8]] | Gang of Four Ch. 5, and every command |
| [[PROG102 Week8/solutions_instructor/PS 8 Solutions\|PS 8 Solutions]] | Instructor only |
| [[PROG102 Week8/solutions_instructor/LAB 8 Solutions\|LAB 8 Solutions]] | Instructor only |

### The One Thing to Take From This Week

**A pattern is a workaround for something the language cannot say.**

Strategy exists because, in 1994, C++ had no way to pass "a piece of behaviour" as a value. You could
pass a function pointer — which carries no state — or a class instance with a virtual method, which is
the pattern. **Both are ways of faking a closure in a language that did not have them.**

C++11 added closures. So Strategy became `auto f = [k](int x){ return x + k; };` and the pattern became
a paragraph in a book about how things used to be done.

**That is not a criticism of the Gang of Four.** It is what happens to good engineering advice when the
substrate improves, and recognising it is the difference between knowing patterns and understanding
them.

### The Measurement That Surprises Everyone

Four ways to give `std::sort` a comparison, on 2,000,000 integers:

| How | Time |
| --- | --- |
| Classic Strategy (virtual call) | 165.7–167.6 ms |
| **`std::function`** | **287.5–304.1 ms** |
| Lambda (template parameter) | 159.9–160.9 ms |
| Default `operator<` | 149.9–151.2 ms |

**`std::function` is the slowest — nearly twice the lambda, and worse than the virtual call.**

Almost everyone predicts the opposite, because `std::function` looks like "the modern way". It is
**type erasure**, which means an indirect call that cannot be inlined — the same mechanism that made
`qsort` twice as slow as `std::sort` back in **Week 3 §L12 §2**, reappearing under a modern name.

### Project 1 Is Due Next Friday

**Week 9 is exception safety and it is a full week.** If Project 1's Parts 1 and 2 are not working
now, this weekend is the time.

### Connections

**Back:** **Week 5**'s `weak_ptr` is what makes Observer safe. **Week 7**'s two principles are what
these patterns implement. **Week 3**'s `qsort` result explains this week's `std::function` benchmark.

**Forward:** **Week 9**'s exception safety asks what happens when an observer throws during
notification. **Week 11** is lambdas and `std::function` properly, and revisits this week's benchmark
with the mechanism explained. **Week 10**'s threads make the Observer's registration list a shared
mutable structure, which is a different problem entirely.

---

*PROG 102 · Week 8 · © CSE Department*
