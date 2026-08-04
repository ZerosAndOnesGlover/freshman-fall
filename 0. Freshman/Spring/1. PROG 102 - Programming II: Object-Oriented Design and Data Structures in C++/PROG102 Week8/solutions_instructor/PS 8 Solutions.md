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

## Part B — Strategy, Measured (30)

### B1 (6)

Adding a fourth strategy: **one new class, zero call sites.**

*Marking: 4 the implementation, 2 the counts.*

### B2 (12)

| | time | vs lambda |
| --- | --- | --- |
| virtual Strategy | 165.7–167.6 ms | 1.04× |
| **`std::function`** | **287.5–304.1 ms** | **1.85×** |
| lambda / template | 159.9–160.9 ms | 1.00× |
| default `operator<` | 149.9–151.2 ms | 0.94× |

*Marking: 8 the four measurements with three runs and identical outputs confirmed, 4 for **a prediction
recorded before running**.*

**Award the prediction marks regardless of whether the prediction was right.** Most students rank
`std::function` second; it is last. **A student who predicted correctly and shows no working should be
spot-checked** — the sheet asks them to write it down first.

### B3 (6)

**(a)** `std::function`, at about **1.85×** the lambda.

**(b)** Type erasure. A `std::function` can hold any callable of the right signature, so it stores a
pointer to a type-erased wrapper and calls through it — **and that call cannot be inlined**, because
the target is not known at compile time. In `std::sort`'s inner loop that is roughly $4 \times 10^7$
uninlinable calls.

**Week 3's `qsort` figure: about 2×.** This week's: 1.85×. **They are close because the mechanism is
identical** — a callable whose type is erased, in a hot loop, costs about a factor of two, whether the
erasure is spelled as a function pointer or as `std::function`.

*Marking: 3 + 3. **Full marks require both ratios and the statement that the mechanism is the same.**
An answer that says "`std::function` is slow because it's dynamic" without connecting to inlining is
2 of the 6.*

### B4 (6)

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

## Part C — Command (22)

### C1 (8), C2 (8)

Both must produce identical output. Reference counts for the append-only version:

| | non-blank lines | types |
| --- | --- | --- |
| 1994 style | **20** | **4** |
| modern | **8** | **2** |

Students implementing **append and erase** will have higher counts for the 1994 version (a second
command class) and roughly unchanged counts for the modern one — **which is the point, and worth a
comment in feedback if they notice it.**

*Marking: 8 + 8, with 3 of the second 8 for the counts.*

### C3 (6)

**(a)** Redo needs a second stack. The 1994 version pushes the popped `unique_ptr<Command>` onto it;
the modern version pushes the popped `Action`. **Roughly equal work** — this is a case where the
lambda version's advantage does not compound.

**(b)** The 1994 version wins when the action must be **inspected**: serialised to a file, sent over a
network, logged with a human-readable name, or displayed in a UI as "Undo *Rename*". **A
`std::function` cannot tell you what it does**; a `Command` object can carry a name and parameters.

*Marking: 3 + 3. **(b) must name inspection, serialisation or identity.** "Sometimes classes are
clearer" is 1.*

---

## Part D — The Argument (16)

### D1 (6)

Expected substance: Strategy and Command existed because C++ had no way to pass behaviour-with-state as
a value; a class with a virtual method was the only mechanism; C++11 lambdas provide it directly, and
the measured result is fewer lines, fewer types and better performance.

*Marking: 6 for a coherent argument citing one pattern with evidence. **The evidence must be from their
own work** — the line count or the benchmark.*

### D2 (6)

Strong counterexamples: **Observer** (lifetime and notification, not callable-passing), **State**
(multiple methods and identity per state), **Template Method** (hierarchy structure), **Composite**
(a tree is a data structure, not a function), **Facade** (an architectural boundary).

*Marking: 6. **The pattern chosen must genuinely not be about packaging a callable.** A student who
picks Strategy and argues badly gets 2; one who picks Observer and argues well gets 6.*

### D3 (4)

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
| B | 30 |
| C | 22 |
| D | 16 |
| **Total** | **100** |

---

## What to Watch For

1. **A `detach` in A2.** Reintroduces the coupling the pattern exists to avoid.
2. **`shared_ptr` observers.** A leak by design.
3. **"It crashes" as the whole of A4(b).** The fact that later observers are *skipped* is what Week 9
   needs.
4. **B3 without both ratios.** The connection to Week 3 is the assessed idea.
5. **A vague B4.** "More flexible" is not an example.
6. **A student who fixed A4.** Note it approvingly; mark the demonstration.

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
