# PROG 101 · Programming I: Structured Programming in C
## Week 0 · Problem Set 0

**Released:** End of Week 0
**Due:** Before Week 1 Lecture 1 (start of next week)
**Submission:** Push to your Git repository; submit the commit hash on the course portal.
**Collaboration policy:** Discussion of concepts allowed; code must be written independently.
**Grading:** Each problem is graded on correctness (70%), code quality (20%), and documentation (10%).

---

> **Revision note (2026-08-16).** Problems 1, 3, 4 and 5 were rebuilt to draw only on Week 0
> material. The previous versions required loops (Week 2), arrays (Week 4), pointers (Week 5),
> `malloc`/`free` (Week 6), recursion (Week 9) and macro-expansion semantics (Week 10) — 65 of
> 100 points tested content from later in the course. See `PREREQUISITE AUDIT.md`.
> The removed problems were good problems in the wrong week; they are preserved with their
> verified answer keys in `_RELOCATED Problems.md` for re-filing under Weeks 6, 9 and 10.
> **Problems 2 and 6 are unchanged**, as are their answer keys and the errata table below.

**Scope of this set.** Everything here is answerable from Lecture 01 (Compilation Model),
Lecture 02 (Toolchain, Make, GDB), Lecture 03 (Hello World Deep-Dive) and Lab 0.

**One forward reference, deliberately scoped.** Problems 5 and 6 ask you to write short
multi-file programs, so you will define a function or two. Use them exactly as Lecture 02 does
in its `main.c` / `utils.c` / `utils.h` example — a return type, a name, parameters, a body.
Calling conventions, pass-by-value semantics and prototypes are **Week 3**; you do not need them
here and will not be assessed on them.

---

## Setup

All your work this week goes in `~/prog101/week0/ps0/`.

```bash
mkdir -p ~/prog101/week0/ps0
cd ~/prog101/week0/ps0
```

Each problem should be in its own file. Submit a `Makefile` that builds all of them.

---

## Problem 1: Preprocessor Investigation (10 pts)

Start from the `hello.c` you built in Lab 0. Run **only** the preprocessor:

```bash
gcc -E hello.c -o hello.i
```

Answer the following in `preprocessor_report.md`. Every answer must cite evidence from *your*
`hello.i` — line numbers or pasted excerpts, not recollection.

1. *(2 pts)* How many lines are in `hello.c`? How many in `hello.i`? State the ratio.
2. *(2 pts)* Find the declaration of `printf` in `hello.i`. Paste it exactly, with its line number.
   Which header did it ultimately come from?
3. *(2 pts)* `hello.i` is full of lines beginning `# 1 "..."`. These are **linemarkers**. Explain
   what they are for. What would break in your `gcc` error messages if they were absent?
4. *(2 pts)* Add `#define GREETING "Hello, world"` to `hello.c` and use it in your `printf`.
   Re-run the preprocessor. Search `hello.i` for the string `GREETING`. What do you find, and what
   does that tell you about when `#define` is resolved?
5. *(2 pts)* `hello.i` contains printf's **declaration** but not its **code**. Explain why, and name
   the pipeline stage at which printf's actual machine code joins your program.

---

## Problem 2: Personal Info Printer (15 pts)

Write `info.c` — a program that:
1. Uses `#define` to define your name, student ID, and graduation year as constants
2. Prints a formatted information card using `printf`

Your output must look *exactly* like this (with your own information):

```
╔══════════════════════════════════════════════════╗
║             PROG 101 Student Profile             ║
╠══════════════════════════════════════════════════╣
║  Name:    Adebayo Glover                         ║
║  ID:      20260001                               ║
║  Year:    2026                                   ║
║  Course:  PROG 101 - Structured Programming in C ║
╚══════════════════════════════════════════════════╝
```

Requirements:
- Use `#define` for at least your name, ID, and year
- The box must be exactly 52 characters wide (including the border characters)
- Each field must be left-aligned within the box
- Compile clean with `-Wall -Wextra -Werror`

**Hint for the box characters:** These are UTF-8 characters. You can paste them directly into your string literals:
`╔ ═ ╗ ║ ╠ ╣ ╚ ╝`

---

## Problem 3: The Remaining Three Stages, By Hand (20 pts)

Problem 1 stopped after preprocessing. Now drive the other three stages yourself, one command at a
time — no all-in-one `gcc hello.c -o hello` until the very end.

