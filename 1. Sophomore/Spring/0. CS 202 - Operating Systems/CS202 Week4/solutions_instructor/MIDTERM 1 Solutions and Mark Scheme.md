# CS 202 · Midterm 1 · Solutions and Mark Scheme
## Instructor Only

---

**100 marks · 75 minutes · covers Weeks 0–3.**

> **Marking principle.** Where a part says *explain* or *justify*, roughly half the marks are for the
> reasoning. **A right method with an arithmetic slip earns most of the marks; a bare wrong number
> earns none.** A correct bare answer to an *explain* part earns about half.

**Every number in this scheme is computed by `solutions_instructor/midterm1_check.sh`**, which runs the course's reference scheduling simulator and `rtsim` on the paper's own inputs and asserts every hand calculation. **Run it before marking** if any course file has changed.

```
$ bash midterm1_check.sh
...
ALL CHECKS PASSED
```

---

## Q1 · The Kernel Boundary (20)

### (a) [4]

- **The low two bits of `CS`** — the current privilege level. **3** in a user program (`CS` = `0x33`). **[1 + 1]**
- **`hlt` in ring 3**: the CPU refuses it and raises **`#GP`**, general protection, entering the kernel through the IDT. **Linux sends the process `SIGSEGV`**, which by default terminates it. **[1 + 1]**

**Do not accept `SIGILL`** — the instruction is valid, merely privileged. Give 1 of the last 2 marks for "an exception" without naming `#GP` or the signal.

### (b) [5]

**Any three of [3]:** `RCX` ← return address (`RIP`); `R11` ← `RFLAGS`; `RFLAGS` masked by `IA32_FMASK` (interrupts off); CPL → 0 (kernel `CS` from `IA32_STAR`); `RIP` ← `IA32_LSTAR`.

**Does not [1]:** **switch the stack** — `RSP` is still the user's. *(Also accept: does not save the other registers.)*

**`r10` [1]:** `SYSCALL` **overwrites `rcx`** with the return address, so it cannot carry an argument.

### (c) [6]

| Buffer | `read()` calls | Time |
|---|---:|---:|
| 1 byte | 8 × 2²⁰ + 1 = **8,388,609** | × 600 ns = **5.03 s** |
| 4,096 bytes | 8 × 2²⁰ / 2¹² + 1 = 2,048 + 1 = **2,049** | × 600 ns ≈ **1.23 ms** |

**[2 + 2]** — 1 each for calls and time. **Accept 8,388,608 and 2,048** (omitting the final call) for full marks if the student states the omission; −½ each otherwise.

**`fgetc` [2]:** stdio keeps **its own buffer in user space** — typically 4,096 bytes — and calls `read` only to refill it, **so each `fgetc` returns a byte from memory without a system call**. The door is paid once per buffer, not once per byte.

### (d) [5]

**`clock_gettime` [3]:** it is served by the **vDSO** — code and data the kernel maps into every process — **so the time is read in ring 3 with no trap.** `getppid` enters the kernel through `SYSCALL`. The ~570 ns difference is the crossing.

**`ENOSYS` [2]:** **almost all of a cheap system call's cost is the entry and exit** — mode switch, register save, page-table switch and speculative-execution mitigations — **which happen whatever the call number.** The work behind the door is a few nanoseconds.

---

## Q2 · Processes and the Context Switch (20)

### (a) [4]

| Transition | Function |
|---|---|
| `UNUSED` → **`EMBRYO`** | `allocproc` |
| `EMBRYO` → **`RUNNABLE`** | `fork` |
| `RUNNABLE` → **`RUNNING`** | `scheduler` |
| `RUNNING` → `RUNNABLE` *(possibly, repeatedly)* | `yield`, on the timer |
| `RUNNING` → **`ZOMBIE`** | `exit` |
| `ZOMBIE` → **`UNUSED`** | the parent's `wait` |

**[4]:** ½ per state reached and ½ per correct function, for the five mandatory transitions, capped at 4. **`SLEEPING` is not required** — the child in the question need not block — but accept it if the student says what it sleeps on.

### (b) [5]

- **Timer interrupt [2]:** the CPU and `alltraps` pushed **all** user registers into the **trap frame** on the process's kernel stack on entry. `swtch` later saves only the kernel's callee-saved registers.
- **System call [2]:** **the same** — the system call entered through `int $64` and `alltraps` built a trap frame — **and** the kernel's `eax`, `ecx`, `edx` at the moment of the switch are **caller-saved**: whoever called `swtch` (ultimately `sched`) has already saved anything it needs from them.
- **Why only four [1]:** `swtch` is an ordinary function call, so by the calling convention it must preserve exactly the callee-saved registers.

**Accept** an answer that gives "the trap frame" for both cases, with the caller-saved explanation once, for full marks.

### (c) [6]

**Working [4]:**

- Calls: 100,000 rounds × **2** write+read pairs × 1,500 ns = **0.30 s**.
- Remainder: 0.60 − 0.30 = **0.30 s**.
- Per switch: 0.30 s ÷ 200,000 = **1.5 µs**.

