---
assessment: Lab 3
course: PROG 101
component: Labs
possible: 20
score: 20
status: graded
started: 2026-10-19
submitted: 2026-10-19
graded: 2026-10-19
source: "LAB 3 Functions Callstack Multifile.md"
---

# PROG 101 · Lab 3
## Answer Sheet — Functions, the Call Stack, and Multi-File Programs

**Assessment:** `LAB 3 Functions Callstack Multifile.md`
**Points available:** 20 (+2 bonus)

Code and the full write-up live in `1. PROG 101/week3/lab3/`: `stack.c`, `pbv.c`, `duration.c`,
`mathutil.h`, `mathutil.c`, `main.c`, `bad.c`, `asrt.c`, `dangling.c`, `Makefile`, `answers.md`.

Clean programs build with `gcc -Wall -Wextra -Werror -pedantic -std=c11 -g`; `bad.c` and `dangling.c`
are *deliberately* broken (the linker error and the dangling pointer are the exercise). All output is
real, from x86-64 Linux with `gcc 15.2.0` and `gdb 17.1`.

---

## Part 1 — Making the Call Stack Visible  (5 points)

**1A** — `./stack`:

```
main      &m = 0x7ffc386f3144
level1    &a = 0x7ffc386f3124
 level2   &b = 0x7ffc386f3104
  level3  &c = 0x7ffc386f30e4
```

1. **Decrease** (`144 → 124 → 104 → 0e4`): the stack grows **downward**.
2. Consecutive frames are a constant **32 bytes** (`0x20`) apart. An `int` is 4 bytes, so the other
   **28** hold the saved return address, the saved frame pointer, and alignment padding (16-byte stack
   alignment at calls).
3. Running twice gives **different** addresses — **ASLR** moves the stack base each launch. The *spacing*
   (32 bytes), not the absolute address, is what stays identical.

**1B** — GDB:

```
#0  level3 () at stack.c:3
#1  0x00005555555551ff in level2 () at stack.c:4
#2  0x0000555555555258 in level1 () at stack.c:5
#3  0x00005555555552b1 in main () at stack.c:10
… info frame: saved rip = 0x…51ff, called by frame at 0x7fffffffd450 …
… frame 1; info locals → b = 2
```

The four frames are the four 1A addresses **in reverse order** (`#0` innermost/lowest → `#3` `main`).
`info frame`'s saved `rbp`/`rip` are the 28 non-local bytes; `frame 1` + `info locals` shows `b = 2`,
proving `level2`'s frame is still live while `level3` runs.

*Marks: 5 / 5*

---

## Part 2 — Pass-by-Value and Storage Duration  (5 points)

**2A** — `./pbv`:

```
before: &v=0x7ffdf2a2e0e4 v=42
  inside: &x=0x7ffdf2a2e0cc x=42 -> 999
after : &v=0x7ffdf2a2e0e4 v=42
```

`&v` and `&x` are **24 bytes apart — two different objects**. `x` is a separate variable in
`try_modify`'s frame, initialised by copying `v`'s value. `x = 999` writes to `0x…e0cc`; nothing writes
to `0x…e0e4`, so `v` stays 42. When the function returns its frame is abandoned.

**2B** — `./duration`:

```
call  counter()  automatic()
   1          1            1
   2          2            1
   3          3            1
   4          4            1
```

`n` is invisible outside in **both** cases, so `static` did **not** change scope. It changed the
**storage duration**: automatic `n` is a fresh stack object each call (always 1); static `n` is the
**same** object, living in the data segment for the whole run, zero-initialised before `main`, so it
accumulates.

*Marks: 5 / 5*

---

## Part 3 — A Multi-File Library  (6 points)

**3A** — separate compilation (`mathutil.o`, `main.o`, link). `./prog`:

