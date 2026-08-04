# PROG 102 · Problem Set 3 — Solutions and Marking Notes
## Ten Problems With the STL

**INSTRUCTOR COPY — not for distribution**

---

## Before Marking

**Reference environment:** g++ 13.3.0, x86-64 Linux, `-std=c++17 -O2`. Outputs below are exact.
Timings in Part B are not; **mark the ratios and the reasoning.**

**Calibration:** Part A is 60 points and rewards knowing the library. A student who solved all ten with
loops has demonstrated something, but not the thing being assessed — apply the rule, and point them at
the nomination exercise, which is where that instinct belongs.

**The marks that matter are B2, C1 and C4.** Those are the three where a student can produce correct
code and still hold a wrong model.

---

## Part A — Ten Problems (60)

Reference input: `v = {5,3,8,1,9,2,8,3,7,4}`.

### A1 (6) — word frequency

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

### A2 (6) — deduplicate preserving order

```
5 3 8 1 9 2 7 4
```

`std::copy_if` with a `std::set<int> seen` captured by reference, using `seen.insert(x).second`.

*Marking: 4 output, 2 justification. **`std::unique` is wrong here** and it is the expected error — it
only removes *adjacent* duplicates, so it needs a sorted range and would destroy the order the question
asks to preserve. A student who tried it, noticed, and said so should get full marks.*

### A3 (6) — k-th largest

`std::nth_element` with `std::greater<int>()`, then read index `k-1`. **3rd largest of `v` is 8.**

$O(n)$ average, against $O(n \log n)$ for a full sort.

*Marking: 3 output, 3 the complexity claim. Must say $O(n)$ **average** — `nth_element` is
introselect and its guarantee is average-case.*

### A4 (6) — group anagrams

Sort each word's characters to form a key; `map<string, vector<string>>`.

```
{"eat","tea","ate"}  {"tan","nat"}  {"bat"}
```

*Marking: 4 correct grouping, 2 the key idea. Accept a character-count key as an alternative and note
it is $O(n)$ per word rather than $O(n \log n)$.*

### A5 (6) — set operations

```
intersection : 4 5
union        : 1 2 3 4 5 6 7
difference   : 1 2 3
```

**The precondition is that both input ranges are sorted.** `set_intersection` on unsorted input
silently produces garbage — no error, no warning.

*Marking: 4 the three results, 2 the precondition. **The precondition is the assessed half.** A student
who does not state it loses 2 even with correct output, because their code works by accident on this
input.*

### A6 (6) — rotate

`std::rotate(w.begin(), w.begin()+3, w.end())`:

```
1 9 2 8 3 7 4 5 3 8
```

*Marking: 4 output, 2 justification.*

### A7 (6) — stable partition

`std::stable_partition`, evens first:

```
8 2 8 4 5 3 1 9 3 7
```

`std::partition` gives a different arrangement (implementation-defined, typically `4 3 8 8 2 ...`-ish)
and is not required to preserve relative order.

*Marking: 3 the stable result, 3 for showing `partition` differs. **The student's `partition` output
need not match anything** — it is unspecified. Mark whether they demonstrated a difference.*

### A8 (6) — statistics

```
min=1 max=9 mean=5.00
```

`std::minmax_element` in one pass; `std::accumulate` with `0.0`; sum of squares via
`std::inner_product` or `accumulate` with a lambda.

*Marking: 4 correct values, 2 for **using `0.0`**. A student whose mean is `5` from an `int`
accumulator gets 0 of those 2 and should be pointed at C1 — they have committed the trap the same
problem set warns about.*

### A9 (6) — longest increasing run

`v = 5 3 8 1 9 2 8 3 7 4`. Strictly increasing consecutive runs: `5`, `3 8`, `1 9`, `2 8`, `3 7`, `4`.
**Longest length 2**, first at index 1.

*Marking: 4 correct answer, 2 method. **Accept a raw loop here with justification** — `std::adjacent_find`
gets you the breaks but assembling the answer is awkward, and this is a legitimate nomination for the
Part A note. A student who nominated this problem has chosen well.*

### A10 (6) — top-N by custom key

`std::partial_sort` or `std::nth_element` + `sort` on the first three. **Not a full sort.**

