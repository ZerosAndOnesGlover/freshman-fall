# PROG 201 · Systems Programming in C
## Week 8 · Lecture 3 of 3
### Interposition, `dlopen`, and Versioning

*“Compatibility means deliberately repeating other people's mistakes.”* — David Wheeler

---

**Reading:** TLPI Ch. 42 · CS:APP §7.13 · `man 3 dlopen`, `man 8 ld.so`, `man 1 gcc` (visibility) · **Previous:** L26 · **Next:** Lab 8 — a plugin system, **Monday of Week 9**

**Coursework:** 📝 **PS 7** due Fri this week 17:00 · 🔬 **Lab 8** Mon of Week 9 15:00–16:50 · 📊 **Quiz 9** Tue of Week 9 · 📝 **PS 9** released Wed of Week 9, due Fri of Week 10 17:00

---

## 1. Search Order Is a Feature

When `ld.so` needs a symbol it searches, in order:

1. the **executable** itself;
2. every library named by **`LD_PRELOAD`**, in order;
3. the `DT_NEEDED` libraries, breadth-first;
4. anything `dlopen`ed with `RTLD_GLOBAL`.

**The first definition found wins**, and every later one is ignored. That rule is called **interposition**, and it is not a loophole — it is the mechanism `LD_PRELOAD` exists to expose.

Twelve lines replace `time()` in any program on the system:

```c
#include <time.h>
#include <stdlib.h>
time_t time(time_t *t)
{
    time_t fixed = 1000000000;
    const char *e = getenv("FAKE_TIME");
    if (e) fixed = (time_t) atoll(e);
    if (t) *t = fixed;
    return fixed;
}
```

```
$ ./usetime
time() = 1788905799 -> Tue Sep  8 23:16:39 2026
$ LD_PRELOAD=./faketime.so ./usetime
time() = 1000000000 -> Sun Sep  9 02:46:40 2001
$ FAKE_TIME=0 LD_PRELOAD=./faketime.so ./usetime
time() = 0 -> Thu Jan  1 01:00:00 1970
```

**No recompilation, no source, no cooperation from the program.** `LD_DEBUG=bindings` confirms where the call went:

```
binding file ./usetime to faketime.so: normal symbol `time' [GLIBC_2.2.5]
```

This is how `faketime`, `tsocks`, `libeatmydata`, most memory profilers and a great deal of testing infrastructure work.

**And it is why `ld.so` ignores `LD_PRELOAD` for set-user-ID binaries** (L25 §4). Without that rule, interposing `getuid` would be a two-line privilege escalation.

---

## 2. Calling the Original: `RTLD_NEXT`

A replacement usually wants to do its own work and then call the real function. `dlsym(RTLD_NEXT, name)` means *"find this symbol in the search order **after** me"*:

```c
static void *(*real_malloc)(size_t);

