# PROG 101 · Programming I: Structured Programming in C
## Week 6 · Problem Set 6: Pointers II — Dynamic Memory

**Released:** Friday 6 November 2026, 10:00 · Week 6 (after Thursday's Lecture 3)
**Due:** Friday 13 November 2026, 17:00 · Week 7 — late penalty from 17:01
**Submission:** Commit to the Freshman Fall repo under `"$PROG101/week6/ps6"`; submit the commit hash on the course portal.
**Total:** 100 points · **Expected time:** about 3 hours

*(Revised 2026-09-26: cut from about five hours to three in the Midterm 1 week. Lab 6, on Monday 9 November,
builds a dynamic array and reads Valgrind reports, so old 1B (extending `Vec`) and Problem 5 (finding the
leak) are now only in the lab. Old 1A went because its `str_dup` was Problem 2's `str_dup` again; the
smaller `strdup_lib` stays, since the string vector links against it. The answer key moved out of this
handout.)*
**What this uses:** Weeks 0–6, including the `typedef struct` `Vec` that Lecture 03 builds.
**Not needed:** function pointers (Week 11), files (Week 8), the rest of `struct` (Week 7).
**Build with:** `gcc -Wall -Wextra -Werror -pedantic -std=c11 -g`
**Check with:** `valgrind --leak-check=full --show-leak-kinds=all --error-exitcode=1`

> **Every submission must be Valgrind-clean.** Zero errors, zero bytes definitely lost. A leak is a
> defect, and it is graded as one.
>
> Every allocation needs a visible, reachable `free` — **including on error paths**.

---
## Problem 1: Ownership by Contract (25 pts)

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
| `str_dup` correct incl. NULL and empty-string cases | 8 |
| `str_ndup` correct and always terminated | 7 |
| `str_release` correct, and the `char **` explanation | 6 |
| Ownership comments present and accurate | 4 |

---

## Problem 2: A Container That Owns Its Contents (45 pts)

Use your Problem 1 `str_dup` for the copies.

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
| `sv_push` copies, grows correctly, is overflow-guarded | 14 |
| Failure leaves the vector consistent (requirement 3) | 9 |
| `sv_remove` correct, order-preserving, frees the element | 9 |
| `sv_free` releases everything; Valgrind-clean under test | 9 |
| Tests exercise push/remove/free | 4 |

---

## Problem 3: Two-Dimensional Allocation (30 pts)

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
   indexed as `m[r*cols + c]`: give one advantage of each. *(8 of the 30 pts.)*

---

## Makefile

```makefile
CC     = gcc
CFLAGS = -Wall -Wextra -Werror -g -std=c11

PROGRAMS = test_strdup_lib test_strvec matrix

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
| 1 | Ownership by Contract | 25 |
| 2 | A Container That Owns Its Contents | 45 |
| 3 | Two-Dimensional Allocation | 30 |
| **Total** | | **100** |

**Automatic deduction:** −5 per Valgrind error or leaked block, applied across the whole set.

---

*PROG 101 · Week 6 · Problem Set 6 · Due Friday 13 November 2026, 17:00 · © CSE Department*
