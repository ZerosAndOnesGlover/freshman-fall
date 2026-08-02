# PROG 101 · Programming I - Structured Programming in C
## Week 0 · Lecture 3: Hello World Deep Dive & Your First C Program

---

## Lecture Goals

By the end of this lecture you will:
- Understand the anatomy of a C program in detail
- Know the difference between declaration and definition
- Understand how `printf` formats output
- Write, compile, and run C programs with confidence
- Know what happens at program startup and shutdown

---

## 1. Anatomy of a C Program

Every C program follows a recognizable structure. Let's look at a slightly richer example than "hello world":

```c
/*
 * program: temperature.c
 * purpose: convert Celsius to Fahrenheit
 * author:  PROG 101
 */

#include <stdio.h>      /* Standard I/O — printf, scanf */
#include <stdlib.h>     /* Standard library — exit, malloc */

/* Function declaration (prototype) — the compiler needs to know
   the signature before we use it below in main() */
double celsius_to_fahrenheit(double celsius);

/* The entry point of the program */
int main(void) {
    double celsius;
    double fahrenheit;

    printf("Enter temperature in Celsius: ");
    scanf("%lf", &celsius);

    fahrenheit = celsius_to_fahrenheit(celsius);

    printf("%.2f°C = %.2f°F\n", celsius, fahrenheit);

    return 0;   /* 0 = success */
}

/* Function definition — the actual implementation */
double celsius_to_fahrenheit(double celsius) {
    return (celsius * 9.0 / 5.0) + 32.0;
}
```

Let's break down every element.

---

## 2. Comments

C has two comment styles:

```c
/* This is a block comment.
   It can span multiple lines.
   Used for file headers, function documentation. */

// This is a line comment. C99 and later. Preferred for inline notes.
```

Comments are stripped out by the preprocessor before the compiler sees anything. They have zero cost at runtime.

**Rule of thumb:** Comment the *why*, not the *what*. The code shows what you're doing; comments explain why you chose to do it that way.

```c
// BAD: comment restates the code
x = x + 1;  // increment x by 1

// GOOD: comment explains the reasoning
x = x + 1;  // offset by 1 because array indices are 0-based but user sees 1-based
```

---

## 3. The Preprocessor Directives

```c
#include <stdio.h>
#include <stdlib.h>
```

`<angle brackets>` search system include paths (like `/usr/include/`).
`"quotes"` search the current directory first, then system paths.

Key headers you will use this course:

| Header | Provides |
|--------|----------|
| `<stdio.h>` | `printf`, `scanf`, `fopen`, `fclose`, `fprintf`, `fgets` |
| `<stdlib.h>` | `malloc`, `free`, `exit`, `atoi`, `rand` |
| `<string.h>` | `strlen`, `strcpy`, `strcmp`, `memcpy`, `memset` |
| `<math.h>` | `sqrt`, `pow`, `sin`, `cos`, `fabs` (link with `-lm`) |
| `<stdbool.h>` | `bool`, `true`, `false` (C99) |
| `<stdint.h>` | `int32_t`, `uint64_t`, etc. (exact-width types) |
| `<assert.h>` | `assert()` — runtime invariant checking |

---

## 4. Declaration vs. Definition

This distinction is *fundamental* to C and causes enormous confusion for beginners.

| Concept | What it does | Example |
|---------|-------------|---------|
| **Declaration** | Tells the compiler a name exists and its type | `double celsius_to_fahrenheit(double);` |
| **Definition** | Provides the actual implementation/storage | `double celsius_to_fahrenheit(double c) { return ...; }` |

**The rule:** A name must be *declared* before it is *used*. It must be *defined* exactly once across the entire program.

```c
// Declaration only (prototype) — typically in header files
double celsius_to_fahrenheit(double celsius);

// Definition — typically in .c files
double celsius_to_fahrenheit(double celsius) {
    return (celsius * 9.0 / 5.0) + 32.0;
}
```

If you use a function *before* declaring it, the compiler will warn (or error), it doesn't know what type to expect for arguments and return value.

If you *define* a function twice (in different `.c` files that are both linked), the linker will error: `multiple definition of 'celsius_to_fahrenheit'`.

---

## 5. Variables and Types

```c
double celsius;     // Declaration of a variable (type + name)
double fahrenheit;
```

In C, variables must be declared *before use* (in C89/C90) or anywhere in the block (in C99 and later, with `-std=c11`). We use C11 in this course.

**C has no automatic initialization.** An uninitialized variable contains whatever bytes happen to be in that memory location, which could be anything. Reading an uninitialized variable is *undefined behavior*.

```c
int x;          // x contains garbage — DO NOT READ before assigning
int y = 0;      // y is properly initialized
```

**Always initialize your variables.**

```c
int count = 0;
double temperature = 0.0;
char *name = NULL;      // NULL pointer is the safe initial value for pointers
```

