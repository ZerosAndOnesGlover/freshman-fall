# PROG 101 · Programming I: Structured Programming in C
## Week 4 · Lecture 3: Buffer Safety and the Bounded String Functions

*“In any respectable branch of engineering, failure to observe such elementary precautions would have long been against the law.”* — C. A. R. Hoare, on array bounds checking, "The Emperor's Old Clothes", Turing Award Lecture (1980)

**Date:** Thursday 22 October 2026 · 10:00–10:50 · Week 4

**Reading:** `man 3 strncpy` · `man 3 snprintf` · `man 3 strlcpy` · CWE-120, CWE-787 · C11 §7.24 *(details at the end of the lecture)*

**Coursework:** 📝 **PS 3** due Fri 23 Oct 17:00 · 📝 **PS 4** released Fri 23 Oct 10:00, due Fri 30 Oct 17:00 · 🔬 **Lab 4** Mon 26 Oct 15:00–16:50 · 📊 **Quiz 4** Tue 27 Oct 10:00–10:10 · 📘 **Midterm 1** Wed 4 Nov 18:00–19:30

---

## Lecture Goals

By the end of this lecture you can:

- Explain why `strcpy` and `gets` are unusable, and what replaced them
- State exactly what `strncpy` does — and why its name is misleading
- Use `snprintf` correctly, including its return value, for both copying and sizing
- Detect truncation, which is the failure mode the "safe" functions introduce

---

## 1. The Problem C Does Not Solve for You

Lectures 1 and 2 built arrays and strings. Both share one property: **C never checks a bound.**

```c
char dest[8];
strcpy(dest, "way too long for eight");   /* writes 23 bytes into 8 */
```

Nothing stops this. `strcpy` copies until it finds a null terminator in the *source*, with no idea
how large the destination is — because it was never told. The extra bytes land on whatever follows
`dest` in memory: other locals, the saved frame pointer, the return address.

That last one is why this matters beyond correctness. Overwriting a return address lets an attacker
choose where the function returns to. **Buffer overflow is the oldest exploitable bug class in
computing**, and it is still in the top ranks of the CWE list decades after it was first documented.

Verified with AddressSanitizer:

```
ERROR: AddressSanitizer: stack-buffer-overflow
    [32, 40) 'd' (line 2) <== Memory access at offset 40 overflows this variable
```

ASan names the variable, its extent, and the offending offset. **Compile with `-fsanitize=address`
during development** — it turns silent corruption into an immediate, precise report.

### The functions to never use

| Function | Why |
|---|---|
| `gets()` | Cannot be used safely — no size parameter exists. **Removed from C11 entirely** |
| `strcpy()` | No bound |
| `strcat()` | No bound |
| `sprintf()` | No bound |

`gets` is the only standard-library function ever deleted from C for being unsafe. If you see it in
old code, that code predates 2011.

---

## 2. `strncpy` Is Not "Safe `strcpy`"

The obvious replacement is `strncpy`. It takes a size, so it looks like the bounded version.

**It does not do what its name suggests, in two separate ways.**

### It does not null-terminate

Verified — copying a 10-character string into an 8-byte buffer:

```
strncpy 10 into 8      [ABCDEFGH]
```

**There is no `\0` anywhere in that buffer.** `strncpy` writes at most `n` bytes; if the source is at
least `n` long, no terminator is written. The result is not a string. Passing it to `strlen`,
`printf("%s")`, or `strcmp` reads past the end of the buffer — the very bug you were trying to avoid.

If you use `strncpy` you must terminate by hand:

```c
strncpy(dest, src, sizeof dest - 1);
dest[sizeof dest - 1] = '\0';          /* mandatory */
```

### It pads the entire buffer

Verified — copying a 2-character string into an 8-byte buffer:

```
strncpy 'AB' into 8    [AB\0\0\0\0\0\0]
```

All eight bytes are written. `strncpy` zero-fills the remainder, so copying a 3-byte name into a
4096-byte buffer writes 4096 bytes. In a loop over many records this is a measurable and completely
pointless cost.

