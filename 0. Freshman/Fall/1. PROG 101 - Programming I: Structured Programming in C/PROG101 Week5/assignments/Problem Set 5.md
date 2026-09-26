# PROG 101 · Programming I: Structured Programming in C
## Week 5 · Problem Set 5: Pointers I

**Released:** Friday 30 October 2026, 10:00 · Week 5 (after Thursday's Lecture 3)
**Due:** Friday 6 November 2026, 17:00 · Week 6 — late penalty from 17:01
**Submission:** Commit to the Freshman Fall repo under `"$PROG101/week5/ps5"`; submit the commit hash on the course portal.
**Total:** 100 points · **Expected time:** about 3 hours

*(Revised 2026-09-26: cut from four to five hours to three. Lab 5, on Monday 2 November, already does the
address-arithmetic tracer, the four `const` combinations and a pointer-bug gallery, so old 1A–1B, Problem 3
and Problem 5 are now only in the lab. Old Problem 2's `reverse_ptr` and `remove_negatives` were the same
functions as Problem 4's, and `p_rotate` repeated Problem Set 4's `rotate_left`; those duplicates went too.
The answer key moved out of this handout.)*
**What this uses:** Weeks 0–5. **Not needed:** function pointers (Week 11), `malloc` (Week 6), structs (Week 7).
**Build with:** `gcc -Wall -Wextra -Werror -pedantic -std=c11`
**Check with:** `valgrind --leak-check=full --error-exitcode=1` and `-fsanitize=address,undefined`

> Zero warnings under the flags above. A warning is a defect.
>
> **No dynamic allocation in this set.** `malloc` and friends are Week 6; everything here works on
> arrays and addresses you already have.

---
## Problem 1: Pointer to Pointer (25 pts)

Create `double_ptr.c`. Implement and demonstrate:

```c
/* Set *ptr to point to whichever of *a or *b is larger.
 * Example: if a=5, b=9, after call *ptr points to b */
void point_to_max(int *a, int *b, int **ptr);

/* Swap two string pointers (not the strings themselves —
 * just make p1 point where p2 pointed and vice versa) */
void swap_strings(const char **p1, const char **p2);

/* Given an array of int pointers ptr_arr[0..n-1],
 * sort the array of pointers so that the values they point to
 * are in ascending order (do not move the values, only the pointers) */
void sort_by_pointed_value(int *ptr_arr[], int n);
```

Write tests that verify each function including edge cases (equal values, single element, etc.).

---

## Problem 2: Pointer Outputs (30 pts)

Create `ptr_algorithms.c`. All functions must use pointer parameters for output. *(10 pts each)*

```c
/* === Pointer-output functions === */

/* Find the longest run of equal consecutive values in arr[0..n-1].
 * Store in *start the pointer to the first element of the run,
 * in *length the length of the run.
 * Example: {1,1,2,3,3,3,2} → *start = &arr[3], *length = 3 */
void longest_run(const int *arr, int n,
                 const int **start, int *length);

/* Given a string s, find the first and last non-whitespace characters.
 * Store pointers to them in *first and *last.
 * If s is all whitespace or empty, set both to NULL. */
void find_word_bounds(const char *s,
                      const char **first, const char **last);

/* === Two-pointer technique === */

/* Given a sorted array arr[0..n-1] and a target sum,
 * find two elements that add to target. Use the two-pointer technique.
 * If found: store pointers to them in *p1 and *p2, return 1.
 * If not found: return 0. */
int two_sum_sorted(const int *arr, int n, int target,
                   const int **p1, const int **p2);
```

---

## Problem 3: Pointer-Only Utilities (45 pts)

Implement `ptrutil.c` with **no array-subscript syntax anywhere** — no `[]` in any function body.
Use pointer arithmetic and pointer comparison only. This is an exercise in seeing `a[i]` for what it
is (`*(a + i)`), not a claim that pointer style is better.

```c
size_t p_strlen(const char *s);
void   p_reverse(int *a, size_t n);
int   *p_find(int *a, size_t n, int target);          /* NULL if absent          */
size_t p_count_between(const int *a, size_t n, int lo, int hi);   /* lo <= x <= hi */
size_t p_remove_negatives(int *a, size_t n);         /* returns new length      */
```

### Requirements

1. **No `[]` in any function body.** Its use costs the marks for that function.
2. Every function must be correct for `n == 0` and `n == 1`.
3. `p_remove_negatives` must preserve relative order and run in **one pass**, O(n): a write pointer
   trailing a read pointer.
4. `const` where the function does not modify — the signatures above already show where.
5. Write `test_ptrutil.c` covering, at minimum, the empty and single-element cases for every
   function.

### Marking

| Component | Points |
|---|---|
| `p_strlen`, `p_find`, `p_count_between` correct | 15 |
| `p_reverse` correct incl. even/odd/n≤1 | 10 |
| `p_remove_negatives` correct, order-preserving, one pass | 12 |
| Tests cover the required edge cases | 8 |


---

## Makefile

```makefile
CC     = gcc
CFLAGS = -Wall -Wextra -Werror -g -std=c11

PROGRAMS = double_ptr ptr_algorithms test_ptrutil

all: $(PROGRAMS)

test_ptrutil: test_ptrutil.o ptrutil.o
	$(CC) $(CFLAGS) -o $@ $^

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

%: %.c
	$(CC) $(CFLAGS) -o $@ $< -lm

clean:
	rm -f $(PROGRAMS) *.o

.PHONY: all clean
```

---

## Grading

| Problem | Topic | Points |
|---|---|---|
| 1 | Pointer to Pointer | 25 |
| 2 | Pointer Outputs | 30 |
| 3 | Pointer-Only Utilities | 45 |
| **Total** | | **100** |

---

*PROG 101 · Week 5 · Problem Set 5 · Due Friday 6 November 2026, 17:00 · © CSE Department*