---

## 6. The `printf` Format System

`printf` is one of the most powerful and flexible functions in C. Its first argument is a *format string*, a string with embedded format specifiers that control how subsequent arguments are printed.

```c
printf(format_string, arg1, arg2, ...);
```

### Format Specifiers

| Specifier | Type | Example | Output |
|-----------|------|---------|--------|
| `%d` | `int` | `printf("%d", 42)` | `42` |
| `%i` | `int` | Same as `%d` | `42` |
| `%u` | `unsigned int` | `printf("%u", 42u)` | `42` |
| `%ld` | `long` | `printf("%ld", 1000000L)` | `1000000` |
| `%f` | `double` | `printf("%f", 3.14)` | `3.140000` |
| `%e` | `double` (scientific) | `printf("%e", 3.14)` | `3.140000e+00` |
| `%g` | `double` (shorter of %f/%e) | `printf("%g", 3.14)` | `3.14` |
| `%c` | `char` | `printf("%c", 'A')` | `A` |
| `%s` | `char *` (string) | `printf("%s", "hi")` | `hi` |
| `%p` | pointer | `printf("%p", ptr)` | `0x7fff...` |
| `%%` | literal `%` | `printf("100%%")` | `100%` |
| `%x` | `unsigned int` (hex) | `printf("%x", 255)` | `ff` |
| `%X` | `unsigned int` (hex upper) | `printf("%X", 255)` | `FF` |
| `%o` | `unsigned int` (octal) | `printf("%o", 8)` | `10` |

### Width and Precision

```c
printf("%10d", 42);       // Right-align in 10 chars:    "        42"
printf("%-10d", 42);      // Left-align in 10 chars:     "42        "
printf("%010d", 42);      // Zero-pad to 10 chars:       "0000000042"
printf("%.2f", 3.14159);  // 2 decimal places:           "3.14"
printf("%8.2f", 3.14159); // Width 8, 2 decimal places:  "    3.14"
printf("%s", "hello");    // Print string
printf("%.3s", "hello");  // Print at most 3 chars: "hel"
```

### Escape Sequences

```c
'\n'    // Newline (line feed, ASCII 10)
'\t'    // Tab (ASCII 9)
'\r'    // Carriage return (ASCII 13)
'\0'    // Null character (ASCII 0) — string terminator
'\\'    // Literal backslash
'\''    // Literal single quote
'\"'    // Literal double quote
'\a'    // Bell (makes terminal beep)
'\b'    // Backspace
```

---

## 7. The `scanf` Function

`scanf` reads formatted input from `stdin`. It is the input counterpart to `printf`.

```c
int x;
scanf("%d", &x);       // Read an integer into x
                       // NOTE: & (address-of) operator — we pass the ADDRESS
                       // so scanf knows where to write the value
```

**Why `&`?** `scanf` needs to *modify* your variable. In C, function arguments are passed *by value*, so the function gets a copy. To modify the original, you must pass its address (a pointer). `scanf` receives the address of `x` and writes the read value there.

```c
double temperature;
scanf("%lf", &temperature);   // %lf for double in scanf (NOT %f)

char name[50];
scanf("%49s", name);          // Read a string (no & needed — array decays to pointer)
                              // %49s limits to 49 chars + null terminator = safe
```

**`scanf` return value:** Returns the number of items successfully read. Always check it:

```c
int x;
if (scanf("%d", &x) != 1) {
    fprintf(stderr, "Error: failed to read integer\n");
    return 1;
}
```

---

## 8. The `return` Statement and Exit Codes

```c
return 0;    // Success
return 1;    // General error
```

The value returned from `main` is the program's **exit code** — a number the OS (and shell scripts) can read to know whether the program succeeded.

```bash
./hello
echo $?         # Print exit code of last command
                # 0 = success, non-zero = failure
```

This is how shell scripts chain programs: `./preprocess && ./compile && ./link` — the `&&` continues only if each program exits with 0.

Alternative: use `exit()` from anywhere in the program:
```c
#include <stdlib.h>

void validate(int x) {
    if (x < 0) {
        fprintf(stderr, "Fatal error: negative value %d\n", x);
        exit(1);    // Exit immediately with code 1
    }
}
```

---

## 9. Program Structure: The Big Picture

A C program consists of one or more `.c` source files (called **translation units**). Each may have a corresponding `.h` header file containing declarations.

```
project/
├── main.c          # Contains main(), entry point
├── math_utils.c    # Utility functions for math
├── math_utils.h    # Declarations for math_utils.c
├── string_utils.c  # Utility functions for strings
├── string_utils.h  # Declarations for string_utils.c
└── Makefile        # Build automation
```

