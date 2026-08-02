# PROG 101 · Programming I: Structured Programming in C
## Week 6 · Problem Set 6: Pointers II — Dynamic Memory

**Released:** Friday, Week 6 · **Due:** Friday, Week 7 at 17:00
**Total:** 100 points
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

### 1B: Complete Dynamic Array Extension (15 pts)

Extend your Lab 3 `DynArray` with:

```c
/* dynarray_ext.h / dynarray_ext.c */

/* Append all elements of src to dst */
void da_extend(DynArray *dst, const DynArray *src);

/* Return a new DynArray containing elements of da where predicate(element) != 0.
 * Caller must call da_free on the result. */
DynArray da_filter(const DynArray *da, int (*predicate)(int));

/* Apply fn to every element in-place: da[i] = fn(da[i]) */
void da_map(DynArray *da, int (*fn)(int));

/* Return the sum of fn(element) for all elements.
 * Initial accumulator value is init. */
int da_reduce(const DynArray *da, int (*fn)(int, int), int init);

/* Return a new DynArray with elements in reverse order.
 * Caller must call da_free on the result. */
DynArray da_reversed(const DynArray *da);

/* Remove all elements where predicate(element) != 0, in-place. */
void da_remove_if(DynArray *da, int (*predicate)(int));

/* Return index of element for which key_fn returns minimum value.
 * Returns -1 if empty. */
int da_min_by(const DynArray *da, int (*key_fn)(int));
```

Demonstrate with:
```c
DynArray nums;
da_init(&nums);
for (int i = 1; i <= 10; i++) da_push(&nums, i);

/* Filter: keep only evens */
int is_even(int x) { return x % 2 == 0; }
DynArray evens = da_filter(&nums, is_even);
da_print(&evens);  /* [2, 4, 6, 8, 10] */

/* Map: square each element */
int square(int x) { return x * x; }
da_map(&evens, square);
da_print(&evens);  /* [4, 16, 36, 64, 100] */

/* Reduce: sum */
int add(int acc, int x) { return acc + x; }
int total = da_reduce(&evens, add, 0);
printf("Sum of squares of evens: %d\n", total);  /* 220 */

da_free(&evens);
da_free(&nums);
```

All must be Valgrind-clean.

---

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

/* (d) */  FILE *f = fopen(p,"r"); char *b = malloc(100); if (!b) return -1; fclose(f); free(b);

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

**4B Dynamic Array Extension (15 pts).**
*Growth must be **multiplicative** (doubling or ×1.5) — cross-reference CS 101 PS 6 B4, where additive growth is shown to give O(n) amortised appends instead of O(1).*
*The subtle one to probe: after `realloc`, **every previously held pointer into the buffer is invalid** — realloc may move the block. A submission that caches `&arr->data[i]` across an append has a latent use-after-free that valgrind will flag only if the block actually moves. Also require the `tmp = realloc(...); if (tmp) ptr = tmp;` idiom — assigning `ptr = realloc(ptr, …)` directly **leaks the original block** when realloc returns NULL.*

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
| **(d)** | `fopen`'s return is never checked; if it fails, `fclose(NULL)` is undefined. Also `f` leaks on the `!b` early return | `Invalid free()` / open file descriptor at exit | Check `f` immediately; `fclose(f)` before the early `return -1` |
| **(e)** | Double free — the allocator's metadata is corrupted | `Invalid free() / delete / delete[] / realloc()` | Free once; adopt `free(p); p = NULL;` so a second call is a safe no-op |

**Marking notes.**

- **(a)** has *two* defects — the leak and the fact that `s` afterwards points at read-only storage.
  Award the 2 for the leak; note the second in feedback as a bonus observation.
- **(d)** is the error-path leak, and it is the one students miss most often: they spot the unchecked
  `fopen` and not the `f` still open at the early return.
- **(b)** is Lecture 2's headline rule. If a student writes the fix without the temporary, they have
  not understood it.

---

*PROG 101 · Week 6 · Problem Set 6 · © CSE Department*
