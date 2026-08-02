# PROG 101 · Programming I: Structured Programming in C
## Week 1 · Lab 1: Memory Layout, Bit Manipulation, and Loop Tracing

**Graded: 20 points (completion + correctness)**
**Duration:** 2 hours
**Submission:** Push to Git, show TA before leaving

---

## Overview

This lab has three parts:
1. **Memory Explorer** — Use GDB to inspect how variables are laid out in memory
2. **Bit Manipulation Library** — Build a reusable set of bit operations
3. **Loop Tracing** — Trace loops by hand, then verify with GDB

---

## Part 1: Memory Explorer (6 pts)

### 1A: sizeof Table

Create `memory_explorer.c`. Fill in this program:

```c
/* memory_explorer.c
 * Explore sizes and memory layout of C types
 */
#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>

int global_int = 42;
double global_double = 3.14;
char global_char = 'X';

int main(void) {
    /* Local variables */
    char   c  = 'A';
    short  s  = 1000;
    int    i  = 100000;
    long   l  = 1000000000L;
    float  f  = 3.14f;
    double d  = 3.14159265358979;
    bool   b  = true;
    
    int    arr[5] = {10, 20, 30, 40, 50};
    int   *ptr = &i;

    /* === Print the size table === */
    printf("╔══════════════════╦══════════╦══════════════════════════════╗\n");
    printf("║ Type             ║ Size     ║ Value                        ║\n");
    printf("╠══════════════════╬══════════╬══════════════════════════════╣\n");
    printf("║ char             ║ %zu byte%s ║ '%c' (ASCII %d)%*s║\n",
           sizeof(c), sizeof(c)==1?"":"s", c, (int)c,
           (int)(21 - printf_width_char(c)), "");

    /* TODO: Print a row for EACH variable (s, i, l, f, d, b, arr, ptr)
     *       Format: type name | sizeof | value
     *       Use correct format specifiers for each type
     *       For arrays: show sizeof(arr) AND sizeof(arr)/sizeof(arr[0])
     *       For pointers: show %p and sizeof(ptr)
     */

    /* === Print addresses === */
    printf("\n=== Variable Addresses ===\n");
    printf("&c   = %p  (local)\n", (void *)&c);
    printf("&i   = %p  (local)\n", (void *)&i);
    printf("&arr = %p  (local, arr[0])\n", (void *)arr);
    /* TODO: print addresses of all local variables and both globals */
    printf("&global_int    = %p  (global)\n", (void *)&global_int);
    printf("&global_double = %p  (global)\n", (void *)&global_double);

    /* === Address arithmetic === */
    printf("\n=== Address Arithmetic ===\n");
    printf("arr[0] is at %p\n", (void *)&arr[0]);
    printf("arr[1] is at %p\n", (void *)&arr[1]);
    printf("arr[2] is at %p\n", (void *)&arr[2]);
    printf("Difference arr[1]-arr[0] = %td bytes\n",
           (char*)&arr[1] - (char*)&arr[0]);

    return 0;
}
```

**Your task:** Complete the TODO sections. Run it and answer in `LAB 1 Memory Bits Loops.md`:

1. On your system, what is `sizeof(int)`? `sizeof(long)`? `sizeof(pointer)`?
2. Are local variables (stack) at higher or lower addresses than globals?
3. What is the address difference between consecutive `int` array elements? Why?
4. Are the local variables stored contiguously in memory? Why or why not?

### 1B: Two's Complement Visualizer

Add this function to `memory_explorer.c`:

```c
/* Print the binary representation of any integer type */
void print_bits(const void *val, size_t size) {
    const unsigned char *bytes = (const unsigned char *)val;
    
    /* Print from most significant byte to least significant */
    for (int byte = (int)size - 1; byte >= 0; byte--) {
        for (int bit = 7; bit >= 0; bit--) {
            printf("%d", (bytes[byte] >> bit) & 1);
        }
        if (byte > 0) printf(" ");
    }
}
```

Use it to print the binary representation of:
```c
signed char values[] = {0, 1, -1, 127, -128, 42, -42};
```

For each value, show:
- The decimal value
- The binary representation (using `print_bits`)
- A one-line explanation of why that bit pattern represents that value

Example output format:
```
  0  →  00000000  (zero: all bits are 0)
  1  →  00000001  (one: LSB is 1)
 -1  →  11111111  (all 1s: -128+64+32+16+8+4+2+1 = -1)
```

---

## Part 2: Bit Manipulation Library (8 pts)

Create `bitlib.h` and `bitlib.c` — a library of bit manipulation functions.

### `bitlib.h`

