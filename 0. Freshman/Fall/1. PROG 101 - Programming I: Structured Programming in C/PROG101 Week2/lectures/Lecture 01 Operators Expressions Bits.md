# PROG 101 · Programming I: Structured Programming in C
## Week 2 · Lecture 1: Operators, Expressions, and Bit Manipulation

**Date:** Tuesday 1 September 2026 · 10:00–10:50 · Week 2

---

## Lecture Goals

By the end of this lecture you will:
- Know all C operators and their precedence
- Understand short-circuit evaluation and why it matters
- Perform bit-level operations with confidence
- Understand what undefined behavior from operators looks like
- Use the comma operator and conditional (ternary) operator

---

## 1. The Complete C Operator Hierarchy

Operators in C have a fixed precedence (which binds tighter) and associativity (left-to-right or right-to-left when precedences are equal).

| Precedence | Operators | Associativity |
|-----------|-----------|---------------|
| 15 (highest) | `()` `[]` `->` `.` | Left to right |
| 14 | Unary: `!` `~` `++` `--` `+` `-` `*` `&` `sizeof` `(cast)` | **Right to left** |
| 13 | `*` `/` `%` | Left to right |
| 12 | `+` `-` | Left to right |
| 11 | `<<` `>>` | Left to right |
| 10 | `<` `<=` `>` `>=` | Left to right |
| 9 | `==` `!=` | Left to right |
| 8 | `&` (bitwise AND) | Left to right |
| 7 | `^` (bitwise XOR) | Left to right |
| 6 | `\|` (bitwise OR) | Left to right |
| 5 | `&&` (logical AND) | Left to right |
| 4 | `\|\|` (logical OR) | Left to right |
| 3 | `?:` (ternary) | **Right to left** |
| 2 | `=` `+=` `-=` `*=` `/=` `%=` `&=` `^=` `\|=` `<<=` `>>=` | **Right to left** |
| 1 (lowest) | `,` (comma) | Left to right |

**Practical rule:** When in doubt, use parentheses. They cost nothing and prevent bugs.

---

## 2. Arithmetic Operators

```c
int a = 17, b = 5;

int sum  = a + b;    // 22
int diff = a - b;    // 12
int prod = a * b;    // 85
int quot = a / b;    // 3  ← INTEGER DIVISION: truncates toward zero
int rem  = a % b;    // 2  ← remainder (sign matches dividend in C)

// Division truncates toward zero (not toward negative infinity)
int q1 = 7 / 2;     // 3  (not 3.5, not 4)
int q2 = -7 / 2;    // -3 (not -4)
int r1 = 7 % 2;     // 1
int r2 = -7 % 2;    // -1 (sign matches dividend -7)
```

### Integer Division: The Classic Bug

```c
double average = 5 / 2;      // WRONG: 5/2 = 2 (integer division), stored as 2.0
double average = 5.0 / 2;    // CORRECT: one operand is double → double division = 2.5
double average = (double)5 / 2;   // CORRECT: explicit cast
```

### The Modulo Operator

Useful for:
```c
x % 2 == 0          // Is x even?
x % 10              // Last digit of x (if x ≥ 0)
x % n               // x "wrapped" into range [0, n-1] (if x ≥ 0)
(x + 1) % n         // Circular increment (next index in circular buffer)
```

---

## 3. Relational and Logical Operators

### Relational Operators (produce 0 or 1)

```c
int x = 5, y = 10;
x < y      // 1 (true)
x > y      // 0 (false)
x <= 5     // 1
x >= 6     // 0
x == 5     // 1  ← double equal sign!
x != 5     // 0
```

In C, **there is no boolean type in C89**. In C99/C11, `<stdbool.h>` provides `bool`, `true`, `false`:
```c
#include <stdbool.h>
bool is_even = (x % 2 == 0);    // true or false
```

Without it, any non-zero integer is "true", zero is "false".

### The Assignment-in-Condition Bug

```c
if (x = 5)    // ASSIGNS 5 to x, then tests if 5 is non-zero → always true
if (x == 5)   // COMPARES x to 5 → the intended meaning

// Defensive style: put the constant on the left
if (5 == x)   // If you accidentally write = instead of ==, compiler catches it:
              // "5 = x" is an error (can't assign to a constant)
```

