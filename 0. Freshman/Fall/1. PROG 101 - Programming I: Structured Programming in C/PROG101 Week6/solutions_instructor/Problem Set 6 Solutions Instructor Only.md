# PROG 101 · Problem Set 6 Solutions
## INSTRUCTOR ONLY — DO NOT DISTRIBUTE

*Moved 2026-09-26 out of the student handout, where it had been printed below the questions.*

---

*(Revised 2026-09-26: the set now has three problems. Old 2 → 1 (25: 8/7/6/4), old 3 → 2 (45: 14/9/9/9/4), old
4 → 3 (30, 8 for the layout comparison). Old 1A, 1B and 5 are no longer asked; their answers below can be ignored.)*

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
