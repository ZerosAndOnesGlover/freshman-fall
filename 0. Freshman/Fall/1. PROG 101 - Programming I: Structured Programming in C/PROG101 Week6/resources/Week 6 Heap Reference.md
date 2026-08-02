# PROG 101 · Week 6 Reference
## Dynamic Memory

---

## The Address Space

Verified ordering (low → high): **text/literals · globals · heap · … · stack**

The heap grows **upward**, the stack **downward**. String literals live in read-only text —
`char *s = "hi"; s[0] = 'H';` is undefined behaviour.

| Region | Lifetime | Size fixed at |
|---|---|---|
| Text | Program | Compile time |
| Data / BSS | Program | Compile time |
| **Heap** | Until `free` | **Run time** |
| Stack | Enclosing block | Run time (8 MB limit) |

---

## Allocation

```c
int *p = malloc(n * sizeof *p);       /* uninitialised; NULL on failure */
int *q = calloc(n, sizeof *q);        /* ZEROED, and checks n*size      */
void *t = realloc(p, m * sizeof *p);  /* preserves contents up to min   */
free(p);
```

| | |
|---|---|
| `sizeof *p` not `sizeof(int)` | Survives a change of type |
| **Do not cast** `malloc` | `void *` converts implicitly; the cast is a C++ habit |
| `malloc` does **not** zero | Verified: 5 of 16 bytes nonzero |
| `malloc(0)` | Implementation-defined; safe to `free` |
| `calloc` checks overflow | `SIZE_MAX/4+1` × 4 wraps to **exactly 0** — verified |
| `realloc(NULL, n)` | Behaves as `malloc` |
| `free(NULL)` | Guaranteed safe no-op |

---

## The Two Rules

**1. Never `p = realloc(p, n);`**

On failure `realloc` returns NULL **and leaves the original allocated**. Assigning back destroys your
only reference — leak plus data loss.

```c
void *t = realloc(p, n);
if (!t) { /* p still valid; recover */ }
else      p = t;
```

**2. `free(p); p = NULL;`**

`free` receives a *copy* of the pointer and cannot null your variable. Nulling it turns a
use-after-free into an immediate fault and a double free into a safe no-op.

---

## Ownership

C provides no help. State the contract in a comment:

```c
/* Returns a newly allocated string. CALLER MUST FREE. */
char *str_dup(const char *s);

/* Takes ownership of `name`; released by list_destroy. */
int list_add(List *l, char *name);
```

| Failure | Cause |
|---|---|
| **Leak** | Nobody freed it |
| **Double free / use-after-free** | Two parties both thought they owned it |

**Error paths are where leaks live.** Every early `return` must free what it has already allocated.

---

## Growth

```c
size_t ncap = cap ? cap * 2 : 4;
if (ncap > SIZE_MAX / sizeof *data) return -1;      /* overflow guard */
T *tmp = realloc(data, ncap * sizeof *data);
if (!tmp) return -1;
data = tmp; cap = ncap;
```

**Doubling gives amortised O(1)** — total copying < 2n, verified up to n = 100,000.
**Fixed increment gives Θ(n²).**

A pointer into the block **dangles after any growth**. Keep indices, not pointers.

---

## Tooling

```bash
gcc -Wall -Wextra -Werror -pedantic -std=c11 -g -O0 prog.c -o prog
valgrind --leak-check=full --show-leak-kinds=all --error-exitcode=1 ./prog
gcc -fsanitize=address,undefined -g prog.c -o prog_san
```

| Valgrind message | Meaning |
|---|---|
| `N bytes in 1 blocks are definitely lost` | A leak |
| `Invalid read/write of size N` | Out of bounds, or after `free` |
| `Invalid free() / delete / delete[] / realloc()` | Double free, or freeing a non-allocated address |
| `Conditional jump ... depends on uninitialised value(s)` | Read before write |
| `still reachable` | Not freed at exit but still pointed to — usually benign |

**ASan does not detect uninitialised reads. Valgrind does.** Run both.

---

*PROG 101 · Week 6 · Reference · © CSE Department*