### Logical Operators: `&&` and `||`

These combine boolean expressions:

```c
int x = 5;
(x > 0) && (x < 10)    // true: x is between 0 and 10
(x < 0) || (x > 100)   // false: x is NOT out of range

!true     // false
!0        // 1 (true)
!5        // 0 (false) — any non-zero is "true", so !non-zero = 0
```

### Short-Circuit Evaluation — Critical

`&&` and `||` use **short-circuit evaluation**: the right operand is **not evaluated** if the result is determined by the left operand alone.

```c
// && short-circuit: if left is false, right is NOT evaluated
int *ptr = NULL;
if (ptr != NULL && *ptr > 0) {    // SAFE: *ptr only evaluated if ptr != NULL
    printf("Positive value\n");
}

// || short-circuit: if left is true, right is NOT evaluated
if (x < 0 || expensive_check(x)) {   // expensive_check only called if x >= 0
    handle_problem();
}
```

This is not just an optimization — it is the standard way to guard against null pointer dereference and other errors. Rely on it.

**Contrast:** Bitwise `&` and `|` always evaluate both sides — no short-circuit:
```c
if (ptr != NULL & *ptr > 0)    // DANGEROUS: *ptr evaluated even if ptr is NULL
```

---

## 4. Increment and Decrement Operators

```c
int x = 5;
x++;    // Post-increment: use x (5), THEN increment → x = 6
++x;    // Pre-increment: increment FIRST, THEN use → x = 7
x--;    // Post-decrement: use x (7), THEN decrement → x = 6
--x;    // Pre-decrement: decrement FIRST, THEN use → x = 5
```

The difference matters only when the value is used in an expression:

```c
int x = 5;
int a = x++;    // a = 5, then x becomes 6
int b = ++x;    // x becomes 7, then b = 7
int c = x--;    // c = 7, then x becomes 6
int d = --x;    // x becomes 5, then d = 5
```

**Rule:** When you just want to increment a variable, `x++` and `++x` are identical. Use `++x` when possible — it is cleaner and sometimes faster (especially for iterators in C++).

### The Undefined Behavior Trap

**Never modify a variable twice in one expression:**
```c
int x = 5;
int y = x++ + x++;    // UNDEFINED BEHAVIOR — order of evaluation is unspecified
int z = ++x + ++x;    // UNDEFINED BEHAVIOR
int a = i + ++i;      // UNDEFINED BEHAVIOR

// These are safe (only one modification):
int y = x++;          // OK
x = x + 1;            // OK
```

The compiler can evaluate the operands of `+` in any order. The result is genuinely unpredictable.

---

## 5. Assignment Operators

The compound assignment operators are shorthand:

```c
x += 5;      // x = x + 5
x -= 3;      // x = x - 3
x *= 2;      // x = x * 2
x /= 4;      // x = x / 4
x %= 7;      // x = x % 7
x <<= 2;     // x = x << 2 (shift left)
x >>= 1;     // x = x >> 1 (shift right)
x &= 0xFF;   // x = x & 0xFF (bitwise AND)
x |= 0x01;   // x = x | 0x01 (bitwise OR)
x ^= mask;   // x = x ^ mask (bitwise XOR)
```

These are not just convenient — they are expressive. `x &= ~(1 << 3)` clearly means "clear bit 3 of x."

---

## 6. Bitwise Operators — The Power Operators

Bitwise operators work on individual bits of integer values. They are essential for:
- Systems programming (registers, flags, masks)
- Cryptography
- Compression
- Network protocol parsing
- Performance-critical code (multiply/divide by powers of 2)

### The Six Bitwise Operators

```c
unsigned char a = 0b11001010;   // 202
unsigned char b = 0b10110101;   // 181

a & b   // AND:  0b10000000 = 128 (bit set only where BOTH are 1)
a | b   // OR:   0b11111111 = 255 (bit set where EITHER is 1)
a ^ b   // XOR:  0b01111111 = 127 (bit set where they DIFFER)
~a      // NOT:  0b00110101 = 53  (flip all bits)
a << 2  // LEFT SHIFT:  multiply by 4 = 808 (bits move left, zeros fill right)
a >> 1  // RIGHT SHIFT: divide by 2 = 101 (bits move right)
```

