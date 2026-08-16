# PROG 101 · Programming I: Structured Programming in C
## Week 5 · Lecture 3: NULL, `const`, and the Classic Pointer Errors

**Date:** Thursday 24 September 2026 · 10:00–10:50 · Week 5

---

## Lecture Goals

By the end of this lecture you can:

- Use `NULL` correctly as a sentinel, and guard every dereference that needs it
- Read and write all four `const` / pointer combinations, and say which one you want
- Recognise the five classic pointer errors on sight
- Choose the right tool — compiler flag, sanitizer, or Valgrind — for each class of bug

---

## 1. Null Pointers

`NULL` is the pointer value guaranteed to compare unequal to any valid object address. It means
"points at nothing."

```c
int *p = NULL;
if (p != NULL) { *p = 5; }     /* guarded */
```

Verified: a null pointer prints as `(nil)` under `%p`, and `p == 0` is true.

**Dereferencing NULL is undefined behaviour.** On Linux it usually faults immediately, because page
zero is unmapped — which is a mercy, since the failure is loud and points at the right line. On an
embedded target with no MMU, address 0 may be real memory, and the write silently corrupts it.

### Where NULL comes from

| Source | Returns NULL when |
|---|---|
| `malloc`, `calloc`, `realloc` | Allocation failed (Week 6) |
| `fopen` | The file could not be opened (Week 8) |
| `strchr`, `strstr` | The needle was not found |
| `bsearch` | The key is absent |
| Your own functions | Whatever you document |

**Every one of these must be checked.** The single most common C crash is dereferencing a returned
pointer without testing it.

```c
FILE *f = fopen(path, "r");
if (f == NULL) { perror(path); return -1; }    /* not optional */
```

### Style

```c
if (p != NULL)    /* explicit */
if (p)            /* idiomatic; identical meaning */
```

Both are correct and both are common. Pick one and be consistent within a file. What you must not do
is write `if (p == 0)` and mentally treat `0` as an integer — `NULL` documents that the value is a
pointer, and that is its entire purpose.

> **A note on `NULL` vs `0`.** In C, `NULL` is a null pointer constant, usually defined as `((void*)0)`
> or `0`. Both work. C23 adds `nullptr` with a proper pointer type. Use `NULL` in this course.

### Guard placement matters

From Week 2's short-circuit rules:

```c
if (p != NULL && *p == 5)     /* correct: && guarantees left-to-right */
if (*p == 5 && p != NULL)     /* WRONG: dereferences before checking */
```

The second is a null dereference with a useless check after it. The order is load-bearing.

---

## 2. `const` and Pointers — Four Combinations

`const` interacts with pointers in two independent places: the thing pointed to, and the pointer
itself. That gives four combinations, and they are frequently confused.

```c
int v = 1, w = 2;

int *p                 = &v;   /* neither const */
const int *pc          = &v;   /* pointer to const int  */
int *const cp          = &v;   /* const pointer to int  */
const int *const cc    = &v;   /* both const            */
```

| Declaration | Can repoint? | Can modify target? |
|---|---|---|
| `int *p` | ✅ | ✅ |
| `const int *pc` | ✅ | ❌ |
| `int *const cp` | ❌ | ✅ |
| `const int *const cc` | ❌ | ❌ |

Verified: `pc = &w;` compiles (repointing is allowed), and `*cp = 99;` compiles and changes `v` to 99
(modifying the target is allowed). The compiler rejects the other two combinations.

### Reading the declaration

**Read right to left from the variable name**, and remember that `const` binds to what is on its
*left* unless it is leftmost:

```
const int *pc;      pc -> pointer -> to int that is const     (target is const)
int *const cp;      cp -> const pointer -> to int             (pointer is const)
```

An equivalent and arguably clearer spelling of the first is `int const *pc;` — the `const` sits
immediately right of what it qualifies. Both mean the same thing; the `const int *` form is more
common.

### Which one you almost always want

**`const T *` — pointer to const.** It is the right type for any parameter you read but do not
modify:

```c
size_t my_strlen(const char *s);
int    total(const int *a, size_t n);
void   print(const struct Record *r);
```

This is not decoration. It:

- **documents the contract** in the type, where it cannot go stale
- **lets the compiler catch** an accidental write inside the function
- **allows callers** to pass a `const` object, which they otherwise could not

`T *const` (const pointer) is rare in parameters — the callee's copy is local anyway, so making it
const affects nothing the caller can see.

### `const` is not a guarantee about the object

```c
int v = 5;
const int *p = &v;
/* *p = 6;  -- rejected */
v = 6;                  /* but this is fine: v itself is not const */
```

`const` on a pointer constrains **access through that pointer**, not the object. Another name for the
same object may still modify it. It is a compile-time promise about *this route*, not a runtime
protection.

---

## 3. The Classic Pointer Errors

Five failure modes. Learn the symptom of each; you will meet all of them.

### 3.1 Uninitialised pointer