*Marking: 4 correct, 2 for avoiding the full sort. A `std::sort` of everything loses the 2.*

---

## Part B — Choosing a Container (20)

### B1 (8)

Reference:

| N | vector | list | ratio |
| --- | --- | --- | --- |
| 1,000 | 0.08 ms | 0.41 ms | 5.1× |
| 5,000 | 0.71 ms | 32.5 ms | 45.9× |
| 20,000 | 6.60 ms | 1,038 ms | 157× |
| 50,000 | 45.3 ms | 8,086 ms | 178× |

Front insertion, 100,000: vector 446 ms, list 3.5 ms — **list wins 128×**.

*Marking: 5 the sorted-insertion table with a growing ratio, 3 the front-insertion reversal. **A
student who only did (a) gets at most 5** — the reversal is what makes the part meaningful.*

### B2 (6) — the assessed question

Expected substance:

> The list's $O(1)$ insertion is real, but reaching the position costs $O(n)$ pointer-chasing through
> scattered memory, whereas the vector finds it with a binary search over contiguous memory. The
> insertion is the cheap part of the operation and the search dominates. **A complexity table describes
> one operation in isolation; a program does the search as well, on hardware where locality matters.**

*Marking: 3 the search/insert distinction, 3 the general lesson. **"Lists are bad" scores 0** — B1(b)
shows the list winning by 128×, and a student who ignores their own second table has not read it.*

### B3 (6)

`int` keys: insert 1.71×, lookup 6.50× in favour of `unordered_map`.

With `std::string` keys the ratio typically **narrows**, because hashing a string is $O(\text{length})$
and touches the character data, while comparing strings often decides on the first few characters. The
hash's constant factor grows relative to the comparison.

*Marking: 4 both tables, 2 a plausible reason. **Accept any coherent explanation supported by their
numbers**, including "it did not change much on my machine" if they measured that and say so.*

---

## Part C — Four Traps (20)

### C1 (5)

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

### C2 (5)

```
original                  size=7 : 1 2 3 2 4 2 5
after std::remove(...,2)  size=7 : 1 3 4 5 4 2 5
after v.erase(newend,end) size=4 : 1 3 4 5
```

**The algorithm has only iterators.** It can read and write elements but cannot change the container's
size, because it has never heard of the container. Only the container can erase.

*Marking: 3 output **including the tail**, 2 the explanation. A student who printed only `size()` and
not the leftover `4 2 5` loses 1 — seeing the garbage is the point.*

### C3 (5)

ASan reports `heap-use-after-free` on the read through the stale iterator. After `reserve`, no report.

**Is it correct?** *(2 of the 5)* — **No, it is not correct; it merely does not currently fail.** The
code still holds an iterator across a `push_back`, which is undefined behaviour whenever a reallocation
occurs. The `reserve` makes reallocation not happen *for this input*; change the count, or add a
`push_back` elsewhere, and it returns.

*Marking: 3 both transcripts, 2 the judgement. **"Yes, it's correct now" scores 0 of the 2.** The
question says "answer carefully" and this is the distinction it is testing.*

### C4 (5)

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
| B | 20 |
| C | 20 |
| **Total** | **100** |

---

## The Nomination Exercise

**Unmarked and required.** Read them anyway — they are the most informative thing in the submission.

**A9 is the best nomination** and the most common good one: assembling "longest increasing run" out of
`adjacent_find` is genuinely worse than a five-line loop. A student who nominated A9 with a clear
argument has understood the rule's purpose.

**A weak nomination** is one that says the loop is better because "I find loops easier to read". Note
it and move on — but a student who nominated *nothing*, or wrote two sentences of filler, has treated
the rule as a hoop. Say so in the feedback: the point of the constraint is to learn what the library
has, and the point of the nomination is that the constraint is not a law.

---

## What to Watch For

1. **`std::unique` for A2.** Removes only adjacent duplicates. The expected error.
2. **Unsorted input to `set_intersection`** (A5). Works by accident on this data.
3. **`accumulate(..., 0)` for the mean** in A8, having been warned in C1 of the same sheet.
4. **"Lists are bad"** in B2, contradicted by their own B1(b) table.
5. **"Yes, `reserve` made it correct"** in C3. The most important correction in the set.

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
