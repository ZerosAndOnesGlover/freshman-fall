---
assessment: Lab 0
course: PROG 101
component: Labs
status: submitted
started: 2026-09-24
submitted: 2026-09-25
source: "LAB 0 Environment Setup.md"
---

# PROG 101 · Lab 0
## Lab Notebook: Environment Setup

**Student:** Adebayo Glover
**Completed:** Parts 1–7. Part 8 (optional exploration challenges) not attempted.
**Machine:** Ubuntu 24.04.5 LTS, x86_64

---

## Part 1: Install the Toolchain

I installed everything with `sudo apt install build-essential gdb valgrind git` and then checked each tool.

| Tool | Required | Installed | OK |
|---|---|---|---|
| `gcc --version` | 11.x or later | GCC 13.3.0 (Ubuntu 13.3.0-6ubuntu2~24.04.1) | ✅ |
| `gdb --version` | 12.x or later | GNU gdb 15.1 | ✅ |
| `make --version` | 4.x or later | GNU Make 4.3 | ✅ |
| `git --version` | 2.x or later | git 2.55.0 | ✅ |
| `valgrind --version` | 3.x | valgrind-3.22.0 | ✅ |

Every tool meets the minimum version, so no problems came up here.

---

## Part 2: Hello World, Stage by Stage

### Step 1: Source

`hello.c` is in `$PROG101/week0/` and matches the handout exactly:

```c
/* hello.c — Week 0, Lab 0 */
#include <stdio.h>

int main(void) {
    printf("Hello, world!\n");
    printf("I am a C programmer.\n");
    return 0;
}
```

### Step 2: Preprocessor (`gcc -E hello.c -o hello.i`)

```
$ wc -l hello.c hello.i
    8 hello.c
  821 hello.i
```

The 8-line source grows to **821 lines**, about 100 times bigger. Almost all of that is `stdio.h` and the
headers it includes: type definitions and `extern` declarations for functions like `printf`, `fopen` and
`__overflow`. My own code is only the last few lines:

```
811  # 983 "/usr/include/stdio.h" 3 4
812
813  # 3 "hello.c" 2
814
815
816  # 4 "hello.c"
817  int main(void) {
818      printf("Hello, world!\n");
819      printf("I am a C programmer.\n");
820      return 0;
821  }
```

**Checkpoint 1: What is the first line of YOUR code in `hello.i`? What line number is it at?**

> The first line of my code is `int main(void) {`, at **line 817** of `hello.i`.
>
> The preprocessor changed two things in my file. It deleted the comment on line 1, which is why the
> comment never appears in `hello.i`. It also replaced `#include <stdio.h>` on line 2 with the whole
> header. The lines that start with `#` are *linemarkers*. For example, `# 4 "hello.c"` on line 816 says
> that the next line is line 4 of `hello.c`. The compiler uses these markers so that its error messages
> point to lines in my file, not lines in `hello.i`.

### Step 3: Compiler (`gcc -S hello.i -o hello.s`)

This is the `main` function from `hello.s`. I left out the `.cfi_*` unwind directives:

```asm
    .section .rodata
.LC0:
    .string "Hello, world!"
.LC1:
    .string "I am a C programmer."
    .text
    .globl  main
main:
    endbr64
    pushq   %rbp                 # prologue: save caller's frame pointer
    movq    %rsp, %rbp           #           set up our own frame
    leaq    .LC0(%rip), %rax     # address of first string
    movq    %rax, %rdi           # → 1st argument register
    call    puts@PLT
    leaq    .LC1(%rip), %rax
    movq    %rax, %rdi
    call    puts@PLT
    movl    $0, %eax             # return 0;
    popq    %rbp                 # epilogue: restore frame pointer
    ret
```

**Checkpoint 2: What assembly instruction is generated for the `return 0;` statement?**

> **`movl $0, %eax`**. On x86-64 Linux (the System V ABI), a function returns an `int` in the `%eax`
> register, so the compiler loads 0 into `%eax`. After that, `popq %rbp` undoes the function's prologue
> and `ret` jumps back to the caller. The caller (the C runtime) then reads `%eax` and uses it as the
> process's exit status.

