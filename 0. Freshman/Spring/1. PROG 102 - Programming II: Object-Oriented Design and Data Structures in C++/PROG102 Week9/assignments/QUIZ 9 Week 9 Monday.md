# PROG 102 · Quiz 9
## Week 9 · Monday, start of lecture · 15 minutes · 20 points

**Covers Week 8** — Lectures 25–27: Observer, Strategy, Command, Template Method, State, and what
C++11 obsoleted.

**Closed book. No devices.** Answer on this sheet.

Name: ________________________  Section: ______  Date: ____________

---

**Q1.** *(3)* A subject holds `std::vector<Observer*>`. One observer goes out of scope, then the
subject notifies.

**(a)** *(1)* What does AddressSanitizer report?

**(b)** *(2)* The `weak_ptr` version fixes it **without** the observer knowing about the subject. Why
does that matter?

<br><br><br>

---

**Q2.** *(4)* Four ways to give `std::sort` a comparison, on 2,000,000 ints:

| | ms |
| --- | --- |
| virtual Strategy | 166 |
| `std::function` | 296 |
| lambda | 160 |
| default `operator<` | 150 |

**(a)** *(2)* Which is slowest, and by what factor against the lambda?

**(b)** *(2)* Explain the mechanism, and name the **Week 3** result that has the same cause.

<br><br><br>

---

**Q3.** *(3)* Command 1994-style needed 20 lines and 4 types; the lambda version needed 8 lines and 2
types.

**Give one concrete case where the 1994 version is still better.**

<br><br><br>

---

**Q4.** *(3)* State the **Open/Closed Principle**, and name the pattern from Week 8 that most clearly
embodies it.

<br><br><br>

---

**Q5.** *(3)* **State** and **Strategy** have identical structure.

**(a)** *(2)* What distinguishes them?

**(b)** *(1)* Name one cost of the State pattern that a `switch` does not have.

<br><br><br>

---

**Q6.** *(2)* Lecture 27 claims: *a design pattern is a workaround for something the language cannot
say.*

**Name one pattern from Weeks 7–8 that this claim does *not* explain**, and say why in one sentence.

<br><br>

---

**Q7.** *(2)* An observer throws from `notify()`, halfway through the subject's list.

**Describe the subject's state afterwards in one sentence.** *(You are not expected to know the
technical term yet — today's lecture supplies it.)*

<br><br>

---

**Total: 20 points**

*PROG 102 · Week 9 · Quiz 9 · © CSE Department*
