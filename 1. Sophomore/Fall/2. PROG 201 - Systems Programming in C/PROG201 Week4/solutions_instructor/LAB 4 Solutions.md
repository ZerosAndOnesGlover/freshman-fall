# PROG 201 · Lab 4 Solutions
## Writing a JIT — Instructor Only

---

**Do not distribute.** Part D's second result — that the JIT ties the C compiler — is the lab's best question and is spoiled by reading this.

**Machine these numbers came from:** Linux 7.0.0-30-generic, gcc 13.3.0 (Ubuntu 24.04), Intel i5-8250U, x86-64. **Everything in Parts A–C is architecture-specific**; a student on an ARM laptop cannot do this lab as written, and §5 says what to do about that.

---

## 1. The Three TODOs

The scaffolding — `code_page`, `make_runnable`, `hexdump`, `try`, the bytecode VM, `horner`, `main` — is unchanged from the skeleton.

```c
static size_t emit_const(unsigned char *c, int k)
{
    size_t n = 0;
    c[n++] = 0x48; c[n++] = 0xc7; c[n++] = 0xc0;    /* mov $k,%rax */
    memcpy(c + n, &k, 4); n += 4;
    c[n++] = 0xc3;                                  /* ret         */
    return n;
}

static size_t emit_poly(unsigned char *c, const int *a, int n)
{
    size_t k = 0;
    c[k++] = 0x48; c[k++] = 0x89; c[k++] = 0xf9;         /* mov %rdi,%rcx  */
    c[k++] = 0x48; c[k++] = 0xc7; c[k++] = 0xc0;         /* mov $a[n],%rax */
    memcpy(c + k, &a[n], 4); k += 4;
    for (int i = n - 1; i >= 0; i--) {
        c[k++] = 0x48; c[k++] = 0x0f; c[k++] = 0xaf; c[k++] = 0xc1;  /* imul %rcx,%rax */
        c[k++] = 0x48; c[k++] = 0x05;                                /* add $a[i],%rax */
        memcpy(c + k, &a[i], 4); k += 4;
    }
    c[k++] = 0xc3;                                       /* ret            */
    return k;
}

static unsigned char *g_page;

static void call_writable(void)
{
    unsigned char *p = code_page(4096);
    emit_const(p, 42);
    ((fn) p)(0);                                   /* no mprotect */
}

static void call_executable(void)
{
    unsigned char *p = code_page(4096);
    emit_const(p, 42);
    mprotect(p, 4096, PROT_READ | PROT_EXEC);
    if (((fn) p)(0) != 42) _exit(3);
}

static void write_executable(void)
{
    g_page[0] = 0x90;                              /* nop, over live code */
}

static void map_rwx(void)
{
    unsigned char *p = mmap(NULL, 4096, PROT_READ | PROT_WRITE | PROT_EXEC,
                            MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    if (p == MAP_FAILED) _exit(4);                 /* refused by the kernel */
    emit_const(p, 42);
    if (((fn) p)(0) != 42) _exit(5);
}

static void part_c(void)
{
    g_page = code_page(4096);
    emit_const(g_page, 42);
    mprotect(g_page, 4096, PROT_READ | PROT_EXEC);

    try("1. call a PROT_READ|PROT_WRITE page", call_writable);
    try("2. call it after mprotect(PROT_READ|PROT_EXEC)", call_executable);
    try("3. write to a PROT_READ|PROT_EXEC page", write_executable);
    try("4. mmap PROT_READ|PROT_WRITE|PROT_EXEC and call it", map_rwx);
}```

Builds clean under `gcc -Wall -Wextra -O2 -g -std=c11 -o jit jit.c`.

---

## 2. Where Students Get Stuck

| # | Symptom | Cause | What to say |
| --- | --- | --- | --- |
| 1 | `emit_const(42)` returns garbage | The four immediate bytes written by hand, or `c[n++] = k` writing one byte | "`memcpy` the `int`. Then `objdump` it." |
| 2 | Polynomial off by a coefficient | Loop written `for (i = 0; i <= n; i++)` — Horner goes **downward** from `a[n]` | Ask them to evaluate by hand for x=2 |
| 3 | Correct for positive x, wrong for negative | Coefficients stored as `unsigned`, or built byte-wise without sign | The `-3` coefficient is `fd ff ff ff` |
| 4 | Segfault the moment `emit_poly` is called | Emitted more than the page, or forgot `ret` | `hexdump` first, run second |
| 5 | Part C experiment 1 does not crash | The body ran in the parent, or `mprotect` was left in from a copy-paste | `try` forks; check the body is passed, not called |
| 6 | Part D: "the JIT is slower!" | Not a bug — see Q6 | This is the question, not a problem |

