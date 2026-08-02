# PROG 101 — Lab 6 Solutions (Instructor)
## The Heap and a Dynamic Array

All figures verified by execution on the reference machine (x86-64, GCC 13, glibc 2.39).

---

## Part 1: Mapping the Address Space (4 pts)

**Expected ordering, low to high:**

```
text / literal   ~ 0x626b8d05c031
global / data    ~ 0x626b8d05e010
heap             ~ 0x626bac34d2b0
stack local      ~ 0x7ffeb6bedd2c
```

**Answer 1 (1 pt).** Text and data sit low, the heap above them, the stack very high. The gap
between heap and stack is enormous on a 64-bit address space.

**Answer 2 (1 pt).** A second `malloc` returns a **higher** address — the heap grows **upward**.
*(Accept a lower address if the allocator reused a freed block; the marking point is that the student
observed and reported rather than assumed.)*

**Answer 3 (1 pt).** A nested call's local sits at a **lower** address — the stack grows
**downward**. Verified in Week 3: frames at `...594`, `...584`, `...574`, 16 bytes apart.

**Answer 4 (1 pt).** `static_local` has **static storage duration**, so it lives in the data segment
with the globals, not on the stack — even though its *scope* is the body of `main`. This is the
scope-versus-lifetime distinction: narrow scope, program lifetime.

*This is the question that separates understanding from observation. A student who says "the compiler
puts them in different places" has not answered it.*

---

## Part 2: Watching `realloc` Move (4 pts)

**Answer 1.** With a small increase the block usually stays put (the allocator extends in place).
With a large one — a megabyte — it almost always **moves**, because there is no room to extend.
Students should try both and report the difference.

**Answer 2.** `alias` still holds the **old** address, which `realloc` has freed. It is a **dangling
pointer**. Dereferencing it is use-after-free.

**Answer 3.** ASan reports `heap-use-after-free`, naming the allocation and the free site.

**Answer 4 (the marking point).** **Never hold a pointer into a block across a reallocation.** Hold
an **index** instead, and recompute the pointer after the growth. This is the same hazard as C++
iterator invalidation, and it is why `vec_at` in Lecture 3 returns a pointer that is explicitly
documented as invalid after the next `push`.

---

## Part 3: Dynamic Array (8 pts)

Reference implementation is Lecture 3's, verified: 30 pushes give capacities **4 → 8 → 16 → 32**,
4 `realloc` calls, **28 elements copied**, geometric bound `copies < 2n` confirmed to n = 100,000.
Valgrind clean.

**Marking.**

| Criterion | Points |
|---|---|
| Grows by doubling from 4, contents preserved | 2 |
| Uses a **temporary** for `realloc`; failure leaves the vector valid | 2 |
| Overflow guard on `ncap * sizeof *data` | 1 |
| `vec_push` returns a status and the tests check it | 1 |
| `vec_free` releases everything and resets the struct | 1 |
| **Valgrind-clean under the test suite** | 1 |

**The three recurring defects:**

1. **`v->cap *= 2` with `cap == 0`** stays 0, so `realloc(..., 0)` is called and the first write is
   out of bounds. Must be `cap ? cap * 2 : 4`.
2. **`v->data = realloc(v->data, ...)`** — the headline bug from Lecture 2. Verified: forcing a
   failure with the temporary leaves the caller's pointer, data and capacity intact; without it, the
   block leaks and the data is gone.
3. **Fixed-increment growth** (`cap += 4`) is Θ(n²). It passes every functional test. Cap the growth
   marks at 1 and show them the arithmetic: 4+8+12+…+n ≈ n²/8.

**Amortised analysis question.** Expected answer: doubling copies 4+8+16+…+n < 2n elements in total
across n pushes, so the average per push is **O(1)** even though individual pushes cost O(n).
Verified: 28 copies for 30 pushes, and 131,068 copies for n = 100,000 — comfortably under 2n.

---

## Part 4: Reading Valgrind (4 pts)

**Verified messages** — students must reproduce these, not paraphrase:

| Program | Valgrind reports |
|---|---|
| `leak.c` | `10 bytes in 1 blocks are definitely lost in loss record 1 of 1` |
| `uaf.c` | `Invalid read of size 4` … `inside a block of size N free'd` |
| `dbl.c` | `Invalid free() / delete / delete[] / realloc()` |
| `uninit.c` | `Conditional jump or move depends on uninitialised value(s)` |

**Answer 2 (the marking point).** **ASan does not detect the uninitialised read.** It catches the
leak, the use-after-free and the double free, but reading `malloc`'d memory before writing it passes
ASan silently and is reported by Valgrind.

Verified directly: a program deliberately inspecting a fresh `malloc(16)` block produced 17
`uninitialised value` reports under Valgrind and nothing under ASan.

**Answer 3.** The practical rule: **run ASan and UBSan during development** (≈2× slowdown, precise
stack and global diagnostics) and **Valgrind before submitting** (≈20–50× slowdown, but catches
uninitialised reads and needs no recompilation). Neither subsumes the other.

*Award 2 for the four messages, 1 for identifying the ASan gap, 1 for a defensible tooling rule.*

---

## Common Submission Problems

| Symptom | Cause | Action |
|---|---|---|
| Valgrind reports leaks in the student's own test harness | Test allocations never freed | −3; it is still a leak |
| `still reachable` at exit reported as an error | Misreading the categories | No deduction; explain the difference from *definitely lost* |
| Part 2 done with a small realloc only | Block never moved, so nothing observed | −2; require the large case |
| Amortised answer says "doubling is faster" | No analysis | −1; require the geometric sum |

---

*PROG 101 · Week 6 · Lab 6 Solutions · Instructor copy — do not distribute*
