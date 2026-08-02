# PROG 101 — Programming I: Structured Programming in C
## Week 5 · Lab 5: Pointer Mechanics and Write-Back

**Duration:** 2 hours · **Points:** 20 · **Room:** BH 215

**Build with:** `gcc -Wall -Wextra -Werror -pedantic -std=c11 -g`
**Check with:** `valgrind --leak-check=full --error-exitcode=1`

---

## Overview

This lab makes pointers observable. You will print addresses and watch arithmetic scale by type,
prove to yourself that arrays are not pointers, exercise all four `const` combinations against the
compiler, and use write-back to return more than one value.

**No `malloc` this week.** Everything operates on storage you already have; the heap arrives in
Week 6.

---
## Part 1: Pointer Mechanics (6 pts)

### 1A: Address Arithmetic Tracer

Create `pointer_trace.c`. Before running each block, predict the output. Then verify.

```c
#include <stdio.h>

int main(void) {
    int arr[] = {10, 20, 30, 40, 50};
    int *p = arr;

    /* Block 1 — predict each line */
    printf("%d\n",  *p);
    printf("%d\n",  *(p + 1));
    printf("%d\n",  *(p + 4));
    printf("%p\n",  (void *)p);
    printf("%p\n",  (void *)(p + 1));

    /* Block 2 */
    p = p + 2;
    printf("%d\n",  *p);
    printf("%d\n",  p[-1]);    /* negative index — legal? */
    printf("%d\n",  p[2]);

    /* Block 3 */
    int *q = &arr[4];
    printf("%td\n", q - p);    /* pointer subtraction — what units? */
    printf("%td\n", p - arr);

    /* Block 4 — sizeof */
    printf("%zu\n", sizeof(arr));      /* total bytes */
    printf("%zu\n", sizeof(p));        /* bytes of the pointer itself */
    printf("%zu\n", sizeof(arr) / sizeof(arr[0]));  /* element count */

    return 0;
}
```

Record in `LAB 3 Pointers Dynarray.md`:
1. Your predictions (before running) for every `printf`
2. Actual output
3. For any wrong prediction: explain why the actual result is correct

### 1B: The Decay Experiment

Create `decay.c` to prove that array-to-pointer decay happens at function boundaries:

```c
#include <stdio.h>

void inside_function(int arr[], int n) {
    printf("sizeof(arr) inside function = %zu\n", sizeof(arr));
    printf("sizeof(int*) on this system = %zu\n", sizeof(int *));
}

int main(void) {
    int arr[10];
    printf("sizeof(arr) in main = %zu\n", sizeof(arr));
    inside_function(arr, 10);
    return 0;
}
```

In `LAB 3 Pointers Dynarray.md`:
1. What is `sizeof(arr)` in `main`? In `inside_function`? Why are they different?
2. What does this tell you about what `inside_function` actually receives?
3. Why must you always pass the array length as a separate parameter?

### 1C: const Pointer Combinations

