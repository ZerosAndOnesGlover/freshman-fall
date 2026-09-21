# PROG 101 · Programming I: Structured Programming in C
## Week 6 · Lecture 1: The Process Memory Map and `malloc`

**Date:** Tuesday 3 November 2026 · 10:00–10:50 · Week 6

---

## Lecture Goals

By the end of this lecture you can:

- Name the regions of a running process's memory and say what lives in each
- Explain why some data must be allocated at run time rather than declared
- Use `malloc` and `calloc` correctly, including checking for failure
- Say precisely what `calloc` gives you that `malloc` does not

---

## 1. Where Things Live

A running C program's memory divides into regions. Verified addresses from a single program on this
machine:

```
text / literals  ~ 0x626b8d05c031      <- low
globals / data   ~ 0x626b8d05e010
heap             ~ 0x626bac34d2b0
stack local      ~ 0x7ffeb6bedd2c      <- high
```

| Region | Contents | Lifetime | Size fixed at |
|---|---|---|---|
| **Text** | Machine code, string literals | Whole program | Compile time |
| **Data / BSS** | Globals, `static` variables | Whole program | Compile time |
| **Heap** | `malloc`'d memory | Until you `free` it | **Run time** |
| **Stack** | Locals, parameters, return addresses | Their enclosing block | Run time, but bounded |

**The heap grows upward from low addresses; the stack grows downward from high ones.** They approach
each other from opposite ends of the address space. On a 64-bit machine there is so much room between
them that they never actually meet — the stack hits its 8 MB `ulimit` long first (Week 3).

Note that string literals live in the **text** region, which is typically read-only. That is why:

```c
char *s = "hello";
s[0] = 'H';            /* UNDEFINED BEHAVIOUR -- usually a segfault */
```

The literal is not yours to modify. To get a writable copy, declare an array:

```c
char s[] = "hello";    /* copies the literal into an array you own */
s[0] = 'H';            /* fine */
```

---

## 2. Why the Heap Exists

Everything you have allocated so far had a size known at compile time:

```c
int a[100];              /* 100 -- decided when you typed it */
```

That fails as soon as the size is decided by the program:

```c
int n;
scanf("%d", &n);
int a[n];                /* a VLA -- allowed in C99, but on the STACK */
```

Variable-length arrays exist, but they live on the stack, so a large `n` overflows it (Week 3), their
lifetime still ends with the block, and they are optional in C11. They do not solve the real problem.

**Three things only the heap can do:**

1. **Size determined at run time** — read a file, count the records, allocate exactly that many
2. **Lifetime outliving the creating function** — return a structure the caller keeps
3. **Size that changes** — grow a buffer as data arrives (Lecture 2)

The third is what makes dynamic data structures possible at all. A linked list, a tree, a hash table
— each node is allocated when needed and freed when not, which cannot be expressed with declarations.

---

## 3. `malloc`

```c
#include <stdlib.h>
void *malloc(size_t size);
```

Returns a pointer to `size` bytes of uninitialised memory, or `NULL` on failure.

```c
int *p = malloc(100 * sizeof *p);
if (p == NULL) { /* handle failure */ }
```

### The `sizeof *p` idiom

Write `sizeof *p`, not `sizeof(int)`:

```c
int *p = malloc(100 * sizeof *p);      /* good */
int *p = malloc(100 * sizeof(int));    /* works, but repeats the type */
```

The first stays correct if you later change `p` to `long *`. The second silently allocates the wrong
amount. `sizeof *p` does not dereference `p` — `sizeof` never evaluates its operand (Week 2), so this
is safe even when `p` is uninitialised.

### Do not cast the return

```c
int *p = malloc(n * sizeof *p);          /* correct C */
int *p = (int *)malloc(n * sizeof *p);   /* unnecessary */
```

`void *` converts to any object pointer implicitly. The cast adds nothing and can *hide* a missing
`#include <stdlib.h>`, which in old C would make the compiler assume `malloc` returns `int`. It is
required in C++, which is where the habit comes from.

### `malloc` does not zero

Verified — `malloc(16)` on this run returned a block with **5 of 16 bytes nonzero**:

```
malloc(16): 5 of 16 bytes nonzero (indeterminate)
calloc(16): 0 of 16 bytes nonzero  <- guaranteed 0
```

The contents are **indeterminate**. Do not rely on them being garbage *or* zero — reading them before
writing is undefined behaviour, and Valgrind reports it:

```
Conditional jump or move depends on uninitialised value(s)
```

