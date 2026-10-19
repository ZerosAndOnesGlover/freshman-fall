# PROG 101 · Week 3 · Lab 3 — Answers

**Name:** Adebayo Glover · **Date:** Monday 19 October 2026
**Build:** `gcc 15.2.0`, `gcc -Wall -Wextra -Werror -pedantic -std=c11 -g` · Inspected with `gdb 17.1`.
All outputs below are real, captured from this machine (x86-64 Linux).

Files: `stack.c`, `pbv.c`, `duration.c`, `mathutil.h`, `mathutil.c`, `main.c`, `bad.c`, `asrt.c`,
`dangling.c`, `Makefile`.

---

## Part 1 — Making the Call Stack Visible (5 pts)

### 1A — Frames have addresses

`./stack`, run one:

```
main      &m = 0x7ffc386f3144
level1    &a = 0x7ffc386f3124
 level2   &b = 0x7ffc386f3104
  level3  &c = 0x7ffc386f30e4
```

**1. Direction *(1 pt)*.** The addresses **decrease** as the calls nest (`144 → 124 → 104 → 0e4`): the
stack grows **downward** toward lower addresses on x86-64.

**2. Spacing *(1 pt)*.** The difference between consecutive frames is constant:

| From → to | Addresses | Difference |
|---|---|---|
| `main` → `level1` | `…144 → …124` | `0x20` = **32** |
| `level1` → `level2` | `…124 → …104` | `0x20` = **32** |
| `level2` → `level3` | `…104 → …0e4` | `0x20` = **32** |

A single `int` is only 4 bytes, so the other **28 bytes** are the frame's bookkeeping: the **saved return
address**, the **saved frame pointer**, and **alignment padding** (x86-64 keeps the stack 16-byte aligned
at call boundaries). The frame is the whole record, not just the local.

**3. Between runs *(1 pt)*.** Running twice gives **different** absolute addresses:

```
run 1: main &m = 0x7ffc386f3144
run 2: main &m = 0x7ffd223cbad4
```

That is **ASLR** (address-space layout randomisation): the kernel moves the stack base on each launch to
make memory-corruption exploits harder. What is *identical* run to run is the **spacing** — always
32 bytes. Absolute addresses are not reproducible; the relative layout is.

### 1B — The same picture in GDB *(2 pts)*

```
(gdb) break level3
Breakpoint 1 at 0x1175: file stack.c, line 3.
(gdb) run
Breakpoint 1, level3 () at stack.c:3
3	static void level3(void) { int c = 3; printf("  level3  &c = %p\n", (void*)&c); }
(gdb) backtrace
#0  level3 () at stack.c:3
#1  0x00005555555551ff in level2 () at stack.c:4
#2  0x0000555555555258 in level1 () at stack.c:5
#3  0x00005555555552b1 in main () at stack.c:10
(gdb) info frame
Stack level 0, frame at 0x7fffffffd430:
 rip = 0x555555555175 in level3 (stack.c:3); saved rip = 0x5555555551ff
 called by frame at 0x7fffffffd450
 Locals at 0x7fffffffd420, Previous frame's sp is 0x7fffffffd430
 Saved registers:
  rbp at 0x7fffffffd420, rip at 0x7fffffffd428
(gdb) frame 1
#1  0x00005555555551ff in level2 () at stack.c:4
(gdb) info locals
b = 2
```

The four `backtrace` frames are the four addresses from 1A, **in reverse order**: `#0` is the innermost
(`level3`, lowest address) and `#3` is `main` (highest address). `info frame` shows the saved `rbp`/`rip`
— the bookkeeping that accounts for the 28 non-local bytes of the 32-byte frame. `frame 1` + `info
locals` shows `b = 2`, i.e. `level2`'s frame is still live and intact while `level3` runs.

---

## Part 2 — Pass-by-Value and Storage Duration (5 pts)

### 2A — Proved by address *(2 pts)*