**Symptom 2 is the common one** and it is not a systems-programming mistake, it is Horner. Have them write the four multiply-add steps for the quartic on paper before touching the emitter.

---

## 3. Reference Output

**Parts A and B**

```
emitted 8 bytes: 48 c7 c0 2a 00 00 00 c3
emit_const(42): f(0) = 42, f(999) = 42   (both should be 42)

emitted 51 bytes: 48 89 f9 48 c7 c0 01 00 00 00 48 0f af c1 48 05 02 00 00 00
                  48 0f af c1 48 05 00 00 00 00 48 0f af c1 48 05 fd ff ff ff
                  48 0f af c1 48 05 07 00 00 00 c3
     x            jit       expected
    -3             43             43
    -2             13             13
    -1              9              9
     0              7              7
     1              7              7
     2             33             33
     3            133            133
     4            379            379
     5            867            867
```

**Part C**

```
1. call a PROT_READ|PROT_WRITE page                Segmentation fault
2. call it after mprotect(PROT_READ|PROT_EXEC)     no signal
3. write to a PROT_READ|PROT_EXEC page             Segmentation fault
4. mmap PROT_READ|PROT_WRITE|PROT_EXEC and call it no signal
```

**Part D**, three runs:

| | ns each | vs the JIT |
| --- | --- | --- |
| JIT-compiled | 2.08 / 2.15 / 2.22 | — |
| C loop over the array | 2.08 / 2.09 / 2.09 | 0.94 / 0.97 / 1.01× |
| bytecode VM | 11.38 / 11.49 / 11.63 | 5.12 / 5.35 / 5.59× |

The bytecode ratio is stable at about 5.5×; the C-loop ratio straddles 1.0 and the honest statement is **"a tie"**.

---

## 4. Answers

**Q1 — `emit_const(-1)`.**

`ff ff ff ff`. Little-endian: the least significant byte first. For −1 every byte is the same so the order is invisible, which is why the question is worth asking about a value like 42 too — `2a 00 00 00`, not `00 00 00 2a`.

**Q2 — the top 32 bits.**

`48 c7 c0` is `mov $imm32,%rax` with a REX.W prefix, and the immediate is **sign-extended** to 64 bits. So `emit_const(-1)` returns `0xffffffffffffffff`, which is −1 as a `long`.

`objdump` says so plainly:

```
0:  48 c7 c0 ff ff ff ff    mov    $0xffffffffffffffff,%rax
```

**This is a fact about the instruction encoding, not about C's integer promotions**, and students who explain it in terms of C have not answered. The follow-up worth asking out loud: *how would you load a 64-bit constant that does not fit in a sign-extended 32 bits?* (`movabs`, `48 b8` + imm64 — ten bytes.)

**Q3 — registers.**

`%rbx`, `%rbp`, `%r12`–`%r15` are **callee-saved**: a function that uses one must save and restore it. `%rax`, `%rcx`, `%rdx`, `%rsi`, `%rdi` and `%r8`–`%r11` are caller-saved and free.

Written down in the **System V AMD64 ABI**, §3.2.1 and Figure 3.4; `man 7 x86-64-abi` where installed; CS:APP §3.7.

**Q4 — two `SIGSEGV`s, two mechanisms.**

**Experiment 1** is the **NX bit** (bit 63 of the PTE): the page is marked no-execute, and the fault is an *instruction fetch* fault. **Experiment 3** is the **write-permission bit**: the page is read-only and the fault is a *store* fault.

Different bits, different fault types, same signal — which is why `SIGSEGV` on its own is a poor diagnostic and why a handler wanting to know needs `si_code` and the error code in the `ucontext`.

Full marks require naming both bits, or at least distinguishing "cannot execute here" from "cannot write here". "Both are permission errors" is [half].

**Q5 — W^X.**