**Observation: there is no `call printf`.** The handout says to look for `call printf`, but the
assembly calls `puts@PLT` twice instead. GCC knows what `printf` does, because it treats it as a
*builtin*. If a `printf` call has a format string with no `%` conversions that ends in `\n`, GCC
replaces it with a call to `puts`, which does the same job faster. You can see this in the string
constants: `.LC0` is `"Hello, world!"` **without** the `\n`, because `puts` prints the newline itself.
GCC does this even with no optimisation flags. To check, I compiled with `-fno-builtin`, which turns
this off, and got `call printf@PLT` twice.

### Step 4: Assembler (`gcc -c hello.s -o hello.o`)

```
$ file hello.o
hello.o: ELF 64-bit LSB relocatable, x86-64, version 1 (SYSV), not stripped

$ ls -la hello.o
-rw-rw-r-- 1 adebayo-glover adebayo-glover 1584 Sep 24 17:03 hello.o

$ nm hello.o
0000000000000000 T main
                 U puts
```

The object file is 1,584 bytes. `file` calls it **relocatable**, not executable. The addresses in it
are not final yet. `main` is at offset `0` because it is the first thing in this file's text section.

**Checkpoint 3: What does the `U` before `printf` mean? Why is it U and not T?**

> Because of the substitution described under Step 3, the undefined symbol here is `puts`, not
> `printf`. The meaning is the same either way.
>
> **`U` means *undefined*.** My code calls this function, but `hello.o` does not contain its code.
> `hello.o` only has a placeholder, called a relocation, that says "the address of `puts` goes here".
> **`T`** means the symbol is *defined* in this file's text (code) section. `main` is `T` because its
> machine code is in `hello.o`.
>
> `puts` (and `printf`) is `U` because I never wrote it. It is defined in the C standard library,
> `libc`. The `#include <stdio.h>` line only gave the compiler a *declaration*, meaning the name and
> type, so the compiler could check my call. The definition comes later, from the **linker**. After
> linking, `nm hello` still shows `U puts@GLIBC_2.2.5`. This is because `hello` is dynamically linked:
> the linker records which `libc` version the symbol comes from, and the dynamic loader
> (`ld-linux-x86-64.so.2`) connects the call to the real `puts` in `libc.so.6` when the program starts.

### Step 5: Link (`gcc hello.o -o hello`)

```
$ ./hello
Hello, world!
I am a C programmer.
$ echo $?
0
```

The exit code is `0`, which matches the `movl $0, %eax` from Step 3.

### Step 6: Full pipeline in one command

```
$ gcc -Wall -Wextra -g -std=c11 -o hello_full hello.c
$ ./hello_full
Hello, world!
I am a C programmer.
```

Even with `-Wall -Wextra` turned on, there were no warnings. The output is the same as the output from
building one stage at a time. The two executables are different sizes, though:

| Binary | Size | `file` reports |
|---|---|---|
| `hello` (staged build) | 15,960 bytes | `dynamically linked … not stripped` |
| `hello_full` (one command) | 17,160 bytes | `dynamically linked … with debug_info, not stripped` |

The 1,200 extra bytes are the DWARF debug information that `-g` adds. GDB needs it to map machine
instructions back to lines of `hello.c` (Part 6). The code that runs is the same in both.

**Takeaway:** `gcc hello.c` runs four programs one after another: preprocessor → compiler →
assembler → linker. Each stage's output is the next stage's input:
`.c` → `.i` → `.s` → `.o` → executable.

---

## Part 3: Explore Assembly

```
$ gcc -S -O0 -fverbose-asm hello.c -o hello_O0.s
$ gcc -S -O2 -fverbose-asm hello.c -o hello_O2.s
$ wc -l hello_O0.s hello_O2.s
  59 hello_O0.s
  53 hello_O2.s
```

`diff` shows 32 changed lines. These are the two versions of `main`, side by side. I left out the
`.cfi_*` directives. The `#` comments come from `-fverbose-asm`:

