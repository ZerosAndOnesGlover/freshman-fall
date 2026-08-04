# PROG 102 · Quiz 6
## Week 6 · Monday, start of lecture · 15 minutes · 20 points

**Covers Week 5** — Lectures 16–18: RAII, `unique_ptr`, `shared_ptr`, `weak_ptr`, move semantics.

**Closed book. No devices.** Answer on this sheet.

Name: ________________________  Section: ______  Date: ____________

---

**Q1.** *(3)* Give `sizeof` for each, on a 64-bit machine:

| Type | `sizeof` |
| --- | --- |
| `int*` | |
| `std::unique_ptr<int>` | |
| `std::shared_ptr<int>` | |

**In one sentence, why is the third larger than the second?**

<br><br>

---

**Q2.** *(3)* A function allocates a `Widget` with `new`, calls a method that throws, and never reaches
its `delete`.

**(a)** *(1)* What happens to the allocation?

**(b)** *(2)* Rewrite the ownership so this cannot happen, and say which mechanism saves you.

<br><br><br>

---

**Q3.** *(3)* Counting allocations:

| Expression | allocations |
| --- | --- |
| `std::shared_ptr<W>(new W)` | |
| `std::make_shared<W>()` | |

**(a)** *(2)* Fill in both.

**(b)** *(1)* What accounts for the difference?

<br><br>

---

**Q4.** *(4)* Two `shared_ptr` nodes point at each other. Both go out of scope.

**(a)** *(1)* What is each `use_count()` before the scope ends?

**(b)** *(1)* Do the destructors run?

**(c)** *(2)* Name the fix, and say **which of the two links** should change.

<br><br><br>

---

**Q5.** *(3)* `std::move(x)` is often described as "moving x".

**(a)** *(2)* What does it actually do? Be precise.

**(b)** *(1)* Where does the move itself happen?

<br><br><br>

---

**Q6.** *(2)* A class has a move constructor that is **not** marked `noexcept`. A `std::vector` of that
type grows.

**What does the vector do, and why?**

<br><br>

---

**Q7.** *(2)* State the **Rule of Zero** in one sentence, and give one example of a class where it does
**not** apply.

<br><br>

---

**Total: 20 points**

*PROG 102 · Week 6 · Quiz 6 · © CSE Department*
