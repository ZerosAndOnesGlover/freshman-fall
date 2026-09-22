# PROG 102 · Quiz 8
## Week 8 · Tuesday, start of lecture · 15 minutes · 20 points

**Date:** Tuesday 16 March 2027 · 10:00–10:15 (start of L25) · Week 8

**Covers Week 7** — Lectures 22–24: what patterns are, creational patterns, structural patterns.

**Closed book. No devices.** Answer on this sheet.

Name: ________________________  Section: ______  Date: ____________

---

**Q1.** *(3)* State the Gang of Four's two design principles.

**(a)** *(2)* Both, in their standard wording.

**(b)** *(1)* Which one does the Decorator pattern rely on?

<br><br><br>

---

**Q2.** *(4)* A data source can be buffered, encrypted or compressed, in any combination.

**(a)** *(2)* How many classes does the **subclassing** approach need for 3 such features? For 10?

**(b)** *(1)* How many does **Decorator** need for 10?

**(c)** *(1)* Measured, a decorator layer costs about **0.58 ns**. Does that change your recommendation?

<br><br><br>

---

**Q3.** *(3)* This is the whole of a thread-safe singleton:

```cpp
static Config& instance() { static Config c; return c; }
```

**(a)** *(1)* What guarantees it is thread-safe?

**(b)** *(1)* What does the compiler emit to implement that?

**(c)** *(1)* Give one reason to avoid Singleton anyway.

<br><br><br>

---

**Q4.** *(3)* A factory contains an `if`-chain on a string, which Week 4 called a design smell.

**Why is it acceptable here?** Your answer must distinguish this case from the one Week 4 objected to.

<br><br><br>

---

**Q5.** *(3)* Name the pattern:

| Description | Pattern |
| --- | --- |
| Makes an existing class fit an interface it was not written for | |
| Lets you treat a tree node and a leaf identically | |
| Provides a simple entry point to a complicated subsystem | |

<br><br>

---

**Q6.** *(2)* A constructor takes six parameters, two of them `bool`.

**Name the pattern that helps, and give one thing it does that default arguments cannot.**

<br><br>

---

**Q7.** *(2)* A colleague adds an abstract interface for a class with exactly one implementation that
has not changed in two years.

**Give the strongest argument *in favour* of their decision.**

<br><br>

---

**Total: 20 points**

*PROG 102 · Week 8 · Quiz 8 · © CSE Department*
