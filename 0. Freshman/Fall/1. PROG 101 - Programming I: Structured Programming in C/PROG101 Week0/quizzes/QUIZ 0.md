# PROG 101 · Programming I: Structured Programming in C
## Week 0 · Quiz 0

**Date:** Tuesday 29 September 2026 · 10:00–10:10 (start of Week 1, Lecture 1)
**Format:** Administered at the start of Week 1, Lecture 1 (Tuesday)
**Duration:** 10 minutes
**Closed book, closed notes**
**Points:** 20 (each question = 2 pts)

---

> This quiz covers the Week 0 lecture material. Read each question carefully.

---

## Section A: Multiple Choice (2 pts each)

**1.** Which compilation stage is responsible for replacing `#include <stdio.h>` with the contents of the header file?

- (A) Compiler
- (B) Assembler
- (C) Preprocessor
- (D) Linker

---

**2.** You compile `program.c` and get this error:
```
undefined reference to 'calculate_tax'
```
Which stage produced this error?

- (A) Preprocessor
- (B) Compiler  
- (C) Assembler
- (D) Linker

---

**3.** What GCC flag produces an assembly language file (`.s`) from a C source file, running only the preprocessor and compiler?

- (A) `-E`
- (B) `-S`
- (C) `-c`
- (D) `-o`

---

**4.** What does the `U` symbol type mean in the output of `nm hello.o`?

- (A) The symbol is defined in the current object file
- (B) The symbol is undefined — it is referenced here but defined elsewhere
- (C) The symbol is uninitialized
- (D) The symbol is a Unix system call

---

**5.** What is wrong with the following C code?

```c
int main(void) {
    int x;
    printf("%d\n", x);
    return 0;
}
```

- (A) `printf` requires `#include <stdlib.h>`, not `#include <stdio.h>`
- (B) `x` is read before being initialized; undefined behavior
- (C) `int main(void)` is invalid; it must be `int main()`
- (D) `return 0` is not a valid exit code

---

## Section B: Short Answer (2 pts each)

**6.** List the four stages of C compilation in order. For each, state what its input and output file types are.

```
Stage 1: ____________   Input: ______   Output: ______

Stage 2: ____________   Input: ______   Output: ______

Stage 3: ____________   Input: ______   Output: ______

Stage 4: ____________   Input: ______   Output: ______
```

---

**7.** What is the difference between a **declaration** and a **definition** in C? Give one example of each.

```
Declaration: _____________________________________________________________

Example: _________________________________________________________________

Definition: ______________________________________________________________

Example: _________________________________________________________________
```

---

**8.** What will the following `printf` call print? Explain why.

```c
printf("%5.2f", 3.14159);
```

```
Output: __________________________________________________________________

Explanation: _____________________________________________________________
```

---

**9.** A student writes this Makefile:

```makefile
hello: hello.c
    gcc -o hello hello.c
```

They run `make` and get:
```
Makefile:2: *** missing separator.  Stop.
```

What is the error and how do they fix it?

```
Error: ___________________________________________________________________

Fix: _____________________________________________________________________
```

---

**10.** In GDB, what is the difference between the `next` command and the `step` command?

```
next: ____________________________________________________________________

step: ____________________________________________________________________

When would you use step instead of next? ___________________________________
```

---

## Answer Key (Instructor Copy: Do Not Distribute)

1. **(C) Preprocessor** — The preprocessor handles all `#` directives before the compiler sees the code.

2. **(D) Linker** — "Undefined reference" is always a linker error. The compiler accepted the function call (it had a declaration). The linker failed to find the definition.

3. **(B) `-S`** — `-E` stops after preprocessing, `-S` stops after compilation (assembly output), `-c` stops after assembly (object file), `-o` names the output.

4. **(B) The symbol is undefined** — `U` means used but not defined in this translation unit. The linker will resolve it.

5. **(B) Reading uninitialized variable** — `x` is declared but never assigned a value. Reading it is undefined behavior. On most systems it'll print garbage, but the C standard allows anything.

6. 
   - Stage 1: **Preprocessing** — Input: `.c` — Output: `.i`
   - Stage 2: **Compilation** — Input: `.i` — Output: `.s`
   - Stage 3: **Assembly** — Input: `.s` — Output: `.o`
   - Stage 4: **Linking** — Input: `.o` — Output: (executable, no extension on Linux)

7. 
   - **Declaration**: announces a name's type to the compiler without providing its implementation or storage. Example: `double sqrt(double x);` or `extern int counter;`
   - **Definition**: provides the actual implementation or storage. Example: `double sqrt(double x) { ... }` or `int counter = 0;`

8. Output: `" 3.14"` (with a leading space)
   - `%5.2f` means: minimum field width of 5 characters, 2 decimal places. `3.14` is 4 characters wide (including decimal point), so one space is prepended to reach width 5.

9. 
   - **Error**: The command line `gcc -o hello hello.c` is indented with spaces, not a TAB character. Make requires TAB indentation for commands.
   - **Fix**: Replace the leading spaces before `gcc` with a single TAB character.

10. 
    - **`next`**: Execute the current line, treating function calls as a single step (step *over* them — don't enter the function).
    - **`step`**: Execute the current line, stepping *into* any function calls (entering them line by line).
    - Use `step` when you need to debug the behavior *inside* a function that is being called.
