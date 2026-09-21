# PROG 101 · Programming I: Structured Programming in C
## Week 6 · Problem Set 6: Pointers II — Dynamic Memory

**Released:** Friday 6 November 2026, 10:00 · Week 6 (after Thursday's Lecture 3)
**Due:** Friday 13 November 2026, 17:00 · Week 7 — late penalty from 17:01
**Submission:** Commit to the Freshman Fall repo under `"$PROG101/week6/ps6"`; submit the commit hash on the course portal.
**Total:** 100 points · **Expected time:** about 5 hours
**What this uses:** Weeks 0–6, including the `typedef struct` `Vec` that Lecture 03 builds.
**Not needed:** function pointers (Week 11), files (Week 8), the rest of `struct` (Week 7).
**Build with:** `gcc -Wall -Wextra -Werror -pedantic -std=c11 -g`
**Check with:** `valgrind --leak-check=full --show-leak-kinds=all --error-exitcode=1`

> **Every submission must be Valgrind-clean.** Zero errors, zero bytes definitely lost. A leak is a
> defect, and it is graded as one.
>
> Every allocation needs a visible, reachable `free` — **including on error paths**.

---
## Problem 1: Dynamic Memory (30 pts)

### 1A: Safe String Heap Operations (10 pts)

Create `heap_strings.c`:

```c
/* Allocate a copy of s on the heap. Caller must free.
 * Returns NULL on malloc failure. */
char *str_dup(const char *s);

/* Allocate a new string that is the concatenation of s1 and s2.
 * Caller must free. Returns NULL on malloc failure. */
char *str_concat(const char *s1, const char *s2);

/* Allocate a new string containing s[start..start+len-1].
 * Clamps to valid range if start or len are out of bounds.
 * Caller must free. Returns NULL on malloc failure. */
char *str_substr(const char *s, int start, int len);

/* Split s on delimiter delim. Return a heap-allocated array of
 * heap-allocated strings. Store count in *n.
 * Example: str_split("a,b,c", ',', &n) → {"a","b","c"}, n=3
 * Caller must free each string and then the array itself. */
char **str_split(const char *s, char delim, int *n);

/* Free a result from str_split: free each string, then the array. */
void str_split_free(char **parts, int n);
```

Write tests that:
- Verify correct output for each function
- Run Valgrind-clean (0 leaks)
- Test empty strings, single characters, no delimiter found

### 1B: Extending Lecture 03's Dynamic Array (15 pts)

Start from the `Vec` of Lecture 03 (`vec_init`, `vec_push`, `vec_free`) and add:

```c
/* Append every element of src to dst. 0 on success, -1 if an allocation failed.
 * Must work when dst and src are the same Vec. */
int vec_extend(Vec *dst, const Vec *src);

/* A new Vec with the elements in reverse order. Caller must vec_free the result. */
Vec vec_reversed(const Vec *v);

/* Remove every element equal to value, in place, keeping order, in one pass.
 * Returns how many were removed. */
size_t vec_remove_value(Vec *v, int value);

/* Give back unused capacity: afterwards cap == len (an empty Vec frees its buffer). */
int vec_shrink_to_fit(Vec *v);

void vec_print(const Vec *v);      /* e.g.  [1, 2, 3] len=3 cap=4 */
```

Demonstrate: push `1..5`, extend with `{3, 4}`, extend the Vec **with itself**, print the reversed copy,
remove every `3`, shrink to fit, and reverse an empty Vec. Expected:

```
[1, 2, 3, 4, 5, 3, 4] len=7 cap=8
[1, 2, 3, 4, 5, 3, 4, 1, 2, 3, 4, 5, 3, 4] len=14 cap=16
[4, 3, 5, 4, 3, 2, 1, 4, 3, 5, 4, 3, 2, 1] len=14 cap=16
removed 4
[1, 2, 4, 5, 4, 1, 2, 4, 5, 4] len=10 cap=16
[1, 2, 4, 5, 4, 1, 2, 4, 5, 4] len=10 cap=10
[] len=0 cap=0
```

All must be Valgrind-clean.

---

## Problem 2: Ownership by Contract (20 pts)

Write `strdup_lib.c` implementing:

```c
/* Returns a newly allocated copy of `s`, or NULL on failure or if `s` is NULL.
   CALLER MUST FREE. */
char *str_dup(const char *s);

/* Returns a newly allocated copy of at most `n` characters, always terminated.
   CALLER MUST FREE. */
char *str_ndup(const char *s, size_t n);

/* Frees *p and sets it to NULL. Safe to call with *p already NULL. */
void  str_release(char **p);
```

### Requirements

1. `str_dup(NULL)` returns NULL rather than crashing.
2. `str_dup("")` returns a valid one-byte allocation containing `'\0'` — **not** NULL.
3. `str_ndup` must terminate even when `n` is shorter than `s`.
4. `str_release` takes `char **`. In `answers.md`, explain in two sentences **why it cannot take
   `char *`** and still do its job.
5. Every function carries an ownership comment saying who frees.

### Marking

| Component | Points |
|---|---|
| `str_dup` correct incl. NULL and empty-string cases | 6 |
| `str_ndup` correct and always terminated | 6 |
| `str_release` correct, and the `char **` explanation | 5 |
| Ownership comments present and accurate | 3 |

---

## Problem 3: A Container That Owns Its Contents (25 pts)

Implement `strvec.c` — a growable array of strings where **the vector owns every string it holds**.

```c
typedef struct { char **items; size_t len, cap; } StrVec;

void sv_init(StrVec *v);
int  sv_push(StrVec *v, const char *s);   /* COPIES s; vector owns the copy */
const char *sv_at(const StrVec *v, size_t i);   /* NULL if out of range     */
int  sv_remove(StrVec *v, size_t i);      /* frees the element, keeps order */
void sv_free(StrVec *v);                  /* frees every string AND items   */
```

### Requirements

1. `sv_push` **copies** its argument. The caller keeps ownership of what it passed in.
2. Growth doubles from an initial 4, guarded against `size_t` overflow.
3. `sv_push` must leave the vector **unchanged** if either allocation fails — no half-added element,
   no leak.
4. `sv_free` frees every string *and* the `items` array, then resets the struct.
5. `sv_remove` frees the removed string and closes the gap with `memmove`, preserving order.
6. `test_strvec.c` must include a test that pushes, removes, and frees, and be Valgrind-clean.

### Marking

| Component | Points |
|---|---|
| `sv_push` copies, grows correctly, is overflow-guarded | 8 |
| Failure leaves the vector consistent (requirement 3) | 5 |
| `sv_remove` correct, order-preserving, frees the element | 5 |
| `sv_free` releases everything; Valgrind-clean under test | 5 |
| Tests exercise push/remove/free | 2 |

---

## Problem 4: Two-Dimensional Allocation (15 pts)

```c
int **make_matrix(size_t rows, size_t cols);   /* zeroed; NULL on failure */
void free_matrix(int **m, size_t rows);
```

### Requirements

1. Every cell starts at zero. Use `calloc`, and say in `answers.md` **why `calloc` rather than
   `malloc` + a loop** — give the two distinct reasons from Lecture 1.
2. If any row allocation fails part-way through, **free the rows already allocated and the row array**
   before returning NULL. A partial failure must not leak.
3. `free_matrix(NULL, 0)` must be safe.
4. In `answers.md`, contrast this row-pointer layout with a single flat `rows*cols` allocation
   indexed as `m[r*cols + c]`: give one advantage of each. *(4 of the 15 pts.)*

---

## Problem 5: Finding the Leak (10 pts)

Each fragment leaks or misuses memory. For each: name the defect, say what Valgrind reports, and fix
it. *(2 pts each.)*

```c
/* (a) */  char *s = malloc(10); s = "hello";

/* (b) */  p = realloc(p, n * sizeof *p);

/* (c) */  int *a = malloc(4*sizeof *a); if (!a) return -1; a = malloc(8*sizeof *a); free(a);

/* (d) */  char *b = malloc(100); if (!b) return -1; if (n < 0) return -1; free(b);

/* (e) */  free(p); free(p);
```

---
## Makefile

```makefile
CC     = gcc
CFLAGS = -Wall -Wextra -Werror -g -std=c11

PROGRAMS = heap_strings test_strdup_lib test_strvec matrix

all: $(PROGRAMS)

test_strdup_lib: test_strdup_lib.o strdup_lib.o
	$(CC) $(CFLAGS) -o $@ $^

test_strvec: test_strvec.o strvec.o strdup_lib.o
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
| 1 | Dynamic Memory Fundamentals | 30 |
| 2 | Ownership by Contract | 20 |
| 3 | A Container That Owns Its Contents | 25 |
| 4 | Two-Dimensional Allocation | 15 |
| 5 | Finding the Leak | 10 |
| **Total** | | **100** |

**Automatic deduction:** −5 per Valgrind error or leaked block, applied across the whole set.

---

## Answer Key (Instructor Copy)

### Problem 1 — Dynamic Memory (30 pts)

**Verification commands** (the rubric says "Valgrind-clean" — here is exactly what that means, confirmed on this machine):

```bash
gcc -Wall -Wextra -Werror -g -std=c11 -o prog prog.c
valgrind --leak-check=full --error-exitcode=1 ./prog
```

A passing run prints:

```
All heap blocks were freed -- no leaks are possible
ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)
```

A leaking run prints `definitely lost: N bytes in M blocks` and, with `--error-exitcode=1`, **exits non-zero** — so this drops straight into a marking script. Use-after-free surfaces separately as `Invalid read of size N`. (`gcc -fsanitize=address,undefined` is a faster alternative and reports `LeakSanitizer: detected memory leaks`; either is acceptable evidence.)

**4A Safe Heap Strings (10 pts).**
*Every function whose contract says "returns NULL on malloc failure" must actually **check** the `malloc` return before writing. Deduct 2 per unchecked allocation — the spec makes this explicit, so it is not a style nit.*
*`strlen` returns the length **without** the NUL, so every allocation must be `strlen(s) + 1`. Off-by-one here is the single most common defect and valgrind catches it as `Invalid write of size 1` — worth running even on submissions that look right.*
*"Caller must free" must be honoured by the student's own test harness too, or their program is not valgrind-clean regardless of library correctness.*

**1B Extending the Vec (15 pts).** Reference, compiled and run under Valgrind (clean); output as in the handout:

```c
/* vec_ext.c — PS 6 1B (reference): extending Lecture 03's Vec */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int   *data;
    size_t len;
    size_t cap;
} Vec;

