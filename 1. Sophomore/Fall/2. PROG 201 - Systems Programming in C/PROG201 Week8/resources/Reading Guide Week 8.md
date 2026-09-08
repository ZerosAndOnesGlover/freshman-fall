# PROG 201 · Reading Guide · Week 8
## CS:APP Chapter 7, and the paper by the person who wrote the loader

---

**This week has one textbook chapter and one paper, and the paper is better.**

CS:APP Chapter 7 is the clearest introduction to linking in print and the source of the GOT/PLT diagrams everyone reproduces. **Ulrich Drepper's *How To Write Shared Libraries*** is forty pages by the person who maintained glibc's dynamic linker, it is free, and it explains not just what the mechanisms are but **what they cost and how to avoid paying** — which is the half no textbook has.

| Source | Read? | Why |
|---|---|---|
| **CS:APP Ch. 7** | **All of it** | Symbol resolution, relocation, static and dynamic libraries, the PLT and GOT |
| **Drepper, *How To Write Shared Libraries*** | **§1–§2, then skim** | Free online. §2.2 on symbol lookup cost and §2.4 on visibility are L27 §7 |
| **TLPI Ch. 41** | **All of it** | Shared libraries: `SONAME`, versions, `ldconfig`, the search order |
| **TLPI Ch. 42** | **All of it** | `dlopen`, `dlsym`, `RTLD_*`, constructors. This is L27 and Lab 8 |
| CS:APP §7.13 | Read | Library interpositioning — compile-time, link-time and load-time |
| `man 8 ld.so` | **Read properly** | Every environment variable, the search order, and the set-user-ID rules |

---

## CS:APP Chapter 7 — the questions to hold

**§7.5–7.6 Symbol resolution**

1. Strong and weak symbols, and the three rules for resolving duplicates. **Write a program with two definitions of the same global in different files and predict what happens** before you build it.
2. `static` at file scope. What does it do to the symbol table, and how does that relate to `-fvisibility=hidden` (L27 §7)?

**§7.7 Relocation**

3. `R_X86_64_PC32` and `R_X86_64_32`. Which one appears in the error when you try to put non-PIC code in a shared library, and why is it that one?
4. Work through Figure 7.10's relocation by hand. Then run `objdump -r` on one of your own `.o` files and find the same shape.

**§7.9–7.10 Libraries**

5. `ar` and the order of `.a` files on the command line. **Why does `gcc prog.c -lfoo -lbar` work and `gcc -lfoo -lbar prog.c` not?** The answer is one sentence about how the linker walks the list.
6. Bryant explains the "one copy in memory" claim for shared libraries. **Which section of the library is shared and which is not?** *(Week 4 L13 §2 has the mechanism.)*

**§7.11–7.12 PIC and the PLT**

7. Figure 7.18's five steps for a lazy PLT call. Match them against the disassembly in L26 §3 — `push $index`, `jmp PLT[0]`, `push link_map`, `jmp resolver`.
8. The book says the GOT entry initially points into the PLT. **Verify it** with `readelf -x .got.plt` on a `-z lazy` binary; L26 §3 is the worked version.
9. §7.12 gives PIC's cost as an extra indirection. Compare the two disassemblies in L26 §5 and say which accesses pay it and which do not.

**§7.13 Interposition**

10. Three kinds: compile-time, link-time (`--wrap`), load-time (`LD_PRELOAD`). For each, say what you must have — the source? the object files? neither? — and give one situation where only that kind will do.

---

## Drepper — the parts worth the time

11. **§1.5, "Impact of Dynamic Linking"**, quantifies startup cost. Compare with L25 §1's measurement on your own machine.
12. **§2.2, "Symbol Lookup"**, explains why lookup is *O(number of libraries × length of the symbol name)* and why the GNU hash exists. Then run `readelf -d yourprogram | grep HASH`.
13. **§2.4.4, visibility**, is the argument for `-fvisibility=hidden` in full. Read it before Lab 8's Part B, where the Makefile already does it.
14. **§3, "Maintaining APIs and ABIs"**, is the definitive account of when you must bump a `SONAME`. Four pages, and it will be the most useful thing you read this term if you ever ship a library.

---

## The Man Pages for This Week

| Page | The paragraph |
|---|---|
| **`man 8 ld.so`** | **The whole thing.** The search order, `LD_PRELOAD`, `LD_DEBUG`, `$ORIGIN`, and the set-user-ID exceptions |
| **`man 3 dlopen`** | The `RTLD_*` flags table, and the NOTES on `dlclose` not necessarily unloading |
| **`man 3 dlsym`** | The paragraph explaining why you check `dlerror` rather than the return value |
| `man 1 readelf` | `-d`, `-l`, `-V`, `-x`. Reference |
| `man 1 objdump` | `-R`, `-T`, `-d -j .plt` |
| `man 1 gcc` | `-fPIC`, `-fPIE`, `-fvisibility`, `-shared`, `-Wl,-z,now` |

**And one thing that is not a man page: `LD_DEBUG=help`.** It lists what glibc's loader will tell you about itself — `libs`, `bindings`, `reloc`, `symbols`, `statistics`, `all` — and it is better than any tool you could install.

---

## Where to Go Deeper

| Source | Topic |
|---|---|
| Levine, *Linkers and Loaders* (1999) | The whole book, and it is free online. Chapter 10 is dynamic linking |
| The System V ABI, AMD64 supplement | The relocation types, formally. §4.4 |
| `man 5 elf` | The ELF format in one page |
| Kell, Mulligan & Sewell, *The Missing Link* (OOPSLA 2016) | What linking actually is, formalised — and how much of it is undefined |
| The `musl` libc source, `ldso/dynlink.c` | 2,000 readable lines that do everything `ld.so` does |
| Bernstein, *Some thoughts on security after ten years of qmail* | Why he static-links, in one paragraph, with the argument stated fairly |

---

## The Habit for This Week

**Ask the loader.**

The habit for Week 5 was to look at the sockets, and for Week 6 the process table. This week's instrument is built into glibc and costs nothing to use:

```bash
LD_DEBUG=libs        ./prog     # which directories, in which order, and what was found
LD_DEBUG=bindings    ./prog     # every symbol, and which object won
LD_DEBUG=reloc       ./prog     # the relocation processing
LD_DEBUG=statistics  ./prog     # what startup actually cost
LD_DEBUG=all         ./prog     # including "calling init" and "calling fini"
```

Every question in this week is answerable from that output:

- *why is it loading the wrong library?* — `libs` shows every directory tried;
- *is my `LD_PRELOAD` winning?* — `bindings` names the object each symbol bound to;
- *why did my destructor not run?* — `all`, and grep for `calling fini`;
- *is this binary lazy or not?* — `bindings`, and look at whether the lines come before `main`'s output.

**It is the difference between guessing about the dynamic linker and reading what it did.** And unlike `strace` or `gdb`, it costs one environment variable and works on anything.

---

*PROG 201 · Week 8 · Reading Guide · © CSE Department*