### Bit Manipulation Patterns

These patterns appear constantly in systems code. Memorize them.

```c
unsigned int x = 0b10110100;
int n = 3;    // bit position (0 = rightmost)

/* SET bit n (force it to 1) */
x |= (1u << n);
// 10110100 | 00001000 = 10111100

/* CLEAR bit n (force it to 0) */
x &= ~(1u << n);
// ~(1u << 3) = ~00001000 = 11110111
// 10111100 & 11110111 = 10110100

/* TOGGLE bit n (flip it) */
x ^= (1u << n);
// 10110100 ^ 00001000 = 10111100

/* TEST bit n (check if it is 1) */
int is_set = (x >> n) & 1;
// or equivalently:
int is_set = !!(x & (1u << n));

/* EXTRACT bits [m..n] (a field of bits) */
// Extract bits 5 down to 2 (4-bit field)
unsigned int field = (x >> 2) & 0xF;   // 0xF = 0b1111

/* SET a multi-bit field */
unsigned int value = 0b1010;
x = (x & ~(0xF << 2)) | ((value & 0xF) << 2);
// Clear the field, then OR in the new value
```

### Shift Operators

```c
unsigned int x = 1;

x << 1     // Multiply by 2:  1 → 2
x << 2     // Multiply by 4:  1 → 4
x << n     // Multiply by 2ⁿ

x >> 1     // Divide by 2:    8 → 4
x >> 2     // Divide by 4:    8 → 2
x >> n     // Divide by 2ⁿ (for unsigned; rounds toward zero)
```

**WARNINGS about shifts:**
1. Shifting by a negative amount: **undefined behavior**
2. Shifting by ≥ bit width: **undefined behavior** (`1 << 32` on a 32-bit int is UB)
3. Left-shifting a negative signed value: **undefined behavior** (C99/C11)
4. Right-shifting a negative signed value: **implementation-defined** (usually arithmetic shift = sign-extended)

```c
// SAFE: use unsigned types for bit manipulation
unsigned int flags = 0u;
flags |= (1u << 7);    // Safe: 1u is unsigned, result is unsigned
```

---

## 7. Practical Bit Manipulation: Working with Flags

A common pattern: packing multiple boolean values into a single integer (a "flags" variable).

```c
/* Define named bit positions */
#define FLAG_READABLE   (1u << 0)   /* bit 0 = 0x01 */
#define FLAG_WRITABLE   (1u << 1)   /* bit 1 = 0x02 */
#define FLAG_EXECUTABLE (1u << 2)   /* bit 2 = 0x04 */
#define FLAG_HIDDEN     (1u << 3)   /* bit 3 = 0x08 */

unsigned int permissions = 0;

/* Set flags */
permissions |= FLAG_READABLE;
permissions |= FLAG_WRITABLE;

/* Test a flag */
if (permissions & FLAG_READABLE) {
    printf("File is readable\n");
}

/* Clear a flag */
permissions &= ~FLAG_WRITABLE;

/* Test multiple flags */
if ((permissions & (FLAG_READABLE | FLAG_EXECUTABLE)) ==
    (FLAG_READABLE | FLAG_EXECUTABLE)) {
    printf("Both readable and executable\n");
}

/* Toggle a flag */
permissions ^= FLAG_HIDDEN;
```

This is exactly how Unix file permissions, Linux kernel flags, and network protocol headers work.

---

## 8. The Ternary (Conditional) Operator

```c
condition ? value_if_true : value_if_false
```

```c
int x = 10;
int abs_x = (x >= 0) ? x : -x;    // absolute value

int max = (a > b) ? a : b;        // maximum of a, b
int min = (a < b) ? a : b;        // minimum of a, b

// Can be used inline
printf("x is %s\n", (x % 2 == 0) ? "even" : "odd");
```

The ternary operator is an *expression* (has a value) — `if/else` is a *statement* (does not).

