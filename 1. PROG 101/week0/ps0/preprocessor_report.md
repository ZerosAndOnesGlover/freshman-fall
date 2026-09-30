# PS 0 · Problem 1: Preprocessor Investigation

**Machine:** Ubuntu 24.04.5 LTS, x86_64, GCC 13.3.0
**Command:** `gcc -E hello.c -o hello.i`

Questions 1–3 use the Lab 0 `hello.c` (8 lines). Question 4 adds the `GREETING` macro, which is the
version of `hello.c` in this folder now. Adding the macro shifts everything after the header by two
lines, so each line number below says which version it comes from.

---

## 1.1 Line counts

```
$ wc -l hello.c hello.i
    8 hello.c
  821 hello.i
```

**8 lines → 821 lines, a ratio of about 1 : 103** (821 / 8 = 102.6). After adding `GREETING` it is
10 → 823.

My own code is only the last 5 lines of `hello.i`, from line 817 (`int main(void) {`) to line 821.
Everything before that came from `#include <stdio.h>`. `hello.i` has 118 linemarker lines, and they
name 27 different files: `hello.c`, `stdc-predef.h` (which GCC includes automatically), `stdio.h`,
and **24 more headers that `stdio.h` includes** (`features.h`, `bits/types.h`, `stddef.h`,
`stdarg.h`, …).

## 1.2 The declaration of `printf`

```
477: extern int printf (const char *__restrict __format, ...);
```

This is line **477** of `hello.i`. It is the same in both versions of `hello.c`, because the
`#define` comes after the `#include`. To find which header it came from, I looked for the nearest
linemarker above it:

```
447: # 334 "/usr/include/stdio.h" 3 4
```

This marker says that line 448 of `hello.i` is line 334 of `/usr/include/stdio.h`. So line 477 is
stdio.h line 334 + 29 = **363**. `grep -n "extern int printf" /usr/include/stdio.h` confirms it:
`363:extern int printf (const char *__restrict __format, ...);`.

So the declaration came from **`/usr/include/stdio.h`**, line 363. It's worth noting what the
declaration contains: a return type (`int`), a first parameter (the format string), and `...` (any
number of further arguments). There is no function body.

## 1.3 Linemarkers

A linemarker has the form `# <line> "<file>" <flags>`, for example `# 3 "hello.c" 2` on line 813. It
tells the compiler: *the next line of this file came from line `<line>` of `<file>`*. The flags
record how headers were entered and left. `1` means "entering an included file", and `2` means
"returning to the file that included it", so `# 3 "hello.c" 2` means "back in `hello.c` at line 3,
after the `#include`". `3` means "this is a system header", which is why GCC doesn't show warnings
from inside `stdio.h`.

**What they're for:** `hello.i` is one long file stitched together from 27 files. The markers let
the compiler track, at every point, which original file and line it is reading. **Without them,
every error message would point into `hello.i` instead of my source.** I tested this. I removed the
`;` after `return 0` and compiled the preprocessed output twice:

```
# with linemarkers (gcc -E)
err.c:7:13: error: expected ‘;’ before ‘}’ token

# without linemarkers (gcc -E -P)
without.i:308:13: error: expected ‘;’ before ‘}’ token
```

Without markers, the error points to line 308 of a temporary file I never wrote, not line 7 of my
source. GDB and debug info (`-g`) depend on the same mapping, so stepping through the program would
show `hello.i` lines too. GCC would also stop recognising system headers, so warnings from inside
`stdio.h` would start appearing.

## 1.4 `#define GREETING`

I added the macro and used it in the first `printf`:

```c
#define GREETING "Hello, world"

int main(void) {
    printf(GREETING "!\n");
```

```
$ gcc -E hello.c -o hello.i
$ grep -n GREETING hello.i
$ echo $?
1
$ grep -n "Hello, world" hello.i
820:    printf("Hello, world" "!\n");
```

**`GREETING` doesn't appear anywhere in `hello.i`.** `grep` finds nothing (exit status 1). The
`#define` line itself is gone too (`grep -c define hello.i` gives 0). On line 820, the macro name
has been replaced by its text, `"Hello, world"`, and the compiler later joins the two adjacent
string literals into `"Hello, world!\n"`.

This shows that **`#define` is resolved entirely during preprocessing, before compilation starts.**
It is text substitution: the compiler never sees the name `GREETING`, so a macro has no type, no
storage and no symbol. The program's output is unchanged (`Hello, world!`).

## 1.5 Declaration, but not code

`hello.i` contains only what `stdio.h` contains, and a header only contains **declarations**: names
and types, like line 477 above. It tells the compiler that a function called `printf` exists, what
it returns and what arguments it takes. That's enough for the compiler to check my calls and
generate code to call it. The **code** of `printf` is not in any header. It was compiled long ago
and is part of the C library, `libc` (`/lib/x86_64-linux-gnu/libc.so.6`).

The machine code joins my program at the **linking** stage (stage 4). The linker finds the
definition in libc and connects my call to it. My `hello` is dynamically linked, so the linker
doesn't copy `printf`'s code into the file. It records that the program needs the symbol from
`libc.so.6` (Problem 3.3 shows `U puts@GLIBC_2.2.5`). The dynamic loader then maps libc into memory
and fills in the address when the program starts.
