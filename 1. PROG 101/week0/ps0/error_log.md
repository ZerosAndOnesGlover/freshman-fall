# PS 0 · Problem 4: Error Log for `broken.c`

**Machine:** Ubuntu 24.04.5 LTS, x86_64, GCC 13.3.0
**Line numbers** refer to `broken.c` exactly as copied from the handout (27 lines).

## How I found them

GCC stops at the first fatal error, so the errors show up in layers. I fixed each layer before
recompiling to reveal the next.

1. **As written.** Preprocessing fails before any C code is compiled:
   ```
   broken.c:1:18: error: missing terminating > character
   broken.c:2:10: fatal error: helpers.h: No such file or directory
   ```
2. **Lines 1–2 fixed.** The compiler now runs and reports syntax errors (errors) and suspicious code
   (warnings). The missing `;` on line 9 also causes a false error on line 13, `'ratio' undeclared`,
   because the declaration of `ratio` got merged into the broken line above it.
3. **Syntax fixed.** It compiles, with 7 warnings, which would all be errors under `-Werror`.
4. **Compile only (`-c`), then link.** The object file builds, and then:
   ```
   undefined reference to `summarise'
   collect2: error: ld returned 1 exit status
   ```
5. **Linked it anyway,** with a do-nothing `summarise` and warnings turned off, to see what the
   undefined behaviour actually does:
   ```
   Version: 2
   Ratio: -1966951776
   Segmentation fault (core dumped)          exit status 139
   ```

**Count.** I found **eleven** separate faults. The handout says ten. I've treated `void main` and
`return 1` as one error, since they're two halves of the same wrong signature for `main`. The
eleventh (the missing `return` in `describe`) is listed at the end.

---

## Error 1
- **Location:** Line 1
- **Problem:** Missing closing `>` in `#include <stdio.h`. GCC: `missing terminating > character`.
- **Category:** Preprocessor error
- **Fix:** `#include <stdio.h>`

## Error 2
- **Location:** Line 2
- **Problem:** `#include "helpers.h"` names a header that doesn't exist. GCC:
  `fatal error: helpers.h: No such file or directory`. It's *fatal*, so compilation stops here.
- **Category:** Preprocessor error
- **Fix:** Remove the line. Nothing in the program needs it once `summarise` is declared and defined
  in the file (Error 8).