void vec_init(Vec *v) { v->data = NULL; v->len = v->cap = 0; }
void vec_free(Vec *v) { free(v->data); v->data = NULL; v->len = v->cap = 0; }

static int vec_grow(Vec *v)
{
    size_t ncap = v->cap ? v->cap * 2 : 4;
    if (ncap > SIZE_MAX / sizeof *v->data) return -1;
    int *tmp = realloc(v->data, ncap * sizeof *v->data);
    if (!tmp) return -1;
    v->data = tmp;
    v->cap = ncap;
    return 0;
}

int vec_push(Vec *v, int value)
{
    if (v->len == v->cap && vec_grow(v) != 0) return -1;
    v->data[v->len++] = value;
    return 0;
}

/* Append every element of src to dst. 0 on success, -1 if an allocation failed. */
int vec_extend(Vec *dst, const Vec *src)
{
    size_t n = src->len;                 /* read first: dst and src may be the same Vec */
    for (size_t i = 0; i < n; i++)
        if (vec_push(dst, src->data[i]) != 0) return -1;
    return 0;
}

/* A new Vec with the elements in reverse order. Caller must vec_free it. */
Vec vec_reversed(const Vec *v)
{
    Vec r;
    vec_init(&r);
    for (size_t i = v->len; i-- > 0; )
        if (vec_push(&r, v->data[i]) != 0) { vec_free(&r); break; }
    return r;
}

