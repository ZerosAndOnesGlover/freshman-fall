# PROG 102 · Quiz 10
## Week 10 · Tuesday, start of lecture · 15 minutes · 20 points

**Covers Week 9** — Lectures 28–30: exceptions, stack unwinding, the three guarantees, `noexcept`,
assertions and contracts.

**Closed book. No devices.** Answer on this sheet.

> **Midterm 2 is later this week** and covers Weeks 5–9. This quiz is a rehearsal for its Week 9
> content.

Name: ________________________  Section: ______  Date: ____________

---

**Q1.** *(3)* Stack unwinding runs destructors as it goes.

**(a)** *(1)* In what order relative to construction?

**(b)** *(2)* This code leaks 400 bytes. Why does unwinding not prevent it?

```cpp
try { int* p = new int[100]; throw std::runtime_error("x"); }
catch (const std::exception&) { }
```

<br><br><br>

---

**Q2.** *(4)* Name the four possible states of an object after an operation threw partway through, and
give the promise of each in one line.

<br><br><br><br>

---

**Q3.** *(3)* A container holds 2 elements. An operation appending 4 more throws on the third copy.

**(a)** *(1)* Under the **basic** guarantee, what can you say about `size()` afterwards?

**(b)** *(1)* Under the **strong** guarantee?

**(c)** *(1)* Which one is `std::vector::insert` in the middle, and why?

<br><br><br>

---

**Q4.** *(3)* Write the three-step recipe for upgrading an operation to the strong guarantee.

**Then name the Week 1 idiom that is exactly this recipe.**

<br><br><br>

---

**Q5.** *(3)* A `noexcept` function throws, inside a `try`/`catch (...)`.

**(a)** *(1)* What does the compiler warn?

**(b)** *(2)* What happens at run time, and does the `catch` run?

<br><br><br>

---

**Q6.** *(2)* Measured: identical source with and without exception support gave 1.53–1.66 ns against
1.49–1.60 ns per call, and **240 bytes against 88 bytes** of code.

**Is "C++ exceptions are zero-cost" true? Answer in one sentence.**

<br><br>

---

**Q7.** *(2)* For each, say **assertion** or **exception**:

| Situation | Which |
| --- | --- |
| A config file that will not parse | |
| An index past the end of a private internal buffer | |

<br><br>

---

**Total: 20 points**

*PROG 102 · Week 10 · Quiz 10 · © CSE Department*
