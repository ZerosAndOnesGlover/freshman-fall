# CS 201 · Week 9 · Lab 9
## Defenses at Work — Canaries, ASLR, NX, and the Sanitizer

---

**When:** **Tuesday of Week 10**, 15:00–16:50, BH 210 — *after* Week 9's three lectures
**Covers:** Week 9 · **Assessment:** unmarked, checked off by the TA
**You need:** `gcc`, `gdb`, `objdump`, `readelf`, `python3`.

> **This lab is defensive.** Every program is one you compile yourself, in this directory, with the
> defenses deliberately switched off so you can see what they do. **Nothing here touches a system you
> do not own.** The point is to understand the mitigations well enough to trust them and to write
> code that does not need them.

---

## Part 1 — See the Canary (20 min)

```c
/* vuln.c */
#include <stdio.h>
#include <string.h>
void vuln(const char *in) { char buf[16]; strcpy(buf, in); puts(buf); }
int main(int c, char **v) { vuln(c > 1 ? v[1] : "hi"); return 0; }
```

```bash
gcc -O0 -g -o vuln vuln.c              # today's defaults — canary ON
objdump -d --no-show-raw-insn -M intel vuln | sed -n '/<vuln>:/,/ret/p'
```

Find these four instructions:

```
mov  rax, QWORD PTR fs:0x28      ; load the canary from thread-local storage
mov  QWORD PTR [rbp-0x8], rax    ; place it below the return address
...                              ; strcpy runs here
mov  rax, QWORD PTR [rbp-0x8]    ; reload
sub  rax, QWORD PTR fs:0x28      ; compare
je   ...                         ; match -> return; mismatch -> __stack_chk_fail
```

*(Verified — this is the default `-O0` output, no flags.)*

**Answer:**

1. **Why is the canary read from `fs:0x28` rather than kept in an ordinary local variable?**
2. It sits at `rbp-0x8` — just below the saved return address at `rbp+8`. Why *there* and not at the bottom of the frame?
3. Now overflow it:
   ```bash
   ./vuln "$(python3 -c 'print("A"*40)')"
   ```
   Expected: `*** stack smashing detected ***: terminated` *(verified)*. **Explain what the check found.**

**✅ CHECKPOINT 1** — the four instructions and your three answers.

---

## Part 2 — See the Overwrite, Safely (25 min)

Now compile the **same code with the canary off**, and watch the overwrite in GDB — exactly the controlled experiment from Week 3's Lab 3.

```bash
gcc -O0 -g -fno-stack-protector -no-pie -z noexecstack -o vuln_nc vuln.c
```

```
(gdb) break *vuln+46          # after the strcpy (find the exact address with: disas vuln)
(gdb) run $(python3 -c 'print("A"*24 + "BBBBBBBB")')
(gdb) x/gx $rbp+8             # the return-address slot
0x7fffffffd258:  0x4242424242424242    <- "BBBBBBBB", your bytes
```

**You have overwritten the return address with `0x42` bytes.** With a real function address there instead, `ret` would jump to it.

**Answer:**

1. It took **24** bytes of padding to reach the return address. Derive that from the frame: `buf` is at `rbp-0x10`. Draw it.
2. The `strcpy` version cannot place a real address containing a **zero byte** (most addresses do). Why? *(What does `strcpy` stop at?)* This is a genuine constraint on real exploits.
3. Even when the address is placed correctly, the program often crashes *inside* the target function rather than running cleanly. Explain, citing Week 3 §L12. *(Hint: `movaps`.)*

> **Do this under GDB, not by feeding addresses on the command line.** The debugger is the safe,
> legible way to see the mechanism, and the null-byte problem in (2) is exactly why command-line
> payloads are awkward.

**✅ CHECKPOINT 2** — the overwritten return address and your three answers.

---

## Part 3 — NX and ASLR (20 min)

### 3.1 The stack is not executable

```bash
readelf -lW vuln | grep GNU_STACK
```

```
GNU_STACK  ...  RW  0x10
```

*(Verified.)* **`RW`, not `RWE`.** Recall Week 3 Lab Part 5.1, where omitting `.note.GNU-stack` produced `RWE`.

**Answer:** which 1990s attack does the missing `E` prevent, and what did the attacker do in response? *(That is L29.)*

### 3.2 Addresses move every run

```c
/* aslr.c */
#include <stdio.h>
int main(void){ int x; printf("stack %p  main %p\n",(void*)&x,(void*)main); return 0; }
```

```bash
gcc -O0 -o aslr aslr.c
for i in 1 2 3 4 5; do ./aslr; done
```

Expected *(verified)*: every address different. Then freeze it:

```bash
setarch -R ./aslr ; setarch -R ./aslr
```

Expected *(verified)*: identical both runs.

**Answer:**

1. What does ASLR deny an attacker? Does it fix the bug?
2. The **low 12 bits** of an address never change under ASLR. Why? *(Week 6.)*
3. A single leaked libc pointer defeats ASLR for all of libc. Explain, connecting to L29 §4.

**✅ CHECKPOINT 3** — GNU_STACK, the two ASLR runs, and your answers.

