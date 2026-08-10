# CS 201 · Problem Set 9 — Solutions
## Instructor Only

---

> **Not for distribution.** All demonstrations run on the student's own sandboxed programs; figures
> verified on the lab image (GCC 13.3, ASan, i5-8250U). **This is a defensive assignment — the marked
> outcome for Q3 is a *fixed* program, proven with a sanitizer.**

---

## Q1 (24) — The Overflow and Its Defenses

### (a) [4]

| Offset from `buf` | Region |
|---|---|
| 0–15 | `buf[16]` |
| 16–23 | saved `rbp` |
| **24–31** | **return address** |

**24 bytes of input reach the return address** *(buf at `rbp-0x10`: 16 + 8 saved rbp = 24)*.

### (b) [5]

```
mov rax, QWORD PTR fs:0x28      ; load canary from thread-local storage
mov QWORD PTR [rbp-0x8], rax    ; store below the return address
mov rax, QWORD PTR [rbp-0x8]    ; reload after the vulnerable region
sub rax, QWORD PTR fs:0x28      ; compare with the original
je  ...                         ; equal -> return; else __stack_chk_fail
```

*(Verified — default `-O0`.)*

**Read from `fs:0x28`** — thread-local storage, unreachable through a stack overflow and randomised per process — so **the attacker cannot learn the value to reproduce it.** A value in an ordinary local would itself be overwritten by the same overflow.

### (c) [4]

**Output: `*** stack smashing detected ***: terminated`** *(verified)*.

**The epilogue compared the reloaded canary with the original and found them different**, because the overflow wrote through the canary's slot on its way to the return address. **The attacker cannot supply the correct value** — it is random and secret — so any overflow that reaches the return address necessarily corrupts the canary and is caught.

### (d) [5]

**`RW` prevents code injection onto the stack** — the classic stack smash that writes shellcode into the buffer and returns into it. With the stack non-executable (NX), those bytes cannot run.

**The attacker's response is code reuse: ret2libc / ROP** (L29) — jump to code that is already executable rather than injecting new code.

### (e) [6]

*(Verified: five runs give five different `&main`; `setarch -R` gives identical addresses.)*

**ASLR denies the attacker the addresses** they need for a jump target or a gadget. **It does not fix the bug** — the overflow still happens; the attacker just cannot reliably use it. **The low 12 bits never change** because they are the page offset (Week 6): a page can be relocated as a whole but nothing within it moves, so intra-page offsets are fixed.

---

## Q2 (18) — The Arms Race

### (a) [6]

| Attack | Defense | Response |
|---|---|---|
| Stack smash, inject code | **NX** — stack not executable | **ret2libc / code reuse** |
| ret2libc, known addresses | **ASLR** — randomise layout | **Leak an address, then compute** |
| ROP gadget chain | **CFI / CET** — valid targets only | JOP, data-only, sigreturn-oriented |

*(One sentence per mechanism required.)*

### (b) [4]

`/bin/ls`: **203**; libc: **6123** `ret` instructions *(verified)*. **So many exist because every function ends in `ret`**, and `ret` is a single byte. **The usable count is higher** because a `ret` can be reached at an *unaligned* offset — the bytes of a longer instruction reinterpreted mid-stream can form a different, useful gadget ending in `c3`.

### (c) [4]

**`ret` pops eight bytes off the stack into `rip` and jumps** (Week 3). An overflow that controls the stack controls a *sequence* of return targets: each gadget's `ret` pops the next gadget's address and jumps to it. **NX did not stop it because ROP executes no new code** — every gadget is in an already-executable page.

### (d) [4]

**[2]** **Landing pads (`endbr64`)** guard the **forward edge**: an indirect call/jump must land on one, so a jump into the middle of a function (where a gadget lives) faults. **The shadow stack** guards the **backward edge**: a hardware-protected second copy of each return address is compared on `ret`, so an overwritten return address no longer matches and faults.

**[2] To check enforcement:** the compiler emitting `endbr64` proves only that it is *compiled in*. Check the CPU (`grep -E 'shstk|ibt' /proc/cpuinfo`), the kernel config, and whether the process opted in (glibc tunables / `GNU_PROPERTY` notes). **On this i5-8250U, `/proc/cpuinfo` shows no `shstk` — the landing pads exist but the hardware does not enforce a shadow stack.** *(Verified.)*

> **Full marks require the "compiled in ≠ enforced" distinction.** It is the honest lesson of the
> whole week.

---

## Q3 (34) — Fix the Bugs

**The marked artefact is the fixed program plus evidence.** All four fixes below were compiled with `-fsanitize=address,undefined` and verified: sanitizer fires on the original, clean on the fix.

### (a) [8] — stack buffer overflow

**Bug:** `strcpy` into a fixed `char buf[64]` from an arbitrary-length `s` — stack overflow. **Consequence:** overwrites the canary / return address; with defenses off, control-flow hijack.

**Fix:** size to the input.

```c
char *dup_upper(const char *s) {
    size_t n = strlen(s);
    char *buf = malloc(n + 1);
    if (!buf) return NULL;
    for (size_t i = 0; i < n; i++) buf[i] = toupper((unsigned char)s[i]);
    buf[n] = 0;
    return buf;                 /* caller frees */
}
```

*(Verified: ASan reports `stack-buffer-overflow` at the `strcpy` line on the original; the fix handles a 75-char input cleanly.)* Accept `snprintf`/`strlcpy` into a bounded buffer if the truncation is intentional and documented.

