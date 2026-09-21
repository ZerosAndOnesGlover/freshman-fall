# PROG 101 · Lab 4 Solutions (Instructor)
## Arrays, Strings, and a String Library

> Lab sat Monday 26 October 2026. Revised 2026-09-21: pointer arithmetic removed from Part 1 (Week 5),
> `strlib` cut to fifteen functions that return indices rather than pointers, test macros replaced by
> functions (macros are Week 10), Part 3 trimmed. Everything below was built with gcc 13.3 under
> `-Wall -Wextra -Werror -pedantic -std=c11 -fsanitize=address,undefined` and run; Valgrind clean.

---

## Part 1: Arrays, Decay, and Bounds (5 pts)

### 1A — expected output

```
  in main:         sizeof(a) = 40
  elements:        10
  inside function: sizeof(a) = 8
```

**Answer 1 (3 pts).** 40 versus 8. In `main`, `a` names an actual array so `sizeof` reports its full
extent. In a parameter list C **adjusts** `int a[10]` to `int *a` — the `10` is discarded entirely —
so `sizeof` reports the pointer's size. The mechanism is **array-to-pointer decay**.

*Full marks require naming decay.* "It becomes a pointer" earns 1 without the term.

**Answer 2 (1 pt).**

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

`strlib.c`:

```c
/* strlib.c — no <string.h>: every function works character by character */
#include <ctype.h>
#include "strlib.h"

size_t str_len(const char *s) {
    size_t n = 0;
    while (s[n] != '\0') {
        n++;
    }
    return n;
}

int str_copy(char *dest, size_t dest_size, const char *src) {
    if (dest_size == 0) {
        return -1;
    }
    size_t i = 0;
    while (src[i] != '\0' && i + 1 < dest_size) {
        dest[i] = src[i];
        i++;
    }
    dest[i] = '\0';
    return src[i] == '\0' ? 0 : -1;
}

int str_append(char *dest, size_t dest_size, const char *src) {
    size_t used = 0;
    while (used < dest_size && dest[used] != '\0') {
        used++;
    }
    if (used == dest_size) {
        return -1;
    }
    size_t need = str_len(src);
    if (used + need >= dest_size) {
        return -1;                      /* unchanged, still terminated */
    }
    for (size_t i = 0; i <= need; i++) {
        dest[used + i] = src[i];
    }
    return 0;
}

int str_compare(const char *s1, const char *s2) {
    size_t i = 0;
    while (s1[i] != '\0' && s1[i] == s2[i]) {
        i++;
    }
    return (unsigned char)s1[i] - (unsigned char)s2[i];
}

int str_compare_nocase(const char *s1, const char *s2) {
    size_t i = 0;
    while (s1[i] != '\0' && tolower((unsigned char)s1[i]) == tolower((unsigned char)s2[i])) {
        i++;
    }
    return tolower((unsigned char)s1[i]) - tolower((unsigned char)s2[i]);
}

int str_find_char(const char *s, char c) {
    for (int i = 0; s[i] != '\0'; i++) {
        if (s[i] == c) {
            return i;
        }
    }
    return -1;
}

int str_find(const char *haystack, const char *needle) {
    size_t n = str_len(haystack), m = str_len(needle);
    for (size_t i = 0; i + m <= n; i++) {
        size_t j = 0;
        while (j < m && haystack[i + j] == needle[j]) {
            j++;
        }
        if (j == m) {
            return (int)i;
        }
    }
    return -1;
}

int str_starts_with(const char *s, const char *prefix) {
    for (size_t i = 0; prefix[i] != '\0'; i++) {
        if (s[i] != prefix[i]) {
            return 0;
        }
    }
    return 1;
}

int str_ends_with(const char *s, const char *suffix) {
    size_t n = str_len(s), m = str_len(suffix);
    if (m > n) {
        return 0;
    }
    for (size_t i = 0; i < m; i++) {
        if (s[n - m + i] != suffix[i]) {
            return 0;
        }
    }
    return 1;
}

void str_to_upper(char *s) {
    for (size_t i = 0; s[i] != '\0'; i++) {
        s[i] = (char)toupper((unsigned char)s[i]);
    }
}

void str_reverse(char *s) {
    size_t n = str_len(s);
    for (size_t i = 0; i < n / 2; i++) {
        char t = s[i];
        s[i] = s[n - 1 - i];
        s[n - 1 - i] = t;
    }
}

void str_trim(char *s) {
    size_t n = str_len(s);
    while (n > 0 && isspace((unsigned char)s[n - 1])) {
        n--;
    }
    s[n] = '\0';
    size_t start = 0;
    while (isspace((unsigned char)s[start])) {
        start++;
    }
    size_t i = 0;
    while (s[start + i] != '\0') {
        s[i] = s[start + i];
        i++;
    }
    s[i] = '\0';
}

int str_count_char(const char *s, char c) {
    int count = 0;
    for (size_t i = 0; s[i] != '\0'; i++) {
        if (s[i] == c) {
            count++;
        }
    }
    return count;
}

int str_word_count(const char *s) {
    int words = 0, in_word = 0;
    for (size_t i = 0; s[i] != '\0'; i++) {
        if (isspace((unsigned char)s[i])) {
            in_word = 0;
        } else if (!in_word) {
            in_word = 1;
            words++;
        }
    }
    return words;
}

int str_is_palindrome(const char *s) {
    size_t n = str_len(s);
    for (size_t i = 0; i < n / 2; i++) {
        if (s[i] != s[n - 1 - i]) {
            return 0;
        }
    }
    return 1;
}
```