`math_utils.h` declares what's in `math_utils.c`:
```c
/* math_utils.h */
#ifndef MATH_UTILS_H    /* Include guard — prevents multiple inclusion */
#define MATH_UTILS_H

double celsius_to_fahrenheit(double celsius);
int factorial(int n);

#endif /* MATH_UTILS_H */
```

`main.c` uses it:
```c
/* main.c */
#include "math_utils.h"     /* Our own header — quotes, not angle brackets */

int main(void) {
    printf("5! = %d\n", factorial(5));
    return 0;
}
```

This separation of declaration (header) from definition (source) is how large C programs stay manageable.

---

## 10. C Standards: Which C Are We Using?

C has evolved through several standards:

| Standard | Year | Key Additions |
|----------|------|---------------|
| K&R C | 1978 | Original C (Kernighan & Ritchie) |
| C89/C90 | 1989/1990 | First ANSI standard |
| C99 | 1999 | `//` comments, `bool`, `stdint.h`, mixed declarations |
| C11 | 2011 | `_Generic`, better Unicode, atomics |
| C17 | 2018 | Bug fixes (no new features) |
| C23 | 2023 | `bool` as keyword, `nullptr`, more |

**This course uses C11** (`-std=c11`). It gives us all modern C features without excessive complexity. Always compile with `-std=c11`.

---

## 11. Common Beginner Errors

```c
// ERROR 1: Forgetting semicolons
int x = 5        // Error: expected ';'

// ERROR 2: Assignment in condition (sometimes intentional, often a bug)
if (x = 5)       // Assigns 5 to x (always true!) — did you mean ==?
if (x == 5)      // Comparison — this is what you want

// ERROR 3: Using uninitialized variables
int x;
printf("%d\n", x);   // Undefined behavior — x holds garbage

// ERROR 4: Off-by-one in arrays
int arr[5];
arr[5] = 10;    // ERROR: valid indices are 0..4, not 0..5

// ERROR 5: FoC11rgetting & in scanf
int x;
scanf("%d", x);     // WRONG: passes value, not address → crash
scanf("%d", &x);    // CORRECT

// ERROR 6: Wrong format specifier
double x = 3.14;
printf("%d\n", x);  // WRONG: %d for int, not double → garbage output
printf("%f\n", x);  // CORRECT

// ERROR 7: Missing return type
main() { ... }      // Old K&R style — implicit int. NOT valid in C99+.
int main(void) { ... return 0; }   // CORRECT
```

---

## Practice Exercises

Work these before the next lecture. Each set moves from *trace* (predict what happens) through *explain* (say why) to *build* (write it yourself) and finally *stretch* (a step past the lecture). Answers are at the end of the section — attempt each exercise before reading them.

**1. (Trace.)** Predict the exact output. Two lines contain undefined or surprising behaviour — identify them.

```c
#include <stdio.h>
int main(void) {
    printf("%d\n", 5 / 2);
    printf("%f\n", 5 / 2);
    printf("%d %d\n", sizeof(int), 3);
    printf("%c\n", 65);
    printf("%s\n", "a\tb");
    return 0;
}
```

**2. (Explain.)** This program compiles but is unsafe. Identify every problem and give a correct version.

```c
#include <stdio.h>
int main(void) {
    char name[10];
    int age;
    printf("Name: ");
    scanf("%s", name);
    printf("Age: ");
    scanf("%d", &age);
    printf("%s is %d\n", name, age);
    return 0;
}
```

**3. (Build.)** Write a program that reads two integers and prints their sum, quotient, and remainder, returning a non-zero exit code on invalid input or division by zero. Then show how to inspect the exit code from the shell.

**4. (Stretch.)** Explain the difference between a declaration and a definition for each of: a function, a global variable, and a `struct` type. Give an example of each that is a declaration but not a definition.


### Answers

**1.** Line 1: **`2`** — integer division truncates toward zero.

Line 2: **undefined behaviour.** `5 / 2` is the `int` `2`, but `%f` tells `printf` to read a `double` from the argument list. Since `printf` is variadic, no conversion happens and no error is raised — it reinterprets whatever bits are in the wrong register. The output is garbage and may differ per run. To print `2.5` you need `5 / 2.0`; to print the `int` as a float, `(double)(5 / 2)`.

Line 3: **also wrong.** `sizeof` yields `size_t`, which is 8 bytes on a 64-bit system, and `%d` expects a 4-byte `int`. The correct specifier is **`%zu`**. This often *appears* to work, which makes it worse.

Line 4: **`A`** — `%c` takes an `int` and prints the character with that code; 65 is ASCII `A`.

Line 5: **`a<tab>b`**.

The general point: `printf` is variadic and **cannot check its arguments against the format string** at runtime. GCC does check when the format is a string literal — `-Wformat` (included in `-Wall`) catches both bugs here, which is a strong argument for never disabling it and for never building a format string dynamically.

**2.** **Three problems.**