Create `const_pointers.c`. For each of the four `const` combinations, demonstrate:
- What operations are allowed (compile and run)
- What operations are forbidden (add a comment showing the error you'd get)

```c
int x = 10, y = 20;

const int *p1 = &x;          /* pointer to const int */
int * const p2 = &x;          /* const pointer to int */
const int * const p3 = &x;    /* const pointer to const int */
int *p4 = &x;                 /* no const */

/* For each pointer, try:
 *   1. *p = 5      (modify value)
 *   2. p = &y      (change target)
 * Mark each as: ALLOWED or FORBIDDEN (error: "...")
 */
```

---

---

## Part 2: Pass-by-Pointer Functions (6 pts)

Create `bypointer.c`. Implement all functions using pointer parameters.

```c
#include <stdio.h>
#include <assert.h>

/* Swap the values of two ints. */
void swap_int(int *a, int *b);

/* Swap the values of two doubles. */
void swap_double(double *a, double *b);

/* Divide a by b. Store quotient in *quot, remainder in *rem.
 * Precondition: b != 0, quot != NULL, rem != NULL */
void divmod(int a, int b, int *quot, int *rem);

/* Compute min and max of arr[0..n-1].
 * Store results in *out_min and *out_max.
 * Precondition: n > 0 */
void minmax(const int arr[], int n, int *out_min, int *out_max);

/* Given a sorted array arr[0..n-1] and a target value,
 * perform binary search.
 * If found: set *found = 1, *index = position.
 * If not found: set *found = 0, *index = -1. */
void binary_search(const int arr[], int n, int target,
                   int *found, int *index);

/* Parse a string of the form "NAME AGE" into separate fields.
 * Copy the name into name_buf (max name_buf_size bytes including null).
 * Store the age as an integer in *age.
 * Returns 1 on success, 0 on parse failure.
 * Example: parse_person("Alice 30", buf, 50, &age) → name="Alice", age=30 */
int parse_person(const char *input, char *name_buf,
                 int name_buf_size, int *age);
```

Write a `main()` that tests every function, printing PASS/FAIL for each case. Include at least three test cases per function (normal, edge, boundary).

---

---

## Part 4: The Pointer Bug Gallery (8 pts)

Five short programs, each with exactly one pointer defect. For each: **predict** what will happen,
**run** it, **run it again under a sanitizer**, and record all three in `answers.md`.

Create each as its own file so one crash does not stop the rest.

### 4A — dangling return

```c
#include <stdio.h>
static int *make(void) { int x = 42; return &x; }
int main(void) { int *p = make(); printf("%d\n", *p); return 0; }
```

Before running anything, change the `printf` to print the **pointer** rather than dereference it:

```c
printf("%p\n", (void *)p);
```

Build at `-O0` and again at `-O2`, and record what `make()` returns in each case. The answer is
probably not what you expect, and it is the **same** at both levels — that sameness is part of the
point. Explain what the compiler did and why it was entitled to. *(2 pts)*

Then restore the dereference and run under `-fsanitize=address`. *(included in the 2 pts)*

### 4B — off the front

```c
#include <stdio.h>
int main(void) {
    int a[5] = {1,2,3,4,5};
    for (int *p = a + 4; p >= a; p--) printf("%d ", *p);
    return 0;
}
```

This prints the right answer. Explain why it is nonetheless undefined behaviour, and give a correct
rewrite. *(2 pts)*

### 4C — the decayed `sizeof`

```c
#include <stdio.h>
static void show(int a[10]) { printf("%zu\n", sizeof a / sizeof a[0]); }
int main(void) { int a[10]; show(a); return 0; }
```

Predict the printed value, then compile with `-Wsizeof-array-argument`. *(2 pts)*

### 4D — unchecked search

```c
#include <stdio.h>
#include <string.h>
int main(void) {
    const char *s = "hello";
    char *p = strchr(s, 'z');
    printf("%c\n", *p);
    return 0;
}
```

Run under Valgrind and paste the report. *(1 pt)*

### 4E — writing through `const`

```c
const int v = 5;
int *p = (int *)&v;    /* cast away const */
*p = 6;
```

This compiles. Explain why it is undefined behaviour anyway, and what the cast actually did.
*(1 pt)*

---

## Deliverables

- The Part 1–3 programs
- Five files for Part 4
- `answers.md` with every recorded observation
- A `Makefile` building everything with the required flags

## Grading

| Component | Points |
|---|---|
| Part 1: address arithmetic, decay, `const` combinations observed | 6 |
| Part 2: pass-by-pointer functions correct | 6 |
| Part 4: all five bugs predicted, run, and explained | 8 |
| **Total** | **20** |

**Automatic deductions:** any compiler warning (−2 each); any Valgrind error in code that is not
*deliberately* buggy (−3 each).

---

*PROG 101 · Week 5 · Lab 5 · © CSE Department*
