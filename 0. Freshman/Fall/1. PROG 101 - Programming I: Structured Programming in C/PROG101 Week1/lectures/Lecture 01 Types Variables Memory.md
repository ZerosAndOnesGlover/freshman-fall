# PROG 101 — Programming I: Structured Programming in C
## Week 1 · Lecture 1: Types, Variables, and the Memory Model

---

## Lecture Goals

By the end of this lecture you will:
- Understand what a type *actually is* at the hardware level
- Know every fundamental C type, its size, and its range
- Understand two's complement representation of signed integers
- Know the difference between the stack and static memory
- Use `sizeof` correctly
- Understand type promotions and implicit conversions

---

## 1. What Is a Type?

Most beginners think of a type as a label — "this is an int, that is a double." That is true but incomplete. Here is the complete picture:

**A type specifies three things:**
1. **How many bytes** the value occupies in memory
2. **How those bytes are interpreted** (as an integer? a float? a character?)
3. **What operations are legal** on the value

Consider: the 32-bit pattern `01000001 00000000 00000000 00000000` (in hex: `0x41000000`) means:

- Interpreted as `int`: the number `1,090,519,040`
- Interpreted as `float`: the number `8.0`
- Interpreted as `char[4]`: the string `"A\0\0\0"`

Same bits. Completely different meaning. **The type is the lens through which you read memory.**

This is not academic. It is the root cause of:
- Why you get garbage when you use the wrong `printf` specifier
- Why casting between types can produce unexpected values
- Why undefined behavior is so dangerous — the compiler may interpret bits however it wants

---

## 2. Memory: The Big Picture

Before types make sense, you need a mental model of memory.

Memory is a giant array of bytes. Each byte has an address — a number from 0 to 2⁶⁴-1 on a 64-bit system.

```
Address     Content
─────────────────────
0x00000000  [byte]
0x00000001  [byte]
0x00000002  [byte]
...
0x7fff5678  [byte]   ← stack (grows downward)
0x7fff5679  [byte]
...
0x00601000  [byte]   ← global/static variables
0x00601001  [byte]
...
0x00400000  [byte]   ← program code (text segment)
```

When you declare `int x = 42;` inside a function, the compiler:
1. Allocates 4 bytes somewhere on the **stack**
2. Stores the two's complement representation of 42 in those 4 bytes
3. Associates the name `x` with that address (name exists only in the compiler — not at runtime)

At runtime, there are no variable names. There are only addresses and bytes.

---

> **Where the integer and floating-point detail went.** How integers are *represented* —
> two's complement, the fixed ranges, and what happens on overflow — is Lecture 2. How real
> numbers are approximated, and the rules for converting between types, is Lecture 3. This
> lecture establishes what a type *is* and how variables occupy memory.

## 3. The `sizeof` Operator

`sizeof` returns the size (in bytes) of a type or variable at **compile time** — it is not a function call, it has zero runtime cost.

```c
printf("sizeof(char)      = %zu\n", sizeof(char));       // 1
printf("sizeof(short)     = %zu\n", sizeof(short));      // 2
printf("sizeof(int)       = %zu\n", sizeof(int));        // 4
printf("sizeof(long)      = %zu\n", sizeof(long));       // 8 (on 64-bit Linux/macOS)
printf("sizeof(float)     = %zu\n", sizeof(float));      // 4
printf("sizeof(double)    = %zu\n", sizeof(double));     // 8
printf("sizeof(pointer)   = %zu\n", sizeof(void *));     // 8 (on 64-bit)

int arr[10];
printf("sizeof(arr)       = %zu\n", sizeof(arr));        // 40 (10 × 4)
printf("array length      = %zu\n", sizeof(arr)/sizeof(arr[0]));  // 10
```

Note: `sizeof` returns type `size_t` — use `%zu` format specifier.

---

## 4. Variable Declaration, Initialization, and Scope

### Declaration Syntax

```c
type variable_name;              // Declaration (uninitialized — DANGEROUS)
type variable_name = value;      // Declaration with initialization (PREFERRED)
type a, b, c;                    // Multiple declarations (avoid for readability)
type a = 1, b = 2, c = 3;       // Multiple with initialization
```

### The Memory of an Uninitialized Variable

When you declare `int x;` inside a function, the compiler reserves 4 bytes on the stack. Those 4 bytes contain whatever was left there by the previous function call. It is not zeroed. It is garbage.

```c
int x;            // 4 bytes on stack — contains garbage
int y = 0;        // 4 bytes on stack — contains 0
```

**Always initialize your variables.** The cost is zero. The benefit is avoiding the most confusing class of bugs in C.

Exception: global and static variables are **zero-initialized** by the C standard:
```c
int global_count;          // Initialized to 0 by the OS/runtime
static int call_count;     // Initialized to 0 by the OS/runtime

int main(void) {
    int local;             // NOT initialized — garbage
    static int persistent; // Initialized to 0 — persists between function calls
}
```

