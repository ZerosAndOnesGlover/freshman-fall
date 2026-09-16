# CS 202 · Operating Systems
## Week 12 · Lecture 1 of 3
### What We Are Protecting, and From Whom

---

**Sat:** Monday of Week 12, 09:00–09:50, VNC 101 · **Reading:** OSTEP 53–54; Saltzer & Schroeder §I · **Next:** L38, least privilege and what it costs

---

## §1 · The Question This Week Asks, Which No Other Week Asked

**Every mechanism in this course so far was designed against bad luck.** The scheduler assumed processes that want the CPU, not processes that want to *keep* it from you. The page replacement algorithm assumed programs with poor locality, not programs choosing their access pattern to evict yours. The file system assumed a power cut, which has no strategy.

**Security assumes an adversary**, and an adversary has three properties that bad luck does not:

1. **It picks the worst case**, not the average. A hash table with an expected O(1) lookup has an adversarial O(n), and the adversary will find it.
2. **It reads your source.** Every mechanism in this course is public. **The secret must be the key, never the design** — Kerckhoffs's principle, which is why this lecture tells you exactly how each defence works.
3. **It does not have to play.** The scheduler's guarantees hold for processes that call `read()`. An adversary calls `read()` with a pointer into kernel memory and sees what happens.

**So the first question is not "what mechanism?" but "what are we protecting, from whom, and what are they allowed to do?"** That is a **threat model**, and a defence without one cannot be evaluated — there is no way to say whether it works.

> **A threat model for this laptop, which is the one we will use all week:**
> **Protecting:** the integrity of the kernel, the confidentiality of other users' files, and the
> availability of the machine to the logged-in user.
> **From:** a program this user ran. It has this user's full authority, it can run for as long as it
> likes, and it has read the source of everything on the machine.
> **Not from:** anyone with physical access, anyone who is already root, and anyone who can
> re-flash the firmware. **Secure Boot is disabled on this machine and the platform is in Setup
> Mode**, so the firmware is outside the model, not inside it.

**Notice what the second line costs us.** A program you ran is not a stranger. It can already read every file you can read, delete your work, and send it anywhere. **Most of what people call "security" on a personal machine is protecting the system from the user's programs, not the user's data from them** — and the distinction is the difference between an annoyance and a disaster.

---

## §2 · The Trusted Computing Base, Counted

**The trusted computing base is everything that has to be correct for the policy to hold.** Not everything that *is* correct — everything whose failure is fatal. It is a set you want small, and it is almost always larger than people think.

On the reference machine, for the model in §1, the TCB includes:

| In the TCB | Size | Why |
|---|---|---|
| **The kernel** | **16.2 MB** compressed, plus **162 MB** of modules | it mediates every access; a bug is total |
| **Every setuid-root binary** | **18 of 2,049 binaries in `/usr/bin`, `/usr/sbin` and `/bin`** | each runs as root with input you control |
| **Every binary with file capabilities** | **4** | same, with less authority |
| **The dynamic loader and libc** | ~2 MB | they run inside every process before `main` |
| **The compiler and the toolchain** | — | it wrote the checks; Thompson's *Reflections on Trusting Trust* |
| **The firmware** | — | outside the model here, but only because we declared it so |

```bash
find /usr/bin /usr/sbin /bin -perm /6000 -type f | wc -l      # 18
getcap -r /usr/bin /usr/sbin /usr/lib                          # 4 files
```

**Eighteen.** That number is the interesting one. Each of those programs runs **as root**, with arguments, environment and input chosen by you:

```
-rwsr-xr-x root /usr/bin/chfn      -rwsr-xr-x root /usr/bin/passwd
-rwsr-xr-x root /usr/bin/chsh      -rwsr-xr-x root /usr/bin/pkexec
-rwsr-xr-x root /usr/bin/gpasswd   -rwsr-xr-x root /usr/bin/su
-rwsr-xr-x root /usr/bin/mount     -rwsr-xr-x root /usr/bin/sudo
-rwsr-xr-x root /usr/bin/newgrp    -rwsr-xr-x root /usr/bin/umount
-rwsr-xr-x root /usr/bin/fusermount3                 ... and 7 setgid
```