| `-O0` (no optimisation) | `-O2` (optimised) |
|---|---|
| `endbr64` | `endbr64` |
| `pushq %rbp` | `subq $8, %rsp` |
| `movq %rsp, %rbp` | |
| `# hello.c:5: printf("Hello, world!\n");` | `# bits/stdio2.h:86: return __printf_chk (...)` |
| `leaq .LC0(%rip), %rax` | `leaq .LC0(%rip), %rdi` |
| `movq %rax, %rdi` | |
| `call puts@PLT` | `call puts@PLT` |
| `# hello.c:6: ...` | |
| `leaq .LC1(%rip), %rax` | `leaq .LC1(%rip), %rdi` |
| `movq %rax, %rdi` | |
| `call puts@PLT` | `call puts@PLT` |
| `# hello.c:7: return 0;` | `# hello.c:8: }` |
| `movl $0, %eax` | `xorl %eax, %eax` |
| `popq %rbp` | `addq $8, %rsp` |
| `ret` | `ret` |

**Checkpoint 4: List two differences you observe between the `-O0` and `-O2` assembly. What do you think the optimizer changed and why?**

> 1. **`return 0;` became `xorl %eax, %eax`, not `movl $0, %eax`.** Both instructions set `%eax` to
>    0, because any value XOR itself is 0. The `xor` version is 2 bytes of machine code (`31 c0`)
>    instead of 5 (`b8 00 00 00 00`), and CPUs treat it as a special "zero this register" instruction.
>    So the optimiser picked the smaller and faster way to get the same result.
>
> 2. **The frame pointer is gone.** At `-O0`, `main` saves `%rbp` and sets it up as a frame pointer
>    (`pushq %rbp` / `movq %rsp, %rbp` … `popq %rbp`). At `-O2`, that is replaced by
>    `subq $8, %rsp` … `addq $8, %rsp`. `main` has no local variables, so it doesn't need a frame
>    pointer, and `%rbp` becomes free for other uses. The stack still has to be adjusted by 8 bytes,
>    because the ABI requires `%rsp` to be a multiple of 16 when `call` runs. The return address that
>    was pushed on entry left it 8 bytes off.
>
> Other differences I noticed:
>
> - **No temporary register.** `-O0` loads each string address into `%rax` and then copies it to
>   `%rdi`. `-O2` loads it straight into `%rdi`. At `-O0`, GCC translates each statement on its own.
>   At `-O2`, it chooses registers for the whole function at once.
> - **Different sections.** At `-O2`, `main` goes into `.text.startup` and is aligned to 16 bytes
>   (`.p2align 4`). The strings go into `.rodata.str1.1` with flags `"aMS"`, which lets the linker
>   merge identical strings from different files.
> - **The source-line comments change.** At `-O0`, every C line (5, 6, 7) has its own comment above
>   its instructions. At `-O2`, lines 5–7 are no longer labelled separately. The first `call` is
>   attributed to `stdio2.h` (`__printf_chk`), because Ubuntu's GCC turns on `_FORTIFY_SOURCE`
>   when optimising, and that swaps `printf` for a checked wrapper. GCC then simplifies the wrapper
>   back to `puts`.
>
> **Why:** `-O0` is meant for compiling quickly and debugging easily. Each statement becomes its own
> separate block of instructions, so a debugger can step through the program line by line. `-O2` is
> meant to make the program itself fast and small. It removes work that isn't needed, keeps values in
> registers, and aligns code. The downside is that instructions no longer match source lines one to
> one, and that's why we debug with `-O0 -g`.

---

## Part 4: My First Makefile

`Makefile` in `$PROG101/week0/`. `cat -A` confirms the recipe lines start with a real TAB (`^I`):

```makefile
CC = gcc
CFLAGS = -Wall -Wextra -Werror -g -std=c11

all: hello temperature

hello: hello.c
	$(CC) $(CFLAGS) -o $@ $<

temperature: temperature.c
	$(CC) $(CFLAGS) -o $@ $<

clean:
	rm -f hello temperature *.o *.i *.s

.PHONY: all clean
```

(My own file also has a comment above each section.) In each recipe, `$@` is the target name and `$<`
is the first prerequisite. So `hello: hello.c` runs `gcc … -o hello hello.c`.

```
$ make
gcc -Wall -Wextra -Werror -g -std=c11 -o hello hello.c
gcc -Wall -Wextra -Werror -g -std=c11 -o temperature temperature.c
$ ./hello
Hello, world!
I am a C programmer.
$ make clean
rm -f hello temperature *.o *.i *.s
$ make hello
gcc -Wall -Wextra -Werror -g -std=c11 -o hello hello.c
$ touch hello.c
$ make
gcc -Wall -Wextra -Werror -g -std=c11 -o hello hello.c
gcc -Wall -Wextra -Werror -g -std=c11 -o temperature temperature.c
```