That message is worth recognising. **ASan does not catch uninitialised reads; Valgrind does.** It is
the main reason to run both.

### `malloc(0)`

Verified: returns **non-NULL** here. The standard permits either a null pointer or a unique
non-null pointer that must not be dereferenced. Either way it is safe to `free`. Do not write code
whose correctness depends on which you get.

### Always check for failure

```c
int *p = malloc(n * sizeof *p);
if (!p) {
    fprintf(stderr, "out of memory\n");
    return -1;
}
```

On Linux with default overcommit settings `malloc` rarely returns NULL for modest sizes — the failure
surfaces later as the OOM killer. That is not a reason to skip the check: it costs two lines, it is
required for correctness on every other platform, and an unchecked NULL becomes a null dereference at
the first use.

---

## 4. `calloc`

```c
void *calloc(size_t nmemb, size_t size);
```

Two differences from `malloc`, and both matter.

**It zeroes the memory.** Verified: all 16 bytes zero. This is genuinely useful when zero is your
initial state — a counter array, a struct whose pointer fields should start NULL.

**It takes the count and size separately, and checks the multiplication.** Verified:

```
calloc(SIZE_MAX/2 + 1, 4) = NULL   <- detects the multiplication overflow
```

Compare with `malloc`:

```c
void *p = malloc(n * size);       /* n * size can OVERFLOW silently */
```

If `n * size` wraps, `malloc` allocates a *small* block and your subsequent writes run far past it.
This is a classic exploitable bug — an attacker supplies a huge `n`, the multiplication wraps, and a
tiny allocation is treated as enormous.

**`calloc` cannot overflow this way**, because it performs the multiplication internally with a check.
When the size comes from untrusted input, prefer `calloc` even if you do not need the zeroing.

