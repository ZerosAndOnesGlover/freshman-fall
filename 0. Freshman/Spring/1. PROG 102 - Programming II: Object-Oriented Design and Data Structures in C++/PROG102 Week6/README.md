# PROG 102 · Programming II — Object-Oriented Design and Data Structures in C++
## Week 6: Implementing Data Structures — Linked Lists and Trees

**Credits:** 4 (3 lecture + 1 lab) · **Prerequisites:** PROG 101 (C), CS 101
**Assessment for this course (overall):** Labs 20%, Problem Sets 30%, Midterms 25%, Final 15%, Projects 10%
**This week's deliverables:** PS 6, Lab 6, Quiz 6 (Monday, covers Week 5) · **Project 1 assigned**

---

### Why This Week Exists

Week 5 ended on the **Rule of Zero**: write none of the five special members, let `std::string`,
`std::vector` and `unique_ptr` do it.

**This week is the exception, and it is the only kind of exception there is.** You are about to write
a container — a class whose entire job is to own and manage a resource that no library type owns for
you. There is nothing to delegate to. **You are the library type now.**

That is why the ordering matters: the Rule of Zero applies to code that *uses* resources. Week 6 is
code that *provides* them, and it is where every technique from Weeks 0–5 gets used at once.

### The Real Point

You are not building a linked list because the world needs another linked list. `std::list` exists and
is better tested than anything you will write this week.

**You are building it because implementing forces you to answer questions using it never asks.** Why
does `std::list` keep a sentinel node? Why does its iterator have `++` but not `+`? Why does inserting
into a `vector` invalidate iterators and inserting into a `list` not?

By Friday you will have answered all three by having had to make the decision yourself.

### Learning Objectives

By the end of Week 6, you should be able to:

1. Implement a templated doubly linked list with a **sentinel node**, and say what the sentinel
   removes.
2. Write the **Rule of Five** for a node-owning container, and say why the Rule of Zero does not apply.
3. Implement `iterator` and `const_iterator` satisfying the **`iterator_traits`** protocol.
4. Explain why your iterator provides `++` but not `+`, and demonstrate that `std::sort` correctly
   refuses it.
5. Get STL algorithms working on your own container — the week's payoff.
6. Implement a templated BST with `unique_ptr` children and a configurable comparator.
7. **Explain and fix the recursive-destructor stack overflow** that node-owning `unique_ptr` chains
   cause.
8. State each container's iterator-invalidation rules and justify them from the implementation.
9. Benchmark your container against the STL equivalent and interpret the difference honestly.

### This Week's Materials

| File | Purpose |
| --- | --- |
| [[L19 Implementing a Doubly Linked List]] | Sentinel, Rule of Five, insert and erase |
| [[L20 Implementing Iterators]] | `iterator_traits`, `const_iterator`, and the category contract |
| [[L21 Implementing a Binary Search Tree]] | `unique_ptr` children, the destructor trap, and the STL comparison |
| [[PS 6 A Templated Doubly Linked List]] | Due Friday of Week 7 |
| [[PROG102 Week6/assignments/QUIZ 6 Week 6 Monday\|QUIZ 6 Week 6 Monday]] | 15 minutes, covers Week 5 |
| [[PROJECT 1 A Container Library]] | **Assigned this week, due Week 9** |
| [[LAB 6 Benchmarking Against std list]] | Measure your list against `std::list` |
| [[PROG102 Week6/resources/Reading Guide Week 6\|Reading Guide Week 6]] | *C++ Primer* §9.2, Ch. 16 revisited, and every command |
| [[PROG102 Week6/solutions_instructor/PS 6 Solutions\|PS 6 Solutions]] | Instructor only |
| [[PROG102 Week6/solutions_instructor/LAB 6 Solutions\|LAB 6 Solutions]] | Instructor only |

### The One Thing to Take From This Week

**An honest interface refuses what it cannot do efficiently.**

Your list's iterator will provide `operator++` and not `operator+`. That is not laziness — a list
*could* offer `+` by looping. It does not, because `it + 500` would look like $O(1)$ and cost $O(n)$,
and the caller would have no way to tell.

The proof that you got it right is that **`std::sort` refuses your iterator**, with the same error it
gives for `std::list`:

```
error: no match for 'operator-' (operand types are 'List<int>::Iter<false>' and ...)
```

**A container that compiles with every algorithm has lied about one of them.**

### The Trap Worth Previewing

Nodes owned by `unique_ptr` are the obvious modern design, and they contain a landmine:

```cpp
struct Node { int v; std::unique_ptr<Node> next; };
```

Destroying the head calls `~Node`, which destroys `next`, which calls `~Node`… **The destructor is
recursive, and it runs on the stack.**

Measured with an 8 MB stack: **500,000 nodes destroy fine; 1,000,000 segfault.** Lecture 21 §4 shows the
fix — an iterative unlink in the destructor — which handles 5,000,000 without trouble.

This is the first bug this course has shown you that **only appears at scale**, and it is why Project 1
requires a test at a million elements.

### Project 1

**Assigned this week, due Week 9.** A container library: your list, your BST, a shared iterator
protocol, and a test suite. Worth 5% directly — and Lecture 18's Rule of Zero versus this week's Rule
of Five is precisely what it examines.

Read the specification this week even though it is due in three. It tells you which decisions are
yours and which are fixed.

### Connections

**Back:** everything. Templates (**W2**), iterator categories (**W3**), the Rule of Five and
`unique_ptr` (**W5**), copy-and-swap (**W1**), `const`-correctness (**W0**). This is the first week
that uses all of it at once, which is why it is placed here.

**Forward:** **Weeks 7–8** are design patterns, and the **Iterator pattern** you implement here is one
of them. **Week 9** makes your container exception-safe. **Week 12** returns to Lab 6's numbers and
explains the traversal gap with cache lines.

---

*PROG 102 · Week 6 · © CSE Department*