```c
/* bitlib.h — Bit manipulation utilities
 * PROG 101, Week 1 Lab
 */
#ifndef BITLIB_H
#define BITLIB_H

#include <stdint.h>

/* Set bit 'n' in 'x' (0 = LSB). Return the modified value. */
uint32_t bit_set(uint32_t x, int n);

/* Clear bit 'n' in 'x'. Return the modified value. */
uint32_t bit_clear(uint32_t x, int n);

/* Toggle bit 'n' in 'x'. Return the modified value. */
uint32_t bit_toggle(uint32_t x, int n);

/* Test bit 'n' in 'x'. Return 1 if set, 0 if clear. */
int bit_test(uint32_t x, int n);

/* Return the number of set bits (1s) in x. (Popcount) */
int bit_count(uint32_t x);

/* Return 1 if x is a power of 2, 0 otherwise. (No loops allowed.) */
int bit_is_power_of_2(uint32_t x);

/* Reverse the bits of x (bit 0 becomes bit 31, etc.) */
uint32_t bit_reverse(uint32_t x);

/* Extract bits [high..low] from x (inclusive).
 * e.g. bit_extract(0b11010110, 5, 2) returns 0b0101 (bits 5,4,3,2)
 */
uint32_t bit_extract(uint32_t x, int high, int low);

/* Set bits [high..low] in x to the given value.
 * e.g. bit_set_field(0xFF00FF00, 11, 8, 0xA) sets bits 11-8 to 0xA
 */
uint32_t bit_set_field(uint32_t x, int high, int low, uint32_t value);

/* Return x with bytes swapped (little-endian ↔ big-endian for 32-bit) */
uint32_t bit_byteswap(uint32_t x);

#endif /* BITLIB_H */
```

### `bitlib.c`

Implement every function. Requirements:
- No loops in `bit_is_power_of_2` — it must be a single expression
- `bit_count` should work correctly for all 32-bit values
- All functions must handle edge cases (n=0, n=31, x=0, x=UINT32_MAX)

Document each function with a comment explaining the bit trick used.

### `test_bitlib.c` — Test Suite

Write a test file that validates every function:

```c
/* test_bitlib.c — Test suite for bitlib */
#include <stdio.h>
#include <stdint.h>
#include "bitlib.h"

static int tests_run = 0;
static int tests_passed = 0;

/* Test helper macro */
#define TEST(description, expected, actual) do { \
    tests_run++; \
    if ((expected) == (actual)) { \
        printf("  PASS: %s\n", description); \
        tests_passed++; \
    } else { \
        printf("  FAIL: %s\n", description); \
        printf("        Expected: 0x%08X (%u)\n", (expected), (expected)); \
        printf("        Actual:   0x%08X (%u)\n", (actual),   (actual)); \
    } \
} while(0)

int main(void) {
    printf("=== Testing bit_set ===\n");
    TEST("Set bit 0 of 0", 0x00000001, bit_set(0, 0));
    TEST("Set bit 31 of 0", 0x80000000, bit_set(0, 31));
    TEST("Set already-set bit", 0x00000001, bit_set(1, 0));
    /* TODO: add at least 3 more tests per function */

    printf("\n=== Testing bit_clear ===\n");
    TEST("Clear bit 0 of 0xFFFFFFFF", 0xFFFFFFFE, bit_clear(0xFFFFFFFF, 0));
    /* TODO: more tests */

    /* TODO: test ALL functions */

    printf("\n=== Testing bit_is_power_of_2 ===\n");
    TEST("1 is power of 2",  1, bit_is_power_of_2(1));
    TEST("2 is power of 2",  1, bit_is_power_of_2(2));
    TEST("4 is power of 2",  1, bit_is_power_of_2(4));
    TEST("3 is NOT",         0, bit_is_power_of_2(3));
    TEST("0 is NOT",         0, bit_is_power_of_2(0));

    printf("\n=== Results ===\n");
    printf("%d/%d tests passed\n", tests_passed, tests_run);
    return (tests_passed == tests_run) ? 0 : 1;
}
```

### Makefile for Part 2

```makefile
CC = gcc
CFLAGS = -Wall -Wextra -Werror -g -std=c11

test_bitlib: test_bitlib.o bitlib.o
	$(CC) $(CFLAGS) -o $@ $^

test_bitlib.o: test_bitlib.c bitlib.h
	$(CC) $(CFLAGS) -c $< -o $@

bitlib.o: bitlib.c bitlib.h
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f test_bitlib *.o

.PHONY: clean
```

---

## Part 3: Loop Tracing (6 pts)

### 3A: Manual Traces