/* Remove every element equal to value, in place, keeping order. Returns how many were removed. */
size_t vec_remove_value(Vec *v, int value)
{
    size_t w = 0;
    for (size_t r = 0; r < v->len; r++)
        if (v->data[r] != value) v->data[w++] = v->data[r];
    size_t removed = v->len - w;
    v->len = w;
    return removed;
}

/* Give back unused capacity: cap becomes len (or the buffer is freed when len == 0). */
int vec_shrink_to_fit(Vec *v)
{
    if (v->len == 0) { vec_free(v); return 0; }
    int *tmp = realloc(v->data, v->len * sizeof *v->data);
    if (!tmp) return -1;
    v->data = tmp;
    v->cap = v->len;
    return 0;
}

void vec_print(const Vec *v)
{
    printf("[");
    for (size_t i = 0; i < v->len; i++) printf(i ? ", %d" : "%d", v->data[i]);
    printf("] len=%zu cap=%zu\n", v->len, v->cap);
}

int main(void)
{
    Vec nums, more;
    vec_init(&nums);
    vec_init(&more);
    for (int i = 1; i <= 5; i++) vec_push(&nums, i);
    for (int i = 3; i <= 4; i++) vec_push(&more, i);
    vec_extend(&nums, &more);
    vec_print(&nums);
    vec_extend(&nums, &nums);                 /* self-extend */
    vec_print(&nums);
    Vec r = vec_reversed(&nums);
    vec_print(&r);
    printf("removed %zu\n", vec_remove_value(&nums, 3));
    vec_print(&nums);
    vec_shrink_to_fit(&nums);
    vec_print(&nums);
    Vec empty;
    vec_init(&empty);
    Vec er = vec_reversed(&empty);
    vec_print(&er);
    vec_free(&r); vec_free(&nums); vec_free(&more); vec_free(&er);
    return 0;
}
```

*3 per function. The two to probe:* **self-extend** — `vec_extend(&v, &v)` must read `src->len` once before
looping, or it never stops; and it works only because it reads `src->data[i]` through the struct after each
possible `realloc`. A version that caches `const int *p = src->data` before the loop reads freed memory as
soon as the buffer moves — Valgrind reports `Invalid read`. And `vec_shrink_to_fit` must use the
`tmp = realloc(...)` idiom: `v->data = realloc(v->data, …)` leaks the block if `realloc` fails.

---

### Problem 2 — Ownership by Contract (20 pts)

```c
/* Returns a newly allocated copy of `s`, or NULL. CALLER MUST FREE. */
char *str_dup(const char *s)
{
    if (!s) return NULL;
    size_t n = strlen(s) + 1;
    char *c = malloc(n);
    if (c) memcpy(c, s, n);
    return c;
}

