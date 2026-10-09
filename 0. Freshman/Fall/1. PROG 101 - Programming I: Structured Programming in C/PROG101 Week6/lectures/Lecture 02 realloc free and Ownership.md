# PROG 101 · Programming I: Structured Programming in C
## Week 6 · Lecture 2: `realloc`, `free`, and Ownership

*“Don't have good ideas if you aren't willing to be responsible for them.”* — Alan Perlis, "Epigrams on Programming" (1982), #95

**Date:** Wednesday 4 November 2026 · 10:00–10:50 · Week 6

**Reading:** `man 3 realloc` · `man 3 free` · K&R, §8.7 · Valgrind manual, "Memory leak detection" *(details at the end of the lecture)*

**Coursework:** 📘 **Midterm 1** today 18:00–19:30 · 📝 **PS 5** due Fri 6 Nov 17:00 · 📝 **PS 6** released Fri 6 Nov 10:00, due Fri 13 Nov 17:00 · 🔬 **Lab 6** Mon 9 Nov 15:00–16:50 · 📊 **Quiz 6** Tue 10 Nov 10:00–10:10

---

## Lecture Goals

By the end of this lecture you can:

- Use `realloc` without leaking the original block on failure
- State the rules for `free` and the three ways to misuse it
- Reason about **ownership**: who frees what, and say it in a comment
- Choose between stack and heap deliberately

---

## 1. `realloc`

```c
void *realloc(void *ptr, size_t size);
```

Resizes an existing allocation, returning a pointer to a block of `size` bytes whose contents are
preserved up to the smaller of the old and new sizes.

Verified:

```
after grow: contents preserved? yes (first 4 = 1 2 3 4)
```

Three behaviours worth knowing exactly:

| Call | Behaviour |
|---|---|
| `realloc(NULL, n)` | Behaves as `malloc(n)` — verified |
| `realloc(p, 0)` | Implementation-defined; returned **NULL** here |
| Growing | Old contents preserved; **new bytes are uninitialised** |

`realloc(NULL, n)` behaving as `malloc` is what lets a growth loop start from a NULL pointer with no
special case — you will use that in Lecture 3.

### The rule that matters

**Never assign `realloc`'s result back to the pointer you passed in.**

```c
p = realloc(p, n);              /* WRONG */
```

If `realloc` fails it returns NULL **and leaves the original block allocated**. Assigning straight
back overwrites your only reference to it: the memory is now unreachable — a leak — and you have also
destroyed the data you were trying to grow.

```c
void *tmp = realloc(p, n);      /* correct */
if (!tmp) { /* p is still valid; recover or bail */ }
else       p = tmp;
```

With a temporary, failure is *recoverable*: the old block is intact and the program still has its
data. This is one of the most common C bugs, and one of the easiest to avoid once seen.

### `realloc` may move the block

If the allocator cannot extend in place, it allocates elsewhere, copies, and frees the original. So:

```c
int *a = malloc(4 * sizeof *a);
int *alias = a;                 /* second pointer to the same block */
int *tmp = realloc(a, 8 * sizeof *tmp);
if (tmp) a = tmp;
/* alias is now a DANGLING pointer if the block moved */
```

**Every other pointer into the block becomes invalid.** This includes pointers you saved into a
struct, indices you converted to pointers, and any iterator you were holding. Keep *indices*, not
pointers, across a possible reallocation.

---

## 2. `free`

```c
void free(void *ptr);
```

Returns a block to the allocator. Three rules:

**`free(NULL)` is safe.** Verified — a guaranteed no-op. So a cleanup path need not test:

```c
free(p);        /* fine even if p is NULL */
```

**Free exactly once.** A double free corrupts the allocator's bookkeeping and typically crashes
somewhere unrelated, later.

**Free only what `malloc`, `calloc`, or `realloc` returned.** Not a stack address, not an interior
pointer:

```c
int *p = malloc(10 * sizeof *p);
free(p + 2);        /* UNDEFINED: not the address malloc returned */
```

### The habit: null after free

```c
free(p);
p = NULL;
```

`free` does not change `p` — it cannot, since it receives a copy of the pointer (Week 5). So `p`
still holds the old address, now dangling.

Setting it to NULL converts two silent bugs into loud ones:

- a later dereference faults immediately at the right place, instead of corrupting a block the
  allocator has since given to someone else
- a second `free(p)` becomes `free(NULL)`, which is a guaranteed no-op rather than a double free

The cost is one line. Do it every time.

---

## 3. Ownership

The heap's hard problem is not allocation. It is deciding **who is responsible for freeing**, and C
gives you no help — no destructors, no reference counting, no garbage collector.

