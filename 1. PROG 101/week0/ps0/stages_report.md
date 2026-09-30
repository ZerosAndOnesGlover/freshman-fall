# PS 0 · Problem 3: The Remaining Three Stages, By Hand

**Machine:** Ubuntu 24.04.5 LTS, x86_64, GCC 13.3.0
**Source:** `hello.c` from Problem 1.4 (with `GREETING`). Each stage was run on its own:

```
$ gcc -E hello.c -o hello.i      # preprocess (Problem 1)
$ gcc -S hello.i -o hello.s      # compile:  C   -> assembly
$ gcc -c hello.s -o hello.o      # assemble: asm -> object
$ gcc    hello.o -o hello        # link:     object -> executable
$ ./hello
Hello, world!
I am a C programmer.
```

---

## 3.1 Sizes

```
$ wc -c hello.i hello.s hello.o hello
21360 hello.i
  761 hello.s
 1584 hello.o
15960 hello
```

| Stage | Artefact | Bytes | Change from previous |
|---|---|---|---|
| (source) | `hello.c` | 233 | — |
| Preprocess | `hello.i` | 21,360 | +21,127 (×92) |
| Compile | `hello.s` | 761 | −20,599 |
| Assemble | `hello.o` | 1,584 | +823 |
| Link | `hello` | 15,960 | **+14,376** |

**Of the three stages in this problem, linking causes the largest increase: +14,376 bytes, about
10× the object file.** The linker wraps my 168 bytes of code and data in a complete, loadable
program: start-up code, dynamic-linking tables, program headers and page-alignment padding. Problem
3.4 breaks this down.

(Preprocessing adds even more bytes overall, but that's Problem 1's stage. `hello.i` is text, and
it is almost all declarations from `stdio.h`. The compiler then shrinks it by 96%. Any declaration
that my code doesn't use produces no assembly, so the 761-byte `hello.s` only contains `main` and
its two strings.)

## 3.2 Reading `hello.s`

**The call.** There is no `call printf`. The two calls in `hello.s` are:

```asm
22:     call    puts@PLT
25:     call    puts@PLT
```

GCC treats `printf` as a *builtin* it understands. When the format string has no `%` conversions
and ends in `\n`, the call does exactly the same thing as `puts`, so GCC replaces it with the
simpler function, even at `-O0`. The string literals prove it: `.LC0` is `"Hello, world!"` with
**no** `\n`, because `puts` adds the newline itself. Compiling with `-fno-builtin` turns the calls
back into `call printf@PLT`. `@PLT` means the call goes through the *Procedure Linkage Table*, a
small stub the linker creates so that the real address in libc can be filled in when the program
runs.

**The strings and their section:**

```asm
 3:     .section .rodata
 4: .LC0:
 5:     .string "Hello, world!"
 6: .LC1:
 7:     .string "I am a C programmer."
 8:     .text
 9:     .globl  main
...
20:     leaq    .LC0(%rip), %rax
21:     movq    %rax, %rdi
22:     call    puts@PLT
```

`.section .rodata` is **read-only data**. Constants that must not change while the program runs go
here. My two string literals are there under the labels `.LC0` and `.LC1`. `.text` on line 8
switches back to the code section, and `leaq .LC0(%rip), %rax` on line 20 loads the string's
address so it can be passed to `puts` in `%rdi`.

**Why the string is kept apart from the instructions:**

- **Different permissions.** The loader maps `.text` as read + execute, and `.rodata` as read-only
  with no execute (`readelf -l hello` shows them in separate `LOAD` segments, flagged `R E` and
  `R`). Data should never be executable. If it were, bytes put into memory by an attacker could be
  run as code. Code should never be writable either. Keeping them in separate sections lets the
  operating system enforce both rules for each memory page.
- **Modifying a string literal is caught.** Writing to a string literal is undefined behaviour in C.
  Because `.rodata` is read-only, trying to do it crashes the program instead of silently changing
  a constant.
- **Instructions and data don't get mixed up.** The CPU never tries to execute the text of a
  string, and constants can be shared or merged. At `-O2`, GCC puts strings in
  `.rodata.str1.1` with the `M` (mergeable) flag, so the linker can store identical strings only
  once.

## 3.3 `nm` before and after linking