### Scope

A variable's **scope** is the region of code where it is visible:

```c
int x = 10;          // File scope (global) — visible everywhere in this file

int main(void) {
    int y = 20;      // Block scope — visible only inside main's { }
    
    {
        int z = 30;  // Inner block scope — visible only inside this { }
        printf("%d %d %d\n", x, y, z);   // OK: all visible here
    }
    
    printf("%d\n", z);   // ERROR: z is out of scope
}
```

**Rule:** Declare variables in the smallest scope where they are needed. This limits the impact of bugs and makes code easier to reason about.

---

## 5. Constants and Literals

```c
// Integer literals
int a = 42;           // Decimal
int b = 0b101010;     // Binary (C23) or use hex: 0x2A
int c = 052;          // Octal (leading 0) — BEWARE: 052 = 42
int d = 0x2A;         // Hexadecimal (leading 0x)

// Suffixes
long        e = 42L;    // L suffix → long
long long   f = 42LL;   // LL suffix → long long
unsigned    g = 42U;    // U suffix → unsigned
unsigned long h = 42UL; // Combined

// Floating-point literals
double x = 3.14;        // double by default
float  y = 3.14f;       // f suffix → float
long double z = 3.14L;  // L suffix → long double
double sci = 6.022e23;  // Scientific notation: 6.022 × 10²³

// Character literals
char c1 = 'A';          // 65
char c2 = '\n';         // 10 (newline)
char c3 = '\x41';       // 65 (hex escape)
char c4 = '\101';       // 65 (octal escape)

// String literals (NOT a type — we cover these later)
const char *s = "Hello";  // Array of chars ending in '\0'
```

---

## 6. The `const` Qualifier

`const` tells the compiler the value should not be modified. It is enforced at compile time:

```c
const double PI = 3.14159265358979;
PI = 3.0;    // ERROR: assignment of read-only variable

const int MAX = 100;
int arr[MAX];    // OK: MAX is a compile-time constant
```

Use `const` wherever the value should not change. It:
- Prevents accidental modification
- Documents your intent to readers
- Enables the compiler to make optimizations
- Is better than `#define` for typed constants (the compiler knows the type)

---

## Practice Exercises

Work these before the next lecture. Each set moves from *trace* (predict what happens) through *explain* (say why) to *build* (write it yourself) and finally *stretch* (a step past the lecture). Answers are at the end of the section — attempt each exercise before reading them.

**1. (Trace.)** Predict each value on a typical 64-bit Linux/GCC system, then verify with a program.

```c
sizeof(char)   sizeof(int)   sizeof(long)   sizeof(void *)
sizeof('a')    sizeof("hi")
INT_MAX + 1    (char)200
```

**2. (Explain.)** Explain why this loop never terminates, and give two different fixes.

```c
for (unsigned i = 10; i >= 0; i--) {
    printf("%u\n", i);
}
```

**3. (Build.)** Write a function `void print_bits(unsigned int n)` that prints all 32 bits of `n`, most significant first. Use it to show the two's complement representation of `-1`, `-8`, and `INT_MIN`.

**4. (Stretch.)** Predict the output and explain the rule that produces it.

```c
#include <stdio.h>
int main(void) {
    int i = -1;
    unsigned u = 1;
    if (i < u) printf("less\n");
    else printf("NOT less\n");
    return 0;
}
```


### Answers

**1.** `1`, `4`, `8`, `8`, then **`4`**, **`3`**, then undefined behaviour, then `-56`.

**`sizeof('a')` is 4, not 1.** A character *constant* in C has type `int`, not `char` — a genuine difference from C++, where it is 1. `sizeof("hi")` is **3** because a string literal is a `char` array including the terminating `'\0'`, whereas `strlen("hi")` is 2.

**`INT_MAX + 1` is undefined behaviour**, not a wrap to `INT_MIN`. Signed overflow is UB, which means the compiler may assume it never happens — and does: with `-O2`, GCC will optimise `if (x + 1 < x)` to `false` outright. Build with `-fsanitize=undefined` and it reports the overflow at runtime. *Unsigned* overflow, by contrast, is fully defined to wrap modulo 2ⁿ.

**`(char)200` is −56** on x86, where plain `char` is signed: 200 exceeds `CHAR_MAX` of 127, and the conversion yields 200 − 256 = −56. Note plain `char` has **implementation-defined signedness** — it is unsigned on ARM — so `char` is a third type distinct from both `signed char` and `unsigned char`. Use `unsigned char` whenever you mean a byte.

Only `sizeof(char) == 1` is guaranteed by the standard. Everything else is a property of the platform.

