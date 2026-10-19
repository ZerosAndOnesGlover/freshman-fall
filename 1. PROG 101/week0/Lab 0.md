---
assessment: Lab 0
course: PROG 101
component: Labs
possible: 100
score: 100
status: graded
started: 2026-09-28
submitted: 2026-09-28
graded: 2026-09-28
source: "LAB 0 Environment Setup.md"
---

# PROG 101 · Lab 0
## Answer Sheet — Environment Setup

**Assessment:** `LAB 0 Environment Setup.md`
**Completion lab** (not graded; completion required before Problem Set 0).

Code lives in `1. PROG 101/week0/lab0/`: `hello.c`, `temperature.c`, `buggy.c` (fixed and
documented), `Makefile`.

**Toolchain verified:**

| Tool | Version |
|---|---|
| `gcc` | 15.2.0 (Ubuntu 15.2.0-16ubuntu1) |
| `gdb` | 17.1 |
| `make` | GNU Make 4.4.1 |
| `git` | 2.55.0 |
| `valgrind` | 3.26.0 |

---

## Part 2 — Hello World: Manual Pipeline

Ran each stage separately rather than the all-in-one command:

```bash
gcc -E hello.c -o hello.i     # preprocess
gcc -S hello.i -o hello.s     # compile  → assembly
gcc -c hello.s -o hello.o     # assemble → object
gcc    hello.o -o hello       # link     → executable
./hello
```

```
Hello, world!
I am a C programmer.
```

**Checkpoint 1 — first line of my code in `hello.i`, and its line number.**
`hello.c` is **8** lines; `hello.i` is **846** lines. The first line of *my* code in `hello.i` is

```c
842: int main(void) {
```

at **line 842**, immediately after the linemarker `# 4 "hello.c"` on line 841 (which says the next
line is line 4 of `hello.c`). Everything above it is the expanded contents of `<stdio.h>`.

**Checkpoint 3 — meaning of the `U` in `nm`.** `nm hello.o` shows:

```
0000000000000000 T main
                 U puts
```

`U` means **undefined**: the symbol is *referenced* by this translation unit but not *defined* here —
the **linker** must supply it from a library. `T` (next to `main`) means the symbol **is** defined, in
the text/code section.

