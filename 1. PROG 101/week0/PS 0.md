---
assessment: PS 0
course: PROG 101
component: Problem Sets
possible: 100
score: 100
status: graded
started: 2026-09-26
submitted: 2026-09-28
graded: 2026-09-30
source: "Problem Set 0.md"
---

# PROG 101 · PS 0
## Answer Sheet

**Assessment:** `Problem Set 0.md`
**Points available:** 100

Code and written reports live in `1. PROG 101/week0/ps0/`:
`hello.c`, `info.c`, `broken.c`, `fixed.c`, `greet.h`/`greet.c`/`main.c`, `Makefile`,
`preprocessor_report.md`, `stages_report.md`, `error_log.md`, `make_report.md`.

Toolchain used throughout: `gcc 15.2.0`, GNU Make 4.4.1, GNU binutils 2.46, x86-64 Linux.

---

### Problem 1 — Preprocessor Investigation  (12 points)

Full evidence in `preprocessor_report.md`.

1. **Line counts.** `hello.c` is **15** lines; `hello.i` is **853** lines — a ratio of about **57:1**.
2. **`printf`'s declaration** is at `hello.i:498`:
   `extern int printf (const char *__restrict __format, ...);`, reached via **`/usr/include/stdio.h`**
   (linemarker `# 341 "/usr/include/stdio.h"` at line 468).
3. **Linemarkers** (`# 1 "..."`) record the original file and line the following text came from, so a
   diagnostic can say `/usr/include/stdio.h:341` instead of `hello.i:498`. Without them, every message
   would cite a position in the expanded file the programmer never wrote.
4. **`#define GREETING`** — searching `hello.i` for `GREETING` finds **0** occurrences; the *string*
   `"Hello, world"` appears instead (at line 850). So `#define` is resolved by the preprocessor before
   the compiler runs; the compiler never sees the macro name.
5. `hello.i` has printf's **declaration** but not its **code**. Headers declare (so calls can be
   type-checked); the machine code is in libc and is attached at the **link** stage.

*Marks: 12 / 12*

---

### Problem 2 — Personal Info Printer  (18 points)

`info.c` uses `#define` for `NAME`, `ID`, `YEAR` and `COURSE`, and prints the card with width
specifiers (`%-38s`, `%-38d`) so the alignment is automatic. It compiles clean under
`-Wall -Wextra -Werror`, and **every output line is exactly 52 characters** (verified by counting
characters, not bytes):

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

*Marks: 18 / 18*

---

### Problem 3 — The Remaining Three Stages  (22 points)

Full answers in `stages_report.md`.

**3.1 Artefact sizes** (`wc -c`): `hello.c` 346 · `hello.i` 21 492 · `hello.s` 833 · `hello.o` 1 656 ·
`hello` 15 992. Largest **relative** increase: preprocessing (≈62×). Largest **absolute** increase:
linking (`hello.o` → `hello`, +14 336 B). Instructive point: `hello.s` is *smaller* than `hello.i`
because most of a header is declarations that generate no code.

**3.2** The string is under `.section .rodata` as `.LC0: .string "Hello, world"` (lines 3–5). The call
goes through the PLT: `call printf@PLT` and `call puts@PLT` (gcc rewrote the format-less second
`printf` into `puts`). `.rodata` is read-only, non-executable data, kept apart from the executable
`.text` so the two regions get different page permissions — a stray write to the string faults instead
of corrupting memory.

**3.3** In `hello.o`, `printf` is **`U`** (undefined — referenced, not supplied). In the linked `hello`
it is still `U` but now **versioned** `printf@GLIBC_2.2.5` with a matching **PLT stub** (`printf@plt`)
that the call routes through. The **link** stage made that change.

**3.4** `hello` is ~10× `hello.o` because linking attaches content absent from a relocatable object:
the **C runtime startup objects** (`crt1.o`/`crti.o`/`crtn.o`, defining `_start` that calls `main`),
the **dynamic-linking machinery** (`PT_INTERP`, PLT/GOT, relocations), and ELF program headers and
extra sections (`.init`, `.fini`, `.plt`, `.got`).

*Marks: 22 / 22*

---