**`pkexec` is on that list**, and in 2022 a bug in how it handled an empty argument vector (**CVE-2021-4034, "PwnKit"**) gave a local user a root shell on essentially every Linux distribution, by way of an environment variable it re-introduced into its own memory. The bug was twelve years old. **It was not a kernel bug.** The kernel did exactly what it was told: run this program as root because the file says so.

**This is the argument for the rest of the week.** You cannot make eighteen programs correct. You can give them less authority so that their bugs matter less — which is §L38's subject.

---

## §3 · The Reference Monitor, and Where the Kernel Is One

**A reference monitor** is the piece that sits between a subject and an object and decides. Anderson's 1972 report gave it three requirements, and they are still the only checklist worth having:

| Requirement | What it means | Where the kernel manages it |
|---|---|---|
| **Complete mediation** | **every** access goes through it, with no path around | the MMU checks every load; `syscall` is the only entry |
| **Tamper-proof** | the subject cannot modify it | ring 0, and the page tables the subject cannot write |
| **Small enough to verify** | you can convince yourself it is right | **the kernel fails this one, and so does every general-purpose OS** |

**The kernel achieves the first two by hardware.** Recall Week 0: `syscall` is not a jump, it is a trap that loads a privileged entry point from an MSR that only privileged code can write. Recall Week 5: the page table's U/S bit is checked by the MMU on *every* access, not by code that might be skipped. **These are complete mediation implemented in silicon**, and they are why an operating system can enforce anything at all.

**The third requirement is where honesty is required.** The Linux kernel is tens of millions of lines. Nobody verifies it. What the industry does instead is **defence in depth**: assume the monitor has bugs, and arrange that a bug is not immediately a catastrophe. The rest of this lecture measures three of those arrangements.

> **Worth knowing what the alternative looks like.** **seL4** is a microkernel of about 10,000 lines
> with a machine-checked proof that its C implementation matches its specification. It satisfies all
> three requirements, and the price is that everything an operating system normally does — drivers,
> file systems, the network stack — lives outside it, in processes, communicating by messages. **That
> is the real trade**: not "secure versus insecure" but "small and provable versus large and fast".

---

## §4 · What One Bug Buys: Three Builds of the Same Program

Here is a bug. It is the oldest one there is.

```c
static void copy_name(const char *src)
{
	char name[16];
	strcpy(name, src);		/* no bound: this is the bug */
	printf("hello, %s\n", name);
}
```

**`strcpy` copies until it finds a zero byte.** If `src` is longer than 16 bytes, the extra bytes go past the end of `name` — into whatever the compiler put next, which on x86-64 means up the stack toward the saved return address. **Overwrite that, and `copy_name` returns to an address you chose.** That is not data corruption, it is **control of the program**.

**The same source, compiled three ways, on this machine** (`smash.c` in `lab/`, argument of 40 bytes):

