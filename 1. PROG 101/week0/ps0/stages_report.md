# Stages Report — Problem 3

**File:** `stages_report.md`
**Course:** PROG 101, Week 0, Problem Set 0
**Toolchain:** `gcc (Ubuntu 15.2.0-16ubuntu1) 15.2.0`, x86-64 Linux

Each stage was driven separately, starting from the `hello.i` produced in Problem 1:

```bash
gcc -S hello.i -o hello.s      # compile:  C   → assembly
gcc -c hello.s -o hello.o      # assemble: asm → object
gcc    hello.o -o hello        # link:     obj → executable
```

---

## 3.1 — Sizes of the four artefacts

```
$ wc -c hello.c hello.i hello.s hello.o hello
  346 hello.c
21492 hello.i
  833 hello.s
 1656 hello.o
15992 hello
```

| Artefact | Bytes | Note |
|---|---|---|
| `hello.c`   | 346     | my source |
| `hello.i`   | 21 492  | full expansion of `<stdio.h>` |
| `hello.s`   | 833     | assembly — every declaration that emitted no code is gone |
| `hello.o`   | 1 656   | binary encoding of the same instructions, plus a symbol table |
| `hello`     | 15 992  | startup files and dynamic-linking machinery attached |

**Which stage causes the largest increase?** It depends how you measure, and both answers are
defensible:

- **Relative to its input, preprocessing is the largest jump:** `hello.c` (346 B) becomes `hello.i`
  (21 492 B), about **62×**. One `#include` pulls in hundreds of lines of declarations.
- **In absolute bytes, linking is the largest jump:** `hello.o` (1 656 B) becomes `hello`
  (15 992 B), an increase of **14 336 bytes** as the runtime startup code and dynamic-linking
  machinery are attached.

The instructive detail is that **`hello.s` is smaller than `hello.i`**: most of `<stdio.h>` is
*declarations*, which generate no code, so compiling discards almost all of it.

---

## 3.2 — Reading `hello.s`

The string literal is stored in a read-only data section (lines 3–5 of `hello.s`):

```asm
	.section	.rodata
.LC0:
	.string	"Hello, world"
```

The call is made through the PLT (note gcc turned my second, format-less `printf` into `puts`):

```
30:	call	puts@PLT
27:	call	printf@PLT
```

Bare `printf("...\n")` with no format specifiers is rewritten by gcc into the cheaper `puts`, so both
appear: `printf@PLT` for the `"%s!\n"` call and `puts@PLT` for the plain-string call.

**Why is the string in `.rodata` and not alongside the instructions?** `.rodata` is **read-only data**.
It is mapped into the process *without write permission*, so a stray write through a string literal
faults (a `SIGSEGV`) instead of silently corrupting memory. The instructions live in `.text`, which is
**executable but not writable**; the string lives in `.rodata`, which is **readable but not
executable**. Separating them lets the two regions be given different page permissions — you cannot do
that if the data is interleaved with the code.

---

## 3.3 — `nm` before and after linking

```
$ nm hello.o
0000000000000000 T main
                 U printf
                 U puts
```

In the **object file**, `printf` is **`U`** — *undefined*: referenced by this translation unit but not
supplied by it, to be found elsewhere at link time. (It has no address.)

```
$ nm hello | grep -E "printf|puts"
                 U printf@GLIBC_2.2.5
                 U puts@GLIBC_2.2.5
```

In the **linked executable**, `printf` is still listed as `U`, but it is now **versioned**
(`printf@GLIBC_2.2.5`) and there is a matching **PLT stub** that the call is routed through:

```
$ objdump -d hello | grep "<printf@plt>"
0000000000001070 <printf@plt>:
    118a:  call  1070 <printf@plt>
```

The **link** stage changed this. The compiler left `printf` as a promise; the linker found which
library supplies it, recorded the required symbol version (`GLIBC_2.2.5`), and manufactured a PLT stub
so the call can be routed to libc at run time. The same happened for `puts`.

---

## 3.4 — Why `hello` is much larger than `hello.o`

`hello` (15 992 B) is roughly **ten times** `hello.o` (1 656 B). Content present in the executable but
absent from the relocatable object includes:

1. **C runtime startup objects** — `crt1.o`, `crti.o`, `crtn.o`. These define `_start`, the real entry
   point, which sets up the process and *calls `main`*. The object file has no `_start`; without it
   `ld` cannot even make a runnable program.
2. **Dynamic-linking machinery** — the `PT_INTERP` segment naming the dynamic linker
   (`/lib64/ld-linux-x86-64.so.2`), plus the PLT/GOT tables and the relocation entries that let
   `printf`/`puts` bind to libc addresses.
3. **ELF program headers and extra sections** — an executable needs loadable-segment program headers
   and sections (`.init`, `.fini`, `.plt`, `.got`) that a relocatable object simply does not have.

---

*PROG 101 · Week 0 · Problem Set 0 · Problem 3*
