# PROG 101 · Programming I: Structured Programming in C
## Week 6 · Lecture 3: Valgrind and Building a Dynamic Array

---

## Lecture Goals

By the end of this lecture you can:

- Read Valgrind's output and act on each category of report
- Choose between Valgrind and the sanitizers for a given symptom
- Build a growable array with correct failure handling
- Explain why doubling the capacity gives amortised O(1) append

---

## 1. Valgrind

Every bug from Lecture 2 is invisible at compile time. Valgrind finds them at run time by simulating
your program and tracking every byte.

```bash
gcc -Wall -Wextra -Werror -pedantic -std=c11 -g -O0 prog.c -o prog
valgrind --leak-check=full --show-leak-kinds=all --error-exitcode=1 ./prog
```

`-g` is essential — without it you get addresses instead of line numbers. `-O0` keeps the line
numbers honest.

### What it reports

| Message | Meaning |
|---|---|
| `Invalid read of size N` | Reading outside an allocation, or after `free` |
| `Invalid write of size N` | Writing outside an allocation — this one corrupts data |
| `Conditional jump or move depends on uninitialised value(s)` | Using memory you never wrote |
| `Invalid free() / delete` | Double free, or freeing a non-allocated address |
| `definitely lost` | A leak: no pointer to the block survives |
| `still reachable` | Not freed at exit, but a pointer still existed — usually benign |

**Aim for "0 errors from 0 contexts" and zero `definitely lost`.** `still reachable` at exit is
often acceptable (globals, one-time caches), but understand each one rather than ignoring the
category.

### A worked example

Reading `malloc`'d memory before writing it produces:

```
Conditional jump or move depends on uninitialised value(s)
Use --track-origins=yes to see where uninitialised values come from
```

Verified: a program that deliberately inspects a fresh `malloc(16)` block generates exactly this, 17
times. Add `--track-origins=yes` and Valgrind names the allocation that produced the value — at some
cost in speed, so it is a second-pass flag rather than a default.

### Valgrind or the sanitizers?

They overlap; neither subsumes the other.

| | Valgrind | ASan / UBSan |
|---|---|---|
| Needs recompilation | No | Yes (`-fsanitize=…`) |
| Speed | ~20–50× slower | ~2× slower |
| Heap overflow | ✅ | ✅ |
| Stack / global overflow | Weak | ✅ Strong |
| **Uninitialised reads** | ✅ | ❌ **Not detected** |
| Leaks | ✅ Detailed | ✅ Basic |
| Undefined behaviour (overflow, shifts) | ❌ | ✅ (UBSan) |

**The uninitialised-read row is the reason to keep using Valgrind** even though ASan is faster and
usually more precise. Run ASan+UBSan during development for speed, and Valgrind before you submit.

---

## 2. Building a Dynamic Array

Everything from Weeks 5 and 6 comes together here. The goal: an array that grows as you append.

```c
typedef struct {
    int   *data;
    size_t len;      /* elements in use   */
    size_t cap;      /* elements allocated */
} Vec;
```

Three fields, and the two size fields are both necessary: `len` is what you have, `cap` is what you
can hold before growing. Recall from Lecture 1 that the allocator will not tell you either.

### Init and destroy

```c
void vec_init(Vec *v)
{
    v->data = NULL;      /* realloc(NULL, n) behaves as malloc -- Lecture 2 */
    v->len = v->cap = 0;
}

void vec_free(Vec *v)
{
    free(v->data);
    v->data = NULL;      /* Lecture 2's habit */
    v->len = v->cap = 0;
}
```

Starting from `NULL` means `vec_push` needs no special case for the first insertion.

### Growth

```c
static int vec_grow(Vec *v)
{
    size_t ncap = v->cap ? v->cap * 2 : 4;
    if (ncap > SIZE_MAX / sizeof *v->data) return -1;   /* overflow guard */

    int *tmp = realloc(v->data, ncap * sizeof *v->data);
    if (!tmp) return -1;                                 /* v->data still valid */

    v->data = tmp;
    v->cap  = ncap;
    return 0;
}

int vec_push(Vec *v, int value)
{
    if (v->len == v->cap && vec_grow(v) != 0) return -1;
    v->data[v->len++] = value;
    return 0;
}
```

Verified — pushing 20 values grows the capacity **4 → 8 → 16 → 32**, with all contents preserved and
Valgrind reporting no leaks and no errors.

