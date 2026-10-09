# PROG 101 · Programming I: Structured Programming in C
## Week 12 · Lecture 3: Debugging

*“The most effective debugging tool is still careful thought, coupled with judiciously placed print statements.”* — Brian Kernighan, "Unix for Beginners" (1979)

**Date:** Thursday 17 December 2026 · 10:00–10:50 · Week 12

**Reading:** GDB Tutorial · Kernighan & Pike, Ch. 5 · `man valgrind` · Zeller, *Why Programs Fail* *(details at the end of the lecture)*

**Coursework:** 📝 **PS 11** due Fri 18 Dec 17:00 · 📝 **PS 12** released Fri 18 Dec 10:00, due Fri 25 Dec 17:00 · 🔬 **Lab 12** Mon 21 Dec 15:00–16:50 · 📕 **Final exam** Thu 24 Dec 14:00

---

## Lecture Goals

By the end of this lecture you can:

- Debug systematically rather than by guessing
- Use GDB to inspect a live crash: backtrace, frames, variables
- Choose the right tool from the symptom
- Explain why "works at `-O0`, breaks at `-O2`" is a diagnosis, not a compiler bug

---

## 1. Debugging Is Not Guessing

The common approach — change something, rerun, repeat — works on easy bugs and fails on hard ones,
because it has no stopping condition and no way to tell a fix from a coincidence.

The systematic method:

**1. Reproduce it reliably.** A bug you cannot trigger is a bug you cannot verify you fixed. Find the
smallest input that shows it.

**2. Reduce the input.** Halve it, rerun, keep the half that still fails. A 10,000-line input reduces
to a handful in a dozen steps. Very often the reduced case makes the cause obvious.

**3. Form a hypothesis that predicts something.** Not "something's wrong with the loop" but "`i`
reaches `n` and we read `a[n]`". A hypothesis you cannot test is not one.

**4. Test one thing at a time.** Two simultaneous changes and a behaviour change tell you nothing.

**5. Fix the cause.** If you cannot explain *why* the fix works, you have moved the bug, not removed
it — a common outcome with memory errors, where a change in layout hides the corruption.

**6. Add a test.** Otherwise it comes back.

---

## 2. GDB

```bash
gcc -Wall -Wextra -g -O0 prog.c -o prog     # -g for symbols, -O0 for honest line numbers
gdb ./prog
```

| Command | Effect |
|---|---|
| `run` (`r`) | Start |
| `bt` | **Backtrace** — the call stack |
| `frame N` (`f`) | Select a frame |
| `print x` (`p`) | Print a variable or expression |
| `info locals` | All locals in the current frame |
| `break f` (`b`) | Breakpoint on a function |
| `break file.c:42` | Breakpoint on a line |
| `next` (`n`) / `step` (`s`) | Over / into |
| `continue` (`c`) | Resume |
| `watch x` | Break when `x` changes |

### A crash, inspected

Verified on a null dereference:

```
Program received signal SIGSEGV, Segmentation fault.
#0  0x0000555555555159 in deref (p=0x0) at crash.c:2
#1  0x000055555555517d in main () at crash.c:3
```

Three things arrive at once: the signal (**SIGSEGV**), the exact line (`crash.c:2`), and — most
useful — **the argument value, `p=0x0`**. The bug is not in `deref`; it is in whoever passed NULL.
The backtrace names them.

`bt` is the first command to run on any crash, every time.

### Batch mode

```bash
gdb -batch -ex run -ex bt ./prog
```

Runs to the crash, prints the backtrace, exits. Useful in scripts and when a bug reproduces only in
a build system.

### `watch` — for corruption

When a variable becomes wrong and you do not know where:

```
(gdb) watch counter
(gdb) continue
Hardware watchpoint 2: counter
Old value = 5
New value = 99
```

GDB stops at the instruction that changed it. This is the fastest route to "who wrote to my
variable", which is otherwise one of the hardest questions to answer.

---

## 3. Matching Tool to Symptom