**The handout's sequence doesn't quite show what it says.** It says that after `touch hello.c`,
`make` recompiles only `hello`. But `make` also built `temperature` here. That's because
`make clean` had deleted `temperature` and `make hello` never rebuilt it. It had to be built
because it was *missing*, not because it was out of date. I ran one more test with both programs
already built:

```
$ touch temperature.c
$ make
gcc -Wall -Wextra -Werror -g -std=c11 -o temperature temperature.c
```

This time Make rebuilt only `temperature`, and `hello` was left alone. This is the incremental
rebuild the handout is describing.

`make clean` also deleted the `hello.i`, `hello.s` and `hello.o` from Part 2, because the recipe
removes `*.o *.i *.s`. It's safe, because all of those can be regenerated from `hello.c`.

**Checkpoint 5: Run `make` twice without changing any file. What does Make print the second time? Why?**

> ```
> $ make
> make: Nothing to be done for 'all'.
> ```
>
> Make decides what to rebuild by comparing **modification times**. It rebuilds a target only if the
> target file is missing, or if one of its prerequisites is newer than it. After the first `make`,
> `hello` is newer than `hello.c` and `temperature` is newer than `temperature.c`, so neither rule
> needs to run. `all` is marked `.PHONY`, so Make always checks it, but checking `all` only means
> checking its two prerequisites, and both are up to date. If I ask for one target directly, I get a
> similar message: `make temperature` prints `make: 'temperature' is up to date.` This is why Make
> saves time on large projects: it only recompiles files whose sources changed.

---

## Part 5: temperature.c

My `temperature.c` is the handout version with two formatting changes. I added a blank line before
the prompt, and I put the result on its own line, indented with tabs:

```c
/* temperature.c — temperature converter */
#include <stdio.h>

double celsius_to_fahrenheit(double celsius);

int main(void) {
    double c;

    printf("\nEnter temperature in Celsius: ");
    if (scanf("%lf", &c) != 1) {
        fprintf(stderr, "Error: invalid input\n");
        return 1;
    }

    printf("\n\t\t\t %.1f°C = %.1f°F\n", c, celsius_to_fahrenheit(c));
    return 0;
}

double celsius_to_fahrenheit(double celsius) {
    return (celsius * 9.0 / 5.0) + 32.0;
}
```

The line `double celsius_to_fahrenheit(double celsius);` above `main` is a *prototype*. `main` calls
the function before its definition appears, so without the prototype the compiler wouldn't know
the function's parameter and return types at that point. The file compiles with
`-Wall -Wextra -Werror` and produces no warnings.

### Tests

```
$ echo "100" | ./temperature

Enter temperature in Celsius: 
			 100.0°C = 212.0°F
```

| Input | Expected (handout) | My program printed | Exit code | Pass |
|---|---|---|---|---|
| `100` | `100.0°C = 212.0°F` | `100.0°C = 212.0°F` | 0 | ✅ |
| `0` | `0.0°C = 32.0°F` | `0.0°C = 32.0°F` | 0 | ✅ |
| `-40` | `-40.0°C = -40.0°F` | `-40.0°C = -40.0°F` | 0 | ✅ |
| `37` *(extra)* | `98.6°F` (body temperature) | `37.0°C = 98.6°F` | 0 | ✅ |
| `abc` *(extra)* | error message | `Error: invalid input` | 1 | ✅ |

All three required cases give the correct values. The output is laid out differently from the
handout's lines only because of the extra `\n` and tabs I added.

**Invalid input.** `scanf` returns how many values it successfully read. For `abc` it returns 0, so
the program writes the error to `stderr` and exits with status 1 instead of printing a nonsense
conversion. The terminal showed:

```
$ echo "abc" | ./temperature

Error: invalid input
Enter temperature in Celsius: 
```

The error line appears *before* the prompt, even though the code prints the prompt first. When
`stdout` is a terminal it is *line-buffered*: output is held in memory until a `\n` is written. The
`\n` at the start of the prompt pushes out the blank line straight away, but
`Enter temperature in Celsius: ` has no newline after it, so it stays in the buffer until the program
exits. `stderr` is unbuffered, so the error is written immediately. In normal use this doesn't come
up, because reading from the keyboard makes glibc flush `stdout` first, so the prompt is visible
before you type.