```c
int *p;
*p = 42;        /* writes to a garbage address */
```

Automatic variables are not zeroed (Week 3). Initialise to `NULL` and assign before use.
`-Wmaybe-uninitialized` catches many cases **at `-O1` and above only**.

### 3.2 Dangling pointer — returning a local's address

```c
int *bad(void) { int local = 42; return &local; }
```

Week 3 covered this in detail, including the verified result that **GCC compiled the function to
return NULL outright** because the UB permitted it. `-Wreturn-local-addr` catches the direct form.

### 3.3 Use after free

```c
free(p);
*p = 5;         /* UNDEFINED: the block is no longer yours */
```

Week 6's topic. The habit that prevents it: `free(p); p = NULL;` — then a later dereference faults
immediately and visibly, instead of silently corrupting a block the allocator has handed to someone
else.

### 3.4 Off-by-one / out-of-bounds

```c
int a[10];
for (int i = 0; i <= 10; i++) a[i] = 0;    /* a[10] is out of bounds */
```

The most common of the five, and the one that produces the strangest symptoms — it corrupts an
adjacent variable, so the failure appears somewhere unrelated.

### 3.5 Null dereference

```c
FILE *f = fopen("missing", "r");
fprintf(f, "...");        /* f is NULL */
```

Check every returning-pointer call.

### The symptom table

| Symptom | Likely cause |
|---|---|
| Immediate segfault at a consistent line | Null dereference |
| Crash far from the real bug; corrupted unrelated variable | Out-of-bounds write |
| Works at `-O0`, breaks at `-O2` | Undefined behaviour of any kind |
| Works today, breaks after unrelated edits | Dangling pointer or buffer overrun |
| Valgrind reports "invalid read of size 4" | Out-of-bounds or use-after-free |

**"Works at `-O0`, breaks at `-O2`" is the signature of UB**, not of a compiler bug. Week 2 explained
why: the optimiser assumes UB never happens.

---

## 4. The Tools

Match the tool to the class of bug.

```bash
gcc -Wall -Wextra -Werror -pedantic -std=c11 prog.c   # compile-time
gcc -fsanitize=address -g prog.c                       # out-of-bounds, use-after-free
gcc -fsanitize=undefined -g prog.c                     # UB: overflow, bad shifts, misaligned
valgrind --leak-check=full --error-exitcode=1 ./prog   # leaks, invalid access
gdb ./prog                                             # inspect a live crash
```

**ASan is the fastest way to locate a memory bug.** It names the variable, its extent, and the
offending offset:

```
ERROR: AddressSanitizer: stack-buffer-overflow
    [32, 40) 'd' (line 2) <== Memory access at offset 40 overflows this variable
```

Compare that with a bare `Segmentation fault`, which tells you nothing.

**Use ASan and UBSan from the first compile of every assignment.** They cost about 2× run time, which
is irrelevant for coursework, and they turn a class of bug that would cost you an evening into a
message that names the line.

> Note that **ASan and Valgrind overlap but are not interchangeable.** ASan is faster and better at
> stack and global overflows; Valgrind needs no recompilation and finds uninitialised-value reads
> that ASan misses. Run both.

---

## 5. Summary

| Idea | Takeaway |
|---|---|
| `NULL` | "Points at nothing"; prints as `(nil)`; comparing to `0` is true |
| Dereferencing NULL | UB — usually faults on Linux, may silently corrupt elsewhere |
| Check every returning-pointer call | `malloc`, `fopen`, `strchr`, `bsearch` all return NULL |
| Guard order | `p && *p`, never `*p && p` — Week 2's short-circuit rule |
| `const int *p` | Can repoint, **cannot** modify target — the one you usually want |
| `int *const p` | **Cannot** repoint, can modify target — rare in parameters |
| `const` constrains the route | Not the object; another name may still modify it |
| Five classic errors | Uninitialised, dangling, use-after-free, out-of-bounds, null deref |
| `-O0` works, `-O2` breaks | The signature of undefined behaviour |
| Tooling | ASan for memory, UBSan for UB, Valgrind for leaks — run all three |

---

## Practice Exercises

Attempt each before reading the answers.

**1. (Read.)** For each, say whether it compiles, and what it means:
(a) `const int *p; p = &x;`  (b) `const int *p; *p = 5;`  (c) `int *const p = &x; p = &y;`
(d) `int *const p = &x; *p = 5;`

**2. (Explain.)** Why does `const char *` allow `s++` but not `s[0] = 'x'`, while `char *const`
allows the opposite? Answer in terms of what each `const` qualifies.

**3. (Fix.)** Four bugs.

```c
char *read_name(void)
{
    char buf[64];
    fgets(buf, sizeof buf, stdin);
    return buf;
}

int first_digit(const char *s)
{
    char *p = strchr(s, '0');
    return *p - '0';
}
```

**4. (Stretch.)** A program crashes with a segfault only when compiled at `-O2`, and runs correctly
at `-O0`. A colleague concludes the optimiser has a bug. Explain why that conclusion is almost
certainly wrong, and give a systematic procedure for finding the real cause.

