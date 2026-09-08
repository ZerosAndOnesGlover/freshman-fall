# PROG 201 · Lab 8 Solutions
## A Plugin System with `dlopen` — Instructor Only

---

**Do not distribute.** Part C's three interposition results are PS 8's Q4, and Part A(b)'s GOT bytes are the lab's best moment.

**Machine these numbers came from:** Linux 7.0.0-30-generic, gcc 13.3.0, **glibc 2.39**, Ubuntu 24.04. The glibc version matters twice: `libdl`/`libpthread`/`librt` are merged into `libc.so.6` since 2.34, and Ubuntu's default `-Wl,-z,relro,-z,now` is why Part A(c) needs a second binary.

---

## 1. The Three TODOs

The scaffolding — `plugin.h`, the three plugins, the `loaded` table, `main`'s argument handling and the timing — is provided.

```c
static int load(const char *path)
{
    if (nloaded >= MAXP) { fprintf(stderr, "too many plugins\n"); return -1; }
    dlerror();                                     /* clear any stale error */
    void *h = dlopen(path, RTLD_NOW | RTLD_LOCAL);
    if (!h) { fprintf(stderr, "dlopen %s: %s\n", path, dlerror()); return -1; }

    /* dlsym can legitimately return NULL, so check dlerror, not the pointer */
    dlerror();
    struct plugin *p = dlsym(h, "prog201_plugin");
    const char *err = dlerror();
    if (err) { fprintf(stderr, "%s: no prog201_plugin: %s\n", path, err); dlclose(h); return -1; }

    if (p->abi != PROG201_PLUGIN_ABI) {
        fprintf(stderr, "%s: ABI %d, this host wants %d -- refusing\n",
                path, p->abi, PROG201_PLUGIN_ABI);
        dlclose(h); return -1;
    }
    if (p->init && p->init() != 0) {
        fprintf(stderr, "%s: init failed\n", path); dlclose(h); return -1;
    }
    loaded[nloaded].handle = h;
    loaded[nloaded].p = p;
    nloaded++;
    printf("loaded %-8s  %s\n", p->name, p->description);
    return 0;
}

/* ---- and the end of main(): TODO 3 then TODO 2 ---- */

    for (int i = 0; i < nloaded; i++)
        printf("  %-8s apply(%ld) = %ld\n", loaded[i].p->name, x, loaded[i].p->apply(x));

    printf("\n");
    for (int i = nloaded - 1; i >= 0; i--) {
        if (loaded[i].p->fini) loaded[i].p->fini();
        dlclose(loaded[i].handle);
    }```

Builds clean under `gcc -Wall -Wextra -O2 -g -std=c11 -o host host.c -ldl`.

---

## 2. Where Students Get Stuck

| # | Symptom | Cause | What to say |
| --- | --- | --- | --- |
| 1 | `dlsym` "works" but the plugin does nothing | Checked the return value instead of `dlerror` | Q4. It is in the man page's first NOTE |
| 2 | A stale error attributed to the wrong plugin | `dlerror()` not cleared before `dlsym` | Same place, next sentence |
| 3 | `p_bad.so` loads and then segfaults | The ABI checked after `init` was called | The struct layout changed; the pointer is not where you think |
| 4 | Their own plugin: "undefined symbol: prog201_plugin" | `PROG201_EXPORT` omitted, with `-fvisibility=hidden` | `nm -D` shows an empty list. **This is Q5 arriving early** |
| 5 | `fini` runs for the wrong plugin, or twice | Unload loop forward rather than reverse, or `dlclose` before `fini` | Reverse order, `fini` first |
| 6 | Part A(b): the `.got.plt` values look like nothing | Read the non-lazy binary | Only `useglib_lazy` has PLT-pointing slots |

**Symptom 4 is the most valuable one in the session.** A student who hits it has discovered visibility by walking into it, and the fix is one macro — send them to `nm -D` rather than telling them.

---

## 3. Reference Output

**Part A(a):**

```
  INTERP  [Requesting program interpreter: /lib64/ld-linux-x86-64.so.2]
 (NEEDED)  Shared library: [libgreet.so]
 (NEEDED)  Shared library: [libc.so.6]

	linux-vdso.so.1 (0x00007e15249a1000)          <- not a file
	libgreet.so => ./libgreet.so
	libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6
	/lib64/ld-linux-x86-64.so.2

0000000000003fc0 R_X86_64_JUMP_SLOT  farewell@Base
0000000000003fc8 R_X86_64_JUMP_SLOT  greet@Base
```

