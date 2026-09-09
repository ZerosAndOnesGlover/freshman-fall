# PROG 201 · Quiz 9
## Administered: Tuesday, Week 9 (first 10 minutes of lecture)

**Name:** _________________________________ **Section:** ___________ **Date:** ___________

**Covers Week 8** — static and dynamic linking, the GOT and PLT, PIC, interposition, `dlopen`, versioning.

**Instructions:** Closed notes. 10 minutes.

> **This quiz is not marked and carries no weight.** The answer key is printed below the questions.
>
> **Project 1 and PS 8 are both due Friday at 17:00.**

---

**Q1.** `ldd ./prog` prints three lines. One of them is not a file on disk. Which, who put it there, and why does it make `clock_gettime` fast?

&nbsp;

&nbsp;

---

**Q2.** In a binary built with lazy binding, the GOT slot for a function initially contains an address **inside the PLT**. Walk through the first call and the second.

&nbsp;

&nbsp;

&nbsp;

---

**Q3.** Your binaries are built with `BIND_NOW`, so §2's mechanism never runs. What is the default buying, and what is it costing?

&nbsp;

&nbsp;

---

**Q4.** `gcc -shared` on an object compiled without `-fPIC` fails. Give the error's essential complaint and say why fixing it at load time is not an option.

&nbsp;

&nbsp;

---

**Q5.** You `LD_PRELOAD` a library that redefines `time()`. It works on your test program and does nothing to `date(1)`. Explain.

&nbsp;

&nbsp;

---

**Q6.** Your `LD_PRELOAD` `malloc` profiler reports 2 allocations for a program with a thousand `malloc`/`free` pairs. What happened, and what evidence would settle it?

&nbsp;

&nbsp;

---

**Q7.** `dlsym(h, "sym")` returns `NULL`. Is that an error? How do you actually find out, and what must you do *before* the `dlsym`?

&nbsp;

&nbsp;

---
---

# Answer Key

*Mark your own. Be honest — nobody else will see this.*

---

**Q1.** **`linux-vdso.so.1`** — the virtual dynamic shared object. **The kernel maps it into every process**; there is no such file anywhere on disk.

It contains implementations of `clock_gettime`, `gettimeofday` and `getcpu` that read a page of kernel-maintained data **without a system call** — so they cost nanoseconds where Week 4 measured `getpid()` at **574 ns**. *(L25 §3.)*

---

**Q2.** The slot points at **its own PLT entry**, just past the start. First call: `call f@plt` → the stub's `jmp *GOT` → control goes **back into the stub** → it pushes the relocation index → jumps to PLT[0], which pushes the link map and jumps to `_dl_runtime_resolve` → the resolver finds the symbol, **writes its address into the GOT slot**, and jumps to it.

Second call: `jmp *GOT` goes straight to the function. The stub is never entered again. Measured: the slots contained `0x1030` and `0x1040`, which are the PLT entries. *(L26 §3.)*

---

**Q3.** **Buying: a read-only GOT.** `-z relro -z now` resolves everything before `main` and then `mprotect`s the GOT read-only, so a bug that lets an attacker write to a chosen address cannot redirect a GOT entry and hijack the next library call.

**Costing: startup time** — every symbol is resolved, including the ones never called. Every distribution has decided that trade is worth it. *(L26 §4.)*

---

**Q4.** `relocation R_X86_64_PC32 against symbol ... can not be used when making a shared object; recompile with -fPIC`.

The relocation assumes a **fixed distance between the code and the data**. A shared library can be mapped anywhere, so `ld.so` would have to patch the **text** to fix it — which would make the text unshareable and private per process, destroying the entire point of a shared library. `-fPIC` instead routes the access through the GOT: **two loads instead of one.** *(L26 §5.)*

---

**Q5.** **`date` does not call `time()`.** It calls **`clock_gettime`**, which is resolved through the **vDSO** — so it never enters libc's PLT and there is nothing for an interposing library to sit in front of.

The general rule: **interposition catches the symbol you interposed, and only that one.** A program reaching the same result by a different route is untouched. *(L27 §3.)*

---

**Q6.** **The compiler deleted the allocations.** At `-O2`, `malloc(n)` followed by `free(p)` with the pointer unused is removable under the as-if rule, and GCC removes it.

The evidence: `objdump -d prog | grep -c '<malloc@plt>'` → **0**, and `nm -D --undefined-only prog | grep -c malloc` → **0**. The binary does not merely fail to call `malloc`; **it does not reference the symbol at all.** Rebuilt `-O0`, the same profiler reports 1,012 mallocs and 1,000 frees. *(L27 §3.)*

---

**Q7.** **Not necessarily an error** — a symbol's *value* can legitimately be `NULL`, so the return value is not the indicator.

Call **`dlerror()` after** the `dlsym` and test that. And you must call `dlerror()` **before** as well, to clear any stale message — it reports the last error and **clears itself when read**, so an earlier unread failure would be blamed on your `dlsym`. *(L27 §4.)*

---

### What to Do With Your Score

There is no score. Instead:

| If you missed | Reread |
|---|---|
| Q1 | L25 §3 |
| **Q2, Q3** | **L26 §3–§4** — and you sat Lab 8 yesterday; go back to the `.got.plt` bytes |
| Q4 | L26 §5 |
| **Q5, Q6** | **L27 §3** — these two are PS 8's Q4, due Friday |
| Q7 | L27 §4 |

**Q6 is the one that recurs**, and this week it recurs immediately: L28 opens with a compiler flag buying 19% where an algorithm change bought 60×, and L30 §5 lists the three separate times this course has deleted its own benchmark.

---

*PROG 201 · Week 9 · Quiz 9 · covers Week 8 · ungraded*
