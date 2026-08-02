# PROG 101 — Programming I: Structured Programming in C
## Week 5 · Problem Set 5: Pointers I

**Released:** Friday, Week 5 · **Due:** Friday, Week 6 at 17:00
**Total:** 100 points
**Build with:** `gcc -Wall -Wextra -Werror -pedantic -std=c11`
**Check with:** `valgrind --leak-check=full --error-exitcode=1` and `-fsanitize=address,undefined`

> Zero warnings under the flags above. A warning is a defect.
>
> **No dynamic allocation in this set.** `malloc` and friends are Week 6; everything here works on
> arrays and addresses you already have.

---
## Problem 1: Pointer Mechanics (15 pts)

### 1A: Pointer Prediction Table (5 pts)

Create `predictions.c`. For each expression, write your prediction as a comment, then verify by running:

```c
#include <stdio.h>
#include <stddef.h>

int main(void) {
    int  a = 10, b = 20, c = 30;
    int *p = &b;
    int *q = &a;

    /* Predict the value printed by each line below.
     * Write your answer as: // → <your prediction>
     */
    printf("%d\n",  *p);              /* → */
    printf("%d\n",  *q);              /* → */
    printf("%d\n",  *p + *q);         /* → */
    printf("%d\n",  *p * *q);         /* → */
    printf("%d\n",  *(p) + 1);        /* → */
    printf("%d\n",  *(&b));           /* → */

    *p = 99;
    printf("%d\n",  b);               /* → */
    printf("%d\n",  *p);              /* → */

    p = &c;
    printf("%d\n",  *p);              /* → */
    printf("%d\n",  b);               /* → (did b change?) */

    q = p;
    printf("%d\n",  *q);              /* → */
    printf("%p\n",  (void *)p);       /* → (same as q's address?) */
    printf("%p\n",  (void *)q);       /* → */
    printf("%d\n",  p == q);          /* → (1 or 0?) */
    printf("%d\n",  *p == *q);        /* → */

    return 0;
}
```

After running, for each wrong prediction write a one-sentence correction explaining the actual behavior.

### 1B: Pointer Arithmetic on Types (5 pts)

Create `ptr_arith.c`. Measure and explain pointer arithmetic across different types:

```c
#include <stdio.h>

int main(void) {
    char   carr[4] = {0};
    short  sarr[4] = {0};
    int    iarr[4] = {0};
    double darr[4] = {0};

    char   *cp = carr;
    short  *sp = sarr;
    int    *ip = iarr;
    double *dp = darr;

    /* Print the byte difference between consecutive elements for each type */
    printf("char*:   +1 advances %td bytes\n", (char*)(cp+1) - (char*)cp);
    printf("short*:  +1 advances %td bytes\n", (char*)(sp+1) - (char*)sp);
    printf("int*:    +1 advances %td bytes\n", (char*)(ip+1) - (char*)ip);
    printf("double*: +1 advances %td bytes\n", (char*)(dp+1) - (char*)dp);

    return 0;
}
```

In comments within the file, explain:
1. Why pointer `+1` advances by different amounts for different types
2. How the compiler knows how many bytes to advance
3. Why this makes `arr[i]` and `*(arr + i)` truly identical

### 1C: Pointer to Pointer (5 pts)

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

## Problem 2: Pointer-Based Data Manipulation (25 pts)

Create `ptr_algorithms.c`. All functions must use pointer parameters for output.

```c
/* === In-place array operations === */

/* Reverse arr[0..n-1] in-place using only pointer arithmetic.
 * No array indexing (arr[i]) allowed — use *(arr+i) or pointer variables. */
void reverse_ptr(int *arr, int n);

/* Remove all negative numbers from arr[0..n-1] in-place.
 * Compacts remaining elements to the front.
 * Stores the new length in *new_n. */
void remove_negatives(int *arr, int *new_n);

/* Partition arr[0..n-1] so all even numbers come before odd numbers.
 * Relative order within each group need not be preserved.
 * Stores count of even numbers in *even_count. */
void partition_even_odd(int *arr, int n, int *even_count);

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

/* Determine if arr[0..n-1] is a palindrome using only two pointers
 * (one starting from each end, moving inward). No indexing allowed. */
int is_palindrome_ptr(const int *arr, int n);

/* Given a sorted array arr[0..n-1] and a target sum,
 * find two elements that add to target. Use the two-pointer technique.
 * If found: store pointers to them in *p1 and *p2, return 1.
 * If not found: return 0. */
int two_sum_sorted(const int *arr, int n, int target,
                   const int **p1, const int **p2);
```

---

---

## Problem 3: `const` Correctness (15 pts)

Lecture 3 gave four combinations of `const` and pointer. This problem checks you can choose among
them deliberately.

