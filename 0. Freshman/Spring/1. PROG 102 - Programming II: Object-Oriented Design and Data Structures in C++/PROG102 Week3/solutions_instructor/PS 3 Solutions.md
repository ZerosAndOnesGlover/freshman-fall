# PROG 102 · Problem Set 3 — Solutions and Marking Notes
## Five Problems With the STL

**INSTRUCTOR COPY — not for distribution**

---

## Before Marking

**Reference environment:** g++ 13.3.0, x86-64 Linux, `-std=c++17 -O2`. Outputs below are exact.
There are no timings in this set.

**Calibration:** Part A is 60 points and rewards knowing Lecture 12's algorithms. A loop where one of
them fits costs part of the problem's marks; a loop in A5 costs nothing.

**The marks that matter are B1 and B3.** Those are the three where a student can produce correct
code and still hold a wrong model.

---

> **Revised 2026-09-22.** Cut to taught material: A3 (`nth_element`), A5 (set algorithms), A6 (`rotate`), A7
> (`stable_partition`) and A10 (`partial_sort`) needed algorithms Lecture 12 never teaches; Part B
> (container timing) is Lab 3; C3 (invalidation under `reserve`) is Lab 3 D2. The no-raw-loops rule is
> relaxed. Remaining: A1, A2, A4, A8, A9 → A1–A5 (12 each); C1, C2, C4 → B1–B3.

## Part A — Five Problems (60)

Reference input: `v = {5,3,8,1,9,2,8,3,7,4}`.

### A1 (12) — word frequency

`unordered_map<string,int>` to count, copy to a `vector<pair<...>>`, `std::sort` with a comparator
falling back to the key.

```
the   3
cat   2
dog   1
```

*Marking: 4 correct output, 2 the container/algorithm justification. **A `map` instead of
`unordered_map` is fine** — the sort discards the order anyway, and a student who says so gets full
justification marks.*

### A2 (12) — deduplicate preserving order

```
5 3 8 1 9 2 7 4
```

`std::copy_if` with a `std::set<int> seen` captured by reference, using `seen.insert(x).second`.

*Marking: 4 output, 2 justification. **`std::unique` is wrong here** and it is the expected error — it
only removes *adjacent* duplicates, so it needs a sorted range and would destroy the order the question
asks to preserve. A student who tried it, noticed, and said so should get full marks.*

### A3 (12) — group anagrams

Sort each word's characters to form a key; `map<string, vector<string>>`.

```
{"eat","tea","ate"}  {"tan","nat"}  {"bat"}
```

*Marking: 4 correct grouping, 2 the key idea. Accept a character-count key as an alternative and note
it is $O(n)$ per word rather than $O(n \log n)$.*

### A4 (12) — statistics

```
min=1 max=9 mean=5.00
```

`std::minmax_element` in one pass; `std::accumulate` with `0.0`; sum of squares via
`std::inner_product` or `accumulate` with a lambda.

*Marking: 4 correct values, 2 for **using `0.0`**. A student whose mean is `5` from an `int`
accumulator gets 0 of those 2 and should be pointed at C1 — they have committed the trap the same
problem set warns about.*

### A5 (12) — longest increasing run

`v = 5 3 8 1 9 2 8 3 7 4`. Strictly increasing consecutive runs: `5`, `3 8`, `1 9`, `2 8`, `3 7`, `4`.
**Longest length 2**, first at index 1.

*Marking: 4 correct answer, 2 method. **Accept a raw loop here with justification** — `std::adjacent_find`
gets you the breaks but assembling the answer is awkward, and this is a legitimate nomination for the
Part A note. A student who nominated this problem has chosen well.*

## Part B — Three Traps (40)

### B1 (14)

```
accumulate({0.5,0.5,0.5}, 0)   -> 0
accumulate({0.5,0.5,0.5}, 0.0) -> 1.5
```

One million `int`s of one million, init `0`:

```
-727379968
```

with UBSan reporting:

```
stl_numeric.h:141:9: runtime error: signed integer overflow:
                     1000000 + 2147000000 cannot be represented in type 'int'
```

**Why the sanitizer catches one and not the other:** signed overflow is **undefined behaviour**;
converting `0.5` to `int` is **well-defined truncation**. UBSan finds undefined behaviour, not wrong
answers.

*Marking: 3 the three results, 2 the distinction. **The distinction is the assessed half** and it is a
genuinely important idea — sanitizers are not correctness checkers.*

### B2 (13)

```
original                  size=7 : 1 2 3 2 4 2 5
after std::remove(...,2)  size=7 : 1 3 4 5 4 2 5
after v.erase(newend,end) size=4 : 1 3 4 5
```

**The algorithm has only iterators.** It can read and write elements but cannot change the container's
size, because it has never heard of the container. Only the container can erase.

*Marking: 3 output **including the tail**, 2 the explanation. A student who printed only `size()` and
not the leftover `4 2 5` loses 1 — seeing the garbage is the point.*

### B3 (13)

```
decltype(vb[0]) is bool? NO   (std::_Bit_reference)
error: cannot bind non-const lvalue reference of type 'bool&' to an rvalue of type 'bool'
```

A template taking `std::vector<T>&` and binding `T& x = v[0];` compiles for every `T` but `bool`.

**On specialization:** `vector<bool>` specialized to *improve space* at the cost of *behaving
differently*, which is exactly what Week 2 §L09 §2.3 warned against. Specialize when a type needs
different logic, not to make one type faster with a different contract.

*Marking: 3 the demonstrations, 2 the specialization lesson. Must connect to the contract, not just say
"vector<bool> is weird".*

---

## Marking Summary

| Part | Points |
| --- | --- |
| A | 60 |
| B | 40 |
| **Total** | **100** |

---

## The Nomination Exercise

**Unmarked and required.** Read them anyway — they are the most informative thing in the submission.

**A5 is the best nomination** and the most common good one: assembling "longest increasing run" out of
`adjacent_find` is genuinely worse than a five-line loop. A student who nominated A5 with a clear
argument has understood the rule's purpose.

**A weak nomination** is one that says the loop is better because "I find loops easier to read". Note
it and move on — but a student who nominated *nothing*, or wrote two sentences of filler, has treated
the rule as a hoop. Say so in the feedback: the point of the constraint is to learn what the library
has, and the point of the nomination is that the constraint is not a law.

---

## What to Watch For

1. **`std::unique` for A2.** Removes only adjacent duplicates. The expected error.
2. **`accumulate(..., 0)` for the mean** in A4, having been warned in B1 of the same sheet.

---

## Feeding Into Week 4

Week 4 turns to inheritance and virtual dispatch — **compile-time polymorphism gives way to runtime
polymorphism**, and the cost changes from zero to one indirection per call.

The framing worth setting up in Monday's lecture: this week's `std::sort` beat `qsort` by 2× precisely
because the template knew the type at compile time and the function pointer did not. **A virtual call
is the function pointer.** Week 4 measures what that costs, and Lab 4 has students read the vtable in
GDB.

---

*PROG 102 · Week 3 · PS 3 Solutions · © CSE Department*
