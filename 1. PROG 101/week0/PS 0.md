---
assessment: PS 0
course: PROG 101
component: Problem Sets
possible: 100
score: 94.5
status: in-progress
started: 2026-09-30
submitted:
graded: 2026-09-30
source: "Problem Set 0.md"
---

# PROG 101 · PS 0

## Answer Sheet

**Assessment:** `Problem Set 0.md`
**Points available:** 100

> Write your answers under each heading. Leave the **Marks** lines alone — they are filled
> in during grading. When you are done, set `status: submitted` in the frontmatter above.

---

**Where the work is.** All code and reports are in `ps0/`. Run `make test` there to build and run
everything. This sheet gives the answer to each question; the report files have the full
evidence: command output, excerpts and line numbers.

| Problem | Files in `ps0/`                                              |
| ------- | ------------------------------------------------------------ |
| 1       | `hello.c`, `preprocessor_report.md`                          |
| 2       | `info.c`                                                     |
| 3       | `stages_report.md`                                           |
| 4       | `broken.c` (as given), `error_log.md`, `fixed.c`             |
| 5       | `greet.h`, `greet.c`, `main.c`, `Makefile`, `make_report.md` |

Everything was run with GCC 13.3.0 and GNU Make 4.3 on Ubuntu 24.04.5, x86_64.

---

### Problem 1 — Preprocessor Investigation (12 points)

**Question 1.1.** How many lines are in `hello.c` and in `hello.i`? State the ratio.

**Answer.** `hello.c` has **8** lines and `hello.i` has **821** (`wc -l`), a ratio of about
**1 : 103**. My own code is only the last 5 lines of `hello.i` (lines 817–821). The rest comes from
`stdio.h` and the 24 other headers it includes.

**Question 1.2.** Paste the declaration of `printf` from `hello.i` with its line number. Which header did it come from?

**Answer.**

```
477: extern int printf (const char *__restrict __format, ...);
```

It came from **`/usr/include/stdio.h`, line 363**. The nearest linemarker above it, on line 447, is
`# 334 "/usr/include/stdio.h" 3 4`, and 334 + (477 − 448) = 363. `grep -n` on `stdio.h` confirms
line 363.

**Question 1.3.** What are linemarkers for? What would break in `gcc` error messages without them?

**Answer.** A linemarker (`# <line> "<file>" <flags>`) records which original file and line the
next line of `hello.i` came from. The flags mark entering an included file (`1`), returning to
the file that included it (`2`), and system headers (`3`). The compiler uses them to report errors
against my source. Without them, errors would point into the preprocessed file. I tested this with
a missing `;`: with markers, GCC reported `err.c:7:13`; after `gcc -E -P`, which removes them, it
reported `without.i:308:13`, a line in a file I never wrote. Debug info would be wrong in the same
way, and warnings from system headers would stop being suppressed.

**Question 1.4.** Add `#define GREETING "Hello, world"`, use it in `printf`, and re-run the preprocessor. What do you find when you search `hello.i` for `GREETING`? What does that tell you?

**Answer.** `grep -n GREETING hello.i` finds **nothing** (exit status 1). The `#define` line is gone
too. Line 820 reads `printf("Hello, world" "!\n");`: the name has been replaced by its text. This
shows that `#define` is resolved entirely by the **preprocessor, before compilation**. It is plain
text substitution, and the compiler never sees the name `GREETING`.

**Question 1.5.** Why does `hello.i` contain `printf`'s declaration but not its code? At which stage does its machine code join the program?

**Answer.** Headers contain only **declarations**, which give a function's name, return type and
parameters. That's all the compiler needs to check a call and generate code for it. The **code**
of `printf` was compiled long ago and lives in the C library (`libc.so.6`). It joins the program at
**linking**. `hello` is dynamically linked, so the linker records which libc symbol the program
needs (`puts@GLIBC_2.2.5`), and the dynamic loader connects the call to libc's code when the
program starts.

_Marks: 11.5 / 12_

---

### Problem 2 — Personal Info Printer (18 points)

**Question 2.** Write `info.c`, which uses `#define` for name, ID and year and prints the 52-character-wide information card, compiling clean with `-Wall -Wextra -Werror`.

**Answer.** `ps0/info.c`. Output:

