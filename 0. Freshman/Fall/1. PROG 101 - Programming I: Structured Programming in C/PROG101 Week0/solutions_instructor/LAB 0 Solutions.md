# PROG 101 — Week 0
## LAB 0 Solutions — INSTRUCTOR ONLY

> **Every implementation below compiles under `gcc -Wall -Wextra -Werror -std=c11` and runs clean
> under `-fsanitize=address,undefined`.** Where the lab requires it, Valgrind output is quoted
> verbatim. Reject any submission that does not build warning-free — `-Werror` is not negotiable in
> this course.

---

## Part 2 — The Manual Pipeline

Expected artefacts and what each proves:

| Step | Command | Output | What to check |
|---|---|---|---|
| Preprocess | `gcc -E hello.c -o hello.i` | `hello.i` | ~800 lines from a 6-line source. `#include` is *textual substitution* |
| Compile | `gcc -S hello.i -o hello.s` | `hello.s` | Contains `.string "Hello, world"` and `call printf` |
| Assemble | `gcc -c hello.s -o hello.o` | `hello.o` | Binary. `nm hello.o` shows `T main` and **`U printf`** |
| Link | `gcc hello.o -o hello` | `hello` | `printf` now resolved; `ldd hello` lists `libc.so.6` |

**The single most useful diagnostic in the whole lab:** `nm hello.o | grep printf` prints
`U printf` — *undefined*. Students who understand that `U` means "the linker must supply this" will
never again be confused by an "undefined reference" error, which is the most common build failure
they will hit all semester.

`wc -l hello.i` typically reports 700–900 lines. Ask why: `stdio.h` pulls in dozens of headers, and
every one is pasted in whole.

---

## Part 3 — Assembly

In `hello.s`, students should identify:

- `.section .rodata` / `.string "Hello, world"` — the literal lives in **read-only** memory. This is
  why `char *p = "hi"; p[0] = 'H';` segfaults, and why literals should be `const char *`.
- `main:` label, `push %rbp` / `mov %rsp,%rbp` — the **function prologue** building the stack frame.
- `call printf@PLT` — the call, routed through the Procedure Linkage Table for dynamic linking.
- `mov $0,%eax` before `ret` — the `return 0`.

Compile with `-O2` and the prologue often disappears entirely. That contrast is worth showing: the
assembly is a *product of the compiler's choices*, not a transcription of the source.

---

## Part 4 — Makefile

```make
CC      = gcc
CFLAGS  = -Wall -Wextra -Werror -std=c11 -g

hello: hello.o
	$(CC) $^ -o $@

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

.PHONY: clean
clean:
	rm -f *.o hello temperature
```

**Recipe lines must start with a real tab.** `Makefile:5: *** missing separator. Stop.` is
this error and nothing else; editors that expand tabs cause it silently.

Check the student can answer: running `make` twice does nothing the second time, because the target
is newer than its prerequisites.

---

## Part 5 — `temperature.c`

Any correct conversion is acceptable. Two things to insist on:

1. **`float` division, not integer.** `(c * 9 / 5) + 32` with `int c` computes `9/5` as… no — it
   computes `c * 9` first, then `/5`, which truncates. `c * 9.0 / 5` avoids it. Test with c = 37:
   correct is 98.6, the integer version gives 98.
2. **`return 0`** at the end of `main`, and a check of `scanf`'s return value if input is read.

---

## Part 6 — GDB Session

The commands students must demonstrate, and what each shows:

| Command | Purpose |
|---|---|
| `break main` | Stop at entry |
| `run` | Start execution |
| `next` / `step` | Over vs. **into** a call — the distinction is the point |
| `print var` | Inspect a value; `print/x var` for hex |
| `info locals` | All locals in the frame |
| `backtrace` | The call chain — **always run this first on a crash** |
| `continue` | Resume |

Compile with **`-g`** or the session shows addresses instead of source lines. A student who says
"GDB didn't show my variables" has forgotten `-g`, and that is the whole lesson.

---

## Part 8 — Exploration Challenges

Expected answers on this platform (x86-64 Linux, gcc 13):

```
char=1  short=2  int=4  long=8  long long=8
float=4  double=8  void*=8
INT_MAX=2147483647  INT_MIN=-2147483648  UINT_MAX=4294967295
CHAR_MIN=-128   (plain char is SIGNED here; it is unsigned on ARM)
```

Only `sizeof(char) == 1` is guaranteed by the standard. Everything else is platform-specific, and a
student who states that has answered better than one who memorised the table.

---

## Marking Scheme

Points follow the allocation printed on the handout. Within each part:

- **Correctness (≈50%).** Passes the required test cases *and* the edge cases listed above.
- **Memory discipline (≈30%).** No leaks, no invalid reads/writes, every `malloc` checked, every
  owner documented. For labs with a Valgrind requirement this is pass/fail: **0 errors, 0 leaks.**
- **Method (≈20%).** Required technique actually used, bounds asserted, `const` applied where the
  function only reads.

**Automatic deductions, regardless of output:**
- Any compiler warning under `-Wall -Wextra`.
- Unchecked `malloc`/`realloc` return.
- `realloc` result assigned directly back to the original pointer (leaks the block on failure).
- A buffer function that can leave its output unterminated.

**Carry-through.** One wrong helper used consistently downstream costs marks once.

---

*PROG 101 · Week 0 · Lab Solutions · Instructor Copy · © CSE Department*