Three details carry the correctness:

- **The temporary `tmp`** — never `v->data = realloc(v->data, …)` (Lecture 2). Verified: forcing a
  `realloc` failure leaves the caller's pointer, data, and capacity untouched.
- **The overflow guard** — `ncap * sizeof *v->data` could wrap for absurd capacities, exactly as in
  Lecture 1's `xmalloc_array`.
- **`vec_push` returns a status** and the caller must check it. A `void` push that silently drops
  values on allocation failure is a bug generator.

### Accessing

```c
int *vec_at(Vec *v, size_t i)
{
    return (i < v->len) ? &v->data[i] : NULL;
}
```

C will not bounds-check for you (Week 4), so if you want the check, write it. Returning `NULL` for
out-of-range forces the caller to think about it; an `assert(i < v->len)` is the alternative when the
index is supposed to be provably valid.

> **Pointers into the array do not survive a push.** `realloc` may move the block (Lecture 2), so any
> `int *` you obtained from `vec_at` dangles after the next `vec_push` that grows. **Keep indices,
> not pointers**, across mutations. This is the same rule that makes C++ iterator invalidation a
> famous hazard.

---

## 3. Why Doubling

Growing by doubling gives **amortised O(1)** append. Growing by a constant does not.

**Doubling.** To reach n elements the capacities are 4, 8, 16, …, n. Each growth copies the current
contents, so the total copying is

```
4 + 8 + 16 + … + n  <  2n
```

a geometric series bounded by 2n. Across n pushes that is O(n) total work, so **O(1) per push on
average** — even though individual pushes that trigger a reallocation cost O(n).

**Constant increment** (`cap += 4`). Growth happens n/4 times, and the i-th copies about 4i
elements:

```
4 + 8 + 12 + … + n  ≈  n²/8
```

which is **Θ(n²)** total, or Θ(n) per push. For n = 100,000 that is the difference between instant
and unusable.

This is the same arithmetic as the string-building cost you met in Week 4, and the same reason
`s += c` in a loop is quadratic in Python. **Geometric growth is the general answer whenever a
structure must grow by an unknown amount.**

*(The growth factor need not be 2. Some implementations use 1.5 to allow reusing freed blocks. Any
factor > 1 gives amortised O(1); the constant differs.)*

---

## 4. Summary

| Idea | Takeaway |
|---|---|
| Valgrind needs `-g -O0` | Otherwise you get addresses, not lines |
| `definitely lost` | A real leak; `still reachable` is usually benign |
| `--track-origins=yes` | Names where an uninitialised value came from; slower |
| **Uninitialised reads** | Valgrind finds them; **ASan does not** — run both |
| `Vec { data, len, cap }` | Both sizes are needed; the allocator tells you neither |
| Start `data = NULL` | `realloc(NULL, n)` acts as `malloc`, so no special first case |
| Grow via a temporary | Verified: on failure the caller's pointer, data and cap survive |
| Guard the multiplication | `ncap * sizeof *data` can wrap |
| `vec_push` returns a status | Silently dropping on failure is a bug generator |
| Pointers dangle after growth | Keep **indices** across mutations |
| Doubling ⟹ amortised O(1) | Total copying < 2n |
| Constant increment ⟹ Θ(n²) | The same trap as quadratic string building |

---

## Practice Exercises

Attempt each before reading the answers.

**1. (Trace.)** A `Vec` starts empty. List every capacity after 30 pushes, the number of `realloc`
calls, and the total number of elements copied.

**2. (Explain.)** Why must `vec_grow` use a temporary rather than
`v->data = realloc(v->data, …)`? Describe the exact state after a failure in each version.

**3. (Fix.)** Three bugs.

```c
int vec_push(Vec *v, int value)
{
    if (v->len == v->cap) {
        v->cap *= 2;
        v->data = realloc(v->data, v->cap * sizeof(int));
    }
    v->data[v->len++] = value;
    return 0;
}
```

**4. (Stretch.)** Add `int vec_remove(Vec *v, size_t i)` that removes element `i`, preserving order,
in O(n). Then explain what should happen to `cap`, and why shrinking on every removal is a mistake.

### Answers

**1.** Capacities: **4, 8, 16, 32.**