```
╔══════════════════════════════════════════════════╗
║             PROG 101 Student Profile             ║
╠══════════════════════════════════════════════════╣
║  Name:    Adebayo Glover                         ║
║  ID:      20260001                               ║
║  Year:    2030                                   ║
║  Course:  PROG 101 - Structured Programming in C ║
╚══════════════════════════════════════════════════╝
```

- **`#define`** is used for `STUDENT_NAME`, `STUDENT_ID`, `GRAD_YEAR` and `COURSE`.
- **Width and alignment:** each row is `║` + 50 characters + `║`. The fields are printed with a
  left-aligned fixed width (`%-39s`, and `%-39d` for the year), so the right border always lands in
  column 52, whatever the value's length. I checked it by measuring every output line: all 8 are
  exactly 52 characters. `diff` against the handout's sample shows no difference.
- **Limitation:** `printf` widths count **bytes**, not characters. The box characters are 3 bytes
  each in UTF-8, so they are only used in the fixed parts of the format strings, and the field
  values must be plain ASCII. A name with an accent (é is 2 bytes) would push that row's border
  one column left.
- **Compiles clean:** `gcc -Wall -Wextra -Werror -g -std=c11` gives no warnings.

_Marks: 14 / 18_

---

### Problem 3 — The Remaining Three Stages, By Hand (22 points)

**Question 3.1.** Tabulate the byte sizes of `hello.i`, `hello.s`, `hello.o` and `hello`. Which stage causes the largest increase, and why?

**Answer.**

| Artefact  | Bytes (`wc -c`) |
| --------- | --------------- |
| `hello.i` | 21,360          |
| `hello.s` | 761             |
| `hello.o` | 1,584           |
| `hello`   | 15,960          |

**Linking** causes the largest increase: +14,376 bytes, turning a 1.6 KB object into a 16 KB
executable. The linker adds everything needed to load and start a program (see 3.4). Compiling
_shrinks_ the file by 96%, because unused declarations from `stdio.h` produce no assembly.

**Question 3.2.** Paste the instruction that calls `printf`, and the line storing your string literal with the section directive above it. What is that section for, and why is the string kept apart from the instructions?

**Answer.**

```asm
 3:     .section .rodata
 4: .LC0:
 5:     .string "Hello, world!"
...
22:     call    puts@PLT
```

The call is to **`puts`, not `printf`**. GCC replaces `printf` with `puts` when the format has no
`%` conversions and ends in `\n` (note that the stored string has no `\n`). `-fno-builtin` brings
back `call printf@PLT`. `.rodata` is **read-only data**. It is kept apart from `.text` so that the
loader can give each its own permissions: `.text` is read + execute, and `.rodata` is read-only and
**not executable** (separate `R E` and `R` segments in `readelf -l`). So data can never be run as
code, code can't be modified, and writing to a string literal crashes instead of silently changing
it.

**Question 3.3.** What letter does `nm hello.o` give `printf`, and what does it mean? What changes in `nm hello`, and which stage changed it?

**Answer.** `nm hello.o` shows `U puts`. **`U` = undefined**: it is called here but defined
elsewhere, and `hello.o` only has a relocation where its address will go. `nm hello` shows
**`U puts@GLIBC_2.2.5`**. The **linker** has resolved it to libc and recorded the version the
program needs. It is still `U` because the code stays in `libc.so.6` and is connected at load
time. By contrast, a `-static` link shows `puts` at a real address. The linker also gave `main` a
real address (`0x1149` instead of `0`), and it added 28 other symbols, including `_start`.

**Question 3.4.** Account for the size difference between `hello` and `hello.o`. Name at least two kinds of content that are in the executable but not in the object file.

**Answer.** `hello.o` has 13 sections; `hello` has 30.

1. **Page-alignment padding: 9,471 bytes, about two-thirds of the file.** The four `LOAD`
   segments have different permissions, so each must start on a new 4 KiB page (file offsets
   `0x0`, `0x1000`, `0x2000`, `0x2db8`), and the gaps between them are zeros.