So ownership must be a *convention*, and it must be written down.

### Three patterns

**1. The creator frees.** Simplest and most common:

```c
int *a = malloc(n * sizeof *a);
/* ...use a... */
free(a);
```

**2. Ownership transfers to the caller.** The function allocates and the caller becomes responsible:

```c
/* Returns a newly allocated string. CALLER MUST FREE. */
char *duplicate(const char *s);
```

That comment is not optional. It is the only place the contract exists.

**3. Ownership transfers into a structure.** The container takes over:

```c
/* Takes ownership of `name`; freed by list_destroy. */
int list_add(List *l, char *name);
```

### The two failure modes

| Failure | Cause | Symptom |
|---|---|---|
| **Leak** | Nobody freed it | Memory grows over time; Valgrind reports it |
| **Double free / use-after-free** | Two parties both thought they owned it | Crash, often far from the cause |

Both come from the same root: **an unstated ownership contract**. Every function that returns a
pointer, or accepts one it might retain, needs a comment saying who frees.

### Matching allocation and release

```c
char *make_greeting(const char *name)
{
    size_t n = strlen(name) + 10;
    char *s = malloc(n);
    if (!s) return NULL;
    snprintf(s, n, "Hello, %s!", name);
    return s;                       /* caller owns */
}

char *g = make_greeting("Ada");
if (g) { puts(g); free(g); }        /* caller frees */
```

One `malloc`, one `free`, on paths that both exist. **Every allocation should have a visible,
reachable `free`** — including on error paths, which is where leaks actually live:

```c
int process(void)
{
    char *a = malloc(100);
    if (!a) return -1;
    char *b = malloc(200);
    if (!b) { free(a); return -1; }   /* MUST free a here */
    /* ... */
    free(b);
    free(a);
    return 0;
}
```

The `free(a)` in the second failure branch is the line people forget, and it is exactly the line
Valgrind will point at.

---

## 4. Stack or Heap?

| Use the **stack** when | Use the **heap** when |
|---|---|
| The size is known at compile time | The size is decided at run time |
| The object dies with the function | It must outlive the function |
| The object is small (say, < 1 KB) | It is large — the stack is only 8 MB |
| You want zero management | You accept the bookkeeping |

**Default to the stack.** It is faster (allocation is one instruction adjusting the stack pointer),
it cannot leak, and it cannot be double-freed. Reach for the heap when one of the right-hand
conditions actually applies — not by habit.

The two mistakes are symmetrical: putting a 4 MB array on the stack (crash), and `malloc`-ing a
three-element temporary that a local array would hold (needless failure paths and a leak risk).

---

## 5. Summary

| Idea | Takeaway |
|---|---|
| `realloc(NULL, n)` | Behaves as `malloc` — no special case needed in growth loops |
| Growing preserves contents | But **new bytes are uninitialised** |
| **Never `p = realloc(p, n)`** | On failure you lose the original and leak it |
| `realloc` may move | Every other pointer into the block dangles — keep indices |
| `free(NULL)` | Guaranteed safe no-op |
| Free exactly once, and only what was allocated | `free(p + 2)` is UB |
| `free(p); p = NULL;` | Turns silent corruption into an immediate fault |
| Ownership is a convention | C provides nothing; write it in a comment |
| Three patterns | Creator frees · transfer to caller · transfer into a structure |
| Error paths leak | The `free` before an early `return` is the forgotten one |
| Default to the stack | Faster, cannot leak, cannot double-free |

---

## Practice Exercises

Attempt each before reading the answers.

**1. (Trace.)** What is wrong with each, and what is the symptom?

```c
(a)  p = realloc(p, n);
(b)  free(p); free(p);
(c)  int *q = p + 2; free(q);
(d)  free(p); printf("%d\n", *p);
```

**2. (Explain.)** `free` receives a copy of the pointer, so it cannot set the caller's variable to
NULL. Why does that mean `free(p); p = NULL;` is worth writing, and what two bugs does it convert
into loud failures?

**3. (Fix.)** Three bugs, one of which is a leak on an error path.

```c
char *join(const char *a, const char *b)
{
    char *r = malloc(strlen(a) + strlen(b) + 1);
    strcpy(r, a);
    strcat(r, b);
    return r;
}
```

**4. (Stretch.)** Write `int grow(int **arr, size_t *cap)` that doubles the capacity of a
heap array, leaving the original untouched on failure. Then explain why the function needs `int **`
and `size_t *` rather than `int *` and `size_t`.

### Answers

**1.**

