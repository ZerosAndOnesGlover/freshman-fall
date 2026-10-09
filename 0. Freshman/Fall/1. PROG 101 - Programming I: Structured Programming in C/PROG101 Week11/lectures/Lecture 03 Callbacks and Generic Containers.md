# PROG 101 · Programming I: Structured Programming in C
## Week 11 · Lecture 3: Callbacks and Generic Containers

*“It is the user who should parameterize procedures, not their creators.”* — Alan Perlis, "Epigrams on Programming" (1982), #76

**Date:** Thursday 10 December 2026 · 10:00–10:50 · Week 11

**Reading:** K&R, §5.11, §6.5 · `man 3 realloc` · `man 3 qsort_r` *(details at the end of the lecture)*

**Coursework:** 📝 **PS 10** due Fri 11 Dec 17:00 · 📝 **PS 11** released Fri 11 Dec 10:00, due Fri 18 Dec 17:00 · 🔬 **Lab 11** Mon 14 Dec 15:00–16:50 · 📊 **Quiz 11** Tue 15 Dec 10:00–10:10 · 📕 **Final exam** Thu 24 Dec 14:00

---

## Lecture Goals

By the end of this lecture you can:

- Pass state to a callback using a context pointer — C's substitute for a closure
- Reason about **ownership**: who frees what, and when
- Build a generic dynamic array that holds any type, including types that own memory
- Explain why `realloc`'s return value must never be assigned to the old pointer

---

## 1. The Problem with Bare Callbacks

Lecture 1 said a function pointer captures nothing. Here is why that hurts.

Suppose you want to apply an operation to every element of an array:

```c
typedef void (*EachFn)(int *elem);

static void each(int *a, size_t n, EachFn f)
{
    for (size_t i = 0; i < n; i++) f(&a[i]);
}
```

Now sum the elements. Where does the running total live? The callback receives only the element, so
the total has to be a global:

```c
static long total;                      /* ugh */
static void add_to_total(int *e) { total += *e; }
```

Globals make the function non-reentrant, untestable in parallel, and impossible to use twice at once.
This is the problem closures solve in other languages, and C has no closures.

---

## 2. The Context Pointer

The fix is one extra parameter, carried through untouched:

```c
typedef void (*EachFn)(void *elem, void *ctx);

static void vec_each(const Vec *v, EachFn f, void *ctx)
{
    for (size_t i = 0; i < v->len; i++) f(vec_at(v, i), ctx);
}
```

`vec_each` never looks inside `ctx`. It only hands it back. The caller decides what it means:

```c
static void sum_ints(void *elem, void *ctx) { *(long *)ctx += *(int *)elem; }

long total = 0;
vec_each(&vi, sum_ints, &total);
```

Verified on 1..10: `sum via callback+ctx = 55  (expected 55)`.

**That is the closure, made explicit.** A closure is code plus captured environment; here the code is
the function pointer and the environment is `ctx`. C makes you carry the environment by hand.

The pattern is everywhere once you see it:

| API | Callback | Context |
|---|---|---|
| `qsort_r` (GNU/BSD) | comparator | `void *arg` |
| POSIX threads | `void *(*start)(void *)` | the `void *` argument |
| `signal` / `sigaction` | handler | *(none — the reason signal handlers are painful)* |
| GTK, libcurl, SQLite | every hook | a `user_data` pointer |

When you design an API that takes a callback, **always include a context pointer.** It costs one
parameter and callers who do not need it pass `NULL`. Omitting it forces every caller into globals,
and you cannot add it later without breaking every existing call.

---

## 3. Ownership

Generic containers force a question you have been able to dodge until now: **who frees the elements?**

Consider a vector of `int`. Nothing to free — the elements are plain data living inside the
vector's own buffer.

Now a vector of:

```c
typedef struct { char *name; int score; } Student;
```

Each `Student` owns a `malloc`'d `name`. Freeing the vector's buffer releases the `Student` structs
but **leaks every `name`**. The container cannot know this: `void *` erased the type, so it has no
idea the struct contains a pointer.

So we hand the knowledge back, exactly as §2 of Lecture 2 predicted:

```c
typedef void (*FreeFn)(void *elem);

typedef struct {
    void   *data;
    size_t  len, cap, elem_size;
    FreeFn  destroy;          /* NULL for plain data */
} Vec;
```

```c
static void vec_free(Vec *v)
{
    if (v->destroy)
        for (size_t i = 0; i < v->len; i++) v->destroy(vec_at(v, i));
    free(v->data);
    v->data = NULL; v->len = v->cap = 0;
}
```

The `if (v->destroy)` guard is the line Lecture 1 promised you would write: calling through a null
function pointer is undefined behaviour, and `NULL` is the legitimate "nothing to do" value.

```c
static void free_student(void *e) { free(((Student *)e)->name); }
```

Note it frees `name` but **not** `e` itself — the struct lives inside the vector's buffer, which
`free(v->data)` releases. Freeing `e` would be a double free of memory the vector never separately
allocated.

