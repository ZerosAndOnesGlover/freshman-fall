# PROG 101 · Lab 5 Solutions (Instructor)
## Pointer Mechanics and Write-Back

All observations below were produced by running the lab's own programs on the reference machine
(x86-64, GCC 13, glibc 2.39). Addresses vary between runs; **offsets and sizes do not**.

---

## Part 1: Pointer Mechanics (6 pts)

### Expected observations

| Quantity | Value |
|---|---|
| `sizeof(char*)`, `sizeof(int*)`, `sizeof(double*)` | **8** each |
| `int *p; p+1` | **+4** bytes |
| `char *p; p+1` | **+1** byte |
| `double *p; p+1` | **+8** bytes |
| `&a` vs `&a[0]` for `int a[10]` | **same address** |
| `a+1` | **+4** bytes |
| `&a+1` | **+40** bytes |
| `sizeof a` in `main` | **40** |
| `sizeof a` in `f(int a[10])` | **8** |

### The four `const` combinations

Verified against the compiler — these are the results students must obtain:

| Written | `p = &other;` | `*p = 5;` |
|---|---|---|
| `int *p` | ✅ | ✅ |
| `const int *p` | ✅ | ❌ rejected |
| `int *const p` | ❌ rejected | ✅ |
| `const int *const p` | ❌ | ❌ |

**Marking.** 2 pts for the size/arithmetic table, 2 pts for `&a` vs `&a+1` **with the type
explanation**, 2 pts for all four `const` results with correct predictions recorded *before*
compiling.

The discriminating answer is `&a + 1`. A student reporting +4 has treated `&a` as `int *`; it is
`int (*)[10]`, so `+1` moves a whole array. Award the mark only with the type named.

---

## Part 2: Pass-by-Pointer Functions (6 pts)

Standard shape:

```c
void swap(int *a, int *b) { int t = *a; *a = *b; *b = t; }

int divide(int a, int b, int *remainder)
{
    if (b == 0) return -1;          /* status via return value */
    *remainder = a % b;             /* second result via pointer */
    return a / b;
}

void min_max(const int *a, size_t n, int *lo, int *hi)
{
    if (n == 0) return;             /* leave outputs untouched -- document this */
    *lo = *hi = a[0];
    for (size_t i = 1; i < n; i++) {
        if (a[i] < *lo) *lo = a[i];
        if (a[i] > *hi) *hi = a[i];
    }
}
```

**Marking notes.**

- **`const` on read-only parameters** is required, not optional — the lab's signatures show it.
  −1 if `min_max` takes a non-const `int *`.
- **The `n == 0` case must be handled and documented.** Leaving `*lo`/`*hi` untouched is fine;
  writing garbage is not; and a version that reads `a[0]` unconditionally is an out-of-bounds read.
- **Watch for `swap` written with a temporary in the caller** — that is not pass-by-pointer, and it
  misses the exercise.

---

## Part 4: The Pointer Bug Gallery (8 pts)

### 4A — dangling return (2 pts)

**Verified result:** `make()` returns `(nil)` at **both** `-O0` and `-O2`.

This surprises nearly everyone, and the sameness is the point. Because returning the address of a
local is undefined behaviour, GCC is entitled to compile the function to whatever it likes — and what
it chose was to discard the address entirely and return a null pointer, even with optimisation off.

**The required insight:** UB is not "you get a stale address that happens to still work." The
*compiler*, not the hardware, decides what the program means, and it may decide your code has no
meaning at all.

Under ASan (with the dereference restored):

```
ERROR: AddressSanitizer: SEGV on unknown address 0x000000000000
```

*Award 1 pt for recording both values, 1 pt for explaining the compiler's entitlement. A student who
predicted "a stale address" and then recorded `(nil)` honestly should get full marks — the prediction
being wrong is the lesson.*

### 4B — off the front (2 pts)

The loop prints `5 4 3 2 1`, which is correct output from an undefined program.

On the final iteration `p` holds `a`, and `p--` forms `a - 1`. C permits pointers within an array
and **one past the end**, but grants no allowance before the start. The pointer is never
dereferenced, yet merely *forming* it is undefined, and so is the subsequent `p >= a` comparison.

It "works" on flat address spaces. It need not on a segmented architecture, and an optimiser that
assumes pointers stay in range may transform the loop.

**Correct rewrite:**

```c
for (int *p = a + 5; p-- != a; ) printf("%d ", *p);
```

Test-then-decrement never forms `a - 1`. *(1 pt for identifying that no dereference is required for
UB; 1 pt for a correct rewrite.)*

### 4C — the decayed `sizeof` (2 pts)

**Verified:** prints **2**, and GCC emits exactly one warning:

```
warning: 'sizeof' on array function parameter 'a' will return size of 'int *'
         [-Wsizeof-array-argument]
```

2 is `sizeof(int *) / sizeof(int)` = 8/4. Students who predicted 10 have made the mistake the
warning exists to catch. *(1 pt for the value, 1 pt for the warning text.)*

### 4D — unchecked search (1 pt)

**Verified Valgrind output:**

```
Invalid read of size 1
 Address 0x0 is not stack'd, malloc'd or (recently) free'd
```

`strchr` returned NULL because `'z'` is absent; `*p` dereferenced it. The fix is to test before
dereferencing.

### 4E — writing through `const` (1 pt)

The cast silences the compiler and changes nothing about the object.

`const int v = 5;` may be placed in **read-only memory**, so the write may fault. Even where it does
not, the compiler is entitled to assume a `const` object never changes and may have propagated the
value 5 into later expressions — so subsequent reads of `v` can legitimately still yield 5 after the
"successful" write.

**What the cast did:** it removed the compiler's *objection*, not the object's constness. Casting
away `const` is only defined when the underlying object was not itself declared `const` — for
example, a `const int *` parameter pointing at a non-const variable.

*Full marks require distinguishing "the pointer's qualification" from "the object's qualification."*

---

## Common Submission Problems

| Symptom | Cause | Action |
|---|---|---|
| Predictions written after running | Defeats the exercise | −2; the lab asks for predictions first |
| `&a + 1` reported as +4 | Treated `&a` as `int *` | −1, explain the type |
| 4A explained as "stale memory" | The common misconception | Correct it in feedback; do not deduct if the value was recorded honestly |
| `%p` used without `(void *)` | UB, and `-pedantic` catches it | −1 |
| No `const` on read-only parameters | Missed Lecture 3 | −1 per function |

---

*PROG 101 · Week 5 · Lab 5 Solutions · Instructor copy — do not distribute*