```bash
gcc -S hello.i -o hello.s      # compile:  C  → assembly
gcc -c hello.s -o hello.o      # assemble: asm → object
gcc    hello.o -o hello        # link:     object → executable
```

Record your findings in `stages_report.md`.

**3.1** *(4 pts)* Tabulate all four artefacts — `hello.i`, `hello.s`, `hello.o`, `hello` — with the
byte size of each (`wc -c`). Which stage causes the largest *increase* in size, and why?

**3.2** *(5 pts)* Open `hello.s`. Find and paste:
- the instruction that calls `printf`
- the line where your string literal is stored, and the section directive above it

Explain what that section is for and why the string is not stored alongside the instructions.

**3.3** *(4 pts)* Run `nm hello.o`. What letter is `printf` given, and what does it mean? Now run
`nm hello`. What has changed about `printf`, and which stage changed it?

**3.4** *(4 pts)* `hello` is far larger than `hello.o`. Account for the difference concretely —
name at least two categories of content present in the executable but absent from the object file.

**3.5** *(3 pts)* Try to link with `ld hello.o -o hello_bad` instead of `gcc`. Paste the error.
Explain what `gcc` supplies at the link step that a bare `ld` invocation does not.

---

## Problem 4: The Compilation Error Hunt (15 pts)

The file `broken.c` below contains **10 deliberate errors**. Every one is diagnosable with Week 0
knowledge: they are preprocessor faults, syntax faults, format-string faults, and linker faults.

Copy this exactly into `broken.c` (do not fix anything yet):

```c
#include <stdio.h
#include "helpers.h"

#define VERSION 2

int describe(int code);

void main(void) {
    int status = 3
    double ratio = 0.75;

    printf("Version: %d\n" VERSION);
    printf("Ratio: %d\n", ratio);
    printf("Status: %s\n", status);

    describe(status);
    summarise(status);

    return 1;
}

int describe(int code) {
    printf("Code %d\n", code)
    if (code = 3) {
        printf("Status is three\n");
    }
}
```

Your task:
1. Create `error_log.md` documenting each error:
   - Error number (1–10)
   - The line and what is wrong
   - What category it is (preprocessor / compiler / linker / undefined behavior)
   - What the fix is
2. Create `fixed.c`: the fully corrected version, compiling clean under
   `gcc -Wall -Wextra -Werror -std=c11`

Format your `error_log.md` like this:

```markdown
## Error 1
- **Location:** Line 1
- **Problem:** Missing closing `>` in `#include <stdio.h`
- **Category:** Preprocessor error
- **Fix:** Change to `#include <stdio.h>`
```

**Note.** One of the ten cannot be found by the compiler at all — it only appears when you try to
link. Say which, and explain why the compiler let it through.

---

## Problem 5: Make and the Incremental Rebuild (20 pts)

Build a three-file project:

- `greet.h` — declares one function
- `greet.c` — defines it; it prints a greeting
- `main.c` — includes `greet.h` and calls it

**5.1** *(6 pts)* Write a `Makefile` that builds `greet` from `main.o` and `greet.o`, using the
automatic variables `$@`, `$<` and `$^` — at least one of each. Include `.PHONY` and a `clean`
target. Use `-Wall -Wextra -Werror -g -std=c11`.

**5.2** *(5 pts)* Demonstrate the timestamp model. Run `make`, then in `make_report.md` record what
rebuilds after each of these, and why:
- `touch main.c`
- `touch greet.c`
- `touch greet.h`
- `make` twice in a row with no edits

**5.3** *(5 pts)* Now deliberately **omit** `greet.h` from the prerequisite lists. Change the
declaration in `greet.h` (add a parameter), rebuild, and describe exactly what goes wrong. Why is
this failure mode worse than a compile error? Restore the prerequisite afterwards.

**5.4** *(4 pts)* Introduce a `Makefile` whose recipe line is indented with **spaces** rather than a
tab. Paste the exact error. Explain why this error is so common and what makes it hard to see.

---

## Problem 6: The Symbols Inspector (20 pts)

Write `symbols.c` containing:
- 3 global variables (one `int`, one `double`, one `char *`)
- 1 static global variable
- 2 functions that use them
- 1 function that is declared but never defined (to study linker errors)

Then use `nm` to inspect the symbol table and answer these questions in `symbols_report.md`:

1. What letter does `nm` use for defined global variables? Paste the relevant line.
2. What letter does `nm` use for undefined symbols? Paste the relevant line.
3. What letter does `nm` use for static (file-scoped) symbols?
4. What happens when you try to link a program that calls the undefined function? Paste the exact linker error.
5. How is the undefined function's symbol shown in `nm` output for `symbols.o`?
6. What is the difference between `nm symbols.o` and `nm symbols` (after linking without the missing function — how can you link without it)?

**Hint for question 6:** You can use `-Wl,--unresolved-symbols=ignore-all` to link despite undefined symbols (for educational purposes only).

---

## Makefile Requirement

Your top-level `Makefile` must:
- Build all programs: `info`, `hello`, `fixed`, `greet`, `symbols`
- Include a `clean` target
- Use `-Wall -Wextra -Werror -g -std=c11` flags
- Have a `test` target that runs quick sanity checks

```makefile
.PHONY: all clean test

