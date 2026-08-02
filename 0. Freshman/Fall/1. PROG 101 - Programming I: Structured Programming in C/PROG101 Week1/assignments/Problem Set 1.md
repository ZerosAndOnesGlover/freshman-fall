# PROG 101 — Programming I: Structured Programming in C
## Week 1 · Problem Set 1

**Released:** End of Week 1 Thursday Lecture
**Due:** Before Week 2 Lecture 1 (Tuesday)
**Submission:** Push to Git, submit commit hash on course portal
**Directory:** `~/prog101/week1/ps1/`

---

## Problem 1: Integer Limits and Two's Complement (15 pts)

### 1A: Compute Limits Manually (5 pts)

Create `limits.c`. Without using `<limits.h>`, compute and print the minimum and maximum values for each of these types:

- `signed char`
- `unsigned char`
- `short`
- `unsigned short`
- `int`
- `unsigned int`

Use *only* bitwise operations and the `sizeof` operator — no hardcoded constants, no `<limits.h>`.

**Hint:** The maximum value of an unsigned n-bit type is `2^n - 1`. For a signed n-bit type, the max is `2^(n-1) - 1`. Think about how to compute `2^n` from `sizeof`.

Then verify your results with `<limits.h>`:
```c
#include <limits.h>
printf("Verification: SCHAR_MAX = %d\n", SCHAR_MAX);
// ... etc.
```

All your computed values must match `<limits.h>`.

### 1B: Two's Complement Arithmetic (5 pts)

Create `twos_complement.c`. Implement and demonstrate:

```c
/* Add two 8-bit signed values using ONLY unsigned arithmetic and bit ops.
 * Then interpret the result as signed.
 * Returns: the signed result of a + b (8-bit)
 */
signed char signed_add_8bit(signed char a, signed char b);

/* Negate an 8-bit signed value using two's complement.
 * Two's complement negation: flip all bits, add 1.
 * Returns: -a
 */
signed char signed_negate_8bit(signed char a);

/* Detect if signed 8-bit overflow occurred in the addition a + b.
 * Returns 1 if overflow would occur, 0 otherwise.
 * Overflow rule: adding two positives gives negative, or two negatives give positive.
 */
int would_overflow_8bit(signed char a, signed char b);
```

Demonstrate these with:
- Normal addition: `100 + 20 = 120`
- Overflow case: `100 + 30` (would overflow 8-bit signed)
- Negation: `-42` = `signed_negate_8bit(42)`

### 1C: Endianness Detective (5 pts)

Create `endianness.c`:

```c
/* Determine and print whether the system is big-endian or little-endian.
 * Do this WITHOUT using any predefined macros or platform checks.
 * Instead: store the value 1 as an int, then read its first byte.
 */
void print_endianness(void);

/* Print the bytes of an int value in memory order (address low to high).
 * Example for 0x12345678 on a little-endian system:
 *   int 0x12345678 in memory: [78] [56] [34] [12]
 */
void print_int_bytes(int value);

/* Manually swap bytes of a 32-bit integer to convert endianness.
 * Implement WITHOUT using bitwise operators — use pointer casting to
 * access individual bytes and swap them.
 */
uint32_t manual_byteswap(uint32_t x);
```

---

## Problem 2: Type Conversion Minefield (15 pts)

### 2A: Predict the Output (5 pts)

Create `predictions.c`. For each of the following code snippets, **first predict** what it will print (write your prediction in a comment), **then run it** and verify:

```c
/* Snippet 1 */
int a = -1;
unsigned int b = 1;
if (a < b)
    printf("a < b\n");
else
    printf("a >= b\n");   /* Predict: which branch? */

/* Snippet 2 */
char c = 200;              /* char may be signed on your system */
printf("%d\n", c);         /* Predict the output */

/* Snippet 3 */
int i = 2147483647;        /* INT_MAX */
printf("%d\n", i + 1);     /* Predict — careful! */

/* Snippet 4 */
unsigned int u = 0;
u = u - 1;
printf("%u\n", u);         /* Predict */

/* Snippet 5 */
double d = 1.0 / 3.0;
printf("%.20f\n", d);      /* Predict: exact or approximate? */

/* Snippet 6 */
int x = (int)3.9;
int y = (int)-3.9;
printf("%d %d\n", x, y);   /* Predict: truncation direction? */

/* Snippet 7 */
int p = 010;               /* Octal literal! */
int q = 0x10;              /* Hex literal */
printf("%d %d\n", p, q);   /* Predict */
```

