# PROG 102 · Lab 2 — Solutions and Checkoff Notes
## What Templates Cost

**INSTRUCTOR / TA COPY — not for distribution**

---

## Before the Session

**This is a measurement lab, and Part C is the whole point.** Parts A, B and D produce numbers that
confirm the lectures. Part C produces a number that **refutes the standard explanation** of those
numbers, and the session should be paced so that everyone reaches it.

**Budget:** A 25 min, B 35 min, C 25 min, D 15 min, with 20 min of slack. **If the room is running
late, cut Part B down to four values of N rather than sacrificing Part C.**

**Two things to say at the start:**

1. **Timing discipline.** `-O2` for every timing, never a sanitizer build, three runs minimum. Students
   who time an ASan build get numbers several times too slow and conclude templates are expensive.
2. **The disappearing-symbol trap.** Part A2 needs members *declared* in the class and *defined*
   outside, or the assembly will be empty. This has now caught students in Lecture 01 §2.1 and PS 2 A1.
   **Warn them explicitly** — it is the single biggest time sink in this session.

**Machines vary.** Text sizes should be close to the reference on x86-64 Linux with GCC 13; on other
compilers or architectures they will not be, and that is fine. **Mark the trend and the comparison, not
the absolute bytes.**

---

> **Revised 2026-09-22.** Part D (error-message lengths) was removed: it repeated PS 2 Part E and needed `std::vector` and
> `std::sort`, which arrive the day after this lab (Week 3). Points re-weighted to keep 40.

## Part A — Is Runtime Really Free? (12)

### A1 (4)

Two stacks, one templated on `T`, one hard-coded to `int`, with members declared in-class and defined
out-of-class.

*Marking: 4. Deduct 2 if members are defined in the class body — A2 will then produce nothing and they
will have spent twenty minutes on it.*

### A2 (4)

| Pair | Result |
| --- | --- |
| `TStack<int>::push` vs `IStack::push` | **Identical**, 11 instructions |
| `TStack<int>::pop` vs `IStack::pop` | **Identical**, 8 instructions |

*Marking: 2 both listings, 1 the verdict. **They must say how they handled label names** — `.L6` vs
`.L9` and the `.LFB` frame labels differ and are not code. A student who reports "different" **because**
of label names has done the work correctly and drawn the wrong conclusion: award 2 of the 3 and
correct it.*

### A3 (4)

Reference, 1024 ints × 20,000 reps:

| | run 1 | run 2 | run 3 |
| --- | --- | --- | --- |
| `TStack<int>` | 32.94 ms | 29.95 ms | 27.86 ms |
| `IStack` | 27.53 ms | 28.49 ms | 27.37 ms |

**Within run-to-run variation.** The template's slowest and second-fastest runs are both in this table,
which is what noise looks like.

*Marking: 2 timings with three runs and a checksum, 1 the verdict. **A student who ran once and
concluded the template is 20% slower gets 1** — the sheet requires three runs, and this is exactly why.
Do not accept a difference claim that is smaller than their own spread.*

---

## Part B — Code Size and Compile Time (16)

### B1 (7)

| types | compile (s) | text (bytes) |
| --- | --- | --- |
| 1 | 0.16 | 2,776 |
| 5 | 0.18 | 4,477 |
| 10 | 0.25 | 6,551 |
| 25 | 0.42 | 12,802 |
| 50 | 0.75 | 23,199 |
| 100 | 1.55 | 43,993 |

*Marking: 6 for a working generator and six data points. Accept four points if they were short of time.*

### B2 (4)

$(43{,}993 - 2{,}776) / 99 \approx$ **416 bytes per instantiation.** Linear.

*Marking: 2 the arithmetic, 2 for arguing linearity **from the numbers** — e.g. that successive
differences are roughly constant, or that a fitted slope predicts intermediate points. "It looks
linear" is 1 of the 2.*

### B3 (5)

$(1.55 - 0.16)/99 \approx$ **14 ms per instantiation.** Compile time grows slightly *faster* than
linearly at the top end on the reference machine.

*Marking: 2 arithmetic, 2 the comparison. **Accept either verdict if argued from their data** — the
superlinearity is mild and machine-dependent.*

---

## Part C — Where Does the Bloat Come From? (12)

### C1 (6)

The generator emits 100 hand-written classes with identical members.

*Marking: 5 for a genuinely equivalent program. **Check they kept the same members** — a hand-written
version missing the copy constructor and assignment will be smaller and will produce a false
disagreement.*

### C2 (6)

| | compile | text |
| --- | --- | --- |
| `Stack<T>` × 100 | 1.55 s | **43,993** |
| 100 hand-written | 1.84 s | **43,993** |

**(a)** Identical — byte for byte on the reference machine.
**(b)** The **template** is faster to compile.
**(c)** Expected reply, in substance:

> The measurement is right: code size does grow linearly with instantiations, and on a large project
> that matters. But it is not caused by templates — writing those hundred classes by hand produces
> exactly the same 43,993 bytes and takes longer to compile. The cost comes from the number of distinct
> types, so the fix is to reduce instantiations, not to give up genericity.

*Marking: 2 (a), 2 (b), 2 (c). **(c) must be fair to the colleague** — a reply that just says "you're
wrong" scores 0 even if technically correct. The sheet asks for fairness deliberately; this is a
communication mark and should be marked as one.*

> **If a student's two text sizes differ by more than a few per cent**, work through it with them
> before they write it up. Almost always one of: different flags between the two builds, the
> hand-written classes missing members, or the template version instantiating extra members the
> hand-written one lacks. **A student who investigates and reports a genuine reproducible difference
> should get full marks** — the sheet promises this and it is the right scientific instinct.

---

## Checkoff Checklist

1. `-O2` used for all timings; **no sanitizer build timed**.
2. Three runs minimum in A3, with a checksum.
3. A2 states how label differences were handled.
4. Part C's hand-written classes have the **same members** as the template.
5. C2(c) is fair to the colleague.

---

## Marking Summary

| Part | Points |
| --- | --- |
| A | 12 |
| B | 16 |
| C | 12 |
| **Total** | **40** |

---

## Note for the Lab

Close on Part C, and make it about method rather than about templates:

> Part B gave you a correct measurement. The explanation everybody attaches to it is wrong, and it took
> **one control experiment** to find that out — write the same classes by hand and compare.

Then the general form:

> **When you measure something, ask what else would produce the same number.**

This is worth ten minutes because it recurs all semester and gets harder each time. **Week 11** asks
whether lambda overhead is real. **Week 12** asks whether a `vector` beats a linked list because of
cache behaviour or because of allocation count — two explanations for one measurement, and the lab
separates them the same way.

It is also the honest reason this course measures everything. Not because measurements are
authoritative — Part C shows they are not, on their own — but because **a measurement is the only thing
you can build a control around.** You cannot run a control on an opinion.

---

*PROG 102 · Week 2 · Lab 2 Solutions · © CSE Department*
