# PROG 102 · Programming II — Object-Oriented Design and Data Structures in C++
## Week 5: Memory Management and RAII

**Credits:** 4 (3 lecture + 1 lab) · **Prerequisites:** PROG 101 (C), CS 101
**Assessment for this course (overall):** Labs 20%, Problem Sets 30%, Midterms 25%, Final 15%, Projects 10%
**This week's deliverables:** PS 5 (released Fri 26 Feb 10:00, due **Fri 5 Mar 17:00**), Lab 5 (**Mon 1 Mar**, 15:00), Quiz 5 (**Tue 23 Feb**, 10:00, covers Week 4) · MIDTERM 1 next Tuesday (2 Mar, 18:00, Weeks 0–4)

---

### Why This Week Exists

Every memory bug in this course so far has had the same shape.

Week 0's `IntStack` leaked if you forgot `stack_free`. Week 1's `CharBuffer` double-freed when copied.
Lab 1's `Roster` did both, three different ways. Week 4's hierarchy leaked when a destructor was not
`virtual`. In each case the language had no way to *say* that a pointer owned what it pointed at, so
the compiler could not check it and the sanitizer had to find it at run time.

**This week C++ gets that vocabulary.** `unique_ptr` means "I own this, exclusively". `shared_ptr`
means "several of us own this". `weak_ptr` means "I can see it and I do not own it". Ownership stops
being a comment and becomes a **type**.

And the payoff is not just tidiness. **The raw version leaks when an exception is thrown, and the
smart-pointer version does not** — verified this week, and it is the thing you cannot get right by
being careful.

### Learning Objectives

By the end of Week 5, you should be able to:

1. State what RAII is in one sentence, and identify the destructor as the mechanism.
2. Use `unique_ptr` and `make_unique`, and explain why `unique_ptr` cannot be copied.
3. Demonstrate that `unique_ptr` costs nothing — and say precisely what "nothing" was measured against.
4. Use `shared_ptr` and `make_shared`, and say what the control block is and what it costs.
5. Explain the **reference cycle** leak, demonstrate it, and fix it with `weak_ptr`.
6. Choose between `unique_ptr`, `shared_ptr`, a reference and a raw pointer for a given situation.
7. Explain rvalue references and what `std::move` actually does — **which is not moving anything**.
8. Write the Rule of Five, and explain why the **Rule of Zero** is better.
9. Pass smart pointers to functions correctly, and say why `const unique_ptr<T>&` is the wrong
   parameter type.

### This Week's Materials

| File | Purpose |
| --- | --- |
| [[L16 RAII and unique_ptr]] | The idiom, exclusive ownership, and what it costs |
| [[L17 shared_ptr weak_ptr and the Cost of Sharing]] | Reference counting, the cycle leak, and the atomic |
| [[L18 Move Semantics]] | Rvalue references, `std::move`, Rule of Five, Rule of Zero |
| [[PS 5 From Raw Pointers to Smart Pointers]] | Due Fri 5 Mar 17:00 |
| [[PROG102 Week5/assignments/QUIZ 5 Week 5 Tuesday\|QUIZ 5 Week 5 Tuesday]] | 15 minutes, covers Week 4 |
| [[LAB 5 Leak Detection with AddressSanitizer]] | Find five leaks, fix them with ownership types |
| [[PROG102 Week5/resources/Reading Guide Week 5\|Reading Guide Week 5]] | *C++ Primer* Ch. 12–13, Meyers Items 18–22, and every command |
| [[PROG102 Week5/solutions_instructor/PS 5 Solutions\|PS 5 Solutions]] | Instructor only |
| [[PROG102 Week5/solutions_instructor/LAB 5 Solutions\|LAB 5 Solutions]] | Instructor only |

### The One Thing to Take From This Week

**`unique_ptr` is not a safer pointer. It is a pointer that says who owns the thing.**

The safety follows from that, and so does everything else: it cannot be copied because ownership is
exclusive; it can be moved because ownership can be transferred; and passing one to a function *by
value* is how you spell "I am giving this to you" in a way the compiler checks.

That is why the guidance in Lecture 16 §7 is about **signatures**, not about safety. Your function's
parameter types should say what happens to the ownership, and then the reader does not have to guess
and the compiler does not have to trust you.

### The Measurement Worth Previewing

`unique_ptr` is described everywhere as "zero-overhead". Lecture 16 §5 checks it, and the honest
answer has three parts:

- **Same size as a raw pointer** — 8 bytes. Verified.
- **Identical generated code** when you pass the *pointee* rather than the smart pointer. Byte for
  byte.
- **Different generated code** in the ownership case — and the difference is **exception-handling
  landing pads**, which is not overhead. It is the extra thing `unique_ptr` does, and the raw version
  **leaks** when an exception is thrown. Verified with a leak counter: raw `allocs=2 frees=1`,
  `unique_ptr` balanced.

So `unique_ptr` is not free. **It is cheaper than free**, because the code it replaces was wrong.

### Midterm 1 Is Next Tuesday

**Tuesday 2 March 2027, 18:00–19:30 — a 75-minute paper covering Weeks 0–4**, one handwritten sheet, one
side. The revision guide is in **Week 4's** `resources/`. This week's material is **not** examinable on it.

Plan accordingly: PS 5 is due Friday 5 March and Lab 5 is Monday 1 March, the day before the paper.

### Connections

**Back:** RAII was named in **Lecture 02 §5** and has been the answer since. The Rule of Three from
**Week 1** becomes the Rule of Five here — and then the **Rule of Zero**, which retires it. **Week 4's**
PS 4 held its shapes as `std::vector<Shape*>` and deleted them by hand; this week replaces that with
`std::vector<std::unique_ptr<Shape>>`.

**Forward:** **Week 6** builds a linked list and BST whose nodes are owned by `unique_ptr`. **Week 9**'s
exception safety is RAII's real justification. **Week 10** is where the `shared_ptr` atomic stops being
a footnote, because that is the week you actually have threads.

---

*PROG 102 · Week 5 · © CSE Department*