For each snippet, document:
- Your prediction before running
- The actual output
- A one-sentence explanation of why

### 2B: Safe Type Conversion Functions (10 pts)

Create `safe_convert.c`. Implement functions that perform conversions safely — detecting overflow before it happens:

```c
#include <stdbool.h>
#include <stdint.h>

/* Safely convert int to signed char.
 * Returns true and sets *result if value fits in signed char.
 * Returns false if value is out of range for signed char.
 */
bool int_to_schar(int value, signed char *result);

/* Safely convert unsigned int to int.
 * Returns true and sets *result if value fits.
 * Returns false if value > INT_MAX.
 */
bool uint_to_int(unsigned int value, int *result);

/* Safely add two ints, detecting overflow.
 * Returns true and sets *result if no overflow.
 * Returns false if the addition would overflow.
 */
bool safe_add_int(int a, int b, int *result);

/* Safely multiply two ints, detecting overflow.
 * Returns true and sets *result if no overflow.
 * Returns false if multiplication would overflow.
 */
bool safe_mul_int(int a, int b, int *result);
```

Test each function with:
- A value that fits
- A value at the boundary (just fits)
- A value just beyond the boundary (doesn't fit)
- Negative values where applicable

---

## Problem 3: Bitwise Calculator (20 pts)

Create `bitcalc.c` — an interactive calculator that works at the bit level.

### Features Required

```
=== Bitwise Calculator ===
Enter expression (or 'q' to quit): 
```

The calculator supports:
- `AND a b` — prints `a & b` in decimal and binary
- `OR a b`  — prints `a | b`
- `XOR a b` — prints `a ^ b`
- `NOT a`   — prints `~a`
- `SHL a n` — prints `a << n` (shift left)
- `SHR a n` — prints `a >> n` (shift right, use unsigned)
- `CNT a`   — count of set bits in a
- `POW2 a`  — print 1 if a is a power of 2, 0 otherwise
- `HEX a`   — print a in hex
- `BIN a`   — print a in binary (32 bits)

### Sample Session

```
=== Bitwise Calculator ===
> BIN 42
42 in binary: 00000000 00000000 00000000 00101010

> AND 60 15
60 & 15:
  60 = 00000000 00000000 00000000 00111100
  15 = 00000000 00000000 00000000 00001111
  &  = 00000000 00000000 00000000 00001100  (12)

> SHL 1 8
1 << 8:
  1   = 00000000 00000000 00000000 00000001
  <<8 = 00000000 00000000 00000001 00000000  (256)

> CNT 255
Count of set bits in 255: 8

> POW2 256
256 is a power of 2: YES

> POW2 100
100 is a power of 2: NO

> q
Goodbye.
```

### Requirements

- Use `scanf` to read the command and operands in a loop
- Use your `bitlib` functions for operations
- Print binary values with spaces every 8 bits for readability
- Handle invalid commands with a helpful message
- The program loops until `q` is entered
- Compile clean: `-Wall -Wextra -Werror`

---

## Problem 4: Number Theory with Loops (20 pts)

Create `numtheory.c`. Implement these functions:

```c
/* Return 1 if n is prime, 0 otherwise.
 * Handle n <= 1 as not prime.
 * Efficiency: check only up to sqrt(n) — no <math.h> needed: stop when i*i > n
 */
int is_prime(long n);

/* Return the nth prime number (1-indexed: nth_prime(1) = 2, nth_prime(2) = 3, etc.)
 * Precondition: n >= 1
 */
long nth_prime(int n);

/* Compute gcd(a, b) using the Euclidean algorithm.
 * gcd(0, x) = x, gcd(x, 0) = x, gcd(0, 0) = 0
 */
long gcd(long a, long b);

/* Compute lcm(a, b) using: lcm = (a / gcd(a,b)) * b
 * Be careful about overflow — divide BEFORE multiplying.
 */
long lcm(long a, long b);

/* Print all prime numbers up to and including limit, one per line.
 * Uses the Sieve of Eratosthenes algorithm.
 * Allocate the boolean sieve array on the stack (if limit <= 10000) or heap.
 */
void sieve_of_eratosthenes(int limit);

/* Return the prime factorization of n.
 * Store factors in the provided array (in ascending order).
 * Store the count of factors in *count.
 * Precondition: n > 1, factors[] has room for at least 64 elements.
 * Example: factorize(360, factors, &count)
 *          → factors = {2, 2, 2, 3, 3, 5}, count = 6
 */
void factorize(long n, long factors[], int *count);
```

Write a `main()` that demonstrates each function:
- `is_prime`: test 10 values (some prime, some not)
- `nth_prime`: print the first 20 primes
- `gcd` / `lcm`: several pairs
- `sieve_of_eratosthenes(100)`: print all primes up to 100
- `factorize`: show factorization of 5 numbers including 360, 1024, 97

---

## Problem 5: ASCII Art Generator (15 pts)

Create `ascii_art.c`. Use nested loops to generate:

### 5A: Patterns

```c
/* Print a right triangle of '*' with height n.
 * Example: n=5
 * *
 * **
 * ***
 * ****
 * *****
 */
void triangle(int n);

/* Print a diamond of '*' with given half-height.
 * Example: half=3
 *   *
 *  ***
 * *****
 * *****
 *  ***
 *   *
 */
void diamond(int half);

/* Print an n×n checkerboard of '#' and '.' characters.
 * Example: n=4
 * #.#.
 * .#.#
 * #.#.
 * .#.#
 */
void checkerboard(int n);
```

### 5B: Number Triangle (Pascal's Triangle)

```c
/* Print the first n rows of Pascal's Triangle.
 * Example: n=5
 *     1
 *    1 1
 *   1 2 1
 *  1 3 3 1
 * 1 4 6 4 1
 *
 * Compute values using the identity: C(row, col) = C(row, col-1) * (row-col+1) / col
 * This avoids overflow better than computing factorials.
 */
void pascals_triangle(int n);
```

### 5C: The Multiplication Table Beautified

```c
/* Print an n×n multiplication table with proper alignment.
 * Headers on both axes. Example: n=5
 *
 *   ×  |   1   2   3   4   5
 * -----+--------------------
 *   1  |   1   2   3   4   5
 *   2  |   2   4   6   8  10
 *   3  |   3   6   9  12  15
 *   4  |   4   8  12  16  20
 *   5  |   5  10  15  20  25
 */
void mult_table(int n);
```

---

## Problem 6: The sizeof Mystery (15 pts)

Create `sizeof_mystery.c`. This problem explores how the compiler lays out data in memory.

### 6A: Struct Padding

Predict, then verify with `sizeof`, the size of each struct:

```c
struct A {
    char  c;      /* 1 byte */
    int   i;      /* 4 bytes */
    char  d;      /* 1 byte */
};
/* Predict sizeof(struct A): ___ bytes. Actual: ___ bytes. */

struct B {
    int   i;      /* 4 bytes */
    char  c;      /* 1 byte */
    char  d;      /* 1 byte */
};
/* Predict sizeof(struct B): ___ bytes. Actual: ___ bytes. */

struct C {
    double d;     /* 8 bytes */
    char   c;     /* 1 byte */
    int    i;     /* 4 bytes */
};
/* Predict sizeof(struct C): ___ bytes. Actual: ___ bytes. */

struct D {
    char   c;
    char   d;
    short  s;
    int    i;
    double db;
};
/* Predict sizeof(struct D): ___ bytes. Actual: ___ bytes. */
```

For each struct:
1. Draw a diagram of how you think the bytes are laid out
2. Use `offsetof` (from `<stddef.h>`) to print the actual offset of each field
3. Explain why the compiler inserted padding (alignment rules)

### 6B: sizeof Gotchas

Explain and demonstrate each of these `sizeof` surprises:

```c
/* Gotcha 1: sizeof(array) vs sizeof(pointer) */
int arr[10];
int *ptr = arr;
printf("sizeof(arr) = %zu\n", sizeof(arr));    /* = ? */
printf("sizeof(ptr) = %zu\n", sizeof(ptr));    /* = ? Why different? */

/* Gotcha 2: sizeof in a macro */
#define ARRAY_LENGTH(arr) (sizeof(arr) / sizeof((arr)[0]))
int numbers[7];
printf("Length = %zu\n", ARRAY_LENGTH(numbers));    /* = 7 */

/* Gotcha 3: sizeof a function parameter */
void test(int arr[]) {
    printf("sizeof(arr) = %zu\n", sizeof(arr));    /* NOT what you expect! */
}

/* Gotcha 4: sizeof evaluates its argument at compile time */
int n = 0;
printf("sizeof(n++) = %zu\n", sizeof(n++));   /* Does n get incremented? */
printf("n = %d\n", n);                         /* What is n? */
```

For each gotcha:
- Show the code
- Show the output
- Explain the underlying reason

---

## Makefile

```makefile
CC = gcc
CFLAGS = -Wall -Wextra -Werror -g -std=c11

PROGRAMS = limits twos_complement endianness predictions safe_convert \
           bitcalc numtheory ascii_art sizeof_mystery

all: $(PROGRAMS)

# Link bitcalc with bitlib
bitcalc: bitcalc.c ../lab1/bitlib.o
	$(CC) $(CFLAGS) -o $@ $^

../lab1/bitlib.o: ../lab1/bitlib.c ../lab1/bitlib.h
	$(CC) $(CFLAGS) -c $< -o $@

# All others: single file
%: %.c
	$(CC) $(CFLAGS) -o $@ $<

clean:
	rm -f $(PROGRAMS) *.o

.PHONY: all clean
```

---

## Submission

```bash
cd ~/prog101/week1/ps1
git add .
git commit -m "PS1 complete: types, bits, loops, sizeof"
```

Submit the commit hash. Include answers to prediction questions in comments within the code.

---

## Grading

| Problem | Points | Key Criteria |
|---------|--------|-------------|
| P1: Integer limits | 15 | Correct computation from `sizeof`, no hardcoding |
| P2: Type conversions | 15 | Correct predictions explained, safe functions correct |
| P3: Bitwise calculator | 20 | All operations work, readable binary output |
| P4: Number theory | 20 | All functions correct, sieve is O(n log log n) |
| P5: ASCII art | 15 | All patterns correct, aligned output |
| P6: sizeof mystery | 15 | Correct predictions, offsets verified, explained |
| **Total** | **100** | |

---

## Answer Key (Instructor Copy)

> **Do not distribute to students.** Totals follow the Grading table above (100 points).
> No errata found. All C below was compiled and run with `gcc 13.3.0 -Wall -Wextra -Werror -std=c11` on x86-64 Linux.
> **Platform caveat:** every numeric answer here assumes 8-bit `char`, 32-bit `int`, little-endian, signed `char`. Students on other targets may legitimately differ — grade the *method*, not the constant.

---

### Problem 1 — Integer Limits and Two's Complement (15 pts)

**1A (5 pts).** Compute from `sizeof` alone. The trap is that `1 << (sizeof(int)*8 - 1)` overflows `int`; shift in a wider **unsigned** type instead:

```c
/* max of an unsigned n-bit type: 2^n - 1  |  signed: 2^(n-1) - 1 */
#define UMAX(T) ((unsigned long long)((1ULL << (sizeof(T) * 8)) - 1ULL))
#define SMAX(T) ((long long)((1ULL << (sizeof(T) * 8 - 1)) - 1ULL))
#define SMIN(T) ((long long)(-(1LL  << (sizeof(T) * 8 - 1))))
```

Verified against `<limits.h>` on this platform — all match:

| Type | Computed min / max | `<limits.h>` |
|---|---|---|
| `signed char` | −128 / 127 | SCHAR_MIN / SCHAR_MAX ✓ |
| `unsigned char` | 0 / 255 | UCHAR_MAX ✓ |
| `int` | −2147483648 / 2147483647 | INT_MIN / INT_MAX ✓ |
| `unsigned int` | 0 / 4294967295 | UINT_MAX ✓ |

*Grading: 3 pts correct derivation from `sizeof`, 2 pts verification against `<limits.h>`. **Deduct 3** for any hardcoded 8/16/32 or literal 127/255 — the whole exercise is deriving them.*
*Common failure: `(1 << (sizeof(int)*8)) - 1` shifts by exactly the width, which is **undefined behaviour**, not zero. The `1ULL` widening is required.*

**1B (5 pts).** Verified outputs: `100+20 = 120` (no overflow), `100+30 = -126` (overflow flagged), `negate(42) = -42`.

```c
signed char signed_add_8bit(signed char a, signed char b) {
    unsigned char ua = (unsigned char)a, ub = (unsigned char)b;
    return (signed char)(unsigned char)(ua + ub);   /* unsigned wrap is well-defined */
}
signed char signed_negate_8bit(signed char a) {
    return (signed char)(unsigned char)(~(unsigned char)a + 1u);
}
int would_overflow_8bit(signed char a, signed char b) {
    int s = (int)a + (int)b;                        /* promote, then range-check */
    return s > 127 || s < -128;
}
```

*The reason to route through `unsigned char`: signed overflow is UB, unsigned wraparound is defined modulo 2ⁿ. Doing the arithmetic unsigned and reinterpreting afterwards is the portable idiom.*
*Worth surfacing: `signed_negate_8bit(-128)` returns **−128** — verified. −128 has no positive counterpart in 8-bit two's complement, so negation is a fixed point there. A student who finds and explains this deserves bonus credit; it is the same asymmetry behind `INT_MIN == -INT_MIN`.*

**1C (5 pts).** Verified on this (little-endian) machine:

```
endianness: little-endian (first byte = 1)
int 0x12345678 in memory: [78] [56] [34] [12]
manual_byteswap(0x12345678) -> 0x78563412
```

```c
uint32_t manual_byteswap(uint32_t x) {            /* no bitwise ops, per the spec */
    uint32_t out;
    unsigned char *s = (unsigned char *)&x, *d = (unsigned char *)&out;
    d[0] = s[3]; d[1] = s[2]; d[2] = s[1]; d[3] = s[0];
    return out;
}
```

*`unsigned char *` is the only pointer type permitted to alias any object — using `char *` is fine too, but `int *`/`short *` would violate strict aliasing and may be miscompiled at `-O2`. Mention this; deduct 1 only if they alias through a non-character type.*

---

### Problem 2 — Type Conversion Minefield (15 pts)

**2A (5 pts).** Verified outputs (identical at `-O0` and `-O2` on this build):

| # | Output | Why |
|---|---|---|
| 1 | **`a >= b`** | Usual arithmetic conversions promote `a` to `unsigned`; −1 becomes 4294967295, which is > 1. gcc flags this with `-Wsign-compare`. |
| 2 | **`-56`** | `char` is signed here; 200 doesn't fit, so it wraps to 200 − 256 = −56. |
| 3 | **`-2147483648`** *(observed)* | `INT_MAX + 1` is **signed overflow — undefined behaviour.** It happened to wrap on this build, but the compiler is entitled to do anything, and at higher optimisation gcc may assume it cannot occur. |
| 4 | **`4294967295`** | Unsigned arithmetic is defined modulo 2³²; `0 − 1` wraps to UINT_MAX. Contrast with #3 — this one is *guaranteed*. |
| 5 | **`0.33333333333333331483`** | Approximate. 1/3 is not representable in binary floating point; the stored double is slightly below 1/3. |
| 6 | **`3 -3`** | Cast to `int` truncates **toward zero**, not toward −∞ — so −3.9 → −3, not −4. |
| 7 | **`8 16`** | `010` is octal (= 8); `0x10` is hex (= 16). The leading-zero-means-octal rule is a classic source of bugs in permission/date code. |

*Grading: ~0.7 pt each — prediction, actual output, and the one-line reason. The critical distinction to reward is **#3 vs #4**: signed overflow is UB, unsigned wraparound is well-defined. A student who calls both "wraps around" has missed the entire point of the pair; deduct on #3.*

**2B (10 pts).** 2.5 pts each. Verified: `safe_add(INT_MAX,1)` → overflow; `safe_add(INT_MAX-1,1)` → ok, `2147483647`; `safe_mul(100000,100000)` → overflow; `safe_mul(INT_MIN,-1)` → overflow.

```c
bool safe_add_int(int a, int b, int *result) {
    if (b > 0 && a > INT_MAX - b) return false;   /* check BEFORE adding */
    if (b < 0 && a < INT_MIN - b) return false;
    *result = a + b; return true;
}
bool safe_mul_int(int a, int b, int *result) {
    if (a == 0 || b == 0) { *result = 0; return true; }
    if (a > 0 && b > 0 && a > INT_MAX / b) return false;
    if (a < 0 && b < 0 && a < INT_MAX / b) return false;
    if (a > 0 && b < 0 && b < INT_MIN / a) return false;
    if (a < 0 && b > 0 && a < INT_MIN / b) return false;
    *result = a * b; return true;
}
```

*The defining requirement: detect overflow **without causing it**. A submission that computes `a + b` and then inspects the result has already invoked UB — the check is worthless because the compiler may optimise it away entirely (gcc does exactly this at `-O2` for `if (a+b < a)`). Deduct 2 per function that tests after the fact. `__builtin_add_overflow` is acceptable if the student explains it.*
*`safe_mul_int(INT_MIN, -1)` must return false — it is the one multiplication whose true result is unrepresentable. Probe for it.*

> **Grader's note — a real trap when testing these.** Do not write
> `printf("%s (%d)\n", safe_add_int(a,b,&r) ? "ok" : "OVF", r);`
> C leaves argument evaluation order **unspecified**, so `r` may be read *before*
> the call executes. Verified: that line prints `ok (0)` while the correctly
> sequenced version prints `ok (2147483647)`. Call first, store the bool, then print.
> If a student's output looks wrong but their logic is right, check for this.

---

### Problem 3 — Bitwise Calculator (20 pts)

```c
void print_binary32(uint32_t v) {                 /* spaces every 8 bits */
    for (int i = 31; i >= 0; i--) {
        putchar((v >> i) & 1u ? '1' : '0');
        if (i % 8 == 0 && i) putchar(' ');
    }
}
int count_bits(uint32_t v) { int c = 0; while (v) { v &= v - 1; c++; } return c; }
int is_pow2(uint32_t v)    { return v && !(v & (v - 1)); }
```

Sample values from the prompt all check out: `BIN 42` → `…00101010`; `60 & 15` = **12**; `1 << 8` = **256**; `CNT 255` = **8**; `POW2 256` → YES, `POW2 100` → NO.

*Grading: 1.5 pts per operation (10 ops = 15), 3 pts binary formatting with 8-bit grouping, 2 pts loop + invalid-command handling.*
*Two correctness landmines to probe: (i) **`SHR` must use an unsigned operand** — right-shifting a negative signed value is implementation-defined (gcc does an arithmetic shift, propagating the sign bit), which is why the spec says "use unsigned"; (ii) `count_bits` via `v &= v-1` (Kernighan) runs in popcount-many iterations rather than 32 — accept the naive 32-iteration loop, but the trick deserves a style bonus.*
*`is_pow2` **must** guard `v != 0`, else 0 reports as a power of two — same defect flagged in CS 101 PS 1 B3.*

---

### Problem 4 — Number Theory (20 pts)

```c
int is_prime(long n) {
    if (n <= 1) return 0;
    if (n <= 3) return 1;
    if (n % 2 == 0) return 0;
    for (long i = 3; i * i <= n; i += 2) if (n % i == 0) return 0;   /* i*i, no sqrt */
    return 1;
}
long nth_prime(int n) {
    int found = 0; long c = 1;
    while (found < n) { c++; if (is_prime(c)) found++; }
    return c;
}
```

*`nth_prime(1) = 2`, `nth_prime(2) = 3` per the 1-indexed spec — check the off-by-one explicitly.*
*The `i * i <= n` bound is required by the prompt (no `<math.h>`). Note for the debrief: `i * i` can overflow `long` for n near `LONG_MAX`; `i <= n / i` is the overflow-safe form and is worth a bonus mark.*
*The rubric credits the sieve as O(n log log n) — that is the Sieve of Eratosthenes bound. A sieve that marks multiples starting at `i*i` (not `2*i`) is the correct optimisation; starting at `2*i` is still correct, just redundant.*

---

### Problems 5–6 — ASCII Art (15 pts) and `sizeof` Mystery (15 pts)

*P5: grade on exact alignment using width specifiers rather than hand-counted spaces; all patterns must scale with the size parameter, not be hardcoded for one value.*
*P6: expected findings on x86-64 — `sizeof(char)=1`, `short`=2, `int`=4, `long`=8, `float`=4, `double`=8, pointers=8. Struct sizes are governed by **alignment and padding**: a `struct { char a; int b; char c; }` occupies **12** bytes (1 + 3 pad + 4 + 1 + 3 tail-pad), not 6. Reordering the members largest-first shrinks it to 8. Require `offsetof` evidence from `<stddef.h>`, and require the student to explain that trailing padding exists so arrays of the struct stay aligned. Award full marks only where the padding is *explained*, not merely observed.*

---

*PROG 101 · Week 1 · Problem Set 1 · © CSE Department*
