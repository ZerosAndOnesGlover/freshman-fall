# PROG 101 · Programming I: Structured Programming in C
## Week 4 · Problem Set 4: Arrays and Strings

**Released:** Friday, Week 4 · **Due:** Friday, Week 5 at 17:00
**Total:** 100 points
**Build with:** `gcc -Wall -Wextra -Werror -pedantic -std=c11`
**Check with:** `valgrind --leak-check=full --error-exitcode=1` and `-fsanitize=address,undefined`

> Every submission must compile with **zero warnings** under the flags above. A warning is a defect.

---
## Problem 1: Array Algorithms (20 pts)

Create `array_algorithms.c`. Implement all functions below with their full signatures. Each must be correct for all inputs including edge cases (empty arrays, single element, duplicates).

```c
/* === Searching === */

/* Linear search: return index of first occurrence of target in arr[0..n-1],
 * or -1 if not found. */
int linear_search(const int arr[], int n, int target);

/* Binary search: return index of target in SORTED arr[0..n-1], or -1.
 * Must be O(log n). */
int binary_search(const int arr[], int n, int target);

/* Return the index of the minimum element in arr[0..n-1].
 * On ties, return the index of the first minimum. */
int find_min_index(const int arr[], int n);

/* Return the index of the maximum element. */
int find_max_index(const int arr[], int n);

/* === Sorting === */

/* Insertion sort: sort arr[0..n-1] in ascending order in-place.
 * Must be O(n²) worst case, O(n) best case (already sorted).
 * Stable: equal elements keep their original relative order. */
void insertion_sort(int arr[], int n);

/* Selection sort: sort arr[0..n-1] in-place.
 * Always O(n²) — finds the minimum and swaps it into position. */
void selection_sort(int arr[], int n);

/* === Transformation === */

/* Remove all occurrences of value from arr[0..n-1] in-place.
 * Compacts remaining elements to the front.
 * Returns the new length of the array.
 * Example: remove_value({1,3,2,3,4,3}, 6, 3) → {1,2,4}, returns 3 */
int remove_value(int arr[], int n, int value);

/* Remove duplicates from a SORTED array in-place.
 * Returns the new length (unique elements only).
 * Example: remove_duplicates({1,1,2,3,3,3,4}, 7) → {1,2,3,4}, returns 4 */
int remove_duplicates(int arr[], int n);

/* Rotate arr[0..n-1] left by k positions in-place.
 * Example: rotate_left({1,2,3,4,5}, 5, 2) → {3,4,5,1,2}
 * Hint: use the reverse trick — O(n), O(1) extra space */
void rotate_left(int arr[], int n, int k);

/* === Analysis === */

/* Return 1 if arr[0..n-1] is sorted in ascending order, 0 otherwise.
 * An array of 0 or 1 elements is considered sorted. */
int is_sorted(const int arr[], int n);

/* Return the number of inversions in arr[0..n-1].
 * An inversion is a pair (i, j) where i < j and arr[i] > arr[j].
 * O(n²) is acceptable. */
int count_inversions(const int arr[], int n);

/* Compute and store the prefix sums of arr[0..n-1] in prefix[0..n].
 * prefix[0] = 0, prefix[i] = arr[0] + arr[1] + ... + arr[i-1]
 * prefix[n] = sum of all elements.
 * This allows O(1) range sum queries: sum(l..r) = prefix[r+1] - prefix[l] */
void compute_prefix_sums(const int arr[], int n, long prefix[]);

/* Given precomputed prefix sums, return the sum of arr[l..r] (inclusive).
 * Precondition: 0 <= l <= r < n */
long range_sum(const long prefix[], int l, int r);
```

Write a `main()` that tests each function with a variety of inputs. Print "PASS" or "FAIL" with expected vs actual values.

---

## Problem 2: String Processing Pipeline (20 pts)

Create `text_pipeline.c` — a program that applies a series of transformations to text.

### The Pipeline

The program reads lines from stdin and processes them through a pipeline of filters, each toggled by command-line flags:

```bash
./text_pipeline [--upper] [--reverse] [--trim] [--count-words] [--number]
```

- `--upper`: Convert each line to uppercase
- `--reverse`: Reverse each line
- `--trim`: Remove leading and trailing whitespace
- `--count-words`: Append ` (N words)` to each line
- `--number`: Prepend line number: `1: `, `2: `, etc.

Filters apply in this order: trim → upper → reverse → count-words → number.

```bash
$ echo -e "  hello world  \n  foo bar baz  " | ./text_pipeline --trim --upper --number
1: HELLO WORLD
2: FOO BAR BAZ

$ echo -e "hello\nworld" | ./text_pipeline --reverse --number
1: olleh
2: dlrow
```

