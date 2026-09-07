# PROG 102 · Programming II — Object-Oriented Design and Data Structures in C++
## Week 1: Operator Overloading and Copy Semantics

**Credits:** 4 (3 lecture + 1 lab) · **Prerequisites:** PROG 101 (C), CS 101
**Assessment for this course (overall):** Labs 20%, Problem Sets 30%, Midterms 25%, Final 15%, Projects 10%
**This week's deliverables:** PS 1, Lab 1, Quiz 1 (Monday, covers Week 0)

---

### Why This Week Exists

Because Week 0 left you holding a class that is correct, complete, and one line away from destroying
itself:

```cpp
CharBuffer a(8);
CharBuffer b = a;      // both objects now hold the same pointer
```

If you did PS 0 Part E, you watched AddressSanitizer report `attempting double-free` on your own code.
**This week explains where that copy constructor came from and what to do about it.**

The answer has two halves. The **Rule of Three** says which functions come as a set. The **copy-swap
idiom** is the way to write them that is short, self-assignment-safe and exception-safe — and it gets
the last of those for free, which is why Week 9 will still be using it.

The other half of the week is **operator overloading**, which is what makes `a + b` and
`std::cout << v` work for your own types. It is easy, and the interesting question is not how but
**when** — the failure mode is a codebase where `+` means something nobody can guess.

### Learning Objectives

By the end of Week 1, you should be able to:

1. Overload the arithmetic, comparison, stream, subscript and call operators, and say which must be
   member functions and which must not.
2. Explain why `operator<<` cannot be a member of your class, and demonstrate what happens if you try.
3. Provide the `const`/non-`const` `operator[]` pair and say which is selected when.
4. State the **Rule of Three** and describe the double-free it prevents.
5. Distinguish shallow from deep copy in terms of what the compiler's generated copy constructor does.
6. Write a copy assignment operator that survives **self-assignment**, and explain precisely how the
   naive version fails — which is *not* a use-after-free.
7. Implement the **copy-swap idiom** and explain why it needs no self-assignment guard.
8. **Count the copies** your code performs, and explain C++17's guaranteed copy elision from measured
   data.
9. Say why `const T&` is the default way to pass a parameter, from a measurement rather than a rule.

### This Week's Materials

| File | Purpose |
| --- | --- |
| [[L04 Operator Overloading]] | Syntax, member vs free, symmetry, `<<`, `[]`, `()`, and when not to |
| [[L05 Copy Semantics and the Rule of Three]] | Shallow vs deep, the generated copy constructor, self-assignment traced |
| [[L06 The Copy-Swap Idiom]] | Copy-swap, copy elision measured, and a first look at moves |
| [[PS 1 A Vector3D Class]] | Due Friday of Week 2 |
| [[PROG102 Week1/assignments/QUIZ 1 Week 1 Monday\|QUIZ 1 Week 1 Monday]] | 15 minutes, start of Monday's lecture |
| [[LAB 1 Debugging Copy Semantics]] | Instrument a class and count every copy it makes |
| [[PROG102 Week1/resources/Reading Guide Week 1\|Reading Guide Week 1]] | *C++ Primer* Ch. 13–14, and the commands to reproduce every measurement |
| [[PROG102 Week1/solutions_instructor/PS 1 Solutions\|PS 1 Solutions]] | Instructor only |
| [[PROG102 Week1/solutions_instructor/LAB 1 Solutions\|LAB 1 Solutions]] | Instructor only |

### The One Thing to Take From This Week

**The compiler writes functions for you, and it does not know what your class means.**

The generated copy constructor performs a memberwise copy. For `int` and `double` members that is
exactly right. For a pointer member it copies the *pointer*, which is right if the pointer is an
observer and catastrophic if it is an owner — and the compiler cannot tell the difference, because
`char*` does not say which one it is.

**This is the first time in the course that the default is silently wrong**, and it will not be the
last. Week 4's non-virtual destructor and Week 10's unsynchronised counter are the same shape of
problem: a language default that is correct for the common case and quietly fatal for yours.

### A Warning About Copy Counting

Lab 1 asks you to count copy constructor calls. **You will find fewer than you predict**, and the
reason is not that the compiler is being clever — it is that **C++17 requires** some copies not to
happen at all.

`V3 c = a + b;` performs **zero** copies, and does so even with `-O0 -fno-elide-constructors`, a flag
whose entire purpose is to disable that optimization. In C++17 there is no copy there to elide.
Lecture 06 measures this across five compiler configurations.

Predict before you measure. The gap between the two is the lab.

### Assessment Reminder

**Quiz 1 is Monday, at the start of lecture, and covers Week 0** — classes, `this`, constructors,
destruction order, `const`, `inline`, namespaces. Quizzes carry no weight and are tracked separately;
they exist so that you find out in Week 1 rather than Week 5.

**Labs are 20% of this course.** Lab 1 is graded.

### Connections

**Back:** Week 0's `CharBuffer` is this week's worked example, and PS 0 Part E is Lecture 05's opening
slide. Destruction order from **Lecture 02** is what makes copy-swap work.

**Forward:** the copy-swap idiom is how **Week 6** implements the linked list and BST, and its
exception safety is the subject of **Week 9**. The Rule of Three becomes the Rule of Five once moves
arrive in **Week 5**. `operator[]`, `operator()` and `operator<` are what make your types usable with
the STL in **Week 3** — `std::sort` needs `<`, and `std::map` needs it too.

---

*PROG 102 · Week 1 · © CSE Department*
