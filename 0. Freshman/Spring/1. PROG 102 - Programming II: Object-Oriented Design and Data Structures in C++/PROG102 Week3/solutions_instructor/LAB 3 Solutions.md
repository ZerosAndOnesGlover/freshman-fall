# PROG 102 · Lab 3 — Solutions and Checkoff Notes
## Profiling STL Containers

**INSTRUCTOR / TA COPY — not for distribution**

---

## Before the Session

**Part B is the session.** A and C and D produce numbers that confirm the lectures; **B produces two
numbers that point in opposite directions**, and the marks are for reconciling them.

**Budget:** A 20 min, B 40 min, C 25 min, D 15 min, 20 min slack. **If time is short, cut Part C to
`int` keys only** rather than shortening B.

**Three things to say before anyone starts:**

1. **Use the result of every benchmark loop.** At `-O2` GCC will delete a loop whose result is never
   read. A student reporting that summing a million `list` elements took 0.00 ms has measured an empty
   loop. `volatile` sink or print it.
2. **Never time a sanitizer build.** Part D2 is the only sanitizer build and it is not timed.
3. **B has two halves and the second one reverses the first.** Say this up front — otherwise students
   finish B1, conclude "lists are useless", and write that in B3 before running B2.

**On the list benchmark at N = 50,000:** it takes about **8 seconds**. That is expected and is the
point. Warn them not to try N = 200,000 unless they want to wait two minutes.

---

## Part A — Traversal (10)

### A1 (6)

| | time | vs vector |
| --- | --- | --- |
| `vector` | 9.7 ms | 1.0× |
| `deque` | 10.6 ms | 1.1× |
| `list` | 61.2 ms | **6.3×** |

*Marking: 6 for three times and the ratios. **Accept 3×–10× for the list** — it varies considerably with
cache size and allocator behaviour. A ratio below 1.5× means the loop was optimised away; send them
back.*

### A2 (4)

Expected substance: all three are $O(n)$ in element count, but a `vector`'s elements are contiguous
so one memory fetch brings in many of them, while a `list`'s nodes are separate allocations scattered
across the heap and each one is an independent trip to memory. `deque` is chunked, so it is nearly as
good as `vector`.

*Marking: 4. **Cache lines need not be named** — Week 12 does that. "Contiguous versus scattered" with
a consequence earns full marks. "Lists are slower" with no mechanism is 1.*

---

## Part B — The Insertion Paradox (14)

### B1 (6)

| N | vector | list | ratio |
| --- | --- | --- | --- |
| 1,000 | 0.08 ms | 0.41 ms | 5.1× |
| 5,000 | 0.71 ms | 32.5 ms | 45.9× |
| 20,000 | 6.60 ms | 1,038 ms | 157× |
| 50,000 | 45.3 ms | 8,086 ms | **178×** |

*Marking: 6 for four values with a **growing** ratio. The growth is the informative part — a student
with a flat ratio has probably used `lower_bound` on the list too (which compiles, walks linearly, and
changes the shape).*

### B2 (4)

| `vector` | `list` | ratio |
| --- | --- | --- |
| 446 ms | 3.5 ms | **128×** |

*Marking: 4. **A student who skipped B2 cannot score B3(b) or (c)** — flag it at checkoff rather than
at marking.*

### B3 (4) — the assessed question

**(a) (1)** vector by ~178× with the search; list by ~128× without it.

**(b) (2)** The list's $O(1)$ insertion is real and B2 demonstrates it. In B1 the insertion is
preceded by a **search**, which for a list is an $O(n)$ walk through scattered memory and for a vector
is an $O(\log n)$ binary search over contiguous memory. **The search dominates**, so the container with
the worse insertion wins the operation.

**(c) (1)** The table describes **one operation in isolation** and says nothing about how you obtained
the position — nor about locality.

*Marking: 1 + 2 + 1. **"Lists are bad" scores 0 for (b)**, since their own B2 refutes it. The answer
must locate the cost in the **search**.*

