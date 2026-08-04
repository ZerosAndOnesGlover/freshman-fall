# PROG 102 · Lab 7
## Refactoring a Messy Hierarchy

**Week 7 · 2-hour lab session · 40 points**
**Deliverable:** `notify_fixed.hpp`, `RESULTS.md`. In-lab checkoff.

---

## Purpose

You are given `notify.hpp`. **It compiles without a warning, it works, and every one of its outputs is
correct.**

It is also what happens when someone expresses *combination* using *inheritance*. Your job is to take
it apart and put it back together with the patterns from this week — and then to say honestly how much
that was worth, which is not the same as saying it was worth a lot.

> **This lab has no measurement.** It is the first one that does not, and that is deliberate: the
> question "is this design better?" has no benchmark. It has an argument, and Part D is where you make
> one.

---

## The Code

A notification can be **timestamped**, **encrypted** and **compressed**, in any combination, over any
of several **transports**. The provided version has a class per combination:

```cpp
class Notifier;
class TimestampedNotifier;
class EncryptedNotifier;
class CompressedNotifier;
class TimestampedEncryptedNotifier;
class TimestampedCompressedNotifier;
class EncryptedCompressedNotifier;
class TimestampedEncryptedCompressedNotifier;
class EmailNotifier;
class SmsNotifier;

Notifier* make(const std::string& cfg);      // returns a raw owning pointer
```

Confirm it builds and runs before changing anything:

```
g++ -std=c++17 -Wall -Wextra -pedantic -g -fsanitize=address,undefined notify_demo.cpp -o nd && ./nd
```

---

## Part A — Diagnose (12 pts)

**A1.** *(4)* Count the classes. Then compute, **for the current design**, how many classes are needed
for:

- 3 features (today);
- 4 features;
- 5 features;
- 4 features × 3 transports.

Show the arithmetic.

**A2.** *(4)* Name **three distinct problems** with the provided code. At least one must be about
ownership rather than about class count.

**A3.** *(4)* The `make()` function returns `Notifier*`.

- **(a)** *(2)* What does that signature fail to tell the caller?
- **(b)** *(2)* What happens if `cfg` is unrecognised? **Trace what the caller does with the result**
  and say what goes wrong.

---

## Part B — Refactor (18 pts)

**B1.** *(10)* Rewrite it using **Decorator**: one class per *feature*, not per combination, composed
at run time.

**Requirements:**

- the transports are the base cases;
- a `Decorator` base holding a `std::unique_ptr<Notifier>`;
- **no raw `new` or `delete` anywhere**;
- **byte-identical output** to the original for every configuration in the demo.

**B2.** *(4)* Rewrite `make()` to return `std::unique_ptr<Notifier>` and build the chain by **parsing
the config string**, so that `"ts+enc+zip"` composes three decorators rather than selecting one class.

**B3.** *(4)* Now add a **fourth feature** (say, `"sig"` for signing).

**Report how many classes and how many lines you added.** Then report how many the original design
would have needed.

---

## Part C — Verify (6 pts)

**C1.** *(4)* Show that your version produces **the same output as the original** for all six demo
configurations. A `diff` of the two programs' output is the expected evidence.

**C2.** *(2)* Confirm sanitizer-clean, and confirm the caller contains **no `delete`.**

---

## Part D — Judgement (4 pts)

**D1.** *(2)* Count classes before and after, **for three features**. The improvement is smaller than
you might expect.

**Report both numbers honestly**, then explain in one sentence why the class count at n = 3 is the
wrong measure.

**D2.** *(2)* Answer in three sentences: **when would the original design have been the right choice?**

There is a real answer. A response of "never" earns nothing.

---

## Submission

- `notify_fixed.hpp` and your demo.
- `RESULTS.md` — the arithmetic, the diff, and Parts A2, A3, B3 and D.
- Machine, OS, compiler version at the top.

---

## Marking

| Part | Points | Focus |
| --- | --- | --- |
| A | 12 | Seeing what is wrong, including the ownership problem |
| B | 18 | The refactor, with identical behaviour |
| C | 6 | Proving behaviour did not change |
| D | 4 | Honest assessment of what it bought |
| **Total** | **40** | |

---

## Reference Results

**A1 — the arithmetic:**

| features | combination classes ($2^n$) | × 3 transports |
| --- | --- | --- |
| 3 | 8 | 24 |
| 4 | 16 | 48 |
| 5 | 32 | 96 |

**B/C — the refactored version**, verified:

```
plain         console: hello
ts            console: [12:00] hello
enc           console: ENC(hello)
zip           console: ZIP(hello)
ts+enc        console: ENC([12:00] hello)
ts+enc+zip    console: ZIP(ENC([12:00] hello))
```

Byte-identical to the original, sanitizer-clean, zero `delete` in the caller.

**D1 — class counts at three features:**

| | classes |
| --- | --- |
| original | 10 |
| refactored | 8 |

**Adding a fourth feature:** original goes to **18**; refactored goes to **9**.

---

## What This Lab Is Really Showing

**Part D1 is the honest part and it is why this lab is only worth 40 points of measurement-free
argument.**

At three features the refactor takes you from 10 classes to 8. That is not a triumph. If you were
shown only that number you would reasonably ask what the fuss was about.

**The win is not the count; it is the derivative.** Adding a fourth feature takes the original from 10
to 18 and the refactored from 8 to 9. The original grows exponentially in features and the refactored
grows linearly, and at n = 3 the two curves have barely separated.

That is worth sitting with, because **it is the shape of most design arguments.** A better design
usually looks marginal on today's requirements and decisive on next year's — which is exactly why
Lecture 22 §6.2 insists you name the change you expect. **If no fourth feature is ever coming, the
original code was fine**, and D2 is asking you to admit that.

The second thing this lab shows is that the class explosion was not even the worst problem. `make()`
returned a raw owning pointer and returned `nullptr` for a bad config — a Week 5 failure and a crash
waiting for a typo in a config file. **The pattern fixed the structure; `unique_ptr` fixed the bug**,
and only one of those two was on the syllabus this week.

---

*PROG 102 · Week 7 · Lab 7 · © CSE Department*
