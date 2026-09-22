# PROG 102 · Lab 2
## What Templates Cost

**Date:** Monday 8 February 2027 · 15:00–16:50 · Lab section (Week 3) — covers Week 2 (L07–L09)
*2-hour lab · 40 points · in-lab checkoff · part of the Labs component (20%)*
**Deliverable:** `bench/` directory with your generators and programs, `RESULTS.md`. In-lab checkoff.

---

## Purpose

The claim from Lecture 09 is that templates are a **zero-overhead abstraction**: the cost is paid at
compile time, not runtime. This lab makes you check both halves of that sentence yourself.

You will measure three things — runtime, binary size, compile time — and then test the explanation
that is usually attached to the results. **One widely-repeated claim about template code bloat does
not survive the measurement**, and Part C is where you find that out.

> **Timing discipline, from the syllabus:** every runtime measurement uses the `-O2` line. **Never time
> a sanitizer build.** Report your machine, OS and compiler version at the top of `RESULTS.md`, and run
> each timing at least three times.

---

## Part A — Is Runtime Really Free? (12 pts)

**A1.** *(4)* Write two stacks holding `int`:

- `TStack<T>` — a class template;
- `IStack` — the same code with `T` replaced by `int` throughout.

Both need `push`, `pop` and `size`. **Declare the members in the class and define them outside**, or
the symbols will not be emitted and A2 will produce nothing.

**A2.** *(4)* Compile both at `-O2 -S` and compare the assembly of `push` and `pop`.

Paste both. **State whether they are identical.** Local label names (`.L6` vs `.L9`) and CFI directives
are bookkeeping, not code — normalise or ignore them, and say that you did.

**A3.** *(4)* Benchmark both: push 1024 `int`s and pop them all, at least 20,000 times. Report the time
for each, **three runs each**, and a checksum proving they did the same work.

**State whether the difference exceeds your run-to-run variation.**

---

## Part B — Code Size and Compile Time (16 pts)

**B1.** *(7)* Write a generator that emits a program instantiating your `Stack<T>` for **N distinct
struct types**. Each struct should be non-trivial — a couple of `double`s and an `int` — and each
instantiation should exercise construction, a `push`, a copy and an assignment.

Run it for **N = 1, 5, 10, 25, 50, 100** and record, for each:

- wall-clock compile time;
- the **text segment size** (`size ./prog`, first column);
- the binary size on disk.

**B2.** *(4)* Plot or tabulate text size against N. **Compute the bytes per additional instantiation.**

Is the growth linear? Say so from your numbers rather than by inspection.

**B3.** *(5)* Do the same for compile time. **Compute the milliseconds per additional instantiation**,
and state whether compile time grows faster than, slower than, or in line with code size.

---

## Part C — Where Does the Bloat Come From? (12 pts)

This is the part that matters.

**C1.** *(6)* Modify your generator to emit, instead of one template instantiated N times, **N separate
hand-written classes** — no templates anywhere. Same members, same operations, same element structs.

Run it at **N = 100** and record compile time and text size.

**C2.** *(6)* Compare against your N = 100 template result. Answer all three:

- **(a)** *(2)* Report both text sizes. **Are they different?**
- **(b)** *(2)* Report both compile times. **Which is faster?**
- **(c)** *(1)* A colleague says "we should avoid templates because they cause code bloat". Using your
  two numbers, write a **two-sentence** reply that is fair to their concern and corrects it.

> If your two text sizes differ substantially, **do not assume the lecture is wrong** — check that the
> hand-written classes really have the same members and that both were built with identical flags. Then
> report what you found either way. A reproducible disagreement is a good result and should be written
> up as one.

---

## Submission

- `bench/` — generators and any scripts, so a marker can rerun everything.
- `RESULTS.md` — all tables, the assembly comparison, and every written answer.
- **Machine, OS and compiler version at the top.**

---

## Marking

| Part | Points | Focus |
| --- | --- | --- |
| A | 12 | Runtime cost measured, not assumed |
| B | 16 | Compile time and code size against instantiation count |
| C | 12 | Testing the explanation, not just the measurement |
| **Total** | **40** | |

---

## Reference Numbers

g++ 13.3.0, x86-64 Linux, `-std=c++17`. **Sizes should match closely; timings will not.**

**A2 — assembly:**

| Function pair | Result |
| --- | --- |
| `TStack<int>::push` vs `IStack::push` | Identical, 11 instructions |
| `TStack<int>::pop` vs `IStack::pop` | Identical, 8 instructions |

**A3 — runtime**, 1024 ints × 20,000 reps, three runs:

| | run 1 | run 2 | run 3 |
| --- | --- | --- | --- |
| `TStack<int>` | 32.94 ms | 29.95 ms | 27.86 ms |
| `IStack` | 27.53 ms | 28.49 ms | 27.37 ms |

**Within run-to-run variation.** Note the template's first run is the slowest of all six and its third
is second-fastest — which is what noise looks like, and why one run would have told you nothing.

**B1 — growth:**

| types | compile (s) | text (bytes) |
| --- | --- | --- |
| 1 | 0.16 | 2,776 |
| 5 | 0.18 | 4,477 |
| 10 | 0.25 | 6,551 |
| 25 | 0.42 | 12,802 |
| 50 | 0.75 | 23,199 |
| 100 | 1.55 | 43,993 |

≈ **416 bytes** and ≈ **14 ms** per additional instantiation.

**C — the comparison:**

| | compile | text |
| --- | --- | --- |
| `Stack<T>` × 100 types | 1.55 s | **43,993** |
| 100 hand-written classes | 1.84 s | **43,993** |

---

## What This Lab Is Really Showing

Part C is the point of the session, and it is a lesson about **explanations** rather than about
templates.

The measurement in Part B is real: code size grows linearly with instantiations, and on a large project
that is a genuine problem. The *explanation* everyone attaches to it — "templates cause bloat" — is
wrong, and Part C falsifies it in about ten minutes. **One hundred types that each need their own
`push` and `pop` require one hundred copies of that code by any mechanism, including copy and paste.**
The template is not the cause. It is the reason you could ask for a hundred of them without noticing.

That distinction changes what you would actually do about it. If templates were the cause, the fix
would be to avoid templates. Since the cause is the *number of distinct types*, the fixes are: use
fewer instantiations, share code that does not depend on `T`, and watch non-type parameters — none of
which involve giving up genericity.

**Getting a correct measurement and then attaching the wrong explanation to it is the most common way
to be wrong with data**, and it is worth having done it once, deliberately, in a lab where the
correction is cheap.

---

*PROG 102 · Week 2 · Lab 2 · © CSE Department*
