# PROG 201 · Systems Programming in C
## Week 10 · Lecture 3 of 3
### Format Strings, Heap Bugs, and the Tools That Find Them

*“Program testing can be used to show the presence of bugs, but never to show their absence!”* — Edsger W. Dijkstra, "Notes on Structured Programming" (EWD249, 1970)

---

**Reading:** *The Art of Software Security Assessment* Ch. 8 · `man 3 printf` (the `%n` note) · the AddressSanitizer and libFuzzer docs · **Previous:** L32 · **Next:** Lab 10 — fuzzing, **Monday of Week 11**

**Coursework:** 📋 **Project 2** released Fri this week, due Fri of Week 12 17:00 · 📝 **PS 9** due Fri this week 17:00 · 🔬 **Lab 10** Mon of Week 11 15:00–16:50 · 📊 **Quiz 11** Tue of Week 11 · 📝 **PS 11** released Wed of Week 11, due Fri of Week 12 17:00

---

> **Sandboxed targets, as all week.** The heap and format-string bugs here are in programs written
> to contain them; the value is in seeing what the sanitizers catch and what ships without them.

---

## 1. The Format String Bug Is Two Primitives in One

The bug is one line:

```c
printf(user_input);        /* instead of printf("%s", user_input) */
```

If the user controls the format string, `printf` obeys its directives — and two of them are catastrophic.

**`%p` reads.** Each conversion specifier consumes an argument; `printf` was given none, so it reads whatever is on the stack where the arguments would have been:

```
$ ./fmt 'AAAA %p %p %p %p %p'
AAAA 0x7fff5f8ee89e 0xffffffffffffffe9 0x16 (nil) 0x7e997b37d380
```

**Those are live addresses off the stack** — stack pointers, saved registers, and eventually the format string itself. `%p` at a high enough position reads the input back:

```
$ ./fmt "$(python3 -c "print('%p '*10)")"
... 0x7025207025207025          <- "%p %p" as bytes: the string is on the stack
```

**That defeats ASLR.** One leaked stack or libc address, and the randomisation the attacker could not predict is now known — which is the information leak L31 §5 and L32 §4 said every real exploit needs. A format-string bug is often the leak that makes a ROP chain possible.

**`%n` writes.** `%n` stores the number of characters printed so far *through a pointer argument*. With a controlled stack, the attacker chooses the pointer:

```
$ ./fmt 'AAAAAAAA%7$n'
Segmentation fault            (exit 139)
```

`%7$n` fetched the 7th argument slot — which holds the `AAAAAAAA` bytes — and tried to write through it. Point it at a real address instead (using `%N$n` to select a stack slot the attacker placed an address in) and it is an **arbitrary write**: any value, to any location, by controlling how many characters are printed before the `%n`. That is enough to overwrite a return address, a GOT entry (Week 8 L26 §4), or a function pointer.

**One bug, both a read and a write primitive**, which is why format-string bugs were once the most valued class there was. The defence is not a mitigation; it is **never passing user data as a format string**, which `-Wformat-security` warns about and which is now a compile error under `-Werror=format-security` in most distributions.

*(glibc has a partial runtime defence — it can refuse `%n` when the format lives in writable memory — but it is not enforced in every build, and the `%p` read primitive it does nothing about. The compile-time rule is the real fix.)*

---

## 2. Heap Bugs Are Silent Without a Sanitizer

The stack bugs above announce themselves — a crash, a canary abort. Heap bugs mostly do not, which is why they ship.

**Use-after-free**: reading memory after it is freed.

```c
char *p = malloc(32); strcpy(p, "hello"); free(p);
return p[0];                 /* the freed byte */
```

**Double-free**: freeing the same pointer twice.

Run both without a sanitizer:

```
$ ./heap_plain u ; echo $?        # use-after-free
5                                  <- returned "successfully", garbage value
$ ./heap_plain d ; echo $?        # double-free
0                                  <- returned 0, no error at all
```

**Both programs exit cleanly.** The use-after-free read stale memory and the double-free did nothing visible — and this is the normal case. A use-after-free is exploitable because the attacker can `malloc` the freed region back (it is on a free list) and control what the dangling pointer now points at; a double-free corrupts the allocator's free list so a later `malloc` returns an attacker-chosen address. Neither is visible in testing, because **nothing checks**.

**AddressSanitizer checks.** Rebuild with `-fsanitize=address`:

```
$ ./heap u
==ERROR: AddressSanitizer: heap-use-after-free
    freed by thread T0 here: ...
    previously allocated by thread T0 here: ...
$ ./heap d
==ERROR: AddressSanitizer: attempting double-free
```

**Measured: the same two bugs that ran silently are caught, with the free site and the allocation site both named.** ASan puts a red-zone around every allocation and marks freed memory poisoned; every load and store is instrumented to check the shadow map. It costs about 2× in time and memory, which is why it is a *testing* tool, not a production one — but as a testing tool it turns "silent and exploitable" into "a stack trace at the exact line".

The families ASan catches, all measured elsewhere this course or above: heap and stack buffer overflow, use-after-free, double-free, use-after-return, and (with `LeakSanitizer`, on by default) leaks.

---

## 3. Fuzzing: Finding the Input You Did Not Think Of

A sanitizer tells you a bug happened. **Fuzzing finds the input that triggers it** — by generating enormous numbers of inputs, running the target on each, and watching for a crash.

