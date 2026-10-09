# CS 201 · Computer Organization & Architecture
## Week 9 · Lecture 1 of 3
### The Stack Under Attack — Buffer Overflows

*“In any respectable branch of engineering, failure to observe such elementary precautions would have long been against the law.”* — C. A. R. Hoare, on array bounds checking, "The Emperor's Old Clothes", Turing Award Lecture (1980)

---

**Reading:** CS:APP §3.10.3–3.10.4 · **Previous:** L27, the application layer

**Coursework:** 📊 **Quiz 9** today · 🔬 **Lab 8** Tue this week 15:00–16:50 · 📝 **PS 9** released Wed this week, due Fri of Week 10 17:00 · 📋 **Project 1** due Fri this week 17:00 · 📝 **PS 8** due Fri this week 17:00 · 📘 **Midterm 2** Mon of Week 10 18:00–19:15

---

## A Note on What This Week Is For

**This is a defensive course.** You are learning how memory-safety attacks work so that you can write code that is not vulnerable to them and understand the defenses that protect the code you cannot rewrite.

**Every demonstration in this week runs on a small program you compiled yourself**, with the defenses deliberately switched off so their absence is visible. Nothing here targets a system you do not own, and the real lesson of the week is the last one: **on a modern machine, with the defaults left on, all of this is much harder than it looks — by design.**

---

## 1. The Vulnerability Is One Missing Check

Week 3 established the single fact this entire week rests on: **`ret` pops eight bytes off the stack and jumps to them, and nothing validates the value.**

Here is a function with a memory-safety bug, and it is a bug you have written:

```c
void vuln(const char *in) {
    char buf[16];
    strcpy(buf, in);        /* copies until a NUL — no length limit */
}
```

`strcpy` copies until it finds a zero byte. **If `in` is longer than 16 bytes, it writes past the end of `buf`** — and the stack grows down, so "past the end" is toward the saved registers and the return address.

```
   high addresses
   ┌─────────────────────┐
   │ return address      │  <- strcpy overwrites this if `in` is long enough
   ├─────────────────────┤
   │ saved rbp           │
   ├─────────────────────┤
   │ buf[16]             │  <- strcpy starts here and writes upward
   └─────────────────────┘
   low addresses
```

**This is the whole mechanism.** The attacker does not need to defeat any check, because there is no check. `strcpy` will faithfully write as many bytes as it is given.

---

## 2. Where the Bytes Land

Compiled at `-O0` with defenses off, `vuln`'s frame is:

```
sub    rsp, 0x20            ; 32-byte frame
lea    rax, [rbp-0x10]      ; buf is at rbp-0x10
```

*(Verified.)* So from the start of `buf`:

| Bytes | Reaches |
|---:|---|
| 0–15 | `buf` itself |
| 16–23 | saved `rbp` |
| **24–31** | **the return address** |

**Overwrite bytes 24–31 and you have chosen where `ret` goes.**

Confirming it in a debugger — the safe, controlled way, exactly as Week 3's Lab did:

```
(gdb) break *vuln+46          # just after the copy
(gdb) run
(gdb) x/gx $rbp+8             # the return address slot
0x7fffffffd258:  0x00000000004011b6    <- now points at win(), not the caller
(gdb) p (void*)win
$1 = (void *) 0x4011b6 <win>
```

*(Verified — the return address was overwritten to a function the program never calls.)*

> **Notice how delicate it already is.** Getting `ret` to land on `win` is easy; getting the program
> to keep running cleanly afterward is not — the alignment rule from Week 3 §L12 bites immediately,
> because `win` then calls `puts`, and `puts` uses `movaps` on a stack that is now misaligned.
> **Real exploitation is fiddly**, and that fiddliness is one of the reasons defenses work.

---

## 3. Classic Code Injection, and Why It No Longer Works

The 1990s version went further: the attacker put **machine code** — shellcode — into `buf` itself, and pointed the return address back into `buf`. The program would `ret` into the attacker's bytes and execute them.

**This worked because the stack was executable.** It is not any more.

You saw the defense in Week 3 without naming it as one. When you omitted `.note.GNU-stack` from an assembly file, `readelf` showed `GNU_STACK` change from `RW` to `RWE`. **`RW` is the defense**: the stack is readable and writable but **not executable** — the **NX bit** from Week 6 §L19, set in every page table entry covering the stack.

```
$ readelf -lW ./prog | grep GNU_STACK
  GNU_STACK  ...  RW  0x10
```

*(Verified — this is the default.)*

**So bytes written to the stack cannot be run as code.** Straight code injection is dead. The attacker's response — reusing code that is already executable — is L29.

---

## 4. The Defense You Cannot See: the Stack Canary

Compile the *same* vulnerable function with today's defaults and look at what GCC inserted:

```
vuln:
    ...
    mov    rax, QWORD PTR fs:0x28      ; load a secret value
    mov    QWORD PTR [rbp-0x8], rax    ; place it just below the return address
    ...                                ; (the vulnerable strcpy runs here)
    mov    rax, QWORD PTR [rbp-0x8]    ; reload it
    sub    rax, QWORD PTR fs:0x28      ; compare with the original
    je     ok
    call   __stack_chk_fail            ; mismatch -> abort
ok: leave
    ret
```

