# PROG 101 — Programming I: Structured Programming in C
## Week 4 · Lab 4: Arrays, Strings, and a String Library

**Duration:** 2 hours · **Points:** 20 · **Room:** BH 215

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

    printf("  &a    = %p\n", (void *)&a);
    printf("  &a[0] = %p\n", (void *)&a[0]);
    printf("  a+1   = %p  (+%td bytes)\n", (void *)(a+1),  (char *)(a+1)  - (char *)a);
    printf("  &a+1  = %p  (+%td bytes)\n", (void *)(&a+1), (char *)(&a+1) - (char *)a);
    return 0;
}
```

**Record in `answers.md`:**

1. The two `sizeof` values, and why they differ. Name the mechanism.
2. `&a` and `&a[0]` print the same address. Why do `a+1` and `&a+1` then differ, and by how much?
3. Compile with `-Wsizeof-array-argument`. What does GCC say about `by_param`?

### 1B: Off-by-one, seen

Write a loop that writes `a[i] = i` for `i` from 0 to 10 **inclusive** — deliberately one too far.

1. Run it normally. Does it crash? What does it print?
2. Rebuild with `-fsanitize=address` and run again. Paste ASan's report into `answers.md`.
3. In one sentence: why is the ASan output more useful than the plain run?

---

## Part 2: String Processing Library (10 pts)

Build `strlib.h` and `strlib.c` — a complete string utility library.

### `strlib.h`

```c
/* strlib.h — String Processing Library
 * PROG 101, Week 2 Lab
 */
#ifndef STRLIB_H
#define STRLIB_H

#include <stddef.h>
#include <stdbool.h>

/* === LENGTH AND COPY === */

/* Return the length of s (not counting '\0'). */
size_t str_len(const char *s);

/* Copy src into dest (dest must have room for strlen(src)+1 bytes).
 * Returns dest. Guarantees null-termination. */
char *str_copy(char *dest, size_t dest_size, const char *src);

/* Append src to the end of dest.
 * dest_size is the total size of the dest buffer.
 * Guarantees null-termination and no overflow. Returns dest. */
char *str_append(char *dest, size_t dest_size, const char *src);

/* === COMPARISON AND SEARCH === */

/* Compare s1 and s2 lexicographically.
 * Returns 0 if equal, negative if s1 < s2, positive if s1 > s2. */
int str_compare(const char *s1, const char *s2);

/* Case-insensitive comparison. */
int str_compare_nocase(const char *s1, const char *s2);

/* Return pointer to first occurrence of c in s, or NULL. */
char *str_find_char(const char *s, char c);

/* Return pointer to last occurrence of c in s, or NULL. */
char *str_find_char_last(const char *s, char c);

/* Return pointer to first occurrence of needle in haystack, or NULL. */
char *str_find(const char *haystack, const char *needle);

/* Return 1 if s starts with prefix, 0 otherwise. */
int str_starts_with(const char *s, const char *prefix);

/* Return 1 if s ends with suffix, 0 otherwise. */
int str_ends_with(const char *s, const char *suffix);

/* === TRANSFORMATION === */

/* Convert s to uppercase in-place. Returns s. */
char *str_to_upper(char *s);

/* Convert s to lowercase in-place. Returns s. */
char *str_to_lower(char *s);

/* Reverse s in-place. Returns s. */
char *str_reverse(char *s);

/* Remove leading whitespace from s in-place. Returns s. */
char *str_trim_left(char *s);

/* Remove trailing whitespace from s in-place. Returns s. */
char *str_trim_right(char *s);

/* Remove both leading and trailing whitespace. Returns s. */
char *str_trim(char *s);

/* Replace all occurrences of old_char with new_char in s in-place.
 * Returns the number of replacements made. */
int str_replace_char(char *s, char old_char, char new_char);

/* === ANALYSIS === */

/* Return the number of occurrences of c in s. */
int str_count_char(const char *s, char c);

/* Return the number of words in s (separated by whitespace). */
int str_word_count(const char *s);

/* Return 1 if s is a palindrome (same forwards and backwards), 0 otherwise.
 * Case-sensitive. */
int str_is_palindrome(const char *s);

/* Return 1 if s contains only digit characters ('0'-'9'), 0 otherwise.
 * Empty string returns 0. */
int str_is_numeric(const char *s);

/* Return 1 if s contains only alphabetic characters, 0 otherwise.
 * Empty string returns 0. */
int str_is_alpha(const char *s);

#endif /* STRLIB_H */
```

### `strlib.c` — Implementation Requirements

- **No standard string functions** (`strlen`, `strcpy`, `strcmp`, etc.) — implement everything from scratch using only character comparisons and `<ctype.h>`
- Exception: you may use `memmove` in `str_trim_left`
- Document every function with a brief comment explaining the approach
- Handle edge cases: NULL is never passed (you may assume valid pointers), but empty strings `""` must work correctly

### `test_strlib.c` — Test Suite

Write thorough tests. Use this structure:

```c
#include <stdio.h>
#include <string.h>
#include "strlib.h"

