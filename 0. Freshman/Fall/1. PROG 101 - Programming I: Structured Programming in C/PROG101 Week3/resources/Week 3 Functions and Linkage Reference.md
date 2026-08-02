# PROG 101 · Week 3 Reference
## Functions · The Call Stack · Scope, Linkage, and Multi-File Programs

---

## Part 1: Declaration vs Definition

```c
int  gcd(int a, int b);              /* declaration — a promise            */
int  gcd(int a, int b) { ... }       /* definition  — the actual code      */
```

| | Declaration | Definition |
|---|---|---|
| States the type | ✅ | ✅ |
| Allocates code | ❌ | ✅ |
| How many allowed | many | **exactly one** |
| Needed by | the **compiler**, to check the call | the **linker**, to resolve it |

**"It compiled" is not "it will link."** A declaration alone gets you through compilation; the
definition must exist somewhere at link time.

---

## Part 2: Pass by Value — The Most Important Rule in C

> **Every argument is copied.** A function receives values, never variables.

```c
void try_modify(int x) { x = 999; }   /* modifies the copy, nothing else */
```

Verified: `&v = 0x7ffcf6d2b0d4` in the caller, `&x = 0x7ffcf6d2b0bc` in the callee — **24 bytes
apart, therefore different objects**. Writing through `x` cannot reach `v`.

This is why `swap(int a, int b)` cannot work, and why Week 5 needs pointers: to modify the caller's
variable you must be handed **its address**, which is itself passed by value.

---

## Part 3: The Call Stack

Each call pushes a **frame** holding parameters, locals, the saved return address, and the saved
frame pointer.

Verified on x86-64 Linux:

```
main      &m = 0x7fffc8b620b4
level1    &a = 0x7fffc8b62094      ← 32 bytes lower
 level2   &b = 0x7fffc8b62074      ← 32 bytes lower
  level3  &c = 0x7fffc8b62054      ← 32 bytes lower
```

| Fact | Detail |
|---|---|
| Direction | Grows **downward** (toward lower addresses) |
| Frame size here | 32 bytes for one `int` — the rest is return address, saved frame pointer, alignment |
| Between runs | Absolute addresses **change** (ASLR); the *differences* do not |
| Capacity | Finite — typically **8 MiB** (`ulimit -s` reports `8192` KiB) |
| On exhaustion | **SIGSEGV**, exit status 139 |

**Unbounded recursion segfaults; an unbounded `while` loop does not** — the loop reuses one frame,
recursion allocates a new one per call.

### In GDB

```
break f | run | backtrace | info frame | frame N | info locals
```

`backtrace` lists frames innermost-first: `#0` is the deepest call, the last frame is `main`.

---

## Part 4: Scope, Storage Duration, and Linkage — Three Different Things

| Declaration | Scope | Storage duration | Linkage |
|---|---|---|---|
| `int x;` in a function | block | automatic (per call) | none |
| `static int x;` in a function | **block** | **static** (whole run) | none |
| `int x;` at file level | file | static | **external** |
| `static int x;` at file level | file | static | **internal** |

**`static` means two different things depending on where it appears.**

- **Inside a function** it changes the *lifetime*, not the visibility. Verified: `static int n = 0; return ++n;`
  yields 1, 2, 3, 4 on successive calls, while the automatic version yields 1 every time. The name is
  invisible outside the function in **both** cases.
- **At file level** it changes the *linkage*, making the name invisible to other translation units.

Static objects are initialised **once**, before `main`, and zero-initialised by default.

---

## Part 5: Multi-File Programs

### Header discipline

```c
#ifndef STATS_H          /* include guard — required */
#define STATS_H

double mean(const double *v, int n);

#endif
```

**Headers contain declarations; `.c` files contain definitions.** Without an include guard, a header
included twice re-declares everything — harmless for functions, fatal for type definitions.

### Separate compilation

```
gcc -Wall -Wextra -Werror -pedantic -std=c11 -c stats.c -o stats.o
gcc -Wall -Wextra -Werror -pedantic -std=c11 -c main.c  -o main.o
gcc stats.o main.o -o prog
```

### `static` at file scope, and the error it produces

Calling a `static` function from another translation unit **compiles** and **fails to link**:

```
/usr/bin/ld: bad.o: in function `main':
bad.c:(.text+0xe): undefined reference to `abs_int'
```

Compilation succeeded because the declaration satisfied the compiler. Linking failed because
`static` gave the definition **internal linkage**, so its symbol was never exported.

### Makefile dependencies

```make
CFLAGS = -Wall -Wextra -Werror -pedantic -std=c11 -g

prog: stats.o main.o
	$(CC) $^ -o $@

stats.o: stats.c stats.h
main.o:  main.c  stats.h
```

Verified: touching `stats.h` rebuilds **both** objects; touching `main.c` rebuilds **only**
`main.o`. Omitting the header from the prerequisites produces a build that silently links a stale
object after a header change.

---

## Part 6: Contracts

```c
/* Precondition:  v != NULL and n > 0
 * Postcondition: returns the arithmetic mean of v[0..n-1]
 * Invariant:     after k iterations, s == sum of v[0..k-1] */
double mean(const double *v, int n) {
    assert(v && n > 0);
    ...
}
```

| Use assertions for | Do **not** use assertions for |
|---|---|
| Programmer errors — violated preconditions, broken invariants | User input or external data |
| Conditions that must be impossible | Conditions that are merely unlikely |
| | **Anything with a side effect** |

`-DNDEBUG` compiles assertions out **entirely**. Verified: `factorial(-1)` aborts with
`Assertion 'n >= 0' failed.` and exit status 134; rebuilt with `-DNDEBUG` it silently returns `1`.
So `assert(read_input(&x) == 1);` stops reading input in a release build.

---

## Part 7: Structured Programming

> **Böhm–Jacopini.** Any computable function can be expressed using only **sequence**, **selection**,
> and **iteration**. `goto` is never *necessary*.

It remains occasionally *useful* — the cleanup-on-error idiom in C is the standard defence — but any
`goto` mesh can be mechanically rewritten with a flag and a loop.

### Function design

| Principle | Test |
|---|---|
| One job | Can you name it without "and"? |
| Short | Does it fit on a screen? |
| Few parameters | More than four suggests a missing struct (Week 7) |
| `static` by default | Export only what the header promises |

---

## Build Line

```
gcc -Wall -Wextra -Werror -pedantic -std=c11 -g
gcc -fsanitize=address        # catches stack-use-after-return
gdb -q ./prog                 # backtrace, info frame, info locals
```

---

*PROG 101 · Week 3 · Reference · © CSE Department*