---

## Part C — Associative Containers (10)

### C1 (5)

| | `map` | `unordered_map` | ratio |
| --- | --- | --- | --- |
| insert | 76.1 ms | 44.5 ms | 1.71× |
| lookup | 98.1 ms | 15.1 ms | **6.50×** |

*Marking: 5. Accept 3×–10× on lookup.*

### C2 (3)

```
map           : 1 2 3 4 5
unordered_map : 3 2 4 1 5
```

`map` gives **sorted iteration**, plus `lower_bound`/`upper_bound` range queries. Whether 6.5× "looks
expensive" is a judgement — **accept either verdict if argued.** The good answer notes that it is
expensive *if you never needed the order*, which is most of the time, and free if you did.

*Marking: 2 the demonstration, 1 the judgement.*

### C3 (2)

`std::find` 2,119 ms against `s.find` 0.3 ms — **about 6,000×**.

The generic algorithm receives only two iterators. **It has no way to know the range is sorted**, let
alone that it is a balanced tree, so it can only walk it.

*Marking: 1 the ratio, 1 the reason. The reason must be about what the algorithm can **know**.*

---

## Part D — `reserve` and Invalidation (6)

### D1 (3)

`reserve` gave **4.59×** at 10⁵ and **2.47×** at 10⁶. Growth factor **2.0**; **21** capacity changes
per million `push_back`s, ending at 1,048,576.

*Marking: 2 the speedups, 1 growth factor and count. **MSVC users will report 1.5 and ~35 changes** —
correct, and worth noting aloud.*

**Why the speedup shrinks with n:** at 10⁶ the total work is dominated by the million constructions
either way; the reallocations are only ~21 events, and their relative contribution falls.

### D2 (3)

ASan `heap-use-after-free`, then silence after `reserve`.

**(2 of the 3)** — **Not correct; merely not currently failing.** The code holds an iterator across a
`push_back`, which is undefined behaviour whenever a reallocation happens. `reserve` removes the
reallocation *for this input size*. Change the count, add a `push_back`, or have someone else's code
grow the vector, and the bug returns — **and it will not be reported next time either, because ASan
only sees the reallocation when it happens.**

*Marking: 1 both transcripts, 2 the judgement. **"Yes, it's fixed" scores 0 of the 2.***

---

## Checkoff Checklist

1. Benchmark results **used**, not discarded — no suspiciously-zero timings.
2. Three runs minimum; `-O2` throughout.
3. **B2 present.** Not optional.
4. B3(b) locates the cost in the search.
5. D2 answers "not correct, merely not failing".

---

## Marking Summary

| Part | Points |
| --- | --- |
| A | 10 |
| B | 14 |
| C | 10 |
| D | 6 |
| **Total** | **40** |

---

## Note for the Lab

Close on Part B, and be careful to close on the right thing. The wrong summary is "linked lists are
slow"; students will leave with it unless you say otherwise, and it is refuted by their own B2 table.

> **Both of your numbers are right. The list's $O(1)$ insertion is real — you measured a 128× win with
> it. You also measured a 178× loss, in a program that had to find the position first.**
>
> **The complexity table answered a question adjacent to the one you asked.**

Then the connection to last week, which is worth making explicit because it is the same lesson from a
different direction:

- **Lab 2:** a correct *measurement* with a wrong *explanation* attached. Fixed by a control.
- **Lab 3:** a correct *theory* answering a slightly different *question*. Fixed by measuring the thing
  you actually intend to do.

**Neither theory nor measurement is self-sufficient**, and the interesting engineering lives in the gap
between them. That gap is where Week 12 ends up, and it is why this course keeps asking for both.

If there is time, one further question worth putting to the room: **which of B1 and B2 looks more like
the code you write?** Almost nobody holds an iterator to the right position already. That is the honest
reason Lecture 11 §8 says "use `vector`, change for a reason you can name."

---

*PROG 102 · Week 3 · Lab 3 Solutions · © CSE Department*