| Build | What happened | Exit |
|---|---|---|
| `-D_FORTIFY_SOURCE=3` *(Ubuntu's default)* | `*** buffer overflow detected ***` | 134, `SIGABRT` |
| `-U_FORTIFY_SOURCE -fstack-protector-strong` | `*** stack smashing detected ***` | 134, `SIGABRT` |
| `-U_FORTIFY_SOURCE -fno-stack-protector` | *(silence)* — segmentation fault | 139, `SIGSEGV` |

**Three different mechanisms, and the difference between them is *when* they notice:**

- **`_FORTIFY_SOURCE` notices before the copy.** The compiler knows `name` is 16 bytes, so it turns `strcpy` into `__strcpy_chk(dst, src, 16)`, which checks the length and aborts. `readelf -sW` shows the call: the default build imports **`__strcpy_chk`**, the others import plain `strcpy`. **The copy never happens.**
- **The stack canary notices at the return.** The compiler puts a random word between the locals and the saved return address, and checks it in the epilogue. The overflow has already happened and already overwritten the return address — **but the check runs before `ret`, so control never transfers.** The canary's value comes from `%fs:0x28`, which the kernel seeds per process; you cannot predict it, and you cannot read it without already being able to read memory.
- **The third build notices nothing.** It returned to `0x4141414141414141` and died on the instruction fetch. **In this build the attacker already won**; the segfault is just what happens when the attacker is a `python3` one-liner rather than someone with a payload.

**Two details from the measurement that are worth more than the table:**

**First, the shorter overflow.** With 24 bytes instead of 40, the canary build **exited 0** and the no-canary build **segfaulted**. That looks backwards until you know what `-fstack-protector-strong` does besides adding the canary: **it re-orders the frame, putting arrays closest to the canary and everything else below.** Twenty-four bytes in the hardened build lands in the canary's padding; in the plain build it lands on the return address. **The re-ordering is doing as much work as the check.**

**Second, and this is the one to remember:** the first version of this measurement ran the fortify build against the plain build and reported that *both* printed `*** buffer overflow detected ***` — from which one would conclude the canary fires in both. **It does not. That message is fortify's; the canary's message is `*** stack smashing detected ***`.** Ubuntu turns both on by default, so a naive comparison measures fortify twice and never tests the canary at all. **The mechanism you think you are measuring is not always the one that fired**, which is this course's Habit 1 pointed at itself.

**What the toolchain does without being asked**, on this machine:

```bash
gcc -O2 -Q --help=common | grep -E 'fstack-clash|fcf-protection'
  -fcf-protection=full            # indirect-branch tracking, if the CPU has it
  -fstack-clash-protection        # [enabled]
```

and across a random sample of 300 files in `/usr/bin` (209 of them ELF):

| Hardening | Count |
|---|---|
| Non-executable stack | **209 of 209** |
| RELRO | **209 of 209** |
| Position-independent (PIE) | **202 of 209** |
| Stack canary | **190 of 209** |

**The stack is not executable anywhere.** That single change — the NX bit, Week 5's page-table permission — killed the classic "inject shellcode onto the stack and jump to it" attack outright, and is why modern exploitation reuses code that is already there (return-oriented programming) instead of supplying its own.

---

## §5 · Making the Addresses Unguessable

**Return-oriented programming needs addresses.** To reuse existing code, you must know where it is. **Address-space layout randomisation** is the answer: move everything, every run.

`aslr.c` prints the addresses of five things. **Two hundred runs:**

| What | Distinct in 200 runs | Range of page numbers |
|---|---|---|
| Code (`main`) | **200** | ~2³² |
| Global data | **200** | ~2³² (**the offset from code never changed**) |
| Heap (`malloc`) | **200** | ~2³² |
| `mmap` region | **200** | ~2³² |
| Stack | **200** | **~2²²** |

```bash
for i in $(seq 200); do ./aslr; done | sort | uniq -c | wc -l     # 200
setarch -R ./aslr                                                 # the same five addresses, every time
```

**Three things in that table matter.**

**The stack gets 22 bits, not 32.** The kernel randomises the stack with a mask of `0x3fffff` pages — about four million positions. Four million sounds like a lot until you have a service that forks a fresh worker per connection and does not re-randomise: **the attacker gets to guess repeatedly**, and 4 million guesses at a thousand a second is an afternoon. **This is why ASLR is a speed bump, not a wall** — it converts a reliable exploit into a probabilistic one.

**The code-to-globals offset never changed in 200 runs** — because they are in the same ELF image, which is relocated as a unit. **One leaked address discloses the whole image.** ASLR's entire value is destroyed by a single information leak, which is why §6 is about leaks and why `kptr_restrict` exists.

**And `setarch -R` turns it all off**, on request, for the convenience of debugging. The protection is a sysctl (`kernel.randomize_va_space = 2`) and a personality flag, both of which the program's own launcher controls.

> **We could not read the parameter.** `/proc/sys/vm/mmap_rnd_bits` is mode 0400 root: **permission
> denied for this account.** The entropies above are measured from the observed spread over 200
> runs, not read from the kernel. **When you cannot read the setting, measure the behaviour** — and
> say which you did.

---

## §6 · The Channels Nobody Declared

**Everything so far protects things the kernel knows are objects: pages, files, registers.** But a program can learn about data it cannot read, by watching something the system was never asked to protect. **Time is the classic one.**

```c
for (int i = 0; i < LEN; i++)
	if (guess[i] != secret[i])
		return 0;		/* stops at the first mismatch */
return 1;
```

**This is correct.** It returns true exactly when the strings match. **And it takes longer the more of the prefix is right**, which means the time it takes is a function of the secret — a **side channel**.

`timing.c` measures it. Eight-byte secret, 20,000 calls per measurement, minimum of several batches, pinned to one core:

| Correct prefix | Time |
|---|---|
| 0 bytes | 3.76 ns |
| 1 byte | **11.30 ns** |
| 2 bytes | 11.28 ns |
| 3 bytes | 13.79 ns |
| 4 bytes | 16.34 ns |
| 5 bytes | 18.80 ns |
| 6 bytes | 21.31 ns |
| 7 bytes | 23.81 ns |
| 8 bytes | 28.83 ns |

**Noise floor — the same guess measured ten times — 1.25 ns.** So the signal is real: **about 2.5 ns per byte, twice the noise**, and the ladder is monotone.

**Now the honest part, because this is where a lecture usually stops.** The measured leak did **not** yield the secret. The attack — try all 36 candidates at each position, keep the slowest, move on — recovers **byte 0 reliably, in three runs out of three, and then stalls**. Across those runs it got 1, 1 and 2 bytes of 8.

**Why byte 0 and not byte 1?** Look at the ladder again: **the step from 0 to 1 byte is 7.5 ns, and every step after it is 2.5 ns.** A wrong first byte exits the loop immediately with a perfectly predicted branch and costs almost nothing; getting the first byte right forces the loop to actually iterate. **That first step is a different, much larger effect than the per-byte cost**, and it is the only one this harness can pull out of the machine's drift.

**Two things had to be fixed before even that much worked**, and both are the same mistake in different clothes:

- Measuring all 36 candidates for `'a'`, then all for `'b'`, and so on, **compares numbers taken minutes apart**, and the CPU's clock drifts by more than 2.5 ns in that time. **Interleave the candidates**, round-robin.
- **The first batch after the guess changes is slow**, because the branch predictor is re-learning where the loop exits — a cost larger than the signal. **Discard it.**

**The constant-time version** — which exclusive-ORs every byte and accumulates, always doing all eight — produces **a flat ladder within noise and recovers 0 of 8**.

**The lesson is not "timing attacks work".** It is that **a side channel's exploitability is a quantitative question**, and the quantity is signal against noise at the attacker's vantage point. Ours was in-process, on a pinned core, with a perfect clock, and we got one byte. An attacker across a network has microseconds of jitter and would get none; an attacker on the *same core* with a shared cache has far better instruments than we used, which is what **Meltdown and Spectre** are — and why this machine's mitigations cost every system call in the course dearly. **`use memcmp` is still the wrong answer; `CRYPTO_memcmp` or an equivalent that always reads everything is the right one**, because the cost of being wrong is not bounded by what we could measure in a lecture.

---

## §7 · Where This Leaves Us

**We have a monitor that mediates completely and cannot be tampered with, and that nobody can verify.** Around it: compiler checks that catch the copy, canaries that catch the return, non-executable stacks that make injected code useless, randomisation that makes reused code hard to find — and channels underneath all of it that were never part of anyone's model.

**Every one of those is a mitigation, not a fix.** The bug in `copy_name` is still there in all three builds.

**So the next lecture asks the other question**: not "how do we stop the program doing damage when it goes wrong?" but **"how do we arrange that it has less damage available to do?"** That is least privilege, it is the one idea in security that scales, and on this machine it costs about **50 nanoseconds per system call**.

---

### What You Should Be Able to Do

1. **Write a threat model** for a system: what is protected, from whom, with what capabilities, and what is explicitly out of scope.
2. **List a TCB** and count it — and explain why 18 setuid binaries is a more useful number than "the kernel is trusted".
3. **State the reference monitor's three requirements**, and say which one a general-purpose kernel fails and what seL4 pays to satisfy it.
4. **Explain what a stack overflow gives an attacker**, and distinguish `_FORTIFY_SOURCE`, the stack canary, and NX by *when each one acts*.
5. **Explain why one leaked address defeats ASLR**, and why the stack's 22 bits is a different proposition from the code's 32.
6. **Recognise a side channel in ordinary correct code**, and say what would have to be true for it to be exploitable.

---

*CS 202 · Week 12 · L37 · © CSE Department*
