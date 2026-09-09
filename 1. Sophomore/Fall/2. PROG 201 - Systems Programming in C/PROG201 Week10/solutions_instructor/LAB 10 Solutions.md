# PROG 201 · Lab 10 Solutions
## Fuzzing a Parser — Instructor Only

---

**Do not distribute.** Part A turns on students finding the three bugs by fuzzing; the source-line
answers below spoil it.

**Machine these numbers came from:** clang (Ubuntu 24.04), glibc 2.39, Linux 7.0.0-30. Fuzzing is
**stochastic** — a student's execution counts will differ, sometimes by orders of magnitude, and
that variance is Q3/Q6, not an error.

> **AFL is not installed** (`apt` package unavailable to a student account) and neither is a system
> libFuzzer standalone; **clang's built-in `-fsanitize=fuzzer` is used instead**, which is
> coverage-guided in the same way AFL is. [[PROG 201 Scheduling Notes]] §20 records it. If a lab
> machine ever gets AFL, the lab is unchanged — `afl-fuzz` on the same target is the natural
> extension.

---

## The Three Planted Bugs

In `parser.c`:

| bug | line | trigger | ASan reports |
| --- | --- | --- | --- |
| **out-of-bounds read** | `return d[4 + len];` line 28 (kind=='R') | any input with `d[3]=='R'` and `len` past the end | heap-buffer-overflow, READ of size 1 |
| **buffer overflow (`memcpy`)** | `memcpy(name, d+4, len);` line 22 (tag=='C') | `d[1]=='C'` with `len` large | overflow — a WRITE past `name[16]`, or (when `d+4` runs off a heap input) a READ past the source. ASan reports whichever boundary it hits first |
| **divide-by-zero** | `return 100 / count;` line 25 (kind=='D') | `d[3]=='D'`, `d[2]==0` | UBSan: division by zero (not a memory error) |

**The div-by-zero is the "not a memory error" one in Q2** — it is caught by **UndefinedBehaviorSanitizer** (`-fsanitize=undefined`, which the Makefile includes), not ASan, and on a plain build it raises `SIGFPE` rather than corrupting anything. Students who expect all three to be ASan crashes should be pointed at the third's different nature.

libFuzzer stops at the first crash; the lab tells students to move it aside and re-run for the others. **Which bug it finds first is seed-dependent** — the OOB read is usually first because `d[3]=='R'` plus a short input is the easiest to stumble into.

---

## Reference Output

**Part A**, a representative run:

```
==ERROR: AddressSanitizer: heap-buffer-overflow ... READ of size 1
SUMMARY: AddressSanitizer: heap-buffer-overflow parser.c:28 in parse
crash-<hash>            (13 bytes: "RRRRRRRRRRRRR" + a length byte)
```

The 13-byte reproducer is `52 52 52 ... 0b` — `d[3]='R'`, and `len=d[0]='R'=0x52=82`, so `d[4+82]=d[86]` reads far past the 13-byte heap block.

**Part B(a):** with `-print_pcs=1`, dozens of `NEW` lines as coverage grows, first crash typically in **the low thousands to low millions of executions depending on seed** (with a seeded corpus, as few as ~10). Any number is fine; the point is that it is *finite and small*.

**Part B(b):** the dumb fuzzer usually finds **nothing in a minute**. The parser gates each bug behind a one-byte check (`d[3]=='R'`, `=='D'`, `d[1]=='C'`), so random input clears one check 1/256 of the time and the OOB read also needs a large `len` — the compound probability is low enough that a minute of random 40-byte inputs rarely hits it, while coverage guidance walks straight in.

**Part C:**

```
asan uaf          -> AddressSanitizer: heap-use-after-free      (exit 1)
asan double-free  -> AddressSanitizer: attempting double-free   (exit 1)
plain uaf         -> rc=5      (ran, returned a garbage byte, NO error)
plain double-free -> rc=0      (ran, exited cleanly, NO error)
```

**The two plain runs are the lab's point in Part C:** both exit as if nothing happened. A normal test suite checking the exit code or the output would pass them. That is why use-after-free and double-free ship.

**Part C, format string:**

```
./fmt 'AAAA %p %p %p %p'          -> AAAA 0x7fff... 0xffff... (nil) ...
./fmt "$(python3 -c "print('%p '*12)")"  -> ... 0x7025207025207025   (the "%p" bytes)
./fmt 'AAAAAAAA%7$n'              -> Segmentation fault (exit 139)
```

The `0x7025...` word is the input string on the stack (`%p ` = 0x25 0x70 0x20 …). The `%n` SIGSEGVs because `%7$n` writes through the `AAAAAAAA` bytes as a pointer — with a **real** leaked address there it would be an arbitrary write, not a crash.

---

## Answers

**Q1.** Type, `parser.c` line, hex of the crash input, byte count. The OOB read at line 29 from ~13 bytes is the usual first find; accept whichever the student's run produced, checked against the table.

**Q2.** All three, each with its line. The div-by-zero (`100 / count`, count==0) is **not a memory-safety error** — it is a `SIGFPE` / UBSan report. Full marks require identifying it as the odd one out.

**Q3.** A finite, small execution count and a coverage-point count. "Coverage-guided" = **the fuzzer keeps inputs that reach new branches and mutates those**, learning valid structure by feedback rather than guessing. [2] the numbers, [2] the definition.

**Q4.** The dumb fuzzer should find little or nothing in a minute. The explanation must include the **magic-byte checks** and a probability: one 1/256 gate is already a barrier to random bytes, and reaching the OOB read also needs a large `len` in the same input. Coverage guidance turns the compound-improbability search into a near-linear one. [2] the result, [2] the probability argument.

**Q5.** The four runs. **The two plain ones**: exit 5 (uaf) and exit 0 (double-free), both silent, both would pass a test suite. That is why these bugs reach production — nothing checks unless you instrument. [2] the four behaviours, [2] the "silent → ships" conclusion.

**Q6.** The leaked word that is the input (`0x7025...`), identified because it is the `%p ` bytes; `%p` defeats ASLR by disclosing a live address (L31 §5). `%n` is a **write** primitive — it stores the character count through a pointer argument the attacker controls — not an accidental crash; it SIGSEGV'd here only because the pointer was the `AAAA` bytes rather than a valid target. [2] the leak, [2] why `%n` is a deliberate write.

**Q7.** After the fix, the fuzzer no longer crashes on that bug and typically **finds one of the others faster** — with the first bug's path no longer terminating the run, coverage reaches deeper. The rule "re-fuzz after every fix" follows: fixing a shallow bug **unblocks** the fuzzer to reach code it could not before. [2] what happened, [2] the rule and why.

---

## Checkoff

- **All three bugs found by fuzzing**, each reproduced under `run_one` with its line — insist on the reproduction, not just the fuzzer's summary, because reproducing is what makes a fuzz finding actionable.
- **The dumb-vs-guided comparison** is the lab's intellectual core; make sure the student ran both and can state the probability argument.
- **The two silent plain heap runs** — have them say out loud that a test suite would have passed both.
- The extension (fuzz a real GitHub project) is genuinely valuable and genuinely sensitive: **remind them that a real finding goes to the maintainers, responsibly, and nowhere else.**

**Timing.** Setup 5, Part A 25, Part B 20, Part C 20, Part D 10 — 80 against 110, leaving generous checkoff time; fuzzing runs are fast and the discussion is where the session lives.

---

*PROG 201 · Week 10 · Lab 10 Solutions · Instructor Only · © CSE Department*
