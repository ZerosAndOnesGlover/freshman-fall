# PROG 201 · Systems Programming in C
## Week 8 · Lecture 2 of 3
### The GOT, the PLT, and Position-Independent Code

*“Any problem in computer science can be solved with another level of indirection.”* — David Wheeler, as quoted by Butler Lampson in his Turing Award Lecture (1993)

---

**Reading:** CS:APP §7.11–7.12 · TLPI §41.3, §41.13 · Drepper, *How To Write Shared Libraries* · **Previous:** L25 · **Next:** L27 — interposition, `dlopen` and versioning

**Coursework:** 📝 **PS 8** released today, due Fri of Week 9 17:00 · 📝 **PS 7** due Fri this week 17:00 · 🔬 **Lab 8** Mon of Week 9 15:00–16:50 · 📊 **Quiz 9** Tue of Week 9

---

## 1. The Problem

Your program calls `greet()`, which lives in `libgreet.so`. At compile time nobody knows where `libgreet.so` will be mapped — and it must be free to move, or two programs could not both use it (and ASLR could not exist).

So the compiler cannot emit `call 0x7f2a4c001234`. It has to emit something that **works out the address at run time**, cheaply, without making the library's code writable.

The answer is two tables:

| | holds | written by |
| --- | --- | --- |
| **GOT** — Global Offset Table | **addresses** of things elsewhere | the dynamic linker |
| **PLT** — Procedure Linkage Table | **code**: tiny stubs that jump through the GOT | nobody — it is read-only |

**The code stays read-only and shareable; only the data table is patched.** That is the whole design.

---

## 2. What a Call Actually Compiles To

`useglib.c` calls `greet(10)`. The compiler emits `call greet@plt`, and the PLT entry is:

```
0000000000001080 <greet@plt>:
    1080:  endbr64
    1084:  jmp    *0x2f3e(%rip)        # 3fc8 <greet@Base>
```

**One indirect jump through a GOT slot**, addressed `%rip`-relative so the whole thing is position independent. And the relocation table says who fills that slot in:

```
$ objdump -R useglib
0000000000003fc8  R_X86_64_JUMP_SLOT   greet@Base
```

`R_X86_64_JUMP_SLOT` means *"put the address of `greet` here"*. Global **data** gets `R_X86_64_GLOB_DAT` instead, and both are entries in the same table.

---

## 3. Lazy Binding, and the Trick That Makes It Work

Resolving a symbol means searching every loaded library's hash table. A program that links against a large library may reference thousands of symbols and call fifty. **Lazy binding** resolves each one on its first call.

The mechanism is one of the cleverest things in Unix, and you can read it out of the binary. Build with lazy binding on and the PLT has an extra entry at the front:

```
0000000000001020 <.plt>:                       ; PLT[0], the trampoline
    1020:  push   0x23ba(%rip)        # GOT+8   <- which library
    1026:  jmp    *0x23bc(%rip)       # GOT+16  <- _dl_runtime_resolve

    1030:  endbr64                                ; PLT[1] = farewell
    1034:  push   $0x0                            ; relocation index 0
    1039:  jmp    1020 <.plt>                     ; go to PLT[0]

    1040:  endbr64                                ; PLT[2] = greet
    1044:  push   $0x1                            ; relocation index 1
    1049:  jmp    1020 <.plt>
```

And now the trick. Look at what the GOT slots contain **in the file, before anything runs**:

```
$ objdump -R useglib_lazy | grep JUMP_SLOT
00000000000033f0 R_X86_64_JUMP_SLOT  farewell@Base
00000000000033f8 R_X86_64_JUMP_SLOT  greet@Base

$ readelf -x .got.plt useglib_lazy
  0x000033f0 30100000 00000000 40100000 00000000
```

**`0x1030` and `0x1040` — the addresses of the PLT stubs themselves.**