**Marking:** 1 for recognising two pairs per round, 1 for the subtraction, 2 for dividing by 200,000 and the answer. **A student who divides by 100,000 rounds** (3.0 µs) has missed that a round has two switches — 2 of 4.

**Bound [2]:** **an upper bound on the switch alone.** The subtraction assumes a `write` and `read` cost the same whether or not they block and wake another process; **blocking and waking do extra work, which is charged to the switch.** Accept "overestimate" with that reason.

### (d) [5]

**787,655.** **[2]**

**Explanation [3]:** **xv6 saves no FPU state on a context switch**, so during the loop both processes' running totals live in **one x87 register** belonging to the CPU. Every one of the twenty million additions of 0.25 happens, into that one register, **so the two printed values sum to both correct answers together: 5,000,000 − 4,212,345 = 787,655.**

**Do not accept** "they share memory" or "a race on a variable" — they share no memory. 1 of 3 for "the FPU is not saved" without the sum argument.

---

## Q3 · Scheduling (20)

### (a) [6]

**FCFS:** `A 0–8, B 8–12, C 12–21, D 21–26`

| | A | B | C | D | **Average** |
|---|---:|---:|---:|---:|---:|
| Turnaround | 8 | 11 | 19 | 23 | **15.25** |
| Response | 0 | 7 | 10 | 18 | **8.75** |

**SRTF:** `A 0–1, B 1–5, D 5–10, A 10–17, C 17–26`

| | A | B | C | D | **Average** |
|---|---:|---:|---:|---:|---:|
| Turnaround | 17 | 4 | 24 | 7 | **13.0** |
| Response | 0 | 0 | 15 | 2 | **4.25** |

*(The reference simulator prints the averages to one decimal: 15.2 and 8.8, 13.0 and 4.2 — the underlying values are those above.)*

**Marking:** 1 per schedule, 1 per pair of averages, for 4; **2 more** for SRTF's preemption of A at *t* = 1 being shown. **A student who runs SJF non-preemptively** (A 0–8, B 8–12, D 12–17, C 17–26: turnaround 12.75, response 6.25) earns 3 of 6 and a comment.

### (b) [4]

- **Turnaround: higher than SRTF [2].** SRTF is optimal for average turnaround with arrivals (L07 §4); round robin interleaves the long jobs with the short ones, delaying the short ones' completion. *(Reference: 18.25.)*
- **Response: lower than FCFS [2].** Every job gets the CPU within one or two quanta of arriving, whereas FCFS makes D wait for all three earlier jobs. *(Reference: 4.5 against 8.75.)*

### (c) [5]

**Shares [3]:** total weight 1,469. **nice 0: 69.7%; nice 5: 22.8%; nice 10: 7.5%.** 1 each; accept 70 / 23 / 7 or 8.

**Own cgroup [2]:** **about half.** The scheduler divides the CPU **between the two groups first**, by their equal weights, and then among the tasks inside each group — **so the nice-10 process, alone in its group, is compared with nobody**, and its nice value no longer matters against the other two (L08 §7).

### (d) [5]

**Bound [2]:** *U* = 0.25 + 0.40 + 0.20 = **0.85**. Bound for *n* = 3: 3(2¹ᐟ³ − 1) ≈ 3 × 0.26 = **0.78**. **0.85 > 0.78, so the bound is inconclusive** — it neither proves nor disproves schedulability. **A student who concludes "not schedulable" from the bound loses both marks.**

**Response-time analysis [3]**, for the 10 ms task (lowest priority, *C* = 2), against *C* = 1 / *P* = 4 and *C* = 2 / *P* = 5:

| *R* | 2 + ⌈*R*/4⌉·1 + ⌈*R*/5⌉·2 |
|---:|---:|
| 2 | 2 + 1 + 2 = 5 |
| 5 | 2 + 2 + 2 = 6 |
| 6 | 2 + 2 + 4 = 8 |
| 8 | 2 + 2 + 4 = **8** — converged |

**8 ms ≤ 10 ms: schedulable.** The two higher-priority tasks need their own checks (1 ≤ 4; the 5 ms task: *R* = 2 + ⌈*R*/4⌉ → 3 ≤ 5), which a complete answer mentions. The reference simulation over the 20 ms hyperperiod reports **no misses**.

---

## Q4 · Synchronization (20)

### (a) [5]

**Interleaving [3]:**

| T1 | T2 | `balance` |
|---|---|---:|
| load `balance` → 100 | | 100 |
| | load `balance` → 100 | 100 |
| add 20 → 120 | | 100 |
| | add 30 → 130 | 100 |
| store 120 | | 120 |
| | store 130 | **130** |

**Final values [2]: 150** (correct), **120**, **130**. 1 for listing wrong values, 1 for including 150.

### (b) [6]

**Lock word [3]** — ½ per event after the first two, up to 3:

