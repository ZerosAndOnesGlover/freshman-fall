# PROG 201 · Systems Programming in C
## Week 8: Dynamic Linking and the Runtime Linker

**Credits:** 4 (3 lecture + 1 lab) · **Prerequisites:** PROG 101; CS 201 as co-requisite
**Assessment for this course (overall):** Problem Sets 35%, Projects 25%, Midterms 25%, Final 15%
**This week's deliverables:** **Midterm 2** (Monday, 18:00–19:30, Weeks 4–7, 12.5%), PS 7 (due Friday), PS 8 (released Wednesday, due Friday of Week 9) and **Quiz 8** (Tuesday, covers Week 7).
**Lab 7 is sat on the Monday of this week**; **Lab 8 covers this week and is sat on the Monday of Week 9.**

> ### **Midterm 2 is the Monday of this week**, 18:00–19:30, covering **Weeks 4–7** — 12.5%.
> Lab 7 is that same afternoon and ends at 16:50. Nothing in Week 8 is on the paper. Marked scripts
> come back in Tuesday's lecture.
>
> **Next Friday has two deadlines**: PS 8 **and Project 1**. PS 8 is about four hours' work — do it
> this week and leave Week 9 for the shell.

---

### Why This Week Exists

Because Week 6 measured a trivial program taking **532 µs statically linked and 679 dynamically**, and never said where the difference went.

It went into a program you have never run on purpose: `/lib64/ld-linux-x86-64.so.2`, which `execve` starts *instead of* your binary and which does several thousand instructions of work before `main`. This week is what it does, why, and what you can do with it.

Three ideas:

1. **Linking is filling in holes**, and the only question is whether it happens at build time or load time. The trade is 49× the file size against a few hundred microseconds of startup and a dependency on the environment.
2. **Code that calls across a library boundary goes through two tables** — a read-only PLT of stubs and a writable GOT of addresses — so the code stays shareable and only the data is patched.
3. **The first definition found wins**, which turns a search order into a feature: twelve lines and an environment variable replace any function in any program on the system.

---

### Learning Objectives

By the end of Week 8, you should be able to:

1. Explain what a relocation is and read one with `objdump -R`.
2. Compare static and dynamic linking on size, startup, updates and deployment, with numbers.
3. Find a binary's interpreter, its `NEEDED` libraries and its `RUNPATH`.
4. State the library search order and say why `ld.so` ignores parts of it for set-user-ID programs.
5. Say what `linux-vdso.so.1` is and why it makes `clock_gettime` fast.
6. **Explain the PLT and the GOT**, and trace a call through both.
7. **Explain lazy binding from the bytes** — the GOT slot that initially points at its own PLT stub.
8. Say why `BIND_NOW` and full RELRO are the default now, and what security property they buy.
9. Explain what `-fPIC` costs and why a shared library cannot do without it.
10. Say what PIE is for.
11. **Use `LD_PRELOAD` to replace a function**, and call the original with `RTLD_NEXT`.
12. **Name three things `LD_PRELOAD` cannot do**, each from a measurement.
13. Use `dlopen`/`dlsym`/`dlclose` correctly, including checking `dlerror` rather than the return value.
14. Design a plugin interface with an ABI number and one exported symbol.
15. Explain symbol versioning and when to bump a `SONAME`.
16. Predict constructor and destructor order, and say when a destructor does not run.

---

### This Week's Materials