Use it for short, clear conditionals. If the condition or branches are complex, use `if/else` for readability.

---

## 9. The Comma Operator

The comma operator evaluates both expressions left-to-right and returns the value of the right:

```c
int x = (3, 5);    // x = 5 (3 is evaluated and discarded)
```

You will rarely write this directly. It appears most naturally in `for` loop headers:

```c
for (int i = 0, j = 10; i < j; i++, j--) {
    // i starts at 0, j starts at 10, both change each iteration
}
```

---

## 10. Operator Precedence: The Traps

The most common precedence mistakes:

```c
/* Trap 1: & binds less tightly than == */
if (x & FLAG == 0)          // Parsed as: x & (FLAG == 0) — WRONG
if ((x & FLAG) == 0)        // CORRECT: parenthesize bitwise ops

/* Trap 2: sizeof is an operator, not a function */
int *p = malloc(sizeof(int) * n);    // CORRECT
int *p = malloc(sizeof(int*) * n);   // BUG: sizeof(int*) = 8, sizeof(int) = 4

/* Trap 3: ++ has higher precedence than * */
*ptr++      // Dereference ptr, THEN increment ptr (common and correct)
(*ptr)++    // Increment the VALUE pointed to by ptr (different!)

/* Trap 4: << has lower precedence than + */
1 << 2 + 1    // Parsed as: 1 << (2+1) = 1 << 3 = 8, NOT (1<<2) + 1 = 5
```

**When in doubt:** add parentheses. There is no award for writing operator precedence from memory.

---

## Practice Exercises

Work these before the next lecture. Each set moves from *trace* (predict what happens) through *explain* (say why) to *build* (write it yourself) and finally *stretch* (a step past the lecture). Answers are at the end of the section — attempt each exercise before reading them.

**1. (Trace.)** Predict each. All are legal C, and several differ from what the same expression means in Python.

```c
3 & 1 == 1
6 & 2 == 2
1 << 2 + 3
7 % -2
-7 % 2
7 / -2
~5
-8 >> 1
```

**2. (Explain.)** Explain why this is undefined behaviour, and what the standard term for the underlying rule is.

```c
int i = 5;
int x = i++ + i++;
printf("%d %d\n", i++, i++);
```

**3. (Build.)** Implement four bit operations on an `unsigned int` flags word: set bit n, clear bit n, toggle bit n, and test bit n. Then write `count_set_bits`.

**4. (Stretch.)** Explain what the comma operator does, why `for (i = 0, j = n; i < j; i++, j--)` is idiomatic, and why `int a = 1, 2;` is a syntax error rather than a use of it.


### Answers

**1.** `1`, **`0`**, `32`, `1`, `-1`, `-3`, `-6`, `-4`.

**`3 & 1 == 1` is `1` and `6 & 2 == 2` is `0`** because in C, `==` binds **tighter** than `&`. They parse as `3 & (1==1)` = `3 & 1` = 1, and `6 & (2==2)` = `6 & 1` = 0. Ritchie later called this precedence an outright mistake, kept only for compatibility. **In Python the precedence is reversed**, so the same two expressions give `True` and `True`. Always write `(flags & MASK) != 0`; `-Wparentheses` warns.

**`1 << 2 + 3` is `32`**, not 7 — `+` binds tighter than `<<`, so it is `1 << 5`.

**`7 % -2` is `1` and `-7 % 2` is `-1`.** Since C99, `/` truncates **toward zero** and `%` takes the sign of the **dividend**. Python does the opposite on both counts: `7 % -2` is `-1` and `-7 % 2` is `1`, because Python floors. The identity `(a/b)*b + a%b == a` holds in both languages; they just resolve the rounding differently. If you need a always-positive modulus in C, write `((a % b) + b) % b`.

`~5` is `-6` because `~n == -n - 1` in two's complement. `-8 >> 1` is `-4`: right-shifting a negative signed value is implementation-defined, and GCC shifts arithmetically (sign-extending).

**2.** Both lines modify `i` more than once between **sequence points**, with no ordering imposed between the modifications. In C11 terms, the two updates are *unsequenced* relative to each other, and the standard makes that explicitly undefined.

