# PROG 102 · Quiz 5
## Week 5 · Monday, start of lecture · 15 minutes · 20 points

**Covers Week 4** — Lectures 13–15: inheritance, virtual functions and the vtable, abstract classes,
virtual destructors, slicing and casting.

**Closed book. No devices.** Answer on this sheet.

> **Midterm 1 is later this week** and covers Weeks 0–4. This quiz is a rehearsal for its Week 4
> content.

Name: ________________________  Section: ______  Date: ____________

---

**Q1.** *(3)* Given `sizeof(Plain)` = 4 for a class with one `int` and no virtual functions:

**(a)** *(1)* What is `sizeof` for the same class with **one** virtual function added?

**(b)** *(1)* With **ten** virtual functions?

**(c)** *(1)* Explain (b) in one sentence.

<br><br><br>

---

**Q2.** *(3)* This prints `9.0` then `0.0` for the same object:

```cpp
SqNV a(3.0); ShapeNV* p = &a;
std::printf("%.1f %.1f", a.area(), p->area());
```

**(a)** *(2)* Why do the two calls disagree?

**(b)** *(1)* What one keyword fixes it?

<br><br><br>

---

**Q3.** *(4)* A base class has a **non-virtual** destructor. A derived object is created with `new` and
deleted through a base pointer.

**(a)** *(2)* Which destructors run, and what is the consequence?

**(b)** *(2)* `-Wall -Wextra` warns about this **only sometimes.** When does it warn, and when is it
silent?

<br><br><br>

---

**Q4.** *(3)* `void by_value(Shape s)` called with a `Square` reports `area = 0.00`, while
`void by_ref(const Shape& s)` reports `9.00`.

**(a)** *(1)* Name the phenomenon.

**(b)** *(2)* Explain it **in terms of the vptr**.

<br><br><br>

---

**Q5.** *(3)* `Der` declares `void f(double)`. Its base declares `void f(int)`. Calling `d.f(1)` with an
**integer** argument runs `Der::f(double)`.

**(a)** *(2)* Why?

**(b)** *(1)* What one line in `Der` fixes it?

<br><br><br>

---

**Q6.** *(2)* A `dynamic_cast<D1*>` on a pointer to a `D2` returns `nullptr`. A `static_cast<D1*>` on
the same pointer compiles and returns a non-null pointer.

**In one sentence, what is the difference?**

<br><br>

---

**Q7.** *(2)* Measured: a virtual call took about **2 nanoseconds** more than a non-virtual one, a
ratio of about 2×.

**Is virtual dispatch expensive? Answer in one sentence, using the absolute number.**

<br><br>

---

**Total: 20 points**

*PROG 102 · Week 5 · Quiz 5 · © CSE Department*