**Part A(b) — the non-lazy PLT:**

```
0000000000001080 <greet@plt>:
    1080:  endbr64
    1084:  jmp    *0x2f3e(%rip)        # 3fc8 <greet@Base>
```

**and the lazy one, which is the lab:**

```
0000000000001020 <.plt>:                       ; PLT[0]
    1020:  push   0x23ba(%rip)        # GOT+8
    1026:  jmp    *0x23bc(%rip)       # GOT+16
    1030:  endbr64                    ; PLT[1] = farewell
    1034:  push   $0x0
    1039:  jmp    1020 <.plt>
    1040:  endbr64                    ; PLT[2] = greet
    1044:  push   $0x1
    1049:  jmp    1020 <.plt>

$ readelf -x .got.plt useglib_lazy
  0x000033f0 30100000 00000000 40100000 00000000
             ^^^^^^^^ = 0x1030          ^^^^^^^^ = 0x1040
$ objdump -R useglib_lazy | grep JUMP_SLOT
00000000000033f0 R_X86_64_JUMP_SLOT  farewell@Base
00000000000033f8 R_X86_64_JUMP_SLOT  greet@Base
```

**The GOT slot for `farewell` (0x33f0) contains 0x1030 — the address of `farewell`'s own PLT entry.**

**Part A(c):**

```
=== LAZY ===
>>> about to call greet the first time
   binding file ./useglib_lazy to libgreet.so: normal symbol `greet'
greet(10)    = 21
>>> about to call greet the second time
greet(20)    = 41
>>> about to call farewell the first time
   binding file ./useglib_lazy to libgreet.so: normal symbol `farewell'
farewell(10) = 9

=== the default build ===
   binding file ./useglib to libgreet.so: normal symbol `farewell'
   binding file ./useglib to libgreet.so: normal symbol `greet'
>>> about to call greet the first time
...

$ readelf -d useglib | grep -E "BIND_NOW|FLAGS"
 (FLAGS)    BIND_NOW
 (FLAGS_1)  Flags: NOW PIE
```

**Part B:**

```
  [double] init
  [square] init
loaded double    multiply by two
loaded square    x squared

loading 2 plugin(s) took 0.211 ms

  double   apply(7) = 14
  square   apply(7) = 49

  [square] fini
  [double] fini
```

```
./p_bad.so: ABI 0, this host wants 1 -- refusing
dlopen ./p_missing.so: ./p_missing.so: cannot open shared object file: No such file or directory
```

and `nm -D --defined-only p_double.so` prints **exactly one line**.

**Part C:**

```
$ ./usetime
time() = 1788905799 -> Tue Sep  8 23:16:39 2026
$ LD_PRELOAD=$PWD/faketime.so ./usetime
time() = 1000000000 -> Sun Sep  9 02:46:40 2001
$ LD_PRELOAD=$PWD/faketime.so date
Tue Sep  8 11:16:39 PM WAT 2026            <- unaffected

/usr/bin/true      [probe] ctor  [probe] dtor
python3 -c pass    [probe] ctor  [probe] dtor
/usr/bin/ls /etc   [probe] ctor
/usr/bin/grep ...  [probe] ctor
```

---

## 4. Answers

**Q1 — the entry that is not a file.**

**`linux-vdso.so.1`** — the virtual dynamic shared object. **The kernel maps it into every process**; there is no such file on disk and `find / -name 'linux-vdso*'` returns nothing.

It holds `clock_gettime`, `gettimeofday`, `getcpu` and `time`, implemented **without a system call** — they read a page of kernel-maintained data directly. That is why `clock_gettime` costs a few nanoseconds where Week 4 measured `getpid()` at **574 ns**.

**Q2 — the GOT slot pointing into the PLT.**

It points at **its own PLT entry**, one instruction past the start (`0x1030` for `farewell`, whose stub begins at `0x1030` with `endbr64` and continues `push $0x0`).