**W^X:** no page should be simultaneously writable and executable, so that an attacker who can write data cannot turn it into code. It is what made the classic stack-smashing-with-shellcode attack stop working.

**This machine does not enforce it** — experiment 4 succeeded. Enforcement exists elsewhere: SELinux policy, PaX/grsecurity kernels, OpenBSD by default, iOS and Apple silicon (where a JIT must call `pthread_jit_write_protect_np`).

The one-sentence consequence: **keeping the discipline anyway is what makes the program portable to the systems that do enforce it, and what limits the damage of a bug in your own emitter** — a JIT with a writable code page is a memory-corruption bug away from being an arbitrary-code-execution bug.

**Q6 — why the JIT only tied C.**

Because `A` and `N` are file-scope `const` and `horner` is `static`, so **gcc -O2 knew the coefficients and the loop count at compile time**. It unrolled the loop, folded `a[2] == 0` away, and emitted very nearly the same instruction sequence the JIT emits — the JIT's whole advantage is specialisation, and the compiler had already specialised.

The right conclusion, and the mark: **a JIT does not beat a static compiler; it beats an interpreter.** JITs exist where the compiler *cannot* know — a regular expression typed at runtime, a query plan, a shader, a language whose types are only known when the code runs.

Students who say "my emitter must be inefficient" have missed it; ask them what `gcc -O2 -S` did to `horner`. The lab extension (coefficients from `argv`) is the fix, and a student who did it and reported a different ratio deserves saying so.

**Q7 — the 5.5×.**

The generated code does not pay: **(1) the dispatch** — a load of the opcode, a bounds-checked branch through a jump table, and a pointer increment, per operation; and **(2) the indirection** — the operand is fetched from the instruction stream in memory rather than being an immediate in the instruction. There is also a branch misprediction cost on the dispatch, which on a short polynomial is most of it.

To close the gap without generating code: **computed goto / threaded dispatch** (`&&label` and `goto *next`), which replaces one hard-to-predict indirect branch with one per opcode, each of which the predictor can learn separately. Typically 20–40% on a real VM — worth having, and not 5×. Accept "superinstructions" or "direct threading" as alternatives.

**Q8 — `__builtin___clear_cache`.**

On x86-64 the instruction and data caches are **coherent in hardware**, so it compiles to nothing. On ARM, ARM64, MIPS, RISC-V and POWER they are not: freshly written bytes sit in the D-cache while the I-cache may still hold whatever was there before, and executing them fetches stale instructions.

**It is a bug you cannot find on this machine** — the code is correct here by accident of the architecture, and fails on the first ARM machine it meets, non-deterministically, depending on cache state. That is the reason the lab requires it: a portability bug with no local symptom is exactly the kind you have to fix by rule rather than by testing.

---

## 5. Students Not on x86-64

Parts A–C are x86-64 encodings. A student on an Apple silicon or ARM laptop has three options, in order of preference:

1. **Use the BH 215 machines**, which is the intended path and the reason the lab is in the lab.
2. **`gcc -static` on an x86-64 box and run under `qemu-user`**, which works and makes Part D's timings meaningless.
3. **Emit AArch64 instead** — `mov x0, #imm` / `mul` / `add` / `ret`, all fixed 32-bit encodings, and arguably an easier target than x86-64. A student who does this has done more work than the lab asked and **must** implement `__builtin___clear_cache` for real (Q8), because on their machine it is not a no-op. Give them the checkoff and ask them to show Q8's failure without it.

---

## 6. Checkoff

The four boxes are in the lab sheet. In practice:

- **Make them disassemble.** A student who has run `objdump` on their own bytes has understood something a student who only ran the program has not. It is the single most valuable two minutes of the session.
- **Ask Q4 out loud.** "Both are segfaults" is where most people stop; the two bits are the answer.
- **Q6 is the lab.** If a student is disappointed that the JIT did not win, that is the moment to teach — ask what the compiler knew, and then point at the 5.5× that it *did* win.
- The extension (coefficients from `argv`, then a conditional with backpatching) is a genuinely hard forty minutes and is the right thing to give a fast student. Backpatching is Week 8's relocation problem in miniature.

---

*PROG 201 · Week 4 · Lab 4 Solutions · Instructor Only · © CSE Department*