> **Why does it behave this way?** `strncpy` was not designed for strings as you use them. It was
> written for early UNIX **fixed-width directory entries**, where a name occupied exactly 14 bytes,
> padded with zeros, and *not* terminated if it filled the field. For that job the behaviour is
> exactly right. It has been misapplied ever since because of its name.

GCC warns about the first hazard:

```
warning: 'strncpy' output truncated copying 8 bytes from a string of length 10
         [-Wstringop-truncation]
```

---

## 3. `snprintf` — The One to Reach For

```c
int snprintf(char *dest, size_t size, const char *format, ...);
```

`snprintf` gets both behaviours right:

- **It always null-terminates** (whenever `size > 0`), truncating the content to fit
- **It writes only what is needed**, no padding

Verified — 10 characters into an 8-byte buffer:

```
snprintf 10 into 8     [ABCDEFG\0]
return value = 10
```

Seven characters plus a terminator. Exactly eight bytes used, and the result is a valid string.

### The return value is the important part

**`snprintf` returns the length it *wanted* to write, not what it actually wrote.** Above it returned
10, though only 7 characters landed.

That makes truncation detectable:

```c
int n = snprintf(dest, sizeof dest, "%s", src);
if (n < 0)                    { /* encoding error */ }
else if (n >= (int)sizeof dest) { /* TRUNCATED */ }
```

Verified: `n >= (int)sizeof dest` is true for the case above. **The cast is required** — `n` is `int`
and `sizeof` is `size_t` (unsigned), so without it the comparison converts `n` to unsigned and
`-Wsign-compare` fires. That is the Week 1 trap in a new place.

### Sizing an allocation

Passing a null destination and size 0 writes nothing and still returns the required length:

```c
int need = snprintf(NULL, 0, "value=%d", 12345);   /* returns 11 */
char *buf = malloc((size_t)need + 1);              /* +1 for the terminator */
snprintf(buf, (size_t)need + 1, "value=%d", 12345);
```

Verified: `need` is 11, and the buffer fills correctly with `value=12345`. This two-pass idiom is the
standard way to build a string of unknown length in C, and it is exact — no guessing at a "big
enough" size.

---

## 4. Concatenation

`strcat` has the same flaw as `strcpy`. `strncat` is bounded, but its parameter means something
different from `strncpy`'s:

> **`strncat`'s `n` is the maximum number of characters to *append*, not the size of the buffer.**

So the bound must be computed from the space remaining:

```c
strncat(dest, src, sizeof dest - strlen(dest) - 1);
```

Verified — appending to `"abc"` in a 10-byte buffer:

```
strncat bounded        [abcXYZXYZ\0]
```

Nine characters plus a terminator. `strncat` *does* always null-terminate, unlike `strncpy` — the two
functions are inconsistent with each other, which is a large part of why they are so error-prone.

**Prefer `snprintf` for concatenation too:**

```c
snprintf(dest, sizeof dest, "%s%s", first, second);
```

One call, one bound, terminated, and truncation detectable from the return value. Building strings by
repeated `snprintf` into a moving offset is also O(n²) if done carelessly — track the offset and
remaining size explicitly if you concatenate in a loop.

---

## 5. `strlcpy` and `strlcat`

BSD introduced these to do the obvious thing: copy with a bound, always terminate, return the source
length so truncation is detectable.

```c
size_t strlcpy(char *dst, const char *src, size_t size);
```

Verified on this system:

```
strlcpy returned 10 (source length), buffer = 'ABCDEFG' (len 7)
truncated? 1   <- test is: return >= size
```

**A correction worth making:** these are widely described as "BSD-only, unavailable on Linux." That
was true for a long time, but **glibc added them in version 2.38**. This machine runs glibc 2.39 and
`strlcpy` compiles and links without any extra library.

They are still **not standard C**, so portable code cannot assume them. But "not on Linux" is now out
of date, and you should check your target's glibc version rather than repeating the old advice.

---

## 6. The Failure Mode You Just Created

Bounded functions eliminate the overflow. They introduce **silent truncation** in its place.

```c
char user[8];
snprintf(user, sizeof user, "%s", "alexandra");   /* stores "alexand" */
```