Write `constcheck.c` containing, for each of the following, either a correct declaration or a short
comment saying it is impossible and why:

1. A pointer that may be repointed but through which the target may not be modified.
2. A pointer that may not be repointed but through which the target may be modified.
3. A pointer that may be neither repointed nor used to modify its target.
4. A function taking an array it promises not to modify.
5. A function that fills a caller-supplied buffer.

Then write, in `answers.md`:

**(a)** For `const char *s`, state which of `s++` and `s[0] = 'x'` compiles, and which `const`
qualifies what. *(4 pts)*

**(b)** For `char *const s`, the same. *(4 pts)*

**(c)** Given `int v = 5; const int *p = &v;`, explain why `*p = 6;` is rejected but `v = 6;` is
allowed. What exactly does `const` constrain? *(4 pts)*

**(d)** Give one concrete benefit of `const` on a parameter that is **not** about preventing your own
mistakes. *(3 pts)*

---

## Problem 4: Pointer-Only Utilities (25 pts)

Implement `ptrutil.c` with **no array-subscript syntax anywhere** — no `[]` in any function body.
Use pointer arithmetic and pointer comparison only. This is an exercise in seeing `a[i]` for what it
is (`*(a + i)`), not a claim that pointer style is better.

```c
size_t p_strlen(const char *s);
void   p_reverse(int *a, size_t n);
int   *p_find(int *a, size_t n, int target);          /* NULL if absent          */
size_t p_count_if(const int *a, size_t n, int (*pred)(int));
size_t p_filter(int *a, size_t n, int (*pred)(int));  /* returns new length      */
void   p_rotate(int *a, size_t n, size_t k);          /* rotate LEFT by k, O(n)  */
```

### Requirements

1. **No `[]` in any function body.** Its use costs the marks for that function.
2. Every function must be correct for `n == 0` and `n == 1`.
3. `p_filter` must preserve relative order and run in **one pass**, O(n).
4. `p_rotate` must be O(n) time and **O(1) extra space**. A temporary array is not acceptable.
   `k` may exceed `n`.
5. `const` where the function does not modify — the signatures above already show where.
6. Write `test_ptrutil.c` covering, at minimum, the empty and single-element cases for every
   function.

### Marking

| Component | Points |
|---|---|
| `p_strlen`, `p_find`, `p_count_if` correct | 6 |
| `p_reverse` correct incl. even/odd/n≤1 | 4 |
| `p_filter` correct, order-preserving, one pass | 6 |
| `p_rotate` O(n) time and O(1) space, handles k > n | 6 |
| Tests cover the required edge cases | 3 |

*Hint for `p_rotate`: three reversals. Reverse the first k, reverse the rest, then reverse the whole
thing. Convince yourself on paper before coding it.*

---

## Problem 5: Reading a Pointer Bug (20 pts)

Each fragment below has exactly one defect. For each, in `answers.md`: **name** the defect,
**explain** what happens at runtime, give the **compiler flag or tool** that would catch it, and
write the **fix**. *(4 pts each.)*

```c
/* (a) */  int *f(void) { int x = 42; return &x; }

/* (b) */  void g(const char *s) { char buf[8]; strcpy(buf, s); }

/* (c) */  int h(int *a, int n) { int t = 0; for (int i = 0; i <= n; i++) t += a[i]; return t; }

/* (d) */  void k(void) { int *p; *p = 5; }

/* (e) */  int m(const char *s) { char *p = strchr(s, 'x'); return *p; }
```

---
## Makefile