### Requirements

```c
/* Apply each transformation as a separate function: */
void apply_trim(char *line);
void apply_upper(char *line);
void apply_reverse(char *line);
void apply_count_words(char *line, size_t line_size);
void apply_number(char *line, size_t line_size, int line_num);

/* Parse flags from argc/argv */
typedef struct {
    int do_upper;
    int do_reverse;
    int do_trim;
    int do_count_words;
    int do_number;
} PipelineFlags;

PipelineFlags parse_flags(int argc, char *argv[]);
```

- Each line buffer must be `char line[1024]`
- Use `fgets` for safe input reading
- Strip the trailing `\n` from `fgets` output
- Unknown flags print a usage message and exit with code 1
- Zero flags: print lines unchanged (passthrough)

---

## Problem 3: Matrix Operations (15 pts)

Create `matrix.c`. A matrix is represented as a 2D array. All functions take explicit row and column counts.

```c
#define MAX_DIM 10

/* Print an m×n matrix with aligned columns */
void matrix_print(const int mat[][MAX_DIM], int m, int n);

/* Add two m×n matrices: result = a + b */
void matrix_add(const int a[][MAX_DIM], const int b[][MAX_DIM],
                int result[][MAX_DIM], int m, int n);

/* Multiply m×n matrix a by n×p matrix b, store in m×p result */
void matrix_multiply(const int a[][MAX_DIM], const int b[][MAX_DIM],
                     int result[][MAX_DIM], int m, int n, int p);

/* Transpose an m×n matrix: result is n×m */
void matrix_transpose(const int mat[][MAX_DIM], int result[][MAX_DIM],
                      int m, int n);

/* Return the trace of a square n×n matrix (sum of diagonal elements) */
int matrix_trace(const int mat[][MAX_DIM], int n);

/* Return 1 if the n×n matrix is symmetric (mat[i][j] == mat[j][i]), 0 otherwise */
int matrix_is_symmetric(const int mat[][MAX_DIM], int n);

/* Fill matrix with the n×n identity matrix (1s on diagonal, 0s elsewhere) */
void matrix_identity(int mat[][MAX_DIM], int n);

/* Rotate an n×n matrix 90 degrees clockwise in-place.
 * Hint: transpose, then reverse each row. */
void matrix_rotate_90(int mat[][MAX_DIM], int n);
```

Demonstrate all operations with a 3×3 matrix and a 3×4 matrix. For `matrix_multiply`, verify against a hand-computed example.

---

## Problem 4: Command-Line Calculator (20 pts)

Create `calc.c` — a fully functional integer calculator that reads expressions from command-line arguments.

```bash
./calc 3 + 4           # = 7
./calc 10 - 3          # = 7
./calc 6 '*' 7         # = 42  (quote * to avoid shell expansion)
./calc 17 / 5          # = 3 (integer division)
./calc 17 % 5          # = 2
./calc 2 ^ 10          # = 1024 (power)
./calc '(' 3 + 4 ')' '*' 2   # = 14 (parenthesized expression)
```

### Architecture

Break it into these components:

```c
/* Tokenizer: convert argv into a flat array of tokens */
typedef enum { TOK_NUMBER, TOK_PLUS, TOK_MINUS, TOK_STAR,
               TOK_SLASH, TOK_PERCENT, TOK_CARET,
               TOK_LPAREN, TOK_RPAREN, TOK_END } TokenType;

typedef struct {
    TokenType type;
    long value;      /* Only valid for TOK_NUMBER */
} Token;

int tokenize(int argc, char *argv[], Token tokens[], int max_tokens);

/* Recursive descent parser (evaluates as it parses) */
/* Grammar:
 *   expr   → term (('+' | '-') term)*
 *   term   → factor (('*' | '/' | '%') factor)*
 *   factor → base ('^' factor)?          ← right-associative power
 *   base   → NUMBER | '(' expr ')'
 */

/* Parser state */
typedef struct {
    const Token *tokens;
    int pos;
    int error;
} Parser;

long parse_expr(Parser *p);
long parse_term(Parser *p);
long parse_factor(Parser *p);
long parse_base(Parser *p);
```

### Error Handling

```bash
./calc 5 / 0           # Error: division by zero
./calc 3 + + 4         # Error: unexpected token
./calc '(' 3 + 4       # Error: missing closing parenthesis
./calc                 # Error: no expression provided
```

### Requirements

- All operations on `long` integers
- Division and modulo check for zero divisor
- Power: handle negative exponents (return error or 0 as you choose)
- Correct operator precedence: `2 + 3 * 4` = 14, not 20
- Parentheses work: `(2 + 3) * 4` = 20
- Power is right-associative: `2 ^ 3 ^ 2` = `2 ^ (3^2)` = `2^9` = 512