> **Is `calloc` slower?** Not usually. For large blocks the OS supplies pages that are already zero
> (it must, so one process cannot read another's data), so `calloc` can skip the memset entirely.
> For small blocks reused from the allocator's free list, it does zero them. Measure before assuming
> `malloc` + `memset` is faster; it generally is not.

---

## 5. `sizeof` Cannot Tell You the Size

Verified:

```
malloc'd 100 ints (400 bytes) but sizeof(ptr) = 8
```

The allocator knows the block size — `free` needs it — but that information is **not available to
your program** through any standard interface. `sizeof` on the pointer gives the pointer's size, 8.

**You must track the length yourself**, and pass it wherever the buffer goes. This is the same lesson
as Week 4's array parameters, and it is why every dynamic structure carries an explicit `size` or
`len` field. Lecture 3 builds exactly that.

---

## 6. Summary

| Idea | Takeaway |
|---|---|
| Four regions | Text, data, heap, stack — verified by address ordering |
| Heap grows up, stack grows down | From opposite ends of the address space |
| String literals | In read-only text; `char *s = "hi"; s[0]='H';` is UB |
| Why the heap | Run-time size, lifetime beyond the function, resizable |
| `malloc(size)` | Returns uninitialised memory, or NULL |
| `sizeof *p` | Not `sizeof(int)` — survives a type change |
| Do not cast `malloc` | `void *` converts implicitly; the cast is a C++ habit |
| `malloc` does not zero | Verified 5/16 bytes nonzero; reading it is UB |
| Valgrind catches it | "uninitialised value" — **ASan does not** |
| `malloc(0)` | Implementation-defined; safe to `free` either way |
| `calloc(n, size)` | Zeroes **and** checks `n * size` for overflow |
| Prefer `calloc` for untrusted `n` | `malloc(n * size)` can wrap silently |
| `sizeof` on a heap pointer | Gives 8 — track the length yourself |

---

## Practice Exercises

Attempt each before reading the answers.

**1. (Trace.)** For each, say what region the object lives in and when it dies:
(a) `int x;` inside a function  (b) `static int y;` inside a function  (c) `int *p = malloc(4);`
(d) the `"hi"` in `char *s = "hi";`

**2. (Explain.)** Why is `malloc(n * sizeof(int))` risky when `n` comes from user input, and what
exactly does `calloc(n, sizeof(int))` do differently?

**3. (Fix.)** Four bugs.

```c
int *make_array(int n)
{
    int *a = (int *)malloc(n);
    for (int i = 0; i <= n; i++) a[i] = 0;
    return a;
}
```

**4. (Stretch.)** Write `void *xmalloc_array(size_t n, size_t size)` that allocates `n * size` bytes,
returns zeroed memory, and **cannot** be made to under-allocate by any values of `n` and `size`.
Explain why simply calling `malloc(n * size)` after an overflow check is subtly harder to get right
than it looks.

### Answers

**1.**

| | Region | Dies |
|---|---|---|
| **(a)** `int x;` in a function | **Stack** | When the enclosing block exits |
| **(b)** `static int y;` in a function | **Data/BSS** | Program exit — narrow scope, long lifetime (Week 3) |
| **(c)** `malloc(4)` | **Heap** | Only when you call `free` |
| **(d)** `"hi"` literal | **Text** (read-only) | Program exit; and it must not be modified |

(b) and (d) are the ones people misplace. A `static` local is *not* on the stack, and a string
literal is *not* in writable memory.

**2.** The risk is **integer overflow in the multiplication**.

`n * sizeof(int)` is computed in `size_t` arithmetic before `malloc` ever sees it. With
`sizeof(int) == 4` and `n` large enough, `n * 4` wraps modulo 2⁶⁴ and produces a small number.
`malloc` then dutifully allocates that small block and returns non-NULL. Every subsequent
`a[i] = ...` writes far past the end.

Because unsigned arithmetic is *defined* to wrap (Week 1), there is no UB and no sanitizer report —
the program simply allocates the wrong amount. That combination, attacker-controlled `n` plus a
silent wrap plus a heap overflow, is a well-known exploit pattern.

**`calloc(n, sizeof(int))` performs the multiplication internally with an overflow check** and
returns NULL if it would wrap. Verified: `calloc(SIZE_MAX/2 + 1, 4)` returns NULL. It also zeroes
the block, though that is the lesser benefit here.

**3.**

- **`malloc(n)` allocates `n` bytes, not `n` ints.** For 100 ints it allocates 100 bytes instead of
  400 — a four-fold under-allocation. → `malloc(n * sizeof *a)`.
- **`i <= n` writes one element past the end.** Valid indices are `0 … n-1`. → `i < n`.
- **The return value is never checked.** If `malloc` fails, `a` is NULL and the loop dereferences it.
  → test `if (!a) return NULL;`.
- **`n` is `int` and may be negative or huge.** `make_array(-1)` converts `-1` to a gigantic `size_t`.
  → take `size_t n`, and prefer `calloc` so the multiplication is checked.

```c
int *make_array(size_t n)
{
    int *a = calloc(n, sizeof *a);    /* checked multiply + zeroed */
    if (!a) return NULL;
    return a;                          /* the loop is now redundant */
}
```

*Note the cast on `malloc` is also unnecessary (§3), though not a bug.* And once `calloc` is used the
zeroing loop disappears entirely — the fix makes the function shorter.

**4.**

```c
#include <stdlib.h>

void *xmalloc_array(size_t n, size_t size)
{
    return calloc(n, size);      /* the checked multiply is the whole point */
}
```

That is the correct answer, and its brevity is the lesson: **the standard library already solved
this**, and reimplementing it is how the bug gets reintroduced.

**Why a hand-rolled check is harder than it looks.** The obvious attempt is:

```c
if (n * size > SOME_LIMIT) return NULL;      /* WRONG */
```

This is useless — the multiplication has already wrapped by the time it is compared. The check must
happen *without* performing the unsafe operation, exactly as with `safe_add` in Week 1:

```c
if (size != 0 && n > SIZE_MAX / size) return NULL;   /* correct */
void *p = malloc(n * size);
if (p) memset(p, 0, n * size);
return p;
```

Three details that are easy to miss:

- **`size != 0` must be tested first**, or `SIZE_MAX / size` divides by zero — undefined behaviour in
  the very check meant to make things safe.
- **The division form is required.** `n > SIZE_MAX / size` is equivalent to `n * size > SIZE_MAX`
  without ever computing the product.
- **`n * size` appears twice more** (in `malloc` and `memset`), and both must use the same value; a
  refactor that changes one is a fresh heap overflow.

*Full marks for `return calloc(n, size);` with the reasoning.* An answer that reimplements it
correctly also earns full marks — but one that reimplements it *incorrectly*, by checking after
multiplying, demonstrates precisely why the library function exists.

---

## Reading

- **K&R, §5.4, §7.8.5** — storage management
- **`man 3 malloc`** — read the NOTES section on overcommit and NULL returns
- **`man 3 calloc`** — the overflow guarantee is stated explicitly
- **CWE-190, CWE-680** — integer overflow leading to buffer overflow

---

*PROG 101 · Week 6 · Lecture 1 · © CSE Department*
