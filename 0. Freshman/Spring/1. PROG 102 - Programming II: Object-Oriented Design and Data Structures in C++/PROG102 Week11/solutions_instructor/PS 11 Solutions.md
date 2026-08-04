# PROG 102 · Problem Set 11 — Solutions and Marking Notes
## Imperative to Functional

**INSTRUCTOR COPY — not for distribution**

---

## Before Marking

**Reference environment:** g++ 13.3.0, x86-64 Linux. `sizeof` values and the SBO threshold are exact;
timings are not.

**This set is due the same day as Project 2, in final-exam week.** It is short for that reason.
**Mark generously on Part C's prose** and strictly on B1, B2 and B4, which are the measurements the
final draws on.

---

## Part A — What a Lambda Is (26)

### A1 (8)

Hand-written functor and lambda both **4 bytes**. Traits: class **yes**, copy-constructible **yes**,
default-constructible **no**.

*Marking: 4 the comparison, 2 both working with `count_if`, 2 the traits.*

### A2 (8)

| Lambda | `sizeof` |
| --- | --- |
| `[]` | **1** |
| `[x]` | **4** |
| `[x,d]` | **16** |
| `[&x]` | **8** |
| `[s]` (`std::string`) | **32** |
| `[&]` capturing two | **16** |

*Marking: 5 the measurements, 3 the predictions **recorded before measuring**.*

**Award prediction marks for honest wrong answers.** The two people usually miss are `[]` (they guess
0, not 1 — Week 0's empty-class rule) and `[s]` (they guess 8, thinking a pointer, not 32).

### A3 (4)

`[x]` prints the value at capture time, not the modified one. With `mutable`, the internal copy
persists across calls.

*Marking: 2 + 2.*

### A4 (6)

**(a)** **No warnings** under `-Wall -Wextra -pedantic`.
**(b)** ASan: `stack-use-after-return ... in operator()`.
**(c)** `[this]` after the object dies: `heap-use-after-free`. `[*this]` returns the correct value.

*Marking: 2 each. **(a) must report the silence explicitly** — a student who writes "no warnings" has
answered; one who omits the part has not checked.*

---

## Part B — Storing Callables (28)

### B1 (10)

| | ns per call |
| --- | --- |
| lambda, direct | **0.606–0.667** |
| function pointer | **1.499–1.539** |
| `std::function` | **2.153–2.209** |

*Marking: 7 the three figures with three runs, 3 for **stating what they changed** to defeat the
optimizer.*

**A student reporting 0.00 ns for any version has not fixed the benchmark.** Deduct 4 and point at the
first attempt in the lab's reference numbers — this is the fourth time this course has done it to
them.

### B2 (8)

`sizeof(std::function<int()>)` = **32**; allocation begins at **17 bytes**.

*Marking: 5 the threshold found by sweeping, 3 the `sizeof`. **Accept any threshold** — it is
implementation-defined, and a student on libc++ will get a different number. Mark the method.*

### B3 (4)

A `std::string` capture is 32 bytes → **allocates**. Captured by reference → 8 bytes → **does not**.

**The risk:** the by-reference version dangles if the lambda outlives the string — A4's bug, arrived at
from a performance motivation, which is how it usually happens in real code.

*Marking: 2 the measurements, 2 the risk. **Full marks require naming the dangling risk**, since the
optimisation invites it.*

### B4 (6) — the assessed question

Expected substance:

> Per bare call, the erasure indirection is essentially the whole cost, so the ratio is large (3.5×).
> Inside `std::sort`, the comparison is one part of a body that also swaps elements, moves data and
> chases memory — so the same absolute overhead is a smaller fraction of the total, giving 1.85×.
> **Both measure the same overhead against different denominators.**

*Marking: 6. **"The sort is doing more work" is the answer**; an answer that claims one of the two
measurements is wrong gets 1.*

---

## Part C — Functional Style (26)

### C1 (14)

Seven rewrites covering map, filter, fold, search, and partition/sort.

*Marking: 2 per rewrite. **Require the category coverage** — a student with seven `transform` calls has
not met the spec.*

### C2 (6)

A composed operation:

```cpp
template <class F, class G> auto compose(F f, G g){ return [f,g](auto x){ return g(f(x)); }; }
```

**Its type is unnamable** — it is a lambda, so `auto` is required, or `std::function` if it must be
stored in a container or returned from a non-template function.

*Marking: 4 working composition, 2 the type discussion. Must mention that the type has no name.*

### C3 (6) — the assessed question

**Two nominations required.** Good ones:

- **A loop with an early exit** that `find_if` cannot express — e.g. one that must break on a condition
  computed from state accumulated so far.
- **A loop doing several unrelated things per element**, where splitting into three algorithm calls
  means three passes.
- **A loop with an index-dependent body** — comparing `v[i]` with `v[i-1]` — where the algorithm
  version needs `adjacent_find` plus assembly and is worse.
- **Anything needing two containers in lockstep** without `zip` (C++23).

*Marking: 3 each. **A nomination with no argument gets 1.** A student who nominates nothing gets 0 —
the sheet requires two, and Week 3's "prefer algorithms" was always bounded.*

---

## Part D — Modern Features (20)

### D1 (6)

`static_assert` on the result, and `std::array<int, N>` where `N` is the computed value.

*Marking: 3 each. **Both proofs required** — a student giving only the `static_assert` has one.*

### D2 (6)

`if constexpr` dispatches correctly. With a plain `if`, the error is that `std::to_string` (or
whatever) has no overload for the type in the untaken branch — **because a plain `if` compiles both
branches.**

*Marking: 3 the working version, 3 the error and explanation.*

### D3 (4)

Before/after with structured bindings.

*Marking: 4.*

### D4 (4)

A ranges rewrite, uncompiled. Expected savings: no iterator pairs, laziness (no intermediate
container), composability.

*Marking: 4 for a plausible rewrite and two named savings. **Do not penalise syntax errors** — they
cannot compile it.*

---

## Marking Summary

| Part | Points |
| --- | --- |
| A | 26 |
| B | 28 |
| C | 26 |
| D | 20 |
| **Total** | **100** |

---

## What to Watch For

1. **0.00 ns in B1.** The fourth self-deleting benchmark of the course.
2. **Missing the silence** in A4(a) — the absence of a warning is the finding.
3. **Claiming one of B4's two ratios is wrong.** Both are correct.
4. **Fewer than two nominations** in C3.
5. **Only one proof** in D1.
6. **`[s]` predicted as 8 bytes** in A2 — worth a comment, since it is the same misconception that
   makes people capture strings by reference and then dangle.

---

## Feeding Into Week 12 and the Final

**Week 12 is the last week**: testing, `perf`, cache behaviour, and system design.

**B1's numbers are the setup for it.** A lambda call is 0.6 ns; a cache miss is roughly 100 ns. **Week
12's opening question is which of those two your program is actually spending its time on**, and
students who have B1 in front of them can answer it.

**Say on Monday that the final's Section D will include a table from Weeks 10–12**, since those are the
weeks not covered by either midterm and students systematically under-revise them.

---

*PROG 102 · Week 11 · PS 11 Solutions · © CSE Department*