---

## Part 4 — The Constructive Half: Find Bugs Before They Ship (30 min)

**This is the most important part of the lab.** The runtime defenses of Parts 1–3 are for code you cannot fix. **For your own code, you find the bug in testing — and the tool is AddressSanitizer.**

### 4.1 It catches the overflow, with the line number

```bash
gcc -O0 -g -fsanitize=address -o vuln_asan vuln.c
./vuln_asan "$(python3 -c 'print("A"*40)')"
```

```
==...==ERROR: AddressSanitizer: stack-buffer-overflow ...
WRITE of size 41 at 0x... thread T0
    #0 ... in strcpy
    #1 ... in vuln vuln.c:3
  [32, 48) 'buf' (line 3) <== Memory access at offset 48 overflows this variable
SUMMARY: AddressSanitizer: stack-buffer-overflow ... in strcpy
```

*(Verified.)* **It names the buffer, the line, and the exact overflowing access.** No debugging required — the tool points at the bug.

### 4.2 It catches use-after-free

```c
/* uaf.c */
#include <stdio.h>
#include <stdlib.h>
int main(void){
    int *p = malloc(4*sizeof(int));
    p[0] = 1; free(p);
    printf("%d\n", p[2]);       /* read after free */
    return 0;
}
```

```bash
gcc -O0 -g -fsanitize=address -o uaf uaf.c && ./uaf
```

```
==...==ERROR: AddressSanitizer: heap-use-after-free ...
freed by thread T0 here: ...
SUMMARY: AddressSanitizer: heap-use-after-free uaf.c:4 in main
```

*(Verified.)* **It reports where the memory was freed *and* where it was misused** — the two events a heap bug decouples in time.

### 4.3 The integer-overflow allocation

```c
size_t count = (size_t)1 << 61, size = 16;   /* 2^61 * 16 = 2^65 wraps to 0 */
size_t bytes = count * size;
printf("bytes = %zu\n", bytes);              /* prints 0 */
void *p = malloc(bytes);                     /* tiny buffer */
void *q = calloc(count, size);               /* NULL — refused */
```

*(Verified: `bytes = 0`; `malloc` returns a tiny pointer; `calloc` returns NULL.)*

**Answer:**

1. `-fsanitize=address` costs ~2× runtime. **Why is that a bargain in testing and unacceptable in production?**
2. ASan found the overflow AND named `buf` at line 3. Compare that with the runtime canary from Part 1 — **what does each tell you that the other does not?**
3. Rewrite the integer-overflow allocation so it refuses safely, using `__builtin_mul_overflow`.

**✅ CHECKPOINT 4** — the two ASan reports and your three answers.

---

## Part 5 — The Format-String Leak (15 min)

```c
/* fmt.c */
#include <stdio.h>
void bad(const char *u)  { printf(u);  putchar('\n'); }     /* user string as format */
void good(const char *u) { printf("%s\n", u); }             /* the fix */
int main(int c, char **v){ const char *s = c>1?v[1]:"%p %p %p"; bad(s); good(s); return 0; }
```

```bash
gcc -O0 -g -Wformat-security -c fmt.c     # note the warning
gcc -O0 -g -o fmt fmt.c
./fmt '%p %p %p %p %p'
```

Expected *(verified)*:

```
0x7ffc... (nil) (nil) 0x7293... (nil)      <- bad(): stack contents leaked
%p %p %p %p %p                             <- good(): printed literally
```

and the compile warns:

```
warning: format not a string literal and no format arguments [-Wformat-security]
```

*(Verified — and this warning is in `-Wall`.)*

**Answer:**

1. Where did `printf` get the values it printed for `%p`, given that `bad` passed no arguments? *(Week 3 calling convention.)*
2. Among the leaked stack words could be the canary and a libc pointer. **Why does that make this "just a leak" as dangerous as a memory-corruption bug?**
3. `%n` *writes* instead of reads. In one sentence, what does that turn a format-string bug into?
4. A format-string vulnerability shipped means a compiler warning was ignored. **What does that tell you about the value of `-Wall -Werror`?**

**✅ CHECKPOINT 5** — the leak, the warning, and your four answers.

---

## Before You Leave

| Task | Command |
|---|---|
| See the canary | `objdump -d -M intel prog \| grep fs:0x28` |
| Check defenses on a binary | `readelf -lW prog \| grep GNU_STACK` ; `readelf -d prog \| grep -i now` |
| Count `endbr64` (CET pads) | `objdump -d -M intel prog \| grep -c endbr64` |
| Disable a defense (to study it) | `-fno-stack-protector`, `-no-pie`, `-z execstack` |
| **Find the bug in testing** | `-fsanitize=address,undefined -g` |
| Watch an overwrite | GDB: `x/gx $rbp+8` after the copy |

**The habit:** **compile with `-Wall -Wextra -fsanitize=address,undefined` while developing.** Nearly every attack in this week began as a warning or a sanitizer report that someone did not run. **The cheapest place to stop an exploit is before it ships.**

---

*CS 201 · Week 9 · Lab 9*
