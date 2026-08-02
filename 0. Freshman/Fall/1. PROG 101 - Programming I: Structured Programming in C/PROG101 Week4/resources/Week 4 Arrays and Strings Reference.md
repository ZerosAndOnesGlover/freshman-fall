# PROG 101 · Week 4 Reference
## Arrays and Strings

---

## Arrays

```c
int a[10];                  /* 10 ints, indices 0..9, UNINITIALISED       */
int b[5] = {1, 2, 3};       /* remaining elements are 0                   */
int c[]  = {1, 2, 3};       /* size 3, inferred                           */
int d[3] = {0};             /* all zero -- the idiomatic zero-fill        */
```

| Expression | Meaning |
|---|---|
| `a[i]` | **Defined as** `*(a + i)` |
| `sizeof a` | Whole array in **bytes**, only where declared |
| `sizeof a / sizeof a[0]` | Element count, only where declared |
| `&a[0]` | Pointer to first element, type `int *` |
| `&a` | Pointer to the **whole array**, type `int (*)[10]` |

**Verified on `int a[10]`:** `sizeof a` is 40 in `main` and **8** inside a function taking `int a[10]`
— the parameter has decayed to `int *`. `-Wsizeof-array-argument` warns.

**Verified pointer arithmetic:** `a+1` advances 4 bytes; `&a+1` advances **40** — the whole array.

### C never checks a bound

```c
int a[10];
a[10] = 0;      /* out of bounds -- undefined behaviour */
```

Plain build: `*** stack smashing detected ***`. Under `-fsanitize=address`:

```
ERROR: AddressSanitizer: stack-buffer-overflow
    [48, 88) 'a' (line 2) <== Memory access at offset 88 overflows this variable
```

**Always pass the length** alongside an array parameter — `sizeof` cannot recover it.

---

## Strings

A string is a `char` array ending in `'\0'`. The terminator is **part of the storage**:

```c
char s[] = "hi";       /* 3 bytes: 'h' 'i' '\0'  -- writable copy      */
char *p  = "hi";       /* pointer to read-only literal -- do NOT modify */
```

| Function | Contract |
|---|---|
| `strlen(s)` | Length **excluding** the terminator; O(n) |
| `strcmp(a,b)` | <0, 0, >0 — not a boolean |
| `strchr(s,c)` | Pointer to first `c`, or **NULL** |
| `strstr(h,n)` | Pointer to first occurrence, or **NULL** |
| `memcpy(d,s,n)` | Fast; **undefined if regions overlap** |
| `memmove(d,s,n)` | Safe when they overlap |

---

## Bounded String Functions

| Function | Null-terminates? | Notes |
|---|---|---|
| `strcpy` | — | **Never use.** No bound |
| `strcat` | — | **Never use.** No bound |
| `sprintf` | — | **Never use.** No bound |
| `gets` | — | **Removed from C11** |
| `strncpy` | ❌ **Not** when the source fills the buffer | Also pads the **whole** buffer with zeros |
| `strncat` | ✅ | Its `n` is chars to **append**, not buffer size |
| **`snprintf`** | ✅ | **Use this.** Returns the length it *wanted* |

**Verified.** Copying 10 chars into an 8-byte buffer:

```
strncpy  -> [ABCDEFGH]      no terminator anywhere
snprintf -> [ABCDEFG\0]     valid string, returns 10
```

### The truncation test

```c
int n = snprintf(dst, cap, "%s", src);
if (n < 0)                 { /* encoding error */ }
else if (n >= (int)cap)    { /* TRUNCATED     */ }
```

The `(int)` cast is required — `cap` is `size_t` (unsigned), and without it a negative `n` becomes
huge. `-Wsign-compare` catches the omission.

### Sizing an allocation exactly

```c
int need = snprintf(NULL, 0, "value=%d", x);   /* writes nothing, returns the length */
char *buf = malloc((size_t)need + 1);
snprintf(buf, (size_t)need + 1, "value=%d", x);
```

Verified: `snprintf(NULL, 0, "value=%d", 12345)` returns **11**.

---

## Build Line

```bash
gcc -Wall -Wextra -Werror -pedantic -std=c11 -g prog.c -o prog
valgrind --leak-check=full --error-exitcode=1 ./prog
gcc -fsanitize=address,undefined -g prog.c -o prog_san && ./prog_san
```

---

## Common Errors

| Symptom | Cause |
|---|---|
| `sizeof` gives 8 in a function | Array decayed to a pointer — pass the length |
| `strlen` reads past the buffer | `strncpy` left it unterminated |
| Writes land in an adjacent variable | Off-by-one: `i <= n` should be `i < n` |
| Segfault modifying a string | Writing through `char *p = "literal"` |
| `strcmp(a,b)` used as a boolean | It returns 0 on **equality** — test `== 0` |

---

*PROG 101 · Week 4 · Reference · © CSE Department*
