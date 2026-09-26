# PROG 101 · Programming I: Structured Programming in C
## Week 4 · Lab 4: Arrays, Strings, and a String Library

**Duration:** 2 hours · **Points:** 20 · **Room:** BH 215
**Date:** Monday 26 October 2026 · 15:00–16:50 · Lab Section (Week 5) — covers Week 4 (Lectures 01–03)

**Tools used:** Weeks 0–4 — arrays, strings with Lecture 02's `const char *s` parameters, `<ctype.h>`,
bounded copying. Not pointer arithmetic (Week 5), macros beyond `#define` constants (Week 10), or `memmove`.

**Build with:** `gcc -Wall -Wextra -Werror -pedantic -std=c11`
**Check with:** `valgrind --leak-check=full --error-exitcode=1`

---

## Overview

Week 4's lectures covered arrays as contiguous storage, strings as null-terminated character arrays,
and the bounded string functions. This lab makes all three concrete: you will observe array decay
first-hand, implement the core of `<string.h>` yourself, and build a small text pipeline.

You will finish with a working `strlib` you understand completely — which is the point. Every
function you write here you have used since Week 2 without knowing what was inside it.

---

## Part 1: Arrays, Decay, and Bounds (5 pts)

### 1A: Watching decay happen

Create `decay.c`:

```c
#include <stdio.h>

static void by_param(int a[10])
{
    printf("  inside function: sizeof(a) = %zu\n", sizeof a);
}

int main(void)
{
    int a[10] = {0};
    printf("  in main:         sizeof(a) = %zu\n", sizeof a);
    printf("  elements:        %zu\n", sizeof a / sizeof a[0]);
    by_param(a);

    return 0;
}
```

**Record in `answers.md`:**

1. The two `sizeof` values, and why they differ. Name the mechanism.
2. Compile with `-Wsizeof-array-argument`. What does GCC say about `by_param`?

### 1B: Off-by-one, seen

Write a loop that writes `a[i] = i` for `i` from 0 to 10 **inclusive** — deliberately one too far.

1. Run it normally. Does it crash? What does it print?
2. Rebuild with `-fsanitize=address` and run again. Paste ASan's report into `answers.md`.
3. In one sentence: why is the ASan output more useful than the plain run?

---

## Part 2: String Processing Library (10 pts)

Build `strlib.h` and `strlib.c` — ten string functions written from scratch.
*(Revised 2026-09-26: cut from fifteen functions, and `word_stats` from seven counters to four, so the lab
fits its session.)* Every "find" returns an
**index** (or `-1`), not a pointer: pointers into strings are Week 5.

### `strlib.h`

```c
/* strlib.h — Lab 4: a small string library, written from scratch */
#ifndef STRLIB_H
#define STRLIB_H

#include <stddef.h>

size_t str_len(const char *s);
int    str_copy(char *dest, size_t dest_size, const char *src);     /* 0, or -1 if it did not fit (dest still terminated) */
int    str_append(char *dest, size_t dest_size, const char *src);   /* same contract */
int    str_compare(const char *s1, const char *s2);                 /* <0, 0, >0 like strcmp */
int    str_find_char(const char *s, char c);                        /* index of first c, or -1 */
int    str_find(const char *haystack, const char *needle);          /* index of first match, or -1; "" matches at 0 */
void   str_to_upper(char *s);
void   str_reverse(char *s);
void   str_trim(char *s);                                           /* leading and trailing whitespace, in place */
int    str_word_count(const char *s);

#endif
```

### `strlib.c` — Implementation Requirements

- **No `<string.h>` at all** — only character comparisons and `<ctype.h>`. Pass `char` values to
  `<ctype.h>` functions as `(unsigned char)` (Lecture 02 §5).
- `str_copy` and `str_append` follow the bounded contract of Lecture 03: never write past
  `dest[dest_size - 1]`, always leave `dest` terminated, return `-1` when the text would not fit.
- Empty strings `""` must work in every function. You may assume no argument is `NULL`.

### `test_strlib.c` — Test Suite

Use two small test functions (not macros — function-like macros and their traps are Week 10):

```c
#include <stdio.h>
#include <string.h>
#include "strlib.h"

static int passed = 0, failed = 0;

static void check_int(const char *desc, int expected, int actual) {
    if (expected == actual) {
        printf("  PASS: %s\n", desc);
        passed++;
    } else {
        printf("  FAIL: %s -> expected %d, got %d\n", desc, expected, actual);
        failed++;
    }
}

static void check_str(const char *desc, const char *expected, const char *actual) {
    if (strcmp(expected, actual) == 0) {
        printf("  PASS: %s\n", desc);
        passed++;
    } else {
        printf("  FAIL: %s -> expected \"%s\", got \"%s\"\n", desc, expected, actual);
        failed++;
    }
}

int main(void) {
    check_int("len empty", 0, (int)str_len(""));
    check_int("len hello", 5, (int)str_len("hello"));
    /* TODO: at least two checks per function, including one edge case each */
    printf("\n=== Results: %d passed, %d failed ===\n", passed, failed);
    return failed > 0;
}
```

---

## Part 3: Text Decomposition (5 pts)

Create `word_stats.c` — a program that reads text from stdin and prints statistics.

### Required Output Format

```
$ echo "The quick brown fox jumps over the lazy dog" | ./word_stats
=== Text Statistics ===
Characters (total):     44
Words:                  9
Lines:                  1
Longest word:           'quick' (5 chars)
```

(The total is 44 because `echo` adds a newline. On a tie for longest, keep the **first** word.)

### Decomposition Requirements

One job per function, each short enough to read at a glance:

```c
int count_chars(const char *text);
int count_words(const char *text);
int count_lines(const char *text);      /* '\n' count, plus 1 if the text ends without one */
int find_longest_word(const char *text, char *result, size_t result_size);  /* copies the word; returns its length */
```

### Reading All of Stdin

```c
/* Read all of stdin into a buffer (max MAX_TEXT_SIZE bytes) */
#define MAX_TEXT_SIZE 65536

char text[MAX_TEXT_SIZE];
size_t total = 0;
int c;
while ((c = getchar()) != EOF && total < MAX_TEXT_SIZE - 1) {
    text[total++] = (char)c;
}
text[total] = '\0';
```

---

---

## Deliverables

Submit a single archive containing:

- `decay.c`, and the off-by-one program from 1B
- `strlib.h`, `strlib.c`, `test_strlib.c`
- The Part 3 decomposition program
- `answers.md` with all recorded answers
- A `Makefile` that builds everything with the required flags

## Grading

| Component | Points |
|---|---|
| Part 1: decay observed and explained; ASan report included | 5 |
| Part 2: `strlib` functions correct, tests pass, Valgrind clean | 10 |
| Part 3: decomposition correct and cleanly factored | 5 |
| **Total** | **20** |

**Automatic deductions:** any compiler warning (−2 each); any Valgrind error (−3 each); use of
`strcpy`, `strcat`, `sprintf` or `gets` outside a deliberate demonstration (−5).

---

*PROG 101 · Week 4 · Lab 4 · Monday 26 October 2026 · © CSE Department*