1. **`scanf("%s", name)` has no width limit.** Any input longer than 9 characters overflows `name` and corrupts the stack — the classic buffer overflow. Fix with a width: `scanf("%9s", name)` (9, not 10 — the terminating `'\0'` needs the tenth byte).
2. **Return values are ignored.** If the user types `abc` at the age prompt, `scanf` returns 0, `age` is never assigned, and the program then reads an **uninitialised variable** — undefined behaviour. `scanf` returns the number of items successfully assigned; check it.
3. **`%s` stops at whitespace**, so "Ada Lovelace" stores only `Ada` and leaves ` Lovelace` in the input buffer to confuse the next read.

```c
#include <stdio.h>
#include <string.h>

int main(void) {
    char name[64];
    int age;

    printf("Name: ");
    if (!fgets(name, sizeof name, stdin)) return 1;
    name[strcspn(name, "\n")] = '\0';          /* strip the newline fgets keeps */

    printf("Age: ");
    if (scanf("%d", &age) != 1) {
        fprintf(stderr, "Not a number\n");
        return 1;
    }
    printf("%s is %d\n", name, age);
    return 0;
}
```

`fgets` with `sizeof buf` is the safe idiom for reading a line: it cannot overflow, and it handles embedded spaces. Its one quirk is that it **keeps the newline**, which `strcspn` removes.

**3.**

```c
#include <stdio.h>

int main(void) {
    int a, b;
    if (scanf("%d %d", &a, &b) != 2) {
        fprintf(stderr, "usage: two integers on stdin\n");
        return 1;
    }
    if (b == 0) {
        fprintf(stderr, "division by zero\n");
        return 2;
    }
    printf("sum = %d\n", a + b);
    printf("quotient = %d\n", a / b);
    printf("remainder = %d\n", a % b);
    return 0;
}
```

```bash
./prog <<< "7 2"
echo $?      # 0
./prog <<< "7 0"
echo $?      # 2
./prog <<< "abc"
echo $?      # 1
```

Three conventions are on display. **Exit code 0 means success**, non-zero means failure — the opposite of C's truthiness, and it is what lets `./prog && next_step` work in a shell. **Distinct codes for distinct failures** let a caller react differently; `sysexits.h` suggests standard values, though small integers are common. And **errors go to `stderr`**, not `stdout`, so that `./prog > results.txt` puts data in the file and still shows the error on the terminal.

Note `b == 0` must be checked *before* dividing: integer division by zero is undefined behaviour in C, not an exception, and on x86 it raises `SIGFPE` and kills the process.

**4.** A **declaration** introduces a name and its type. A **definition** additionally allocates storage or supplies the body. Every definition is a declaration; the reverse does not hold.

**Function.** `int square(int n);` is a declaration (a *prototype*) — no body, no code emitted. `int square(int n) { return n * n; }` is the definition. A program may repeat the declaration in every translation unit, but must contain **exactly one** definition.

**Global variable.** `extern int counter;` is a declaration — it promises the variable exists somewhere. `int counter;` at file scope is a **definition**: it allocates 4 bytes. This is why a header declares globals with `extern` and exactly one `.c` file defines them; putting `int counter;` in a header gives `multiple definition of 'counter'` at link time.

**Struct type.** `struct Node;` is a declaration of an *incomplete type* — the name exists, the layout does not. You may form `struct Node *` pointers to it, but not declare a `struct Node` variable or use `sizeof`. `struct Node { int v; struct Node *next; };` is the definition.

The incomplete-type case is genuinely useful: it enables **opaque pointers**, where a header exposes `typedef struct HashTable HashTable;` plus functions taking `HashTable *`, and the `.c` file alone knows the fields. Callers physically cannot reach inside, which is how C achieves encapsulation without classes. the Hashtables appendix's hash table API is built exactly this way.



---

## Key Vocabulary

| Term                        | Definition                                                                    |
| --------------------------- | ----------------------------------------------------------------------------- |
| **Translation unit**        | A single `.c` file after preprocessing, the unit the compiler works on        |
| **Declaration**             | Tells the compiler a name exists and its type, without defining it            |
| **Definition**              | Provides the actual storage or implementation                                 |
| **Format string**           | The first argument to `printf`/`scanf` containing specifiers                  |
| **Format specifier**        | A `%`-prefixed code specifying how to format an argument                      |
| **Exit code**               | The integer returned from `main`, the OS reads this                           |
| **Include guard**           | `#ifndef/#define/#endif` pattern preventing double-inclusion of headers       |
| **Undefined behavior (UB)** | Code the C standard allows compilers to handle however they choose — avoid it |

---

## Reading Assignment

Before Lab 0:
- **K&R Chapter 1** — "A Tutorial Introduction" — read completely
- **King, Ch. 1-2** — Introducing C, C Fundamentals

---

*Next: Lab 0 — [[LAB 0 Environment Setup]]*