No crash, no warning at run time, no corruption. Just wrong data — a username that does not match, a
path that points at the wrong file, a hash computed over a prefix.

**Truncation is a real failure and must be handled, not ignored:**

```c
int n = snprintf(user, sizeof user, "%s", name);
if (n >= (int)sizeof user) {
    fprintf(stderr, "name too long (%d chars, max %zu)\n", n, sizeof user - 1);
    return -1;
}
```

Whether truncation is acceptable is a *design* decision. Truncating a display label is usually fine;
truncating a filename, an authentication token, or a database key is a bug that will surface much
later and far away. Decide deliberately, and write down which one you chose.

---

## 7. The `sizeof` Trap

One more way bounds go wrong. Verified:

```
sizeof(arr) = 32   <- the array
sizeof(ptr) = 8    <- the POINTER
```

```c
void process(char *buf)
{
    snprintf(buf, sizeof buf, "...");   /* BUG: sizeof buf is 8, the pointer size */
}
```

Inside a function, an array parameter has **decayed to a pointer** (Lecture 1), so `sizeof` gives the
pointer's size — 8 on this machine — regardless of the array's real length. The bound is silently
wrong, and on a 32-bit build it would be 4 instead.

**A function that receives a buffer must also receive its size:**

```c
void process(char *buf, size_t cap)
{
    snprintf(buf, cap, "...");
}
```

`sizeof` is only trustworthy where the array is *declared*, in the scope that declares it.

---

## 8. Summary

| Idea | Takeaway |
|---|---|
| C checks no bounds | `strcpy` writes past the end without complaint |
| Never use | `gets` (removed from C11), `strcpy`, `strcat`, `sprintf` |
| `strncpy` | **Does not null-terminate** when the source fills the buffer |
| `strncpy` also | **Pads the whole buffer** with zeros — O(size), not O(strlen) |
| Its real purpose | Fixed-width UNIX directory fields, not general string copying |
| **`snprintf`** | Always terminates, no padding — the default choice |
| Its return value | The length it **wanted**; `n >= (int)size` means truncated |
| `snprintf(NULL, 0, …)` | Returns the required length — use it to size a `malloc` |
| `strncat`'s `n` | Max chars to **append**, not buffer size — inconsistent with `strncpy` |
| `strlcpy` | Not standard C, but **in glibc since 2.38** — the "Linux lacks it" advice is stale |
| New failure mode | Bounded calls trade overflow for **silent truncation** — handle it |
| `sizeof` on a parameter | Gives the **pointer** size; pass the capacity explicitly |
| Tooling | `-fsanitize=address` names the variable and offset precisely |

---

## Practice Exercises

Attempt each before reading the answers.

**1. (Trace.)** For `char d[6];`, give the exact bytes after each, marking any missing terminator:
(a) `strncpy(d, "abcdefgh", 6)`  (b) `strncpy(d, "ab", 6)`  (c) `snprintf(d, 6, "abcdefgh")`

**2. (Explain.)** Why is `if (n > sizeof dest)` a wrong truncation test for `snprintf`, on two
separate counts?

**3. (Fix.)** Four bugs.

```c
void make_path(char *out, const char *dir, const char *file)
{
    strcpy(out, dir);
    strcat(out, "/");
    strncat(out, file, sizeof out);
}
```

**4. (Stretch.)** Write `int join(char *dst, size_t cap, const char **parts, size_t n, const char *sep)`
that joins `n` strings with `sep`. Return 0 on success and −1 if the result would not fit. It must
never overflow, must always leave `dst` a valid string, and must be **O(total length)**.

### Answers

**1.**

| | Bytes | Terminated? |
|---|---|---|
| **(a)** `strncpy(d,"abcdefgh",6)` | `a b c d e f` | **No** — 6 bytes written, no room for `\0`. Not a string |
| **(b)** `strncpy(d,"ab",6)` | `a b \0 \0 \0 \0` | Yes — and note **all 6 bytes** were written; the tail is zero-padded |
| **(c)** `snprintf(d,6,"abcdefgh")` | `a b c d e \0` | Yes — 5 characters plus terminator; returns **8** |

