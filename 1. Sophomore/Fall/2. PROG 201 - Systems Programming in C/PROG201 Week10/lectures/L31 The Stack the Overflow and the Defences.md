# PROG 201 · Systems Programming in C
## Week 10 · Lecture 1 of 3
### The Stack, the Overflow, and the Defences

---

**Reading:** CS:APP §3.10.3–3.10.4 · Aleph One, *Smashing the Stack for Fun and Profit* (1996) · `man 1 setarch`, `man 5 proc` (`randomize_va_space`) · **Previous:** L30 · **Next:** L32 — return-oriented programming

---

> **Everything in this week is done in a sandbox, on binaries the course gives you.** The targets are
> compiled with protections deliberately removed and run under `setarch -R`, which turns off address
> randomisation **for that one process** — the machine-wide setting is never touched. Nothing here is
> a technique for attacking a program you were not handed. The reason to learn how these attacks
> work is in the second half of every lecture: **you cannot reason about a defence you have not seen
> defeated.**

---

## 1. What the Overflow Overwrites

Week 6 said a function's locals live on the stack. Here is what else does. On x86-64, a call pushes the return address, and the callee's frame grows *downward* from there:

```
higher addresses
    ...
    saved return address   <- where `ret` will jump
    saved %rbp
    char buf[64]            <- a local array, growing UP toward the return address
    ...
lower addresses            <- %rsp
```

**A write past the end of `buf` runs straight into the saved return address.** Nothing separates them; the array and the control-flow target are adjacent memory. `gets(buf)` reads until a newline with no bound, so a long line writes through `buf`, through the saved `%rbp`, and into the return address — and when the function returns, the CPU jumps wherever those eight bytes now say.

This is the whole vulnerability, and it is one function call old: `gets` has been documented as impossible to use safely since the 1990s and was finally removed from C11, and it is still in a hundred codebases under other names.

---

## 2. Finding the Distance

The only number the attack needs from the stack is the distance from the start of `buf` to the saved return address. You find it by overwriting with a marker and seeing where it lands.

Send 72 `A`s and then eight `B`s to the course's `vuln`, under a debugger:

```
$ python3 -c "import sys; sys.stdout.buffer.write(b'A'*72 + b'BBBBBBBB\n')" > in72
$ setarch -R gdb -q -ex 'run < in72' ./vuln
Program received signal SIGSEGV
(gdb) x/gx $rsp
0x7fffffffd1f0:  0x4242424242424242
```

**`0x42` is `B`.** The eight bytes after 72 padding bytes are exactly what the `ret` tried to use as an address. So the offset is **72**, and everything from byte 72 onward is a return address the attacker chooses. (`buf` is 64 bytes; the extra 8 is the saved `%rbp` in between.)

Real tools automate this with a **cyclic pattern** — a De Bruijn sequence where every 8-byte window is unique, so the crashed `%rsp` value tells you the offset directly. The manual version above is enough to see what is happening.

---

## 3. The First Defence: the Stack Canary

The compiler's answer, on by default since the mid-2000s: put a random value between the locals and the saved return address, and check it is untouched before returning.

```
    saved return address
    saved %rbp
    CANARY                  <- a random 8 bytes, checked on the way out
    char buf[64]
```

You can see it in any normal binary:

```
$ objdump -d prog | grep -c "fs:0x28"      # the canary is read from %fs:0x28
5
```

`%fs:0x28` is thread-local storage — the canary is per-thread and set at startup from the kernel's random pool. An overflow that reaches the return address **must** cross the canary, so on the way out `__stack_chk_fail` sees a changed value and aborts:

```
$ python3 exploit.py | setarch -R ./vuln_canary
*** stack smashing detected ***: terminated       (exit 134, SIGABRT)
```

**Measured: the identical overflow that hijacks the unprotected binary is caught by the canary and turns into a controlled abort.** That is the difference between an exploit and a crash report.

What the canary does **not** stop:

- **A write that skips it.** An overflow through an *index* — `buf[user_controlled] = x` — reaches the return address without touching the canary. Canaries stop contiguous overruns, not arbitrary writes.
- **A leak.** If the program prints uninitialised stack or has a format-string bug (L33), the attacker reads the canary and writes it back unchanged.
- **The overwrite of a local before the canary** — a function pointer or a length field lower in the frame.

The canary is `-fstack-protector-strong` and it is nearly free (one load, one compare, one branch per protected function). **Never turn it off**, and the course's target only lacks it because the lab's whole point is to show you what it was doing.

---

## 4. The Second Defence: NX, and Why It Created ROP

The classic 1996 attack put the *code* on the stack: fill `buf` with machine-code instructions ("shellcode"), and point the return address back into `buf`. The CPU returns into the buffer and runs the attacker's code.

**NX — the no-execute bit — ended that.** Every page has an execute permission, and the stack is mapped without it:

```
$ readelf -l vuln | grep -A1 GNU_STACK
  GNU_STACK  ...  RW      0x10         <- read+write, NOT execute
```

Return into the stack now and the CPU faults on the first instruction fetch:

```
$ python3 shellcode.py | setarch -R ./vuln
Segmentation fault       (exit 139)
```

**Measured: shellcode on a non-executable stack does not run — it SIGSEGVs on the instruction fetch.** On a pre-2004 executable stack (`-z execstack`) the same bytes would have run; NX is why the attack of *Smashing the Stack* stopped working.