---

---

## Problem 5: Safe String Building (25 pts)

Lecture 3 established that `strcpy`, `strcat` and `sprintf` cannot be used safely, that `strncpy`
does not null-terminate, and that `snprintf`'s return value is the length it *wanted* to write.

Write `strbuild.c` implementing:

```c
/* Appends `src` to `dst`, which has total capacity `cap` (including the terminator).
   Returns 0 on success, -1 if the result would not fit.
   On failure `dst` must still be a valid, null-terminated string. */
int sb_append(char *dst, size_t cap, const char *src);

/* Joins `n` strings with `sep` into `dst`. Same contract as above.
   Must be O(total output length) -- no repeated rescanning. */
int sb_join(char *dst, size_t cap, const char **parts, size_t n, const char *sep);

/* Formats into a freshly allocated string of exactly the right size.
   Returns NULL on allocation failure. CALLER MUST FREE. */
char *sb_sprintf(const char *fmt, ...);
```

### Requirements

1. **No `strcpy`, `strcat`, `sprintf`, or `gets`.** Their use is an automatic zero on this problem.
2. `sb_append` and `sb_join` must **never** write past `dst + cap - 1`.
3. Both must leave `dst` null-terminated on **every** path, including failure and `cap == 0`.
4. `sb_join` must be O(total length). A `strcat` in the loop rescans the prefix each time and is
   Θ(n²) — this will be checked by inspection.
5. `sb_sprintf` must use the two-pass `snprintf(NULL, 0, ...)` idiom to size the allocation exactly.
   Do not guess a buffer size.
6. Write `test_strbuild.c` covering at minimum: exact fit, one byte short, `cap == 0`, `cap == 1`,
   empty inputs, and `n == 0` for the join.

### Marking

| Component | Points |
|---|---|
| `sb_append` correct, including all boundary cases | 7 |
| `sb_join` correct **and** O(total length) | 8 |
| `sb_sprintf` sized exactly via the two-pass idiom | 6 |
| Test suite covers the six required cases | 4 |

*Hint: the truncation test is `n >= (int)cap`, and the cast matters — see Lecture 3 §3.*

---
## Makefile

```makefile
CC = gcc
CFLAGS = -Wall -Wextra -Werror -g -std=c11

PROGRAMS = array_algorithms text_pipeline matrix calc test_strbuild

all: $(PROGRAMS)

# text_pipeline reuses the strlib you built in Lab 4
text_pipeline: text_pipeline.c ../lab4/strlib.o
	$(CC) $(CFLAGS) -o $@ $^

../lab4/strlib.o: ../lab4/strlib.c ../lab4/strlib.h
	$(CC) $(CFLAGS) -c $< -o $@

test_strbuild: test_strbuild.o strbuild.o
	$(CC) $(CFLAGS) -o $@ $^

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

%: %.c
	$(CC) $(CFLAGS) -o $@ $<

clean:
	rm -f $(PROGRAMS) *.o

.PHONY: all clean
```

---

## Submission

```bash
cd ~/prog101/week2/ps2
git add .
git commit -m "PS2 complete: functions, arrays, strings, matrix, calculator"
```

---

## Grading

| Problem | Points | Key Criteria |
|---------|--------|-------------|
| P1: Call stack experiments | 15 | Accurate measurements, correct explanations |
| P2: Array algorithms | 20 | All functions correct, edge cases handled |
| P3: Text pipeline | 20 | All flags work, correct order, safe I/O |
| P4: Matrix operations | 20 | Correct math, including rotate |
| P5: Calculator | 25 | Correct precedence, parentheses, error handling |
| **Total** | **100** | |

---

---

## Answer Key (Instructor Copy)

### Problem 1 — Array Algorithms (20 pts)

*Grade each function on correctness plus these edge cases, which is where submissions actually fail: length 0, length 1, all-equal elements, and already-sorted/reverse-sorted input.*
*Recurring C-specific defects to probe: (i) passing an array to a function decays it to a pointer, so `sizeof(arr)` inside the callee gives the **pointer** size (8), not the array size — every function must take an explicit length parameter, and a student computing `sizeof(arr)/sizeof(arr[0])` inside a function has an 8/4 = 2 bug; (ii) writing to `arr[n]` on a loop bound of `i <= n`; (iii) returning a pointer to a local array (dangling — see PROG 101 Week 3).*

---

### Problem 2 — String Processing Pipeline (20 pts)

*The graded C-specific concerns: every buffer write must be bounded (`fgets`, `snprintf`, `strncpy` — never `gets`, `strcpy` into a fixed buffer, or unbounded `scanf("%s")`); every string must remain NUL-terminated; `strncpy` specifically does **not** NUL-terminate when the source fills the buffer, which is the single most common silent bug in this problem.*
*Flags must be applied in the documented order and must compose — test at least one two-flag combination, since a common structure applies only the last flag parsed.*