*(Verified — GCC 13.3 at `-O0`, no flags. `-fstack-protector-strong` is on by default.)*

**The canary is a random value placed between the local buffers and the saved return address.** An overflow large enough to reach the return address must first overwrite the canary. Before `ret`, the function checks it. **A buffer overflow now aborts instead of returning to attacker-controlled code:**

```
$ ./prog "$(python3 -c 'print("A"*40)')"
*** stack smashing detected ***: terminated
```

*(Verified.)*

**Why it is hard to defeat.** The canary is read from `fs:0x28` — thread-local storage the attacker cannot read through the overflow — and it is randomised per process. **To overwrite the return address without tripping it, the attacker would have to write the exact canary value, which they do not know.** A byte-by-byte overflow that stops at the canary cannot reach the return address.

**Its limits, which L29 exploits:** it protects the *return address*, not other targets, and a bug that reads memory (a format-string leak, L30) can disclose the canary and defeat it.

---

## 5. The Defense That Moves the Target: ASLR

Even with an executable stack, an attacker needs to know *where* their payload is — an address to jump to. **Address Space Layout Randomization makes that address different every run.**

```
$ for i in 1 2 3; do ./prog; done
stack 0x7fff79d19a14  main 0x57b51ea0f169
stack 0x7ffd8989f8f4  main 0x6533c801a169
stack 0x7fffecae3594  main 0x5eaa4a3f8169
```

*(Verified — every base address changes.)* You saw this in Week 6's `/proc/self/maps` without a name: the addresses moved between runs.

**Turn it off and the addresses freeze:**

```
$ setarch -R ./prog ; setarch -R ./prog
stack 0x7fffffffd3b4  main 0x555555555169
stack 0x7fffffffd3b4  main 0x555555555169
```

*(Verified — identical.)*

**ASLR does not fix the bug. It denies the attacker the addresses they need to exploit it**, so an exploit written for one run fails on the next. Combined with a non-executable stack and a canary, it is why the 1990s stack smash does not simply work today.

**Its weakness** is that only the *base* is randomised, and only the high bits move — the low 12 bits are the page offset and are constant, because a page cannot be relocated within itself. A single leaked address de-randomises everything at that layer, which is again why the memory-*disclosure* bugs of L30 matter as much as the memory-*corruption* ones.

---

## 6. Writing Code That Is Not Vulnerable

The bug was never the stack layout. **It was an unbounded copy.** The fixes are ordinary:

| Instead of | Use | Why |
|---|---|---|
| `strcpy(d, s)` | `snprintf(d, n, "%s", s)`, or `strlcpy` | Bounded by the destination size |
| `gets(buf)` | `fgets(buf, n, stdin)` | `gets` cannot be used safely and was removed from C11 |
| `sprintf(d, ...)` | `snprintf(d, n, ...)` | Bounded |
| Manual length maths | `__builtin_add_overflow`, or a checked allocator | L30 |
| Nothing | **`-fsanitize=address`** in testing | Reports the overflow with a stack trace |

**And turn the warnings on.** `-Wall -Wextra` flags many of these, and **AddressSanitizer catches the overflow at the moment it happens**, pointing at the exact line — which is worth far more in development than any runtime defense.

> **The defenses of §4 and §5 are for the code you cannot fix** — the library you did not write, the
> binary you cannot recompile. **For your own code, the fix is to not write the bug**, and the tools
> to find it before you ship exist and are free.

---

## 7. What to Take Away

1. **The vulnerability is a missing bounds check**, not anything exotic. `strcpy` writes what it is given.
2. **The return address is at a fixed offset from the buffer** — 24 bytes here — and overwriting it chooses where `ret` goes.
3. **NX killed straight code injection.** The stack is `RW`, not `RWE`.
4. **The stack canary** aborts an overflow that reaches the return address, and it is read from a per-process secret the attacker cannot see.
5. **ASLR** denies the attacker the addresses they need — every base moves each run.
6. **These defenses compose**, which is why the classic attack no longer simply works.
7. **For your own code, the fix is the bounded call and the sanitizer**, not the runtime defense.

---

## Exercises

1. `buf[16]` sits at `rbp-0x10`. How many bytes must be written to reach the return address? Draw the frame and mark each region.
2. The same overflow "works" under GDB (the return address changes) but the program crashes rather than running cleanly. Explain, referring to Week 3 §L12.
3. `readelf -lW` shows `GNU_STACK RW`. What attack does the missing `E` prevent, and what did Week 3's Lab do to add it back?
4. A canary is read from `fs:0x28` rather than kept in a normal variable. Why does that matter for its security?
5. ASLR randomises the base but not the low 12 bits. Explain why, and say what a single leaked pointer gives an attacker.
6. Rewrite `vuln` so it cannot overflow, and name a compiler flag that would have caught the original in testing.

---

*Next: L29 — when the code the attacker needs is already in the program.*