First call: `call farewell@plt` → the stub's `jmp *GOT` → the GOT sends control **back into the stub** → `push $0x0` (the relocation index) → `jmp PLT[0]` → `push GOT+8` (the link map) → `jmp *GOT+16` (`_dl_runtime_resolve`) → the resolver finds `farewell`, **writes its address into the GOT slot**, and jumps to it.

Second call: `jmp *GOT` now goes straight to `farewell`. The stub is never re-entered.

Full marks require the write-back. A student who describes the first call and stops has [3 of 5].

**Q3 — the two orderings.**

**Lazy**: each symbol binds at its first call, and the second call to `greet` binds nothing. **`BIND_NOW`**: both bind before `main` produces any output.

The flag is **`-z now`** (with `-z relro` making the pair "full RELRO"), and Ubuntu passes it by default.

**Why it is the default: a writable GOT is a target.** Any bug allowing a write to a chosen address can redirect a GOT entry, so the next call to `printf` goes wherever the attacker said. Full RELRO resolves everything up front and then `mprotect`s the GOT read-only, so there is nothing to overwrite. It costs startup time for symbols that are never called — a trade every distribution has now made.

**Q4 — `dlerror`, not the return value.**

**`dlsym` can legitimately return `NULL`**, because a symbol's *value* may be zero — a global initialised to 0, or a weak symbol that is deliberately absent. So `NULL` is a valid result and not an error indicator.

`dlerror` must be called **before** as well as after, because it reports the last error and **clears itself when read**. If an earlier `dlopen` failed and nobody read the message, your `dlsym` will be blamed for it.

**Q5 — one exported symbol.**

The Makefile compiles plugins with **`-fvisibility=hidden`**, which makes every symbol hidden unless marked, and `plugin.h` defines `PROG201_EXPORT` as `__attribute__((visibility("default")))` for the one that must not be.

Two reasons of any of: a smaller dynamic symbol table, so loading is faster (symbol lookup is proportional to table size); **the ABI you have promised not to break is now written down** rather than being "whatever I forgot to mark `static`"; no accidental collisions between two plugins' helpers; and the compiler can optimise hidden functions better, since it knows nothing outside can interpose them.

**Q6 — why `date` was unaffected.**

**`date` does not call `time()`.** It calls **`clock_gettime`**, which on Linux is resolved through the **vDSO** — so it neither enters libc's PLT nor makes a system call, and there is nothing for an `LD_PRELOAD` library to sit in front of.

The general rule: **interposition catches the symbol you interposed, and only that one.** A program that reaches the same functionality by a different route is untouched, and the vDSO is the most common such route.

**Q7 — destructors.**

`true` and `python3` ran it; **`ls` and `grep` did not**. `LD_DEBUG=all` confirms: for `true` the loader prints `calling fini` for every object; **for `ls` it prints none**.

What it means: **a `LD_PRELOAD` tool that reports from a destructor silently reports nothing for some perfectly ordinary programs** — and gives no indication that it has done so, which is the worst possible failure mode for a measuring tool.

A way to write one that does not have the problem, any of: write incrementally to a file or fd as you go, so a partial result survives; interpose `exit`/`_exit` **and** keep the destructor, taking whichever fires first (guard against reporting twice); or `atexit` from a constructor, which has the same limitation but is at least explicit.

**Q8 — two `RTLD_GLOBAL` plugins.**

The first one loaded wins: the second plugin's calls to its own `helper` bind to the **first plugin's** definition, silently, and the symptom is a plugin behaving as though it had somebody else's code in it — which it does.

---

## 5. Checkoff

The four boxes are in the lab sheet. In practice:

- **Part A(b) is the lab.** Make them point at the hex bytes and the disassembly on the same screen. It is the moment lazy binding stops being a diagram.
- **Q3's "why is it the default" is the security half**, and it is worth saying out loud that Week 10 is the attack this prevents.
- **Part C(c) is PS 8's Q4** and takes four minutes. Do not let a pair skip it — it is due Friday.
- The extension (hot reloading) is genuinely surprising: `dlclose` frequently does **not** unload, and the second `dlopen` returns the same handle with the old code still in it.

**Timing.** Setup 5, Part A 25, Part B 40, Part C 25 — 95 against 110. **Part A can be shortened** by giving out the disassembly on paper, but Part B cannot: three TODOs is the right amount of typing for one session and no more.

---

*PROG 201 · Week 8 · Lab 8 Solutions · Instructor Only · © CSE Department*
