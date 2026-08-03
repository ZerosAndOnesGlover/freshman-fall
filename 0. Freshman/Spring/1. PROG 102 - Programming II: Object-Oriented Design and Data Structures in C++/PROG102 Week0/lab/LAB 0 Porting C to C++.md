# PROG 102 · Lab 0
## Porting C to C++

**Week 0 · 2-hour lab session · 40 points**
**Deliverable:** `stack.cpp`, `RESULTS.md`. In-lab checkoff by your TA.

> **Labs are worth 20% of this course.** They are a graded component, not a completion gate. If you
> are also taking CS 102, do not carry its habits across — there, labs are ungraded and gated at 10 of
> 13. Here, a missed lab costs you marks directly.

---

## Purpose

Two things, one of which looks like admin and is not.

**First, confirm your toolchain works** — all six tools, on the machine you will actually use. You
need ThreadSanitizer in Week 10, which is a midterm week. Discovering a broken install then is
expensive; discovering it now costs twenty minutes.

**Second, port a working C program to C++** and observe precisely what changes. The answer is: less
than you expect at runtime, and one thing that matters enormously in maintenance.

---

## Part A — Toolchain (8 pts)

**A1.** *(4)* Confirm each tool runs and record its version:

| Tool | Command | Needed from |
| --- | --- | --- |
| g++ | `g++ --version` | Week 0 |
| gdb | `gdb --version` | Week 4 |
| valgrind | `valgrind --version` | Week 5 |
| AddressSanitizer | build with `-fsanitize=address` | Week 5 |
| ThreadSanitizer | build with `-fsanitize=thread` | Week 10 |
| perf | `perf --version` | Week 12 |

Paste the transcript into `RESULTS.md`. **If any tool is missing, say so explicitly** and raise it with
your TA in this session — that is what the session is for.

**A2.** *(2)* Confirm your compiler is in C++17 mode by printing `__cplusplus`:

```cpp
#include <cstdio>
int main() { std::printf("__cplusplus = %ld\n", __cplusplus); }
```

Built with `-std=c++17` this prints **`201703`**. Report yours.

**A3.** *(2)* Build one trivial program **both** ways and confirm both run:

```
g++ -std=c++17 -Wall -Wextra -pedantic -g -fsanitize=address,undefined t.cpp -o t
g++ -std=c++17 -O2 -Wall -Wextra t.cpp -o t
```

**State in one line which of the two you would use to time a program, and why.**

---

## Part B — The Port (16 pts)

You are given `stack.c`: a growable integer stack, in C, that works. **Do not modify it.**

```c
struct IntStack { int* data; int count; int cap; };

void stack_init(struct IntStack* s, int cap);
void stack_push(struct IntStack* s, int v);
int  stack_pop(struct IntStack* s);
int  stack_size(const struct IntStack* s);
int  stack_empty(const struct IntStack* s);
void stack_free(struct IntStack* s);
```

**B1.** *(10)* Write `stack.cpp`: the same data structure as a C++ class, with

- `data`, `count` and `cap` **private**;
- the constructor doing what `stack_init` did, taking capacity, marked `explicit`;
- the destructor doing what `stack_free` did;
- `push`, `pop`, `size`, `empty`, `capacity` as member functions;
- **`const` on exactly those members that do not modify the object**;
- the initializer list **in declaration order**.

`empty()` should return `bool`, not `int`.

> **Growth without `realloc`.** `realloc` is a C function that does not run constructors, and you
> should not use it on C++ objects. Allocate a new array, copy across, `delete[]` the old one. It is
> four lines. Week 3 shows you why `std::vector` is the real answer.

**B2.** *(3)* Your `main` must produce **byte-identical output** to the C version, and must contain
**no cleanup call of any kind.**

**B3.** *(3)* Build with the development line. It must be **clean** — no warnings — and run clean under
`-fsanitize=address,undefined`. Paste both transcripts.

---

## Part C — Prove Nothing Changed (8 pts)

**C1.** *(4)* Run both programs and diff the output:

```
diff <(./stack_c) <(./stack_cpp)
```

Paste the result. The reference output is:

```
size=5 cap=8
25 16 9 4 1
```

**C2.** *(4)* The growth policy doubles capacity from 2, so pushing five elements ends at capacity 8.

**Confirm your version reports `cap=8`.** If it reports something else, your growth condition or your
initial capacity differs — find out which, and say so. *(A version that reports `cap=5` is not wrong,
but it is not this program.)*

---

## Part D — What the Port Bought (8 pts)

**D1.** *(4)* Take the **C** version, delete the single line `stack_free(&s);`, and rebuild with
`-fsanitize=address`. Report what the sanitizer says.

The reference result is a leak of **32 bytes in 1 allocation** — the array had grown to capacity 8, so
$8 \times 4 = 32$ bytes.

**D2.** *(4)* Now attempt the same sabotage on your **C++** version: make it leak the buffer by
deleting one line of `main`.

**You will find there is no line to delete.** Answer both:

- **(a)** *(2)* Why not? Answer in one sentence, naming the mechanism.
- **(b)** *(2)* The C version's bug was *forgetting a call*. **What class of bug has the port
  eliminated, and what has it not?**

> For (b): the honest answer is not "C++ has no memory bugs". Your class still calls `new[]` and
> `delete[]` by hand, and Lecture 02 §6 showed one way it can still go badly wrong. Say what is now
> impossible and what is merely harder.

---

## Submission

- `stack.cpp` — compiles clean, runs clean, no cleanup call in `main`.
- `RESULTS.md` — the toolchain table, both transcripts, the diff, and D1/D2.
- **Your machine, OS and compiler version** at the top.

---

## Marking

| Part | Points | Focus |
| --- | --- | --- |
| A | 8 | Toolchain confirmed working, both build lines understood |
| B | 16 | A correct, `const`-marked, warning-free class |
| C | 8 | The port genuinely changed nothing observable |
| D | 8 | Naming what the destructor removed, and what it did not |
| **Total** | **40** | |

---

## Reference Transcript

g++ 13.3.0, x86-64 Linux, `-std=c++17`.

**C and C++ versions, both:**

```
size=5 cap=8
25 16 9 4 1
```

`diff` reports no difference.

**C version with `stack_free` removed:**

```
Direct leak of 32 byte(s) in 1 object(s) allocated from:
SUMMARY: AddressSanitizer: 32 byte(s) leaked in 1 allocation(s).
```

**C++ version:** clean under `-fsanitize=address,undefined`, with no cleanup call in `main`.

---

## What This Lab Is Really Showing

The two programs do the same work, at the same speed, with the same memory layout. The port bought
you **nothing at runtime** — and that is the point worth taking away, because it is what makes the one
real difference visible.

In C, the buffer is freed because `main` remembers to say so. In C++, it is freed because `IntStack`
*cannot exist* without eventually being destroyed. The correctness moved out of the caller and into
the type.

**That is the whole of RAII, and it is the reason this language is worth the trouble.** Every early
`return`, every exception in Week 9, every thread that unwinds in Week 10 — all of them run that
destructor, and none of them had to be thought about by whoever wrote them.

Week 5 makes it a discipline. This week, notice that it happened.

---

*PROG 102 · Week 0 · Lab 0 · © CSE Department*
