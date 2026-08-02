# PROG 101 — Week 11 Reference
## Function Pointers and Generic Programming

---

## Function Pointers

```c
int (*p)(int, int) = add;    /* pointer to function; no & needed */
p(3, 4);                     /* call -- (*p)(3,4) is identical   */
typedef int (*BinOp)(int, int);
```

**The parentheses are load-bearing:**

```c
int *f(int);      /* FUNCTION returning int*  */
int (*p)(int);    /* POINTER to function      */
```

**Right-left rule:** start at the identifier, go right when you can, left when you must, parentheses
override.

| | |
|---|---|
| `add` == `&add` | Function names decay to pointers |
| `sizeof(int (*)(int))` | **8** — it is a pointer |
| Arithmetic on it | **None.** Functions are not an array |
| Conversion to `void *` | **Not guaranteed** by C (POSIX adds it for `dlsym`) |
| Captures anything? | **No.** Pass a context pointer |

---

## Dispatch Tables

```c
Handler transition[S_COUNT] = { h_idle, h_run, h_done };
if (s < 0 || s >= S_COUNT) return ERROR;   /* MUST bounds-check */
return transition[s](input);
```

Turns a branch into an index. **A structure win, not a speed win** — a dense `switch` already
compiles to a jump table. Adding a case becomes one row; the dispatch code never changes.

**Indexing out of range calls through garbage** — a wild jump. The bounds check is what makes the
table safe.

---

## `void *` and Type Erasure

```c
int  x = 42;
void *v = &x;      /* no cast needed either way */
int  *back = v;
```

C11 §6.3.2.3 guarantees the round trip for **object** pointers. What is lost: the type, the size, and
every operation. Generic code takes those back as parameters:

```c
void qsort(void *base, size_t nmemb, size_t size,
           int (*compar)(const void *, const void *));
```

**Three of the four parameters exist to replace what `void *` destroyed.**

**Byte arithmetic:** cast to `char *` first — `sizeof(char)` is 1 by definition. `void *` arithmetic
is a GNU extension and `-pedantic` rejects it.

---

## Comparators

**The contract:** negative if the first sorts before the second, zero if equivalent, positive if
after. Must be **consistent** and **transitive** — an inconsistent comparator is undefined behaviour
and can drive the sort out of bounds.

```c
/* CORRECT for every input */
int cmp(const void *a, const void *b)
{ int l=*(const int*)a, r=*(const int*)b; return (l>r)-(l<r); }

/* BROKEN: signed overflow is UNDEFINED */
int cmp_bad(const void *a, const void *b)
{ return *(const int*)a - *(const int*)b; }
```

**Verified:** sorting `{INT_MAX, -2}` with `cmp_bad` leaves the array **unsorted**. UBSan:
`signed integer overflow: 2147483647 - -2 cannot be represented in type 'int'`.

| Element type | Comparator receives | Get the value with |
|---|---|---|
| `int` | `const int *` | `*(const int *)a` |
| `char *` | `const char *const *` | `strcmp(*l, *r)` |
| `struct T` | `const T *` | `x->field` |

**Multi-key:** return early on the first key that discriminates.

```c
int c = (y->score > x->score) - (y->score < x->score);
return c ? c : strcmp(x->name, y->name);
```

**`qsort` is not guaranteed stable.** If you need it, add the original index as a final key.

**`bsearch`:** the array must already be sorted by the same comparator; pass `&key`; the return is a
**pointer**, not an index.

---

## Callbacks and Context

A function pointer captures nothing. Pass the environment explicitly:

```c
typedef void (*EachFn)(void *elem, void *ctx);
void each(const Vec *v, EachFn f, void *ctx);   /* ctx passed through untouched */
```

**Always include a context parameter** in any API taking a callback. Callers who do not need it pass
NULL; without it, every caller is forced into globals — non-reentrant and untestable — and it cannot
be added later without breaking every existing call.

---

## Ownership in Generic Containers

`void *` erased the type, so the container cannot know whether elements own memory. Hand the
knowledge back:

```c
typedef void (*FreeFn)(void *elem);
if (v->destroy) for (size_t i=0;i<v->len;i++) v->destroy(vec_at(v,i));
free(v->data);
```

The `if (v->destroy)` guard matters — calling through a NULL function pointer is undefined.

A `destroy` for a struct owning a string frees **the string, not the element** — the element lives
inside the container's own buffer.

---

## The Bargain

| You get | You give up |
|---|---|
| One implementation for every type | **No type checking** — pushing an `int` into a `double` vector compiles |
| Runtime-selectable behaviour | An indirect call per element, rarely inlined |
| Genuine code reuse | A cast at every access |

C gives you the mechanism and trusts you. Knowing precisely what you traded is the point.

---

*PROG 101 · Week 11 · Reference · © CSE Department*
