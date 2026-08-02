# PROG 101 · Week 3
## LAB 3 Solutions — INSTRUCTOR ONLY

**Total: 20 points.** Every output below was produced by compiling and running the code with
`gcc -Wall -Wextra -Werror -pedantic -std=c11 -g` on x86-64 Linux.

---

## Part 1: Making the Call Stack Visible (5 pts)

### 1A — verified output

```
main      &m = 0x7fffc8b620b4
level1    &a = 0x7fffc8b62094
 level2   &b = 0x7fffc8b62074
  level3  &c = 0x7fffc8b62054
```

**1. Direction *(1 pt)*.** The addresses **decrease** with each nested call — the stack grows
**downward** on x86-64.

*Accept "toward lower addresses". Students who answer "up" because the frames are drawn above one
another on the board have described the picture, not the machine.*

**2. Spacing *(1 pt)*.** Consecutive frames are **32 bytes** apart, and the spacing is constant here:

| From → to | Difference |
|---|---|
| `main` → `level1` | `0x20` = 32 |
| `level1` → `level2` | `0x20` = 32 |
| `level2` → `level3` | `0x20` = 32 |

A single `int` is 4 bytes, so 28 bytes are something else: the **saved return address**, the **saved
frame pointer**, and **alignment padding** (x86-64 requires 16-byte stack alignment at call
boundaries). The frame is the whole bookkeeping record, not just the local.

*Constant spacing here is a consequence of all four functions having identically shaped frames.
Students should not conclude that frames are always the same size — a function with more locals
takes more.*

**3. Between runs *(1 pt)*.** The addresses **differ on every run**. This is **ASLR** (address space
layout randomisation): the kernel randomises the stack base to make memory-corruption exploits
harder.

What stays **identical** run to run is the *differences* — always 32 bytes. Absolute addresses are
not reproducible; relative layout is.

*A student who reports identical addresses across runs has probably run it once and copied. Ask them
to run it again in front of you.*

### 1B — GDB *(2 pts)*

```
(gdb) break level3
(gdb) run
(gdb) backtrace
#0  level3 () at stack.c:3
#1  0x... in level2 () at stack.c:4
#2  0x... in level1 () at stack.c:5
#3  0x... in main () at stack.c:8
```

The four `backtrace` frames correspond one-to-one with the four addresses from 1A, **in reverse
order**: `#0` is the innermost (`level3`, lowest address) and `#3` is `main` (highest address).

`info frame` shows the frame's base and the saved return address — the 28 bytes accounted for in
part 2. `frame 1` then `info locals` shows `b = 2`, confirming that `level2`'s frame is still live
and intact while `level3` runs.

*The point of 1B is that `backtrace` is not a debugger abstraction — it is a literal readout of the
structure whose addresses they printed in 1A.*

---

## Part 2: Pass-by-Value and Storage Duration (5 pts)

### 2A — verified output *(2 pts)*

```
before: &v=0x7ffcf6d2b0d4 v=42
  inside: &x=0x7ffcf6d2b0bc x=42 -> 999
after : &v=0x7ffcf6d2b0d4 v=42
```

**The address-based explanation, which is what earns the marks:**

`&v` is `0x...b0d4` and `&x` is `0x...b0bc` — **24 bytes apart, and therefore different objects**.
`x` is not another name for `v`; it is a separate variable in `try_modify`'s frame, initialised by
*copying* `v`'s value at the moment of the call.

`x = 999` writes to `0x...b0bc`. Nothing ever writes to `0x...b0d4`, so `v` is still 42. When
`try_modify` returns, its frame is abandoned and `x` ceases to exist.

*Reject answers that only say "because C is pass-by-value" — that is the name of the phenomenon, and
the question explicitly asks for the address argument. Award 1 of 2.*

### 2B — storage duration *(3 pts)*

**Verified table** *(1 pt)*:

| Call | `counter()` | `automatic()` |
|---|---|---|
| 1 | 1 | 1 |
| 2 | 2 | 1 |
| 3 | 3 | 1 |
| 4 | 4 | 1 |

**What `static` changed** *(2 pts)*:

`static` changed the **storage duration**, not the **scope**.

| | `int n` | `static int n` |
|---|---|---|
| **Scope** (where the name is visible) | the function | the function — **unchanged** |
| **Storage duration** (how long it lives) | one call | the whole program run |
| **Where it lives** | the stack frame, created and destroyed per call | the data segment, allocated once at load time |
| **Initialisation** | every call | **once**, before `main` |

The automatic `n` is a fresh object in a fresh frame each call, so `++n` always yields 1. The static
`n` is the *same object* every call, so `++n` accumulates.

**These are two independent properties**, and this is the whole lesson: a name can be invisible from
outside while the object it names outlives every call. Students routinely conflate the two because
`static` at *file* scope changes linkage instead — which is Part 3's subject.

---

## Part 3: A Multi-File Library (6 pts)

### 3A — verified *(3 pts)*

```
gcd(48,18)=6 gcd(-48,18)=6 gcd(17,5)=1 gcd(0,7)=7
factorial: 1 1 2 6 24 120 720 5040 40320 362880 3628800 39916800 479001600
primes<30: 2 3 5 7 11 13 17 19 23 29
```

