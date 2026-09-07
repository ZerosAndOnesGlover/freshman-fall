# PROG 102 · Programming II: Object-Oriented Design and Data Structures in C++
## Course Overview and Syllabus
### Year 1 · Spring · 4 credits

---

## Course Identity

| | |
| --- | --- |
| **Code** | PROG 102 |
| **Title** | Programming II: Object-Oriented Design and Data Structures in C++ |
| **Credits** | 4 (3 lecture + 1 lab) |
| **Semester** | Spring, Year 1 |
| **Meeting** | 3 lectures per week + one 2-hour lab section |
| **Prerequisites** | **PROG 101 (C), CS 101** |
| **Language** | **C++ (C++17 standard)** |
| **Assessment** | **Labs 20%, Problem Sets 30%, Midterms 25%, Final 15%, Projects 10%** |

---

## Course Description

PROG 102 teaches C++ and object-oriented programming. C++ is chosen because it is two languages at
once: a high-level OOP language *and* a systems language. It extends C with classes, templates and
the STL while preserving C's control over memory.

**Learning C++ after C is the ideal progression, because you already know what the abstractions are
built on.** When you write `v[i]` on a `std::vector`, you know there is a pointer and an offset
underneath, because you wrote that pointer and offset by hand last semester. Students who meet C++
first have to take the abstractions on faith. You do not.

OOP is a design paradigm, not a set of language features. Encapsulation, inheritance, polymorphism
and abstraction are principles for managing complexity in large systems. This course teaches them in
C++ while simultaneously **rebuilding, from scratch, the data structures you studied in CS 101 and are
studying in CS 102** — linked lists, trees, hash tables and graphs, using templates.

By the end you will have implemented enough of the STL to understand why it is designed the way it is.

---

## The Thesis of This Course

CS 102 runs on a single sentence: *every algorithm is correct under an assumption.* PROG 102 has its
own, and it is the reason this course is full of measurements:

> **Every abstraction in C++ has a cost. Name it, measure it, then decide whether to pay it.**

C++ is unusual in that most of its abstractions cost *nothing at runtime* — templates, `unique_ptr`,
and range-`for` all compile to what you would have written by hand. But some cost a great deal, and
the language does not tell you which is which. A virtual call costs an indirection. A `shared_ptr`
copy costs an atomic increment. A `std::function` costs an indirect call and possibly a heap
allocation. A linked list costs a cache miss per node.

**None of these are reasons to avoid the feature.** They are reasons to know the number. Every week
of this course you will measure one of them yourself, and by Week 12 you will have a table of what
your tools actually cost on real hardware — which is a thing very few working C++ programmers can
claim.

---

## What Changes From PROG 101

PROG 101 taught you C: manual memory, raw pointers, `malloc` and `free`, and the discipline of
freeing everything you allocate. Four things change.

1. **The destructor replaces `free()`.** In C, cleanup is a thing you remember to do. In C++, it is a
   thing the language does when an object leaves scope. This one mechanism — RAII — is the foundation
   of everything in Weeks 5, 9 and 10.
2. **The compiler generates code for you, and you must know what it generated.** Copy constructors,
   assignment operators, and template instantiations all appear without you writing them. The Rule of
   Three (Week 1) exists because the *generated* copy constructor is wrong for any class holding a
   pointer.
3. **Types can be parameters.** A template is a program that runs at compile time and emits a class.
   This is why `Stack<int>` and `Stack<std::string>` are, to the compiler, unrelated types.
4. **You will write less code that manages memory, and more code that manages ownership.** The
   question stops being "who calls `free`?" and becomes "who owns this?" — and `unique_ptr`,
   `shared_ptr` and `weak_ptr` are three different answers.

**PROG 101 is a hard prerequisite.** Pointers, arrays, the heap/stack distinction, and `struct` are
used from Week 0 without re-teaching.

---

## Weekly Schedule

| Week | Topic | Assessments |
| --- | --- | --- |
| **0** | C to C++: Classes and Objects | PS 0, Lab 0 |
| **1** | Operator Overloading and Copy Semantics | PS 1, Lab 1, Quiz 1 |
| **2** | Templates and Generic Programming | PS 2, Lab 2, Quiz 2 |
| **3** | The Standard Template Library (STL) | PS 3, Lab 3, Quiz 3 |
| **4** | Inheritance and Polymorphism | PS 4, Lab 4, Quiz 4 · *Midterm 1 announced* |
| **5** | Memory Management and RAII | PS 5, Lab 5, Quiz 5 · **MIDTERM 1** (Weeks 0–4) |
| **6** | Implementing Data Structures: Linked Lists and Trees | PS 6, Lab 6, Quiz 6 · **Project 1 assigned** |
| **7** | Design Patterns I: Creational and Structural | PS 7, Lab 7, Quiz 7 |
| **8** | Design Patterns II: Behavioral | PS 8, Lab 8, Quiz 8 |
| **9** | Exception Handling and Robust Software | PS 9, Lab 9, Quiz 9 · **Project 1 due** |
| **10** | Concurrency: Threads and Synchronization | PS 10, Lab 10, Quiz 10 · **MIDTERM 2** (Weeks 5–9) |
| **11** | Functional Programming in C++ and Modern Features | PS 11, Lab 11, Quiz 11 |
| **12** | Software Engineering: Testing, Profiling, and Systems Design | Lab 12 · **FINAL EXAM** · **Project 2 due** |