```
gcd(48,18)=6 gcd(-48,18)=6 gcd(17,5)=1 gcd(0,7)=7
factorial: 1 1 2 6 24 120 720 5040 40320 362880 3628800 39916800 479001600
primes<30: 2 3 5 7 11 13 17 19 23 29
lcm(2147483646, 2147483647)=4611686011984936962
```

All three required lines match exactly. **Bonus (`+2`):** `lcm` divides before multiplying —
`((long long)a / gcd(a,b)) * b` — so `lcm(2147483646, 2147483647)` returns the full product
`4611686011984936962` instead of overflowing.

**3B** — `bad.c` **compiles cleanly**, then fails at **link** time:

```
/usr/bin/x86_64-linux-gnu-ld.bfd: bad.o: in function `main':
bad.c:11:(.text+0xe): undefined reference to `abs_int'
collect2: error: ld returned 1 exit status
```

Compilation succeeded because a declaration is a promise. The **linker** needs a definition with
**external** linkage, but `abs_int` is `static` in `mathutil.c` (**internal** linkage) — `nm mathutil.o`
shows it as a local symbol (`t abs_int`), not exported. "It compiled" is not "it will link."

**3C** — `Makefile`. `touch mathutil.h; make` rebuilds **both** `main.o` and `mathutil.o`; `touch main.c;
make` rebuilds **only** `main.o`; unchanged → `Nothing to be done`.

*Marks: 6 / 6*

---

## Part 4 — Contracts and the First Dangling Pointer  (4 points)

**4A** — `assert(n >= 0)` in `factorial`:

```
asrt: mathutil.c:20: factorial: Assertion `n >= 0' failed.
Aborted (core dumped)          (exit 134 = 128 + SIGABRT)
```

With `-DNDEBUG` the same call prints **`1`** and exits 0 — the assertion is compiled out entirely.
Assertions must **never** carry a **side effect** (e.g. `assert(read_input(&x) == 1);`), because
`-DNDEBUG` deletes the whole expression; nor should they validate user input.

**4B** —

1. Version 1 with no flags: `warning: function returns address of local variable
   [-Wreturn-local-addr]` — on **by default** (no `-Wall`/`-Wextra`).
2. Version 2 with `-Wall -Wextra -pedantic`: **no warning** (the address launders through `identity()`).
3. Version 2 under `-fsanitize=address`: **`stack-use-after-return`**, with ASan naming `x` in `make2`'s
   frame as the target of the read.
4. Both returned addresses point into a frame that no longer exists; the next call reuses those bytes.
   The compiler caught version 1 with a **local, syntactic** check (the `return` and `&x` are in one
   function) but missed version 2, which needs **inter-procedural** analysis of what `identity()` does —
   the gap ASan fills at run time.

*Marks: 4 / 4*

---

## Grading Summary

| | |
|---|---|
| **Score** | 20 / 20 (+2 bonus) |
| **Percent** | 100% |
| **Graded** | 2026-10-19 |

**Feedback:**
Complete and correct. Part 1 records the four addresses, reports the constant 32-byte spacing, explains
the 28 non-local bytes (saved return address, saved frame pointer, alignment), and identifies ASLR across
runs; the GDB backtrace is matched frame-for-frame to 1A in reverse order, with `info frame` and
`frame 1`/`info locals` used as asked. Part 2 explains pass-by-value purely from the two addresses (24
bytes apart) rather than restating the name, and correctly separates scope from storage duration for
`static`. Part 3 compiles separately with all three output lines matching, explains the linker error as
internal vs external linkage (with `nm` evidence), and the Makefile rebuilds exactly the right objects.
Part 4 shows the assertion firing twice (active vs `-DNDEBUG`), names the side-effect rule, distinguishes
the default `-Wreturn-local-addr` from the silent laundered version, pastes the ASan
`stack-use-after-return` report, and gives the local-vs-inter-procedural explanation. No stray warnings.
Bonus `lcm` included and overflow-safe near `INT_MAX`.
