# Compilation Error Hunt — Problem 4

**File:** `error_log.md`
**Course:** PROG 101, Week 0, Problem Set 0
**Toolchain:** `gcc (Ubuntu 15.2.0-16ubuntu1) 15.2.0`, x86-64 Linux

`broken.c` contains **10 deliberate errors**. Each is listed with its line, category and fix. The
corrected file is `fixed.c`, which compiles clean under
`gcc -Wall -Wextra -Werror -std=c11`.

---

## Error 1
- **Location:** Line 1
- **Problem:** `#include <stdio.h` — missing the closing `>`.
- **Category:** Preprocessor error (fatal).
- **Fix:** `#include <stdio.h>`

## Error 2
- **Location:** Line 2
- **Problem:** `#include "helpers.h"` — the file does not exist (and nothing from it is used).
- **Category:** Preprocessor error (fatal).
- **Fix:** Remove the line, or create `helpers.h`.

## Error 3
- **Location:** Line 8
- **Problem:** `void main(void)` — `main` must return `int`.
- **Category:** Compiler error.
- **Fix:** `int main(void)`

## Error 4
- **Location:** Line 9
- **Problem:** `int status = 3` — missing terminating `;`.
- **Category:** Compiler error (syntax).
- **Fix:** `int status = 3;`

## Error 5
- **Location:** Line 12
- **Problem:** `printf("Version: %d\n" VERSION);` — the missing comma means the two tokens are
  *adjacent*; `VERSION` is the integer `2`, not a string, so they cannot concatenate.
- **Category:** Compiler error (syntax).
- **Fix:** `printf("Version: %d\n", VERSION);`

## Error 6
- **Location:** Line 13
- **Problem:** `%d` used to print a `double` (`ratio`) — a format/argument type mismatch.
- **Category:** Undefined behavior (diagnosed as a format warning).
- **Fix:** `printf("Ratio: %f\n", ratio);`

## Error 7
- **Location:** Line 14
- **Problem:** `%s` used to print an `int` (`status`) — the argument is not a `char *`.
- **Category:** Undefined behavior (diagnosed as a format warning).
- **Fix:** `printf("Status: %d\n", status);`

## Error 8
- **Location:** Line 17 (the `summarise(status);` call)
- **Problem:** `summarise` is never declared or defined.
- **Category:** **Linker error.**
- **Fix:** Declare it (`void summarise(int code);`) and define it, or remove the call.

## Error 9
- **Location:** Line 19
- **Problem:** `return 1;` inside a function declared `void` — a void function cannot return a value.
  (`main` should return `int` anyway, see Error 3.)
- **Category:** Compiler error.
- **Fix:** Make `main` return `int` and use `return 0;`.

## Error 10
- **Location:** Lines 23 and 25
- **Problem:** The `printf` on line 23 is missing its `;`, and line 25 uses `if (code = 3)` —
  **assignment**, not comparison, which assigns 3 (always true).
- **Category:** Compiler error (syntax) / logic error.
- **Fix:** Add the `;`; change `=` to `code == 3`.

---

## The error the compiler cannot catch

**Error 8 (`summarise`) is the one that only the linker finds at the link stage.** C lets a
translation unit *call* a function that no file defines: the compiler emits an **undefined symbol**
(`U summarise`) into `hello`-style object code and moves on, because it cannot see the whole program —
another translation unit might supply `summarise`. Only the **linker**, which collects every
translation unit and library, can demand that the symbol resolve.

Verified: with a prototype present (`void summarise(int code);`) but no definition, compilation
succeeds —

```
$ gcc -Wall -Wextra -std=c11 -c w5.c -o w5.o
$ nm w5.o | grep summarise
                 U summarise
```

— and then linking fails:

```
$ gcc w5.o -o w5
/usr/bin/x86_64-linux-gnu-ld.bfd: w5.o: in function `main':
w5.c:(.text+0x7f): undefined reference to `summarise'
collect2: error: ld returned 1 exit status
```

This is why "undefined reference" errors look so different from compiler errors: the program is already
binary by the time it happens.

---

## The diagnostic cascade

The two preprocessor faults are **fatal** and mask everything after them, so the errors surface in
waves. Fixing and re-running is required — a single `gcc` run does not show all ten.

**Wave 1 — as issued:**

```
broken.c:1:18: error: missing terminating ‘>’ character
broken.c:2:10: fatal error: helpers.h: No such file or directory
compilation terminated.
```

**Wave 2 — after Errors 1 and 2 are fixed:**

```
w2.c:7:6:  warning: return type of ‘main’ is not ‘int’ [-Wmain]
w2.c:9:5:  error: expected ‘,’ or ‘;’ before ‘double’
w2.c:11:27: error: expected ‘)’ before numeric constant
w2.c:11:23: warning: format ‘%d’ expects a matching ‘int’ argument [-Wformat=]
w2.c:12:27: error: ‘ratio’ undeclared (first use in this function)
w2.c:13:22: warning: format ‘%s’ expects argument of type ‘char *’, but argument 2 has type ‘int’
w2.c:16:5:  error: implicit declaration of function ‘summarise’
w2.c:18:12: error: ‘return’ with a value, in function returning void [-Wreturn-mismatch]
w2.c:22:30: error: expected ‘;’ before ‘if’
w2.c:26:1:  warning: control reaches end of non-void function [-Wreturn-type]
```

Note the cascade: the missing `;` on line 9 leaves `ratio` undeclared, so gcc reports *that* on line 12
rather than the `%d`-for-`double` mismatch. Error 6 (the format mismatch) only becomes visible once
Error 4 is fixed — here in **wave 3**:

```
w3.c:12:21: warning: format ‘%d’ expects argument of type ‘int’, but argument 2 has type ‘double’
w3.c:13:22: warning: format ‘%s’ expects argument of type ‘char *’, but argument 2 has type ‘int’
```

**Wave 4 — the link:**

```
/usr/bin/x86_64-linux-gnu-ld.bfd: w5.o: in function `main':
w5.c:(.text+0x7f): undefined reference to `summarise'
collect2: error: ld returned 1 exit status
```

(A modern-gcc note: since GCC 14, `implicit declaration of function` is an **error** by default in
C11 mode, whereas the original key notes it as a warning under `-Werror` only. Either way the
`summarise` problem is the one whose *resolution* is deferred to the linker.)

---

*PROG 101 · Week 0 · Problem Set 0 · Problem 4*