### Answers

**1.**

| | Compiles? | Meaning |
|---|---|---|
| **(a)** `const int *p; p = &x;` | ✅ | The **pointer** is not const, so repointing is allowed |
| **(b)** `const int *p; *p = 5;` | ❌ | The **target** is const through `p`; writing through it is rejected |
| **(c)** `int *const p = &x; p = &y;` | ❌ | The **pointer** is const; it cannot be reassigned after initialisation |
| **(d)** `int *const p = &x; *p = 5;` | ✅ | Only the pointer is const; the target is an ordinary `int` |

(b) and (c) are the two errors; they are opposites, which is exactly why the pair is worth
memorising as a pair.

**2.** The two `const`s qualify different things.

**`const char *s`** — the `const` applies to the `char` being pointed at. So:
- `s++` is fine: `s` itself is an ordinary variable, and moving it changes nothing about any `char`.
- `s[0] = 'x'` is rejected: it writes through `s` to a `char` that has been declared const *via this
  route*.

**`char *const s`** — the `const` applies to the pointer. So:
- `s++` is rejected: `s` is a const object and cannot be modified after initialisation.
- `s[0] = 'x'` is fine: the pointed-to `char` carries no const qualification.

The mnemonic that actually works: **`const` qualifies whatever is immediately to its left, unless it
is leftmost, in which case it qualifies what is immediately to its right.** In `char *const s`, the
`const` is right of the `*`, so it qualifies the pointer. In `const char *s` it is leftmost, so it
qualifies the `char`.

**3.**

- **`read_name` returns the address of a local array.** `buf` dies when the function returns —
  a dangling pointer. GCC warns `-Wreturn-local-addr`. Fix: take a caller-supplied buffer, which is
  the idiomatic C shape:
  ```c
  char *read_name(char *out, size_t cap) { return fgets(out, (int)cap, stdin); }
  ```
- **`fgets`' return value is ignored.** It returns `NULL` on EOF or error, in which case `buf` holds
  no valid data — and in `read_name` it was never initialised, so the caller receives garbage.
- **`strchr` may return `NULL`** when the character is absent, and `*p` then dereferences it. This is
  the unchecked-return bug from §1.
- **`strchr(s, '0')` searches for the literal digit zero, not "any digit".** Even given a string full
  of digits, this finds only `'0'`. If the intent is "first digit", the function is wrong regardless
  of the null check.

```c
int first_digit(const char *s)
{
    for (; *s; s++)
        if (*s >= '0' && *s <= '9') return *s - '0';
    return -1;                    /* documented: no digit found */
}
```

*(Note the corrected version needs no `strchr` at all, and returns a sentinel rather than
dereferencing something that may not exist.)*

**4.** The conclusion is almost certainly wrong because **GCC's optimiser is used by essentially every
Linux distribution to build essentially every package.** A miscompilation affecting ordinary code
would be found within days. The base rate for "my program has UB" versus "the optimiser is broken" is
overwhelmingly lopsided.

The real explanation is Week 2's: **undefined behaviour**. At `-O0` the compiler translates fairly
literally and the UB happens to do something survivable. At `-O2` the optimiser applies
transformations that are valid *only* for programs without UB — deleting a check it can prove
redundant, keeping a value in a register, reordering reads. The program's behaviour changes because
it never had a defined behaviour to preserve.

**A systematic procedure:**

1. **Rebuild with `-fsanitize=address,undefined -g -O1`.** This finds the large majority immediately
   and names the exact line. Do this before anything else — it is one command and often ends the
   investigation.
2. **Run under Valgrind** if the sanitizers are silent; it catches uninitialised-value reads that ASan
   does not.
3. **Turn the warnings up**: `-Wall -Wextra -Wpedantic -Wshadow -Wconversion`. Fix every one.
4. **Bisect the optimisation level** — try `-O1`, and individual flags like
   `-fno-strict-aliasing` or `-fno-strict-overflow`. If disabling a specific assumption fixes it, that
   assumption names your bug: strict aliasing means a type-punning violation, strict overflow means
   signed overflow.
5. **Only then** produce a minimal reproducer and consider a compiler bug — and expect the reproducer
   itself to reveal the UB while you are reducing it, which is the usual outcome.

*Full marks require step 4's diagnostic reasoning:* `-fno-strict-overflow` "fixing" the crash is not a
fix, it is a **diagnosis**.

---

## Reading

- **K&R, §5.4–5.5** — address arithmetic and character pointers
- **`man valgrind`**, and the **AddressSanitizer** and **UndefinedBehaviorSanitizer** wiki pages
- **C11 §6.7.3** — type qualifiers, including how `const` composes with pointers
- **Regehr, "A Guide to Undefined Behavior in C and C++"** — Part 3 covers the `-O0`/`-O2` divergence

---

*PROG 101 · Week 5 · Lecture 3 · © CSE Department*