(a) and (c) are the comparison that matters: given the same overlong input, `strncpy` produces
something unusable while `snprintf` produces a valid, truncated string *and* tells you it truncated.

**2.** Two independent errors.

**It is off by one.** `snprintf` writes at most `size - 1` characters plus a terminator. If `n` is
exactly `sizeof dest`, the content did not fit — one character was dropped. The correct boundary is
`n >= size`, not `n > size`.

**It compares signed against unsigned.** `n` is `int`; `sizeof` yields `size_t`, which is unsigned.
The usual arithmetic conversions turn `n` unsigned, so a negative `n` — which `snprintf` returns on
an encoding error — becomes a huge positive value and the test wrongly reports truncation. GCC's
`-Wsign-compare` flags it, and under `-Werror` it will not build.

```c
if (n < 0)                      { /* encoding error */ }
else if (n >= (int)sizeof dest) { /* truncated */ }
```

Both halves are needed: the cast, and the separate negative check *before* it.

**3.**

- **`strcpy(out, dir)` is unbounded.** No knowledge of `out`'s size.
- **`strcat(out, "/")` is unbounded.** Same problem.
- **`sizeof out` is the pointer size (8), not the buffer size.** `out` is a parameter and has decayed
  to a pointer, so the bound is meaningless — and it is a bound on *appending* anyway, which is not
  what the author intended.
- **The function never receives the buffer's capacity**, which is the root cause of the third bug and
  makes the first two impossible to fix in place.

```c
int make_path(char *out, size_t cap, const char *dir, const char *file)
{
    int n = snprintf(out, cap, "%s/%s", dir, file);
    if (n < 0 || n >= (int)cap) return -1;      /* truncated: report it */
    return 0;
}
```

One call replaces three, the bound is correct, the result is always terminated, and truncation is
reported rather than silently producing a wrong path — which for a filesystem path is exactly the
case where truncation must not pass unnoticed.

**4.**

```c
int join(char *dst, size_t cap, const char **parts, size_t n, const char *sep)
{
    if (cap == 0) return -1;
    dst[0] = '\0';                       /* valid string from the outset */

    size_t off = 0;
    for (size_t i = 0; i < n; i++) {
        int w = snprintf(dst + off, cap - off, "%s%s",
                         i ? sep : "", parts[i]);
        if (w < 0) return -1;
        if ((size_t)w >= cap - off) {    /* would not fit */
            dst[cap - 1] = '\0';         /* keep it a valid string */
            return -1;
        }
        off += (size_t)w;
    }
    return 0;
}
```

**Why each piece is needed:**

- **`cap == 0` first.** With no space at all, even writing a terminator is an overflow. Every later
  step assumes at least one byte.
- **`dst[0] = '\0'` immediately** guarantees the postcondition "`dst` is a valid string" even if the
  loop never runs (`n == 0`) or fails on the first part.
- **`cap - off` is the remaining space**, and it never underflows because `off` is only advanced
  after confirming `w < cap - off`.
- **The truncation check uses `>=`**, matching Exercise 2, and casts `w` to `size_t` only *after*
  testing `w < 0` — casting a negative to `size_t` first would produce an enormous value and pass the
  test.
- **On failure it still terminates `dst`** before returning, so a caller that ignores the return
  value still has a usable (if truncated) string rather than an unterminated buffer.

**Why it is O(total length):** each `snprintf` writes into `dst + off` and advances `off` by exactly
what it wrote, so every output byte is written once. The common wrong answer uses `strcat` in the
loop, which rescans the accumulated prefix on every iteration to find its end — that is **Θ(n²)** in
the total length, the same "Schlemiel the Painter" shape as naive string concatenation.

---

## Reading

- **`man 3 strncpy`** — read the BUGS/NOTES section; the manual itself warns you
- **`man 3 snprintf`** — the RETURN VALUE section is the whole lecture
- **`man 3 strlcpy`** — check whether your glibc has it
- **CWE-120, CWE-787** — the buffer-overflow entries in the Common Weakness Enumeration
- **C11 §7.24** — the string handling library; note `gets` is absent

---

*PROG 101 · Week 4 · Lecture 3 · © CSE Department*
