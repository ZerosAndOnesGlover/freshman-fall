# PROG 101 · Programming I: Structured Programming in C
## Week 0 · Problem Set 0

**Released:** Friday 25 September 2026, 17:00 · Week 0
**Due:** Tuesday 29 September 2026, 10:00 (start of Week 1, Lecture 1) — Lab 0 on Monday 28 September comes first
**Submission:** Commit to the Freshman Fall repo under `"$PROG101/week0/ps0"`; submit the commit hash on the course portal.
**Collaboration policy:** Discussion of concepts allowed; code must be written independently.
**Grading:** Each problem is graded on correctness (70%), code quality (20%), and documentation (10%).
**Expected time:** about 3 hours

> **Revision note (2026-09-26).** Cut to about three hours. Problem 6 (symbols) repeated Problem 3.3's `nm`
> work and asked for a `char *` global, but pointers are Week 5; it was removed, with 3.5. The answer key
> moved out of this handout.

---

> **Revision note (2026-08-16).** Problems 1, 3, 4 and 5 were rebuilt to draw only on Week 0
> material. The previous versions required loops (Week 2), arrays (Week 4), pointers (Week 5),
> `malloc`/`free` (Week 6), recursion (Week 9) and macro-expansion semantics (Week 10) — 65 of
> 100 points tested content from later in the course. See [[Year1 - Freshman/PREREQUISITE AUDIT|PREREQUISITE AUDIT]].
> The removed problems were good problems in the wrong week; they are preserved with their
> verified answer keys in [[_RELOCATED Problems]] for re-filing under Weeks 6, 9 and 10.
> **Problems 2 and 6 are unchanged**, as are their answer keys and the errata table below.

**Scope of this set.** Everything here is answerable from Lecture 01 (Compilation Model),
Lecture 02 (Toolchain, Make, GDB), Lecture 03 (Hello World Deep-Dive) and Lab 0.

**One forward reference, deliberately scoped.** Problem 5 asks you to write a short
multi-file program, so you will define a function or two. Use them exactly as Lecture 02 does
in its `main.c` / `utils.c` / `utils.h` example — a return type, a name, parameters, a body.
Calling conventions, pass-by-value semantics and prototypes are **Week 3**; you do not need them
here and will not be assessed on them.

---

## Setup

All your work this week goes in `$PROG101/week0/ps0/`.

```bash
mkdir -p "$PROG101/week0/ps0"
cd "$PROG101/week0/ps0"
```

Each problem should be in its own file. Submit a `Makefile` that builds all of them.

---

## Problem 1: Preprocessor Investigation (12 pts)

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
4. *(3 pts)* Add `#define GREETING "Hello, world"` to `hello.c` and use it in your `printf`.
   Re-run the preprocessor. Search `hello.i` for the string `GREETING`. What do you find, and what
   does that tell you about when `#define` is resolved?
5. *(3 pts)* `hello.i` contains printf's **declaration** but not its **code**. Explain why, and name
   the pipeline stage at which printf's actual machine code joins your program.

---

## Problem 2: Personal Info Printer (18 pts)

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

## Problem 3: The Remaining Three Stages, By Hand (22 pts)

Problem 1 stopped after preprocessing. Now drive the other three stages yourself, one command at a
time — no all-in-one `gcc hello.c -o hello` until the very end.

```bash
gcc -S hello.i -o hello.s      # compile:  C  → assembly
gcc -c hello.s -o hello.o      # assemble: asm → object
gcc    hello.o -o hello        # link:     object → executable
```

Record your findings in `stages_report.md`.

**3.1** *(5 pts)* Tabulate all four artefacts — `hello.i`, `hello.s`, `hello.o`, `hello` — with the
byte size of each (`wc -c`). Which stage causes the largest *increase* in size, and why?

**3.2** *(6 pts)* Open `hello.s`. Find and paste:
- the instruction that calls `printf`
- the line where your string literal is stored, and the section directive above it

Explain what that section is for and why the string is not stored alongside the instructions.

**3.3** *(6 pts)* Run `nm hello.o`. What letter is `printf` given, and what does it mean? Now run
`nm hello`. What has changed about `printf`, and which stage changed it?

**3.4** *(5 pts)* `hello` is far larger than `hello.o`. Account for the difference concretely —
name at least two categories of content present in the executable but absent from the object file.

---

## Problem 4: The Compilation Error Hunt (20 pts)

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

## Problem 5: Make and the Incremental Rebuild (28 pts)

Build a three-file project:

- `greet.h` — declares one function
- `greet.c` — defines it; it prints a greeting
- `main.c` — includes `greet.h` and calls it

**5.1** *(8 pts)* Write a `Makefile` that builds `greet` from `main.o` and `greet.o`, using the
automatic variables `$@`, `$<` and `$^` — at least one of each. Include `.PHONY` and a `clean`
target. Use `-Wall -Wextra -Werror -g -std=c11`.

**5.2** *(7 pts)* Demonstrate the timestamp model. Run `make`, then in `make_report.md` record what
rebuilds after each of these, and why:
- `touch main.c`
- `touch greet.c`
- `touch greet.h`
- `make` twice in a row with no edits

**5.3** *(7 pts)* Now deliberately **omit** `greet.h` from the prerequisite lists. Change the
declaration in `greet.h` (add a parameter), rebuild, and describe exactly what goes wrong. Why is
this failure mode worse than a compile error? Restore the prerequisite afterwards.

**5.4** *(6 pts)* Introduce a `Makefile` whose recipe line is indented with **spaces** rather than a
tab. Paste the exact error. Explain why this error is so common and what makes it hard to see.

---

## Makefile Requirement

Your top-level `Makefile` must:
- Build all programs: `info`, `hello`, `fixed`, `greet`
- Include a `clean` target
- Use `-Wall -Wextra -Werror -g -std=c11` flags
- Have a `test` target that runs quick sanity checks

```makefile
.PHONY: all clean test

all: info hello fixed greet

test: all
	@echo "Testing info..."
	./info
	@echo "Testing greet..."
	./greet
	@echo "All tests passed."

clean:
	rm -f info hello fixed greet *.o *.i *.s
```

---

## Submission

```bash
cd "$PROG101/week0/ps0"
git add .
git commit -m "PS0: complete — all 5 problems"
git log --oneline -1    # Copy this commit hash for submission
```

Submit on the course portal:
- Your commit hash
- A brief reflection (2-3 sentences): what was the most surprising thing you learned this week?

---

## Grading Rubric

| Problem | Points | Key Criteria |
|---------|--------|-------------|
| P1: Preprocessor Investigation | 12 | Evidence cited from own `hello.i`, not recollection |
| P2: Info Printer | 18 | Exact formatting, `#define` used |
| P3: Three Stages By Hand | 22 | Each stage driven separately, assembly read correctly |
| P4: Error Hunt | 20 | All 10 errors found, categories correct, linker case identified |
| P5: Make and Incremental Rebuild | 28 | Automatic variables used, stale-header hazard demonstrated |
| **Total** | **100** | |

**Late policy:** 10% deducted per day late. No submissions accepted after 5 days.

---

*PROG 101 · Week 0 · Problem Set 0 · Due Tuesday 29 September 2026, 10:00 · © CSE Department*