/* At most `n` chars, always terminated. CALLER MUST FREE. */
char *str_ndup(const char *s, size_t n)
{
    if (!s) return NULL;
    size_t len = strnlen(s, n);
    char *c = malloc(len + 1);
    if (!c) return NULL;
    memcpy(c, s, len);
    c[len] = '\0';                /* strnlen never counts it -- add it here */
    return c;
}

void str_release(char **p)
{
    if (!p) return;
    free(*p);                     /* free(NULL) is a safe no-op */
    *p = NULL;
}
```

**Verified:** `str_dup("hello")` copies correctly and is a distinct allocation; `str_dup(NULL)`
returns NULL; `str_dup("")` returns a valid one-byte block. Valgrind clean.

**Requirement 4 — why `char **`.** Because pointers are passed **by value**. Given `char *p`, the
function receives a *copy* of the address; it can free the block, but assigning `p = NULL` changes
only the copy and the caller's variable still holds the dangling address. To modify the caller's
pointer you must be given that pointer's address, which is `char **`. *(This is Week 5's rule: to
modify a caller's `T`, take a `T *` — here `T` is `char *`.)*

**Marking notes.**

- **`str_dup("")` must not return NULL.** An empty string is a valid string; returning NULL conflates
  "empty" with "failed" and breaks every caller that checks for NULL as an error. −2 if wrong.
- **`c[len] = '\0'` in `str_ndup` is mandatory**, because `strnlen` stops at `n` without counting a
  terminator. A student using `strncpy` here must also terminate explicitly — Week 4's rule.
- **`if (!p) return;` in `str_release`** guards the outer pointer; `free(*p)` needs no guard because
  `free(NULL)` is defined.
- Accept `strdup` being unavailable as an excuse for nothing — it is POSIX, not C11, which is exactly
  why the problem asks students to write it.

---

### Problem 3 — A Container That Owns Its Contents (25 pts)

```c
int sv_push(StrVec *v, const char *s)
{
    if (v->len == v->cap) {
        size_t nc = v->cap ? v->cap * 2 : 4;
        if (nc > SIZE_MAX / sizeof *v->items) return -1;
        char **t = realloc(v->items, nc * sizeof *v->items);
        if (!t) return -1;                  /* v->items still valid */
        v->items = t;
        v->cap   = nc;
    }
    char *copy = str_dup(s);
    if (!copy) return -1;                   /* capacity grew, len did not: consistent */
    v->items[v->len++] = copy;
    return 0;
}

int sv_remove(StrVec *v, size_t i)
{
    if (i >= v->len) return -1;
    free(v->items[i]);
    memmove(&v->items[i], &v->items[i+1], (v->len - i - 1) * sizeof *v->items);
    v->len--;
    return 0;
}