---

## Assessment Breakdown

| Component | Weight | Details |
| --- | --- | --- |
| **Labs (13)** | 20% | Labs 0–12, one per week, marked on an in-lab checkoff. **Lowest 1 dropped.** |
| **Problem Sets (12)** | 30% | PS 0–11, released Friday, due the following Friday. **Lowest 1 dropped.** No problem set in Week 12. |
| **Midterm Exam 1** (Week 5) | 12.5% | 75 minutes. Covers Weeks 0–4. One handwritten sheet, 1 side. |
| **Midterm Exam 2** (Week 10) | 12.5% | 75 minutes. Covers Weeks 5–9. Same rules. |
| **Final Exam** (Week 12) | 15% | Comprehensive, 180 minutes. Two handwritten sheets. |
| **Project 1** (assigned Week 6, due Week 9) | 5% | A substantial implementation with a written analysis. |
| **Project 2** (due Week 12) | 5% | The capstone: a data structure library with tests. |
| **Total** | **100%** | |

> **These weights come directly from the Year 1 curriculum document**, which specifies *Labs 20%,
> Problem Sets 30%, Midterms 25%, Final 15%, Projects 10%*. The only elaboration is the split of
> Midterms into two equal halves and Projects into two equal halves. **No component has been added or
> removed.**

### A Note on Project 2's Weight

Project 2 is the largest single piece of work in the course — a templated data structure library with
a full test suite — and the table above says it is worth 5%. That looks wrong, and students ask about
it every year, so here is the actual arithmetic.

**Project 2 is assessed twice.** The artefact is worth 5%. The demo and code review of that artefact
**is Lab 12**, which is part of the 20% lab component. The curriculum document is explicit about this:
Week 12's lab *is* "final project demo and code review".

So the real weight is closer to **6.5%**, and more importantly, Project 2 is the thing the Week 12
final exam questions are drawn from. **Building it is how you revise.** Treating it as a 5% throwaway
is the single most reliable way to have a bad final exam.

### Quizzes Carry No Direct Weight

The assessment line above sums to 100% without them, and that is what the curriculum specifies.
**They are still required.**

Quizzes are 15 minutes at the start of Monday's lecture, Weeks 1–11. **Quiz *N* covers Week *N−1***
— the same convention as CS 101 and CS 102. They are marked and returned quickly so that you and the
staff can see where you stand *before* an exam makes it expensive.

In a language this large, the failure mode is not misunderstanding one idea. It is quietly not
noticing that you never understood references, and discovering that in Week 5 when `unique_ptr` stops
making sense. **The quizzes exist to catch that in Week 2.**

---

## Language and Toolchain

**The course standard is C++17**, as specified by the curriculum document. Code that requires C++20
or later will not be accepted, with one signposted exception: Week 11 *discusses* the C++20 ranges
library for context, and clearly marks which parts you cannot use.

### The Two Build Lines

You will use exactly two commands all semester. Learn them in Week 0.

**Development — always use this one:**

```
g++ -std=c++17 -Wall -Wextra -pedantic -g -fsanitize=address,undefined prog.cpp -o prog
```

**Measurement — only for timing runs:**

```
g++ -std=c++17 -O2 -Wall -Wextra prog.cpp -o prog
```

> **Never time a sanitizer build.** AddressSanitizer makes programs several times slower. Every
> timing table in this course was produced with the `-O2` line, and every correctness claim with the
> sanitizer line. **Mixing them up is the most common source of a nonsensical lab result.**

### Required Tools

| Tool | Used from | For |
| --- | --- | --- |
| **g++ 13.3** | Week 0 | The reference compiler. Anything newer is fine; report your version. |
| **gdb** | Week 4 | Inspecting the vtable by hand |
| **AddressSanitizer** | Week 5 | Leak and use-after-free detection |
| **valgrind** | Week 5 | Second opinion on leaks; slower but catches different things |
| **ThreadSanitizer** | Week 10 | Race detection — the only practical way to find these |
| **perf** | Week 12 | Cache misses and profiling |

**All of these are free and available on the lab machines.** Week 0's lab is partly about confirming
your own machine has them, because discovering in Week 10 that you cannot run ThreadSanitizer is a bad
week to discover it.

### On `-Wall -Wextra`

These are not optional and they are not decoration. **A submission that does not compile cleanly
under `-Wall -Wextra` loses marks**, stated on every problem set.

The reason is specific to this language: C++ will compile a great deal of code that is wrong, and the
warnings are where the compiler tells you it noticed. In PROG 101 an ignored warning cost you a
segfault. In C++ it costs you a silent copy of a 10-megabyte vector, and nothing crashes at all.