```makefile
CC     = gcc
CFLAGS = -Wall -Wextra -Werror -g -std=c11

PROGRAMS = predictions ptr_arith double_ptr ptr_algorithms \
           constcheck test_ptrutil

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
| 1 | Pointer Mechanics | 15 |
| 2 | Pointer-Based Data Manipulation | 25 |
| 3 | `const` Correctness | 15 |
| 4 | Pointer-Only Utilities | 25 |
| 5 | Reading a Pointer Bug | 20 |
| **Total** | | **100** |

---

## Answer Key (Instructor Copy)

### Problem 1 — Pointer Mechanics (15 pts)

**1A Prediction Table (5 pts).** Verified output, in order:

| Expression | Value | Note |
|---|---|---|
| `*p` | `20` | `p` aims at `b` |
| `*q` | `10` | `q` aims at `a` |
| `*p + *q` | `30` | 20 + 10 |
| `*p * *q` | `200` | 20 × 10. The space in `* *q` is **required** — `**q` would lex as a single token |
| `*(p) + 1` | `21` | dereference *then* add; contrast `*(p + 1)`, which reads the next `int` — out of bounds here |
| `*(&b)` | `20` | `*` and `&` cancel |
| `b` after `*p = 99` | `99` | writing through the pointer mutates `b` itself |
| `*p` after | `99` | same object |
| `*p` after `p = &c` | `30` | now aims at `c` |
| `b` after | `99` | **unchanged** — repointing `p` does not touch what it previously referenced |
| `*q` after `q = p` | `30` | both aim at `c` |
| `p == q` | `1` | same address |
| `*p == *q` | `1` | same value (trivially, same object) |

*Grading: 5 pts across 16 lines — roughly 0.3 each, rounded in the student's favour. The two conceptually load-bearing rows are `b` after `p = &c` (repointing ≠ mutating) and `*(p) + 1` vs `*(p + 1)`. A student who gets those two right and slips elsewhere should still score ≥ 4.*
*`printf("%p", …)` **must** cast to `void *` — passing an `int *` is UB for `%p`. The prompt already does this correctly; flag any student who removes the cast.*

**1B Pointer Arithmetic (5 pts).** Verified on x86-64:

| Type | `+1` advances | `sizeof` |
|---|---|---|
| `char *` | 1 byte | 1 |
| `short *` | 2 bytes | 2 |
| `int *` | 4 bytes | 4 |
| `double *` | 8 bytes | 8 |

1. Pointer arithmetic is in **units of the pointed-to type**, not bytes — `p + 1` means "the next object of this type", so the byte step is `sizeof(*p)`. This is what makes `arr[i]` ≡ `*(arr + i)` work uniformly for every element type.
2. The compiler knows the size **statically**, from the pointer's declared type; it multiplies the index by `sizeof` at compile time. This is also why arithmetic on `void *` is not permitted by the standard (gcc allows it as an extension, treating it as size 1).

*The `(char*)(xp+1) - (char*)xp` idiom in the prompt is the correct way to measure this: subtracting two `char *` yields a byte count. Subtracting the original typed pointers would give `1` for every type — worth pointing out, as a student may "simplify" it and lose the whole result.*

**1C Pointer to Pointer (5 pts).**
*Expected: `int **pp = &p;` gives `*pp` ≡ `p` (an `int *`) and `**pp` ≡ the `int`. Assigning `*pp = &c` **repoints `p` itself** — that is the whole reason double pointers exist: to let a callee modify the caller's pointer. Grade on whether the student connects this to the practical case (a function that allocates and must hand the pointer back, e.g. `void alloc_it(int **out)`), not merely on tracing arrows.*

---

### Problem 2 — Pointer-Based Data Manipulation (25 pts)

*Where "pointer-only" is required, indexing with `arr[i]` should cost marks only if the spec explicitly forbade it; otherwise treat `*(arr+i)` and `arr[i]` as identical (they are, by definition).*
*Probe the classic reversal bug: a two-pointer reverse with `while (lo <= hi)` swaps the middle element with itself on odd lengths — harmless — but `while (lo < hi)` is correct and clearer. Neither is wrong; a loop that runs `lo != hi` **is** wrong for even lengths (the pointers cross without ever being equal, running off both ends). Test with both an odd- and even-length array.*

---

### Problem 3 — `const` Correctness (15 pts)

```c
const int *p1;              /* 1. repoint yes, modify target no  */
int *const p2 = &v;         /* 2. repoint no,  modify target yes */
const int *const p3 = &v;   /* 3. neither                        */

int  total(const int *a, size_t n);      /* 4. promises not to modify */
void fill(char *out, size_t cap);        /* 5. must NOT be const      */
```

**(a) `const char *s` — 4 pts.** `s++` **compiles**; `s[0] = 'x'` is **rejected**. The `const` is
leftmost so it qualifies the `char` being pointed at, not the pointer. Moving the pointer changes no
`char`, so it is permitted.

**(b) `char *const s` — 4 pts.** Exactly reversed: `s++` is **rejected**, `s[0] = 'x'` **compiles**.
The `const` sits right of the `*`, so it qualifies the pointer itself.

*Verified: all four cases compile-checked; the results match the table above.*

The rule to state: **`const` qualifies whatever is immediately to its left, unless it is leftmost, in
which case it qualifies what is immediately to its right.**

**(c) — 4 pts.** `const` constrains **access through that particular pointer**, not the object.
`p` promises *"I will not modify anything through p"*; it says nothing about `v`, which is an
ordinary non-const `int` and may be assigned by name. It is a compile-time promise about **a route**,
not runtime protection of storage.

Students who answer "because `v` is not const" have the right conclusion; award full marks only if
they identify that the qualification attaches to the access path.

**(d) — 3 pts.** Any one of:

- **It widens what callers may pass.** A caller holding a `const int *` cannot pass it to a function
  taking `int *`; the `const` version accepts both.
- **It documents the contract in the type**, where it cannot go stale the way a comment can.
- **It enables optimisation** in some cases, by telling the compiler the callee will not write
  through that pointer.

*Reject "it stops me making mistakes"* — the question explicitly excludes that.

---

### Problem 4 — Pointer-Only Utilities (25 pts)

```c
size_t p_strlen(const char *s)
{ const char *p = s; while (*p) p++; return (size_t)(p - s); }