So the first call to `greet` goes: `call greet@plt` → `jmp *GOT` → and the GOT sends it **back into its own PLT entry**, one instruction further on, where it pushes the relocation index and falls into PLT[0], which pushes the link map and jumps to the resolver. The resolver finds `greet`, **writes its real address into the GOT slot**, and jumps to it.

**The second call jumps straight there.** The GOT slot no longer points at the PLT, so the stub is never entered again.

`LD_DEBUG=bindings` shows it happening:

```
>>> about to call greet the first time
   binding file ./useglib_lazy to libgreet.so: normal symbol `greet'
greet(10)    = 21
>>> about to call greet the second time
greet(20)    = 41                                   <- nothing bound
>>> about to call farewell the first time
   binding file ./useglib_lazy to libgreet.so: normal symbol `farewell'
farewell(10) = 9
```

**Each symbol is resolved exactly once, at its first call, and never again.**

---

## 4. Except That It Is Switched Off

Everything in §3 required `-Wl,-z,lazy -Wl,-z,norelro`, because **on this system lazy binding is not the default**:

```
$ readelf -d useglib | grep -E "BIND_NOW|FLAGS"
 0x000000000000001e (FLAGS)     BIND_NOW
 0x000000006ffffffb (FLAGS_1)   Flags: NOW PIE
```

and the same program built normally binds everything before `main`:

```
   binding file ./useglib to libgreet.so: normal symbol `farewell'
   binding file ./useglib to libgreet.so: normal symbol `greet'
>>> about to call greet the first time
greet(10)    = 21
```

**Ubuntu compiles with `-Wl,-z,relro,-z,now` by default**, and most distributions now do. The reason is security, and it is Week 10's subject arriving early:

**A writable GOT is an attacker's dream.** Any bug that lets somebody write a chosen value to a chosen address can overwrite a GOT entry, and then the program's next call to `printf` goes wherever they said. **Full RELRO** — `-z relro -z now` together — resolves everything at load time and then `mprotect`s the GOT read-only (Week 4 L15 §1, in the loader).

So the trade is explicit:

| | lazy (`-z lazy`) | now (`-z now`, the default) |
| --- | --- | --- |
| Startup | resolves only what is called | resolves **everything** |
| Per-call | one indirect jump, after the first | one indirect jump |
| The GOT | **writable for the process's life** | **read-only after startup** |
| A GOT-overwrite attack | available | not available |

**The curriculum's description of lazy binding is correct and describes a configuration you have to ask for.** Both are worth knowing: you will read the lazy mechanism in every book, and you will find `BIND_NOW` in every binary on the machine.

---

## 5. Position-Independent Code, and What It Costs

A shared library may be mapped at any address, so its code must not contain absolute addresses. `-fPIC` is what arranges that, and the cost is measurable in two instructions.

```c
int counter = 7;
int get(void) { return counter; }
```

**Without `-fPIC`:**

```
<get>:
   endbr64
   mov    0x0(%rip),%eax        ; load counter directly
   ret
```

**With `-fPIC`:**

```
<get>:
   endbr64
   mov    0x0(%rip),%rax        ; load the ADDRESS of counter from the GOT
   mov    (%rax),%eax           ; then load counter
   ret
```

**Two loads instead of one**, for every access to a global that might be interposed (L27). Function calls pay the PLT's indirect jump. In 1995 this was the reason people avoided shared libraries; on a machine with a load-store unit and a data cache it is usually unmeasurable, and the exceptions are tight loops over globals.

**It is not optional.** A non-PIC object simply cannot go into a shared library:

