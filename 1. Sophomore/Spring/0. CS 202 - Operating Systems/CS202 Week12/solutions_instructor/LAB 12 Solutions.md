# CS 202 · Lab 12 — Solutions and Running Notes
## **INSTRUCTOR ONLY** · Do not distribute

---

**Tuesday of the completion period, 15:00–16:50, BH 210.** Unmarked; attendance and check-off recorded.

**Every figure below is from the reference machine** (i5-8250U, Ubuntu 24.04.4, kernel 7.0.0-31, GCC 13.3.0). **Student numbers will differ in the third digit and should not differ in the order of magnitude.**

> **Running the session.** Part A is 45 minutes and **most students will need 55**. If you are
> behind at 15:50, **cut A5 entirely** — it is marked optional in the handout for this reason — and
> start the demos. **Part B must not be cut**: it is the last contact before Friday's deadline, and
> the students who most need it are the ones who will not come if it looks optional.

---

## Part A

### A1 · The Week 0 claim (Q1–Q3)

**Q1.** `sgdt` succeeds:

```
sgdt from user mode succeeded: GDT base 0xfffffe397b808000 limit 127
```

**It is a kernel address** — the top bits are all ones, so it is in the upper half of the 48-bit canonical space, which is the kernel's half. **A student can tell without privilege because user addresses on x86-64 are below `0x0000_8000_0000_0000`** and this is not.

**Q2. Neither mechanism is broken.** `kptr_restrict = 1` does what it says: it zeroes pointers printed **through `%pK` by the kernel**. `CONFIG_X86_UMIP=y` also does what it says: it asks the kernel to enable **User-Mode Instruction Prevention**, which is a **CPU feature this Kaby Lake R part does not have** (`umip` is absent from `/proc/cpuinfo` flags).

**The gap is between the configuration and the silicon**, and nothing reports it — no boot warning, no `dmesg` line, no failure. **This is Habit 1 in its purest form and it is the reason it opened the course.**

**Expect confusion here, and let it run.** The common wrong answer is "the kernel has a bug". Push with: *which line of kernel code is wrong?* There isn't one.

**Q3.**

```
gather_data_sampling     Vulnerable
```

**Everything else in the directory says `Mitigation:` or `Not affected`.** GDS ("Downfall") affects the gather instruction's use of the AVX register buffer. **"Vulnerable" here does not mean the kernel forgot** — it means **the microcode that provides the mitigation is not present on this machine**, and the kernel is telling the truth about it rather than staying silent. *(Note `old_microcode: Not affected`, which is about a different check; the two are not in conflict.)*

**The teaching point:** this is the *opposite* of the UMIP case. **Here the system reports the gap; there it did not.** Ask the students which they would rather have.

---

### A2 · Three ways to catch one bug (Q4–Q6)

**Q4.** With 40 bytes:

| Build | Message | Exit |
|---|---|---|
| default (`_FORTIFY_SOURCE=3`) | `*** buffer overflow detected ***: terminated` | **134** (`SIGABRT`) |
| `-fstack-protector-strong`, no fortify | `*** stack smashing detected ***: terminated` | **134** |
| neither | *(silence)* | **139** (`SIGSEGV`) |

**When each acts:**

- **fortify: before the copy.** `strcpy` became `__strcpy_chk(dst, src, 16)`, which compares the length against the known destination size and aborts. **The overflow never happens.**
- **the canary: at the return**, in the epilogue, after the overflow has already overwritten everything including the saved return address. **Control never transfers, which is the only thing that matters.**
- **neither: nothing acted.** The function returned to `0x4141414141414141` and died on the instruction fetch. **The attacker had already won**; the segfault is only because the "payload" was the letter A.

> **This is the exercise that catches instructors as well as students.** The first version of this
> lab compared the *default* build against `-fno-stack-protector` and found both printing
> **`buffer overflow detected`** — concluding, wrongly, that the canary fires in both. It does not:
> that message is **fortify's**, and Ubuntu enables fortify and the canary together, so the naive
> comparison **measures fortify twice and never tests the canary**. `-U_FORTIFY_SOURCE` is what
> makes the experiment an experiment.

**Q5.** With 24 bytes: **the canary build exits 0; the plain build segfaults.**

**`-fstack-protector-strong` re-orders the frame**, placing arrays immediately below the canary and scalars below them, so that an overflow must pass through the canary to reach anything else. Twenty-four bytes in that layout lands in padding below the canary; **in the plain build the same 24 bytes reach the saved return address.** **The re-ordering is doing as much work as the check** — say so, because students remember the canary and forget the layout.

**Q6.** `readelf -sW smash_fortify | grep chk` shows **`__strcpy_chk`**; the other two builds import plain `strcpy`. The canary build shows **`__stack_chk_fail`**, which the plain build does not.

---

### A3 · Randomisation (Q7–Q9)

**Q7.** **200 distinct values in 200 runs, for all five.**

**Q8.** **The difference between the code address and the global-data address is identical in every run** — they are in one ELF image, relocated as a unit. **One leaked address discloses the whole image**: every function, every string, every got entry, at a fixed offset from the leak. **ASLR's entire value is destroyed by a single information leak**, which is why `kptr_restrict`, `dmesg_restrict` and Yama exist and why A1's `sgdt` matters.

**Q9.** The stack spans about **4 million pages** across the 200 samples — **about 22 bits**, matching `STACK_RND_MASK` on x86-64. The other four span about **2³²**.

