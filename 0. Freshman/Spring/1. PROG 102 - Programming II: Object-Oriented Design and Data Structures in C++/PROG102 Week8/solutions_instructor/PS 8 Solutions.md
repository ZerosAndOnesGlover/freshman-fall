# PROG 102 · Problem Set 8 — Solutions and Marking Notes
## Observer and Strategy

**INSTRUCTOR COPY — not for distribution**

---

## Before Marking

**Reference environment:** g++ 13.3.0, x86-64 Linux. Counts and sanitizer verdicts are exact; timings
are not.

**This set is due the same day as Project 1**, and it is short for that reason. **Mark Part D
generously** — it is argument, students will be tired, and a defensible position argued briefly is
worth full marks.

**Mark B2 and B3 strictly.** They are the week's central result and the place a wrong model shows.

---

> **Revised 2026-09-22.** Removed B2–B3 (timing the four Strategy forms — Lecture 26 §3's own table). B4 is B2. Capture and
> `std::function` are now taught for use in the new Lecture 25 §4 box. Items re-weighted to keep 100.

## Part A — Observer (32)

### A1 (6)

```
ERROR: AddressSanitizer: stack-use-after-scope
    ... in Subject::set(int)  observer.cpp:14
```

*Marking: 4 the working naive version, 2 the report with the line and function named. **The error names
`Subject::set`, not the observer** — a student who reports the observer as the fault has read the
message and not the cause.*

### A2 (10)

```
observers registered: 2
temp saw 1
alive saw 1
after temp dies, registered: 2
alive saw 42
after notify (pruned):     1
```

*Marking: 5 `weak_ptr` storage with `lock()`-based skipping, 3 pruning during notification, 2 the three
counts reported.*

**Grep for `detach`.** A student who added one has reintroduced the coupling the pattern avoids —
deduct 3 and point at L25 §3.1.

**A student using `shared_ptr` observers** has made the subject co-own them, which leaks by design.
Deduct 5 and explain.

### A3 (6)

**(a)** A `weak_ptr` does not remove itself when the object dies — it merely knows the object is gone.
`observers.size()` counts entries, not live observers, and entries are only removed when notification
walks the list.

**(b)** `live_count()` locks each entry and counts the successes. **It matters when the count is
user-visible or drives a decision** — "no subscribers left, shut down the producer" would be wrong with
the stale count.

*Marking: 3 + 3. **(b) must give a situation where the difference changes behaviour**, not just a
number.*

### A4 (10)

**(a) (4)** Attaching during `notify` mutates the vector being iterated — Week 3's invalidation. Under
ASan this is typically a `heap-use-after-free` or a corrupted traversal. **Any reproducible
demonstration earns the marks**; the exact report varies with the container state.

**(b) (3)** The exception propagates out of `set`, and **observers after the throwing one are never
notified.** The subject is left having notified a prefix of its list.

**(c) (3)** Any pair of handlers where one's effect depends on the other having run.

*Marking: 4 + 3 + 3. **(b)'s answer must state that the remaining observers are skipped** — that is the
fact Week 9 builds on. "It crashes" is 1.*

**Do not award marks for fixing these.** The sheet says not to, and a student who fixed (b) has
pre-empted Week 9 — note it approvingly and mark A4(b) on the demonstration.

---

## Part B — Strategy (16)

### B1 (8)

Adding a fourth strategy: **one new class, zero call sites.**

*Marking: 4 the implementation, 2 the counts.*

### B2 (8)

Acceptable, if specific:

- **storing heterogeneous callables in one container** — a `vector<function<void()>>` of unrelated
  lambdas, which a template parameter cannot express because each lambda has a distinct type;
- **crossing an ABI or translation-unit boundary** — a callback registered in a library compiled
  separately;
- **storing a callable as a member** whose type is not known at class-definition time;
- **runtime selection** — choosing among callables based on data.

*Marking: 6 for a specific case with a clear statement of what a template parameter could not do.
**"More flexible" with no example is 3**, as the sheet warns.*

---

## Part C — Command (30)

### C1 (10), C2 (10)

Both must produce identical output. Reference counts for the append-only version:

| | non-blank lines | types |
| --- | --- | --- |
| 1994 style | **20** | **4** |
| modern | **8** | **2** |

Students implementing **append and erase** will have higher counts for the 1994 version (a second
command class) and roughly unchanged counts for the modern one — **which is the point, and worth a
comment in feedback if they notice it.**

*Marking: 8 + 8, with 3 of the second 8 for the counts.*

### C3 (10)

**(a)** Redo needs a second stack. The 1994 version pushes the popped `unique_ptr<Command>` onto it;
the modern version pushes the popped `Action`. **Roughly equal work** — this is a case where the
lambda version's advantage does not compound.

**(b)** The 1994 version wins when the action must be **inspected**: serialised to a file, sent over a
network, logged with a human-readable name, or displayed in a UI as "Undo *Rename*". **A
`std::function` cannot tell you what it does**; a `Command` object can carry a name and parameters.

*Marking: 3 + 3. **(b) must name inspection, serialisation or identity.** "Sometimes classes are
clearer" is 1.*

---

## Part D — The Argument (22)

### D1 (8)

Expected substance: Strategy and Command existed because C++ had no way to pass behaviour-with-state as
a value; a class with a virtual method was the only mechanism; C++11 lambdas provide it directly, and
the measured result is fewer lines, fewer types and better performance.

*Marking: 6 for a coherent argument citing one pattern with evidence. **The evidence must be from their
own work** — the line count or the benchmark.*

### D2 (8)

Strong counterexamples: **Observer** (lifetime and notification, not callable-passing), **State**
(multiple methods and identity per state), **Template Method** (hierarchy structure), **Composite**
(a tree is a data structure, not a function), **Facade** (an architectural boundary).

*Marking: 6. **The pattern chosen must genuinely not be about packaging a callable.** A student who
picks Strategy and argues badly gets 2; one who picks Observer and argues well gets 6.*

### D3 (6)

Anything plausible and specific: pattern matching / `std::variant` absorbing **Visitor**; reflection
absorbing **Abstract Factory** or serialisation-flavoured Command; coroutines absorbing some **State**
machines; modules changing the calculus for **Facade** and the compilation-firewall argument.

*Marking: 4 for a named feature and a coherent paragraph. **Do not require the prediction to be
plausible to you** — argument quality only.*

---

## Marking Summary

| Part | Points |
| --- | --- |
| A | 32 |
| B | 16 |
| C | 30 |
| D | 22 |
| **Total** | **100** |

---

## What to Watch For

1. **A `detach` in A2.** Reintroduces the coupling the pattern exists to avoid.
2. **`shared_ptr` observers.** A leak by design.
3. **"It crashes" as the whole of A4(b).** The fact that later observers are *skipped* is what Week 9
   needs.
4. **A vague B2.** "More flexible" is not an example.
5. **A student who fixed A4.** Note it approvingly; mark the demonstration.

---

## Feeding Into Week 9

Week 9 opens on **A4(b)**: an observer threw, later observers were never notified, and the subject is
left having notified a prefix of its list.

**Ask on Monday which exception guarantee that is.** The answer is *none of the three* — the operation
neither completed, nor rolled back, nor left the object merely valid-but-changed in a documented way.
It is the case Week 9 exists to give a name to, and students who did A4(b) have the transcript in front
of them.

---

*PROG 102 · Week 8 · PS 8 Solutions · © CSE Department*