| Symptom | First tool | Why |
|---|---|---|
| Segfault, consistent line | **GDB `bt`** | Gives the line and the arguments |
| Crash far from the real bug | **ASan** | Names the variable, extent, and offset |
| Works at `-O0`, breaks at `-O2` | **UBSan** | The signature of undefined behaviour |
| Memory grows over time | **Valgrind `--leak-check=full`** | Reports each leaked block and its allocation site |
| Wrong result, no crash | **Tests + `gcov`** | Find the untested branch |
| Variable becomes wrong | **GDB `watch`** | Stops at the write |
| Uninitialised value | **Valgrind** | ASan does **not** detect these |

**Start with the compiler.** `-Wall -Wextra -Werror -pedantic` costs nothing and runs every build.
Then the sanitizers, which cost ~2×. Then Valgrind, which costs 20–50× but catches what ASan cannot.

---

## 4. `-O0` Works, `-O2` Breaks

This deserves its own section because the natural conclusion is wrong.

**It is almost never a compiler bug.** GCC builds essentially every package in every Linux
distribution; a miscompilation of ordinary code would be found in days. The base rate is
overwhelming.

**It is almost always undefined behaviour.** At `-O0` the compiler translates fairly literally and
the UB happens to do something survivable. At `-O2` the optimiser applies transformations valid only
for programs *without* UB — deleting a check it can prove redundant, keeping a value in a register,
reordering reads. The behaviour changes because there was never a defined behaviour to preserve.

You have seen this concretely twice this term:

- `if (x + 1 < x)` as an overflow check is **deleted**, because signed overflow cannot happen in a
  valid program (Week 2).
- `int *f(void) { int x = 42; return &x; }` compiles to **`return NULL`** — verified at both `-O0`
  and `-O2` (Week 3).

### The diagnostic procedure

1. **Rebuild with `-fsanitize=address,undefined -g -O1`.** Ends most investigations immediately.
2. **Run under Valgrind** if the sanitizers are silent — it catches uninitialised reads they miss.
3. **Turn warnings up:** add `-Wshadow -Wconversion -Wundef`. Fix every one.
4. **Bisect the assumption.** If `-fno-strict-aliasing` fixes it, you have a type-punning violation.
   If `-fno-strict-overflow` fixes it, you have signed overflow.

**Step 4 is a diagnosis, not a fix.** Shipping with `-fno-strict-overflow` leaves the bug in place
and hides it. The flag tells you *which* undefined behaviour you have; then you go and remove it.

---

## 5. Habits

- **Read the whole error message.** The answer is in it more often than not, and C's messages get
  worse the further you read from the first one — fix the first error and recompile.
- **Compile at `-O2` while developing.** `-Wmaybe-uninitialized` reports **nothing at `-O0`**
  (verified in Week 3), so a whole class of warning is invisible in a debug build.
- **When stuck, explain it aloud.** Articulating the problem surfaces the wrong assumption, because
  you must state it to say it.
- **Keep a bug journal.** The bugs you find hardest reveal your specific blind spots, and they repeat.
- **Be precise about what you know.** "It doesn't work" is not a report. "It segfaults in
  `list_insert` at line 40 when the list is empty" is — and the second one usually contains its own
  answer.

---

## 6. Summary

| Idea | Takeaway |
|---|---|
| Reproduce first | A bug you cannot trigger is one you cannot verify fixed |
| Reduce the input | Halve and rerun; the reduced case is often self-explaining |
| One change at a time | Two changes and a behaviour change prove nothing |
| Explain the fix | If you cannot say why it works, you moved the bug |
| `bt` first | Gives the line **and the argument values** — verified `p=0x0` |
| `watch x` | Stops at the instruction that corrupts a variable |
| `-g -O0` for GDB | Otherwise line numbers lie |
| Develop at `-O2` | `-Wmaybe-uninitialized` is silent at `-O0` |
| `-O0` works, `-O2` breaks | **Undefined behaviour**, not a compiler bug |
| `-fno-strict-overflow` "fixes" it | That is a **diagnosis**; go remove the UB |
| Tool order | Compiler flags → sanitizers → Valgrind |
| Uninitialised reads | Valgrind only; **ASan misses them** |

---

## Practice Exercises

**1. (Diagnose.)** A program prints correct output at `-O0` and garbage at `-O2`. No pointer
arithmetic anywhere. Give your first three actions, in order, with the reason for each.

