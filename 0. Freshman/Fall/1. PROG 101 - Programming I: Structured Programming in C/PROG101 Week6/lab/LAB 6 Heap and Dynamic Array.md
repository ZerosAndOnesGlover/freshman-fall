# PROG 101 · Programming I: Structured Programming in C
## Week 6 · Lab 6: The Heap and a Dynamic Array

**Duration:** 2 hours · **Points:** 20 · **Room:** BH 215
**Date:** Monday 9 November 2026 · 15:00–16:50 · Lab Section (Week 7) — covers Week 6 (Lectures 01–03)

**Build with:** `gcc -Wall -Wextra -Werror -pedantic -std=c11 -g`
**Check with:** `valgrind --leak-check=full --show-leak-kinds=all --error-exitcode=1`

---

## Overview

This lab is where memory management becomes real. You will map a running process's address space,
watch `realloc` move a block out from under a stale pointer, build a growable array with correct
failure handling, and read Valgrind's output until it is boring.

**Everything you submit must be Valgrind-clean.** That is the standard from this week onward.

---

## Part 1: Mapping the Address Space (4 pts)

Create `where.c` that prints the address of one object from each storage class:

```c
#include <stdio.h>
#include <stdlib.h>

static int global_var = 1;

int main(void)
{
    static int static_local = 2;
    int        stack_local  = 3;
    int       *heap_ptr     = malloc(sizeof *heap_ptr);
    const char *literal     = "text";

    printf("  literal      %p\n", (void *)literal);
    printf("  global       %p\n", (void *)&global_var);
    printf("  static local %p\n", (void *)&static_local);
    printf("  heap         %p\n", (void *)heap_ptr);
    printf("  stack        %p\n", (void *)&stack_local);
    free(heap_ptr);
    return 0;
}
```

**Record in `answers.md`:**

