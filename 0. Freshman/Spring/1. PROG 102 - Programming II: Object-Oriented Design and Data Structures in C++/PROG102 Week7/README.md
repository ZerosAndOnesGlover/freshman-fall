# PROG 102 · Programming II — Object-Oriented Design and Data Structures in C++
## Week 7: Design Patterns I — Creational and Structural

**Credits:** 4 (3 lecture + 1 lab) · **Prerequisites:** PROG 101 (C), CS 101
**Assessment for this course (overall):** Labs 20%, Problem Sets 30%, Midterms 25%, Final 15%, Projects 10%
**This week's deliverables:** PS 7, Lab 7, Quiz 7 (Monday, covers Week 6) · **Project 1 due Week 9**

---

### Why This Week Exists

Six weeks of this course have been about **mechanism**: what a virtual call costs, what a template
generates, where the vptr lives. Every question had a measurement that settled it.

**This week is about judgement**, and the change of gear is real. There is no experiment that tells you
whether a Factory Method is the right answer here. What there is instead is a vocabulary — about
twenty named structures that recur in object-oriented code — and the value is that once a thing has a
name, a team can discuss it.

That is the honest case for patterns and it is smaller than the Gang of Four's. **A pattern is not a
solution; it is a name for a shape of solution**, and Lecture 22 §6 is about when reaching for one
makes the code worse.

### The Two Principles

Everything this week reduces to two sentences from the Gang of Four, and they are worth more than the
catalogue:

> **Favour object composition over class inheritance.**
> **Program to interfaces, not implementations.**

You have already been taught both without the labels. **Week 4 §L13 §2** said prefer composition
because inheritance is the tightest coupling C++ offers. **Week 6's** container was built against the
iterator *protocol* rather than any concrete type, which is why `std::accumulate` worked on it.

### Learning Objectives

By the end of Week 7, you should be able to:

1. Say what a design pattern is — and what it is not.
2. Implement **Singleton**, **Factory Method**, **Abstract Factory** and **Builder**, and say what
   problem each solves.
3. Explain why a function-local `static` is a thread-safe singleton, and name the mechanism.
4. Implement **Adapter**, **Decorator**, **Composite** and **Facade**.
5. **Quantify** the combinatorial argument for Decorator, and measure what a decorator layer costs.
6. Recognise a pattern in code you did not write — including in the standard library.
7. Argue *against* a pattern when it does not fit, which is the harder skill.

### This Week's Materials

| File | Purpose |
| --- | --- |
| [[L22 What Patterns Are]] | The idea, the two principles, and when not to |
| [[L23 Creational Patterns]] | Singleton, Factory Method, Abstract Factory, Builder |
| [[L24 Structural Patterns]] | Adapter, Decorator, Composite, Facade |
| [[PS 7 Factory Method and Decorator]] | Due Friday of Week 8 |
| [[PROG102 Week7/assignments/QUIZ 7 Week 7 Monday\|QUIZ 7 Week 7 Monday]] | 15 minutes, covers Week 6 |
| [[LAB 7 Refactoring a Messy Hierarchy]] | Take a class explosion apart with patterns |
| [[PROG102 Week7/resources/Reading Guide Week 7\|Reading Guide Week 7]] | Gang of Four, and every command to reproduce this week |
| [[PROG102 Week7/solutions_instructor/PS 7 Solutions\|PS 7 Solutions]] | Instructor only |
| [[PROG102 Week7/solutions_instructor/LAB 7 Solutions\|LAB 7 Solutions]] | Instructor only |

### The One Thing to Take From This Week

**Patterns are descriptions, not prescriptions.**

The Gang of Four did not invent these structures. They went looking through code that worked, found
the same shapes recurring, and wrote them down. **That is why the Iterator you built in Week 6 turns
out to be one of them** — you did not apply a pattern, you solved a problem, and the solution had a
name already.

The failure mode is the reverse: starting from the catalogue and looking for somewhere to put a
Factory. Lab 7 gives you a hierarchy mangled by exactly that instinct.

### The Measurement That Justifies Decorator

Suppose a data source can be buffered, encrypted, compressed — **n independent, combinable features.**

| features | subclasses needed | decorators needed |
| --- | --- | --- |
| 3 | 8 | 3 |
| 5 | 32 | 5 |
| **10** | **1024** | **10** |

$2^n$ against $n$. Subclassing requires a class for every *combination*
(`BufferedEncryptedFileSource`); decorating requires one per *feature*, composed at run time.

**And it costs about 0.6 ns per layer** — measured in Lecture 24 §3.3, on chains up to eight deep. That
is the whole trade, and it is unusually favourable.

### Assessment Reminder

**Quiz 7 is Monday and covers Week 6** — the list, the iterator protocol, the BST, and the recursive
destructor.

**Project 1 is due Week 9.** You should have Parts 1 and 2 substantially working by the end of this
week. Week 8 is patterns again and Week 9 is exception safety, so **the time you have for Project 1 is
now.**

### Connections

**Back:** **Week 4**'s abstract base classes are what every pattern here is built from. **Week 5**'s
`unique_ptr` is how a Decorator owns what it wraps. **Week 6**'s Iterator is a pattern you have
already implemented.

**Forward:** **Week 8** is behavioural patterns — Observer, Strategy, Command, State. **Week 9**'s
exception-safety work uses RAII, which the Gang of Four would have called a pattern if C++ had had
destructors when they wrote. **Week 11**'s lambdas make Strategy nearly free.

---

*PROG 102 · Week 7 · © CSE Department*
