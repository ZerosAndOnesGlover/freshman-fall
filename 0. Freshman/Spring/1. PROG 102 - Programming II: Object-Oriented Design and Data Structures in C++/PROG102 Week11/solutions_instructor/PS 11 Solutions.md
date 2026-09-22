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

> **Revised 2026-09-22.** Part B (timing callables, the `std::function` allocation threshold, and the 1.85× versus 3.5×
> question) was removed: Lab 11 Parts A–C are the same experiments. Old C and D are B and C;
> re-weighted to keep 100.

## Part A — What a Lambda Is (35)

### A1 (10)

Hand-written functor and lambda both **4 bytes**. Traits: class **yes**, copy-constructible **yes**,
default-constructible **no**.

*Marking: 4 the comparison, 2 both working with `count_if`, 2 the traits.*

### A2 (10)

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

### A3 (6)

`[x]` prints the value at capture time, not the modified one. With `mutable`, the internal copy
persists across calls.

*Marking: 2 + 2.*

### A4 (9)

**(a)** **No warnings** under `-Wall -Wextra -pedantic`.
**(b)** ASan: `stack-use-after-return ... in operator()`.
**(c)** `[this]` after the object dies: `heap-use-after-free`. `[*this]` returns the correct value.

*Marking: 2 each. **(a) must report the silence explicitly** — a student who writes "no warnings" has
answered; one who omits the part has not checked.*

---

## Part B — Functional Style (32)

### B1 (16)

Seven rewrites covering map, filter, fold, search, and partition/sort.

*Marking: 2 per rewrite. **Require the category coverage** — a student with seven `transform` calls has
not met the spec.*

### B2 (8)

A composed operation:

```cpp
template <class F, class G> auto compose(F f, G g){ return [f,g](auto x){ return g(f(x)); }; }
```

**Its type is unnamable** — it is a lambda, so `auto` is required, or `std::function` if it must be
stored in a container or returned from a non-template function.

*Marking: 4 working composition, 2 the type discussion. Must mention that the type has no name.*

### B3 (8) — the assessed question

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

## Part C — Modern Features (33)

### C1 (9)

`static_assert` on the result, and `std::array<int, N>` where `N` is the computed value.

*Marking: 3 each. **Both proofs required** — a student giving only the `static_assert` has one.*

### C2 (9)

`if constexpr` dispatches correctly. With a plain `if`, the error is that `std::to_string` (or
whatever) has no overload for the type in the untaken branch — **because a plain `if` compiles both
branches.**

*Marking: 3 the working version, 3 the error and explanation.*

### C3 (7)

Before/after with structured bindings.

*Marking: 4.*

### C4 (8)

A ranges rewrite, uncompiled. Expected savings: no iterator pairs, laziness (no intermediate
container), composability.

*Marking: 4 for a plausible rewrite and two named savings. **Do not penalise syntax errors** — they
cannot compile it.*

---

## Marking Summary

| Part | Points |
| --- | --- |
| A | 35 |
| B | 32 |
| C | 33 |
| **Total** | **100** |

---

## What to Watch For

1. **Missing the silence** in A4(a) — the absence of a warning is the finding.
2. **Fewer than two nominations** in B3.
3. **Only one proof** in C1.
4. **`[s]` predicted as 8 bytes** in A2 — worth a comment, since it is the same misconception that
   makes people capture strings by reference and then dangle.

---

## Feeding Into Week 12 and the Final

**Week 12 is the last week**: testing, `perf`, cache behaviour, and system design.

**Lab 11's numbers are the setup for it.** A lambda call is 0.6 ns; a cache miss is roughly 100 ns. **Week
12's opening question is which of those two your program is actually spending its time on**, and
students who have Lab 11's table in front of them can answer it.

**Say on Monday that the final's Section D will include a table from Weeks 10–12**, since those are the
weeks not covered by either midterm and students systematically under-revise them.

---

*PROG 102 · Week 11 · PS 11 Solutions · © CSE Department*
