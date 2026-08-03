# PROG 102 · Lab 1 — Solutions and Checkoff Notes
## Debugging Copy Semantics

**INSTRUCTOR / TA COPY — not for distribution**

---

## Before the Session

**Distribute `roster.hpp` and `roster_demo.cpp` unmodified.** The four bugs are ordered so that fixing
one exposes the next, and that ordering is the pedagogy. Students who "fix everything at once" from
reading the code have skipped the lab — redirect them to Part A and require the transcripts.

**Open by compiling it in front of the room:**

```
g++ -std=c++17 -Wall -Wextra -pedantic -c roster_demo.cpp -o /dev/null
```

Nothing. Not one warning. **Say out loud that this file contains four bugs, three of which will corrupt
memory**, and let that sit before anyone starts.

**Timing:** Part A takes about 50 minutes and is the substance. Part B is 30. Reserve the last 20 for
C and D — students consistently over-run on B2's growth code, which is not where the marks are.

---

## The Four Bugs

| # | Bug | Found by | Sanitizer verdict |
| --- | --- | --- | --- |
| 1 | `delete names` should be `delete[] names` | A1 | `alloc-dealloc-mismatch` |
| 2 | Destructor never frees the individual strings | A2 | `10 byte(s) leaked in 2 allocation(s)` |
| 3 | `add` never checks `count` against `cap` | A3 | `heap-buffer-overflow`, WRITE of size 8 |
| 4 | No copy constructor / copy assignment | A4 | `attempting double-free` |

**Three of the four are one mistake** — `Roster` owns things and does not say so. Only bug 3 is a
classic C bounds error. Make this point at the end, not the start.

---

## Part A — Diagnose (14)

### A1 (3)

```
ERROR: AddressSanitizer: alloc-dealloc-mismatch (operator new [] vs operator delete)
```

The disagreeing functions are **`new[]`** in the constructor and **`delete`** in the destructor. The
rule: `new` pairs with `delete`, `new[]` pairs with `delete[]`, and mixing them is undefined behaviour.

*Marking: 1 the error, 1 naming both functions, 1 the rule.*

### A2 (3)

```
Direct leak of 6 byte(s) in 1 object(s)
Direct leak of 4 byte(s) in 1 object(s)
SUMMARY: AddressSanitizer: 10 byte(s) leaked in 2 allocation(s).
```

**10 = 6 + 4 = `"grace"` + NUL, and `"ada"` + NUL.**

*Marking: 2 the transcript, 1 accounting for the bytes. **The byte arithmetic is the assessed part** —
it demonstrates they understand the strings are separate allocations from the array.*

### A3 (4)

```
ERROR: AddressSanitizer: heap-buffer-overflow
WRITE of size 8
    in Roster::add(char const*)  roster.hpp:17
```

The constructor promised an array of exactly `cap` pointers. `add` writes at index `count` without
ever comparing it to `cap`. **The write is 8 bytes because it is writing a `char*`, not a character** —
worth pointing out; students often expect 1.

*Marking: 2 transcript, 2 the sentence. Full marks require naming `cap` as the promise that was broken.*

### A4 (4)

```
a=0x502000000030  b=0x502000000030  same=YES
ERROR: AddressSanitizer: attempting double-free
```

Missing:

```cpp
Roster(const Roster&);
Roster& operator=(const Roster&);
```

*Marking: 2 the addresses and equality, 2 naming both functions with signatures. **A student naming
only the copy constructor gets 1** — assignment is a separate function and is separately missing.*

---

## Part B — Repair (14)

### B1 (4)

```cpp
~Roster() {
    for (int i = 0; i < count; ++i) delete[] names[i];
    delete[] names;
}
```

**Order matters**: free the strings before the array holding their pointers. Reversing it is a
use-after-free, and ASan catches it — a student who hits this has learned something and should be told
so.

*Marking: 2 `delete[]` on the array, 2 the loop. Deduct 1 for looping to `cap` rather than `count` —
only the first `count` slots were ever written, so the rest are uninitialised pointers.*

### B2 (3)

Allocate a new array, copy the pointers across, `delete[]` the old array. **Do not deep-copy the
strings here** — the pointers are being moved, not duplicated.

*Marking: 2 correct growth, 1 for not using `realloc`. A student who deep-copies the strings during
growth has a leak; deduct 1 and point at ASan.*

### B3 (7)