This is not merely "the value is unpredictable" — it is UB, so the compiler is entitled to produce anything at all. GCC and Clang give different answers for `i++ + i++`, and both are correct. `-Wsequence-point` (in `-Wall`) warns.

The `printf` line has a **second, independent** problem: the order in which function arguments are evaluated is **unspecified** even without the double modification. `f(g(), h())` may call `h` first. That is a weaker category than UB — one of a set of permitted orders is chosen — but it still means `printf("%d %d", i++, i++)` may print `5 6` or `6 5`.

The rule to carry: **modify a variable at most once per expression, and do not read it elsewhere in that expression except to compute the new value.** `i = i + 1` is fine. `a[i] = i++` is not. When in doubt, split into separate statements — the semicolon is a sequence point, and it is free.

**3.**

```c
#define SET(f, n)     ((f) |=  (1u << (n)))
#define CLEAR(f, n)   ((f) &= ~(1u << (n)))
#define TOGGLE(f, n)  ((f) ^=  (1u << (n)))
#define TEST(f, n)    (((f) >> (n)) & 1u)

int count_set_bits(unsigned int n) {
    int count = 0;
    while (n) {
        n &= n - 1;          /* clears the lowest set bit */
        count++;
    }
    return count;
}
```

The four operations map onto the operators exactly: **OR sets** (1 forces a 1), **AND with the complement clears** (0 forces a 0), **XOR toggles** (1 flips), and a shift-and-mask tests.

Every macro parameter is parenthesised, and `1u` is unsigned. Both matter: without the inner parentheses `SET(f, a|b)` expands wrongly, and `1 << 31` on a signed `int` is undefined behaviour while `1u << 31` is fine. In real code prefer `static inline` functions to macros — they get type checking and evaluate arguments once.

`n &= n - 1` is **Kernighan's trick**. Subtracting 1 flips the lowest set bit to 0 and sets every bit below it; ANDing with the original clears that one bit and nothing else. The loop therefore runs once per *set* bit rather than 32 times — O(popcount) instead of O(width). GCC exposes the hardware instruction directly as `__builtin_popcount`, and C23 standardises it as `stdc_count_ones`.

**4.** The **comma operator** evaluates its left operand, discards the result, evaluates its right operand, and yields *that* value. It is a sequence point, so the left side is fully evaluated — including side effects — before the right side begins.

In the `for` loop it is the only way to run **two** initialisations and **two** updates in slots that syntactically permit just one expression each. `i++, j--` increments `i`, discards the result, decrements `j`, and yields that — and since the `for` header discards the update expression's value anyway, both side effects are all that matter. This is the standard two-pointer traversal used for reversing an array or testing a palindrome.

`int a = 1, 2;` is a syntax error because the comma there is **not the operator** — in a declaration, the comma is a *separator* between declarators, so the parser expects another declarator (a name) after it and finds the literal `2`. The same character is a separator in function argument lists too, which is why `f(a, b)` passes two arguments while `f((a, b))` passes one.

Outside `for` headers and a few macro idioms, the comma operator is best avoided: `x = (a(), b());` is legal, obscure, and better written as two statements. Knowing it exists mainly protects you from misreading code that uses it.



---

## Key Vocabulary

| Term | Definition |
|------|-----------|
| **Precedence** | Which operator binds more tightly when they appear together |
| **Associativity** | Left-to-right or right-to-left when operators have equal precedence |
| **Short-circuit** | `&&` and `\|\|` skip evaluating the right operand when unnecessary |
| **Bitwise AND** | `a & b`: bit set only where both a and b have a 1 |
| **Bitwise OR** | `a \| b`: bit set where either a or b has a 1 |
| **Bitwise XOR** | `a ^ b`: bit set where a and b differ |
| **Bit mask** | A pattern of bits used with AND/OR/XOR to isolate or set specific bits |
| **Shift** | `<<` and `>>`: multiply/divide by powers of 2 |
| **Ternary** | `cond ? a : b`: expression-level if-else |
| **UB** | Undefined behavior: the compiler may do anything |

---

*Next: Lecture 3 — Control Flow: if, switch, while, for*