all: info hello fixed greet symbols

test: all
	@echo "Testing info..."
	./info
	@echo "Testing greet..."
	./greet
	@echo "All tests passed."

clean:
	rm -f info hello fixed greet symbols *.o *.i *.s
```

---

## Submission

```bash
cd ~/prog101/week0/ps0
git add .
git commit -m "PS0: complete — all 6 problems"
git log --oneline -1    # Copy this commit hash for submission
```

Submit on the course portal:
- Your commit hash
- A brief reflection (2-3 sentences): what was the most surprising thing you learned this week?

---

## Grading Rubric

| Problem | Points | Key Criteria |
|---------|--------|-------------|
| P1: Preprocessor Investigation | 10 | Evidence cited from own `hello.i`, not recollection |
| P2: Info Printer | 15 | Exact formatting, `#define` used |
| P3: Three Stages By Hand | 20 | Each stage driven separately, assembly read correctly |
| P4: Error Hunt | 15 | All 10 errors found, categories correct, linker case identified |
| P5: Make and Incremental Rebuild | 20 | Automatic variables used, stale-header hazard demonstrated |
| P6: Symbols Inspector | 20 | All 6 questions answered with evidence |
| **Total** | **100** | |

**Late policy:** 10% deducted per day late. No submissions accepted after 5 days.

---

## Answer Key (Instructor Copy)

> **Do not distribute to students.** Totals follow the Grading Rubric above (100 points).
> All C below was compiled with `gcc 13.3.0 -Wall -Wextra -Werror -std=c11` and executed.

### ⚠️ Errata — CORRECTED in the text above

Two defects from the original P2/P6 material, verified against `gcc 13.3.0` / GNU `nm` on
x86-64 Linux. Both **have now been fixed in this document**. (A third erratum concerned the
Kelvin column of the retired temperature-table problem; it moved with that problem to
`_RELOCATED Problems.md`.)

| Location | Was (wrong) | Now |
|---|---|---|
| P6 reference answer 6 | "after which the symbol remains `U` in the executable". It does not. After `gcc -Wl,--unresolved-symbols=ignore-all symbols.o -o symbols_ignored`, `nm symbols_ignored \| grep undefined_function` returns **nothing** — the symbol is dropped, not retained. | Reworded to state the symbol does not appear in the linked executable's symbol table, and that calling it still crashes at runtime. |
| P2 box width | The prose requirement said the box "must be exactly 40 characters wide", but the sample art in the same problem is **52** characters on every line, and the note formerly here asserted it was 40. The art was widened to fit the full course title without the prose being updated. | Resolved in favour of the art: prose now requires **52**, and the grading note's field width is corrected from `%-27s` to `%-38s` to match. |

Students holding a pre-correction copy must not be penalised for a 40-character box.

---

### Problem 1 — Preprocessor Investigation (10 pts)

1. *(2 pts)* Typical `hello.c` is 5–7 lines; `hello.i` on glibc is **roughly 700–900 lines** for a
   bare `#include <stdio.h>`. Accept any figure of that order — it varies by libc version and by
   which headers `stdio.h` pulls in. Award the marks for *stating both numbers and the ratio*, not
   for hitting a target. A student reporting 30,000 lines has probably included more than `stdio.h`;
   ask, do not deduct.
2. *(2 pts)* The declaration is `extern int printf (const char *__restrict __format, ...);`,
   reached via `/usr/include/stdio.h`. Require the pasted line **and** a line number.
3. *(2 pts)* Linemarkers record the original file and line of the text that follows, so diagnostics
   can point at `hello.c:4` rather than `hello.i:812`. Without them every error message would cite
   a position in the expanded file, which the student never sees. Accept any answer that reaches
   "error messages would reference the wrong file/line".
