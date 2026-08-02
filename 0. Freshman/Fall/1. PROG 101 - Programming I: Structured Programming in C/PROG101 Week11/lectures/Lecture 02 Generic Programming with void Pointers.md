# PROG 101 · Programming I: Structured Programming in C
## Week 11 · Lecture 2: Generic Programming with `void *`

---

## Lecture Goals

By the end of this lecture you can:

- Explain what `void *` guarantees and what it destroys
- Use `qsort` and `bsearch` correctly on any type
- Write a comparator that is correct for **all** inputs, not just the ones you tested
- Explain why `return a - b;` is a bug, and demonstrate it

---

## 1. Type Erasure

Lecture 1 made *code* passable. This lecture makes *data* passable.

`void *` is a pointer to memory of unspecified type. It is C's one escape hatch from the type
system:

```c
int   x = 42;
void *v = &x;        /* no cast needed on the way in  */
int  *back = v;      /* no cast needed on the way out */
printf("%d\n", *back);   /* 42 */
```

Verified: `int* -> void* -> int* : 42`. C11 §6.3.2.3 guarantees this round trip for any **object**
pointer — convert to `void *` and back and you get the original pointer.

What you lose is everything else. A `void *` does not know:

- what type it points to
- how many bytes the object occupies
- how to compare, copy, print, or destroy it

So generic code in C works by taking those back as **explicit parameters**. That is the entire
design pattern of this lecture:

> Erase the type, then hand back the operations you erased.

`qsort` is the canonical example, and it is worth reading its signature as a sentence.

---

## 2. `qsort`

```c
void qsort(void *base, size_t nmemb, size_t size,
           int (*compar)(const void *, const void *));
```

| Parameter | Meaning | Why it is needed |
|---|---|---|
| `base` | address of the first element | the data, type erased |
| `nmemb` | how many elements | erased type cannot tell you |
| `size` | bytes per element | erased type cannot tell you |
| `compar` | how to order two of them | erased type cannot tell you |

Four parameters, and three of them exist purely to replace what `void *` threw away.

```c
static int cmp_int(const void *x, const void *y)
{
    int l = *(const int *)x, r = *(const int *)y;
    return (l > r) - (l < r);
}

int a[] = { 5, -3, 12, 0, 7, -8, 12 };
qsort(a, sizeof a / sizeof a[0], sizeof a[0], cmp_int);
```

Verified output: `-8 -3 0 5 7 12 12`

### The contract

The comparator must return:

- **negative** if the first argument sorts **before** the second
- **zero** if they are equivalent
- **positive** if the first sorts **after** the second

Note "negative", not "−1". Any negative value will do, which is what tempts people into the bug in §3.

The comparator must also be **consistent**: if `cmp(a,b) < 0` then `cmp(b,a) > 0`, and ordering must
be transitive. An inconsistent comparator does not merely mis-sort — it can drive the sort out of
bounds. The standard says the behaviour is undefined, and glibc's introsort will happily run off the
end of the array.

### Casting inside the comparator

```c
int l = *(const int *)x;
```

Read it right to left: take `x` (a `const void *`), treat it as `const int *`, dereference. Keep the
`const` — dropping it is a warning under `-Wall`, and the comparator has no business modifying the
array it is ordering.

---

## 3. The Subtraction Trap

This comparator appears in countless tutorials:

```c
static int cmp_bad(const void *x, const void *y)
{
    return *(const int *)x - *(const int *)y;   /* WRONG */
}
```

It is concise, it looks clever, and it is **broken**.

Subtraction of two `int`s can overflow, and signed overflow in C is **undefined behaviour**. When
the true difference exceeds `INT_MAX`, the result is not merely wrong — the program has no defined
meaning.

Verified, sorting the two-element array `{ INT_MAX, -2 }`:

```
a = 2147483647, b = -2   -> a is clearly GREATER
true difference          = 2147483649
correct (l>r)-(l<r)      = 1   <- positive, correct

qsort with cmp_bad gives: [2147483647, -2]   <- WRONG ORDER
qsort with cmp_ok  gives: [-2, 2147483647]   <- sorted
```

The bad comparator leaves the array **unsorted**. UBSan names the cause exactly:

```
runtime error: signed integer overflow: 2147483647 - -2 cannot be represented in type 'int'
```

**Why this bug survives.** It is correct whenever `|a − b| ≤ INT_MAX`, which covers every small test
array anyone writes. It fails only on wide-ranging data — timestamps, hashes, file sizes, sentinel
values like `INT_MIN`. It ships, and then it corrupts a sort in production on data nobody tested.

### The correct idiom

```c
return (l > r) - (l < r);
```

Two comparisons, each yielding 0 or 1, subtracted. The result is exactly −1, 0, or +1, and no
arithmetic on the values themselves ever happens. It cannot overflow **for any input**.