---

## Textbooks

**Primary:**

- **Lippman, Lajoie & Moo — *C++ Primer*, 5th ed. (Addison-Wesley, 2012).** The course's main text.
  Approachable and thorough. **Note it predates C++17**; where it and the lectures disagree on modern
  practice, the lectures win.
- **Stroustrup, B. — *The C++ Programming Language*, 4th ed. (Addison-Wesley, 2013).** Written by the
  creator of the language. Comprehensive, and the definitive reference — **but it is a reference, not
  a tutorial.** Look things up in it; do not try to read it front to back in your first semester.

**Essential once you can write C++ at all:**

- **Meyers, S. — *Effective Modern C++* (O'Reilly, 2014).** 42 specific ways to improve your code.
  Start reading it around Week 5, when you have enough context for the items to land. Items 18–22
  (smart pointers) and 23–30 (move semantics) map directly onto Weeks 5 and 11.
- **Gamma, Helm, Johnson & Vlissides — *Design Patterns* (Addison-Wesley, 1994).** "The Gang of Four".
  The canonical patterns reference and the source for Weeks 7 and 8. **It is 30 years old and its
  C++ is dated** — read it for the structure of the ideas, not the code samples.

**How to use four books:** you are not expected to read all of them. *C++ Primer* is the one to work
through. The other three are for looking things up, and each becomes useful at a different point in
the semester — the schedule above tells you when.

**Also keep open:** [cppreference.com](https://en.cppreference.com). It is more accurate and far more
current than any book, including these. Learning to read its notation is a genuine course objective.

---

## Grading Scale

This course uses the **university-wide 13-band scale** defined in [[UNIVERSITY POLICIES]] (Academic
Registry) — A+ 97–100, A 93–96, A− 90–92, B+ 87–89, B 83–86, B− 80–82, C+ 77–79, C 73–76, C− 70–72,
D+ 67–69, D 63–66, D− 60–62, F below 60. The registry copy governs if the two ever differ.

---

## Course Policies

- **Late policy:** 20% deduction per day; no submissions accepted after 3 days late. Projects have a
  separate, stricter policy stated on each project specification.
- **Code must compile.** A submission that does not compile with the development build line scores
  zero on the affected part. This is harsher than it sounds only if you leave submission to the last
  hour. **Submit something that compiles early, then improve it.**
- **Collaboration:** discussing designs is encouraged. **Writing code together is not.** The line: you
  may leave a conversation with an idea in your head; you may not leave it with text on your screen.
  Name your collaborators on every submission — this costs you nothing and its absence is what turns
  a discussion into misconduct.
- **Generative tools:** permitted for explaining concepts and for debugging code you wrote. Not
  permitted for producing solutions. **State any use on the submission.** The reason is narrow and
  practical: Weeks 5, 10 and 12 assess whether you can write correct C++ under exam conditions, and a
  term of outsourced problem sets produces a predictable result there.
- **Library use:** the STL is encouraged everywhere *except* the week you are implementing the thing.
  You may not use `std::list` in Week 6, whose entire point is to build one. Each assignment states
  its own restrictions explicitly.
- **Exams:** closed book, closed device. The handwritten-sheet allowance is generous — build it as you
  go rather than the night before, since making it is most of the revision.

---

## Accessibility and Support

Anything you need in order to participate — extended time, a distraction-reduced room, materials in
advance, an alternative lab arrangement — is arranged by emailing the instructor, **without requiring
you to disclose a reason.**

Office hours are posted on the course portal. **Come with a specific question, the code, and the exact
compiler error**; that turns a 40-minute session into a 5-minute one. For C++ specifically: paste the
*first* error, not the last. A template error message is 200 lines long and only the first three
matter, which is itself a skill this course will teach you.

---

## What You Should Be Able to Do by Week 12

1. Write a class with correct construction, copy, move and destruction semantics, and **say which of
   the five special members the compiler generated for you and what each one does**.
2. Explain why the Rule of Three exists by describing the double-free it prevents.
3. Write a class template with an iterator that works with STL algorithms.
4. Choose an STL container from the operations you need and their complexity, and defend the choice.
5. Explain virtual dispatch at the level of the vtable, and **state what it costs**.
6. Use `unique_ptr`, `shared_ptr` and `weak_ptr` correctly, and say which one a given ownership
   situation calls for.
7. Implement a templated linked list and BST with iterators, from nothing.
8. Recognise where a design pattern applies — **and where reaching for one makes the code worse**.
9. State the three exception-safety guarantees and write a container operation offering the strong one.
10. Find a data race with ThreadSanitizer and fix it with the cheapest correct synchronisation.
11. Write modern C++: lambdas, `std::function`, structured bindings, `constexpr`.
12. Take a measurement of your own code, explain what the memory hierarchy did, and **decide whether
    the abstraction was worth its cost** — which is the whole course in one sentence.

---

*PROG 102 · Course Syllabus · © CSE Department*
