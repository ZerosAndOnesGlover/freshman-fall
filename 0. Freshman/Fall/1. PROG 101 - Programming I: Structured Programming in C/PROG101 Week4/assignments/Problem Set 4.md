# PROG 101 · Programming I: Structured Programming in C
## Week 4 · Problem Set 4: Arrays and Strings

**Released:** Friday 23 October 2026, 10:00 · Week 4 (after Thursday's Lecture 3)
**Due:** Friday 30 October 2026, 17:00 · Week 5 — late penalty from 17:01
**Submission:** Commit to the Freshman Fall repo under `"$PROG101/week4/ps4"`; submit the commit hash on the course portal.
**Total:** 100 points · **Expected time:** about 5 hours
**Build with:** `gcc -Wall -Wextra -Werror -pedantic -std=c11`
**Check with:** `-fsanitize=address,undefined` and `valgrind --leak-check=full --error-exitcode=1`

> Every submission must compile with **zero warnings** under the flags above. A warning is a defect.

---

## What this problem set uses

Weeks 0–4, above all this week's: arrays, passing them to functions with a length, 2-D arrays (Lecture 01),
strings as `char` arrays and the `const char *s` parameter style Lecture 02 writes its own `strlen` with,
`fgets`, `<ctype.h>`, `strcspn`, and bounded string handling with `snprintf` (Lecture 03).

**Not needed and not expected:** pointer arithmetic or pointers beyond Lecture 02's string parameters
(Week 5), `malloc` (Week 6), `struct`/`enum` (Week 7), `argc`/`argv`, recursion (Week 9), variadic
functions (never taught), `memcpy`.

---

## Problem 1: Array Algorithms (30 pts)

Create `array_algorithms.c` with these functions, each correct on empty arrays, single elements and duplicates:

```c
int  linear_search(const int arr[], int n, int target);   /* first index, or -1 */
int  binary_search(const int arr[], int n, int target);   /* sorted arr, O(log n), or -1 */
void insertion_sort(int arr[], int n);                    /* ascending, stable, in place */
int  remove_duplicates(int arr[], int n);                 /* sorted arr; returns new length */
void rotate_left(int arr[], int n, int k);                /* in place; k may exceed n */
int  count_inversions(const int arr[], int n);            /* pairs i < j with arr[i] > arr[j] */
void compute_prefix_sums(const int arr[], int n, long prefix[]);   /* prefix[0] = 0 ... prefix[n] */
long range_sum(const long prefix[], int l, int r);        /* sum of arr[l..r] in O(1) */
```

Examples: `remove_duplicates({1,1,2,3,3,3,4}, 7)` → `{1,2,3,4}`, returns `4`;
`rotate_left({1,2,3,4,5}, 5, 2)` → `{3,4,5,1,2}` (hint: reverse the first `k`, reverse the rest,
reverse the whole); `count_inversions({3,1,2}, 3)` → `2`; for `{2,4,6,8,10}`, `range_sum(prefix, 1, 3)` → `18`.

Write a `main` that checks every function on at least two inputs and prints `PASS`/`FAIL` with expected
and actual values. It returns non-zero if anything failed.

---

## Problem 2: A Text Pipeline (20 pts)

Create `text_pipeline.c`. Read lines from standard input with `fgets` into `char line[1024]`, strip the
`\n` (`line[strcspn(line, "\n")] = '\0';`), and pass every line through the same fixed pipeline:

**trim → upper-case → reverse → count words → number**, printing `N: LINE (k words)`.

```c
void apply_trim(char line[]);          /* remove leading and trailing whitespace, in place */
void apply_upper(char line[]);
void apply_reverse(char line[]);
int  count_words(const char line[]);   /* maximal runs of non-space characters */
```

```bash
$ printf '  hello world  \n  foo bar baz  \n' | ./text_pipeline
1: DLROW OLLEH (2 words)
2: ZAB RAB OOF (3 words)
```

Build the output line with `snprintf` into a buffer, never `sprintf`. Pass `char` values to `toupper` and
`isspace` as `(unsigned char)` (Lecture 02 §5). An empty or all-space line must print `N:  (0 words)`.

---

## Problem 3: Matrix Operations (20 pts)

Create `matrix.c`. A matrix is a 2-D array with a fixed column bound, and every function takes explicit sizes:

```c
#define MAX_DIM 10

void matrix_print(int mat[][MAX_DIM], int m, int n);                  /* aligned columns */
void matrix_add(int a[][MAX_DIM], int b[][MAX_DIM], int result[][MAX_DIM], int m, int n);
void matrix_multiply(int a[][MAX_DIM], int b[][MAX_DIM], int result[][MAX_DIM], int m, int n, int p);
void matrix_transpose(int mat[][MAX_DIM], int result[][MAX_DIM], int m, int n);
int  matrix_trace(int mat[][MAX_DIM], int n);
void matrix_identity(int mat[][MAX_DIM], int n);
```

(No `const` on the 2-D parameters: in C11, passing an `int[][10]` to a `const int[][10]` parameter is a
constraint violation that `-pedantic -Werror` rejects — try it, and record the message.)

Demonstrate with `A = {{1,2,3},{4,5,6},{7,8,9}}` and the 3×4 `B = {{1,0,2,1},{0,1,1,0},{2,1,0,1}}`: print
`A + A`, `A × B` (check one entry by hand in a comment), `Bᵀ`, `trace(A)`, and `A × I`.

---

## Problem 4: Safe String Building (30 pts)

Lecture 03 established that `strcpy`, `strcat` and `sprintf` cannot be used safely and that `strncpy`
does not null-terminate. Write `strbuild.c`:

```c
#define PART_LEN 32

/* Appends src to dst, which has total capacity cap (terminator included).
   Returns 0 on success, -1 if the result would not fit.
   On failure dst must still be a valid, null-terminated string. */
int sb_append(char dst[], size_t cap, const char src[]);

/* Joins n strings with sep into dst. Same contract as above.
   Must be O(total output length) -- no repeated rescanning of dst. */
int sb_join(char dst[], size_t cap, const char parts[][PART_LEN], size_t n, const char sep[]);
```

1. **No `strcpy`, `strcat`, `sprintf`, `gets`.** Their use is an automatic zero on this problem.
2. Neither function may ever write past `dst[cap - 1]`, and `dst` must be terminated on **every** path,
   including failure and `cap == 0`.
3. `sb_join` must remember where the output ends instead of calling `strlen(dst)` each time round the loop:
   rescanning makes it Θ(n²).
4. `main` tests at least: exact fit, one byte short, `cap == 0`, `cap == 1`, an empty `src`, and `n == 0`.

| Component | Points |
|---|---|
| `sb_append` correct, including all boundary cases | 10 |
| `sb_join` correct **and** O(total length) | 12 |
| Test suite covers the six required cases | 8 |

---

## Makefile

```makefile
CC = gcc
CFLAGS = -Wall -Wextra -Werror -pedantic -std=c11 -g

PROGRAMS = array_algorithms text_pipeline matrix strbuild

all: $(PROGRAMS)

%: %.c
	$(CC) $(CFLAGS) -o $@ $<

check: all
	./array_algorithms && ./strbuild && ./matrix > /dev/null
	valgrind --leak-check=full --error-exitcode=1 -q ./array_algorithms > /dev/null

clean:
	rm -f $(PROGRAMS)

.PHONY: all check clean
```

---

## Grading

| Problem | Points |
|---|---|
| 1 Array algorithms | 30 |
| 2 Text pipeline | 20 |
| 3 Matrix operations | 20 |
| 4 Safe string building | 30 |
| **Total** | **100** |

**Automatic deductions:** any compiler warning (−3 each); any ASan/UBSan report or Valgrind error (−5 each).

---

## Answer Key (Instructor Copy)

> **Do not distribute to students.** Everything below was built with gcc 13.3 under the flags above plus
> `-fsanitize=address,undefined`, and `make check` (including Valgrind) passes.

### Problem 1 (30) — reference

```c
/* array_algorithms.c — PS 4 Problem 1 (reference) */
#include <stdio.h>

int linear_search(const int arr[], int n, int target) {
    for (int i = 0; i < n; i++) {
        if (arr[i] == target) {
            return i;
        }
    }
    return -1;
}

int binary_search(const int arr[], int n, int target) {
    int lo = 0, hi = n - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (arr[mid] == target) {
            return mid;
        } else if (arr[mid] < target) {
            lo = mid + 1;
        } else {
            hi = mid - 1;
        }
    }
    return -1;
}

void insertion_sort(int arr[], int n) {
    for (int i = 1; i < n; i++) {
        int key = arr[i];
        int j = i - 1;
        while (j >= 0 && arr[j] > key) {
            arr[j + 1] = arr[j];
            j--;
        }
        arr[j + 1] = key;
    }
}

int remove_duplicates(int arr[], int n) {
    if (n == 0) {
        return 0;
    }
    int len = 1;
    for (int i = 1; i < n; i++) {
        if (arr[i] != arr[len - 1]) {
            arr[len] = arr[i];
            len++;
        }
    }
    return len;
}

static void reverse_range(int arr[], int lo, int hi) {
    while (lo < hi) {
        int t = arr[lo];
        arr[lo] = arr[hi];
        arr[hi] = t;
        lo++;
        hi--;
    }
}

void rotate_left(int arr[], int n, int k) {
    if (n == 0) {
        return;
    }
    k = k % n;
    reverse_range(arr, 0, k - 1);
    reverse_range(arr, k, n - 1);
    reverse_range(arr, 0, n - 1);
}

int count_inversions(const int arr[], int n) {
    int count = 0;
    for (int i = 0; i < n; i++) {
        for (int j = i + 1; j < n; j++) {
            if (arr[i] > arr[j]) {
                count++;
            }
        }
    }
    return count;
}

void compute_prefix_sums(const int arr[], int n, long prefix[]) {
    prefix[0] = 0;
    for (int i = 0; i < n; i++) {
        prefix[i + 1] = prefix[i] + arr[i];
    }
}

long range_sum(const long prefix[], int l, int r) {
    return prefix[r + 1] - prefix[l];
}

static int failures = 0;

static void check(const char *label, long got, long want) {
    printf("%s %-28s got %ld want %ld\n", got == want ? "PASS" : "FAIL", label, got, want);
    if (got != want) {
        failures++;
    }
}

static int same(const int a[], const int b[], int n) {
    for (int i = 0; i < n; i++) {
        if (a[i] != b[i]) {
            return 0;
        }
    }
    return 1;
}

int main(void) {
    int a[] = {5, 3, 8, 3, 1};
    check("linear_search hit", linear_search(a, 5, 3), 1);
    check("linear_search miss", linear_search(a, 5, 9), -1);
    check("linear_search empty", linear_search(a, 0, 5), -1);

    int sorted[] = {1, 3, 5, 7, 9, 11};
    check("binary_search first", binary_search(sorted, 6, 1), 0);
    check("binary_search last", binary_search(sorted, 6, 11), 5);
    check("binary_search miss", binary_search(sorted, 6, 4), -1);

    int s[] = {4, 2, 5, 1, 3};
    int s_want[] = {1, 2, 3, 4, 5};
    insertion_sort(s, 5);
    check("insertion_sort", same(s, s_want, 5), 1);

    int d[] = {1, 1, 2, 3, 3, 3, 4};
    int d_want[] = {1, 2, 3, 4};
    int d_len = remove_duplicates(d, 7);
    check("remove_duplicates length", d_len, 4);
    check("remove_duplicates contents", same(d, d_want, 4), 1);

    int r[] = {1, 2, 3, 4, 5};
    int r_want[] = {3, 4, 5, 1, 2};
    rotate_left(r, 5, 2);
    check("rotate_left by 2", same(r, r_want, 5), 1);
    int r2[] = {1, 2, 3};
    int r2_want[] = {2, 3, 1};
    rotate_left(r2, 3, 7);
    check("rotate_left by 7 (k > n)", same(r2, r2_want, 3), 1);

    int inv[] = {3, 1, 2};
    check("count_inversions {3,1,2}", count_inversions(inv, 3), 2);
    int rev[] = {4, 3, 2, 1};
    check("count_inversions reversed", count_inversions(rev, 4), 6);

    int p[] = {2, 4, 6, 8, 10};
    long prefix[6];
    compute_prefix_sums(p, 5, prefix);
    check("prefix[5] (total)", prefix[5], 30);
    check("range_sum(1, 3)", range_sum(prefix, 1, 3), 18);
    check("range_sum(0, 0)", range_sum(prefix, 0, 0), 2);

    printf("%d failure(s)\n", failures);
    return failures != 0;
}
```

Output: all 16 checks `PASS`, `0 failure(s)`. *3 per function (24) + 6 for the self-checking `main`.*
The classic bugs: `binary_search` computing `(lo + hi) / 2` (fine at these sizes, overflows for huge
arrays — mention but do not deduct); `rotate_left` without `k % n` (`k = 7`, `n = 3` fails).

### Problem 2 (20) — reference

```c
/* text_pipeline.c — PS 4 Problem 2 (reference): trim -> upper -> reverse -> count words -> number */
#include <ctype.h>
#include <stdio.h>
#include <string.h>

void apply_trim(char line[]) {
    size_t len = strlen(line);
    while (len > 0 && isspace((unsigned char)line[len - 1])) {
        line[--len] = '\0';
    }
    size_t start = 0;
    while (line[start] != '\0' && isspace((unsigned char)line[start])) {
        start++;
    }
    size_t i = 0;
    while (line[start + i] != '\0') {
        line[i] = line[start + i];
        i++;
    }
    line[i] = '\0';
}

void apply_upper(char line[]) {
    for (size_t i = 0; line[i] != '\0'; i++) {
        line[i] = (char)toupper((unsigned char)line[i]);
    }
}

void apply_reverse(char line[]) {
    size_t len = strlen(line);
    for (size_t i = 0; i < len / 2; i++) {
        char t = line[i];
        line[i] = line[len - 1 - i];
        line[len - 1 - i] = t;
    }
}

int count_words(const char line[]) {
    int words = 0;
    int in_word = 0;
    for (size_t i = 0; line[i] != '\0'; i++) {
        if (isspace((unsigned char)line[i])) {
            in_word = 0;
        } else if (!in_word) {
            in_word = 1;
            words++;
        }
    }
    return words;
}

int main(void) {
    char line[1024];
    int number = 0;
    while (fgets(line, sizeof line, stdin) != NULL) {
        line[strcspn(line, "\n")] = '\0';
        number++;
        apply_trim(line);
        apply_upper(line);
        apply_reverse(line);
        char out[1100];
        snprintf(out, sizeof out, "%d: %s (%d words)", number, line, count_words(line));
        puts(out);
    }
    return 0;
}
```

On `'  hello world  \n  foo bar baz  \n\n   \none\n'`:

```
1: DLROW OLLEH (2 words)
2: ZAB RAB OOF (3 words)
3:  (0 words)
4:  (0 words)
5: ENO (1 words)
```

*4 per stage (16) + 4 for `snprintf` and the `(unsigned char)` casts.* Words are counted after reversal,
which does not change the count.

### Problem 3 (20) — reference

```c
/* matrix.c — PS 4 Problem 3 (reference) */
#include <stdio.h>

#define MAX_DIM 10

void matrix_print(int mat[][MAX_DIM], int m, int n) {
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < n; j++) {
            printf("%5d", mat[i][j]);
        }
        printf("\n");
    }
}

void matrix_add(int a[][MAX_DIM], int b[][MAX_DIM], int result[][MAX_DIM], int m, int n) {
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < n; j++) {
            result[i][j] = a[i][j] + b[i][j];
        }
    }
}

void matrix_multiply(int a[][MAX_DIM], int b[][MAX_DIM], int result[][MAX_DIM],
                     int m, int n, int p) {
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < p; j++) {
            int sum = 0;
            for (int k = 0; k < n; k++) {
                sum += a[i][k] * b[k][j];
            }
            result[i][j] = sum;
        }
    }
}

void matrix_transpose(int mat[][MAX_DIM], int result[][MAX_DIM], int m, int n) {
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < n; j++) {
            result[j][i] = mat[i][j];
        }
    }
}

int matrix_trace(int mat[][MAX_DIM], int n) {
    int t = 0;
    for (int i = 0; i < n; i++) {
        t += mat[i][i];
    }
    return t;
}

void matrix_identity(int mat[][MAX_DIM], int n) {
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            mat[i][j] = (i == j);
        }
    }
}

int main(void) {
    int a[MAX_DIM][MAX_DIM] = {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}};
    int b[MAX_DIM][MAX_DIM] = {{1, 0, 2, 1}, {0, 1, 1, 0}, {2, 1, 0, 1}};
    int id[MAX_DIM][MAX_DIM];
    int r[MAX_DIM][MAX_DIM];

    printf("A + A:\n");
    matrix_add(a, a, r, 3, 3);
    matrix_print(r, 3, 3);
    printf("A x B (3x3 times 3x4):\n");
    matrix_multiply(a, b, r, 3, 3, 4);
    matrix_print(r, 3, 4);
    printf("B transposed (4x3):\n");
    matrix_transpose(b, r, 3, 4);
    matrix_print(r, 4, 3);
    printf("trace(A) = %d\n", matrix_trace(a, 3));
    matrix_identity(id, 3);
    matrix_multiply(a, id, r, 3, 3, 3);
    printf("A x I:\n");
    matrix_print(r, 3, 3);
    return 0;
}
```

```
A + A:
    2    4    6
    8   10   12
   14   16   18
A x B (3x3 times 3x4):
    7    5    4    4
   16   11   13   10
   25   17   22   16
B transposed (4x3):
    1    0    2
    0    1    1
    2    1    0
    1    0    1
trace(A) = 15
A x I:
    1    2    3
    4    5    6
    7    8    9
```

Hand check: row 1 of `A × B`, column 1 = `1·1 + 2·0 + 3·2 = 7`. *3 per function (18) + 2 for recording the
`const` message: "invalid use of pointers to arrays with different qualifiers in ISO C before C2X
[-Werror=pedantic]".*

### Problem 4 (30) — reference

```c
/* strbuild.c — PS 4 Problem 4 (reference) */
#include <stdio.h>
#include <string.h>

#define PART_LEN 32

/* Copies src (with its terminator) to dst[at...]; returns the new length. The caller has checked it fits. */
static size_t copy_at(char dst[], size_t at, const char src[]) {
    size_t i = 0;
    while (src[i] != '\0') {
        dst[at + i] = src[i];
        i++;
    }
    dst[at + i] = '\0';
    return at + i;
}

/* Appends src to dst (capacity cap, terminator included). 0 on success, -1 if it would not fit.
   dst stays a valid string on every path. */
int sb_append(char dst[], size_t cap, const char src[]) {
    if (cap == 0) {
        return -1;
    }
    size_t used = 0;
    while (used < cap && dst[used] != '\0') {   /* bounded strlen: never reads past cap */
        used++;
    }
    if (used == cap) {              /* dst was not terminated inside cap: repair it */
        dst[cap - 1] = '\0';
        return -1;
    }
    size_t add = strlen(src);
    if (used + add >= cap) {
        return -1;                  /* unchanged, still terminated */
    }
    copy_at(dst, used, src);
    return 0;
}

/* Joins n strings with sep into dst. O(total output length): tracks the end instead of rescanning. */
int sb_join(char dst[], size_t cap, const char parts[][PART_LEN], size_t n, const char sep[]) {
    if (cap == 0) {
        return -1;
    }
    dst[0] = '\0';
    size_t used = 0;
    size_t sep_len = strlen(sep);
    for (size_t i = 0; i < n; i++) {
        if (i > 0) {
            if (used + sep_len >= cap) {
                return -1;
            }
            used = copy_at(dst, used, sep);
        }
        size_t len = strlen(parts[i]);
        if (used + len >= cap) {
            return -1;
        }
        used = copy_at(dst, used, parts[i]);
    }
    return 0;
}

static int failures = 0;
static void check(const char label[], int ok) {
    printf("%s %s\n", ok ? "PASS" : "FAIL", label);
    failures += !ok;
}

int main(void) {
    char buf[8] = "abc";
    check("append exact fit (abc+dddd in 8)", sb_append(buf, 8, "dddd") == 0 && strcmp(buf, "abcdddd") == 0);
    char buf2[8] = "abc";
    check("append one byte short (abc+ddddd in 8)", sb_append(buf2, 8, "ddddd") == -1 && strcmp(buf2, "abc") == 0);
    char buf3[1] = "";
    check("append cap == 1", sb_append(buf3, 1, "x") == -1 && buf3[0] == '\0');
    check("append empty src", sb_append(buf, 8, "") == 0 && strcmp(buf, "abcdddd") == 0);
    char z[4] = "zz";
    check("append cap == 0", sb_append(z, 0, "x") == -1 && strcmp(z, "zz") == 0);

    const char parts[3][PART_LEN] = {"red", "green", "blue"};
    char out[32];
    check("join three", sb_join(out, sizeof out, parts, 3, ", ") == 0 && strcmp(out, "red, green, blue") == 0);
    check("join n == 0", sb_join(out, sizeof out, parts, 0, ", ") == 0 && strcmp(out, "") == 0);
    char small[16];
    check("join one byte short (16 chars in 16)", sb_join(small, sizeof small, parts, 3, "--") == -1 && strlen(small) < sizeof small);
    char fit[17];
    check("join exact fit (16 chars in 17)", sb_join(fit, sizeof fit, parts, 3, "--") == 0 && strcmp(fit, "red--green--blue") == 0);
    char tiny[10];
    check("join too small leaves a string", sb_join(tiny, sizeof tiny, parts, 3, ", ") == -1 && strlen(tiny) < sizeof tiny);
    printf("%d failure(s)\n", failures);
    return failures != 0;
}
```

```
PASS append exact fit (abc+dddd in 8)
PASS append one byte short (abc+ddddd in 8)
PASS append cap == 1
PASS append empty src
PASS append cap == 0
PASS join three
PASS join n == 0
PASS join one byte short (16 chars in 16)
PASS join exact fit (16 chars in 17)
PASS join too small leaves a string
0 failure(s)
```