### TA check

```
$ make clean && make && ./hello && ./temperature <<< "100"
rm -f hello temperature *.o *.i *.s
gcc -Wall -Wextra -Werror -g -std=c11 -o hello hello.c
gcc -Wall -Wextra -Werror -g -std=c11 -o temperature temperature.c
Hello, world!
I am a C programmer.

Enter temperature in Celsius: 
			 100.0°C = 212.0°F
```

---

## Part 6: My First GDB Session

I copied `buggy.c` from the lab's `starter/` folder into `$PROG101/week0/`.

My first copy didn't compile. The linker reported `undefined reference to 'add_three'`, because the
copy was missing the last three lines: the *definition* of `add_three`. The prototype on line 16 was
enough for the compiler to accept the call, but the linker then had no code to connect it to. This
is the same `U` (undefined symbol) idea as Checkpoint 3. The only difference is that this time no
library supplies the symbol. I restored the missing lines, and after that my copy matched the starter
byte for byte (`diff` printed nothing).

### Let the compiler find it

```
$ gcc -Wall -g -std=c11 -o buggy buggy.c
buggy.c: In function ‘main’:
buggy.c:24:11: warning: ‘total’ is used uninitialized [-Wuninitialized]
   24 |     total = total + add_three(a, b, c);
      |     ~~~~~~^~~~~~~~~~~~~~~~~~~~~~~~~~~~
buggy.c:19:9: note: ‘total’ was declared here
   19 |     int total;
      |         ^~~~~
```

The warning is on **line 24**, and the variable is **`total`**, which is declared on line 19. "Used
uninitialized" means the program *reads* `total`, on the right-hand side of `=`, before anything has
been *written* to it. C does not set local variables to zero automatically. The compiler still
produced a program, because this is only a warning and not an error.

```
$ ./buggy                 $ ./buggy                 $ ./buggy
Total:    32825           Total:    32824           Total:    32826
Expected: 60              Expected: 60              Expected: 60
```

`Total` is wrong, and it is **different on every run**.

### Watch it in GDB

```
$ gdb ./buggy
(gdb) break 24
Breakpoint 1 at 0x116a: file buggy.c, line 24.
(gdb) run
Breakpoint 1, main () at buggy.c:24
24	    total = total + add_three(a, b, c);
(gdb) print total
$1 = 32767
(gdb) print a
$2 = 10
(gdb) next
26	    printf("Total:    %d\n", total);
(gdb) print total
$3 = 32827
(gdb) continue
Total:    32827
Expected: 60
[Inferior 1 (process …) exited normally]
```

Before line 24 runs, `a` already holds 10, because `int a = 10;` has run. `total` holds **32767**,
a value my program never assigned. After `next`, `total` is 32767 + 60 = 32827, so `add_three`
worked correctly and the only problem is the starting value.

I looked at the value more closely:

```
(gdb) print &total
$1 = (int *) 0x7fffffffd18c
(gdb) print/x total
$2 = 0x7fff
```

32767 is `0x7fff`. That is the upper half of a 64-bit stack address like `0x00007fff…`. The 4 bytes
that `total` occupies are a stack slot that still contains part of an address left there by code
that ran before `main`, probably the C runtime's start-up code. When a function is called, its local
variables get whatever bytes are already in that part of the stack.

This also explains why the value is **the same every time under GDB, but changes outside it**. GDB
turns off address-space layout randomisation (ASLR), so the stack is always at `0x7fff…`. In normal
runs, Linux moves the stack to a random place. The top half of the stack address then comes out as
`0x7ffc`–`0x7ffe` (32764–32766), and adding 60 gives the 32824–32826 I saw. To check, I ran it with
ASLR turned off (`setarch -R ./buggy`), and it printed `Total: 32827` every time, the same as in
GDB.

### Fix

I changed `int total;` to `int total = 0;`. I also added `int d = a + b + c;` so the expected value
is calculated from the same variables instead of repeating the literals `10 + 20 + 30`. The comment
block at the top of `buggy.c` now describes the bug and the fix. It is longer than before, so in my
file the statement GDB stopped at is now line 36 rather than 24.