If you find it cryptic, the explicit form is equally good and compiles to the same thing:

```c
if (l < r) return -1;
if (l > r) return  1;
return 0;
```

**Subtraction is safe only when you can prove the range is bounded** — for example comparing two
`unsigned char` values, or array indices you know are small. When in doubt, use the idiom.

---

## 4. Comparators for Real Types

### Strings

```c
static int cmp_str(const void *a, const void *b)
{
    /* array of char*: each element IS a char*, so a is a char** */
    const char *const *l = a, *const *r = b;
    return strcmp(*l, *r);
}
```

The double indirection is where people slip. `qsort` hands you the **address of the element**. If
the element is itself a `char *`, then the address of it is a `char **`.

`strcmp` already returns negative/zero/positive, so it can be returned directly — and it is safe,
because it compares `unsigned char` values and returns a bounded difference.

### Structs, ordering by a field

```c
typedef struct { char *name; int score; } Student;

static int by_score_desc(const void *a, const void *b)
{
    const Student *x = a, *y = b;
    return (y->score > x->score) - (y->score < x->score);   /* y first: descending */
}
```

Swapping `x` and `y` reverses the order. Verified on four students:

```
before sort:  ada 91 · grace 97 · linus 84 · ken 88
after  sort:  grace 97 · ada 91 · ken 88 · linus 84
```

### Multi-key ordering

Sort by score descending, then by name ascending for ties:

```c
static int by_score_then_name(const void *a, const void *b)
{
    const Student *x = a, *y = b;
    int c = (y->score > x->score) - (y->score < x->score);
    if (c) return c;                    /* primary key decided it */
    return strcmp(x->name, y->name);    /* tie-break              */
}
```

**Return early on the first key that discriminates.** This pattern extends to any number of keys and
is how you get a total order out of several partial ones.

### A note on stability

`qsort` is **not guaranteed stable** — equal elements may be reordered. The C standard says nothing
about it.

Tested on eight records with identical keys, glibc preserved the input order. That is an
implementation detail of glibc's merge sort, **not a guarantee**, and it does not hold when glibc
falls back to introsort under memory pressure. If you need stability, encode it: add the original
index as a final tie-break key, which turns your comparator into a total order and makes stability
explicit rather than accidental.

---

## 5. `bsearch`

```c
void *bsearch(const void *key, const void *base, size_t nmemb, size_t size,
              int (*compar)(const void *, const void *));
```

Same shape, and it returns a pointer to a matching element or `NULL`.

```c
int key = 7;
int *found = bsearch(&key, a, n, sizeof a[0], cmp_int);
```

Verified: `bsearch(7) -> found, index 4`; `bsearch(99) -> NULL`.

Three requirements that bite:

1. **The array must already be sorted** by the same comparator. `bsearch` on unsorted data does not
   error — it silently returns the wrong answer, usually `NULL`.
2. **You pass the address of the key**, not the key. `bsearch(&key, ...)`, never `bsearch(key, ...)`.
3. **The return is a pointer, not an index.** Get the index by subtracting:
   `ptrdiff_t i = found - a;` — and check for `NULL` first.

This is your Week 9 binary search, made generic by exactly the same four-parameter trick.

---

## 6. Byte Arithmetic

How does generic code reach element `i` when it does not know the type?

```c
void  *base = arr;
size_t es   = sizeof arr[0];
int    val  = *(int *)((char *)base + i * es);
```

Cast to `char *` first. `sizeof(char)` is 1 **by definition**, so `char *` arithmetic counts bytes.
You cannot do arithmetic on `void *` at all in standard C — GCC allows it as an extension, treating
it as 1 byte, but `-pedantic` rejects it and it is not portable.

Verified over `{10,20,30,40,50}`: elements 0–4 read back correctly as 10, 20, 30, 40, 50.

Every generic container you write will contain this line in some form. In Lecture 3 it becomes:

```c
static void *vec_at(const Vec *v, size_t i)
{
    assert(i < v->len);
    return (char *)v->data + i * v->elem_size;
}
```

---

## 7. Summary

| Idea | Takeaway |
|---|---|
| `void *` | Erases the type; round trip guaranteed for **object** pointers (C11 6.3.2.3) |
| The pattern | Erase the type, then hand back the erased operations as parameters |
| `qsort`'s four parameters | Three of them replace what `void *` destroyed |
| Comparator contract | Negative / zero / positive; must be consistent and transitive |
| `return a - b;` | **Undefined behaviour** on overflow — verified to mis-sort |
| `(l > r) - (l < r)` | Correct for every input; no arithmetic on the values |
| `char *` in comparators | Element address is `char **` when the element is `char *` |
| Multi-key | Return early on the first key that discriminates |
| Stability | Not guaranteed; encode the original index if you need it |
| `bsearch` | Array must be pre-sorted; pass `&key`; returns a pointer, not an index |
| Byte arithmetic | Cast to `char *`; `void *` arithmetic is not standard C |

