# PROG 102 · Programming II — Object-Oriented Design and Data Structures in C++
## Week 0: C to C++ — Classes and Objects

**Credits:** 4 (3 lecture + 1 lab) · **Prerequisites:** PROG 101 (C), CS 101
**Assessment for this course (overall):** Labs 20%, Problem Sets 30%, Midterms 25%, Final 15%, Projects 10%
**This week's deliverables:** PS 0, Lab 0. **No quiz** — Quiz 1, in Week 1, covers this week.

---

### Why This Week Exists

Because the most useful fact about C++ is one you can verify in an afternoon, and almost nobody is
told it first:

> **A class is a struct whose functions take the object as a hidden first argument.**

That is not a simplification for beginners. It is what the compiler does, and Lecture 01 proves it by
compiling a member function and the equivalent C function and showing the generated assembly is
**byte-for-byte identical**.

Starting here matters because C++ spends the next twelve weeks stacking abstractions on top of this
one mechanism. Students who never see the bottom of the stack end up treating `virtual`, templates and
smart pointers as magic with unpredictable costs. You are coming from C, so you do not have to.

### A Note on Lecture 00

**Week 0 has four lecture files but three timetabled lectures.** `L00` is the orientation-session
primer and is not one of the three; Lectures 01–03 are Monday, Wednesday and Friday as usual. The
same holds for the numbering across the course — **L01–L39 are the 39 timetabled lectures**, three per
week for thirteen weeks, and L00 sits outside that count.

It exists because Lectures 01–03 use notation that is not in C — references, `::`, `new`/`delete`,
`auto`, overloading, `static_assert` — and teaching the *meaning* of classes while the *syntax* is
still unfamiliar makes both harder than they need to be. **Read L00 before Lecture 01**, then keep it
open as a reference for the first fortnight.

If you already write some C++, skim it and read §5 on references properly. References are the one
construct in it with no C equivalent, and everything from Lecture 02 onward assumes them.

### Learning Objectives

By the end of Week 0, you should be able to:

1. Explain what `obj.method(args)` compiles to, and name the register `this` arrives in on x86-64.
2. Show from `sizeof` that member functions add **nothing** to an object's size, and say where the code lives instead.
3. Read a mangled C++ symbol well enough to recover the function's namespace, class and parameter types.
4. Say why a function defined inside a class body is implicitly `inline`, and what that does to the emitted symbol.
5. Write constructors using a **member initializer list**, and state the two cases where the list is not optional.
6. Predict the exact order of constructor and destructor calls for a scope containing several objects.
7. State what `private` actually prevents — and demonstrate that it is a compile-time rule, not a runtime barrier.
8. Explain what `const` on a member function does to the type of `this`, and read the compiler error when it is violated.
9. Distinguish `class` from `struct` in C++ **completely** — there is exactly one difference.

### This Week's Materials

| File | Purpose |
| --- | --- |
| `lectures/L00 C++ Syntax for C Programmers.md` | **Read first.** The notation Lectures 01–03 assume — references, `::`, `new`/`delete`, `auto`, overloading |
| `lectures/L01 From C to C++.md` | The `this` pointer proved in assembly, object size, name mangling, `extern "C"` |
| `lectures/L02 Constructors Destructors and Object Lifetime.md` | Initializer lists, lifetime, destruction order, the road to RAII |
| `lectures/L03 Encapsulation const and Namespaces.md` | Access control, `const` member functions, `inline`, namespaces |
| `assignments/PS 0 Classes Constructors and const.md` | Due Friday of Week 1 |
| `lab/LAB 0 Porting C to C++.md` | Port a working C program to C++ — and confirm your toolchain |
| `resources/Course Overview Syllabus.md` | **Read this in full in Week 0** — assessment, the two build lines, policies |
| `resources/Reading Guide Week 0.md` | *C++ Primer* Ch. 1–2 with guiding questions, plus the commands to reproduce every lecture measurement |
| `solutions_instructor/PS 0 Solutions.md` | Instructor only |
| `solutions_instructor/LAB 0 Solutions.md` | Instructor only |

### The One Thing to Take From This Week

**C++ does not hide the machine from you; it hides the machine from your source code.** The two are
different claims, and the difference is the whole course.

Every abstraction you meet after this week — operators, templates, virtual functions, smart pointers,
lambdas — compiles down to something you could have written in C. Some compile down to *exactly* what
you would have written, and cost nothing. Some do not. **Week 0's job is to establish that you can
always go and look**, using `g++ -S`, `nm`, and `sizeof`, and that looking is normal practice rather
than an advanced technique.

### A Note on the Lab

Lab 0 is partly a toolchain check, and that is not filler. You need `g++`, `gdb`, `valgrind`,
AddressSanitizer, ThreadSanitizer and `perf` working **on the machine you will actually use**.

Discovering in Week 10 that you cannot run ThreadSanitizer is a genuinely bad week to discover it —
Week 10 is a midterm week. Twenty minutes now is the cheapest this check will ever be.

### Assessment Reminder

**Labs are weighted in this course** — 20%, a graded component, not a completion gate. This differs
from CS 102, which you are taking concurrently, where labs are ungraded but gated at 10 of 13. Do not
carry the CS 102 habit across: here, a missed lab costs you marks directly.

**Quizzes carry no weight** and are tracked separately. **Quiz *N* covers Week *N−1***.

### Connections

**Back:** PROG 101 supplies pointers, `struct`, the heap/stack distinction, and `malloc`/`free`. All
are used from Lecture 01 without re-teaching. CS 101 supplies the algorithmic vocabulary.

**Forward:** the `this` pointer from Lecture 01 is what makes operator overloading readable in
**Week 1** and what the vtable extends in **Week 4**. Destruction order from Lecture 02 is the entire
mechanism behind RAII in **Week 5** and exception safety in **Week 9**. `const`-correctness from
Lecture 03 is assumed by every STL algorithm in **Week 3**.

---

*PROG 102 · Week 0 · © CSE Department*