```
before: &v=0x7ffdf2a2e0e4 v=42
  inside: &x=0x7ffdf2a2e0cc x=42 -> 999
after : &v=0x7ffdf2a2e0e4 v=42
```

`&v` is `0x…e0e4` and `&x` is `0x…e0cc` — **24 bytes apart, and therefore two different objects**. `x`
is not another name for `v`; it is a separate variable in `try_modify`'s frame, created by *copying* `v`'s
value at the moment of the call. `x = 999` writes to `0x…e0cc`; nothing ever writes to `0x…e0e4`, so `v`
is still 42. When `try_modify` returns, its frame is abandoned and `x` ceases to exist.

### 2B — Storage duration *(3 pts)*

Verified table:

| Call | `counter()` | `automatic()` |
|---|---|---|
| 1 | 1 | 1 |
| 2 | 2 | 1 |
| 3 | 3 | 1 |
| 4 | 4 | 1 |

`n` is invisible outside its function in **both** cases — `static` did **not** change the **scope**. It
changed the **storage duration**:

| | `int n;` | `static int n;` |
|---|---|---|
| **Scope** | the function | the function — **unchanged** |
| **Storage duration** | one call | the whole program run |
| **Where it lives** | the stack frame, built and destroyed per call | the data segment, allocated once at load |
| **Initialisation** | every call (indeterminate) | once, before `main` (zero) |

The automatic `n` is a fresh object in a fresh frame each call, so `++n` is always 1. The static `n` is
the **same object** every call, so `++n` accumulates. Scope and storage duration are independent: a name
can be invisible from outside while the object it names outlives every call.

---

## Part 3 — A Multi-File Library (6 pts)

### 3A — Separate compilation *(3 pts)*

```
gcc -Wall -Wextra -Werror -pedantic -std=c11 -c mathutil.c -o mathutil.o
gcc -Wall -Wextra -Werror -pedantic -std=c11 -c main.c     -o main.o
gcc mathutil.o main.o -o prog
```

`./prog`:

```
gcd(48,18)=6 gcd(-48,18)=6 gcd(17,5)=1 gcd(0,7)=7
factorial: 1 1 2 6 24 120 720 5040 40320 362880 3628800 39916800 479001600
primes<30: 2 3 5 7 11 13 17 19 23 29
lcm(2147483646, 2147483647)=4611686011984936962
```

All three required lines match the specification exactly. (`mathutil.c` has the one file-private helper
`static int abs_int(int x)`; `is_prime` uses `d <= n / d` to avoid `d * d` overflow.)

**Bonus.** `lcm` is implemented as `((long long)a / gcd(a, b)) * b` — dividing **before** multiplying, so
inputs near `INT_MAX` do not overflow. The last line above is the proof: `lcm(2147483646, 2147483647)`
returns `4611686011984936962` (their product, ~4.6 × 10¹⁸, which fits in `long long`) instead of wrapping.

### 3B — The linker error *(2 pts)*

`bad.c` compiles cleanly:

```
$ gcc -Wall -Wextra -Werror -pedantic -std=c11 -g -c bad.c -o bad.o
compiled OK -> bad.o
```

Linking it against `mathutil.o` fails:

```
$ gcc bad.o mathutil.o -o badprog
/usr/bin/x86_64-linux-gnu-ld.bfd: bad.o: in function `main':
…/bad.c:11:(.text+0xe): undefined reference to `abs_int'
collect2: error: ld returned 1 exit status
```

**The failing stage is linking.** Compilation of `bad.c` **succeeded** because a declaration is a promise:
`int abs_int(int x);` told the compiler the name exists with that type, which is all it needs to emit a
call with an unresolved symbol. The **linker** must then find a definition with **external linkage** —
but `abs_int` is `static` in `mathutil.c`, i.e. **internal linkage**, so it is not exported at all.
Confirmed with `nm mathutil.o`:

```
0000000000000000 t abs_int      # lowercase 't' = local symbol, not exported
```

*"It compiled" is not "it will link."*

### 3C — The Makefile *(1 pt)*

