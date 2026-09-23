# PROG 102 · Programming II — Object-Oriented Design and Data Structures in C++
## Week 4: Inheritance and Polymorphism

**Credits:** 4 (3 lecture + 1 lab) · **Prerequisites:** PROG 101 (C), CS 101
**Assessment for this course (overall):** Labs 20%, Problem Sets 30%, Midterms 25%, Final 15%, Projects 10%
**This week's deliverables:** PS 4 (released Fri 19 Feb 10:00, due **Fri 26 Feb 17:00**), Lab 4 (**Mon 22 Feb**, 15:00), Quiz 4 (**Tue 16 Feb**, 10:00, covers Week 3) · MIDTERM 1 announced (sat Tue 2 Mar)

---

### Why This Week Exists

Weeks 2 and 3 gave you polymorphism that costs nothing: a template resolves at compile time and
`maxof<int>` is byte-identical to a hand-written function.

**This week gives you the other kind.** A virtual function is chosen at **run time**, from the object
itself, and that buys you something templates cannot: a `std::vector<Shape*>` holding squares and
circles you did not know about when you compiled the loop.

It costs one pointer indirection. **That is measured here, and the measurement is more interesting
than the textbook number**, because the compiler turns out to be considerably cleverer than the model
you are about to be taught.

The other half of the week is the **rules you cannot get wrong**: virtual destructors, slicing, and
what `protected` actually means. The first of those silently leaks memory and your build line will not
always warn you.

### Learning Objectives

By the end of Week 4, you should be able to:

1. Distinguish **is-a** from **has-a**, and choose inheritance or composition accordingly.
2. Explain what `public`, `protected` and `private` inheritance do, and why you will almost always
   want the first.
3. Describe the vtable mechanism precisely: what is stored in the object, what is stored per class.
4. **Read a vtable in GDB** and say which slot corresponds to which function.
5. State what a virtual call costs, from your own measurement, and explain why the naive benchmark is
   wrong.
6. Write an abstract base class with pure virtual functions, and say why it cannot be instantiated.
7. State the **virtual destructor rule**, demonstrate the leak it prevents, and say exactly when your
   compiler warns and when it does not.
8. Recognise **object slicing** and give two ways to avoid it.
9. Use `override` and `final`, and explain what each catches.
10. Use `dynamic_cast` correctly, know what it costs, and know why needing it is usually a design smell.

### This Week's Materials

| File | Purpose |
| --- | --- |
| [[L13 Inheritance]] | Base and derived, is-a vs has-a, access specifiers, `override` |
| [[L14 Virtual Functions and the vtable]] | The mechanism, the cost measured, and speculative devirtualization |
| [[L15 Abstract Classes Destructors and Casting]] | Pure virtual, the destructor rule, slicing, `dynamic_cast` |
| [[PS 4 A Shape Hierarchy]] | Due Fri 26 Feb 17:00 |
| [[PROG102 Week4/assignments/QUIZ 4 Week 4 Tuesday\|QUIZ 4 Week 4 Tuesday]] | 15 minutes, covers Week 3 |
| [[LAB 4 Reading the vtable in GDB]] | Find the vptr, walk the vtable, watch it change |
| [[PROG102 Week4/resources/MIDTERM 1 Revision Guide\|MIDTERM 1 Revision Guide]] | **Weeks 0–4, sat Tue 2 Mar (Week 6).** Start now |
| [[PROG102 Week4/resources/Reading Guide Week 4\|Reading Guide Week 4]] | *C++ Primer* Ch. 15, and every command to reproduce this week |
| [[PROG102 Week4/solutions_instructor/PS 4 Solutions\|PS 4 Solutions]] | Instructor only |
| [[PROG102 Week4/solutions_instructor/LAB 4 Solutions\|LAB 4 Solutions]] | Instructor only |

### The One Thing to Take From This Week

**A virtual call asks the object which function to run.**

Everything follows from that. The object must therefore *carry* the answer — that is the vptr, and it
is why `sizeof` grows by 8 the moment a class gains its first virtual function. Ten virtual functions
cost the same as one, because it is one pointer either way.

It is also why slicing destroys polymorphism (copying into a base-typed variable copies the base's
vptr), and why a non-virtual destructor leaks (the delete asks the *static* type, which does not know
about the derived part).

### The Measurement, and a Warning About It

The textbook claim is "one extra indirection, negligible". Lecture 14 measures it, and getting an
honest number took **three attempts**:

1. First version compared `vector<unique_ptr<Shape>>` against `vector<PlainSq>` — measuring dispatch
   *and* pointer-chasing *and* separate allocations.
2. Second used contiguous storage for both — but the virtual objects were 16 bytes against 8, so the
   loop touched twice the memory.
3. Third padded both types to 16 bytes. **Ratio ≈ 1.9×, about 2.1 ns per call.**

**Each fix changed the answer**, and the first version overstated the cost substantially. This is Lab
2's lesson arriving from the other side: not a wrong explanation for a right number, but **a number
that answered a different question than the one asked.**

Then the assembly turned out to show something no textbook mentions, which Lecture 14 §5 covers.

### Midterm 1

**Announced this week, sat Tuesday 2 March 2027, 18:00–19:30 (Week 6).** A 75-minute paper, covers **Weeks 0–4**, one handwritten sheet
(one side). The revision guide is in `resources/` and is worth reading *this* week, not next — it
lists what is examinable and what is not, and points at the specific measurements you are expected to
be able to explain.

### Connections

**Back:** the `this` pointer from **L01** is what a virtual call dereferences to find the vptr.
**Week 1's** Rule of Three becomes the Rule of Three *plus a virtual destructor*. **Week 3's**
`qsort`-versus-`std::sort` result was about function pointers being uninlinable — a virtual call *is*
a function pointer, and the same argument applies.

**Forward:** **Weeks 7 and 8** are design patterns, nearly all of which are built on abstract base
classes. **Week 9**'s exception hierarchy is an inheritance hierarchy. **Week 12** returns to this
week's benchmark and explains the remaining gap with cache behaviour.

---

*PROG 102 · Week 4 · © CSE Department*