| File | Purpose |
| --- | --- |
| [[L25 Static and Dynamic Linking]] | Where Week 6's 147 µs went; **785,232 bytes against 16,056**; the `INTERP` header; `linux-vdso.so.1`, which is not a file; the five-step search order; what dynamic linking buys and costs; **`libdl` and `libpthread` no longer exist** |
| [[L26 The GOT the PLT and Position Independent Code]] | Two tables and why; a call as `jmp *(%rip)`; **the GOT slot that holds its own PLT address**, read out of the file; **lazy binding is off by default here** and why that is a security decision; `-fPIC`'s **two loads instead of one**; PIE and ASLR |
| [[L27 Interposition dlopen and Versioning]] | The search order as a feature; twelve lines that replace `time()`; `RTLD_NEXT` and the bootstrap problem; **three measured things `LD_PRELOAD` cannot do**; `dlopen` flags and the `dlerror` rule; the plugin pattern; **`memcpy@GLIBC_2.2.5` and `memcpy@@GLIBC_2.14`**; constructor order |
| [[LAB 8 A Plugin System with dlopen]] | Read a binary, then build a plugin host. **Monday of Week 9** |
| `lab/host.c`, `lab/plugin.h`, `lab/p_*.c`, `lab/Makefile` | The skeleton, three plugins, and the L25–L27 examples |
| [[PS 8 A malloc Profiler with LD_PRELOAD]] | Interpose the allocator, then find out what it cannot see. Due **Friday of Week 9** |
| [[PROG201 Week8/assignments/QUIZ 8 Week 8 Tuesday\|QUIZ 8 Week 8 Tuesday]] | Ten minutes, covers **Week 7**, answer key printed |
| [[PROG201 Week8/resources/Reading Guide Week 8\|Reading Guide Week 8]] | CS:APP Ch. 7, TLPI Ch. 41–42, and **Drepper's *How To Write Shared Libraries*** |
| `solutions_instructor/` | Instructor only |

---

### The One Thing to Take From This Week

**Ask the loader.**

`LD_DEBUG` is built into glibc, costs one environment variable, and answers every question this week can raise:

| Question | Command |
| --- | --- |
| Why is it loading the *wrong* library? | `LD_DEBUG=libs` — every directory tried, in order |
| Is my `LD_PRELOAD` actually winning? | `LD_DEBUG=bindings` — names the object each symbol bound to |
| Is this binary lazy or eager? | `LD_DEBUG=bindings` — are the bindings before or after `main`'s output? |
| Why did my destructor not run? | `LD_DEBUG=all`, and grep for `calling fini` |
| What did startup cost? | `LD_DEBUG=statistics` |

**The last row of that table is how this week's most useful finding was made.** A `LD_PRELOAD` tool that reports from a destructor prints nothing at all for `ls` and `grep` — and `LD_DEBUG=all` shows why in one line: for those programs the loader **runs no fini functions**. Nothing in the tool, the program or the compiler says so; the loader does, if you ask it.

---

### Assessment Reminder

**Midterm 2 is Monday, 18:00–19:30, worth 12.5%**, covering **Weeks 4–7**: `mmap` and allocators, sockets and C10K, the shell and job control, and filesystems. Nothing from this week is on it.

**Labs and quizzes carry no weight** and are still required. **Quiz 8 is at the start of Tuesday's lecture and covers Week 7.**

> **Lab 7** — Week 7's filesystem corruption — is sat on the **Monday of this week**, the afternoon
> of Midterm 2. **Lab 8** covers this week and is sat on the **Monday of Week 9**.

Both are tracked in [[_PROG 201 Lab and Quiz Record]].

---

### Connections

**Back:** **Week 6 L19 §4 measured the gap this week explains.** **Week 4's `mprotect`** is what full RELRO does to the GOT, and **Week 4's `mmap`** is how every library gets into the address space — one physical copy, many page tables. **Week 3's `-lpthread`** has been a no-op all term, and §6 of L25 says why. **Week 0's async-signal-safety** governs what a `LD_PRELOAD` report may call.

**Sideways:** **CS 201 Week 8 is on linking and loading from the machine's side** — the same ELF file, read as an object format rather than as a process.

**Forward:** **Week 9 profiles**, and PS 8's interposer is a profiler with the cheapest possible instrumentation. **Week 10's return-oriented programming is L26 §4's writable GOT**, used by an attacker — which is exactly why the default changed. **Week 11's containers** ship a filesystem so that the dynamic linker finds what it expects.

---

*PROG 201 · Week 8 · © CSE Department*
