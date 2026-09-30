---
assessment: Quiz 0
course: PROG 101
component: Quizzes
possible: 20
score: 20
status: submitted
started: 2026-09-30
submitted: 2026-09-30
graded: 2026-09-30
source: "QUIZ 0.md"
---

# PROG 101 · Quiz 0
## Answer Sheet

**Assessment:** `QUIZ 0.md`
**Points available:** 20

> Write your answers under each heading. Leave the **Marks** lines alone — they are filled
> in during grading. When you are done, set `status: submitted` in the frontmatter above.

---

### Answer

#### Section A — Multiple Choice

**Question 1.** Which compilation stage replaces `#include <stdio.h>` with the contents of the header file?

**Answer.** **(C) Preprocessor.** Every line starting with `#` is a preprocessor directive, and the
preprocessor handles them all before the compiler runs. In Lab 0, `gcc -E` turned my 8-line
`hello.c` into an 821-line `hello.i`, and almost all of the extra lines were `stdio.h`.

**Question 2.** Compiling `program.c` gives `undefined reference to 'calculate_tax'`. Which stage produced this error?

**Answer.** **(D) Linker.** The compiler only needs a *declaration* (prototype) to accept a call, so
compilation succeeds. The linker then looks for the function's *definition* in every object file
and library, and it reports "undefined reference" when it can't find one. I got exactly this error
in Lab 0 for `add_three`, when my copy of `buggy.c` was missing the function body.

**Question 3.** Which GCC flag produces an assembly file (`.s`) from a C source file, running only the preprocessor and compiler?

**Answer.** **(B) `-S`.** For comparison: `-E` stops after preprocessing (`.i`), `-c` stops after
assembling (`.o`), and `-o` only names the output file. It doesn't choose which stages run.

**Question 4.** What does the `U` symbol type mean in the output of `nm hello.o`?

**Answer.** **(B) The symbol is undefined: it is referenced here but defined elsewhere.** The object
file calls the function but doesn't contain its code. The linker fills in the address later, from
another object file or from a library such as `libc`. A symbol defined in the file's code section
is shown as `T` instead.

**Question 5.** What is wrong with this code?

```c
int main(void) {
    int x;
    printf("%d\n", x);
    return 0;
}
```

**Answer.** **(B) `x` is read before being initialized, which is undefined behaviour.** A local
variable is not set to zero automatically. It holds whatever bytes were already in its memory, so
the program can print a different value every time. (The snippet also leaves out
`#include <stdio.h>`, but none of the options is about that.)

#### Section B — Short Answer

**Question 6.** List the four stages of C compilation in order, with the input and output file types of each.

**Answer.**

| Stage | Name | Input | Output |
|---|---|---|---|
| 1 | Preprocessing | `.c` (source) | `.i` (preprocessed source) |
| 2 | Compilation | `.i` | `.s` (assembly) |
| 3 | Assembly | `.s` | `.o` (object file) |
| 4 | Linking | `.o` files and libraries | executable (no extension on Linux, e.g. `hello`) |

**Question 7.** What is the difference between a declaration and a definition in C? Give one example of each.

**Answer.**

- **Declaration:** tells the compiler a name and its type, so the name can be used, but does not
  create it. There is no function body and no memory is allocated. A name can be declared many
  times.
  Example: `int add_three(int a, int b, int c);`
- **Definition:** actually creates the thing. For a function, that means giving its body; for a
  variable, it means allocating its memory. A name must be defined exactly once in the whole
  program. A definition also counts as a declaration.
  Example: `int add_three(int a, int b, int c) { return a + b + c; }`

**Question 8.** What does `printf("%5.2f", 3.14159);` print? Why?

**Answer.** Output: ` 3.14`, with **one leading space**.

`.2` rounds the number to 2 decimal places, which gives `3.14`, 4 characters long. `5` is the
*minimum field width*: if the result is shorter than 5 characters, it is padded on the left with
spaces until it is 5 wide. So one space is added in front.

**Question 9.** The Makefile below gives `Makefile:2: *** missing separator.  Stop.` What is the error and the fix?

```makefile
hello: hello.c
    gcc -o hello hello.c
```

**Answer.**

- **Error:** line 2, the recipe line, starts with spaces. Make only treats a line as a command if
  it starts with a **TAB** character, so it can't make sense of line 2.
- **Fix:** replace the spaces before `gcc` with one TAB. `cat -A Makefile` shows the difference: a
  TAB is displayed as `^I`, and spaces are shown as they are.

**Question 10.** In GDB, what is the difference between `next` and `step`? When would you use `step`?

**Answer.**

- **`next`:** runs the current line and stops at the next line of the *same* function. If the line
  calls a function, the whole call runs without stopping (it "steps over" it).
- **`step`:** runs the current line, but if the line calls a function that has debug info, GDB
  stops at the first line *inside* that function (it "steps into" it).
- **When to use `step`:** when you think the bug is inside the function being called. For example,
  on `total = total + add_three(a, b, c);` I would use `step` to follow the addition inside
  `add_three`, and `next` if I trusted `add_three` and only wanted to see the new value of `total`.

*Marks: 20 / 20*

---

## Grading Summary

_Filled in by the grader._

| | |
|---|---|
| **Score** | 20 / 20 |
| **Percent** | 100% |
| **Graded** | 2026-09-30 |

**Feedback:**

All ten answers are technically correct. Q8 was checked by execution: `printf("%5.2f", 3.14159)`
prints `[ 3.14]` — exactly one leading space, 5 characters wide, with `.2` rounding to `3.14` and
the `5` supplying the minimum field width. Q6's stage table, Q7's declaration/definition
distinction and Q10's `next`/`step` contrast are all accurate, and Q5 correctly notes the missing
`#include <stdio.h>` without being distracted by it.

**One caveat the grader must close.** Section A was answered with bare letters — (C), (D), (B), (B),
(B) — but this answer sheet contains **no option lists**, and the original `QUIZ 0.md` handout is not
in the registry, so the letter choices could not be checked. The *reasoning* under each letter is
correct and consistent with the course material, which is why full credit is awarded here. Confirm the
five letters against the original quiz before releasing the mark; if any letter is wrong, deduct 1
point for that question only.