| | Bug | Symptom |
|---|---|---|
| **(a)** | On failure `realloc` returns NULL and leaves the block allocated; the assignment destroys the only reference | **Leak**, plus loss of the data. Valgrind: "definitely lost" |
| **(b)** | Double free — the allocator's metadata is corrupted | Crash, usually inside `malloc`/`free` at a *later*, unrelated call |
| **(c)** | `free` given an interior pointer, not what `malloc` returned | UB; glibc typically aborts with "invalid pointer" |
| **(d)** | Use after free | Undefined. May print the old value, may print garbage, may crash — and the block may already belong to another allocation |

(d) is the most dangerous because it frequently *appears to work*: the freed bytes usually still hold
the old value until reused.

**2.** Because `free` cannot do it for you, and the dangling pointer left behind is indistinguishable
from a valid one.

Pointers are passed by value (Week 5), so `free` receives a copy of the address. It can release the
block, but it cannot reach back and modify the caller's variable. After `free(p)`, `p` still holds
the old address — a pointer that looks perfectly ordinary and refers to memory the allocator may hand
to someone else at any moment.

Setting `p = NULL` converts **two** silent bugs into immediate, localised failures:

- **Use after free** becomes a **null dereference**, which faults at the offending line instead of
  silently reading or writing a block that now belongs to unrelated data.
- **Double free** becomes `free(NULL)`, which is a guaranteed no-op instead of allocator corruption
  that crashes somewhere else entirely.

The pattern trades a class of far-away, non-deterministic bugs for a class of immediate, obvious
ones. That is almost always the right trade.

**3.**

- **`malloc`'s return is not checked.** If it fails, `strcpy` dereferences NULL.
- **The allocation is one byte short — no, it is correct.** `strlen(a) + strlen(b) + 1` is exactly
  right: both strings plus one terminator. *(This is the plausible-looking line that is actually
  fine; the exercise includes it deliberately.)*
- **`strcpy`/`strcat` are unbounded** (Week 4). Here the size was computed correctly so they do not
  overflow — but the code is fragile: any later edit to the length calculation silently becomes a
  heap overflow. Use `snprintf`, which cannot.
- **No ownership comment.** The caller must free `r`, and nothing says so.

```c
/* Returns a newly allocated concatenation, or NULL. CALLER MUST FREE. */
char *join(const char *a, const char *b)
{
    size_t n = strlen(a) + strlen(b) + 1;
    char *r = malloc(n);
    if (!r) return NULL;
    snprintf(r, n, "%s%s", a, b);
    return r;
}
```

*The leak-on-error-path in the prompt is the caller's:* code that calls `join` in a loop and returns
early on some other condition without freeing. The fix above cannot prevent that — only the comment
can, which is the point.

**4.**

```c
int grow(int **arr, size_t *cap)
{
    size_t ncap = *cap ? *cap * 2 : 4;
    if (ncap < *cap) return -1;                     /* size_t overflow */
    int *tmp = realloc(*arr, ncap * sizeof **arr);
    if (!tmp) return -1;                            /* *arr still valid */
    *arr = tmp;
    *cap = ncap;
    return 0;
}
```

**Why `int **` and `size_t *`.** The function must modify **two variables belonging to the caller**:
the array pointer (because `realloc` may move the block) and the capacity. Parameters are passed by
value, so given `int *arr` the function would receive a copy — assigning to it would change nothing
the caller can see, the caller would keep using the old, possibly-freed pointer, and the new block
would leak.

To modify a caller's `T`, take a `T *`. Here `T` is `int *` and `size_t`, giving `int **` and
`size_t *`. This is Week 5 Lecture 1's rule, applied twice in one signature.

**Three details that make it correct on failure:**

- **The temporary.** `realloc` into `tmp`, and only publish it to `*arr` after confirming success —
  otherwise a failure destroys the caller's pointer, which is the §1 bug.
- **`*arr` and `*cap` are left untouched** when it returns −1, so the caller's array is still valid
  and still has its old capacity. The caller can retry, degrade, or bail.
- **The `ncap < *cap` check** catches `size_t` doubling overflow. It is unreachable in practice at
  these sizes, but it costs one comparison and its absence is the kind of thing that becomes a
  vulnerability when the capacity is attacker-influenced.

*A stricter answer* also checks `ncap > SIZE_MAX / sizeof **arr` before the multiplication, for the
same reason Lecture 1's `xmalloc_array` did.

---

## Reading

- **`man 3 realloc`** — the RETURN VALUE section states the failure behaviour explicitly
- **`man 3 free`** — and note what it says about `NULL`
- **K&R, §8.7** — a storage allocator, implemented; worth reading once
- **Valgrind manual, "Memory leak detection"** — the four leak categories and what each means

---

*PROG 101 · Week 6 · Lecture 2 · © CSE Department*
