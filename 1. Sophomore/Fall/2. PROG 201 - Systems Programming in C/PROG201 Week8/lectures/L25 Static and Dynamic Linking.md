# PROG 201 · Systems Programming in C
## Week 8 · Lecture 1 of 3
### Static and Dynamic Linking

---

**Reading:** CS:APP Ch. 7 · TLPI Ch. 41–42 · `man 8 ld.so`, `man 1 ld`, `man 1 readelf` · **Previous:** L24 · **Next:** L26 — the GOT, the PLT and PIC

---

## 1. Where Week 6's 147 Microseconds Went

L19 §4 measured the cost of running a command and found something it did not explain:

| | per command |
| --- | --- |
| a trivial **statically** linked binary | **532.4 µs** |
| the same source, **dynamically** linked | **679.3 µs** |

**One hundred and forty-seven microseconds, 22%, for a program that does nothing.** This week is what happens in that gap, and it is a program you have never run explicitly: **the dynamic linker**.

Repeated here as a whole-process measurement, 1,000 `fork`+`exec`+`wait` cycles of a `int main(void){return 0;}`:

| | µs per process |
| --- | --- |
| static | 503, 571, 750 |
| dynamic | 852, 881, 948 |

The spread is wide — this is a whole process creation and the machine is not quiet — but **the direction is the same in every paired run**, and it is a few hundred microseconds.

What you get for it is §2.

---

## 2. What Linking Is

A compiler turns each `.c` into a `.o` with **holes** in it: places where an address will go, and a note saying which symbol goes there. Those notes are **relocations**.

```
$ objdump -R useglib
OFFSET            TYPE                 VALUE
0000000000003fc0  R_X86_64_JUMP_SLOT   farewell@Base
0000000000003fc8  R_X86_64_JUMP_SLOT   greet@Base
0000000000003fd8  R_X86_64_GLOB_DAT    __libc_start_main@GLIBC_2.34
```

**Linking is filling in the holes.** The only question is *when*:

| | when | what you ship |
| --- | --- | --- |
| **Static** | at build time, by `ld` | one file, containing every library routine you used |
| **Dynamic** | at **load** time, by `ld.so` | your code, plus a list of libraries you need |

The difference is visible immediately:

```
hello_dyn         16056 bytes
hello_sta        785232 bytes
```

**Forty-nine times**, for a program whose source is three lines. The static binary contains `printf`, its formatting machinery, `malloc`, the locale tables `printf` consults, and everything those pull in.

---

## 3. The Interpreter

A dynamically linked ELF file names its own loader, in a program header:

```
$ readelf -l hello_dyn | grep -A1 INTERP
  INTERP  0x318 ... 0x1c
      [Requesting program interpreter: /lib64/ld-linux-x86-64.so.2]
```

**`execve` reads that and runs `ld.so` instead of your program.** The dynamic linker maps your executable and its libraries, resolves the relocations, runs the initialisers, and *then* jumps to your entry point. Your `main` runs several thousand instructions into the process's life.

The list of what it must find is also in the file:

```
$ readelf -d hello_dyn | head -3
 0x0000000000000001 (NEEDED)   Shared library: [libc.so.6]
 0x000000000000000c (INIT)     0x1000
 0x0000000000000019 (INIT_ARRAY) 0x3db0
```

`ldd` is the readable version, and it works by **running the program with a special environment variable** rather than by parsing it — which is why `ldd` on an untrusted binary is a bad idea, and why `readelf -d` is what you should use on one:

```
$ ldd hello_dyn
	linux-vdso.so.1 (0x00007e15249a1000)
	libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007e1524600000)
	/lib64/ld-linux-x86-64.so.2 (0x00007e15249a3000)
```

**Three entries and only one is a file you asked for.** `linux-vdso.so.1` is not on disk at all — the kernel maps it into every process, and it holds fast implementations of `gettimeofday`, `clock_gettime` and `getcpu` that run **without a system call**. It is the reason `clock_gettime` costs nanoseconds and `getpid` costs 574 (Week 4 L15 §3).

---

## 4. How `ld.so` Finds a Library

In order, and the order is the whole of "why does it load the wrong one":

1. **`DT_RPATH`** in the executable — deprecated;
2. **`LD_LIBRARY_PATH`** — the environment variable;
3. **`DT_RUNPATH`** in the executable — the modern form, and unlike `RPATH` it does **not** apply to the library's own dependencies;
4. the cache, **`/etc/ld.so.cache`**, built by `ldconfig` from `/etc/ld.so.conf`;
5. the default directories, `/lib` and `/usr/lib`.

`$ORIGIN` in a `RUNPATH` expands to the directory of the object being loaded, which is how a program ships private libraries next to itself:

```
gcc -o useglib useglib.c -L. -lgreet -Wl,-rpath,'$ORIGIN'
```

