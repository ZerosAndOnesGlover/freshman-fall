# Preprocessor Report — Problem 1

**File:** `preprocessor_report.md`
**Course:** PROG 101, Week 0, Problem Set 0
**Toolchain:** `gcc (Ubuntu 15.2.0-16ubuntu1) 15.2.0`, x86-64 Linux

All evidence below is taken from the `hello.i` produced from my own `hello.c`
(`gcc -E hello.c -o hello.i`).

---

## 1.1 — Line counts and ratio

```
$ wc -l hello.c hello.i
15 hello.c
853 hello.i
```

`hello.c` is **15 lines**; `hello.i` is **853 lines**. The ratio is about **57:1** — a single
`#include <stdio.h>` expands to roughly 850 lines, almost all of it declarations pulled in
transitively by `stdio.h`. Preprocessing is therefore the largest *relative* expansion in the whole
pipeline.

---

## 1.2 — The declaration of `printf`

```
$ grep -n "extern int printf" hello.i
498:extern int printf (const char *__restrict __format, ...);
```

Pasted exactly with its line number:

```c
extern int printf (const char *__restrict __format, ...);
```

It sits under the linemarker `# 341 "/usr/include/stdio.h" 3 4` (at `hello.i:468`), so it ultimately
comes from **`/usr/include/stdio.h`** (the glibc header reached through `<stdio.h>`).

---

## 1.3 — Linemarkers

Lines beginning `# 1 "..."` are **linemarkers**. They tell the compiler which original file and
line the *following* text corresponds to. For example:

```
468: # 341 "/usr/include/stdio.h" 3 4
...
498: extern int printf (const char *__restrict __format, ...);
```

means "the text that follows was, in the source, line 341 of `/usr/include/stdio.h`". There are **117**
linemarkers in my `hello.i`.

If they were absent, the compiler would have nothing but the *expanded* file to point at, so a
diagnostic about the `printf` declaration would say `hello.i:498` instead of
`/usr/include/stdio.h:341`. Every error and warning would cite a position in a file the programmer
never wrote or sees.

---

## 1.4 — The `#define GREETING` test

After adding `#define GREETING "Hello, world"` and using it in the `printf`:

```
$ grep -c GREETING hello.i
0
$ grep -n '"Hello, world"' hello.i
850:    printf("%s!\n", "Hello, world");
```

Searching the preprocessed output for the macro **name** `GREETING` finds **nothing** (0 matches).
What appears in its place, at `hello.i:850`, is the **string it stands for**, `"Hello, world"`.

This tells me the macro is resolved by the **preprocessor**, *before* the compiler runs: the compiler
never sees the token `GREETING` at all. (`#define` is a text substitution performed during
preprocessing, not a feature the compiler knows about.)

---

## 1.5 — Declaration vs. definition

`hello.i` contains printf's **declaration** — `extern int printf (...)` — but not its **code**. A
header only *promises* the function's type (name, parameters, return type) so that calls can be
type-checked. The actual machine code for `printf` lives in the C standard library (glibc), already
compiled.

printf's machine code joins my program at the **link stage**: the compiler emits an *undefined*
reference to `printf` in `hello.o` (visible as `U printf` under `nm hello.o`), and the linker resolves
it by pulling in the libc definition and wiring up a PLT entry. **Headers declare; libraries define;
the linker attaches.**

---

*PROG 101 · Week 0 · Problem Set 0 · Problem 1*