### Problem 4 — The Compilation Error Hunt  (20 points)

Full log in `error_log.md`; corrected file is `fixed.c` (compiles clean under
`-Wall -Wextra -Werror -std=c11`).

| # | Line | Problem | Category | Fix |
|---|---|---|---|---|
| 1 | 1 | `#include <stdio.h` missing `>` | Preprocessor | `#include <stdio.h>` |
| 2 | 2 | `#include "helpers.h"` — file absent | Preprocessor | remove it |
| 3 | 8 | `void main(void)` | Compiler | `int main(void)` |
| 4 | 9 | `int status = 3` missing `;` | Compiler (syntax) | add `;` |
| 5 | 12 | `"Version: %d\n" VERSION` missing comma | Compiler (syntax) | add `,` |
| 6 | 13 | `%d` for a `double` | Undefined behavior | `%f` |
| 7 | 14 | `%s` for an `int` | Undefined behavior | `%d` |
| 8 | 17 | `summarise` never declared/defined | **Linker** | declare + define it |
| 9 | 19 | `return 1;` in a `void` function | Compiler | make `main` return `int` |
| 10 | 23/25 | missing `;`; `if (code = 3)` assignment | Compiler / logic | add `;`; `code == 3` |

**Only the linker finds Error 8.** With a prototype but no definition, `gcc -c` succeeds and
`nm` shows `U summarise`; only `gcc w5.o -o w5` reports `undefined reference to 'summarise'`. C lets
you call a function no file defines (it cannot see the whole program); the linker can.

*Marks: 20 / 20*

---

### Problem 5 — Make and the Incremental Rebuild  (28 points)

Full log in `make_report.md`. The single top-level `Makefile` builds `info`, `hello`, `fixed`, `greet`,
uses `$@`, `$<`, `$^`, `.PHONY` (on `all`/`clean`/`test`) and a `clean` target, with
`-Wall -Wextra -Werror -g -std=c11`.

**5.2 Timestamp model:** `touch main.c` → rebuilds only `main.o` then relinks; `touch greet.c` →
only `greet.o` then relinks; `touch greet.h` → rebuilds **both** objects then relinks (both list it as
a prerequisite); `make` twice → `Nothing to be done for 'all'.`

**5.3 Stale-header hazard:** with `greet.h` dropped from the prerequisites, changing `greet.h` to
`void greet(int times)` and `greet.c` to match (but leaving `main.c` alone) rebuilt **only `greet.o`**,
left `main.o` stale, **linked with no diagnostic**, and ran printing `Hello 0` — the callee read
whatever happened to be in the argument register (nondeterministic). This is worse than a compile
error: `-Wall -Wextra -Werror` cannot see it, because each translation unit is internally consistent
and the disagreement is only *between* them.

**5.4 Tabs:** a space-indented recipe gives `Makefile.spaces:2: *** missing separator.  Stop.` Recipes
must begin with a real tab. It is common because editors silently expand tabs to spaces, and hard to
see because a tab and spaces look identical (`cat -A` shows `^I`).

*Marks: 28 / 28*

---

## Reflection

The most surprising thing was how much happens before `main` even runs. A 15-line `hello.c` becomes
an 853-line `hello.i`, and most of that vanishes again into 833 bytes of assembly because a header is
almost all declarations. The other surprise was the stale-header hazard in 5.3: the build compiled
clean, linked clean, and *still* produced a wrong program — I had assumed a clean `-Werror` build
meant the program was correct.

---

## Grading Summary

| | |
|---|---|
| **Score** | 100 / 100 |
| **Percent** | 100% |
| **Graded** | 2026-09-30 |

**Feedback:**
All five problems complete and verified with real tool output. Problem 1 cites its own `hello.i`
(line numbers and excerpts, including the 0 hits for `GREETING`). `info.c` reproduces the 52-column
card exactly and compiles clean with `-Werror`; `fixed.c` is correct and the ten errors are all
located, categorised, and fixed, with the linker-only case (`summarise`) correctly singled out.
Problem 3 drives each stage separately and reads `.rodata`/PLT correctly. `make_report.md` reproduces
the timestamp table, the stale-header demo, and the tab error. Clear, well-documented work.