`Makefile` (excerpt):

```make
prog: main.o mathutil.o
	$(CC) $(CFLAGS) -o $@ main.o mathutil.o

main.o:     main.c     mathutil.h
	$(CC) $(CFLAGS) -c main.c -o main.o

mathutil.o: mathutil.c mathutil.h
	$(CC) $(CFLAGS) -c mathutil.c -o mathutil.o
```

Demonstration — `touch mathutil.h; make` rebuilds **both** objects, because both list the header as a
prerequisite:

```
gcc … -c main.c     -o main.o
gcc … -c mathutil.c -o mathutil.o
gcc … -o prog main.o mathutil.o
```

`touch main.c; make` rebuilds **only** `main.o`:

```
gcc … -c main.c -o main.o
gcc … -o prog main.o mathutil.o
```

Unchanged: `make: Nothing to be done for 'all'.` (Leaving `mathutil.h` out of the prerequisites is the
classic bug: the build appears to work and silently uses stale objects after a header change.)

---

## Part 4 — Contracts and the First Dangling Pointer (4 pts)

### 4A — Assertions *(2 pts)*

`assert(n >= 0)` added to `factorial`. With assertions active:

```
$ ./asrt
asrt: mathutil.c:20: factorial: Assertion `n >= 0' failed.
Aborted (core dumped)
(exit: 134)
```

Exit status **134** = 128 + `SIGABRT` (6). Rebuilt with `-DNDEBUG`, the same call prints **`1`** and exits
0 — the assertion is *compiled out entirely*, and `factorial(-1)` silently returns a meaningless answer.

**What assertions should never be used for:** anything with a **side effect**, because `-DNDEBUG` deletes
the whole expression — e.g. `assert(read_input(&x) == 1);` would stop reading input in a release build.
(Equally, never use them to validate **user input**; that is an expected condition needing real error
handling that survives `-DNDEBUG`.)

### 4B — The two dangling pointers *(2 pts)*

**1. Version 1, no warning flags at all:**

```
dangling.c: In function 'make':
dangling.c:22:45: warning: function returns address of local variable [-Wreturn-local-addr]
   22 | static int *make(void) { int x = 42; return &x; }
```

The flag is **`-Wreturn-local-addr`**, and it is **on by default** (no `-Wall`, no `-Wextra`, no
optimisation). GCC treats this as serious enough to report unconditionally. Running it here even
segfaults (exit 139).

**2. Version 2 with full `-Wall -Wextra -pedantic`: silence.** No warning at all. The address launders
through `identity()`, and GCC's analysis does not follow it across the call.

**3. Version 2 under `-fsanitize=address`:**

```
ERROR: AddressSanitizer: stack-use-after-return on address 0x779f3f0f0020 …
READ of size 4 at 0x779f3f0f0020 thread T0
    #0 … in main …/dangling.c:31
Address 0x779f3f0f0020 is located in stack of thread T0 at offset 32 in frame
    #0 … in make2 …/dangling.c:19
  This frame has 1 object(s):
    [32, 36) 'x' (line 19) <== Memory access at offset 32 is inside this variable
SUMMARY: AddressSanitizer: stack-use-after-return
```

The error class is **`stack-use-after-return`**.

**4. Frame explanation.** `x` lives in `make`'s / `make2`'s frame. When that function returns, its frame
is abandoned — the stack pointer moves back up past it (exactly as 1A shows the frames unwinding), and the
very next call reuses those bytes. The returned address points at a slot (`…0f0020`) in a frame that no
longer exists; by the time `main` reads it, the `42` may have been overwritten.

The compiler caught version 1 because the `return` and the `&x` are in the **same function** — a purely
**local, syntactic** check. It missed version 2 because proving the bug requires **inter-procedural**
analysis: knowing what `identity()` does with its argument. That is exactly the reasoning static analysis
gives up on and runtime instrumentation (ASan) handles — which is why the course uses both.

---

*PROG 101 · Week 3 · Lab 3 · Adebayo Glover*