---

## Practice Exercises

Attempt each before reading the answers.

**1. (Trace.)** Given `int v[] = { INT_MIN, 0, INT_MAX };` and `cmp_bad` from §3, state which pair
of comparisons overflows and what the true ordering should be.

**2. (Fix.)** Three bugs. Find and fix all of them.

```c
int cmp(void *a, void *b) { return strcmp(a, b); }
char *words[] = { "pear", "apple", "fig" };
qsort(words, sizeof words, sizeof(char *), cmp);
```

**3. (Build.)** Write a comparator ordering `Student { char *name; int score; }` by **score
ascending**, breaking ties by **name descending**.

**4. (Stretch.)** `bsearch` returns `NULL` when the key is absent. Write `lower_bound`: return the
index of the first element **not less than** the key, or `n` if none is. Explain why `bsearch`
cannot give you this.

### Answers

**1.** Both comparisons involving `INT_MIN` and a non-negative value overflow:

| Pair | True difference | Fits in `int`? |
|---|---|---|
| `0 - INT_MIN` | 2147483648 | ❌ `INT_MAX` is 2147483647 |
| `INT_MAX - INT_MIN` | 4294967295 | ❌ |
| `INT_MAX - 0` | 2147483647 | ✅ exactly fits |

So `INT_MAX - 0` is the only safe one, and it fits by exactly one. The true ordering is
`INT_MIN < 0 < INT_MAX`; `cmp_bad` may report any of these backwards, and the program has no defined
behaviour once overflow occurs.

**2.** The bugs:

- **`sizeof words` is the array's size in bytes (24), not the element count.** `qsort` is told there
  are 24 elements in a 3-element array and reads far out of bounds. Use
  `sizeof words / sizeof words[0]`.
- **The comparator's parameters must be `const void *`,** not `void *`. The signature must match
  `int (*)(const void *, const void *)` exactly.
- **`strcmp(a, b)` is wrong.** `qsort` passes the *address of the element*, and each element is a
  `char *`, so `a` is a `char **`. Passing it to `strcmp` compares the pointer bytes as if they were
  text — reading whatever the pointer values happen to look like. Dereference once first.

```c
static int cmp(const void *a, const void *b)
{
    const char *const *l = a, *const *r = b;
    return strcmp(*l, *r);
}

qsort(words, sizeof words / sizeof words[0], sizeof words[0], cmp);
```

Note `sizeof words[0]` rather than `sizeof(char *)` — same value, but it stays correct if the element
type changes.

**3.**

```c
static int by_score_asc_name_desc(const void *a, const void *b)
{
    const Student *x = a, *y = b;
    int c = (x->score > y->score) - (x->score < y->score);   /* ascending */
    if (c) return c;
    return strcmp(y->name, x->name);                          /* descending */
}
```

Ascending puts `x` first in the comparison; descending on the tie-break swaps the `strcmp`
arguments. The `if (c) return c;` early return is the load-bearing line — without it the tie-break
would overwrite the primary key.

**4.**

```c
static size_t lower_bound(const void *key, const void *base, size_t n, size_t size,
                          int (*cmp)(const void *, const void *))
{
    size_t lo = 0, hi = n;                 /* half-open [lo, hi) */
    while (lo < hi) {
        size_t mid = lo + (hi - lo) / 2;   /* no overflow */
        if (cmp((const char *)base + mid * size, key) < 0)
            lo = mid + 1;                  /* mid is too small; discard it */
        else
            hi = mid;                      /* mid might be the answer; keep it */
    }
    return lo;
}
```

**Why `bsearch` cannot do this:** `bsearch` answers a *membership* question and returns `NULL` on
failure, discarding the position information entirely. Worse, when duplicates exist it may return
**any** matching element, not the first — the standard does not say which.

`lower_bound` answers a *position* question, which is strictly more informative: it tells you where
the key is **or where it would be inserted**. That single change makes it the right primitive for
insertion into a sorted array, for counting occurrences (`upper_bound − lower_bound`), and for range
queries — none of which `bsearch` supports.

Two details worth noting: the interval is **half-open**, so `hi = mid` (not `mid - 1`) is correct and
the loop still shrinks; and `lo + (hi - lo) / 2` avoids the overflow that `(lo + hi) / 2` risks —
the bug that sat in the JDK's binary search for nine years.

---

## Reading

- **`man 3 qsort`**, **`man 3 bsearch`** — read both signatures carefully
- **K&R, §5.11** — the `qsort` reimplementation
- **C11 §6.3.2.3** — pointer conversions
- **C11 §7.22.5** — the searching and sorting utilities, including the comparator requirements

---

*PROG 101 · Week 11 · Lecture 2 · © CSE Department*