## Error 3
- **Location:** Line 8 (and line 19)
- **Problem:** `void main(void)`. In a hosted C program, `main` must return `int`, and the return
  value becomes the program's exit status. GCC: `warning: return type of 'main' is not 'int'
  [-Wmain]`. Line 19 then has `return 1;` in a function declared `void`: `warning: 'return' with a
  value, in function returning void`. Even with `int main`, returning 1 would tell the shell that
  the program *failed*.
- **Category:** Compiler error (warning without `-Werror`, error with it)
- **Fix:** `int main(void)` and `return 0;`

## Error 4
- **Location:** Line 9
- **Problem:** Missing `;` after `int status = 3`. GCC: `error: expected ',' or ';' before
  'double'`. The error is reported against the *next* token. It also causes a false error on
  line 13 (`'ratio' undeclared`).
- **Category:** Compiler error (syntax)
- **Fix:** `int status = 3;`

## Error 5
- **Location:** Line 12
- **Problem:** Missing comma: `printf("Version: %d\n" VERSION);`. After preprocessing, this becomes
  `printf("Version: %d\n" 2);`, a string immediately followed by a number, which isn't valid C. GCC:
  `error: expected ')' before numeric constant`. It also warns that `%d` has no matching argument.
- **Category:** Compiler error (syntax). It is visible in the source, but the text the compiler
  actually sees is produced by the preprocessor.
- **Fix:** `printf("Version: %d\n", VERSION);`

## Error 6
- **Location:** Line 13
- **Problem:** `%d` with a `double` argument. `%d` expects an `int`. GCC: `format '%d' expects
  argument of type 'int', but argument 2 has type 'double' [-Wformat=]`. On x86-64, a `double` is
  passed in a different register (`%xmm0`) from an `int` (`%esi`), so `printf` reads a register
  that was never set. It printed `Ratio: -1966951776`.
- **Category:** Undefined behaviour (format-string fault; caught by `-Wall`)
- **Fix:** `printf("Ratio: %.2f\n", ratio);` prints `Ratio: 0.75`

## Error 7
- **Location:** Line 14
- **Problem:** `%s` with an `int` argument. `%s` expects the address of a string, so `printf` treats
  the number 3 as a memory address and tries to read characters from address 3. GCC: `format '%s'
  expects argument of type 'char *', but argument 2 has type 'int' [-Wformat=]`. This is what
  crashed the program: `Segmentation fault`, exit status 139.
- **Category:** Undefined behaviour (format-string fault; caught by `-Wall`)
- **Fix:** `printf("Status: %d\n", status);`

## Error 8: the linker error
- **Location:** Line 17
- **Problem:** `summarise(status);` calls a function that is **defined nowhere**. It isn't in this
  file, and it isn't in any library. The linker reports:
  `undefined reference to 'summarise'` / `collect2: error: ld returned 1 exit status`.
- **Category:** Linker error
- **Fix:** Declare and define it. In `fixed.c`:
  `void summarise(int code);` above `main`, and
  `void summarise(int code) { printf("Summary: status %d\n", code); }` below it.

## Error 9
- **Location:** Line 23
- **Problem:** Missing `;` after `printf("Code %d\n", code)`. GCC: `error: expected ';' before
  'if'`.
- **Category:** Compiler error (syntax)
- **Fix:** `printf("Code %d\n", code);`

## Error 10
- **Location:** Line 24
- **Problem:** `if (code = 3)` **assigns** 3 to `code` instead of comparing. The value of an
  assignment is the value assigned (3, which counts as true), so the branch *always* runs, whatever
  `code` was. GCC: `warning: suggest parentheses around assignment used as truth value
  [-Wparentheses]`.
- **Category:** Logic error (valid C, but caught by `-Wall`)
- **Fix:** `if (code == 3)`. I tested `fixed.c` with `status = 4`, and "Status is three" is
  correctly not printed.

## Error 11 (extra)
- **Location:** Lines 22–27
- **Problem:** `describe` is declared to return `int`, but it ends without a `return` statement. GCC:
  `warning: control reaches end of non-void function [-Wreturn-type]`. If a caller ever used the
  result, it would get whatever was left in `%eax`, which is undefined behaviour. Here the result is
  ignored, so the program happens to work, but `-Werror` still rejects it.
- **Category:** Compiler warning; undefined behaviour if the value is used
- **Fix:** `return 0;` at the end of `describe`.

---

## Which error can't be found by the compiler, and why

**Error 8, `summarise`.** The compiler works on **one file at a time**. When it reaches a call, it
only needs to know that the function exists and how to call it, which is what a declaration gives
it. It has no way of knowing whether some *other* file or library will provide the definition, so
it assumes one will. It just records "call `summarise` here" as a relocation, and `nm` would show
`U summarise`. Only the **linker** sees every object file and library together, and it's the first
stage that can notice that no definition exists anywhere.

This is the same as my `add_three` error in Lab 0, and it's what Quiz 0 Question 2 was about.

**One caveat from my test.** GCC 13 *does* warn here (`implicit declaration of function
'summarise'`), but only because `summarise` isn't declared at all. Before C99, C let you call an
undeclared function, so GCC still accepts it with a warning. Under `-Werror`, that warning stops
the build before linking. But if `helpers.h` had existed and declared `summarise` (as the line 2
include suggests was intended), the compiler would have had nothing to warn about. I tested this:
with a one-line `helpers.h` containing `void summarise(int code);`, `gcc -Wall -Wextra -c` printed
nothing about `summarise` and exited 0. The link then failed with
`undefined reference to 'summarise'`, exactly as the handout describes.