```
$ nm hello.o
0000000000000000 T main
                 U puts
```

The function is **`puts`**, not `printf`, because of the substitution in 3.2. It is marked **`U`,
undefined**: `hello.o` calls it but doesn't contain its code. The assembler only left a
*relocation*, a note saying "put the address of `puts` here". `main` is `T` (defined in the text
section) at offset 0, because it is the first and only function in the file, and its final address
isn't known yet.

```
$ nm hello
0000000000001149 T main
                 U puts@GLIBC_2.2.5
                 U __libc_start_main@GLIBC_2.34
0000000000001060 T _start
... (30 symbols in total, compared with 2 in hello.o)
```

Two things have changed, and the **linker** made both changes:

1. **`puts` is now `puts@GLIBC_2.2.5`.** The linker found the definition in `libc.so.6` and
   recorded exactly which library version the program needs. It is **still `U`**, because `hello`
   is dynamically linked, so libc's code is not copied in. The link is finished at run time by the
   dynamic loader (`/lib64/ld-linux-x86-64.so.2`, the program interpreter written into the file).
   I checked this with a static link (`gcc -static hello.o`), which does copy libc's code in. There,
   `nm` shows `T _IO_puts` and `W puts` (a weak alias to it) at a real address, `0x404d40`.
2. **`main` has a real address**, `0x1149` instead of `0`, because the linker has placed it within
   the complete program. It also added 28 new symbols. `_start` is the real entry point, and it
   calls `__libc_start_main`, which then calls my `main`.

## 3.4 Why `hello` is so much bigger than `hello.o`

`size` shows that the actual code and data grow from 168 bytes to 2,020. That's still nowhere near
15,960. The sections in each file:

```
hello.o: .text .rela.text .data .bss .rodata .comment .note.GNU-stack .note.gnu.property
         .eh_frame .rela.eh_frame .symtab .strtab .shstrtab                          (13)

hello:   .interp .note.gnu.property .note.gnu.build-id .note.ABI-tag .gnu.hash .dynsym
         .dynstr .gnu.version .gnu.version_r .rela.dyn .rela.plt .init .plt .plt.got
         .plt.sec .text .fini .rodata .eh_frame_hdr .eh_frame .init_array .fini_array
         .dynamic .got .data .bss .comment .symtab .strtab .shstrtab                   (30)
```

The executable contains four kinds of content that the object file doesn't have:

1. **Page-alignment padding, most of the difference.** A program is loaded into memory page by
   page, and a page is 4 KiB. The executable is split into four `LOAD` segments, which start at
   file offsets `0x0`, `0x1000`, `0x2000` and `0x2db8`. Each one gets its own permissions (R,
   R+X, R, R+W), so each has to start on its own page. The gaps between the end of one segment and
   the start of the next are 2,520 + 3,707 + 3,244 = **9,471 bytes of zero padding**. That's about
   two-thirds of the file.
2. **Dynamic-linking information**, needed because `puts` lives in a shared library: `.interp`
   (the path `/lib64/ld-linux-x86-64.so.2`), `.dynamic`, `.dynsym` and `.dynstr` (the symbols to
   look up at run time), `.gnu.version` and `.gnu.version_r` (the `GLIBC_2.2.5` version
   requirement), `.rela.dyn` and `.rela.plt`, and the `.plt` and `.got` tables that
   `call puts@PLT` goes through.
3. **Start-up and shutdown code from the C runtime.** `hello.o` only contains `main`, but a
   program needs somewhere to start. `gcc -v` shows that the linker adds five start-up object
   files: `Scrt1.o` (`_start`), `crti.o` and `crtn.o` (`_init` and `_fini` in `.init` and
   `.fini`), and `crtbeginS.o` and `crtendS.o` (`register_tm_clones`, `__do_global_dtors_aux`,
   `.init_array` and `.fini_array`). These are the extra `t` and `T` symbols in `nm hello`.
4. **Headers and metadata for the loader:** the ELF *program headers* (the `LOAD` table), a
   build ID (`.note.gnu.build-id`), an ABI tag (`.note.ABI-tag`, which says "for GNU/Linux 3.2.0"),
   and `.eh_frame_hdr`, a lookup table for exception unwinding.