4. *(2 pts)* `GREETING` does not appear in `hello.i` — the *string* `"Hello, world"` appears in its
   place. `#define` is resolved by the preprocessor, before the compiler runs; the compiler never
   sees the macro name at all. This is the point of the problem.
5. *(2 pts)* Headers declare, libraries define. `stdio.h` tells the compiler printf's *type* so
   calls can be type-checked; the machine code lives in libc and is attached at the **link** stage.
   Full marks require naming linking.

*Common failure: answering from Lecture 01 rather than from a file. Every item says "cite evidence".
An answer with no pasted excerpt or line number earns half, however correct.*

### Problem 2 — Info Printer (15 pts)

*Grading: 5 pts `#define` used for name/ID/year (a `const char *` or literal in the `printf` earns 0 for this item — the requirement is the preprocessor), 6 pts exact 52-character box with correct alignment, 4 pts clean compile under `-Wall -Wextra -Werror`.*
*Alignment is best done with width specifiers, e.g. `printf("║  Name:    %-38s ║\n", NAME);` — verified to reproduce the sample art exactly. The 11-character label prefix (`║` plus two spaces plus a padded field name), the explicit trailing space and the closing border leave exactly **38** columns for the value; note the space before `║` in the format string is not part of the field, so `%-39s` overshoots to 53. The longest value, the 38-character course title, fills the field exactly. Students who pad by hand with spaces get the right output for their own name but break for any other — mention it, deduct only if the output is actually misaligned.*
*Note: the box characters are multi-byte UTF-8, so `strlen` counts **bytes, not characters** and returns far more than 52 — verified, a border line is **156** bytes (52 box-drawing characters at 3 bytes each) and a content line is **56** (two `║` at 3 bytes plus 50 ASCII). A student who "verifies" width with `strlen` and panics is not wrong about the count — explain the distinction. This is worth a bonus mark if raised unprompted.*

### Problem 3 — The Remaining Three Stages, By Hand (20 pts)

**3.1** *(4 pts)* Representative figures on x86-64 / gcc 13.3.0 — **accept any values of this
shape**, they vary by toolchain:

| Artefact | Size | Note |
|---|---|---|
| `hello.i` | ~22 KB | preprocessing is the largest *relative* jump: a 100-byte source becomes tens of KB |
| `hello.s` | ~1 KB | assembly discards every declaration that generated no code |
| `hello.o` | ~1.5 KB | binary encoding of the same instructions, plus a symbol table |
| `hello` | ~16 KB | linking attaches startup files and dynamic-linking machinery |

Two defensible answers to "largest increase": **preprocessing** in relative terms (×200), **linking**
in absolute bytes from `.o`. Award full marks for either *with* a reason. The instructive point is
that `.s` is *smaller* than `.i` — most of a header is declarations, which emit no code.

**3.2** *(5 pts)* The call is `call printf@PLT` (or `call puts@PLT` — see below). The literal sits
under `.section .rodata` as `.string "Hello, world"`. `.rodata` is read-only data: mapped without
write permission, so a stray write to a string literal faults instead of corrupting memory. It is
separated from `.text` because the two get different page permissions.

> **Expect `puts`, not `printf`.** At `-O0` gcc still rewrites `printf("...\n")` with no format
> specifiers into `puts("...")`. A student who finds `call puts@PLT` and reports it has read their
> own file correctly — award full marks, and treat noticing the substitution as a bonus. Students
> who "find" `call printf@PLT` when their assembly says `puts` are reciting the prompt.

**3.3** *(4 pts)* In `hello.o`, printf (or puts) is **`U`** — undefined, referenced but not
supplied. In the linked `hello` it is either resolved to an address or appears as a PLT stub
entry; the **link** stage changed it.

**3.4** *(4 pts)* Two categories suffice. Accept from: the C runtime startup objects
(`crt1.o`, `crti.o`, `crtn.o`) that call `main`; the dynamic-linker path and `PT_INTERP` segment;
the PLT/GOT relocation machinery; ELF program headers absent from a relocatable object; symbol
and debug sections from the startup files.

**3.5** *(3 pts)* Bare `ld hello.o -o hello_bad` fails with `undefined reference to '_start'`
(and usually cannot find libc at all). `gcc` at link time supplies the startup objects that define
`_start`, the default library search paths, `-lc`, and the dynamic-linker setting. The lesson:
`gcc` is a *driver*, not a compiler — it orchestrates cpp, cc1, as and ld.

### Problem 4 — The Compilation Error Hunt (15 pts)