> Also accept — and reward — a student who notices the original returns `strdup(buf)` and asks who
> frees it; the `toupper((unsigned char)...)` cast to avoid UB on negative `char` is a bonus.

### (b) [8] — integer-overflow allocation

**Bug:** `n * sizeof(int)` wraps for large `n`, producing a small allocation the loop then overflows. **Consequence:** heap overflow.

**Fix:**

```c
int *make_array(size_t n) {
    size_t bytes;
    if (__builtin_mul_overflow(n, sizeof(int), &bytes)) return NULL;
    return calloc(n, sizeof(int));      /* calloc also checks internally */
}
```

*(Verified: `make_array((size_t)1<<62)` returns NULL — $2^{62}\times 4 = 2^{64}$ wraps to 0 — and `make_array(8)` works. Note $2^{61}$ does **not** overflow when the multiplier is 4; the wrap needs $n \ge 2^{62}$.)*

### (c) [8] — format string

**Bug:** `fprintf(logfile, user_msg)` uses attacker data as a format string. **Consequence:** `%p`/`%x` leak memory (stack, canary, libc pointers); `%n` writes memory.

**Fix:**

```c
void log_msg(const char *user_msg) {
    fprintf(logfile, "%s", user_msg);
}
```

*(Verified: `-Wformat-security` warns on the original; a `%p`-laden input leaks stack words from the original and prints literally from the fix.)*

### (d) [10] — two bug classes

**Bug 1 — unchecked index:** `cache[i]` with `i` unvalidated is an out-of-bounds read/write. **Bug 2 — use-after-free / dangling pointer:** `reset()` frees `cache` and reallocates, but any index computed against a stale assumption, or a `get` between the `free` and the reassignment, is a use-after-free. *(A caller pattern `reset(); get(5); reset(); get(5)` exercises the stale-pointer window.)*

**Fix:** bound the index against a stored length, and null the pointer on free so a stale use is a clean crash rather than silent corruption:

```c
static int *cache;
static size_t cache_n;
void set(size_t i, int v) { if (i < cache_n) cache[i] = v; }
int  get(size_t i)        { return i < cache_n ? cache[i] : 0; }
void reset(void) {
    free(cache);
    cache = calloc(1024, sizeof(int));
    cache_n = cache ? 1024 : 0;
}
```

*(Verified: ASan reports `heap-buffer-overflow` for an out-of-range index and `heap-use-after-free` for the stale-pointer pattern on the original; the fix is clean.)*

**Naming both classes is required for full marks** — a student who fixes only the bounds check keeps 6 of 10.

---

## Q4 (16) — The Security Mindset

### (a) [4]

**Trust no input** — e.g. Week 8's length-prefix framing: a claimed length is not a fact. **Read what code *can* do** — e.g. Week 1's signed overflow, where `x+1>x` *can* be assumed always true and the check deleted. **Defence in depth** — e.g. this week's layered canary + NX + ASLR + CET. *(Any concrete earlier-week example per principle.)*

### (b) [4]

**A leak defeats the canary and ASLR** — the two defenses that rely on the attacker *not knowing* a value. Leak the canary and an overflow can reproduce it; leak one libc pointer and the whole library's gadget layout is de-randomised. **A serious exploit chains a disclosure bug with a corruption bug**, which is why the leak is as valuable as the corruption.

### (c) [4]

**TOCTOU example:** `access(path, W_OK)` then `open(path)`; an attacker swaps `path` for a symlink between the two. **Atomic fix:** `open` first (with `O_NOFOLLOW` as appropriate) and check the returned descriptor's properties with `fstat`, never re-resolving the name. **It is a security bug** because the gap lets an adversary make a privileged action operate on a target the check never approved — a privilege escalation, not merely a wrong answer.

### (d) [4]

**Accept either side, argued.** The strong case *for*: every mitigation here — canary, NX, ASLR, CET, ASan — exists to detect or hinder an out-of-bounds access that the language permitted in the first place; a bounds-checked language emits none of them because the access cannot occur. **A design that removes the vulnerability:** Rust's ownership/borrow model (compile-time), or any bounds-checked array type (run-time), or a garbage-collected language for use-after-free. **The honest counter**, worth credit: those carry costs — runtime bounds checks, GC pauses, borrow-checker friction — and C's permission is *also* what makes the systems programming in this course possible. **Week 12 returns to exactly this trade.**

---

## Mark Summary

| | |
|---|---:|
| Q1 | 24 |
| Q2 | 18 |
| Q3 | 34 |
| Q4 | 16 |
| **Total** | **100** |

**Where the class loses marks, in order:**

1. **Q3(d)** — fixing one of the two bug classes and missing the other.
2. **Q2(d)** — asserting CET is "on" because `endbr64` is present, without checking enforcement.
3. **Q1(e)** — saying ASLR "fixes" the bug rather than denying the attacker addresses.
4. **Q3** generally — a fix with no sanitizer evidence. **The evidence is half the mark.**
5. **Q4(b)** — not naming *which two* defenses a leak defeats.

**A note on grading tone:** reward students who write the bounded, checked, sanitizer-clean version and can explain *why each defense exists*. The goal of this week is engineers who do not ship the bug — not students who can describe an attack.

---

*CS 201 · Week 9 · PS 9 Solutions · Instructor Only*