void p_reverse(int *a, size_t n)
{
    if (n < 2) return;
    int *l = a, *r = a + n - 1;
    while (l < r) { int t = *l; *l = *r; *r = t; l++; r--; }
}

int *p_find(int *a, size_t n, int target)
{
    for (int *p = a; p != a + n; p++) if (*p == target) return p;
    return NULL;
}

size_t p_count_if(const int *a, size_t n, int (*pred)(int))
{
    size_t c = 0;
    for (const int *p = a; p != a + n; p++) if (pred(*p)) c++;
    return c;
}

size_t p_filter(int *a, size_t n, int (*pred)(int))
{
    int *w = a;
    for (int *r = a; r != a + n; r++) if (pred(*r)) *w++ = *r;
    return (size_t)(w - a);
}

void p_rotate(int *a, size_t n, size_t k)
{
    if (n == 0) return;
    k %= n;
    if (k == 0) return;
    p_reverse(a, k);
    p_reverse(a + k, n - k);
    p_reverse(a, n);
}
```

**Verified: 16 checks passing, Valgrind clean** — including `n = 0`, `n = 1`, even and odd lengths,
all-kept and none-kept filters, and `k > n`.

**Marking notes.**

- **`p_rotate` is where the marks separate.** The three-reversal algorithm is O(n) time and O(1)
  space. A solution using a temporary array is O(n) space and loses 3 of the 6; a repeated
  rotate-by-one is O(n·k) and loses 4.
- **`k %= n` before anything else** handles `k > n`. Verified: `k = 7` on `n = 5` gives the same
  result as `k = 2`. Omitting it reads out of bounds.
- **`n == 0` must be guarded before `k %= n`** — otherwise it is a division by zero, which is
  undefined behaviour in the very line meant to make the function safe. This is the same shape as
  Week 6's `size != 0` guard before `SIZE_MAX / size`.
- **`p_filter` must be one pass** with a write cursor trailing a read cursor. Removing elements one
  at a time with a shift is Θ(n²) — cap at 3 of 6 and name the cost.
- **`p != a + n` rather than `p < a + n`.** Both work for arrays; `!=` is the convention that
  generalises. Do not deduct for `<`.
- **Any `[]` in a function body** costs that function's marks, as stated in the problem.

---

### Problem 5 — Reading a Pointer Bug (20 pts)

*4 points each: 1 for naming, 1 for the runtime consequence, 1 for the tool, 1 for the fix.*

| | Defect | At runtime | Caught by | Fix |
|---|---|---|---|---|
| **(a)** | Returning the address of a local | The frame dies at return; the pointer dangles | `-Wreturn-local-addr` | Return by value, or take a caller-supplied `int *out` |
| **(b)** | Unbounded `strcpy` into an 8-byte buffer | Overflows `buf` when `s` is longer; corrupts adjacent stack | ASan; `-Wstringop-overflow` sometimes | `snprintf(buf, sizeof buf, "%s", s)` |
| **(c)** | `i <= n` off-by-one | Reads `a[n]`, one past the end | ASan / Valgrind | `i < n` |
| **(d)** | Uninitialised pointer dereferenced | Writes 5 to an arbitrary address | `-Wmaybe-uninitialized` (**at `-O1`+ only**) | Initialise before use |
| **(e)** | `strchr` result not checked for NULL | `*p` dereferences NULL when `'x'` is absent | Valgrind; static analysis | `if (!p) return -1;` before dereferencing |

**Marking notes.**

- **(a)** GCC compiles this to `return NULL` under optimisation — verified. A student who says "you
  get a stale address" has the common misconception; award the mark but correct it, because the point
  is that UB is a *compiler* phenomenon, not a hardware one.
- **(d)** The tool answer must note that `-Wmaybe-uninitialized` reports **nothing at `-O0`**.
  Verified. A bare "the compiler warns" is worth half.
- **(b)** Accept `strlcpy` or a manual bounded copy as the fix. Do **not** accept `strncpy` without
  an explicit terminator assignment, since `strncpy` does not null-terminate when the source fills
  the buffer.
- **(e)** Also accept restructuring to avoid `strchr` entirely. The mark is for recognising the
  unchecked return, which is the single most common C crash.

---

*PROG 101 · Week 5 · Problem Set 5 · © CSE Department*