### Stating the contract

Every container needs its ownership rule written down, because it cannot be inferred:

> `vec_push` **copies** `elem_size` bytes into the vector. The vector then owns that copy. If the
> element contains pointers, the vector owns those too, and `destroy` must release them.

That is a *transfer of ownership*. The caller must not free what it pushed:

```c
Student s;
s.name = malloc(strlen(names[i]) + 1);
strcpy(s.name, names[i]);
s.score = scores[i];
vec_push(&vs, &s);        /* vector now owns s.name -- do NOT free it here */
```

Get this wrong in either direction and you get a double free or a leak. Both are silent until they
are not.

---

## 4. The Generic Vector

Here it is in full. This is the code you will extend in Lab 8.

```c
static int vec_init(Vec *v, size_t elem_size, FreeFn destroy)
{
    v->data = NULL; v->len = 0; v->cap = 0;
    v->elem_size = elem_size; v->destroy = destroy;
    return 0;
}

static void *vec_at(const Vec *v, size_t i)
{
    assert(i < v->len);
    return (char *)v->data + i * v->elem_size;   /* Lecture 2 §6 */
}

static int vec_push(Vec *v, const void *elem)
{
    if (v->len == v->cap) {
        size_t ncap = v->cap ? v->cap * 2 : 4;
        void *nd = realloc(v->data, ncap * v->elem_size);
        if (!nd) return -1;                      /* old buffer still valid */
        v->data = nd; v->cap = ncap;
    }
    memcpy((char *)v->data + v->len * v->elem_size, elem, v->elem_size);
    v->len++;
    return 0;
}
```

Verified: pushing 1..10 gives `len=10 cap=16`, having grown 4 → 8 → 16. Valgrind and ASan both clean.

### The `realloc` rule

```c
void *nd = realloc(v->data, ncap * v->elem_size);
if (!nd) return -1;
v->data = nd;
```

**Never write `v->data = realloc(v->data, ...)`.** If `realloc` fails it returns `NULL` *and leaves
the original block allocated*. Assigning straight back overwrites your only pointer to it — the
memory is now unreachable and leaked, and you have destroyed the data you were trying to grow.

Using a temporary means failure is recoverable: the old buffer is intact and the vector is still
valid, so returning `-1` leaves the caller with a working container.

This is one of the most common C bugs and one of the easiest to avoid.

### Growth by doubling

`cap = cap ? cap * 2 : 4` gives **amortised O(1)** `push`. Doubling means n pushes trigger
log₂(n) reallocations copying 1 + 2 + 4 + … + n < 2n elements total, so the per-push average is
constant.

Growing by a fixed amount instead (`cap + 4`) makes it Θ(n²) — the same arithmetic as the string
concatenation you will meet in CS 101 Week 9.

---

## 5. It Really Is Generic

The same `Vec` code, unchanged, holding `Student` structs that own memory:

```c
Vec vs;
vec_init(&vs, sizeof(Student), free_student);
/* ... push four students ... */
qsort(vs.data, vs.len, vs.elem_size, cmp_student);
vec_each(&vs, print_student, NULL);
vec_free(&vs);
```

Verified output:

```
before sort:
    ada       91
    grace     97
    linus     84
    ken       88
after qsort (descending by score):
    grace     97
    ada       91
    ken       88
    linus     84
```

Valgrind: **no leaks, no errors.** ASan and UBSan: clean.

Note that `qsort` works directly on `vs.data` — the vector's fields are exactly `qsort`'s first three
parameters, because both are built on the same "pointer, count, element size" representation. That is
not a coincidence; it is the standard C idiom for a run of homogeneous objects.

### What you have actually built

Compare with Week 7's linked list of `int`. To store `double` you copied the file and changed the
type. To store `Student` you copied it again. Three near-identical files, three places to fix every
bug.

The generic vector is written **once**. The cost is:

- No type checking — pushing an `int` into a `Vec` of `Student` compiles cleanly and corrupts memory
- An indirect call per element for callbacks, which the compiler usually cannot inline
- Every access needs a cast

That is C's bargain. C++ templates and Rust generics buy the type safety back at compile time; C
gives you the mechanism and trusts you. Knowing precisely what you gave up is the point of this
lecture.

---

## 6. Summary

| Idea | Takeaway |
|---|---|
| Bare callbacks force globals | A function pointer captures nothing |
| Context pointer | `void *ctx` carried through untouched — the closure, made explicit |
| Always include `ctx` | Costs one parameter; cannot be added later without breaking callers |
| Ownership must be stated | The container cannot infer it — `void *` erased the type |
| `destroy` callback | Hands back the knowledge the type erasure destroyed |
| `if (v->destroy)` | `NULL` means "nothing to do"; calling it would be UB |
| `free_student` frees `name`, not `e` | The struct lives in the vector's buffer |
| **Never** `p = realloc(p, ...)` | On failure you leak the original and lose your only pointer |
| Doubling growth | Amortised O(1); fixed-increment growth is Θ(n²) |
| The bargain | One implementation, no type safety — know what you traded |

