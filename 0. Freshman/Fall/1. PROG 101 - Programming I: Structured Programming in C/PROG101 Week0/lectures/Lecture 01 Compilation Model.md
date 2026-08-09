# PROG 101 · Programming I: Structured Programming in C
## Week 0 · Lecture 1: What Is a Compiler? The C Compilation Model

---

## Lecture Goals

By the end of this lecture you will:
- Understand what a compiler *actually does*, step by step
- Know the four distinct phases of C compilation
- Be able to explain why compiler errors differ from linker errors
- Know what the tool-chain is and what each tool does
- Have dissected a Hello World program line by line

---

## 1. Why C?
	
Before anything else: why are we learning C in 2026?

Because C is the language of the machine. Every layer of software you will ever build on top of: Linux, Python, Node.js, SQLite, your web browser's engine; is written in C (or C++, which is C with additions). When you learn C, you are learning the *lingua franca* of systems programming.

More importantly: C hides nothing. Python hides memory allocation. Java hides pointers. C hides nothing. Writing `int *p = malloc(sizeof(int));` forces you to confront the machine directly. That confrontation builds a mental model that makes you better at *every* language you use afterward, because you know what is happening underneath.

**The principle:** understand the machine. The abstractions will follow naturally.

---

## 2. The Myth of "Running Code"

When you write a C program and "run" it, most people imagine a magic box that reads your text file and executes it. This is incorrect.

What actually happens is a **multi-stage translation pipeline** that converts your human-readable C source into a binary file the CPU can execute directly. This pipeline has four stages:

```
Source Code (.c)
       │
       ▼  Stage 1: Preprocessing
Preprocessed Source (.i)
       │
       ▼  Stage 2: Compilation
Assembly Code (.s)
       │
       ▼  Stage 3: Assembly
Object Code (.o)
       │
       ▼  Stage 4: Linking
Executable (a.out / your_program)
```

Each stage is a separate program. Together they form the **tool-chain**.

---

## 3. Stage 1: The Preprocessor (`cpp`)

The preprocessor is a **text substitution engine**. It runs *before* the compiler sees your code. It handles lines beginning with `#`.

### What the preprocessor does:

**`#include`: File Insertion**

```c
#include <stdio.h>
```

The preprocessor literally opens the file `stdio.h` (found in `/usr/include/`) and pastes its entire contents into your source file at that exact location. The compiler never sees `#include`: it sees the contents of `stdio.h` instead.

You can verify this yourself:
```bash
gcc -E hello.c -o hello.i    # Run only the preprocessor
wc -l hello.c                 # Original: ~6 lines
wc -l hello.i                 # After: 800+ lines (all of stdio.h)
```

**`#define`: Text Substitution**

```c
#define PI 3.14159
#define SQUARE(x) ((x) * (x))
```