1. Sort the five addresses. Which regions sit low, which high?
2. Allocate a **second** heap block and print it. Does the heap grow up or down?
3. Call a function that prints the address of *its* local. Does the stack grow up or down?
4. `static_local` and `stack_local` are both declared inside `main`. Why are their addresses so far
   apart? *(This is Week 3's scope-versus-lifetime distinction, made visible.)*

---

## Part 2: Watching `realloc` Move (4 pts)

```c
int *a = malloc(4 * sizeof *a);
for (int i = 0; i < 4; i++) a[i] = i;
int *alias = a;                       /* a second pointer to the same block */

printf("before: a=%p alias=%p\n", (void *)a, (void *)alias);
int *tmp = realloc(a, 1024 * 1024 * sizeof *tmp);
if (tmp) a = tmp;
printf("after:  a=%p alias=%p\n", (void *)a, (void *)alias);
```

**Record in `answers.md`:**

1. Did the block move? (Try both a small and a very large new size.)
2. If it moved, what is `alias` now? Name the defect.
3. Run with `-fsanitize=address` and dereference `alias` afterwards. Paste the report.
4. State the rule this demonstrates about holding pointers across a reallocation, and what you
   should hold instead.

---

## Part 3: Dynamic Array (8 pts)

Implement the complete `DynArray` from Lecture 3.

### Files Required

```
dynarray.h    — header (provided skeleton below — complete it)
dynarray.c    — implementation (you write from scratch)
test_dynarray.c — test suite (you write)
```

### `dynarray.h` (complete this)

```c
#ifndef DYNARRAY_H
#define DYNARRAY_H

#include <stddef.h>
#include <stdbool.h>

typedef struct {
    int    *data;
    size_t  size;
    size_t  capacity;
} DynArray;

void   da_init(DynArray *da);
void   da_free(DynArray *da);

void   da_push(DynArray *da, int value);
int    da_pop(DynArray *da);

int    da_get(const DynArray *da, size_t i);
void   da_set(DynArray *da, size_t i, int value);

/* Insert value at index i, shifting elements right.
 * Precondition: i <= da->size */
void   da_insert(DynArray *da, size_t i, int value);

/* Remove element at index i, shifting elements left.
 * Precondition: i < da->size */
void   da_remove(DynArray *da, size_t i);

/* Return the index of the first element equal to value, or -1. */
int    da_find(const DynArray *da, int value);

/* Remove all elements (size → 0) without freeing memory. */
void   da_clear(DynArray *da);

/* Print all elements: [a, b, c, ...] */
void   da_print(const DynArray *da);

/* Return true if da1 and da2 contain the same elements in the same order. */
bool   da_equal(const DynArray *da1, const DynArray *da2);

/* Sort elements in ascending order with insertion sort (Week 4) -- qsort needs a
 * comparator function pointer, which is Week 11. */
void   da_sort(DynArray *da);

#endif
```

### Implementation Requirements

- Initial capacity: 8
- Growth factor: 2× when full
- Never shrink capacity on `pop` or `remove` (shrinking is an optional extension)
- All functions that accept an index must `assert` it is in bounds
- `da_free` must set `data = NULL`, `size = 0`, `capacity = 0` after freeing
- Clean Valgrind: `valgrind --leak-check=full ./test_dynarray` → 0 errors, 0 leaks

### `test_dynarray.c` — Required Test Cases

Write tests that cover:

```c
/* Growth behavior */
void test_growth(void) {
    DynArray da;
    da_init(&da);
    /* Push 100 elements and verify:
     *   1. Every element is retrievable with da_get
     *   2. da.size is correct after each push
     *   3. da.capacity is always >= da.size
     *   4. da.capacity is always a power of 2 (given initial cap 8 and 2x growth)
     */
    for (int i = 0; i < 100; i++) {
        da_push(&da, i * i);
        /* verify invariants here */
    }
    da_free(&da);
}

/* Insert and remove */
void test_insert_remove(void) {
    /* Build [10, 20, 30], insert 15 at index 1 → [10, 15, 20, 30]
     * Remove index 2 → [10, 15, 30]
     * Verify contents exactly */
}

/* Edge cases */
void test_edge_cases(void) {
    /* Empty array: pop should assert (don't test — just know)
     * Single element: push, get, pop → size 0
     * Insert at front (index 0)
     * Insert at back (index == size)
     * Remove first element
     * Remove last element
     */
}

/* Sort */
void test_sort(void) {
    /* Push {5,3,1,4,2}, sort, verify {1,2,3,4,5} */
    /* Push already-sorted, sort, verify unchanged */
    /* Push reverse-sorted, sort, verify sorted */
    /* Single element: sort leaves it unchanged */
}

/* Find */
void test_find(void) {
    /* found: returns correct index */
    /* not found: returns -1 */
    /* duplicates: returns index of first occurrence */
    /* empty array: returns -1 */
}
```

### Amortized Analysis Question

In `LAB 3 Pointers Dynarray.md`, answer:

> If `da_init` sets capacity to 8 and `da_push` doubles when full, how many total element copies occur when pushing 64 elements into an initially empty DynArray? Show the work (list each resize event and how many elements are copied). What is the average copies-per-push?

---

---

## Part 4: Reading Valgrind (4 pts)

Write four tiny programs, each with exactly one defect, and record Valgrind's **exact** message for
each:

| Program | Defect |
|---|---|
| `leak.c` | `malloc` with no `free` |
| `uaf.c` | Use after `free` |
| `dbl.c` | Double `free` |
| `uninit.c` | Read `malloc`'d memory before writing it |

**In `answers.md`:**

1. Paste the four messages verbatim.
2. Which of the four does **ASan not detect**? Verify by building each with
   `-fsanitize=address` and comparing.
3. State the practical rule this gives you about which tool to run and when.

---

## Deliverables

- `where.c`, the Part 2 program, `dynarray.h` / `dynarray.c` / `test_dynarray.c`, and the four
  Part 4 programs
- `answers.md` with every recorded observation
- A `Makefile` building everything with the required flags

## Grading

| Component | Points |
|---|---|
| Part 1: address map recorded and explained | 4 |
| Part 2: reallocation move observed; the rule stated | 4 |
| Part 3: dynamic array correct **and Valgrind-clean** | 8 |
| Part 4: four messages captured; the ASan gap identified | 4 |
| **Total** | **20** |

**Automatic deductions:** any compiler warning (−2 each); any Valgrind error in code not
*deliberately* buggy (−3 each).

---

*PROG 101 · Week 6 · Lab 6 · © CSE Department*