**2.** An `unsigned` value **can never be negative**, so `i >= 0` is always true — a tautology. When `i` is 0 and decrements, it wraps to `UINT_MAX` (4,294,967,295) rather than −1, and the loop runs forever.

GCC's `-Wtype-limits` (part of `-Wextra`) reports *comparison of unsigned expression >= 0 is always true*, which is why `-Wextra` is not optional.

**Fix 1 — use a signed counter:**

```c
for (int i = 10; i >= 0; i--)
```

**Fix 2 — keep unsigned and restructure the test**, which is the right move when the index must be `size_t` for array work:

```c
for (unsigned i = 10; i-- > 0; )   /* runs with i = 9..0 */
```

or, to include 10:

```c
for (unsigned i = 11; i-- > 0; )
```

The `i-- > 0` idiom tests the value *before* decrementing, so it stops correctly at 0 without ever wrapping.

This matters constantly in real code because `sizeof` and `strlen` return `size_t`, which is unsigned. The pattern `for (size_t i = len - 1; i >= 0; i--)` is the same bug, with the extra hazard that `len - 1` is `SIZE_MAX` when `len` is 0.

**3.**

```c
#include <stdio.h>
#include <limits.h>

void print_bits(unsigned int n) {
    for (int i = 31; i >= 0; i--) {
        putchar((n >> i) & 1u ? '1' : '0');
        if (i % 8 == 0 && i) putchar(' ');
    }
    putchar('\n');
}

int main(void) {
    print_bits((unsigned)-1);       /* 11111111 11111111 11111111 11111111 */
    print_bits((unsigned)-8);       /* 11111111 11111111 11111111 11111000 */
    print_bits((unsigned)INT_MIN);  /* 10000000 00000000 00000000 00000000 */
    return 0;
}
```

The parameter must be **`unsigned`**: `n >> i` on a negative signed value is implementation-defined (GCC sign-extends, filling with 1s), which would corrupt the output. On an unsigned value the shift is guaranteed logical, filling with 0s.

The three outputs make two's complement concrete. `-1` is all ones, which is why `~0 == -1`. `-8` is `~8 + 1`. And `INT_MIN` is a single leading 1 — with the crucial consequence that **`-INT_MIN` overflows**, since `+2147483648` is not representable. The range is asymmetric: −2³¹ to 2³¹−1. That asymmetry is the root of the `abs(INT_MIN)` bug and of the comparator overflow you will meet in Week 3.

**4.** It prints **`NOT less`**.

The rule is the **usual arithmetic conversions**. When a binary operator has one `int` and one `unsigned int` operand of the same rank, the signed operand is converted to unsigned. So `-1` becomes `(unsigned)-1` = 4,294,967,295, and the comparison `4294967295 < 1` is false.

The signed value is not "promoted to something wider" — on this platform there is no wider type at the same rank, so the conversion loses the sign entirely. (If `long` were involved and could hold every `unsigned int` value, the unsigned operand would convert to `long` instead and the comparison would work as expected. The rules depend on the relative sizes of the types, which is why they are so easy to get wrong.)

`-Wsign-compare`, included in `-Wextra`, warns here.

The practical instance you will hit is comparing an index against `strlen` or `sizeof`, both of which return unsigned `size_t`:

```c
for (int i = 0; i < (int)strlen(s); i++)   /* cast, or use size_t */
```

and the guard `if (len - 1 >= 0)`, which is always true for unsigned `len` and is a real source of out-of-bounds reads when `len` is 0. **Never mix signed and unsigned in a comparison.** Pick one and cast explicitly.



---

## Key Vocabulary

| Term | Definition |
|------|-----------|
| **Type** | Specifies size, interpretation, and valid operations for a value |
| **Two's complement** | The standard binary representation of signed integers |
| **Integer overflow** | Exceeding a type's range: defined for unsigned (wraps), UB for signed |
| **IEEE 754** | The standard for binary floating-point representation |
| **Integer promotion** | Automatic conversion of small integer types to `int` in expressions |
| **Implicit conversion** | Type change performed automatically by the compiler |
| **Explicit cast** | A programmer-written type conversion: `(double)x` |
| **Scope** | The region of code where a variable name is visible |
| **`sizeof`** | Compile-time operator returning size in bytes of a type or variable |
| **`const`** | Qualifier declaring a variable's value must not change |
| **Undefined behavior (UB)** | Code the C standard allows compilers to handle in any way |

---

## Questions to Sit With

1. Why does `-128` require a special case in two's complement? What is `-(−128)` for an 8-bit signed integer?
2. What does `printf("%d\n", 'A' + 1)` print? Why?
3. What happens to `unsigned int x = 0; x = x - 1;`? Is this defined or undefined behavior?
4. Why might `sizeof(long)` give different results on different systems, and how do you write code that's portable?

---

*Next: Lecture 2 — Operators, Expressions, and Bit Manipulation*