For each loop below, trace execution in a table (like the example in Lecture 3).
Then verify your trace by running the code with `printf` statements added.

**Loop 1:**
```c
int x = 1;
while (x < 100) {
    x *= 3;
}
printf("x = %d\n", x);
```

Create the trace table with columns: `iteration | x (before) | condition | x *= 3 | x (after)`

**Loop 2:**
```c
int n = 12;
int result = 0;
while (n > 0) {
    result += n % 2;
    n /= 2;
}
printf("result = %d\n", result);
```

Trace table with: `iteration | n (before) | n % 2 | result | n /= 2 | n (after)`

After tracing: what does this loop compute? (Hint: look at what `n % 2` produces each iteration.)

**Loop 3:**
```c
int a = 48, b = 36;
while (b != 0) {
    int t = b;
    b = a % b;
    a = t;
}
printf("a = %d\n", a);
```

Trace table: `iteration | a | b (before) | t = b | b = a%b | a = t`

After tracing: what famous algorithm is this? What does it compute?

### 3B: Debug the Loop

This loop has a bug. Find it using **only GDB** (set a breakpoint, step through, inspect variables — no reading the code to find it):

Create `buggy_loop.c`:

```c
/* buggy_loop.c — Find and fix the bug using GDB */
#include <stdio.h>

/* Sum of odd numbers from 1 to n (inclusive) */
/* Should return: 1 + 3 + 5 + ... (all odd numbers <= n) */
int sum_odd(int n) {
    int sum = 0;
    for (int i = 1; i < n; i += 2) {
        sum += i;
    }
    return sum;
}

int main(void) {
    /* Expected: sum_odd(10) = 1+3+5+7+9 = 25 */
    printf("sum_odd(10) = %d (expected 25)\n", sum_odd(10));

    /* Expected: sum_odd(1) = 1 */
    printf("sum_odd(1)  = %d (expected 1)\n",  sum_odd(1));

    /* Expected: sum_odd(7) = 1+3+5+7 = 16 */
    printf("sum_odd(7)  = %d (expected 16)\n", sum_odd(7));

    return 0;
}
```

In `LAB 1 Memory Bits Loops.md`, document:
1. Your GDB session (commands used, output seen)
2. What the bug is and why it's a bug
3. The fix
4. The corrected version of the function

### 3C: Write Loops from Spec

Implement `loops.c` containing these three functions:

```c
/* Return the number of digits in a positive integer n.
 * num_digits(0) = 1, num_digits(5) = 1, num_digits(42) = 2,
 * num_digits(100) = 3, num_digits(999999) = 6
 * Hint: use a loop that divides by 10
 */
int num_digits(int n);

/* Return the sum of digits of a non-negative integer.
 * digit_sum(0) = 0, digit_sum(42) = 6, digit_sum(999) = 27
 */
int digit_sum(int n);

/* Return 1 if n is prime, 0 otherwise.
 * A prime has no divisors other than 1 and itself.
 * Handle edge cases: is_prime(0) = 0, is_prime(1) = 0, is_prime(2) = 1
 * EFFICIENCY: you do not need to check all divisors up to n.
 *             Think about what the maximum divisor to check is.
 */
int is_prime(int n);
```

Write a `main()` that tests each function with a variety of inputs.

---

## Deliverables

```
week1/lab1/
├── memory_explorer.c      # Part 1A + 1B
├── bitlib.h               # Part 2 header
├── bitlib.c               # Part 2 implementation
├── test_bitlib.c          # Part 2 test suite
├── buggy_loop.c           # Part 3B (with fix applied)
├── loops.c                # Part 3C
├── Makefile               # Builds everything
└── LAB 1 Memory Bits Loops.md          # Answers to all questions + loop traces + GDB session
```

```bash
cd ~/prog101/week1/lab1
git add .
git commit -m "Week 1 Lab 1: memory, bitlib, loops"
```

Show your TA: `make && ./test_bitlib` — all tests must pass.

---

## Grading

| Part | Points | Criteria |
|------|--------|---------|
| 1A: sizeof table + questions | 3 | Complete, correct answers |
| 1B: two's complement visualizer | 3 | Correct binary output, correct explanations |
| 2: bitlib implementation | 5 | All functions correct, documented |
| 2: test suite | 3 | Tests all functions, at least 3 cases each |
| 3A: loop traces | 2 | Correct tables, algorithm identification |
| 3B: GDB debugging | 2 | GDB session documented, bug correctly identified |
| 3C: loop implementations | 2 | All three functions correct |
| **Total** | **20** | |
| Bonus: `bit_count` in O(1) | 2 | No loops, no branches — look up "popcount" trick |