Every occurrence of `PI` in your source is replaced with `3.14159` before compilation. This is pure text replacement, not a function call, not a variable. Understanding this distinction is critical. (We'll return to macro pitfalls in Week 10.)

**Conditional Compilation**

```c
#ifdef DEBUG
    printf("Debug value: %d\n", x);
#endif
```

The preprocessor includes or excludes blocks of code based on whether macros are defined. This enables debug builds vs release builds from the same source.

---

## 4. Stage 2: The Compiler (`cc1`)

The compiler translates preprocessed C source into **assembly language**: human-readable CPU instructions specific to your architecture (x86-64, ARM, RISC-V, etc.).
 
```c
// Your C code:
int add(int a, int b) {
    return a + b;
}
```

Compiles to x86-64 assembly:
```asm
add:
    movl    %edi, %eax      ; move first argument into eax
    addl    %esi, %eax      ; add second argument to eax
    ret                      ; return (eax holds the return value)
```

You can inspect this:
```bash
gcc -S hello.c -o hello.s    # Run preprocessor + compiler only
cat hello.s                   # Read the assembly output
```

The compiler is where:
- **Type checking** happens (catching `int x = "hello"`)
- **Optimization** happens (`-O2`, `-O3` flags)
- **Syntax errors** are caught

This is why a **compiler error** tells you the exact line and character of your mistake, the compiler is reading your text and understanding its structure.

---

## 5. Stage 3: The Assembler (`as`)

The assembler converts human-readable assembly (`.s` files) into **machine code** (`.o` files): binary patterns of `0s` and `1s` that the CPU executes directly.

The output is an **object file**, not yet a complete program. It contains:
- Machine code for the functions you defined
- A **symbol table** listing the names of functions/variables this file defines or needs
- Placeholder addresses for symbols defined in other files

```bash
gcc -c hello.c -o hello.o    # Run through assembler (produces .o)
file hello.o                  # Shows: ELF 64-bit relocatable
objdump -d hello.o            # Disassemble: view machine code
```

---

## 6. Stage 4: The Linker (`ld`)

The linker is the most misunderstood part of the toolchain. It takes one or more object files and **combines them into a single executable**, resolving all the placeholder addresses.

When your `hello.c` calls `printf()`, your object file has a placeholder that says "I need the function called `printf`." The linker finds `printf` in `libc.so` (the C standard library), fills in the actual address, and produces a complete executable.

```
hello.o  ──┐
           ├── [linker] ──▶  a.out (executable)
libc.so  ──┘
```

This is why **linker errors** look different from compiler errors:
- Compiler error: `error: use of undeclared identifier 'foo'` — you typed something wrong
- Linker error: `undefined reference to 'foo'` — you declared something the compiler accepted, but no object file provides the definition

```bash
gcc hello.o -o hello          # Linking step only
# Or do all stages in one command:
gcc hello.c -o hello          # Full pipeline
```

---

## 7. The Full Toolchain

| Tool | Role | Flag to stop here |
|------|------|-------------------|
| `cpp` (preprocessor) | Text substitution, file inclusion | `gcc -E` |
| `cc1` (compiler) | C → assembly | `gcc -S` |
| `as` (assembler) | assembly → object code | `gcc -c` |
| `ld` (linker) | object files → executable | (full compilation) |

Supporting tools you will use constantly:
- **`make`**: Build automation. Knows which files changed and only recompiles what's needed.
- **`gdb`**: The GNU Debugger. Step through code, inspect memory, read registers.
- **`valgrind`**: Memory error detector. Catches memory leaks, invalid reads/writes, use-after-free.

---

## 8. Hello World: Dissected Line by Line

```c
#include <stdio.h>

int main(void) {
    printf("Hello, world!\n");
    return 0;
}
```

**Line 1: `#include <stdio.h>`**
- Preprocessor directive (not C code)
- Inserts the Standard I/O header
- Gives us the *declaration* of `printf` (not the definition, that's in libc)
- Angle brackets `<>` mean: look in system include directories
- Quotes `"myfile.h"` mean: look in the current directory first

**Line 3: `int main(void)`**
- `main` is the program's entry point: where execution begins
- `int` return type: the OS receives this as the program's exit code
- `void` parameter: explicitly no parameters (as opposed to `int argc, char *argv[]`)
- `{` opens the function body

**Line 4: `printf("Hello, world!\n");`**
- `printf`, "print formatted", outputs text to stdout
- `"Hello, world!\n"`: a string literal stored in the program's read-only data section
- `\n`: escape sequence for newline (ASCII 10)
- `;`: statement terminator (not optional in C)

**Line 5: `return 0;`**
- Returns 0 to the OS (convention: 0 = success, non-zero = error)
- The shell can check this: `echo $?` after running your program
- In `main`, `return 0` is equivalent to `exit(0)`

**Line 6: `}`**
- Closes the function body

---

## 9. The `main` Function and Program Entry

The OS doesn't call `main` directly. The actual sequence is:

```
OS loads executable
    │
    ▼
_start() [in crt0.o, provided by glibc]
    │
    ▼ sets up stack, initializes C runtime
main(argc, argv, envp)
    │
    ▼ your code runs
return value
    │
    ▼
exit() [calls cleanup handlers, flushes stdio, etc.]
    │
    ▼
_exit() [system call to OS]
```

`_start` is the *actual* entry point of the executable. It sets up the C runtime environment before handing off to `main`. You almost never need to know this, but a great engineer knows it.

---

## 10. Why This Matters (The Engineer's Perspective)

Understanding the compilation pipeline gives you:

1. **Faster debugging**: you instantly know whether an error is a preprocessor, compiler, or linker problem, which tells you where to look.

2. **Control over builds**: you can compile multiple `.c` files separately and link them, speeding up large projects (only recompile what changed).

3. **Security understanding**: buffer overflows, format string attacks, and ROP exploits are all intelligible once you understand how the compiler translates your C into machine code.

4. **Performance understanding**: optimization flags (`-O2`, `-O3`) tell you the compiler can restructure your code. Knowing about inlining, loop unrolling, and instruction selection starts here.

5. **Portability understanding**: the preprocessor's conditional compilation is how the same source compiles on Linux, macOS, and Windows.

---

## Practice Exercises

Work these before the next lecture. Each set moves from *trace* (predict what happens) through *explain* (say why) to *build* (write it yourself) and finally *stretch* (a step past the lecture). Answers are at the end of the section — attempt each exercise before reading them.

**1. (Trace.)** Given `hello.c` below, predict what each command produces and say which of the four stages it stops after.

```c
#include <stdio.h>
#define GREETING "Hello"

int main(void) {
    printf("%s, world\n", GREETING);
    return 0;
}
```

```bash
gcc -E hello.c
gcc -S hello.c
gcc -c hello.c
gcc hello.c
```

**2. (Explain.)** These two errors look similar but come from different stages. Explain what produces each and how you would fix it.

```
error: implicit declaration of function 'sqrt'
/usr/bin/ld: /tmp/cc8Hs2.o: undefined reference to `sqrt'
```

**3. (Build.)** Write a two-file program: `mathutils.h` declaring `int square(int)`, `mathutils.c` defining it, and `main.c` using it. Give the exact commands to build it in separate compilation, and explain why the header must not contain the definition.

**4. (Stretch.)** Run `nm` on an object file and on the final executable. Explain what the letters `T`, `U`, `D`, and `B` mean, and why `printf` changes category between the two.


### Answers

**1.** - `gcc -E` — **preprocessor only.** Emits C source to stdout: `stdio.h` fully expanded (hundreds of lines of declarations), `GREETING` replaced by the literal `"Hello"`, and the `#define` line gone. Try `gcc -E hello.c | wc -l` — the two-line program becomes ~800 lines.
- `gcc -S` — **through compilation.** Writes `hello.s`, assembly text. You will see `.string "Hello, world"` and a `call printf`.
- `gcc -c` — **through assembly.** Writes `hello.o`, a binary object file. `printf` appears as an *undefined* symbol; check with `nm hello.o` and look for `U printf`.
- `gcc` — **all four stages including linking.** Writes `a.out`, an executable, with `printf` resolved against the C library.

The chain is cumulative: each flag stops one stage later. The reason to know it is diagnostic — a macro misbehaving is a `-E` problem, an "undefined reference" is a **link** error and nothing to do with your syntax, and knowing which stage failed tells you which half of the toolchain to look at.

**2.** The first is from the **compiler** (stage 2). It means no declaration of `sqrt` was visible, so the compiler does not know its parameter or return types. Fix: `#include <math.h>`, which supplies the prototype `double sqrt(double);`.

The second is from the **linker** (stage 4, `ld`). The declaration was found, so the compiler happily emitted a `call sqrt`, but no *definition* — no actual machine code — was supplied at link time. Fix: link the math library with `gcc prog.c -lm`.

The distinction is the practical payoff of the four-stage model. A **declaration** tells the compiler the type signature; a **definition** provides the code. A header gives you the first, a library the second, and you need both. This is why `-lm` exists at all: on glibc the math functions live in a separate archive from the rest of libc, and it must be named explicitly.

Note the linker error names a `.o` file and an odd temporary path — that is your program's object file. Any error mentioning `ld`, `.o` files, or "undefined reference" is a linking problem, and no amount of editing the *syntax* of the calling line will fix it.

**3.**

```c
/* mathutils.h */
#ifndef MATHUTILS_H
#define MATHUTILS_H
int square(int n);
#endif

/* mathutils.c */
#include "mathutils.h"
int square(int n) { return n * n; }

/* main.c */
#include <stdio.h>
#include "mathutils.h"
int main(void) { printf("%d\n", square(7)); return 0; }
```

```bash
gcc -Wall -Wextra -std=c11 -c mathutils.c    # -> mathutils.o
gcc -Wall -Wextra -std=c11 -c main.c        # -> main.o
gcc mathutils.o main.o -o prog
```

The header must hold only the **declaration** because `#include` is literal text substitution. A definition in the header would be copied into *every* translation unit that includes it, and the linker would then find two definitions of `square` — `multiple definition of 'square'`. One declaration per unit is fine; one definition per *program* is the rule.

The include guard prevents a related problem: if `mathutils.h` were included twice in one file (directly and via another header), the declaration would appear twice. Duplicate *declarations* are actually legal for functions, but not for `struct` or `typedef` definitions, so guards are unconditional practice.

**4.**

```bash
gcc -c hello.c && nm hello.o
gcc hello.c -o hello && nm hello | grep -w printf
```

The letters name the **section** a symbol lives in (uppercase = external/global, lowercase = local):

- **T** — *text*: a defined function, i.e. actual machine code. `main` is `T`.
- **U** — *undefined*: referenced here, defined elsewhere. The linker's job is to resolve every one.
- **D** — *data*: an initialised global or static variable (`int counter = 5;`).
- **B** — *bss*: an uninitialised global or static (`int counter;`). It occupies no space in the file — the loader zeroes it at startup, which is why a large uninitialised array does not bloat the binary.

`printf` is **U** in `hello.o` because your translation unit only calls it. After linking it is resolved — against libc, which is dynamically linked by default, so in the executable it appears as `U` still but now with a PLT entry, and `ldd hello` shows the dependency on `libc.so.6`. Link statically with `gcc -static` and it becomes **T**: the code is copied into your binary, which grows from ~16 KB to ~800 KB.

`nm` is the fastest way to answer "is this symbol actually in there?" when a link fails, and `nm -C` demangles C++ names when you meet them later.



---

## Key Vocabulary

| Term | Definition |
|------|-----------|
| **Source file** | Human-readable `.c` text |
| **Preprocessor** | Text substitution before compilation |
| **Compiler** | Translates C to assembly |
| **Assembly** | Human-readable CPU instructions |
| **Object file** | Binary machine code for one translation unit |
| **Linker** | Combines object files into an executable |
| **Executable** | A complete binary the OS can run |
| **Toolchain** | The complete set of tools (compiler + assembler + linker + debugger) |
| **Symbol** | A name (function or variable) that the linker resolves across files |

---

## Questions to Sit With

1. If `#include` just pastes file contents, what happens if you `#include` a file that `#include`s the same file again? (Hint: `#include` guards)
2. Why does the linker need to exist as a separate step? Why not combine all code into one object file?
3. What is the difference between a *declaration* and a *definition* in C? (This distinction is fundamental and we will return to it.)

---

*Next: Lecture 2 — [[Lecture 02 Tool-chain Make GDB]]*