---

## Practice Exercises

Attempt each before reading the answers.

**1. (Trace.)** `vec_push` is called 20 times on a fresh vector. List every capacity value the vector
takes, and state how many `realloc` calls happened.

**2. (Explain.)** Why does `free_student` free `e->name` but not `e`? What happens if it frees both?

**3. (Build.)** Write `vec_pop(Vec *v, void *out)`: remove the last element, copying it into `out` if
`out` is non-NULL. State what must happen about `destroy` and justify it.

**4. (Stretch.)** Write `vec_filter(Vec *v, int (*pred)(const void *elem, void *ctx), void *ctx)`
which removes every element for which `pred` returns 0. It must not leak, must be O(n), and must
call `destroy` exactly once on each removed element.

### Answers

**1.** Capacities: **4, 8, 16, 32.**

| Push | Trigger | New capacity |
|---|---|---|
| 1 | `cap == 0` | 4 |
| 5 | `len == cap == 4` | 8 |
| 9 | `len == cap == 8` | 16 |
| 17 | `len == cap == 16` | 32 |

**Four `realloc` calls.** The first is `realloc(NULL, ...)`, which is equivalent to `malloc` — the
standard defines it that way, which is why `vec_init` can leave `data` as `NULL` and `vec_push` needs
no special case for the first insertion.

Final state after 20 pushes: `len = 20`, `cap = 32`. Verified at 10 pushes: `len=10 cap=16`.

**2.** Because they were allocated by **different owners**.

`e->name` came from its own `malloc` and nothing else will free it — so `destroy` must.

`e` itself is **not a separate allocation**. It is a pointer *into the middle of* `v->data`, the one
buffer the vector allocated. The elements are laid out contiguously inside it.

Freeing both is undefined behaviour on the second free: you would be passing `free` a pointer that
was never returned by `malloc` (unless the element happens to be at index 0, where it points at the
start of the buffer — which is arguably worse, because then it *looks* valid, frees the whole buffer
early, and every subsequent element access is a use-after-free). Then `free(v->data)` in `vec_free`
frees it again.

Under Valgrind this reports `Invalid free() / delete / delete[] / realloc()`. In production it
corrupts the allocator's metadata and crashes somewhere unrelated.

**3.**

```c
static int vec_pop(Vec *v, void *out)
{
    if (v->len == 0) return -1;
    v->len--;
    void *last = (char *)v->data + v->len * v->elem_size;
    if (out) {
        memcpy(out, last, v->elem_size);
        return 0;                     /* ownership TRANSFERRED to caller */
    }
    if (v->destroy) v->destroy(last); /* nobody took it -- destroy it */
    return 0;
}
```

**The `destroy` rule is the whole exercise.** It depends on whether the caller took the element:

- **`out` is non-NULL** — the element has been handed to the caller, who now owns it and must
  eventually release any memory it holds. The vector must **not** call `destroy`; doing so would
  hand the caller a struct whose `name` pointer is already freed — a use-after-free waiting to
  happen.
- **`out` is NULL** — the element is being discarded and nobody else has a reference. The vector
  **must** call `destroy`, or every pointer inside the element leaks.

Note `v->len--` happens before computing `last`, which is why the index is `v->len` and not
`v->len - 1`. And this must be documented, because a caller cannot guess it.

**4.**

```c
static void vec_filter(Vec *v, int (*pred)(const void *, void *), void *ctx)
{
    size_t w = 0;                                     /* write cursor */
    for (size_t r = 0; r < v->len; r++) {             /* read cursor  */
        void *src = (char *)v->data + r * v->elem_size;
        if (pred(src, ctx)) {
            if (w != r)
                memcpy((char *)v->data + w * v->elem_size, src, v->elem_size);
            w++;
        } else if (v->destroy) {
            v->destroy(src);                          /* exactly once */
        }
    }
    v->len = w;
}
```

This is the **two-cursor compaction** idiom, and it satisfies all three requirements:

- **O(n)** — one pass, each element examined once. Removing elements one at a time with a shift
  would be O(n²).
- **`destroy` exactly once per removed element** — called in the `else` branch, at the moment the
  element is passed over. Survivors are never destroyed; they are moved.
- **No leak** — every element is either copied forward (still owned by the vector) or destroyed.

The `if (w != r)` guard skips self-copies. It is not merely an optimisation: `memcpy` with
overlapping source and destination is undefined behaviour, and when `w == r` they are the same
address. `memmove` would also be correct, but avoiding the call entirely is clearer.

Capacity is deliberately left unchanged — shrinking would mean another `realloc` and would surprise
a caller who is about to push again.

---

## Reading

- **K&R, §5.11, §6.5** — function pointers and self-referential structures
- **`man 3 realloc`** — read the RETURN VALUE section; the failure behaviour is the point
- **`man 3 qsort_r`** — the GNU/BSD variant that takes a context pointer, and why it exists

---

*PROG 101 · Week 11 · Lecture 3 · © CSE Department*