The ten planted defects:

| # | Line | Problem | Category | Fix |
|---|---|---|---|---|
| 1 | 1 | `#include <stdio.h` — missing `>` | Preprocessor | `#include <stdio.h>` |
| 2 | 2 | `#include "helpers.h"` — file does not exist | Preprocessor | Remove it, or create the header |
| 3 | 8 | `void main(void)` — `main` must return `int` | Compiler | `int main(void)` |
| 4 | 9 | `int status = 3` — missing `;` | Compiler (syntax) | Add `;` |
| 5 | 12 | `printf("Version: %d\n" VERSION)` — missing comma; the two literals concatenate | Compiler | `printf("Version: %d\n", VERSION);` |
| 6 | 13 | `%d` used to print a `double` | Undefined behavior | `printf("Ratio: %f\n", ratio);` |
| 7 | 14 | `%s` used to print an `int` | Undefined behavior | `printf("Status: %d\n", status);` |
| 8 | 17 | `summarise` never declared or defined | Linker | Define it, or remove the call |
| 9 | 19 | `return 1;` inside a function declared `void` | Compiler | Make `main` return `int` (see #3) and `return 0;` |
| 10 | 23 / 25 | Missing `;` after `printf("Code %d\n", code)`, and `if (code = 3)` — assignment, not comparison | Compiler (syntax) / logic | Add `;`; use `code == 3` |

**Verified diagnostics** (`gcc 13.3.0`, `-Wall -Wextra -std=c11`). Errors surface in waves — the two
preprocessor faults are *fatal* and mask everything else, so students must fix and re-run
iteratively. Say so in the debrief; a student who reports "only two errors" has run the compiler
exactly once.

| Wave | What gcc says |
|---|---|
| 1 (as issued) | `error: missing terminating > character` · `fatal error: helpers.h: No such file or directory` |
| 2 (after #1, #2) | `warning: return type of 'main' is not 'int' [-Wmain]` · `error: expected ',' or ';' before 'double'` · `error: expected ')' before numeric constant` · `warning: format '%s' expects argument of type 'char *' [-Wformat=]` · `warning: implicit declaration of function 'summarise'` |
| 3 (after #4, #5) | `warning: format '%d' expects argument of type 'int', but argument 2 has type 'double'` · `warning: 'return' with a value, in function returning void [-Wreturn-type]` · `warning: suggest parentheses around assignment used as truth value [-Wparentheses]` · `warning: control reaches end of non-void function [-Wreturn-type]` |
| 4 (link) | `/usr/bin/ld: undefined reference to 'summarise'` · `collect2: error: ld returned 1 exit status` |

Note that `%d`-for-`double` (#6) is *invisible* in wave 2: the missing semicolon on line 9 means
`ratio` is never declared, so gcc reports `'ratio' undeclared` instead. The format error only
appears once #4 is fixed. This cascade is the point of the exercise.

**Which one only the linker catches:** #8, `summarise`. C lets you *call* a function the compiler
has never seen — under C99/C11 this is a constraint violation that gcc reports as
`implicit declaration of function 'summarise'` (a **warning** by default, an error under
`-Werror`), but with only `-std=c11` and no `-Werror` it compiles to an object file carrying a `U`
symbol. The failure surfaces at link: `undefined reference to 'summarise'`. This is the same lesson
as Problem 6 approached from the other side.

**Two subtleties worth raising in class:**
- **#5 is silent.** Adjacent string literals concatenate in C, so `"Version: %d\n" VERSION` is not a
  syntax error if `VERSION` were a *string* macro. Here `VERSION` is `2`, so it fails — but change
  it to `#define VERSION "2"` and the code compiles and prints garbage for `%d`. Worth demonstrating.
- **#10's `if (code = 3)`** assigns and then tests 3, which is always true. `-Wall` catches it with
  `suggest parentheses around assignment used as truth value`. This is the single most valuable
  warning in the set — it is the reason `-Wall` is not optional.

*Grading: 1.5 pts per error (location + category + fix). A student who counts the missing `;` and
the `=`/`==` on lines 23/25 as two separate errors and therefore reports 11 has found the same set —
accept it. Award bonus credit for noticing that `describe` has no `return` statement despite being
declared `int` (a genuine 11th defect the prompt did not count).*

### Problem 5 — Make and the Incremental Rebuild (20 pts)

**5.1** *(6 pts)* Reference `Makefile`:

```makefile
CC      = gcc
CFLAGS  = -Wall -Wextra -Werror -g -std=c11
OBJS    = main.o greet.o

.PHONY: all clean

all: greet

greet: $(OBJS)
	$(CC) $(CFLAGS) $^ -o $@

%.o: %.c greet.h
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f greet $(OBJS)
```

*2 pts `$^` in the link rule, 2 pts `$<` in the compile rule, 1 pt `$@`, 1 pt `.PHONY` + `clean`.*

**5.2** *(5 pts)* Verified behaviour:

| Action | Rebuilds | Why |
|---|---|---|
| `touch main.c` | `main.o`, then relink | only that object is out of date |
| `touch greet.c` | `greet.o`, then relink | same |
| `touch greet.h` | **both** objects, then relink | both list `greet.h` as a prerequisite |
| `make` twice | `make: Nothing to be done for 'all'.` | no prerequisite is newer than its target |

**5.3** *(5 pts)* Verified. With `greet.h` dropped from the prerequisites and the declaration
changed from `void greet(void)` to `void greet(int times)`, `make` rebuilds **only `greet.o`** —
its own source changed — and leaves `main.o` stale, still compiled against the old declaration.
It then **links without a single diagnostic** and runs:

```
gcc -Wall -Wextra -Werror -g -std=c11 -c greet.c -o greet.o
gcc -Wall -Wextra -Werror -g -std=c11 main.o greet.o -o greet
$ ./greet
Hello 0
exit=0
```

The caller passes no argument; the callee reads whatever happens to be in the argument register.
Here that was 1, so the loop ran once. **The value is not deterministic** — students will report
different output, including no output or a very long loop, and all of those are correct
observations. Do not grade against a specific number.

Why this is worse than a compile error: there is no error. `-Wall -Wextra -Werror` is powerless,
because each translation unit is individually consistent — the disagreement exists only *between*
them, and nothing in the build is looking there. Full marks require that contrast, not just
"it breaks".

**5.4** *(4 pts)* `Makefile:5: *** missing separator.  Stop.` Recipe lines must begin with a real
tab. It is common because many editors expand tabs to spaces silently, and hard to see because tabs
and spaces are visually identical. Accept mention of `cat -A` or `.RECIPEPREFIX` as a diagnostic.

### Problem 6 — Symbols Inspector (20 pts)

Reference answers (`nm` letters are case-significant: **uppercase = global/external, lowercase = local/static**):

1. **`D`** — initialised global in the data segment. (An uninitialised global is **`B`**, BSS; a `const` one is often **`R`**, read-only data.)
2. **`U`** — undefined: referenced here, must be supplied by another translation unit at link time.
3. **`d`/`b`/`t`** — the lowercase counterparts, indicating file scope (`static`). A `static` function is **`t`**; a non-static function is **`T`**.
4. Linking fails at the **linker** stage, not the compiler — the exact wording on GNU ld is along the lines of:
   `undefined reference to 'never_defined'` followed by `collect2: error: ld returned 1 exit status`.
5. In `nm symbols.o` the never-defined function appears with type **`U`** and no address — the object file records the dependency without resolving it.
6. `nm symbols.o` lists only this translation unit's symbols, with `U` entries still outstanding. `nm symbols` (the linked executable) shows those symbols **resolved to addresses**, plus everything pulled in from libc and the startup files — a much longer listing (verified: 9 symbols in the object file against 36 in the executable). Linking despite the missing symbol requires `-Wl,--unresolved-symbols=ignore-all`. Note that the unresolved symbol is then **absent from the executable's symbol table altogether** — `nm symbols_ignored | grep undefined_function` returns nothing, it does *not* survive as a `U` entry — and the call site is left aimed at an unrelocated PLT stub, so invoking it dies with `SIGSEGV` (verified: exit status 139).

*Grading: 3 pts each for Q1–Q3 and Q5–Q6, 2 pts Q4 — **pasted evidence is required** for Q1, Q2, and Q4; an answer stating the letter without the `nm` line earns half.*
*The key insight to look for across the whole problem: the compiler is happy to emit an object file full of `U` symbols. Only the **linker** demands they all resolve. This is why "undefined reference" errors look and read so differently from compiler errors.*

### Makefile

*Grading is folded into the per-problem marks; a submission whose top-level `Makefile` does not build all five targets loses 2 points overall. Require `.PHONY` on `clean`/`test`/`all`, and the exact flag set `-Wall -Wextra -Werror -g -std=c11`.*

---

*PROG 101 · Week 0 · Problem Set 0 · © CSE Department*