```
$ gcc -Wall -g -std=c11 -o buggy buggy.c
$ ./buggy
Total:    60
Expected: 60
```

The warning is gone, and it's also clean with `-Wextra` added. The output is 60.

**Checkpoint 6: What value did `total` hold before line 24 ran? Was it the same on every run? What does that tell you about a local variable that is never given a value?**

> Under GDB, `total` held **32767** (`0x7fff`) before line 24 ran. It was **not** the same from run
> to run in general. Normal runs printed 32824, 32825 and 32826, which means the starting value was
> 32764–32766. The value was stable only under GDB, because GDB turns off ASLR.
>
> This shows that a local variable which is never given a value starts with **whatever bytes are
> already in its memory**. In this case that was part of a stack address left behind by earlier
> code. The C standard calls this an *indeterminate value*, and reading it is undefined behaviour.
> The program can give different results on different runs, on different machines, or with
> different compiler flags. It can even seem correct by luck. The fix is to always initialise local
> variables, and to compile with `-Wall` so the compiler points out the ones I miss.

---

## Part 7: Git Repository

- **Repository:** the repository already existed. It is the Fall submissions repo, rooted at
  `Year1 Freshman/Fall/`, and it holds all six courses, with a GitHub remote. So I skipped
  `git init`.
- **Identity:** I set `user.name` and `user.email` for this repo, using my IST email address.
- **`.gitignore`:** I did **not** run the handout's `cat > .gitignore << 'EOF'` block. In `$FALL1` it
  would overwrite the semester-root `.gitignore`, which has the OS, editor and Obsidian rules. The
  course folder already has its own `.gitignore` that ignores everything except `*.c`, `*.h`,
  `Makefile`, `*.sh` and `*.md`. That covers everything the handout's version lists (`a.out`, `*.o`,
  `*.i`, `*.s`, `hello`, `temperature`, `buggy`) and also catches `hello_full`. `git status --ignored`
  confirmed that none of the build output was going to be committed.
- **Commit:** I committed `hello.c`, `temperature.c`, `buggy.c`, `Makefile` and this notebook in one
  commit, `PROG 101: Lab 0 environment setup (Week 0)`, and pushed it to `origin/main`.
- **Not done yet:** the `ACADEMICS` / `FALL1` / `PROG101` exports in `~/.bashrc` (Part 2 Step 1 and
  Part 7).

---

## Lab Deliverables

- [x] All tools installed and verified (`gcc`, `gdb`, `make`, `git`) — Part 1
- [x] `hello.c` compiles and runs correctly — Part 2
- [x] `temperature.c` passes all three test cases — Part 5
- [x] `buggy.c` bug found, fixed, and documented with a comment — Part 6
- [x] `Makefile` working (builds and cleans) — Part 4
- [x] Git repository initialized with first commit — Part 7
- [x] Answers to all Checkpoint Questions — summary below

---

## Checkpoint Answers (summary)

1. **First line of my code in `hello.i`:** `int main(void) {` at line 817 of 821.
2. **Assembly for `return 0;`:** `movl $0, %eax`, followed by `popq %rbp` / `ret`.
3. **Meaning of `U` in `nm`:** the symbol is used but not defined in this object file. It is
   defined in `libc` and resolved by the linker and the dynamic loader. GCC changed `printf` to
   `puts` here, so the symbol shown is `U puts`.
4. **Two differences between `-O0` and `-O2`:** (a) `return 0;` becomes `xorl %eax, %eax`
   instead of `movl $0, %eax`, which is a smaller way to set the register to zero; (b) the
   frame-pointer setup (`push`/`mov`/`pop %rbp`) is replaced by a single 8-byte stack adjustment
   that keeps the stack aligned for `call`. The optimiser removes work that isn't needed and picks
   cheaper instructions, but the instructions no longer map one to one onto source lines.
5. **Make on the second run:** `make: Nothing to be done for 'all'.` Both targets are newer than
   their source files (Make compares modification times), so no recipe needs to run.
6. **`total` before line 24:** 32767 (`0x7fff`) under GDB. It is not the same on every run:
   normal runs printed 32824–32826, and GDB is stable only because it turns off ASLR. A local
   variable that is never given a value holds whatever bytes were already in its memory (here,
   part of a leftover stack address). Reading it is undefined behaviour, so always initialise.