```
$ gcc -shared -o bad.so pic_no.o
/usr/bin/ld: relocation R_X86_64_PC32 against symbol `counter' can not be
used when making a shared object; recompile with -fPIC
```

The reason is worth stating exactly: **the relocation the compiler emitted assumes a fixed distance between the code and the data, and `ld.so` cannot fix it up without writing to the code** — which would make the text unshareable, which is the entire point of a shared library.

---

## 6. PIE, and Why Your Executable Is One Too

`readelf` said `Flags: NOW PIE`. A **position-independent executable** is an executable built like a shared library, so the kernel can load it at a random address.

That is **ASLR** — address space layout randomisation. Without PIE, the executable's own code is at a fixed address in every run, and an attacker who wants a gadget knows exactly where it is (Week 10). With PIE, they do not.

```
$ ./tiny_dyn; ./tiny_dyn        # /proc/self/maps differs every run
```

It costs the same indirection as §5 plus a register (`%rbx` is reserved for the GOT pointer on 32-bit x86; on x86-64 `%rip`-relative addressing makes it nearly free), and every distribution now enables it by default. `-no-pie` turns it off, and the only good reasons are measurement and Week 10's lab.

---

## 7. Reading a Binary

The five commands that answer almost every question in this week:

| Command | Tells you |
| --- | --- |
| `readelf -d` | `NEEDED`, `RUNPATH`, `BIND_NOW`, `SONAME` — the dynamic section |
| `readelf -l` | the segments, including `INTERP` and `GNU_RELRO` |
| **`objdump -R`** | **the relocations: every hole and who fills it** |
| `objdump -d -j .plt` | the stubs |
| `nm -D --undefined-only` | what this object needs from somewhere else |
| `nm -D --defined-only` | what it provides |

**And one environment variable that is better than all of them: `LD_DEBUG`.** `LD_DEBUG=help` lists what it can print; `libs` shows the search, `bindings` shows every symbol resolution, `reloc` shows the relocation processing, `statistics` shows what startup cost. It is built into glibc's loader and needs no tooling at all.

---

## Summary

- Code cannot contain the address of something in another library, so calls go through **two tables**: the **PLT** (read-only code stubs) and the **GOT** (writable addresses, filled by `ld.so`).
- A call compiles to `jmp *offset(%rip)` through a GOT slot, with an `R_X86_64_JUMP_SLOT` relocation naming the symbol.
- **Lazy binding**: the GOT slot initially holds the address of **its own PLT stub**, so the first call falls into the resolver, which patches the slot; the second call goes straight through. Observed in the file: the slots contain `0x1030` and `0x1040`, the PLT entries themselves.
- **It is off by default here.** Ubuntu builds with `-z relro -z now`, so everything binds before `main` and the GOT is then **read-only** — because a writable GOT is a target.
- **`-fPIC` costs one extra load per global access** (the address from the GOT, then the value) and is **mandatory** for a shared library: a non-PIC object cannot be linked into one, because fixing its relocations would mean writing to the text.
- **PIE** applies the same treatment to executables so that ASLR can randomise them.
- `readelf -d`, `objdump -R` and **`LD_DEBUG=bindings`** answer most questions in this week.

---

## Exercises

1. Build a program with `-z lazy -z norelro` and one without, and compare `objdump -d -j .plt` for both. Which one has a PLT[0], and why does the other not need one?
2. Print the GOT slot for a function before and after its first call, using `gdb` — `x/gx` on the address `objdump -R` gave you. Do it for both binaries from (1).
3. Time 10 million calls to a function in a shared library, and the same function compiled into the program. Where does the difference go, and is it what you expected?
4. Compile a file with and without `-fPIC` and `diff` the disassembly. Which accesses changed and which did not? *(Locals will not. Say why.)*
5. `LD_DEBUG=statistics ./yourprogram`. What does it report about relocation processing, and how does the number change with `LD_BIND_NOW=1`?
6. Take a program with full RELRO and confirm the GOT is read-only at run time by finding it in `/proc/pid/maps`. Then build with `-z norelro` and confirm it is not.
7. `-no-pie` a program and run it twice, printing the address of `main`. Then rebuild as PIE and repeat. What did you just demonstrate?

---

*PROG 201 · Week 8 · L26 · © CSE Department*