void sv_free(StrVec *v)
{
    for (size_t i = 0; i < v->len; i++) free(v->items[i]);
    free(v->items);
    v->items = NULL;
    v->len = v->cap = 0;
}
```

**Verified:** 5 pushes grow the capacity 4 → 8, contents preserved, copies independent of the source
strings, `sv_free` resets the struct. Valgrind clean with `--show-leak-kinds=all`.

**Marking notes.**

- **Requirement 3 is the discriminating one.** Order matters: grow **first**, then duplicate. If the
  duplication fails after `len` has been incremented, the vector holds an uninitialised pointer that
  `sv_free` will later pass to `free` — a crash. The version above increments `len` only after the
  copy succeeds, so a failure leaves a vector with extra capacity and unchanged contents, which is
  consistent and usable.
- **`sv_push` must copy.** A version storing the caller's pointer directly is a different (and
  legitimate) design — but it is not the one specified, and it makes `sv_free` a double-free waiting
  to happen. −8 and explain the ownership contract.
- **`memmove`, not `memcpy`**, in `sv_remove` — the regions overlap. −2 for `memcpy`.
- **`sv_at` must bounds-check** and return NULL, not `v->items[i]` unconditionally.
- **Deduct −5 per Valgrind error**, per the set's stated policy. The commonest is forgetting to free
  the individual strings in `sv_free` and only freeing `items` — Valgrind reports it as *definitely
  lost*, one block per string.

---

### Problem 4 — Two-Dimensional Allocation (15 pts)

```c
int **make_matrix(size_t rows, size_t cols)
{
    int **m = calloc(rows, sizeof *m);
    if (!m) return NULL;
    for (size_t r = 0; r < rows; r++) {
        m[r] = calloc(cols, sizeof **m);
        if (!m[r]) {
            for (size_t k = 0; k < r; k++) free(m[k]);   /* unwind */
            free(m);
            return NULL;
        }
    }
    return m;
}

void free_matrix(int **m, size_t rows)
{
    if (!m) return;
    for (size_t r = 0; r < rows; r++) free(m[r]);
    free(m);
}
```

**Verified:** every cell of a 3×4 matrix is zero after allocation; writes work; `free_matrix(NULL,0)`
is safe; Valgrind clean.

**Why `calloc` — the two reasons (4 pts).**

1. **It zeroes the memory**, which requirement 1 demands, and for large blocks the OS supplies
   already-zero pages so it is often free.
2. **It checks `rows * sizeof *m` for overflow.** `malloc(rows * sizeof *m)` can wrap silently for a
   large `rows`, allocating a small block that the loop then writes far past — verified in Lecture 1
   that `SIZE_MAX/4 + 1` times 4 wraps to **exactly 0**.

Students giving only the zeroing reason get 2 of 4.

**Requirement 2 — the unwind (4 pts).** The inner `for (k < r)` loop is the whole marking point.
Returning NULL without freeing the rows already allocated leaks `r` blocks, and Valgrind reports each
one. This is the "error paths leak" lesson from Lecture 2.

**Requirement 4 — row-pointers vs flat (4 pts).**

| Layout | Advantage |
|---|---|
| **Row pointers** (`int **`) | Natural `m[r][c]` syntax; rows may differ in length (ragged arrays); rows can be swapped in O(1) by exchanging pointers |
| **Flat** (`int *`, `m[r*cols+c]`) | One allocation and one `free`; **contiguous**, so far better cache behaviour and it can be passed to code expecting a flat buffer; no pointer-chase per access |

*Full marks require one genuine advantage each.* The contiguity/cache point is the one that matters
in practice and is worth calling out if a student misses it.

---

### Problem 5 — Finding the Leak (10 pts)

*2 points each: 1 for the defect, 1 for the fix.*

| | Defect | Valgrind says | Fix |
|---|---|---|---|
| **(a)** | The pointer is overwritten with a string literal; the 10-byte block is unreachable | `10 bytes in 1 blocks are definitely lost` | Copy into it: `strcpy(s,"hello")` — or better `snprintf(s,10,"hello")`. Also: `s` now points at a literal, so a later `free(s)` would be an invalid free |
| **(b)** | `p = realloc(p, …)` — on failure the original block leaks and the only reference is destroyed | `definitely lost` on the allocation-failure path | Use a temporary: `void *t = realloc(p,n); if (t) p = t;` |
| **(c)** | The first allocation is overwritten by the second and never freed | `16 bytes in 1 blocks are definitely lost` | `free(a)` before reassigning, or use a second variable |
| **(d)** | `b` leaks on the `n < 0` early return: the error path skips `free` | `definitely lost: 100 bytes in 1 blocks` | `free(b)` before the early `return -1` (or validate `n` before allocating) |
| **(e)** | Double free — the allocator's metadata is corrupted | `Invalid free() / delete / delete[] / realloc()` | Free once; adopt `free(p); p = NULL;` so a second call is a safe no-op |

**Marking notes.**

- **(a)** has *two* defects — the leak and the fact that `s` afterwards points at read-only storage.
  Award the 2 for the leak; note the second in feedback as a bonus observation.
- **(d)** is the error-path leak, and it is the one students miss most often: every early `return` after a
  `malloc` needs its own `free`. (2026-09-21: the old version used `fopen`, which is Week 8.)
- **(b)** is Lecture 2's headline rule. If a student writes the fix without the temporary, they have
  not understood it.

---

*PROG 101 · Week 6 · Problem Set 6 · © CSE Department*