The curriculum specifies **AFL**. It is not installed on these machines and a student account cannot add it — so the course uses **libFuzzer**, which ships inside clang and needs only a one-line entry point:

```c
int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    parse(data, size);        /* the code under test */
    return 0;
}
```

```
$ clang -fsanitize=fuzzer,address -o fuzz target.c
$ ./fuzz corpus
```

That is **coverage-guided** fuzzing, which is the important idea and the reason it works. libFuzzer does not throw random bytes; it instruments the target so it can see **which branches each input reaches**, keeps inputs that reach new code, and mutates those. So it *learns* the structure of valid input by feedback, finding its way past `if (data[3] == 'R')` checks that random bytes would pass one time in 256.

Run it on a parser with three planted bugs:

```
$ ./fuzz corpus
==ERROR: AddressSanitizer: heap-buffer-overflow
    READ of size 1 ... in parse
SUMMARY: AddressSanitizer: heap-buffer-overflow parse_target.c:15:29 in parse
```

**Measured: libFuzzer plus ASan found a planted out-of-bounds read, pinpointed to `parse_target.c:15:29`, from a 13-byte reproducer — after about ten executions with a seeded corpus.** The crashing input is saved automatically, so the bug is reproducible forever after.

Two honest points about fuzzing:

- **It is stochastic.** The same fuzzer with a different random seed found the same bug in ten executions or in hundreds of thousands, depending on the seed. A bug found fast on one run may take much longer on another; "the fuzzer found nothing in an hour" is not proof of no bug.
- **Coverage guidance is what makes it practical.** A "dumb" fuzzer throwing random bytes at the same parser would need, on average, 256 tries just to get past the one-byte magic check, and exponentially more for each subsequent check. Feedback turns an exponential search into a roughly linear one, and it is the single idea that made fuzzing go from a curiosity to how Chrome, the kernel, and every serious C codebase are now tested (Google's OSS-Fuzz runs it on thousands of projects continuously).

---

## 4. The Modern Development Loop

Put the three together and you have how memory-safety bugs are actually kept out of C today — not by writing perfect code, but by **making the bugs loud during testing**:

1. **Compile with the warnings on.** `-Wall -Wextra -Werror=format-security` makes the format-string bug a build failure.
2. **Test under sanitizers.** `-fsanitize=address,undefined` turns silent heap and integer bugs into stack traces. Run your existing test suite this way; it costs nothing to write.
3. **Fuzz the parsers.** Anything that consumes untrusted input — a file format, a network protocol, a command line — gets a `LLVMFuzzerTestOneInput` and runs continuously.
4. **Ship with the mitigations on.** Canary, NX, ASLR, PIE, full RELRO (Week 8), and CFI or a shadow stack where available — so that a bug that survives all of the above is still hard to exploit.

**The two halves are different jobs.** Steps 1–3 find bugs and are done by the developer during testing; step 4 makes the surviving bugs expensive and is done by the compiler and the OS in production. This week has been the second half — the mitigations, and why each one exists — but the leverage is in the first half. **The cheapest exploit to defend against is the bug that never shipped**, and a `-fsanitize=address` test run plus a fuzzer is the cheapest way to not ship it.

---

## Summary

- **A format-string bug is two primitives.** `%p` reads the stack — leaking addresses that **defeat ASLR** — and `%n` writes through a pointer argument, giving an **arbitrary write**. The fix is compile-time: never pass user data as a format, enforced by `-Werror=format-security`.
- **Heap bugs are silent.** A use-after-free returned a garbage value and a double-free exited 0 — both ran cleanly, which is why they ship.
- **AddressSanitizer catches them**, naming the free site and the allocation site, at ~2× cost — a testing tool that turns silent-and-exploitable into a stack trace.
- **AFL is unavailable; libFuzzer (in clang) replaces it.** Coverage-guided fuzzing instruments the target to keep inputs that reach new branches, learning valid structure by feedback.
- **Measured: libFuzzer + ASan found a planted out-of-bounds read at `parse_target.c:15:29` from a 13-byte input, in ~10 executions** — and fuzzing is stochastic, so the seed changes how long it takes.
- The modern loop: **warnings on, sanitizers in testing, fuzz the parsers, mitigations in production.** The first three find bugs; the fourth makes survivors expensive; and the cheapest bug to defend is the one that never shipped.

---

## Exercises

1. Write a program with `printf(argv[1])` and leak ten stack words. Find the offset at which your own input appears, and explain how you would turn that into a chosen-address read.
2. Get a `%n` write to change a variable to a chosen value, using a read-only format first and then a user-controlled one. What is the largest value you can write, and how long does it take?
3. Compile a use-after-free with and without `-fsanitize=address`. What does each do? Now add `-fsanitize=undefined` and find a bug ASan alone misses.
4. Write a small parser with a magic-byte check and fuzz it with libFuzzer. Add coverage output (`-print_pcs=1`) and watch it discover the magic byte. How many executions until it gets past the check?
5. Compare a coverage-guided run against a "dumb" random fuzzer you write in ten lines. Give both the same time budget on the same target. What is the ratio of bugs found?
6. Fuzz the same target with three different `-seed=` values and report the executions-to-first-crash for each. What does the spread tell you about "the fuzzer found nothing"?
7. Take a real small C library from GitHub, add a `LLVMFuzzerTestOneInput` for its parser, and run it for five minutes under ASan. Report what you find, responsibly.

---

*PROG 201 · Week 10 · L33 · © CSE Department*