**And NX is exactly why the next lecture exists.** If you cannot inject code, you reuse code that is already there and already executable — the program's own instructions. That is return-oriented programming, and it is the direct consequence of this one defence.

---

## 5. The Third Defence: ASLR, and the PIE It Needs

ROP and ret2libc both need the *address* of the code they reuse. Address-space layout randomisation moves things every run so the attacker cannot know those addresses.

`setarch -R` turns it off for one process, which is how the sandbox works:

```
$ ./leak; ./leak; ./leak                 # ASLR on: stack moves every run
0x7ffc17efdfa0
0x7ffd0d335310
0x7ffe6097e0b0
$ setarch -R ./leak; setarch -R ./leak   # ASLR off: fixed
0x7fffffffd340
0x7fffffffd340
```

But ASLR has a gap that is the most important thing in this lecture, and it is measured:

**ASLR randomises the stack, the heap, and shared libraries — but on a non-PIE executable it does *not* randomise the program's own code.** A non-PIE binary is loaded at a fixed address (0x400000), so its functions and gadgets are in the same place every run. Our fixed-address ROP chain **still works with ASLR fully on**, as long as the target is non-PIE:

```
$ python3 exploit.py | ./vuln            # no setarch, ASLR on
[unlock] correct key -- launching a shell
```

**PIE is what closes the gap.** A position-independent executable (Week 8 L26 §6) is loaded at a random base too, so its own code moves:

```
$ python3 exploit.py | ./vuln_pie        # PIE + ASLR
Segmentation fault                        # the hardcoded 0x4011f6 is not where unlock is
```

So the real defence is **ASLR *and* PIE together**, which is why every distribution now compiles executables as PIE by default. ASLR alone protects the libraries; PIE protects the program. An attacker facing both needs an **information leak** — some bug that prints an address — to defeat the randomisation before the address-dependent part of the exploit can run, and half of modern exploitation is finding that leak.

---

## 6. The Layers, and How They Compose

Four defences, and the order they were added is the order attacks defeated the previous one:

| Defence | Stops | Defeated by | On by default |
| --- | --- | --- | --- |
| **Stack canary** | contiguous overwrite of the return address | index writes, leaks, lower-frame targets | yes (`-fstack-protector-strong`) |
| **NX** | executing injected code | **reusing existing code — ROP** (L32) | yes |
| **ASLR** | knowing library addresses | an information leak; and it misses non-PIE code | yes (kernel) |
| **PIE** | knowing the program's own addresses | an information leak | yes |

**No single one is sufficient and together they are strong.** The measured picture from this lecture:

- canary alone turned the exploit into an abort;
- NX alone turned shellcode into a SIGSEGV but left ROP open;
- ASLR alone left a non-PIE binary fully exploitable;
- PIE closed that.

**Defence in depth is not a slogan here; it is the literal design.** An attacker must defeat every layer, and each layer costs them a separate capability — a non-contiguous write, a code-reuse technique, and an information leak. A program that has all four and no memory-disclosure bug is, against this class of attack, genuinely hard.

The rest of the week is the two things that get through anyway: **code reuse** (L32, the answer to NX) and **format strings** (L33, an answer to both the canary and ASLR, because it both reads and writes).

---

## Summary

- A stack buffer and the saved return address are **adjacent memory**; an unbounded write into the buffer overwrites the address the function returns to. `gets` is the canonical way in.
- The only stack number the attack needs is the **offset to the return address** — 72 here, found by overwriting with a marker.
- **The stack canary** puts a random value before the return address; the identical exploit becomes `*** stack smashing detected ***` (exit 134). It does not stop index writes, leaks, or lower-frame targets.
- **NX** makes the stack non-executable: shellcode on the stack **SIGSEGVs** (exit 139), which is precisely why ROP was invented.
- **ASLR randomises the stack, heap and libraries but not a non-PIE program's own code** — the fixed-address chain still worked with ASLR on. **PIE** closes that gap; both together need an information leak to defeat.
- The four layers compose: each costs the attacker a separate capability, which is what "defence in depth" concretely means.

---

## Exercises

1. Find the offset to the return address in the course's `vuln` yourself, with the marker method and then with a cyclic pattern. Do they agree?
2. Compile the same source with and without `-fstack-protector-strong` and diff the disassembly of the vulnerable function. Where are the extra instructions, and what do they read?
3. Overwrite the return address with the address of a function that takes no argument, and confirm it runs. Why does adding a `system()` call inside it then crash, and what one extra gadget fixes it? *(L32 §3.)*
4. Turn the stack executable with `-z execstack` and get the shellcode from §4 to run. Then turn it off and watch it SIGSEGV. What was the exit code each time?
5. Run the fixed-address exploit against the non-PIE target with ASLR on, and then against the PIE target. Explain the difference in one sentence about which regions ASLR moves.
6. A canary protects the return address. Write a program with a function pointer *below* the buffer and overwrite that instead. Does the canary fire? Why not?
7. Read `randomize_va_space` in `man 5 proc`. What do the values 0, 1 and 2 mean, and which one does `setarch -R` give you for a single process?

---

*PROG 201 · Week 10 · L31 · © CSE Department*