**Two rules worth having.** `LD_LIBRARY_PATH` is a debugging tool and not a deployment mechanism — it applies to every program you then run, including the ones that did not want it. And **`ld.so` ignores `LD_LIBRARY_PATH` and `LD_PRELOAD` for set-user-ID programs**, which is the only thing standing between interposition (L27) and trivially becoming root.

---

## 5. What Dynamic Linking Buys

**Disk and memory.** One `libc.so.6` on disk, and — the part that matters — **one copy in physical memory shared by every process**, because it is mapped `MAP_PRIVATE` from the same file (Week 4 L13 §2). A machine running two hundred processes has one copy of libc's text.

**Updates.** A security fix in libc fixes every program at once. With static linking, every program that used the vulnerable routine must be rebuilt and redistributed — which is a supply-chain problem rather than a technical one, and is the strongest argument against static linking in a distribution.

**Plugins.** Code chosen at run time rather than at build time, which is L27 and Lab 8.

**Interposition.** Replacing a function in somebody else's program without their source, which is L27 and PS 8.

## And what it costs

**Startup time** — §1's few hundred microseconds, which matters for a program you run a million times and not at all for one you run once.

**A dependency on the environment.** A static binary runs anywhere; a dynamic one needs the right libraries with the right versions in the right places. "Works on my machine" is very often this.

**An indirection on every call and every global** — L26.

**And a class of failure that does not exist otherwise:** the wrong library, silently. §4's search order is five deep, and nothing warns you when step 2 wins.

---

## 6. The Libraries That Are Not There Any More

```
$ ls /usr/lib/x86_64-linux-gnu/libdl.so /usr/lib/x86_64-linux-gnu/libpthread.so
(neither exists)
```

**Since glibc 2.34, `libdl`, `libpthread`, `librt` and `libutil` have been merged into `libc.so.6`.** The `-ldl`, `-lpthread` and `-lrt` on your command lines all term have been no-ops, kept because they are harmless and because older systems need them.

Two consequences:

- **`dlopen` no longer needs `-ldl`** and `pthread_create` no longer needs `-lpthread` — but a program built without them will not run on an older glibc, so keep them.
- Week 3's observation that `<threads.h>` works without `-pthread` is the same change.

**This is what library versioning is for**, and §7 of L27 is how a single `libc.so.6` can contain `GLIBC_2.2.5` and `GLIBC_2.34` versions of the same symbol at once.

---

## 7. Static Linking Is Not Dead

It went away and came back, and the arguments are worth knowing because they are current:

**For:** one file to deploy, no version skew, no `ld.so` at startup, and — the modern reason — **a container image that is one binary**, with no distribution inside it. Go statically links by default and produces exactly that.

**Against:** the supply-chain problem in §5; larger binaries; **NSS**, where glibc's `getpwnam` and `gethostbyname` `dlopen` their backends at run time, so a "static" glibc binary is not static and warns you about it; and licensing, since static linking against an LGPL library has obligations that dynamic linking does not.

**The compromise most systems have settled on**: dynamic for the base system, static for shipped applications, and `musl` rather than glibc when you want static to actually mean static.

---

## Summary

- **Linking is filling in holes**, and the only question is whether it happens at build time or at load time.
- Static: **785,232 bytes** against dynamic's **16,056** for the same three-line program — 49×.
- A dynamic executable names its own **interpreter** in an `INTERP` header, and `execve` runs that instead. Your `main` starts thousands of instructions into the process.
- **`linux-vdso.so.1` is not a file** — the kernel maps it in, and it is why `clock_gettime` needs no system call.
- The library search order is **`RPATH`, `LD_LIBRARY_PATH`, `RUNPATH`, `ld.so.cache`, defaults** — and `ld.so` ignores the environment ones for set-user-ID programs.
- Dynamic linking buys **shared memory, one-place updates, plugins and interposition**; it costs **a few hundred microseconds of startup**, a dependency on the environment, an indirection per call, and a way to load the wrong library silently.
- **Since glibc 2.34 there is no `libdl`, `libpthread` or `librt`** — they are inside `libc.so.6`.

---

## Exercises

1. Build the same program statically and dynamically and compare `size`, `readelf -d`, and `nm -D --undefined-only`. Which symbols does the dynamic one need and the static one does not?
2. `ldd /usr/bin/python3`. How many of those libraries does your own code call into, and how many are dependencies of dependencies?
3. Put a `libgreet.so` in two directories with different behaviour and make each one win, by `LD_LIBRARY_PATH` and by `RUNPATH`. Which beats which?
4. `LD_DEBUG=libs ./yourprogram`. Count the directories `ld.so` tried before it found libc, and explain the order from §4.
5. Time a static and a dynamic build of the same program over 1,000 executions. Is your gap the same shape as §1's, and what else is in your number?
6. `strace -e trace=openat ./hello_dyn`. Which files did the dynamic linker open that the static one did not?
7. Write a program that calls `clock_gettime` in a loop and `strace` it. How many system calls do you see, and what does that tell you about the vDSO?

---

*PROG 201 · Week 8 · L25 · © CSE Department*