void *malloc(size_t n)
{
    if (!real_malloc) real_malloc = dlsym(RTLD_NEXT, "malloc");
    void *p = real_malloc(n);
    count++;
    return p;
}
```

**There is a bootstrapping problem in those four lines, and it is the whole difficulty of writing one of these.** `dlsym` itself may allocate — so the first call to `malloc` calls `dlsym`, which calls `malloc`, which calls `dlsym`. Two fixes, and real profilers use both:

- **A recursion flag**, `__thread int inside`, so a nested call takes a different path;
- **a small static bootstrap arena** that satisfies allocations made before `real_malloc` is known. Its blocks must never be passed to the real `free`, so `free` has to recognise them by address.

Get this wrong and the symptom is a segfault before `main`, which is a confusing place to start debugging.

---

## 3. Three Things `LD_PRELOAD` Cannot Do

All three were measured, and all three are the difference between a tool that works and a tool that quietly reports nothing.

**It cannot intercept a call the compiler removed.** A test program with 1,000 `malloc(128)`/`free` pairs, built `-O2`:

```
$ objdump -d leaky | grep -c '<malloc@plt>'
0
$ nm -D --undefined-only leaky | grep -c malloc
0
```

**GCC deleted every allocation** — the C standard lets it, since the pointers are unused — so `malloc` is not merely uncalled, it is **not a symbol the binary references at all**. The profiler reported 2 allocations, both from stdio. The same source at `-O0` reports **1,012 mallocs, 1,000 frees, 12 never freed**, which is correct.

**It cannot intercept a different symbol that does the same job.** The `time()` interposition above works on our program and **does nothing to `date(1)`**, which prints the real time — because `date` calls `clock_gettime`, which on Linux is resolved through the **vDSO** and never enters libc's PLT at all.

**It cannot rely on a destructor to report.** `__attribute__((destructor))` runs when `ld.so` runs the fini functions, and that does not always happen:

```
/usr/bin/true      [probe] ctor  [probe] dtor
python3 -c pass    [probe] ctor  [probe] dtor
/usr/bin/ls /etc   [probe] ctor
/usr/bin/grep ...  [probe] ctor
```

`LD_DEBUG=all` confirms it: for `true`, `ld.so` prints `calling fini` for every object; **for `ls` it prints none at all.** Interposing `_exit` does not help, because a library's internal calls do not go through the PLT.

**So a `LD_PRELOAD` tool that prints its report from a destructor silently prints nothing for some perfectly ordinary programs.** Write incrementally to a file, or verify the exit path for the program you actually care about. This is PS 8's Q4, and it is the same shape as every "the absence of output is not a result" finding this term.

---

## 4. `dlopen`: Choosing Code at Run Time

```c
void *h = dlopen("./plugin.so", RTLD_NOW | RTLD_LOCAL);
void *sym = dlsym(h, "prog201_plugin");
dlclose(h);
```

The flags matter:

| Flag | Meaning |
| --- | --- |
| **`RTLD_NOW`** | resolve everything now; **fail here** rather than crashing on a later call |
| `RTLD_LAZY` | resolve on first use — an unresolved symbol becomes a crash, later, somewhere else |
| **`RTLD_LOCAL`** (default) | this library's symbols are **not** visible to later `dlopen`s |
| `RTLD_GLOBAL` | they are — which means this plugin can now interpose on the next one |

**Use `RTLD_NOW | RTLD_LOCAL` for plugins.** `RTLD_NOW` turns "a broken plugin crashes the host an hour later" into "the plugin fails to load"; `RTLD_LOCAL` stops two plugins that happen to define the same helper from silently sharing one.

### The error-checking rule nobody follows

**`dlsym` can legitimately return `NULL`** — a symbol's value may be zero. So the return value is not the error indicator:

```c
dlerror();                                  /* clear any stale error   */
void *sym = dlsym(h, "prog201_plugin");
const char *err = dlerror();                /* THIS is the test        */
if (err) { ... }
```

`dlerror` also **clears itself when read**, so a stale message from an earlier failure will be attributed to this call if you do not clear it first.

---

## 5. The Plugin Pattern

A plugin should export **one** symbol — a struct of everything the host needs — rather than a dozen functions the host looks up by name. It makes the interface a single thing to version:

```c
#define PROG201_PLUGIN_ABI 1

struct plugin {
    int         abi;
    const char *name;
    const char *description;
    int       (*init)(void);
    long      (*apply)(long x);
    void      (*fini)(void);
};
```

and the host checks the ABI **before** calling anything:

```
$ ./host ./p_double.so ./p_square.so ./p_bad.so ./p_missing.so
  [double] init
  [square] init
./p_bad.so: ABI 0, this host wants 1 -- refusing
dlopen ./p_missing.so: cannot open shared object file: No such file or directory
loaded double    multiply by two
loaded square    x squared

loading 2 plugin(s) took 0.232 ms

  double   apply(7) = 14
  square   apply(7) = 49
```

**Three things that separate a plugin system from a `dlopen` call:**

- **An ABI number, checked first.** Without it, a plugin built against an older struct layout is a crash inside your host with your name on the stack trace.
- **`dlclose` in reverse order**, after each plugin's `fini`. And know that `dlclose` **may not actually unload** — if anything still references the library it stays, and a plugin with thread-local storage or a registered `atexit` handler often keeps it alive.
- **Nothing in the host's symbol table the plugin can accidentally match.** `RTLD_LOCAL` plus `-fvisibility=hidden` in the plugin (§7).

---

## 6. Symbol Versioning

`libc.so.6` has been binary compatible since 1997. It manages that by holding **several versions of the same symbol at once**:

```
$ nm -D --with-symbol-versions /lib/x86_64-linux-gnu/libc.so.6 | grep memcpy@
  memcpy@GLIBC_2.2.5          <- old behaviour, for old binaries
  memcpy@@GLIBC_2.14          <- the DEFAULT for anything linked now
```

The `@@` marks the default: a program linked today gets `GLIBC_2.14`, and a binary from 2010 that recorded a dependency on `GLIBC_2.2.5` still gets exactly the function it was built against. `readelf -V` shows **41 version definitions** in this libc, and `pthread_cond_wait` and `realpath` have the same treatment.

**This is why a binary built on an old distribution runs on a new one and not the other way round.** The new libc still contains the old versions; the old libc does not contain the new ones, and the error is the familiar

```
./prog: /lib/x86_64-linux-gnu/libc.so.6: version `GLIBC_2.34' not found
```

