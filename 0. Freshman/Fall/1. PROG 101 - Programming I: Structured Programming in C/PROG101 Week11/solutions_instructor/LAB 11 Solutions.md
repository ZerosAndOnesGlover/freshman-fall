# PROG 101 · Lab 11 Solutions (Instructor)
## Generic Programming in C

Reference implementations verified: comparator behaviour on `{INT_MAX, -2}`, the generic vector on
three element types including an owning struct, and callbacks with context. Valgrind clean.

---

## Part 1: The Comparator That Fails (5 pts)

### 1A — verified results

| Comparator | `{INT_MAX, -2}` after `qsort` |
|---|---|
| `cmp_bad` (subtraction) | `[2147483647, -2]` — **unsorted** |
| `cmp_ok` (`(l>r)-(l<r)`) | `[-2, 2147483647]` — sorted |

**UBSan report on the bad version:**

```
runtime error: signed integer overflow: 2147483647 - -2 cannot be represented in type 'int'
```

**Answer 3 (the marking point, 2 pts).** `cmp_bad` is correct **whenever `|a − b| ≤ INT_MAX`** — that
is, whenever the subtraction does not overflow. That covers every small test array anyone writes by
hand, which is exactly why the bug ships. It fails on wide-ranging data: timestamps, hashes, file
sizes, and any array containing both a large positive and a large negative value.

Students must state the *condition*, not just "it works on small numbers".

*Also worth crediting:* the result is not merely wrong, it is **undefined behaviour**, so the
compiler may transform the surrounding code on the assumption that it cannot happen.

### 1B — sorting strings (2 pts)

`qsort` passes the **address of the element**. The element is a `char *`, so the comparator receives
a pointer to a pointer — static type `const char *const *`.

```c
static int cmp_str(const void *a, const void *b)
{
    const char *const *l = a, *const *r = b;
    return strcmp(*l, *r);
}
```

**Passing `a` straight to `strcmp`** compares the *bytes of the pointer values* as if they were text
— reading whatever the addresses happen to look like, and running off the end since there is no
guaranteed terminator. It usually does not crash, which makes it worse.

---

## Part 2: A Generic Vector (8 pts)

```c
int gvec_push(GVec *v, const void *elem)
{
    if (v->len == v->cap) {
        size_t ncap = v->cap ? v->cap * 2 : 4;
        if (ncap > SIZE_MAX / v->elem_size) return -1;
        void *tmp = realloc(v->data, ncap * v->elem_size);
        if (!tmp) return -1;                       /* v->data still valid */
        v->data = tmp;
        v->cap  = ncap;
    }
    memcpy((char *)v->data + v->len * v->elem_size, elem, v->elem_size);
    v->len++;
    return 0;
}

void gvec_free(GVec *v)
{
    if (v->destroy)
        for (size_t i = 0; i < v->len; i++) v->destroy(gvec_at(v, i));
    free(v->data);
    v->data = NULL;
    v->len = v->cap = 0;
}
```

**Verified:** 10 pushes give `len=10 cap=16` (grown 4→8→16); works with `int`, `double`, and a
`Student { char *name; int score; }` whose `destroy` frees the name. Valgrind clean including the
owning case.

**Marking.**

| Criterion | Points |
|---|---|
| `memcpy` of `elem_size` bytes — never stores the caller's pointer | 2 |
| Doubling from 4 with the overflow guard | 2 |
| Temporary for `realloc`; failure leaves the vector usable | 1 |
| `destroy` called on every element, guarded by `if (v->destroy)` | 2 |
| Valgrind-clean on all three element types | 1 |

**`gvec_at` returns `void *`** because the container does not know the element type — it cannot
return a value of a type it has erased. The caller must **cast it back** to the correct pointer type
and dereference: `int x = *(int *)gvec_at(v, i);`. Nothing checks that the cast is right, which is
Part 4's subject.

**The recurring defect:** a `destroy` that frees the *element* as well as the string it owns. The
element lives inside `v->data`, so freeing it is a double free once `free(v->data)` runs. Verified in
Week 11 Lecture 3.

---

## Part 3: Callbacks with Context (4 pts)

```c
static void sum_ints(void *elem, void *ctx) { *(long *)ctx += *(int *)elem; }

long total = 0;
gvec_each(&v, sum_ints, &total);        /* verified: 1..10 gives 55 */
```

**Answer 3 (1 pt) — without `ctx`.** The accumulator would have to be a **global**. That makes the
function non-reentrant, impossible to use twice concurrently or with two different accumulators, and
awkward to test. The context pointer is C's explicit substitute for a closure: the function pointer
carries the code, `ctx` carries the captured environment.

*Award the mark only if the student names a concrete consequence (reentrancy, testability, or
concurrent use) rather than "globals are bad".*

---

## Part 4: The Cost of the Bargain (3 pts)

Expected observations:

**1. Pushing an `int` into a `double` vector.** It **compiles with no warning** — `gvec_push` takes
`const void *`, and any object pointer converts implicitly. It copies `sizeof(double)` = 8 bytes
starting at the address of a 4-byte `int`, so it reads 4 bytes past the variable and stores garbage.
Under ASan this is a stack-buffer-overflow read; without it, silent corruption.

**2. Wrong cast on `gvec_at`.** Also compiles silently, and reinterprets the bytes. Reading a
`double` element as an `int *` yields nonsense.

**3. `destroy = NULL` on owning structs.** Valgrind reports one *definitely lost* block **per
element** — the structs are freed with the buffer, but the strings they owned are not.

**The three-sentence summary (marking point).** Look for: C's generic mechanism costs **all static
type checking** — the compiler cannot verify that `elem_size`, the pushed type, and the cast on
retrieval agree, and a mismatch is silent. It also costs an indirect call per element and a cast at
every access. Templates or generics buy the checking back **at compile time**, generating a separate
correctly-typed implementation per type, at the cost of code size and compile time.

---

## Common Submission Problems

| Symptom | Cause | Action |
|---|---|---|
| Part 1 answered without running UBSan | Asserted rather than observed | −2 |
| `cmp_bad` described as "might overflow" | No condition given | −1; require `\|a−b\| ≤ INT_MAX` |
| `gvec_push` stores the pointer | Missed requirement 1 | −4; it is a different container |
| No overflow guard | Missed Week 6's lesson | −1 |
| Part 4 done by reasoning, not by running | The exercise is empirical | −2 |

---

*PROG 101 · Week 11 · Lab 11 Solutions · Instructor copy — do not distribute*
