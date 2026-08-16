# PROG 102 · Quiz 3
## Week 3 · Tuesday, start of lecture · 15 minutes · 20 points

**Covers Week 2** — Lectures 07–09: function and class templates, deduction, instantiation,
specialization, and what templates cost.

**Closed book. No devices.** Answer on this sheet.

Name: ________________________  Section: ______  Date: ____________

---

**Q1.** *(3)* One template definition:

```cpp
template <typename T> T maxof(T a, T b) { return a > b ? a : b; }
```

instantiated for `int`, `double` and `long`.

**(a)** *(1)* How many symbols appear in the object file?

**(b)** *(1)* In `_Z5maxofIiET_S0_S0_`, which part encodes the template argument?

**(c)** *(1)* The symbols are marked `W`, not `T`. **What does that mean, and which Week 0 feature
uses the same mechanism?**

<br><br><br>

---

**Q2.** *(3)* A class template's declarations are in `stack.hpp` and its definitions in `stack.cpp`.
A program using `Stack<int>` fails to link.

**(a)** *(1)* What does `nm stack.o` show?

**(b)** *(2)* Explain the failure in terms of what each translation unit had.

<br><br><br>

---

**Q3.** *(3)* `maxof(3, 7.5)` does not compile, but `maxof(3, 7.5f + 0.0)` would, and
`maxof<double>(3, 7.5)` does.

**(a)** *(2)* Why does the first fail? Use the word *deduction*.

**(b)** *(1)* Why does supplying `<double>` fix it?

<br><br><br>

---

**Q4.** *(3)* Given:

```cpp
template <typename T> struct Traits          { /* generic */ };
template <>           struct Traits<int>     { /* full    */ };
template <typename T> struct Traits<T*>      { /* partial */ };
```

State which version is selected for each:

| Type | Version |
| --- | --- |
| `Traits<double>` | |
| `Traits<int>` | |
| `Traits<int*>` | |
| `Traits<int**>` | |

<br><br>

---

**Q5.** *(4)* Instantiating `Stack<T>` for 100 distinct types produced 43,993 bytes of machine code.
Writing 100 equivalent classes by hand produced **the same 43,993 bytes**, and compiled slower.

**(a)** *(2)* What does this show about the cause of "template code bloat"?

**(b)** *(2)* A colleague concludes "so we should stop using templates". Give the **correct**
engineering response in one sentence.

<br><br><br>

---

**Q6.** *(2)* `sizeof(FixedArray<int,8>)` is 32 on a machine where `sizeof(int)` is 4.

**Where is the value 8 stored in the object?**

<br><br>

---

**Q7.** *(2)* Measured error lengths: a plain type error was **6 lines**, a direct template error was
**5 lines**, and the same mistake through `std::sort` was **78 lines**.

**What makes the third one long?** *(The answer is not "templates".)*

<br><br>

---

**Total: 20 points**

*PROG 102 · Week 3 · Quiz 3 · © CSE Department*