A full test file (30 checks, all pass):

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

static int sign(int x) { return (x > 0) - (x < 0); }

int main(void) {
    check_int("len empty", 0, (int)str_len(""));
    check_int("len hello", 5, (int)str_len("hello"));
    char buf[8];
    check_int("copy fits", 0, str_copy(buf, sizeof buf, "abc"));
    check_str("copy contents", "abc", buf);
    check_int("copy too long", -1, str_copy(buf, sizeof buf, "abcdefghij"));
    check_str("copy truncated but terminated", "abcdefg", buf);
    char ap[8] = "ab";
    check_int("append fits exactly", 0, str_append(ap, sizeof ap, "cdefg"));
    check_str("append contents", "abcdefg", ap);
    check_int("append one short", -1, str_append(ap, sizeof ap, "h"));
    check_str("append unchanged on failure", "abcdefg", ap);
    check_int("compare equal", 0, sign(str_compare("hello", "hello")));
    check_int("compare prefix", -1, sign(str_compare("hell", "hello")));
    check_int("compare nocase", 0, sign(str_compare_nocase("HeLLo", "hello")));
    check_int("find_char hit", 2, str_find_char("hello", 'l'));
    check_int("find_char miss", -1, str_find_char("hello", 'z'));
    check_int("find hit", 6, str_find("hello world", "world"));
    check_int("find empty needle", 0, str_find("abc", ""));
    check_int("find miss", -1, str_find("aaa", "aab"));
    check_int("starts_with", 1, str_starts_with("prefix", "pre"));
    check_int("ends_with too long", 0, str_ends_with("fix", "suffix"));
    char u[] = "MiXeD 1!";
    str_to_upper(u);
    check_str("to_upper", "MIXED 1!", u);
    char r[] = "abcd";
    str_reverse(r);
    check_str("reverse even", "dcba", r);
    char e[] = "";
    str_reverse(e);
    check_str("reverse empty", "", e);
    char t[] = "  \t hi there \n";
    str_trim(t);
    check_str("trim", "hi there", t);
    char blank[] = "   ";
    str_trim(blank);
    check_str("trim all spaces", "", blank);
    check_int("count_char", 3, str_count_char("banana", 'a'));
    check_int("word_count", 3, str_word_count("  one two\tthree \n"));
    check_int("word_count empty", 0, str_word_count(""));
    check_int("palindrome", 1, str_is_palindrome("racecar"));
    check_int("not palindrome", 0, str_is_palindrome("ab"));
    printf("\n=== Results: %d passed, %d failed ===\n", passed, failed);
    return failed > 0;
}
```

**Marking.** 10 for all fifteen correct with at least two tests each; −1 per function that fails an edge case
(`""`, not-found, exact fit). The three that separate marks: `str_copy`/`str_append` terminating on
failure; `str_find("abc", "")` returning 0; `str_compare` comparing as `unsigned char`.

---

## Part 3: Text Decomposition (5 pts)

```c
/* word_stats.c — Lab 4 Part 3 (reference) */
#include <ctype.h>
#include <stdio.h>