2. **Dynamic-linking information:** `.interp` (the loader's path), `.dynamic`, `.dynsym`,
   `.dynstr`, `.gnu.version_r`, `.rela.plt`, and the `.plt` and `.got` tables.
3. **C runtime start-up code:** `Scrt1.o`, `crti.o`, `crtbeginS.o`, `crtendS.o` and `crtn.o`
   (`_start`, `_init`, `_fini`, `.init_array` and `.fini_array`).
4. **Loader metadata:** program headers, a build ID and an ABI tag note.

_Marks: 21.5 / 22_

---

### Problem 4 — The Compilation Error Hunt (20 points)

**Question 4.** Document each error in `broken.c` (location, problem, category, fix) in `error_log.md`, write a corrected `fixed.c`, and say which error only appears at link time and why.

**Answer.** Full log: `ps0/error_log.md`. Fixed version: `ps0/fixed.c`, which compiles clean
under `-Wall -Wextra -Werror -std=c11` and prints `Version: 2`, `Ratio: 0.75`, `Status: 3`,
`Code 3`, `Status is three`, `Summary: status 3`.

| #   | Line  | Problem                                      | Category                                  | Fix                           |
| --- | ----- | -------------------------------------------- | ----------------------------------------- | ----------------------------- |
| 1   | 1     | `#include <stdio.h` has no closing `>`       | Preprocessor                              | `#include <stdio.h>`          |
| 2   | 2     | `helpers.h` doesn't exist (fatal)            | Preprocessor                              | remove the include            |
| 3   | 8, 19 | `void main` with `return 1;`                 | Compiler                                  | `int main(void)`, `return 0;` |
| 4   | 9     | missing `;` after `int status = 3`           | Compiler (syntax)                         | add `;`                       |
| 5   | 12    | missing comma: `"…%d\n" VERSION`             | Compiler (syntax)                         | `"…%d\n", VERSION`            |
| 6   | 13    | `%d` given a `double`                        | Undefined behaviour                       | `%.2f`                        |
| 7   | 14    | `%s` given an `int`                          | Undefined behaviour                       | `%d`                          |
| 8   | 17    | `summarise` is defined nowhere               | **Linker**                                | declare and define it         |
| 9   | 23    | missing `;` after `printf(...)`              | Compiler (syntax)                         | add `;`                       |
| 10  | 24    | `if (code = 3)` assigns instead of comparing | Logic error                               | `==`                          |
| 11  | 22–27 | `int describe` has no `return`               | Compiler warning; UB if the value is used | `return 0;`                   |

I found **eleven** faults, not ten. The eleventh is kept separate so the count can be checked.
Errors 6 and 7 aren't just theoretical: after fixing the syntax, the program printed
`Ratio: -1966951776` and then crashed with a segmentation fault on the `%s`.

**The linker-only error is Error 8.** The compiler handles one file at a time, and a call only
needs a declaration. It can't know whether another file or library will provide the definition,
so it just leaves an undefined symbol for later. Only the linker sees all the code together, so
only the linker can find out that no definition exists
(`undefined reference to 'summarise'`). As written, GCC also warns about an _implicit
declaration_, because nothing declares `summarise`. I checked that if `helpers.h` had existed and
declared it, compilation would have been completely silent and only the link would have failed.

_Marks: 20 / 20_

---

### Problem 5 — Make and the Incremental Rebuild (28 points)

**Question 5.1.** Write a Makefile that builds `greet` from `main.o` and `greet.o`, using `$@`, `$<` and `$^`, with `.PHONY` and `clean`, and the required flags.

**Answer.** `ps0/Makefile`:

- **Link rule:** `greet: main.o greet.o` → `$(CC) $(CFLAGS) -o $@ $^`. `$^` is all the objects.
- **Object rules:** `main.o: main.c greet.h` and `greet.o: greet.c greet.h` →
  `$(CC) $(CFLAGS) -c -o $@ $<`. `$<` is just the `.c` file, so the header isn't passed to `gcc -c`.
- **Other targets:** `.PHONY: all clean test`, a `clean` target, and
  `CFLAGS = -Wall -Wextra -Werror -g -std=c11`. The same Makefile builds `info`, `hello`, `fixed`
  and `greet`, and `make test` runs all four.

**Question 5.2.** After running `make`, what rebuilds after `touch main.c`, `touch greet.c`, `touch greet.h`, and after running `make` twice with no edits? Why?

**Answer.** Make rebuilds a target when a prerequisite is newer than it:

- **`touch main.c`:** rebuilds `main.o`, then relinks `greet`.
- **`touch greet.c`:** rebuilds `greet.o`, then relinks `greet`.
- **`touch greet.h`:** rebuilds **both** `.o` files, because both list the header as a
  prerequisite, then relinks.
- **Twice with no edits:** `make: Nothing to be done for 'all'.` Every target is newer than its
  prerequisites.

**Question 5.3.** Remove `greet.h` from the prerequisites, change its declaration (add a parameter), rebuild, and describe what goes wrong. Why is this worse than a compile error?

**Answer.** After changing `greet.h` to `void greet(int year);`, `make` said
**`'greet' is up to date.`** and rebuilt nothing. Then I updated `greet.c` to print the year. Make
rebuilt only `greet.o` and linked it with the **stale** `main.o`, which still calls `greet()` with
no argument. The program built and ran without any error and printed
`Hello from greet.c, class of 1!`. The "year" is whatever was left in the argument register `%edi`,
which is `argc`: `./greet a b` printed 3, and `./greet a b c d e` printed 6. With the prerequisite
restored, Make recompiled `main.c`, and GCC immediately reported
`error: too few arguments to function 'greet'`.

It is **worse than a compile error** because nothing reports it. The build succeeds, the source
looks correct, and the program's behaviour depends on leftover register values, so the bug can pass
testing. It also only shows up as a real error after a clean rebuild or on a different machine. I
restored the prerequisite, and the submitted files are the original versions.

**Question 5.4.** Indent a recipe line with spaces instead of a TAB. Paste the exact error. Why is it so common, and what makes it hard to see?

**Answer.**

```
Makefile.4sp:13: *** missing separator. Stop.
Makefile.8sp:13: *** missing separator (did you mean TAB instead of 8 spaces?). Stop.
```

Make only treats a line as a recipe if it **starts with a TAB character**. A line starting with
spaces is read as a rule or variable assignment, and Make can't find the `:` or `=` "separator".
It's common because most editors insert spaces when you press Tab, and copying from web pages or
PDFs turns TABs into spaces. It's hard to see because a TAB and spaces look identical on screen,
and the message only mentions TABs when there are exactly 8 spaces. `cat -A` shows a TAB as `^I`,
which makes the difference visible.

_Marks: 27.5 / 28_

---

## Grading Summary

_Filled in by the grader._

|             |              |
| ----------- | ------------ |
| **Score**   | 94.5 / 100   |
| **Percent** | 94.5%        |
| **Graded**  | 2026-09-30   |

**Feedback:**

Verified by re-running every command on Ubuntu 24.04.5 / GCC 13.3.0. The technical work is strong:
almost every measurement, line number and quoted diagnostic reproduced exactly, including the
`nm` symbol counts, the `2,520 + 3,707 + 3,244 = 9,471` padding arithmetic, the seven-warning cascade
in `broken.c`, and the stale-header experiment down to `make: *** [Makefile:28: main.o] Error 1`.

**Deductions:**

- **Problem 2 (−4).** `ps0/info.c` still ships placeholder data: `STUDENT_ID "20260001"` and
  `GRAD_YEAR 2030`, each carrying a `/* TODO: replace with my real ... */` comment. Problem 2 asks
  for *your* ID and year, and `20260001` appears nowhere else in the registry. The box engineering is
  flawless — all eight lines measure exactly 52 characters with the right border in column 52, and it
  compiles clean under `-Wall -Wextra -Werror` — but the two fields the problem is actually about are
  unfilled. **Fix this before submitting.**
- **Problem 1 (−0.5).** The answer to 1.1 gives 8 and 821, but the `hello.c` and `hello.i` in `ps0/`
  are 10 and 823 (the `GREETING` version). `preprocessor_report.md` explains the two versions, but the
  graded answer sheet presents the 8-line figures as the answer with no inline caveat, so it does not
  match the submitted artifacts. Restate it as "10 → 823" or note the switch in the answer itself.
- **Problem 3 (−0.5).** The padding is described as "about two-thirds" of the file; 9,471 / 15,960 is
  59.3%, i.e. about three-fifths. The 3.2 excerpt also shows only the first of the two `call puts@PLT`
  instructions.
- **Problem 5 (−0.5).** The 5.2 table says a first bare `make` rebuilt "nothing", but the transcript
  around it only ever runs `make greet`, so a bare `make` does still build `info`, `hello` and `fixed`.

Problem 4 is full marks. Finding eleven faults where the handout says ten, correctly identifying
`summarise` as the link-time-only error, and testing the `helpers.h` caveat yourself is exactly the
right treatment of that question.

**Not done:** the frontmatter still reads `status: in-progress` with an empty `submitted:` date. Set
`status: submitted` once the `info.c` values are corrected.
