# PROG 101 — Lab 4 Solutions (Instructor)
## Arrays, Strings, and a String Library

**Reference implementation verified:** all functions match the standard library across the test
matrix below; compiles clean under `-Wall -Wextra -Werror -pedantic -std=c11`; Valgrind clean.

---

## Part 1: Arrays, Decay, and Bounds (5 pts)

### 1A — expected output

```
  in main:         sizeof(a) = 40
  elements:        10
  inside function: sizeof(a) = 8
  &a    = 0x7ffcf4fa5230
  &a[0] = 0x7ffcf4fa5230
  a+1   = 0x7ffcf4fa5234  (+4 bytes)
  &a+1  = 0x7ffcf4fa5258  (+40 bytes)
```

Addresses vary per run; the **offsets** do not.

**Answer 1 (2 pts).** 40 versus 8. In `main`, `a` names an actual array so `sizeof` reports its full
extent. In a parameter list C **adjusts** `int a[10]` to `int *a` — the `10` is discarded entirely —
so `sizeof` reports the pointer's size. The mechanism is **array-to-pointer decay**.

*Full marks require naming decay.* "It becomes a pointer" earns 1 without the term.

**Answer 2 (2 pts).** Same address, different **types**. `&a[0]` is `int *`; `&a` is `int (*)[10]`.
Pointer arithmetic scales by the pointed-to type, so `a+1` moves one `int` (**4 bytes**) and `&a+1`
moves one whole array (**40 bytes**).

Students who say "they're the same thing" have missed the entire point — the addresses coincide
precisely because the array starts at its own first element, but the types differ and the arithmetic
follows the type.

**Answer 3 (1 pt).**

```
warning: 'sizeof' on array function parameter 'a' will return size of 'int *'
         [-Wsizeof-array-argument]
```

### 1B — the off-by-one

Verified outputs:

| Build | Result |
|---|---|
| Plain `-Wall -Wextra` | `*** stack smashing detected ***: terminated` |
| `-fsanitize=address` | `ERROR: AddressSanitizer: stack-buffer-overflow`<br>`[48, 88) 'a' (line 2) <== Memory access at offset 88 overflows this variable` |

**Marking note.** The plain build *does* abort here, thanks to GCC's stack protector — students may
therefore report "it crashed" and think the two are equivalent. They are not, and the required
answer is *why* ASan is more useful: it names the **variable**, its **extent** `[48, 88)`, the
**offending offset** (88), and the **source line**. "Stack smashing detected" tells you only that
something, somewhere, overflowed something.

Note also that the plain result is not guaranteed — with a different array size or optimisation
level the program may run to completion with silent corruption. That unreliability is itself the
argument for the sanitizer.

---

## Part 2: String Processing Library (10 pts)

Reference implementations, all verified against the standard library:

```c
size_t my_strlen(const char *s)
{
    const char *p = s;
    while (*p) p++;
    return (size_t)(p - s);          /* pointer difference = element count */
}

char *my_strcpy(char *dst, const char *src)
{
    char *d = dst;
    while ((*d++ = *src++)) ;        /* copies the terminator too, then tests it */
    return dst;
}

int my_strcmp(const char *a, const char *b)
{
    while (*a && *a == *b) { a++; b++; }
    return (int)((unsigned char)*a) - (int)((unsigned char)*b);
}

char *my_strchr(const char *s, int c)
{
    char ch = (char)c;
    for (; *s; s++) if (*s == ch) return (char *)s;
    return ch == '\0' ? (char *)s : NULL;
}

int my_strncmp(const char *a, const char *b, size_t n)
{
    for (size_t i = 0; i < n; i++) {
        if (a[i] != b[i]) return (int)((unsigned char)a[i]) - (int)((unsigned char)b[i]);
        if (a[i] == '\0') return 0;
    }
    return 0;
}
```

### Verification performed

| Check | Result |
|---|---|
| `my_strlen` vs `strlen` on 5 inputs incl. empty and high-byte | matches |
| `my_strcpy` vs `strcpy`, and returns `dst` | matches |
| `my_strcmp` **sign** vs `strcmp` on all 25 pairs | matches |
| High-byte comparison (`"\xff"` vs `"a"`) | matches |
| `my_strchr` present / absent / terminator | matches |
| `my_strncmp` prefix, differing, `n == 0` | matches |
| Valgrind | clean |

### The three details that separate marks

**1. `unsigned char` in `strcmp` (3 pts).** The standard specifies that characters are compared as
`unsigned char`. With plain `char` — signed on x86 — `"\xff"` compares as −1 and sorts *before*
`"a"`, which is backwards. Verified: the unsigned version agrees with `strcmp`, the signed version
does not. This is the single most common wrong answer and it passes every ASCII-only test.

**2. `strcmp` returns a difference, not a boolean (2 pts).** Any negative/zero/positive triple is
conforming; do not require −1/0/1. Deduct only if the *sign* is wrong.

**3. `my_strchr` must find `'\0'` (1 pt).** `strchr(s, '\0')` returns a pointer to the terminator,
not NULL — a genuine quirk of the specification. The naive loop `for (; *s; s++)` exits before
testing it, so the trailing conditional is required. Award the point for handling it; mention it in
feedback if missed, since it is easy to overlook and rarely tested.

**Remaining 4 pts:** `my_strlen` and `my_strcpy` correct (2), test suite covers empty strings and a
non-ASCII byte (2).

*Deduct 3 for any Valgrind error, and 2 per compiler warning, per the lab's stated policy.*

---

## Part 3: Text Decomposition (5 pts)

Marked on **decomposition**, not cleverness. Look for:

| Criterion | Points |
|---|---|
| Each function does one thing and is named for it | 2 |
| No function longer than ~25 lines | 1 |
| Buffers passed with an explicit capacity, never `sizeof` on a parameter | 1 |
| Output matches the required format exactly | 1 |

**The recurring defect** is a single 80-line `main` that reads, tokenises, counts and prints. It may
be correct and still earn 1 of 5 — the exercise is about structure, and saying so in feedback is more
useful than the mark.

**The second recurring defect** is `sizeof(buf)` inside a function that received `buf` as a
parameter. That is Part 1's lesson reappearing in the student's own code, and it is worth pointing at
explicitly: they measured it in 1A and then wrote the bug in Part 3.

---

## Common Submission Problems

| Symptom | Cause | Action |
|---|---|---|
| `my_strcmp` wrong on non-ASCII | Plain `char` comparison | −3, explain the `unsigned char` rule |
| `my_strlen` returns `int` | Should be `size_t` | −1, note the standard signature |
| `my_strcpy` loop misses the terminator | `while (*src) *d++ = *src++;` then no `*d = '\0'` | −2 |
| Tests only use ASCII lowercase | Insufficient coverage | −2 of the test marks |
| `strcpy` used inside `strlib.c` | Defeats the exercise | 0 for that function |

---

*PROG 101 · Week 4 · Lab 4 Solutions · Instructor copy — do not distribute*
