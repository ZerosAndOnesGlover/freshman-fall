# PROG 101 · Programming I: Structured Programming in C
## Week 4 · Problem Set 4: Arrays and Strings

**Released:** Friday 23 October 2026, 10:00 · Week 4 (after Thursday's Lecture 3)
**Due:** Friday 30 October 2026, 17:00 · Week 5 — late penalty from 17:01
**Submission:** Commit to the Freshman Fall repo under `"$PROG101/week4/ps4"`; submit the commit hash on the course portal.
**Total:** 100 points · **Expected time:** about 3 hours

*(Revised 2026-09-26: cut from about five hours to three. Lab 4, on Monday 26 October, builds `str_trim`,
`str_to_upper`, `str_reverse` and `str_word_count`, so the text pipeline (old Problem 2) is now only in the
lab. `linear_search` and `count_inversions` left Problem 1. The answer key moved out of this handout.)*
**Build with:** `gcc -Wall -Wextra -Werror -pedantic -std=c11`
**Check with:** `-fsanitize=address,undefined` and `valgrind --leak-check=full --error-exitcode=1`

> Every submission must compile with **zero warnings** under the flags above. A warning is a defect.

---

## What this problem set uses

Weeks 0–4, above all this week's: arrays, passing them to functions with a length, 2-D arrays (Lecture 01),
strings as `char` arrays and the `const char *s` parameter style Lecture 02 writes its own `strlen` with,
`fgets`, `<ctype.h>`, `strcspn`, and bounded string handling with `snprintf` (Lecture 03).

**Not needed and not expected:** pointer arithmetic or pointers beyond Lecture 02's string parameters
(Week 5), `malloc` (Week 6), `struct`/`enum` (Week 7), `argc`/`argv`, recursion (Week 9), variadic
functions (never taught), `memcpy`.

---

## Problem 1: Array Algorithms (35 pts)

Create `array_algorithms.c` with these functions, each correct on empty arrays, single elements and duplicates:

```c
int  binary_search(const int arr[], int n, int target);   /* sorted arr, O(log n), or -1 */
void insertion_sort(int arr[], int n);                    /* ascending, stable, in place */
int  remove_duplicates(int arr[], int n);                 /* sorted arr; returns new length */
void rotate_left(int arr[], int n, int k);                /* in place; k may exceed n */
void compute_prefix_sums(const int arr[], int n, long prefix[]);   /* prefix[0] = 0 ... prefix[n] */
long range_sum(const long prefix[], int l, int r);        /* sum of arr[l..r] in O(1) */
```

Examples: `remove_duplicates({1,1,2,3,3,3,4}, 7)` → `{1,2,3,4}`, returns `4`;
`rotate_left({1,2,3,4,5}, 5, 2)` → `{3,4,5,1,2}` (hint: reverse the first `k`, reverse the rest,
reverse the whole); for `{2,4,6,8,10}`, `range_sum(prefix, 1, 3)` → `18`.

Write a `main` that checks every function on at least two inputs and prints `PASS`/`FAIL` with expected
and actual values. It returns non-zero if anything failed.

---

## Problem 2: Matrix Operations (25 pts)

Create `matrix.c`. A matrix is a 2-D array with a fixed column bound, and every function takes explicit sizes:

```c
#define MAX_DIM 10

void matrix_print(int mat[][MAX_DIM], int m, int n);                  /* aligned columns */
void matrix_add(int a[][MAX_DIM], int b[][MAX_DIM], int result[][MAX_DIM], int m, int n);
void matrix_multiply(int a[][MAX_DIM], int b[][MAX_DIM], int result[][MAX_DIM], int m, int n, int p);
void matrix_transpose(int mat[][MAX_DIM], int result[][MAX_DIM], int m, int n);
int  matrix_trace(int mat[][MAX_DIM], int n);
void matrix_identity(int mat[][MAX_DIM], int n);
```

(No `const` on the 2-D parameters: in C11, passing an `int[][10]` to a `const int[][10]` parameter is a
constraint violation that `-pedantic -Werror` rejects — try it, and record the message.)

Demonstrate with `A = {{1,2,3},{4,5,6},{7,8,9}}` and the 3×4 `B = {{1,0,2,1},{0,1,1,0},{2,1,0,1}}`: print
`A + A`, `A × B` (check one entry by hand in a comment), `Bᵀ`, `trace(A)`, and `A × I`.

---

## Problem 3: Safe String Building (40 pts)

Lecture 03 established that `strcpy`, `strcat` and `sprintf` cannot be used safely and that `strncpy`
does not null-terminate. Write `strbuild.c`:

```c
#define PART_LEN 32

/* Appends src to dst, which has total capacity cap (terminator included).
   Returns 0 on success, -1 if the result would not fit.
   On failure dst must still be a valid, null-terminated string. */
int sb_append(char dst[], size_t cap, const char src[]);

/* Joins n strings with sep into dst. Same contract as above.
   Must be O(total output length) -- no repeated rescanning of dst. */
int sb_join(char dst[], size_t cap, const char parts[][PART_LEN], size_t n, const char sep[]);
```

1. **No `strcpy`, `strcat`, `sprintf`, `gets`.** Their use is an automatic zero on this problem.
2. Neither function may ever write past `dst[cap - 1]`, and `dst` must be terminated on **every** path,
   including failure and `cap == 0`.
3. `sb_join` must remember where the output ends instead of calling `strlen(dst)` each time round the loop:
   rescanning makes it Θ(n²).
4. `main` tests at least: exact fit, one byte short, `cap == 0`, `cap == 1`, an empty `src`, and `n == 0`.

| Component | Points |
|---|---|
| `sb_append` correct, including all boundary cases | 12 |
| `sb_join` correct **and** O(total length) | 16 |
| Test suite covers the six required cases | 12 |

---

## Makefile

```makefile
CC = gcc
CFLAGS = -Wall -Wextra -Werror -pedantic -std=c11 -g

PROGRAMS = array_algorithms matrix strbuild

all: $(PROGRAMS)

%: %.c
	$(CC) $(CFLAGS) -o $@ $<

check: all
	./array_algorithms && ./strbuild && ./matrix > /dev/null
	valgrind --leak-check=full --error-exitcode=1 -q ./array_algorithms > /dev/null

clean:
	rm -f $(PROGRAMS)

.PHONY: all check clean
```

---

## Grading

| Problem | Points |
|---|---|
| 1 Array algorithms | 35 |
| 2 Matrix operations | 25 |
| 3 Safe string building | 40 |
| **Total** | **100** |

**Automatic deductions:** any compiler warning (−3 each); any ASan/UBSan report or Valgrind error (−5 each).

---

*PROG 101 · Week 4 · Problem Set 4 · Due Friday 30 October 2026, 17:00 · © CSE Department*