All three lines match the specification exactly.

*Watch `gcd(0,7)`. The Euclidean loop `while (b) { t = a%b; a = b; b = t; }` returns 7 immediately and
correctly. A student who special-cases zero has usually broken `gcd(0,0)`, which should be 0.*

*`factorial(12) = 479001600` is the largest that fits in a 32-bit `int`; the signature returns `long`
precisely so 13 upward do not silently overflow. Worth pointing out — it is the Week 1 material
paying off.*

### 3B — the linker error *(2 pts)*

```
/usr/bin/ld: bad.o: in function `main':
bad.c:(.text+0xe): undefined reference to `abs_int'
collect2: error: ld returned 1 exit status
```

**The failing stage is linking.**

Compilation of `bad.c` **succeeded** because a declaration is a promise, and the compiler's job ends
at trusting it: `int abs_int(int x);` told the compiler the name exists with that type, which is all
it needs to emit a call instruction with an unresolved symbol.

The **linker** must then find a definition with **external linkage**. `static` gives `abs_int`
**internal linkage** — its symbol is not exported from `mathutil.o` at all, so no definition is
visible to resolve against.

*This is the single most useful thing in Part 3: it shows that the compiler and the linker check
different things, and that "it compiled" is not "it will link". Students who answer "compilation"
have not read the error, which names `ld`.*

### 3C — the Makefile *(1 pt)*

```make
CFLAGS = -Wall -Wextra -Werror -pedantic -std=c11 -g

prog: mathutil.o main.o
	$(CC) $^ -o $@

mathutil.o: mathutil.c mathutil.h
main.o:     main.c     mathutil.h

clean:
	rm -f prog *.o
```

Touching `mathutil.h` must rebuild **both** objects, because both list it as a prerequisite.
Touching `main.c` rebuilds only `main.o`.

*The common omission is leaving `mathutil.h` out of the prerequisites. The build then appears to work
and silently uses a stale object after a header change — which is precisely the bug the exercise is
inoculating against. Deduct the point if the header is missing.*

---

## Part 4: Contracts and the First Dangling Pointer (4 pts)

### 4A — assertions *(2 pts)*

`factorial(-1)` with assertions active:

```
asrt: asrt.c:3: factorial: Assertion `n >= 0' failed.
Aborted (core dumped)
```

Exit status **134** (128 + SIGABRT).

Rebuilt with `-DNDEBUG`, the same call prints **`1`** and exits 0 — the assertion is compiled out
entirely, and the function silently returns a meaningless answer for invalid input.

**What assertions must never be used for:** anything with a **side effect**, because `-DNDEBUG`
deletes the whole expression. `assert(read_input(&x) == 1);` stops reading input in a release build.

*Also acceptable: never use assertions to validate **user input or external data**. Those are
expected conditions requiring real error handling, not programmer errors. The `-DNDEBUG` build must
still reject them.*

### 4B — the two dangling pointers *(2 pts)*

**1. Version 1, with no warning flags at all:**

```
dangling.c: In function 'make':
dangling.c:2:45: warning: function returns address of local variable [-Wreturn-local-addr]
    2 | static int *make(void) { int x = 42; return &x; }
      |                                             ^~
```

The flag is **`-Wreturn-local-addr`**, and it is **on by default** — it needs neither `-Wall` nor
`-Wextra` nor optimisation. GCC treats this as serious enough to report unconditionally, which is a
strong signal about how reliably wrong the code is.

**2. Version 2, with the full `-Wall -Wextra -pedantic`: no warning at all.** The address launders
through `identity()`, and GCC's analysis does not follow it across the call.

**3. Under `-fsanitize=address`:**

```
ERROR: AddressSanitizer: stack-use-after-return on address 0x7ac79b100020
READ of size 4 at 0x7ac79b100020 thread T0
    #0 ... in main
```

The error class is **stack-use-after-return**.

**4. The frame explanation.** `x` lives in `make`'s frame. When `make` returns, that frame is
abandoned — the stack pointer moves back up past it, and the very next call reuses those bytes. In
Part 1's terms, the address returned is the `0x...2054`-style slot belonging to a frame that no
longer exists.

The compiler caught version 1 because the `return` statement and the `&x` are in the same function —
a purely local, syntactic check. It missed version 2 because proving it requires **inter-procedural**
analysis: knowing what `identity` does with its argument. That is exactly the class of reasoning
static analysis gives up on and runtime instrumentation handles, which is why the course uses both.

*Full marks require the compiler-vs-sanitizer contrast in point 4. Students who only describe the
dead frame get 1 of 2.*

---

## Marking Summary

| Part | Points | Watch for |
|---|---|---|
| 1 | 5 | Addresses must decrease; ASLR noted; `backtrace` mapped to frames |
| 2 | 5 | 2A must argue from the two addresses; 2B must separate scope from duration |
| 3 | 6 | 3B must say **linking**, and explain why compiling succeeded |
| 4 | 4 | 4B.4 must contrast local vs inter-procedural analysis |
| **Total** | **20** | |

---

*PROG 101 · Week 3 · Lab 3 Solutions · Instructor copy — do not distribute*
