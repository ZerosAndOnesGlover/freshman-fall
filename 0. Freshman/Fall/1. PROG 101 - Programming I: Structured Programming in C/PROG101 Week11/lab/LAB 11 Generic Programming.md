# PROG 101 · Programming I: Structured Programming in C
## Week 11 · Lab 11: Generic Programming in C

**Duration:** 2 hours · **Points:** 20 · **Room:** BH 215
**Lab session:** Monday of Week 12 — sat after this week's Tue–Thu lectures, and covers Week 11.

**Build with:** `gcc -Wall -Wextra -Werror -pedantic -std=c11 -g`
**Check with:** `valgrind --leak-check=full --error-exitcode=1`

---

## Overview

C has no templates and no generics. What it has is `void *` and function pointers — and this lab
shows how far that gets you. You will write comparators that survive inputs the naive version
cannot, build a container that holds any type, and meet the cost of the bargain: no type checking
whatsoever.

---

## Part 1: The Comparator That Fails (5 pts)

### 1A: Demonstrate the bug

```c
static int cmp_bad(const void *a, const void *b)
{ return *(const int *)a - *(const int *)b; }

static int cmp_ok(const void *a, const void *b)
{ int l = *(const int *)a, r = *(const int *)b; return (l > r) - (l < r); }
```

Sort `{INT_MAX, -2}` with each. **Record in `answers.md`:**

1. The resulting array in both cases.
2. Rebuild with `-fsanitize=undefined` and paste UBSan's report for the bad version.
3. Why does `cmp_bad` pass every test anyone writes casually? State the exact condition under which
   it is correct.

### 1B: Sorting strings

Sort `{"pear","apple","fig"}` with `qsort`. Get the comparator's indirection right.

**Record:** the type `qsort` actually passes to the comparator, and what happens if you pass it
straight to `strcmp`.

---

## Part 2: A Generic Vector (8 pts)

Build `gvec.h` / `gvec.c` — a dynamic array holding elements of **any** type.

```c
typedef void (*FreeFn)(void *elem);

typedef struct {
    void  *data;
    size_t len, cap, elem_size;
    FreeFn destroy;          /* NULL for plain data */
} GVec;

int   gvec_init(GVec *v, size_t elem_size, FreeFn destroy);
void *gvec_at  (const GVec *v, size_t i);
int   gvec_push(GVec *v, const void *elem);      /* copies elem_size bytes */
void  gvec_free(GVec *v);
```

### Requirements

1. `gvec_push` **copies** `elem_size` bytes. It must never store the caller's pointer.
2. Growth doubles from 4, with an overflow guard on `ncap * elem_size`.
3. Use a temporary for `realloc`; failure must leave the vector usable.
4. `gvec_free` calls `destroy` on **every** element when it is non-NULL, then frees the buffer.
5. Test with **three** element types: `int`, `double`, and a struct that owns a `malloc`'d string.
6. Valgrind-clean, including the owning-struct case.

**In `answers.md`:** explain why `gvec_at` returns `void *` rather than the element, and what the
caller must do with it.

---

## Part 3: Callbacks with Context (4 pts)

Add to your vector:

```c
typedef void (*EachFn)(void *elem, void *ctx);
void gvec_each(const GVec *v, EachFn f, void *ctx);
```

1. Use it to sum a vector of `int` into a `long` held in `ctx`. *(2 pts)*
2. Use it to print a vector of structs, passing a `FILE *` through `ctx`. *(1 pt)*
3. **In `answers.md`:** what would you be forced to do if `gvec_each` had no `ctx` parameter, and why
   is that worse? *(1 pt)*

---

## Part 4: The Cost of the Bargain (3 pts)

Deliberately make each of these mistakes, observe what happens, and record it:

1. Push an `int` into a `GVec` initialised for `double`. Does it compile? Does it warn? What does the
   data look like afterwards?
2. Call `gvec_at` and assign the result to the wrong pointer type.
3. Initialise a vector of owning structs with `destroy = NULL` and run Valgrind.

**In `answers.md`:** summarise in three sentences what C's generic-programming bargain costs you, and
what a language with templates or generics buys back.

---

## Deliverables

- `gvec.h`, `gvec.c`, `test_gvec.c`, and the Part 1 and Part 4 programs
- `answers.md` with every recorded observation
- A `Makefile` building everything with the required flags

## Grading

| Component | Points |
|---|---|
| Part 1: both comparators, UBSan report, correctness condition | 5 |
| Part 2: generic vector correct and Valgrind-clean on all three types | 8 |
| Part 3: callbacks with context working; the no-`ctx` analysis | 4 |
| Part 4: three failures observed; the bargain summarised | 3 |
| **Total** | **20** |

---

*PROG 101 · Week 11 · Lab 11 · © CSE Department*