| Event | Word |
|---|---:|
| T1 locks: CAS 0 → 1 | **1** |
| T2 tries: CAS fails; exchanges in 2; `FUTEX_WAIT` | **2** |
| T3 tries: CAS fails; sees 2; `FUTEX_WAIT` | **2** |
| T1 unlocks: exchanges in 0, saw 2; `FUTEX_WAKE` | **0** |
| T2 acquires: wakes, exchanges in 2, saw 0 | **2** |
| T2 unlocks: exchanges in 0, saw 2; `FUTEX_WAKE` | **0** |
| T3 acquires: wakes, exchanges in 2, saw 0 | **2** |
| T3 unlocks: exchanges in 0, saw 2; `FUTEX_WAKE` | **0** |

**System calls [2]: five** — two waits (T2, T3) and three wakes (T1, T2, T3 unlocking).

**Unnecessary [1]: T3's final wake** — nobody is waiting. **The lock accepts it** because a woken thread cannot know whether others are still asleep, so it sets 2 rather than 1; **setting 1 could lose a wake-up**, and an extra wake-up only costs a system call.

### (c) [5]

- **`if` [2½]:** being signalled is not the same as running. **Between the producer's signal and the woken consumer re-acquiring the mutex, another consumer can take the item**, and the woken consumer proceeds with an empty buffer. Spurious wake-ups have the same effect.
- **One shared CV with `signal` [2½]:** a signal intended for one kind of waiter can wake the other kind. **A consumer that takes the last item signals, meaning to wake the producer, and wakes another consumer**, which finds nothing and sleeps; the producer sleeps on; **every thread ends up asleep** — a deadlock.

### (d) [4]

- **One CPU: sleep [1½].** The holder is not running while the waiter runs, so spinning cannot shorten the wait.
- **Few-nanosecond hold, holder running, 8 CPUs: spin [1½].** The lock frees within the spin, avoiding two system calls and a context switch.
- **xv6 kernel spinlock with interrupts off: spin [1].** A holder cannot be preempted on its CPU, so it is running on some CPU and will release soon — and the kernel cannot sleep in contexts that hold a spinlock anyway.

---

## Q5 · Synthesis: `procstat` (20)

**This question is marked on reasoning.** Accept any answer that is correct for xv6 and argued; the points below are what full-mark answers contain.

### (a) [5]

- **Where [2]:** in **`trap()`**, in the **timer interrupt** case, for **`myproc()`** — the process that was running when the tick arrived — before `yield`.
- **Lock [2]:** **`ptable.lock`**. `procstat` reads several fields of a `struct proc` that the scheduler and `exit` change on other CPUs under that lock.
- **Without it [1]:** an **inconsistent snapshot** — a process's state from before an `exit` and its name from after its slot was reused by `allocproc`; or a `ticks` value torn mid-update on a machine where the increment is not atomic. **Accept** "a process that no longer exists" or "fields from two different processes".

*(Incrementing `ticks` itself need not take `ptable.lock` if only its own CPU updates it and a slightly stale read is acceptable — **a student who argues this, and still takes the lock in `procstat` for the other fields, deserves full marks.**)*

### (b) [5]

- **Check [2]:** **that the whole buffer, `buf` to `buf + sizeof(struct pstat)`, lies within the calling process's user memory** — below `curproc->sz`.
- **Function [1]:** **`argptr`** (L03 §7).
- **Without it [2]:** the caller passes **a kernel address**, and the system call **writes attacker-influenced data into kernel memory** — a process's own name and state, which the caller controls through `exec` — enough to corrupt kernel structures and escalate privilege. **Accept** "overwrite kernel memory" with any concrete consequence; 1 of 2 for "crash the kernel".

### (c) [5]

- **Per process [2]:** 64 calls × 1,000 per second × 600 ns = **38.4 ms of CPU per second — 3.84%.**
- **One call [1]:** 1,000 calls × 600 ns = **0.6 ms per second.**
- **A cost of the single call [2]** — accept one argued: it **holds `ptable.lock` for all 64 copies at once**, blocking scheduling on every CPU for that time; it **copies a larger buffer** each call; it needs a **fixed maximum** in the interface; its result may be **stale for processes near the end** by the time it is read.

### (d) [5]

- **The attack [3]:** ticks are charged to **whichever process is running when the timer interrupt arrives**. A process that **runs for most of each 10 ms tick interval and then blocks or yields just before the tick** is almost never the one running at the interrupt, so it is **charged almost nothing** while using most of the CPU — **and the scheduler then favours it**, because it has the fewest ticks. *(L08 §2's gaming, against a different accounting rule.)*
- **The fix [2]** — accept any that charges actual use: **measure time on every switch** — read a high-resolution clock (`rdtsc`) in `sched`/`scheduler` and charge the elapsed interval to the outgoing process; or charge a fraction of a tick based on time since the process was scheduled.

**1 of 3** for "sleep often" without connecting it to *when* ticks are charged.

---

*CS 202 · Midterm 1 · Solutions and Mark Scheme · Instructor Only*