#define MAX_TEXT_SIZE 65536

int count_chars(const char *text) {
    int n = 0;
    while (text[n] != '\0') {
        n++;
    }
    return n;
}

int count_non_space(const char *text) {
    int n = 0;
    for (int i = 0; text[i] != '\0'; i++) {
        if (!isspace((unsigned char)text[i])) {
            n++;
        }
    }
    return n;
}

int count_words(const char *text) {
    int words = 0, in_word = 0;
    for (int i = 0; text[i] != '\0'; i++) {
        if (isspace((unsigned char)text[i])) {
            in_word = 0;
        } else if (!in_word) {
            in_word = 1;
            words++;
        }
    }
    return words;
}

int count_lines(const char *text) {
    int lines = 0, last = '\n';
    for (int i = 0; text[i] != '\0'; i++) {
        if (text[i] == '\n') {
            lines++;
        }
        last = text[i];
    }
    return (last != '\n') ? lines + 1 : lines;    /* a final line without '\n' still counts */
}

/* Copies the first longest word into result; returns its length. */
int find_longest_word(const char *text, char *result, size_t result_size) {
    int best_start = 0, best_len = 0, i = 0;
    while (text[i] != '\0') {
        while (text[i] != '\0' && isspace((unsigned char)text[i])) {
            i++;
        }
        int start = i;
        while (text[i] != '\0' && !isspace((unsigned char)text[i])) {
            i++;
        }
        if (i - start > best_len) {
            best_start = start;
            best_len = i - start;
        }
    }
    size_t k = 0;                                 /* copy, never past result_size - 1 */
    while ((int)k < best_len && k + 1 < result_size) {
        result[k] = text[best_start + (int)k];
        k++;
    }
    result[k] = '\0';
    return best_len;
}

int count_vowels(const char *text) {
    int n = 0;
    for (int i = 0; text[i] != '\0'; i++) {
        char c = (char)tolower((unsigned char)text[i]);
        if (c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u') {
            n++;
        }
    }
    return n;
}

int count_digits(const char *text) {
    int n = 0;
    for (int i = 0; text[i] != '\0'; i++) {
        if (isdigit((unsigned char)text[i])) {
            n++;
        }
    }
    return n;
}

int main(void) {
    char text[MAX_TEXT_SIZE];
    size_t total = 0;
    int c;
    while ((c = getchar()) != EOF && total < MAX_TEXT_SIZE - 1) {
        text[total++] = (char)c;
    }
    text[total] = '\0';

    char longest[64];
    int longest_len = find_longest_word(text, longest, sizeof longest);
    printf("=== Text Statistics ===\n");
    printf("Characters (total):     %d\n", count_chars(text));
    printf("Characters (no spaces): %d\n", count_non_space(text));
    printf("Words:                  %d\n", count_words(text));
    printf("Lines:                  %d\n", count_lines(text));
    printf("Longest word:           '%s' (%d chars)\n", longest, longest_len);
    printf("Vowels:                 %d\n", count_vowels(text));
    printf("Digits:                 %d\n", count_digits(text));
    return 0;
}
```

Verified: the fox sentence gives `44 / 35 / 9 / 1 / 'quick' (5) / 11 / 0`; `printf 'a1 bb2\nccc'` gives
`10 / 8 / 3 / 2 / 'bb2' (3) / 1 / 2`; empty input gives zeros and `''`.