---

### Problem 3 — Matrix Operations (15 pts)

*Rotation is the discriminating part. In-place 90° clockwise rotation of an n×n matrix = **transpose, then reverse each row**; counter-clockwise = transpose, then reverse each column. A student who rotates into a second matrix is correct but has taken the easier route — full marks unless the spec demanded in-place.*
*Check indexing on non-square input if the spec allows it: multiplication of an m×n by an n×p yields m×p, and the inner loop must run over the **shared** dimension n. Off-by-one and transposed-index bugs are the norm here; test with a non-symmetric matrix such as `{{1,2},{3,4},{5,6}}`, because square symmetric test data hides index swaps.*

---

### Problem 4 — Command-Line Calculator (20 pts)

*This is a full recursive-descent or shunting-yard exercise. Grade in three layers:*
1. *Tokenizer (5) — multi-digit and decimal literals, whitespace skipping, unknown-character rejection.*
2. *Parser/evaluator (12) — correct **precedence** (`*` `/` bind tighter than `+` `-`) and correct **associativity** (all four are left-associative, so `8 - 3 - 2` must be `3`, not `7`; `16 / 4 / 2` must be `2`, not `8`). Parentheses must override both. **These two expressions are the highest-value tests in the whole problem set** — they distinguish a real parser from one that just scans left to right or mishandles the operator stack.*
3. *Error handling (8) — division by zero, unbalanced parentheses, trailing garbage, empty input. Each must produce a diagnostic and a non-zero exit status, not a crash or a silent wrong answer.*

*Cross-reference: CS 101 PS 7 B5 solves the same problem with two explicit stacks under the simplification that input is **fully parenthesised**. This problem removes that crutch, which is exactly why precedence must now be handled. Students taking both courses should be encouraged to compare the two designs.*

---

*PROG 101 · Week 2 · Problem Set 2 · © CSE Department*

### Problem 5 — Safe String Building (25 pts)

```c
int sb_append(char *dst, size_t cap, const char *src)
{
    if (cap == 0) return -1;
    size_t used = strlen(dst);
    int n = snprintf(dst + used, cap - used, "%s", src);
    if (n < 0 || (size_t)n >= cap - used) { dst[cap - 1] = '\0'; return -1; }
    return 0;
}

int sb_join(char *dst, size_t cap, const char **parts, size_t n, const char *sep)
{
    if (cap == 0) return -1;
    dst[0] = '\0';
    size_t off = 0;
    for (size_t i = 0; i < n; i++) {
        int w = snprintf(dst + off, cap - off, "%s%s", i ? sep : "", parts[i]);
        if (w < 0) return -1;
        if ((size_t)w >= cap - off) { dst[cap - 1] = '\0'; return -1; }
        off += (size_t)w;
    }
    return 0;
}

char *sb_sprintf(const char *fmt, ...)
{
    va_list ap;
    va_start(ap, fmt);
    va_list ap2;
    va_copy(ap2, ap);                 /* a va_list cannot be traversed twice */
    int need = vsnprintf(NULL, 0, fmt, ap);
    va_end(ap);
    if (need < 0) { va_end(ap2); return NULL; }
    char *s = malloc((size_t)need + 1);
    if (s) vsnprintf(s, (size_t)need + 1, fmt, ap2);
    va_end(ap2);
    return s;
}
```

**Marking notes.**

- **`va_copy` is the discriminating detail in `sb_sprintf`.** A `va_list` may not be reused after
  being passed to `vsnprintf`; the first call consumes it. Students who call `vsnprintf` twice on the
  same `ap` have undefined behaviour that happens to work on x86-64 and fails on other ABIs. Award
  the full 6 only with `va_copy`; award 4 for an otherwise-correct two-pass without it, and say why.
- **`sb_join` must advance an offset**, not call `strlen(dst)` each iteration. The `strlen`-per-
  iteration version is correct but Θ(n²); cap it at 5 of 8 and note the Schlemiel-the-Painter shape.
- **The `cap == 0` guard comes first** in both functions. Without it, `dst[0] = '\0'` and
  `cap - used` both misbehave — the latter underflows to a huge `size_t`.
- **`dst[cap - 1] = '\0'` on the failure path** is what keeps requirement 3 true. A student who
  returns −1 without terminating leaves the caller an unterminated buffer, which is worse than the
  truncation they were guarding against.
- **Any use of `strcpy`/`strcat`/`sprintf` is 0 for this problem**, as stated. Say so in the feedback
  rather than deducting silently.
