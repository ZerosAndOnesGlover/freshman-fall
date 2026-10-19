---
assessment: Quiz 0
course: PROG 101
component: Quizzes
possible: 20
score: 20
status: graded
started: 2026-09-29
submitted: 2026-09-29
graded: 2026-09-29
source: "QUIZ 0.md"
---

# PROG 101 · Quiz 0
## Answer Sheet

**Assessment:** `QUIZ 0.md`
**Points available:** 20 (10 questions × 2)

---

## Section A — Multiple Choice

### Question 1  (2 pts)

**Which compilation stage replaces `#include <stdio.h>` with the header's contents?**

**Answer: (C) Preprocessor.** All `#` directives (`#include`, `#define`, conditional compilation) are
handled by the preprocessor, *before* the compiler ever sees the code.

*Marks: 2 / 2*

### Question 2  (2 pts)

**`undefined reference to 'calculate_tax'` — which stage produced this error?**

**Answer: (D) Linker.** "Undefined reference" is always a linker error. The compiler accepted the call
(it had a declaration to type-check against); the *linker* failed to find a definition anywhere among
the object files and libraries.

*Marks: 2 / 2*

### Question 3  (2 pts)

**Which flag produces a `.s` assembly file, running only the preprocessor and compiler?**

**Answer: (B) `-S`.** `-E` stops after preprocessing, `-S` stops after compilation (emits assembly),
`-c` stops after assembly (emits an object file), and `-o` names the output.

*Marks: 2 / 2*

### Question 4  (2 pts)

**What does the `U` symbol type mean in `nm hello.o`?**

**Answer: (B) The symbol is undefined — referenced here but defined elsewhere.** The linker must
supply it. (By contrast `T` means defined in the current object's code section.)

*Marks: 2 / 2*

### Question 5  (2 pts)

**What is wrong with this code?**

```c
int main(void) {
    int x;
    printf("%d\n", x);
    return 0;
}
```

**Answer: (B) `x` is read before being initialized — undefined behavior.** `x` is declared but never
assigned. A local variable is not zero-initialised; reading it is undefined behaviour and typically
prints garbage.

*Marks: 2 / 2*

---

## Section B — Short Answer

### Question 6  (2 pts)

**The four stages of C compilation, with input and output types.**

```
Stage 1: Preprocessing   Input: .c   Output: .i  (expanded source)
Stage 2: Compilation     Input: .i   Output: .s  (assembly)
Stage 3: Assembly        Input: .s   Output: .o  (object file)
Stage 4: Linking         Input: .o   Output: executable (no extension on Linux)
```

*Marks: 2 / 2*

### Question 7  (2 pts)

**Difference between a declaration and a definition.**

- **Declaration:** announces a name's *type* to the compiler without providing its implementation or
  storage — it promises that the thing exists somewhere. Example: `double sqrt(double x);` or
  `extern int counter;`
- **Definition:** provides the actual implementation (code) or storage. Example:
  `double sqrt(double x) { ... }` or `int counter = 0;`

*Marks: 2 / 2*

### Question 8  (2 pts)

**What does `printf("%5.2f", 3.14159);` print, and why?**

**Output:** `" 3.14"` — with a **leading space**.

`%5.2f` means a minimum field width of **5** characters with **2** decimal places. `3.14159` rounds to
`3.14`, which is only 4 characters wide (the digits and the `.`), so a single space is prepended to
reach the width of 5.

*Marks: 2 / 2*

### Question 9  (2 pts)

**Why does the Makefile below fail with `Makefile:2: *** missing separator. Stop.`?**

```makefile
hello: hello.c
    gcc -o hello hello.c
```

**Error:** the recipe line (`gcc -o hello hello.c`) is indented with **spaces**, not a real **TAB**.
Make requires recipe lines to begin with a tab; spaces are not accepted.

**Fix:** replace the leading spaces before `gcc` with a single **TAB** character.

*Marks: 2 / 2*

### Question 10  (2 pts)

**Difference between GDB's `next` and `step`.**

- **`next`:** executes the current line, treating a function call as a *single* step — it steps **over**
  the call without entering the function.
- **`step`:** executes the current line, stepping **into** any function call so you can watch it run line
  by line.
- **Use `step`** when the bug is likely *inside* the function being called; use `next` to stay at the
  current level.

*Marks: 2 / 2*

---

## Grading Summary

| | |
|---|---|
| **Score** | 20 / 20 |
| **Percent** | 100% |
| **Graded** | 2026-09-29 |

**Feedback:**
Full marks. All five multiple-choice answers correct with the right reasoning (preprocessor for
`#include`; linker for "undefined reference"; `-S` for assembly; `U` = undefined; uninitialised read =
UB). The four stages are listed in order with correct file types, declaration vs definition is stated
crisply with examples, the `%5.2f` field-width explanation correctly notes the leading space, the
Makefile error is identified as space indentation and fixed with a tab, and `next` vs `step` is
correctly distinguished including when to use `step`.