**The other half of versioning is the `SONAME`.** A library's `DT_SONAME` is what gets recorded in programs that link against it — `libgreet.so.1`, not `libgreet.so`. The convention:

| | meaning |
| --- | --- |
| `libfoo.so` | the **link-time** name, a symlink, in the `-dev` package |
| `libfoo.so.1` | the **SONAME** — bump it when the ABI breaks |
| `libfoo.so.1.4.2` | the actual file |

**Change a struct's layout or a function's signature and you must bump the SONAME.** Adding a function does not require it. Getting this wrong is how a distribution upgrade breaks every program at once.

---

## 7. Constructors, Destructors, and Order

```c
__attribute__((constructor)) static void setup(void) { ... }
__attribute__((destructor))  static void teardown(void) { ... }
```

They run around `main`, and the order is not arbitrary:

```
$ ./order                        # links -la -lb, and a preload
  ctor b
  ctor a
  [probe] ctor                   <- LD_PRELOAD, after the NEEDED libraries
  ctor main
  --- main ---
  dtor main
  [probe] dtor
  dtor a
  dtor b
```

**Dependencies are constructed first and destructed last**, and the destructor order is the exact reverse of the constructor order. Within one library, `__attribute__((constructor(priority)))` orders them.

Three rules:

- **A constructor runs before `main`, so nothing in your program is initialised yet.** Calling into your own code from one is a way to use uninitialised globals.
- **A destructor may not run at all** — §3, measured.
- **Constructors in `dlopen`ed libraries run during the `dlopen` call**, which is why a plugin's `init` in §5 is a better place for real work: it can fail and report, and a constructor cannot.

### Visibility

By default every non-`static` symbol in a shared library is exported, which is slow to resolve, easy to collide with, and impossible to change later without breaking somebody. The fix is two things together:

```
gcc -fvisibility=hidden ...
__attribute__((visibility("default"))) int the_one_symbol_i_export;
```

**Hidden by default, exported deliberately.** It shrinks the dynamic symbol table, speeds up loading, and — most usefully — means the set of things you have promised not to break is written down in your source rather than implied by which functions you forgot to mark `static`.

---

## Summary

- **The first definition found wins**, and `LD_PRELOAD` is second in the search order — so twelve lines replace `time()` in any program. `ld.so` ignores it for set-user-ID binaries.
- **`dlsym(RTLD_NEXT, ...)`** calls the original, and bootstrapping it needs a recursion flag and a static arena, because `dlsym` may allocate.
- **Three measured limits:** `-O2` **deleted all 1,010 malloc/free pairs** so there was nothing to intercept; interposing `time` does nothing to `date`, which calls `clock_gettime` through the **vDSO**; and `ld.so` runs no destructors at all for `ls` and `grep`, so a destructor-based report silently prints nothing.
- **`dlopen` with `RTLD_NOW | RTLD_LOCAL`.** Check `dlerror`, not `dlsym`'s return value, and clear it first.
- A plugin exports **one struct with an ABI number**, checked before anything is called. `dlclose` may not unload.
- **Symbol versioning** lets one `libc.so.6` hold `memcpy@GLIBC_2.2.5` and `memcpy@@GLIBC_2.14`. 41 versions in this one. It is why old binaries run on new systems and not the reverse.
- **Bump the SONAME when the ABI breaks.**
- Constructors run **dependencies first**, destructors in exact reverse; a `dlopen`ed library's constructor runs inside `dlopen`. Compile plugins `-fvisibility=hidden`.

---

## Exercises

1. Interpose `open()` and log every path a program opens. Run it on `ls`, `cat` and `python3`. Which of the three surprises you?
2. Write the `malloc` interposer **without** the recursion guard and describe exactly how it fails. Then add the guard and keep the failing version in your notes.
3. Interpose `getuid` to return 0 and run something that checks it. Now make that program set-user-ID and try again. What did `ld.so` do?
4. `dlopen` a library twice without `dlclose`ing it. How many times does its constructor run, and what does that tell you about the reference count?
5. Build `libgreet.so.1` with a `SONAME`, link against it, then build an incompatible `libgreet.so.2`. What does the program do when only version 2 is installed?
6. Give a library two functions with the same name and different versions using a version script. Prove with `nm -D --with-symbol-versions` that both are there.
7. Compile a library with and without `-fvisibility=hidden` and compare `nm -D --defined-only | wc -l`. How much of your library was public by accident?

---

*PROG 201 · Week 8 · L27 · © CSE Department*