**2. (Explain.)** Why does GDB need `-g`, and why is `-O0` recommended alongside it?

**3. (Apply.)** A `long` counter is 5 at the top of a loop and 99 three iterations later, and nothing
in the visible code writes to it. Give the GDB command that finds the culprit, and say what it does.

**4. (Stretch.)** A colleague fixes an intermittent crash by adding a `printf` inside the failing
function; the crash disappears. Explain what most likely happened, why the "fix" is dangerous, and
how you would find the real cause.

### Answers

**1.**

1. **Rebuild with `-fsanitize=address,undefined -g -O1`.** The symptom is the classic signature of
   undefined behaviour, and UBSan reports the exact line and kind. It is one command and ends most
   such investigations.
2. **Run under Valgrind** if the sanitizers are silent, because it detects **uninitialised value
   reads** that ASan does not — and "garbage output" is exactly that symptom.
3. **Raise the warnings** (`-Wall -Wextra -Wpedantic -Wshadow -Wconversion`) and fix every one; then,
   if still unexplained, bisect with `-fno-strict-aliasing` and `-fno-strict-overflow` to identify
   *which* assumption is being violated.

*Concluding "compiler bug" is not among the first three actions, and stating that earns credit.*

**2. `-g` emits debugging symbols** — the mapping from machine addresses to source lines, variable
names, and types. Without it GDB shows raw addresses and `??` for function names.

**`-O0` is recommended because optimisation destroys the correspondence** between source and
machine code. At `-O2` variables are kept in registers or eliminated (`<optimized out>`), code is
reordered so stepping jumps around unpredictably, and functions are inlined so they do not appear in
the backtrace. The line numbers are not *wrong* so much as no longer meaningful.

*The tension worth noting:* if the bug only manifests at `-O2`, you must debug at `-O2` — usually
with `-Og`, which optimises while preserving debuggability.

**3.**

```
(gdb) watch counter
(gdb) continue
```

`watch` sets a **watchpoint**: GDB stops execution at the instruction that modifies `counter` and
reports the old and new values. On most hardware this uses a debug register, so it costs almost
nothing.

This answers "who wrote to my variable" directly. The likely culprits are a buffer overrun in an
adjacent variable, a stale pointer writing through freed memory, or an out-of-bounds array write —
all of which are invisible in the source near the counter. ASan would also catch the first and third.

**4.** **What most likely happened:** the `printf` changed the program's memory layout or timing, and
the bug is still there.

Adding a call changes stack-frame size and alignment, so a buffer overrun that was corrupting a live
variable may now land in padding. It also flushes buffers and takes time, which can hide a race. In
optimised builds it acts as a barrier that prevents the compiler from keeping a value in a register —
so a use of an uninitialised or aliased variable starts reading memory instead.

**Why it is dangerous:** nothing was fixed. The corruption still occurs; it merely lands somewhere
currently harmless. It will return on the next unrelated change to the function — a new local, a
different compiler version, a different optimisation level — and by then the `printf` will look
load-bearing and nobody will know why.

**How to find the real cause:**

1. **ASan first.** A layout-sensitive bug is almost always a buffer overflow or use-after-free, and
   ASan finds both regardless of layout, naming the variable and offset.
2. **Valgrind** if ASan is silent, for uninitialised reads.
3. **Remove the `printf` and reproduce deliberately** — the bug returning on removal confirms it was
   never a fix.
4. If it is intermittent and timing-related, suspect **uninitialised memory** rather than a race —
   this course is single-threaded, so timing sensitivity usually means reading whatever the stack or
   heap happened to contain.

*Full marks require identifying that the bug is still present.* "The printf fixed a race" is a
plausible-sounding answer that misses the point, and in a single-threaded program it is almost
certainly wrong.

---

## Reading

- **GDB Tutorial** (sourceware.org) — the first ten commands are 90% of the value
- **Kernighan & Pike, Ch. 5** — debugging
- **`man valgrind`**; the ASan and UBSan wiki pages
- **Zeller, *Why Programs Fail*** — optional; systematic debugging as a discipline

---

*PROG 101 · Week 12 · Lecture 3 · © CSE Department*