**For an attacker who can retry:** 4 million guesses is an afternoon at a thousand a second, **and a server that forks a worker per connection without re-execing does not re-randomise** — the child inherits the parent's layout, so every crash is another draw from the *same* distribution, or no draw at all. **ASLR converts a reliable exploit into a probabilistic one; it does not prevent one.**

**`setarch -R` exists because debugging is impossible otherwise** — a breakpoint address that changes every run, a core dump that cannot be compared with the last one. **The protection is a personality flag the launcher controls**, which is worth noticing in a week about who is allowed to decide what.

> **Do not let the sysctl question pass.** `/proc/sys/vm/mmap_rnd_bits` is **mode 0400 root**:
> permission denied for this account. **The entropy figures above are measured, not read.** Ask the
> students which of the two they would trust, and why.

---

### A4 · What a filter costs (Q10–Q12)

**Q10. The control gives about −3 ns, i.e. nothing** — two identical measurements with nothing changed between them.

**It is non-negotiable because the obvious harness is wrong in a way that looks right.** Measuring once before the filter and once after reports **1,044 ns then 868 ns** — the filter apparently making system calls **17% faster**. The cause is **CPU frequency ramp** on an idle laptop: the first loop runs at a low clock. **A plausible number from a broken harness is this course's standard failure**, and a control that must return zero is the cheapest instrument that detects it.

**Q11.**

| Filter | Cost |
|---|---|
| 1 × 15 instructions | **+51.9 ns** |
| 1 × 205 instructions | **+52.7 ns** |
| 5 × 15 instructions | **+48.9 ns** |

**The cost does not depend on the length of the filter, nor on the number of filters.** **It is the check, not the rules**: entering the seccomp path at all. The rules are JIT-compiled (`net.core.bpf_jit_enable = 1`).

**The implication: do not ration rules.** Write the policy you actually want. **Ration the *filter*, not its contents** — do not install one on a path that does not need it.

**Q12.** **159 = 128 + 31**, and **31 is `SIGSYS`**. The shell reports `Bad system call`.

**Why not `SIGKILL`:** `SIGSYS` says *the policy refused a system call*, which is a different fact from *something killed this process*. **A supervisor can report it accurately**, a core dump records `si_syscall`, and `SECCOMP_RET_TRAP` lets a handler emulate the call instead of dying. **`SIGKILL` would throw that information away.**

---

### A5 · The timing channel (Q13–Q15) — optional

**Q13.** The ladder rises monotonically, **about 2.5 ns per byte**, against a **noise floor of 1.25 ns** measured by repeating the identical measurement ten times. **The signal is real** — twice the noise.

**Q14.** **The first step is 7.5 ns; every later step is 2.5 ns.**

A wrong *first* byte exits the loop immediately, with the branch perfectly predicted and essentially no work; getting the first byte right forces the loop to iterate at all. **That is a different effect from the per-byte cost**, and it is the only one large enough to survive the machine's drift — **which is why the attack recovers byte 0 in three runs out of three and then stalls** (1, 1 and 2 bytes of 8).

**So "early-exit comparison leaks the secret" is too strong for this machine at this scale.** It leaks **one byte reliably and the rest below the noise from this vantage point**. **The honest claim is that the leak is real, and that exploitability is a quantitative question** about signal against noise where the attacker stands. An attacker sharing a core with a cache-based instrument is in a far better position than this harness.

**Q15.** The constant-time ladder is **flat within noise** and the attack recovers **0 of 8**. It costs **every comparison the full eight bytes** — in the cold-memory mode, about **600 ns against 360 ns for the fastest early exit**. **Constant time means constant at the worst case, and that is the price.**

---

## Part B · Running the demos

**Four minutes each, TA keeps time.** Post the order at the start so nobody watches the clock.

**What to look for, and what to say:**

| What you see | Say |
|---|---|
| boots, one Part D number on screen, one honest bug | **nothing — this is a complete demo**; check them off |
| boots, no measurement | **"Part D is 20 marks and it is the part with numbers."** Point at the handout |
| `symlink()` returns a plausible wrong number | **the duplicate system call number** — `grep SYS_ syscall.h \| sort -k3 -n` |
| a new call appears to do nothing at all | **the stale `usys.o`** — `objdump -d usys.o \| grep -A2 '<name>:'`, then `make clean` |
| `usertests` fails in the `sbrk` tests | `copyout` on a lazily-allocated page — **the fault handler must cover kernel access too** |
| panic at `init`, `eip 0x1010101` | **this is what the abandoned copy-on-write attempt did.** Tell them the reference hit it too and could not find it in the time available; **advise reverting to the working tree, not debugging it on Thursday** |
| does not boot, student is embarrassed | **"Good. That is what this session is for."** Then spend the four minutes on it |

**Do not let a demo become a debugging session longer than four minutes.** Note the symptom, name the likely layer, and move on — **the queue is the whole value of the session.**

**Q16 is the last thing they write this term.** Make them write it down: **one fix, and the command that proves it.** Students who leave without a next action are the ones who submit nothing.

---

## Check-Off

- **Q1, Q3, Q4, Q10, Q12** answered — five lines;
- `runs.txt`, 200 lines;
- **the demo, working or not.**

**Record attendance in [[_CS 202 Lab and Quiz Record]].** [[Year2 - Sophomore/COURSE POLICIES|COURSE POLICIES]] costs a letter grade at a second unexcused absence, **and this is the last session at which that can be incurred.**

---

*CS 202 · Week 12 · Lab 12 Solutions · Instructor Only*