| Push | Trigger | New capacity | Elements copied |
|---|---|---|---|
| 1 | `cap == 0` | 4 | 0 (`realloc(NULL, …)`) |
| 5 | `len == cap == 4` | 8 | 4 |
| 9 | `len == cap == 8` | 16 | 8 |
| 17 | `len == cap == 16` | 32 | 16 |

**4 `realloc` calls**, and **28 elements copied** in total (0 + 4 + 8 + 16). Final state after 30
pushes: `len = 30`, `cap = 32`.

Note 28 < 2 × 30 = 60, consistent with the geometric bound in §3. Verified at 20 pushes: capacities
4, 8, 16, 32 with contents intact.

**2.** Because `realloc` returns NULL on failure **while leaving the original block allocated**.

**With a temporary:** `tmp` is NULL, `v->data` still points at the original block, `v->len` and
`v->cap` are unchanged. The vector is fully intact and usable; `vec_push` returns −1 and the caller
can retry, degrade, or exit cleanly. Verified: forcing a failure left the four stored values readable
and the pointer unchanged.

**Without a temporary:** `v->data` is overwritten with NULL. The original block is still allocated
but **nothing points to it** — an unrecoverable leak — and the vector's data is gone. Worse, `v->cap`
may already have been increased, so the structure now claims capacity it does not have, and the next
`vec_push` dereferences NULL.

One failure produces a leak, data loss, and a corrupted invariant. The temporary costs one line.

**3.**

- **`v->cap *= 2` is 0 when the vector is empty.** Starting from `cap == 0`, doubling gives 0, so
  `realloc(…, 0)` is called and `v->data[0]` writes out of bounds. → `v->cap ? v->cap * 2 : 4`.
- **`realloc`'s result is assigned straight back** — the Exercise 2 bug. → use a temporary and return
  −1 on failure.
- **The return value is not checked at all**, so the function returns 0 (success) even when the
  allocation failed, and then writes through a NULL pointer.

*Also worth flagging:* `sizeof(int)` should be `sizeof *v->data`, so the code survives a change of
element type; and there is no guard against `ncap * sizeof` overflowing.

```c
int vec_push(Vec *v, int value)
{
    if (v->len == v->cap) {
        size_t ncap = v->cap ? v->cap * 2 : 4;
        if (ncap > SIZE_MAX / sizeof *v->data) return -1;
        int *tmp = realloc(v->data, ncap * sizeof *v->data);
        if (!tmp) return -1;
        v->data = tmp;
        v->cap  = ncap;
    }
    v->data[v->len++] = value;
    return 0;
}
```

**4.**

```c
int vec_remove(Vec *v, size_t i)
{
    if (i >= v->len) return -1;
    memmove(&v->data[i], &v->data[i + 1], (v->len - i - 1) * sizeof *v->data);
    v->len--;
    return 0;
}
```

**`memmove`, not `memcpy`.** The source and destination overlap, and `memcpy` has undefined behaviour
when they do. This is a real distinction, not pedantry — `memcpy` may copy in an order that corrupts
overlapping data.

The count `v->len - i - 1` is the number of elements *after* `i`. When `i` is the last element that
is 0, and `memmove` with size 0 is well-defined, so no special case is needed.

**What should happen to `cap`: nothing.** Leave the capacity alone.

**Why shrinking on every removal is a mistake.** It destroys the amortised guarantee. Consider a
vector at exactly the shrink threshold, with the caller alternating push and remove:

- push → capacity is full → grow, copying n elements
- remove → now below threshold → shrink, copying n elements
- push → grow again…

Every single operation costs O(n), so a sequence of n operations is **Θ(n²)** — the very cost that
doubling was introduced to avoid. This is called **thrashing**, and it is why real implementations
either never shrink automatically or use **hysteresis**: grow at 100% full, but shrink only when
usage drops below 25%, and shrink to half. The gap between the two thresholds means a single
operation can never trigger the opposite resize.

*Full marks require identifying the alternating-operation worst case*, not merely saying "shrinking
is slow." And the practical answer many libraries choose — expose an explicit `shrink_to_fit` and let
the caller decide — is worth credit too.

---

## Reading

- **Valgrind Quick Start Guide** — 15 minutes, and it covers everything you need
- **`man 3 memmove`** — and note the explicit contrast with `memcpy`
- **K&R, §8.7** — a complete storage allocator in about a page
- **CLRS, §17.4** — the amortised analysis of dynamic tables, formally

---

*PROG 101 · Week 6 · Lecture 3 · © CSE Department*