```cpp
Roster(const Roster& o) : names(new char*[o.cap]), count(o.count), cap(o.cap) {
    for (int i = 0; i < count; ++i) {
        names[i] = new char[std::strlen(o.names[i]) + 1];
        std::strcpy(names[i], o.names[i]);
    }
}
void swap(Roster& o) noexcept {
    std::swap(names, o.names); std::swap(count, o.count); std::swap(cap, o.cap);
}
Roster& operator=(Roster o) { swap(o); return *this; }
```

Reference output from the repaired class:

```
a: size=3 cap=4  ada grace alan
deep? a[0]=0x502000000030 b[0]=0x502000000090 same=no
c: size=3 alan
self-assign ok: ada
```

Sanitizer-clean, exit 0.

*Marking: 3 deep copy constructor (the inner string loop is the point — a copy constructor that copies
only the pointer array is still bug 4), 2 `swap` covering **all three** members and `noexcept`, 2
by-value `operator=` with no guard.*

**Grep the submission for `== &`.** A leftover self-assignment guard means copy-swap was not understood.

---

## Part C — Count the Copies (8)

### C1 (5)

| Case | ctor | copy | assign | dtor |
| --- | --- | --- | --- | --- |
| (i) `Roster b = a;` | 0 | 1 | 0 | 0 |
| (ii) `c = a;` | 0 | 1 | 1 | 1 |
| (iii) `show(Roster r)` — by value | 0 | 1 | 0 | 1 |
| (iv) `show2(const Roster&)` | 0 | 0 | 0 | 0 |

Row (ii) shows copy-swap's shape clearly: **one copy** (the by-value parameter), one assignment call,
one destruction (the parameter, carrying the old state away).

*Marking: 1 per row, plus 1 for a correct harness.*

### C2 (3)

(iii) costs **one full deep copy** — an array allocation plus one allocation and `strcpy` per name.
(iv) costs **nothing**.

At ten thousand names, (iii) is **10,001 heap allocations and ten thousand string copies, per call**.
(iv) remains zero.

*Marking: 1 the difference, 2 the scaled cost. **Require a number**, not "it would be slower".*

---

## Part D — What the Tools Did (4)

### D1 (2)

**`-Wall -Wextra -pedantic` reported zero of the four.**

`-Weffc++` on the original reports:

```
warning: 'class Roster' has pointer data members [-Weffc++]
warning:   but does not declare 'Roster(const Roster&)' [-Weffc++]
warning:   or 'operator=(const Roster&)' [-Weffc++]
```

**That is two of the four** — bugs 4 and its assignment counterpart. It does **not** catch the
`delete`/`delete[]` mismatch or the missing bounds check.

*Marking: 1 for "zero", 1 for the `-Weffc++` output. **A student who claims `-Weffc++` catches all four
has not run it.***

### D2 (2)

A clean `-Wall -Wextra` build is evidence that **the code is well-formed and free of the specific
patterns GCC has been taught to recognise as suspicious**. It is not evidence of correctness, and in
particular it says nothing about ownership, lifetime or aliasing — which is where every bug in this
lab lived.

*Marking: 2. **"It means nothing" scores 1**, not 0 — it is an over-correction, but the sheet warns
against it, so mark it down rather than out. The target answer distinguishes *well-formed* from
*correct*.*

---

## Checkoff Checklist

1. Part A transcripts present **in order**, one bug at a time.
2. Repaired destructor frees strings **before** the array.
3. Copy constructor deep-copies the **strings**, not just the pointer array.
4. No `== &` anywhere in the class.
5. `a = a` runs sanitizer-clean.
6. D1 reports **zero** for `-Wall -Wextra`.

---

## Marking Summary

| Part | Points |
| --- | --- |
| A | 14 |
| B | 14 |
| C | 8 |
| D | 4 |
| **Total** | **40** |

---

## Note for the Lab

Close with the observation that the four bugs are really two:

> **One of these is a C bug** — the missing bounds check — and you were all trained to find it last
> semester. **The other three are the same C++ bug wearing three hats:** this class owns something and
> never said so.

Then the honest part. `-Wall -Wextra -pedantic`, which this course requires on every submission,
**caught none of them**. `-Weffc++` caught half. AddressSanitizer caught all four, one at a time, and
told you the line.

That is the real lesson of the session, and it is not "use more flags". It is that **the compiler
checks what your program says, and the sanitizer checks what it does** — and ownership bugs are
invisible to the first because C++ has no syntax that distinguishes an owning pointer from a
non-owning one.

**Week 5 does.** `unique_ptr` is that missing syntax, and after this lab students will understand why
it exists rather than merely how to spell it.

---

*PROG 102 · Week 1 · Lab 1 Solutions · © CSE Department*