static int passed = 0, failed = 0;

#define CHECK_INT(desc, expected, actual) do { \
    if ((int)(expected) == (int)(actual)) { \
        printf("  PASS: %s\n", desc); passed++; \
    } else { \
        printf("  FAIL: %s → expected %d, got %d\n", desc, (int)(expected), (int)(actual)); \
        failed++; \
    } \
} while(0)

#define CHECK_STR(desc, expected, actual) do { \
    if (strcmp((expected), (actual)) == 0) { \
        printf("  PASS: %s\n", desc); passed++; \
    } else { \
        printf("  FAIL: %s → expected \"%s\", got \"%s\"\n", desc, (expected), (actual)); \
        failed++; \
    } \
} while(0)

#define CHECK_NULL(desc, actual) do { \
    if ((actual) == NULL) { \
        printf("  PASS: %s\n", desc); passed++; \
    } else { \
        printf("  FAIL: %s → expected NULL\n", desc); failed++; \
    } \
} while(0)

void test_str_len(void) {
    printf("=== str_len ===\n");
    CHECK_INT("empty string",   0, str_len(""));
    CHECK_INT("single char",    1, str_len("a"));
    CHECK_INT("hello",          5, str_len("hello"));
    CHECK_INT("with spaces",    9, str_len("hello bob"));
    CHECK_INT("null bytes won't appear, but newline", 6, str_len("a\nb\nc\n"));
}

void test_str_compare(void) {
    printf("=== str_compare ===\n");
    CHECK_INT("equal strings",     0,  str_compare("hello", "hello"));
    CHECK_INT("empty equals empty",0,  str_compare("", ""));
    CHECK_INT("a < b",            -1,  str_compare("a", "b") < 0 ? -1 : 1);
    CHECK_INT("b > a",             1,  str_compare("b", "a") > 0 ? 1 : -1);
    CHECK_INT("prefix < full",    -1,  str_compare("hell", "hello") < 0 ? -1 : 1);
}

/* TODO: Write test functions for EVERY function in strlib.h */
/* At minimum 4 test cases per function, covering:
 *   - Normal case
 *   - Empty string
 *   - Edge case (single char, not found, etc.)
 *   - A case you would have missed if you only tested the happy path
 */

int main(void) {
    test_str_len();
    test_str_compare();
    /* TODO: call all test functions */

    printf("\n=== Results: %d passed, %d failed ===\n", passed, failed);
    return failed > 0 ? 1 : 0;
}
```

---

---

## Part 3: Text Decomposition (5 pts)

Create `word_stats.c` — a program that reads text from stdin and prints statistics.

### Required Output Format

```
$ echo "The quick brown fox jumps over the lazy dog" | ./word_stats

=== Text Statistics ===
Characters (total):    44
Characters (no spaces): 35
Words:                  9
Lines:                  1
Longest word:           'jumps' (5 chars)
Shortest word:          'The' (3 chars)
Vowels:                 11
Consonants:             24
Digits:                 0
Uppercase letters:      1
Lowercase letters:      34
Most frequent char:     'o' (4 times)
```

### Decomposition Requirements

You **must** decompose this into separate functions. Each function must:
- Do exactly one thing
- Have a clear, descriptive name
- Be no longer than 20 lines
- Be individually testable

Required function signatures (implement all):

```c
/* Count total characters (excluding EOF) */
int count_chars(const char *text);

/* Count non-whitespace characters */
int count_non_space(const char *text);

/* Count words (whitespace-delimited) */
int count_words(const char *text);

/* Count lines ('\n' characters, or 1 if no '\n' but text is non-empty) */
int count_lines(const char *text);

/* Find the longest word; copy it into result (result_size bytes max).
 * Returns the length of the longest word. */
int find_longest_word(const char *text, char *result, size_t result_size);

/* Find the shortest word; copy it into result.
 * Returns the length of the shortest word. */
int find_shortest_word(const char *text, char *result, size_t result_size);

/* Count vowels (a,e,i,o,u — case insensitive) */
int count_vowels(const char *text);

/* Count consonants (alphabetic, non-vowel) */
int count_consonants(const char *text);

/* Count digit characters */
int count_digits(const char *text);

/* Count uppercase letters */
int count_uppercase(const char *text);

/* Count lowercase letters */
int count_lowercase(const char *text);

/* Find the most frequent character (any character, including space).
 * On ties, return the one with the lower ASCII value.
 * Stores the frequency in *freq. Returns the character. */
char most_frequent_char(const char *text, int *freq);
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

*PROG 101 · Week 4 · Lab 4 · © CSE Department*