*(Note: the handout expects `U printf`, but on this toolchain gcc rewrote both `printf("...\n")` calls
— they contain no format specifiers — into the cheaper `puts`, so the undefined symbol is `puts`. The
meaning of `U` is identical. For a `printf` that keeps its name, see `PS 0`'s `hello.i`.)*

---

## Part 3 — Explore Assembly

**Checkpoint 2 — the assembly for `return 0;`.** In `hello.s` (at `-O0`):

```asm
movl	$0, %eax        # the return value
popq	%rbp
ret
```

The value is placed in `%eax` (the return-value register) before `ret`. At `-O2` the same statement
becomes the shorter zeroing idiom `xorl %eax, %eax`.

```bash
gcc -S -O0 -fverbose-asm hello.c -o hello_O0.s    # 59 lines
gcc -S -O2 -fverbose-asm hello.c -o hello_O2.s    # 53 lines
```

**Checkpoint 4 — two differences between `-O0` and `-O2`:**

1. **The stack frame is dropped.** `-O0` opens with a full prologue — `pushq %rbp`, `movq %rsp, %rbp`,
   plus `.cfi_*` frame directives; `-O2` omits the frame pointer entirely (just `subq $8, %rsp`).
2. **Arguments and the return value are handled more directly.** `-O0` loads a temporary first
   (`leaq .LC0(%rip), %rax` then `movq %rax, %rdi`); `-O2` loads straight into the argument register
   (`leaq .LC0(%rip), %rdi`), and returns via `xorl %eax, %eax` instead of `movl $0, %eax`.

`-O2` also enables `-D_FORTIFY_SOURCE=3` and puts `main` in a `.text.startup` section. The point: the
assembly is a *product of the compiler's choices*, not a line-by-line transcription of the source.

---

## Part 4 — My First Makefile

`Makefile` builds `hello` and `temperature`, with a `clean` target, using `$@` and `$<`, and `.PHONY`.

**Checkpoint 5 — `make` twice.** The second run prints:

```
make: Nothing to be done for 'all'.
```

because every target is already **newer** than its prerequisites — nothing is out of date, so there is
no work to do.

---

## Part 5 — `temperature.c`

```bash
$ echo "100" | ./temperature
100.0°C = 212.0°F
$ echo "0"   | ./temperature
0.0°C = 32.0°F
$ echo "-40" | ./temperature
-40.0°C = -40.0°F
$ echo "37"  | ./temperature     # extra: the integer-division trap
37.0°C = 98.6°F
```

All three required cases pass. The conversion uses `celsius * 9.0 / 5.0` — floating-point literals —
so it does not truncate (the buggy `c * 9 / 5` form would give `98` for `37`).

---

## Part 6 — First GDB Session

Compiling the original buggy source with `-Wall -g`:

```
buggy_orig.c:24:11: warning: ‘total’ is used uninitialized [-Wuninitialized]
   24 |     total = total + add_three(a, b, c);
      |     ~~~~~~^~~~~~~~~~~~~~~~~~~~~~~~~~~~
buggy_orig.c:19:9: note: ‘total’ was declared here
   19 |     int total;
```

GDB session:

```
(gdb) break 24
(gdb) run
Breakpoint 1, main () at buggy_orig.c:24
24	    total = total + add_three(a, b, c);
(gdb) print total        → $1 = 0
(gdb) print a            → $2 = 10
(gdb) next
(gdb) print total        → $3 = 60
(gdb) continue
Total:    60
Expected: 60
```

**Checkpoint 6 — value of `total` before line 24, and what it means.** On this machine the slot held
**0**, so the result happened to come out right (`60`) — but that is luck, not correctness. A local
variable is *not* zero-initialised: it holds whatever bytes were left in that stack slot, so the value
is **undefined** and can differ between runs and machines. To make the garbage visible I rebuilt with
`-ftrivial-auto-var-init=pattern`, which fills the slot with a recognisable pattern:

```bash
$ gcc -g -ftrivial-auto-var-init=pattern -o buggy_pattern buggy_orig.c
$ ./buggy_pattern
Total:    -16842950
Expected: 60
```

**The fix** (`buggy.c`, documented in a comment): `int total = 0;` — initialise the accumulator so it
starts from a known value. The warning disappears and the output is `60`:

```
$ gcc -Wall -Wextra -Werror -g -std=c11 -o buggy buggy.c   # no warnings
$ ./buggy
Total:    60
Expected: 60
$ gcc -fsanitize=address,undefined ... && ./buggy          # clean
Total:    60
Expected: 60
```

---

## Part 7 — Git Repository

The six Freshman Fall courses share one repository rooted at the Fall submissions folder; PROG 101 is
`1. PROG 101/`. The week-0 work was committed with a `Week 0`-style message, and compiled binaries,
`*.o`, `*.i` and `*.s` are ignored.

---

## Part 8 — Exploration Challenges

**Challenge 1 — C++ file with the C compiler.** `gcc test.c` fails:

```
test.c:1:1: error: unknown type name ‘class’
```

but `gcc test.cpp` **compiles fine**. `gcc` is a *driver*: it chooses the language from the file
extension and runs the C++ compiler for `.cpp`. (A program using the C++ standard library would then
fail to link without `g++`, which adds `libstdc++`.)

**Challenge 2 — inspect the binary.** `file` reports
`ELF 64-bit LSB pie executable, x86-64 … dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2`;
`strings` finds `Hello, world!`; `readelf -h` shows the ELF header (magic `7f 45 4c 46`, class ELF64,
little-endian).

**Challenge 3 — printf in libc.**

```
$ nm -D /lib/x86_64-linux-gnu/libc.so.6 | grep -w printf
0000000000064080 T printf@@GLIBC_2.2.5
```

`T` = **defined** in the shared library — this is the definition the linker resolved `U printf` against.

---

## Lab Deliverables

- [x] Tools installed and verified (`gcc`, `gdb`, `make`, `git`, `valgrind`)
- [x] `hello.c` compiles and runs
- [x] `temperature.c` passes all three test cases
- [x] `buggy.c` bug found, fixed, and documented with a comment
- [x] `Makefile` builds and cleans
- [x] Git repository in use with the week-0 commit
- [x] All checkpoint answers recorded here

TA demonstration:

```
$ make clean && make && ./hello && ./temperature <<< "100"
Hello, world!
I am a C programmer.
Enter temperature in Celsius: 100.0°C = 212.0°F
```

---

## Grading Summary

| | |
|---|---|
| **Score** | 100 / 100 (completion) |
| **Percent** | 100% |
| **Graded** | 2026-09-28 |

**Feedback:**
Completion lab signed off. Every stage was driven manually and read correctly (`U puts` recognised as
undefined, with the `printf`→`puts` substitution explained). The `-O0`/`-O2` contrast names the dropped
frame pointer and the direct argument/return handling. `temperature.c` passes all three cases (and the
extra `37` check confirms floating-point division). The uninitialised-variable bug is found from the
compiler warning *and* in GDB, correctly diagnosed as undefined (not zero), demonstrated with the
pattern-init build, and fixed by initialising `total`. All three challenges completed.
